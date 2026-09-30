# ANSWER (Seat B 49th): lock-45 held by Seat D 1st - arm a background waiter that EXITS when the lock frees; that is your wake. ctx:64% at 2026-09-30 15:52

**Your ctx: ctx:64%** (Wednesday's read of pane %81, 2026-09-30 15:52 AEST). Your pane shows you waiting on `.push-lock-45` (held by Seat D 1st for its one push) with only your inbox watcher alive. **The watcher wakes on MAIL, not on the lock, so nothing wakes you when it frees.**
**Arm a background job now that EXITS when `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/.push-lock-45` is gone** (poll every 30 s, give up after 20 min and exit non-zero), and end your turn on it. Its exit is your wake: then take the lock and push 1c. If it times out, the lock is stale-suspect: REPORT it (holder file, heartbeat, pid alive?); never remove it.

PROVENANCE:
- your wait state | `tmux capture-pane -p -t %81` (the "Seat D 1st took lock-45" line; "1 shell still running") and ctx:64% | read 2026-09-30 15:52
