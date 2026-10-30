Seat W 10th

## BLUF
GO on your KS-1384 plan as mailed (01:17Z). Start F-a's edits now: items 1 and 5 first, items 2-4 locally, and no push of F-a until #1825 has merged (read by gh pr view + ls-remote, its own step). Then F0, F-b, R stacked, each ending READY FOR GATE TIER 1. Your 71-cell matrix is accepted as the plan; the gate will run its own mutants beside yours.

## Start authority (quoted, so you can check it in your own inbox)
Kam, 2026-10-30 10:07:32 AEDT, live board, verbatim: "Decision secuura-wednesday-go-counts-as-kams-word-1030: a — Yes: Wednesday's GO counts for starting work inside my standing grants (recommended)". This build sits inside Kam's card secuura-ks1384-f0-build-approval-1029 (a, "Build F-a, F0, F-b and R") and his 11:30:27 "pleas prioritise and action both". Signature classes still pause for Kam; F0 deploys are his, per box, after the census, and none is in your scope.

## Your asks, ruled
a. Throwaway Postgres: YES, exactly as you specified. Container s-w10-pg, postgres:15-alpine with --pull=never (only if already local; if not local, the real-DB cells ship UNMEASURED with the instrument named, no pull), bound to 127.0.0.1:55471 only, the repo's init + migrations, no data from any box, no chain keys in its environment. Read the before-state (name absent, port free, container and dangling-volume counts) and prove the same counts after `docker rm -f -v s-w10-pg`. Stop it at your wrap at the latest. It is reversible and local, so it is inside the grant; it is NOT a box.
b. payloadTimestamp = the STORED payload's timestamp, read in the upsert's own RETURNING (cell w2): ACCEPTED. That is the design's "stored metadata_payload" read correctly. Say it in the PR body as a reading, and list the new field for Kam's Platform S comms step (you send nothing).
c. The non-production 202 sentence: ACCEPTED (change it to say nothing was persisted locally). List it in the PR body beside payloadTimestamp as a response-text change.
d. Worktrees for F0/F-b/R made at their items from the previous head: ACCEPTED (saves three installs).
e. The stale caller lines in the comment at index.ts:1430-1431 (519 and 858, not 507 and 804): fix it in F-a since you edit dbPersistAnchor; say so in the PR body.

## Your disclosed faults
Accepted. The boot `cd` carried the harness cwd into the shared checkout and your first baseline vitest swept it (gitignored logs + two vitest caches rewritten, no tracked change, no ref). Keep every command absolute (`npm --prefix`, `git -C`) as you said, and name the side effects once more in your wrap.

## Checkpoint duties (unchanged)
Re-read KS-1384 and KS-772 at every checkpoint for Stuart's 09:01 UTC (20:01 AEDT) check; quote any new comment in your next mail; act on none.

Wednesday
