GATE B2075: GO WITH FINDINGS
@ 9d4ddb7 on main 4d8713e

Gate G2 (Sonnet), round 1 of 2, lane NX-S2 (RD-1017 + RD-975). Re-commissioned by Tuesday s326; the first gate agent died before writing this. No authorization path found (the change adds an audit tag and reorders a date-field list), so G2 stands. Re-measured 08:0x AEDT 25 Nov by gh api -X GET: main = 4d8713e5353d589a8680d328e2e00a69b8ea7480 (not moved), branch = 9d4ddb7f52ad2f23777d8b662abce0cbd1662b9f.

## Measured
- Red-first at BASE 11149d3f (rf.log/rf.json): 9 failed, 9 passed of 18 (RD-1017 S1 S2 W1 W2 W3; RD-975 B1 B2 B3 S1).
- Head: new 18 of 18 green; the 28 suites naming the audit tags/export/data sources/business hours: 509 of 509 green.
- Red-proof (product blob restored to 6d8e5139, then put back to a7426b07): 9 failed, 9 passed; the failing names are IDENTICAL to the rf set (compared by program over rf.json and redproof.json: 9 = 9, equal).
- Probes (audit shapes, hours in machine tz and in UTC) rc 0; tables in probe-hours-table.txt, probe-audit.json.
- Merge tree = merge commit 24bd05df85f62210c659d61c339a101be20d3efa (head 9d4ddb7f + main 4d8713e5), built in scratch, clean. Full verify under the NexusAI jest lock: VERDICT: PASS, 6341/6341 tests across 400 suites (jest exit 0), 0 FAIL lines, verify rc 0, lock-wrapper rc 0, 07:45:16-08:07:20. Matches the expected 6341/400.
- gitleaks: control first (planted fake key, `gitleaks dir`) rc 1 = fired; BASE..head (2 commits) rc 0, no leaks; the two real commit messages plus the five landing texts rc 0, no leaks.
- Reads: backend/server.js diff is exactly 4 added / 1 removed (key + comment; list reorder + comment); no other file of backend touched.

## Attack, RD-1017
- Every `AUDIT_ACTIONS.<name>` read is now a key (S1 census, 17 names; plus grep: the only two SETTINGS_CHANGE readers are lines 17369 and 17619, the two writers). No `Object.keys/values(AUDIT_ACTIONS)` enumeration exists in server.js, so no consumer changes what it counts; rd994 already expected `SETTINGS_CHANGE: 2` (row R12) and rd932/rd994 are in the 509 green.
- JSON and CSV export, filter, winston line (`[AUDIT] SETTINGS_CHANGE`), buffer JSON round trip: carried (wire cells W1-W3, gate probe). Secret never reaches an entry (C2: 0 in four outputs; details keys exactly action/authMode/dataSourceId/name and action/dataSourceId/name). Viewer 403.
- Three shapes outside the tested property (none is a defect of this change): (1) the audit buffer's on-disk file on a real server and the first-run open window of the setup routes (named NOT RUN by the seat); (2) the three string-literal `auditLog('DATA_SOURCE_*_REJECT')` writers, still outside the AUDIT_ACTIONS census and unchanged; (3) entries written before the change keep an undefined action and are not back-filled, so a SETTINGS_CHANGE filter shows only post-change history (disclosed in the PR body).

## Attack, RD-975
- Demo answer: seed rows carry Job_Start_Time_UTC only. Before: 1445 jobs/16 users or nobody depending on the seeding hour. After: 587 jobs/15 users on a UTC server (an independent CSV count agrees), 1381 jobs/16 users at UTC+11. Disclosed in PR body.
- Callers of generateBusinessHoursReport (server.js lines 8746, 9076, 9235, 9447, all pass allLogs through unchanged): no one asserts the old order; rd798 and the other chat tests are green in the merge verify.
- Log Analytics rows: Job_Start_Time_UTC is `new Date(val).toISOString()` or the raw TimeGenerated, always a string; a flat jobInfo row now dates by its start rather than created_at (probe: LA_row_jobInfo_flat changes, expected direction).

## Findings
1. MINOR, does not block. Non-string start field (number, Date, object) in a row now makes the whole report return its error sentence (`log[field].trim is not a function`), where at BASE created_at parsed first and masked it. Probes numeric_start_with_created_at, date_object_start. No producer in the repo (LA rows are ISO strings, SQLite column TEXT). Already disclosed in the PR body and FOR-RECORDS. Suggest a `typeof` guard in a later lane.
2. MINOR, does not block. Lenient-parser start values (`"1"`, `"2026"`, `"Print Job 1"`) now date the row at a fabricated midnight and a date-only start reads as midnight UTC (on a UTC server a weekday row with a good created_at is now listed outside hours). Previously hidden by created_at first. No producer in repo. Disclosed.
3. MINOR, does not block. Report still reads server-local time, so counts depend on server zone (587 vs 1381 for the same demo rows). Pre-existing, disclosed.
4. INFO. Two sibling readers (getStatsFromLogs, generateUserCountReport) still try created_at first; two chat answers can disagree on a row whose times differ. Left deliberately (Q-5); disclosed.
5. INFO. Not run by anyone: hosted CodeQL/Build on the merge commit (Tuesday reads it at the PR), Linux, real-server audit disk file. Landing text covers the hosted checks.
6. INFO. PR title/body carry Jira ids (RD-1017, RD-975) but no person's name and no coordinator card id; the key choice and left-out tickets are named as the coordinator's. Fine.
7. INFO (fixed by gate). landing.txt held VERIFY_RESULT_PLACEHOLDER; replaced with the measured merge-verify result. Other texts (pr-body, pr-title, commit-messages, FOR-RECORDS) checked against the commission and the measurements; no correction needed. FOR-RECORDS still holds the literal `<VERDICT line>` fill-in, to be completed at the records pass.

## Before landing (Tuesday)
Open the PR from landing.txt; re-measure main first (if it moved and touched backend/**, __tests__/**, scripts/**, package*.json, the lane goes back to a seat); wait for hosted checks with --min-checks 7; merge commit pinned to 9d4ddb7f; read the Deploy demo run (both jobs must read skipped; never approve). No Blocker, no Major.
