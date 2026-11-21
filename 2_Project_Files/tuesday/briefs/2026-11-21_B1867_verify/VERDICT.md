GATE B1867: GO @ 8efae98 on main 8ae5e08 (second reader)

# Second reader, round 2 of 2 (the delta): P07, P10, P14, P15, P16 and the six mutants of round 1, re-run at the fix-round head

Reader B1867 (Opus), in session, 2026-11-21 21:49 to 22:05 AEDT. I am the successor of round-1 reader B1860. My yardstick is `2026-11-21_B1860_verify/VERDICT.md` and its `evidence/`. My items are the kit B1862 section "FOR TUESDAY: THE ROUND-2 DELTA REVIEW", the "Both" line and the "Reader B1860" line, plus the commission's items 2, 3, 4 and 6 (deviation 5). The merge measurement (item 5) belongs to B1866. I ran the two cheap checks of it anyway: they are under Scope.

## BLUF
- **GO. No Blocker, no Major, no Minor.** Round 1's F1, F2 and F3 are closed, and each is now held by a builder cell that my mutants turn red.
- **F1 is closed (D23, a refused reader stays refused).** P07 handed out 0 bytes after the first `SpoolCorrupt` in both shapes, on every run (head-1 to head-13). Round 1 handed out 2,548. My own mutant `mNotSticky` (the refusal not recorded) brings round 1's 2,548 back, and it turns both the builder's S02 cases and P07 red.
- **F2 is closed (a free-race cell for the spool cap).** `mCheckOutsideLock` was run **8 times. All 8 runs turned the builder's `C06_writers_released_together_never_pass_the_spool_cap_over_100_iterations` red by assertion**, and P14, P15 and P16 were red too (8 of 8 each). The seat ran it once (deviation 5): **the seat's claim holds**.
- **F3 is closed (A03 extended).** `mUnknownEarly` turns the builder's A03 red by assertion (`Assert.Equal() Failure`, `Expected: 3`), as well as P10.
- **D2, D6 and C06 are unchanged at the head.** P10: 22 kinds, 1 reason, 1 message, 1 throw site. P14: 200 x 6. P15: 300 x 8. P16: 200 x 6. Each iteration count was printed, the results match round 1, and all six of round 1's mutants are still red.
- **Suite:** 1311, failed 0, skipped 4 (local, through the lock). **Hosted run of 8efae983:** PASS. The control with 1310/401 gives FAIL 5.

## How it was measured
- **Clone.** I cloned with `git clone --no-hardlinks` from the seat's clone into my session scratchpad (`.../scratchpad/b1867/clone`). Push URL `invalid://no-push`. Detached at `8efae983b8537d8e2b429a60c2f8d1412cb97f4b`: its parents are `2807d697...` (C1) and `8ae5e08c...` (main), and C1's one parent is `5dd0f859...`. I re-read by `gh api -X GET` under the project's login at 21:50:00: branch = `8efae983...`, main = `8ae5e08c...`.
- **Lock.** Every dotnet job went through the kit's `heavy.py`, copied unchanged (sha256 `31adedc8...`). There were 29 jobs, one heavy job each: load first, `mkdir` of `.tools/wave1-heavy.lock.d` with `owner.txt`, released by move. All 29 released folders are in `/private/tmp/b1867-gate/_quarantine/locks/` (`evidence/gate.log`). Lock waits were between 0 and 8 (other seats); a wait is not a finding.
- **Restore.** `--locked-mode -p:NuGetAudit=false` with `CI=true`, rc 0. Afterwards `git status --porcelain` printed nothing (before my probe file went back), so no lock file changed. `--source-documents` was never run, no key folder was opened, and every value was synthetic. Nothing printed holds a value: the evidence was scanned for 43-character base64url runs and 64-hex runs (0 hits; a planted 43-character control counts 1) and by gitleaks (rc 0).
- **Probes.** Round 1's `SecondReaderProbes.cs`, scratch only and never committed. The final text is in `evidence/SecondReaderProbes.cs.txt`. I changed it in two ways, both in the harness and neither in an assertion (see Harness note):
  - P13's reflection walk now retries a collection that another thread changes under it, and it skips `ExecutionContext`.
  - I added P13b, which reports per field and asserts nothing.
- **Runs of the Jobs test project** (Release, build 0 warnings and 0 errors each time):
  - head-1 to head-3 (round-1 probe text unchanged): 142 tests, failed 1. The one red was P13 crashing with `InvalidOperationException: Collection was modified` inside my own walk. It is not a product red; see Harness note.
  - head-4 to head-13 (final text): 142 or 143 tests, **failed 0**. head-12 and head-13 come after the last mutant undo.

