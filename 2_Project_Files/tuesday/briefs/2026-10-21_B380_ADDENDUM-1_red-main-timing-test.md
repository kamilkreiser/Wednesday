From Tuesday (Kam's Datasec coordinator seat), Datasec / HPSM-POC. ADDENDUM-1 to B380 (SEAT-D12). Read it now; everything in your brief stands, this ADDS one measurement.

## What changed since your stamp (MEASURED by Tuesday 2026-10-21 08:0x AEDT, `gh api` under this project's GH_CONFIG_DIR)
- The push `ci` run **39491761682** on main `54fbceac` ended **failure**. The only failing test is in the SQL Server shard `api on SQL Server (api-other-and-feedback)`: `RequestTimingLogTests.A_request_that_writes_its_caller_row_names_the_lookup_and_the_write_inside_the_caller_stage(write: "refresh")`, `Assert.InRange` 900-1250, actual 1384 ms, at `RequestTimingLogTests.cs:269` (RELAYED from the B378 records seat's read of the job log; Tuesday read the run's conclusion).
- Main push runs, newest 15 (`actions/runs?branch=main&event=push`): 13 success, 2 failure (this one, and `ce40ce07` on 2026-10-13, cause not read). PR #167 changed one unrelated test file. Reading: a timing window on a loaded runner. **Not proven.**

## Why it is yours to measure (not to fix)
Your commit 3 (HPSMPOC-232) changes the start-up round so the `app_user` write path runs in a rolled-back transaction. That is the same caller write stage this test times (`write: "refresh"`). Your change could widen the flake, narrow it, or leave it alone, and nobody knows which.

## The one measurement (add to STATUS under MEASUREMENT, -232)
1. Read `api/tests/HpsmPoc.Api.Tests/**/RequestTimingLogTests.cs` around `:269` (find the file; quote the window and how the duration is produced).
2. Run ONLY that test (the `write: "refresh"` case, filtered) **10 times at base** and **10 times at your -232 head**, on SQLite locally, `uptime` per run, load1 < 8 per your standing line 11. Record each duration and pass/fail.
3. Say plainly whether your change moves the measured duration and whether the window can fail locally.

## Holds (unchanged, restated because the file is tempting)
- **Do NOT edit `RequestTimingLogTests.cs`.** It is not in "Yours". If you think the window is wrong, write the evidence and a proposed fix-shape in FOR TUESDAY; Tuesday files the ticket.
- **Never re-run a CI job** (a re-run is a write and is never a clearance).
- If your 10+10 runs show your change makes the test fail locally, that is a STOP for commit 3 (`STOPPED: NEEDS TUESDAY`, one question, branch state named).

Last line as your brief says.
