# RED Hydrogen One cross-tree copy ownership

Vendor commit: `d30ac19025b348ca61535afaaecb23b95347b2f4`
Stock authority: `.118` / `7277a1accf9595bb727f2189863cf5f6249dd99322e2953432bca6e448365f1e`.

## Result

**0 `PRODUCT_COPY_FILES` destination collisions.**

Ownership decisions:
- `vendor/etc/libnfc-nci.conf` — vendor-owned exact RED `.118` hardware config.
- `vendor/etc/thermal-engine.conf` — vendor-owned exact RED `.118` hardware config.
- `vendor/etc/permissions/android.hardware.nfc.hce.xml` — source/device-owned AOSP feature declaration.
- `vendor/etc/permissions/android.hardware.nfc.xml` — source/device-owned AOSP feature declaration.

Device copy destinations: `129`.
Vendor copy destinations: `48`.
