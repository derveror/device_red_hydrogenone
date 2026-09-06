from __future__ import annotations

import re
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MATRIX = ROOT / "framework_compatibility_matrix.xml"
BOARD_CONFIG = ROOT / "BoardConfig.mk"

EXPECTED_RED_PRIVATE_INSTANCES = {
    (
        "com.fingerprints.extension",
        "1.0",
        "IFingerprintSensorTest",
        "default",
    ),
    (
        "vendor.cm.hardware.thermal3d",
        "1.0",
        "IThermal3d",
        "default",
    ),
    (
        "vendor.leia.hardware.leiadisp",
        "1.0",
        "ILeiadisp",
        "default",
    ),
}

EXPECTED_MATRIX_HAL_NAMES = {
    "android.hardware.graphics.mapper",
    "com.fingerprints.extension",
    "vendor.cm.hardware.thermal3d",
    "vendor.leia.hardware.leiadisp",
}


def matrix_instances(root: ET.Element) -> set[tuple[str, str, str, str]]:
    result: set[tuple[str, str, str, str]] = set()
    for hal in root.findall("hal"):
        name = hal.findtext("name")
        version = hal.findtext("version")
        if not name or not version:
            continue
        for interface in hal.findall("interface"):
            iface = interface.findtext("name")
            if not iface:
                continue
            for instance in interface.findall("instance"):
                if instance.text:
                    result.add((name, version, iface, instance.text.strip()))
    return result


class RedPrivateVintfFcmTest(unittest.TestCase):
    def setUp(self) -> None:
        self.text = MATRIX.read_text(encoding="utf-8")
        self.root = ET.fromstring(self.text)

    def test_device_framework_matrix_is_wired_into_board_config(self) -> None:
        board = BOARD_CONFIG.read_text(encoding="utf-8")
        self.assertRegex(
            board,
            re.compile(
                r"DEVICE_FRAMEWORK_COMPATIBILITY_MATRIX_FILE\s*:=.*?"
                r"\$\(DEVICE_PATH\)/framework_compatibility_matrix\.xml",
                re.S,
            ),
        )

    def test_matrix_keeps_only_intended_device_specific_additions(self) -> None:
        self.assertEqual(self.root.tag, "compatibility-matrix")
        self.assertEqual(self.root.attrib.get("type"), "framework")
        names = {hal.findtext("name") for hal in self.root.findall("hal")}
        self.assertEqual(names, EXPECTED_MATRIX_HAL_NAMES)

    def test_red_private_manifest_instances_are_declared_exactly(self) -> None:
        instances = matrix_instances(self.root)
        self.assertTrue(
            EXPECTED_RED_PRIVATE_INSTANCES.issubset(instances),
            f"missing RED private FCM instances: {sorted(EXPECTED_RED_PRIVATE_INSTANCES - instances)}",
        )

    def test_red_private_hals_use_hwbinder_and_are_not_blanket_optional(self) -> None:
        expected_names = {item[0] for item in EXPECTED_RED_PRIVATE_INSTANCES}
        for hal in self.root.findall("hal"):
            if hal.findtext("name") not in expected_names:
                continue
            self.assertEqual(hal.attrib.get("format"), "hidl")
            self.assertNotEqual(hal.attrib.get("optional"), "true")
            self.assertEqual(hal.findtext("transport"), "hwbinder")

    def test_existing_mapper_compatibility_entry_is_preserved(self) -> None:
        mapper = next(
            hal
            for hal in self.root.findall("hal")
            if hal.findtext("name") == "android.hardware.graphics.mapper"
        )
        self.assertEqual(mapper.findtext("version"), "2.0")
        interface = mapper.find("interface")
        self.assertIsNotNone(interface)
        self.assertEqual(interface.findtext("name"), "IMapper")
        self.assertEqual(interface.findtext("instance"), "default")


if __name__ == "__main__":
    unittest.main()
