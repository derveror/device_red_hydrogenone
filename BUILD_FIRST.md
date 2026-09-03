# First LineageOS 22.2 build gate — RED Hydrogen One

This file is the current entrypoint for the first complete-workspace build attempt. It replaces the older `.109` / `m bacon` bring-up instructions.

## Authoritative inputs

- Target: LineageOS `lineage-22.2` / Android 15.
- Device tree: `device/red/hydrogenone` from branch `lineage-22.2-stock118-rework`.
- Vendor tree: `vendor/red/hydrogenone` from the exact commit pinned in `docs/reference/cross-tree-lock.json`.
- Stock authority: RED `H1A1000.082ho.01.00.10r.118`.
- Transitional boot kernel: the exact `.118` 4.4.153+ `Image.gz-dtb` already checked into `prebuilt/Image.gz-dtb` and regression-tested by SHA-256.

The final milestone remains a validated source-built RED kernel; the `.118` prebuilt is intentionally limited to userspace/boot bring-up.

## Clean checkout

A reproducible local-manifest template is checked in at:

```text
docs/manifests/hydrogenone-lineage-22.2.xml
```

After `repo init` for LineageOS 22.2, install that file as a local manifest before `repo sync`. It pins the custom RED vendor revision and the required LineageOS kernel/sepolicy projects.

## First gate: validate the workspace

From the root of the complete LineageOS source tree:

```bash
bash device/red/hydrogenone/tools/build/run_m_nothing_preflight.sh --validate-only
```

This verifies the required Git checkouts are present and clean and that the vendor checkout exactly matches the cross-tree lock. It does not sync, reset, clean, or build anything.

## Second gate: run `m nothing`

Only after validation succeeds:

```bash
bash device/red/hydrogenone/tools/build/run_m_nothing_preflight.sh
```

The script performs exactly:

```bash
source build/envsetup.sh
lunch lineage_hydrogenone-userdebug
m nothing
```

and stores the complete build output, revision metadata and exit status under:

```text
out/hydrogenone-build-logs/
```

The first failing `m nothing` log is the authoritative next debugging input. Do not pre-emptively change unrelated HALs or blobs before examining that failure.

## Later gates

Do not move to these until `m nothing` is GREEN:

```text
bootimage
vendorimage
systemimage
target-files-package
otapackage
```

After the build gates are GREEN, proceed to staged physical-device bring-up and collect kernel/init/first-stage mount/SELinux/linker logs before hardware-subsystem iteration.

## Flashing boundary

The device is A/B. Before destructive physical testing, preserve recovery paths and stock critical partitions/slot state. Do not substitute a donor boot image, donor DTB, or donor firmware for the canonical RED `.118` evidence.
