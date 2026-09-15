#include "legacy_avb1_verifier_policy.h"

namespace hydrogenone {

bool ShouldSkipLegacyAvb1Verification(std::string_view verified_boot_state,
                                      std::string_view verity_mode,
                                      std::string_view avb_version,
                                      std::string_view vbmeta_device_state,
                                      bool virtual_ab_enabled) {
  return verified_boot_state == "orange" && verity_mode == "logging" &&
         avb_version.empty() && vbmeta_device_state.empty() &&
         !virtual_ab_enabled;
}

} // namespace hydrogenone
