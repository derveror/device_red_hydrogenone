from __future__ import annotations

import re
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEVICE_MK = ROOT / "device.mk"
VENDOR_PROP = ROOT / "vendor.prop"
SYSTEM_EXT_PROP = ROOT / "system_ext.prop"
BOARD_CONFIG = ROOT / "BoardConfig.mk"
DEVICE_MANIFEST = ROOT / "manifest.xml"
INIT_TARGET_RC = ROOT / "rootdir/etc/init/hw/init.target.rc"


class RadioDataPlaneRuntimeContractTest(unittest.TestCase):
    def test_post_fs_starts_ipa_gsi_firmware_after_qseecom(self) -> None:
        text = INIT_TARGET_RC.read_text(encoding="utf-8")
        match = re.search(r"(?ms)^on post-fs\n(?P<body>.*?)(?=^\S|\Z)", text)
        self.assertIsNotNone(match, "init.target.rc must define a post-fs action")

        commands = [
            line.strip()
            for line in match.group("body").splitlines()
            if line.strip() and not line.lstrip().startswith("#")
        ]
        self.assertIn("write /dev/ipa 1", commands)
        self.assertLess(
            commands.index("wait_for_prop vendor.sys.listeners.registered true"),
            commands.index("write /dev/ipa 1"),
        )

    def test_red118_dsds_defaults_to_lte_capable_mode(self) -> None:
        text = VENDOR_PROP.read_text(encoding="utf-8")
        self.assertRegex(text, r"(?m)^ro\.telephony\.default_network=22,22$")

    def test_fp3_data_plane_is_enabled(self) -> None:
        text = VENDOR_PROP.read_text(encoding="utf-8")
        self.assertRegex(text, r"(?m)^persist\.vendor\.dpmhalservice\.enable=1$")
        self.assertRegex(text, r"(?m)^persist\.vendor\.data\.mode=concurrent$")
        self.assertRegex(text, r"(?m)^ro\.vendor\.use_data_netmgrd=true$")

    def test_matching_fp3_dpm_framework_is_enabled(self) -> None:
        properties = SYSTEM_EXT_PROP.read_text(encoding="utf-8")
        self.assertRegex(properties, r"(?m)^persist\.vendor\.dpm\.feature=11$")
        board = BOARD_CONFIG.read_text(encoding="utf-8")
        self.assertRegex(
            board,
            r"(?m)^TARGET_SYSTEM_EXT_PROP \+= \$\(DEVICE_PATH\)/system_ext\.prop$",
        )

    def test_ipa_configuration_manager_is_packaged(self) -> None:
        text = DEVICE_MK.read_text(encoding="utf-8")
        for package in ("ipacm", "IPACM_cfg.xml"):
            self.assertRegex(text, rf"(?m)^\s*{re.escape(package)}(?:\s*\\)?$")

    def test_dpm_qmi_service_is_declared_in_vintf(self) -> None:
        root = ET.parse(DEVICE_MANIFEST).getroot()
        instances = {
            (
                hal.findtext("name"),
                hal.findtext("version"),
                interface.findtext("name"),
                interface.findtext("instance"),
            )
            for hal in root.findall("hal")
            for interface in hal.findall("interface")
        }
        self.assertIn(
            (
                "com.qualcomm.qti.dpm.api",
                "1.0",
                "IdpmQmi",
                "dpmQmiService",
            ),
            instances,
        )


if __name__ == "__main__":
    unittest.main()
