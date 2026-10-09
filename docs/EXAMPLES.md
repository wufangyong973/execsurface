# ExecSurface Command Examples

**Current supported release:** ExecSurface `v1.0.0` on Linux x86_64, including GitHub Action `AETHERXGLOBAL/execsurface@v1`. For a copy-ready CI example, see [Stable v1 Consumer](../examples/github-action-consumer-v1.yml) and [example selection](../examples/README.md). Historical Alpha.5 Python/pytest recipes are evidence replay examples, not current installation instructions.

These are **illustrative command recipes**, not claims that ExecSurface has separately certified every ecosystem.

ExecSurface observes a command on supported Linux x86_64. The project command itself remains your responsibility.

The GitHub Action wraps its command input in `/bin/bash -lc`, so local learn/check examples below use the same wrapper.

## Deterministic hello-drift smoke test

Build the CLI, then run the repository-owned example from the project root:

```bash
cargo build --locked -p execsurface
examples/hello-drift.sh target/debug/execsurface
```

The script uses a fresh temporary working directory and asserts that the unchanged command reports `PASS` with exit status 0. It then adds one `/bin/echo` process and asserts that ExecSurface reports `REVIEW` with exit status 10. The example requires the same Linux x86_64 ptrace support as the public CLI. For the full install and workflow walkthrough, see the [Five-Minute Start](QUICKSTART_5_MIN.md). This example demonstrates a behavior path; it is not independent security validation.

## Rust

```bash
execsurface init --command "cargo test --locked" --github-actions

execsurface learn --   /bin/bash -lc 'cargo test --locked'

execsurface check   --policy execsurface-policy.json   -- /bin/bash -lc 'cargo test --locked'
```

The ExecSurface repository's own Rust workflow is continuously tested.

## Python

Illustrative project command:

```bash
execsurface init --command "python -m pytest" --github-actions

execsurface learn --   /bin/bash -lc 'python -m pytest'

execsurface check   --policy execsurface-policy.json   -- /bin/bash -lc 'python -m pytest'
```

This does not imply Python-specific observer semantics. ExecSurface observes the resulting Linux process/file/network effects.

## Node

Illustrative project command:

```bash
execsurface init --command "npm test" --github-actions

execsurface learn --   /bin/bash -lc 'npm test'

execsurface check   --policy execsurface-policy.json   -- /bin/bash -lc 'npm test'
```

This does not imply Node-specific observer semantics.

## CI advice

Choose a command that is stable enough to baseline and narrow enough that drift is reviewable.

If a test command intentionally includes highly nondeterministic network/process behavior, split the workflow or choose a more specific command instead of normalizing meaningful differences away.
