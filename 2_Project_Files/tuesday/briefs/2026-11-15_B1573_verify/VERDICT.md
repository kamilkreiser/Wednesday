GATE B1573: NO GO @ 29b1bea on main 3a69065

BLUF: tier G2, ROUND 2 OF 2 (the cap), 2026-11-15 16:20-17:45 AEDT. Head 29b1bea25f59d1caf64dc9d92f109e571b86a46e = one forward commit on ced69979, three LaneMA test files, 0 product bytes. F1's rows (poll, clause-5 16 and 64) are now steady and every kill holds. But the fix made the THIRD row, the hand-off row, flaky on unchanged code: 2 red in 70 unchanged-code batches, then 7 red in 60 in an interleaved head-vs-old-head run (old head ced69979: 1 in 60). So F1 as a class (a new row red on unchanged code) is NOT closed. Findings: Blocker 0, Major 1, Minor 2, Info 3.

## Refs, scope, merge
- ls-remote: branch = 29b1bea25f59d1caf64dc9d92f109e571b86a46e, main = 3a69065a6e35ed5b5f9ee76ea8f3648f60ee13cc. Head is one commit on ced69979 (parent printed). Open PRs: 0; PRs with the branch as head: 0.
- Against the merge-base with main (ccc41367): 3 paths, all added, all `tests/MpsCalc.Api.Tests/LaneMA*.cs` (3 of 3 inside the lane). Against ced69979: 215 added, 47 removed, all in those three files. No src/, .github/, csproj.
- Main since the base touches 12 paths (3 under scripts/, 9 under web/); overlap with the branch: 0. `git merge-tree --write-tree` was REFUSED by the seat hook (a write verb outside the Tuesday folder), so the merge is shown by disjoint path sets (0 overlap) and not by a computed tree. Merge result not built or tested.
- Deploy: none (ci.yml has no merge-triggered deploy).

## Scans (by hand, python -I, planted control fires)
Names (Kam, Kamil, Kreiser, Steve, Peter, Paul, Blanchard, Inch, Waite, Friday, Tuesday, Wednesday, Thursday, Philip, Cuffy, Anupam, Baidya, Datasec): 0 over 545 added lines and the commit message (control `_by_Kam_` fires). Non-ASCII 0, Cf 0, URLs/uuid/keys/ghp_/AKIA 0, B-numbers 0. Hand CodeQL rows: sensitive-name row hits only `CancellationToken` (the word "Token"; nothing is written anywhere, 0 file writes, 0 Console, 0 Process.Start, 0 Random, 0 XML readers, 0 RegExp, 0 Skip, 0 pragma). Fixed waits added: park loops, probe holds and a 20 ms sample window inside setup only (before the timed region), none makes a row pass. CodeQL csharp: NOT RUN (cannot extract on arm64); hosted CodeQL is the only C# proof.

