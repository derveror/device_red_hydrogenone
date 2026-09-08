from __future__ import annotations

import re
import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools" / "build" / "run_m_nothing_preflight.sh"


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
            "kernel/essential/msm8998",
            "device/qcom/sepolicy-legacy-um",
            "docs/reference/cross-tree-lock.json",
            "vendor_commit",
            "git -C",
            "status --porcelain",
            "rev-parse HEAD",
        ):
            self.assertIn(required, text, required)

    def test_script_runs_only_the_first_real_build_gate_and_captures_it(self) -> None:
        text = SCRIPT.read_text(encoding="utf-8")
        self.assertRegex(text, r"source\s+[\"']?build/envsetup\.sh")
        self.assertRegex(text, r"\bm\s+nothing\b")
        self.assertIn("tee", text)
        self.assertIn("PIPESTATUS", text)
        self.assertIn("out/hydrogenone-build-logs", text)
        self.assertNotRegex(text, r"\bm\s+(?:bootimage|vendorimage|systemimage|otapackage|bacon)\b")

    def test_script_supports_validation_without_starting_a_build(self) -> None:
        text = SCRIPT.read_text(encoding="utf-8")
        self.assertIn("--validate-only", text)
        self.assertRegex(text, r"VALIDATE_ONLY=.*(?:false|0)")

    def test_default_lunch_selects_bp1a_and_records_success(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            top = Path(directory)
            (top / ".repo").mkdir()
            (top / "build").mkdir()
            (top / "build/envsetup.sh").write_text(
                'lunch() { [[ "$1" == "lineage_hydrogenone-bp1a-userdebug" ]]; }\n'
                'm() { [[ "$1" == "nothing" ]] && echo BUILD_GATE_REACHED; }\n'
            )
            projects = ["vendor/red/hydrogenone", "device/red/hydrogenone",
                        "kernel/essential/msm8998", "device/qcom/sepolicy-legacy-um"]
            for relative in projects:
                project = top / relative
                project.mkdir(parents=True)
                subprocess.run(["git", "init", "-q", str(project)], check=True)
                if relative == "device/red/hydrogenone":
                    lock = project / "docs/reference/cross-tree-lock.json"
                    lock.parent.mkdir(parents=True)
                    vendor_sha = subprocess.check_output(
                        ["git", "-C", str(top / projects[0]), "rev-parse", "HEAD"], text=True).strip()
                    lock.write_text(json.dumps({"vendor_commit": vendor_sha}))
                    subprocess.run(["git", "-C", str(project), "add", "."], check=True)
                subprocess.run(["git", "-C", str(project), "-c", "user.name=Test",
                                "-c", "user.email=test@example.invalid", "commit", "-q",
                                "--allow-empty", "-m", "fixture"], check=True)
            env = dict(os.environ)
            env.pop("HYDROGENONE_LUNCH_TARGET", None)
            env.pop("HYDROGENONE_LOG_DIR", None)
            result = subprocess.run(["bash", str(SCRIPT), "--top", str(top)],
                                    env=env, capture_output=True, text=True, timeout=20)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("BUILD_GATE_REACHED", result.stdout)
            self.assertEqual(next((top / "out/hydrogenone-build-logs").glob("*.status")).read_text(), "0\n")


if __name__ == "__main__":
    unittest.main()
