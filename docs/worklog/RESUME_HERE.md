# ASSISTANT RESUME MARKER — Hydrogen One LineageOS 22.2

> **READ THIS FILE FIRST AFTER ANY INTERRUPTION.**

**Marker version:** 13
**Last completed action file:** `docs/worklog/2026-09-02/0018-bootstrap-regression-green.md`  
**Logging protocol active:** YES

## Current repository checkpoints

### Device
- Repository: `derveror/device_red_hydrogenone`.
- Branch: `lineage-22.2-stock118-rework`.
- Working branch: `test/lineage-22.2-bringup`.
- Cross-tree lock pins vendor `266c8f95d0212c9cc5c91a200363276d45e045b1`.
- Fresh zero-collision cross-tree evidence is pinned to that exact vendor commit.
- Production local-manifest template: `docs/manifests/hydrogenone-lineage-22.2.xml`.
- Fresh-workspace bootstrap: `docs/manifests/README.md`.
- Production first-build runner: `tools/build/run_m_nothing_preflight.sh`.
- Current first-build entrypoint: `BUILD_FIRST.md`.
- Latest bootstrap regression run `33687675809` passed `verify=success` and `cross_tree=success`.

### Vendor
- Repository: `derveror/proprietary_vendor_red_hydrogenone`.
- Working branch: `test/lineage-22.2-bringup` (based on `lineage-22.2-android15-contract`).
- Current payload-equivalent documentation head and device pin: `266c8f95d0212c9cc5c91a200363276d45e045b1`.

## Canonical stock authority

- Build: `H1A1000.082ho.01.00.10r.118`.
- Android 9 / API 28; first API 27.
- Archive SHA-256: `7277a1accf9595bb727f2189863cf5f6249dd99322e2953432bca6e448365f1e`.
- Exact `.118` boot/kernel, product identity, vendor patch, DSDS/qcrild, fstab migration, camera topology/tuning and major Android 15 ownership contracts are pinned.

## Repository-side readiness status

GREEN and regression-tested:

- canonical `.118` stock/source/boot/kernel contracts;
- Android 15 device/vendor ownership split;
- vendor exact pin and zero cross-tree copy collisions;
- VINTF/init/radio/fstab/camera static contracts;
- clean-checkout local manifest and live repository revisions;
- fresh LineageOS 22.2 bootstrap documentation;
- deterministic non-destructive `m nothing` preflight/log capture;
- removal of stale `.109`/4.4.78/`m bacon` first-build guidance.

## Hard architecture constraints

- Target LineageOS 22.2 / Android 15 / API 35.
- Never create `device/red/msm8998-common`.
- Never create `vendor/red/msm8998-common` or another RED common vendor repository.
- Open/adapted config -> `device/red/hydrogenone`.
- Proprietary payload/generated proprietary modules -> `vendor/red/hydrogenone`.
- `.118` stock outranks donor assumptions.

## Immediate next action — EXTERNAL EXECUTION BOUNDARY

The next decisive proof requires the user's complete local LineageOS 22.2 workspace. No further speculative repository patch should be made before this result.

From a clean synced LineageOS top, run first:

```bash
bash device/red/hydrogenone/tools/build/run_m_nothing_preflight.sh --validate-only
```

If and only if that succeeds, run:

```bash
bash device/red/hydrogenone/tools/build/run_m_nothing_preflight.sh
```

Collect the newest files from:

```text
out/hydrogenone-build-logs/
```

Specifically the matching timestamp triplet:

```text
m-nothing-<timestamp>.log
m-nothing-<timestamp>.meta.txt
m-nothing-<timestamp>.status
```

The first actual `m nothing` result is the authoritative next debugging input. Fix only errors emitted by that build.

## After `m nothing` GREEN

Advance one target at a time:

1. `bootimage`;
2. `vendorimage`;
3. `systemimage`;
4. `target-files-package`;
5. `otapackage`;
6. image-size/VINTF/SELinux/linker/install audits from actual output;
7. staged physical H1A1000 bring-up;
8. source-built RED-compatible kernel as the final kernel milestone.

## Recovery rule

After interruption, do **not** infer state from chat prose. Read this marker, then the last numbered action file, verify device/vendor branch heads and permanent CI, then resume from the external `m nothing` gate above unless a newer numbered action exists.
