# ExecSurface Documentation

This directory separates **current public guidance** from **engineering evidence and historical records**. For the present product state, start with the documents in the first section rather than inferring current behavior from an older milestone record.

## Current public product

- [Current Status](STATUS.md) — authoritative public support, distribution and validation state.
- [Production Readiness](PRODUCTION_READINESS.md) — retained P9 qualification contract and evidence supporting the published bounded v1.0.0 release.
- [Compatibility & Stability Contract](COMPATIBILITY.md) — active stable-v1 compatibility boundary and its qualification evidence.
- [Five-Minute Start](QUICKSTART_5_MIN.md) — shortest controlled PASS → REVIEW walkthrough.
- [Self-Service Start](SELF_SERVICE_START.md) — installation and first-use path for independent users.
- [GitHub Action](GITHUB_ACTION.md) — current `@v1` CI integration and stable Action usage.
- [Copy-ready stable v1 consumer](../examples/github-action-consumer-v1.yml) — least-privilege example with explicit custody pins and independent test-success gating.
- [Current vs historical examples](../examples/README.md) — use v1 for new projects; preserve Alpha fixtures only for replay.
- [Troubleshooting](TROUBLESHOOTING.md) — environment, ptrace and evidence-health diagnostics.
- [Examples](EXAMPLES.md) — command-line usage examples.
- [Why provenance is not the same as runtime behavioral integrity](WHY_RUNTIME_BEHAVIORAL_INTEGRITY.md) — shareable technical explanation of the problem ExecSurface addresses.
- [Ecosystem Positioning](ECOSYSTEM_POSITIONING.md) — factual scope/interoperability map relative to adjacent runtime-security and provenance systems; not a winner ranking.

## Evaluation and external evidence

- [Independent Evaluation](INDEPENDENT_EVALUATION.md) — how an external evaluator can reproduce, challenge or falsify the public release.
- [Technical Evaluation](TECHNICAL_EVALUATION.md) — repeatable technical evaluation pack.
- [Team & Evidence Governance](TEAM_AND_EVIDENCE_GOVERNANCE.md) — evidence discipline, role separation and anti-drift rules.
- [`external/`](external/) — external engagement protocols, baselines and evidence ledgers.
- GitHub issue `#118` — stable-v1 independent external evaluation and post-release review hub.
- GitHub issue `#114` — P8 evidence qualification and tracking.
- GitHub issue `#129` — P9 production-readiness and v1.0 qualification program.
- GitHub issue `#134` — P9.3 compatibility and stability contract gate.

Negative, partial, unsupported, reproduction-failure and no-fit findings are retained as first-class evidence. A contact, referral, invitation, internal test or self-evaluation PASS is not independent validation by itself.

## Contributor entry points

New contributors can start from repository Issues labeled `good first issue` and `help wanted`. Current newcomer-scoped work includes deterministic examples, Python/pytest and Node.js/npm recipes, a minimal GitHub Action consumer example, and current-documentation auditing.

Contributions must preserve product boundaries, negative evidence, fail-closed behavior and the distinction between internal/community engineering work and independent external validation. See [`CONTRIBUTING.md`](../CONTRIBUTING.md).

## Architecture and engineering

- [`architecture/`](architecture/) — current and historical architecture records.
- [`development/`](development/) — bounded development/research protocols and engineering records.
- [`milestones/`](milestones/) — milestone evidence. These files are historical records unless a current-status document explicitly incorporates them.

## Releases and distribution

- [crates.io Publishing](CRATES_IO_PUBLISHING.md) — registry publication process and safeguards.
- [`release/`](release/) — current release-decision material.
- [`releases/`](releases/) — release-specific public notes and retained evidence.

## Historical archive

- [`archive/`](archive/) — superseded state documents and retained historical material.

Historical failures, negative evidence and closed gates are intentionally preserved. Moving a record into an archive changes its operational location, not its evidentiary meaning and never converts a failure into a pass.

## Source-of-truth order

When documents from different dates appear to conflict, use this order for current public facts:

1. immutable published release/tag metadata for release identity and artifacts;
2. `docs/STATUS.md` for current support, distribution and validation state;
3. root `README.md` for the current user-facing path;
4. the latest release-specific document under `docs/releases/`;
5. dated milestone/development/archive records for chronology and historical evidence only.

ExecSurface **v1.0.0** is the supported stable release for Linux x86_64 with native ptrace as the bounded public observer. Alpha.5/Alpha.6 are immutable historical releases, not recommended for new onboarding. ARM64 and independent external validation are not claimed without corresponding evidence.

Security-sensitive findings must follow [`SECURITY.md`](../SECURITY.md) rather than public evidence channels.
