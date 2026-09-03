#!/usr/bin/env bash
set -euo pipefail

VALIDATE_ONLY=false
LUNCH_TARGET="${HYDROGENONE_LUNCH_TARGET:-lineage_hydrogenone-userdebug}"
TOP="${ANDROID_BUILD_TOP:-$(pwd)}"
LOG_DIR="${HYDROGENONE_LOG_DIR:-}"

usage() {
    cat <<'EOF'
Usage: bash device/red/hydrogenone/tools/build/run_m_nothing_preflight.sh [options]

Run the first real Hydrogen One LineageOS 22.2 build gate from a complete,
clean workspace and preserve a timestamped log.

Options:
  --validate-only       Verify workspace/revisions but do not source envsetup or build.
  --top PATH            LineageOS source-tree root (default: $ANDROID_BUILD_TOP or cwd).
  --lunch TARGET        Lunch target (default: lineage_hydrogenone-userdebug).
  --log-dir PATH        Log directory (default: <top>/out/hydrogenone-build-logs).
  -h, --help            Show this help.

Environment equivalents:
  HYDROGENONE_LUNCH_TARGET
  HYDROGENONE_LOG_DIR
EOF
}

fail() {
    printf 'preflight: ERROR: %s\n' "$*" >&2
    exit 1
}

while (($#)); do
    case "$1" in
        --validate-only)
            VALIDATE_ONLY=true
            shift
            ;;
        --top)
            (($# >= 2)) || fail "--top requires a path"
            TOP="$2"
            shift 2
            ;;
        --lunch)
            (($# >= 2)) || fail "--lunch requires a target"
            LUNCH_TARGET="$2"
            shift 2
            ;;
        --log-dir)
            (($# >= 2)) || fail "--log-dir requires a path"
            LOG_DIR="$2"
            shift 2
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        *)
            fail "unknown argument: $1"
            ;;
    esac
done

TOP="$(cd "$TOP" 2>/dev/null && pwd)" || fail "cannot enter source top: $TOP"
cd "$TOP"

[[ -f build/envsetup.sh ]] || fail "not a complete Android source top: missing build/envsetup.sh"
[[ -d .repo ]] || fail "not a repo workspace: missing .repo"

DEVICE_PATH="device/red/hydrogenone"
VENDOR_PATH="vendor/red/hydrogenone"
KERNEL_PATH="kernel/essential/msm8998"
SEPOLICY_PATH="device/qcom/sepolicy-legacy-um"
LOCK_PATH="$DEVICE_PATH/docs/reference/cross-tree-lock.json"

for path in "$DEVICE_PATH" "$VENDOR_PATH" "$KERNEL_PATH" "$SEPOLICY_PATH"; do
    [[ -d "$path" ]] || fail "required project path is missing: $path"
    git -C "$path" rev-parse --is-inside-work-tree >/dev/null 2>&1 \
        || fail "required project is not a Git checkout: $path"

    dirty="$(git -C "$path" status --porcelain)"
    [[ -z "$dirty" ]] || {
        printf 'preflight: dirty checkout: %s\n%s\n' "$path" "$dirty" >&2
        fail "workspace must be clean before the first build gate"
    }
done

[[ -f "$LOCK_PATH" ]] || fail "missing cross-tree lock: $LOCK_PATH"
EXPECTED_VENDOR_HEAD="$(python3 - "$LOCK_PATH" <<'PY'
import json
import sys
from pathlib import Path

lock = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
value = lock.get("vendor_commit", "")
if not value:
    raise SystemExit("cross-tree lock has no vendor_commit")
print(value)
PY
)"

VENDOR_HEAD="$(git -C "$VENDOR_PATH" rev-parse HEAD)"
[[ "$VENDOR_HEAD" == "$EXPECTED_VENDOR_HEAD" ]] \
    || fail "vendor revision mismatch: expected $EXPECTED_VENDOR_HEAD, got $VENDOR_HEAD"

TIMESTAMP="$(date -u +%Y%m%dT%H%M%SZ)"
if [[ -z "$LOG_DIR" ]]; then
    LOG_DIR="$TOP/out/hydrogenone-build-logs"
fi
mkdir -p "$LOG_DIR"
LOG_FILE="$LOG_DIR/m-nothing-$TIMESTAMP.log"
META_FILE="$LOG_DIR/m-nothing-$TIMESTAMP.meta.txt"
STATUS_FILE="$LOG_DIR/m-nothing-$TIMESTAMP.status"

record_revision() {
    local label="$1"
    local path="$2"
    printf '%s=%s\n' "$label" "$(git -C "$path" rev-parse HEAD)"
}

{
    printf 'timestamp_utc=%s\n' "$TIMESTAMP"
    printf 'top=%s\n' "$TOP"
    printf 'lunch_target=%s\n' "$LUNCH_TARGET"
    printf 'expected_vendor_commit=%s\n' "$EXPECTED_VENDOR_HEAD"
    record_revision device_head "$DEVICE_PATH"
    record_revision vendor_head "$VENDOR_PATH"
    record_revision kernel_head "$KERNEL_PATH"
    record_revision sepolicy_head "$SEPOLICY_PATH"
    printf 'host_uname=%s\n' "$(uname -a)"
    printf 'python=%s\n' "$(python3 --version 2>&1)"
    printf 'java=%s\n' "$(java -version 2>&1 | head -n 1 || true)"
    if command -v free >/dev/null 2>&1; then
        free -h
    fi
} | tee "$META_FILE"

printf 'preflight: workspace validation passed\n'
printf 'preflight: metadata: %s\n' "$META_FILE"

if [[ "$VALIDATE_ONLY" == true ]]; then
    printf 'preflight: --validate-only requested; build was not started\n'
    printf 'VALIDATED_ONLY\n' > "$STATUS_FILE"
    exit 0
fi

printf 'preflight: starting first build gate: %s -> m nothing\n' "$LUNCH_TARGET"
printf 'preflight: full build log: %s\n' "$LOG_FILE"

set +e
(
    set +u
    set -e
    source build/envsetup.sh
    lunch "$LUNCH_TARGET"
    m nothing
) 2>&1 | tee "$LOG_FILE"
BUILD_STATUS=${PIPESTATUS[0]}
set -e

printf '%s\n' "$BUILD_STATUS" > "$STATUS_FILE"
printf 'preflight: m nothing exit status: %s\n' "$BUILD_STATUS"
printf 'preflight: status file: %s\n' "$STATUS_FILE"

exit "$BUILD_STATUS"
