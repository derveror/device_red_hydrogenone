# ASSISTANT RESUME MARKER — Hydrogen One LineageOS 22.2

> **READ THIS FILE FIRST AFTER ANY INTERRUPTION.**

**Marker version:** 6  
**Last completed action file:** `docs/worklog/2026-09-02/0007-cross-tree-collisions-proven-false-positive.md`  
**Logging protocol active:** YES

## Current repository checkpoints

### Device
- Repository: `derveror/device_red_hydrogenone`.
- Branch: `lineage-22.2-stock118-rework`.
- Cross-tree lock points to vendor `6fef3d7c6333602d7114aefa0284a03f5aadb454`.
- Permanent cross-tree checkout uses the same vendor commit.
- Published `cross-tree-copy-contract.json` still has stale authority from the prior vendor pin and must be regenerated.
- The previously reported 49 live collisions are **proven diagnostic false positives**: every device-side owner was `vendor-tree/hydrogenone-vendor.mk`, because the one-shot workflow nested the vendor checkout inside the device scan root. No runtime file pruning is required from that list.

### Vendor
- Repository: `derveror/proprietary_vendor_red_hydrogenone`.
- Branch: `lineage-22.2-android15-contract`.
- Current GREEN head: `6fef3d7c6333602d7114aefa0284a03f5aadb454`.
- Relative to `d30ac190...`, this head changes only permanent vendor CI; proprietary payload/config is unchanged.

## Canonical stock authority

- Build: `H1A1000.082ho.01.00.10r.118`.
- Android 9 / API 28; first API 27.
- Archive SHA-256: `7277a1accf9595bb727f2189863cf5f6249dd99322e2953432bca6e448365f1e`.
- Exact `.118` boot/kernel, product identity, vendor patch, DSDS/qcrild, fstab migration, camera topology/tuning and major Android 15 ownership contracts are pinned.

## Build-readiness finding already established

LineageOS 22.2 roomservice resolves ordinary `lineage.dependencies` GitHub entries as `LineageOS/<repository>`. The custom `derveror/proprietary_vendor_red_hydrogenone` therefore needs a local-manifest strategy; do not add it as a normal LineageOS dependency entry.

## Hard architecture constraints

- Target LineageOS 22.2 / Android 15 / API 35.
- Never create `device/red/msm8998-common`.
- Never create `vendor/red/msm8998-common` or another RED common vendor repository.
- Open/adapted config -> `device/red/hydrogenone`.
- Proprietary payload/generated proprietary modules -> `vendor/red/hydrogenone`.
- `.118` stock outranks donor assumptions.

## Immediate next action — DO THIS FIRST

Fix only the one-shot regeneration workflow so the vendor checkout is outside the device scan root (for example move it to `$RUNNER_TEMP/vendor-tree` before invoking `cross_tree_contract.py`). Rerun the exact live audit. If zero collisions, regenerate `cross-tree-copy-contract.json` with vendor authority `6fef3d7c...`, self-delete the one-shot workflow, and verify permanent device CI GREEN.

## After cross-tree GREEN

1. Create/test reproducible local-manifest template.
2. Make the kernel branch explicit in `lineage.dependencies`.
3. Move to actual clean LineageOS workspace `lunch lineage_hydrogenone-userdebug` + `m nothing`.

## Recovery rule

After interruption, do **not** infer state from chat prose. Read this marker, then the last numbered action file, then verify both branch heads and active one-shot workflows from GitHub before continuing.
