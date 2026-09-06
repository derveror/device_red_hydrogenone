from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BOARD_CONFIG = ROOT / "BoardConfig.mk"
BOOT_CONTRACT = ROOT / "docs/stock/h1a1000-r118/boot-image-contract.json"


class BootHeaderReleasetoolsContractTest(unittest.TestCase):
    def setUp(self) -> None:
        self.board = BOARD_CONFIG.read_text(encoding="utf-8")
        self.stock = json.loads(BOOT_CONTRACT.read_text(encoding="utf-8"))

    def test_stock_and_board_require_boot_header_v1(self) -> None:
        self.assertEqual(self.stock["header"]["header_version"], 1)
        self.assertRegex(
            self.board,
            re.compile(r"^BOARD_BOOT_HEADER_VERSION\s*:=\s*1\s*$", re.M),
        )

    def test_recovery_as_boot_forwards_header_version_to_releasetools(self) -> None:
        self.assertRegex(
            self.board,
            re.compile(r"^BOARD_USES_RECOVERY_AS_BOOT\s*:=\s*true\s*$", re.M),
        )
        self.assertRegex(
            self.board,
            re.compile(
                r"^BOARD_MKBOOTIMG_ARGS\s*\+=\s*--header_version\s+"
                r"\$\(BOARD_BOOT_HEADER_VERSION\)\s*$",
                re.M,
            ),
            "recovery-as-boot target-files must rebuild boot.img with the stock v1 header",
        )

    def test_no_conflicting_literal_header_version_is_injected(self) -> None:
        for line in self.board.splitlines():
            if "BOARD_MKBOOTIMG_ARGS" not in line or "--header_version" not in line:
                continue
            self.assertNotRegex(line, r"--header_version\s+(?:0|2|3|4)(?:\s|$)")


if __name__ == "__main__":
    unittest.main()
