# Declared-rename allowance in A6 - report (harness engineer, 2026-11-11)
Root: /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/ . Every changed file has a copy `<file>.pre-1111-rename`. No git write verbs, no Spark round, nothing under night/briefs or READY_* touched.

## Finding that redirects the commission
The delta script in tasks/code_patch/checker.sh (read by code_patch2 at run time) only compares REDS; it never flagged a vanished passing cell.
The "declared cell LOST" verdict o132/o133 hit lives in spark/tiers/tier_checker.py (test_only_input / doc_only vitest A6; test_only_bash declared-cell and sibling-cell A6).
KS-2149/2155/2156 are bash-suite tickets, so that is where the allowance does the work. Both places were done.

## Files changed (+/-)
- spark/tiers/tier_brief.py +60/-0 : parse_renames(), check_renames() (pure, shared)
- spark/tiers/tier_checker.py +16/-1 : A6 in the vitest tier, bash declared cells, bash sibling cells
- spark/brief_lint.py +12/-0 : validates `## Renames`, emits B_RENAMES (JSON)
- spark/round.sh +6/-0 : writes B_RENAMES into input.json as `declared_renames`
- tasks/code_patch/checker.sh +30/-2 : delta script grades declared pairs (3rd arg = $INPUT)
- tasks/code_patch2/checker.sh +1/-1 : passes "$INPUT" to the extracted delta script
- spark/README.md +17/-0 : dated section naming this commission
- tests/a6_declared_rename_arms.sh : NEW, 210 lines

## Field format (brief)
    ## Renames
    - `<old cell full name>` -> `<new cell full name>`
Full name = checker's own cell name: vitest/jest fullName; bash `<suite basename> :: <label>`.
Lint refuses (rc 2): malformed bullet, `*` / `...` wildcard, old==new, a name in two pairs (not one-to-one), empty block, bash_patch/bash_patch2 tier.
A6 grades pairs against measured cells: old in baseline AND gone after; new NOT in baseline, present after, PASSING. Else FAIL: typo'd old, new red/absent, old still present, new pre-existing. Undeclared disappearances stay LOST. No block = no code path changes.

## My arms: tests/a6_declared_rename_arms.sh -> 31 PASS, 0 FAIL (rc 0)
D (real delta script extracted from checker.sh, hand-made vitest JSON), 12 arms:
- a no declaration, rename: rc 0 (as before; that script never flagged it), PASS
- b declared, new passes: rc 0, "accepted", PASS
- c declared, new FAILS: rc 1, PASS (arm expects FAIL)
- d old never in baseline: rc 1, PASS
- e declared pair + undeclared second change: rc 1 via NEW red on the second cell, PASS
- extra: old still present -> FAIL; new already in baseline -> FAIL; key absent -> unchanged
- 4 byte-identity arms: new script == .pre-1111-rename script, output and rc, with no 3rd arg and with an input lacking the key
L (brief_lint on temp briefs), 9 arms: none -> B_RENAMES=''; good block -> JSON; wildcard / dupe-new / chain / malformed / old==new / empty / bash_patch -> rc 2.
T (real tier_checker.py, test_only_bash fixture clone, clone clean after each), 10 arms:
- a no declaration, rename -> FAIL A6 ... LOST
- b declared, new passes -> PASS A6 (+ INFO accepted)
- c declared, new FAILS -> FAIL "new cell is failed, it must pass"
- d old never in baseline -> FAIL "never in the baseline"; bogus second pair -> FAIL
- e declared pair + undeclared second disappearance -> FAIL LOST (second cell named); both declared -> PASS; two renames undeclared -> FAIL LOST
- good output, no declaration -> PASS (default unchanged)

