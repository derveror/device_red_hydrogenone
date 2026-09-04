# RED Hydrogen One H1A1000 - LineageOS 22.2

# Qualcomm common userspace
$(call inherit-product, hardware/qcom-caf/common/common.mk)

PRODUCT_SHIPPING_API_LEVEL := 27
PRODUCT_COMPATIBLE_PROPERTY_OVERRIDE := true
PRODUCT_CHARACTERISTICS := nosdcard

# Heap / display
$(call inherit-product, frameworks/native/build/phone-xhdpi-6144-dalvik-heap.mk)
TARGET_SCREEN_HEIGHT := 2560
TARGET_SCREEN_WIDTH := 1440
PRODUCT_AAPT_CONFIG := normal
PRODUCT_AAPT_PREF_CONFIG := 560dpi
PRODUCT_AAPT_PREBUILT_DPI := xxxhdpi xxhdpi xhdpi hdpi

# Overlays
DEVICE_PACKAGE_OVERLAYS += \
    $(LOCAL_PATH)/overlay \
    $(LOCAL_PATH)/overlay-lineage
PRODUCT_ENFORCE_RRO_TARGETS := *

# A/B / update engine
AB_OTA_POSTINSTALL_CONFIG += \
    RUN_POSTINSTALL_system=true \
    POSTINSTALL_PATH_system=system/bin/otapreopt_script \
    FILESYSTEM_TYPE_system=ext4 \
    POSTINSTALL_OPTIONAL_system=true
PRODUCT_PACKAGES += \
    otapreopt_script \
    fastbootd \
    update_engine \
    update_engine_sideload \
    update_verifier
PRODUCT_PACKAGES_DEBUG += \
    bootctl \
    update_engine_client

# Boot control - source implementation, compatible with stock 4.4 UFS path
PRODUCT_PACKAGES += \
    android.hardware.boot-service.qti \
    android.hardware.boot-service.qti.recovery
$(call soong_config_set,QTI_GPT_UTILS,USE_BSG_FRAMEWORK,false)

# Android 8 vendor HIDL compatibility
PRODUCT_PACKAGES += \
    android.hidl.allocator@1.0.vendor \
    libhidlbase-v32.recovery \
    libhidlmemory.recovery

# Audio - Qualcomm msm8998 source HAL with RED stock policy/mixer configuration
PRODUCT_PACKAGES += \
    android.hardware.audio@6.0-impl:32 \
    android.hardware.audio.effect@6.0-impl:32 \
    android.hardware.audio.service \
    android.hardware.bluetooth.audio@2.1-impl \
    android.hardware.soundtrigger@2.2-impl \
    audio.bluetooth.default \
    audio.primary.msm8998 \
    audio.r_submix.default \
    audio.usb.default \
    libaudio-resampler \
    libqcompostprocbundle \
    libqcomvisualizer \
    libqcomvoiceprocessing \
    libvolumelistener

