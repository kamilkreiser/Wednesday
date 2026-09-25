KS-1303 run-shell-suites.sh now waits on orphaned children: tee keeps the pipe open until a suite's background child exits
state In Progress

## BLUF

Suite output in `run-shell-suites.sh` is now piped through `tee` (the KS-1127 headline-per-cause fix). A consequence shipped with it: **a suite that leaves a background child holding stdout or stderr delays the runner until that child exits.** `tee` cannot see end-of-file while any process still holds the write end of the pipe.

Non-blocking, recorded in #1234's squash body (merged `e68e2f0e837d`). A separate fix from the `/tmp/rss.*` residue also recorded there, hence a separate ticket.

## Why it matters

The runner is the gate on every push. A suite that forks something and returns cleanly now makes the **whole runner** hang for as long as that child lives — and the symptom is "the push is slow", attributed to the runner rather than to the suite that forked. The runner's own verdict is unaffected, which is what makes it hard to trace: nothing fails, it just stops for a while.

## NOT claimed

No suite is known to do this today. The finding is the **mechanism** the `tee` introduces, measured by the gate at the merge — not an observed hang. I have not surveyed the 60 suites for background children.

## Fix shape

Redirect the child's stdout/stderr explicitly rather than inheriting the pipe, or bound the wait (read with a timeout and report the suite that held it, so the symptom names its own cause instead of looking like runner slowness).

## Board search before filing (team Secuura-PK, 1,291 issues incl. archived, 3,644 comments, literal match on titles, descriptions and comments)

* `tee` -> 142 total / 60 open and `orphan` -> 73 / 20, both far too generic to indicate ownership; the open rows were scanned and none concerns the runner's pipe.
* `run-shell-suites.sh` -> 29 total / 14 open — read for an existing owner; none names this.
* Control that fires: `run-shell-suites.sh` -> 29. Nonsense control -> **0**.

`Refs KS-1127`; does not close it.
