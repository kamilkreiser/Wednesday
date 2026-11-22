# FOR RECORDS: OXPd 2 Sessions F13 test-race fix (kit B1912, WP1.5 follow-up), gate G2 round 1, reader B1918

Not repository text. For the next OXPd records pass (backlog, runbook, design notes); nothing here was written into
the project. No person is named.

## What lands

- ONE commit `ea72d921` on main `bf6b441e`, two test files only: `tests/Datasec.Suite.Sessions.Tests/Fakes.cs`
  (32 added, 2 removed) and `RefreshBoundCellTests.cs` (43 added, 16 removed). No file under `src/`; no package,
  lock, project, solution, workflow or build file. Totals 1578 -> 1579 (both legs); rules files 500 (unchanged);
  Ran 111, floor 111 (unchanged).
- Cause (diagnosis B1908, re-read by this gate at source): `main` `bf6b441e`'s push run 45001737294 was red on linux on
  F13 because F13's fake refresher handed out its two answers by ARRIVAL order; a preempted timed-out call let the live
  call take `late`, which the broker legally kept. The broker is right: `AcceptLocked` is reached only with
  `error is null` (`TokenBroker.cs:430-438`); a time-out sets `RefreshTimedOut` (`:403-406`) and hands the late call to
  `DisposeWhenDone` (`:508-527`).
- The fix: F13's answers keyed on the call's index (`FakeRefresher.AnswerOfCall`); a new cell
  `F13_the_late_answer_is_never_kept_when_the_timed_out_call_answers_after_the_second_call` that holds call 1 at a
  test-only seam (`BeforeAnswer`, observed through `Answering`) until call 2 has started its answer: red against
  arrival-order answers on every run, green against index-keyed answers on every run; the fake records a call before
  it counts it, inside its one lock.

## From this gate

1. **Named survivor (as the kit said):** `mCountFirst` (the fake counting before it records) leaves the Sessions
   assembly green. Closed by reading the lock; no cell can hold a call at that point.
2. **Gate mutant mKeepLate (a real broker fault: the timed-out call's late answer accepted into the held grant
   instead of disposed) is caught by BOTH F13 cells**, and by F11 and F05 late: Sessions assembly `Total: 75, Errors:
   0, Failed: 4`. The index keying does not hide this fault.
3. **Ordering not covered by any cell (test gap, Minor, the code is right by reading):** in both F13 cells the late
   answer arrives while call 2 is still in flight (`firstRelease` is set before `secondRelease`). No cell lets the
   late answer arrive AFTER call 2's answer has been accepted. By reading, `DisposeWhenDone` disposes in either case.
   Backlog candidate: one more `LateAnswerAfterTimeOut` variant that releases `secondRelease` first.
4. **Seam scope:** `BeforeAnswer`, `AnswerOfCall` and `Answering` are set or read only in F13's shared scenario
   (`RefreshBoundCellTests.cs:133`, `:136`, `:160`, `:162`); every cell gets its own `Kit` and so its own
   `FakeRefresher` (`Support.cs:223`), so a seam cannot leak between cells.
5. **The runbook gains:** the xunit v3 native runner `-method` loop (`loop.sh`, pass only on `Total: 1, Errors: 0,
   Failed: 0`) as the way to prove a race cell red first; the deterministic seam pattern (hold a call, observe a
   counter) in place of sleeps.
6. **Still open (NOT DECIDED of the kit, unchanged):** whether the hosted linux leg shows the race again after the
   landing (UNMEASURED until main's next push run: step 6 of `landing.txt` reads it). Pre-existing and not this lane's:
   `release_guard.py` prints `GUARD-WARN: development CA deny-list holds 0 fingerprints (owed)` (seat X27's FOR
   TUESDAY; RELAYED, not re-run by this gate).
