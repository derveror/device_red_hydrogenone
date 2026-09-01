LOCAL_PATH := device/red/hydrogenone

PRODUCT_SHIPPING_API_LEVEL := 27
PRODUCT_CHARACTERISTICS := nosdcard

PRODUCT_PROPERTY_OVERRIDES += \
    ro.hardware.keystore=msm8998 \
    ro.hardware.gatekeeper=msm8998