PRODUCT_COPY_FILES += \
    $(LOCAL_PATH)/audio/audio_effects.conf:$(TARGET_COPY_OUT_VENDOR)/etc/audio_effects.conf \
    $(LOCAL_PATH)/audio/audio_output_policy.conf:$(TARGET_COPY_OUT_VENDOR)/etc/audio_output_policy.conf \
    $(LOCAL_PATH)/audio/audio_platform_info.xml:$(TARGET_COPY_OUT_VENDOR)/etc/audio_platform_info.xml \
    $(LOCAL_PATH)/audio/audio_policy_configuration.xml:$(TARGET_COPY_OUT_VENDOR)/etc/audio_policy_configuration.xml \
    $(LOCAL_PATH)/audio/audio_policy_volumes.xml:$(TARGET_COPY_OUT_VENDOR)/etc/audio_policy_volumes.xml \
    $(LOCAL_PATH)/audio/default_volume_tables.xml:$(TARGET_COPY_OUT_VENDOR)/etc/default_volume_tables.xml \
    $(LOCAL_PATH)/audio/listen_platform_info.xml:$(TARGET_COPY_OUT_VENDOR)/etc/listen_platform_info.xml \
    $(LOCAL_PATH)/audio/mixer_paths_tasha.xml:$(TARGET_COPY_OUT_VENDOR)/etc/mixer_paths_tasha.xml \
    $(LOCAL_PATH)/audio/mixer_paths_tasha_tfa.xml:$(TARGET_COPY_OUT_VENDOR)/etc/mixer_paths_tasha_tfa.xml \
    $(LOCAL_PATH)/audio/mixer_paths_tasha_tfa_a3d.xml:$(TARGET_COPY_OUT_VENDOR)/etc/mixer_paths_tasha_tfa_a3d.xml \
    $(LOCAL_PATH)/audio/sound_trigger_mixer_paths.xml:$(TARGET_COPY_OUT_VENDOR)/etc/sound_trigger_mixer_paths.xml \
    $(LOCAL_PATH)/audio/sound_trigger_platform_info.xml:$(TARGET_COPY_OUT_VENDOR)/etc/sound_trigger_platform_info.xml \
    frameworks/av/services/audiopolicy/config/a2dp_audio_policy_configuration.xml:$(TARGET_COPY_OUT_VENDOR)/etc/a2dp_audio_policy_configuration.xml \
    frameworks/av/services/audiopolicy/config/bluetooth_audio_policy_configuration.xml:$(TARGET_COPY_OUT_VENDOR)/etc/bluetooth_audio_policy_configuration.xml \
    frameworks/av/services/audiopolicy/config/r_submix_audio_policy_configuration.xml:$(TARGET_COPY_OUT_VENDOR)/etc/r_submix_audio_policy_configuration.xml \
    frameworks/av/services/audiopolicy/config/usb_audio_policy_configuration.xml:$(TARGET_COPY_OUT_VENDOR)/etc/usb_audio_policy_configuration.xml

# Camera provider wrapper; camera HAL payload remains in future vendor tree
PRODUCT_PACKAGES += \
    android.hardware.camera.provider@2.4-impl:32 \
    android.hardware.camera.provider@2.4-service


