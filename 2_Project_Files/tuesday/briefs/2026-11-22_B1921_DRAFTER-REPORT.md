STARTABLE: YES

# B1921 DRAFTER REPORT: lane D (seat Datasec/OXPd2-X33), the state database's audit-integrity limit and duplicate race (owed item 43 (1) and (2))

Written 2026-11-22 at about 22:01 AEDT by the read-only Opus drafter for Tuesday (s311), on `2026-11-22_B1920-B1922_OXPD-WAVE2-KITS_DRAFTER_COMMISSION.md`, lane D only. Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-22_B1921_SEAT-X33_oxpd2-d-audit-limit-duplicate-race.md` (75773 bytes, 228 lines, sha256 `e82ed0351f19208e69401e30d6a51e04cca5217d49a9e56ebb1721fc2df1d677` at the sidecar write), sidecar `.measured` beside it (`stamp_check.py <kit>` exits 0: 135 claims, 135 measured), scratch `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s311/d1921/` (`gate/` = the seat's `<src>`, 14 files; `logs/proto.out` = the summary of every run; `tools/proto.py`, `genpatches.py`, `fill.py`). Stamp: 8 slots `____` (S1 to S7 and the last line), none pre-written.

## BLUF
- **Startable.** Both items have frozen patches measured end to end in a FRESH scratch clone at `4a0a9717` by `git apply`, the seat's way. No migration, no snapshot, no public member, no package, no `.csproj`, no lock file (`surface.py`: `PUBLIC: equal (85 lines)`, `SCHEMA: equal (8 files)` on both chains, its control `CONTROL FIRED: 2 of 2`).
- **43 (2), the race, is a code fix with three red-first cells.** A test-only `SaveChangesInterceptor` (`RaceWinner`) inserts the same key on the shared SQLite connection at the registry's save. At BASE that reproduces the readers' finding exactly: `DbUpdateException` (`UNIQUE constraint failed: Devices.SerialKey`), and the next audit append on the same context fails too. The fix (+17 -1 in `EfDeviceRegistry.cs`): on `DbUpdateException`, `ChangeTracker.Clear()` (the stale path's shape), then read the key again. If it is held, `DuplicateDevice`; if not, `throw;`. Red at BASE: Data `Total: 55, Errors: 0, Failed: 3`. Green: 55/0. Mutants: `mNoMap` reddens 1 cell, `mNoClear` 2, `mAlwaysDuplicate` 1, each on the cells named.
- **43 (1) by default (Q1 = a) is a NAMED LIMIT**, as the commission said. Two README edits name the in-save hooks (a `SavingChanges` handler, a save interceptor, and also an entry being added) and say what "through the library" means. Two limit cells go beside the existing three. They are red against the alternative's guard (57 run, 2 failed), so a future close must change them on purpose.
- **The alternative (Q1 = b) was built and measured, so you have a real choice.** It is a refusal in `ChangeTracker.StateChanged` and `Tracked` handlers, active only while a save runs. It is 42 product lines, red first on 2 cells at the race state (58 run, 2 failed), green at 58/0, and `mNoStateChanged` reddens both cells. It needs no schema change, and its public lines are equal (the async override reads equal because ` async ` is read as a blank). The whole solution passes: 1585 total, 0 failed.
- **Whole solution, locally:** Q1 = a `total: 1584`, `failed: 0`, `succeeded: 1580`, `skipped: 4`. Q1 = b gives 1585 / 0 / 1581 / 4. Main is 1579 hosted, so +5 (a) or +6 (b).

## Facts re-measured (instrument; control)
- Origin (`gh api -X GET`, project `GH_CONFIG_DIR`, 21:48:47): main `4a0a9717277f60647dfc174e60ec04fc7008e615`; private true, push true; 19 PRs all closed, 0 open; 21 branches; `matching-refs/heads/b1921` 0 rows. Only PR 12 of 19 touches a Data path (24 files; every other PR 0). The positive control is PR 12 itself.
- BASE tree: `ac3bf369805ef760a583afb1dbc785c64ace6b1b` in the drafter's clone, equal to `gh api .../git/commits/4a0a9717 --jq .tree.sha`. 500 tracked files.
- Absence of prior work at BASE: `git grep -c -F` for `RaceWinner`, `NewContextWith`, `lost_duplicate_race`, `StateChanged` and `SavingChanges` over `src` and `tests` each print 0 files. Control: `limit_asserted_ExecuteDelete` prints 1.
- The Data assembly at BASE: `Total: 52, Errors: 0, Failed: 0`.
- The commission's sweep footnote does not hold for D. Lane D does NOT compile against the secret store: `grep -c -i -F 'Secrets'` prints 0 on the Data csproj, the Data tests csproj, the Devices csproj and both Data lock files. Control: the Sessions csproj prints 1. Only `tests/Datasec.Suite.Data.Tests` references the Data project. The Server does not.
- Toolchain: `.tools/dotnet/dotnet --version` prints 10.0.404; gitleaks 8.30.1. `words.py --control` fired 13 of 13. The five patches and two messages read `WORDS: clean (7 files)`.
- `unittest` ran 111 tests, OK. `repo_rules.py` (no `--source-documents`; `test ! -e <d1921>/1_Project_Definition` rc 0) printed `RULES: clean (500 files)`. `gitleaks dir` over the a-chain clone and over the neutral copies of the patches and messages: rc 0. The planted random token: rc 1, then quarantined.
- Lock and load: 42 heavy jobs, every one through the round's `heavy.py`, ONE at a time. load1 read between 4.92 and 13.36; jobs waited while it was 7 or more; lock waits up to 14 polls behind other holders. No test ran outside the lock. No other lane's lock was touched.
- Stale clone note: the shared checkout `<project>/2_Project_Files` does not hold `4a0a9717` (`cat-file` fails). The drafter cloned `file://` from lane T's clone (read-only clone) and proved the tree against the origin's.

