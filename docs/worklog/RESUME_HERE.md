# ASSISTANT RESUME MARKER — Hydrogen One LineageOS 22.2

Read this file first after interruption.

## Current checkpoints

- Device: `derveror/device_red_hydrogenone`, branch
  `118-lineage-22.2-kernel-302`; the radio/camera runtime restoration has passed
  its complete build and artifact gates and is published on the named branch.
- Vendor: `derveror/proprietary_vendor_red_hydrogenone`, branch
  `lineage-22.2-kernel-302`, commit
  `d366bcb55dee043b801b86b9adca0f209051e825`.
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
- Vendor tree owns 662 selected proprietary files, including the exact `.118`
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
  transport (`tftp_server`, `libqsocket.so`, `libqrtr.so`) and starts it in the
  core init class so the modem can fetch `wlanmdsp.mbn` before ICNSS reports
  firmware-ready. Physical Wi-Fi validation is still required.
- The current vendor selection contains 662 files and 507 proprietary ELF
  modules; all 507 have checkelf enabled and zero exceptions. Extraction now
  replays the complete Android 15 compatibility pipeline automatically.
- The latest full `mka bacon` build passes SELinux/neverallow, VINTF, partition
  size and ZIP integrity checks. Its artifacts are:
  - OTA `lineage-22.2-20260915-UNOFFICIAL-hydrogenone.zip`, 851,086,541 bytes,
    SHA-256 `6c62df4d0879b8958660c2c2dfb870f1bafd379dcab4e0913fc5923e9c9d6d67`;
  - production `boot.img`, 32,403,456 bytes, SHA-256
    `b076a961e93a8b6e0bb6ecd6f1853bd80c483a69fe8a4dfc338edc4653f6f584`;
  - `vendor.img`, 333,439,208 bytes, SHA-256
    `aa1ca0228d019916527d912cd672a5cb7dd6bb7d1df475473c890bbbe0c3b198`.
- The latest changes do not touch DTS, defconfig, DTB order, display,
  touchscreen, recovery or boot-image layout. They add only the stock
  core-class WLAN TFTP service to the existing device init file.
- Only the user can enter Lineage Recovery physically; never issue
  `adb reboot recovery` or `fastboot reboot recovery` on this device.
- No command may flash or reboot the phone without a new explicit user request.
  The next runtime gate is a user-controlled install followed by Wi-Fi,
  Bluetooth, camera/flashlight, USB and boot-log validation.
