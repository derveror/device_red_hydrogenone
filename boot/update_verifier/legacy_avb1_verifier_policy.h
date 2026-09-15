#pragma once

#include <string_view>

namespace hydrogenone {

bool ShouldSkipLegacyAvb1Verification(std::string_view verified_boot_state,
                                      std::string_view verity_mode,
                                      std::string_view avb_version,
                                      std::string_view vbmeta_device_state,
                                      bool virtual_ab_enabled);

} // namespace hydrogenone
