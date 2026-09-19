# RED Hydrogen One (`hydrogenone`) — LineageOS 22.2

Device configuration for the RED Hydrogen One H1A1000 (Snapdragon 835 / MSM8998), intended for:

```text
device/red/hydrogenone
```

Target userspace is LineageOS 22.2 / Android 15. The sole hardware and stock-userspace authority for this rework is RED build `H1A1000.082ho.01.00.10r.118` (Android 9).

Canonical stock archive SHA-256:

```text
7277a1accf9595bb727f2189863cf5f6249dd99322e2953432bca6e448365f1e
```

## Authority and reference policy

RED `.118` controls device-specific facts: boot image layout, partition sizes, stock identity, modem/radio behavior, RED/CloudMinds hardware, firmware and proprietary userspace.

Maintained LineageOS 22.2 MSM8998 trees are architectural references only. Essential PH-1 (`mata`) is the primary reference for MSM8998/A-B/Treble structure; OnePlus 5/5T, Nubia Z17 and Razer Phone are secondary references. Donor-specific hardware payloads are not treated as RED hardware evidence.

Canonical analysis is recorded under:

```text
docs/stock/h1a1000-r118/
```

Important machine-readable contracts include `boot-image-contract.json`, radio evidence, stock inventories and the cross-tree vendor lock.

## Current build contract

### Stock identity

The product compatibility identity is pinned to RED `.118`:

```text
RED/HydrogenONE/HydrogenONE:9/PKQ1.190118.001/118:userdebug/release-keys
```

Verified stock values include:

- Android 9 / SDK 28; first API level 27
- system security patch `2019-04-05`
- vendor security patch `2018-08-05`
- Treble, system-as-root and A/B
- platform `msm8998`

### Boot / kernel

The device now builds its RED-specific Linux 4.4.302 kernel from source:

```text
repository: derveror/android_kernel_red_msm8998
branch: lineage-22.2
path: kernel/red/msm8998
config: lineageos_hydrogenone_defconfig
```

The exact verified kernel commit is recorded in `KERNEL_SOURCE.md` and
`docs/reference/cross-tree-lock.json`. The build uses only the four production/PVT
DTBs (TM, TM CSP, SIM and JDI) in their RED order. SmartPort is intentionally
excluded; RED Leia/display support remains in scope.

Verified boot contract:

- Android boot header v1
- page size 4096
- kernel load address `0x00008000`
- ramdisk address `0x01000000`
- second address `0x00f00000`
- tags address `0x00000100`
- boot partition 64 MiB
- system partition 4 GiB
- vendor partition 1 GiB

The complete source build, DTB decompilation/order checks, appended-image layout,
module build and boot-partition budget have passed. Source-built 4.4.302 commit
`a70742ff` boots Recovery and Android on physical hardware, but live evidence
shows its module loader subtracting the KASLR delta from an already-absolute LLD
CRC. Current commit `bc1283e4` accepts both raw LLD kcrctab entries and the
standard relocated ARM64 form. Its full A/B OTA gates pass; physical Wi-Fi
validation remains.

### Kernel command line

The Android 15 command line retains RED `.118` hardware/runtime arguments such as `msm_rtb.filter=0x37`, HMP/power-aware scheduler flags and `firmware_class.path=/vendor/firmware_mnt/image`. It also keeps `androidboot.boot_devices=soc/1da4000.ufshc` for modern first-stage block-device discovery.

Stock build/signing identity such as `buildvariant=userdebug` and the stock `veritykeyid` is intentionally not hardcoded into the Android 15 build.

### Radio

Canonical `.118` evidence identifies:

- `persist.radio.multisim.config=dsds`
- modem family `MPSS.AT.2.0...`
- primary `vendor.qcrild`
- DSDS second instance `vendor.qcrild2`

The Android 15 rootdir starts those two qcrild instances. It does not start `vendor.qcrild3` or the superseded `vendor.ril-daemon*` path, and it does not advertise `vendor.rild.libpath`.

### Filesystems

The active Android 15 fstab keeps the measured RED UFS partition paths and MSM8998 firmware/persist mounts while using the Android 15 migration contract:

- A/B first-stage mounts for system and vendor
- userdata migrated to FBE with `fileencryption=ice` and quota
- modem at `/vendor/firmware_mnt`
- Bluetooth firmware at `/vendor/bt_firmware`
- DSP at `/vendor/dsp`
- persist at `/mnt/vendor/persist`

`rootdir/etc/fstab.qcom` and recovery fstab are regression-tested as one mount contract. Raw `.118` boot-ramdisk fstab extraction is still a separate evidence gap; the Android 15 FBE configuration is therefore a deliberate migration decision, not a claim that stock Android 9 used identical flags.

