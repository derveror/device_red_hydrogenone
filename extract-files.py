#!/usr/bin/env -S PYTHONPATH=../../../tools/extract-utils python3
# SPDX-License-Identifier: Apache-2.0
# H1A1000 / HydrogenONE LineageOS 22.2 bring-up extraction scaffold.

from extract_utils.fixups_blob import blob_fixup, blob_fixups_user_type
from extract_utils.fixups_lib import lib_fixups
from extract_utils.main import ExtractUtils, ExtractUtilsModule

from tools.hidlbase_shim_fixup_paths import HIDLBASE_SHIM_FIXUP_PATHS

namespace_imports = [
    'device/red/hydrogenone',
    'hardware/qcom-caf/msm8998',
    'hardware/qcom-caf/wlan',
    'vendor/qcom/opensource/data-ipa-cfg-mgr-legacy-um',
    'vendor/qcom/opensource/dataservices',
]

# Canonical RED .118 Android 9 HIDL interfaces still reference the removed
# android::hardware::details::gBnConstructorMap ABI. LineageOS 22.2 provides
# the narrow compatibility implementation through libhidlbase_shim. Apply the
# exact readelf-proven path set during extraction so regenerating vendor/red/
# hydrogenone does not lose the Android 15 compatibility fix.
blob_fixups: blob_fixups_user_type = {
    HIDLBASE_SHIM_FIXUP_PATHS: blob_fixup().add_needed('libhidlbase_shim.so'),
}

module = ExtractUtilsModule(
    'hydrogenone',
    'red',
    blob_fixups=blob_fixups,
    lib_fixups=lib_fixups,
    namespace_imports=namespace_imports,
)

if __name__ == '__main__':
    ExtractUtils.device(module).run()
