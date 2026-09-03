#!/usr/bin/env -S PYTHONPATH=../../../tools/extract-utils python3
# SPDX-License-Identifier: Apache-2.0
# H1A1000 / HydrogenONE LineageOS 22.2 bring-up extraction scaffold.

from extract_utils.fixups_blob import blob_fixup, blob_fixups_user_type
from extract_utils.fixups_lib import lib_fixups
from extract_utils.main import ExtractUtils, ExtractUtilsModule

# Legacy HIDL fixup groups were derived from older Hydrogen One vendor ELF
# dependencies. The authoritative payload for the current bring-up is RED .118
# Android 9; keep these groups only as compatibility-analysis helpers until the
# full .118 extraction contract is regenerated from the canonical vendor manifest.
from tools.legacy_hidl_fixup_paths import (
    HIDL_BASE_ONLY,
    HIDL_BASE_TRANSPORT,
    HIDL_BASE_TRANSPORT_HWBINDER,
)

namespace_imports = [
    'device/red/hydrogenone',
    'hardware/qcom-caf/msm8998',
    'hardware/qcom-caf/wlan',
    'vendor/qcom/opensource/data-ipa-cfg-mgr-legacy-um',
    'vendor/qcom/opensource/dataservices',
]

# Legacy split-HIDL transport compatibility. The rare binaries that reference
# transport/hwbinder without libhidlbase are intentionally not auto-fixed here;
# handle them only from linker evidence instead of guessing.
blob_fixups: blob_fixups_user_type = {
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
