# QA Gate 83 verdict: Secuura/Distributed_Secuura PR 1898 (KS-1926, package_format_gate dead-pid picker), tier 2

## BLUF
**GO WITH NOTES.** The product-free change does what it says: the diff to package_format_gate.test.sh is exactly the two picker lines plus two comments, the new picker is `ps -p`, the same test the gate uses, and red-first reproduced on this machine (3 pass / 2 fail by assertion at base, 5/0 at head, 3 runs). Full package_format_gate.test.sh is 435/0 at base and at head. Merge-tree onto current develop is clean, fragment check OK with a planted defect caught. One real note: **the new suite's SKIP line is not recognised as a skip by run-shell-suites.sh** (G83-F1), so the honest-skip path is reported as a plain pass. Not blocking; a one-character fix.

## Heads
- START (logs/head_start.log, 2026-11-01T13:06Z): PR head `1c3accf3888310102c9693730fa4f17b6f6f1827` (matches expected), develop `8126b22bd5aa505be194996c9301b6e1ced5583e`, merge-base `d7691f35...` as expected.
- END (logs/head_end.log, 13:18Z): PR head unchanged `1c3accf3...`, worktree HEAD identical. Develop moved again to `ca36945e974081be6abbc15e548f4f8d02767e14` (nothing under systemTest or the KS-1926 fragments changed in 8126b22b..ca36945e); merge-tree re-run against it (section 7).
- Diffstat (logs/diffstat.log, logs/raw.log): 4 files, +114/-2 as claimed (1 M, 3 A).

## FINDINGS
- **G83-F1 (MEDIUM-LOW, claim not met in the runner)** The suite prints `SKIP: no live process ...` (with a colon). `run-shell-suites.sh` classifies a skip with `grep -qE '^[[:space:]]*SKIP[[:space:]]*[-—]'` (dash or em dash after SKIP, the "SKIP —" convention of KS-1127). A colon does not match. Measured (logs/runner_mini_skip.log): with `ps` shimmed to show no other-user pid, the suite prints the SKIP line, runs 3 cells, exits 0, and the runner prints `shell suites: 2 passed, 0 failed, 0 skipped`. So the skip path is counted as a pass, exactly what the runner's own comment says must not happen ("it is COUNTED, so it cannot read as a pass"). Fix: print `SKIP — no live process ...`. The control (real ps, logs/runner_mini_real.log) is `2 passed, 0 failed, 0 skipped` with 5 cells. Practical exposure: a user who is root, or a box with no other-user processes (some CI containers); there the picker's red-first property is not exercised and nothing says so.
- **G83-F2 (LOW, test strength)** In the skip path, nothing proves the pickers at all, and mutants that break the skip decision survive (M7, M8 below). Consequence of F1 plus the design; acceptable once F1 is fixed because the skip is then visible.
- **G83-F3 (INFO)** The seam is a text substitution into `eval`: the suite greps the subject for the literal `dead=$((50000 + RANDOM % 9000));`, so a future edit of that range makes the control cell ("exactly two picker lines") fail loudly (found != 2) rather than silently pass. Good; Spark's worry that it would run the original line is covered by that CONTROL cell.
- **G83-F4 (INFO)** New suite file mode is 100644, same as its sibling package_format_gate*.test.sh and the ks* suites (runner uses `bash <file>`, so not required). package_format_gate.test.sh mode stays 100644 (index lines `100644 100644`).
- **G83-F5 (INFO, environment)** Full shell runner at head here: `105 passed, 1 failed, 2 skipped (of 108)` (logs/runner_full_head.log), not the author's 107/0/1. The one failure, `blockchain_testing_target_base_follows_the_slot.test.sh`, is `FATAL: tsx not installed` (no node_modules in my fresh worktree) and fails the same way at base (logs/btb_head.log, logs/btb_base.log, both rc 2). The extra skip is preflight_test_types_ratchet_leg (also deps/environment). Neither touches this PR. The new suite ran inside it: 5 passed, 0 failed (log line 1905-1911).
- No HIGH. No finding blocks.

