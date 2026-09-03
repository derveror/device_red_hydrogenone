#!/usr/bin/env python3
"""Generate and validate the reference-archive section of source-lock.json."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Sequence

FIELD_MAP = {
    "sha256": "archive_sha256",
    "archive_size_bytes": "archive_size_bytes",
    "uncompressed_size_bytes": "uncompressed_size_bytes",
    "file_count": "file_count",
    "root_directory": "root_directory",
    "embedded_source_commit": "embedded_source_commit",
}


def _index(
    records: Sequence[dict[str, Any]], label: str
) -> tuple[dict[str, dict[str, Any]], list[str]]:
    index: dict[str, dict[str, Any]] = {}
    errors: list[str] = []
    for record in records:
        name = str(record.get("archive", ""))
        if not name:
            errors.append(f"{label}: archive record has no name")
            continue
        if name in index:
            errors.append(f"{label}: duplicate archive: {name}")
            continue
        index[name] = record
    return index, errors


def validate_source_lock(
    lock: dict[str, Any], inventory: list[dict[str, Any]]
) -> list[str]:
    raw_locked = lock.get("reference_archives", [])
    if not isinstance(raw_locked, list):
        return ["source lock: reference_archives must be a list"]
    locked_records = [record for record in raw_locked if isinstance(record, dict)]
    errors: list[str] = []
    if len(locked_records) != len(raw_locked):
        errors.append("source lock: every reference archive must be an object")

    locked, locked_errors = _index(locked_records, "source lock")
    observed, observed_errors = _index(inventory, "inventory")
    errors.extend(locked_errors)
    errors.extend(observed_errors)

    for name in sorted(set(locked) - set(observed)):
        errors.append(f"missing archive from inventory: {name}")
    for name in sorted(set(observed) - set(locked)):
        errors.append(f"unexpected archive in inventory: {name}")

    for name in sorted(set(locked) & set(observed)):
        expected_record = locked[name]
        actual_record = observed[name]
        for expected_field, observed_field in FIELD_MAP.items():
            expected = expected_record.get(expected_field)
            actual = actual_record.get(observed_field)
            if expected != actual:
                errors.append(
                    f"{name}: {expected_field} expected {expected}, got {actual}"
                )
    return errors


def reference_records_from_inventory(
    inventory: Sequence[dict[str, Any]],
) -> list[dict[str, Any]]:
    indexed, errors = _index(inventory, "inventory")
    if errors:
        raise ValueError("; ".join(errors))

    records: list[dict[str, Any]] = []
    for name in sorted(indexed):
        observed = indexed[name]
        record: dict[str, Any] = {"archive": name}
        for lock_field, inventory_field in FIELD_MAP.items():
            if inventory_field not in observed:
                raise ValueError(f"{name}: missing inventory field: {inventory_field}")
            record[lock_field] = observed[inventory_field]
        records.append(record)
    return records


def _load_object(path: Path, label: str) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot read {label} {path}: {exc}") from exc
    if not isinstance(payload, dict):
        raise ValueError(f"{label} root must be a JSON object")
    return payload


def _load_inventory(path: Path) -> list[dict[str, Any]]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot read inventory {path}: {exc}") from exc
    if not isinstance(payload, list) or not all(isinstance(item, dict) for item in payload):
        raise ValueError("inventory root must be an array of objects")
    return payload


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Validate or update the locked reference-archive metadata."
    )
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--validate", action="store_true")
    mode.add_argument("--write-reference-section", action="store_true")
    parser.add_argument("--lock", required=True, type=Path)
    parser.add_argument("--inventory", required=True, type=Path)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        lock = _load_object(args.lock, "source lock")
        inventory = _load_inventory(args.inventory)
        if args.validate:
            errors = validate_source_lock(lock, inventory)
            if errors:
                for error in errors:
                    print(error, file=sys.stderr)
                return 1
            print(f"source lock verified: {len(inventory)} archives")
            return 0

        lock["reference_archives"] = reference_records_from_inventory(inventory)
        args.lock.write_text(
            json.dumps(lock, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
            newline="\n",
        )
        print(f"source lock updated: {len(inventory)} archives")
        return 0
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
