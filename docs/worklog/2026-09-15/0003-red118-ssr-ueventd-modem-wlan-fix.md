# RED .118 SSR ueventd modem/WLAN fix

## Runtime symptom

The Android 15 system booted successfully from slot A, but Wi-Fi could not be
enabled. The first HAL attempt loaded the source-built `wlan.ko`, then timed out
waiting for driver readiness. Later retries returned `EEXIST` because that
first module remained loaded without creating `wlan0` or a `wiphy`.

ICNSS debugfs evidence placed the failure below the Android Wi-Fi framework:

- `REGISTER_DRIVER` was posted and processed once;
- `SERVER_ARRIVE`, `FW_READY`, and every WLFW QMI request counter were zero;
- ICNSS remained in state `0x180` (`SSR REGISTERED | PDR REGISTERED`).

The IPC Router exposed `dsps_IPCRTR` but no `mpss_IPCRTR`. The modem subsystem
and `vendor.peripheral.modem.state` both remained offline even though the two
RED .118 `qcrild` instances repeatedly voted for the modem through the running
Android 11-compatible peripheral-manager service.

## Root cause proof

`pm-service` runs as user and group `system`, while `/dev/subsys_modem` was
created as `0600 root:root`. The curated Hydrogen One `ueventd.rc` had omitted
the SSR device rule, so the peripheral manager could not open the subsystem
device that holds the modem power vote.

The original RED .118 `vendor.img` specifies exactly:

```text
/dev/subsys_*             0640   system     system
```

The same rule is present in the LineageOS 22.2 MSM8998 device trees for Razer
cheryl, Essential mata, OnePlus msm8998-common, and Nubia msm8998-common.
Existing legacy Qualcomm SELinux policy already permits `vendor_per_mgr` to
read the `ssr_device` character device, so no policy expansion is required.

## Permanent tree change

- Restore the exact RED .118 `/dev/subsys_* 0640 system system` rule.
- Add a regression contract for the effective SSR ownership and mode.
- Do not change the kernel, DTBs, WLAN blobs, peripheral-manager blobs, or
  SELinux policy for this fix.

## Verification status

- The new regression test failed before the ueventd change and passed after it.
- Device unit contracts: 172 tests PASS.
- Device full-tree contract: PASS.
- Vendor contracts: 99 tests PASS.
- Kernel contracts: 10 tests PASS.
- Live device/vendor copy-destination audit: zero collisions.
- Incremental `bacon` build with the bundled JDK 21: PASS.
- Final A/B OTA ZIP integrity and SignApk signature structure: PASS.
- Packaged `vendor.img` contains the exact SSR ueventd rule: PASS.
- `boot.img` is 32,399,360 bytes against the 67,108,864-byte partition
  limit (34,709,504 bytes free): PASS.
- OTA security patch level is `2026-09-01`.
- OTA SHA-256:
  `7a17ea895f0c6454ad9b83905bf1b694e091a0dd99fbab8f120f06198d814646`.
- `boot.img` SHA-256:
  `f8bbf83df1d20e8825d1beb3c4e2712aa4f4f8ae1dcd3ca8a88c54f931c2e73f`.
- `vendor.img` SHA-256:
  `0cb356fa50acabdeb0f5430ab72ee3f526fbc902013cd597df033aeeede978fb`.

Physical validation remains required. The successful build must not be
reported as proof that the modem reaches `ONLINE`, that `mpss_IPCRTR` appears,
or that Wi-Fi works on hardware.