## 1. package_format_gate.test.sh diff exactness (logs/pfg_diff.log)
Three-dot diff vs merge-base: two hunks, `@@ -651,7 +651,8 @@` and `@@ -880,7 +881,8 @@`. Each replaces one `kill -0` loop with the `ps -p "$dead" >/dev/null 2>&1` loop and adds one comment line; `+6 -2` total. Nothing else. Modes 100644 both sides. File at repo root `systemTest/__tests__/` as claimed.

## 2. Picker correctness and termination
- Gate's death test (check-package-format.sh:336, `_sweep_dead_stages`): `ps -p "$pid" >/dev/null 2>&1 && continue`. The new picker is the same command and the same redirect, so "dead for the test" == "dead for the gate". The gate comment at :321 states the EPERM reason.
- Terminates: the loop increments `dead` until `ps -p` fails. Start range 50000-58999; macOS pids top out at 99999 and a pid above the max is "not found", so it ends within bounded steps unless ~41000 consecutive pids are live. Mutant M4 (no increment) hangs, which is the expected behaviour of that defect and shows the increment is what ends the loop.
- Never returns a live pid at pick time (the postcondition the suite asserts). Residual race (pid reused between pick and gate run) is inherent and the same as before.
- Zombies show in `ps -p` as alive; the gate sees the same, consistent.
- Note the gate itself still uses `kill -0` at :447, :455, :502 but only for its own same-user child processes (EPERM impossible); not the same class.

## 3. Red-first and the SKIP branch (logs/other-user evidence)
- Live other-user pids exist here: `ps -axo pid=,user=` shows root 1, 478, 480, ... (logs/otheruser_procs.log); `kill -0 1` rc 1 (operation not permitted), `ps -p 1` rc 0. The suite picked pid 58433 (also not signalable, ps sees it).
- Base (new suite copied onto the merge-base tree, logs/new_suite_on_base.log): `3 passed, 2 failed`, both failures by assertion: `picker 1/2 ... start 58433, picked '58433', which ps -p sees`, rc 1. Head: `5 passed, 0 failed` on three runs (logs/new_suite_head_1..3.log), rc 0 each.
- SKIP branch: it triggers only when no process is both not-signalable and visible. EXPECT=3 then and the run exits 0. It is honest in text (says why) but see G83-F1: the runner does not count it. It cannot hide a failure of the 3 cells that do run (CONTROL cells still assert, and exit requires FAIL=0 and PASS=EXPECT). A skipped run still prints the ratio `3 passed, 0 failed`.

## 4. Full runs (logs/pfg_full_base.log, logs/pfg_full_head.log, logs/runner_*.log)
- package_format_gate.test.sh: base `435 passed, 0 failed`; head `435 passed, 0 failed`. Matches.
- New suite x3: 5/0 each. Shell runner `--list`: 108 suites, includes `systemTest/__tests__/package_format_gate_dead_pid.test.sh`; `--check-unreached`: `OK - all 108 tracked shell suite(s) are reached` (logs/runner_list.log, logs/runner_check.log). Full runner: see G83-F5.

## 5. Mutants (scripts/mutants.py; copies under /private/tmp/gate83_spark/mut, repo untouched; logs/mut_*.log, logs/mutants_summary.log)
| Mutant | Result |
|---|---|
| M1 picker at case 20 back to kill -0 | KILLED (4/1, the one picker cell for that site) |
| M2 picker at case 32 back to kill -0 | KILLED (4/1) |
| M3 both back to kill -0 | KILLED (3/2) |
| M4 picker without increment | KILLED (hangs, alarm 20 s) |
| M5 picker loop condition inverted | KILLED (3/2) |
| M6 suite's run_picker returns the start pid | KILLED (3/2) |
| M7 SKIP condition always true | SURVIVED (3/0, rc 0), see G83-F1/F2 |
| M8 live-pid search never finds one (forced skip) | SURVIVED (3/0), same cause |
| M9 final `ps -p` assertion removed from the cell | SURVIVED (5/0); equivalent while the picker is correct, because the other picker mutants are caught by the same cell. Combined M3+M9 would pass, but M9 alone removes the one assertion; low value |
Tally: 9 mutants, 6 killed, 3 survived (M7, M8 are the skip route; M9 equivalent-ish). Each picker site is killed separately (M1, M2: the two sites are independently pinned).

