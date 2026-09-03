# Action 0014 — `BUILD_FIRST.md` update blocked by blob-SHA mismatch

**Repository:** `derveror/device_red_hydrogenone`  
**Branch:** `lineage-22.2-stock118-rework`

## Intended action

Replace the stale first-build instructions that still referenced:

- RED `.109` / kernel 4.4.78;
- `m bacon` as the first build target.

The intended replacement points to canonical `.118`, the exact `.118` transitional 4.4.153+ prebuilt kernel, the checked-in local manifest, and the tested `run_m_nothing_preflight.sh` workflow.

## Failure

The first `update_file` call supplied an incorrect current blob SHA for `BUILD_FIRST.md` and GitHub returned HTTP `409` (`file does not match supplied SHA`).

## Repository impact

**None.** GitHub rejected the write atomically. `BUILD_FIRST.md` remained unchanged.

No force update, reset, or overwrite was attempted.

## Next action

Re-read `BUILD_FIRST.md`, use the exact returned blob SHA (`f42809651c966d57392ccea5d12b1e92b5e402ec` as observed before the failed write, subject to re-verification), and apply the same documentation-only replacement.
