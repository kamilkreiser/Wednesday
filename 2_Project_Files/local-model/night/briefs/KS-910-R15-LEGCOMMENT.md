# KS-910 R15-LEGCOMMENT - re-brief at develop 9f0265eb0 of READY_KS-910_ornith35b-q4_BASHPATCH-REANCHORED-REBRIEF-PASS-7of7_2026-09-16.diff.md (written 20:36 on 2026-09-21 by Wednesday's census15 drafter; the body below is the old brief night/briefs/KS-910.md VERBATIM, whose three '-' lines and context are byte-identical at the tip - measured in the Premises block added at the end)


## What is wrong (one paragraph)
`pre_push_hook_base.test.sh:49` says **"Leg 12 of the preflight now reaches this suite on every gated push"** and credits leg 12 with the red a commit-signing developer would get. Leg 12 runs `run-shell-suites.sh --check-unreached` (`preflight.sh:521`), which only proves a suite is REACHABLE and exits before the run block — it executes no cell. The leg that RUNS every shell suite on a gated push is **leg 14** (`preflight.sh:544` `step "14/15  Every shell test suite must actually RUN"`, `:631` a bare `bash scripts/run-shell-suites.sh`), added by #806 on 2026-09-11, five days after this comment was written. Kam ruled: keep leg 12 as reachability, correct the comment. **This task: line 49 becomes a sentence that calls leg 12 reachability and names leg 14 as the leg that runs the suite, plus one new shell suite proving the false wording is gone, the corrected wording is present, and the comment's next line and the suite's syntax are untouched.** NOT in this task: `:50-51` (still true — leg 14 does run the suite), any code, `preflight.sh`, `run-shell-suites.sh`.

## The exact change — ONE WHOLE-RUN REPLACEMENT (three comment lines out, three in) in `Blockchain/Dev/scripts/__tests__/pre_push_hook_base.test.sh`
REBRIEF r2 (Wednesday, after r1 + its retry both marked line 50 as `-` instead of line 49 — an edit INSIDE a hard-wrapped comment run lands one line off; the run is therefore replaced WHOLE). Lines 49, 50 and 51 are one wrapped sentence; all three are removed and the re-wrapped sentence is added. Context above: line 48 is `#` alone. Context below: line 52 is `export GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null`.
```
-# Leg 12 of the preflight now reaches this suite on every gated push, so anyone
-# who signs their commits gets that red, pointing at the hook rather than at
-# their own config.
+# Leg 12 of the preflight only proves this suite is REACHABLE (it runs no
+# cell); leg 14 RUNS it on every gated push, so anyone who signs their commits
+# gets that red, pointing at the hook rather than at their own config.
```
All six lines are byte-exact — copy them. Your hunk has exactly these THREE `-` lines and THREE `+` lines, in this order, with line 48 above and line 52 below as context. Do not touch any other line.

## The test — CREATE THE NEW FILE `Blockchain/Dev/scripts/__tests__/pre_push_hook_base_leg_comment.test.sh`

File: `Blockchain/Dev/scripts/__tests__/pre_push_hook_base_leg_comment.test.sh`

bash 3.2. It lives under `Blockchain/Dev/scripts/__tests__/` beside the reference and READS the subject at `$REPO_ROOT/Blockchain/Dev/scripts/__tests__/pre_push_hook_base.test.sh` (it never runs it). Its shape is the reference `Blockchain/Dev/scripts/__tests__/docker_build_empty_table.test.sh` (full content in `files[...]`): `#!/usr/bin/env bash`, a header comment, `set -uo pipefail`, `TOTAL_CELLS=`, `HERE`/`REPO_ROOT` from `${BASH_SOURCE[0]}`, the set-but-empty refusal, the `[ -f ]` / `[ -r ]` FATAL lines, `pass=0; fail=0`, `ok()` / `bad()`, and the totals + INCOMPLETE guard + `exit`. No temp dir is needed — nothing is written.

**Reproduce the file below EXACTLY as written — every line, in order.** Do not invent a helper, do not rename a variable, do not reword a message. Every value a cell reads is assigned FIRST, above the first cell. The file contains no backslash anywhere; keep it that way. **Your diff for this file is a NEW-FILE diff: `--- /dev/null`, `+++ b/Blockchain/Dev/scripts/__tests__/pre_push_hook_base_leg_comment.test.sh`, ONE hunk header `@@ -0,0 +1,58 @@`, then EVERY line with a leading `+` (a blank line is a lone `+`) — no context lines, no `-` lines: you are not diffing the reference.**

