# RED Hydrogen One H1A1000 - LineageOS 22.2 bring-up

# Qualcomm common userspace
$(call inherit-product, hardware/qcom-caf/common/common.mk)

# Android 8.1 HIDL compatibility.
# H1 stock linker namespaces were not isolated and proprietary blobs use the
# split O-MR1 libhidlbase/libhidltransport/libhwbinder ABI.  LineageOS 22.2
# provides libhidlbase-v32 specifically for old vendor binaries.
PRODUCT_PACKAGES += \
    android.hidl.allocator@1.0.vendor \
    libhidlbase-v32.vendor \
    libhidlmemory.vendor:64 \
    libhwbinder \
    libhwbinder.vendor

# Device shipped with Android 8.1 / API 27
PRODUCT_SHIPPING_API_LEVEL := 27

# Heap/display
$(call inherit-product, frameworks/native/build/phone-xxhdpi-6144-dalvik-heap.mk)
TARGET_SCREEN_HEIGHT := 2560
TARGET_SCREEN_WIDTH := 1440

# A/B update engine
AB_OTA_POSTINSTALL_CONFIG += \
    RUN_POSTINSTALL_system=true \
    POSTINSTALL_PATH_system=system/bin/otapreopt_script \
    FILESYSTEM_TYPE_system=ext4 \
    POSTINSTALL_OPTIONAL_system=true
PRODUCT_PACKAGES += \
    otapreopt_script \
    update_engine \
    update_engine_sideload \
    update_verifier
PRODUCT_PACKAGES_DEBUG += update_engine_client

# Device fstab.  Do not use the O-MR1 stock fstab directly on Android 15;
# stock userdata used footer FDE.  First Lineage bring-up formats /data to
# ext4 FBE/ICE, matching maintained MSM8998 Lineage trees.
PRODUCT_COPY_FILES += \
    $(LOCAL_PATH)/rootdir/etc/fstab.qcom:$(TARGET_COPY_OUT_VENDOR)/etc/fstab.qcom \
    $(LOCAL_PATH)/rootdir/etc/fstab.qcom:$(TARGET_COPY_OUT_RECOVERY)/root/first_stage_ramdisk/fstab.qcom

# Stock-derived board init, modernized for split /vendor paths.
# Stale msm-vidc insmods were removed because VIDC is built into RED kernel 4.4.78.
PRODUCT_COPY_FILES += \
    $(LOCAL_PATH)/rootdir/etc/init/hw/init.target.rc:$(TARGET_COPY_OUT_VENDOR)/etc/init/hw/init.target.rc

# Keep VINTF kernel enforcement relaxed during the first stock-vendor bring-up.
# Tighten this after boot + HAL validation.
PRODUCT_OTA_ENFORCE_VINTF_KERNEL_REQUIREMENTS := false

# Soong
PRODUCT_SOONG_NAMESPACES += $(LOCAL_PATH)

# v0.3 strategy: a completely untouched Android 8.1 vendor is only a diagnostic stage.
# The final LOS 22.2 port must rebuild vendor from H1 stock blobs and apply legacy-HIDL
# compatibility fixups, then progressively replace standard Qualcomm HALs with source builds.

# Legacy Qualcomm property compatibility
PRODUCT_COMPATIBLE_PROPERTY_OVERRIDE := true
