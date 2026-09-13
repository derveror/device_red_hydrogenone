# RED Hydrogen One LineageOS 22.2 project state

Last updated: 2026-09-13.

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
  `a6560ec388398760f3d45e7634ba23c89f4a2eb6`.
- Kernel repository: `derveror/android_kernel_red_msm8998`, commit
  `440e8eb4eea36404d340a2a4ad001cf013304447`.
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

The pinned Android 15 vendor selection contains 460 files. Its
`proprietary-files.txt`, `proprietary-manifest.json` and on-disk payload agree
on all 460 entries. This includes the exact `.118` 64-bit `libssd.so` loaded by
`qseecomd` through `dlopen`; ordinary `DT_NEEDED` analysis does not expose that
runtime dependency.

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
- The device extraction list mirrors the current 460-file vendor selection.

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

- A complete LineageOS 22.2 OTA build completed successfully on 2026-09-13.
- The packaged kernel reports Linux `4.4.302+` and the boot image is below the
  stock 64 MiB partition limit.
- Lineage Recovery boots on the physical H1A1000 with the source-built kernel.
- A durable normal-boot trace reached Android init and identified `qseecomd`
  exiting with status 255 before publishing
  `vendor.sys.listeners.registered`.
- The rebuilt vendor image now contains the exact `.118` `libssd.so` and mounts
  the dedicated `cmlog` securefs partition before starting `qseecomd`.

The QSEE correction has built and passed static/image verification but has not
yet been installed on the phone. Full Android userspace boot and physical-device
operation of radio, camera, audio, sensors, Leia/display, DRM, GNSS, Wi-Fi,
Bluetooth, NFC, fingerprint, power, thermal management and OTA remain unproven.

## Next gates

1. Install the verified 2026-09-13 OTA from Lineage Recovery.
2. Attempt normal boot without overwriting the recoverable alternate slot.
3. Capture another durable boot trace if Android userspace still does not start.
4. Validate installed VINTF, SELinux, linker namespaces and image sizes.
5. Continue physical subsystem bring-up only after a stable userspace boot.
