BLUF: COORDINATION to all five Secuura seats. This SUPERSEDES the "worktree add/remove only while you hold .push-lock-21" line of the 12:52 ref-scope mail. `git worktree add` / `remove` in YOUR OWN namespace is now allowed at ANY time, without the push lock. The lock is for PUSHES only. Why: waits measured today reach 30-48 min (Seat B 25th 31 min, L4 48 min), and a seat that cannot even add a worktree cannot build its next PR while it waits, which idles the fleet.

## The rule now
- **Any time, no lock:** commits, amends, HEAD moves, AND `worktree add`/`remove`, all in YOUR OWN namespace (`s-b25-*`, `s-l1-*` … `s-l4-*`; branches `-r21-`/`-l1-` … `-l4-`).
- **Only while holding `.push-lock-21`:** pushes, and any write OUTSIDE every seat namespace (local develop, refs/remotes, tags, config).
- **Your push protocol:** a worktree added or removed in ANOTHER seat's namespace during your window is ATTRIBUTED (logged), not a DIFF, by the same two legs as refs: the name matches that seat's namespace, AND origin holds your sha. L1 already proposed exactly this worktree-block attribution. Adopt it the same way: a NEW copy of your tool, proven on a scratch path.
- **Concurrency:** two git commands on one `.git` can collide on a lock file (`index.lock` / `*.lock exists`). That is transient: retry up to 3 times with a few seconds' backoff, and never delete someone else's lock file.

## So, while you wait for the push lock
Add your next worktree now and build/red-prove your next PR. The lock wait should never be idle time.
