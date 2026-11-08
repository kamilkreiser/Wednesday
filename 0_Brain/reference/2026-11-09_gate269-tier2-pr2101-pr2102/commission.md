# Gate 269, tier 2 BATCH, round 1 of 2: PR 2101 (KS-1783) + PR 2102 (KS-1864), test-only (2102 also carries one tool-written ratchet baseline file). Launched 2026-11-09 ~03:4x AEDT by the 01:53 Wednesday seat

Common rules: /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-07_gate_tier1_common.md, read whole first, applied at TIER 2 DEPTH (through code: diff read, cells re-run with a planted defect of your own, words true; no adversarial product probing beyond that). Stop line: if anything in either PR touches a product byte or needs tier 1, write NEEDS TIER 1 for that PR and stop on it. Batched under Kam's 2026-09-18 no-duplicate-gates rule: one session, ONE VERDICT PER PR.

Heads (Wednesday's ls-remote ~03:4x, equal to the READYs): PR 2101 7e0396990dfdc30742e4acef0f079e0ef44d797c; PR 2102 247e62dc7337a0f87e2b8a20d9c6107e6fcccf14. Develop 6220c168cc923d64c01c68b9693cfddb98f97a5c. Re-read all at start and end. Clone on the boot volume /private/tmp/g269 (QA no-rm, name its size); stop if DevMASTER under 10 GiB; load1 under 8; never cd; no box.

READYs (claims, untested by Wednesday): T 16th's mails, bodies in /private/tmp/wed_newmail/batch_20261108T163001Z.txt (KS-1783) and /private/tmp/wed_newmail/batch_20261108T164722Z.txt (KS-1864); evidence under /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-09_seatT-16th/evidence/ (pB5_ks1783, pB6_ks1864). Both originate from local-model (Spark/Ornith) passes, read by Wednesday at source. Wednesday's ruling: the baseline file in 2102 is allowed ONLY as written by `check.cjs services/api-gateway --update` (briefs_staged/2026-11-09_T16_answer_b6.md).

Per PR:
- 2101: do the three changed L6 cells now fail on a placeholder-shaped hash and pass on a real one (reproduce the seat's plant on one file; plant your own variant)? Any other cell in those files of the same shape left unpinned (name it, do not fix)?
- 2102: are the four test edits type-only (no assertion, no behaviour change)? Re-run `node scripts/typecheck-tests/check.cjs services/api-gateway` (cwd Blockchain/Dev) on the head: 15 errors, 15 in the baseline, 0 stale, rc 0? Is every removed baseline line one the head truly no longer produces (no line removed that still errors)? Plant a type error: rc 1.
- Both: words in the PR bodies and the ticket comments true at the head; merge tree on develop; paths shared with each other (expected none) or any open PR.

Output: /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-09_gate269-tier2-pr2101-pr2102/verdict.md, line 1 exactly 'PR 2101: <GO|GO WITH NOTES|NO GO|NEEDS TIER 1>; PR 2102: <...>', then per the common rules. Findings only; post nothing.
