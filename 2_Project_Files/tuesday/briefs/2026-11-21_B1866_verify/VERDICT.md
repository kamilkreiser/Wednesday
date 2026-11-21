GATE B1866: NO GO @ 8efae98 on main 8ae5e08

Gate G1, round 2 of 2 (delta), whole-lane reader (successor of B1859). OXPd 2, lane G, the job service: fix commit C1
`2807d697992ee51d77792b7d66a1021a54da26de` (one parent 5dd0f859) and merge commit C2
`8efae983b8537d8e2b429a60c2f8d1412cb97f4b` (parents C1 and main `8ae5e08cadf6460f6f87fff091d3bafada2efe41`), branch
`b1841/wp17-scan-and-print-jobs`. Read and measured 2026-11-21, 21:49 to 22:09 AEDT (clocks by `date`), on Opus 5.5,
in the gate's own clones in the session scratchpad (`b1866-clone` for builds and mutants, `b1866-rules` for the rules
reads; cloned from the seat's clone, push URL `invalid://no-push`). Origin read by `gh api -X GET` under the project
GH_CONFIG_DIR at 21:50:11: branch = 8efae983, main = 8ae5e08c, pull requests 11 in all, 0 open, none with head
`b1841/...`; `compare main...8efae983` ahead 3, behind 0, 33 files, the only non-added row `modified
Datasec.Suite.slnx +2 -0`. Every heavy job went through the kit's `heavy.py` (sha256 `31adedc8...`; all eleven kit
tools 11 of 11 equal to THE TOOLS), the wave lock by `mkdir` with `owner.txt`, released by move into
`/private/tmp/b1866-gate/_quarantine/locks/` (58 releases; none left under `.tools/` by this reader); restores with
`-p:NuGetAudit=false`. `repo_rules.py` never got `--source-documents`; no key folder was opened, listed or hashed;
synthetic values only, none printed. Scratch and logs: `/private/tmp/b1866-gate/`. Probe sources, outputs, the mutant
program and its output, the hosted readings and the A03 loops are in `evidence/` beside this file.

