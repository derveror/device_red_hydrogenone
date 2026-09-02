# ASSISTANT RESUME MARKER — Hydrogen One LineageOS 22.2

> **READ THIS FILE FIRST AFTER ANY INTERRUPTION.**

**Marker version:** 3  
**Last completed action file:** `docs/worklog/2026-09-02/0004-cross-tree-repin-ci-failure.md`  
**Logging protocol active:** YES

## Current repository checkpoints

### Device
- Repository: `derveror/device_red_hydrogenone`
- Branch: `lineage-22.2-stock118-rework`
- Last non-log project checkpoint before worklog: `4036ecea476c5561001310ec17451cb8bcb18adb`.
- Cross-tree lock was advanced in commit `5cc099b7fa65ab183476ed403351c82013084974` to vendor `6fef3d7c...`, but the permanent device CI run `33684878692` failed. Treat the repin as **UNVERIFIED/BROKEN until fixed or reverted**.

### Vendor
- Repository: `derveror/proprietary_vendor_red_hydrogenone`
- Branch: `lineage-22.2-android15-contract`
- Current vendor head: `6fef3d7c6333602d7114aefa0284a03f5aadb454`.
- Vendor CI at this head is GREEN.
- `6fef3d7c...` is one commit ahead of `d30ac190...` and changes only `.github/workflows/verify-vendor-contract.yml`.

## Canonical stock authority

- Build: `H1A1000.082ho.01.00.10r.118`
- Android: 9 / API 28; first API 27
- Archive SHA-256: `7277a1accf9595bb727f2189863cf5f6249dd99322e2953432bca6e448365f1e`
- Exact `.118` boot/kernel, product identity, vendor patch, DSDS/qcrild, fstab migration and major static ownership contracts remain pinned.

## Hard architecture constraints

- Target LineageOS 22.2 / Android 15 / API 35.
- Never create `device/red/msm8998-common`.
- Never create `vendor/red/msm8998-common` or another RED common vendor repository.
- Open/adapted config -> `device/red/hydrogenone`.
- Proprietary payload/generated proprietary modules -> `vendor/red/hydrogenone`.
- `.118` stock outranks donor assumptions.

## Immediate next action — DO THIS FIRST

Inspect exact failure logs:

- device `verify` job: `100429832398`;
- device `cross_tree` job: `100429832118`;
- workflow run: `33684878692`.

Find the first real assertion failures. Do not declare the new vendor pin valid and do not proceed to `m nothing` readiness until this gate is GREEN again.

## After that

Continue build-readiness analysis of `lineage.dependencies` / local-manifest requirements. Current known fact: LineageOS `roomservice.py` resolves normal `lineage.dependencies` GitHub entries under the `LineageOS/` organization, so the custom `derveror/proprietary_vendor_red_hydrogenone` cannot simply be added as a normal dependency entry without a separate local-manifest strategy.

## Recovery rule

After an interruption, do **not** infer state from chat prose. Read this marker, then the last numbered action file, then verify both branch heads from GitHub before continuing.
