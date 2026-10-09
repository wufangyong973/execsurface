# Python/pytest: unchanged PASS and deliberate-write REVIEW

Historical example, archived at ExecSurface **v0.1.0-alpha.5**; it has not been
re-run against v1.0.0. This recipe learns and checks the **same real pytest
command** against a tiny public fixture using that pinned Alpha.5 release. The current public support
scope is Linux x86_64 with native `ptrace`; `doctor` must succeed on the host.
This is a reproducible integration example, not independent external validation.
Independent Alpha.5 findings belong in [issue #118](https://github.com/AETHERXGLOBAL/execsurface/issues/118).

From the repository root, first obtain the checksum-verified Alpha.5 binary using
the installation notes of the [immutable Alpha.5 release](https://github.com/AETHERXGLOBAL/execsurface/releases/tag/v0.1.0-alpha.5). Keep its reviewed
path in `EXEC_SURFACE_BIN`; this recipe records its digest and checks its version.
Then create a Python 3.12 or 3.13 environment and install the hash-pinned test
selection. Installation may download packages; the observed test uses no network
or external services.

```sh
python3.13 -m venv /tmp/execsurface-pytest-env
/tmp/execsurface-pytest-env/bin/python -m pip install \
  --require-hashes --only-binary=:all: \
  -r examples/python-pytest/requirements.lock

EXEC_SURFACE_BIN=/absolute/path/to/checksum-verified/execsurface
/tmp/execsurface-pytest-env/bin/python examples/python-pytest/run.py \
  --execsurface "$EXEC_SURFACE_BIN" \
  --output /tmp/execsurface-pytest-first-run
```

Use a new output directory each time. The runner refuses to overwrite a retained
run, copies its two public fixture files, and retains the native command receipts,
stdout/stderr, baseline and verdict JSON. A failed expectation writes `failure.json`
and exits nonzero, retaining the failure. `--python` may explicitly select another
interpreter with the exact dependencies installed; otherwise the runner uses its
own interpreter.

The observed command is:

```sh
python -m pytest -q -s -p no:cacheprovider test_fixture.py
```

The runner also disables plugin autoload and bytecode writes. `-s` disables
pytest's random temporary-file output capture; the **runner** still retains both
streams. Default pytest output capture was tested and made unchanged runs report
REVIEW for varying scratch-file names/deleted inode paths. These explicit fixture
choices keep this small workload deterministic without changing ExecSurface
normalization, policy or acceptance thresholds. They are not a recipe for hiding
arbitrary application drift.

The runner performs the ordinary `learn --output ... --workspace ... --label ...`
and `check --baseline ... --workspace ... --json-output ...` flows:

| Step | Pytest result | ExecSurface result | Asserted exit |
| --- | --- | --- | --- |
| Learn `write_extra: false` | One passing test | Baseline written | 0 |
| Check unchanged fixture | One passing test | PASS; no drift | 0 |
| Set public fixture `write_extra: true`, check again | One passing test | REVIEW; added `$WORKSPACE/drift.txt` write | 10 |

The same assertion, command, Python interpreter and baseline remain selected.
Only the public fixture's boolean changes. The test then writes the harmless
`drift.txt` inside its fresh workspace. The runner verifies its native file-write
finding and verifies the baseline bytes did not change.

The **baseline** records the selected observed execution surface. The **policy**
interprets differences; this recipe uses the unchanged built-in REVIEW policy for
unmatched drift. It does not relearn after drift or weaken policy to get PASS.
ERROR, BLOCK, unexpected exit, lost report or an unavailable observer fails the
recipe rather than counting as either expected outcome.

The fixture contains no secrets. It adds no environment enumeration or
secret/file-content collection. ExecSurface's existing metadata observer may
record local executable and filesystem paths; review retained receipts before
sharing them. A PASS here establishes this selected observed fixture comparison;
it does not establish containment, malware safety, complete observation of every
possible effect or independent custody.