**BLUF.** The product delta is right and the round-1 Major is gone: G18, G21, G02 (b), G19 (c)(d), G05 and G13 all read
as the kit expects; 213 of 213 round-1 outcomes are as at round 1 except exactly the F1, F2 and F4 rows, which are now
typed (0 hangs, 0 raw `OperationCanceledException`); 25 of 26 gate mutants red (mReasonDisposed the named survivor on
the lane's cells); the merge holds (`merge-tree` clean, tree = head's tree); suite 1311 failed 0; hosted PASS. **But
one shipped cell is now a flaky red: `ReceiverTests.A03` fails with `InvalidOperationException: Collection was
modified` in 12 of 40 runs of the Jobs test project at the head** (0 of 10 with D21's `CopyAsync` yield removed). The
cause is test-side and traced: A03's reachability walk (`StringsReachableFrom`, `ReceiverTests.cs:144`) now follows
the receive's still-registered `WaitAsync` timer on the test clock into the shared test cancellation token and from
there into OTHER tests' running receivers, whose dictionaries change under it. That is the commission's NO GO class
"a red": **one Major. Product code needs no change; the fix is one test helper.** The whole-solution run (the CI
shape) did not show it: 0 of 16 local runs, both hosted legs green; Tuesday may weigh that (see F1). Two Minors and
records lines besides.

## Findings

| # | Severity | Finding | Recommendation |
|---|---|---|---|
| F1 | **Major** (a red) | **`A03_the_secret_is_compared_in_fixed_time_over_SHA256_and_its_text_is_not_kept` is flaky at the head.** MEASURED: Jobs test project alone, built at the clean head, 40 runs back to back: **12 failed** (only A03, each `System.InvalidOperationException : Collection was modified; enumeration operation may not execute.` at `ReceiverTests.cs:621` from `:144`; evidence/a03-loop-lane-40.txt); with the gate's probes beside it 2 of 20 (evidence/a03-loop-probes-20.txt); during the gate's 43 mutant runs of the Jobs project 3 more times (mJobAad, mCheckOutsideLock run 3, mReasonDisposed). Whole solution: 0 of 15 in a loop plus 1 of 1 (evidence/a03-loop-solution-15.txt); hosted 8efae983 green on both legs. **Attribution, MEASURED:** with mYieldCopy (D21's `CopyAsync` yield removed) A03 failed 0 of 10 runs. **Mechanism, MEASURED** by a path-recording copy of the walk (evidence/GateWalkProbe.cs.txt, 30 rounds x 10 runs, 87 walks met a changing collection; evidence/a03-walk-paths.txt): `ScanReceiver > _time:ManualClock > _timers > ManualTimer > CancellationPromise > registration > ... Linked2CancellationTokenSource > ... CancellationPromise > AsyncStateMachineBox > <CopyAsync> > <>4__this:ScanReceiver > _spool:JobSpool > _jobs:Dictionary` (and `_scans`). Before D21 the copy of a synchronous body finished before `WaitAsync`, so no timer existed; now the copy is pending when `WaitAsync` is called, its timer is still on the test clock when the walk runs, and its cancellation registration sits on `TestContext.Current.CancellationToken`, which every running test shares, so the walk reaches other tests' receivers. The product's behaviour is the intended D21 behaviour; A03's two new assertions (one comparison for an unknown job and a closed scan) are not the cause. | Test-only, one helper: make `StringsReachableFrom` not follow into `TimeProvider`, `Task`, `CancellationTokenSource`/`CancellationTokenRegistration` and `ExecutionContext` objects (none is the receiver's own state), or run the walk over the receiver's own fields only; then a loop of 40 Jobs-project runs, 0 failed. If Tuesday rules that a red seen only in project-level runs (never in the CI shape) is not the NO GO class, this row grades down to Minor (cells) and the verdict reads GO WITH FINDINGS; the gate did not write landing texts because its own reading is NO GO. |
| F2 | Minor (text) | **mReasonDisposed does not survive "by construction".** The kit (D22, D27 (b)) and STATUS say D22's general-catch line is reached only in a race. MEASURED (probe G22): a caller's body whose read throws `ObjectDisposedException` reaches it on one thread, every time: the receive ends `JobNotFound` (an `IOException` body ends `ScanRefused`), and under mReasonDisposed that row reads `ScanRefused`. So the survivor is a missing cell, not a limit; and a body (a caller's stream, not the spool) that throws `ObjectDisposedException` now gets `JobNotFound`, which the README gives only to a disposed spool. Typed either way; no product fault (the job is wiped by `Fail`, so "not found" is true afterwards). | Records line, or one W02 row: a body that throws `ObjectDisposedException` ends `JobNotFound` (kills mReasonDisposed). |
| F3 | Minor (records) | **A good answer whose close never completes ends `ResponseTimedOut` at the send bound.** MEASURED (G22): the printer's job id is read, `DisposeAsync` never returns, the call ends `ResponseTimedOut` at 30 minutes (bounded, typed). README: "An answer stream that fails to close changes nothing" is true of a close that throws (G22: a close throwing `IOException` returns the value), not of one that hangs; a caller that retries would print twice, the cost D20 named. | One README Limits clause, or records. |
| F4 | Records | The README's `ObjectDisposedException` list is exact for the named members (G22 and G13, below); the async and byte forms (`ReadAsync`, `ReadByte`, `WriteAsync`, `WriteByte`, a writer's `DisposeAsync`) throw it too through `Read`, `Write` and `Dispose`; not separately named. `GUARD-WARN: development CA deny-list holds 0 fingerprints (owed)` is tracked: `<project>/BACKLOG.md:13-15` (owed item 2) names that exact line. | Records only. |

No Blocker. No text names a person, a ticket, a brief or says anyone decided anything (words scan, section 7).

## 1. What the kit's FOR TUESDAY section gives this reader, re-run at 8efae983

Probe file: round 1's `GateProbeTests.cs` unchanged but its output name, plus one new test G22 (evidence/
GateProbeTests.cs.txt), run inside the lane's test project, then moved to quarantine (`status --porcelain` 0 lines
after). Run p-test: total 138 (120 + 18), the 18 probe tests passed; A03 failed in that run (F1).

| Row | Expected (kit) | Measured at the head |
|---|---|---|
| G18 answer stream throws its own OCE | `TransportFailed` | `TransportFailed`, fixed message, no inner; "rows differing from the property: 0" |
| G18 transport throws its own OCE | `TransportFailed` | `TransportFailed` (unchanged) |
| G21 every poll's answer throws its own OCE | `TransportFailed` after three polls | `TransportFailed` |
| G02 (b) body whose read blocks its thread | `ReceiveTimedOut`, no hang | `ReceiveTimedOut` with the clock moved 20 min, returned before the body was freed: True; after the free still `ReceiveTimedOut` |
| G19 (c) transport blocks its thread | `ResponseTimedOut` | `ResponseTimedOut` (clock moved 31 min), and after the free |
| G19 (d) answer stream blocks its thread | `ResponseTimedOut` | `ResponseTimedOut`, and after the free |
| G05 spool cap exact over two jobs | unchanged | job A 1000 value, job B 500 value, +1 `SpoolFull`, reserved 1000 then 0 |
| G13 spool disposed under a receive | `JobNotFound` | `JobNotFound`, fixed message, no inner |
| G13 reader, writer, writer `Dispose`, `WipeJob` after spool `Dispose` | `ObjectDisposedException` as the README lists | `ObjectDisposedException` x4 |

**The 213 round-1 outcomes** (program comparison of the two output files, random bit-flip offsets normalised): 376 lines
both; the only differing lines are the F1 rows (G18, G21), the F2 rows (G02 (b), G19 (c), G19 (d), each also "after
free") and the F4 row (G13 spool disposed). Tally now: 35 values, 172 `JobServiceException` (172 of 172 with the fixed
message and no inner), 6 other, 0 hangs (round 1: 35 / 166 / 9 / 3). The 6 others are the four G13 disposed-spool rows
the README lists, the caller's own token cancelled (`TaskCanceledException`, allowed) and the test-seam row (delete
hook made to throw a non-I/O exception). G17's 40 random flips: 40 `SpoolCorrupt`, every handed-out count a prefix of
whole verified chunks.