## Findings
| # | Sev | Where | Finding |
|---|---|---|---|
| F1' | Major | `LaneMAPollAndHandOffTests.cs:122` (`using var pool = await LaneMAParkedPool.LeaveFree(FreeThreads)` in the hand-off row) | Hand-off row red on UNCHANGED code, cause: `SourceStoreUnavailableException` (its lock not taken within 2 s) thrown at `:150` (`await Task.WhenAll(thirdSteps)`): the 24 first steps and 24 third steps have 500 ms between the release at 1.5 s and the 2 s bound, and the new pin leaves them 8 threads on a loaded box. Measured: full LaneMA batches at head, 70 batches (30 at 4 CPUs, 20 at 2, 20 unset): 2 red, both this row (U4 run 2 at load 22.7 to 26.1; U0 run 7 at load 17.2 to 20.0); 0 red at 2 CPUs. Interleaved, hand-off row alone, 4-CPU pool, same minute, load median about 19: head 7 red of 60, old head ced69979 1 of 60. At load 6 to 10 (the builder's range) it is quiet; at 17 to 30 it is not. Claim "0 red in 90 clean runs" is contradicted at higher load. The builder's own note said the row "needs no starved pool"; the pin it added is the cause of the rise. |
| F2' | Minor | STATUS | "F2 closed, free is a read-back fact" is true for the three rows I ran (read back 8, 12, 24 in every printed line, `busy for other reasons 2`); the hand-off pin is the only place the floor hurt. |
| F3' | Minor | STATUS F3 | Round-1 stage row under m0 now shown red at the default pool by the builder; I saw the existing LaneM5 rows red under m0 at 2 and 4 CPUs (2 of 2 rows with the stage row red in all 3) and the stage row red 3 of 3 at the unset pool (other three existing rows: 1 passed, 3 other reds). Not reproduced by round 1 gate; claim now consistent. Closed. |
| I1 | Info | poll row, clause-5 rows | Closed on my numbers: 0 red in 70 batches of the four rows' classes at 4, 2 and unset (the poll and clause-5 rows never red; old head: poll row red 1 of 40 at 4 CPUs in my run). |
| I2 | Info | kills | m0, m1, m2 (the kit's forms, built 0 warnings) each turn their named rows red 3 of 3 at 4, 2 and unset (27 runs): m0 turns both clause-5 rows red (`.../64 answered later than 2500 ms`, 4 to 7 reds with the existing LaneM5 rows) at every size; m1 turns the poll row red (`16/24 polling steps answered later than 2500 ms (max about 6050 ms)`); m2 turns the hand-off row red (`in 8 to 16/24 stores`). Hand-off row also goes red under m0 and m1 (side effect, as the builder said). |
| I3 | Info | hosted risk | ci.yml runs `dotnet test MpsCalc.slnx` on `ubuntu-latest`; the three test projects may run in parallel, so a loaded runner is likely, not exotic. Hosted flake rate UNMEASURED. |

## What stands and what would close it (this is the cap)
F1' stands. It closes with a change to the hand-off row only, and nothing else:
1. Drop the pin from the hand-off row (take out `using var pool ...LeaveFree` at `:122`, or call it with a free count the row needs: the row asserts order, not thread starvation). The mutant m2 does not need a starved pool. Print `Environment.ProcessorCount` and `ThreadPool.ThreadCount` from the row itself if the print is wanted.
2. Optionally, widen the arrival margin without touching any product threshold: release the held stores at about 1.2 s instead of 1.5 s (the second steps, aged 1 s, have given up at 1 s), so first and third steps have about 800 ms rather than 500 ms.
3. Re-measure the proof the gate used: the hand-off row alone, interleaved against ced69979, 60 each at 4 CPUs at load 17 to 25, 0 red; then the matrix again for m2 3 of 3.

## Claims (STATUS)
true: scope (3 files, no product byte); build 0 warnings; commit message and identity (one address); mutants m0, m1, m2 3 of 3 red at 2, 4, unset; poll and clause-5 rows 0 red; F2 read-back printed; F3 re-measure direction. False: "F1 closed" and "0 red in 90 clean runs" as a statement about the whole LaneMA class (hand-off row red 2 of 70, 7 of 60 interleaved). Not shown: whole Api project at 4 and unset (3641 each): NOT RUN by me.

## Runs (load1 printed per run in the saved logs)
U 4 CPUs 30 runs, 1 red (hand-off). U 2 CPUs 20 runs, 0 red. U unset (18 CPUs) 20 runs, 1 red (hand-off). Base ced69979 poll and hand-off rows at 4 CPUs 40 batches: 1 red (poll 24/24 late, max 2709 ms, the original F1). Head poll and hand-off rows 4 CPUs 40 batches: 0 red. Mutants 27 runs: 27 of 27 red on the named rows. Interleaved hand-off row: old head 1/60, head 7/60.

## NOT RUN
Hosted CI, hosted CodeQL, CodeQL csharp pack (x86_64-only extractor, arm64 box), the whole Api project (W) at head, `git merge-tree` (hook refused; disjoint paths shown instead), a real 2- or 4-vCPU Linux runner. Disclosed deviation: my clone is under the session scratchpad, not `.tools/g1573/clone` (the seat hook refuses git write verbs on a clone under the project tree). Heavy slot 2 held for the whole gate and released (holder moved). Nothing pushed, no PR, no Jira, no deploy.
