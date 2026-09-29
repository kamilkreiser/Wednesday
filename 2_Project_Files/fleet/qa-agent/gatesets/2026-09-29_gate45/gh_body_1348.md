`Refs KS-1054`

## Why
gate44 finding **N-1346-1 (Major)**: `deploy.sh` **exits 0** over failed startup migrations. It prints
`ERROR … Post-deploy verification found 1 issue(s)` and then returns success, so the deploy reads as
having worked.

Kam's ruling (a), verbatim:

> "The migration run returns its failed count. /health reports it, so the deploy scripts' existing
> /health checks (deploy-all.sh:281, deploy.sh:823) see it and **the deploy reads as failed**. The
> running service is not stopped."

`deploy-all.sh` already does that (`exit 1` on a failed smoke test). `deploy.sh` did not. PR #1346
landed the shared predicate and both call sites; its squash subject was composed to say "deploy-all
fails on them" precisely because this half was missing. This is that half.

## The change
`verify_deployment()` counted `ERRORS` and its **last command was `log_error`, an echo**, so the
function returned 0. It now `return 1`s when `ERRORS` is non-zero.

**One `return` is the whole fix, and no call site needed editing.** This file runs under
`set -euo pipefail` (`deploy.sh:28`) and `verify_deployment` is called **unchecked** at both sites — as
`deploy_services`' last command, and directly in the `verify)` branch — so a non-zero return aborts the
script with that status at either. Adding `|| exit 1` at the call sites would be a second, redundant
path to the same outcome, and a second path is a second thing to keep true.

## Test Evidence
**Touched:** `Blockchain/Dev/deployment/azure/deploy.sh` (+11, of which 1 is the `return` and 9 are the
comment recording why), and the existing shell suite (+53). 2 files, +64/−0.

**Ran** (base `8ba2da02d980`, head `1bb58b4ebb97`):
- **Whole suite 14 passed / 0 failed** (the 11 existing cells plus E0, E1, E2).
- 🔴 **RED-FIRST, with `deploy.sh` reverted to `8ba2da02d980` and the test half byte-unchanged:
  13 passed / 1 failed, and the one failure is E1 ALONE.** E0 and E2 stay green, so the red is neither
  a fixture failure nor an unconditional one. Restored by byte copy, sha256-equal, tree clean, suite
  back to 14/0.
- `bash -n` clean on both changed files.

**How E1 is driven, and why it is not a grep.** A grep for `return 1` passes on a **commented-out**
line, and a line-number pin drifts — this file's line numbers have moved repeatedly. So the cell
**extracts the real summary block from `deploy.sh` by its own marker** (`# ── Summary ─`, asserted to
occur exactly once by E0), strips the closing brace, stubs `log_success`/`log_error`, injects `ERRORS`,
and **executes the product's own bytes**, capturing rc with no pipeline in the measured statement.
- **E0** asserts the marker is unique, so the extraction is unambiguous.
- **E1** drives it with `ERRORS=2` and requires a non-zero rc.
- **E2** drives the same block with `ERRORS=0` and requires rc 0 — the arm that stops E1 from passing
  for the wrong reason, because a block that failed unconditionally would fail a **clean** deploy,
  which is worse than the defect.
An empty extraction is reported as a **fixture failure by name**, not as a product result.

**NOT run / NOT covered:**
1. **`deploy.sh` was not run against any real environment** — no Azure, demo or kintsugi deploy, and no
   migration run against a real database. What is proved is that the verification summary's exit status
   now reflects its own error count.
2. **The end-to-end propagation is argued from `set -e` and read call sites, not executed.** Driving
   `deploy.sh verify` whole needs `az` and `curl` stubs and a resolvable API FQDN; gate44 did that and
   measured the rc-0 defect, and this PR does not repeat it.
3. **The other gate44 Minors on this path are NOT fixed here** and stay open: N-1346-2 (`ran:false`
   still prints a pass line, although the gateway's own module says it is not a clean run), N-1346-3
   (an absent, empty or non-JSON body counts as a passing check in the smoke summary and in deploy.sh's
   "all checks OK"), N-1346-4 (`python3` missing from PATH reads a failed body as "not JSON — SKIPPED",
   failing open). Each needs a decision about the pass LINE rather than the exit status, and pass-and-warn
   for an absent field is deliberate — failing closed there would block a rollback to an older image.
4. Push preflight: **12/15 legs ran, 3 SKIPPED — legs 3, 4 and 8, "local stack not up". Nothing
   failed.** That is the hook's wording and it is **not a pass**; stated as a ratio.

**Migrations + config:** none. No schema change, no config default, no compose or bicep line.

**RUNTIME change in the deploy path → a §5f live sweep is owed**, and KS-1054 stays open.
