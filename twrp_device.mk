# Recovery-only product configuration for RED Hydrogen One.
PRODUCT_USE_DYNAMIC_PARTITIONS := false
PRODUCT_SHIPPING_API_LEVEL := 27
PRODUCT_ENFORCE_ARTIFACT_PATH_REQUIREMENTS := false

PRODUCT_SYSTEM_PROPERTIES += \
    ro.product.device=hydrogenone \
    ro.product.vendor.device=hydrogenone \
    ro.twrp.target.devices=hydrogenone,HydrogenONE,H1A1000
