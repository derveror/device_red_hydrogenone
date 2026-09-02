# RED Hydrogen One `.118` build-property provenance

The previously located public property capture has now been checked against files extracted from the canonical unencrypted `.118` archive. The key build identity matches the stock images and is no longer the sole source for these facts.

## Directly verified from extracted stock

```text
ro.build.id=PKQ1.190118.001
ro.build.display.id=H1A1000.082ho.01.00.10r.118
ro.build.version.incremental=118
ro.build.version.release=9
ro.build.version.sdk=28
ro.build.version.security_patch=2019-04-05
ro.vendor.build.security_patch=2018-08-05
ro.build.type=userdebug
ro.build.tags=release-keys
ro.build.fingerprint=RED/HydrogenONE/HydrogenONE:9/PKQ1.190118.001/118:userdebug/release-keys
ro.product.model=H1A1000
ro.product.name=HydrogenONE
ro.product.device=HydrogenONE
ro.board.platform=msm8998
ro.product.first_api_level=27
ro.build.system_root_image=true
ro.build.ab_update=true
ro.treble.enabled=true
```

The canonical package-level `build.prop` SHA-256 is:

```text
11ac6401f766b8a7f95a860817e05059d398f2a6d0d474664ee3dd1bbc52d545
```

The extracted vendor `build.prop` SHA-256 is:

```text
0db904462c5e464a40a5574314f040143322ec31cf6d6f0481ca9c9d3747ffe4
```

## Historical public source

The independent capture remains useful provenance and was pinned at commit:

```text
xdaGari/tadiphone-buildprop-archive
4f53547b326b17b140fb70e9f2aebd2344cc3af6
```

Its filenames and Git blob SHAs were:

- `system.system.build.prop`: `1f723ebfba74471d96ff416e8a67286495136786`
- `system.system.product.build.prop`: `95ae909ca9297797f53ababe780def7fd3bb02d5`
- `vendor.build.prop`: `e128605ea758112ad73dbc70c745547e86c85e33`

The source is now corroboration. The canonical extracted archive controls all later decisions.

## Android 15 boundary

Properties such as Bluetooth `cherokee`, NFC `nqx.default`, DSDS, Qualcomm RIL, IMS, camera, audio, FPC, CloudMinds, and Leia settings are candidates for dependency mapping—not automatic additions to Android 15. Each retained property needs an owning process, an Android 15 property context, a correct partition, and runtime validation.