```
#!/usr/bin/env bash
# =============================================================================
# TESTS for the leg-12 comment in pre_push_hook_base.test.sh (KS-910)
# =============================================================================
# Preflight leg 12 runs `run-shell-suites.sh --check-unreached`: it proves every
# suite is REACHABLE and executes no cell. Leg 14 is the leg that RUNS them. The
# KS-883 comment said leg 12 "reaches" the suite on every gated push, crediting
# the red to a leg that never runs it. Kam ruled (2026-09-16 09:53): keep leg 12
# as reachability, correct the comment. These cells pin the corrected wording.
#
# Usage: bash Blockchain/Dev/scripts/__tests__/pre_push_hook_base_leg_comment.test.sh
#        HOOK_BASE_SUITE=/path/to/other/copy bash ...   (red-proof)
# =============================================================================
set -uo pipefail
TOTAL_CELLS=4

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$HERE/../../../.." && pwd)"
if [ "${HOOK_BASE_SUITE+set}" = set ] && [ -z "$HOOK_BASE_SUITE" ]; then
  echo "FATAL: HOOK_BASE_SUITE is set but EMPTY - refusing to silently grade the shipped file." >&2
  exit 2
fi
SUBJ="${HOOK_BASE_SUITE-$REPO_ROOT/Blockchain/Dev/scripts/__tests__/pre_push_hook_base.test.sh}"
[ -f "$SUBJ" ] || { echo "FATAL: pre_push_hook_base.test.sh not found at $SUBJ" >&2; exit 2; }
[ -r "$SUBJ" ] || { echo "FATAL: HOOK_BASE_SUITE is not readable at $SUBJ" >&2; exit 2; }

pass=0; fail=0
ok()  { echo "  ok   $1"; pass=$((pass + 1)); }
bad() { echo "  FAIL $1"; echo "     $2"; fail=$((fail + 1)); }

stale_hits="$(grep -c -F 'Leg 12 of the preflight now reaches this suite' "$SUBJ" || true)"
fix_hits="$(grep -c -F 'leg 14 RUNS it on every gated push' "$SUBJ" || true)"
anchor_hits="$(grep -c -F 'carried no docs change at all. A green cell there meant nothing.' "$SUBJ" || true)"

# CELL 1 - red at the tip
if [ "$stale_hits" -eq 0 ]; then ok "the false claim that leg 12 reaches this suite on every gated push is gone"
else bad "the false leg-12 claim is still present" "hits=$stale_hits"; fi

# CELL 2 - red at the tip
if [ "$fix_hits" -eq 1 ]; then ok "the comment names leg 14 as the leg that runs this suite"
else bad "the corrected leg-14 wording is not present exactly once" "hits=$fix_hits"; fi

# CONTROL CELL 3 - green on both trees
if [ "$anchor_hits" -eq 1 ]; then ok "CONTROL the untouched line above the edited run is still there"
else bad "CONTROL the untouched line above the edited run moved or vanished" "hits=$anchor_hits"; fi

# CONTROL CELL 4 - green on both trees
if bash -n "$SUBJ"; then ok "CONTROL pre_push_hook_base.test.sh parses (bash -n)"
else bad "CONTROL pre_push_hook_base.test.sh does not parse" "bash -n failed"; fi

echo ""
echo "  $pass passed, $fail failed (of $TOTAL_CELLS cells)"
if [ "$((pass + fail))" -ne "$TOTAL_CELLS" ]; then
  echo "  INCOMPLETE - $((pass + fail)) of $TOTAL_CELLS cells ran"
  exit 1
fi
[ "$fail" -eq 0 ] || exit 1
exit 0
```

CELL 1 and CELL 2 are red at the untouched tip **by assertion** (`stale_hits` is 1, `fix_hits` is 0 — both assigned above the cells, nothing unbound, nothing crashes). CONTROL CELL 3 and CONTROL CELL 4 are green on both trees: line 47 is not edited, and a comment edit cannot break `bash -n`.

## Where (parsed into the checklist — every **must change** line must appear as a `-` line in your diff)
* `:49` — **must change**: `# Leg 12 of the preflight now reaches this suite on every gated push, so anyone`
* `:50` — **must change**: `# who signs their commits gets that red, pointing at the hook rather than at`
* `:51` — **must change**: `# their own config.`
* `:47` — (correct) `# carried no docs change at all. A green cell there meant nothing.` — stays

