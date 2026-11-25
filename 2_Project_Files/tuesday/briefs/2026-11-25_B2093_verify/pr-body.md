## What this changes

`generateAutomaticInsights` (the function behind `GET /api/key-insights` and three chat paths) read a job's time as `new Date(job.Job_Start_Time || Date.now())` in two places: the per-user day and week buckets, and the check for unusual print times (before 6 or after 22, more than 10 jobs raises the red `UNUSUAL_TIME_PATTERN` item). The stores fill `Job_Start_Time_UTC` (the Log Analytics parsers, the demo seed and the local store), not `Job_Start_Time`, so every real or seeded job took the time of the read: run at night, every job counted as off-hours; run by day, the item did not show, and the same jobs were put in today's day and week bucket.

Both places now read the job's own start time through one small helper, `jobStartDate(job)`: `Job_Start_Time`, then `Job_Start_Time_UTC`; null when neither is present or parses. A job with no start time:

- is not counted in the unusual-time item;
- is in no day or week bucket and sets no first or last seen time;
- **still counts** in the user's jobs, sheets and pixel totals, the top-user and scan/print lists, and the summary (once, not twice, not zero).

A job whose time does not parse no longer fails the whole insights run (it returned the "Failed to generate insights" answer).

## Behaviour change (read this before deploying)

- **The demo's off-hours item changes once it is deployed.** The seeded demo rows carry only `Job_Start_Time_UTC` (1445 rows, all dated). Before: the item read "1445 jobs during off-hours" when the check ran at night and did not appear by day. After: the same item at every hour of the day, with the count of seed rows whose own start hour in the server's zone is before 6 or after 22: 60 in a UTC server, 676 in Australia/Sydney (measured by a program over the seed file). The hosted demo's zone was not measured; the repository's Dockerfile sets none.
- A user with only undated jobs has `firstSeen` and `lastSeen` of null in `topUsers` (a Date before). No page script reads them; the chat prompts print them as JSON.
- The hour is the server's local hour of the start time (`getHours()`), as before for `Job_Start_Time`. The item's count therefore depends on the server's time zone.

## Choices that are the coordinator's

- The field order: `Job_Start_Time` first, then `Job_Start_Time_UTC` (the order the business-hours report took in RD-975).
- The existing chat test `__tests__/rd798-log-injection-chat-and-learning.test.js` is re-pinned: route 190 no longer reads the clock, so its child process runs in UTC, the off-hours paragraph shows in both clock states, and three cells say what they now pin.
- An undated job stays in the totals and out of the buckets.
- The rows this ticket does not list are left alone (next section).

## Not in this change (disclosed)

- **The `hour > 22` test.** The item's text says "10 PM - 6 AM", the test counts hours 0 to 5 and 23, so a job started between 22:00 and 22:59 is not counted (9 of the 1445 seed rows in UTC). Left alone.
- **Other readers of the bare field and other time readers** in `backend/server.js` (for example the users route that reads `Job_Start_Time || TimeGenerated`, the two readers that read `Job_Start_Time || jobStartTime || TimeGenerated`, and the chat helpers that pick the first date field present). Their neighbours are RD-695 and RD-688.
- **A field order that stops at the first present value.** A job whose `Job_Start_Time` is present but not a date is left out even if its `Job_Start_Time_UTC` parses (the field is read first-present, as `_jobDate` does).
- **Frame note.** `backend/print-glossary*.json` holds KQL that names a Log Analytics column `Job_Start_Time` (`HpamPrinterLogs_StatisticsJobData_CL`). The statement "no store fills `Job_Start_Time`" is about the writers in this repository (the four Log Analytics parsers, the seed, the local store), which fill only `Job_Start_Time_UTC`. Whether any path hands raw Log Analytics columns to this function was not measured; the helper reads `Job_Start_Time` first, so the behaviour holds either way.
- Not tested: the HTTP route and the chat routes that call the function, a hosted instance and its time zone, Log Analytics rows, a number or a Date object as a start field, Linux, a real browser.

## The result (20 new cells; one test file re-pinned)

- Before (main): 14 of the 20 new cells fail, and 2 of the 65 cells of the re-pinned file (the two route-190 answers); a third cell of that file reads the clock and is red or green by the hour. After: all pass. With only the product edit and the re-pins reverted, the same 14 fail (names compared by program).
- Full verify of the merge of this branch into main (`d473243d`): ``VERDICT: PASS`, 6449 tests in 404 suites, the pair the counts file carries`.
- Local CodeQL (javascript), main against head: NEW 0, KEPT 0.
- gitleaks over the diff and the commit messages: no leaks found; the control fired.

## Files

- `backend/server.js` (29 lines added, 14 removed: the two readers and the new helper).
- `__tests__/rd798-log-injection-chat-and-learning.test.js` (re-pinned: 19 added, 16 removed).
- New: `__tests__/rd974-undated-job-is-not-off-hours.test.js` (20 cells).
- `scripts/verify-expected-counts.json`: 6429 / 403 to **6449 / 404**, by `npm run verify -- --maxWorkers=2 --update-counts` (second commit).

## Deploy

None. Merging starts a `Deploy demo` run, because `backend/**` and `__tests__/**` are not in its `paths-ignore`. Both of its jobs require `vars.CI_DEPLOY_ENABLED == 'true'` (the repository has no Actions variables) and the deploy job also needs approval from a required reviewer on the `demo` environment. The last runs of the workflow all read skipped.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
