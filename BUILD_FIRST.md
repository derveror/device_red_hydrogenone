# Build and boot gates — RED Hydrogen One / LineageOS 22.2

## Current state

The user reports a successful complete build, followed by a failed boot.
For that existing workspace, the next step is collecting the existing boot
failure with [BOOT_DIAGNOSTICS.md](docs/BOOT_DIAGNOSTICS.md), not repeating
`m nothing` as if the build had never succeeded.

Current device and vendor branch: `codex/lineage-22.2-bringup`.
The exact compatible vendor SHA remains pinned in
`docs/reference/cross-tree-lock.json`. Hardware authority is RED .118;
cheryl device + vendor is the primary reference and mata is secondary.

The selected .118 prebuilt is Linux 4.4.153+ and lacks the BPF syscall required
by the normal LineageOS 22.2 BPF-loading path. A successful build or the init
import correction does not resolve that kernel incompatibility.

## New workspace or changed sources

The fresh-workspace manifest instructions are in `docs/manifests/README.md`.
From a complete source top, the existing preflight runner validates the
checkouts and vendor pin without changing them:

```bash
bash device/red/hydrogenone/tools/build/run_m_nothing_preflight.sh --validate-only
bash device/red/hydrogenone/tools/build/run_m_nothing_preflight.sh
```

The runner selects `lineage_hydrogenone-bp1a-userdebug`, runs `m nothing`,
and preserves output, revisions and the command exit status under
`out/hydrogenone-build-logs/`. The explicit release is the user's working
LineageOS 22.2 target. No source reset or forced sync is needed.

## Rebuild after the boot evidence is reviewed

For the user's existing source top, this records a full incremental build:

```bash
cd /home/surface/los
mkdir -p logs/hydrogenone
(
    set -e
    set -o pipefail
    source build/envsetup.sh
    lunch lineage_hydrogenone-bp1a-userdebug
    m bacon 2>&1 | tee "logs/hydrogenone/build_$(date +%Y%m%d_%H%M%S).log"
)
```

The init import is installed in vendor. Rebuilding or replacing only boot.img
cannot deliver that correction to an existing vendor image. Use matching built
artifacts after review. No flash or formatting command is prescribed here.
Image compilation still needs boot/header, mount, SELinux, linker and physical
hardware validation. Keep the existing failed image and its logs available.