## D-decisions (all the coordinator's to confirm; the kit's defaults)
- D1, named limit (Q1 = a).
- D2, the alternative, built only on S4 = b.
- D3, recognise the race by re-reading the key, not by provider error codes. Those codes are UNMEASURED here.
- D4, a non-key `DbUpdateException` is rethrown and the tracker is cleared.
- D5, `Clear()` drops every tracked entry, as `SaveOrStale` does.
- D6, the cells' names and helpers.
- D7, one commit.

## Q-questions for Tuesday (each with its default)
- **Q1 (STOP-CLASS, answered in words at S4, "a" or "b"):** a NAMED LIMIT (default, `3a-limit.diff`) or the in-save refusal (`3b-guard-red.diff` plus `3b-guard-fix.diff`).
  - What b would cost: about 29 more test lines and 42 product lines, an event pair per context, `SaveChangesAsync` made `async`, and a G1 read of a new guard.
  - What b would still leave as limits: `ExecuteUpdate`, `ExecuteDelete`, raw SQL, a command interceptor, and an entry being added.
- Q2: a non-key failure is rethrown untyped and the tracker is cleared. Default yes. Alternatives: no clear (BASE), or a new enum member (a public change, not allowed).
- Q3: re-read the key after a failure. Default yes. The alternative is the provider error codes.
- Q4: `Clear()` drops all tracked entries. Default yes, as the stale path does.
- Q5: one commit for 43 (1) and (2). Default yes.
- Q6: Opus by `<project>/CLAUDE.md:7`. The routing row C2 (`model-routing.md:92`) would say Sonnet.
- Q7: READY by Step 0 + 150 min, push by Step 0 + 110, pane `Datasec/OXPd2-X33`, gate G1 on Opus.

