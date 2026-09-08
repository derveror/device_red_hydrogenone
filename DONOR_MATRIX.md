# MSM8998 donor matrix for H1A1000 / LineageOS 22.2

## Primary: Razer Phone (`cheryl`)

User decision, 2026-09-08: use the maintained LineageOS 22.2 cheryl device AND
vendor trees as the primary comparison for RED integration. The user's rationale
is the closer stock Android generation: cheryl 7.1.1 to 9, RED 8.1 to 9, while
mata received Android 10. Verify actual HAL/blob ABI and kernel interfaces for
each transfer; release history alone does not establish binary compatibility.
RED .118 remains the authority for hardware, partitioning, calibration and blobs.
Essential remains the current UAPI header build dependency only; selecting a
reference does not replace the actual RED boot kernel or import donor DTBs.

### GNSS/location ABI
Use `cheryl` before `mata` for the Qualcomm GNSS/location source ABI. The Razer
Phone launched on Android 7.1.1 and its final official Android release was 9.0,
which aligns with RED `.118` Android 9 vendor consumers. Its maintained
LineageOS 22.2 tree deliberately preserves the legacy Qualcomm `LocApiBase` ABI
while adapting the source stack to Android 15 build rules.

For Hydrogen One GNSS this means:
- RED `.118` remains hardware/configuration/proprietary-blob truth;
- `cheryl` is the first donor for `libgps.utils`, `libloc_core`,
  `liblocation_api`, `libgnss`, and the QTI GNSS HIDL frontend;
- `mata`, OnePlus msm8998 and Nubia remain cross-checks for Android 15 platform
  contracts, ownership and generic msm8998 integration;
- never copy Razer device identity, partitioning, kernel DTBs, or GPS configs.

## Secondary: Essential PH-1 (`mata`)
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
