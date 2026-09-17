# RED Hydrogen One LineageOS 22.2 project state

Last updated: 2026-09-17.

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
  `0c0351fcfc0a00edece8147403675d3575185e7f`.
- Kernel repository: `derveror/android_kernel_red_msm8998`, commit
  `2fb7457475a6fb2de07ea603717dac6a83eecb1a`.
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

The device extraction list contains 712 files. It includes the RED `.118`
selection, the Android 15 QCRIL interface closure, one coherent FP3 QMI
generation and the matching QCRIL database plus every upgrade from version 0
through version 10. The stock manifest, each reference override and every
transformed hash are recorded separately so the origin of each file remains
explicit. The stock selection includes the exact
`.118` 64-bit `libssd.so` loaded by `qseecomd` through `dlopen`; ordinary
`DT_NEEDED` analysis does not expose that runtime dependency. It also contains
the exact `.118` SSC sensor payload for both architectures while retaining the
Android 15 source-owned HIDL wrapper.

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
- The device extraction list mirrors the current 712-file vendor selection.

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

- Complete LineageOS 22.2 OTA builds passed on 2026-09-13 through 2026-09-16.
- The packaged kernel reports Linux `4.4.302+` and the boot image is below the
  stock 64 MiB partition limit.
- Lineage Recovery boots on the physical H1A1000 with the source-built kernel.
- The QSEE securefs, QTI Keymaster, `/dev/ion` and SSC corrections allow normal
  Android userspace to reach setup/system UI. Touchscreen, flashlight, USB
  debugging and normal Android boot have been confirmed on the physical phone.
- Wi-Fi is runtime-verified on 2.4 GHz and 5 GHz. Browser traffic no longer
  triggers the qcacld TSO spinlock reboot after the production lock
  initialization fix.
- Camera preview and still capture are runtime-verified for both front and rear
  sensors. Aperture receives a successful JPEG callback and saves each image;
  the earlier frozen shutter and missing-file failure is no longer reproduced.
- The earlier WLAN failure was traced to a `wlan.ko` `module_layout` CRC
  mismatch. Dynamic debug proved the kernel computed `0xffffffe183b71df1`
  while the module required `0x13d71df1`; the Clang/LLD vmlinux stores the raw
  CRC and has no relocation for that kcrctab entry.
- Current kernel commit `2fb7457475a6fb2de07ea603717dac6a83eecb1a`
  accepts either the exact raw CRC emitted by LLD or the standard relocated
  ARM64 form used by other link paths. It keeps `wlan.ko` external like stock
  `.118`; maintained MSM8998 references instead avoid this loader path by
  building qcacld into the kernel.

Bluetooth and the remaining hardware subsystems retain their own runtime
validation gates.

The first Android 15 QCRIL candidate was installed and published supported
IRadio 1.4 and RadioConfig 1.1 interfaces, but physical testing still showed an
unknown baseband, no IMEI and no SIM. Runtime traces proved two independent
causes. The Android 15 init tree did not create the stock-required
`/dev/socket/qmux_radio` and `/data/vendor/radio` state, so both `qcrild`
instances repeatedly crashed in `QtiBusSocketTransport::clientLoop()`. Creating
those paths live kept both daemons stable for more than 120 seconds. The next
failure was `qmi_client_init_instance returned (-17) for DMS`; `-17` is the QMI
client parameter error and exposed the mixed QCRIL/QMI generations.

Vendor commit `0c0351fcfc0a00edece8147403675d3575185e7f` replaces that mixed
closure with the byte-identical FP3 QMI set shared by the maintained Mata,
Cheryl, Nubia and OnePlus MSM8998 references, packages its version-10 database,
and bridges the retained RED IMS-private IDL to its matching stock provider.
The device init now reproduces the required QtiBus socket, radio-data directory,
database flags and MBN-copy completion trigger.

The corrected candidate completed the normal Clang 19/LLVM/LLD
`mka bacon -j7` path on 2026-09-17. VINTF is compatible, all device and vendor
contract tests pass, and the installed image contains the expected QMI hashes,
database upgrades and init directives. Its artifacts are:

- OTA `lineage-22.2-20260917-UNOFFICIAL-hydrogenone.zip`, 858,334,655 bytes,
  SHA-256 `6a78e95d96a3d0e1c9b8fd9cdb6fb78b49e89edb04d1c75f0dcb6b977a920224`;
- `boot.img`, 32,403,456 bytes, SHA-256
  `c89def7c5a2f8d7296966d9c56dcb38ce279b08928111eca2eccc36d54cecf90`;
- `vendor.img`, 369,557,736 bytes, SHA-256
  `137409e2129fe179c65ca847287231af0e36e028014aca47d7f3f416a4425773`.

This corrected radio candidate has not yet been installed. Baseband, IMEI, SIM,
calls and data remain physical runtime gates; build success is not reported as
a radio fix.

## Next gates

1. Install the corrected radio candidate only after a separate explicit user
   request, preserving the known-working slot as fallback.
2. Verify baseband, IMEI, SIM detection, calls/data and the absence of Android
   15 unsupported-radio-HAL errors while confirming Wi-Fi and camera regressions
   have not been introduced.
3. Diagnose Bluetooth separately after the radio result is known.
