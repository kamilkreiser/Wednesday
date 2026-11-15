NO GO
GATE B1564: NO GO @ ced6997 on main ccc4136 (main has since moved to ee44790; see Refs)

BLUF: tier G2, round 1 of 2, 2026-11-15 12:53-13:50 AEDT, independent clone at head. Branch `b1564/mps-lane-ma-source-wait-pins` @ `ced69979a0080816f1e5a911bce1cdbf1fe591b0` (1 commit, 3 new test files, 0 product bytes) is the right change and every row does kill its mutant (m0, m1, m2 each turn their named row red, 3 of 3 at the shipped thresholds, and again 2 of 2 on a 2-CPU pool). On the machine's default pool the rows are green every time (26 batch runs of the rows, 0 red; whole Api project 3641 passed, 0 failed; build 0 warnings). But the rows are NOT stable on UNCHANGED code when the process's pool is the size of a hosted runner's: with `DOTNET_PROCESSOR_COUNT=4` the same rows went red on unchanged code in 4 of 35 runs (the clause-5 16-step row and the poll row, every answer late by 25 to 170 ms past the 500 ms margin at once). The builder hit the same red once in its own full suite and fixed it by moving ONE row from 8 to 12 free threads; the poll row (which failed twice in my runs) and the hand-off row still use 8. Hosted CI will run these rows on a 2- or 4-vCPU runner on every push to main, so this is a flaky gate waiting to happen. Findings: Blocker 0, Major 1, Minor 3, Info 4. Round 2: make the rows stable on a small pool without loosening the 500 ms line, re-measure, then land.

