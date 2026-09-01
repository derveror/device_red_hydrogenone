#!/usr/bin/env bash
set -euo pipefail
ROOT=$(cd "$(dirname "$0")/.." && pwd)
cd "$ROOT"
python3 -m unittest discover -s tests -v
python3 tools/validate_tree.py .
if [[ $# -eq 1 ]]; then
    python3 tools/validate_twrp_boot.py "$1"
fi
