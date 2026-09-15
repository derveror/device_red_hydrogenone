#include <string>

#include <BootControlClient.h>
#include <android-base/logging.h>
#include <android-base/properties.h>

#include "legacy_avb1_verifier_policy.h"
#include "update_verifier/update_verifier.h"

int main(int argc, char **argv) {
  if (android::base::GetProperty("ro.boot.slot_suffix", "").empty()) {
    return 0;
  }

  android::base::InitLogging(argv, &android::base::KernelLogger);

  const std::string verified_boot_state =
      android::base::GetProperty("ro.boot.verifiedbootstate", "");
  const std::string verity_mode =
      android::base::GetProperty("ro.boot.veritymode", "");
  const std::string avb_version =
      android::base::GetProperty("ro.boot.avb_version", "");
  const std::string vbmeta_device_state =
      android::base::GetProperty("ro.boot.vbmeta.device_state", "");
  const bool virtual_ab_enabled =
      android::base::GetBoolProperty("ro.virtual_ab.enabled", false);

  if (!hydrogenone::ShouldSkipLegacyAvb1Verification(
          verified_boot_state, verity_mode, avb_version, vbmeta_device_state,
          virtual_ab_enabled)) {
    return update_verifier(argc, argv);
  }

  LOG(WARNING) << "Unlocked RED AVB1 reports dm-verity logging mode while "
                  "using a linear target; marking without block verification.";

  const auto module = android::hal::BootControlClient::WaitForService();
  if (module == nullptr) {
    LOG(ERROR) << "Error getting bootctrl module.";
    return update_verifier(argc, argv);
  }

  const int32_t current_slot = module->GetCurrentSlot();
  const auto is_successful = module->IsSlotMarkedSuccessful(current_slot);
  if (!is_successful.has_value()) {
    LOG(ERROR) << "Failed to read successful state for slot " << current_slot;
    return update_verifier(argc, argv);
  }

  if (is_successful.value()) {
    LOG(INFO) << "Booting slot " << current_slot
              << ": isSlotMarkedSuccessful=1";
    return 0;
  }

  const auto result = module->MarkBootSuccessful();
  if (!result.success) {
    LOG(ERROR) << "Error marking booted successfully: " << result.errMsg;
    return update_verifier(argc, argv);
  }

  LOG(INFO) << "Marked legacy RED AVB1 slot " << current_slot
            << " as booted successfully.";
  if (!android::base::SetProperty("ota.warm_reset", "0")) {
    LOG(WARNING) << "Failed to reset the warm reset flag";
  }

  return 0;
}
