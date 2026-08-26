# MSM8998 donor matrix for H1A1000 / LineageOS 22.2

## Primary: Essential PH-1 (`mata`)
Use for architecture and build layout, not hardware-specific DTS/blobs.

Matches H1A1000 particularly well:
- Qualcomm MSM8998
- A/B OTA
- Treble split system/vendor
- recovery-as-boot
- UFS controller path `soc/1da4000.ufshc`
- 4096-byte boot page
- `Image.gz-dtb`
- current LineageOS 22.2 still uses a 4.4 MSM8998 kernel
- qcwcn Wi-Fi and legacy Qualcomm sepolicy patterns

## Secondary: OnePlus 5/5T (`cheeseburger`/`dumpling`, `msm8998-common`)
Use for modern LineageOS 22.2 Qualcomm userspace patterns:
- audio.primary.msm8998 and Qualcomm audio policy structure
- camera provider 2.4 patterns
- graphics allocator/composer/mapper stack
- qcwcn Wi-Fi
- RIL/QTI compatibility packages
- legacy-UM sepolicy
- modern power/health/USB replacements

Do NOT copy its partition model: OnePlus 5/5T is not the same A/B layout as H1A1000.

## Secondary: Pixel 2/2 XL (`wahoo` + `walleye`/`taimen`)
Use for mature Qualcomm proprietary blob handling, A/B/Treble conventions and
MSM8998-era Google compatibility fixes. Hardware-specific panel/camera/touch remain RED-specific.

## RED-specific authority
For these, stock H1A1000 always wins over donors:
- all 60 appended DTBs / board IDs
- TM/JDI/SIM display variants and Leia 4-View display
- Synaptics/ST touch
- FPC fingerprint wiring
- CloudMinds SmartPort / PCIe accessory path
- panel/backlight GPIO/regulator topology
- camera sensor topology
- audio routing/mixer files
- charging/battery/haptics
