# RED Hydrogen One H1A1000 - LineageOS 22.2 product
$(call inherit-product, $(SRC_TARGET_DIR)/product/core_64_bit.mk)
$(call inherit-product, vendor/lineage/config/common_full_phone.mk)
$(call inherit-product, $(SRC_TARGET_DIR)/product/full_base_telephony.mk)
$(call inherit-product, $(SRC_TARGET_DIR)/product/product_launched_with_o_mr1.mk)

# Proprietary output is optional during the source-only compile stage.
$(call inherit-product-if-exists, vendor/red/hydrogenone/hydrogenone-vendor.mk)

# Device definition is inherited last, matching maintained Lineage device trees.
$(call inherit-product, device/red/hydrogenone/device.mk)

PRODUCT_NAME := lineage_hydrogenone
PRODUCT_DEVICE := hydrogenone
PRODUCT_BRAND := RED
PRODUCT_MODEL := Hydrogen One
PRODUCT_MANUFACTURER := RED
PRODUCT_RELEASE_NAME := hydrogenone

PRODUCT_ACTIONABLE_COMPATIBLE_PROPERTY_DISABLE := true
PRODUCT_COMPATIBLE_PROPERTY_OVERRIDE := true
PRODUCT_CHARACTERISTICS := nosdcard

# Stock identity for proprietary compatibility and complete partition fingerprints.
PRODUCT_BUILD_PROP_OVERRIDES += \
    BuildDesc="hamberger_verizon-user 8.1.0 H1A1000.010ho.01.01.01r.109 109 release-keys" \
    BuildFingerprint=RED/HydrogenONE/HydrogenONE:8.1.0/H1A1000.010ho.01.01.01r.109/109:user/release-keys \
    DeviceName=HydrogenONE
