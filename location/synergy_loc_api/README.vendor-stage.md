# Optional `libsynergy_loc_api` backend

`libsynergy_loc_api` links against proprietary Qualcomm modules
`libqmi_cci` and `libqmi_common_so`. Those modules are generated only after
RED `.109` blobs are extracted into `vendor/red/hydrogenone`.

The RED `.109` GNSS configuration supplied with this tree does not set
`GNSS_DEPLOYMENT=1` (SS5), so the normal `libloc_api_v02.so` backend is used.
For the source-only `m nothing` gate, Soong therefore must not parse the
optional synergy module. Its blueprint is stored as `Android.bp.vendor-ready`
and it is absent from the base `PRODUCT_PACKAGES` list.

Do not enable it merely because the QMI blobs exist. Enable it only if later
stock inspection or device logs prove that Hydrogen One actually selects the
SS5 backend. In that case, after the QMI prebuilt modules exist:

1. Rename `Android.bp.vendor-ready` to `Android.bp`.
2. Add `libsynergy_loc_api` to `PRODUCT_PACKAGES`.
3. Run `m nothing -j1`, then `m vendorimage -j1`.
