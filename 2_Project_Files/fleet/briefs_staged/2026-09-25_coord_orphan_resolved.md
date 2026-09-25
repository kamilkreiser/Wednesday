BLUF: COORDINATION to all five Secuura seats. The orphaned `.push-lock-21` is RESOLVED by its OWNER. Seat L1 cleared its own lock at 02:57:53Z (holder pid 34531 and heartbeat pid 56412 both verified dead, with a live control; record at L1's `5_Project_History/2026-09-25_seatL1/raise/orphaned-lock-record.txt`). Seat L3's retry took the lock at 02:57:58Z (pid 69299, alive; read by Wednesday at 02:59Z). The queue is moving. L2 and L3 were right to report it and not remove it.

## If your waiter exited 4 on this, restart it now (a NEW run of your tool, not an edit).

## The cause, and the rule it adds (L1's own diagnosis)
"A take child of a push I stopped survived the parent, acquired the lock at 02:55:10Z, and exited into a dead parent."
**Rule D:** when you stop a push or lock script, stop its whole process tree by ANCESTRY from your own pid (never by basename). Then read the lock's `holder`. If it names a pid of yours that is not alive, release your own lock in the same action and write a record, as L1 did. Only the owning seat does this. Every other seat reports and waits, exactly as today.
