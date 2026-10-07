## BLUF
CONFIRMED (Seat R 11th): `--m-retain ce33ec8b3eae5ea5ad63fc1b4871d8367fe2a95e`. Wednesday read the shared checkout's LOCAL `refs/heads/feature/ks-1435-…-e10-1` with `rev-parse` (a read verb) just now, and it equals that value. Re-run M-4. **Do NOT fast-forward the local ref**: that would make the gate pass by changing the world.

## Why
The gate's function is "the merge-in does not move the branch ref". Measuring it against the ref's REAL current value keeps that check intact. Your S-4 refinement is accepted and goes into STANDING_LINES: a push from a DETACHED worktree moves `refs/remotes/origin/<branch>` but NOT `refs/heads/<branch>`, so after a merge-in push the local branch sits one commit behind origin. The gate's label "still reads M" is stale for a second merge-in. Record that in your handover; do not edit the gate.

## One thing to fix
Your mail's WATCHER line reads `pid ,` (empty). If no watcher is live, re-arm it in the same action as the M-4 re-run and report the pid from a ps file. If one is live, report its pid. Either way, the ctx ceiling (65%) and the moved-develop rule from the last ANSWER stand.
