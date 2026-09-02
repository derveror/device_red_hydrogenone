# ASSISTANT RESUME MARKER — Hydrogen One LineageOS 22.2

> **READ THIS FILE FIRST AFTER ANY INTERRUPTION.**

**Marker version:** 4  
**Last completed action file:** `docs/worklog/2026-09-02/0005-build-readiness-roomservice-audit.md`  
**Logging protocol active:** YES

## Current repository checkpoints

### Device
- Repository: `derveror/device_red_hydrogenone`
- Branch: `lineage-22.2-stock118-rework`.
- Cross-tree lock currently points to vendor `6fef3d7c6333602d7114aefa0284a03f5aadb454`.
- The first repin CI failed because the permanent workflow and published cross-tree evidence still referred to `d30ac190...`.
- `.github/workflows/verify-analysis.yml` has already been updated to checkout `6fef3d7c...`.
- A one-shot `regenerate-cross-tree-evidence.yml` is active for diagnostics/regeneration; its first attempt showed the live contract tool itself returned nonzero before evidence rewrite, so current device/vendor copy collisions must be diagnosed before declaring the repin GREEN.

### Vendor
- Repository: `derveror/proprietary_vendor_red_hydrogenone`.
- Branch: `lineage-22.2-android15-contract`.
- Current GREEN head: `6fef3d7c6333602d7114aefa0284a03f5aadb454`.
- Relative to `d30ac190...`, this head changes only the permanent vendor CI workflow; proprietary payload/config is unchanged.

## Canonical stock authority

- Build: `H1A1000.082ho.01.00.10r.118`.
- Android 9 / API 28; first API 27.
- Archive SHA-256: `7277a1accf9595bb727f2189863cf5f6249dd99322e2953432bca6e448365f1e`.
- Exact `.118` boot/kernel, product identity, vendor patch, DSDS/qcrild, fstab migration, camera topology/tuning and major Android 15 ownership contracts are pinned.

## Build-readiness finding already established

LineageOS 22.2 `roomservice.py` resolves ordinary `lineage.dependencies` entries as `LineageOS/<repository>`. Therefore the custom `derveror/proprietary_vendor_red_hydrogenone` cannot be added as a normal dependency entry. A checked-in local-manifest strategy is required for reproducible clean checkout. LineageOS-owned kernel/sepolicy dependencies remain suitable for `lineage.dependencies`.

## Hard architecture constraints

- Target LineageOS 22.2 / Android 15 / API 35.
- Never create `device/red/msm8998-common`.
- Never create `vendor/red/msm8998-common` or another RED common vendor repository.
- Open/adapted config -> `device/red/hydrogenone`.
- Proprietary payload/generated proprietary modules -> `vendor/red/hydrogenone`.
- `.118` stock outranks donor assumptions.

## Immediate next action — DO THIS FIRST

Read the latest run/log of `regenerate-cross-tree-evidence.yml` and obtain the exact `LIVE_COPY_DESTINATION_COLLISIONS` list. Fix ownership collisions based on source/vendor responsibility, then regenerate evidence and restore permanent CI to GREEN.

## After cross-tree GREEN

Create/test the reproducible local-manifest template and make the kernel branch explicit in `lineage.dependencies`, then move to actual clean LineageOS workspace `lunch` + `m nothing`.

## Recovery rule

After interruption, do **not** infer state from chat prose. Read this marker, then the last numbered action file, then verify both branch heads and any active one-shot workflow from GitHub before continuing.
