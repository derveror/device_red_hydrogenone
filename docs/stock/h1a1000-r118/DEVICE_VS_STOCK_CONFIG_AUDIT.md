# RED `.118` device-owned vendor configuration audit

Canonical stock: `H1A1000.082ho.01.00.10r.118` / `7277a1accf9595bb727f2189863cf5f6249dd99322e2953432bca6e448365f1e`.

This report compares every `LOCAL_PATH`-owned file copied into `/vendor` with the same destination in canonical RED `.118` `vendor.img`.

## Summary

- Local vendor-copy mappings: **86**
- Byte-identical to stock: **74**
- Intentionally adapted for Android 15: **7**
- Equivalent stock data installed at a different destination, or source-only configuration: **5**
- Missing device source: **0**

The exact stock hardware set now includes RED audio platform and mixer routing, all six camera profiles, power hints, public-library policy, WCNSS configuration and hardware-key layout. The active source-HAL NFC configuration is byte-identical to stock `libnfc-nxp_default.conf`, installed as `libnfc-nxp.conf` because that is the filename read by the Lineage NXP HAL.

## Intentional Android 15 adaptations

- `audio/audio_effects.conf` — source audio-effect module names and libraries.
- `audio/audio_policy_volumes.xml` — current framework volume-policy schema.
- `audio/default_volume_tables.xml` — current framework defaults.
- `rootdir/etc/fstab.qcom` — first-stage mount, A/B and FBE contract.
- `gps/izat.conf` — current package names and Android group translation.
- `media/media_codecs_vendor_audio.xml` — current source codec contract.
- `configs/sec_config` — Android group translation for retained Qualcomm services.

## Different destinations or source-only files

- `configs/nfc/libnfc-nxp.conf` — exact stock `libnfc-nxp_default.conf` content under the source HAL's active filename.
- `rootdir/etc/ueventd.rc` — curated source-kernel device-node ownership.
- `wifi/wifi_concurrency_cfg.txt` — source Wi-Fi HAL configuration.
- `wifi/WCNSS_qcom_cfg.ini` — exact stock content copied to the firmware path used by the source driver; stock exposes that path through a symlink.
- `keylayout/gpio-keys.kl` — exact stock system key layout installed in the Lineage vendor partition.

The machine-readable hashes and per-path status are in `device-vs-stock-config-audit.json`. The former line-by-line diff snapshot was removed because it described the superseded device configuration and could no longer be reproduced from the active authority set.
