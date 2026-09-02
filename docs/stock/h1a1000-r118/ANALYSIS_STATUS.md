# RED Hydrogen One `.118` analysis / LineageOS 22.2 bring-up status

**Target:** LineageOS 22.2 / Android 15 / API 35  
**Canonical stock:** `H1A1000.082ho.01.00.10r.118` / Android 9 / API 28, first API 27  
**Stock archive SHA-256:** `7277a1accf9595bb727f2189863cf5f6249dd99322e2953432bca6e448365f1e`  
**Current state:** canonical stock intake and major P0 static contracts are pinned; full Lineage workspace compilation and physical-device bring-up remain pending.

## Verified stock identity

| Field | Canonical `.118` value |
|---|---|
| Build ID | `PKQ1.190118.001` |
| Display ID | `H1A1000.082ho.01.00.10r.118` |
| Incremental | `118` |
| Android / SDK | `9` / `28` |
| First API level | `27` |
| System security patch | `2019-04-05` |
| Vendor security patch | `2018-08-05` |
| Type / tags | `userdebug` / `release-keys` |
| Fingerprint | `RED/HydrogenONE/HydrogenONE:9/PKQ1.190118.001/118:userdebug/release-keys` |
| Device / model | `HydrogenONE` / `H1A1000` |
| Platform | `msm8998` |
| Layout | Treble, system-as-root, A/B |

The active Lineage product/build contract now uses the `.118` fingerprint and vendor security patch instead of the older `.109` identity.

## Stock filesystem and dependency intake

The canonical stock analysis currently records:

| Partition | Objects | Regular | Directories | Symlinks | Regular bytes | ELF |
|---|---:|---:|---:|---:|---:|---:|
| system | 4,828 | 3,951 | 620 | 257 | 3,701,404,141 | 2,108 |
| vendor | 3,666 | 3,314 | 130 | 222 | 639,476,061 | 2,805 |

Additional completed intake includes:

- 4,913 distinct regular ELF files: 2,997 ELF32 and 1,916 ELF64;
- 37,285 `DT_NEEDED` edges with zero `readelf` failures in the inventory pass;
- 195 APK and 118 JAR containers validated;
- 127 rc files, 286 service definitions, 582 action blocks and 18 imports parsed;
- 594 property definitions / 289 unique keys;
- 33 SELinux/policy files and 4,250 context entries inventoried;
- 85 firmware files totaling 136,691,149 bytes;
- 14 kernel-module paths reducing to 11 unique hashes.

This is substantial structural/dependency evidence, but exhaustive Android 15 ownership/consumer classification for every stock path is not yet complete.

## Boot / partition contract — DONE and pinned

Canonical `.118` `boot.img` and partition metadata are recorded in `boot-image-contract.json`.

Verified values:

- boot image SHA-256 `8e120a2920f5d4eec65cb5929d31fe271738af85b218d5adb96035eb28806af6`;
- Android boot header v1, header size 1,648, page size 4,096;
- kernel load address `0x00008000`;
- ramdisk address `0x01000000`;
- second address `0x00f00000`;
- tags address `0x00000100`;
- boot partition 64 MiB;
- system partitions 4 GiB;
- vendor partitions 1 GiB;
- kernel payload size 37,015,950;
- kernel payload SHA-256 `584ed86bab46bf57c2cd6b6b48ac4026c5d24a70d57bcdd04472d39c5591064d`;
- ramdisk size 9,466,573;
- ramdisk SHA-256 `7be9e9c0eedcb38aa8829ccd94a8813b082d7760de93a56b9b35e7175a070767`.

The active `prebuilt/Image.gz-dtb` is the exact canonical `.118` kernel and is regression-tested by size and SHA. The older `.109` 4.4.78 kernel is no longer the active bring-up payload.

The final milestone is still a source-built RED-capable kernel; the `.118` prebuilt remains a controlled transitional bring-up choice.

## Kernel command line — DONE as Android 15 migration contract

The active BoardConfig retains verified RED `.118` hardware/runtime arguments including:

- `msm_rtb.filter=0x37`;
- `sched_enable_hmp=1`;
- `sched_enable_power_aware=1`;
- `firmware_class.path=/vendor/firmware_mnt/image`.

It also keeps `androidboot.boot_devices=soc/1da4000.ufshc` for Android 15 first-stage device discovery.

Stock build/signing identity (`buildvariant=userdebug`, stock `veritykeyid`) is intentionally not hardcoded.

## Radio startup contract — DONE statically

Canonical `.118` evidence established:

- `persist.radio.multisim.config=dsds`;
- modem token `MPSS.AT.2.0.c4-00988-8998_GEN_PACK-1`;
- stock shell startup path for `vendor.qcrild`;
- DSDS second instance `vendor.qcrild2`.

The active Android 15 rootdir starts exactly the primary and second qcrild instances. It does not start `vendor.qcrild3` or the legacy `vendor.ril-daemon*` path. The stale `.109` `vendor.rild.libpath` property has been removed.

This proves the static startup choice, not successful modem registration/voice/data/IMS on physical hardware.

