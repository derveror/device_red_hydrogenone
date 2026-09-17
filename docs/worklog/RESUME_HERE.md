# ASSISTANT RESUME MARKER — Hydrogen One LineageOS 22.2

Read this file first after interruption.

## Repository authority

- Device: `derveror/device_red_hydrogenone`, branch
  `118-lineage-22.2-kernel-302`.
- Vendor: `derveror/proprietary_vendor_red_hydrogenone`, branch
  `lineage-22.2-kernel-302`, commit
  `0c0351fcfc0a00edece8147403675d3575185e7f`.
- Kernel: `derveror/android_kernel_red_msm8998`, branch `lineage-22.2`, commit
  `2fb7457475a6fb2de07ea603717dac6a83eecb1a`.
- Stock authority: `H1A1000.082ho.01.00.10r.118`.
- Stock archive SHA-256:
  `7277a1accf9595bb727f2189863cf5f6249dd99322e2953432bca6e448365f1e`.

Do not create new branches. Do not change the kernel branch unless a diagnosed
kernel defect requires it. Never issue a reboot, flash or sideload command
without a new explicit user approval. Only the user can enter Lineage Recovery
reliably using the hardware buttons; never run `adb reboot recovery` or
`fastboot reboot recovery`.

## Fixed architecture decisions

- Target LineageOS 22.2 / Android 15 / API 35.
- Kernel input is `kernel/red/msm8998`, Linux `4.4.302+`.
- Exact RED DTBs: TM, TM CSP, SIM and JDI.
- No RED `msm8998-common` repositories and no prebuilt kernel.
- SmartPort excluded; standard USB/Bluetooth/charging and Leia/display retained.
- Device tree owns open configuration and source wrappers; vendor tree owns
  proprietary runtime payload.
- RED `.118` controls device-specific firmware and configuration. Mata, Cheryl,
  OnePlus and Nubia are compatibility references, not device identity sources.

## Confirmed physical runtime state

- Lineage Recovery and LineageOS boot with the source-built kernel.
- Touchscreen, USB debugging, flashlight and normal Android boot work.
- Wi-Fi works on 2.4 and 5 GHz after the WLFW transport and kernel CRC fixes.
- Front/rear camera preview and still JPEG capture work.
- Bluetooth remains unresolved.
- The previously installed radio candidate exposes IRadio 1.4 and RadioConfig
  1.1, but baseband remains unknown and IMEI/SIM are absent.

## Radio diagnosis completed

The missing baseband/IMEI is not the original Android 15 unsupported-HAL error:
the compatible interfaces are now published. Both `vendor.qcrild` processes
instead crashed in `QtiBusSocketTransport::clientLoop()` because the Android 15
init tree did not create `/dev/socket/qmux_radio`.

A reversible live test created `/dev/socket/qmux_radio` as `radio:radio`, mode
`2770`, and `/data/vendor/radio` as `system:radio`, mode `0770`, with the stock
SELinux contexts. `/dev/socket/qmux_radio/ril_ipc` appeared and both QCRIL
instances stayed stable for more than 120 seconds. This proves the missing init
runtime contract caused the crash loop.

After QtiBus stabilized, QCRIL failed DMS initialization with
`qmi_client_init_instance returned (-17)`. Qualcomm defines `-17` as
`QMI_CLIENT_PARAM_ERR`. The Android 15 QCRIL had been mixed with the older RED
QMI client/IDL generation.

All four maintained MSM8998 reference vendor trees carry byte-identical FP3
6.A.025.0 QMI libraries and the same version-10 QCRIL database. Vendor commit
`0c0351fcfc0a00edece8147403675d3575185e7f` now packages that coherent closure,
the database and upgrades 0 through 10. The retained RED 64-bit IMS-private IDL
is linked to stock `lib-imsrcsbaseimpl.so`, its verified symbol provider; no
undefined-symbol bypass is used. Device init permanently creates the QtiBus
and radio-data state and reproduces the database/MBN-copy flags.

## Current candidate

The corrected candidate completed `mka bacon -j7`; VINTF is compatible, all 112
vendor tests, all 179 device unit tests and the full-tree audit pass. The
installed output contains the exact expected QMI hashes, all QCRIL database
upgrades, the IMS provider bridge and the new init contract.

- OTA: `lineage-22.2-20260917-UNOFFICIAL-hydrogenone.zip`, 858,334,655 bytes,
  SHA-256 `6a78e95d96a3d0e1c9b8fd9cdb6fb78b49e89edb04d1c75f0dcb6b977a920224`.
- `boot.img`: 32,403,456 bytes, SHA-256
  `c89def7c5a2f8d7296966d9c56dcb38ce279b08928111eca2eccc36d54cecf90`.
- `vendor.img`: 369,557,736 bytes, SHA-256
  `137409e2129fe179c65ca847287231af0e36e028014aca47d7f3f416a4425773`.

This candidate has not been installed. Do not claim the radio fixed from build
evidence. The next gate, only after explicit user approval, is recovery
sideload followed by baseband, IMEI, SIM, calls/data and Wi-Fi/camera regression
checks.
