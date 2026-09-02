# RED .118 device-owned vendor config audit

Canonical stock: `H1A1000.082ho.01.00.10r.118` / `7277a1accf9595bb727f2189863cf5f6249dd99322e2953432bca6e448365f1e`.

This report compares every LOCAL_PATH-owned file copied into `/vendor` with the same destination in canonical RED `.118` `vendor.img`.

## Summary

- local vendor-copy mappings: **88**
- byte-identical to stock: **64**
- different from stock: **17**
- no stock counterpart: **7**
- missing device source: **0**

A byte difference is evidence for review, not an automatic error: modern Lineage source-owned policy/config may intentionally differ from Android 9 stock.

## Different from stock

- `audio/audio_effects.conf` → `vendor/etc/audio_effects.conf` — device `74f0013c9525dbfd8e45534b33e5518a00468644f9778b08bb1ff8cb4c098573`, stock `387a18a8998a18047fad580f9e264a5fa5938466fe995c60e0a07f2221874273`
- `audio/audio_platform_info.xml` → `vendor/etc/audio_platform_info.xml` — device `39d02d782c4d67b5127a4cfd44b47601d862ca957f4a4682737a08e61cc5295f`, stock `614af67cfec5dc1ad38e70ad04b0e9e323b514c572e7291b8535e6023efbd186`
- `audio/audio_policy_volumes.xml` → `vendor/etc/audio_policy_volumes.xml` — device `ed8fdde0fe14942f016ad6918794a0a2c0293c2fe99eacc07ba9f7d8ab00fab8`, stock `9c57331b5ef78822c9c8525b90a88d49a9bb28ed02edd7dff47ca5158497eca6`
- `configs/camera/camera_config.xml` → `vendor/etc/camera/camera_config.xml` — device `93164993489e7ff40e1b8cf9bd0199dadd6e5e4a0ef1020b2fd7cb47035bcda7`, stock `505796da505af5784891ae2ae3569cbaba69f01814fdbfbdc2a2e219ffc512e5`
- `configs/camera/imx268_main_chromatix.xml` → `vendor/etc/camera/imx268_main_chromatix.xml` — device `d242a4f0d9a12a4151453b043cc7f31c9c15a55546daa2c05e60b2586a228912`, stock `f54e448f3761639f58e2a2f179fec01e818d8396c04ee2b6e734637dff0cb960`
- `configs/camera/imx268_sub_chromatix.xml` → `vendor/etc/camera/imx268_sub_chromatix.xml` — device `ad8f742ec79764e6fc321f9ca96b5a914b4bdfac8f54fd5d694eaae779de35c8`, stock `81d26e891b9dd566655fc02ca003fa224d4781e6f80bf27f500bb346d878daf3`
- `configs/camera/imx380_main_chromatix.xml` → `vendor/etc/camera/imx380_main_chromatix.xml` — device `23b3e0aa42ef7e81d6c2d25fcd11548b6a504d5241fc59b310ac34ddfe22dbfd`, stock `6aafe4a658400600464f938d2fa6ffc00fcb84fb8e1e8aa0b30dbd4cb23fef04`
- `configs/camera/imx380_sub_chromatix.xml` → `vendor/etc/camera/imx380_sub_chromatix.xml` — device `87f7fab10011542a6e1be11b988ca8a6b8e256a0dce910b2d9dd65afc4da3636`, stock `7a389af8ca1f4bb95135894f538f52436160b613b905206e5fa2481aed598f7d`
- `audio/default_volume_tables.xml` → `vendor/etc/default_volume_tables.xml` — device `8d9025527a672bca499f6276c44ceba4b977470de09c6b1eb60fa03509658c21`, stock `700b3e3979801bc09875e948bfae489d4c488e8b17911e8dcc2eebbfd17bb4ec`
- `rootdir/etc/fstab.qcom` → `vendor/etc/fstab.qcom` — device `66a8f24700e63ac4299ed2d4e5048793970b56d59b88af1ef987d8248197d990`, stock `5be6c9032f01c591d219f24ac6d1fd9533a2c3b70bcf3c55737f0d57d0441c7a`
- `gps/izat.conf` → `vendor/etc/izat.conf` — device `a343f6fb4e5296b551c7f984f2773262d5910d16334e2a854e7998531fff5673`, stock `734de6b55845c355d327908311b24de6b90c5b9b60c0666a6be5663580a5e93f`
- `media/media_codecs_vendor_audio.xml` → `vendor/etc/media_codecs_vendor_audio.xml` — device `5000daee7b9868ba34f4648cc4b384400cf260e5907b33ac773e06984d4f11ff`, stock `35db19dac127e0b23090621353978afc14d64ece22ff324f8ced2c78d842a41f`
- `media/media_profiles_V1_0.xml` → `vendor/etc/media_profiles_V1_0.xml` — device `ed964883deb2d655e5d6b11131e60874559af9750c5cb97b041d4951f0c3c15e`, stock `a88313e1cccb57c7dd5c22fe11907e04e25425f0764d6b118788f423f4cd9721`
- `audio/mixer_paths_tasha.xml` → `vendor/etc/mixer_paths_tasha.xml` — device `e326b61384277d425495af22f1680d74ed311125ad1525f1a65ad2fa326752e3`, stock `d17baa0cc2866a100cad237a7c057a8f0f2c24cb150be3f4b5bdf85200140fd2`
- `power/powerhint.xml` → `vendor/etc/powerhint.xml` — device `84ae45dd1273034d395315e88fdd0b7b9a5c66f74e5a6e883c2bdb70701e3717`, stock `2e8ad4504f16340763e7cdd22a0ed244f9824871601b550857a018be279e5209`
- `configs/public.libraries.txt` → `vendor/etc/public.libraries.txt` — device `dc8a626b687150f6915a0072b4a0e3f1b8b831bdb6390c942e28dd076dd482d0`, stock `1a9e83ec1152e884ab8d7db338739902620aca0e8540f731511dabee6fa4e025`
- `configs/sec_config` → `vendor/etc/sec_config` — device `aa8f3201eba6208b0a3c9ab039aa0e6875463c9b8710397ee6fbb26913fa80b7`, stock `bbdfba0ec570136e627fe806b35fa3c7b292a3c1da60f12e14f38036b78942e9`

## No stock counterpart

- `configs/camera/imx332_chromatix.xml` → `vendor/etc/camera/imx332_chromatix.xml`
- `configs/camera/s5k2t7sp_chromatix.xml` → `vendor/etc/camera/s5k2t7sp_chromatix.xml`
- `configs/nfc/libnfc-nxp.conf` → `vendor/etc/libnfc-nxp.conf`
- `rootdir/etc/ueventd.rc` → `vendor/etc/ueventd.rc`
- `wifi/wifi_concurrency_cfg.txt` → `vendor/etc/wifi/wifi_concurrency_cfg.txt`
- `wifi/WCNSS_qcom_cfg.ini` → `vendor/firmware/wlan/qca_cld/WCNSS_qcom_cfg.ini`
- `keylayout/gpio-keys.kl` → `vendor/usr/keylayout/gpio-keys.kl`
