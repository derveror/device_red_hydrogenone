from __future__ import annotations

import hashlib
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

EXPECTED = {
    "configs/camera/camera_config.xml": (5903, "436c8d655df7bde99889a10e2fdd6a7a1c9c540829b5428c55de61bdb6d9e5ef"),
    "configs/camera/imx268_main_chromatix.xml": (11295, "70726f6300db246e16316dac0d8fc0ae46851543df0aa6c9ee9d54367d9abcd2"),
    "configs/camera/imx268_sub_chromatix.xml": (11271, "436887e6d26c83d7be69dc10403edee5e56c416566e563eef962521f3dd3fa84"),
    "configs/camera/imx380_main_chromatix.xml": (14923, "e6d7d669c9771161f9337eb8d47a40ba720b093712cc0f75f809462ddb6431df"),
    "configs/camera/imx380_sub_chromatix.xml": (16489, "9cb4ed48cca0bb97314872779686150728a4129efe0ac07af2c9c33d944649fd"),
}


class CameraStock118ContractTest(unittest.TestCase):
    def test_exact_canonical_red118_camera_files(self) -> None:
        failures = []
        for relative, (expected_size, expected_sha) in EXPECTED.items():
            path = ROOT / relative
            if not path.is_file():
                failures.append(f"missing {relative}")
                continue
            data = path.read_bytes()
            actual_sha = hashlib.sha256(data).hexdigest()
            if len(data) != expected_size:
                failures.append(f"{relative}: size {len(data)} != {expected_size}")
            if actual_sha != expected_sha:
                failures.append(f"{relative}: sha256 {actual_sha} != {expected_sha}")
        self.assertEqual(failures, [], "camera stock identity mismatch:\n" + "\n".join(failures))

    def test_red_3d_modes_match_stock_contract(self) -> None:
        for name in (
            "imx268_main_chromatix.xml",
            "imx268_sub_chromatix.xml",
            "imx380_main_chromatix.xml",
            "imx380_sub_chromatix.xml",
        ):
            text = (ROOT / "configs/camera" / name).read_text(encoding="utf-8")
            self.assertIn("CM_3D_VIDEO_MODE", text, name)
            self.assertNotIn("ARC_3D_MODE", text, name)

        for name in ("imx380_main_chromatix.xml", "imx380_sub_chromatix.xml"):
            text = (ROOT / "configs/camera" / name).read_text(encoding="utf-8")
            self.assertIn("CM_3D_SNAPSHOT_MODE", text, name)
            self.assertIn("CM_PANORAMA_MODE", text, name)


if __name__ == "__main__":
    unittest.main()
