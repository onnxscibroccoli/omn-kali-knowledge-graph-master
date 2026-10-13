#!/usr/bin/env python3
"""Privacy-first, append-only task-loop evidence and reviewable bot proposals.

Usage: python3 tools/bot_library.py validate PATH
       python3 tools/bot_library.py record MANIFEST EVENT --store PRIVATE_DIR
       python3 tools/bot_library.py propose MANIFEST --run-id RUN --store PRIVATE_DIR
No network, cloud mutations, secret extraction, or automatic bot execution.
"""
import argparse
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import sys
from datetime import datetime

TAG = "broccoli.bot/v1"
EVTAG = "broccoli.bot-action/v1"
IDENT = re.compile(r"^[a-z][a-z0-9_-]{2,63}$")
HEX = re.compile(r"^[0-9a-f]{64}$")
EMAIL = re.compile(r"(?i)\\b[a-z0-9._%+-]+@[a-z0-9.-]+\\.[a-z]{2,}\\b")
PHONE = re.compile(r"(?<!\\d)(?:\\+?1[ .-]?)?\\(?[2-9]\\d{2}\\)?[ .-]?[2-9]\\d{2}[ .-]?\\d{4}(?!\\d)")
PLATFORMS = {"android-local", "android-cloud", "linux-desktop", "browser",
             "github-actions", "oci-api", "mcp", "llm"}
ACTIONS = {"observe", "plan", "authorize", "execute", "verify",
           "checkpoint", "recover", "publish"}
RESULTS = {"PASS", "FAIL", "BLOCKED", "NOT_PROVEN"}
EVENT_KEYS = {"schema", "bot_id", "run_id", "event_id", "timestamp",
              "platform", "action", "step_id", "milestone_id", "result",
              "caused_by_request_id", "evidence_ref", "evidence_sha256",
              "verified_by"}
MANIFEST_KEYS = {"schema", "id", "version", "description", "owner_repo",
                 "source_ref", "platforms", "capabilities", "preconditions",
                 "steps", "milestones", "recovery", "checkin_policy",
                 "secret_refs", "acceptance"}
PROTECTED_FIELD = re.compile(r"(?i)(token|password|private.key|credential|session.cookie|oauth.code|bearer)")
REVIEWERS = {"independent-checker", "ci", "user-acceptance"}


def canonical(data):
    return json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def fail(message):
    raise ValueError(message)


def load(path):
    with open(path, encoding="utf-8") as stream:
        return json.load(stream)


def check_public_payload(value):
    blob = canonical(value)
    if EMAIL.search(blob) or PHONE.search(blob):
        fail("Rejected: possible personal contact information")
    if "-----BEGIN" in blob or "sk-proj-" in blob or "ghp_" in blob:
        fail("Rejected: probable embedded secret")
    if isinstance(value, dict):
        for key, item in value.items():
            if PROTECTED_FIELD.search(key) and key != "secret_refs":
                fail("Rejected: sensitive field name")
            check_public_payload(item)
    elif isinstance(value, list):
        for item in value:
            check_public_payload(item)


def validate_manifest(data):
    if set(data) != MANIFEST_KEYS or data["schema"] != TAG:
        fail("Invalid manifest schema or fields")
    if not IDENT.fullmatch(data["id"]):
        fail("Invalid bot identifier")
    if data["source_ref"] != "main":
        fail("Canonical sources must be main only")
    if not isinstance(data["platforms"], list) or not data["platforms"] or not set(data["platforms"]) <= PLATFORMS:
        fail("Invalid platform capabilities")
    if not data["capabilities"] or not isinstance(data["capabilities"], list):
        fail("Capabilities required")
    if not isinstance(data["steps"], list) or not data["steps"]:
        fail("Typed steps required")
    ids = []
    for step in data["steps"]:
        if set(step) != {"id", "platform", "action", "capability", "expected_postcondition", "risk"}:
            fail("Unexpected or missing step fields")
        if not IDENT.fullmatch(step["id"]) or step["platform"] not in data["platforms"]:
            fail("Invalid step target")
        if step["action"] not in ACTIONS or step["capability"] not in data["capabilities"]:
            fail("Unknown action/capability")
        if step["risk"] not in {"read-only", "reversible", "sensitive", "privileged"}:
            fail("Invalid risk classification")
        ids.append(step["id"])
    if len(set(ids)) != len(ids):
        fail("Duplicate step identifier")
    mids = []
    for checkpoint in data["milestones"]:
        if set(checkpoint) != {"id", "after_step", "requires_human", "acceptance_gate"}:
            fail("Invalid milestone fields")
        if not IDENT.fullmatch(checkpoint["id"]) or checkpoint["after_step"] not in ids:
            fail("Invalid milestone")
        if not isinstance(checkpoint["requires_human"], bool):
            fail("Human checkpoint flag required")
        mids.append(checkpoint["id"])
    if not mids or len(mids) != len(set(mids)):
        fail("At least one distinct milestone required")
    if set(data["checkin_policy"]) != {"mode", "on_failure", "on_sensitive", "on_completion"}:
        fail("Checkin policy required")
    if data["checkin_policy"]["mode"] != "milestone":
        fail("Continuous unsolicited supervision is not a reproducible bot policy")
    if data["checkin_policy"]["on_failure"] != "pause" or data["checkin_policy"]["on_sensitive"] != "user_approval":
        fail("Fail-closed milestone checkpoints required")
    if not isinstance(data["secret_refs"], list):
        fail("Use secret references only")
    for ref in data["secret_refs"]:
        if not re.fullmatch(r"(?:env|vault|keyring):[A-Z][A-Z0-9_]{2,63}", ref):
            fail("Secrets must be references, not embedded values")
    check_public_payload(data)
    return data