## (f) Existing arms, run as-is
PASS: tests/test_only_bash_spark_arms.sh 35/0; spark/tests/code_patch2_arms.sh 10/0; spark/tests/bash_patch2_arms.sh 22/0.
FAIL, all traceable to host/environment, NOT shown to be caused by this change (I did not re-run them on the .pre copies):
- spark/tests/arms.sh 23/7 and test_only_arms.sh 9/6 and eval_warn_arms.sh (c): "STALE BRIEF ... develop 0b55401ad5dc" (the old real briefs' tips drifted).
- spark/tests/new_tiers_arms.sh 22/25: HARNESS "cache/deps/Blockchain/Dev/node_modules is absent" (fixture deps missing on this mini).
- test_only_arms T5 compares against a .pre-1018 lint, so it already differed before today.
Direct lint regression I ran instead: 831 brief dirs, old (.pre-1111-rename) vs new lint: 125 byte-identical, 706 identical except the added `B_RENAMES=''` line, 0 different (output + rc).
tests/a6_isolation_arms.sh NOT RUN: needs a writable Secuura clone (it plants and restores a break; !CODING is off limits). Its A6 block and run_vitest, extracted from checker.sh, are md5-identical before/after my edit.

## UNMEASURED
- No real vitest/jest run through code_patch/code_patch2 checker with a declaration (D arms use hand-made JSON; the bash tier T arms are real).
- The vitest tiers (test_only_input, doc_only) share the edited A6 code but have no rename arm of their own.
- round.sh injection tested only by reading + bash -n; no --control round carried a `## Renames` block end to end (T arms feed input.json directly).
- Lint cannot see baseline/after; "old present in baseline" is enforced by A6, not lint.
- code_patch: a failed declaration also trips the isolation re-check, so the FAIL text ends "isolation re-check still red: none run" (cosmetic; the DECLARED RENAME FAIL line is in suite_delta.out).
- comment_patch/checker.sh has its own A6; not touched, not wired in round.sh.
- Bash cell names with digits: LOST uses digit-normalised keys; declared pairs are exact strings.

## What the next operator can brief
- KS-2149, KS-2155 (rename-only, bash suites via test_only_bash): yes, add the `## Renames` block with exact `<suite>.test.sh :: <label>` names read from a baseline run.
- KS-2156 piece 2: yes if its blocker was only the cell rename; the new cell must pass and every other cell must remain. Operator should run lint and a --control round with the golden first (the unmeasured end-to-end leg).

## Addendum: pre-edit vs post-edit on the four failing arms files (coordinator's no-skip request)
Method: scratch copies under scratchpad/cmp/{pre,post} (runs/ cut to the KS-1388 dir; spark-ab, spark/cache, spark/work, hosted, omlx, node_modules left out). In `pre`, all 7 .pre-1111-rename files restored over their twins. Same arms, same env, run in both. test_only_arms and eval_warn needed spark/cache, so both copies symlink the real spark/cache (those two were re-run that way; the first pass crashed in the fixture build on both sides).
| arms file | pre PASS/FAIL | post PASS/FAIL | failing sets |
| arms.sh | 23/7 | 23/7 | IDENTICAL (A3-dry-run, A3b, A7-real-round, A7e, A7b, A7c, A7d) |
| test_only_arms.sh | 9/6 | 9/6 | IDENTICAL (T2, T2b, T3a, T3b, T4e, T5) |
| eval_warn_arms.sh | 1/2 | 1/2 | IDENTICAL ((a), (c); (a) is a node_modules-absent HARNESS stop in the copy) |
| new_tiers_arms.sh | 22/25 | 22/25 | IDENTICAL (same 25 names, node_modules absent in the fixture deps) |
Verdict: no arm fails post that passes pre. The causes are STALE BRIEF (develop moved) and missing node_modules, not this change.
ONE REGRESSION FOUND INSIDE AN ALREADY-RED ARM, AND FIXED: test_only_arms T5 (lint vs the .pre-1018 lint) failed pre with 78 dirs differing, but post with 644, because my lint printed an extra `B_RENAMES=''` line for every brief. Fix (real tree, .pre copy kept): spark/brief_lint.py now emits B_RENAMES ONLY when a `## Renames` block exists, so a brief without one lints byte-identically. Re-measured: old-vs-new lint over 831 brief dirs = 831 byte-identical (was 125 + 706 with the extra line); test_only_arms T5 post = 78 dirs, same as pre; my a6_declared_rename_arms re-run = 32 PASS, 0 FAIL (the lint "none" arm now asserts no B_RENAMES line). The two real-tree runs I reported earlier for T5 (644) predate this fix.
Caveat: the copies share the real spark/cache through a symlink, and the post-fix full set of four was not re-run in the real tree, only test_only_arms T5 in the post copy and the lint comparison over all dirs.