## Rulings (the delta)
| Item | Ruling | Evidence |
|---|---|---|
| **P07** (expected 0 bytes after the first refusal, both shapes) | **Holds.** "five junk bytes before the header": 0 bytes; "a junk record after the header": 0 bytes. Same on head-9, head-10, head-11 and every other run. **Round 1: 2,548 and 2,548.** In the code, `SpoolFileReader.Read` checks `_refused` after `ThrowIf(_closed)` and before `EnsureLive` (`SpoolFileReader.cs:69-73`). `_refused` is set only by a `SpoolCorrupt` or `StorageFailed` from `NextChunk` (`:88-96`). Both `Read(byte[],..)` and both `ReadAsync` forms go through `Read(Span)`. | `probe-out-head-{9,10,11}.txt`, `job-mNotSticky-2.log` |
| **P10** (22 kinds, one reason, exactly one comparison each) | **Holds, unchanged.** `failure kinds 22; distinct reasons 1; distinct messages 1; distinct throw sites 1`. The one throw site is `ScanReceiver.Authenticate` at `ScanReceiver.cs:171`, the same line as round 1. P10's per-call comparison count is still exactly one; the test is green on every run. P10b: 500 wrong secrets left the live scan open and its file in place. P11's medians (reported, not ruled) are 5.2 to 5.5 us. | same |
| **A03 extended** | **Holds.** It asserts 3 comparisons after an unknown job (a job with no scan) and 4 after a closed scan, and `Assert.All(calls, (32, 32))`. It goes red under `mUnknownEarly`. | `job-mUnknownEarly-1.log` |
| **P14** (200 x 6 receives, cap 300,000) | **Holds, unchanged.** Accepted 539 / 528 / 533, `SpoolFull` 661 / 672 / 667. Highest reservation sampled: 299,991 / 299,996 / 299,963. Reservation 0 after the wipes every time. | head-9/10/11 |
| **P15** (300 x 8 writers, cap 200,000) | **Holds, unchanged.** Never past the cap. The reservation equalled the bytes taken. Largest unfilled remainder: 836 / 840 / 924. Refusals: `SpoolFull 2400` only. Reservation 0 after the wipes. | same |
| **P16** (200 iterations, 6 writers racing `WipeSession` and `WipeJob`) | **Holds, unchanged.** Lowest sample 0, highest 399,976 against a cap of 400,000, reservation 0 at the end every time. | same |
| **D6 P13** (no secret text kept; the hash cleared at close) | **Holds.** Secret text 0, raw bytes 0, UTF-8 bytes 0. The hash was kept once while the scan was open and 0 times after `CloseScan`. The walk now reaches far more objects, other tests' objects included (see Harness note), so the 0 and the 1 hold over a larger graph than in round 1. | same |

## The six mutants of round 1, at the new head (each applied by `evidence/mutant.py`, one heavy job, undone, proved by `git diff --quiet -- src` rc 0)
| Mutant | Red by assertion: builder cells | Red: my probes | Round 1's builder reds |
|---|---|---|---|
| mLenientFinal | S03 cut-or-extended; S03 cut at a full final chunk | P02 | the same |
| mNonceNoFile | S04 nonce | P08 | the same |
| mUnknownEarly | **A03 (new, F3 closed)** | P10 | none |
| mWrongCloses | A02, L01 | P10b, P12, P13 | the same |
| mCheckOutsideLock | **C06 free race (new, F2 closed): 8 of 8 runs** | P14, P15, P16: 8 of 8 each | none |
| mForgetLeak | C06 exact (new), C06 free race (new), ReceiverTests C06 two uploads | P14, P15, P16 | ReceiverTests C06 only |
| **mNotSticky** (my own, D23) | **S02 both shapes** | P07 (2,548 bytes back in both shapes) | (new in this round) |

**`mCheckOutsideLock` repeated (deviation 5):** I ran it as runs 1 to 8, each a separate heavy job. Each printed `total: 143`, `failed: 4`, and each named the free-race cell, P14, P15 and P16. The free-race cell's first assertion was `C06 race: the sampled reservation passed the spool cap` in 7 runs and `C06 race: the writers together passed the spool cap` in 1. Control: the same count on head-11's log is 0. The mutant text is byte-equal to `3-mutants.txt`'s block.

