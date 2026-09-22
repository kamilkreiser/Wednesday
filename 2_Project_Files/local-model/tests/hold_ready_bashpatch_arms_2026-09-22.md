# hold_ready.py bash_patch arms — Tue 22 Sep 2026 10:29:11 AEST

backup: /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/hold_ready.py.pre-0922-1022-bashpatch
backup check at 10:22 (before any edit): `cmp hold_ready.py hold_ready.py.pre-0922-1022-bashpatch` rc=0; the backup is 32701 B, mtime 22 Sep 04:43 (cp -p) — the pre-edit code exactly. (A line here first compared the backup to `.pre-0922-0443-a3predicate`, the code BEFORE the 04:43 edit, and printed rc=1 — expected and not a check of anything; replaced 10:30.)
diff stat:  1 file changed, 287 insertions(+), 4 deletions(-)

## Defect reproduction (OLD code — the backup — on the bash ERREXIT PASS 7/7 run)
hold_ready: REFUSE — checker.out has no 'mode: code_patch' line — the input says code_patch but the checker did not run it as one
rc=2

## Arm A — regression: test_only --dry-run on runs/2026-09-22_ks947-ornith35b-night2 (BEFORE captured on the old code at 10:22, AFTER on the final code)
cmd: hold_ready.py <ks947 night2> - F3F4b-R16 MFA-LIMITER-OPTION-PARITY-AND-SPEC-MAX --dry-run
clock-normalised diff rc=0 (6 / 6 lines); raw cmp rc=1 (the clock stamp only)
VERDICT: PASS (A test_only regression)
AFTER output:
DRY-RUN OK → READY_KS-947-F3F4b-R16_ornith35b-q4_BRIEFED-TESTONLY-MFA-LIMITER-OPTION-PARITY-AND-SPEC-MAX-PASS-8of8_2026-09-22.diff.md
  golden: golden not located — no byte-identity claim is made
  plus=66 minus=0 cells=10 tampers=3 nonascii=0
  header: > ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks947-ornith35b-night2/out.md.checker/patch.diff`** (from `ls` at 10:29 2026-09-22). Checker T3 (verbatim from checker.out): `PASS T3 diff applies at th
  prnote: **PR NOTES for the raise seat:** TEST-ONLY — zero product bytes; one file, apply `patch.diff` strictly at the tip (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` and state it)
rc=0

## Arm B — regression: code_patch --dry-run on runs/2026-09-22_ks1265-ornith35b-night with golden feed3/1265EARLYGUARD-R16
clock-normalised diff rc=0 (6 / 6 lines); raw cmp rc=1 (the clock stamp only)
VERDICT: PASS (B code_patch regression)
AFTER output (first 2 lines):
DRY-RUN OK → READY_KS-1265-EARLYGUARD-R16_ornith35b-q4_BRIEFED-CODEPATCH-ISSUERNAME-AT-GUARD-BEFORE-SAVE-PASS-7of7_2026-09-22.diff.md
  golden: CONTENT-compared against the drafter's golden `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_feed3-drafter-precheck/1265EARLYGUARD-R16/out.md.checker/patch.diff` (bytes DIFFER: `cmp` rc 1); change lines (`+`/`-`, ordered) I

## Arm C — test_only FAIL run (runs/2026-09-22_ks947-ornith35b-night, T4 FAIL): refusal shape unchanged
rc=2
hold_ready: REFUSE — checker.out RESULT is not PASS: RESULT: FAIL (1 failed) — stopped at T4 (the diff is not the brief's lines; no test is run); FAIL lines: ['FAIL T4 BRIEF LINES — MISSING \'+\' \'const blanked = call.replace(/\\\'[^\\\']*\\\'/g, "\\\'\\\'").split(LF).map((line) => line.split(\\\'/
VERDICT: PASS (C test_only FAIL refused rc 2)

## Arm D1 — bash FAIL run: scratch COPY of the ERREXIT run (done.md has no bash FAIL row today) with 'PASS B5' -> 'FAIL B5 …' and 'RESULT: PASS (7/7)' -> 'RESULT: FAIL (1 failed)'; the run dir itself is never modified
rc=2
hold_ready: REFUSE — checker.out RESULT is not PASS: RESULT: FAIL (1 failed); FAIL lines: ['FAIL B5 GREEN-AFTER: still red after the script hunk (rc=1, 2 FAIL line(s), load_error=0): Blockchain/Dev/scripts/__tests__/validate_lint_errexit.test.sh passes with the script hunk (rc=0, 0 FAIL lines, 3 pass line(s))']
VERDICT: PASS (D1 bash FAIL refused rc 2 naming the RESULT and FAIL lines)

## Arm D2 — artefact contradiction: copy with section_1.diff.opts = '--recount' while the B2 line says (strict)
rc=2
hold_ready: REFUSE — B2 line claims (strict) but a section carries an accommodation: [(1, '--recount', [])]
VERDICT: PASS (D2 strict-claim vs opts refused)
(first attempt at 10:27 PASSED rc 0 — sections.json carries ABSOLUTE paths into the ORIGINAL run dir, so the copy's opts were never read; fixed: section files are now resolved under the run's own out.md.checker/ by basename, with a stderr NOTE when sections.json points elsewhere)

## Arm D2b — converse: copy whose B2 line names an accommodation while no opts/as-written/pre-b3c artefact shows one
rc=2
hold_ready: REFUSE — B2 line names an accommodation but no section's opts/as-written/pre-b3c artefact shows one: PASS B2 every section applies at the tip — with an accommodation: section_1.diff: --recount;
VERDICT: PASS (D2b accommodation-claim vs artefacts refused)

## Arm D3 — task-type signals disagree: copy with a 'mode: code_patch' line prepended to checker.out while night_meta.json says tasks/bash_patch
rc=2
hold_ready: REFUSE — task-type signals disagree: night_meta.json's task path says bash_patch=True but checker.out's shape (a B0 line and no `mode:` line) says bash_patch=False
VERDICT: PASS (D3 signal disagreement refused)

## Arm D4 — red_first.out re-count disagrees with the B4 run line (copy with one planted 'FAIL:' line appended)
rc=2
hold_ready: REFUSE — red_first.out re-count FAIL=3 pass=1 != B4 run line fail_lines=2 pass_lines=1
VERDICT: PASS (D4 red re-count mismatch refused)

## Arm D5 — golden COPY with one '+' change line altered: must say DIFFERS with a count, never CONTEXT-ONLY
rc=0
  golden: DIFFERS from the drafter's golden `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/37c28f31-b065-4f99-b37a-8976d071f996/scratchpad/golden_d5/out.md.checker/patch.diff` (`cmp` rc 1): 2 change line(s) (`+`/`-`, ndiff) differ in validate-lint.sh (2; run 4 vs golden 4); APPLIED PRODUCT IDENTICAL: the two checkers' own `after.sh` (the script after its hunk) `cmp` rc 0 — read the diff before raising
VERDICT: PASS (D5 altered golden reported DIFFERS)

## Arm D6 — golden '-': no identity claim
rc=0
  golden: golden not located — no identity claim is made
VERDICT: PASS (D6 no golden -> no claim)

## Arm D7 — copy without night_meta.json (moved aside): checker.out's shape alone still detects bash_patch
rc=0
DRY-RUN OK → READY_KS-1139-1139ERREXIT-R16B_ornith35b-q4_BRIEFED-BASHPATCH-X-PASS-7of7_2026-09-22.diff.md
VERDICT: PASS (D7 shape-only detection)

## Arm E — the six PASS runs, --dry-run with their feed8 goldens (expected: ERREXIT + HOOKENV BYTE-IDENTICAL; BANNER/STACKLEGS/DEMOBASE/LATESTSLOT CONTEXT-ONLY)
Wednesday's pre-measurement said the bodies are identical with context-only differences. Measured here per pair (< golden, > run, from `diff`): BANNER — the run's hunk header carries a trailer (`@@ -709,7 +709,7 @@ echo -e ""` vs `@@ -709,7 +709,7 @@`) and lacks the golden's leading context line ` echo ""`; STACKLEGS — the run has one extra ' ' (blank context) line at the end of hunk 1; DEMOBASE — same, one extra ' ' line; LATESTSLOT — the run has one extra EMPTY line (no leading space, the trailing-blank dialect) at the end of hunk 1. In all four the ordered '+'/'-' lines are identical in every section and the two checkers' after.sh files cmp rc 0. (A first pre-measure counted '' as a change line via `l[:1] in '+-'` and reported LATESTSLOT 73 vs 72 — a false positive; the tool uses `in ('+','-')`.)
### ERREXIT — hold_ready.py <runs/2026-09-22_ks1139-ornith35b-night> <feed8/ERREXIT> 1139ERREXIT-R16B VALIDATE-LINT-ARITHMETIC-COUNTERS-UNDER-ERREXIT --seat 'Wednesday (the 07:2x seat)' --dry-run
rc=0
DRY-RUN OK → READY_KS-1139-1139ERREXIT-R16B_ornith35b-q4_BRIEFED-BASHPATCH-VALIDATE-LINT-ARITHMETIC-COUNTERS-UNDER-ERREXIT-PASS-7of7_2026-09-22.diff.md
  golden: the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1139-ornith35b-night/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_feed8-drafter-precheck/ERREXIT/out.md.checker/patch.diff` rc 0, Wednesday (the 07:2x seat)); APPLIED PRODUCT IDENTICAL: the two checkers' own `after.sh` (the script after its hunk) `cmp` rc 0
  touched=['Blockchain/Dev/scripts/__tests__/validate_lint_errexit.test.sh', 'systemTest/schemathesis/validate-lint.sh'] product_plus=2 product_minus=2 red=rc1/2FAIL green=rc0/3pass sibs=0 strict=True cat_ok=True rewritten=[] nonascii=0
