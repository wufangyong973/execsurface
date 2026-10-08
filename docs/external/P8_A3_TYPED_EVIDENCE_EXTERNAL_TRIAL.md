# ExecSurface Experimental Typed-Evidence External Trial

Status: **PRE-RELEASE EXTERNAL TRIAL PACKET — not a public release**  
Tracking: #157  
External evidence authority: #114  
Real-workload authority: #140

## Frozen product target

This trial does **not** test the published Alpha.5 binary.

It tests the experimental typed-evidence source exactly at:

`cea214244d7efe05fea2108a5f5d8ed6287d9a3f`

The feature remains unreleased and experimental.

A trial result does not automatically become P8-A1, P8-A4 or P9.5 evidence. Qualification happens later under #114 / #140.

## Before you start

For the cleanest independence record:

1. choose the workload yourself;
2. do not ask AETHER X to operate or troubleshoot the first attempt;
3. preserve the first result even if it fails;
4. use a new output directory for every retry;
5. do not weaken evidence checks to obtain a successful result.

A failed build, unsupported environment, ERROR, incomplete result, verifier rejection or no-fit result is useful evidence.

## Security notice — historical trial packet revisions

The original packet revision referenced in Issue #157 has a confirmed **public CI log privacy gap**: child-process stdout/stderr from the experimental `observe` stage may escape into shared runner logs before evaluator review. This is distinct from the reported technical trial outcome; the historical result and its initial qualification remain unchanged.

**Do not run that original revision with sensitive workloads in public CI.** Upgrade to a separately qualified harness revision with quiet build/doctor/observe stages before using a shared CI runner. Run any older pinned packet only in a private environment with separately reviewed log handling. Re-running is not a substitute for the original independent result, and should be declared a follow-up.

The repaired harness deliberately sends child stdout/stderr to a discard sink rather than retaining them in logs or artifacts; bounded diagnostics retain stage and exit status. For detailed compiler or observer diagnostics, reproduce privately in a controlled environment. The raw typed-evidence artifact can still contain paths and must be inspected prior to external sharing. See [privacy defect and independent reporter](https://github.com/AETHERXGLOBAL/execsurface/issues/164) for the original report, verification and test gate.

## Privacy boundary

The capture harness deliberately does **not** save:

- your command/argv;
- target stdout;
- target stderr;
- environment values;
- stdin;
- network payloads;
- file contents.

The typed evidence itself can contain observed **paths**. Inspect it before sharing.

You are not required to post the raw typed-evidence file publicly. You may submit the privacy-minimized summary, consumer report and hashes and keep raw evidence local unless more detail is safe and necessary.

Never post credentials, tokens, proprietary source, secrets, private file contents or sensitive paths.

## 1. Obtain the packet

Clone the public repository and check out the exact **packet revision recorded in the #157 closeout comment**.

Example:

```bash
git clone https://github.com/AETHERXGLOBAL/execsurface.git execsurface-trial-packet
cd execsurface-trial-packet
git checkout <PACKET_SHA_FROM_ISSUE_157>
git status --short
```

Tracked packet files must be clean.

## 2. Materialize the frozen product target

From the packet repository:

```bash
git worktree add ../execsurface-typed-target cea214244d7efe05fea2108a5f5d8ed6287d9a3f
git -C ../execsurface-typed-target rev-parse HEAD
git -C ../execsurface-typed-target status --short
```

Expected HEAD:

`cea214244d7efe05fea2108a5f5d8ed6287d9a3f`

Do not modify tracked files in that worktree.

## 3. Choose your workload

Choose a command that matters to **your** project or a public project you independently selected.

The workload directory must be outside:
- the trial-packet repository;
- the frozen ExecSurface source worktree.

Do not use an AETHER X-authored demo if you want the result considered for external real-workload evidence.

## 4. Run one initial trial

Use a fresh output path outside the packet, product-source and workload directories.

From anywhere:

```bash
python3 /path/to/execsurface-trial-packet/scripts/p8_a3_external_trial_capture.py \
  --expected-packet-sha <PACKET_SHA_FROM_ISSUE_157> \
  --target-source /path/to/execsurface-typed-target \
  --workdir /path/to/your-project \
  --output-dir /tmp/execsurface-typed-trial-initial \
  -- cargo test --locked
```

Replace `cargo test --locked` with the command **you** selected.

The harness:
- verifies the packet revision;
- verifies the exact frozen product SHA;
- refuses dirty tracked product source;
- builds with `cargo build --locked -p execsurface`;
- runs `execsurface doctor`;
- runs your command once through experimental `observe --evidence-output`;
- validates the evidence with the independent stdlib-only reference consumer;
- records only bounded metadata/hashes.

It does not decide whether you are independent. It deliberately writes:

`UNQUALIFIED_PENDING_EXTERNAL_EVIDENCE_REVIEW`

until AETHER X qualifies the submitted result.

## 5. Preserve the initial output directory

Do **not** reuse or overwrite it.

The expected files are:

- `trial-summary.json` — privacy-minimized result;
- `consumer-report.json` — bounded verifier summary if validation succeeded;
- `typed-evidence.json` — raw + typed experimental evidence; inspect before sharing.

If the trial fails before evidence validation, the summary is still preserved with a failure code where possible.

## 6. Review before sharing

Check:

```bash
cat /tmp/execsurface-typed-trial-initial/trial-summary.json
cat /tmp/execsurface-typed-trial-initial/consumer-report.json 2>/dev/null || true
```

Inspect `typed-evidence.json` locally for path sensitivity before sharing it.

## 7. Submit the initial result

Use the **Experimental Typed-Evidence Trial** issue template.

Record:
- your relationship to AETHER X / ExecSurface;
- assistance received **before** the first result;
- packet SHA;
- frozen product SHA;
- workload/repository identity if shareable;
- environment;
- build / doctor / observe / consumer outcome;
- collection health and target outcome;
- any suspected false completeness/effect claim;
- setup, privacy, usability or performance friction;
- hashes or safe evidence locator;
- whether the tool fits the workload.

Negative and no-fit results are explicitly valid.

## Assisted retry rule

If AETHER X later helps troubleshoot, do not replace the first result.

Create a new output directory and identify the follow-up as assisted.

The original initial result remains the primary evidence record.

## Claims boundary

This trial packet does not claim:
- external validation;
- adoption;
- production readiness;
- stable typed-evidence compatibility;
- P8/P9.5 closeout.

Those claims require separate qualification from actual external evidence.
