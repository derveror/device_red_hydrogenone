# RED `.118` analysis and LineageOS 22.2 status

## Canonical identity

| Field | Value |
|---|---|
| Build | `H1A1000.082ho.01.00.10r.118` |
| Build ID | `PKQ1.190118.001` |
| Android / SDK | `9` / `28` |
| First API | `27` |
| System patch | `2019-04-05` |
| Vendor patch | `2018-08-05` |
| Layout | Treble, system-as-root, A/B |

Archive SHA-256:
`7277a1accf9595bb727f2189863cf5f6249dd99322e2953432bca6e448365f1e`.

The stock intake includes verified partition images, build properties, boot
header, DTBs, init/property/VINTF inventories, ELF dependency data, firmware and
kernel-module metadata. Raw proprietary binaries are not duplicated in the
device tree.

## Boot and partition evidence

- Android boot header v1, header size 1,648 and page size 4,096;
- boot partition 64 MiB;
- system partition 4 GiB;
- vendor partition 1 GiB;
- verified kernel and ramdisk hashes in `boot-image-contract.json`;
- verified stock command-line and partition XML records.

The stock boot payload reports Linux 4.4.153+. That fact remains historical
evidence. The LineageOS product instead builds the RED Linux 4.4.302 source tree
from `kernel/red/msm8998`; no stock kernel prebuilt is a build input.

## Runtime contracts

- Android 15 first-stage fstab uses real RED UFS paths and A/B mounts.
- Userdata uses the LineageOS FBE migration contract.
- Stock `.118` radio evidence selects DSDS with `vendor.qcrild` and
  `vendor.qcrild2`.
- The stock camera topology and main/sub chromatix files are hash-pinned.
- The stock audio platform/mixer, six-camera media profiles, power hints,
  public-library policy, WCNSS configuration and key layout are hash-pinned.
- The source NFC HAL receives exact stock `libnfc-nxp_default.conf` content
  under its active `libnfc-nxp.conf` filename.
- Leia/display remains in scope; the rear proprietary accessory port is
  deliberately excluded.

## Vendor payload audit

Pinned vendor commit:
`70276f1d7ea9d70b04dd91c04b9a48c13f6795b8`.

The selected list, manifest and on-disk payload each contain 459 entries. Stock
copies of `libhidlbase`, `libhidltransport` and `libhwbinder` are pruned because
the Android 15 source tree owns those providers. Sixty-three exact `.118` HIDL
consumers receive `libhidlbase_shim`; `imsdatadaemon` is retargeted from
`libhwbinder.so` to `libhidlbase.so`. The identities and operations are pinned
in `docs/reference/vendor-hidl-runtime-contract.json` and the vendor fixup
registries.

## Current repository gates

- canonical stock identity and boot contracts;
- source kernel and four-DTB contract;
- radio, fstab, camera, init and VINTF static contracts;
- device/vendor copy ownership;
- reproducible 459-file extraction list and compatibility fixups;
- rejection of superseded stock identity and raw reference trees;
- rejection of SmartPort runtime control and kernel prebuilts.

The current device-vs-stock configuration audit covers 86 device-owned vendor
copy mappings: 74 are byte-identical at the same destination, seven are
documented Android 15 adaptations and five are source-only or use a different
Lineage destination. No mapped device source is missing.

## Remaining proof

A full clean LineageOS build and physical-device boot have not yet been proven.
The next gates are `m nothing`, individual images, target-files, OTA, installed
VINTF/SELinux/linker inspection and staged H1A1000 testing. No hardware subsystem
is declared working solely from repository-level checks.
