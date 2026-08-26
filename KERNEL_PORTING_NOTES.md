# Kernel plan: RED 4.4.78 -> maintained MSM8998 4.4

## Phase 1: boot Lineage with exact stock RED kernel
`prebuilt/Image.gz-dtb` is the exact stock H1A1000 kernel payload from the supplied boot image.
It contains the kernel plus 60 appended DTBs. This avoids losing RED-specific board support while
userspace is being modernized.

Stock kernel identity:
- Linux 4.4.78-perf+
- ARM64 / MSM8998
- binder, hwbinder, vndbinder
- dm-verity / dm-crypt
- ext4 ICE encryption support

Important RED-only/RED-selected config found in the stock IKCONFIG includes:
- `CONFIG_CM_SMARTPORT=y`
- `CONFIG_TOUCHSCREEN_SYNAPTICS_DSX=y`
- `CONFIG_TOUCHSCREEN_SYNAPTICS_DSX_I2C=y`
- `CONFIG_TOUCHSCREEN_ST=y`
- `CONFIG_TOUCHSCREEN_ST_I2C=y`
- `CONFIG_INPUT_FPC_FINGERPRINT=y`
- `CONFIG_AUDIO_EXT_CLK=y`
- `CONFIG_QPNP_HAPTIC=y`

## Phase 2: move to Lineage Essential MSM8998 4.4 tree
The current `android_kernel_essential_msm8998` lineage-22.2 tree is Linux 4.4.302, so it is a
much better long-term base than leaving the 2018 RED 4.4.78 kernel permanently.

Port order:
1. Import/decompile RED production PVT DTS variants (TM, TM-CSP, SIM, JDI).
2. Bring over panel/backlight/touch/regulator nodes and validate boot/display.
3. Port Synaptics DSX/ST touch support (generic Qualcomm trees already contain related drivers).
4. Port FPC fingerprint device wiring/driver changes.
5. Port audio external-clock changes and RED Tavil routing.
6. Port QPNP haptics differences.
7. Port `CM_SMARTPORT` last; it appears to be the most device/vendor-specific driver.
8. Rebuild external modules and remove stock `/system/lib/modules` dependency.

Do not use `mata`/OnePlus DTBs or boot images directly on H1A1000.

## Stock external modules verified in v0.3
The supplied stock module set uses vermagic `4.4.78-perf+ SMP preempt mod_unload modversions aarch64`.
`qca_cld3_wlan.ko`, `msm_11ad_proxy.ko`, and `wil6210.ko` are byte-identical to vendor copies.

MSM VIDC is not an external module on this build:
- `CONFIG_MSM_VIDC_V4L2=y`
- `CONFIG_MSM_VIDC_VMEM=y`
- `CONFIG_MSM_VIDC_GOVERNORS=y`

QCE/QCEDEV are also built in.  Do not spend bring-up time hunting the stale `.ko` names referenced
by old init scripts.
