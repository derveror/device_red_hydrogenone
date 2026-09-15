# RED Hydrogen One LineageOS 22.2 project state

Last updated: 2026-09-15.

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
  `f99b7f3f6c284ac418eda689a4f89e556fb33069`.
- Kernel repository: `derveror/android_kernel_red_msm8998`, commit
  `f3819ee742506ded5da6b0cb65a0b47b5fc63ef6`.
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

The pinned Android 15 vendor selection contains 663 files. Its
`proprietary-files.txt`, `proprietary-manifest.json` and on-disk payload agree
on all 663 entries. This includes the exact `.118` 64-bit `libssd.so` loaded by
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
- The device extraction list mirrors the current 663-file vendor selection.

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

- Complete LineageOS 22.2 OTA builds passed on 2026-09-13 and 2026-09-14; the
  WLAN transport candidate completed a fresh full build on 2026-09-15.
- The packaged kernel reports Linux `4.4.302+` and the boot image is below the
  stock 64 MiB partition limit.
- Lineage Recovery boots on the physical H1A1000 with the source-built kernel.
- The QSEE securefs, QTI Keymaster, `/dev/ion` and SSC corrections allow normal
  Android userspace to reach setup/system UI. Touchscreen, camera, flashlight
  and USB debugging have been confirmed on the physical phone.
- The installed build still lacks Wi-Fi and Bluetooth. Runtime comparison with
  stock `.118` identified the missing boot-time QRTR name service: without it
  the modem never publishes WLAN QMI and ICNSS remains before firmware-ready.
- The new candidate contains exact `.118` `qrtr-ns`, `tftp_server`,
  `libqsocket.so` and `libqrtr.so` payloads. It starts `vendor.qrtr-ns` before
  `vendor.tftp_server` with the stock credentials and capability. All 508
  proprietary ELF checks are enabled with zero exceptions. The complete build
  passes SELinux/neverallow, VINTF and ZIP integrity checks. Its
  333,463,784-byte `vendor.img` is below the 1 GiB limit; the OTA SHA-256 is
  `bcb028f8137fbd370354ac2e65fe172c9f017299a6efa343de247b25dc21f51f`.

Physical Wi-Fi recovery from this candidate is not yet proven. Bluetooth and
the remaining hardware subsystems retain their own runtime validation gates.

## Next gates

1. Install the WLAN transport OTA only after a separate explicit user request,
   preserving the known-working slot as fallback.
2. Capture early boot and Wi-Fi logs and verify `vendor.qrtr-ns`,
   `vendor.tftp_server`, modem WLAN QMI service publication, ICNSS
   firmware-ready and interface creation.
3. Diagnose Bluetooth separately after the Wi-Fi result is known.
