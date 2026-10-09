<p align="center"><strong>AETHER X GLOBAL</strong></p>

# ExecSurface

<p align="center"><strong>Code diff shows what changed. ExecSurface shows what started happening.</strong></p>

<p align="center">
  <a href="https://github.com/AETHERXGLOBAL/execsurface/actions/workflows/ci.yml"><img alt="CI" src="https://github.com/AETHERXGLOBAL/execsurface/actions/workflows/ci.yml/badge.svg"></a>
  <a href="https://github.com/AETHERXGLOBAL/execsurface/releases"><img alt="Release" src="https://img.shields.io/github/v/release/AETHERXGLOBAL/execsurface?include_prereleases&label=release"></a>
  <img alt="License Apache-2.0" src="https://img.shields.io/badge/license-Apache--2.0-blue">
  <img alt="Linux x86_64" src="https://img.shields.io/badge/platform-Linux%20x86__64-informational">
  <img alt="Stable v1.0" src="https://img.shields.io/badge/status-Stable%20v1.0-brightgreen">
</p>

ExecSurface learns an accepted **runtime execution surface**, runs the same command later, and reports execution behavior that appeared, disappeared, or changed.

It is intended for CI pipelines, dependencies, developer tools and AI-assisted workflows where source review alone does not show every runtime effect.

