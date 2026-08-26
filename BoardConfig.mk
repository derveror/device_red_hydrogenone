# RED Hydrogen One H1A1000 (HydrogenONE) - LineageOS 22.2 bring-up
DEVICE_PATH := device/red/hydrogenone

# Architecture / platform
TARGET_ARCH := arm64
TARGET_ARCH_VARIANT := armv8-a
TARGET_CPU_ABI := arm64-v8a
TARGET_CPU_ABI2 :=
TARGET_CPU_VARIANT := generic
TARGET_CPU_VARIANT_RUNTIME := cortex-a73
TARGET_2ND_ARCH := arm
TARGET_2ND_ARCH_VARIANT := armv8-a
TARGET_2ND_CPU_ABI := armeabi-v7a
TARGET_2ND_CPU_ABI2 := armeabi
TARGET_2ND_CPU_VARIANT := generic
TARGET_2ND_CPU_VARIANT_RUNTIME := cortex-a73
TARGET_BOARD_PLATFORM := msm8998
TARGET_BOOTLOADER_BOARD_NAME := msm8998
TARGET_OTA_ASSERT_DEVICE := hydrogenone,HydrogenONE,H1A1000
TARGET_NO_BOOTLOADER := true
BOARD_USES_QCOM_HARDWARE := true

# A/B - confirmed by stock fstab/build properties
AB_OTA_UPDATER := true
# Build a device-specific vendor image from H1A1000 proprietary blobs.
AB_OTA_PARTITIONS += \
    boot \
    system \
    vendor

# Audio / media
AUDIO_FEATURE_ENABLED_EXTENDED_COMPRESS_FORMAT := true
BOARD_SUPPORTS_SOUND_TRIGGER := true
BOARD_USES_ALSA_AUDIO := true
TARGET_USES_ION := true

# Display
TARGET_SCREEN_DENSITY := 560

# HIDL / Treble
DEVICE_FRAMEWORK_COMPATIBILITY_MATRIX_FILE := \
    hardware/qcom-caf/common/vendor_framework_compatibility_matrix.xml \
    hardware/qcom-caf/common/vendor_framework_compatibility_matrix_legacy.xml \
    vendor/lineage/config/device_framework_matrix.xml
DEVICE_MANIFEST_FILE := $(DEVICE_PATH)/manifest.xml
DEVICE_MATRIX_FILE := hardware/qcom-caf/common/compatibility_matrix.xml
PRODUCT_FULL_TREBLE_OVERRIDE := true

# Kernel - use RED stock 4.4.78 first. It contains all H1A1000 board DTBs.
BOARD_KERNEL_BASE := 0x00000000
BOARD_KERNEL_PAGESIZE := 4096
BOARD_KERNEL_IMAGE_NAME := Image.gz-dtb
TARGET_PREBUILT_KERNEL := $(DEVICE_PATH)/prebuilt/Image.gz-dtb
BOARD_KERNEL_CMDLINE := androidboot.hardware=qcom msm_rtb.filter=0x37 ehci-hcd.park=3
BOARD_KERNEL_CMDLINE += lpm_levels.sleep_disabled=1 sched_enable_hmp=1 sched_enable_power_aware=1
BOARD_KERNEL_CMDLINE += service_locator.enable=1 swiotlb=2048 androidboot.configfs=true
BOARD_KERNEL_CMDLINE += androidboot.usbcontroller=a800000.dwc3 androidboot.boot_devices=soc/1da4000.ufshc
BOARD_KERNEL_CMDLINE += loop.max_part=7

# Partitions - exact stock raw image/partition capacities supplied from H1A1000 firmware
BOARD_BOOTIMAGE_PARTITION_SIZE := 67108864 # 64 MiB
BOARD_SYSTEMIMAGE_PARTITION_SIZE := 4294967296 # 4 GiB
BOARD_VENDORIMAGE_PARTITION_SIZE := 1073741824 # 1 GiB
BOARD_SYSTEMIMAGE_FILE_SYSTEM_TYPE := ext4
BOARD_VENDORIMAGE_FILE_SYSTEM_TYPE := ext4
BOARD_FLASH_BLOCK_SIZE := 262144
TARGET_COPY_OUT_VENDOR := vendor
TARGET_USERIMAGES_USE_EXT4 := true

# Device launched on Android 8.1 / API 27
BOARD_SHIPPING_API_LEVEL := 27

# Recovery is in boot on this A/B device (stock boot ramdisk contains recovery)
BOARD_USES_RECOVERY_AS_BOOT := true
TARGET_NO_RECOVERY := true
TARGET_RECOVERY_FSTAB := $(DEVICE_PATH)/rootdir/etc/recovery.fstab

# Root compatibility symlinks for Qualcomm/RED vendor blobs
BOARD_ROOT_EXTRA_SYMLINKS := /mnt/vendor/persist:/persist
BOARD_ROOT_EXTRA_SYMLINKS += /vendor/dsp:/dsp
BOARD_ROOT_EXTRA_SYMLINKS += /vendor/firmware_mnt:/firmware
BOARD_ROOT_EXTRA_SYMLINKS += /vendor/bt_firmware:/bt_firmware

# RIL
ENABLE_VENDOR_RIL_SERVICE := true

# Security / legacy vendor
VENDOR_SECURITY_PATCH := 2018-12-01
include device/qcom/sepolicy-legacy-um/SEPolicy.mk
BOARD_VENDOR_SEPOLICY_DIRS += $(DEVICE_PATH)/sepolicy/vendor
PRODUCT_PRIVATE_SEPOLICY_DIRS += $(DEVICE_PATH)/sepolicy/private
PRODUCT_PUBLIC_SEPOLICY_DIRS += $(DEVICE_PATH)/sepolicy/public
BOARD_AVB_ENABLE := false

# Wi-Fi - same Qualcomm qcwcn family used by current msm8998 Lineage trees
BOARD_WLAN_DEVICE := qcwcn
WPA_SUPPLICANT_VERSION := VER_0_8_X
BOARD_WPA_SUPPLICANT_DRIVER := NL80211
BOARD_WPA_SUPPLICANT_PRIVATE_LIB := lib_driver_cmd_$(BOARD_WLAN_DEVICE)
BOARD_HOSTAPD_DRIVER := NL80211
BOARD_HOSTAPD_PRIVATE_LIB := lib_driver_cmd_$(BOARD_WLAN_DEVICE)
WIFI_DRIVER_FW_PATH_STA := "sta"
WIFI_DRIVER_FW_PATH_AP := "ap"
WIFI_DRIVER_FW_PATH_P2P := "p2p"
WIFI_HIDL_FEATURE_DUAL_INTERFACE := true
WIFI_HIDL_UNIFIED_SUPPLICANT_SERVICE_RC_ENTRY := true
