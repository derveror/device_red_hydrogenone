from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "tools" / "validate_tree.py"


class TreeContractTests(unittest.TestCase):
    def test_tree_contract_validator_passes(self) -> None:
        result = subprocess.run(
            [sys.executable, str(VALIDATOR), str(ROOT)],
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("TREE CONTRACT: PASS", result.stdout)


if __name__ == "__main__":
    unittest.main()
