# RED Hydrogen One .118 radio init evidence

This is a diagnostic evidence record, not a donor-derived radio configuration.

Stock archive SHA-256: `7277a1accf9595bb727f2189863cf5f6249dd99322e2953432bca6e448365f1e`

## Summary

- Multi-SIM property values observed: `['dsds']`
- qcrild services defined by stock init: `['vendor.qcrild', 'vendor.qcrild2', 'vendor.qcrild3']`
- qcrild instances explicitly started by stock init: `[]`
- Defined but not explicitly started: `['vendor.qcrild', 'vendor.qcrild2', 'vendor.qcrild3']`

Runtime recommendation is limited to instances explicitly started by stock init evidence; service definitions alone do not prove an instance should be started.

## Relevant properties

- `extra:build.prop:99` — `persist.data.iwlan.ims.enable=1`
- `extra:build.prop:103` — `persist.dbg.allow_ims_off=1`
- `extra:build.prop:96` — `persist.radio.VT_ENABLE=1`
- `extra:build.prop:97` — `persist.radio.VT_HYBRID_ENABLE=1`
- `extra:build.prop:100` — `persist.radio.data_con_rprt=1`
- `extra:build.prop:107` — `persist.radio.flex_map_inactive=true`
- `build.prop:90` — `persist.radio.multisim.config=dsds`
- `build.prop:47` — `persist.vendor.radio.apm_sim_not_pwdn=1`
- `build.prop:49` — `persist.vendor.radio.custom_ecc=1`
- `build.prop:50` — `persist.vendor.radio.rat_on=combine`
- `build.prop:48` — `persist.vendor.radio.sib16_support=1`
- `build.prop:87` — `rild.libpath=/system/vendor/lib64/libril-qc-qmi-1.so`
- `extra:build.prop:64` — `ro.telephony.default_network=22,22`
- `build.prop:89` — `vendor.rild.libpath=/system/vendor/lib64/libril-qc-qmi-1.so`

## Radio/IMS service definitions

- `etc/init/hw/init.qcom.rc:1038` — `ims_regmanager` -> `/system/vendor/bin/exe-ims-regmanagerprocessnative`; disabled=`True`
- `etc/init/hw/init.target.rc:441` — `vendor.ims_rtp_daemon` -> `/system/vendor/bin/ims_rtp_daemon`; disabled=`False`
- `etc/init/hw/init.target.rc:366` — `vendor.imsdatadaemon` -> `/system/vendor/bin/imsdatadaemon`; disabled=`True`
- `etc/init/hw/init.target.rc:359` — `vendor.imsqmidaemon` -> `/system/vendor/bin/imsqmidaemon`; disabled=`False`
- `etc/init/hw/init.target.rc:446` — `vendor.imsrcsservice` -> `/system/vendor/bin/imsrcsd`; disabled=`False`
- `etc/init/qcrild.rc:1` — `vendor.qcrild` -> `/vendor/bin/hw/qcrild`; disabled=`True`
- `etc/init/qcrild.rc:8` — `vendor.qcrild2` -> `/vendor/bin/hw/qcrild -c 2`; disabled=`True`
- `etc/init/qcrild.rc:15` — `vendor.qcrild3` -> `/vendor/bin/hw/qcrild -c 3`; disabled=`True`
- `etc/init/rild.rc:1` — `vendor.ril-daemon` -> `/vendor/bin/hw/rild`; disabled=`True`
- `etc/init/vendor.rild.rc:1` — `vendor.ril-daemon` -> `/vendor/bin/hw/rild`; disabled=`True`
- `etc/init/hw/init.qcom.rc:1055` — `vendor.ril-daemon2` -> `/vendor/bin/hw/rild -c 2`; disabled=`True`
- `etc/init/hw/init.qcom.rc:1062` — `vendor.ril-daemon3` -> `/vendor/bin/hw/rild -c 3`; disabled=`True`

## Explicit starts

- `etc/init/hw/init.qcom.rc:1044` under `property:persist.ims.regmanager.mode=1` — `start ims_regmanager`
- `etc/init/hw/init.target.rc:430` under `property:vendor.ims.QMI_DAEMON_STATUS=1` — `start vendor.imsdatadaemon`
