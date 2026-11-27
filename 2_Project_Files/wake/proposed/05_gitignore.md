# Proposal 5: `.gitignore` lines for generated packs

TARGET: `.gitignore`
APPEND at the end of the file:

```new
# WED-170 step 1 (2026-11-27): wake packs are GENERATED at every launch from tracked files; never committed (gitignore at creation)
0_Brain/wake/
2_Project_Files/wake/out/WAKE-*
# handover.sh: temp files left for inspection after an I/O fault, and the write lock: a directory that exists only while a write runs, or, after a write died, the same directory set aside by the recovery line as STATE-<seat>.lock.d.stale-<stamp>
0_Brain/tasks/STATE-*.md.tmp.*
0_Brain/tasks/STATE-*.lock.d*
```

**In the same action, Wednesday removes line 29 of `.git/info/exclude`** (`2_Project_Files/wake/out/`, added 2026-11-27 as a local stop-gap "the lane gitignore proposal replaces this at cut-over"). While that line stands, the whole of the lane's `out/` is ignored on this machine and the round statuses and saved test output there never reach git (the second checker's N12). The build seat does not touch `.git`; this is the coordinator's one-line edit, and this proposal does not assume the line is there or gone.

## Reason

The census found two 740 KB generated digests committed at every launch and counted generated files as a standing cost. The pack is rebuilt at each launch from files that are themselves tracked, so committing it adds history and merge noise for no information. Ignoring it also keeps the rotation script's stray-file check quiet. The state files `STATE-<seat>.md` and `STATE-<seat>-archive.md` are NOT ignored: they are the handover and must travel by git.

Round 3 (the checker's m6): round 2 ignored the whole of `2_Project_Files/wake/out/`, which would have kept the lane's own records (`out/STATUS_round1.md`, the saved test output) out of git. The pattern is now `out/WAKE-*`: only the generated packs and sidecars. The lock directory pattern is new with the write lock.

Round 4 (the second checker's N3): the lock pattern was `STATE-*.lock.d/`, which did not match the directory the recovery line leaves behind (`STATE-<seat>.lock.d.stale-<stamp>`). So: a write dies, the seat runs the recovery line, writes its handover, and the rotation script then REFUSES on that stray untracked directory, at 85 to 90% context. The pattern is now `STATE-*.lock.d*`, which covers the live lock, a set-aside one, and everything inside either (the tool's temp files now live inside the lock directory while a write runs). The sidecar wording is gone with the sidecar: round 4 carries the grants register whole and writes one file.

Checked read-only with a scratch excludes file (`git -c core.excludesFile=<scratch> check-ignore -v ...`), results in `STATUS.md`: ignored are `0_Brain/wake/WAKE-wednesday.md`, `2_Project_Files/wake/out/WAKE-wednesday.md`, `0_Brain/tasks/STATE-wednesday.md.tmp.123`, `0_Brain/tasks/STATE-wednesday.lock.d/owner`, `0_Brain/tasks/STATE-wednesday.lock.d/state.tmp.123-abc`, `0_Brain/tasks/STATE-wednesday.lock.d.stale-20261127-101500/owner` (round 4: re-run, see `STATUS.md`); NOT ignored are `0_Brain/tasks/STATE-wednesday.md`, `0_Brain/tasks/STATE-wednesday-archive.md`, `2_Project_Files/wake/out/STATUS_round1.md`, `2_Project_Files/wake/out/tests_last_run.txt`.

ROLLBACK: remove the six lines (`git revert` of the commit).
