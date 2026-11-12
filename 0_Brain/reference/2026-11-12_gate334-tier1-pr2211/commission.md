# Gate 334, TIER 1 (Opus; routing v1.0 tier-1 row: a DATA-DESTRUCTION path — the kyc GDPR erasure cascade). Seat R 109th's row 19 = KS-1931 = PR 2211. Commissioned 2026-11-12 ~17:48 AEDT by the 16:49 Wednesday seat.

Method: copy-and-change of `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-12_gate331-tier1-pr2209/commission.md` (a tier-1 gate on a product row; read it and gate 332's verdict.md in `2026-11-12_gate332-tier1-pr2209-r2/` for the output shape, controls, mutant discipline and Constraints).

Pins (Wednesday's `git ls-remote origin` ~17:47 AEDT; RE-READ at start and end, and say if either moved): develop acee38da1ce7e9e94d4ec3186bb512b1794c7cb9 (PR 2157's squash, 3 api-gateway files, moved after the PR was cut); refs/pull/2211/head c0e112d6bc3e7cc74f3111ceacb42b0e1489be83 (ONE commit on develop cea1cdc2b07d). Merge-tree onto develop with each side's own merge-base, plus a control that develop's lines survive.

READY (read whole; reproduce, do not trust): `ready_r109_ks1931_mail.txt` in THIS folder.

What the row claims (from the READY, unverified by Wednesday): services/kyc/src/index.ts +4 -2: dbGetVerificationsByUser gains `throwOnError = false` and, after its log line, `if (throwOnError) throw err;`; the erasure cascade dbDeleteUserData passes true, so a failed verification read STOPS the cascade (before: it logged, continued with an empty image list and deleted the verification rows, orphaning legacy images while the route said all data was deleted). Every other caller (the GET route) keeps the empty list. New test ks1931-erasure-cascade-stops-when-the-verification-read-fails.test.ts (+151, 4 cells: R1, R2 red-first; C1, C2 controls). kyc whole suite 90/90 at develop, 94/94 at head. Body statement 2: the DELETE route still has no try block, so a failed cascade leaves the request unanswered and an unguarded rejection can exit the kyc process (UNCHANGED by this PR).

Questions:
1. **Correctness:** enumerate EVERY caller of dbGetVerificationsByUser at head (with a control); confirm only the cascade passes true and every other caller's behaviour is byte-unchanged. Reproduce R1/R2 red at develop and green at head; add mutants (cascade passes false; throw before the log; throw swallowed by an outer catch in the cascade; default flipped to true) and report survivors.
2. **What the cascade does on the new throw:** trace dbDeleteUserData and its callers at head: what has ALREADY been deleted when the throw fires (order of operations), is anything left half-erased, and does the caller (the DELETE route and any other entry point: queue consumer, admin path) surface the failure or swallow it? Is the new behaviour strictly safer than develop's (no case where develop erased fully and head now erases less without saying so)?
3. **Body statement 2 (DELETE route, no try):** measure it at head (a probe with a stand-in database is fine): unanswered request, process exit, or an Express default handler? State that it is PRE-EXISTING (develop) and whether this PR changes how often it fires (it now fires on a read failure that used to be swallowed): grade that consequence honestly.
4. **Suite and controls:** whole services/kyc vitest suite at head (or say why not), red-first by reverting index.ts only, a planted control that must fail. Load1 < 8.
5. **Census:** open PRs touching the 2 paths (with a control).
6. **PR body:** tier-1 statement, the behaviour change and statement 2 true to your measurements, Refs only, NO-PAIR.

Spark: the test-digest STANDARD (`2_Project_Files/local-model/digest/digest.py`) on any long log, raw rc read beside it (known bug G331-2209-5). Spark shadow review (`2_Project_Files/local-model/gate/spark_review.py --pr-body-file`, work dir outside WEDNESDAY as gates 332/333 did) as a calibration row only.

OUTPUT: `verdict.md` in THIS folder. First line: 'PR 2211: GO / GO WITH NOTES / NO GO (at head c0e112d6bc3e; tier 1; round 1)'. Findings G334-2211-N, graded (Major / Minor / Note / Info). NOT TESTED. The Spark result. If your Write is refused, return the text in full.

Constraints: exactly gate 332's. Read-only on the project checkout and every worktree (clone into `scratch/` in THIS folder for any write verb; installs only there, `--ignore-scripts`). Every npm/npx/vitest/tsc invocation names its directory explicitly and never runs from the WEDNESDAY working directory. No push, no comment, no ticket write, no merge, no mail. Never `cd`. If DevMASTER drops, wait, re-read what you wrote, then resume.
