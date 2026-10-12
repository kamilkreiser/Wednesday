GO to S94N (Datasec/NexusAI-N): RD-838 round 3. SUPERSEDES Q1's "not built" default in Tuesday's 19:05:56Z ANSWER.

KAM RULED (live board, 2026-10-13 09:46:48 AEDT, view=tuesday, verbatim): "Decision nexusai-rd838-rd640-round3-1013: a — Yes, round 3 under RD-838". Option a's text: "N builds RD-838 on RD-640's branch with the two fixes and the missing cells; full tier-1 gate; merges in turn only on a GO." Put this ruling on RD-838 as a comment in your first turn (it is the authority for a third round past the cap); mail Tuesday the comment id.

BUILD exactly your confirmed plan: branch rd-838-erasure-chain-canonical-key-s94n off b214f6f, forward-merge main (now 08a81e2; re-read ls-remote first), own worktree, RD-827 own install.
- Fix 1 (F-640-1): key the loop by the canonical hop path, not dev:ino.
- Fix 2 (F-640-2): the cap counts LINKS; 256 to nothing is walked, 257 is kept; code and comment say the same number.
- Red-first cells at b214f6f: the F-640-1 shape at the four levels; 255/256/257 to nothing and to data; the survivor cells (unwalkable chain KEPT; hop dir EACCES/ENOTDIR KEPT). Mutants: M-inoKey, M-walkErrPurges, M-dirErrIsEnd, M-capOffByOne, plus RD-640's six.
- Linux leg in Docker node:24 as uid 1000, or "NOT RUN" said plainly.
- Partition: your plan measured NO overlap for RD-838's files across all open heads; re-check against main 08a81e2 before you push.
- READY FOR QA tier 1 with PRIOR WORK (RD-640 r1/r2 and gate 19's rows), NOT TESTED, and the round count ("round 3 of the RD-640 class, by Kam's 09:46:48 ruling").

GATE: RD-839's READY (057a69d) is HELD so both erasure tickets share ONE tier-1 gate. Tuesday commissions it when RD-838's READY lands. Proof holds queue behind any merge ticket (P's RD-823 merge holds the lock now).
-- Tuesday
