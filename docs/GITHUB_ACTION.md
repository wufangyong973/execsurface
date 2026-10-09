# GitHub Action

## Public channel

The current stable Action channel is:

```text
AETHERXGLOBAL/execsurface@v1
```

`v1` is the moving stable major channel and is promoted only after the immutable version release has passed release-binary, Cargo/tag and Action consumer gates.

For maximum pinning after this release, use:

```text
AETHERXGLOBAL/execsurface@v1.0.0
```

Do not use `@main` or a historical Alpha channel as the normal consumer path.

## Copy-ready current-v1 consumer workflow

For a Rust repository, use the **[stable-v1 copy-ready workflow](../examples/github-action-consumer-v1.yml)**. It deliberately runs the target tests independently, then checks execution-surface drift with `@v1`, `require-custody: "true"`, fail-closed REVIEW and least-privilege permissions.

Before adopting it, review and commit the policy and baseline, then configure the two **trusted repository variables** `EXECSURFACE_BASELINE_DIGEST` and `EXECSURFACE_POLICY_SHA256`. The values must come from trusted maintainer approval, not untrusted PR content. The baseline is learned using exactly the same `/bin/bash -lc` wrapper on a comparable Linux x86_64 environment; environmental differences may legitimately trigger REVIEW. Do not automatically rewrite the baseline to silence the result.

The [v1 example qualification workflow](../.github/workflows/v1-consumer-example-smoke.yml) exercises the published `@v1` Action against PASS, REVIEW, BLOCK and ERROR with externally supplied custody pins. Its results are separate from the historic Alpha.5 Python/pytest example.


## Minimal workflow

```yaml
name: ExecSurface

on:
  pull_request:

permissions:
  contents: read

jobs:
  execsurface:
    runs-on: ubuntu-24.04
    steps:
      - uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7.0.1
      - name: Run the target command as its own correctness gate
        run: cargo test --locked
      - name: ExecSurface runtime drift
        id: execsurface
        uses: AETHERXGLOBAL/execsurface@v1
        with:
          command: "cargo test --locked"
          baseline: execsurface.lock.json
          policy: execsurface-policy.json
          fail-on-review: "false"
          upload-artifact: "true"
      - name: Show ExecSurface verdict
        run: echo "ExecSurface verdict: ${{ steps.execsurface.outputs.verdict }}"
```

The separate target-command step above is intentional. In stable v1.0.0, ExecSurface evaluates execution-surface drift; it does not turn the wrapped target's native exit code or signal into the ExecSurface verdict.

## Binary installation inside the Action

Remote Action consumption does not build ExecSurface from source. The Action reads its pinned immutable release tag, downloads the Linux x86_64 archive and checksum, verifies the checksum and version, then runs the accepted check/verdict path. Repository-local `uses: ./` development uses a locked source build.

## Wrapper consistency

The Action executes `/bin/bash -lc <command>`. Learn with the same wrapper:

```bash
execsurface learn -- /bin/bash -lc 'cargo test --locked'
```

`execsurface init --command "cargo test --locked" --github-actions` generates a starter workflow and matching learn/check commands.

## Policy behavior

Without an explicit policy, unmatched drift is REVIEW. PASS succeeds; REVIEW succeeds by default; `fail-on-review=true` makes REVIEW fail; BLOCK fails; ERROR fails.

### Stable v1 target-outcome boundary

The stable-v1 target command's native `exit_code` / terminating `signal` is retained in the structured report, but it is **report metadata rather than a verdict input**.

Consequences:

- `ExecSurface: PASS` means there was no policy-relevant execution-surface drift finding;
- it does **not** prove the wrapped target command succeeded;
- a nonzero or signalled target can still receive PASS if its observed surface has no review/block finding;
- run/gate a command such as `cargo test`, `pytest` or a build separately when its success is itself required;
- do not use the Action's `exit-code` output as the target command's native exit status.

This target-outcome behavior was first discovered in the Alpha line and was explicitly frozen into the v1 stable compatibility contract. Any future target-outcome enforcement requires a versioned compatibility decision.

## Outputs

- `verdict`
- `exit-code` — **ExecSurface verdict code** (`0`, `2`, `10`, `20`), not the target command's native exit code
- `report-json`
- `summary-markdown`
- `artifact-url`
- `artifact-digest`
- `sarif-status`

The target command's native exit/signal can be inspected in the structured report where available.

## SARIF

Current runtime effects do not prove which repository source file/line caused an effect. `sarif-status` remains `not-generated:no-source-provenance`.

## Permissions

Start with:

```yaml
permissions:
  contents: read
```

ExecSurface does not require PR-comment write permission.

## Security boundary

A PASS means the recorded comparison and policy did not identify review/block execution-surface drift. It does not prove the target command succeeded, and it does not prove the program is safe.

See [Current Status](STATUS.md) for the **stable v1.0.0 Linux x86_64/native-ptrace scope** and declared limitations. The old Alpha.5/Alpha.6 releases remain historical evidence, not current onboarding defaults.
