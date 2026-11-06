GO WITH NOTES
Head: 0dbf24bc0ce40135ed98fcff92661d752b95f350 (branch feature/ks-1728-shell-suites-grade-with-printf-grep-q-under-pipefail-two-batch-1; readings by ls-remote: 2026-11-06T07:59:51Z, 08:26:46Z, 08:34:06Z, all this SHA). A commit voids this verdict.

# Gate 228, tier 1, round 2 of 2: Secuura / Blockchain PR 2047 (KS-1728)

PRIOR ROUND: gate 226 gated this same SHA at tier 2, NO GO as a routing label only. Its report: /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-06_gate226-tier2-pr2047-ks1728/verdict.md. Its F1 is closed by this tier. F2 is re-graded below. F3 is unchanged.

## BLUF

- **The form change hides no broken guard in normal running.** 34 guard-break runs (24 distinct breaks, 6 slot credentials, 7 tracked credentials, 11 hook) on base and head: 34 of 34 gave the same rc, the same counts and zero differing output lines after normalising temp paths and SHAs. Every break went red in at least one suite except H3, which is F3 and is green on both sides.
- **Leg 14 in its real form is green and identical to the standalone runs:** 7 passed, 0 failed, 0 lines differing, 0 "Broken pipe". A broken hook makes leg 14 set fail=1. No closed pipe or output volume produced a false pass.
- **The form does add one narrow channel that base lacks (F1).** If bash cannot write its here-string temp file, `grep` never runs, the statement reads as "no match", and every negative-shape site passes. I measured a real broken hook reading 10 passed, 0 failed on head and red on base, using an injected fault. A persistent temp failure goes red on both sides. I never saw it happen without injection.
- **The commission's count of negated sites is too low.** Gate 226's 6 counts only the `! grep` spelling. By measurement, **31 of the 108 sites** pass on no match, and 23 of those are in the hook suites.
- **Pre-existing and outside this PR (F3):** no hook suite proves that a red preflight refuses a push.
- Merge tree on develop 35bcfa000b44: rc 0, clean.

## FINDINGS

### F1 (Minor; new with this form, latent). A here-string temp failure turns a negative-shape assertion green
- **Where:** the 31 sites in the Q2 table, for example `ks884_pre_push_tag_named_develop.test.sh:90`, `:141`, `:151` and `pre_push_hook_base.test.sh:285`, `:434`, `:470`, `:493`, `:648`, `:749`, `:818`.
- **Oracle:** Purpose. A guard's suite must not read green on a broken guard.
- **Evidence class:** MEASURED AT RUNTIME, with an injected fault. The natural occurrence was not observed.
- **FOUND:** on /bin/bash 3.2.57 a failed here-string prints `cannot create temp file for here document`, does not run grep, and the statement returns non-zero. Both ways of failing to get the temp file were driven:
  - create denied by `sandbox-exec`, write failed by `ulimit -f 0` (`evidence/q2_channels.txt`);
  - new negative shape and `! grep` shape: GREEN (false); old pipe form under the same fault: RED (correct); positive shape: RED (fails closed).
- This closes gate 226's "NOT TESTED: /tmp itself full or unwritable". Its `TMPDIR=/nonexistent` probe stayed correct only because bash falls back to another directory.
- **TESTED at suite level** (`evidence/q2_demo_fault_at_negative_sites.txt`), hook mutant H2 (preflight always runs), fault wrapper on ks884:90, :141, :151 only:

| side | no fault | fault |
|---|---|---|
| base | rc 1, 7 passed, 3 failed | rc 1, 7 passed, 3 failed |
| head | rc 1, 7 passed, 3 failed | **rc 0, 10 passed, 0 failed**, 3 here-doc errors on stderr |

