# ASSISTANT RESUME MARKER — Hydrogen One LineageOS 22.2

Read this file first after interruption.

## Current checkpoints

- Device: `derveror/device_red_hydrogenone`, branch
  `118-lineage-22.2-kernel-302`; the radio/camera runtime restoration has passed
  its complete build and artifact gates and is published on the named branch.
- Vendor: `derveror/proprietary_vendor_red_hydrogenone`, branch
  `lineage-22.2-kernel-302`, commit
  `f5192d041cb9bc914b5e438c1fc54c1aae7f8891`.
- Kernel: `derveror/android_kernel_red_msm8998`, commit
  `a70742ff9578d6aa0201f66a389659386c716f10`.
- Stock authority: `H1A1000.082ho.01.00.10r.118`.
- Stock archive SHA-256:
  `7277a1accf9595bb727f2189863cf5f6249dd99322e2953432bca6e448365f1e`.

## Fixed architecture decisions

- Target LineageOS 22.2 / Android 15 / API 35.
- Kernel build input is `kernel/red/msm8998`, Linux 4.4.302.
- Exact RED DTBs: TM, TM CSP, SIM and JDI.
- No RED `msm8998-common` repositories.
- SmartPort excluded; standard USB/Bluetooth/charging and Leia/display retained.
- Device tree owns open configuration and source wrappers.
- Vendor tree owns 663 selected proprietary files, including the exact `.118`
  `libssd.so` required by the SSD QSEE listener and the physically verified
  RED `.118` QTI Keymaster and SSC sensor stacks.
- Stock HIDL base libraries are source-owned, with narrow compatibility fixups
  for verified `.118` consumers.

## Current runtime checkpoint

- The source-built Linux `4.4.302+` kernel boots Lineage Recovery and LineageOS
  22.2 reaches the setup/system UI on the physical H1A1000; touchscreen input is
  confirmed working.
- The installed build boots to Android with touchscreen, camera, flashlight and
  USB debugging working. Wi-Fi and Bluetooth remain unavailable; those are
  runtime observations, not build claims.
- The new uninstalled candidate restores the exact Bluetooth Cherokee property
  and source `libbt-vendor`, the stock persist-backed WLAN MAC link, the RED
  camera power ABI, and a byte-verified 185-file stock `.118` production camera
  closure. SmartPort remains excluded.
- The installed candidate includes the exact RED `.118` QRTR/TFTP transport
  (`qrtr-ns`, `tftp_server`, `libqsocket.so`, `libqrtr.so`). Runtime evidence
  reaches modem WLAN service publication, then the `f3819ee` kernel rejects
  `wlan.ko` at `module_layout` under KASLR/MODVERSIONS.
- Current kernel commit `a70742ff9578d6aa0201f66a389659386c716f10`
  restores the upstream ARM64 kcrctab relocation contract. It is now present
  in a clean complete LineageOS boot/OTA artifact, but that artifact has not
  been tested on the phone.
- The current vendor selection contains 663 files and 508 proprietary ELF
  modules; all 508 have checkelf enabled and zero exceptions. Extraction now
  replays the complete Android 15 compatibility pipeline automatically.
- The superseded installed-candidate build embeds kernel `f3819ee`, not
  `a70742ff`. Its historical artifacts are:
  - OTA `lineage-22.2-20260915-UNOFFICIAL-hydrogenone.zip`, 851,038,702 bytes,
    SHA-256 `bcb028f8137fbd370354ac2e65fe172c9f017299a6efa343de247b25dc21f51f`;
  - production `boot.img`, 32,403,456 bytes, SHA-256
    `7f62ec5933809d2031b30b9530e3dadd43d7160641c51d624b299e7efde56e30`;
  - `vendor.img`, 333,463,784 bytes, SHA-256
    `6745d19884af9eaf5ebd2274304eabbaaaab8ac6521c625bdd632f8a320f3d3a`.
- The `a70742ff` kernel change does not touch DTS, defconfig, DTB order,
  display, touchscreen, recovery or boot-image layout. It restores only the
  ARM64 KASLR/module-CRC relocation contract.
- The current clean `a70742ff` build completed with `mka bacon -j8`. It passes
  VINTF (`COMPATIBLE`), partition-size, SignApk/ZIP, boot-payload, exact
  four-DTB, module-strip and 435/435 CRC gates. Current artifacts are:
  - OTA `lineage-22.2-20260915-UNOFFICIAL-hydrogenone.zip`, 851,026,784 bytes,
    SHA-256 `3b54b9dfa3b16291a9b84cea390155f94b3b4b8b50ed3df1b40386addc49b4f1`;
  - `boot.img`, 32,403,456 bytes, SHA-256
    `c67f079d1ece6a39a6d436d100a50d943e51a053f648892c3f1da265598a6132`;
  - `vendor.img`, 333,467,880 bytes, SHA-256
    `ed83894f4ddb10b51c65791d1e9f8609d6ca1d3ac4524603a32df6879f300f0b`.
  Full build evidence is in
  `docs/worklog/2026-09-15/0004-arm64-kcrctab-clean-build.md`.
- Only the user can enter Lineage Recovery physically; never issue
  `adb reboot recovery` or `fastboot reboot recovery` on this device.
- No command may flash or reboot the phone without a new explicit user request.
  The clean build and exact kernel/module/DTB/boot verification gate is now
  complete. The next gate is a user-controlled recovery install and physical
  runtime collection; build success alone does not prove Wi-Fi or Bluetooth.
