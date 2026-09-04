# Hydrogen One GNSS cheryl ABI design

## Goal
Keep the LineageOS 22.2 / Android 15 GNSS service source-built while exposing the
legacy Qualcomm location ABI required by the canonical RED `.118` Android 9
proprietary location consumers.

## Authority and donor order
1. RED `.118` is hardware, configuration, proprietary payload, firmware and runtime truth.
2. Razer Phone `cheryl` LineageOS 22.2 is the primary GNSS/location source-ABI donor.
3. `mata`, OnePlus msm8998 and Nubia msm8998 are Android 15/platform cross-checks.

`cheryl` is preferred for GNSS because the device ended its official upgrade path
on Android 9 and its maintained LineageOS 22.2 tree still exports the legacy
`LocApiBase`, `MsgTask`, and gps-utils ABI consumed by Pie-era Qualcomm blobs.

## Architecture
- Source-owned: `libgps.utils`, `libloc_core`, `liblocation_api`, `libgnss`,
  `android.hardware.gnss@1.0-impl-qti`, and `android.hardware.gnss@1.0-service-qti`.
- RED proprietary consumers retained: `libloc_api_v02`, `libizat_core`,
  `liblbs_core`, `libdataitems`, `libflp`, `libgeofence`, `liblocationservice`
  and the rest of the selected `.118` location payload.
- RED-owned configuration stays RED-specific; no Razer GPS config is imported.
- The obsolete local GNSS 2.1 frontend and source `libbatching/libgeofencing`
  generation are removed so there is only one active Qualcomm location ABI.
- `manifest.xml` owns `android.hardware.gnss@1.0::IGnss/default` because the
  cheryl-compatible service has no VINTF fragment.

## Verification
Static regression tests must prove the required legacy function signatures and
single GNSS frontend generation. Workspace validation must then build the source
GPS closure together with RED `.118` `libloc_api_v02`, `libizat_core`,
`liblbs_core`, `liblocationservice`, and `libgnsspps` with normal checkelf
validation enabled. No `allow_undefined_symbols` workaround is accepted.
