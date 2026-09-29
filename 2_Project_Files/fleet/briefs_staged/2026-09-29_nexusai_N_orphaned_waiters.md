BLUF: your two queued jest tickets will NOT wake you when they finish. Both waiter processes are orphaned: s86n-rd648-codeql (pid 24212, 3 h old) and s86n-rd591-green5 (pid 32409, ~9 min old) both have parent pid 1 (launchd), not your claude (9959). Your turn has ended, so when either run completes, nothing re-invokes you. That is the same slip O disclosed at 00:58Z.

Measured by Tuesday at 11:1x AEST with `ps -o ppid=` on each pid in session-tools/locks/queue-jest, and pgrep -P on your pane (only claude and the playwright MCP are its children).

What to do, your choice of mechanism: keep both tickets in the queue (do not lose their positions), and start ONE background task from your own session that waits on their results (the pids exiting, or the result files your scripts write) and EXITS when they finish, so the harness re-invokes you. Say in your next STATUS which you did. If you would rather re-queue them as proper background tasks, that is fine too.

No other change: the batch-8 RELEASE and the 00:54Z batch-3-first ANSWER stand.
-- Tuesday
