# FOR RECORDS: the session and token broker lane (head 70c1fad5), reader B1838

What a records pass should file. None of it blocks the merge; none of it is decided by this reader.

## Follow-ups on this library (from VERDICT.md findings)
1. F1: bound a refresher that blocks before returning its task (`await Task.Yield()` or `Task.Run` before the call), or
   a README `## Limits` line. The second reader's view on the bound decides how high this goes.
2. F2: README `## Limits` line: a wall clock set back while the server runs, followed by a restart inside the window,
   restores a session with more idle time than it really has (bounded by its idle timeout). Whether to fix it needs a
   time source that survives a restart: an open point, decided by nobody.
3. F3: the record writer's buffer estimate (6 bytes per string character) or a broker-owned buffer cleared on growth,
   and a cell measuring it.
4. F4: two cells: a record whose `written` instant is ahead of the clock; a record-store read that throws at restore.
   Note that a transient read error at start erases every session it hits (fail closed).
5. F5: the kit's "at most" vs the code's "less than" at restore; the unused `SignOutReason.RestartWindow`.

## Owed elsewhere (not findings against this lane)
6. `Datasec.Suite.Secrets`: a listing that also names records that do not open, so a consumer can delete a damaged
   record and restore the rest (ANSWER-1 point 3). Until then one unreadable record stops the broker from starting.
7. The host wiring (unowned): who calls `Sweep()` and how often (at least as often as the shortest idle timeout); the
   secret-store partition the host gives the broker (one process per partition).
8. Local `repo_rules.py --source-documents` is red on main 5e36d8dc with 37 R5 rows under `contracts/oxpd2/hp/` (lane
   C's files, landed); the hosted `rules` job cannot see it (no supplied-source folder on a runner). Already routed by the
   seat's FOR TUESDAY point 6; not re-run by this reader.
9. The runbook gains this lane's checks: the restart test, the raw scan of the store root, and that `words.py` counts
   the restore-written `linux-x64` / `win-x64` of every new lock file.
10. The root README's Layout section does not list the two new projects.
11. `OXPD2-14` stays open (it holds WP1.4 too); no Jira call was made by the seat or by this reader.

## Process notes
12. The seat's STATUS DEVIATIONS 9 (a stray `rm -f /dev/null`, no effect) and 11 (a worktree left in the seat's own
    clone under `<lane>/scratch/main-5e36`).
13. This reader's probes (`reader-probes.cs.txt`, output `reader-probes-output.txt`) are kept in this folder only; they
    are not part of the lane and were never pushed. Five of them could become cells (F2, F3, F4).
14. The workspace hook refuses git write verbs outside the session scratchpad; the reader's builds and mutants ran in a
    second clone there (push URL `invalid://no-push`). Later gate commissions can say so up front.