## Refs, scope, merge (measured)
- `git ls-remote` (12:54): branch = `ced69979a0080816f1e5a911bce1cdbf1fe591b0`, main = `ccc413677810b8b06e88e74e7cf3d3f8c2729592` (= the kit's S2). `rev-list --left-right --count origin/main...HEAD`: 0 1. `diff --name-status`: 3 paths, all `A`: `tests/MpsCalc.Api.Tests/LaneMAClause5Tests.cs`, `LaneMAParkedPool.cs`, `LaneMAPollAndHandOffTests.cs`. All match `LaneMA*.cs` (3 of 3 inside the lane, 0 outside; no `src/`, `.github/`, csproj, global.json). Removed lines 0.
- Identity (`git log --format='%h %ae | %ce'`): `ced6997 <the repo's configured address> | <same>`; the attribution line `Co-Authored-By: Claude Sonnet 5.5` ends the message (1). Message has the key MPSCALC-99 once in the subject (the kit asks for it), no B-number, no person's name.
- At 13:45 main had MOVED to `ee447909c2f3cda510e856608cf1aeaa62316d41` (the web-only change of a sibling lane: 9 paths under `web/`, 0 under `tests/MpsCalc.Api.Tests`, 0 under `src/`). `git merge-tree --write-tree origin/main ced69979...`: clean (rc 0), tree `4f0bf794d73146b120a70c5db576fcb85606f654`. The merge result was not rebuilt or re-tested: the only difference from the head I tested is 9 `web/` files that no dotnet job reads (stated, not measured).
- Open PRs at 12:55: 1 (#193, the sibling web lane, 9 `web/` paths): overlap with this branch 0 paths.
- Deploy: none could trigger (no `.github`, no `src/`, no `infra/`, no `scripts/`; MPS `ci.yml` has no merge-triggered deploy job).

## Scans (step 7), my own program `scratchpad/scan.py` (python -I)
- Names `(?<![A-Za-z])<name>(?![a-z])` (Kam, Kamil, Kreiser, Steve, Peter, Paul, Blanchard, Inch, Waite, Friday, Tuesday, Wednesday, Thursday, Philip, Cuffy, Anupam, Baidya): 0 hits over 377 added lines and 0 over the commit message. Control: `x _by_Kam_ y` fires 1. Non-ASCII added lines 0; Cf characters 0 (control: planted Cf would count). URLs, uuid shapes, `ghp_`, `AKIA`, key blocks, `.local`, `Source_Documents`: 0 added lines. B-number, WED-, SWEEP shapes: 0.
- CodeQL pre-scan rows by hand over every added line, test files included (C# rows are the kit's, the standard has none): sensitive-NAME row (password, passwd, secret, token, credential, apikey, api_key, private_key, auth, case-insensitive): 0 added lines (control: a planted `var password = 1; File.WriteAllText(p, passwordX);` fires 2 rows, the name row and the write row). File writes / `Console.Write` / `StreamWriter`: 0. `Process.Start`: 0. Weak hash or `new Random(`: 0. XML readers: 0. `new RegExp(`/`innerHTML`: 0. The one added `catch` (`LaneMAPollAndHandOffTests.cs:91`, `SourceStoreUnavailableException`) records the answer and rethrows nothing but swallows nothing the row does not assert. No path or log line is built from a request value (every path is `_tree.Local(...)` of a temp folder; the `output.WriteLine` lines print counts and timings only).
- Fixed sleeps added (step 8 of the kit): `LaneMAClause5Tests.cs:110` `Task.Delay(bound / 2)` pacing of the held wait; `LaneMAParkedPool.cs:46` `Thread.Sleep(ParkPoll)` keeps a parked thread parked; `:50` `Task.Delay(ParkGuard)` failure bound; `LaneMAPollAndHandOffTests.cs:126` `Task.Delay(1 s)` ages the second step's arrival; `:137` `Task.Delay(1500 ms)` pacing of the held wait. Each is pacing or a bound, none makes a row pass. No `Skip`, no `#pragma` (0).
- Assertion words exist at main (`git grep -c -F` at origin/main): overlay Busy sentence 1 (`InventoryEndpoints.cs`), source Busy sentence 1 (`SourceLifecycle.cs`), `SOURCE_STORE_WRITE_FAILED` 3. No new product word.
- **CodeQL CLI csharp pack: NOT RUN, and it cannot run on this box.** `codeql database create --language=csharp` (v2.27.4, both `--build-mode=none` and the default) fails: `csharp/tools/osx64/Semmle.Autobuild.CSharp: Bad CPU type in executable`. The C# extractor ships as x86_64 only; this machine is arm64 and has no Rosetta (`arch -x86_64 /usr/bin/true`: `Bad CPU type in executable`; `libhostpolicy.dylib` is x86_64: `incompatible architecture`). No control could be built either (the control database fails the same way). The hand rows above are the floor; hosted CodeQL is the only proof for C#. The standard's "the CLI IS on the box" is true for javascript and python; for csharp it is not usable (Minor 3).

## Part A rows, each at its mutant (my own clone and my own planted mutants; load printed per run in the table below)
Mutants planted in scratch worktrees of the head (not in the clone), one line each, shipped thresholds, built rc 0, 0 warnings:
- m0 `SourceLifecycle.cs:630`: `await before.WaitAsync(Remaining(arrival, LockTimeout));` -> `if (!before.Wait(Remaining(arrival, LockTimeout))) { throw GiveUpTurn(before, mine, LockTimeout); }` (the kit's form).
- m1 `SourceLifecycle.cs:705`: `await Task.Delay(LockPoll);` -> `Thread.Sleep(LockPoll); await Task.CompletedTask;` (the bare `Thread.Sleep` of the kit leaves an async method with no await, which `TreatWarningsAsErrors` refuses as a build break; same adaptation as the builder's, Info 2).
- m2 `SourceLifecycle.cs:667` (inside `GiveUpTurn`, `:665`): `_ = before.ContinueWith(_ => mine.TrySetResult(), ...)` -> `_ = before; mine.TrySetResult();`.
Results (first reason line):
- (a) clause 5 under m0, 3 of 3 red at the shipped 12 threads: `63/64 overlay writers answered later than 2500 ms (max 5522 ms) while 16 source steps waited`; run 2 `63/64 ... (max 6017 ms)`; run 3 `61/64 ... (max 7007 ms)`. Margin over the 2500 ms line 3.0 to 4.5 s. The 64-step case is red 3 of 3 too but narrower: `18/64 source steps answered later than 2500 ms (max 3431 ms)`, `12/64 (max 3060 ms)`, `14/64 (max 3230 ms)`; margin 0.56 to 0.93 s. Under a 2-CPU pool, m0 with the clause-5 filter: red 2 of 2 (counts in the table).
- (b) finding 1, poll under m1, 3 of 3 red: `18/24 polling steps answered later than 2500 ms (max 6065 ms)`, `17/24 (max 6009 ms)`, `17/24 (max 6045 ms)`; the clause-5 rows stay green under m1 (A16 max 2015 to 2038 ms). 2-CPU pool: poll row red 2 of 2.
- (c) finding 2, the four existing rows (`LaneM5SourceLockWaitTests`: stage, validate, activate, rollback, 64 waiters) under m0, 3 runs: ALL FOUR GREEN 3 of 3 here (max 2034, 2021, 2023, 2007 ms against a 2500 ms line). The builder measured stage red 3 of 3 at 2652 to 2656 ms; I could not reproduce a single red in the existing four, so "one of four by a thin margin" is not shown on this box (Minor 2). It does not weaken the new rows: they go red 3 of 3 with the existing four unedited.
- (d) finding 3, hand-off under m2, 3 of 3 red: `in 13/24 stores the step behind a step that gave up its place took the store before the step in front of it` (13 of 24 each time; 2-CPU pool 2 of 2, also 13/24). The existing LaneM5 rows stay green under m2 (3 of 3 runs, 4 rows). The clause-5 and poll rows stay green under m2.
- Side reds, as the builder said: the hand-off row also goes red under m0 and m1 (the mutant blocks the hand-in on the test thread; 51 s and 1 m 39 s runs), harmless.

## Findings
| # | Grade | Where | Finding and measurement |
|---|---|---|---|
| F1 | Major | `LaneMAClause5Tests.cs:140` (`overlayLate == 0`), `LaneMAPollAndHandOffTests.cs:111` (`late == 0`), `LaneMAPollAndHandOffTests.cs:20` (`FreeThreads = 8`), `LaneMAClause5Tests.cs:64` (`[InlineData(16, 12)]`) | **Red on UNCHANGED code.** Default pool of this 18-CPU box, load1 4.9 to 7.2: 0 red in 26 batch runs of the rows (10 x four rows, 15 x clause-5 rows, 1 whole-project run). With `DOTNET_PROCESSOR_COUNT=4` (the pool size of a hosted runner; a configuration variable, no load made): 4 red of 35 batch runs. Clause-5 16-step row: `1/64 overlay writers answered later than 2500 ms (max 2688 ms)` (tag base-cpu4, run 3) and `64/64 overlay writers answered later than 2500 ms (max 2527 ms)` (tag all4-cpu4, run 2). Poll row: `24/24 polling steps answered later than 2500 ms (max 2541 ms)` (run 1) and `(max 2664 ms)` (run 11). In every red the WHOLE group arrived late together (median = max), i.e. one pool stall of 25 to 170 ms past the 500 ms margin, not a slow product path. The builder met the same red once in its full suite (1/64 at 2582 ms) and raised ONE row from 8 to 12 free threads; at 12 it still reds under a 4-thread-minimum pool, and the poll and hand-off rows still use 8. 2-CPU pool: 0 red in 5. Not fixed at the root. A row that is red once on unchanged code is a Major by the commission. |
| F2 | Minor | `LaneMAParkedPool.cs:32` | `toPark = Math.Max(Math.Max(ThreadPool.ThreadCount, minimum) - free, 0)`: "leave N free" is a ceiling, not a guarantee. When the pool holds fewer than N threads it parks 0 (printed: `0 pool threads parked` in a 64-step run, 2 to 21 in others; up to 73 in the m0 runs), so the free-thread count the row asserts against varies run to run with earlier tests and machine size. The row's kill is independent of that (m0 and m1 red every time), but its flake odds (F1) are not. |
| F3 | Minor | STATUS, PART A (c), RESIDUE | Builder claims the existing stage row goes red 3 of 3 under m0 at 2652 to 2656 ms ("one of four, thin"). Not reproduced: 0 of 4 red in 3 runs (max 2034 ms). Claim not shown on this box; the new rows' kill (A16 3.0 to 4.5 s, A64 0.56 to 0.93 s over the line) is measured and true. |
| F4 | Minor | gate tooling, not the change | The standard's step 7 says run CodeQL's own pack when the CLI is on the box; for csharp the CLI cannot extract on this arm64 box (x86_64-only extractor, no Rosetta): NOT RUN, no control possible. Hosted CodeQL is the only C# proof. Tuesday: consider a note in the standard. |
| I1 | Info | STATUS RESIDUE "HAND is probabilistic under m2" | Measured deterministic here: 13/24 stores overtaken in 5 of 5 runs (3 default pool, 2 on a 2-CPU pool); the builder saw 8, 18, 13. Stronger than claimed. |
| I2 | Info | m1 form | Kit's one-line `Thread.Sleep(LockPoll)` does not build under warnings-as-errors (async without await); both the builder and I use `Thread.Sleep(LockPoll); await Task.CompletedTask;`. Disclosed. |
| I3 | Info | product, `SourceLifecycle.cs:630, :705`; `CatalogueOverlayStore.cs:619, :716` | Does raising free threads hide a product timing problem? No, from the code: the product's waits are `await before.WaitAsync(...)` (`:630`), `await Task.Delay(LockPoll)` (`:705`) and, for the overlay, `await before.WaitAsync(...)` (`:619`) and `await Task.Delay(25)` (`:716`); a waiting step holds no thread, and the three mutants prove the rows see a held thread (m0 and m1 red with the pool restricted). The number of free threads only sets how many pool threads the HARNESS leaves for the burst of 80 to 144 Busy answers that all fire at the same instant (every request shares one 2000 ms deadline). It is harness capacity. But it is the harness, and it is not yet sized for a small pool (F1). |
| I4 | Info | refs | Main moved to `ee447909` (web only) during the gate; merge-tree with it is clean (see Refs). Open PR #193 is the sibling web lane. |

## Builder claims (step 8)
true: scope (3 new files, 0 removed lines, 0 outside); ASCII 0 and names 0 (mine equal); build 0 warnings rc 0 and 4 new rows named; Api 3641 passed 0 failed 0 skipped (mine: 3641, 0 failed, 0 skipped, 8 m 33 s); m0 red 3 of 3 on the 12-thread clause-5 row (63/64 late, 5.5 to 7.0 s); poll row red under m1; hand-off row red under m2, existing LaneM5 rows green under m2; fixed-sleep list; "5/5 targeted runs green" (mine: 26 of 26 batch runs on the default pool). Not reproduced: existing stage row red under m0 (F3). Not shown, now measured against it: "the rows are stable" / "Fix ... free threads 8 -> 12" (F1: red on unchanged code at a 4-thread-minimum pool, and 2 of 3 rows still at 8). The builder's own RESIDUE already says the under-load half of the project's timing rows is unmeasured.

## What the round-2 builder should do (suggestions, not a design)
1. Reproduce F1 first: `DOTNET_PROCESSOR_COUNT=4` and the `LaneMA` filter, 30 runs; it reds about 1 in 9 batches for me.
2. Make the rows size their harness to the burst, not to a constant: give every row (poll and hand-off included) at least as many free threads as it has simultaneous answers at the deadline (24 for poll, 80 to 128 for clause 5 at the instant), or stagger the arrival so the deadline does not coincide, and keep m0 and m1 red 3 of 3 with the shipped numbers; do not loosen the 2000 ms bound or the 500 ms margin.
3. Print `ThreadPool.ThreadCount` and the number actually left free beside each row's result (F2), so the next gate can see the quantity the row depends on.
4. Re-measure: unchanged code 30 runs at the default pool and 30 at `DOTNET_PROCESSOR_COUNT=4` and `=2`, each mutant 3 runs at each, whole Api project once.

## Runs (every run: counts and load)
Machine load1 stayed between 4.77 and 15.4, never near 24. The load gate (two reads 120 s apart, not independent) was taken at the start of these slots: build 8.14 (first read); base10 8.65 then 6.85; cpu4/cpu2 11.07 then 8.35; whole Api project 6.31 then 6.22; a16 slot 4.9; the mutant slots m1/m2/m0-cpu2 and later followed within a minute of the previous slot on a gate already taken, with the load printed before and after each run (reads under 24 each time). `dotnet --version` printed 10.0.404 in every slot. Another seat's orphaned MSBuild nodes (about 4 CPUs at 86 percent, from 11:48) shared the box throughout; load is the printed figure. Heavy slot: `.tools/.heavy-lock-1` by `mkdir`, holder file moved to my scratch after each slot, `rmdir` after (0 locks left; `ls` printed no match). Rows: `LaneMA` = 4 rows (A16, A64, poll, hand-off); "a16" = the 2 clause-5 rows; mutant batches also run the 4 existing LaneM5 rows (8 rows). Env tags: `cpu4` = `DOTNET_PROCESSOR_COUNT=4`, `cpu2` = `=2`.

| tag | run | start | load1 before -> after | rc | counts | first reason line of a red |
|---|---|---|---|---|---|---|
| base10 | 1 | 12:58:55 | 6.85 -> 6.65 | 0 | failed 0 passed 4 total 4 |  |
| base10 | 2 | 12:59:07 | 6.65 -> 6.55 | 0 | failed 0 passed 4 total 4 |  |
| base10 | 3 | 12:59:19 | 6.55 -> 6.77 | 0 | failed 0 passed 4 total 4 |  |
| base10 | 4 | 12:59:31 | 6.77 -> 7.10 | 0 | failed 0 passed 4 total 4 |  |
| base10 | 5 | 12:59:44 | 7.10 -> 7.08 | 0 | failed 0 passed 4 total 4 |  |
| base10 | 6 | 12:59:57 | 7.08 -> 7.13 | 0 | failed 0 passed 4 total 4 |  |
| base10 | 7 | 13:00:12 | 7.13 -> 7.16 | 0 | failed 0 passed 4 total 4 |  |
| base10 | 8 | 13:00:26 | 7.16 -> 7.14 | 0 | failed 0 passed 4 total 4 |  |
| base10 | 9 | 13:00:39 | 7.14 -> 6.80 | 0 | failed 0 passed 4 total 4 |  |
| base10 | 10 | 13:00:50 | 6.80 -> 6.53 | 0 | failed 0 passed 4 total 4 |  |
| m0 | 1 | 13:01:11 | 6.60 -> 5.86 | 1 | failed 3 passed 5 total 8 | 18/64 source steps answered later than 2500 ms (max 3431 ms); 63/64 overlay writers answered later than 2500 ms (max 5522 ms) while 16 source steps waited |
| m0 | 2 | 13:02:49 | 5.86 -> 6.81 | 1 | failed 3 passed 5 total 8 | 12/64 source steps answered later than 2500 ms (max 3060 ms); 63/64 overlay writers answered later than 2500 ms (max 6017 ms) while 16 source steps waited |
| m0 | 3 | 13:04:28 | 6.81 -> 7.95 | 1 | failed 3 passed 5 total 8 | 14/64 source steps answered later than 2500 ms (max 3230 ms); 61/64 overlay writers answered later than 2500 ms (max 7007 ms) while 16 source steps waited |
| m1 | 1 | 13:06:03 | 8.52 -> 10.32 | 1 | failed 2 passed 6 total 8 | 18/24 polling steps answered later than 2500 ms (max 6065 ms) |
| m1 | 2 | 13:08:07 | 10.32 -> 9.88 | 1 | failed 2 passed 6 total 8 | 17/24 polling steps answered later than 2500 ms (max 6009 ms) |
| m1 | 3 | 13:10:11 | 9.88 -> 11.83 | 1 | failed 2 passed 6 total 8 | 17/24 polling steps answered later than 2500 ms (max 6045 ms) |
| m2 | 1 | 13:12:21 | 15.36 -> 13.64 | 1 | failed 1 passed 7 total 8 | in 13/24 stores the step behind a step that gave up its place took the store before the step in front of it |
| m2 | 2 | 13:12:44 | 13.64 -> 12.13 | 1 | failed 1 passed 7 total 8 | in 13/24 stores the step behind a step that gave up its place took the store before the step in front of it |
| m2 | 3 | 13:13:13 | 12.13 -> 11.07 | 1 | failed 1 passed 7 total 8 | in 13/24 stores the step behind a step that gave up its place took the store before the step in front of it |
| base-cpu4 | 1 | 13:15:44 | 8.35 -> 7.52 | 0 | failed 0 passed 4 total 4 |  |
| base-cpu4 | 2 | 13:15:58 | 7.52 -> 6.80 | 0 | failed 0 passed 4 total 4 |  |
| base-cpu4 | 3 | 13:16:15 | 6.80 -> 6.53 | 1 | failed 1 passed 3 total 4 | 1/64 overlay writers answered later than 2500 ms (max 2688 ms) while 16 source steps waited |
| base-cpu4 | 4 | 13:16:28 | 6.53 -> 6.49 | 0 | failed 0 passed 4 total 4 |  |
| base-cpu4 | 5 | 13:16:42 | 6.49 -> 6.39 | 0 | failed 0 passed 4 total 4 |  |
| base-cpu2 | 1 | 13:18:55 | 7.68 -> 10.86 | 0 | failed 0 passed 4 total 4 |  |
| base-cpu2 | 2 | 13:19:08 | 10.86 -> 9.88 | 0 | failed 0 passed 4 total 4 |  |
| base-cpu2 | 3 | 13:19:31 | 9.88 -> 10.00 | 0 | failed 0 passed 4 total 4 |  |
| base-cpu2 | 4 | 13:19:45 | 10.00 -> 9.72 | 0 | failed 0 passed 4 total 4 |  |
| base-cpu2 | 5 | 13:20:04 | 9.72 -> 9.34 | 0 | failed 0 passed 4 total 4 |  |
| fullapi | 1 | 13:24:24 | 6.31 -> 5.85 | 0 | failed 0 passed 3641 total 3641 |  |
| a16-def | 1 | 13:35:04 | 4.92 -> 5.01 | 0 | failed 0 passed 2 total 2 |  |
| a16-def | 2 | 13:35:10 | 5.01 -> 5.08 | 0 | failed 0 passed 2 total 2 |  |
| a16-def | 3 | 13:35:17 | 5.08 -> 5.08 | 0 | failed 0 passed 2 total 2 |  |
| a16-def | 4 | 13:35:23 | 5.08 -> 5.23 | 0 | failed 0 passed 2 total 2 |  |
| a16-def | 5 | 13:35:29 | 5.23 -> 5.50 | 0 | failed 0 passed 2 total 2 |  |
| a16-def | 6 | 13:35:36 | 5.50 -> 5.46 | 0 | failed 0 passed 2 total 2 |  |
| a16-def | 7 | 13:35:43 | 5.46 -> 5.43 | 0 | failed 0 passed 2 total 2 |  |
| a16-def | 8 | 13:35:49 | 5.43 -> 5.43 | 0 | failed 0 passed 2 total 2 |  |
| a16-def | 9 | 13:35:55 | 5.43 -> 5.56 | 0 | failed 0 passed 2 total 2 |  |
| a16-def | 10 | 13:36:02 | 5.56 -> 5.51 | 0 | failed 0 passed 2 total 2 |  |
| a16-def | 11 | 13:36:08 | 5.51 -> 5.58 | 0 | failed 0 passed 2 total 2 |  |
| a16-def | 12 | 13:36:15 | 5.58 -> 5.61 | 0 | failed 0 passed 2 total 2 |  |
| a16-def | 13 | 13:36:21 | 5.61 -> 5.56 | 0 | failed 0 passed 2 total 2 |  |
| a16-def | 14 | 13:36:27 | 5.56 -> 5.52 | 0 | failed 0 passed 2 total 2 |  |
| a16-def | 15 | 13:36:34 | 5.52 -> 5.67 | 0 | failed 0 passed 2 total 2 |  |
| a16-cpu4 | 1 | 13:36:41 | 5.67 -> 5.70 | 0 | failed 0 passed 2 total 2 |  |
| a16-cpu4 | 2 | 13:36:48 | 5.70 -> 5.81 | 0 | failed 0 passed 2 total 2 |  |
| a16-cpu4 | 3 | 13:36:55 | 5.81 -> 5.99 | 0 | failed 0 passed 2 total 2 |  |
| a16-cpu4 | 4 | 13:37:03 | 5.99 -> 6.38 | 0 | failed 0 passed 2 total 2 |  |
| a16-cpu4 | 5 | 13:37:10 | 6.38 -> 6.35 | 0 | failed 0 passed 2 total 2 |  |
| a16-cpu4 | 6 | 13:37:18 | 6.35 -> 6.30 | 0 | failed 0 passed 2 total 2 |  |
| a16-cpu4 | 7 | 13:37:24 | 6.30 -> 6.19 | 0 | failed 0 passed 2 total 2 |  |
| a16-cpu4 | 8 | 13:37:31 | 6.19 -> 6.18 | 0 | failed 0 passed 2 total 2 |  |
| a16-cpu4 | 9 | 13:37:37 | 6.18 -> 6.24 | 0 | failed 0 passed 2 total 2 |  |
| a16-cpu4 | 10 | 13:37:43 | 6.24 -> 6.12 | 0 | failed 0 passed 2 total 2 |  |
| a16-cpu4 | 11 | 13:37:49 | 6.12 -> 6.11 | 0 | failed 0 passed 2 total 2 |  |
| a16-cpu4 | 12 | 13:37:56 | 6.11 -> 6.03 | 0 | failed 0 passed 2 total 2 |  |
| a16-cpu4 | 13 | 13:38:02 | 6.03 -> 5.94 | 0 | failed 0 passed 2 total 2 |  |
| a16-cpu4 | 14 | 13:38:09 | 5.94 -> 6.47 | 0 | failed 0 passed 2 total 2 |  |
| a16-cpu4 | 15 | 13:38:15 | 6.47 -> 6.44 | 0 | failed 0 passed 2 total 2 |  |
| m0-cpu2 | 1 | 13:40:23 | 5.46 -> 5.52 | 1 | failed 2 passed 0 total 2 | 63/64 overlay writers answered later than 2500 ms (max 6026 ms) while 16 source steps waited; 64/64 overlay writers answered later than 2500 ms (max 4066 ms) while 64 source steps waited |
| m0-cpu2 | 2 | 13:40:47 | 5.52 -> 5.75 | 1 | failed 2 passed 0 total 2 | 49/64 source steps answered later than 2500 ms (max 6025 ms); 64/64 overlay writers answered later than 2500 ms (max 5021 ms) while 16 source steps waited |
| m1-cpu2 | 1 | 13:41:11 | 5.75 -> 5.69 | 1 | failed 1 passed 0 total 1 | 18/24 polling steps answered later than 2500 ms (max 6604 ms) |
| m1-cpu2 | 2 | 13:41:19 | 5.69 -> 5.81 | 1 | failed 1 passed 0 total 1 | 18/24 polling steps answered later than 2500 ms (max 6051 ms) |
| m2-cpu2 | 1 | 13:41:27 | 5.81 -> 5.74 | 1 | failed 1 passed 0 total 1 | in 9/24 stores the step behind a step that gave up its place took the store before the step in front of it |
| m2-cpu2 | 2 | 13:41:31 | 5.74 -> 5.76 | 1 | failed 1 passed 0 total 1 | in 15/24 stores the step behind a step that gave up its place took the store before the step in front of it |
| all4-cpu4 | 1 | 13:41:37 | 5.76 -> 5.80 | 1 | failed 1 passed 3 total 4 | 24/24 polling steps answered later than 2500 ms (max 2541 ms) |
| all4-cpu4 | 2 | 13:41:49 | 5.80 -> 5.70 | 1 | failed 1 passed 3 total 4 | 64/64 overlay writers answered later than 2500 ms (max 2527 ms) while 16 source steps waited |
| all4-cpu4 | 3 | 13:42:03 | 5.70 -> 5.75 | 0 | failed 0 passed 4 total 4 |  |
| all4-cpu4 | 4 | 13:42:20 | 5.75 -> 5.52 | 0 | failed 0 passed 4 total 4 |  |
| all4-cpu4 | 5 | 13:42:34 | 5.52 -> 5.52 | 0 | failed 0 passed 4 total 4 |  |
| all4-cpu4 | 6 | 13:42:49 | 5.52 -> 5.15 | 0 | failed 0 passed 4 total 4 |  |
| all4-cpu4 | 7 | 13:43:05 | 5.15 -> 5.13 | 0 | failed 0 passed 4 total 4 |  |
| all4-cpu4 | 8 | 13:43:16 | 5.13 -> 5.03 | 0 | failed 0 passed 4 total 4 |  |
| all4-cpu4 | 9 | 13:43:27 | 5.03 -> 4.80 | 0 | failed 0 passed 4 total 4 |  |
| all4-cpu4 | 10 | 13:43:45 | 4.80 -> 4.77 | 0 | failed 0 passed 4 total 4 |  |
| all4-cpu4 | 11 | 13:44:03 | 4.77 -> 4.82 | 1 | failed 1 passed 3 total 4 | 24/24 polling steps answered later than 2500 ms (max 2664 ms) |
| all4-cpu4 | 12 | 13:44:15 | 4.82 -> 5.07 | 0 | failed 0 passed 4 total 4 |  |
| all4-cpu4 | 13 | 13:44:34 | 5.07 -> 6.11 | 0 | failed 0 passed 4 total 4 |  |
| all4-cpu4 | 14 | 13:44:46 | 6.11 -> 5.78 | 0 | failed 0 passed 4 total 4 |  |
| all4-cpu4 | 15 | 13:44:57 | 5.78 -> 5.99 | 0 | failed 0 passed 4 total 4 |  |

Whole Api project, unchanged head (`fullapi`, tag in the table): rc 0, failed 0, passed 3641, skipped 0, 8 m 33 s (base per the builder: 3637; +4 = the four new rows). Build of `MpsCalc.slnx -c Release` at head: rc 0, `0 Warning(s) 0 Error(s)`. Engine (743) and Import (196) were not re-run: the diff touches only `tests/MpsCalc.Api.Tests`, no file those projects read (stated, not measured).

## CI predicates (ci.yml at head)
Job `dotnet`: build `MpsCalc.slnx -c Release` rc 0, 0 warnings (warnings are errors by `Directory.Build.props`), test Api project rc 0, 0 failed. Jobs `package` and `python` read none of the three paths. Hosted CI runs `dotnet test MpsCalc.slnx --no-build` on `ubuntu-latest` (a private repo: 2 vCPU); F1 is the risk there.

## NOT RUN
Hosted CI, hosted CodeQL, the CodeQL CLI csharp pack (cannot run: x86_64-only extractor on an arm64 box, F4), Engine and Import test projects at head (no path they read changed), the merge result at main `ee447909` (build or tests; only the merge-tree), a real 2- or 4-vCPU Linux runner (the `DOTNET_PROCESSOR_COUNT` runs change the pool's size only, on an 18-CPU machine; they are a probe, not a hosted run), any run with load above this box's 4.8 to 15.4, gitleaks (the secret, host and key-block rows of my scan ran instead; 0), a second round of the builder's own mutants. Nothing was pushed, no PR, no Jira write, no `az`, no docker, no hosted HTTP except `gh api -X GET` and `git fetch`/`ls-remote` over SSH.

## Tier (step 9)
G2 as the kit says. Tests only; no security-shaped issue found; no raise to G1.

## Landing
`landing.txt` holds the head-pinned squash for `ced69979`. Do NOT run it on this verdict: it is NO GO. If round 2 pushes a new head, the commands are re-issued by a new gate (the `--match-head-commit` pin refuses any other sha).
