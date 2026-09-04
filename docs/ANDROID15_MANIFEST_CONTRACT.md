# RED Hydrogen One Android 15 device VINTF ownership

**Target:** LineageOS 22.2 / Android 15 API 35  
**Stock authority:** RED `.118` (`7277a1accf9595bb727f2189863cf5f6249dd99322e2953432bca6e448365f1e`)

`device/red/hydrogenone/manifest.xml` owns only source-built HAL instances that require the device manifest. Proprietary instances are owned by `vendor/red/hydrogenone` service fragments and are not duplicated here.

## Device-manifest source ownership

The device manifest currently declares exactly these source-owned interfaces:

- audio 6.0 / `IDevicesFactory/default`;
- audio effect 6.0 / `IEffectsFactory/default`;
- Bluetooth audio 2.1 / `IBluetoothAudioProvidersFactory/default`;
- camera provider 2.4 / `ICameraProvider/legacy/0`;
- gatekeeper 1.0 / `IGatekeeper/default`;
- GNSS 1.0 / `IGnss/default`;
- graphics allocator 2.0 / `IAllocator/default`;
- graphics composer 2.1 / `IComposer/default`;
- graphics mapper 2.1 / `IMapper/default` as `passthrough`, `arch="32+64"`;
- keymaster 3.0 / `IKeymasterDevice/default`;
- NFC 1.2 / `INfc/default`;
- sensors 1.0 / `ISensors/default`;
- soundtrigger 2.2 / `ISoundTriggerHw/default`.

The versions follow the actual LineageOS 22.2 packages selected by `device.mk`. GNSS is the intentional exception to the newer `mata` frontend: Hydrogen One uses the maintained `cheryl` LineageOS 22.2 Qualcomm GPS closure because RED `.118` proprietary location consumers require the older Pie-era `LocApiBase` ABI.

## GNSS source HAL ownership

The active source service is:

```text
gps/android/Android.bp
android.hardware.gnss@1.0-service-qti
```

Unlike the removed 2.1 frontend, it has no private VINTF fragment, so `manifest.xml` owns `android.hardware.gnss@1.0::IGnss/default`. Vendor tests continue to forbid the retained Android 9 stock GNSS wrapper from registering the same default instance.

## Vendor-owned HALs

Fingerprint, Bluetooth HCI/FM/ANT, OMX, Wi-Fi display, RED thermal3d, Leia display, eSE, and the stock radio/IMS/UIM contract are declared by verified fragments in `vendor/red/hydrogenone` on the Android 15 contract branch. GNSS and standard NFC stock service wrappers were removed from vendor because the Android 15 device tree owns their standard default instances.

This split is enforced by `tests/test_android15_manifest_contract.py` and the vendor VINTF tests.
