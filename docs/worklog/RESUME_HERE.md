# ASSISTANT RESUME MARKER — Hydrogen One LineageOS 22.2

> **READ THIS FILE FIRST AFTER ANY INTERRUPTION.**

**Marker version:** 5  
**Last completed action file:** `docs/worklog/2026-09-02/0006-cross-tree-live-collision-diagnostic.md`  
**Logging protocol active:** YES

## Current repository checkpoints

### Device
- Repository: `derveror/device_red_hydrogenone`.
- Branch: `lineage-22.2-stock118-rework`.
- Cross-tree lock points to vendor `6fef3d7c6333602d7114aefa0284a03f5aadb454`.
- Permanent cross-tree checkout has been updated to the same vendor commit.
- Published `cross-tree-copy-contract.json` is stale and still belongs to the earlier zero-collision state.
- Live diagnostic against the current device tree + vendor `6fef3d7c...` found 49 duplicate install destinations; exact list is preserved in Action 0006.
- Do NOT declare cross-tree GREEN and do NOT merely rewrite the evidence authority until these ownership collisions are resolved.

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

Inspect device/vendor producers for the 49 destinations listed in Action 0006. Classify each group as device/source-owned or vendor/proprietary-owned. Add ownership regression tests first, confirm RED, then prune the losing side. Pay special attention to `init.msm.usb.configfs.rc` and standard NFC permission XMLs, which may be source-owned rather than vendor-owned.

## After collision cleanup

1. Regenerate `cross-tree-copy-contract.json` from the exact current trees.
2. Remove the one-shot `regenerate-cross-tree-evidence.yml`.
3. Restore permanent device CI and cross-tree job to GREEN.
4. Create/test reproducible local-manifest template and explicit kernel dependency branch.
5. Move to actual clean LineageOS workspace `lunch lineage_hydrogenone-userdebug` + `m nothing`.

## Recovery rule

After interruption, do **not** infer state from chat prose. Read this marker, then the last numbered action file, then verify both branch heads and active one-shot workflows from GitHub before continuing.