# RED .109 camera module topology and chromatix-selection XMLs.
# Binary sensor/chromatix libraries remain proprietary and are supplied by vendor/red/hydrogenone.
PRODUCT_COPY_FILES += \
    $(LOCAL_PATH)/configs/camera/camera_config.xml:$(TARGET_COPY_OUT_VENDOR)/etc/camera/camera_config.xml \
    $(LOCAL_PATH)/configs/camera/csidtg_camera.xml:$(TARGET_COPY_OUT_VENDOR)/etc/camera/csidtg_camera.xml \
    $(LOCAL_PATH)/configs/camera/csidtg_chromatix.xml:$(TARGET_COPY_OUT_VENDOR)/etc/camera/csidtg_chromatix.xml \
    $(LOCAL_PATH)/configs/camera/imx214_chromatix.xml:$(TARGET_COPY_OUT_VENDOR)/etc/camera/imx214_chromatix.xml \
    $(LOCAL_PATH)/configs/camera/imx230_chromatix.xml:$(TARGET_COPY_OUT_VENDOR)/etc/camera/imx230_chromatix.xml \
    $(LOCAL_PATH)/configs/camera/imx230_qc2002_chromatix.xml:$(TARGET_COPY_OUT_VENDOR)/etc/camera/imx230_qc2002_chromatix.xml \
    $(LOCAL_PATH)/configs/camera/imx230_qc2002_with_gyro_chromatix.xml:$(TARGET_COPY_OUT_VENDOR)/etc/camera/imx230_qc2002_with_gyro_chromatix.xml \
    $(LOCAL_PATH)/configs/camera/imx258_bear_chromatix.xml:$(TARGET_COPY_OUT_VENDOR)/etc/camera/imx258_bear_chromatix.xml \
    $(LOCAL_PATH)/configs/camera/imx258_chromatix.xml:$(TARGET_COPY_OUT_VENDOR)/etc/camera/imx258_chromatix.xml \
    $(LOCAL_PATH)/configs/camera/imx258_lc898217xc_chromatix.xml:$(TARGET_COPY_OUT_VENDOR)/etc/camera/imx258_lc898217xc_chromatix.xml \
    $(LOCAL_PATH)/configs/camera/imx258_mono_bear_chromatix.xml:$(TARGET_COPY_OUT_VENDOR)/etc/camera/imx258_mono_bear_chromatix.xml \
    $(LOCAL_PATH)/configs/camera/imx258_mono_chromatix.xml:$(TARGET_COPY_OUT_VENDOR)/etc/camera/imx258_mono_chromatix.xml \
    $(LOCAL_PATH)/configs/camera/imx268_main_chromatix.xml:$(TARGET_COPY_OUT_VENDOR)/etc/camera/imx268_main_chromatix.xml \
    $(LOCAL_PATH)/configs/camera/imx268_sub_chromatix.xml:$(TARGET_COPY_OUT_VENDOR)/etc/camera/imx268_sub_chromatix.xml \
    $(LOCAL_PATH)/configs/camera/imx298_chromatix.xml:$(TARGET_COPY_OUT_VENDOR)/etc/camera/imx298_chromatix.xml \
    $(LOCAL_PATH)/configs/camera/imx298_gt24c64_chromatix.xml:$(TARGET_COPY_OUT_VENDOR)/etc/camera/imx298_gt24c64_chromatix.xml \
    $(LOCAL_PATH)/configs/camera/imx318_chromatix.xml:$(TARGET_COPY_OUT_VENDOR)/etc/camera/imx318_chromatix.xml \
    $(LOCAL_PATH)/configs/camera/imx332_chromatix.xml:$(TARGET_COPY_OUT_VENDOR)/etc/camera/imx332_chromatix.xml \
    $(LOCAL_PATH)/configs/camera/imx362_chromatix.xml:$(TARGET_COPY_OUT_VENDOR)/etc/camera/imx362_chromatix.xml \
    $(LOCAL_PATH)/configs/camera/imx362_chromatix_bear.xml:$(TARGET_COPY_OUT_VENDOR)/etc/camera/imx362_chromatix_bear.xml \
    $(LOCAL_PATH)/configs/camera/imx362_gt24c64a_chromatix.xml:$(TARGET_COPY_OUT_VENDOR)/etc/camera/imx362_gt24c64a_chromatix.xml \
    $(LOCAL_PATH)/configs/camera/imx376_chromatix.xml:$(TARGET_COPY_OUT_VENDOR)/etc/camera/imx376_chromatix.xml \
    $(LOCAL_PATH)/configs/camera/imx378_chromatix.xml:$(TARGET_COPY_OUT_VENDOR)/etc/camera/imx378_chromatix.xml \
    $(LOCAL_PATH)/configs/camera/imx380_main_chromatix.xml:$(TARGET_COPY_OUT_VENDOR)/etc/camera/imx380_main_chromatix.xml \
    $(LOCAL_PATH)/configs/camera/imx380_sub_chromatix.xml:$(TARGET_COPY_OUT_VENDOR)/etc/camera/imx380_sub_chromatix.xml \
    $(LOCAL_PATH)/configs/camera/ov12a10_bear_chromatix.xml:$(TARGET_COPY_OUT_VENDOR)/etc/camera/ov12a10_bear_chromatix.xml \
    $(LOCAL_PATH)/configs/camera/ov12a10_chromatix.xml:$(TARGET_COPY_OUT_VENDOR)/etc/camera/ov12a10_chromatix.xml \
    $(LOCAL_PATH)/configs/camera/ov13850_chromatix.xml:$(TARGET_COPY_OUT_VENDOR)/etc/camera/ov13850_chromatix.xml \
    $(LOCAL_PATH)/configs/camera/ov13850_q13v06k_chromatix.xml:$(TARGET_COPY_OUT_VENDOR)/etc/camera/ov13850_q13v06k_chromatix.xml \
    $(LOCAL_PATH)/configs/camera/ov13855_chromatix.xml:$(TARGET_COPY_OUT_VENDOR)/etc/camera/ov13855_chromatix.xml \
    $(LOCAL_PATH)/configs/camera/ov13880_chromatix.xml:$(TARGET_COPY_OUT_VENDOR)/etc/camera/ov13880_chromatix.xml \
    $(LOCAL_PATH)/configs/camera/ov2281_chromatix.xml:$(TARGET_COPY_OUT_VENDOR)/etc/camera/ov2281_chromatix.xml \
    $(LOCAL_PATH)/configs/camera/ov2680_chromatix.xml:$(TARGET_COPY_OUT_VENDOR)/etc/camera/ov2680_chromatix.xml \
    $(LOCAL_PATH)/configs/camera/ov4688_chromatix.xml:$(TARGET_COPY_OUT_VENDOR)/etc/camera/ov4688_chromatix.xml \
    $(LOCAL_PATH)/configs/camera/ov5670_chromatix.xml:$(TARGET_COPY_OUT_VENDOR)/etc/camera/ov5670_chromatix.xml \
    $(LOCAL_PATH)/configs/camera/ov5670_f5670bq_chromatix.xml:$(TARGET_COPY_OUT_VENDOR)/etc/camera/ov5670_f5670bq_chromatix.xml \
    $(LOCAL_PATH)/configs/camera/ov5695_chromatix.xml:$(TARGET_COPY_OUT_VENDOR)/etc/camera/ov5695_chromatix.xml \
    $(LOCAL_PATH)/configs/camera/ov7251_chromatix.xml:$(TARGET_COPY_OUT_VENDOR)/etc/camera/ov7251_chromatix.xml \
    $(LOCAL_PATH)/configs/camera/ov8856_chromatix.xml:$(TARGET_COPY_OUT_VENDOR)/etc/camera/ov8856_chromatix.xml \
    $(LOCAL_PATH)/configs/camera/ov8858_chromatix.xml:$(TARGET_COPY_OUT_VENDOR)/etc/camera/ov8858_chromatix.xml \
    $(LOCAL_PATH)/configs/camera/ov8865_chromatix.xml:$(TARGET_COPY_OUT_VENDOR)/etc/camera/ov8865_chromatix.xml \
    $(LOCAL_PATH)/configs/camera/s5k2l7_8953_chromatix.xml:$(TARGET_COPY_OUT_VENDOR)/etc/camera/s5k2l7_8953_chromatix.xml \
    $(LOCAL_PATH)/configs/camera/s5k2l7_chromatix.xml:$(TARGET_COPY_OUT_VENDOR)/etc/camera/s5k2l7_chromatix.xml \
    $(LOCAL_PATH)/configs/camera/s5k2l7sx_chromatix.xml:$(TARGET_COPY_OUT_VENDOR)/etc/camera/s5k2l7sx_chromatix.xml \
    $(LOCAL_PATH)/configs/camera/s5k2t7sp_chromatix.xml:$(TARGET_COPY_OUT_VENDOR)/etc/camera/s5k2t7sp_chromatix.xml \
    $(LOCAL_PATH)/configs/camera/s5k3l8_chromatix.xml:$(TARGET_COPY_OUT_VENDOR)/etc/camera/s5k3l8_chromatix.xml \
    $(LOCAL_PATH)/configs/camera/s5k3l8_f3l8yam_chromatix.xml:$(TARGET_COPY_OUT_VENDOR)/etc/camera/s5k3l8_f3l8yam_chromatix.xml \
    $(LOCAL_PATH)/configs/camera/s5k3l8_mono_chromatix.xml:$(TARGET_COPY_OUT_VENDOR)/etc/camera/s5k3l8_mono_chromatix.xml \
    $(LOCAL_PATH)/configs/camera/s5k3m2xm_chromatix.xml:$(TARGET_COPY_OUT_VENDOR)/etc/camera/s5k3m2xm_chromatix.xml \
    $(LOCAL_PATH)/configs/camera/s5k3m2xm_chromatix_bear.xml:$(TARGET_COPY_OUT_VENDOR)/etc/camera/s5k3m2xm_chromatix_bear.xml \
    $(LOCAL_PATH)/configs/camera/s5k3m2xx_chromatix.xml:$(TARGET_COPY_OUT_VENDOR)/etc/camera/s5k3m2xx_chromatix.xml \
    $(LOCAL_PATH)/configs/camera/s5k3m3sm_chromatix.xml:$(TARGET_COPY_OUT_VENDOR)/etc/camera/s5k3m3sm_chromatix.xml \
    $(LOCAL_PATH)/configs/camera/s5k3p3sm_chromatix.xml:$(TARGET_COPY_OUT_VENDOR)/etc/camera/s5k3p3sm_chromatix.xml \
    $(LOCAL_PATH)/configs/camera/s5k3p8sp_chromatix.xml:$(TARGET_COPY_OUT_VENDOR)/etc/camera/s5k3p8sp_chromatix.xml

