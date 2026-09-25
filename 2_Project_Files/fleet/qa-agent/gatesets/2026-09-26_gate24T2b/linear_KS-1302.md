KS-1302 run-shell-suites.sh leaves one empty /tmp/rss.* directory behind on every run under a long TMPDIR
state In Progress

## BLUF

`run-shell-suites.sh` creates a short-path working directory when `TMPDIR` is long (the KS-1135 fix, so tsx's IPC socket path stays under the platform limit) and **does not remove it**. Every such run leaves **one empty** `/tmp/rss.*` **directory** behind.

Non-blocking and recorded in #1234's squash body (merged `e68e2f0e837d`). Filed separately because it is a distinct fix from the `tee` behaviour also recorded there.

## Why it is worth tracking

The runner is executed on every push, and now also by hand in fresh worktrees (the only place these suites run since Actions was retired). One directory per run accumulates silently in `/tmp` — harmless individually, and exactly the kind of residue nobody attributes later because the creating process is long gone and the directory is empty.

## NOT claimed

No failure, no disk-pressure incident, and no measurement of how many have accumulated on any machine. This is the mechanism, recorded at the merge that introduced it.

## Fix shape

A `trap` that removes the directory on exit, including the abort paths — the runner already has abort paths (rc 2 on a fixture build failure, per #1218), so the trap must cover those and not only the clean exit.

## Board search before filing (team Secuura-PK, 1,291 issues incl. archived, 3,644 comments, literal match on titles, descriptions and comments)

* `/tmp/rss.` -> 2 total / 2 open: **KS-1127** and **KS-1135**, and both hits are this seat's own merge comments from today, not a pre-existing owner. `rss.XXXX` -> 1 / 1 (KS-1135, likewise).
* `run-shell-suites.sh` -> 29 total / 14 open — read for an existing owner of this residue; none.
* Control that fires: `run-shell-suites.sh` -> 29. Nonsense control -> **0**.

`Refs KS-1135`; does not close it.
