# Stock /system/lib/modules inventory

All supplied modules use the exact stock kernel vermagic `4.4.78-perf+ ... aarch64`.
The active WLAN/WiGig modules are byte-identical to the copies already present under vendor/lib/modules.

| module | bytes | depends | sha256 |
|---|---:|---|---|
| `br_netfilter.ko` | 28126 | `-` | `9dda310b70ed68a9eff066441b7d67aba9b35f1f63fd62e90206c4656f7683e1` |
| `lcd.ko` | 15782 | `-` | `0589683f2ffe6c98dd8adcb9be55e0e6adf913b74f88b2225a36d4cdbca61f02` |
| `mpq-adapter.ko` | 29190 | `-` | `99c4e7aa97b44ca3c02b357a814bb99e739b24aa6c12dba4ed81db80d1f9cdf4` |
| `mpq-dmx-hw-plugin.ko` | 135902 | `tspp,mpq-adapter` | `871a23b9321d319060e51466a614714d728f0bb471846d3de655b11a84e9fb72` |
| `msm_11ad_proxy.ko` | 43894 | `-` | `b4e8622e9c86fd8ae0558cd016f461f7838c7a11e73794c2669ac4935ad11d02` |
| `qca_cld3_wlan.ko` | 7666534 | `-` | `fed3923e7e101dfa63efbf579a837ebe7e33e10f95f989d18d2bd70e5dfa492c` |
| `rdbg.ko` | 20326 | `-` | `88dfe3ca0157858773d69084fdbbab33c0784f1c4d7b71ca6d8836fd9f23fa22` |
| `test-iosched.ko` | 33662 | `-` | `89919761d1092a8410500a8c04903574b91e8e52ad5597f3d5d06cbacde12d60` |
| `tspp.ko` | 69830 | `-` | `1fb42a2f8ad833f41124bf0b2201e46068c0105a69ab9272b44f73b13f9b0f8b` |
| `ufs_test.ko` | 50142 | `test-iosched` | `7f14bbeb3c99b96a5549c1542812e3dcd141ae65c97925437ecd4ffa4f236cf7` |
| `wil6210.ko` | 405206 | `msm_11ad_proxy` | `b69a06ee13b6aa61f5e962a03e6d75f6b610bdf6aa5f6b9f57310a8a9d1702fc` |

## Important correction

The stock init scripts try to insmod `msm-vidc-vmem.ko`, `msm-vidc.ko`,
`msm-vidc-dyn-gov.ko`, and `msm-vidc-table-gov.ko` from `/system/lib/modules`,
but none are present in the supplied directory. This is consistent with the stock
IKCONFIG: `CONFIG_MSM_VIDC_V4L2=y`, `CONFIG_MSM_VIDC_VMEM=y`,
`CONFIG_MSM_VIDC_GOVERNORS=y`. The video driver is built into the kernel; those
insmod lines are stale and should be removed/ignored.

Likewise QCE/QCEDEV are built-in (`CONFIG_CRYPTO_DEV_QCE50=y`,
`CONFIG_CRYPTO_DEV_QCEDEV=y`, `CONFIG_CRYPTO_DEV_QCOM_MSM_QCE=y`), so factory
`crypto.driver.load` insmods are not required for normal bring-up.
