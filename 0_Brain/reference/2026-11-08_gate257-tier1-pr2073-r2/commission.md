# Gate 257, tier 1, ROUND 2 OF 2: PR 2073, KS-1152 (connector-key rotate: rotated true only on a count of 1 or more). Launched 2026-11-08 by the 21:2x Wednesday seat

Common rules: /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-07_gate_tier1_common.md, read whole first. Corrections: develop is cfb6c1573ba9c948ebbe898fb2aec283bb9954ab by Wednesday's ls-remote at 22:1x AEDT (re-read at your start and end; it moves tonight); the QA template's no-rm rule wins (leave your clone at /private/tmp/g257, name its size). DevMASTER about 23 GiB free with a NAS move running: one clone; stop under 12 GiB. Keep load1 under 8. Never cd, even in a subshell. If a hook refuses git merge-tree, do what gate 255 did: run it in a clone under the session scratchpad, and say so.

Head 2684a29d8f576ff74634f07ad6576af5bd00370b (Wednesday's ls-remote, equal to the READY), a fast-forward from round 1's 9709acff5c5f; base bdbb11b21585; 8 paths.
READY: /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-08_seatY-8th/mail/out_03_ready_ks1152.md (read whole). Evidence under that seat folder.
Round 1: gate 245, /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-07_gate245-tier1-y-auth/verdict.md, PR 2073's F1 and F2. Cards: secuura-ks1152-rotated-true-on-count-zero-1107 = a and secuura-ks-1152-rotate-says-rotated-when-old-key-lives-1106 = b, by decision_queue.sh show. Wednesday's design ruling (A2: keep PRIOR_KEY_STILL_ACTIVE, message branched for the 0 case, console.warn; B1 wording) is Wednesday's, not Kam's: say if it is wider than his card.

Cap round: a further NO GO ships what is closed and tickets the rest; say per finding whether it blocks.
1. Gate 245's F1 and F2 closed, by your own read and run.
2. The 0 branch: is rotated false, priorKeysRevoked 0 and the warning exactly what the code returns for an existing organisation with a count of 0, and true only for 1 or more? Plant a defect of your own in the branch.
3. The seat's carried finding: after a 0, a retry answers rotated true (count 1) while an older key with no connector id still validates. Reproduce it. Is it inside the card's words, or does it make "rotated" a false statement Stuart's team will act on? This is the deciding question.
4. Spec text and S-K-OWNERSHIP-CONTRACT.md (Stuart's team reads it): every sentence true of the code at this head?
5. systemTest connector_keys.py:230 and its live caller: does any real caller now break?
6. Merge tree on develop cfb6c1573ba9 (PR 2060 merged, which shares platform.ts): clean, and do the KS-1152 cells still pass on the merged tree? Open PRs sharing a path (2072, 2077 on the generated yaml): whichever merges second regenerates; confirm the regeneration is deterministic.

Output: /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-08_gate257-tier1-pr2073-r2/verdict.md, as the common rules say. Findings only; post nothing; write nothing outside this folder and your clone.