## Vendor tree

The proprietary tree is required and is expected at:

```text
vendor/red/hydrogenone
```

The current Android 15 vendor contract lives in:

```text
derveror/proprietary_vendor_red_hydrogenone
branch: lineage-22.2-kernel-302
```

The exact compatible vendor commit is pinned by:

```text
docs/reference/cross-tree-lock.json
```

Device CI checks out that exact vendor revision and runs the live cross-tree contract. `hydrogenone-vendor.mk` is inherited fail-fast, so a build checkout without the required RED vendor tree is not considered a valid full build configuration. The generated `BoardConfigVendor.mk` is deliberately not included: its obsolete Android 9 VNDK-28 request is invalid in LineageOS 22.2, while the required recovery compatibility library is selected explicitly from the available VNDK v32 prebuilts.

The vendor tree is generated from verified `.118` blobs and has permanent Android 15 contract tests for selected blobs, ELF closure/exceptions, VINTF ownership and P0 daemon requirements.

## Source-side subsystems

The tree contains Android 15 source-side configuration for audio/media, camera configuration, NFC, GNSS/location, overlays, power, rootdir, SELinux, Wi-Fi and RED-specific hardware paths.

Every retained hardware configuration is now classified against canonical `.118` evidence, the pinned vendor payload, or the RED source kernel. Historical filenames and comments are not accepted as hardware proof.

Narrow `DISABLE_CHECKELF` exceptions in the vendor tree are limited to audited legacy proprietary modules whose ABI behavior cannot be represented by the Android 15 vendor stubs. They are hash/symbol pinned and remain runtime hypotheses until verified on physical hardware; there is no global ELF-check bypass.

## Build

Place the repositories at:

```text
device/red/hydrogenone
vendor/red/hydrogenone
kernel/red/msm8998
```

Then from a LineageOS 22.2 checkout:

```bash
source build/envsetup.sh
lunch lineage_hydrogenone-bp1a-userdebug
m nothing
```

The explicit `bp1a` release component is required by the current LineageOS 22.2
build environment. The device product declares `user`, `userdebug` and `eng`
variants with that release token.

This is a hard build invariant, not a selectable release flavor. Hydrogen One
`userdebug` builds always use `lineage_hydrogenone-bp1a-userdebug`, whose
platform SPL is `2026-09-01`. Do not substitute `ap4a`: it emits SPL
`2025-01-05`, and the installed Lineage Recovery aborts the OTA as an
`SPL downgrade`. Check `PLATFORM_SECURITY_PATCH` after `lunch` and
`post-security-patch-level` in the finished OTA before sideload.

After `m nothing` is clean, run the image gates explicitly:

```bash
m bootimage
m vendorimage
m systemimage
m target-files-package
m otapackage
```

Do not treat static CI or successful image compilation as proof of a bootable
ROM. The next candidate must be built from the pinned `.118` branches through
the normal Clang 19/LLVM/LLD path and physically validated.

## Current verification gates

Permanent device CI validates:

- canonical `.118` source locks and stock records
- unit/contract tests
- stock-authoritative boot geometry and the pinned RED source-kernel identity
- exact TM/TM-CSP/SIM/JDI DTB selection and source-kernel workspace revision
- radio DSDS/qcrild behavior
- Android 15 fstab and kernel-cmdline contracts
- tree audits and stale-source guards
- live device/vendor cross-tree compatibility against the pinned vendor commit

Permanent vendor CI validates its Android 15 proprietary contract independently.

## Remaining milestones

The current work is not declared release-complete. Major remaining gates are:

1. install the verified `bc1283e4` OTA only with explicit user approval while
   preserving the working slot;
2. capture the first Wi-Fi enable attempt with kernel and Android logs;
3. verify `wlan.ko` loads, ICNSS reaches firmware-ready and a WLAN interface is
   created before changing any other subsystem;
4. validate P1 hardware (telephony/IMS, Wi-Fi, Bluetooth, GNSS, sensors,
   fingerprint, camera, NFC, audio, thermal/suspend, A/B OTA/recovery);
5. validate RED-specific display/Leia behavior; SmartPort remains explicitly
   out of scope;
6. iterate only from captured evidence, one proven blocker at a time.

## Dependencies

`lineage.dependencies` declares the LineageOS legacy Qualcomm SELinux tree and
the RED MSM8998 kernel repository at `kernel/red/msm8998`. The local manifest
and cross-tree lock pin the exact verified source-kernel revision.
