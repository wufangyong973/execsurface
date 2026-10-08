# Contributing to ExecSurface

ExecSurface prioritizes precision, reproducibility, explicit limitations, and evidence-preserving engineering.

**Current supported public release:** `v1.0.0` within the documented Linux x86_64/native-`ptrace` contract. Older Alpha.5 contribution tasks and examples remain useful historical evidence, but they must not be presented as the current stable consumer path without a new exact-v1 run, public artifact verification and fresh CI.

## New to ExecSurface?

Start with repository Issues labeled `good first issue` and `help wanted`.

Current newcomer-scoped entry points include:

- #120 — deterministic `hello-drift` PASS → REVIEW example;
- #121 — Python/pytest integration recipe with a deterministic fixture;
- #122 — Node.js/npm integration recipe with controlled runtime drift;
- #123 — minimal GitHub Action consumer example pinned to Alpha.5;
- #124 — audit stale current-version references without rewriting historical evidence.

These tasks are intentionally bounded so contributors can improve usability and integrations without silently changing runtime semantics, evidence authority, support claims or release guarantees.

Independent Alpha.5 findings remain preserved in [Issue #118](https://github.com/AETHERXGLOBAL/execsurface/issues/118). Current real-workload post-v1 evidence is tracked in [Issue #140](https://github.com/AETHERXGLOBAL/execsurface/issues/140). A contribution or self-test is valuable engineering work, but is not automatically independent external validation or product adoption.

## Before opening a change

Use an issue or ADR first for changes that affect:

- observation semantics or completeness;
- canonical effect identity or normalization;
- baseline or lockfile semantics;
- policy or verdict semantics;
- backend authority/capability claims;
- provenance, attestation, or executable binding;
- privacy or security boundaries;
- supported platforms or public installation paths.

Small documentation, test, typo, and non-semantic maintenance changes do not require an ADR unless they alter a claim or contract.

## Development checks

Before proposing a code change, run the relevant local checks:

```bash
cargo fmt --all -- --check
cargo clippy --locked --workspace --all-targets -- -D warnings
cargo test --locked --workspace --all-targets
```

For public CLI or observer changes, also exercise the relevant `doctor`, `learn`, `check`, GitHub Action, and adversarial fixtures.

## Evidence rules

Every contribution must preserve these rules:

- no feature claim without tests;
- no benchmark claim without reproduction details;
- no security conclusion from an exit code alone;
- no hidden failure or discarded negative evidence;
- no threshold weakening to obtain PASS;
- no silent schema/baseline reinterpretation;
- no backend authority promotion from backend identity alone;
- incomplete, ambiguous, unsupported, or lost evidence cannot silently become PASS.

Every normalization or equivalence change requires an adversarial counterexample or regression fixture that demonstrates the failure mode it is intended to prevent.

## Pull request expectations

A pull request should state:

1. the problem and intended contract change;
2. files/semantics affected;
3. tests added or rerun;
4. negative/adversarial cases considered;
5. compatibility or migration impact;
6. any claim that must remain explicitly bounded.

If a test fails, classify the failure before changing implementation or acceptance logic. Retain material failures in the repository or linked GitHub evidence when they affect a gate or public claim.

## Scope boundary

ExecSurface is a runtime behavioral-integrity and verification layer for observed execution-surface drift.

Changes that turn it into an EDR, antivirus, malware detector, sandbox, general observability platform, generic policy engine, or agent framework are out of scope unless governance explicitly changes the product boundary.

## Security findings

Do not publish vulnerability details through normal issues when disclosure could create security risk. Follow [SECURITY.md](SECURITY.md).

## Documentation and historical records

Current documentation is indexed in [docs/README.md](docs/README.md). Historical milestone, release, failure, and external-review records are preserved for provenance; do not rewrite them merely because a later release superseded their state.

## License

By contributing, you agree that your contribution is provided under the repository's Apache-2.0 license unless an explicit repository policy states otherwise.
