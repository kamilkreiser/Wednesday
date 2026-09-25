BLUF: COORDINATION to all five Secuura seats. This SUPERSEDES the "bounded 20-min wait, then STOP" clause of the PUSH-WINDOW LOCK line in your brief. The lock's HOLDER changing is progress, not a timeout. Found by Seat B 25th: five seats, each push holding the lock 6-9 minutes, means a 20-minute bound on the WAIT would stop seats on a healthy lock.

## The new rule (replaces the 20-minute wait bound)
1. **Hold the lock for ONE push only**: take it, push one branch, verify at origin (`ls-remote`), release. Re-queue for your next branch. No seat holds it across a series. That keeps the queue fair.
2. **Keep waiting while the lock is HEALTHY.** Healthy = its holder pid is alive AND its heartbeat is under 5 min old. A changing holder is the queue moving. Keep polling, with no total bound.
3. **STOP and mail only when ONE of these holds:**
   (a) the SAME holder (same pid and branch) has held it for more than 20 minutes;
   (b) the heartbeat is more than 5 min stale with a dead pid;
   (c) you have waited 60 minutes in total.
   Never remove a lock you do not hold; that rule is unchanged.
4. **While you wait, keep working:** build and red-prove your next PR in your own worktree. Waiting on the lock must never idle a seat.
5. If your push tool bakes in a 20-minute or 21-poll limit, extend it to rule 3 with the same care you used for the keepalive: a copy beside the original, and prove the new wait on a scratch path before it guards a real push.

## Unchanged
Keepalive per invocation; `ls-remote` after every push; the second rc 141 means STOP; the legs 3/4/8 wording.
