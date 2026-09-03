# RED Hydrogen One H1A1000 - LineageOS 22.2 product
$(call inherit-product, $(SRC_TARGET_DIR)/product/core_64_bit.mk)
$(call inherit-product, vendor/lineage/config/common_full_phone.mk)
$(call inherit-product, $(SRC_TARGET_DIR)/product/full_base_telephony.mk)
$(call inherit-product, $(SRC_TARGET_DIR)/product/product_launched_with_o_mr1.mk)

# Keep the Android 9 vendor ABI available for the stock RED .118 blobs. This is
# a product variable and must be set before product configuration becomes
# readonly; assigning it from BoardConfigVendor.mk breaks Android 15 dumpvars.
PRODUCT_EXTRA_VNDK_VERSIONS += 28

# Verified RED .118 proprietary vendor output is required for a real build.
$(call inherit-product, vendor/red/hydrogenone/hydrogenone-vendor.mk)

# Device definition is inherited last, matching maintained Lineage device trees.
$(call inherit-product, device/red/hydrogenone/device.mk)

PRODUCT_NAME := lineage_hydrogenone
PRODUCT_DEVICE := hydrogenone
PRODUCT_BRAND := RED
PRODUCT_MODEL := H1A1000
PRODUCT_MANUFACTURER := RED
PRODUCT_RELEASE_NAME := hydrogenone

PRODUCT_ACTIONABLE_COMPATIBLE_PROPERTY_DISABLE := true
PRODUCT_COMPATIBLE_PROPERTY_OVERRIDE := true
PRODUCT_CHARACTERISTICS := nosdcard

# Canonical RED .118 identity used for proprietary compatibility.
PRODUCT_BUILD_PROP_OVERRIDES += \
    BuildFingerprint=RED/HydrogenONE/HydrogenONE:9/PKQ1.190118.001/118:userdebug/release-keys \
    DeviceName=HydrogenONE
