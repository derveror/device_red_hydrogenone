# RED H1A1000 `.109` stock facts used by this tree

Stock package: `H1A1000.010ho.01.01.01r.109_VZW_exfastboot.lzma2.7z`

- Android 8.1 / API 27, security patch 2018-12-01.
- SoC: Qualcomm MSM8998 / Snapdragon 835.
- A/B layout, UFS controller `soc/1da4000.ufshc`.
- `boot.img`: header v0, page 4096, 64 MiB.
- Kernel payload: Linux 4.4.78-perf+, exact SHA-256
  `6cf3a70ece8b32dcd6bccf9db1a22c1da29b9b37fe67cc0e4ec9b4f87fec2426`.
- Kernel payload contains 60 appended DTBs, including RED/CloudMinds board/display variants.
- System partition: 4 GiB; vendor partition: 1 GiB.
- Bluetooth controller property: `qcom.bluetooth.soc=cherokee`.
- RIL path migrated for Android 15 to `vendor.rild.libpath=/vendor/lib64/libril-qc-qmi-1.so`.
- NFC property: `ro.hardware.nfc_nci=nqx.default`; stock NXP default config selects PN80T (`0x08`).
- Camera configuration contains multiple stock module variants; all selection XMLs are preserved,
  while proprietary sensor/chromatix libraries remain vendor blobs.

Do not package or replace device-private `persist`, modem, Bluetooth/DSP firmware, TZ/QSEE,
bootloader, or calibration partitions in the first LineageOS payload.
