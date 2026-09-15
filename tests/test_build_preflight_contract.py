from __future__ import annotations

import re
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools" / "build" / "run_m_nothing_preflight.sh"
ANDROID_PRODUCTS = ROOT / "AndroidProducts.mk"
BP1A_LUNCH = "lineage_hydrogenone-bp1a-userdebug"


class BuildPreflightContractTest(unittest.TestCase):
    def test_script_exists_and_has_valid_bash_syntax(self) -> None:
        self.assertTrue(SCRIPT.is_file(), SCRIPT)
        result = subprocess.run(["bash", "-n", str(SCRIPT)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_script_is_non_destructive_and_fails_fast(self) -> None:
        text = SCRIPT.read_text(encoding="utf-8")
        self.assertIn("set -euo pipefail", text)
        for forbidden in ("repo sync", "git reset", "git clean", "rm -rf"):
            self.assertNotIn(forbidden, text, forbidden)

    def test_script_validates_complete_workspace_and_exact_vendor_pin(self) -> None:
        text = SCRIPT.read_text(encoding="utf-8")
        for required in (
            "build/envsetup.sh",
            "device/red/hydrogenone",
            "vendor/red/hydrogenone",
            "kernel/red/msm8998",
            "device/qcom/sepolicy-legacy-um",
            "docs/reference/cross-tree-lock.json",
            "vendor_commit",
            "kernel_commit",
            "git -C",
            "status --porcelain",
            "rev-parse HEAD",
        ):
            self.assertIn(required, text, required)
        self.assertIn("kernel revision mismatch", text)

    def test_script_runs_only_the_first_real_build_gate_and_captures_it(self) -> None:
        text = SCRIPT.read_text(encoding="utf-8")
        self.assertRegex(text, r"source\s+[\"']?build/envsetup\.sh")
        self.assertIn(BP1A_LUNCH, text)
        self.assertRegex(text, r"\bm\s+nothing\b")
        self.assertIn("tee", text)
        self.assertIn("PIPESTATUS", text)
        self.assertIn("out/hydrogenone-build-logs", text)
        self.assertNotRegex(text, r"\bm\s+(?:bootimage|vendorimage|systemimage|otapackage|bacon)\b")

    def test_android15_lunch_choices_include_the_bp1a_release(self) -> None:
        text = ANDROID_PRODUCTS.read_text(encoding="utf-8")
        for variant in ("user", "userdebug", "eng"):
            self.assertIn(f"lineage_hydrogenone-bp1a-{variant}", text)
        self.assertNotRegex(text, r"lineage_hydrogenone-(?:user|userdebug|eng)(?:\s|\\|$)")

    def test_script_supports_validation_without_starting_a_build(self) -> None:
        text = SCRIPT.read_text(encoding="utf-8")
        self.assertIn("--validate-only", text)
        self.assertRegex(text, r"VALIDATE_ONLY=.*(?:false|0)")


if __name__ == "__main__":
    unittest.main()
