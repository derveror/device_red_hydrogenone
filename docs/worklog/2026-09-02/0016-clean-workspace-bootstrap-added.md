# Action 0016 — Add fresh LineageOS 22.2 workspace bootstrap procedure

**Repository:** `derveror/device_red_hydrogenone`  
**Branch:** `lineage-22.2-stock118-rework`  
**Bootstrap documentation commit:** `5528fb06216f40a9e8d3252aa8668ee2cdce4653`

## Action

Added:

```text
docs/manifests/README.md
```

## Scope

The procedure is explicitly for a **fresh separate source directory** and is not a reset/repair procedure for an existing Lineage workspace.

It documents:

1. creating a new source directory;
2. `repo init` for LineageOS `lineage-22.2` with Git LFS;
3. downloading the checked-in Hydrogen One local manifest from the device branch;
4. parsing the downloaded XML before sync;
5. `repo sync` without `--force-sync`;
6. running `run_m_nothing_preflight.sh --validate-only`;
7. running the real preflight only after validation passes;
8. preserving the generated `m nothing` log/metadata/status files;
9. not advancing to image/OTA targets before `m nothing` is GREEN.

## Safety choices

- The instructions do not reset or clean an existing source tree.
- They do not use `--force-sync` on the fresh checkout.
- They do not start a build before the tested preflight validates the required project revisions.
- The custom RED vendor continues to come from the checked-in local manifest, not Lineage roomservice.

## Next action

Add a lightweight repository regression test for this bootstrap document: ensure it references the production manifest URL, LineageOS 22.2, the validate-only preflight, the real preflight, and does not introduce `--force-sync`. Run permanent CI and require GREEN.
