from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "manifests" / "README.md"
MANIFEST = ROOT / "docs" / "manifests" / "hydrogenone-lineage-22.2.xml"


class WorkspaceBootstrapDocsTest(unittest.TestCase):
    def test_bootstrap_document_and_manifest_exist(self) -> None:
        self.assertTrue(DOC.is_file(), DOC)
        self.assertTrue(MANIFEST.is_file(), MANIFEST)

    def test_bootstrap_points_to_production_manifest(self) -> None:
        text = DOC.read_text(encoding="utf-8")
        self.assertIn(
            "https://raw.githubusercontent.com/derveror/device_red_hydrogenone/"
            "lineage-22.2-stock118-rework/docs/manifests/hydrogenone-lineage-22.2.xml",
            text,
        )
        self.assertIn(".repo/local_manifests/hydrogenone.xml", text)

    def test_bootstrap_targets_lineage_22_2_and_tested_preflight(self) -> None:
        text = DOC.read_text(encoding="utf-8")
        self.assertIn("-b lineage-22.2", text)
        self.assertIn("run_m_nothing_preflight.sh --validate-only", text)
        self.assertIn("run_m_nothing_preflight.sh", text)
        self.assertIn("m nothing", text)

    def test_fresh_bootstrap_does_not_force_sync_or_skip_first_gate(self) -> None:
        text = DOC.read_text(encoding="utf-8")
        bash_blocks = re.findall(r"```bash\n(.*?)```", text, flags=re.DOTALL)
        repo_sync_blocks = [block for block in bash_blocks if re.search(r"(?m)^repo sync\b", block)]
        self.assertEqual(len(repo_sync_blocks), 1, repo_sync_blocks)
        self.assertNotIn("--force-sync", repo_sync_blocks[0])

        for later_target in ("m bootimage", "m vendorimage", "m systemimage", "m otapackage", "m bacon"):
            self.assertNotIn(later_target, text)


if __name__ == "__main__":
    unittest.main()