def verify_evidence(event, store):
    if event["result"] != "PASS" or event["action"] != "verify":
        return
    if event["verified_by"] not in REVIEWERS:
        fail("PASS requires independent verification")
    rel = event.get("evidence_ref", "")
    digest = event.get("evidence_sha256", "")
    if not rel.startswith("evidence/") or ".." in Path(rel).parts or not HEX.fullmatch(digest):
        fail("PASS requires private evidence artifact with digest")
    target = (store / rel).resolve()
    if not target.is_relative_to((store / "evidence").resolve()):
        fail("Evidence must remain in private store")
    if not target.is_file() or hashlib.sha256(target.read_bytes()).hexdigest() != digest:
        fail("Evidence absent or changed")


def check_event(event, manifest, store):
    if not isinstance(event, dict) or set(event) != EVENT_KEYS or event["schema"] != EVTAG:
        fail("Unexpected event fields (raw actions or secrets cannot be logged)")
    if event["bot_id"] != manifest["id"]:
        fail("Wrong bot")
    for field in ("run_id", "event_id", "step_id"):
        if not IDENT.fullmatch(event[field]):
            fail("Invalid event identity")
    if event["step_id"] not in {s["id"] for s in manifest["steps"]}:
        fail("Unknown step")
    if event["milestone_id"] is not None and event["milestone_id"] not in {m["id"] for m in manifest["milestones"]}:
        fail("Unknown milestone")
    if event["platform"] not in manifest["platforms"] or event["action"] not in ACTIONS or event["result"] not in RESULTS:
        fail("Unknown execution boundary")
    if event["caused_by_request_id"] is not None and not IDENT.fullmatch(event["caused_by_request_id"]):
        fail("Invalid causality tag")
    datetime.fromisoformat(event["timestamp"].replace("Z", "+00:00"))
    check_public_payload(event)
    verify_evidence(event, store)


def journal_path(store, bot_id, run_id):
    return store / "runs" / bot_id / (run_id + ".jsonl")


def read_chain(file):
    events = []
    previous = "0" * 64
    if not file.exists():
        return events, previous
    for line in file.read_text(encoding="utf-8").splitlines():
        entry = json.loads(line)
        if set(entry) != {"previous_hash", "hash", "event"} or entry["previous_hash"] != previous:
            fail("Broken journal chain")
        digest = hashlib.sha256((previous + canonical(entry["event"])).encode()).hexdigest()
        if digest != entry["hash"]:
            fail("Journal integrity check failed")
        previous = digest
        events.append(entry["event"])
    return events, previous


def record(manifest, event, store):
    check_event(event, manifest, store)
    path = journal_path(store, event["bot_id"], event["run_id"])
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    fd = os.open(path, os.O_CREAT | os.O_RDWR, 0o600)
    with os.fdopen(fd, "r+", encoding="utf-8") as handle:
        fcntl.flock(handle, fcntl.LOCK_EX)
        existing, prev = read_chain(path)
        if any(x["event_id"] == event["event_id"] for x in existing):
            fail("Duplicate event: no replay")
        stamp = hashlib.sha256((prev + canonical(event)).encode()).hexdigest()
        handle.seek(0, os.SEEK_END)
        handle.write(canonical({"previous_hash": prev, "hash": stamp, "event": event}) + "\n")
        handle.flush()
        os.fsync(handle.fileno())
    print("EVENT_RECORDED=YES")
    print("JOURNAL_PRIVACY=PRIVATE_LOCAL_ONLY")


def propose(manifest, run_id, store):
    path = journal_path(store, manifest["id"], run_id)
    events, last = read_chain(path)
    milestones = {m["id"] for m in manifest["milestones"]}
    passed = set()
    for event in events:
        check_event(event, manifest, store)
        if event["action"] == "verify" and event["result"] == "PASS" and event["milestone_id"]:
            passed.add(event["milestone_id"])
    if not events or passed != milestones:
        fail("Cannot promote: independent acceptance evidence missing")
    if any(e["result"] in ("FAIL", "BLOCKED") for e in events):
        fail("Cannot promote a failed run without an explicitly verified recovery run")
    output = {"schema": "broccoli.bot-proposal/v1", "bot_id": manifest["id"],
              "version": manifest["version"], "run_id": run_id,
              "platforms": manifest["platforms"], "milestones": sorted(passed),
              "journal_hash": last, "status": "REVIEW_REQUIRED",
              "source_ref": "main"}
    root = store / "proposals"
    root.mkdir(parents=True, exist_ok=True, mode=0o700)
    target = root / (manifest["id"] + "-" + run_id + ".json")
    with os.fdopen(os.open(target, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600), "w") as file:
        json.dump(output, file, indent=2)
        file.write("\n")
    print("BOT_PROPOSAL=REVIEW_REQUIRED")
    print("PUBLICATION=NOT_AUTOMATIC")


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("command", choices=["validate", "record", "propose"])
    p.add_argument("manifest", type=Path)
    p.add_argument("event", nargs="?", type=Path)
    p.add_argument("--store", type=Path)
    p.add_argument("--run-id")
    args = p.parse_args()
    data = validate_manifest(load(args.manifest))
    if args.command == "validate":
        print("MANIFEST=VALID")
    elif args.store is None:
        fail("Private --store required")
    elif args.command == "record":
        if args.event is None:
            fail("Event file required")
        record(data, load(args.event), args.store.resolve())
    else:
        if not args.run_id or not IDENT.fullmatch(args.run_id):
            fail("Run ID required")
        propose(data, args.run_id, args.store.resolve())


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, KeyError, TypeError) as e:
        print("BOT_LIBRARY_BLOCKED=" + str(e), file=sys.stderr)
        sys.exit(2)