# Cgroups / task profiles for legacy Qualcomm daemons
PRODUCT_COPY_FILES += \
    system/core/libprocessgroup/profiles/cgroups_28.json:$(TARGET_COPY_OUT_VENDOR)/etc/cgroups.json \
    system/core/libprocessgroup/profiles/task_profiles_28.json:$(TARGET_COPY_OUT_VENDOR)/etc/task_profiles.json

# ConfigStore is obsolete on Android 15
PRODUCT_PACKAGES += disable_configstore

# Display - generic msm8998 source stack; RED panel stays in stock kernel DTBs
PRODUCT_PACKAGES += \
    android.hardware.graphics.allocator@2.0-impl:64 \
    android.hardware.graphics.allocator@2.0-service \
    android.hardware.graphics.composer@2.1-service \
    android.hardware.graphics.mapper@2.0-impl-2.1 \
    gralloc.msm8998 \
    hwcomposer.qcom \
    libdisplayconfig \
    libvulkan \
    vendor.qti.hardware.memtrack-service

# DRM
PRODUCT_PACKAGES += android.hardware.drm-service.clearkey

# Gatekeeper / keymaster source service wrappers
PRODUCT_PACKAGES += \
    android.hardware.gatekeeper@1.0-impl \
    android.hardware.gatekeeper@1.0-service \
    android.hardware.gatekeeper@1.0.vendor \
    android.hardware.keymaster@3.0-impl \
    android.hardware.keymaster@3.0-service

