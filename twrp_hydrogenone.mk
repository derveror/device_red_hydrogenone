$(call inherit-product, $(SRC_TARGET_DIR)/product/base.mk)
$(call inherit-product, $(SRC_TARGET_DIR)/product/core_64_bit_only.mk)
$(call inherit-product, vendor/twrp/config/common.mk)
$(call inherit-product, device/red/hydrogenone/device.mk)

PRODUCT_DEVICE := hydrogenone
PRODUCT_NAME := twrp_hydrogenone
PRODUCT_BRAND := RED
PRODUCT_MODEL := H1A1000
PRODUCT_MANUFACTURER := RED
