# Proposal 5: `.gitignore` lines for generated packs

TARGET: `.gitignore`
APPEND at the end of the file:

```new
# WED-170 step 1 (2026-11-27): wake packs and their dropped-rows sidecars are GENERATED at every launch from tracked files; never committed (gitignore at creation)
0_Brain/wake/
2_Project_Files/wake/out/WAKE-*
# handover.sh: temp files (present only between write and rename, or left for inspection after an I/O fault) and the write lock (a directory that exists only while a write runs)
0_Brain/tasks/STATE-*.md.tmp.*
0_Brain/tasks/STATE-*.lock.d/
```

## Reason

The census found two 740 KB generated digests committed at every launch and counted generated files as a standing cost. The pack is rebuilt at each launch from files that are themselves tracked, so committing it adds history and merge noise for no information. Ignoring it also keeps the rotation script's stray-file check quiet. The state files `STATE-<seat>.md` and `STATE-<seat>-archive.md` are NOT ignored: they are the handover and must travel by git.

Round 3 (the checker's m6): round 2 ignored the whole of `2_Project_Files/wake/out/`, which would have kept the lane's own records (`out/STATUS_round1.md`, the saved test output) out of git. The pattern is now `out/WAKE-*`: only the generated packs and sidecars. The lock directory pattern is new with the write lock.

Checked read-only with a scratch excludes file (`git -c core.excludesFile=<scratch> check-ignore -v ...`), results in `STATUS.md`: ignored are `0_Brain/wake/WAKE-wednesday.md`, `0_Brain/wake/WAKE-wednesday.dropped.txt`, `2_Project_Files/wake/out/WAKE-wednesday.md`, `2_Project_Files/wake/out/WAKE-wednesday.dropped.txt`, `0_Brain/tasks/STATE-wednesday.md.tmp.123`, `0_Brain/tasks/STATE-wednesday.lock.d/owner`; NOT ignored are `0_Brain/tasks/STATE-wednesday.md`, `0_Brain/tasks/STATE-wednesday-archive.md`, `2_Project_Files/wake/out/STATUS_round1.md`, `2_Project_Files/wake/out/tests_last_run.txt`.

ROLLBACK: remove the six lines (`git revert` of the commit).
