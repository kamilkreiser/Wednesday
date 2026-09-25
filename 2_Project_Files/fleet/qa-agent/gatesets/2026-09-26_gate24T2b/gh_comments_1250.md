--- comment 5834086925 by linear[bot] at 2026-09-25T14:29:08Z
<!-- linear-linkback -->
<details>
<summary><a href="https://linear.app/secuura/issue/KS-1303/run-shell-suitessh-now-waits-on-orphaned-children-tee-keeps-the-pipe">KS-1303 run-shell-suites.sh now waits on orphaned children: tee keeps the pipe open until a suite's background child exits</a></summary>
<p>

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
</p>
</details>
<details>
<summary><a href="https://linear.app/secuura/issue/KS-1302/run-shell-suitessh-leaves-one-empty-tmprss-directory-behind-on-every">KS-1302 run-shell-suites.sh leaves one empty /tmp/rss.* directory behind on every run under a long TMPDIR</a></summary>
<p>

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
</p>
</details>
<!-- linear-review-link -->
<p><a href="https://linear.app/secuura/review/ks-1302-ks-1303-rsstrap-trap-the-runners-short-tmpdir-and-drop-the-98ab078e8dda">Review in Linear</a></p>

