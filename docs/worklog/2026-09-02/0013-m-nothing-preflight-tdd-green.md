# Action 0013 — Deterministic `m nothing` preflight TDD RED -> GREEN

**Production branch:** `lineage-22.2-stock118-rework`  
**Production script commit:** `4dfead860c82b0f8681ba21c569c262e353ba9a5`  
**Production regression-test commit:** `b15f6f8ed24ba53a1e9ec65d75356295a4c95fe8`

## RED

An isolated branch `build-preflight-tdd` introduced `tests/test_build_preflight_contract.py` before the implementation existed.

RED run:

```text
workflow: Build preflight TDD
run: 33687048175
job: 100436887851
```

The five contract tests failed only because `tools/build/run_m_nothing_preflight.sh` did not yet exist. No unrelated infrastructure or existing project contract failed.

## Implementation

Added:

```text
tools/build/run_m_nothing_preflight.sh
```

The script is intentionally non-destructive. It does **not** run `repo sync`, `git reset`, `git clean`, or source-tree deletion commands.

It requires a complete repo workspace and validates these Git checkouts:

```text
device/red/hydrogenone
vendor/red/hydrogenone
kernel/essential/msm8998
device/qcom/sepolicy-legacy-um
```

Each checkout must be clean. It reads the exact vendor SHA from:

```text
device/red/hydrogenone/docs/reference/cross-tree-lock.json
```

and refuses to build if `vendor/red/hydrogenone` is not at that exact commit.

It records device/vendor/kernel/sepolicy HEADs and host metadata under:

```text
out/hydrogenone-build-logs/
```

It supports `--validate-only` to perform all prerequisite/revision checks without sourcing the Android build environment or starting a build.

The real first build gate is exactly:

```text
source build/envsetup.sh
lunch lineage_hydrogenone-userdebug
m nothing
```

The complete output is piped through `tee`; the original build exit status is preserved through `PIPESTATUS[0]` and written to a separate status file.

No later image/OTA target is invoked by this script.

## Isolated GREEN

TDD GREEN run:

```text
workflow: Build preflight TDD
run: 33687137879
job: 100437175949
```

All five preflight contract tests passed.

## Production GREEN

Permanent production run after promoting the script/test:

```text
workflow: Verify stock intake and analysis tooling
run: 33687201146
```

Results:

```text
verify:     SUCCESS
cross_tree: SUCCESS
```

The production `verify` job passed JSON/source locks, every unittest module including the preflight contract, `test_full_tree.py`, canonical stock checks and exact `.118` boot/kernel verification. The production `cross_tree` job passed against exact pinned vendor commit `6fef3d7c6333602d7114aefa0284a03f5aadb454`.

## Result

The repository now has one tested, deterministic entrypoint for the first real full-Lineage workspace build attempt. The next authoritative input is no longer another static guess: it is the output of this script on the user's complete LineageOS 22.2 workspace.

## Next action

Replace/redirect the stale historical `BUILD_FIRST.md` instructions, which still reference the old `.109` 4.4.78 kernel and `m bacon`, so there is only one current first-build procedure. Then update `RESUME_HERE.md` and prepare the exact local-workspace commands for validation followed by the first `m nothing` run.
