from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RECOVERY_INIT = ROOT / "rootdir/etc/init.recovery.qcom.rc"


def parse_actions(text: str) -> list[tuple[str, list[str]]]:
    actions: list[tuple[str, list[str]]] = []
    trigger: str | None = None
    commands: list[str] = []

    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if raw_line == raw_line.lstrip() and line.startswith("on "):
            if trigger is not None:
                actions.append((trigger, commands))
            trigger = line[3:]
            commands = []
        elif trigger is not None:
            commands.append(line)

    if trigger is not None:
        actions.append((trigger, commands))
    return actions


class RecoveryInitOrderTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.actions = parse_actions(RECOVERY_INIT.read_text(encoding="utf-8"))

    def triggers_containing(self, command: str) -> list[str]:
        return [trigger for trigger, commands in self.actions if command in commands]

    def test_ufs_wait_runs_during_fs_after_ueventd_is_available(self) -> None:
        self.assertEqual(
            self.triggers_containing("wait /dev/block/platform/soc/1da4000.ufshc"),
            ["fs"],
        )

    def test_recovery_usb_properties_are_set_during_init(self) -> None:
        self.assertEqual(
            self.triggers_containing("setprop sys.usb.controller a800000.dwc3"),
            ["init"],
        )
        self.assertEqual(
            self.triggers_containing("setprop sys.usb.configfs 1"),
            ["init"],
        )


if __name__ == "__main__":
    unittest.main()
