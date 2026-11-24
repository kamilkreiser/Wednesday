# FOR-RECORDS: RD-1017, RD-975 (records pass, after the landing); RD-577 records-only; RD-974 the next lane

Fill in `<N>` (the PR) and `<M>` (its merge commit) after the landing. Take the Deploy demo line from landing.txt step 4.

Jira GET at the gate (07:5x AEDT 25 Nov): RD-1017 To Do (Bug, labels records-pass-1120,security, 0 comments); RD-975 To Do (Bug, label b1363-2026-11-07, 0 comments); RD-577 To Do (2 comments, the second a 2026-11-11 ruling record); RD-974 To Do (0 comments); RD-518 Release Ready.

## RD-1017: result comment

Landed by pull request <N>, merge commit <M>: a merge commit of the reviewed head `9d4ddb7f`. A is `40e8ffc0` (the change), K is `9d4ddb7f` (the counts).

- **Change.** `AUDIT_ACTIONS` in `backend/server.js` gains the key `SETTINGS_CHANGE: 'SETTINGS_CHANGE'`, after `ROLE_CHANGED`. The two writers (`POST /api/setup/data-sources`, `DELETE /api/setup/data-sources/:id`) already named it; their entries now carry the action. Details unchanged. 2 lines added.
- **Whose call.** The new key, rather than pointing the two entries at `CONFIG_CHANGE`, was the coordinator's default (the ticket offered both). The new key keeps the rd994 census (`SETTINGS_CHANGE` 2, row R12) true. It is not a product-owner ruling.
- **This is a new tag for filters.** An export filtered by `SETTINGS_CHANGE` now returns these entries; no filter could return them before. Entries written before the change keep no action (the field was `undefined` and is not stored or exported); nothing back-fills them.
- **Measured (new file `rd1017-...`, 10 cells).** At main `11149d3f` 5 cells red: S1, S2, W1, W2, W3 (the census read one undefined name; the filtered export returned 0 entries in JSON and CSV after an add and a remove). At the head 10 of 10 green. With only the product edit reverted the same 5 red. The gate measured this in its own trees. Controls green both sides: both entries written with details, another tag returns neither, no export holds the stored secret (also 0 in the gate's own probe), a viewer is refused 403.
- **Gate probes (real server, own cells):** a failed add (400), a viewer's add (403, writes `REQUEST_DENIED`, no `SETTINGS_CHANGE`) and a delete of a missing id (404) write no `SETTINGS_CHANGE` entry; two adds and one delete write three; every `SETTINGS_CHANGE` row's details keys are exactly `action, authMode, dataSourceId, name` (add) and `action, dataSourceId, name` (remove); 0 rows with an undefined action in the export; a lower-case filter (`settings_change`) returns 0 (the filter is case-sensitive, as before); the line the log writes now reads `[AUDIT] SETTINGS_CHANGE` and the entry survives a JSON round trip of the buffer (lifted function; the disk file on a real server not run).
- **Verification.** Full verify `VERDICT: PASS`, 6341 tests in 400 suites (the seat at both commits; the gate on the merge with main `4d8713e5`). Local CodeQL NEW 0, KEPT 0. gitleaks none. Gate B2075: <VERDICT line>.
- **Not tested.** A hosted instance, the open first-run window, the audit buffer's disk file on a real server, Linux, the writers that pass a string literal to `auditLog` (`DATA_SOURCE_ALLOWLIST_REJECT` x3, `DATA_SOURCE_ENDPOINT_REJECT` x1: not `AUDIT_ACTIONS` reads, outside the census cell).
- **Deploy.** None. Deploy demo run for <M>: <conclusions, from landing.txt step 4>.
- **Move.** To the column the records pass uses for a landed lane awaiting acceptance (RD-1036 and RD-1021 used the same).

## RD-975: result comment

Landed by pull request <N>, merge commit <M>, the same two commits.

- **Change.** In `generateBusinessHoursReport` the date-field list moves `created_at` from first to last. 3 lines changed (one comment line, one list). Order now `Job_Start_Time, Job_Start_Time_UTC, Job_Start_Time_Local, Timestamp, Date, jobInfo__jobStartedTimestamp__time, jobInfo__jobDoneTimestamp__time, TimeGenerated [UTC], Job_Completed_Time_UTC, created_at`.
- **Measured (new file `rd975-...`, 8 cells).** At `11149d3f` 4 red: B1, B2, B3, S1 (a job started 10:00 and stored 23:00 listed outside; started 23:00 and stored 10:00 not listed; a seeded row judged by its stored time; the list began with `created_at`). At the head 8 of 8 green; reverted product the same 4 red. Controls green: `created_at` alone still dates a row, an unreadable start falls through, agreeing times and a Sunday read as before, no error logged.
- **The demo's answer (gate measurement, `probe-hours-table.txt`).** The 1445 seeded rows carry `Job_Start_Time_UTC` only. Before: every row had the seeding time, so the report said 1445 jobs by 16 users outside hours if the store was seeded at night, and nobody if seeded in the day. After, on a server clock in UTC: 587 jobs by 15 users outside hours, whatever the seeding time (an independent count over the CSV agrees: 587 and 15). The report reads the server's local time as before; the same rows on a server at UTC+11 read 1381 jobs by 16 users.
- **Limits found by the gate (neither has a known producer in the repository; both new at the head):**
  1. A non-string start field (number, Date object, object) makes the whole report return its error sentence (`Business hours analysis error: TypeError: log[field].trim is not a function`), because the loop calls `.trim()` before it tests the type. At `11149d3f` the same row read fine, since `created_at` parsed first. Log Analytics rows carry ISO strings (`getDateTime`, `row.TimeGenerated`) and the SQLite column is TEXT, so none was found.
  2. A start field the JavaScript parser accepts as a date without being one (`"1"`, `"2026"`, `"Print Job 1"`) now dates the row at midnight of year 2000/2001/2026; a date-only start (`2026-11-23`) reads as midnight UTC, so on a UTC server a weekday row with a good `created_at` is now listed outside hours. Neither was visible before, because `created_at` came first.
  Candidate: a `typeof` guard and a stricter date test in a later lane (RD-974's lane touches the same function family; fold it in or file it).
- **Other readers left (Q-5).** `getStatsFromLogs` (`created_at` first, list at line 6123 of the merged file) and `generateUserCountReport` (line 13413) still try `created_at` first, so two chat answers can disagree on a row whose two times differ. The ticket's "13411 and 13445" are, at main `fab4fa41`, the same function's list and its body; the records pass should name 6123 and 13413 (numbers at the merge).
- **Verification, deploy, move:** as RD-1017.

## RD-577: records-only (not built here)

Comment and move only, if the records pass agrees; no code. The sweep says fixed on main: the status readout carries the RD-518 change (a comment at `backend/server.js` ~18584 says it read an unset `KEY_VAULT_NAME` and now reports `not_configured` correctly) and RD-518 reads Release Ready. RD-577's own comment 1 says it must not ship ahead of RD-518, and its comment 2 (2026-11-11) records a ruling that is not a move. The records pass should re-read RD-518's state before moving RD-577.

## RD-974: the next lane (not built here)

The off-hours check of `generateAutomaticInsights` (`new Date(job.Job_Start_Time || Date.now())`). Needs `__tests__/rd798-log-injection-chat-and-learning.test.js` IN ITS PARTITION: the cells `C-BODY-HOURS LIVE` and `C-BODY-HOURS OUT 190` pin the clock-dependent paragraph the ticket calls the bug and must be re-pinned; and a design choice (does `Job_Start_Time_UTC` count as a start time for the check, since the seeded rows carry only that field). Its partition must also name `backend/server.js` lines near 20292 and 20397 only, and must not share a path with an open lane. Fold in, as a candidate, the two RD-975 limits above (they are in a different function: a separate decision).
