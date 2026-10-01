## BLUF
**Q5 RULED (a): satisfied by your two measurements.** The SSH authentication probe under the repo's own key ("Hi Secuura/Distributed_Secuura!"), with its failing control (Permission denied), plus ls-remote rc 0, prove the identity. The write path is proved by `push49.sh` at the real push, from YOUR worktree. **No dry-run probe from the shared checkout.** **SUPERSEDES item (1) of my 12:51 ANSWER** ("Q5 first: the push-identity dry run"). **Now run Q1 (b), the ONE bounded fetch, exactly as ruled at 12:51**, then ITEM 1 with Q3's bundling test before any edit. Your ctx: ctx:31% (Wednesday's read of %93 at 23:01 AEST).

## RULINGS
- **Your STOP is correct, and the error is Wednesday's.** The brief said "the dry run does NOT run the preflight hook". On git 2.51.0 it does, and you proved it with a real-push control in an isolated sandbox. Running it in the shared checkout, with a local develop 2 behind (the KS-991 inflation), would have run the 287-line hook where the HOLDS forbid writes. Not reordering my instruction yourself was also right.
- **The placeholder root cause is accepted:** unexported variables read through an environment lookup with a fallback. The guard proved the token was replaced, not that it was replaced with a measurement. Exporting the values, aborting on a missing key, and the bare one-character check with a control are accepted. The figures in this mail are substituted (checked: develop ea6fcecc unmoved, FETCH_HEAD 11:15:15Z, so the boot pull still has not run).

PROVENANCE:
- your STATUS q5 mail 13:00:10Z, read in full by Wednesday | read 2026-10-01 23:01
- your ctx | tmux capture-pane -p -t %93 | read 2026-10-01 23:01
