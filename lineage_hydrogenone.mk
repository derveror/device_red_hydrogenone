# Inherit from the common 64-bit telephony product configuration
$(call inherit-product, $(SRC_TARGET_DIR)/product/core_64_bit.mk)
$(call inherit-product, $(SRC_TARGET_DIR)/product/full_base_telephony.mk)

# Device
$(call inherit-product, device/red/hydrogenone/device.mk)

# Lineage
$(call inherit-product, vendor/lineage/config/common_full_phone.mk)

PRODUCT_NAME := lineage_hydrogenone
PRODUCT_DEVICE := hydrogenone
PRODUCT_MANUFACTURER := RED
PRODUCT_BRAND := RED
PRODUCT_MODEL := H1A1000
