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
  `bc1283e4bf00425cf60f43d549f49ff26bf7474e`.
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
  reaches modem WLAN service publication, then the `a70742ff` kernel rejects
  `wlan.ko` at `module_layout` under KASLR/MODVERSIONS.
- Dynamic debug reports `0xffffffe183b71df1` versus module `0x13d71df1`.
  The exact LLD vmlinux stores raw `0x13d71df1` with no relocation for that
  kcrctab entry, proving that unconditional KASLR subtraction corrupts it.
- Current kernel commit `bc1283e4bf00425cf60f43d549f49ff26bf7474e`
  accepts both the raw LLD CRC and the standard relocated ARM64 form. Its
  source tests and normal LLD boot-image gates pass; it has not been installed.
- The current vendor selection contains 663 files and 508 proprietary ELF
  modules; all 508 have checkelf enabled and zero exceptions. Extraction now
  replays the complete Android 15 compatibility pipeline automatically.
- The earlier superseded candidate embeds kernel `f3819ee`. Its historical
  artifacts are:
  - OTA `lineage-22.2-20260915-UNOFFICIAL-hydrogenone.zip`, 851,038,702 bytes,
    SHA-256 `bcb028f8137fbd370354ac2e65fe172c9f017299a6efa343de247b25dc21f51f`;
  - production `boot.img`, 32,403,456 bytes, SHA-256
    `7f62ec5933809d2031b30b9530e3dadd43d7160641c51d624b299e7efde56e30`;
  - `vendor.img`, 333,463,784 bytes, SHA-256
    `6745d19884af9eaf5ebd2274304eabbaaaab8ac6521c625bdd632f8a320f3d3a`.
- The installed `a70742ff` build artifacts are:
  - OTA `lineage-22.2-20260915-UNOFFICIAL-hydrogenone.zip`, 851,026,784 bytes,
    SHA-256 `3b54b9dfa3b16291a9b84cea390155f94b3b4b8b50ed3df1b40386addc49b4f1`;
  - `boot.img`, 32,403,456 bytes, SHA-256
    `c67f079d1ece6a39a6d436d100a50d943e51a053f648892c3f1da265598a6132`;
  - `vendor.img`, 333,467,880 bytes, SHA-256
    `ed83894f4ddb10b51c65791d1e9f8609d6ca1d3ac4524603a32df6879f300f0b`.
- The `bc1283e4` kernel change does not touch DTS, defconfig, DTB order,
  display, touchscreen, recovery or boot-image layout. It restores only the
  module-CRC comparison so raw and relocated kcrctab formats both work.
- The current `bc1283e4` boot-image build passes the 15,655,357-byte kernel
  payload limit, exact four-DTB order and exact `wlan.ko` CRC gate.
- The full `bc1283e4` A/B OTA build completed with `mka bacon -j8` and VINTF
  `compatible`:
  - OTA `lineage-22.2-20260916-UNOFFICIAL-hydrogenone.zip`, 851,029,208 bytes,
    SHA-256 `d3a582d50980d8d9e9eb1350f8f9ffb535a8d2f4b821209c3962e768de9581dc`;
  - `boot.img`, 32,403,456 bytes, SHA-256
    `1234df9d5112e481a354177467bb513e41c16c7bddf3094677d6acee1a96d854`;
  - kernel payload, 15,655,357 bytes, SHA-256
    `9d066fb204fbce603692fcfb6e3512866da5a163e00dd3814ae2867d9768c150`;
  - packaged `wlan.ko`, 5,660,568 bytes, SHA-256
    `a8126f3fb6c58516a3263a63454f67068035c643682a8f26a630d933a8516c72`.
- Only the user can enter Lineage Recovery physically; never issue
  `adb reboot recovery` or `fastboot reboot recovery` on this device.
- No command may flash or reboot the phone without a new explicit user request.
  The full build and exact kernel/module/DTB/boot verification gate is now
  complete. The next gate is a user-controlled recovery install and physical
  runtime collection; build success alone does not prove Wi-Fi or Bluetooth.