VERDICT: PASS (E ERREXIT BYTE-IDENTICAL)
### HOOKENV — hold_ready.py <runs/2026-09-22_ks1034-ornith35b-night> <feed8/HOOKENV> 1034HOOKENV-R16B HOOK-REPO-ROOT-UNDER-GIT-DIR-LINKED-WORKTREE --seat 'Wednesday (the 07:2x seat)' --dry-run
rc=0
DRY-RUN OK → READY_KS-1034-1034HOOKENV-R16B_ornith35b-q4_BRIEFED-BASHPATCH-HOOK-REPO-ROOT-UNDER-GIT-DIR-LINKED-WORKTREE-PASS-7of7_2026-09-22.diff.md
  golden: the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1034-ornith35b-night/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_feed8-drafter-precheck/HOOKENV/out.md.checker/patch.diff` rc 0, Wednesday (the 07:2x seat)); APPLIED PRODUCT IDENTICAL: the two checkers' own `after.sh` (the script after its hunk) `cmp` rc 0
  touched=['Blockchain/Dev/scripts/__tests__/check_stack_safety_hook_env.test.sh', 'Blockchain/Dev/scripts/check-stack-safety.sh'] product_plus=2 product_minus=1 red=rc1/2FAIL green=rc0/5pass sibs=1 strict=True cat_ok=True rewritten=[] nonascii=0
VERDICT: PASS (E HOOKENV BYTE-IDENTICAL)
### BANNER — hold_ready.py <runs/2026-09-22_ks972-ornith35b-night> <feed8/BANNER> 972BANNER-R16B START-BANNER-RETIRED-ADMIN-DEFAULT-CREDENTIAL --seat 'Wednesday (the 07:2x seat)' --dry-run
rc=0
DRY-RUN OK → READY_KS-972-972BANNER-R16B_ornith35b-q4_BRIEFED-BASHPATCH-START-BANNER-RETIRED-ADMIN-DEFAULT-CREDENTIAL-PASS-7of7_2026-09-22.diff.md
  golden: CONTEXT-ONLY difference from the drafter's golden `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_feed8-drafter-precheck/BANNER/out.md.checker/patch.diff` (bytes DIFFER: `cmp` rc 1; run 4505 B vs golden 4503 B): change lines (`+`/`-`, ordered) IDENTICAL in every section (start-secuura.sh 2, start_secuura_banner.test.sh 78); context/empty lines run vs golden: start-secuura.sh 5/6 context; hunk headers differ (start-secuura.sh: run `@@ -709,7 +709,7 @@ echo -e ""` vs golden `@@ -709,7 +709,7 @@`); APPLIED PRODUCT IDENTICAL: the two checkers' own `after.sh` (the script after its hunk) `cmp` rc 0; the new test's content IS its `+` lines, so the created file is identical
  touched=['Blockchain/Dev/scripts/__tests__/start_secuura_banner.test.sh', 'Start_Up/start-secuura.sh'] product_plus=1 product_minus=1 red=rc1/2FAIL green=rc0/4pass sibs=4 strict=False cat_ok=True rewritten=[] nonascii=0
VERDICT: PASS (E BANNER CONTEXT-ONLY)
### STACKLEGS — hold_ready.py <runs/2026-09-22_ks1047-ornith35b-night> <feed8/STACKLEGS> 1047STACKLEGS-R16B PRE-PUSH-COMMENT-STACK-LEGS-3-4-8 --seat 'Wednesday (the 07:2x seat)' --dry-run
rc=0
DRY-RUN OK → READY_KS-1047-1047STACKLEGS-R16B_ornith35b-q4_BRIEFED-BASHPATCH-PRE-PUSH-COMMENT-STACK-LEGS-3-4-8-PASS-7of7_2026-09-22.diff.md
  golden: CONTEXT-ONLY difference from the drafter's golden `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_feed8-drafter-precheck/STACKLEGS/out.md.checker/patch.diff` (bytes DIFFER: `cmp` rc 1; run 4522 B vs golden 4520 B): change lines (`+`/`-`, ordered) IDENTICAL in every section (pre-push 2, pre_push_stack_legs_comment.test.sh 74); context/empty lines run vs golden: pre-push 6/5 context; hunk headers identical; APPLIED PRODUCT IDENTICAL: the two checkers' own `after.sh` (the script after its hunk) `cmp` rc 0; the new test's content IS its `+` lines, so the created file is identical
  touched=['.githooks/pre-push', 'Blockchain/Dev/scripts/__tests__/pre_push_stack_legs_comment.test.sh'] product_plus=1 product_minus=1 red=rc1/2FAIL green=rc0/4pass sibs=7 strict=False cat_ok=False rewritten=[1] nonascii=0
VERDICT: PASS (E STACKLEGS CONTEXT-ONLY)
### DEMOBASE — hold_ready.py <runs/2026-09-22_ks1033-ornith35b-night> <feed8/DEMOBASE> 1033DEMOBASE-R16B DEMO-MUTATION-GUARD-COMMIT-RANGE-BASE --seat 'Wednesday (the 07:2x seat)' --dry-run
rc=0
DRY-RUN OK → READY_KS-1033-1033DEMOBASE-R16B_ornith35b-q4_BRIEFED-BASHPATCH-DEMO-MUTATION-GUARD-COMMIT-RANGE-BASE-PASS-7of7_2026-09-22.diff.md
  golden: CONTEXT-ONLY difference from the drafter's golden `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_feed8-drafter-precheck/DEMOBASE/out.md.checker/patch.diff` (bytes DIFFER: `cmp` rc 1; run 6394 B vs golden 6392 B): change lines (`+`/`-`, ordered) IDENTICAL in every section (check-no-demo-mutation.sh 8, check_no_demo_mutation_base.test.sh 126); context/empty lines run vs golden: check-no-demo-mutation.sh 10/9 context; hunk headers identical; APPLIED PRODUCT IDENTICAL: the two checkers' own `after.sh` (the script after its hunk) `cmp` rc 0; the new test's content IS its `+` lines, so the created file is identical
  touched=['Blockchain/Dev/scripts/__tests__/check_no_demo_mutation_base.test.sh', 'Blockchain/Dev/scripts/check-no-demo-mutation.sh'] product_plus=6 product_minus=2 red=rc1/2FAIL green=rc0/5pass sibs=0 strict=False cat_ok=True rewritten=[] nonascii=0
VERDICT: PASS (E DEMOBASE CONTEXT-ONLY)
### LATESTSLOT — hold_ready.py <runs/2026-09-22_ks1093-ornith35b-night> <feed8/LATESTSLOT> 1093LATESTSLOT-R16B LATEST-SLOT-SYMLINK-CHECK-IGNORE-SHAPE --seat 'Wednesday (the 07:2x seat)' --dry-run
rc=0
DRY-RUN OK → READY_KS-1093-1093LATESTSLOT-R16B_ornith35b-q4_BRIEFED-BASHPATCH-LATEST-SLOT-SYMLINK-CHECK-IGNORE-SHAPE-PASS-7of7_2026-09-22.diff.md
  golden: CONTEXT-ONLY difference from the drafter's golden `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_feed8-drafter-precheck/LATESTSLOT/out.md.checker/patch.diff` (bytes DIFFER: `cmp` rc 1; run 6778 B vs golden 6777 B): change lines (`+`/`-`, ordered) IDENTICAL in every section (check-stack-safety.sh 4, check_stack_safety_latest_slot_symlink.test.sh 67); context/empty lines run vs golden: check-stack-safety.sh 13/13 context + 1/0 empty; hunk headers identical; APPLIED PRODUCT IDENTICAL: the two checkers' own `after.sh` (the script after its hunk) `cmp` rc 0; the new test's content IS its `+` lines, so the created file is identical
  touched=['Blockchain/Dev/scripts/__tests__/check_stack_safety_latest_slot_symlink.test.sh', 'Blockchain/Dev/scripts/check-stack-safety.sh'] product_plus=3 product_minus=1 red=rc1/3FAIL green=rc0/6pass sibs=1 strict=True cat_ok=False rewritten=[] nonascii=0
VERDICT: PASS (E LATESTSLOT CONTEXT-ONLY)

## Arm totals: PASS 17 · FAIL 0 — Tue 22 Sep 2026 10:29:12 AEST

## REAL HOLDS — Tue 22 Sep 2026 10:29:38 AEST
### ERREXIT
HELD → /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/READY_KS-1139-1139ERREXIT-R16B_ornith35b-q4_BRIEFED-BASHPATCH-VALIDATE-LINT-ARITHMETIC-COUNTERS-UNDER-ERREXIT-PASS-7of7_2026-09-22.diff.md
  golden: BYTE-IDENTICAL; touched=2 product_plus=2 product_minus=2 red=rc1/2FAIL green=rc0/3pass sibs=0 strict=True cat_ok=True rewritten=[]
rc=0
### HOOKENV
HELD → /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/READY_KS-1034-1034HOOKENV-R16B_ornith35b-q4_BRIEFED-BASHPATCH-HOOK-REPO-ROOT-UNDER-GIT-DIR-LINKED-WORKTREE-PASS-7of7_2026-09-22.diff.md
  golden: BYTE-IDENTICAL; touched=2 product_plus=2 product_minus=1 red=rc1/2FAIL green=rc0/5pass sibs=1 strict=True cat_ok=True rewritten=[]
rc=0
### BANNER
HELD → /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/READY_KS-972-972BANNER-R16B_ornith35b-q4_BRIEFED-BASHPATCH-START-BANNER-RETIRED-ADMIN-DEFAULT-CREDENTIAL-PASS-7of7_2026-09-22.diff.md
  golden: CONTEXT-ONLY; touched=2 product_plus=1 product_minus=1 red=rc1/2FAIL green=rc0/4pass sibs=4 strict=False cat_ok=True rewritten=[]
rc=0
### STACKLEGS
HELD → /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/READY_KS-1047-1047STACKLEGS-R16B_ornith35b-q4_BRIEFED-BASHPATCH-PRE-PUSH-COMMENT-STACK-LEGS-3-4-8-PASS-7of7_2026-09-22.diff.md
  golden: CONTEXT-ONLY; touched=2 product_plus=1 product_minus=1 red=rc1/2FAIL green=rc0/4pass sibs=7 strict=False cat_ok=False rewritten=[1]
rc=0
### DEMOBASE
HELD → /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/READY_KS-1033-1033DEMOBASE-R16B_ornith35b-q4_BRIEFED-BASHPATCH-DEMO-MUTATION-GUARD-COMMIT-RANGE-BASE-PASS-7of7_2026-09-22.diff.md
  golden: CONTEXT-ONLY; touched=2 product_plus=6 product_minus=2 red=rc1/2FAIL green=rc0/5pass sibs=0 strict=False cat_ok=True rewritten=[]
rc=0
### LATESTSLOT
HELD → /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/READY_KS-1093-1093LATESTSLOT-R16B_ornith35b-q4_BRIEFED-BASHPATCH-LATEST-SLOT-SYMLINK-CHECK-IGNORE-SHAPE-PASS-7of7_2026-09-22.diff.md
  golden: CONTEXT-ONLY; touched=2 product_plus=3 product_minus=1 red=rc1/3FAIL green=rc0/6pass sibs=1 strict=True cat_ok=False rewritten=[]
rc=0

## Post-hold verification — Tue 22 Sep 2026 10:30:14 AEST
verify_readies.py (fence byte-identical to the run's patch.diff; RESULT + B2 lines quoted verbatim; brief located; golden verdict):
1139ERREXIT: fences=1 fence1==patch.diff:True RESULT quoted:True B2 quoted:True brief located:True golden:BYTE-IDENTICAL
1034HOOKENV: fences=1 fence1==patch.diff:True RESULT quoted:True B2 quoted:True brief located:True golden:BYTE-IDENTICAL
972BANNER: fences=1 fence1==patch.diff:True RESULT quoted:True B2 quoted:True brief located:True golden:CONTEXT-ONLY
1047STACKLEGS: fences=2 fence1==patch.diff:True fence2==section_1.diff (REANCHORED):True RESULT quoted:True B2 quoted:True brief located:True golden:CONTEXT-ONLY
1033DEMOBASE: fences=1 fence1==patch.diff:True RESULT quoted:True B2 quoted:True brief located:True golden:CONTEXT-ONLY
1093LATESTSLOT: fences=1 fence1==patch.diff:True RESULT quoted:True B2 quoted:True brief located:True golden:CONTEXT-ONLY
ls:
-rw-r--r--@ 1 kam_code  staff  13834 22 Sep 10:29 /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/READY_KS-1033-1033DEMOBASE-R16B_ornith35b-q4_BRIEFED-BASHPATCH-DEMO-MUTATION-GUARD-COMMIT-RANGE-BASE-PASS-7of7_2026-09-22.diff.md
-rw-r--r--@ 1 kam_code  staff  11258 22 Sep 10:29 /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/READY_KS-1034-1034HOOKENV-R16B_ornith35b-q4_BRIEFED-BASHPATCH-HOOK-REPO-ROOT-UNDER-GIT-DIR-LINKED-WORKTREE-PASS-7of7_2026-09-22.diff.md
-rw-r--r--@ 1 kam_code  staff  12842 22 Sep 10:29 /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/READY_KS-1047-1047STACKLEGS-R16B_ornith35b-q4_BRIEFED-BASHPATCH-PRE-PUSH-COMMENT-STACK-LEGS-3-4-8-PASS-7of7_2026-09-22.diff.md
-rw-r--r--@ 1 kam_code  staff  14034 22 Sep 10:29 /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/READY_KS-1093-1093LATESTSLOT-R16B_ornith35b-q4_BRIEFED-BASHPATCH-LATEST-SLOT-SYMLINK-CHECK-IGNORE-SHAPE-PASS-7of7_2026-09-22.diff.md
-rw-r--r--@ 1 kam_code  staff  11762 22 Sep 10:29 /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/READY_KS-1139-1139ERREXIT-R16B_ornith35b-q4_BRIEFED-BASHPATCH-VALIDATE-LINT-ARITHMETIC-COUNTERS-UNDER-ERREXIT-PASS-7of7_2026-09-22.diff.md
-rw-r--r--@ 1 kam_code  staff  11497 22 Sep 10:29 /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/READY_KS-972-972BANNER-R16B_ornith35b-q4_BRIEFED-BASHPATCH-START-BANNER-RETIRED-ADMIN-DEFAULT-CREDENTIAL-PASS-7of7_2026-09-22.diff.md
nothing quarantined this session; run dirs and goldens untouched (git status clean under runs/); no writes outside 2_Project_Files/local-model/ and the scratchpad.
