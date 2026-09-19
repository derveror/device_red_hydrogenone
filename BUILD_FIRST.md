# First LineageOS 22.2 build gate — RED Hydrogen One

This file is the current entrypoint for the first complete-workspace build attempt.

## Authoritative inputs

- Target: LineageOS `lineage-22.2` / Android 15.
- Device tree: `device/red/hydrogenone` from branch `118-lineage-22.2-kernel-302`.
- Vendor tree: `vendor/red/hydrogenone` from branch `lineage-22.2-kernel-302` and the exact commit pinned in `docs/reference/cross-tree-lock.json`.
- Kernel tree: `kernel/red/msm8998` from `derveror/android_kernel_red_msm8998`, branch `lineage-22.2`, at the exact commit pinned in the same lock.
- Stock authority: RED `H1A1000.082ho.01.00.10r.118`.
- Active kernel: source-built RED Linux 4.4.302 with `lineageos_hydrogenone_defconfig` and the exact TM/TM-CSP/SIM/JDI DTB set.

## Clean checkout

A reproducible local-manifest template is checked in at:

```text
docs/manifests/hydrogenone-lineage-22.2.xml
```

After `repo init` for LineageOS 22.2, install that file as a local manifest before `repo sync`. It pins the custom RED vendor and kernel revisions plus the required LineageOS sepolicy project.

## First gate: validate the workspace

From the root of the complete LineageOS source tree:

```bash
bash device/red/hydrogenone/tools/build/run_m_nothing_preflight.sh --validate-only
```

This verifies the required Git checkouts are present and clean and that both the vendor and kernel checkouts exactly match the cross-tree lock. It does not sync, reset, clean, or build anything.

## Second gate: run `m nothing`

Only after validation succeeds:

```bash
bash device/red/hydrogenone/tools/build/run_m_nothing_preflight.sh
```

The script performs exactly:

```bash
source build/envsetup.sh
lunch lineage_hydrogenone-bp1a-userdebug
m nothing
```

and stores the complete build output, revision metadata and exit status under:

```text
out/hydrogenone-build-logs/
```

The first failing `m nothing` log is the authoritative next debugging input. Do not pre-emptively change unrelated HALs or blobs before examining that failure.

Do not use the historical `test/lineage-22.2-bringup`, `work`, or generated
`codex/*` branches for this gate. Those snapshots contain either a late
`PRODUCT_EXTRA_VNDK_VERSIONS` assignment or a VNDK-28 request, both of which
fail before product discovery on LineageOS 22.2. Use the device branch and
exact vendor revision listed above.

The release component is not optional: every Hydrogen One build must use
`lineage_hydrogenone-bp1a-userdebug`. The `bp1a` configuration carries the
project SPL `2026-09-01`. Building with `ap4a` instead produces SPL
`2025-01-05`, and the installed Lineage Recovery rejects that OTA as an
`SPL downgrade`. Verify `PLATFORM_SECURITY_PATCH=2026-09-01` before starting
`m bacon` and verify the same value in the finished OTA metadata before
sideload.

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
