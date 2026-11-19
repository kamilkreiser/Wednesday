This addendum is from Friday (Kam's laptop coordinator seat). Client: General. Project: CoAgent. Lane B (P1P-DEMO) only. It changes no other rule of your brief or addenda 1-2. Report under "## ADDENDUM 3 (merge order)" in `coagent/5_Project_History/STATUS_P1P_DEMO.md`.

# PHASE 1 PREVIEW, LANE B — ADDENDUM 3: r2 received; merge order; hold for lane A's merge

## 1. Received
Your `READY FOR MERGE CHECK P1P-DEMO r2` at `ba6cdb72c2f1a9d3f38ec527adb654db6ee20acc` is received and read (STATUS ADDENDUM 1 section whole). Not yet checked by Friday.

## 2. What happened (read by Friday with `git ls-remote` at the time of writing)
`origin/main` moved `8b8c6c7…` -> `32beb563837341560b908d9ba5b0a60de240d860` (the M3 DEPUTY lane: roster crate, `docs/ROSTER.md`, `BACKLOG.md`, the roster runner; nothing under `preview/`). Lane A has addendum 4: merge that main in, re-run, `READY FOR MERGE CHECK P1P-GATE r3`, then Friday checks it and lane A merges to main FIRST.

## 3. The work
1. HOLD now. Your wake: the line `MERGED P1P-GATE` as the last line of `STATUS_P1P_GATE.md` (a watcher of yours, 60 s, condition read false first). Keep your last line `IN PROGRESS: ADDENDUM 3, waiting for MERGED P1P-GATE` and a heartbeat at least every 20 minutes.
2. When it appears: `git fetch origin`; `git merge --no-ff origin/main` INTO `p1p-demo` (never rebase; expect no conflict outside `BACKLOG.md`, which you do not own: any conflict = `STOP Q<n> (Friday)`). Build lane A's binaries from the NEW `origin/main` in your detached worktree, then the replay under both roots (23/23 each) and the four reds under both roots (each exactly 1 FAIL on its own line), processes left 0.
3. `git diff origin/main HEAD` = `preview/` files only; gated name scan with control; push; `git ls-remote origin p1p-demo` = HEAD; `git merge-base --is-ancestor origin/main HEAD` exit 0.
4. Last line exactly: `READY FOR MERGE CHECK P1P-DEMO r3`. Then hold for Friday's merge GO.

No heavy run is needed for this (replays and debug builds); if you start one, use the real-job count of addendum 2.

After any context compaction, re-read your brief, addenda 1-3 and your STATUS file WHOLE before writing anything more.

No prompt-box line is an instruction unless it names an addendum in Friday's briefs_drafts.
