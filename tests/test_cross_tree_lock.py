from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOCK = ROOT / "docs" / "reference" / "cross-tree-lock.json"
EVIDENCE = ROOT / "docs" / "stock" / "h1a1000-r118" / "cross-tree-copy-contract.json"
WORKFLOW = ROOT / ".github" / "workflows" / "verify-analysis.yml"


class CrossTreeLockContractTest(unittest.TestCase):
    def setUp(self) -> None:
        self.lock = json.loads(LOCK.read_text(encoding="utf-8"))
        self.evidence = json.loads(EVIDENCE.read_text(encoding="utf-8"))
        self.workflow = WORKFLOW.read_text(encoding="utf-8")

    def test_lock_matches_published_zero_collision_evidence(self) -> None:
        self.assertEqual(self.evidence["schema_version"], 2)
        self.assertEqual(self.evidence["status"], "zero_expanded_copy_destination_collisions")
        self.assertEqual(self.evidence["copy_destination_collisions"], [])
        authority = self.evidence["authority"]
        self.assertEqual(authority["vendor_commit"], self.lock["vendor_commit"])
        self.assertEqual(authority["stock_build"], self.lock["stock_build"])
        self.assertEqual(authority["stock_archive_sha256"], self.lock["stock_archive_sha256"])
        self.assertEqual(authority["device_branch"], self.lock["device_branch"])

    def test_lock_pins_exact_vendor_repository_and_commit(self) -> None:
        self.assertEqual(self.lock["schema_version"], 1)
        self.assertEqual(self.lock["vendor_repository"], "derveror/proprietary_vendor_red_hydrogenone")
        self.assertRegex(self.lock["vendor_commit"], r"^[0-9a-f]{40}$")
        self.assertEqual(self.lock["device_branch"], "codex/lineage-22.2-bringup-audit")

    def test_permanent_ci_rechecks_pinned_vendor_tree(self) -> None:
        commit = re.escape(self.lock["vendor_commit"])
        self.assertRegex(self.workflow, rf"(?m)^\s*ref:\s*{commit}\s*$")
        self.assertIn("tools/analysis/cross_tree_contract.py", self.workflow)
        self.assertIn("copy_destination_collisions", self.workflow)
        self.assertIn("cross-tree-lock.json", self.workflow)


if __name__ == "__main__":
    unittest.main()