- **What bounds it:**
  - Persistent failure fails closed. With all writes denied, the four credential and hook suites read rc 1 or 2 on both sides (`evidence/q2_whole_suite_no_temp.txt`).
  - The false green needs a guard regression and a write failure on exactly those lines, while the neighbouring lines' writes succeed. TMPDIR had 305 GiB free when measured.
  - Slot credentials `:141`, faulted on all four calls, stays red through its YES control (`evidence/q2_demo_fault_at_negative_sites.txt`). A fault on one NO call alone would pass that cell (READ ONLY, not driven).
- **The balance against base:** the old form has its own false-green channel, but only above the 64 KB pipe buffer.
  - Old form, needle on line 1: 0 false no-match in 2000 runs at 65,535 bytes and below, 300 of 300 at 69,999 bytes and above (rc 141). New form: 0 at every size (`evidence/q4_size_threshold.txt`, load average about 11).
  - The largest text any site greps in these seven suites is **1,847 bytes** (`evidence/q4_text_sizes.txt`).
  - So on today's text the old channel was out of reach and the new one is reachable only under this fault. That agrees with the PR's own statement that this is not a proven cure.
- **Fix-shape, owner's call, prose only (READ ONLY, not built):** `[[ $out == *needle* ]]` or `case` needs neither pipe nor temp file and removes both channels. A cheaper alternative is for the runner to treat `cannot create temp file for here document` in a suite log as a failure. A regression test would be the fault wrapper above with a broken hook, which must read red.

### F2 (Minor at most; I would grade it a note). Gate 226's empty pattern at `check_shared_relink.test.sh:1060` is not reachable by any real input
- **Evidence class:** MEASURED AT RUNTIME for the truth table, READ ONLY for the callers.
- **Callers:** tree-wide there are 3, at `:1063`, `:1066` and `:1069`. All pass literal strings, no variable is involved, and nothing sources the suite (`evidence/q3_callers.txt`). So a caller's variable cannot go empty.
- **Missing argument:** under the suite's `set -u` it aborts with `$3: unbound variable` (rc 1), which is red (`evidence/q3_primitive.txt`).
- **The only pair where old and new differ:** empty pattern with zero bytes of gate output. Base at this line is `printf '%s'`, giving bad; head gives ok. With any non-empty output, an empty pattern passes on both sides, so the helper was already vacuous there before this PR.
- It takes a future edit adding a blank-text caller. Gate 226's guard suggestion is still sound and still optional.

### F3 (Minor; pre-existing, outside this PR's diff, for routing). No hook suite proves a red preflight refuses a push
- **File:** `.githooks/pre-push`, the final `|| { ...; exit 1; }` after the preflight call.
- **Oracle:** Purpose.
- **Evidence class:** MEASURED AT RUNTIME.
- **TESTED:** H3 changes that `exit 1` to `exit 0`, placed in my own worktree as the real hook. All 8 hook suites that are green on this sparse tree stay green, base and head alike where run (`evidence/q1_h3_all_hook_suites.txt`, `q1_matrix.txt`).
- The ninth, `preflight_deps`, is red with and without H3, on the same 5 FAIL lines, because my sparse tree lacks files it reads. It is not evidence either way.
- A grep of every `*.test.sh` finds no fixture preflight that exits non-zero and no assertion on the refusal text (`evidence/q1_h3_coverage_search.txt`).
- **Effect if the hook regressed there:** every leg of the preflight becomes advisory, and no suite would say so.
- **Not a defect today:** the hook itself is correct at this SHA. A regression test would give the fixture preflight a non-zero exit and assert the push did not land.

