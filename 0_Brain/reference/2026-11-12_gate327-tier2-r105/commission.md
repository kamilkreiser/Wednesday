# Gate 327, TIER 2 (Sonnet; routing v1.0 tier-2 row: one comment line + test cells, no behaviour change claimed). Seat R 105th's batched READY round 1: PR 2203 (KS-2169) and PR 2206 (KS-2005). Commissioned 2026-11-12 ~12:5x AEDT by the 12:3x Wednesday seat.

Method: copy-and-change of `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-12_gate320-tier2-pr2196/commission.md`. Read it whole: its Constraints, output shape and controls all apply. Calibration: gate 320's, 322's and 324's verdict.md.

Pins (Wednesday's `git ls-remote origin` 12:57:20 AEDT; RE-READ at start and end, and say if any moved): develop 1247e1af3c203d369d01b4d574de377adeec4b98; refs/pull/2203/head 67baaef2f105c4fcf03bd66660d91fb990be7d2d (cut on 697f422f1a39); refs/pull/2206/head 36c0b86b3dd0d634c635f72e1a854872f56f5a4d (cut on 088fa84da10c). Merge-tree each onto 1247e1af3c20 with each side's own merge-base (never `git merge-file` with a hand-chosen base: ledger 2026-11-12).

READY (read whole; reproduce, do not trust): `ready_r105_mail.txt` in THIS folder.

What the rows claim (from the READY, unverified by Wednesday):
- PR 2203: `services/transfer/src/index.ts` +1 -1 is a COMMENT line only (line ~427; emitted JS claimed identical); two new cells R7 (trim before max) and R8 (true, false, 0 and an array each answer 400) in the ks2055 test, +18. transfer suite 481 -> 483 green.
- PR 2206: one new cell R6 (ONE created and 13 failed answers 200 with success false) in `services/originate/src/__tests__/ks1990-seed-demo-users-success-follows-the-counts.test.ts`, +10. originate suite 2,598 -> 2,599 green under JEST.

Questions:
1. PR 2203 comment-only claim: prove the `index.ts` change is a comment (emitted JS identical by your own build, with a planted non-comment change that DOES change the emit). Does the new comment's text say anything false about the code it sits on (the bound, who ruled it)?
2. PR 2203 cells: R7 and R8 RED against a plausible wrong implementation (reproduce the seat's plant `z.coerce.string().max(1000).trim().nullish()` AND one plant of your own choosing), GREEN at the head. Do R7/R8 test the property the ticket names, or something adjacent?
3. PR 2206 cell: R6 RED against gate 195's mutant g1 (`created === 0` -> `created < 2` at adminConfig.ts ~2163) and against one mutant of your own; GREEN at the head. **Run originate under JEST with a whole-suite invocation you have checked is not a path filter** (the seat's finding R105-F1: its kit appended `run` to a jest script, which jest reads as a path filter, and a first read showed 2 suites as the whole suite). State the suite and test counts and how you know they are the whole suite.
4. tsc with tests: the seat reports 4 errors in two EXISTING untouched test files (ks1937, ks488) under types node,jest. Reproduce at develop and at the head: equal? (pre-existing = a filing note, not this gate's defect).
5. Census: open PRs touching each row's paths (with a control). The seat names PRs 2087 and 2158 as listing adminConfig.ts (not the test file). Confirm no shared path for either row.
6. PR bodies: no closing word; PR 2206's body no longer carries a "Refs" before another ticket's key (the seat's own slip (b), fixed by a body edit); read the live bodies.

Spark: use the test-digest STANDARD (`2_Project_Files/local-model/digest/digest.py`, report at `0_Brain/reference/2026-11-12_spark-test-digest-harness/report.md`) on your whole-suite logs, raw logs kept; then the Spark shadow review (`2_Project_Files/local-model/gate/spark_gate.sh` / `spark_review.py` with `--pr-body-file`), one request at a time. Record recall/false positives against your findings.

OUTPUT: `verdict.md` in THIS folder. First line: 'PR 2203: <GO / GO WITH NOTES / NO GO> · PR 2206: <...> (heads 67baaef2f105 / 36c0b86b3dd0; tier 2)'. Findings G327-2203-N and G327-2206-N, graded. NOT TESTED. The Spark result. If your Write is refused, return the text in full.

Constraints: exactly gate 320's. Read-only on the project checkout (clone into `scratch/` in THIS folder for any write verb; installs only there with `--ignore-scripts`). No push, no comment, no ticket write, no merge, no mail. If DevMASTER drops, wait, re-read what you wrote, then resume.
