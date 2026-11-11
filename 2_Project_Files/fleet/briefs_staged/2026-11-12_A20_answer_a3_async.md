Seat A 20th

ANSWER: A3 signal handler needs an async spawn, and the exit codes. RULED: (A). This EXTENDS item 2 of Wednesday's plan ANSWER of 18:03:58Z (which ruled the codes 130/143 before your measurement); nothing in it is withdrawn.

Read whole by Wednesday: your QUESTION. Your three measurements (no handler: rc 143, finally skipped, child orphaned; handler over spawnSync: never ran, parent waited and exited 0; handler over async spawn: ran at +961 ms, child killed, rc 143, no orphan) are accepted as YOURS and they decide it: item 1 cannot be done without the async spawn.

THE RULING:
1. Item 1 = (A): move the prisma run from spawnSync to an async spawn; the post-run status check, the existence/freshness check and the OK line move into the child's exit callback. On SIGINT / SIGTERM the handler kills the child, removes the staging directory and exits 130 / 143 (128 + signal number, today's codes). All other messages and exit codes (0, 2, prisma's own, null status -> 1) unchanged. The restructure is inside the commissioned fix (the ticket asks for handlers that clean up and kill the child; this is the only way that works on Node), and it is Wednesday's call: say so in the PR body with your three measurements as the reason.
2. Cells: the three behaviours as cells (no orphan after a SIGTERM to the parent; staging dir gone after SIGINT and after SIGTERM; rc 130 / 143), red at develop where they can be (orphan + leftover dir), the codes pinned as unchanged; and a mutant that puts spawnSync back must turn the orphan/leftover cells red. Keep using a stand-in child (sleep) as you did; say so.
3. Pin census before the push (the rule in your brief): the OK-line text and any message you move.
4. Your defaults for items 3 and 5 are ACCEPTED: item 3 by comparing the client file's mtime with the run's start time (non-destructive); item 5 prints `path.relative(svc, generated)`. Say both in the PR body as Wednesday-accepted choices.
5. Pace unchanged: A3 to READY; A4 only if A3's READY reads 40 or under.

Not a signature class: a dev script and its test on a new branch.

Wednesday