# GNSS - Qualcomm MSM8998 legacy ABI source stack.
# Razer cheryl is the primary source-ABI donor here because its maintained
# LineageOS 22.2 tree preserves the Pie-era Qualcomm LocApiBase ABI required
# by RED .118 libloc_api_v02/libizat_core/liblbs_core while adapting the HAL
# frontend to Android 15 build rules. RED stock remains configuration truth.
PRODUCT_PACKAGES += \
    android.hardware.gnss@1.0-impl-qti \
    android.hardware.gnss@1.0-service-qti \
    libgnss \
    libgnsspps

# RED GNSS configuration modules. gps.conf/flp.conf/antenna info stay owned by
# the local prebuilt_etc definitions; RED-specific Izat/LOWI/SAP/XTWiFi files
# are copied directly and are not replaced with Razer configuration.
PRODUCT_PACKAGES += \
    flp.conf \
    gnss_antenna_info.conf \
    gps.conf

PRODUCT_COPY_FILES += \
    $(LOCAL_PATH)/gps/izat.conf:$(TARGET_COPY_OUT_VENDOR)/etc/izat.conf \
    $(LOCAL_PATH)/gps/lowi.conf:$(TARGET_COPY_OUT_VENDOR)/etc/lowi.conf \
    $(LOCAL_PATH)/gps/sap.conf:$(TARGET_COPY_OUT_VENDOR)/etc/sap.conf \
    $(LOCAL_PATH)/gps/xtwifi.conf:$(TARGET_COPY_OUT_VENDOR)/etc/xtwifi.conf

# Health
PRODUCT_PACKAGES += \
    android.hardware.health-service.qti \
    android.hardware.health-service.qti_recovery

# Init / fstab / ueventd
PRODUCT_COPY_FILES += \
    $(LOCAL_PATH)/rootdir/etc/fstab.qcom:$(TARGET_COPY_OUT_VENDOR)/etc/fstab.qcom \
    $(LOCAL_PATH)/rootdir/etc/fstab.qcom:$(TARGET_COPY_OUT_RECOVERY)/root/first_stage_ramdisk/fstab.qcom \
    $(LOCAL_PATH)/rootdir/etc/ueventd.rc:$(TARGET_COPY_OUT_VENDOR)/etc/ueventd.rc

