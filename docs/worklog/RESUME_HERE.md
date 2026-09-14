# ASSISTANT RESUME MARKER — Hydrogen One LineageOS 22.2

Read this file first after interruption.

## Current checkpoints

- Device: `derveror/device_red_hydrogenone`, branch
  `118-lineage-22.2-kernel-302`; the RED `.118` ION ueventd fix is built and
  awaiting its physical normal-boot test.
- Vendor: `derveror/proprietary_vendor_red_hydrogenone`, branch
  `lineage-22.2-kernel-302`, commit
  `aa87d1e184ab100547a5cb3262393dd96c5348bc`.
- Kernel: `derveror/android_kernel_red_msm8998`, commit
  `39e74780ffb29d0b6ac30e9d68ae5b1195fe529e`.
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
- Vendor tree owns 464 selected proprietary files, including the exact `.118`
  `libssd.so` required by the SSD QSEE listener and the physically verified
  RED `.118` QTI Keymaster stack.
- Stock HIDL base libraries are source-owned, with narrow compatibility fixups
  for verified `.118` consumers.

## Current runtime checkpoint

- The source-built Linux `4.4.302+` kernel boots Lineage Recovery on H1A1000.
- The first normal-boot trace showed `qseecomd` repeatedly exiting with status
- Earlier traces fixed the missing RED `.118` `libssd.so` dependency and the
  `cmlog` securefs `mounton` policy. The resulting QTI-Keymaster OTA installed
  successfully on slot `B` but still remained at the RED logo.
- Durable traces v10/v11 prove that Linux `4.4.302+` does not panic, qseecomd
  becomes ready, persist/cmlog and `/data` mount, and the bootloader-preloaded
  `keymaster64` app is visible as QSEE app ID `65537`.
- v11 isolates the remaining failure before the first ION/QSEE command. The
  curated production `ueventd.rc` omitted `/dev/ion`, leaving it
  `0600 root:root`; the exact RED `.118` rule is
  `/dev/ion 0664 system system`. The controlled Recovery chroot had succeeded
  only after that stock mode was applied manually.
- The device tree now restores the stock ION rule and has a regression test.
  All 141 tests, the full-tree contract and full `mka bacon` pass. The rule was
  verified inside the final sparse `vendor.img`; no diagnostic markers are in
  the production kernel.
- New OTA: `lineage-22.2-20260914-UNOFFICIAL-hydrogenone.zip`, SHA-256
  `483a69f65e0b6166460b9df9e33c04835e88a899227e88c8c3c86ef4e6212186`.
- Production `boot_b` was restored from the verified full 64 MiB backup after
  diagnostic v11; slot `B` is active/bootable with retry count seven. The
  phone is currently in Lineage Recovery on slot `B`.
- Only the user can enter Lineage Recovery physically; never issue
  `adb reboot recovery` or `fastboot reboot recovery` on this device.
- The next gate is commit/push, sideload of the rebuilt ION-fix OTA, then one
  normal-boot test. Do not claim a complete Android boot before that result.
