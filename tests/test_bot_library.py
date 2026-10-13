import hashlib
import importlib.util
import json
import os
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("bot_library", ROOT / "tools" / "bot_library.py")
bot = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bot)


class BotLibraryTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.store = Path(self.tmp.name)
        self.m = bot.validate_manifest(json.loads((ROOT / "bots/oci-admission-preflight.json").read_text()))
        self.run = "testrun"
        self.n = 0

    def event(self, step, action, platform, result, milestone=None):
        self.n += 1
        return {
            "schema": "broccoli.bot-action/v1",
            "bot_id": self.m["id"],
            "run_id": self.run,
            "event_id": "event_" + str(self.n),
            "timestamp": "2026-01-01T00:00:00Z",
            "platform": platform, "action": action, "step_id": step,
            "milestone_id": milestone, "result": result,
            "caused_by_request_id": None,
            "evidence_ref": None,
            "evidence_sha256": None,
            "verified_by": None
        }

    def proof(self, event):
        rel = "evidence/" + self.run + "/" + event["event_id"] + ".json"
        path = self.store / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text('{"fixture_only":true}')
        event["evidence_ref"] = rel
        event["evidence_sha256"] = hashlib.sha256(path.read_bytes()).hexdigest()
        event["verified_by"] = "independent-checker"

    def test_main_only_and_schema_boundary(self):
        modified = dict(self.m)
        modified["source_ref"] = "0123456789abcdef"
        with self.assertRaises(ValueError):
            bot.validate_manifest(modified)
        modified = dict(self.m)
        modified["contact_email"] = "not-allowed"
        with self.assertRaises(ValueError):
            bot.validate_manifest(modified)

    def test_reject_sensitive_action_payload(self):
        event = self.event("check_oci", "observe", "oci-api", "PASS")
        event["password"] = "never-store-secrets"
        with self.assertRaises(ValueError):
            bot.check_event(event, self.m, self.store)

    def test_reject_fake_verify_without_artifact(self):
        event = self.event("verify_auth", "verify", "oci-api", "PASS", "oci_authenticated")
        event["verified_by"] = "independent-checker"
        with self.assertRaises(ValueError):
            bot.record(self.m, event, self.store)

    def test_hash_chain_dedup_and_private_permissions(self):
        event = self.event("check_oci", "observe", "oci-api", "PASS")
        bot.record(self.m, event, self.store)
        path = bot.journal_path(self.store, self.m["id"], self.run)
        self.assertEqual(path.stat().st_mode & 0o777, 0o600)
        events, digest = bot.read_chain(path)
        self.assertEqual(len(events), 1)
        self.assertEqual(len(digest), 64)
        with self.assertRaises(ValueError):
            bot.record(self.m, event, self.store)
        content = path.read_text()
        path.write_text(content.replace("check_oci", "check_oci_tampered"))
        with self.assertRaises(ValueError):
            bot.read_chain(path)

    def test_proposal_requires_complete_independent_milestones(self):
        observe = self.event("check_oci", "observe", "oci-api", "PASS")
        bot.record(self.m, observe, self.store)
        first = self.event("verify_auth", "verify", "oci-api", "PASS", "oci_authenticated")
        self.proof(first)
        bot.record(self.m, first, self.store)
        with self.assertRaises(ValueError):
            bot.propose(self.m, self.run, self.store)
        second = self.event("verify_desktop", "verify", "linux-desktop", "PASS", "access_preserved")
        self.proof(second)
        bot.record(self.m, second, self.store)
        bot.propose(self.m, self.run, self.store)
        p = json.loads((self.store / "proposals" / (self.m["id"] + "-" + self.run + ".json")).read_text())
        self.assertEqual(p["status"], "REVIEW_REQUIRED")
        self.assertEqual(len(p["milestones"]), 2)
        self.assertEqual(p["source_ref"], "main")


if __name__ == "__main__":
    unittest.main()