### Notes (no severity)
- **N1, correcting a number carried in the commission.** "6 negated sites" counts one spelling. `if grep ...; then bad` is the same assertion, and the READY's "31 always-match" already said so. See Q2.
- **N2, launch condition, not the PR.** Started with SIGINT ignored on entry, as a background `&` does, `run_shell_suites` reads 79 passed rather than 82, because the SIGINT cells report themselves UNREACHABLE and score ok. Under default SIGINT it reads 82 and matches gate 226 exactly. My first leg 14 run showed this. A seat quoting 79 has a launch difference, not a lost cell (`evidence/q4_A_clean.out`, `q4_A2_clean_INT_default.out`).
- **N3.** The seven suites still hold short early-closing pipes the census does not count, for example `git diff --name-only ... | grep -q` at `pre_push_hook_base.test.sh:551`, `:553`, `:629`, `:631`, `git log -1 | grep -q` and `git ls-remote | grep -q .` (`evidence/q4_remaining_early_close_shapes_head.txt`). All carry small fixture output, well under the 64 KB threshold above. Most would err red. `:551` and `:631` would drop a PRECONDITION-LOST line. READ ONLY, unchanged by this PR, extends gate 226's F3.

## Per-question results

**Q1, false green in a guard. FAIL condition, stated before running: head green while base red, or different failing cells.** Result: never (`evidence/q1_matrix.txt`, `q1_guard_mutants.txt`, per-run output in `q1_runs/`). Suites are unedited at each SHA; guard copies are passed through CHECKER_SH, CHECK_SH and HOOK_SH; every edit asserted its anchor, and unmutated copies are the green baselines. Guards are byte-identical between base and head (`git diff` empty).

| break | suite | base and head |
|---|---|---|
| S1 shared literal exits 0 | check_slot_credentials | red, 18/14 |
| S2 shared not detected | same | red, 20/12 |
| S3 blank reads clean | same | red, 30/2 |
| S4 no .env exits 0 | same | red, 31/1 |
| S5 teardown offered for any failure | same | red, 31/1 |
| S6 shared muted by --quiet | same | red, 31/1 |
| N1 final exit 0 | no_tracked_credentials_root | red, 11/5 |
| N2 tracked half blind | same | red, 15/1 |
| N3 negation half blind | same | red, 12/4 |
| N4 defeated discovery reads clean | same | red, 14/2 |
| N5 dangling symlink missed | same | red, 15/1 |
| N6 git env not scrubbed | same | red, 14/2 |
| N7 root by path, not git | same | red, 11/5 |
| H1 preflight never runs | pre_push_hook_base / ks884 | red 27/9, red 8/2 |
| H2 preflight always runs | both | red 32/4, red 7/3 |
| H3 preflight red swallowed | both | **green, green (F3)** |
| H4 format gate red swallowed | both | red 35/1, green |
| H5 missing gate passes | both | red 34/2, green |
| H6 stale develop not ignored | both | red 35/1, red 8/2 |
| H7 KS-854 no base skips | both | red 34/2, red 9/1 |
| H8 KS-882 contains tip skips | both | red 34/2, green |
| H9 tag captures base | both | green, red 9/1 |
| H10 first ref only | both | red 34/2, green |
| H11 missing-gate text always | pre_push_hook_base | red 33/3 |

H11's row is in `evidence/q2_negative_site_table.txt`; the rest are in q1_matrix.txt. Greens in the ks884 and pre_push_hook_base columns other than H3 are breaks outside that suite's subject; the other suite catches each of them.

**Q2, sites that assert a negative.** Method: each of the 108 sites corrupted one at a time to never-match in my own copy, the suite run, restored and checked by sha256; green runs were re-traced to prove the line executed. Result: **73 red, 35 green, exactly the READY's 73 + 31 + 4.** Zero trace hits on exactly the READY's four unreachable sites (orchestrate_jobs 208, 448; run_shell_suites 166, 201). So 31 sites pass on no match (`evidence/q2_never_match_all_sites.tsv`).

