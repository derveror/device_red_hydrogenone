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
`0c0351fcfc0a00edece8147403675d3575185e7f`.

The selected list, manifest and on-disk payload each contain 712 entries. Stock
copies of `libhidlbase`, `libhidltransport` and `libhwbinder` are pruned because
the Android 15 source tree owns those providers. Sixty-three exact `.118` HIDL
consumers receive `libhidlbase_shim`; `imsdatadaemon` is retargeted from
`libhwbinder.so` to `libhidlbase.so`. The Android 15 QCRIL override includes one
coherent FP3 QMI generation and the matching version-10 database. The identities
and operations are pinned in the source lock, ELF audit, extraction manifest and
fixup registries.

## Current repository gates

- canonical stock identity and boot contracts;
- source kernel and four-DTB contract;
- radio, fstab, camera, init and VINTF static contracts;
- device/vendor copy ownership;
- reproducible 712-file extraction list and compatibility fixups;
- rejection of superseded stock identity and raw reference trees;
- rejection of SmartPort runtime control and kernel prebuilts.

The current device-vs-stock configuration audit covers 86 device-owned vendor
copy mappings: 74 are byte-identical at the same destination, seven are
documented Android 15 adaptations and five are source-only or use a different
Lineage destination. No mapped device source is missing.

## Current runtime proof and remaining gates

A complete LineageOS 22.2 OTA build has succeeded, and the source-built Linux
`4.4.302+` kernel boots Lineage Recovery on the physical H1A1000. A durable
normal-boot trace exposed a boot-critical stock dependency absent from the
initial selection: `qseecomd` loads `libssd.so` with `dlopen` and exits before
publishing `vendor.sys.listeners.registered` when that SSD listener is missing.

Physical trace v7 verifies that the rebuilt vendor image's `.118` `libssd.so`
correction works: `qseecomd` remains running and publishes its listener-ready
property in 39 ms. The trace then exposed an omitted RED policy rule: enforcing
SELinux denied `init` the `mounton` permission when mounting the `.118` `cmlog`
securefs partition at `/mnt/vendor/persist/data`. The physical filesystem holds
the expected `keymaster64` state, while Keymaster exited and vold waited in
`cryptfs enablefilecrypto` when the mount was absent.

The device policy now restores the exact stock `.118`
`allow init persist_drm_file:dir mounton;` permission. The resulting complete
OTA passes Android SELinux/neverallow, VINTF and integrity checks. Update Engine
successfully wrote and verified that OTA on slot `A`, but its normal-boot test
remained at the RED logo for at least 150 seconds without ADB or fastboot.
This physical symptom was investigated with durable trace v8. The corrected
securefs mount, qseecomd and `/data` mount all succeeded, but the generic
MSM8998 Keymaster repeatedly exited. A read-only system chroot captured its
failed attempt to open absent
`/vendor/firmware_mnt/image/keymaster.mdt` firmware.

Hydrogen One instead carries Keymaster firmware in dedicated A/B raw
partitions. The exact RED `.118` QTI service/implementation was tested in the
same chroot with the generic implementation absent. It opened QSEECom/ION,
completed TrustZone requests, registered `IKeymasterDevice/default`, and
remained running with LineageOS 22.2's source-built `libion`. That controlled
test applied the stock device-node modes manually.

After installing the QTI-Keymaster OTA, durable physical trace v11 proved that
the bootloader-preloaded `keymaster64` application is found as QSEE app ID
`65537`, but production Keymaster fails before its first ION/QSEE command. The
curated `ueventd.rc` had omitted the stock `.118`
`/dev/ion 0664 system system` rule, leaving the node `0600 root:root`. The rule
is now restored with a regression contract. The rebuilt OTA passes all tree
tests, full Android build, filesystem, VINTF and ZIP-integrity checks, and the
final sparse vendor image contains the exact rule. A physical normal-boot test
reached the Lineage boot animation. Durable trace v16 then proved that the
kernel remained alive while `vendor.sensors-hal-1-0` repeatedly failed with
`Couldn't load sensors module`. `system_server` blocked twice for 66 seconds in
`SystemSensorManager.nativeCreate` and was killed by its software watchdog.

The vendor selection now contains the exact stock `.118` arm/arm64 SSC module,
its registry and low-latency dependencies, `libsdsprpc`, and the two stock sensor
configs. Device init boots SLPI and runs the stock registry control plane while
the Android 15 source-owned HIDL wrapper remains selected. All four proprietary
modules pass Android 15 ELF checks in both architectures, and the complete
vendor image passes SELinux and partition-size checks. The sensor-corrected full
OTA and final incremental rebuild pass, including ZIP integrity, VINTF, the
source-built `4.4.302+` kernel and the exact four-DTB order. A subsequent
physical test reached the LineageOS setup/system UI and confirmed touchscreen
input. Wi-Fi, Bluetooth, camera/flashlight and USB data/ADB remained unavailable
in that installed build.

Physical testing now confirms touchscreen, Wi-Fi on 2.4/5 GHz, camera preview
and still capture, flashlight, USB debugging and normal Android boot. The
source-built kernel and device-specific recovery remain unchanged. Bluetooth
is still a separate unresolved runtime gate.

The first Android 15 QCRIL candidate published framework-supported radio HALs
but still exposed no baseband, IMEI or SIM. Live traces proved missing
`qmux_radio` and radio-data init state caused both QCRIL instances to crash;
after recreating the exact stock runtime contract, DMS initialization failed
with QMI client error `-17`. This identified a mixed QCRIL/QMI ABI generation.
The next candidate uses the byte-identical FP3 QMI closure and version-10 QCRIL
database shared by four maintained MSM8998 references, while preserving RED
`.118` modem firmware and device configuration. The full OTA, VINTF, ELF and
tree tests pass. Runtime baseband, IMEI, SIM, calls and data validation remains
required; no radio success is declared from build proof alone.
