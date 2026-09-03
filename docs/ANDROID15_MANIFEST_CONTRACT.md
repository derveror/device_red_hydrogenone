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
- graphics allocator 2.0 / `IAllocator/default`;
- graphics composer 2.1 / `IComposer/default`;
- graphics mapper 2.1 / `IMapper/default` as `passthrough`, `arch="32+64"`;
- keymaster 3.0 / `IKeymasterDevice/default`;
- NFC 1.2 / `INfc/default`;
- sensors 1.0 / `ISensors/default`;
- soundtrigger 2.2 / `ISoundTriggerHw/default`.

The versions follow the actual LineageOS 22.2 packages selected by `device.mk` and the current official MSM8998/mata pattern where applicable.

## Self-fragmented source HAL

GNSS is deliberately absent from the monolithic device manifest. The local source service:

```text
gps/android/2.1/Android.bp
android.hardware.gnss@2.1-service-qti
```

owns `android.hardware.gnss@2.1-service-qti.xml` through its `vintf_fragments` property. Declaring GNSS again in `manifest.xml` would create duplicate ownership.

## Vendor-owned HALs

Fingerprint, Bluetooth HCI/FM/ANT, OMX, Wi-Fi display, RED thermal3d, Leia display, eSE, and the stock radio/IMS/UIM contract are declared by verified fragments in `vendor/red/hydrogenone` on the Android 15 contract branch. GNSS and standard NFC stock service wrappers were removed from vendor because the Android 15 device tree owns their standard default instances.

This split is enforced by `tests/test_android15_manifest_contract.py` and the vendor VINTF tests.
