from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from tools.analysis.tree_compare import compare_inventories, compare_pairs, main


class TreeCompareTest(unittest.TestCase):
    def test_distinguishes_identical_changed_and_unique_paths(self) -> None:
        left = {
            "archive": "left.zip",
            "files": [
                {"path": "same", "sha256": "a"},
                {"path": "changed", "sha256": "b"},
                {"path": "left-only", "sha256": "c"},
            ],
        }
        right = {
            "archive": "right.zip",
            "files": [
                {"path": "same", "sha256": "a"},
                {"path": "changed", "sha256": "x"},
                {"path": "right-only", "sha256": "y"},
            ],
        }

        result = compare_inventories(left, right)

        self.assertEqual(result["identical_paths"], ["same"])
        self.assertEqual(result["different_paths"], ["changed"])
        self.assertEqual(result["left_only_paths"], ["left-only"])
        self.assertEqual(result["right_only_paths"], ["right-only"])
        self.assertEqual(result["common_paths"], 2)
        self.assertEqual(result["identical_common_paths"], 1)
        self.assertEqual(result["different_common_paths"], 1)

    def test_rejects_duplicate_paths_inside_one_inventory(self) -> None:
        left = {
            "archive": "left.zip",
            "files": [
                {"path": "duplicate", "sha256": "a"},
                {"path": "duplicate", "sha256": "b"},
            ],
        }
        right = {"archive": "right.zip", "files": []}

        with self.assertRaisesRegex(ValueError, "left.zip.*duplicate path.*duplicate"):
            compare_inventories(left, right)

    def test_compare_pairs_resolves_exact_names_and_rejects_unknown_archive(self) -> None:
        inventories = [
            {"archive": "a.zip", "files": []},
            {"archive": "b.zip", "files": []},
        ]

        result = compare_pairs(inventories, [("b.zip", "a.zip")])
        self.assertEqual(result[0]["left"], "b.zip")
        self.assertEqual(result[0]["right"], "a.zip")

        with self.assertRaisesRegex(ValueError, "unknown archive: missing.zip"):
            compare_pairs(inventories, [("a.zip", "missing.zip")])

    def test_cli_sorts_pair_results_and_writes_stable_json(self) -> None:
        inventories = [
            {"archive": "z.zip", "files": [{"path": "same", "sha256": "1"}]},
            {"archive": "a.zip", "files": [{"path": "same", "sha256": "1"}]},
            {"archive": "m.zip", "files": []},
        ]
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "inventory.json"
            first = root / "first.json"
            second = root / "second.json"
            source.write_text(json.dumps(inventories), encoding="utf-8")
            argv = [
                "--inventory",
                str(source),
                "--pair",
                "z.zip:a.zip",
                "--pair",
                "a.zip:m.zip",
            ]

            self.assertEqual(main([*argv, "--output", str(first)]), 0)
            self.assertEqual(main([*argv, "--output", str(second)]), 0)
            self.assertEqual(first.read_bytes(), second.read_bytes())
            payload = json.loads(first.read_text(encoding="utf-8"))

        self.assertEqual(
            [(item["left"], item["right"]) for item in payload],
            [("a.zip", "m.zip"), ("z.zip", "a.zip")],
        )

    def test_cli_summary_only_keeps_counts_and_omits_path_arrays(self) -> None:
        inventories = [
            {"archive": "a.zip", "files": [{"path": "same", "sha256": "1"}]},
            {"archive": "b.zip", "files": [{"path": "same", "sha256": "1"}]},
        ]
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "inventory.json"
            output = root / "comparison.json"
            source.write_text(json.dumps(inventories), encoding="utf-8")

            self.assertEqual(
                main(
                    [
                        "--inventory",
                        str(source),
                        "--pair",
                        "a.zip:b.zip",
                        "--summary-only",
                        "--output",
                        str(output),
                    ]
                ),
                0,
            )
            payload = json.loads(output.read_text(encoding="utf-8"))

        self.assertEqual(payload[0]["common_paths"], 1)
        self.assertNotIn("identical_paths", payload[0])
        self.assertNotIn("different_paths", payload[0])
        self.assertNotIn("left_only_paths", payload[0])
        self.assertNotIn("right_only_paths", payload[0])


if __name__ == "__main__":
    unittest.main()
