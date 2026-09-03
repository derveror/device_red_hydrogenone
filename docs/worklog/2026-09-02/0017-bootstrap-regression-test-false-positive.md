# Action 0017 — Bootstrap documentation regression test false positive

**Production run:** `33687602610`  
**Failing job:** `100438678289`  
**Commit under test:** `cbd6a66b239d304d6b4381d6e40075f83c87af6f`

## Observed result

The permanent unit-test stage ran 94 tests. All established device/vendor/stock/build-preflight/local-manifest contracts passed except one newly added bootstrap documentation assertion:

```text
test_fresh_bootstrap_does_not_force_sync_or_skip_first_gate
```

## Root cause

The bootstrap document correctly uses this actual sync command:

```bash
repo sync \
  -c \
  --no-clone-bundle \
  --no-tags \
  -j"$(nproc --all)"
```

It does **not** pass `--force-sync`.

However, the prose immediately below intentionally states:

```text
This bootstrap intentionally does not use `--force-sync`...
```

The regression test used a naive whole-document assertion:

```python
self.assertNotIn("--force-sync", text)
```

so it failed on the safety explanation itself rather than on an unsafe command.

## Project impact

No build/runtime configuration is affected. This is a regression-test false positive. The documented sync command is already non-forcing and should remain unchanged.

## Next action

Refine the test to inspect Bash code blocks containing `repo sync` and assert that `--force-sync` is absent from those command blocks, while allowing explanatory prose to mention the option. Re-run permanent CI and require full GREEN.
