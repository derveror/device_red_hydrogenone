from __future__ import annotations

import json
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

# Clean-checkout contract for the active LineageOS 22.2 bring-up.
ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "docs" / "manifests" / "hydrogenone-lineage-22.2.xml"
LOCK = ROOT / "docs" / "reference" / "cross-tree-lock.json"
DEPENDENCIES = ROOT / "lineage.dependencies"


class LocalManifestContractTest(unittest.TestCase):
    def test_manifest_exists_and_is_well_formed(self) -> None:
        self.assertTrue(MANIFEST.is_file(), MANIFEST)
        root = ET.parse(MANIFEST).getroot()
        self.assertEqual(root.tag, "manifest")

    def test_manifest_has_exact_project_paths_and_revisions(self) -> None:
        root = ET.parse(MANIFEST).getroot()
        lock = json.loads(LOCK.read_text(encoding="utf-8"))
        projects = {node.attrib["path"]: node.attrib for node in root.findall("project")}

        expected = {
            "device/red/hydrogenone": {
                "name": "device_red_hydrogenone",
                "remote": "derveror",
                "revision": "lineage-22.2-stock118-rework",
            },
            "vendor/red/hydrogenone": {
                "name": "proprietary_vendor_red_hydrogenone",
                "remote": "derveror",
                "revision": lock["vendor_commit"],
            },
            "kernel/essential/msm8998": {
                "name": "android_kernel_essential_msm8998",
                "remote": "lineageos",
                "revision": "lineage-22.2",
            },
            "device/qcom/sepolicy-legacy-um": {
                "name": "android_device_qcom_sepolicy_vndr",
                "remote": "lineageos",
                "revision": "lineage-22.2-legacy-um",
            },
        }
        self.assertEqual(set(projects), set(expected))
        for path, wanted in expected.items():
            for key, value in wanted.items():
                self.assertEqual(projects[path].get(key), value, (path, key))

    def test_manifest_defines_explicit_github_remotes(self) -> None:
        root = ET.parse(MANIFEST).getroot()
        remotes = {node.attrib["name"]: node.attrib for node in root.findall("remote")}
        self.assertEqual(remotes["derveror"].get("fetch"), "https://github.com/derveror/")
        self.assertEqual(remotes["lineageos"].get("fetch"), "https://github.com/LineageOS/")

    def test_manifest_never_adds_red_common_trees(self) -> None:
        text = MANIFEST.read_text(encoding="utf-8")
        self.assertNotIn("device/red/msm8998-common", text)
        self.assertNotIn("vendor/red/msm8998-common", text)

    def test_lineage_dependencies_pin_lineage_owned_branches(self) -> None:
        dependencies = json.loads(DEPENDENCIES.read_text(encoding="utf-8"))
        by_path = {entry["target_path"]: entry for entry in dependencies}
        self.assertEqual(by_path["kernel/essential/msm8998"].get("branch"), "lineage-22.2")
        self.assertEqual(by_path["device/qcom/sepolicy-legacy-um"].get("branch"), "lineage-22.2-legacy-um")

    def test_custom_vendor_is_not_misdeclared_as_lineage_dependency(self) -> None:
        dependencies = json.loads(DEPENDENCIES.read_text(encoding="utf-8"))
        repositories = {entry["repository"] for entry in dependencies}
        self.assertNotIn("proprietary_vendor_red_hydrogenone", repositories)


if __name__ == "__main__":
    unittest.main()
