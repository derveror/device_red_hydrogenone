# ASSISTANT RESUME MARKER — Hydrogen One LineageOS 22.2

> **READ THIS FILE FIRST AFTER ANY INTERRUPTION.**

**Marker version:** 7  
**Last completed action file:** `docs/worklog/2026-09-02/0008-cross-tree-evidence-regenerated-green.md`  
**Logging protocol active:** YES

## Current repository checkpoints

### Device
- Repository: `derveror/device_red_hydrogenone`.
- Branch: `lineage-22.2-stock118-rework`.
- Cross-tree lock pins vendor `6fef3d7c6333602d7114aefa0284a03f5aadb454`.
- Fresh zero-collision cross-tree evidence was regenerated against that exact vendor commit.
- One-shot regeneration workflow self-deleted successfully.
- Regeneration commit: `e01f8d83fb20aa90abf1c790fbb0e9ea8871f892`.
- Action 0008 records the successful isolated-root audit.

### Vendor
- Repository: `derveror/proprietary_vendor_red_hydrogenone`.
- Branch: `lineage-22.2-android15-contract`.
- Current GREEN head: `6fef3d7c6333602d7114aefa0284a03f5aadb454`.

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

Confirm permanent device `verify-analysis.yml` on the current post-regeneration branch head. Both `verify` and `cross_tree` jobs must be GREEN. If GREEN, record it as the next action and proceed to the reproducible local-manifest/dependency gate.

## After permanent CI GREEN

1. Create/test a local-manifest template for device/vendor + required Lineage dependencies.
2. Make kernel branch explicit in `lineage.dependencies`.
3. Validate manifest XML and path/branch pins statically.
4. Move to actual clean LineageOS workspace `lunch lineage_hydrogenone-userdebug` + `m nothing`.

## Recovery rule

After interruption, do **not** infer state from chat prose. Read this marker, then the last numbered action file, then verify both branch heads and active workflows from GitHub before continuing.