| group | sites | could a regression slip on head that would not on base? |
|---|---|---|
| Hook behaviour | ks884 :90, :141, :151; pre_push_hook_base :285, :434, :470, :493, :648, :749, :818 | Normally no: each went red identically under a real hook break, on both sides (`evidence/q2_negative_site_table.txt`). Only under F1. **Driven with the fault:** ks884 :90, :141, :151. The other seven share the mechanism and were not driven. |
| Hook fixture preconditions | ks884 :80, :136, :146, :174; pre_push_hook_base :256, :349, :390, :428, :558, :636, :686, :705, :764 | Not a guard assertion. Under F1 a lost precondition would go unnoticed for that case. Not driven. |
| Credentials | check_slot_credentials: 0 pure sites; no_tracked_credentials_root: 0 (all `[ rc ] && grep`, which fail closed) | :141 is mixed: 3 NO cells plus 1 YES control. See F1. |
| Re-link | check_shared_relink :394, :478, :1085 | Same mechanism, sampled by mechanism only, not driven. |
| Orchestrator and runner | orchestrate_jobs :245, :324, :411, :444; run_shell_suites :197 | Same mechanism, not driven. The 4 orchestrate sites are gate 226's `! grep` ones, along with ks884 :141 and :151. |

**Q3.** See F2. Minor is the ceiling; not reachable by any real input.

**Q4, leg 14 in real form.** Lines 608 to 754 of preflight.sh extracted byte for byte (`scratch/leg14_extract.sh`), run with cwd Blockchain/Dev, slot-target sourced first, `set -uo pipefail`, /bin/bash 3.2.57. Only `step()` is a stub. The real `run-shell-suites.sh` reached exactly the seven (`evidence/q4_leg14_summary.txt`).
- **Clean env, default SIGINT:** rc 0, `shell suites: 7 passed, 0 failed, 0 skipped`, fail=0, 54 s; 39 variables de-slotted, ALLOW_FORCE stripped. Cells 112, 32, 10, 16, 18, 36, 82.
- **Against gate 226's standalone head outputs:** **0 differing lines in all seven**, 0 "Broken pipe", after normalising times, pids and tree path (`evidence/q4_vs_standalone.txt`).
- **Polluted (ALLOW_FORCE=1, GIT_DIR=decoy, GIT_CONFIG_PARAMETERS):** rc 0, the runner clears them, decoy config and refs unchanged.
- **Broken hook:** 5 passed, 2 failed, fail=1, rc 1.
- **Closed reader, SIGPIPE default:** rc 141 both for green and red; a false red, never a false pass.
- **Closed reader, SIGPIPE ignored:** green rc 0, red rc 1, the true verdict.
- **stdout closed outright:** green rc 0, red rc 1.
- **Volume:** the runner writes each suite to a file, not a pipe. A suite printing 5 MB keeps its rc (green 0, red 1), and a skip line before 5 MB is still counted. The hook and leg 14 put no pipe around the runner (READ ONLY).
- **FAIL condition, a red suite reading rc 0 or fail=0:** never met.

**Q5, merge tree.** Develop measured `35bcfa000b442943667deeee2cf7cec4f56d0cd0`, equal to pins.txt and unmoved at the end. `git merge-tree --write-tree` rc **0**, tree **`7b67a0ee283460dfdd7c1f39b4b69d9572bf37af`**, equal to gate 226's second reading. Merge-base aa4200e8a34c; PR files 9, develop files 108, shared paths 0 (`evidence/q5_merge_tree.txt`). I did not re-plant gate 226's same-line control.

## Taken on trust from gate 226, and what I sampled
- **On trust:** Q1 scope list; Q2 matrix beyond my probes; Q5 CRASHED arm; Q7 round trip; Q8 census and remainder; Q9 the 8 product scripts; Q10 legs 3, 4, 8; Q11 docs fragments.
- **Sampled myself and agreed:** cell counts in all seven, on my own worktrees and through the real runner; the bite split, now across all 108 sites rather than 3; merge tree and shared paths; the empty-pattern truth table.
- **Sampled and extended:** its here-string temp result. It was correct for what it ran, but it did not reach the failing case, which is F1.

