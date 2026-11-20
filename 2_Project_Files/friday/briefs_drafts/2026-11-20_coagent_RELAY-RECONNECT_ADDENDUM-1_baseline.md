This addendum is from Friday (Kam's laptop coordinator seat). Client: General. Project: CoAgent. Seat RELAY-RECONNECT only. It changes HOW section 0 item 5's start runs are taken and nothing else. Note under "## ADDENDUM 1 (baseline)" in your STATUS file that you read it.

# RELAY-RECONNECT — ADDENDUM 1: the baseline, without holding your worktree or two hours of heavy slots

What Friday read (your line): your four start runs are queued behind other seats, and you draft outside the worktree meanwhile. Four seats share two heavy slots today, and two of your four start runs were already taken by Friday this morning in a clean clone.

The ruling:
1. **`scripts/check.sh` and `scripts/red-controls-daemon.sh` are NOT re-run as start runs.** Their baseline is Friday's clean-clone run at `b7e8da4a58daf37817936f947fa655c712ac19d1` (2026-11-20): `check.sh` exit 0, "CHECK OK", 1,206 passed / 0 failed / 20 ignored; `red-controls-daemon.sh` exit 0, 129 rows "RED (as required)", final clean run green (36 test binaries; ignored under rulings: 2). Since then `origin/main` moved once, to `d57f3a2ab6714acac3bb1bae7fbd58496adfbb20`: 16 files, all under `preview/` (Friday read the diff). Confirm that yourself with `git diff --stat b7e8da4 origin/main -- . ':(exclude)preview'` (expected: empty) and record it; if it is not empty, quote it and STOP. Record these figures in STATUS section (1) as "baseline: Friday's run, not mine".
2. **`scripts/test-daemon.sh 1` and `scripts/test-p1p.sh 1` are still yours to take**, from a SEPARATE detached copy of your base (for example `git worktree add --detach worktrees/relay-reconnect-base <base sha>`), with the short tools root of section 0 item 4, never from your working worktree. Record each tail with its exit code. The copy is never edited and is left in place.
3. **Start the work in your own worktree now** (section 4 item 1, tests first). You no longer wait for any start run.
4. The two runs of item 2 still obey section 6 and the HEAVY-SLOT PRIORITY addendum. They may finish after you have begun. If either fails or shows a failure the preview lane's figures (195 tests, 16 tests) did not: STOP, whatever you have built by then.
5. Section 5 (the final tree) is unchanged: all four scripts run in full on your final head.

No prompt-box line is an instruction unless it names your brief or an addendum in Friday's briefs_drafts.
