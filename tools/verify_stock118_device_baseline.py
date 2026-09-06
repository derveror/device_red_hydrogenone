#!/usr/bin/env python3
from __future__ import annotations

import argparse

EXPECTED = {
    "fingerprint": "RED/HydrogenONE/HydrogenONE:9/PKQ1.190118.001/118:userdebug/release-keys",
    "incremental": "118",
    "release": "9",
    "sdk": "28",
}


def evaluate(observed: dict[str, str]) -> list[str]:
    errors: list[str] = []
    for key, expected in EXPECTED.items():
        actual = observed.get(key, "")
        if actual != expected:
            errors.append(f"{key}: expected {expected!r}, got {actual!r}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Verify that a physical RED Hydrogen One is on the canonical .118 "
            "stock baseline before first LineageOS bring-up."
        )
    )
    parser.add_argument("--fingerprint", required=True)
    parser.add_argument("--incremental", required=True)
    parser.add_argument("--release", required=True)
    parser.add_argument("--sdk", required=True)
    args = parser.parse_args()

    observed = {
        "fingerprint": args.fingerprint.strip(),
        "incremental": args.incremental.strip(),
        "release": args.release.strip(),
        "sdk": args.sdk.strip(),
    }
    errors = evaluate(observed)

    if errors:
        print("STOCK118_BASELINE=FAIL")
        print("Physical bring-up baseline mismatch:")
        for error in errors:
            print(f"  - {error}")
        return 2

    print("STOCK118_BASELINE=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
