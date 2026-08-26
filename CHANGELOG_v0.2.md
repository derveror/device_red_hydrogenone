# v0.2
- Confirmed current LineageOS 22.2 Essential `mata` is the primary architecture donor.
- Confirmed current `mata` kernel is Linux 4.4.302, suitable as later source-kernel base.
- Added stock vendor init references and H1-specific SmartPort/FPC notes.
- Scanned all supplied vendor ELF dependencies for Android 8.1 HIDL ABI breakage.
- Added broad proprietary extraction inventory (excluding old compiled SELinux/VINTF outputs).
- Added conservative extract-utils HIDL fixup scaffold.
- Documented stock `/system/lib/modules` dependency of the prebuilt RED kernel.
- Added kernel port plan and donor matrix.
