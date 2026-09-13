# ASSISTANT RESUME MARKER — Hydrogen One LineageOS 22.2

Read this file first after interruption.

## Current checkpoints

- Device: `derveror/device_red_hydrogenone`, branch
  `118-lineage-22.2-kernel-302`.
- Vendor: `derveror/proprietary_vendor_red_hydrogenone`, commit
  `a6560ec388398760f3d45e7634ba23c89f4a2eb6`.
- Kernel: `derveror/android_kernel_red_msm8998`, commit
  `440e8eb4eea36404d340a2a4ad001cf013304447`.
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
- A full LineageOS 22.2 build completed successfully on 2026-09-13.
- The first normal-boot trace showed `qseecomd` repeatedly exiting with status
  255 and init blocked on `vendor.sys.listeners.registered`.
- RED `.118` `qseecomd` requires `libssd.so` through `dlopen`; the rebuilt vendor
  image now contains the exact blob.
- The device rootdir now mounts `/dev/block/bootdevice/by-name/cmlog` at
  `/mnt/vendor/persist/data` before `post-fs` starts `qseecomd`, matching stock
  `.118` ordering.
- This rebuilt OTA is statically verified but has not yet been installed on the
  phone. The next gate is a controlled sideload from the already working
  Lineage Recovery followed by one normal-boot attempt.
