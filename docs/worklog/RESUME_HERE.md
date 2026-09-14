# ASSISTANT RESUME MARKER — Hydrogen One LineageOS 22.2

Read this file first after interruption.

## Current checkpoints

- Device: `derveror/device_red_hydrogenone`, branch
  `118-lineage-22.2-kernel-302`; the radio/camera runtime restoration has passed
  its complete build and artifact gates and is published on the named branch.
- Vendor: `derveror/proprietary_vendor_red_hydrogenone`, branch
  `lineage-22.2-kernel-302`, commit
  `4dce3edee53619e1d1cd15182c6189f3208f283c`.
- Kernel: `derveror/android_kernel_red_msm8998`, commit
  `aba534bba4e9d779245ee077e83bb99a9522d24d`.
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
- Vendor tree owns 659 selected proprietary files, including the exact `.118`
  `libssd.so` required by the SSD QSEE listener and the physically verified
  RED `.118` QTI Keymaster and SSC sensor stacks.
- Stock HIDL base libraries are source-owned, with narrow compatibility fixups
  for verified `.118` consumers.

## Current runtime checkpoint

- The source-built Linux `4.4.302+` kernel boots Lineage Recovery and LineageOS
  22.2 reaches the setup/system UI on the physical H1A1000; touchscreen input is
  confirmed working.
- The installed build still has no working Wi-Fi, Bluetooth, camera/flashlight,
  or USB data/ADB connection. Those are runtime observations, not build claims.
- The new uninstalled candidate restores the exact Bluetooth Cherokee property
  and source `libbt-vendor`, the stock persist-backed WLAN MAC link, the RED
  camera power ABI, and a byte-verified 185-file stock `.118` production camera
  closure. SmartPort remains excluded.
- The current vendor selection contains 659 files and 504 proprietary ELF
  modules; all 504 have checkelf enabled and zero exceptions. Extraction now
  replays the complete Android 15 compatibility pipeline automatically.
- The latest full `mka bacon` build passes SELinux/neverallow, VINTF, partition
  size and ZIP integrity checks. Its artifacts are:
  - OTA `lineage-22.2-20260914-UNOFFICIAL-hydrogenone.zip`, 851,032,189 bytes,
    SHA-256 `5e0c2bfef452332f0239026c53034512b196e09916b03d763c31d4dd96cc26e2`;
  - production `boot.img`, 32,403,456 bytes, SHA-256
    `2ec6064ea4454cbd0a0131a9993f110357126038a904ef6e6c49ade134cc3c5c`;
  - `vendor.img`, 333,304,040 bytes, SHA-256
    `dd5ac315c07174f4d247d3fe02cf6aec5e833d001a67da19a4ca7938163c9d7e`.
- The latest changes do not touch DTS, defconfig, DTB order, display,
  touchscreen, recovery, init ordering, or boot-image layout.
- Only the user can enter Lineage Recovery physically; never issue
  `adb reboot recovery` or `fastboot reboot recovery` on this device.
- No command may flash or reboot the phone without a new explicit user request.
  The next runtime gate is a user-controlled install followed by Wi-Fi,
  Bluetooth, camera/flashlight, USB and boot-log validation.