## Chain inputs (each produced by an earlier step or present at BASE)
| Step | Inputs | Produced by or present at |
|---|---|---|
| 0 | the kit, Stamp S4 (Q1) | Tuesday's stamp |
| 1 | `<src>` (14 files), `<repo>` local values, origin, main's push run | drafter scratch (exists), `<repo>`, GitHub |
| 2 | the six owned files at BASE | Step 1 clone |
| 3 | `1-race-red.diff`, `2-race-fix.diff`, the baseline build | Step 1 |
| 4 (a)-(c) | the green race tree, `mutants.py` | Step 3, Step 1 |
| 5 | `3a-limit.diff` or the two 3b patches | Step 1 (tree from Step 4) |
| 4 (d)/(e) | the tree after Step 5, plus `3b-guard-fix.diff` (its `SuiteDbContext.cs` part only, `--include`) or `mutants.py` | Step 5, Step 1 |
| 6 | the staged tree, the commit message of the chain | Step 5, Step 1 |
| 7 | the commit, `origin/main` | Step 7 (a), the fetch of 7 (b) |
One ordering fact is MEASURED: `3b-guard-fix.diff` whole does NOT apply on top of `3a-limit.diff` (README hunk). So Step 4 (d) uses `--include=src/Datasec.Suite.Data/SuiteDbContext.cs`, as the drafter ran it.

## STOP-severity checks: run or marked
These were run once on the drafter's own prototype output, with their controls fired:
- `surface.py`: control 2 of 2, PASS on both chains.
- The red-first counts and the mutant reds.
- `words.py`: control 13 of 13.
- `gitleaks`: control rc 1.
- `repo_rules`, `unittest`, and the whole solution.

These are marked NEVER RUN in the kit:
- `hosted2.py` on a lane head, and on BASE by the drafter (Tuesday's read of main is RELAYED).
- The neutral-object scan of `run_step.py` (wordings RELAYED from B1917).
- The locked `--force` restore with the lock-file comparison, the two publishes, and `release_guard.py` (RELAYED from B1912).
- The b-chain's `unittest`, `repo_rules` and `gitleaks`.

## UNMEASURED
- Every cell's behaviour on the hosted Linux and Windows legs. The native SQLite differs per runtime. The kit makes a one-leg-alone red a STOP, never a skip.
- The unique-violation codes of PostgreSQL and SQL Server, and any run against a real server.
- A command interceptor that rewrites SQL. It is named as a limit and has no cell.
- Cancellation or a broken connection during the re-check (DERIVED: it propagates).
- That `Clear()` drops a caller's other pending changes. This is EF Core's contract, DERIVED, with no cell.

## Outside-the-fences disclosure
- Written: the kit, its `.measured` sidecar, this report, and files under `fleet/state/s311/d1921/` only.
- Repositories:
  - The project repository, origin and Jira: READ only. `gh api -X GET` only, under the project `GH_CONFIG_DIR`. No Jira call.
  - The shared checkout: one `git cat-file -t` (read).
  - Lane T's clone `<project>/.tools/b1917/clone`: one `git clone --no-hardlinks file://...` FROM it (a read of its objects). Nothing was written there.
- Write verbs: `git apply`, `checkout --detach` and `git add` (index only, in `clone2`) ran only in my own scratch clones under `d1921/` (push URL `invalid://no-push`). No commit, no push.
- The heavy lock `<project>/.tools/wave1-heavy.lock.d`: taken and released by `heavy.py` 42 times. That folder is the shared lock, as the commission's toolchain line requires. Released locks were moved into `d1921/_quarantine/locks/`.
- Nothing under `Source_Documents/`, the NAS library, any key folder, `fleet/briefs_staged/`, the scoreboard, `_ledger.md`, or a WEDNESDAY/FRIDAY tree was opened.
- No decision card was read.
- The drafter's own commission was read as a file.
- Nothing was deleted (the planted secret went to `d1921/_quarantine/`).
- No message to any human.
- No `cd`.