## Filesystem / encryption contract — DONE as Android 15 migration contract

The active fstab is regression-tested for:

- RED UFS partition paths;
- A/B first-stage system/vendor mounts;
- userdata FBE using `fileencryption=ice` and quota;
- modem -> `/vendor/firmware_mnt`;
- Bluetooth firmware -> `/vendor/bt_firmware`;
- DSP -> `/vendor/dsp`;
- persist -> `/mnt/vendor/persist`;
- removable SD/USB and zram support;
- identical recovery/runtime fstab source.

This is an intentional Android 15 migration contract. Raw `.118` boot-ramdisk fstab extraction is still an evidence gap, so no claim is made that stock Android 9 used identical userdata flags.

## Vendor tree / cross-tree contract — DONE for current static gate

The Android 15 proprietary tree is required at:

```text
vendor/red/hydrogenone
```

Current compatible vendor revision is pinned by `docs/reference/cross-tree-lock.json`:

```text
repository: derveror/proprietary_vendor_red_hydrogenone
commit: d30ac19025b348ca61535afaaecb23b95347b2f4
branch lineage: lineage-22.2-android15-contract
```

Device makefiles now inherit the vendor tree fail-fast rather than allowing a misleading source-only full product configuration.

Permanent device CI performs a live checkout of the exact pinned vendor commit and validates the cross-tree contract. Permanent vendor CI independently validates its Android 15 proprietary contract, including selected blobs, ELF audit/exception policy, VINTF ownership and P0 daemon requirements.

## VINTF / init / P0 ownership — STATIC CONTRACT IN PLACE

Stock Android 9 VINTF/init data has been analyzed as evidence rather than copied wholesale. The current device/vendor trees have static contract tests for Android 15 ownership, selected service declarations, P0 providers and cross-tree collisions.

Stock evidence includes RED-specific Leia/CloudMinds declarations and Qualcomm legacy HAL families. These remain subject to subsystem-by-subsystem Android 15/runtime validation; passing static ownership tests does not prove every HAL can register successfully on-device.

## Current permanent verification gates

Device CI currently covers:

- source/archive locks and canonical `.118` records;
- unit and tree-contract tests;
- exact `.118` boot/header/kernel contract;
- partition sizes;
- `.118` product identity and vendor patch level;
- qcrild/DSDS startup contract;
- kernel command-line migration contract;
- Android 15 fstab migration contract;
- device/vendor configuration provenance guards;
- stale-source / duplicate-install audits;
- live compatibility against the pinned vendor commit.

Vendor CI independently covers the proprietary Android 15 contract.

These gates are static/repository gates. They are not substitutes for a full Lineage build or a booted phone.

## Still pending before the port can be called build- and boot-ready

### P0 build gates

1. Run a clean LineageOS 22.2 workspace with the pinned device/vendor revisions:
   - `source build/envsetup.sh`
   - `lunch lineage_hydrogenone-userdebug`
   - `m nothing`
2. Fix only failures produced by that current build.
3. Pass explicit image/package targets:
   - `m bootimage`
   - `m vendorimage`
   - `m systemimage`
   - `m target-files-package`
   - `m otapackage`
4. Check final image sizes, installed VINTF, SELinux policy compilation, linker namespaces and duplicate module/install paths from actual build output.

### P0 physical bring-up

5. Boot on the H1A1000 with stock critical partitions/slot state recoverable.
6. Capture kernel/init/first-stage mount/SELinux/zygote/SurfaceFlinger/adb logs.
7. Establish stable boot, display, touch, userdata/FBE, USB, charging, reboot and basic Wi-Fi/audio.

### P1 hardware validation

8. Validate cellular registration, SMS, calls, data and IMS behavior.
9. Validate Bluetooth, GNSS, sensors, fingerprint, camera/video, NFC, power/thermal, suspend, battery/charging, recovery and A/B OTA.

### P2 RED-specific hardware

10. Validate Leia/4-View display stack, RED-specific display firmware/framework behavior, SmartPort, special camera topology and RED haptics/accessories.

### Final kernel milestone

11. Replace the transitional exact `.118` prebuilt kernel with a validated source-built RED kernel/DTB configuration without losing RED panel, touch, fingerprint, audio, haptics, SmartPort and other board-specific hardware.

## Evidence-completeness work that remains in parallel

- finish per-file Android 15 ownership classification for the complete system/vendor inventory;
- map every retained proprietary blob to an actual init/HAL/framework/ELF consumer;
- document final linker namespace and destination partition decisions;
- close raw boot-ramdisk fstab evidence;
- continue replacing any legacy `.109` carry-over configuration only when `.118` or runtime evidence supports the replacement.

## Bottom line

The rework is no longer the old `.109` donor-heavy tree: canonical `.118` boot identity, kernel, radio startup, vendor pinning and major Android 15 static contracts are now enforced by tests. The next decisive proof is a **fresh full LineageOS 22.2 build from these exact branches**, followed by staged physical-device bring-up. No claim is made yet that the resulting ROM boots successfully on the H1A1000.
