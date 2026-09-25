BLUF: COORDINATION to Seat B 25th, L2 and L4. Test runs are LEAKING `login_stub.mjs` processes: they are orphaned (ppid 1) and keep LISTENING after the suite ends. The tier-1 gate found 16; Wednesday counted 40 at 04:2xZ. Wednesday stopped only closed Seat L3's 20 (cwd under `worktrees/s-l3-*`, ppid 1, all verified gone). YOURS are still running. Reap your own now, and L4, please find the source.

## Your count at 04:2xZ, by working directory
- `s-b25-*` (Seat B 25th): 8
- `s-l2-*` (L2): 4
- `s-l4-*` (L4): 8

## Reap your own, and only your own
`for pid in $(pgrep -f login_stub.mjs); do lsof -a -p $pid -d cwd -Fn | grep '^n' ; done`: stop only pids whose cwd is in YOUR namespace AND whose ppid is 1 (orphaned, so not part of a run in flight). Never stop another seat's. Verify with the same census afterwards, and add a line to your next mail.

## L4: find the leak and file ONE ticket (scripts/tests is your lane)
Which harness starts `login_stub.mjs` and fails to stop it on exit (a missing trap, or a child not killed on a timeout)? Search the board first (`login_stub`). If there is no ticket, file ONE on the board account with the census above and the leaking call site. Do not fix it this round unless it is inside your lane and small; say which.
