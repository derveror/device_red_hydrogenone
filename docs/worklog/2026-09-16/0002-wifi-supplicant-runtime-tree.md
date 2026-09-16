# Wi-Fi supplicant runtime-tree restoration

**Date:** 2026-09-16

**Device branch:** `118-lineage-22.2-kernel-302`

**Vendor branch:** `lineage-22.2-kernel-302` (unchanged)

**Kernel branch:** `lineage-22.2` (unchanged)

## Runtime failure boundary

The installed build successfully starts the exact RED `.118` `cnss-daemon`,
completes the WLFW handshake, loads `wlan.ko` version `5.1.1.77V`, creates
`wlan0` and `p2p0`, and exposes both interfaces through the legacy Wi-Fi HAL.
Wificond also creates its client interface successfully.

Android nevertheless removed `wlan0` on every enable attempt. Wi-Fi metrics
recorded six setup failures due to supplicant and no corresponding HAL or
wificond setup failures.

## Proven root cause

Verbose runtime logging exposed the exact AIDL exception:

```text
wpa_supplicant: Failed to write to /data/vendor/wifi/wpa/wpa_supplicant.conf.
wpa_supplicant: Conf file does not exists: /data/vendor/wifi/wpa/wpa_supplicant.conf
SupplicantStaIfaceHalAidlImpl: Conf file does not exist (code 1)
WifiNative: Failed to setup iface in supplicant
```

`/data/vendor/wifi` existed, but the device init script did not create the
`wpa` and `wpa/sockets` runtime directories. LineageOS 22.2 reference trees
for cheryl, mata, Pro1, OnePlus MSM8998 and Xiaomi MSM8998 all explicitly
create the same three-directory hierarchy during `post-fs-data`.

## Runtime proof

The directories were created temporarily on the running device, assigned to
`wifi:wifi`, mode `0770`, and relabelled with the compiled file contexts. No
reboot or flash was performed.

After that one change:

- the base supplicant configuration copied successfully;
- the AIDL supplicant registered `wlan0`;
- `WifiNative` switched `wlan0` to STA connectivity mode;
- the framework remained in `EnabledState` / `ConnectModeState`;
- `cmd wifi status` reported `Wifi is enabled`;
- an explicit scan returned real 2.4 GHz and 5 GHz access points.

This proves that the missing runtime tree, rather than the kernel, firmware,
CNSS transport, HAL or wificond, caused the observed Wi-Fi enable failure.

## Permanent implementation

`init.qcom.rc` now creates the following paths during `post-fs-data`:

```text
/data/vendor/wifi                 0770 wifi wifi
/data/vendor/wifi/wpa             0770 wifi wifi
/data/vendor/wifi/wpa/sockets     0770 wifi wifi
```

The compiled Android 15 file-context rule labels the `wpa` subtree as
`wpa_data_file`, which grants the AIDL supplicant the required config-file and
control-socket access. No permissive policy or new SELinux allow rule was
added.

## Verification

- The new contract test failed before the init change and passed afterwards.
- Device tests: 175 passed; complete-tree contract passed.
- Full `mka bacon -j7`: PASS in 5 minutes 55 seconds.
- Packaged target-files `init.qcom.rc` contains the three required mkdir
  directives.
- VINTF compatibility: `compatible`.
- OTA: `lineage-22.2-20260916-UNOFFICIAL-hydrogenone.zip`, 851,071,220 bytes,
  SHA-256 `491862a8717ca3399e78450d3497c545db8307e77e6213635628e9381f22735b`.
- Boot image: 32,403,456 bytes,
  SHA-256 `01084bfa71d167d6e7ec0d70fa970d4092e48857d6eaded4050ec2fd8ad7ef52`.
- Vendor image: 333,541,608 bytes,
  SHA-256 `197a2b8c712a171c30da5d04be9c88f762a81bcb486fd919c785186d2d56502d`.
- Kernel payload: 15,655,357 bytes, 1,121,859 bytes below 16 MiB,
  SHA-256 `9d066fb204fbce603692fcfb6e3512866da5a163e00dd3814ae2867d9768c150`.
- OTA security patch level: `2026-09-01`.

Physical validation after installing the new OTA remains required to prove
that init recreates and labels the hierarchy correctly from a fresh boot.
