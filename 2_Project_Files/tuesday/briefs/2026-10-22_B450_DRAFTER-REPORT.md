# B450 drafter report (read-only drafter for Tuesday), 2026-10-22 ~12:30 AEDT

Brief: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-22_B450_SEAT-F1_mps-main-red-feedback-ticket-test.md` (cloned from B446). Fences held: `gh api` GETs under the project's `.gh-config` (exists, project account active), one `ls-remote`, no git write, no fetch, no HTTP to an app host, no Jira, no `decision_queue.sh`. Scratch copies of three main files are in the session scratchpad only.

## Facts (MEASURED unless marked)
- `main` = f5b6f5a7 at 12:04; 0 open PRs; no `b444*`, `b445*`, `b446*`, `b450*` branch on origin yet.
- Run 39514401396 (`ci`, push, attempt 1) failure; job `dotnet` failed at the `dotnet test` step (23:21:42 to 23:24:37Z); `package` skipped; `web` and `python` green. The sibling run 39514401121 and the previous commit's `ci` run are success. Test counts and the failing text are RELAYED from BACKLOG `[B406-MAIN-RED]` and B406 STATUS:50 (the drafter did not read the log).
- Prior work: `[B100-1]` (attempt 2 re-run green, nobody fixed), B160 STATUS:32 (seen again, log kept in the B160 evidence folder), `[B340-B318-C1]` (17 of 31 filtered mutant runs red; class alone 3 of 3 green), `[B406-MAIN-RED]`. All four have the same signature (`pending`, `attempts 1`, `TIMEOUT`). Each seat deferred it as "not my file"; none owned it; ticketing it is "not ruled".

## Cause (CODE READ only, NOT run, UNMEASURED as behaviour)
In `FeedbackTickets.cs` `AttemptAsync`, `Save(failed)` (line 301, writes `TIMEOUT`, which the test polls) runs BEFORE `Schedule` (lines 305/309-310, `due = clock + 1 min`). The test (`FeedbackTicketTests.cs`, failing line 191) waits for `TIMEOUT`, then does ONE `Clock.Now += 2 min`. If that jump lands between the two statements, `Schedule` reads the jumped clock, `due = now + 3 min`, the fake clock stands still, and the second wait times out at 15 s with exactly the reported state. Test-side race, not a product defect, in the drafter's reading. The same one-shot jump is at line 172 (`A_500_then_a_201_after_the_first_backoff_...`); the safe form already exists at line 216 (`WaitForTicket(..., tick: ...)`).
- Expected fix: use the existing `tick` parameter at the two one-shot jumps (test-only, no timeout change). No edit to `FeedbackApiTests.cs` is needed (`WaitForTicket` lives there, is shared by 16 call sites and B446's tests, and is NOT in the partition).
- Red proof designed: a scratch-only widener (`Task.Delay` between `Save` and `Schedule`) makes the race deterministic at base; the fixed file must be green under the same widener.

## Proposals
- Tier 2 (G2) if test-only; tier 1 (G1) if `FeedbackTickets.cs` changes (the seat STOPS before that).
- Routing row C2, Sonnet 5.5, pilot. Not C3: no auth or security design surface; the fix is mechanical in a unit test. Not local: P4 (Datasec).
- Pane `Datasec/MPS-F1`, branch `b450/feedback-ticket-test-main-red`, target READY 14:00, hard stop 15:00.

## Open questions for Tuesday
1. R-F1-2: allow 2 `nice -n 19` busy processes (under 10 min) for the under-load loop while other seats run heavy jobs? Default written: yes.
2. R-F1-5: the project `CLAUDE.md` says Friday merges after CodeQL; Tuesday's 2026-10-16 grant says Tuesday lands. The landing rule quoted: squash with head pinned (`--match-head-commit`).
3. `heavy-slot-1` was present at 12:0x (holder not opened); the seat reads holders at launch.
4. The brief says "Branch CI is read, never re-run": pushing the branch starts CI by itself; if that CI is red on this same test, the fix failed and READY is not claimed.
5. A ticket for the test class remains "not ruled" (B406 item 3(c)); the brief files none.
