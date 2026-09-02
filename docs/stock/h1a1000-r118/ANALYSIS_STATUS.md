# RED Hydrogen One `.118` stock analysis status

**Target:** LineageOS 22.2 / Android 15 / API 35  
**Stock:** Android 9 / API 28, first API 27  
**Status:** acquisition and structural inventory complete; per-file Android 15 ownership classification in progress

## Verified build identity

| Field | Stock value |
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

## Filesystem inventory

| Partition | Objects | Regular | Directories | Symlinks | Regular bytes | ELF |
|---|---:|---:|---:|---:|---:|---:|
| system | 4,828 | 3,951 | 620 | 257 | 3,701,404,141 | 2,108 |
| vendor | 3,666 | 3,314 | 130 | 222 | 639,476,061 | 2,805 |

Every indexed object has partition-relative path, object type, mode, UID/GID, inode/link metadata, size, original symlink target, file type, and SHA-256 where applicable. The full TSV inventories are stored compressed in the analysis evidence bundle.

## Partition and boot contract

- Qualcomm UFS layout spans LUN0–LUN5 with 4,096-byte sectors.
- 81 partition definitions and 203 rawprogram entries were normalized.
- `system_a/b` are 4 GiB each; `vendor_a/b` are 1 GiB each; `boot_a/b` are 64 MiB each.
- Both slots receive system, vendor, boot, modem/DSP/Bluetooth, and boot-chain payloads.
- `boot.img` uses boot header v1, page size 4,096, kernel size 37,015,950, ramdisk size 9,466,573, header OS 9.0 and patch level 2019-04.
- The kernel is Linux 4.4.153+, built with GCC 4.9; IKCONFIG is present.
- 57 appended DTBs were identified; 22 are explicit CloudMinds/RED JDI/TM/SIM EVT/DVT/PVT variants.

Confirmed kernel/DTB hardware evidence includes FPC fingerprint, Synaptics and Cypress touch variants, TFA98xx audio amplifiers, TI LM36923H backlight, `cloudminds,smartport`, a 4,510 mAh battery profile, PMIC LRA haptics, and RED display identifiers.

## Vendor runtime contract

- Vendor VINTF manifest target level: 3.
- 73 vendor HAL package names and 95 normalized vendor fqname rows.
- Important stock contracts include audio/effect 4.0, fingerprint 2.1, camera provider 2.4 `legacy/0`, graphics 2.x, keymaster 3.0, NFC 1.1, radio 1.1 dual-slot, sensors 1.0, soundtrigger 2.1, Wi-Fi 1.2, and Qualcomm radio/IMS/display/location families.
- RED-specific declarations include `vendor.cm.hardware.thermal3d@1.0` and `vendor.leia.hardware.leiadisp@1.0`.
- The exact manifest is evidence only: obsolete or unsupported Android 9 declarations will not be copied blindly into Android 15.

## Init, properties, SELinux, and packages

- 127 rc files, 286 service definitions, 582 action blocks, and 18 imports were parsed.
- 271 service definitions belong to the active system+vendor runtime set.
- 231 referenced executables resolve; 40 do not. Thirteen non-disabled missing executables demonstrate that the stock package itself contains stale init references.
- 594 property definitions produce 289 unique keys; 207 keys are defined more than once and seven have conflicting values.
- 4,913 distinct regular ELF files were analyzed: 2,997 ELF32 and 1,916 ELF64, with 37,285 `DT_NEEDED` edges and zero `readelf` failures. Ten unresolved `libgcc.so` edges are confined to ADSP RFSA payloads.
- 195 APK and 118 JAR containers were validated. There are 76 privileged APKs and 31 distinct v1 signing certificates.
- 33 SELinux/policy files and 4,250 context entries were inventoried. Compiled Android 9 policy is evidence only; Android 15 policy must be recreated as source and pass current neverallows.

## Firmware and modules

- 85 firmware files totaling 136,691,149 bytes were classified by source partition.
- RED-named payload includes `qtc800h.bin`, `qtc800h_8998_660.bin`, `qtc800s_dsp.bin`, `leia_pfp_470.fw`, and `leia_pm4_470.fw`.
- 14 kernel-module paths reduce to 11 unique hashes; all carry vermagic `4.4.153+ SMP preempt mod_unload modversions aarch64`.
- Duplicates across system/vendor exist for `qca_cld3_wlan.ko`, `wil6210.ko`, and `msm_11ad_proxy.ko`.

## Current tree audit

The existing 423-file Hydrogen One tree contains:

- 248 files identical at the same path to donor device content;
- 42 files modified from donor paths;
- only 70 files identical to `.118` stock evidence;
- 93 proprietary-list entries, 91 of which exist in `.118` stock and two of which do not.

This confirms that the current tree remains historical input and must not be treated as a completed RED-derived Android 15 tree.

## Remaining work before tree rewrite is considered evidence-complete

1. Classify every system/vendor path into AOSP-built, RED proprietary, firmware/config, obsolete/debug, or prohibited per-device data.
2. Resolve each retained blob to an actual init/HAL/framework/ELF consumer.
3. Decide Android 15 destination partition and linker namespace for every proprietary module.
4. Replace stale Android 9 init/VINTF/property/SELinux assumptions with Android 15 contracts.
5. Generate a complete `proprietary-files.txt`, blob-fixup set, and reproducible `vendor/red/hydrogenone` tree.
6. Rebuild `device/red/hydrogenone` from measured partition/boot/hardware facts, flattening only justified donor-common configuration.
7. Validate through clean `m nothing`, image targets, VINTF, enforcing SELinux, first boot, and hardware tests.

No claim is made yet that the final device/vendor trees are complete or bootable from this new stock analysis.
