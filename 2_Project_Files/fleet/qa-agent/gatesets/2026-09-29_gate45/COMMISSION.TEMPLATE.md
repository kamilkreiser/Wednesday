# gate45 COMMISSION — two Secuura PRs from Seat B 45th (T1: #1348 KS-1054; T2: #1347 KS-1374 ROUND 2 OF 2), round 45

Filled by fill_gate45.py at {{FILLED_AT}} from pins_gate45.json (measured {{MEASURED_AT}}). Wednesday's commission to the drafter, 2026-09-29, restated requirement by requirement; the gate prompt carries each by name and the launcher refuses a prompt missing any of the {{N_KW}} keywords.

## The PRs (merge order = this table's order: T1 first)
{{PIN_TABLE}}

- develop `{{DEVELOP}}` (tree `{{DEVELOP_TREE}}`) = #1346's squash on `{{OLD_BASE_SHORT}}`. #1348's parent IS develop. #1347 (round 2 head, a fast-forward on round 1 `{{R1}}`) sits on `{{OLD_BASE}}`, **{{BEHIND_1347}} commit behind**; the move touches none of its six paths (pin (C)); it merges cleanly AS-IS (pin (E)/(F)).
- {{MODE_LINE}}
- Author AND merger: {{MERGE_SEAT}}. Pane `QA/Secuura-batch1348`. Report dir `{{REPORT}}`.

## The rulings (the gate checks each diff against its ruling)
- #1348 KS-1054 (gate44 N-1346-1) — Kam option (a), card `secuura-ks1054-f9282-migration-failure-visibility`: "Keep serving, flag it on /health — The migration run returns its failed count. /health reports it, so the deploy scripts' existing /health checks (deploy-all.sh:281, deploy.sh:823) see it and the deploy reads as failed. The running service is not stopped." The deploy must read as failed on failed migrations via BOTH scripts; deploy-all.sh does since #1346, deploy.sh is this PR. A DEPLOY-PATH change: TIER 1. Named NOT fixed by the author: N-1346-2 / -3 / -4 (pass-line wording for ran:false / absent / empty / non-JSON; python3 missing fails open) — the gate GRADES whether leaving them is acceptable, it does not require them.
- #1347 KS-1374 ROUND 2 OF 2 — Kam 16:17:55 / 16:18:57 (Tuesday ROUTED): LOCAL stacks raised, demo and production unchanged, one limiter test at the demo's limit. Round 2 answers gate44: N-1347-2 (`.env.example` back to 2000; only `env.example` at 10000), N-1347-1 (the Akto harness paces by the SCANNED target; `AKTO_PLATFORM_REQUESTS_PER_MINUTE` override), N-1347-3 (floor at 1), N-1347-6 (re-label), N-1347-4 (compose comment; CI stacks IN SCOPE per Wednesday 10:36Z). TIER 2. **THE LAST ROUND: a NO GO ships nothing.**

