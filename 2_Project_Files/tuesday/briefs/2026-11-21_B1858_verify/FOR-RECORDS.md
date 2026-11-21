# FOR RECORDS: WP3.8, the shared Graph HTTP layer (lane A), round-2 delta check

For a records pass after the lane lands. Nothing here was written to the project. R1 to R6 are the round-1 check's
records (2026-11-21_B1847_verify/VERDICT.md), carried unchanged by the fix round's kit (D7: records only, no code) and
confirmed still open at cfa31851 by this reader.

## Runbook (`SETUP_RUNBOOK.md`, check table)

- The solution builds and tests two more projects: `src/Datasec.Suite.Graph` and `tests/Datasec.Suite.Graph.Tests`.
- Local totals, measured by this reader through the wave lock:
  - head cfa31851 alone: 1091 (894 + 176 + 21), failed 0, skipped 4
  - merged with main 762e774e: 1170 (973 + 176 + 21), failed 0, skipped 4; RULES: clean (368 files); build/tests
    Ran 60
- The lane's own count is 197 tests (176 of the first commit, 21 rows of the second).

## README (`README.md`, Layout section)

The Layout section lists neither project. It needs two lines: `src/Datasec.Suite.Graph` (the shared Graph HTTP
layer) and `tests/Datasec.Suite.Graph.Tests`. Round 1's Q14: a records lane's or Tuesday's job, after the landing.

## BACKLOG (`BACKLOG.md`)

1. **R1** `MaxThrottleRetries` and `MaxNextLinkLength` have no upper bound (round 1 measured 20,001 sends at
   `MaxThrottleRetries = 20000` with `Retry-After: 0`); only a caller can set them; the default is 3. Optional later:
   cap like `MaxPieceRetries` (0 to 1000).
2. **R2** The token source has no time bound inside the layer: a source that never answers holds the call until the
   CALLER cancels. The adapter over lane D's broker should bound the broker call (report A11 line 95: the Workpath app
   waits at most 10 s, RELAYED).
3. **R3** Redirects and the caller's `HttpClient.DefaultRequestHeaders` are the host's: build the Graph `HttpClient`
   with automatic redirects off and no default `Authorization`. Whether .NET drops `Authorization` on a cross-host
   redirect is UNMEASURED.
4. **R4** The token is a .NET `string` that cannot be wiped: a design point for the adapter, beside lane D's byte
   token (not a finding).
5. **R5** The total-wait cap has a single guarding test (`ThrottleTests.TheTotalWaitCapEndsTheCall`); the upload's
   total wait has no cell of its own (it holds: 4 requests and 60 s at 1000 piece retries, round 1's measurement).
6. **R6** The round-1 builder's one `sed -i` on its own lane scratch file (process only).
7. **N13 (named limit, this round)** An item of `value` holding a string the JSON reader cannot decode is returned
   unvalidated as a cloned `JsonElement`; a module that turns it into text meets .NET's own refusal
   (`InvalidOperationException`). Whether the modules must expect that, or the layer should refuse such a page, is NOT
   DECIDED (the fix kit's item 1). This reader measured it: round 1's page shape `value item invalid UTF-8` is a value
   at cfa31851 (this reader's probe), and the seat's widened random bodies spoil item strings with no conversation
   failing on them, because the layer never reads an item as text.
8. **The adapter from lane D's broker to `IGraphTokenSource`** (who writes it, where it lives; broker failures all
   fold into `Unauthorized`): the round-1 kit's NOT DECIDED items 1 and 2, still open. Lane D (pull request 9) is now
   on main.
9. **A tenant test is needed.** Every Graph behaviour in the tests is assumed. Exit test E3.3 is NOT proved by this
   lane, and `OXPD2-16` stays open.
10. **Release guard deny-list (not this lane's):** `build/release_guard.py` prints `GUARD-WARN: development CA
    deny-list holds 0 fingerprints (owed)` on both publish folders (the seat's FOR TUESDAY 7; the owed D12 item of the
    bootstrap lane).

## Process (the fix round's seat)

- Deviation 1: one stray `cd /dev/null` typed in a hash command; it failed and changed nothing (process record).
- Deviation 2: the boundary scan's planted control carried 4 of the list's words, and the printed `control rc=0` was
  `tail`'s, not the scanner's; the 4 HIT lines are its proof (process record; this reader's own C8 reflection walk at
  cfa31851 passed).
- The fix round's kit and its drafter disclosed one scratch console run outside the wave lock at load 11 (the
  drafter's process, recorded at the stamp S1).

## This reader's own process

- Every git write verb, build, probe and mutant ran in clones under the session scratchpad
  (`.../scratchpad/b1858/{head,merge,probe,probe1,mut,red}`, push URL `invalid://no-push`), because the workspace hook
  refuses write verbs elsewhere; the read clone, tools, logs and moved lock folders are in `/private/tmp/b1858-gate/`.
- The scratch merge commit f35b8daa (tree 84b6bc81) was made with a throwaway identity and is never pushed.