$(foreach f,$(wildcard $(LOCAL_PATH)/rootdir/etc/init/hw/*.rc),\
    $(eval PRODUCT_COPY_FILES += $(f):$(TARGET_COPY_OUT_VENDOR)/etc/init/hw/$(notdir $f)))

# IRQ / Qualcomm security config; canonical RED .118 thermal config is vendor-owned
PRODUCT_COPY_FILES += \
    $(LOCAL_PATH)/configs/msm_irqbalance.conf:$(TARGET_COPY_OUT_VENDOR)/etc/msm_irqbalance.conf \
    $(LOCAL_PATH)/configs/sec_config:$(TARGET_COPY_OUT_VENDOR)/etc/sec_config \
    $(LOCAL_PATH)/configs/public.libraries.txt:$(TARGET_COPY_OUT_VENDOR)/etc/public.libraries.txt

# Lights - generic Lineage sysfs service
PRODUCT_PACKAGES += \
    android.hardware.light-service.lineage

# Media
PRODUCT_COPY_FILES += \
    $(LOCAL_PATH)/media/media_codecs.xml:$(TARGET_COPY_OUT_VENDOR)/etc/media_codecs.xml \
    $(LOCAL_PATH)/media/media_codecs_performance.xml:$(TARGET_COPY_OUT_VENDOR)/etc/media_codecs_performance.xml \
    $(LOCAL_PATH)/media/media_codecs_vendor_audio.xml:$(TARGET_COPY_OUT_VENDOR)/etc/media_codecs_vendor_audio.xml \
    $(LOCAL_PATH)/media/media_profiles_V1_0.xml:$(TARGET_COPY_OUT_VENDOR)/etc/media_profiles_V1_0.xml \
    frameworks/av/media/libstagefright/data/media_codecs_google_audio.xml:$(TARGET_COPY_OUT_VENDOR)/etc/media_codecs_google_audio.xml \
    frameworks/av/media/libstagefright/data/media_codecs_google_telephony.xml:$(TARGET_COPY_OUT_VENDOR)/etc/media_codecs_google_telephony.xml \
    frameworks/av/media/libstagefright/data/media_codecs_google_video.xml:$(TARGET_COPY_OUT_VENDOR)/etc/media_codecs_google_video.xml

# NFC - source service; canonical RED .118 libnfc-nci.conf is vendor-owned
PRODUCT_PACKAGES += \
    android.hardware.nfc@1.2-service \
    com.android.nfc_extras \
    Tag

PRODUCT_COPY_FILES += \
    $(LOCAL_PATH)/configs/nfc/libnfc-nxp.conf:$(TARGET_COPY_OUT_VENDOR)/etc/libnfc-nxp.conf

# OMX source frontend/service; proprietary codecs remain in vendor
PRODUCT_PACKAGES += \
    android.hardware.media.omx@1.0-service \
    libc2dcolorconvert \
    libOmxCore \
    libOmxVdec \
    libOmxVenc \
    libstagefrighthw

# Power/thermal config from stock; stock power HAL itself remains vendor-owned for P0
PRODUCT_COPY_FILES += \
    $(LOCAL_PATH)/power/powerhint.xml:$(TARGET_COPY_OUT_VENDOR)/etc/powerhint.xml

# Recovery
PRODUCT_PACKAGES += \
    android.hidl.allocator@1.0.recovery \
    libhidlmemory.recovery

PRODUCT_COPY_FILES += \
    $(LOCAL_PATH)/rootdir/etc/init.recovery.qcom.rc:$(TARGET_COPY_OUT_RECOVERY)/root/init.recovery.qcom.rc

# Seccomp
PRODUCT_COPY_FILES += \
    $(LOCAL_PATH)/seccomp/mediacodec.policy:$(TARGET_COPY_OUT_VENDOR)/etc/seccomp_policy/mediacodec.policy \
    $(LOCAL_PATH)/seccomp/mediaextractor.policy:$(TARGET_COPY_OUT_VENDOR)/etc/seccomp_policy/mediaextractor.policy

# Sensors wrapper; sensor HAL data remains vendor-owned
PRODUCT_PACKAGES += \
    android.hardware.sensors@1.0-impl:64 \
    android.hardware.sensors@1.0-service

# Qualcomm partition mount-point helpers
PRODUCT_PACKAGES += \
    vendor_bt_firmware_mountpoint \
    vendor_dsp_mountpoint \
    vendor_firmware_mnt_mountpoint

# Hardware feature declarations verified from stock .109 / physical product
PRODUCT_COPY_FILES += \
    frameworks/native/data/etc/android.hardware.audio.low_latency.xml:$(TARGET_COPY_OUT_VENDOR)/etc/permissions/android.hardware.audio.low_latency.xml \
    frameworks/native/data/etc/android.hardware.bluetooth.xml:$(TARGET_COPY_OUT_VENDOR)/etc/permissions/android.hardware.bluetooth.xml \
    frameworks/native/data/etc/android.hardware.bluetooth_le.xml:$(TARGET_COPY_OUT_VENDOR)/etc/permissions/android.hardware.bluetooth_le.xml \
    frameworks/native/data/etc/android.hardware.camera.flash-autofocus.xml:$(TARGET_COPY_OUT_VENDOR)/etc/permissions/android.hardware.camera.flash-autofocus.xml \
    frameworks/native/data/etc/android.hardware.camera.front.xml:$(TARGET_COPY_OUT_VENDOR)/etc/permissions/android.hardware.camera.front.xml \
    frameworks/native/data/etc/android.hardware.camera.full.xml:$(TARGET_COPY_OUT_VENDOR)/etc/permissions/android.hardware.camera.full.xml \
    frameworks/native/data/etc/android.hardware.camera.raw.xml:$(TARGET_COPY_OUT_VENDOR)/etc/permissions/android.hardware.camera.raw.xml \
    frameworks/native/data/etc/android.hardware.fingerprint.xml:$(TARGET_COPY_OUT_VENDOR)/etc/permissions/android.hardware.fingerprint.xml \
    frameworks/native/data/etc/android.hardware.location.gps.xml:$(TARGET_COPY_OUT_VENDOR)/etc/permissions/android.hardware.location.gps.xml \
    frameworks/native/data/etc/android.hardware.nfc.hce.xml:$(TARGET_COPY_OUT_VENDOR)/etc/permissions/android.hardware.nfc.hce.xml \
    frameworks/native/data/etc/android.hardware.nfc.xml:$(TARGET_COPY_OUT_VENDOR)/etc/permissions/android.hardware.nfc.xml \
    frameworks/native/data/etc/android.hardware.opengles.aep.xml:$(TARGET_COPY_OUT_VENDOR)/etc/permissions/android.hardware.opengles.aep.xml \
    frameworks/native/data/etc/android.hardware.sensor.accelerometer.xml:$(TARGET_COPY_OUT_VENDOR)/etc/permissions/android.hardware.sensor.accelerometer.xml \
    frameworks/native/data/etc/android.hardware.sensor.compass.xml:$(TARGET_COPY_OUT_VENDOR)/etc/permissions/android.hardware.sensor.compass.xml \
    frameworks/native/data/etc/android.hardware.sensor.gyroscope.xml:$(TARGET_COPY_OUT_VENDOR)/etc/permissions/android.hardware.sensor.gyroscope.xml \
    frameworks/native/data/etc/android.hardware.sensor.light.xml:$(TARGET_COPY_OUT_VENDOR)/etc/permissions/android.hardware.sensor.light.xml \
    frameworks/native/data/etc/android.hardware.sensor.proximity.xml:$(TARGET_COPY_OUT_VENDOR)/etc/permissions/android.hardware.sensor.proximity.xml \
    frameworks/native/data/etc/android.hardware.telephony.cdma.xml:$(TARGET_COPY_OUT_VENDOR)/etc/permissions/android.hardware.telephony.cdma.xml \
    frameworks/native/data/etc/android.hardware.telephony.gsm.xml:$(TARGET_COPY_OUT_VENDOR)/etc/permissions/android.hardware.telephony.gsm.xml \
    frameworks/native/data/etc/android.hardware.touchscreen.multitouch.jazzhand.xml:$(TARGET_COPY_OUT_VENDOR)/etc/permissions/android.hardware.touchscreen.multitouch.jazzhand.xml \
    frameworks/native/data/etc/android.hardware.usb.accessory.xml:$(TARGET_COPY_OUT_VENDOR)/etc/permissions/android.hardware.usb.accessory.xml \
    frameworks/native/data/etc/android.hardware.usb.host.xml:$(TARGET_COPY_OUT_VENDOR)/etc/permissions/android.hardware.usb.host.xml \
    frameworks/native/data/etc/android.hardware.vulkan.compute-0.xml:$(TARGET_COPY_OUT_VENDOR)/etc/permissions/android.hardware.vulkan.compute.xml \
    frameworks/native/data/etc/android.hardware.vulkan.level-0.xml:$(TARGET_COPY_OUT_VENDOR)/etc/permissions/android.hardware.vulkan.level.xml \
    frameworks/native/data/etc/android.hardware.vulkan.version-1_0_3.xml:$(TARGET_COPY_OUT_VENDOR)/etc/permissions/android.hardware.vulkan.version.xml \
    frameworks/native/data/etc/android.hardware.wifi.direct.xml:$(TARGET_COPY_OUT_VENDOR)/etc/permissions/android.hardware.wifi.direct.xml \
    frameworks/native/data/etc/android.hardware.wifi.xml:$(TARGET_COPY_OUT_VENDOR)/etc/permissions/android.hardware.wifi.xml \
    frameworks/native/data/etc/android.software.midi.xml:$(TARGET_COPY_OUT_VENDOR)/etc/permissions/android.software.midi.xml

# Physical key layout
PRODUCT_COPY_FILES += \
    $(LOCAL_PATH)/keylayout/gpio-keys.kl:$(TARGET_COPY_OUT_VENDOR)/usr/keylayout/gpio-keys.kl

# USB source service
PRODUCT_PACKAGES += android.hardware.usb@1.3-service.dual_role_usb

# Vibrator source service
PRODUCT_PACKAGES += vendor.qti.hardware.vibrator.service

# VNDK compatibility for legacy vendor binaries in recovery
PRODUCT_COPY_FILES += \
    prebuilts/vndk/v32/arm64/arch-arm64-armv8-a/shared/llndk-stub/libvndksupport.so:$(TARGET_COPY_OUT_RECOVERY)/root/system/lib64/libvndksupport.so

# Wi-Fi
PRODUCT_COPY_FILES += \
    $(LOCAL_PATH)/wifi/p2p_supplicant_overlay.conf:$(TARGET_COPY_OUT_VENDOR)/etc/wifi/p2p_supplicant_overlay.conf \
    $(LOCAL_PATH)/wifi/wifi_concurrency_cfg.txt:$(TARGET_COPY_OUT_VENDOR)/etc/wifi/wifi_concurrency_cfg.txt \
    $(LOCAL_PATH)/wifi/wpa_supplicant_overlay.conf:$(TARGET_COPY_OUT_VENDOR)/etc/wifi/wpa_supplicant_overlay.conf \
    $(LOCAL_PATH)/wifi/WCNSS_qcom_cfg.ini:$(TARGET_COPY_OUT_VENDOR)/firmware/wlan/qca_cld/WCNSS_qcom_cfg.ini

PRODUCT_PACKAGES += \
    android.hardware.wifi-service \
    hostapd \
    hostapd_cli \
    libwifi-hal-qcom \
    libwpa_client \
    WifiOverlay \
    wpa_supplicant \
    wpa_supplicant.conf

# Soong namespaces needed by selected source modules
PRODUCT_SOONG_NAMESPACES += \
    $(LOCAL_PATH) \
    hardware/google/interfaces \
    hardware/google/pixel \
    hardware/qcom-caf/bt/libbt-vendor \
    hardware/qcom-caf/common/libqti-perfd-client

# Do not claim a modern kernel VINTF pass while using stock 4.4.78.
PRODUCT_OTA_ENFORCE_VINTF_KERNEL_REQUIREMENTS := false
