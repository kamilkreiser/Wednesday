# gate46 COMMISSION — ONE Secuura PR: #1348 KS-1054 ROUND 2 OF 2 (T1), author Seat B 45th, merger {{MERGE_SEAT}}, round 46

Filled by fill_gate46.py at {{FILLED_AT}} from pins_gate46.json (measured {{MEASURED_AT}}). Wednesday's commission to the drafter, 2026-09-29, restated requirement by requirement; the gate prompt carries each by name and the launcher refuses a prompt missing any of the {{N_KW}} keywords.

## The PR
{{PIN_TABLE}}

- develop `{{DEVELOP}}` (tree `{{DEVELOP_TREE}}`) = #1347's squash on `{{OLD_BASE_SHORT}}`. #1348 (round 2 head, a fast-forward on round 1 `{{R1}}`) sits on `{{OLD_BASE}}`, **{{BEHIND}} commit behind**; the move touches none of its two paths (pin (C)); it merges cleanly AS-IS (pin (E)).
- {{R2_LINE}}
- {{MODE_LINE}}
- Author Seat B 45th (wrapped); merger {{MERGE_SEAT}}. Pane `QA/Secuura-batch1348r2`. Report dir `{{REPORT}}`.

## The ruling and the round
- #1348 KS-1054 (gate44 N-1346-1) — Kam option (a), card `secuura-ks1054-f9282-migration-failure-visibility`: the deploy reads as failed on failed migrations via BOTH scripts; the running service is not stopped. A DEPLOY-PATH change: TIER 1.
- gate45 measured the deploy.sh fix CORRECT and NO GO'd round 1 on N-1348-1 (`mktemp -t` with no X's: GNU refuses, 13/1 on Debian) and N-1348-2 (E1 blind to the return value: a `return 1` -> `return 0` tamper kept 14/0). Round 2 claims both fixed in the test file only.
- N-1348-3 (deploy.sh now also aborts on a portal nginx page, a failed demo login, an empty/non-JSON /health) is in scope, already told to Kam. N-1346-2/-3/-4 are named NOT fixed (a later design item): not required.
- **ROUND 2 OF 2: a NO GO ships nothing on this class and goes to Kam as a card.**

## What the gate must check
1. **N-1348-1 and N-1348-2 re-checked as rows with evidence**; the ks1054 suite on BOTH macOS (bash 3.2 / BSD) and a GNU/Debian image (python:3.12-slim; ubuntu:24.04 for the mktemp reading); red at base (E1 alone) on both; the `return 1` -> `return 0` tamper MUST red E1 and an unconditional-return tamper MUST red E2, on both. (N-1348-1-RECHECK, N-1348-2-RECHECK, SUITE-MACOS-BASH32, SUITE-GNU-DEBIAN, MKTEMP-GNU-1348, E1-RED-AT-BASE-1348, TAMPER-RETURN-0-REDS-E1, TAMPER-UNCONDITIONAL-REDS-E2, E2-CLEAN-DEPLOY-RETURNS-0-1348, RED-AT-BASE, GREEN-AT-HEAD, TAMPER-RIGHT-REASON, TAMPER-UNIQUE-ANCHOR, RESTORE-SHA256)
2. **The drafter's doubts**: E1 passes on any non-zero rc; the test :124 comment names a `TAMPER_RETURN_ZERO` arm the file does not carry; `return 1` occurs twice in deploy.sh; the pre-existing arms; modes; the round-2 delta is test-only and deploy.sh is byte-equal to round 1. (E1-ANY-NONZERO-1348, TAMPER-ARM-COMMENT-1348, PRE-EXISTING-ARMS-1348, MODE-100755-RECORDED-1348, ROUND2-DELTA-TEST-ONLY, PRODUCT-UNCHANGED-SINCE-G45)
3. **Everything that held in gate45 still holds**: N-1348-1…-5 as rows; the PR body's round-2 section; the KS-1054 raise comment. (GATE45-HELD-STILL-HOLDS, GATE45-FINDINGS-ROWS-1348, PR-BODY-ROUND2-1348, RAISE-COMMENT-B82BEBB3)
4. **deploy.sh on the deploy path, stubs only, re-driven at the round-2 head beside gate45's figures.** (DEPLOY-SH-VERIFY-DRIVEN-1348, DEPLOY-SERVICES-TAIL-1348, SET-E-CALL-SITES-1348, ERR-TRAP-LINE-1348, BEHAVIOUR-WIDER-THAN-MIGRATIONS-1348, RULING-A-BOTH-SCRIPTS-1348, NAMED-NOT-FIXED-1348)
5. **Whole suites before / after**: develop, head, END; macOS and GNU. (WHOLE-SUITE-BEFORE-AFTER, NO-NEW-RED, SUITES-AT-END)
6. **Every test referencing a changed path**, listed, classified, run. The drafter's census: {{CENSUS_N}} file(s). (CENSUS-TESTS-RUN, CENSUS-LISTED)
7. **Key-scan the subject** (KS-1054 only, no `(#n)`, landed <= 92) **TRUE of the diff**; body `Refs KS-1054`, no closing keyword. (SUBJECT-KEY-SCAN, SUBJECT-LANDS-AT, SUBJECT-TRUE-OF-DIFF, REFS-OWN-KEY, NO-CLOSING-KEYWORD)
8. **END**: #1348 over develop `{{DEVELOP_SHORT}}` (over #1347's squash), END_TREE `{{END_TREE}}`, overlap with the move measured. (END-TREE, CLEAN-MERGE-1348-OVER-8C81, OVERLAP-MEASURED)
9. **The cap**: ROUND-2-OF-2-CAP-1348. Plus DISK-ENOSPC, TIERING, and **REPORT-HASH-LAST**: the report's `## MERGE ADDENDUM` is the LAST thing written; nothing goes into report.md after the verdict mail, whose body carries the report's sha256.

## GO
The GO string, as the GO mail's SUBJECT: `{{GO}}` — {{MERGE_SEAT}} (the successor) merges. Verdict mail subject: `{{VERDICT_SUBJECT}}`.

## The drafter's predictions (to be re-derived by the gate, never adopted)
- pin_gate46.py -> pin_1.out: #1348 over develop clean; END_TREE `{{END_TREE}}`.
- testrefs_gate46.py -> testrefs_1.out: {{CENSUS_N}} test file(s) — {{CENSUS_LIST}}
- keyscan_gate46.py -> keyscan_1.out: {{KEYSCAN}}
- linear_read_gate46.py -> linear_read_1.out: {{LINEAR_LINE}}
- drafter_return_probe.out: the real summary block driven as the round-2 test drives it (function wrapper): rc == the return value (1/0/7) on bash 3.2 and bash 5.2; unconditional tamper rc 1 at ERRORS=0; the round-2 mktemp template works on GNU coreutils 9.7 where the round-1 form is refused.
