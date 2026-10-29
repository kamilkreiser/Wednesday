STARTABLE: YES, after Tuesday stamps the 7 slots and the last line (8 four-underscore lines, counted with the split pattern; control: a scratch line holding four underscores reads 1). Launch only through launch_when_cool; load1 7.01 / 11.33 / 12.68 at 13:40 (falling).

# B892 drafter report (Tuesday's read-only kit drafter), 2026-10-29 13:38 to about 13:50 AEDT

Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-29_B892_SEAT-G198_nexusai-139-rd900-tamper-cell-gate-tier2.md` (122 lines; 0 `@X@` tokens; 0 non-ASCII bytes; no person's name). Shape: B870 and B881 (read whole, with the finished B870 STATUS). Pane `Datasec/NexusAI-G198`, ports 9800-9809, G2 tier 2, round 1 of 2.

## Merge ref state (the one asked for)
- `refs/pull/139/merge` = `61df8a49fe86fde7ffbf23c7c19e9a1d489872a7`, **computed by GitHub at 13:38:00 AEDT over the CURRENT main `0df1e348`** (parents `0df1e348`, `1e9a2c03`; tree `5ca6818a2485dd0bf5c71c6bce94ba3ff0c154da`). `compare/0df1e348...61df8a49` = the one test path; file blob at the merge ref `45a2a890` = the head's. Head tree `6b9195db`, main tree `911b3e14`. PR #139 open, non-draft, `mergeable` true, `mergeable_state` blocked then unstable (checks running).
- The hosted `build` job `123229864385` was created 02:38:03Z, after the merge ref (02:38:00Z): it judges `61df8a49`. The kit tells the gate to build its OWN merge (`merge-tree` + `commit-tree` in its clone) and to say whether its tree equals the hosted tree.

## Measured and re-derived (byte-exact copies saved, `git hash-object` equal to the blobs)
- Test file main `885e5cf1` (686 lines) -> head `45a2a890` (702 lines). `diff -U0` hunks: -360 +360,3 / -361,0 +364 / -372,2 +375,3 / -376,2 +380,7 / -382,0 +392 / -383,0 +394 / -388,0 +400 / -391,2 +403,6 / -395 +411; removed old lines 360, 372, 373, 376, 377, 391, 392, 395; added 24; all inside old 359-397. Head pointers: `TORN_STORE_REFUSAL` 363, `isProductRefusal` 364, `describe` 366, cell `test(` 373, loop 393-410, `stormTorn` 400, `expect` 411-412. Main: regex 361, describe 363, cell 370, assertion 395. Titles by raw regex 15 = 15, equal lists.
- Helper `2e0f5208`: tamper branch 49-64, `code: e.code || null` 88, `firstErrors` 96. Product `bba3742b`: text built at 3247-3248, `_storeUnreadable` 3260-3267, code 3264.
- Counts file `38c0ae66`, 5223 / 310; depth-1 census 310 at main `0df1e348`. B889 has not landed (no `b889*` ref).
- Deploy switch: variables 0, environments [dev]. Last `Deploy demo` on main (`0df1e348`, PR #138's landing) run `40802579782` skipped, both jobs skipped, 0 steps.
- Hosted: Analyze python and actions success (results 0), javascript-typescript and build in progress, CodeQL summary `neutral` (not a result), 0 open alerts on the PR ref and merge ref (incomplete set); main has 124 open alerts, none at an rd407 path. Build job log of main's last push IS readable (`gh api -X GET --allow-escape-sequences .../logs`; without the flag the file is empty): rd407 `PASS` in 15.572 s on ubuntu-24.04 / node 24; the log prints no cell counters when green.

## D-decisions
- D1: gate runs on its own merge of head into current main and compares the tree with the hosted merge ref (the brief's ask).
- D2: P8 stated precisely: a hosted green proves `torn + lost + finalLost` above 0 on Linux (an agreed refusal needs a torn sample), not the figure; a hosted red prints the counters and is a Major, never a loosening.
- D3: 6 whole + 16 cell-alone runs on the committed bytes, 12 probe-copy runs for the six counters; the kit states the rule-of-three bound (about 13 percent per run, machine-local) and that it says nothing about Linux.
- D4: the builder's honest limit (the `refusals` term cannot flip the verdict) is proved from source and measured (T4), graded Note.
- D5: mutants GM0-GM9 plus GM6c, tamper T0-T4, predicate probe against the product's real error; one NEW check beyond B870: GM0 neutrality and a hosted-log read.

## Q-questions for Tuesday at stamp (each with its default)
- Q1 Tier 2 / round 1 of 2 on the new class "the tamper-control cell's refusal evidence" (B870 on the same file was a GO, not a NO GO; census of NO GO files: 3, none this class). Default: accept.
- Q2 B889 lands first (your stamp said so): its landing recomputes the merge ref and moves the counts pair; the kit lists it as EXPECTED (rd891 test + counts file together), makes the verify read main's new pair, and says hosted facts then belong to the earlier merge ref. Does the gate wait for B889, or run now? Default: run now, re-pin at the end.
- Q3 One hosted sample: the gate cannot re-run CI. Default: the refreshed `Build` after B889's landing is the second Linux sample (LANDING step 1).
- Q4 The dead `refusals` term and the redundant code clause: Note, not Major. Default: Note.
- Q5 G198 / 9800-9809: only the closed builder kit B877 names the block; no live pane or kit does; lsof clean. Default: accept; re-run the scan at the stamp. Hard stop suggestion 180 / 270 minutes (about 45 storm runs, 12 mutants, one verify, a lock queue).
- Q6 Run counts (6 whole, 16 cell, 12 probe) and the extra GM0 / T4. Default: keep.

## UNMEASURED
Every red or green (nothing was run); `torn` on the Linux runner; the hosted `build`, the javascript-typescript analysis and `CodeQL` conclusions (in progress at 13:39); the final `mergeable_state`; whether B889 lands before the gate ends; the 7-file neighbour list (derived by the gate).
