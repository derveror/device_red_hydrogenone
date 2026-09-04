# GNSS cheryl ABI Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the incompatible mata-generation Qualcomm GPS source closure with the maintained cheryl LineageOS 22.2 legacy ABI closure required by RED `.118` Android 9 location blobs.

**Architecture:** RED `.118` remains proprietary/configuration truth while `cheryl` supplies the source ABI for the Qualcomm GPS core and HIDL 1.0 frontend. Android 15 ownership stays explicit: source owns the standard GNSS default instance and vendor keeps the proprietary Qualcomm/RED consumer closure.

**Tech Stack:** Android Soong/Blueprint, HIDL GNSS 1.0, Qualcomm MSM8998 location stack, Python unittest contract tests.

**Spec:** `docs/superpowers/specs/2026-09-03-gnss-cheryl-abi-design.md`

## Global Constraints
- Target LineageOS 22.2 / Android 15 API 35.
- Canonical stock is RED `.118` Android 9.
- Do not import Razer identity, partitions, kernel/DTB, firmware or GPS configuration.
- Do not use `allow_undefined_symbols` to hide ABI mismatches.
- Keep the complete direct RED `.118` proprietary consumer closure selected when replacing `libgps.utils`, `libloc_core`, and `liblocation_api` with source.

---

### Task 1: Lock the RED/cheryl GNSS ABI contract
**Files:**
- Create: `tests/test_gnss_cheryl_abi_contract.py`
- Modify: `tests/test_android15_manifest_contract.py`

- [x] Write tests requiring GNSS HIDL 1.0, legacy `LocApiBase`/gps-utils signatures and a single active QTI frontend.
- [x] Run the focused test on the old tree and verify it fails for the intended 2.1/new-ABI reasons.
- [x] Lock all 18 symbols from the observed RED `.118 libloc_api_v02` checkelf failure and forbid Razer donor identity in active `gps/` sources.

### Task 2: Replace the active Qualcomm GPS source closure
**Files:**
- Replace from cheryl 22.2: `gps/core`, `gps/utils`, `gps/gnss`, `gps/location`, `gps/pla`, `gps/android`, `gps/Android.bp`
- Remove obsolete active-generation directories: `gps/batching`, `gps/geofence`, `gps/android/2.1`, `gps/android/utils`

- [x] Import the maintained cheryl LineageOS 22.2 source closure pinned to `e7990dd5b94c16574c45bd241a23f1abc76b9638`.
- [x] Preserve RED-owned `gps/*.conf` and local GNSS configuration modules.

### Task 3: Wire Android 15 product and VINTF ownership
**Files:**
- Modify: `device.mk`
- Modify: `manifest.xml`
- Modify: `docs/ANDROID15_MANIFEST_CONTRACT.md`
- Modify: `DONOR_MATRIX.md`

- [x] Package GNSS 1.0 source impl/service plus `libgnss` and `libgnsspps`.
- [x] Remove active GNSS 2.1/seccomp/libbatching/libgeofencing package selection.
- [x] Declare `android.hardware.gnss@1.0::IGnss/default` in the device manifest.
- [x] Persist `cheryl` as the primary GNSS/location ABI donor.

### Task 4: Protect and build the complete RED location consumer closure
**Files:**
- Vendor: `tools/prune_source_owned_location_core.py`
- Vendor: `tests/test_android15_collision_resolution.py`

- [x] Expand the vendor prune preflight from six consumers to all 20 direct RED `.118` consumers of `libgps.utils`, `libloc_core`, or `liblocation_api`.
- [ ] In the Lineage workspace build the source providers/front-end:
  `libgps.utils libloc_core liblocation_api libgnss libgnsspps android.hardware.gnss@1.0-impl-qti android.hardware.gnss@1.0-service-qti`.
- [ ] In the same invocation build the full proprietary consumer gate:
  `libDRPlugin libdataitems libdrplugin_client libevent_observer libflp libgdtap libgeofence libizat_client_api libizat_core liblbs_core libloc_api_v02 liblocationservice liblocationservice_glue liblowi_wifihal libulp2 libxtadapter libxtwifi_ulp_adaptor vendor.qti.gnss@1.0-impl xtwifi-client xtwifi-inet-agent`.
- [ ] Require checkelf to resolve the previous 18 `libloc_api_v02` symbols without exceptions and verify no other consumer reports source-core ABI failures.
- [ ] If the complete targeted closure is green, commit the generated vendor location-core pruning, update the device/vendor cross-tree lock to the tested pair, and proceed to full `m bacon`.
