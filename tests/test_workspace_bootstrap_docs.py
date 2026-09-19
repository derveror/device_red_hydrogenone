from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "manifests" / "README.md"
MANIFEST = ROOT / "docs" / "manifests" / "hydrogenone-lineage-22.2.xml"
BP1A_LUNCH = "lineage_hydrogenone-bp1a-userdebug"


class WorkspaceBootstrapDocsTest(unittest.TestCase):
    def test_bootstrap_document_and_manifest_exist(self) -> None:
        self.assertTrue(DOC.is_file(), DOC)
        self.assertTrue(MANIFEST.is_file(), MANIFEST)

    def test_bootstrap_points_to_production_manifest(self) -> None:
        text = DOC.read_text(encoding="utf-8")
        self.assertIn(
            "https://raw.githubusercontent.com/derveror/device_red_hydrogenone/"
            "118-lineage-22.2-kernel-302/docs/manifests/hydrogenone-lineage-22.2.xml",
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

    def test_all_markdown_build_commands_pin_bp1a(self) -> None:
        invalid_commands: list[str] = []
        generic_mentions: list[str] = []
        command_pattern = re.compile(r"(?m)^\s*lunch\s+(lineage_hydrogenone\S+)\s*$")

        for document in sorted(ROOT.rglob("*.md")):
            text = document.read_text(encoding="utf-8")
            relative = document.relative_to(ROOT)
            for target in command_pattern.findall(text):
                if target != BP1A_LUNCH:
                    invalid_commands.append(f"{relative}: {target}")
            if "lineage_hydrogenone-userdebug" in text:
                generic_mentions.append(str(relative))

        self.assertEqual(invalid_commands, [])
        self.assertEqual(generic_mentions, [])

    def test_primary_build_docs_explain_the_spl_guard(self) -> None:
        for relative in ("BUILD_FIRST.md", "README.md"):
            text = (ROOT / relative).read_text(encoding="utf-8")
            self.assertIn(BP1A_LUNCH, text, relative)
            self.assertIn("2026-09-01", text, relative)
            self.assertIn("2025-01-05", text, relative)
            self.assertIn("SPL downgrade", text, relative)


if __name__ == "__main__":
    unittest.main()