## 6. Other kill -0 lines (logs/kill0_all.log, logs/picker_candidates.log)
36 hits at head in total; excluding the PR's own files (fragments, comments, the new suite) about 24 code lines. All remaining ones test liveness of a process the script itself started (same user, so no EPERM): run-shell-suites.sh:322, docker-build.sh:236, stop-environment.sh:33, check_shared_relink.test.sh:433-434, run_shell_suites.test.sh:591,776,780,875-880,1006-1013, check-package-format.sh:447,455,502. None is a dead-pid picker feeding a later `ps -p` check. A search for other pid pickers (`dead=`, `RANDOM %`) finds only the two fixed sites and the new suite. Candidates for a later look, not defects: stop-environment.sh:33 reads a pid from a pid file, where a pid owned by another user would read as stopped (`kill -0 $PID`); not in this PR's class (no ps -p counterpart).

## 7. Merge and fragments
- merge-tree of head onto develop 8126b22b: rc 0, tree `992af76bf7253286db108c322f043a03dc6a0a88` (logs/merge_tree.log). Onto current develop ca36945e: rc 0, tree `0b7ff29d1a46d56604ddb2cb3f0b236128c70cf4` (logs/merge_tree_current.log). Clean.
- `node Blockchain/Dev/scripts/docs-fragments.mjs check` at head: rc 0, `flow 117 legacy + 49 new, cheat 112 legacy + 49 new; lint clean, render passes html_docs_check`, final `OK`, with 2 ADVISORY (committed pages lag the render, by design as in gates 78/81/82) (logs/frag_check_clean.log). Planted `<div>` on the KS-1926 flow fragment: rc 1, `tags are not balanced: <div> opened 1, closed 0`, `FAIL` (logs/frag_check_planted.log); restored from git, sha256 equal (RESTORE_OK).

## Spark shadow calibration
Evidence: evidence/spark_shadow/ (facts.json, targeted_*.log, review.json, prompt and raw output). spark_gate.sh ran both files at head and on base product: 440 passed, 0 failed each, 287 s. That is not a red-first, because the PR is test-only and the shadow runs head's tests against base product (identical); it proves the green only.
Spark review verdict: **GO WITH NOTES** (4 Notes, 0 Major, 0 Minor). Match with mine: verdict yes.
- Recall of my findings: G83-F1 (colon vs dash, runner miscounts the skip): **missed**. G83-F2 (skip path unproven): partly hit (its note 1 says the skip branch was not run; quote not found in input). G83-F3 (eval seam): hit in spirit (its note 3, but it misses that the CONTROL cell catches a changed line). G83-F5, F4: not raised. Recall of substantive findings: about 1 of 2 partial, 0 of 1 for the main one.
- False positives: note 2 (race), true but acknowledged by the author and inherent; note 4 (fragments as "product_files"), harmless classification. Two of four quotes were not found verbatim in the input (evidence_quote_found_in_input false).
- It did not read run-shell-suites.sh, which is where the finding lives.

## Notes for the PR body
1. Change the SKIP line to `SKIP — no live process owned by another user is visible to this account` so run-shell-suites.sh counts it (regex `^[[:space:]]*SKIP[[:space:]]*[-—]`); then the runner prints `1 skipped` on such hosts.
2. Optional: say in the fragment that the shadow/CI numbers on a root-only host run 3 cells and skip the red-first cells.
3. Numbers confirmed: 435/0 at base and head, 5/0 new suite (3 runs), 3 pass / 2 fail at base by assertion with live root pid, 108 suites reached. The "107 pass / 0 fail / 1 skip" was not reproduced here (105/1/2) because a fresh worktree has no node_modules; the failing suite fails the same at base.
