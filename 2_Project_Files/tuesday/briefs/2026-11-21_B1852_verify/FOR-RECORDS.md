# FOR RECORDS: the session and token broker lane, fix round (head e9095598 on 70c1fad5), reader B1852

What a records pass should file. None of it blocks the merge; none of it is decided by this reader.

## Text points on this library
1. **`src/Datasec.Suite.Sessions/TokenBrokerOptions.cs:14`** (the seat's own open text point, confirmed at e9095598):
   the XML comment of `RestartWindow` still says "A record is restored only if its last activity is at most this long
   ago". The code (`TokenBroker.cs:760`, `idle >= _restartWindow` drops), the README and cell R10 say "less than"
   (a record idle exactly the window is dropped). One word in a comment; fix with the next change to the library.
2. The README's D24 limit sentence says "only for a step smaller than the time since the record was last written". It
   is true when that time is read AT THE RESTART (E08: a 25-minute step one minute after the last write, restart at true
   idle 29 minutes: restored; restart at true idle 10 minutes: dropped). A reader could take it as the time at the step.
   Optional clarity: "smaller than the time from the record's last write to the restart".

## Limits now stated in the README (from the first check's points), for the backlog
3. D21: after a time-out, a refresher that ignores cancellation can overlap the next call of that session (at most one
   more call per `RefreshTimeout` per session; the late answer disposed; a late rotation lost). Cell F13.
4. D24: a wall clock set back while the server runs, then a restart inside the window, lengthens a restored session's
   idle life by at most the step. Cell E08. The reader's own probe still measures it (a 30-minute session read at true
   idle 49 minutes hands out a token), as the README says. A fix needs a time source that survives a restart: an open
   point, decided by nobody.
5. D28: a blocking `SessionEvent` handler blocks the callers of that refresh. README line, no cell, no code.
6. D20's cost: a refresher that blocks past the bound keeps its pool thread until it returns. Whether WP1.4's real
   refresher blocks before its first await is UNMEASURED (no such refresher exists yet).
7. D26 (b): a record-store read that fails at restart erases every record it hits (fail closed). Cell R09.

## Owed elsewhere (not findings against this lane; carried from the first check)
8. `Datasec.Suite.Secrets`: a listing that also names records that do not open, so a consumer can delete a damaged
   record and restore the rest. Until then one unreadable record stops the broker from starting.
9. The host wiring (unowned): who calls `Sweep()` and how often (at least as often as the shortest idle timeout); the
   secret-store partition the host gives the broker (one process per partition).
10. The runbook gains this lane's checks: F11 (a refresher blocking inside its call, test clock), E07 (idle during a
    refresh), P04 (the writer's cleared report), and the D20 waits (a cell that starts a refresh without awaiting waits
    for `Calls` and `LiveTimers` before it reads them or moves the clock).
11. The root README's Layout section does not list the two new projects.

## Process notes
12. The seat's deviations 1 (predictions written after the first edits, before any run), 2 (one `sed -i` on one
    comment line of its own test file, in the reviewed diff) and 8 (a gitleaks rc first read through a pipe, rerun
    alone) are records only.
13. This reader's probe file (round 1's 37 cases, `2026-11-21_B1838_verify/reader-probes.cs.txt`) needed ONE change
    to run at the new head: its seeded fuzz moved the test clock as soon as `Refresher.Calls` had grown, which with D20
    is no longer synchronous, so all 20 seeds first ended on their 10 s guard (`probes-1.log`); with the same wait the
    lane's cells added (the call entered and its bound armed, then the clock moved), 111 of 111 passed. The changed probe
    file is `reader-probes-r2.cs.txt` in this folder (scratch only; never part of the lane).
14. Two readers share one wave lock; waits behind the second reader were not findings.
