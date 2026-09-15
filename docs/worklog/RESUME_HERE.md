# ASSISTANT RESUME MARKER — Hydrogen One LineageOS 22.2

Read this file first after interruption.

## Current checkpoints

- Device: `derveror/device_red_hydrogenone`, branch
  `118-lineage-22.2-kernel-302`; the radio/camera runtime restoration has passed
  its complete build and artifact gates and is published on the named branch.
- Vendor: `derveror/proprietary_vendor_red_hydrogenone`, branch
  `lineage-22.2-kernel-302`, commit
  `f99b7f3f6c284ac418eda689a4f89e556fb33069`.
- Kernel: `derveror/android_kernel_red_msm8998`, commit
  `f3819ee742506ded5da6b0cb65a0b47b5fc63ef6`.
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
- The new uninstalled Wi-Fi candidate adds the exact RED `.118` QRTR/TFTP
  transport (`qrtr-ns`, `tftp_server`, `libqsocket.so`, `libqrtr.so`). The
  stock `vendor.qrtr-ns` core service starts before TFTP so the modem can
  publish WLAN QMI and fetch `wlanmdsp.mbn` before ICNSS reports
  firmware-ready. Physical Wi-Fi validation is still required.
- The current vendor selection contains 663 files and 508 proprietary ELF
  modules; all 508 have checkelf enabled and zero exceptions. Extraction now
  replays the complete Android 15 compatibility pipeline automatically.
- The latest full `mka bacon` build passes SELinux/neverallow, VINTF, partition
  size and ZIP integrity checks. Its artifacts are:
  - OTA `lineage-22.2-20260915-UNOFFICIAL-hydrogenone.zip`, 851,038,702 bytes,
    SHA-256 `bcb028f8137fbd370354ac2e65fe172c9f017299a6efa343de247b25dc21f51f`;
  - production `boot.img`, 32,403,456 bytes, SHA-256
    `7f62ec5933809d2031b30b9530e3dadd43d7160641c51d624b299e7efde56e30`;
  - `vendor.img`, 333,463,784 bytes, SHA-256
    `6745d19884af9eaf5ebd2274304eabbaaaab8ac6521c625bdd632f8a320f3d3a`.
- The latest changes do not touch DTS, defconfig, DTB order, display,
  touchscreen, recovery or boot-image layout. They add only the stock
  core-class QRTR name service before the existing WLAN TFTP service.
- Only the user can enter Lineage Recovery physically; never issue
  `adb reboot recovery` or `fastboot reboot recovery` on this device.
- No command may flash or reboot the phone without a new explicit user request.
  The next runtime gate is a user-controlled install followed by Wi-Fi,
  Bluetooth, camera/flashlight, USB and boot-log validation.
