# ASSISTANT RESUME MARKER — Hydrogen One LineageOS 22.2

Read this file first after interruption.

## Current checkpoints

- Device: `derveror/device_red_hydrogenone`, branch
  `118-lineage-22.2-kernel-302`.
- Vendor: `derveror/proprietary_vendor_red_hydrogenone`, commit
  `a6560ec388398760f3d45e7634ba23c89f4a2eb6`.
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
- Vendor tree owns 460 selected proprietary files, including the exact `.118`
  `libssd.so` required by the SSD QSEE listener.
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
- The following slot-`A` normal boot did not complete. The phone remained on
  the RED logo for at least 150 seconds with neither ADB nor fastboot visible
  and did not automatically return to the bootloader during observation.
- The phone was last observed at the RED logo. Only the user can enter Lineage
  Recovery physically; never issue `adb reboot recovery` or
  `fastboot reboot recovery` on this device.
- The next gate is a new durable normal-boot trace from slot `A`. Do not change
  another runtime component or claim Android boot until that evidence is read.
