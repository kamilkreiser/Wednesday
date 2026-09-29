## The ruling this implements

Kam, on `secuura-ks1054-f9282-migration-failure-visibility`, option (a), verbatim:

> **[a] Keep serving, flag it on /health** — The migration run returns its failed count. /health
> reports it, so the deploy scripts' existing /health checks (deploy-all.sh:281, deploy.sh:823) see it
> and the deploy reads as failed. The running service is not stopped.

## The defect, in one sentence

`check-startup-migrations.sh` already distinguished **three** states in its OUTPUT — a clean tick, a
named skip, a failure — and then collapsed the first two into **rc 0**. Neither caller could tell
"ran clean" from "never ran", so both printed a passing line for a check that did not run. The
information existed and was thrown away at the boundary. That is why gate44's N-1346-2, N-1346-3 and
N-1346-4 are one item and not three one-liners.

## The change: a third exit code

- **rc 0** — the check RAN and was clean.
- **rc 1** — the deploy step FAILS: migrations failed, `failed` malformed, **or python3 is absent**.
- **rc 2** — **PASS-WITH-SKIP**: `ran:false`, field ABSENT, body EMPTY, body non-JSON. The deploy
  still PASSES — that is the rollback rule — but the caller stops reporting a clean run.

`ran:false` is now read **before** `failed`, which is the whole of N-1346-2: a `{ran:false,
failed:0}` body used to print a clean "0 failed" tick, the most misleading of the four skip shapes
because it names the field and reports a number.

⚠ **rc 2 is not backwards-compatible with either call site, deliberately.** Both wrote
`if predicate` / `if ! predicate`, under which rc 2 is a truthy failure. Shipping the predicate alone
would flip ABSENT from pass to FAIL and break the rollback rule. **The predicate and both callers
change in one commit**; neither half is separately correct. That is not theoretical — see the Test
Evidence note about the moment the suite read 36/0 green while `deploy.sh` would have failed a
rollback.

## N-1346-4: python3 absent now FAILS CLOSED, and that changed during review

I proposed rc 2 (pass-with-skip, message naming the parser). **Wednesday ruled rc 1, fail closed**,
and her reasoning is the one that holds: a missing parser is a **host** defect, not an image
property, so the rollback argument that protects the ABSENT case does not reach it. `deploy-all.sh`
**already** fails a deploy without python3, at its login-token parse (`:299`), so failing closed makes
`deploy.sh` consistent with the script beside it rather than inventing a new failure mode. And Kam's
ruling is explicit that the deploy reads as FAILED. Recorded as a decision, not presented as obvious.

## Behaviour per script, per body shape (measured on the merged develop, not reasoned)

| body shape | deploy.sh before | deploy.sh after | deploy-all.sh before | deploy-all.sh after |
|---|---|---|---|---|
| `{ran:true,failed:0}` | pass, "all checks OK" | unchanged | `✓`, exit 0 | unchanged |
| `{ran:false,failed:0}` | **`✓ 0 failed`, "all checks OK"** | `⚠ SKIPPED`, **still exit 0**, "passed with 1 check(s) SKIPPED" | **`✓` PASS** | `⚠ SKIPPED`, SKIP++, **still exit 0** |
| ABSENT | **"all checks OK"** | `⚠ SKIPPED`, **still exit 0** | **`✓` PASS** | `⚠ SKIPPED`, SKIP++, **still exit 0** |
| EMPTY | exit 1 (via the health grep) | **exit 1, unchanged** | **`✓` PASS** | `⚠ SKIPPED`, SKIP++, exit 0 |
| non-JSON | exit 1 (same route) | **exit 1, unchanged** | **`✓` PASS** | `⚠ SKIPPED`, SKIP++, exit 0 |
| `failed:2` / malformed | exit 1 | unchanged | `✗` FAIL | unchanged |
| **python3 absent** | **exit 0, "all checks OK", body misreported as "not JSON"** | **exit 1, naming the parser** | exit 1 via the login parse | `✗` FAIL, naming the parser |

**Exit statuses are unchanged on all four skip shapes.** Only python3-absent moves, and only because
that was ruled. The EMPTY / non-JSON divergence between the two scripts is **kept** and is listed in
NOT COVERED: closing it either way would change what a real deploy does on a live path.

## Test Evidence

**Touched:** `deployment/azure/check-startup-migrations.sh` (+57/−…),
`deployment/azure/deploy.sh`, `deployment/azure/deploy-all.sh`, and the ks1054 shell suite. Four
files, +378/−30.

