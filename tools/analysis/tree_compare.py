#!/usr/bin/env python3
"""Compare normalized reference-tree inventories by path and content hash."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Sequence


def _path_hash_map(inventory: dict[str, Any]) -> dict[str, str]:
    archive = str(inventory.get("archive", "<unnamed>"))
    result: dict[str, str] = {}
    files = inventory.get("files")
    if not isinstance(files, list):
        raise ValueError(f"{archive}: files must be a list")
    for item in files:
        if not isinstance(item, dict):
            raise ValueError(f"{archive}: file record must be an object")
        path = str(item["path"])
        if path in result:
            raise ValueError(f"{archive}: duplicate path: {path}")
        result[path] = str(item["sha256"])
    return result


def compare_inventories(
    left: dict[str, Any], right: dict[str, Any]
) -> dict[str, object]:
    left_map = _path_hash_map(left)
    right_map = _path_hash_map(right)
    common = set(left_map) & set(right_map)
    identical = sorted(path for path in common if left_map[path] == right_map[path])
    different = sorted(common - set(identical))
    left_only = sorted(set(left_map) - set(right_map))
    right_only = sorted(set(right_map) - set(left_map))
    return {
        "left": str(left["archive"]),
        "right": str(right["archive"]),
        "left_files": len(left_map),
        "right_files": len(right_map),
        "common_paths": len(common),
        "identical_common_paths": len(identical),
        "different_common_paths": len(different),
        "left_only_paths": left_only,
        "right_only_paths": right_only,
        "identical_paths": identical,
        "different_paths": different,
    }


def _inventory_index(
    inventories: Sequence[dict[str, Any]],
) -> dict[str, dict[str, Any]]:
    index: dict[str, dict[str, Any]] = {}
    for inventory in inventories:
        name = str(inventory.get("archive", ""))
        if not name:
            raise ValueError("inventory record has no archive name")
        if name in index:
            raise ValueError(f"duplicate archive: {name}")
        index[name] = inventory
    return index


def compare_pairs(
    inventories: Sequence[dict[str, Any]],
    pairs: Sequence[tuple[str, str]],
) -> list[dict[str, object]]:
    index = _inventory_index(inventories)
    results: list[dict[str, object]] = []
    for left_name, right_name in pairs:
        for name in (left_name, right_name):
            if name not in index:
                raise ValueError(f"unknown archive: {name}")
        results.append(compare_inventories(index[left_name], index[right_name]))
    return sorted(results, key=lambda item: (str(item["left"]), str(item["right"])))


def _parse_pair(value: str) -> tuple[str, str]:
    left, separator, right = value.partition(":")
    if not separator or not left or not right:
        raise argparse.ArgumentTypeError(
            "pair must be written as <left-archive>:<right-archive>"
        )
    return left, right


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Compare normalized archive inventories by exact archive name."
    )
    parser.add_argument("--inventory", required=True, type=Path)
    parser.add_argument("--pair", required=True, action="append", type=_parse_pair)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument(
        "--summary-only",
        action="store_true",
        help="omit path arrays while retaining exact comparison counts",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        payload = json.loads(args.inventory.read_text(encoding="utf-8"))
        if not isinstance(payload, list):
            raise ValueError("inventory root must be a JSON array")
        inventories = [item for item in payload if isinstance(item, dict)]
        if len(inventories) != len(payload):
            raise ValueError("every inventory record must be a JSON object")
        results = compare_pairs(inventories, args.pair)
        if args.summary_only:
            path_keys = {
                "left_only_paths",
                "right_only_paths",
                "identical_paths",
                "different_paths",
            }
            results = [
                {key: value for key, value in result.items() if key not in path_keys}
                for result in results
            ]
    except (OSError, json.JSONDecodeError, KeyError, ValueError) as exc:
        parser.error(str(exc))

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(results, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
