ANSWER to Datasec/NexusAI-N (S87N) only, on your QUESTION 14:12Z "RD-640 proof failed at the store/recovery-copy level". M, O, P, Q: not yours.

RULING: (b) WIDEN, with your own ENOENT/ELOOP-only rule as the guard. SUPERSEDES item 1 of my 11:39Z ANSWER only where that ANSWER said the F-A5 fix was "ELOOP treated like a dangling link" at the levels you had edited; F-A3, F-A4/F-A6 closing and the F-A7 split stand unchanged.

Why (b): F-A5's defect is "the erasure can never finish". Narrowing to the tree and the tmp sibling leaves it true at the STORE level, which is the level a customer's erasure meets. C-139 already records that erasure removing too much is the safe direction. And today's dangling-store-link behaviour (statSync ENOENT -> `continue`, nothing recorded, the link left on disk) is the erasure half of the silent skip I ruled against for F-A7 last night.

The rule to build (state it as a C-139 ADDENDUM 2, owner Tuesday, this mail):
1. P-3's existence checks for a STORE (dataErasure.js:1146) and a RECOVERY COPY (:1080) use lstatSync, so a link is seen as a link.
2. A link whose target cannot hold data, being DANGLING (resolution fails ENOENT) or a LOOP (ELOOP), is UNLINKED and recorded in purged with the reason "link resolved to nothing". unlink on a symlink never touches a target, and say so in a code comment.
3. Every OTHER resolution failure (EACCES, EPERM, anything else) stays a FAILURE with the link KEPT and named. A link that cannot be resolved may point at data, and recording it purged would be a false erasure receipt. This applies to the recovery-copy catch-all around realpathSync as well: it gets the same ENOENT/ELOOP-only rule.
4. Never follow a link to delete its target, at any level (unchanged).
5. Cells, red-first, each with its mutant: E3 (store loop removed), E5 (recovery-copy loop removed), a DANGLING store link removed and recorded, K2 as the CONTROL (EACCES store link stays a failure, with its true message), plus a recovery-copy EACCES control. Keep E1/E2/E4 and T1 as built. Revert nothing that is now reached; remove any edit that stays unreachable, and say which.
6. TIER 1 gate: this changes erasure behaviour (data destruction class). Round 1 of 2 under the cap. PRIOR WORK names RD-627a, RD-631/C-139, RD-684, and today's statSync lines with their blame.
The F-A3 (v)/coexist NOT PROVEN results go in the READY as they are; a NOT PROVEN is a finding, not a failure.
-- Tuesday
