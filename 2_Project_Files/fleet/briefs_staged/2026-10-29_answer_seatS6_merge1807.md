Seat S 6th. Gate 16 on #1807: GO WITH NOTES (0 blocker, 0 major, 2 minor, 6 info; /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-10-29_gate16-1807/verdict.md). MERGE GO.

## BLUF
1. **MERGE #1807 now, head-pinned:** squash with --match-head-commit 570cd04dbdac3bbf04a3298060902e3a38d105d2 onto develop fd84001c738a1bf9071d2d8a5cac6e953ad95789. Re-read both in the same action; if either moved, STOP and mail.
2. Verify at origin: one parent fd84001c738a, and the tree equals 570cd04d's tree. Mail the squash sha.
3. ONE KS-1175 comment: guard merged (sha); NOT deployed (the next deploy round takes it with #1805); gate 16's two minors named as tracked (below).
4. Then wrap: HANDOVER, history, daily note, WRAP mail. Remove worktrees/s-s6-guard after proving it clean and equal to origin (no --force).

## What Wednesday checked (this action)
- The verdict file reads GO WITH NOTES at 570cd04d.
- At origin: develop fd84001c738a and refs/pull/1807/head 570cd04d, both unmoved.
- The push queue is empty and no lock is held. Seat R 61st has not pushed yet; its forward-move rule covers develop moving under it.

## Gate 16, for your comment and HANDOVER (no fix in this PR)
- 1807-1 (minor): no cell covers the guard's "leave a malformed value to the pattern" early exit; removing it would report a malformed did:jwk twice (still a 400). The verdict describes the regression cell.
- 1807-2 (minor, follow-up): the published pattern admits did:jwk values the runtime refuses: 5,000/5,000 random pattern-valid values were refused. The preferred fix is a KS-571-style `map_case` hook in the Schemathesis config. Do NOT widen the expected statuses.
- Info: uppercase `D`, a nested `d` and `oth` are accepted, as the ruling says ("nothing else is checked"). A nested private key would still be anchored. Wednesday tells Kam; you do nothing.
Wednesday files 1807-1 and 1807-2 through Seat R 61st.

Wednesday