**G22 (the delta's own shapes, 29 rows):** body throwing `ObjectDisposedException` = `JobNotFound`, `IOException` =
`ScanRefused`, folder gone and reserved 0 both (F2); receive on a spool disposed before the upload = `JobNotFound`;
`CloseScan`, a second `Dispose`, `LastStart` after dispose = values; `OpenScan`, `ListFiles`, `OpenRead`, `OpenWrite`,
`WipeSession`, `Sweep`, `CreateJob` on a disposed spool = `ObjectDisposedException` (all named by the README); reader
`ReadAsync`, `ReadByte` and writer `WriteAsync`, `WriteByte`, `DisposeAsync`, `Dispose` of a disposed spool =
`ObjectDisposedException` (F4); reader `Dispose` = value; a send whose document is a reader of a disposed spool =
`TransportFailed`; a good answer whose close throws `IOException` = value; whose close never completes =
`ResponseTimedOut` at the send bound, not before (F3); the caller's token cancelled while the answer read blocks =
`TaskCanceledException` (allowed).

## 2. Scope (C1, C2)

- C1 = `git diff 5dd0f859 2807d697`: exactly the seven files (`PrintJobSender.cs` +21 -4, `README.md` +24 -7,
  `ScanReceiver.cs` +20 -3, `SpoolFileReader.cs` +16 -1, `HardeningTests.cs` A +465, `ReceiverTests.cs` +12,
  `SenderTests.cs` +4); no project, lock, solution or other file. The src part is byte-equal to the kit's `1-code.diff`
  (`cmp` equal). 562 added lines, 0 outside printable ASCII (a planted U+200B counts 1).
- No cell weakened: the two changed round-1 cells only ADD (A03: the unknown-job and closed-scan comparisons; J08 send
  bound: one `Guard.Signal` before reading `Tokens[0]`).
- C2: `git diff 2807d697 8efae983 -- src/Datasec.Suite.Jobs tests/Datasec.Suite.Jobs.Tests` 0 bytes (control: the
  same against 5dd0f859 36242 bytes); paths C2 changes against C1 outside main's change list since 762e774e: 0.
  `main..head`: 32 `A` (round 1's 31 plus `HardeningTests.cs`, by `comm`) and 1 `M`, `Datasec.Suite.slnx` 2 / 0; the
  two lines directly after `src/Datasec.Suite.Graph/...` (line 7) and `tests/Datasec.Suite.Graph.Tests/...` (line
  19); both groups ordinal-sorted (True, True; control with a planted out-of-order line False).
- Census (D19), by program over the 14 library files: HEAD1 28 `catch`, 16 with `when`; head 32 and 18 (control line
  counts 1). `ForceYielding`: 3 (sender 2, receiver 1).
- Read whole: the four changed product files and the delta of the three test files; `JobSpool.cs` and
  `SpoolFileWriter.cs` read whole for the exceptions paragraph.

## 3. The README's exceptions paragraph against the code

Named, and measured throwing `ObjectDisposedException`: `CreateJob`, `OpenWrite`, `OpenRead`, `ListFiles`, `WipeJob`,
`WipeSession`, `Sweep` of a disposed spool (each `ObjectDisposedException.ThrowIf(_disposed)`, directly or through
`TryLive`); a writer's `Write` (through `Reserve`) and `Dispose` (through `Complete`, `Seal`, `EnsureLive`); a reader's
`Read` (through `EnsureLive`, after the sticky check); a writer or reader already disposed itself (`ThrowIf(_closed)`);
`ScanReceiver.OpenScan` (through `CreateJob`). Not throwing it, and not named: `Dispose`, `LastStart`, `ToString`, a
reader's `Dispose`, `CloseScan`, `ReceiveAsync` (now `JobNotFound`: `Probe` returns false on a disposed spool, `Fail`
and `GoneToken` map it), the sender (a disposed document maps to `TransportFailed`). **Omitted: none** but the
async/byte forms that route through the named members (F4). "A receive whose spool is disposed before or during the
upload ends with `JobNotFound`": both measured (G22, G13). True as written; F2 adds the caller's-body case.

## 4. Mutants (gate's own program on PRODUCT code of the head; each one heavy job, `dotnet test` of the Jobs test project which builds first, 120 cases, no probe file; undone by restoring the bytes, proved by `git diff --quiet` rc 0 AND `cmp` against a pre-mutant copy True, every time)

| Mutant | RED (by assertion) |
|---|---|
| mFinal | S03 x2 |
| mNonce | S04 |
| mJobAad | S05 (A03 also, the F1 flake) |
| mRelease | 11: S02, S02 sticky, S03 x4, S04, S05 x2, L01 |
| mSpoolCap | **C06 exact and C06 free race** (survived at round 1; F3 of round 1 closed) |
| mSecret | A03 (assertion `Values differ`) |
| mOracle | A02, T03 |
| mBusy | A05, L01 |
| mTimeout | T01 x2, T01 blocking, L01 |
| mPartial (re-made for the new `Fail`) | 18 (C01-C06, T01, T01 blocking) |
| mZero | K01, P02, W02, W03 |
| mWipeOrder | P02, W02, W03 |
| mStart | R01, P02 |
| mAttr | J02 x3 |
| mReqId | J06, Y03 |
| mState | J06 x2, Y03 |
| mReadBound | J08, J08 blocking answer |
| mF1 | J09 send, J09 track |
| mClose | J09 close x2 |
| mYieldRun | J08 blocking transport |
| mYieldRead | J08 blocking answer |
| mYieldCopy | T01 blocking (10 of 10 runs; A03 0 of 10: F1's attribution) |
| mFailDisposed | W02 disposed |
| mStickyOwn2 (own form: `SpoolCorrupt` no longer recorded, `StorageFailed` still) | S02 sticky x2 |
| mCheckOutsideLock | C06 free race, **7 of 7 runs** (1 + 6) |
| mReasonDisposed | lane cells: **NONE (survived)**; with probe G22 present: the ODE-body row flips `JobNotFound` -> `ScanRefused` (F2) |

Round-1 list 17 of 17 re-made (mPartial re-made for the new `Fail`), the kit's seven plus mSticky in an own form, and
mReasonDisposed: 25 of 26 red on the lane's cells, the named survivor killable by a deterministic input (F2). (A first
own form of mSticky, the capture line removed, does not compile: CS0649 under warnings-as-errors; not counted.) After
the last undo: `git diff --quiet` rc 0, the whole solution rebuilt (`0 Warning(s)`, `0 Error(s)`) before every green
claim below.

## 5. Suite, merge, rules, hosted

- At the head, through the lock: `dotnet restore Datasec.Suite.slnx --locked-mode -p:NuGetAudit=false` with `CI=true`
  rc 0, 0 lines naming `http`, `status --porcelain` 0; build `0 Warning(s)`, `0 Error(s)`; `dotnet test -c Release
  --no-build`: `Passed!`, **`total: 1311`, `failed: 0`**, `succeeded: 1307`, `skipped: 4`. After the mutants, rebuilt
  0/0 and 15 more whole-solution runs: 15 of 15 `total: 1311`, `failed: 0`.
- **The merge:** `git merge-tree --write-tree 8ae5e08c 8efae983` rc 0, tree `326d668f78c4213a537cd88fe5855cdde1feb09f`
  = `8efae983^{tree}` (no further resolution). Control: `merge-tree 2807d697 8ae5e08c` prints `CONFLICT (content):
  Merge conflict in Datasec.Suite.slnx` (the one the seat resolved).
- `build/repo_rules.py <clone>` (no option; no sibling `1_Project_Definition`): `R5 hash half NOT RUN`, **`RULES: clean
  (402 files)`** rc 0 (ls-tree 402 = main 370 + 32). `unittest discover -s build/tests`: **`Ran 60 tests`**, `OK`.
- Hosted run 44895751397 of 8efae983 by GET (`hosted.py` R5-aware, sha256 `e73339f3...`, `--total 1311 --rules 402
  --skipped-linux 4 --skipped-windows 19 --unit 60 --floor 60`): four jobs success, attempt 1, 0 other runs; linux
  `total: 1311` x2, `succeeded: 1307`, `skipped: 4`, `GUARD: clean (10 files)`; windows `total: 1311` x2, `succeeded:
  1292`, `skipped: 19`, `GUARD: clean (11 files)`; both 0 warnings 0 errors; secret-scan both PLANTED-CONTROL lines,
  `objects of this commit not among them 0`, `no leaks found` x3; rules `Ran 60 tests in`, `UNIT-TEST FLOOR: ran 60,
  floor 60`, `RULES: clean (402 files)`. **`HOSTED 8efae983...: PASS`** rc 0; control `--total 1312`: `FAIL 4`. Windows
  log: 0 skipped lines naming a Jobs test (control: 9 name `KeyRing`). Each publish leg holds the `GUARD-WARN` line once
  (F4, tracked).
- CodeQL: NOT RUN (no Analyze on a branch push; C# extraction cannot run on this arm64 machine).

## 6. The seat's deviations (STATUS DEVIATIONS 1 to 6)

1. A no-op `builtin cd` in a subshell while hashing: **accepted as records** (no file changed; this gate re-hashed the
   eleven tools: 11 of 11 equal).
2. Five product files in the pre-mutant copy, not four: **accepted** (`JobSpool.cs` is where mSpoolCap and
   mCheckOutsideLock act; this gate kept five too).
3. `RULES: clean (360 files)` before staging, 361 after; `unittest` first call in the wrong form: **accepted** (the
   program counts tracked files; this gate measured 402 at the merged head and `Ran 60`).
4. mYieldRun's whitespace in the mutant only: **accepted** (the head's src delta is byte-equal to `1-code.diff`).
5. mCheckOutsideLock run once: **re-run by this gate 6 more times: 7 of 7 red on C06 free race** (failed 1 each, once
   with the A03 flake beside it). Accepted.
6. main moved to 8ae5e08c before the merge: **accepted** (D30's last sentence; the merge measured clean above; 1311 =
   1191 + 120, 402 = 370 + 32).

## 7. Texts

`words.py --control`: `CONTROL FIRED: 13 of 13`. Over the 562 added lines of C1 and both commit messages:
`WORDS: clean (3 files)`. Both messages equal the kit's files (but git's trailing blank line), each ending in the
attribution line. gitleaks 8.30.1 (`--no-banner --redact --ignore-gitleaks-allow --exit-code 1`): planted control
(built by program from two halves, never printed) rc 1; the added lines and both messages under neutral names rc 0;
`src/Datasec.Suite.Jobs` and `tests/Datasec.Suite.Jobs.Tests` at the head rc 0 each. README: D19 to D23 each stated;
untrue or incomplete sentences: none false, F3 one clause short.

## 8. Landing texts

NOT WRITTEN: item 7 is for GO or GO WITH FINDINGS only. If Tuesday grades F1 down (its last sentence), they can be
written against the same head without a further measurement.

## 9. What was NOT tested

- Linux and Windows locally (macOS arm64 only); the gate's probes and the A03 loops ran here only; the hosted legs
  ran the lane's cells once each.
- CodeQL; the R5 hash half; the two publishes locally (the hosted GUARD lines were read instead).
- A fix for F1 (the helper change is a recommendation, not measured).
- B1867's points (P07, P10, P14 to P16 and its six mutants) beyond the shared mutants above.
- A real transport, a device, what HP's devices send.
