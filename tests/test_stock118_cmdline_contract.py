from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BOARD = ROOT / "BoardConfig.mk"
BOOT = ROOT / "docs" / "stock" / "h1a1000-r118" / "boot-image-contract.json"


class Stock118CmdlineContractTest(unittest.TestCase):
    def setUp(self) -> None:
        self.board = BOARD.read_text(encoding="utf-8")
        self.boot = json.loads(BOOT.read_text(encoding="utf-8"))

    def _board_cmdline(self) -> str:
        parts = []
        for line in self.board.splitlines():
            m = re.match(r"\s*BOARD_KERNEL_CMDLINE\s*(?::=|\+=)\s*(.*)$", line)
            if m:
                parts.extend(m.group(1).split())
        return " ".join(parts)

    def test_retains_red118_hardware_runtime_tokens(self) -> None:
        stock = set(self.boot["header"]["cmdline"].split())
        required = {
            "msm_rtb.filter=0x37",
            "sched_enable_hmp=1",
            "sched_enable_power_aware=1",
            "firmware_class.path=/vendor/firmware_mnt/image",
        }
        self.assertTrue(required <= stock, required - stock)
        active = set(self._board_cmdline().split())
        self.assertTrue(required <= active, required - active)

    def test_does_not_hardcode_stock_build_or_signing_identity(self) -> None:
        active = set(self._board_cmdline().split())
        self.assertNotIn("buildvariant=userdebug", active)
        self.assertFalse(any(x.startswith("veritykeyid=") for x in active), active)

    def test_keeps_android15_bootdevice_discovery_token(self) -> None:
        active = set(self._board_cmdline().split())
        self.assertIn("androidboot.boot_devices=soc/1da4000.ufshc", active)


if __name__ == "__main__":
    unittest.main()
