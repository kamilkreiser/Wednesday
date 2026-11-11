# Drafter notes: brief_B135.md (Seat B 135th), 2026-11-11 about 17:5x AEDT

Read whole: commission; B 134th's brief (all 145 lines); B 134th's HANDOVER (FINAL block, whole file); B 134th's wrap_body.txt, launch_preflight and history entry (top); Wednesday's three mails to B 134th; R 96th's answer + addendum; B 133rd's queue-table header and rows 7i / 8y (spot reads only). NOT opened: gate 306 / 307 verdicts, B 133rd's STANDING ITEMS / TRAPS sections, Linear, the PR API, the commission's named spark folder.

## Live readings (read-only, no fetch)
- `GIT_OPTIONAL_LOCKS=0 git ls-remote origin refs/heads/develop 'refs/pull/*/head'` through the shared checkout at 17:42:44 AEDT: rc 0, 2,090 lines. develop = `fcd178ff34fa3b289baeb1c1fb6783161bec3e0d` (equals B 134th's MERGED and the commission). PR 2171 head `be5d7b6057cd00f85cc4978bf29fd6b3fe7071ee` still shown as refs/pull/2171/head (merged PRs keep their ref).
- Program compare (python -I): 53 tail rows + 5 rows 8y to 8zc = 58 of 58 heads equal, 0 moved, planted last-digit control refused. No queued PR is missing.
- Line count: B 134th's brief says "2,089 lines" at 16:49 (before PR 2171 existed); now 2,090 = 2,089 pull refs + develop. The +1 is PR 2171's ref; consistent, not a contradiction.
- history.md: `Seat B 135` = 0, `Seat B 134` = 1, `Seat B 133` = 2, `Seat B 132` = 2; 6,564,288 bytes; headings B 134th line 1, B 133rd 13, S 55th 25, U 23rd 37. `df -g`: 2,432 GiB available.

## Stale pins corrected (all moved to `fcd178ff34fa`)
1. develop `6911aa643db1` -> `fcd178ff34fa3b289baeb1c1fb6783161bec3e0d` in BLUF, plan, pins.
2. B 134th's rows 8y to 8zc carried "Set-up merge tree on `249be7c8cd14`: ... (RECOMPUTE)" (a pre-PR-2165 develop, TWO develops old) and 8y "B 133rd's set-up merge tree ... `a1751cd6941d`": all five struck from the row text; the brief says none is carried and every tree is computed on `fcd178ff34fa`. `evidence/merge_trees_plan_b134.out` (on `6911aa643db1`) is named stale.
3. B 134th's PR 2166 READY (06:24Z, develop `6911aa643db1`) named stale and not reused; `tools/run_merge_b134.sh` case lines 2166 / 2171 and `tools/ready_build2_b134.py` CFG entries (`base` / `gdev` = `6911aa643db1`) named do-not-reuse (verified by grep).
4. Seat names / counts: B 134th -> B 135th everywhere, B 135th's wrap target 'FOR SEAT B 136th'; ordinal counts re-taken (B 134's own heading now 1; B 133 now 2, not 1).
5. Spark operator o140 -> o143 (commission and `reference/2026-11-11_spark-operator-o143/`). Pace line "about 16.5 points" set-up replaced by the 15 aim with B 134th's 21.9 / 19.4 and boot range 17 to 23.
6. ROW 0 section, stamp block and 'RULED BY WEDNESDAY AT THE STAMP' of B 134th removed as spent; the tail line now says row 0 (PR 2171) is MERGED and struck beside row 8x.
7. Disk and `[KS-907]` live-session facts re-keyed (B 134th's preflight read, PID 71165 = R 96th).

## Contradictions found
1. **Commission vs artefacts, owed edits:** the commission (and B 134th's HANDOVER wording) lists "heads_vs_brief, pr_states, fetch_refs_q: PR 2171 out" as owed. By grep they are ALREADY done: `heads_vs_brief_b134.py` DEVELOP12 `fcd178ff34fa` with 2171 in MERGED_REF; `fetch_refs_q_b134.py` docstring records 2171 added then taken out again (61 rows); `pr_states_b134.py` carries 2171 in its extra list (its job is states of merged PRs, so it stays). What is still owed: take 2166 (and later rows) out as they merge, add rows 8z to 8zc to pr_states, and re-point `faults_count_b134.py` PATH and BRIEF MARKER. The brief says this; a seat that "takes 2171 out" again would hit an assert.
2. **Tool-file count:** HANDOVER says `tools/` 40 files; `ls` shows 47. B 134th's own kit_copy line says 48 tools files for B 133rd's source. The brief tells B 135th to take its own probe count and say which it finds. Not resolved by me.
3. **B 134th's percent at wrap:** history entry says "about 59 percent"; wrap mail and tool figure say 60.9 percent measured at the start of its wrap (609,499 tokens), after readings of 57.4 at MERGED. I used 60.9 as measured and the readings by name.
4. **PLAN reading:** B 134th's plan mail said 17.5, its HANDOVER says 20.0 by the transcript record; the brief gives both (boot range 17 to 23 with B 133rd's 23.0).
5. **History heading source:** HANDOVER item 17 says the counter's rm / find hits are words in its own text; not a contradiction, carried as is.
6. **Wednesday's stamp:** B 134th's brief had a stamp block that "WINS". This brief's stamp block is empty by design (drafter writes none) and says so; do not read the missing stamp as a missing ruling.
7. **Proposal flagged for Wednesday (not a ruling):** the dearest B 134th set-up cost was reading B 133rd's TRAPS CARRIED (26 KB). The brief marks "HANDOVER trap list plus STANDING ITEMS may stand in" as a PROPOSAL; until stamped, B 135th reads it as B 134th's brief binds it. Strike or stamp it.
8. **Row 36 vs row 8zc (not a contradiction, a watch):** R 96th's row 36 writes `services/transfer/src/index.ts`; PR 2170 writes `services/transfer/src/approvalWorkflowService.ts` (carried file lists). Different files; the brief tells B 135th to recompute at each tree.

## UNMEASURED by me
Merge trees of rows 8y to 8zc on `fcd178ff34fa` (merge-tree --write-tree is barred); that the squash `fcd178ff34fa` has one parent `6911aa643db1` (carried from B 134th's evidence, not re-read in its clone); PR API state, bodies, Linear state of every ticket; the two gate verdict files; the exact PRs for R 96th's rows 36 to 38 (arrive by mail); S 56th's existence; B 134th's clone contents (the directory holds one entry, not listed); `merge_b135.py` / `send_wrap_b135.sh` are re-keys of `tools/merge_b134.py` and `tools/send_wrap_b134.sh`, both confirmed present by `ls`.

## Provenance
Every queued ticket has a `KS-NNNN | <source> | read 2026-11-11` line (53 tail rows generated by program from B 134th's lines 92 to 144 with the head-equality statement re-dated to 17:42:44; five rows 8y to 8zc written separately). Brief is lean by design: unchanged procedure is named by file and line range.