**Ran**, each count named with the SHA and the platform it was measured on:

- Baseline at develop `a72149a1a803`: **14 passed / 0 failed**. At head `8f4f0ef14963`: **36 passed /
  0 failed** on macOS (bash 3.2.57) **and on GNU** (`python:3.12-slim`, bash 5.2.37, coreutils 9.7,
  Python 3.12.14 — all three printed in the same run, per N-1348-1).
- **Red-first, in two stages.** The predicate cells first: 15 passed / **7 failed** against the
  unchanged product. Then the caller cells: 28 passed / **5 failed**, with R1 red — which is the one
  that mattered, because at that moment the predicate returned rc 2 and `deploy.sh` would have FAILED
  a deploy over an ABSENT field. **No P-cell could see that**: it is a property of the call sites.
- **Test half alone: 19 passed / 14 failed.** Product files restored to develop, my cells kept — so
  14 cells are driven by the product change, and restoring gave 36/0 again.
- **Eight tamper arms, each setting the product to the PASSING value, each required to red**, each
  anchor proved unique first and each file restored byte-equal afterwards: ABSENT `exit 2→0` reds P4;
  the `ran:false` branch disabled reds P8; the python3 guard disabled reds P9 and P9b; EMPTY
  `exit 2→0` reds P7; the call site counting rc 2 as an ERROR reds R1; the summary's third arm
  removed reds R5; deploy-all's SKIP turned back into a PASS reds R8; and the `return` replaced by an
  unstubbed helper reds E1.
- **Whole shell suite: 61 passed, 0 failed, 0 skipped (of 61)**, rc 0.
- **Recorded modes** by `git ls-tree` at the head: `100755` on all three scripts, with the test file
  at `100644` **in the same commit** as the control. `core.filemode` is false, so the on-disk bit is
  not evidence. `bash -n` clean on all four files.

**NOT run:** the scripts were run against **no real environment** — no deploy, no migration, no live
`/health`. The pre-push preflight ran **12 of 15 legs with 3 SKIPPED** (legs 3, 4 and 8 — no local
stack on port 6882) and nothing failed; the hook's own output says that is not a pass, so it is quoted
as a ratio. A GitHub squash merge runs no local hook.

**Migrations + config:** none. No migration, no `.env`, no compose, no bicep, no env template, no
baseline row.

## Two findings from gate46 folded in, as directed

- **N-1348-6** — E1 accepted **any** non-zero rc, so an edit that dropped the `return` and ended the
  branch on a helper the driver did not stub kept the suite green while the real script exited 0 over
  failed migrations. E1 now requires rc **exactly 1**, and every `log_*` helper is stubbed. **Driven
  both ways:** under the pre-hardening `!= "0"` test the same tamper leaves the suite **36/0 green**,
  and under the hardened test it reds. The hole was real and this closes it.
- **N-1348-7** — a comment claimed "The TAMPER_RETURN_ZERO arm below drives it"; `git grep` found that
  line and nothing else, so the file made a false statement about itself. Corrected here rather than
  in #1348, because a new head would have voided the gate that graded it.

## A correction to one of my own cells, because a tamper caught it

R8 began life as `grep -q smoke_skip`. The tamper that replaces the skip **call** with
`smoke_test … "0 failed" "0 failed"` — precisely the regression the cell exists to stop — left the
`smoke_skip()` **definition** in the file, so the grep still matched and the suite stayed green. A
presence-grep cannot see whether a path is wired. R8 now extracts and **executes** deploy-all.sh's own
call site against a stub predicate and asserts the counters, with rc 0 and rc 1 as controls.

## NOT COVERED

- **The EMPTY / non-JSON divergence between the two scripts is kept, for Kam** (gate45 N-1348-3):
  `deploy.sh` aborts on those two shapes via its health check, `deploy-all.sh` passes them. Closing
  it in either direction changes a live deploy outcome.
- **N-1346-9 is out of scope**: `deploy-all.sh --skip-build` deploys a tag no build produced, so it
  has no working rollback path. That is on Wednesday's backlog, not this PR.
- The scripts are not exercised against any real environment, so the rendering is proven by driving
  their own extracted bytes, not by a deploy.
- **RUNTIME change on the deploy path: a live sweep is owed** and KS-1054 stays In Progress.

Refs KS-1054
