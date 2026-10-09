# ExecSurface examples — current v1 first

**For new users, use stable ExecSurface v1.0.0, not the historical Alpha tags.**

| Path | Status | Recommended use |
| --- | --- | --- |
| [Stable v1 GitHub Action consumer](github-action-consumer-v1.yml) | **Current v1** (`AETHERXGLOBAL/execsurface@v1`) | Copy-ready Rust CI integration after explicit baseline and policy custody setup |
| [Five-Minute Start](../docs/QUICKSTART_5_MIN.md) | **Current v1** | Test the published v1 binary against controlled PASS/REVIEW scenarios |
| [Python/pytest PASS→REVIEW](python-pytest/README.md) | **Historical Alpha.5** | Replay preserved third-party contributed evidence only; not v1 onboarding |
| [Minimal controlled drift](hello-drift.sh) | Check selected release/CLI contract | Small local demonstration |

## Supported stable release

- GitHub Release: https://github.com/AETHERXGLOBAL/execsurface/releases/tag/v1.0.0
- Stable Action: `AETHERXGLOBAL/execsurface@v1`
- Immutable Action: `AETHERXGLOBAL/execsurface@v1.0.0`
- Linux x86_64 with native `ptrace`; see [current status](../docs/STATUS.md).
- A PASS is an execution-surface drift result, **not** proof that the target command exited successfully. Keep the native test/build step independent.

## Historical evidence is not a current default

The Python/pytest recipe contributed through [PR #128](https://github.com/AETHERXGLOBAL/execsurface/pull/128) by @astrogilda deliberately preserves the immutable Alpha.5 binary pin, original receipts, and negative nondeterminism evidence. It was **not** relabeled as a v1 test or independently certified for v1. The historical example remains discoverable for exact replay; new installations and workflows should use the v1 links above.

The stable v1 copy-ready GitHub Action workflow builds on the original external example direction proposed by @PandaHUN777 in [PR #127](https://github.com/AETHERXGLOBAL/execsurface/pull/127), with added v1 target-success gating, external custody pins and a copy-safe documentation link.

No Alpha result or external community comment should be represented as independent v1 adoption.
