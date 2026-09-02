# RED Hydrogen One (`hydrogenone`) — LineageOS 22.2

Device configuration for the RED Hydrogen One H1A1000 (Snapdragon 835 / MSM8998), intended for:

```text
device/red/hydrogenone
```

Target userspace is LineageOS 22.2 / Android 15. The canonical hardware and stock-userspace authority for this rework is RED build `H1A1000.082ho.01.00.10r.118` (Android 9), not the older `.109` tree history.

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

First bring-up deliberately uses the exact kernel extracted from the canonical RED `.118` `boot.img`. This preserves RED DTBs and board wiring while userspace is brought up.

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
- kernel payload size `37015950`
- kernel SHA-256 `584ed86bab46bf57c2cd6b6b48ac4026c5d24a70d57bcdd04472d39c5591064d`

`prebuilt/Image.gz-dtb` is regression-tested against that exact size and hash.

`kernel/essential/msm8998` remains a temporary build dependency for generated MSM8998 kernel/UAPI headers used by source-built Qualcomm components. Its Mata kernel image or DTBs are not used as the Hydrogen One boot payload.

The final target remains a source-built RED-capable kernel. The stock prebuilt is a controlled bring-up stage, not the release end state.

### Kernel command line

The Android 15 command line retains RED `.118` hardware/runtime arguments such as `msm_rtb.filter=0x37`, HMP/power-aware scheduler flags and `firmware_class.path=/vendor/firmware_mnt/image`. It also keeps `androidboot.boot_devices=soc/1da4000.ufshc` for modern first-stage block-device discovery.

Stock build/signing identity such as `buildvariant=userdebug` and the stock `veritykeyid` is intentionally not hardcoded into the Android 15 build.

### Radio

Canonical `.118` evidence identifies:

- `persist.radio.multisim.config=dsds`
- modem family `MPSS.AT.2.0...`
- primary `vendor.qcrild`
- DSDS second instance `vendor.qcrild2`

The Android 15 rootdir starts those two qcrild instances. It does not start `vendor.qcrild3` or the legacy `vendor.ril-daemon*` path. The stale `.109` `vendor.rild.libpath` property has been removed.

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
branch: lineage-22.2-android15-contract
```

The exact compatible vendor commit is pinned by:

```text
docs/reference/cross-tree-lock.json
```

Device CI checks out that exact vendor revision and runs the live cross-tree contract. `BoardConfigVendor.mk` and `hydrogenone-vendor.mk` are inherited fail-fast; a build checkout without the required RED vendor tree is not considered a valid full build configuration.

The vendor tree is generated from verified `.118` blobs and has permanent Android 15 contract tests for selected blobs, ELF closure/exceptions, VINTF ownership and P0 daemon requirements.

## Source-side subsystems

The tree contains Android 15 source-side configuration for audio/media, camera configuration, NFC, GNSS/location, overlays, power, rootdir, SELinux, Wi-Fi and RED-specific hardware paths.

Some configuration originated during the older `.109` bring-up. Such files are retained only where current tests/evidence justify them or are explicitly treated as legacy carry-over pending `.118` validation. A historical filename or comment must not be interpreted as `.118` proof.

Narrow `DISABLE_CHECKELF` exceptions in the vendor tree are limited to audited legacy proprietary modules whose ABI behavior cannot be represented by the Android 15 vendor stubs. They are hash/symbol pinned and remain runtime hypotheses until verified on physical hardware; there is no global ELF-check bypass.

## Build

Place the repositories at:

```text
device/red/hydrogenone
vendor/red/hydrogenone
```

Then from a LineageOS 22.2 checkout:

```bash
source build/envsetup.sh
lunch lineage_hydrogenone-userdebug
m nothing
```

The two-component lunch form is valid on LineageOS 22.2; when no release component is supplied the build environment resolves the default release configuration. The device product itself declares `lineage_hydrogenone-user`, `lineage_hydrogenone-userdebug` and `lineage_hydrogenone-eng`.

After `m nothing` is clean, run the image gates explicitly:

```bash
m bootimage
m vendorimage
m systemimage
m target-files-package
m otapackage
```

Do not treat static CI or successful image compilation as proof of a bootable ROM. A new full LineageOS workspace build from the current `.118` branches and physical H1A1000 bring-up are still required.

## Current verification gates

Permanent device CI validates:

- canonical `.118` source locks and stock records
- unit/contract tests
- exact `.118` boot/kernel identity
- radio DSDS/qcrild behavior
- Android 15 fstab and kernel-cmdline contracts
- tree audits and stale-source guards
- live device/vendor cross-tree compatibility against the pinned vendor commit

Permanent vendor CI validates its Android 15 proprietary contract independently.

## Remaining milestones

The current work is not declared release-complete or device-bootable. Major remaining gates are:

1. finish exhaustive `.118` per-file ownership/dependency classification;
2. close remaining evidence gaps such as raw stock boot-ramdisk fstab data;
3. run a clean full LineageOS 22.2 workspace build from the pinned device/vendor revisions;
4. fix build-system failures only from their actual logs;
5. perform staged physical bring-up with logs for kernel/init/mounts/SELinux/graphics/touch/radio;
6. validate P1 hardware (telephony/IMS, Wi-Fi, Bluetooth, GNSS, sensors, fingerprint, camera, NFC, audio, thermal/suspend, A/B OTA/recovery);
7. validate RED-specific P2 hardware such as Leia display/3D and SmartPort;
8. replace the transitional prebuilt kernel with a validated source-built RED kernel.

## Dependencies

`lineage.dependencies` declares the LineageOS legacy Qualcomm SELinux tree and the maintained Essential MSM8998 kernel source needed for current build plumbing. The RED boot payload remains the exact verified `.118` prebuilt until the source-kernel milestone is completed.
