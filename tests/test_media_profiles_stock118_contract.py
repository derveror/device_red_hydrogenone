from __future__ import annotations

import hashlib
import json
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "docs" / "stock" / "h1a1000-r118" / "device-vs-stock-config-audit.json"
MEDIA = ROOT / "media" / "media_profiles_V1_0.xml"
SOURCE = "media/media_profiles_V1_0.xml"
STOCK_SHA = "7277a1accf9595bb727f2189863cf5f6249dd99322e2953432bca6e448365f1e"


def stock_identity() -> tuple[int, str]:
    audit = json.loads(AUDIT.read_text(encoding="utf-8"))
    if audit.get("authority", {}).get("stock_archive_sha256") != STOCK_SHA:
        raise AssertionError("media profile audit is not bound to canonical RED .118")
    for row in audit.get("rows", []):
        if row.get("source") == SOURCE:
            if row.get("stock_size") is None or not row.get("stock_sha256"):
                raise AssertionError("canonical media profile identity is missing")
            return int(row["stock_size"]), str(row["stock_sha256"])
    raise AssertionError("media profile source is missing from canonical audit")


class MediaProfilesStock118ContractTest(unittest.TestCase):
    def test_exact_canonical_red118_media_profiles(self) -> None:
        expected_size, expected_sha = stock_identity()
        data = MEDIA.read_bytes()
        self.assertEqual(len(data), expected_size)
        self.assertEqual(hashlib.sha256(data).hexdigest(), expected_sha)

    def test_red_camera_profile_ids_zero_through_five_are_preserved(self) -> None:
        root = ET.parse(MEDIA).getroot()
        ids = sorted(
            int(element.attrib["cameraId"])
            for element in root.findall("CamcorderProfiles")
            if "cameraId" in element.attrib
        )
        self.assertEqual(ids, [0, 1, 2, 3, 4, 5])


if __name__ == "__main__":
    unittest.main()
