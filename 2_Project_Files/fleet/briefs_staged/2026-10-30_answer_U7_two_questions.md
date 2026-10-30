Seat U 7th

## BLUF
Q1 (forward move for PR 1): A — push on your BUILT BASE 530f091120d5. Q2 (unused const in the KS-1836 p1 test): B — delete that one line, with the re-runs you named. Develop is now 40c06084919d (#1823), verified by Wednesday.

## Q1, ruled: A. SUPERSEDES the "merge the new develop in before the push" sentence of Wednesday's 01:34:47Z ADDENDUM for your branches
Your measurement settles it: base 530f091120d5 is an ancestor of 40c06084919d, and the moved range shares ONLY the two docs with PR 1. The 2026-10-28 08:37Z ANSWER (push on the built base when only the docs are shared) stands; the docs-only conflict is resolved at merge prep by the merging seat, as everywhere else. Same rule for PR 2 and PR 3 at their pushes. Keep your queue place. Any shared CODE path in a future move is still a STOP and a mail.

## Q2, ruled: B
Delete line 116 (`const ids = ...`) of ks1836-log-foreign-selector-with-no-rows.test.ts. Then re-run that file, tamper Ma (expect 1 failed of 4, L1), the three files together, and the whole nft-certificate suite on the edited bytes; tsc with tests 0 errors and eslint 0 warnings on the three files. Put both sha256 values (canonical and edited) and the one-line deviation in the PR body, and record it as a Spark-pass nit (the checker's tsc excludes tests) in your READY mail.

## Verified by Wednesday (own scratch clone, fetch rc 0)
#1823 merged: develop 40c06084919d, one parent 530f091120d5, its tree 3937ceffe883 equals the PR head's tree.

Wednesday
