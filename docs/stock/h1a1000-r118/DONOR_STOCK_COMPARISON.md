# RED `.118` stock versus LineageOS 22.2 donor vendor trees

This comparison measures exact paths and SHA-256 values. It does not declare donor blobs compatible merely because a path or digest matches.

## Results

| Donor archive | Listed proprietary files | Exact path + identical bytes | Same path, changed bytes | Identical bytes at moved path | Path absent from RED stock | Unique RED paths matched |
|---|---:|---:|---:|---:|---:|---:|
| Essential mata | 845 | 54 | 516 | 0 | 275 | 55 |
| Nubia msm8998-common | 445 | 93 | 271 | 0 | 81 | 95 |
| OnePlus dumpling | 50 | 0 | 14 | 0 | 36 | 0 |
| OnePlus msm8998-common | 732 | 62 | 448 | 1 | 221 | 65 |
| Razer cheryl | 710 | 119 | 350 | 1 | 240 | 123 |

Across donors, 147 unique RED stock paths have an identical donor payload. Fifty-six were classified as high-confidence platform-common evidence and 31 as medium-confidence evidence. Examples include Qualcomm CNE profiles, A530/A540/IPA firmware, QSEE/gatekeeper/keystore libraries, RFSA DSP libraries, qcril database migrations, and performance profiles.

## Interpretation

- Dumpling's device-specific vendor archive has **zero** exact RED matches. It is useful for wiring patterns, not as a RED blob source.
- Common vendor archives contain real Qualcomm/MSM8998 overlap, but hundreds of same-path files differ by build, vendor, hardware, or firmware revision.
- Cheryl has the largest exact overlap among the supplied individual archives, while Nubia and OnePlus common trees expose useful platform grouping.
- Exact identical bytes are evidence of common origin, not proof that an Android 9 binary is valid under Android 15 linker, VINTF, SELinux, property, or framework rules.

## Adoption rule

1. Prefer the exact RED `.118` file when a proprietary consumer still exists.
2. Prefer a LineageOS/AOSP source-built replacement when maintained and compatible.
3. Use donor trees to understand module declarations, extraction fixups, dependencies, shims, VINTF fragments, and modern Android 15 integration.
4. Never import a donor-specific binary merely to satisfy a missing path.
5. Flatten justified open common configuration into `device/red/hydrogenone`; keep all RED proprietary payload in `vendor/red/hydrogenone`.
6. Do not create `device/red/msm8998-common` or `vendor/red/msm8998-common`.

The full per-file comparison is retained in the evidence package identified by `analysis-evidence.sha256`.
