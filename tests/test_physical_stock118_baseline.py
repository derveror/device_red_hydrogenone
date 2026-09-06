from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "tools" / "verify_stock118_device_baseline.py"
BOOT_CONTRACT = ROOT / "docs" / "stock" / "h1a1000-r118" / "boot-image-contract.json"
DOC = ROOT / "docs" / "PHYSICAL_BRINGUP_BASELINE.md"

STOCK118 = {
    "fingerprint": "RED/HydrogenONE/HydrogenONE:9/PKQ1.190118.001/118:userdebug/release-keys",
    "incremental": "118",
    "release": "9",
    "sdk": "28",
}
STOCK109 = {
    "fingerprint": "RED/HydrogenONE/HydrogenONE:8.1.0/H1A1000.010ho.01.01.01r.109/109:user/release-keys",
    "incremental": "109",
    "release": "8.1.0",
    "sdk": "27",
}


def run_checker(values: dict[str, str]) -> subprocess.CompletedProcess[str]:
    cmd = [sys.executable, str(CHECKER)]
    for key in ("fingerprint", "incremental", "release", "sdk"):
        cmd.extend([f"--{key}", values[key]])
    return subprocess.run(cmd, text=True, capture_output=True, check=False)


class PhysicalStock118BaselineTest(unittest.TestCase):
    def test_canonical_stock118_is_accepted(self) -> None:
        result = run_checker(STOCK118)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("STOCK118_BASELINE=PASS", result.stdout)

    def test_verizon_stock109_is_rejected(self) -> None:
        result = run_checker(STOCK109)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("STOCK118_BASELINE=FAIL", result.stdout)
        self.assertIn("baseline mismatch", result.stdout)

    def test_stock118_boot_contract_is_header_v1(self) -> None:
        contract = json.loads(BOOT_CONTRACT.read_text(encoding="utf-8"))
        self.assertEqual(contract["header"]["header_version"], 1)
        self.assertEqual(contract["build_properties"]["ro.build.version.release"], "9")
        self.assertEqual(contract["build_properties"]["ro.build.version.sdk"], "28")

    def test_physical_bringup_doc_blocks_109_baseline(self) -> None:
        text = DOC.read_text(encoding="utf-8")
        self.assertIn("H1A1000.082ho.01.00.10r.118", text)
        self.assertIn("H1A1000.010ho.01.01.01r.109", text)
        self.assertIn("must not", text.lower())


if __name__ == "__main__":
    unittest.main()
