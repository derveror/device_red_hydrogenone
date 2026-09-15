# RED .118 WLAN firmware transport restoration

## Runtime evidence

The source-built `wlan.ko` loads on the physical Hydrogen One, but ICNSS does
not receive the modem firmware-ready event. Comparison with stock `.118`
startup shows that RED starts `vendor.tftp_server` in the core init class. The
modem uses that QRTR transport to fetch `wlanmdsp.mbn` before publishing its WLAN
QMI service.

## Implemented contract

- retain the exact stock `.118` AArch64 `tftp_server`;
- retain its exact private `libqsocket.so` and `libqrtr.so` dependencies;
- start `vendor.tftp_server` with the stock service path, class and user;
- keep all three payloads pinned as P0 by size and SHA-256;
- preserve the source-built Linux 4.4.302 kernel and all existing boot/runtime
  fixes without changing DTS, defconfig or DTB order.

Vendor commit: `d366bcb55dee043b801b86b9adca0f209051e825`.

## Verification

- 92 vendor contract tests pass;
- 164 device contract tests and the full-tree contract pass;
- all 507 proprietary ELF modules retain `check_elf_files`, with zero
  exceptions;
- the packaged transport files match their stock `.118` hashes;
- `tftp_server` is packaged executable and receives the existing Qualcomm
  `rfs_access_exec` SELinux label;
- full `mka bacon` completes successfully for Android 15 / LineageOS 22.2;
- final OTA SHA-256:
  `6c62df4d0879b8958660c2c2dfb870f1bafd379dcab4e0913fc5923e9c9d6d67`.

The OTA has not yet been installed. Wi-Fi recovery is therefore a build-backed
hypothesis, not a physical-device success claim. Bluetooth remains a separate
runtime bring-up item.
