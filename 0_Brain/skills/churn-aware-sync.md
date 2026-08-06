# Two-pass churn-aware sync — ritual

Promoted at the 2026-08-06 consolidation (Kam-approved). Earned it: used twice
(WED-56/57), both times avoiding a sync that would have been stale before it
finished.

**The problem it solves:** syncing drives while agents are mid-session means the
data changes underneath the copy. A single pass finishes "successfully" and is
already out of date — worst of all, it *looks* complete.

## The two passes

1. **Bulk pass — while agents are still working.** Moves the large, stable
   majority (code, tools, history). Do not wait for a quiet moment that may
   never come.
2. **Cleanup pass — after the agents' receipts land.** Small, fast, and catches
   exactly the files the session was writing while pass 1 ran: daily notes,
   ledger rows, history entries, scoreboard.

## The verification that actually matters

**Check content at the FINAL destination, never leg exit codes.** Pick a file
you know changed at the origin today and grep it for today's content at the end
of the chain. `rc=0` on each hop certifies only that those two roots match — it
says nothing about whether an upstream leg ever ran. See
[[../learnings/2026-08-05_verify-the-chain-not-the-legs]], which came from a
pass that reported rc=0 and 0 failed while the destination lacked that morning's
writes entirely.

Also: `ls` is not enough — a file can exist and be stale. Grep for the content.

## Housekeeping

- Check for conflict copies afterwards and merge them by hand; record the merge.
  (A `.spoken.log` fork was merged sort-unique across three drives on 08-05.)
- Sync moves content, not always modes — **re-check exec bits on scripts** after
  a sync. A watcher whose `+x` was lost fails with "Permission denied" and looks
  like a code bug.
- Before unplugging: run a "nothing changed" check so the drive leaves in a
  known state.

**Related:** [[../learnings/2026-08-05_verify-the-chain-not-the-legs]],
[[../learnings/2026-07-31_fully-portable-drive]],
[[../learnings/2026-08-06_exercise-mechanisms-before-arming]]
