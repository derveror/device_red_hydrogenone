from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "docs" / "stock" / "h1a1000-r118" / "device-vs-stock-config-audit.json"
STOCK_SHA = "7277a1accf9595bb727f2189863cf5f6249dd99322e2953432bca6e448365f1e"
CAMERA_FILES = (
    "configs/camera/camera_config.xml",
    "configs/camera/imx268_main_chromatix.xml",
    "configs/camera/imx268_sub_chromatix.xml",
    "configs/camera/imx380_main_chromatix.xml",
    "configs/camera/imx380_sub_chromatix.xml",
)


def expected_camera_identity() -> dict[str, tuple[int, str]]:
    audit = json.loads(AUDIT.read_text(encoding="utf-8"))
    authority = audit.get("authority", {})
    if authority.get("stock_archive_sha256") != STOCK_SHA:
        raise AssertionError(f"unexpected stock authority: {authority}")
    by_source = {row["source"]: row for row in audit.get("rows", [])}
    result: dict[str, tuple[int, str]] = {}
    for source in CAMERA_FILES:
        row = by_source.get(source)
        if row is None:
            raise AssertionError(f"camera source missing from canonical audit: {source}")
        if not row.get("stock_sha256") or row.get("stock_size") is None:
            raise AssertionError(f"camera stock identity missing from canonical audit: {source}")
        result[source] = (int(row["stock_size"]), str(row["stock_sha256"]))
    return result


class CameraStock118ContractTest(unittest.TestCase):
    def test_exact_canonical_red118_camera_files(self) -> None:
        failures = []
        for relative, (expected_size, expected_sha) in expected_camera_identity().items():
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
