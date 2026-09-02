# Action 0015 — Replace stale first-build instructions with current `.118` preflight

**Repository:** `derveror/device_red_hydrogenone`  
**Branch:** `lineage-22.2-stock118-rework`  
**Documentation commit:** `0aec6a162ccd97edb9fc6f707487d52df9342abf`

## Action

Updated `BUILD_FIRST.md` after the SHA-conflict attempt recorded in Action 0014.

## Removed stale guidance

The previous document incorrectly directed the project to:

- use the old RED `.109` 4.4.78 prebuilt kernel;
- run `m bacon` as the first build gate;
- describe the proprietary vendor state as if it still needed ad-hoc extraction.

Those statements no longer matched the verified repository state.

## Current guidance

`BUILD_FIRST.md` now states:

- canonical stock authority is RED `.118`;
- transitional bring-up kernel is the exact `.118` 4.4.153+ payload already regression-tested by SHA;
- reproducible source acquisition uses `docs/manifests/hydrogenone-lineage-22.2.xml`;
- first workspace check is:

```bash
bash device/red/hydrogenone/tools/build/run_m_nothing_preflight.sh --validate-only
```

- first real build gate is:

```bash
bash device/red/hydrogenone/tools/build/run_m_nothing_preflight.sh
```

which internally runs only `envsetup`, `lunch lineage_hydrogenone-userdebug`, and `m nothing` and captures complete logs.

The later `bootimage`, `vendorimage`, `systemimage`, target-files and OTA gates are explicitly blocked until `m nothing` is GREEN.

## Result

There is now one current first-build entrypoint instead of conflicting historical instructions.

## Next action

Confirm permanent CI remains GREEN after this documentation cleanup. Then add the clean-workspace bootstrap instructions for installing the checked-in local manifest and syncing a fresh LineageOS 22.2 checkout before running the tested preflight.