**One false start, named:** `mNotSticky-1` used `_ = ex.Reason;`. That fails the build with CS0649, which the project treats as an error. My first `run.sh` then ran the stale binaries anyway: those were the binaries of `mCheckOutsideLock-8`, so it showed C06 reds. **That run is void.** I fixed `run.sh` to refuse a test run after a failed build. I made the mutant `_refused = null;` and re-ran it as `mNotSticky-2`: build rc 0, reds S02 x2 and P07. head-12 and head-13 rebuilt the head: green. Every other mutant run printed `build rc 0` (`evidence/job-*.log`).

## Scope, census, texts (the "Both" line, commission item 2)
- **C1 = exactly the kit's seven files:** `M` PrintJobSender.cs, README.md, ScanReceiver.cs, SpoolFileReader.cs, ReceiverTests.cs, SenderTests.cs; `A` HardeningTests.cs. Files outside the lane's two folders: 0. Control: the same filter over `5dd0f859..8ae5e08c` counts 45. No `.csproj`, lock file, `.props` or `.slnx` in C1 (0).
- **C2 changes no lane file:** `git diff 2807d697 8efae983 -- src/Datasec.Suite.Jobs tests/Datasec.Suite.Jobs.Tests` = 0 bytes. Control: C1 against HEAD1 over the same paths = 13,071 bytes.
- **`main..head`:** 32 `A` rows under the lane's two folders and 1 `M Datasec.Suite.slnx`, numstat `2 0`. Paths outside the lane and the solution file: 0. The `src/` line sits directly after `Datasec.Suite.Graph` (line 7) and the `tests/` line directly after `Datasec.Suite.Graph.Tests` (line 19). Both groups are in ordinal order by program (10 and 9 names); a reversed control list reads not ordinal.
- **The merge, two cheap checks (B1866 owns this item):** `git merge-tree --write-tree 8ae5e08c 8efae983` rc 0, tree `326d668f...`, equal to `8efae983^{tree}`.
- **The census of D19:** 14 library `.cs` files. **28 `catch` sites at HEAD1 (16 with `when`) and 32 at the head (18 with `when`)**, counted by program. This equals the kit and the STATUS.
- **`words.py`** (`--control`: 13 of 13) over the 562 added lines of C1, the 2 added lines of C2 and both commit messages: `WORDS: clean (4 files)`, rc 0. **gitleaks 8.30.1** over the same four files under neutral names: rc 0, `no leaks found`. The planted control (built by program, never printed) gives rc 1. Both messages are true to their commits and end with the Co-Authored-By line.

## The README's exceptions paragraph against the code (commission item 3; read from source)
**Named, and true** (each checked at its site):
- `JobSpool.CreateJob` (`JobSpool.cs:97`).
- `OpenWrite`, `OpenRead`, `ListFiles` (through `TryLive`, `:404/:410`).
- `WipeJob` (`:202`), `WipeSession` (`:224`), `Sweep` (`:241`).
- A writer of a disposed spool: `Write` (through `Reserve`, or `Seal`, then `EnsureLive`); a writer's `Dispose` (through `Complete`, `Seal`, `EnsureLive`; not caught by `Complete`'s two catches, so it leaves `Dispose`).
- A reader of a disposed spool: `Read` (through `EnsureLive`).
- A writer or reader already disposed: `ThrowIf(_closed)` (`SpoolFileWriter.cs:74`, `SpoolFileReader.cs:68`).
- `ScanReceiver.OpenScan` (through `CreateJob`).
- A receive whose spool is disposed gives `JobNotFound` on all four routes: `Probe` returns false (`JobSpool.cs:294`); `GoneToken`'s ODE is caught (`ScanReceiver.cs:192`); an ODE or the job's `Gone` cancellation inside the copy is caught (`:232`); `Fail`'s `WipeJob` ODE is swallowed (`:286`). The builder's W02 holds the receive, `CreateJob`, `WipeJob`, a reader's `Read`, a writer's `Write` and its `Dispose`.

**Members that throw it and are not named one by one:** only forms of the named members.
- `ReadAsync` and `WriteAsync` (both overloads each) call `Read` and `Write` and throw the same exception synchronously.
- The `Stream` base members (`ReadByte`, `WriteByte`, `CopyTo`, `CopyToAsync`) go through them too.

