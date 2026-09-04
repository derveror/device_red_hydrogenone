from __future__ import annotations

import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "manifest.xml"

EXPECTED_SOURCE_FQINSTANCES = {
    "android.hardware.audio@6.0::IDevicesFactory/default",
    "android.hardware.audio.effect@6.0::IEffectsFactory/default",
    "android.hardware.bluetooth.audio@2.1::IBluetoothAudioProvidersFactory/default",
    "android.hardware.camera.provider@2.4::ICameraProvider/legacy/0",
    "android.hardware.gatekeeper@1.0::IGatekeeper/default",
    "android.hardware.gnss@1.0::IGnss/default",
    "android.hardware.graphics.allocator@2.0::IAllocator/default",
    "android.hardware.graphics.composer@2.1::IComposer/default",
    "android.hardware.graphics.mapper@2.1::IMapper/default",
    "android.hardware.keymaster@3.0::IKeymasterDevice/default",
    "android.hardware.media.omx@1.0::IOmx/default",
    "android.hardware.media.omx@1.0::IOmxStore/default",
    "android.hardware.nfc@1.2::INfc/default",
    "android.hardware.sensors@1.0::ISensors/default",
    "android.hardware.soundtrigger@2.2::ISoundTriggerHw/default",
}

# These are supplied by vendor/red/hydrogenone VINTF fragments and therefore
# must not be duplicated in device/red/hydrogenone/manifest.xml.
PROPRIETARY_HAL_NAMES = {
    "android.hardware.biometrics.fingerprint",
    "android.hardware.bluetooth",
    "android.hardware.radio",
    "android.hardware.radio.config",
    "android.hardware.secure_element",
    "com.fingerprints.extension",
    "com.qualcomm.qti.ant",
    "com.qualcomm.qti.wifidisplayhal",
    "vendor.cm.hardware.thermal3d",
    "vendor.leia.hardware.leiadisp",
    "vendor.qti.esepowermanager",
    "vendor.qti.hardware.fm",
    "vendor.qti.hardware.radio.am",
    "vendor.qti.hardware.radio.ims",
    "vendor.qti.hardware.radio.lpa",
    "vendor.qti.hardware.radio.qcrilhook",
    "vendor.qti.hardware.radio.qtiradio",
    "vendor.qti.hardware.radio.uim",
    "vendor.qti.hardware.radio.uim_remote_client",
    "vendor.qti.hardware.radio.uim_remote_server",
}

# The cheryl-compatible QTI GNSS 1.0 source service and the Lineage media OMX
# source service have no proprietary VINTF fragments; their default instances
# are therefore owned by the device manifest above.
SELF_FRAGMENTED_SOURCE_HAL_NAMES: set[str] = set()


def normalized_instances(root: ET.Element) -> set[str]:
    result: set[str] = set()
    for hal in root.findall("hal"):
        name = hal.findtext("name")
        if not name:
            continue
        explicit = [node.text.strip() for node in hal.findall("fqname") if node.text]
        for fqname in explicit:
            result.add(f"{name}{fqname}")
        version = hal.findtext("version")
        if version:
            for interface in hal.findall("interface"):
                iface = interface.findtext("name")
                if not iface:
                    continue
                for instance in interface.findall("instance"):
                    if instance.text:
                        result.add(f"{name}@{version}::{iface}/{instance.text.strip()}")
    return result


class Android15ManifestContractTest(unittest.TestCase):
    def setUp(self) -> None:
        self.text = MANIFEST.read_text(encoding="utf-8")
        self.root = ET.fromstring(self.text)

    def test_manifest_is_android15_device_contract_not_legacy_placeholder(self) -> None:
        self.assertEqual(self.root.tag, "manifest")
        self.assertEqual(self.root.attrib.get("type"), "device")
        self.assertEqual(self.root.attrib.get("target-level"), "5")
        self.assertNotIn(".109", self.text)
        self.assertNotIn("future vendor tree", self.text)

    def test_expected_source_owned_instances_are_declared_exactly(self) -> None:
        instances = normalized_instances(self.root)
        self.assertEqual(instances, EXPECTED_SOURCE_FQINSTANCES)

    def test_proprietary_and_self_fragmented_hals_are_not_duplicated(self) -> None:
        names = {hal.findtext("name") for hal in self.root.findall("hal")}
        conflicts = sorted((PROPRIETARY_HAL_NAMES | SELF_FRAGMENTED_SOURCE_HAL_NAMES) & names)
        self.assertEqual(conflicts, [], f"duplicate VINTF ownership in device manifest: {conflicts}")

    def test_mapper_keeps_required_passthrough_architecture(self) -> None:
        mapper = next(
            hal
            for hal in self.root.findall("hal")
            if hal.findtext("name") == "android.hardware.graphics.mapper"
        )
        transport = mapper.find("transport")
        self.assertIsNotNone(transport)
        self.assertEqual(transport.text, "passthrough")
        self.assertEqual(transport.attrib.get("arch"), "32+64")


if __name__ == "__main__":
    unittest.main()
