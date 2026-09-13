# ASSISTANT RESUME MARKER — Hydrogen One LineageOS 22.2

Read this file first after interruption.

## Current checkpoints

- Device: `derveror/device_red_hydrogenone`, branch
  `118-lineage-22.2-kernel-302`.
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
  255 because RED `.118` `libssd.so` was missing. After adding the exact blob,
  physical trace v7 proved that qseecomd stays running and publishes
  `vendor.sys.listeners.registered=true` in 39 ms.
- Trace v7 then proved that enforcing SELinux denied `init` the `mounton`
  permission for `/mnt/vendor/persist/data`. The physical `cmlog` partition
  contains RED securefs state, including `keymaster64`, and its failed mount
  caused Keymaster to exit while vold waited in `cryptfs enablefilecrypto`.
- Device policy now restores the exact stock `.118` permission:
  `allow init persist_drm_file:dir mounton;`.
- The rebuilt OTA passed the complete Android build, SELinux/neverallow, VINTF,
  137 unit tests, full-tree audit and ZIP integrity. Its SHA-256 is
  `6f0d377c91cf8d825f82a16560519750b0123b47ebe6dea684944dce8ebc463f`.
- The corrected OTA was installed successfully from Recovery: Update Engine
  wrote and verified `boot_a`, `system_a` and `vendor_a` and finished with
  status 0. The saved sideload log SHA-256 is
  `56f30165150452c31eb0fd6491b9eea30919e36532607cd6168d00e9a609a0bc`.
- Durable trace v8 proved that the corrected securefs mount succeeds, qseecomd
  remains ready and `/data` mounts, but the generic MSM8998 Keymaster exits
  because it expects absent file-based
  `/vendor/firmware_mnt/image/keymaster.mdt` firmware. This is not a kernel
  panic and is not a Linux 4.4.302 failure.
- A read-only Recovery chroot test proved that the exact RED `.118` QTI
  Keymaster stack instead uses the device's dedicated Keymaster partitions,
  registers `IKeymasterDevice/default`, and remains running with the current
  LineageOS source-built `libion`.
- Device/vendor now select only that QTI stack. Full `mka bacon` passed; the new
  OTA SHA-256 is
  `fb4890863015e01bcf210d12c4ad4b5e1b5b0ff256be0937e8ff698bda2b2f65`.
- Production `boot_a` was restored byte-exactly after diagnostic boot v8. The
  phone is in Lineage Recovery on slot `A`; no phone partition contains the
  temporary chroot overlay.
- Only the user can enter Lineage Recovery physically; never issue
  `adb reboot recovery` or `fastboot reboot recovery` on this device.
- The next gate is one sideload of the new QTI-Keymaster OTA followed by one
  normal-boot test. Do not claim a complete Android boot before that result.
