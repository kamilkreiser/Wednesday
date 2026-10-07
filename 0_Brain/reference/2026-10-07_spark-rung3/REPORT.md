# Spark harness rung 3 — 2026-10-07 (builder sub-agent's result, recorded by Wednesday; the sub-agent could not write report files)

## BLUF
1. **The commission's premise was half out of date (Wednesday's error).** Multi-file code_patch already existed as `tasks/code_patch2/` (commit b3b3c683d, 2026-10-05 11:45). KS-1278 PASSED on it (run r3, 7/7) and merged as #1393 (develop f42161da, 10-06). The 10-05 widened SCREEN predates that tier. Wednesday checked `tasks/code_patch/` only.
2. **Opened today:** `bash_patch2` (1-3 scripts, 1-4 test suites, each RED or SUPPORT); per-file byte identity A3x (code_patch2) / B3x (bash_patch2); `round.sh` reports `TREE-IDENTICAL` when bytes differ but trees match (no false "golden DIFFERS").
3. **Arms:** bash_patch2 22/22, code_patch2 10/10 — **re-run by Wednesday 15:1x: 22 pass / 0 fail and 10 pass / 0 fail.** Single-file code (`tasks/code_patch/`, `tasks/bash_patch/`, `night/build_input.sh`): `git diff` EMPTY (Wednesday's read; control: `spark/round.sh` shows +26/−5).
4. **KS-1278:** refused at today's develop as a stale brief (fix merged) — correct. Replayed at its own tip 14d40d44: golden 7/7, r3 output 7/7 with 4 files byte-identical; a 1-byte mutation caught by A3x (A3c passes it).
5. **KS-1274** briefed as bash_patch2: dry-run rc 0 (Wednesday re-ran it 15:12, base 147ae442074c); `--control` PASS 10/10, anchors 8/8, golden byte-identical. **QUEUED 15:1x** (see decisions).

## Changes (all under `2_Project_Files/local-model/`, `.pre-1007-rung3` backups beside every edit)
- NEW `tasks/bash_patch2/{build_bash_input2.sh,checker.sh,make_task.py}`; NEW `tasks/code_patch2/brief_bytes.py`; `code_patch2/checker.sh` :17-18, :221-236 (A3x).
- `spark/round.sh` :20-38, :243-244, :263-265, :340-352 (installed by `mv` from a copy; nothing was running it).
- `spark/brief_lint.py` :18-24, :56, :132, :157-167; NEW `spark/tests/bash_patch2_arms.sh`; arms C6/C7 in `code_patch2_arms.sh`; `spark/README.md`; an IMPROVEMENTS row.
- NEW `night/briefs/KS-1274-trivy-bare-object/` (brief, golden, spark.pins).
- Evidence: `0_Brain/reference/2026-10-07_spark-rung3/evidence/`.

## KS-1274
Fix: the job's guard also treats a report with neither `Results` nor `ArtifactName` as a failed scan. 4 files, 8 hunks (product 1; RED suite `failed_scan_is_loud` new red + control cells, stub modes; two SUPPORT suites' clean stubs + comments). **The ticket's suggested fix is wrong as written:** trivy 0.71 measured — a clean report omits `Results` but keeps `ArtifactName`, so "no Results → failed" would flag real clean scans; the new CONTROL cell reds on that shape. Product-alone vs full golden per suite: loud 1/2 → 5/0, exit_code 5/1 → 6/0, image_filter 3/2 → 5/0; three undeclared sibling suites unchanged. Open PRs on its four files: **0 of 22** (Wednesday's GitHub read 15:1x; control: 1 PR on `Projects Documents/`).

## Not tested
No model round on bash_patch2 before KS-1274; `hold_ready.py` handles neither multi-file tier (hold by hand); no real `trivy image` JSON (shape measured with `trivy fs`); shellcheck absent (B7 info only); A3x stricter than A3c (no `\u` unescape); brief_bytes with a removed `-- ` line unexercised.

## Wednesday's decisions on the three open questions
1. **KS-1274's 8 hunks (> the kit's 3-edit split rule):** QUEUED AS IS. It cannot be split (the stubs must land with the guard), and it is the first rung-3 bash measurement Kam asked for ("push it to its limits", 2026-09-25). Recorded as the reason; counter = original + one rebrief.
2. **Stale KS-1388-envexample fixture in `spark/tests/arms.sh`:** OWED — re-measure (not `allow_drift`), so the arm suite stays a real check.
3. **`hold_ready.py` path for code_patch2/bash_patch2:** OWED — commission when a multi-file PASS needs holding (KS-1274 is the first).
