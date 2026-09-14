# RED Hydrogen One LineageOS 22.2 project state

Last updated: 2026-09-14.

This is the current status for `device/red/hydrogenone`. Detailed stock evidence,
generated audits and historical worklogs remain under `docs/`.

## Target and authority

- Device: RED Hydrogen One H1A1000 (`hydrogenone`), Qualcomm MSM8998.
- Target: LineageOS 22.2 / Android 15 / API 35.
- Sole stock authority: `H1A1000.082ho.01.00.10r.118`, Android 9 / API 28.
- First API level: 27.
- Stock archive SHA-256:
  `7277a1accf9595bb727f2189863cf5f6249dd99322e2953432bca6e448365f1e`.
- Stock fingerprint:
  `RED/HydrogenONE/HydrogenONE:9/PKQ1.190118.001/118:userdebug/release-keys`.
- Donor repositories are architecture and adaptation references only.

## Selected repositories

- Device branch: `118-lineage-22.2-kernel-302`.
- Vendor repository: `derveror/proprietary_vendor_red_hydrogenone`, commit
  `b9e652a35e9dd5b5bec3dfa349ca445f62b2b0ef`.
- Kernel repository: `derveror/android_kernel_red_msm8998`, commit
  `a2af472c6545873a1f8884468ea84381d69be21a`.
- Kernel path: `kernel/red/msm8998`.
- Kernel config: `lineageos_hydrogenone_defconfig`.

No RED `msm8998-common` device or vendor repository is used.

## Kernel state

The only LineageOS kernel build input is the RED Linux 4.4.302 source tree. It
builds the four production/PVT variants TM, TM CSP, SIM and JDI with the stock
board/display identities and ordering. The `.118` boot image remains evidence
for boot-header, command-line, DTB and partition constraints; it is not copied
into the product.

SmartPort is excluded. Standard USB, USB-C charging, Bluetooth and normal power
paths remain in scope. RED Leia/display and the stock multi-camera topology
remain in scope.

## Vendor payload and HIDL compatibility

The pinned Android 15 vendor selection contains 474 files. Its
`proprietary-files.txt`, `proprietary-manifest.json` and on-disk payload agree
on all 474 entries. This includes the exact `.118` 64-bit `libssd.so` loaded by
`qseecomd` through `dlopen`; ordinary `DT_NEEDED` analysis does not expose that
runtime dependency. It also contains the exact `.118` SSC sensor payload for
both architectures while retaining the Android 15 source-owned HIDL wrapper.

The platform HIDL base libraries are source-owned and are not selected as RED
prebuilts. Sixty-three exact `.118` HIDL consumers receive the narrow
`libhidlbase_shim` dependency. `imsdatadaemon` is patched from a direct
`libhwbinder.so` dependency to the Android 15 `libhidlbase.so` provider. The
ARM32 camera face-processing blob has only its three verified obsolete symbol
versions cleared. These transformations are reproduced by `extract-files.py`
and pinned in `docs/reference/vendor-hidl-runtime-contract.json`.

## Device/vendor ownership

- Open configuration and source HAL wrappers belong in the device tree.
- Proprietary runtime payload and generated proprietary modules belong in the
  vendor tree.
- Device and vendor copy destinations are checked for collisions.
- Source-owned GNSS, NFC, Wi-Fi, camera and media wrappers must not coexist with
  conflicting proprietary implementations.
- The device extraction list mirrors the current 474-file vendor selection.

## Confirmed static contracts

- `.118` product identity, security patch and partition sizes;
- boot header v1 and recovery-as-boot layout;
- A/B first-stage mounts and Android 15 FBE migration;
- RED UFS paths and firmware mount points;
- DSDS `vendor.qcrild` plus `vendor.qcrild2` startup;
- source-built 4.4.302 kernel path and exact RED DTB set;
- stock `.118` camera topology and chromatix selection;
- exact `.118` audio platform/mixer, six-camera media profiles, NFC base,
  public-library policy, Wi-Fi firmware configuration and key layout;
- source/vendor VINTF and init ownership;
- vendor ELF dependency and fixup registry;
- absence of SmartPort runtime control and kernel prebuilts from this tree.

## Proven build and recovery gates

- Complete LineageOS 22.2 OTA builds passed on 2026-09-13 and, with the SSC
  correction, on 2026-09-14.
- The packaged kernel reports Linux `4.4.302+` and the boot image is below the
  stock 64 MiB partition limit.
- Lineage Recovery boots on the physical H1A1000 with the source-built kernel.
- The QSEE securefs, QTI Keymaster and `/dev/ion` corrections moved normal boot
  past the RED logo to the Lineage boot animation.
- Durable trace v16 contains no kernel panic, GPU fault or hardware watchdog.
  It proves that `system_server` was killed by its software watchdog after two
  66-second waits in `SystemSensorManager.nativeCreate`, while
  `vendor.sensors-hal-1-0` repeatedly reported `Couldn't load sensors module`.
- The exact `.118` SSC module, registry dependencies and configs are now
  restored for arm/arm64. The Android 15 module build, `check_elf_file`, SELinux
  neverallow checks and complete `vendor.img` build pass. The resulting
  `vendor.img` is 319,480,028 bytes against the 1 GiB partition limit. A full
  `mka bacon` and a final incremental rebuild both pass; the final OTA SHA-256
  is `f0b63723a732d16b2e2d6f4b7cb88a84080b7470e45d75f04d1fee83e6c1ecf2`.

Full Android userspace boot and physical-device operation of radio, camera,
audio, sensors, Leia/display, DRM, GNSS, Wi-Fi, Bluetooth, NFC, fingerprint,
power and thermal management remain unproven until the rebuilt OTA is installed
and observed on the phone.

## Next gates

1. Commit and push the verified device-tree SSC correction.
2. Replace the temporary diagnostic boot image only with the verified production
   artifact and install the OTA from physically entered Lineage Recovery.
3. Capture a durable normal-boot trace and verify that the sensor HAL registers
   without another `system_server` watchdog reset.
4. Continue physical subsystem bring-up only after stable Android userspace.