> **Current stable release:** **v1.0.0** is the supported stable release for the documented Linux x86_64 + native `ptrace` product boundary.
>
> **Self-service:** no signup, API key, meeting, or AETHER X approval is required.
>
> **Important stable-v1 boundary:** an ExecSurface PASS is a drift-verdict PASS, not proof that the wrapped target command itself exited successfully. See [What a result means](#what-a-result-means) and [Current Status](docs/STATUS.md).

## Why developers use it

A dependency update, build script, test command or AI-assisted tool can change runtime behavior without making that behavior obvious in the code diff you are reviewing.

ExecSurface gives you a deliberately narrow workflow:

```text
learn accepted runtime behavior
            ↓
run the command again
            ↓
compare observed execution surfaces
            ↓
PASS / REVIEW / BLOCK / ERROR
```

Typical questions it helps answer:

- Did this command start launching a new executable?
- Did a dependency begin touching new paths?
- Did a workflow start connecting to a new destination?
- Did runtime behavior disappear or change after an update?
- Is the observation incomplete enough that a clean PASS would be unjustified?

If that problem is relevant to your work, try the **[Five-Minute Start](docs/QUICKSTART_5_MIN.md)**, browse the **[good first issues](https://github.com/AETHERXGLOBAL/execsurface/issues?q=is%3Aissue+is%3Aopen+%22Good+first+issue%22)**, or join the **[Discussions](https://github.com/AETHERXGLOBAL/execsurface/discussions)**.

If you find the project useful, a GitHub **Star** helps other developers discover it. External criticism, failed reproductions and counterexamples are equally useful to the project.

## Start here

Choose the path that matches your environment.

### A. Linux x86_64 — no Rust required (recommended first run)

Download the published release, verify its checksum, and install it in your user path:

```bash
VERSION=v1.0.0
TARGET=x86_64-unknown-linux-gnu
ASSET="execsurface-${VERSION}-${TARGET}.tar.gz"

curl -fLO "https://github.com/AETHERXGLOBAL/execsurface/releases/download/${VERSION}/${ASSET}"
curl -fLO "https://github.com/AETHERXGLOBAL/execsurface/releases/download/${VERSION}/${ASSET}.sha256"
sha256sum -c "${ASSET}.sha256"
tar -xzf "${ASSET}"

mkdir -p "$HOME/.local/bin"
install -m 0755 "execsurface-${VERSION}-${TARGET}/execsurface" "$HOME/.local/bin/execsurface"
export PATH="$HOME/.local/bin:$PATH"

execsurface --version
execsurface doctor
```

Then run the controlled **PASS → REVIEW** walkthrough in **[Five-Minute Start](docs/QUICKSTART_5_MIN.md)**.

### B. Rust already installed

```bash
cargo install execsurface --version "=1.0.0" --locked
execsurface --version
execsurface doctor
```

The current stable release is `v1.0.0`. Exact-version installation remains recommended for reproducible evaluation. See [crates.io Publishing](docs/CRATES_IO_PUBLISHING.md).

### C. Add it to a GitHub Actions project

First generate conservative starter files from your project directory:

```bash
execsurface init --command "cargo test --locked" --github-actions
```

`init` creates a starter policy and workflow. It **does not run your target command** and does not create a baseline automatically.

The generated workflow uses the stable v1 Action channel:

```text
AETHERXGLOBAL/execsurface@v1
```

For a copy-ready, least-privilege Rust consumer with independent target-success gating and external baseline/policy custody pins, use **[the stable-v1 GitHub Action example](examples/github-action-consumer-v1.yml)**. For non-Rust projects, adapt the target command and learn the baseline under the same wrapper.

Do not use `@main` or historical `@v0.1` as the default for new consumers. See the **[GitHub Action guide](docs/GITHUB_ACTION.md)**.

If the wrapped command's own success matters—for example `cargo test`, `pytest` or a build—keep that command as its own CI gate as well. In v1.0, target exit/signal remains report metadata and does not by itself change the ExecSurface drift verdict.

## First real project

Replace the example command with the command you actually want to monitor.

```bash
execsurface doctor
execsurface init --command "cargo test --locked" --github-actions
execsurface learn -- /bin/bash -lc 'cargo test --locked'
execsurface check --policy execsurface-policy.json -- /bin/bash -lc 'cargo test --locked'
```

Review `execsurface-policy.json`, `.github/workflows/execsurface.yml`, and `execsurface.lock.json` before committing them.

If `doctor` fails, follow the action it prints and see **[Troubleshooting](docs/TROUBLESHOOTING.md)**. `doctor` never elevates privileges, changes ptrace settings, or weakens host security settings.

## What a result means

| Result | Exit code | Meaning |
|---|---:|---|
| PASS | 0 | comparison/evaluation completed with no review/block execution-surface finding |
| ERROR | 2 | evidence/comparison/policy could not be established |
| REVIEW | 10 | one or more findings require review |
| BLOCK | 20 | one or more findings matched blocking policy |

**Stable v1 target-outcome boundary:** these exit codes are ExecSurface verdict codes. The wrapped target command's native exit code or terminating signal is retained in the structured report but is **not verdict-bearing in v1.0.0**. Therefore `ExecSurface: PASS` does not mean the wrapped target command succeeded. A nonzero or signalled target can still receive PASS when there is no policy-relevant execution-surface finding. Keep the target command's own success/failure gate when correctness of that command matters. This contract was explicitly frozen before v1 release.

ExecSurface does **not** infer that drift is malicious. It reports observed drift and evaluates the explicit policy you selected.

## What is observed

The current Linux x86_64 native `ptrace` reference backend can produce evidence for descendant process spawn/exec, pathname access attempts, successful-open file descriptor identity, covered fd-attributed read/write effects, rename/delete operations in the covered syscall set, network connect destinations, trace-time relative/openat/openat2 path semantics, causal executable chains, and explicit observer incompleteness.

Incomplete evidence cannot silently become PASS.

The portable ptrace guard may conservatively mark some clone/thread concurrency incomplete even when exact fd-table sharing is not proven. Raw observation v2 does not retain enough `CLONE_FILES` detail to certify exact sharing, so this guard intentionally trades possible false incompleteness for preventing the known false-completeness class. This is not an exact shared-FD attribution repair.

## Security boundary

ExecSurface detects **observed execution-surface drift under its recorded observer and policy**.

It is **not** antivirus, EDR, malware detection, a sandbox, or a proof that a program is safe.

The governing boundaries are:

- **NO EXECUTION-SURFACE DRIFT ≠ PROGRAM IS SAFE**
- **EXECSURFACE PASS ≠ TARGET COMMAND SUCCEEDED**
- **OBSERVED BEHAVIOR ≠ ALL POSSIBLE BEHAVIOR**
- **NO OBSERVED NETWORK ≠ NETWORK ACCESS IS IMPOSSIBLE**
- **TRACE COMPLETENESS DEPENDS ON THE OBSERVATION BACKEND**

The default evidence boundary excludes file contents, environment values, stdin, network payloads and full child argv values.

The public correctness-reference backend is native `ptrace`. eBPF/BPF-LSM work remains research-only/non-default and is not the public PASS/learn/check backend.

See **[Security Policy](SECURITY.md)**, **[Current Status](docs/STATUS.md)** and **[Troubleshooting](docs/TROUBLESHOOTING.md)**.

## Baseline is not policy

The baseline answers what canonical execution surface was accepted. The policy answers what drift should be allowed, reviewed or blocked. A new baseline is not automatically an approval decision.

## Qualification and independent evaluation

ExecSurface v1.0.0 completed the repository's strengthened internal stable-release qualification for the documented Linux x86_64 + native `ptrace` boundary. The release chain proved exact source/tag identity, checksum and provenance, zero-contact public binary consumption, immutable-tag installation, stable `@v1` PASS/REVIEW/BLOCK/ERROR behavior, and exact crates.io installation. Independent external validation is not claimed. See **[Current Status](docs/STATUS.md)** for exact run IDs and limitations.

Independent external validation remains open as additional evidence rather than a blocker to this bounded stable-v1.0.0 state. Use [Self-Service Start](docs/SELF_SERVICE_START.md), [Five-Minute Start](docs/QUICKSTART_5_MIN.md), [Independent Evaluation](docs/INDEPENDENT_EVALUATION.md), and [Technical Evaluation Pack](docs/TECHNICAL_EVALUATION.md).

External findings remain welcome through **[Issue #118 — Independent External Validation & Post-Release Review](https://github.com/AETHERXGLOBAL/execsurface/issues/118)**. Negative, partial, unsupported-environment, usability and performance-problem results are welcome. Internal qualification is not evidence of independent adoption or external validation.

## Independent external static review — historical Alpha

On **2026-09-27**, the maintainer of [awesome-ai-security-tools](https://github.com/scadastrangelove/awesome-ai-security-tools) independently inspected ExecSurface's **then-public Alpha** code/documentation and added it to the project's [WATCHLIST.md](https://github.com/scadastrangelove/awesome-ai-security-tools/blob/main/WATCHLIST.md) ([addition commit](https://github.com/scadastrangelove/awesome-ai-security-tools/commit/e0ec97f6f0b696d6a5ab0cb2158b8b4c1458c831)). [Original reviewer statement](https://github.com/scadastrangelove/awesome-ai-security-tools/issues/133#issuecomment-5857686313).

**Scope of that review:** source/documentation inspection only — **the reviewer did not execute ExecSurface**. The reviewer independently identified meaningful caveats: the observed command executes before a BLOCK decision can prevent subsequent CI steps, evidence can contain sensitive paths or network destinations, and REVIEW may require explicit fail-on-review configuration. This watchlist inclusion is **not** an endorsement, security audit, external runtime validation, integration, customer adoption or a review of the later stable v1.0.0 release.

Current v1 product behavior and validation must be assessed against the [v1.0.0 release](https://github.com/AETHERXGLOBAL/execsurface/releases/tag/v1.0.0), the [current status](docs/STATUS.md) and fresh independent trials. The historic review remains useful adverse/neutral evidence; it does not certify the current release.

## Selected external technical engagement

ExecSurface is developed under an evidence-first rule: external technical discussion is useful signal, but it is not automatically product validation or adoption.

Selected public records:

- **NVIDIA OpenShell — execution-generation lifecycle safety:** AETHER X contributed execution-generation, idempotency and fail-closed conditional-action invariants to [OpenShell #4009](https://github.com/NVIDIA/OpenShell/issues/4009). The issue author subsequently published a live SDK reproduction of the stale-target class across stop/start and delete/recreate. [Impact record #161](https://github.com/AETHERXGLOBAL/execsurface/issues/161).
- **OpenAI Codex — thread identity / control-surface addressability:** AETHER X contributed identity/placement and routing-contract analysis to [Codex #49729](https://github.com/openai/codex/issues/49729). Independent Windows and macOS reports supplied positive controls showing target conversations could remain valid through native/helper routes while the parent route still failed. [Impact record #162](https://github.com/AETHERXGLOBAL/execsurface/issues/162).
- **OpenAI Codex — daemon execution continuity:** AETHER X separated daemon reachability from restoration of the same in-flight execution in [Codex #50299](https://github.com/openai/codex/issues/50299); the external reporter confirmed the distinction matched the observed failure and an OpenAI maintainer later reported a fix path. [Impact record #160](https://github.com/AETHERXGLOBAL/execsurface/issues/160).

These records establish technical engagement and, where stated, external reproduction or acknowledgement of the underlying problem framing. They do **not** establish NVIDIA/OpenAI adoption, endorsement, integration or independent validation of ExecSurface.

For the company-level evidence summary, see the **[AETHER X GLOBAL organization profile](https://github.com/AETHERXGLOBAL#selected-external-engineering-contributions)**.

## Distribution and verification

The current stable v1 distribution surfaces are:

- checksum-verified GitHub Release binary for Linux x86_64;
- exact stable install `cargo install execsurface --version "=1.0.0" --locked` for Rust users;
- GitHub Action `AETHERXGLOBAL/execsurface@v1` after stable-channel promotion.

For maximum Action pinning, use `AETHERXGLOBAL/execsurface@v1.0.0`.

Optional GitHub build provenance verification:

```bash
gh attestation verify "$ASSET" -R AETHERXGLOBAL/execsurface
```

A valid attestation links the artifact to its build source/workflow. It does **not** prove the binary is safe.

## Documentation

Start with the **[Documentation Index](docs/README.md)**. It separates current product documentation from historical engineering evidence.

Key documents:

- [Current Status](docs/STATUS.md)
- [Five-Minute Start](docs/QUICKSTART_5_MIN.md)
- [GitHub Action](docs/GITHUB_ACTION.md)
- [Current v1 vs historical examples](examples/README.md)
- [Troubleshooting](docs/TROUBLESHOOTING.md)
- [Independent Evaluation](docs/INDEPENDENT_EVALUATION.md)
- [Technical Evaluation Pack](docs/TECHNICAL_EVALUATION.md)
- [v1.0.0 stable release record](docs/releases/v1.0.0.md)
- [Alpha.6 historical release record](docs/releases/v0.1.0-alpha.6.md)
- [Alpha.5 historical release record](docs/releases/v0.1.0-alpha.5.md)
- [Roadmap](ROADMAP.md)
- [Contributing](CONTRIBUTING.md)
- [Governance](GOVERNANCE.md)
- [Support](SUPPORT.md)

## Developing ExecSurface

```bash
cargo fmt --all -- --check
cargo clippy --locked --workspace --all-targets -- -D warnings
cargo test --locked --workspace --all-targets
cargo run -p execsurface -- --version
cargo run -p execsurface -- doctor
```

Architecture-affecting changes remain evidence-gated. See [CONTRIBUTING.md](CONTRIBUTING.md) and [GOVERNANCE.md](GOVERNANCE.md).

## License

Apache-2.0. See [LICENSE](LICENSE) and [NOTICE](NOTICE).