## Output
Exactly ONE ```diff block with TWO files: `--- a/Blockchain/Dev/scripts/__tests__/pre_push_hook_base.test.sh` / `+++ b/Blockchain/Dev/scripts/__tests__/pre_push_hook_base.test.sh` (one hunk), then `--- /dev/null` / `+++ b/Blockchain/Dev/scripts/__tests__/pre_push_hook_base_leg_comment.test.sh` (one `@@ -0,0 +1,58 @@` hunk, all `+`); paths repo-relative; blank context lines keep their leading space.

## Premises (measured)

Every factual claim the `+` line and the new suite assert or rely on, each read at `48e65c435` with `git show 48e65c435:<file>` on 2026-09-16 (20:1x) unless another instrument is named.

1. **"Leg 12 of the preflight only proves this suite is REACHABLE (it runs no cell)"** — `Blockchain/Dev/scripts/preflight/preflight.sh:506` `step "12/15  Every shell test suite must be REACHED by the runner (KS-731 / QA F-800-07)"` and `:521` `if ! run_delegated bash scripts/run-shell-suites.sh --check-unreached; then`. `Blockchain/Dev/scripts/run-shell-suites.sh:56` `--check-unreached) MODE="check" ;;`; the check block `:80-144` ends in `exit 1` or `exit 0` at `:143`, before the run loop at `:221`. The file's own `preflight.sh:554` agrees: "Leg 12 is `--check-unreached`, which exits before the run block."
2. **"leg 14 RUNS it on every gated push"** — `preflight.sh:544` `step "14/15  Every shell test suite must actually RUN (KS-731 / QA FR-800-03)"`, `:631` `if ! env "${env_clear[@]}" bash scripts/run-shell-suites.sh; then` (no argument → `MODE="run"`, `run-shell-suites.sh:53`/`:57`). The runner globs `Blockchain/Dev/scripts/__tests__/*.test.sh` (`:48-51`, `:62-69`) and runs every hit (`:221-230`, no exclusion list); `git ls-tree 48e65c435 Blockchain/Dev/scripts/__tests__/` lists `pre_push_hook_base.test.sh`. Every leg is reached: the only `exit` between `:150` and `:690` is the step-header/TOTAL_LEGS mismatch abort at `:173`, and all fifteen headers read `/15` with `TOTAL_LEGS=15` (`:130`). Stated residual: if leg 14's environment measurement comes back empty (`:620-626`) the suites are NOT run and the leg sets `fail=1`, so that push is blocked — every push that PASSES has run the suite. Leg 14 landed in `ec2d8c4ca` (#806, 2026-09-11; `git log -S`), after this comment (`3bfbd06eb`, 2026-09-06).
3. **"gated push"** — not new: the term is already in the `-` line and is the ticket's own; the hook runs the preflight for any push touching `Blockchain/Dev` and unconditionally when no base can be computed (`.githooks/pre-push:195`, `:203`).
4. **The rest of the sentence (formerly `:50-51`, re-wrapped in r2 with its words unchanged) stays true** ("anyone who signs their commits gets that red, pointing at the hook") — they describe why KS-883 isolates git config for the whole file (`:34-52`); with leg 14 executing the suite in the pushing developer's environment (only slot variables are cleared, `:627-631`), a regression of that isolation would red on the push. Words not edited; only the wrap moved (r2).
5. **Kam's ruling** — Linear KS-910 (read 20:07) carries the ticket's option 2 "correct the comment to 'reachable'"; the ruling text "keep leg 12 as reachability (CI runs the suites), correct the comment; close on the comment fix (polish)" is quoted from the commission, not re-read from a Linear comment (the ticket has no comments). "CI runs the suites" measured true: GitHub Actions run 34961722314 (`GET /actions/runs/34961722314/jobs`), step `All shell test suites (KS-666 / KS-731 — globbed, not listed)` executed → `failure`; `.github/workflows/pr-security-gates.yml:100` `run: bash scripts/run-shell-suites.sh`. The `+` line does NOT assert this.

Claims deliberately NOT made: anything about CI or GitHub Actions; any leg count other than the two leg numbers.

## Notes for the raise (not for the model)

- **Pre-measured before this brief was written** (scratch clone `git clone --shared` of the Secuura checkout, `checkout 48e65c435`, by script file): the new suite alone at the tip → `2 passed, 2 failed (of 4 cells)`, rc 1, both reds by assertion; with the one-line edit → `4 passed, 0 failed (of 4 cells)`, rc 0; the completeness arm proven to fire on the GREEN tree (CONTROL CELL 4 cut out → `INCOMPLETE - 3 of 4 cells ran`, rc 1). The product itself is a suite, and the checker's B6 will run it as a sibling (its own header names its basename): `pre_push_hook_base.test.sh` read `28 passed, 0 failed` before and after the edit. The file is 58 lines and carries no backslash (`grep -c` = 0).
- **Which comment is false, measured.** Every `Leg 12` / `leg 12` line at the tip, in both files: `preflight.sh:139` (a measured instance of leg 12's runner skipping in a non-git checkout — true), `:545` ("Leg 12 proves every suite is FINDABLE. Nothing proved any of them RUNS" — true), `:554` ("Leg 12 is `--check-unreached`, which exits before the run block" — true, `run-shell-suites.sh:80-144` exits in check mode), `:654` ("`--check-unreached` already enforces exactly this for SUITES (leg 12)" — true), and `pre_push_hook_base.test.sh:49` — **false**, the ticket's sentence, at the ticket's line. `run-shell-suites.sh` carries no leg-12 claim.
- **Why the corrected line names leg 14 and not CI.** The ticket (written when the preflight had 12 legs) says "no shell test suite runs on a gated push". That is stale at this tip: leg 14 (`ec2d8c4ca`, #806, 2026-09-11) runs the bare runner, which loops over every globbed suite (`run-shell-suites.sh:221-230`, roots `Blockchain/Dev/scripts/__tests__` + `systemTest/__tests__`, no exclusion list), so the red `:50-51` promises is real — only its attribution to leg 12 is false. Kam's "(CI runs the suites)" is also measured true (GitHub Actions run 34961722314, `PR Security Gates (KS-168)`, step `All shell test suites (KS-666 / KS-731 — globbed, not listed)` executed on 2026-09-15 and concluded `failure`), but a code comment that names a CI workflow's state would restate a fact the repo's docs currently record the opposite way (see below); the leg-14 fact is in the same tree and cannot drift out from under it silently without this suite's CELL 2 noticing a rename.
- **Adjacent stale comment, NOT touched — a Kam-class reconciliation.** `preflight.sh:548-550` says "GitHub Actions is retired for this repository (Kam, 2026-08-27; see CONTRIBUTING.md), so BOTH `run: bash scripts/run-shell-suites.sh` workflow steps are dormant." It sits under "Measured at e26cfce2b:" (a dated measurement, true on 2026-09-04 when Actions was 100% `startup_failure`), but as present tense it is now contradicted by the run above and by Kam's own 09:53 words. `CONTRIBUTING.md` asserts the retirement in five places (`:419-423`, `:449-450`, `:485-486`, `:494-504`, `:603-604`). Whether the 2026-08-27 retirement ruling is superseded is Kam's call; the KS-789 r2 brief raises the same question.
- **The ticket's option-1 gap is closed by leg 14, not by this ticket.** Worth saying in the close-out comment so nobody reopens KS-910 for option 1: the suites DO execute on every gated push today (leg 14), and in CI.

## Premises re-measured at develop 9f0265eb06ecf24d4de18149ce862ad2330a61ee (census15 drafter, 20:36 2026-09-21, scratchpad --shared clone)
- `pre_push_hook_base.test.sh` :49-:51 at the tip are the three '-' lines above byte for byte (`git show HEAD:<file> | sed -n 47,52p`; count of the :49 line = 1); the old READY's canonical patch applies STRICT at the tip (rc 0; -R rc 1); the new suite `pre_push_hook_base_leg_comment.test.sh` is ABSENT at the tip (`cat-file -e` rc 1).
- The task shape is bash_patch (build with `tasks/bash_patch/build_bash_input.sh KS-910 <out> <this brief> product=Blockchain/Dev/scripts/__tests__/pre_push_hook_base.test.sh ref=Blockchain/Dev/scripts/__tests__/pre_push_hook_base.test.sh test_file=Blockchain/Dev/scripts/__tests__/pre_push_hook_base_leg_comment.test.sh`); both files are test files - zero product bytes. Ticket KS-910 Backlog on the board login, no PR.
