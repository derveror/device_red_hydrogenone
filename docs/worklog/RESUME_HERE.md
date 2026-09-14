# ASSISTANT RESUME MARKER — Hydrogen One LineageOS 22.2

Read this file first after interruption.

## Current checkpoints

- Device: `derveror/device_red_hydrogenone`, branch
  `118-lineage-22.2-kernel-302`; the RED `.118` SSC sensor correction has passed
  its complete build and artifact gates and is ready for commit/push.
- Vendor: `derveror/proprietary_vendor_red_hydrogenone`, branch
  `lineage-22.2-kernel-302`, commit
  `b9e652a35e9dd5b5bec3dfa349ca445f62b2b0ef`.
- Kernel: `derveror/android_kernel_red_msm8998`, commit
  `a2af472c6545873a1f8884468ea84381d69be21a`.
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
- Vendor tree owns 474 selected proprietary files, including the exact `.118`
  `libssd.so` required by the SSD QSEE listener and the physically verified
  RED `.118` QTI Keymaster and SSC sensor stacks.
- Stock HIDL base libraries are source-owned, with narrow compatibility fixups
  for verified `.118` consumers.

## Current runtime checkpoint

- The source-built Linux `4.4.302+` kernel boots Lineage Recovery on H1A1000.
- Earlier traces fixed the missing RED `.118` `libssd.so` dependency and the
  `cmlog` securefs `mounton` policy.
- Durable traces v10/v11 prove that Linux `4.4.302+` does not panic, qseecomd
  becomes ready, persist/cmlog and `/data` mount, and the bootloader-preloaded
  `keymaster64` app is visible as QSEE app ID `65537`.
- v11 isolates the remaining failure before the first ION/QSEE command. The
  curated production `ueventd.rc` omitted `/dev/ion`, leaving it
  `0600 root:root`; the exact RED `.118` rule is
  `/dev/ion 0664 system system`. The controlled Recovery chroot had succeeded
  only after that stock mode was applied manually.
- The device tree now restores the stock ION rule and has a regression test.
  This moved normal boot to the Lineage animation.
- Durable trace v16 then isolated the current failure: the kernel remains alive,
  but `vendor.sensors-hal-1-0` cannot load a sensor module. `system_server`
  blocks twice for 66 seconds in `SystemSensorManager.nativeCreate`, and its
  software watchdog restarts Android userspace.
- The vendor tree now restores the exact stock `.118` arm/arm64 `sensors.ssc`,
  `libsensor_reg`, `libsns_low_lat_stream_stub`, `libsdsprpc` and two sensor
  configs. Device init boots SLPI and runs the stock sensor registry control
  plane while the Android 15 source HIDL wrapper remains authoritative.
- All four new modules pass Android 15 ELF checking for both architectures;
  the complete vendor image and SELinux neverallow checks pass. Full and final
  incremental `mka bacon` builds pass. The final artifacts are:
  - OTA `lineage-22.2-20260914-UNOFFICIAL-hydrogenone.zip`, 853,047,186 bytes,
    SHA-256 `f0b63723a732d16b2e2d6f4b7cb88a84080b7470e45d75f04d1fee83e6c1ecf2`;
  - production `boot.img`, 32,391,168 bytes, SHA-256
    `5103376dc9bcd01a9de65c2f4d4398130b14948fe16fabe72a4eef3a7063c5c4`;
  - `vendor.img`, 319,480,028 bytes, SHA-256
    `8f28010a5d99d5bf5df7e8a313650d9d7f8e913ad0b0b7ed0a579459c23928d2`.
- Device unit tests: 146 PASS; vendor tests: 84 PASS; full-tree and
  cross-tree ownership contracts: PASS. The production kernel is `4.4.302+`,
  has the exact four-DTB order and contains no v16 diagnostic marker.
- The phone is currently in physically entered Lineage Recovery on slot `A`.
  `boot_a` contains the temporary v16b diagnostic image and must be replaced by
  a verified production artifact before the normal-boot test.
- Only the user can enter Lineage Recovery physically; never issue
  `adb reboot recovery` or `fastboot reboot recovery` on this device.
- Do not commit the isolated diagnostic kernel worktree or claim a complete
  Android boot before the sensor-corrected physical result.
- The next gate is device commit/push, then sideload from physically entered
  Recovery and one observed normal-boot attempt.
