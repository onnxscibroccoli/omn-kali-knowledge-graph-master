#!/usr/bin/env python3
"""Enrich discovered tools with evidence-aware quality and lineage metadata.

This layer never executes discovered tools. It combines explicit retest evidence
with deterministic path/signal heuristics. Unproven candidates remain unproven.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ARCHIVE_MARKERS = ("backup", "archive", "mirror", "legacy", "quarantine", "template")
TEST_MARKERS = ("/test/", "/tests/", "test-suite/", ".test.", "_test.", "smoke")
PURPOSE_WORDS = re.compile(r"[a-z0-9]+")
STOPWORDS = {"scripts", "script", "tools", "tool", "bin", "src", "lib", "production", "reference", "test", "tests", "sh", "py", "mjs", "js"}

def tokens(path: str) -> set[str]:
    return {x for x in PURPOSE_WORDS.findall(path.lower()) if x not in STOPWORDS}

def similarity(a: str, b: str) -> float:
    aa, bb = tokens(a), tokens(b)
    if not aa or not bb:
        return 0.0
    return len(aa & bb) / max(1, min(len(aa), len(bb)))

def infer(entry: dict) -> tuple[str, str, str]:
    path = entry["path"].lower()
    if any(marker in path for marker in ARCHIVE_MARKERS):
        return "LOW", "Historical, archived, mirrored, or template implementation.", "ARCHIVE_ONLY"
    if any(marker in path for marker in TEST_MARKERS):
        return "MEDIUM", "Supporting test or smoke verification artifact.", "SUPPORTING_TEST"
    if entry.get("kind") == "workflow":
        return "MEDIUM", "CI or orchestration workflow definition.", "SUPPORTING_TEST"
    confidence = entry.get("discovery", {}).get("confidence", "low")
    if confidence == "high":
        return "MEDIUM", "Candidate executable with strong source-discovery signals.", "RETEST_REQUIRED"
    if confidence == "medium":
        return "MEDIUM", "Candidate executable with source-discovery signals.", "RETEST_REQUIRED"
    return "LOW", "Candidate executable with weak discovery signals and no explicit proof.", "NEW_IMPLEMENTATION"

def qualify(registry: dict, evidence: dict) -> dict:
    explicit = {item["tool_id"].lower(): item for item in evidence.get("evidence", [])}
    entries = registry.get("entries", [])
    high = []
    for item in entries:
        ev = explicit.get(item["tool_id"].lower())
        if ev and ev.get("quality") == "HIGH" and ev.get("retest_status") == "PASS":
            high.append(item)

    for item in entries:
        ev = explicit.get(item["tool_id"].lower())
        if ev:
            q = {
                "quality": ev["quality"],
                "historical_proof": ev.get("historical_proof", False),
                "historical_refs": ev.get("historical_refs", []),
                "retest_status": ev.get("retest_status", "NOT_RUN"),
                "retest_refs": ev.get("retest_refs", []),
                "intended_purpose": ev["intended_purpose"],
                "lineage_relation": "none",
                "replacement_tool_id": None,
                "improvement_strategy": ev["improvement_strategy"],
                "rationale": ev.get("rationale", "")
            }
        else:
            quality, purpose, strategy = infer(item)
            q = {
                "quality": quality,
                "historical_proof": False,
                "historical_refs": [],
                "retest_status": "NOT_RUN",
                "retest_refs": [],
                "intended_purpose": purpose,
                "lineage_relation": "none",
                "replacement_tool_id": None,
                "improvement_strategy": strategy,
                "rationale": "No explicit historical or live retest evidence was supplied."
            }

        if q["quality"] == "LOW":
            candidates = [
                h for h in high
                if h["repository"] == item["repository"]
                and h["kind"] == item["kind"]
                and h["tool_id"] != item["tool_id"]
            ]
            best = max(candidates, key=lambda h: similarity(item["path"], h["path"]), default=None)
            shared = tokens(item["path"]) & tokens(best["path"]) if best else set()
            same_stem = Path(item["path"]).stem.lower() == Path(best["path"]).stem.lower() if best else False
            if best and (same_stem or len(shared) >= 2) and similarity(item["path"], best["path"]) >= 0.5:
                q["lineage_relation"] = "likely_related"
                q["replacement_tool_id"] = best["tool_id"]
                q["improvement_strategy"] = "REUSE_VALIDATED_TOOL"
                q["rationale"] = (
                    "Low-confidence candidate has a high-quality validated sibling with "
                    "meaningful path/purpose overlap. Prefer the validated implementation."
                )

        if q["retest_status"] == "PASS":
            item.setdefault("evidence", {})["status"] = "PASS"
            item["evidence"]["tests"] = q["retest_refs"]
            item["evidence"]["last_verified_at"] = evidence.get("generated_at", "")
            item["evidence"]["notes"] = q["rationale"]
        elif q["retest_status"] == "FAIL":
            item.setdefault("evidence", {})["status"] = "FAIL"
            item["evidence"]["tests"] = q["retest_refs"]
        item["qualification"] = q

    registry["qualification"] = {
        "schema_version": "omnikali.tool-qualification/v1",
        "policy": "explicit live PASS outranks historical proof; missing proof remains unproven",
        "high_quality_count": sum(1 for e in entries if e["qualification"]["quality"] == "HIGH"),
        "historical_retest_required_count": sum(1 for e in entries if e["qualification"]["quality"] == "HISTORICAL_RETEST_REQUIRED"),
        "low_quality_count": sum(1 for e in entries if e["qualification"]["quality"] == "LOW"),
        "medium_quality_count": sum(1 for e in entries if e["qualification"]["quality"] == "MEDIUM")
    }
    return registry

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("registry", type=Path)
    parser.add_argument("evidence", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    registry = json.loads(args.registry.read_text(encoding="utf-8"))
    evidence = json.loads(args.evidence.read_text(encoding="utf-8"))
    output = qualify(registry, evidence)
    args.output.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(output["qualification"], sort_keys=True))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