## NOT TESTED
- A real `git push` through the real hook and full preflight. Leg 14 is an extraction, and the other 15 legs were not run.
- A natural temp-write failure. F1 is injected. Disk-full was approximated by `ulimit -f 0`, not by a full volume.
- Any bash but 3.2.57. The hook's comments name an Ubuntu VM. Newer bash may hold small here-strings in a pipe rather than a temp file, which would change F1 there; that is from memory, not measured.
- The fault wrapper on 28 of the 31 negative-shape sites: only ks884's three were driven through a whole suite, plus slot credentials :141, which is not one of the 31.
- A fault on one call of slot credentials :141.
- Guard breaks against check_shared_relink, orchestrate_jobs and run_shell_suites' own subjects. The commission asked for the two credential suites and the hook suite. Those three got the never-match sweep and leg 14 only.
- Heavy load beyond incidental load average about 11 from my own sweep. The original "Broken pipe" remains unreproduced at real text sizes in my sample (0 in 2000 at 1,846 bytes), which is not proof it cannot occur.
- run_shell_suites :201 and orchestrate_jobs :448 when reached: still not driven, as gate 226 reported.
- The PR title and body, and the Linear ticket: not read this round.
- Whether the two GitHub Actions workflows are truly dormant.

## Own conduct
- **Writes:** this folder only, in evidence/, scratch/, tmp/, repo/. No box, no docker, nothing posted, no git write in the source checkout. Gate 226's folder was read only; its two worktrees are still clean. All my worktrees are clean except wt_leg14's deliberate moves.
- **Clone:** `repo/` is `--shared` on gate 226's clone, so it relies on that clone's objects. Six sparse worktrees of about 4 MB each; folder total 43 MB. No npm install.
- **Network:** ls-remote three times and one fetch of two refs into my clone, using the Secuura Blockchain project's deploy key by file path. Its value was neither read nor printed.
- **Outside this folder:** suites make their own temp fixtures under the default TMPDIR and remove them themselves. Pointing TMPDIR inside this folder would have nested fixtures inside the WEDNESDAY repo and falsified the "outside any work tree" cells. No probe wrote to that directory on purpose.
- **Quarantine, no rm:** the other suites in wt_leg14 moved to `scratch/_quarantine_2026-11-06_leg14_other_suites/`, so the real runner reached only the seven. No `cd` in my commands; `scratch/run_in.py` and `run_in_int.py` set the working directory.
- **Errors of mine, in the open:**
  1. My first sparse pattern omitted Dockerfiles, so check_shared_relink went red on my tree (111/1) and leg 14 read 6 of 7. I read why it was red before believing it, added Dockerfiles and re-ran. The invalid run is kept under `evidence/q4_*FIRST_RUN_INVALID*`.
  2. My first leg 14 runs were launched in the background with SIGINT ignored, which is N2. I re-ran with default SIGINT, and that run is the reported one.
  3. My text-size harness failed twice on its own quoting and produced nothing before it worked. No number came from those runs.
  4. The Bash tool's hook refused one command for zsh word splitting; I rewrote it under bash.
  5. The sweep and the leg 14 re-run overlapped, so timings are not clean. Results were unaffected as far as I can tell: the sweep split and the 7/7 both match independent readings.

## Evidence index
`/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-06_gate228-tier1-pr2047-ks1728/evidence/`: q1_matrix.txt, q1_guard_mutants.txt, q1_runs/, q1_h3_all_hook_suites.txt, q1_h3_coverage_search.txt; q2_never_match_all_sites.tsv, q2_negative_site_table.txt, q2_channels.txt, q2_demo_fault_at_negative_sites.txt, q2_whole_suite_no_temp.txt; q3_callers.txt, q3_primitive.txt; q4_leg14_summary.txt, q4_A_clean.out, q4_A2_clean_INT_default.out, q4_B_polluted.out, q4_C_red.out, q4_vs_standalone.txt, q4_text_sizes.txt, q4_size_threshold.txt, q4_remaining_early_close_shapes_head.txt; q5_merge_tree.txt. Scripts: `scratch/`.
