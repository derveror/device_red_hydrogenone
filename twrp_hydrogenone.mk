# RED Hydrogen One H1A1000 — TWRP 12.1
LOCAL_PATH := device/red/hydrogenone

$(call inherit-product, $(SRC_TARGET_DIR)/product/core_64_bit.mk)
$(call inherit-product, $(SRC_TARGET_DIR)/product/base.mk)
$(call inherit-product, $(LOCAL_PATH)/twrp_device.mk)
$(call inherit-product, vendor/twrp/config/common.mk)

PRODUCT_DEVICE := hydrogenone
PRODUCT_NAME := twrp_hydrogenone
PRODUCT_BRAND := RED
PRODUCT_MODEL := H1A1000
PRODUCT_MANUFACTURER := RED
PRODUCT_RELEASE_NAME := RED Hydrogen One
