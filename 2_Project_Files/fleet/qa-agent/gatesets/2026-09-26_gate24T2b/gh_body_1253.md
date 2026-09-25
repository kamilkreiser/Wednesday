#1253 KS-1297 GUARDGAPS: anchor the abort counts, cover the worktree, pin bare call sites
head 6b88e4f03e82e3da0672efb1bb757ba5da912d6a

## BLUF

Three gaps the **#1218 tier-2c gate measured** in the new six-cell pre-push fixture guard and recorded as non-blocking. All three are coverage gaps in one suite and one test pass. **6 → 10 cells.**

None of these was a live failure: the suite passes 6/0 at the merged head, and the shipped behaviour is an improvement on what preceded it. Each item is a way the property the guard asserts can be false while it stays green.

## NB-1218-a — both abort-line counts are anchored

`grep -c 'FIXTURE BUILD FAILED'` → `grep -c '^FIXTURE BUILD FAILED'` at `:91` (`T1_NAMED`) and `:181` (`C6_NAMED`).

**One of those two is a NARROWING, not a tightening, and it should be read as such.** `T1_NAMED` asserts the abort line **was** produced, so unanchored was too loose and `^` tightens it — that is NB-1218-a exactly. `C6_NAMED` is the CONTROL and asserts the line was **not** produced; there the unanchored form was the *stricter* of the two, because a prefixed variant would have reddened it. Anchoring both is still right: the hook is the only producer of that line and always writes it at the start of a line, so the narrow form is the precise one and the two cells now agree on what "the abort line" means. But it is a direction change and it is stated rather than buried.

## NB-1218-b — `repo_state()` did not cover the working tree at all

It hashed `HEAD` + `for-each-ref` + `.git/config`, and nothing else. **A worktree-only write to the caller's repository was therefore outside the comparison entirely**, and cells 2 and 3 would have called such a repo "byte-identical". It now also hashes `status --porcelain` (an unstaged edit or an untracked addition) and `ls-files -s` (an index change).

The pre-widening form is kept under its own name **solely** so cell 8 can show what it missed — a widened hash that nobody showed could detect the thing is not a detector.

## NB-1218-c — the ticket names a shape that cannot defeat the guard

The ticket says *"`errexit` suspended at a call site is not pinned"*. **Measured on `/bin/bash` 3.2.57, that family cannot defeat the guard at all.** `build_fixture` aborts with an explicit `exit 2` at `:155-159`, and the subject carries `set -uo pipefail` with **no `-e`** — so no one's errexit is load-bearing here. What matters is whether the call site **swallows** that `exit 2`:

| call-site shape | rc | suite carried on? |
|---|---|---|
| `bf` — the shape all 12 real call sites use | 2 | **no** |
| `bf \|\| true` | 2 | **no** |
| `if bf; then :; fi` | 2 | **no** |
| `bf && :` | 2 | **no** |
| `( bf )` | **0** | **YES** |
| `x=$(bf)` | **0** | **YES** |
| `bf \| cat` | **0** | **YES** |

So the family that defeats it is a call site inside a **subshell**, where `exit 2` ends only the subshell and the suite runs all 28 cells against a fixture that was never built. A cell built on the `||`/`if` wording would have been a cell that cannot fail.

**The property pinned is therefore static: every `build_fixture` call site is a bare command.** Measured **12 of 12 bare, 0 wrapped**. Green today, red the moment one is wrapped. Cell 10 is its two-way control: the predicate must fire on a subshell call site and must **not** fire on the measurably-safe `|| true` shape, so the assertion's scope is honest and nobody later "fixes" a non-problem.

The ticket's own text is corrected by a facts-only comment on KS-1297; the defect class is *"a call site that runs `build_fixture` in a subshell"*, not *"errexit suspended"*.

## Test Evidence

**Touched:** `Blockchain/Dev/scripts/__tests__/pre_push_hook_base_fixture_guard.test.sh` (1 file, +115 / −3).

**Ran — the in-hook gate on this push** (a `Blockchain/Dev` change, so the preflight ran):
- `pre_push_hook_base.test.sh` **28 passed, 0 failed**
- **`pre_push_hook_base_fixture_guard.test.sh` 10 passed, 0 failed** — the declared figure, produced by the patched guard itself
- `run_shell_suites.test.sh` **49 passed, 0 failed** (this worktree carries the base runner; the 55 figure belongs to #1250)
- the preflight verdict and the shell-suite tally are quoted in the READY mail as measured, never as a pass

**Ran — GREEN and three red arms, one per conjunct, each isolated:**
- **GREEN: 10 passed, 0 failed.**
- **RED 1** — both anchors reverted in a copy: **9/1**, cell 7 alone.
- **RED 2** — `repo_state` un-widened in a copy: **9/1**, cell 8 alone.
- **RED 3** — one call site wrapped in a subshell (`c1`, chosen so the other cells' line-anchored seds still apply): **8/2**, cell 9 and its own control, nothing else.
- A coarser fourth arm wrapping the **`c0`** call site reads **5/5**; the breakdown is reported rather than the number, because it *additionally* reds cells 1, 2, 4 and 10 — those cells' seds are anchored on `^build_fixture "$WORK/c0"…`, which the wrap no longer matches, so **cells 4 and 10 correctly detect that their own tamper did not apply**. That is those guards working. The `c1` arm is the one quoted for isolation.

**A mistake inside this PR's own work, disclosed:** cell 7's first draft asserted that a prefixed line fails `grep -c '^…'` and satisfies `grep -c '…'`. Those are facts about **grep**, true on every machine forever — **a cell that cannot fail.** It now asserts a property of the suite read from its own bytes (both counts anchored, 2 of 2, 0 loose), and the grep demonstration is demoted to the control reported beside it.

**NOT run / NOT covered:**
- **The `INT`/`TERM` behaviour of nothing here is touched** — this PR adds no trap.
- **NB-1218-b is pinned for an unstaged edit and an index change, not for every conceivable worktree mutation.** A change that leaves `status --porcelain` and `ls-files -s` both identical would still slip through; I did not try to enumerate such a case.
- **NB-1218-c is pinned STATICALLY, not behaviourally.** The cell reads the subject's call sites; it does not run the suite under a wrapped call site and assert the abort survives — because at develop it would not survive, which is the gap itself. The seven-row table above is the behavioural measurement, taken by hand.
- **No measurement on Linux or on bash ≥ 4.** All shell measurements are macOS `/bin/bash` 3.2.57.
- The 12-of-12 call-site census is over `pre_push_hook_base.test.sh` only. **If another suite ever calls `build_fixture`, this cell does not see it.**

**Migrations + config:** none. Test-harness only — no migration, no `package.json`, no lockfile, no workflow, no runtime code.

## Scope

`Refs KS-1297` — this PR's own key. It closes neither KS-1297 nor its parents, which are written `ks897` and `ks896` un-hyphenated so no attachment lands on them.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