**Members that do NOT throw it, correctly not named:**
- `JobSpool.Dispose` (idempotent), `ReservedBytes`, `LastStart`, `ChunkBytes`; `ScanReceiver.CloseScan` (it does not touch the spool).
- A reader's `Dispose`; a writer's `Flush` (it does nothing).
- `PrintJobSender`: a document stream that throws an ODE becomes `TransportFailed` through `DocumentFailure` (`PrintJobSender.cs:189-193`).

**No member that throws `ObjectDisposedException` is missing from the paragraph.** One nuance goes to FOR RECORDS (b).

## Suite and hosted (commission item 4)
- **Local whole solution at the head, through the lock (`all-1`, my probe file moved out first):** restore rc 0, build 0 warnings and 0 errors, **`total: 1311`, `failed: 0`, `succeeded: 1307`, `skipped: 4`**.
- **Hosted, by GET:** `hosted.py 8efae983... --total 1311 --rules 402 --skipped-linux 4 --skipped-windows 19 --unit 60 --floor 60` gives `HOSTED 8efae983b8537d8e2b429a60c2f8d1412cb97f4b: PASS`, rc 0 (`evidence/hosted-8efae983.txt`).
  - Four check runs: success, attempt 1, 0 runs beside them.
  - linux: 1311 / 1307 / 4. windows: 1311 / 1292 / 19.
  - `RULES: clean (402 files)`, `Ran 60 tests`, `UNIT-TEST FLOOR: ran 60, floor 60`.
  - The secret-scan's planted controls fired.
  - Control with `--total 1310 --rules 401`: `FAIL 5` on the four total and succeeded rows and the rules row, rc 1 (`evidence/hosted-control-1310.txt`).

## The seat's deviations (commission item 6; B1867 owes 5 at least)
- **Deviation 5 (mCheckOutsideLock run once): ruled, no finding.** Re-run 8 times (see the mutant section above): 8 of 8 red on the builder's free-race cell, by assertion. The kit's "8 of 8" now holds on my runs as well.
- I also read deviations 1 to 4 and 6. Their rulings are B1866's. Nothing in my items contradicts them: my `main..head` and the hosted totals (1311 and 402) confirm 6.

## Findings
None at Minor or above.

## FOR RECORDS (not findings)
- **(a) Harness note: my P13, not the product.** At the head, round 1's reflection walk in P13 reaches other tests' objects. The path, printed by program in `probe-out-head-8.txt` and `-9.txt`: `ScanReceiver._time` (the TEST fake `ManualClock`) holds `_timers`; a `ManualTimer`'s state is a `CancellationPromise` of a `WaitAsync`; its registration is a `CallbackNode` on the test runner's one shared token; the next node belongs to other in-flight tests' linked token sources and `CopyAsync` state machines.
  - So head-1 to head-3 crashed inside my walk (`Collection was modified`) while another test changed its own `_scans`.
  - The fake clock keeps its timers; `TimeProvider.System` does not. The extra reach comes from the test fake and the shared test token, never from a field of the receiver or the spool. P13b reports each field on its own: at most 4 strings, 1 array, the same as round 1.
  - DERIVED: round 1 did not see this because the receive then ran without `ForceYielding`; not measured.
- **(b) Order of checks on a refused reader or a broken writer.** A reader that has refused its file throws its `SpoolCorrupt` (or `StorageFailed`) on every later `Read`, even after its job is wiped or its spool is disposed, because the `_refused` check comes before `EnsureLive`. A broken writer likewise throws its broken reason before `Reserve`. Both are typed `JobServiceException`s, so the README's "only these exceptions" property holds. Read the paragraph's list as where an `ObjectDisposedException` CAN come from, not where it always does. DERIVED from source; not probed.
- (c) The A03 "unknown job" is a spool job with no scan. P10 also covers the default id and another spool's job: one comparison each.
- (d) Round 1's FOR RECORDS (a) to (d) stand as the kit relays them; nothing in this round changes them.

## NOT tested
- `StorageFailed` sticky (Q33: the same line, no cell). I could not cause an `IOException` from the file under the reader; it is DERIVED from `SpoolFileReader.cs:92`.
- Windows and Linux locally: only macOS arm64. The hosted legs were read by GET only.
- The merge's restore/build chain on its own, `repo_rules.py`, `build/tests` and the whole B1859 list (G18, G21, G02 (b), G19 (c)(d), G05, G13, the 213 outcomes, the seat's mutants mF1 to mSticky): B1866's items.
- The landing texts and the release guard's `GUARD-WARN` line: B1866's items.
- Timing at the machine level (P11 is an in-process median). Two processes over one root. The key in swap.
- CodeQL: NOT RUN.
