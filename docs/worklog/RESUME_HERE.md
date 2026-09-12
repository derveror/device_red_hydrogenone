# ASSISTANT RESUME MARKER — Hydrogen One LineageOS 22.2

Read this file first after interruption.

## Current checkpoints

- Device: `derveror/device_red_hydrogenone`, branch
  `118-lineage-22.2-kernel-302`.
- Vendor: `derveror/proprietary_vendor_red_hydrogenone`, commit
  `70276f1d7ea9d70b04dd91c04b9a48c13f6795b8`.
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
- Vendor tree owns 459 selected proprietary files.
- Stock HIDL base libraries are source-owned, with narrow compatibility fixups
  for verified `.118` consumers.

## Verification boundary

Repository tests and static contracts do not prove a successful ROM build or
boot. From a clean complete workspace run:

```bash
bash device/red/hydrogenone/tools/build/run_m_nothing_preflight.sh --validate-only
bash device/red/hydrogenone/tools/build/run_m_nothing_preflight.sh
```

Then advance through `bootimage`, `vendorimage`, `systemimage`, target-files and
OTA. Fix only failures observed in current build or physical-device logs.