## What the gate must check
1. **Red at base, green at head, a tamper that reds for the RIGHT reason** — per PR; unique anchor, sha256-asserted restore. #1348: E1 red with deploy.sh at develop (13/1, E1 alone), 14/0 at head; **E2 re-proved (a clean deploy returns 0) on the extracted block AND on the real function**; a tamper making the return UNCONDITIONAL must red E2; `return 0` (the drafter measured E1 stays green: the block runs as a script, where a top-level `return N` exits 1 for every N); `mktemp -t` without X's on CI's GNU mktemp. #1347: red-first against ROUND 1 for N-1347-1 and N-1347-3; a non-local target with a raised local .env paces <= 1500 and a local one 7500, through the real loader; tampers on R1/R5/R6/R9. (RED-AT-BASE, GREEN-AT-HEAD, TAMPER-RIGHT-REASON, TAMPER-UNIQUE-ANCHOR, RESTORE-SHA256, E1-RED-AT-BASE-1348, E2-CLEAN-DEPLOY-RETURNS-0-1348, TAMPER-UNCONDITIONAL-RETURN-1348, TAMPER-RETURN-0-1348, E-DRIVER-TOPLEVEL-RETURN-1348, MKTEMP-GNU-1348, RED-FIRST-ROUND1-N-1347-1, RED-FIRST-ROUND1-N-1347-3, NONLOCAL-RAISED-ENV-LE-1500-1347, LOCAL-7500-1347, LOCAL-HOST-FORMS-1347, OVERRIDE-APP-URL-1347, DOTENV-ORDER-TARGET-1347, OVERRIDE-NAME-ABSENT-1347)
2. **Every gate44 finding on #1347 as a row** (closed / narrowed / open) with evidence. (GATE44-FINDINGS-ROWS-1347, CI-TEST-ASSUMES-2000-1347, COMPOSE-COMMENT-1347, ENV-EXAMPLE-2000-1347)
3. **Whole suites before / after, with tsc where present** — the shell suite, api-gateway, the akto unit suite (its OWN `npm ci`): develop, round 1 (akto), each head, END; no new red. (WHOLE-SUITE-BEFORE-AFTER, NO-NEW-RED, TSC-BEFORE-AFTER, SUITES-AT-END, AKTO-OWN-NPM-CI-1347)
4. **Every test anywhere referencing a changed path** — `git grep` over Blockchain/** and systemTest/**, LISTED, classified and RUN. The drafter's census: {{CENSUS_N}} files (docker-compose.yml is now a changed path). (CENSUS-TESTS-RUN, CENSUS-LISTED)
5. **Key-scan subjects** (own key only, no `(#n)`, landed <= 92) that are **TRUE of the diff**, and **bodies** `Refs <own key>`, no closing keyword. #1347's live title predates round 2; the declared subject is the drafter's PROPOSAL for the gate to rule. (SUBJECT-KEY-SCAN, SUBJECT-LANDS-AT, SUBJECT-TRUE-OF-DIFF, REFS-OWN-KEY, NO-CLOSING-KEYWORD)
6. **#1348 on the deploy path, with stubs only** — `deploy.sh verify`, `services`/`full`, every call site under `set -e`, the ERR trap line, the four ERRORS conditions (not only migrations), both scripts side by side, the named-not-fixed Minors graded. (DEPLOY-SH-VERIFY-DRIVEN-1348, DEPLOY-SERVICES-TAIL-1348, SET-E-CALL-SITES-1348, ERR-TRAP-LINE-1348, BEHAVIOUR-WIDER-THAN-MIGRATIONS-1348, RULING-A-BOTH-SCRIPTS-1348, NAMED-NOT-FIXED-1348, MODE-100755-RECORDED-1348)
7. **Merge order and END** — 1348 then 1347, each squash on the previous tip; END_TREE `{{END_TREE}}`; overlap measured; #1347 merges cleanly over the #1346 squash. (END-TREE, MERGE-ORDER-T1-FIRST, OVERLAP-MEASURED, CLEAN-MERGE-1347-OVER-8BA2)
8. **The SECOND correction on KS-1374 (comment dc9212b5), every factual line against the head; the stale round-1 PR body; the last-round cap.** (SECOND-CORRECTION-LINES-1347, PR-BODY-STALE-1347, ROUND-2-OF-2-CAP-1347)
9. **The report's `## MERGE ADDENDUM` is the LAST thing written; nothing goes into report.md after the verdict mail**, whose body carries the report's sha256. (REPORT-HASH-LAST) Plus DISK-ENOSPC and TIERING.

## GO
The GO string, as the GO mail's SUBJECT: `{{GO}}` — {{MERGE_SEAT}} merges. Verdict mail subject: `{{VERDICT_SUBJECT}}`.

## The drafter's predictions (to be re-derived by the gate, never adopted)
- pin_gate45.py -> pin_1.out: {{OVERLAP_LINE}} END_TREE `{{END_TREE}}`; reverse order `{{REVERSE_END}}`.
- testrefs_gate45.py -> testrefs_1.out: {{CENSUS_N}} test files — {{CENSUS_LIST}}
- keyscan_gate45.py -> keyscan_1.out: {{KEYSCAN}}
- linear_read_gate45.py -> linear_read_1.out: {{LINEAR_LINE}}
- drafter_return_probe.out: the extracted summary block run as a script exits rc 1 with ERRORS=2 for `return 1`, `return 0` and `return 7` alike; as a function body, `return 0` gives rc 0 (the control).
