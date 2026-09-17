Wednesday -> Seat B (Secuura/Blockchain-B)

## BLUF
**SUPERSEDES item 5 of Wednesday's #1021 GO ("#1022 does NOT need a push").** Develop has moved to 81ee4b729 (read by the #1022 gate launcher's `--check` at 18:2x AEST; it REFUSED, rc 18, because develop moved onto `audit-baseline.json`). So after your #1021 MERGED receipt: **merge develop into #1022, re-measure, push, and mail HEAD MOVED** — the tier-1 gate is drafted and will be re-pinned to the new head before launch.

## Recommendation
1. Send #1021's MERGED receipt first (as the GO asked).
2. On #1022's branch: `git merge --no-ff` the then-current develop (never rebase, never cherry-pick). Expected: `audit-baseline.json` merges clean (the #1021 gate measured both orders → tree 1b03e6951, 34 rows). Predict the tree read-only first; name it.
3. Re-measure on the merged head: audit-gate + audit-locks rc 0 with the real baseline (34 rows), and the negative control (develop's locks with the 3 hono rows removed → rc 1, exactly the 3). Content re-read: the 4 PR files byte-identical to 58684e653 except the baseline file's merged row set.
4. Push, POST-PUSH CHECKS, then mail `HEAD MOVED: #1022 KS-1211 @<new head> (Seat B)` with the head read from origin, the merged tree, and the re-measured gate lines.
