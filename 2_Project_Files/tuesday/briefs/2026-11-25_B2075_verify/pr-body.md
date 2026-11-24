## What this changes

Two small fixes in `backend/server.js` (4 lines added, 1 removed), with two new test files and the suite counts.

**RD-1017: the data-source audit entries had no action.** `POST /api/setup/data-sources` and `DELETE /api/setup/data-sources/:id` write an audit entry named `AUDIT_ACTIONS.SETTINGS_CHANGE`, and the `AUDIT_ACTIONS` object had no such key. So each entry's action was `undefined`: the audit export's action filter (a strict comparison) could never return it, its CSV action column read empty, and the line written to the log read `[AUDIT] undefined`. The object now holds `SETTINGS_CHANGE: 'SETTINGS_CHANGE'`. The details of both entries are unchanged.

**This adds a new action tag.** From this change, `GET /api/admin/audit-log/export?action=SETTINGS_CHANGE` returns these entries, which no filter could return before. Entries already in the audit buffer from before the change keep an empty action (the field was never stored); only new entries carry the tag.

**RD-975: the business-hours report dated a job by when the row was stored.** `generateBusinessHoursReport` tried `created_at` first among its date fields. `created_at` is the time a row was stored, so a row stored at night (a seeded demo store, for example) was judged by that time and not by the time it was printed. The list now tries the job's own start fields first and `created_at` last, the order the file's other readers already use. A row with no readable start field is still judged by `created_at`.

**What the demo's answer now says.** On the demo seed's 1445 rows (every row carries only `Job_Start_Time_UTC`), the report now lists 587 jobs by 15 users outside business hours on a server whose clock is UTC, whatever time the store was seeded. Before, every row carried the seeding time, so the answer was all 1445 jobs (16 users) if seeded at night and nobody if seeded in the day. The report reads the server's local time, as before; on a server in another zone the count moves with the zone.

**Choices that are the coordinator's, not the product owner's:**
- The new key `SETTINGS_CHANGE` rather than pointing the two entries at an existing tag. It keeps the audit-field guard's census (`rd994`) true, which already counts `SETTINGS_CHANGE` as 2 calls.
- Two other readers of the same file that also try `created_at` first (the user-count report and the statistics reader) are left as they are.
- Three tickets from the same list were left out of this change: the off-hours check of the automatic insights (needs the chat route's pinned answers re-pinned and a decision), the risk-condition type checks (a measurement first), and one that is measure-only.

## The result (from the new test cells; 18 in two files)

- **Before (main `11149d3f`):** 9 of 18 cells fail: RD-1017 S1, S2, W1, W2, W3 and RD-975 B1, B2, B3, S1. The census reads one undefined name; the export filtered by `SETTINGS_CHANGE` returns 0 entries in JSON and in CSV after an add and a remove; a job started at 10:00 and stored at 23:00 is listed outside business hours, and one started at 23:00 and stored at 10:00 is not.
- **After:** all 18 pass. With only the product edits reverted, the same 9 fail.
- **Controls (green before and after):** both entries are written with their details, a filter for another tag returns neither, no export holds the stored secret, a viewer is refused the export (403), `created_at` alone still dates a row, an unreadable start field falls through to `created_at`, and a Sunday is outside hours.
- The 28 suites that name the audit tags, the export, the data-source routes or business hours: 509 of 509 pass, `rd798` and `rd994` among them.

## Files (4 files; two commits: the change, then the suite counts written by the project's own command)

- `backend/server.js`: 4 lines added, 1 removed.
- New: `__tests__/rd1017-data-source-audit-action-defined.test.js` (10 tests) and `__tests__/rd975-business-hours-report-reads-job-start-first.test.js` (8 tests).
- `scripts/verify-expected-counts.json`: 6323 / 398 to **6341 / 400**, by `npm run verify -- --maxWorkers=2 --update-counts`.

## Verification

- Full verify, run at both commits by the author and again on the merge with current main: `VERDICT: PASS`, 6341/6341 tests across 400 suites, `EADDRINUSE` 0.
- Local CodeQL (javascript-security-extended), main against head: NEW 0, KEPT 0, `rc 0 PASS`.
- gitleaks over the whole diff and the commit messages: no leaks found. The control fired.

## Not in this change (named)

- A start field that is not a string (a number or a date object) makes the whole report return its error sentence, because the loop calls `.trim()` on it. Measured at the head; before this change such a row was dated by `created_at` first and never reached the field. No store in the repository produces one (Log Analytics rows carry ISO strings, the SQLite column is text).
- A start field that is a bare word or number (`"1"`, `"2026"`, `"Print Job 1"`) is accepted as a date by the JavaScript parser and now dates the row at midnight in the year it names; a date-only start (`2026-11-23`) reads as midnight UTC. Neither shape is written by a store in the repository.
- The two other readers that try `created_at` first, so the chat answers of "who printed in the last day" and "who printed outside business hours" can still disagree on a row whose two times differ.
- Not tested: a hosted instance, Linux, the winston log file's text and the audit buffer's disk file on a real server (both read from the lifted function only), Log Analytics rows against a real workspace, and the hosted Build and CodeQL on the merge commit.

## Deploy

None. Merging starts a `Deploy demo` run, because `backend/**`, `__tests__/**` and `scripts/**` are not in its `paths-ignore`. Both of its jobs require `vars.CI_DEPLOY_ENABLED == 'true'`, and the deploy job also needs approval from a required reviewer on the `demo` environment. The last 20 runs of the workflow all read skipped.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
