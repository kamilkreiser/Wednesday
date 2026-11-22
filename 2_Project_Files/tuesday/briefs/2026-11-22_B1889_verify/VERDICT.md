GATE B1889: GO WITH FINDINGS @ edaa1b7 on main ca94ed9 (second reader)

# Second reader, lane G round 3 (test-only, delta): the A03 helper fix at edaa1b70, re-run by the successor of B1867

Reader B1889 (Opus), in session, 2026-11-22 from 10:28 to 10:45 AEDT. I succeed round-2 reader B1867, and its verdict and `evidence/` are my yardstick. My items:
- commission items 1 to 5;
- kit B1872's bullet "THE DELTA REVIEW, BOTH READERS", without the W02 body cell and mReasonDisposed (Stamp S4 answered Q38 NO);
- "reader B1867 its P13 at the head".

The merge readiness, the landing texts and the deviation rulings (items 6 and 7) belong to B1888. I ran the merge's cheap checks anyway; they are under Scope.

## BLUF
- **GO WITH FINDINGS: one Minor (text), no Major, no Blocker.** The fix holds at the head, and the product is unchanged byte for byte.
- **Determinism.** At the head the A03 loop ran 60 + 40 = **100 runs, 0 failed**. The forcing probe at the head was green 3 of 3: faults 0, the other spool's root reached 0 times of 300, its own spool's root 300 of 300. At HEAD2 the same probe was red 3 of 3 (faults 5, 7, 7, and every completed walk reached the other receiver's spool).
- **HEAD2's own loop read 0 of 40 here, then 0 of 100 more** (MEASURED). The seat read 5 of 40, B1866 12 of 40 and the drafter 0 of 145 (all RELAYED). On this machine the loop is not a red-first instrument; the forcing probe is.
- **Nothing of the receiver or its spool is lost.** The census reads 6 of 6, 52 types and 22 skipped-type fields, of which 4 are non-generated: `ScanReceiver._time`, `JobSpool._time`, `PrintJobSender._time` and `SpoolJob.Gone`. There are exactly 3 SKIP paths (the receiver's clock, the spool's clock, a job's `Gone`). Own objects: 5 by the fixed walk and 5 by the old walk, in 3 of 3 runs; own objects lost: 0.
- **My P13 at the head is green 3 of 3:** secret text 0, raw 0, UTF-8 0; the hash kept 1 time while open and 0 after close. P13b per field is the same as round 2.
- **The property is still caught.** `mUnknownEarly`, `mKeepField` and `mKeepInSpool` each turn A03 red. `mKeepTask` survives (the named limit), and I rule it acceptable.
- **F1 (Minor, text).** My own mutant `mKeepInGone` (the secret's text kept as the state of a callback on the job's `Gone` source) also survives at the head and is red at HEAD2. That limit is not among the named ones.
- **Suite at the head through the lock:** `total: 1524`, `failed: 0`, `succeeded: 1520`, `skipped: 4`. **Hosted:** `HOSTED edaa1b7088baf50f182a01388b1778d645fc29a6: PASS` with `--total 1524 --rules 476`. The control with 1523/475 gives `FAIL 5`, rc 1.

## How it was measured
- **Origin, read by `gh api -X GET` under the project's `GH_CONFIG_DIR` at 10:28:51:**
  - `b1841/wp17-scan-and-print-jobs` = `edaa1b7088baf50f182a01388b1778d645fc29a6`, and main = `ca94ed966ff476d31e2d35cb1ae0cc5c5d4b39b5`.
  - Open pull requests: 0.
  - Check runs of edaa1b70: linux, secret-scan, rules and windows, each completed and success.
  - Lane I's `b1861/wp03-ci-guard-follow-ups` = `ff1defac...` (as the commission says; not my item).
- **Clones.** I made two clones with `git clone --no-hardlinks` from the seat's clone into my session scratchpad (`.../scratchpad/b1889/head` and `.../head2`), both with push URL `invalid://no-push`. They are detached at edaa1b70 (parents `2cfbd9dd...` and `ca94ed96...`) and at 8efae983 (parents `2807d697...` and `8ae5e08c...`). `status --porcelain` printed 0 lines in both at the end.
- **Tools.** The kit's 16 files are copied with `cp -Rc`, and all 16 sha256 values are equal to the source folder and to THE TOOLS table. The controls: `words.py` 13 of 13, `a03loop.py` 3 of 3, `slnx_order.py` 2 of 2.
- **Lock.** Every dotnet job went through the kit's `heavy.py`, unchanged. That made 272 jobs, each a `mkdir` of `.tools/wave1-heavy.lock.d` with `owner.txt`, released by move. All 272 released folders are in my scratch `_quarantine/locks/`, with at most 6 waits (B1888's jobs); see `evidence/gate.log`. When I finished, the lock folder held B1888's `owner.txt`, not mine.
- **Restore.** `--locked-mode -p:NuGetAudit=false` with `CI=true`, rc 0 in both clones, and no lock file changed. `--source-documents` was never run, and no key folder and nothing under `Source_Documents/` was opened.
- **Mutants.** The four kit texts are parsed by program from `3-mutants.txt` (byte-equal), together with my one extra mutant (`evidence/mutant.py`, `mut1.sh`, `mut2.sh`). Each was applied, run in one heavy job, undone, and proved by `cmp` (rc 0) and `git diff --quiet -- src` (rc 0). After the last mutant, both whole solutions were rebuilt (0 warnings, 0 errors). The clean Jobs dll has no mutant marker (lambda marker 0, `KeptTask` 0), and the head loop `green2` (40 runs) came after that rebuild.

## Rulings
| Item | Ruling | Evidence |
|---|---|---|
| Scope `HEAD2..C1` | **Holds.** C1 `2cfbd9dd` has one parent, `8efae983`, and one row, `M tests/Datasec.Suite.Jobs.Tests/ReceiverTests.cs`, numstat `19 2`. **`git diff 8efae983 2cfbd9dd` is byte-equal to `1-a03.diff`** (`cmp` rc 0); a planted control with one extra space differs. I read the file at the head (lines 597-666): the six types, `IsNotOwnState` by `IsAssignableFrom`, and one more clause before `!seen.Add`. A03 (lines 101-146) is unchanged: its assertions at `:128`, `:134`, `:135`, `:139`, `:140`, `:141`, `:145`. | `evidence/HEAD2..C1.diff` |
| C2 changes no lane byte | **Holds.** `git diff C1 C2 -- src/Datasec.Suite.Jobs tests/Datasec.Suite.Jobs.Tests` is 0 bytes (control: HEAD2..C1 over tests, 1,971 bytes). `git diff 8efae983 edaa1b70 -- src/Datasec.Suite.Jobs` is 0 bytes: **no product byte changed**. C2's rows that are not among main's rows since `8ae5e08c`: 0. | |
| The merge (two cheap checks; B1888 owns it) | `git merge-tree --write-tree ca94ed96 2cfbd9dd` gives tree `83d583a5...`, equal to `edaa1b70^{tree}`. `main..head`: 32 A and 1 M (`Datasec.Suite.slnx`, `2 0`); 0 paths outside the lane and the solution file. `slnx_order.py`: `SLNX: ordinal, job lines 1 and 1`. `ls-files`: 476. | |
| Words and gitleaks | **Clean.** `words.py` over the 19 added lines and both commit messages (as read from the commits): `WORDS: clean (3 files)`, rc 0. C1's message equals `commit-message-a03-only.txt`, C2's equals `merge-message.txt`, and both end with the Co-Authored-By line. gitleaks 8.30.1 (`--redact --ignore-gitleaks-allow --exit-code 1`) over those three files plus C1's `ReceiverTests.cs` under neutral names gives rc 0; a planted control (built by program, never printed) gives rc 1. Added lines outside printable ASCII: 0. | |
| A03 loop at the head | **0 failed in 100.** `LOOP green: runs 60, failed runs 0, A03 failures 0, other failures 0, totals ['120']` and, after the mutant rebuild, `LOOP green2: runs 40, failed runs 0, ...`. | `evidence/LOOP-head*.txt` |
| A03 loop at HEAD2 | **0 failed in 140 here:** `LOOP red: runs 40, failed runs 0` and `LOOP red2: runs 100, failed runs 0`. Recorded under Q37, not a finding. The forcing probe below is the red. | `evidence/LOOP-head2*.txt` |
| Forcing probe (kit's text, scratch only) | **HEAD2 red 3 of 3.** Each run reads `total: 121`, `failed: 1`, and the one red is `B1872Force.F1...`. The FORCE lines: faults 5, 7, 7 of 300, every one `Collection was modified; enumeration operation may not execute.`, and every completed walk reached the other spool's root (295, 293, 293). **Head green 3 of 3** (`total: 123`, `failed: 0`): faults 0, other root 0, own root 300 of 300. | `evidence/force-head2.txt`, `probe-head.txt` |
| D34 census and own objects (my item 3) | **No object of the receiver or its spool is lost.** In each of 3 runs: `CENSUS CONTROL ... 6 of 6`; `CENSUS library types 52; skipped-type fields 22; open ... 11`; the 4 non-generated skipped-type fields named above (the other 18 belong to async state machines); exactly the 3 SKIP paths; `OWN OBJECTS ... fixed walk: 5; by the old walk: 5`; `OF THOSE ... 0`. The library objects that only the old walk reached were other tests' objects (`SpoolFileInfo`, `Exchange`, `PrintJobSender`, `JobServiceException`), 5, 0 and 7 across the three runs. My own source search of `src/Datasec.Suite.Jobs/*.cs` found no `.Register(`, `CreateTimer`, `AsyncLocal` or `ThreadLocal` (control `TimeProvider`: 9 lines) and no static field by pattern. | `evidence/probe-head.txt` |
| P13 at the head (my round-2 harness, unchanged, scratch only) | **Green 3 of 3** (`total: 143`, `failed: 0`; all 23 of my round-2 probes are green as well). `D6 P13: reachable strings 4, byte arrays 2; secret text 0, raw 0, UTF-8 0; hash kept 1 while open, 0 after close` (round 2: 537 strings, because its walk reached foreign objects). Collection-changed retries 0, foreign-path lines 0. P13b: `ScanReceiver._spool` strings 4, arrays 1; `JobSpool._jobs` strings 3, arrays 1; `_time` 0 and 0. All equal to round 2. | `evidence/p13-srp-{1,2,3}.txt` |
| Mutants on A03 at the head | `mUnknownEarly`: red, `Assert.Equal() Failure: Values differ` at `ReceiverTests.cs:135`. `mKeepField`: red, `A03: the receiver keeps the secret's text` at `:144`. `mKeepInSpool`: red, same message at `:144`. Each is total 120, failed 1, and A03 is the only red. | `evidence/job-mut-head-*.log` |
| mKeepTask (the named survivor) | **Survives at the head:** an explicit build (dll changed, `KeptTask` present in it), then 120 tests, 0 failed. **Red at HEAD2** (`A03: the receiver keeps the secret's text`), so this is a catch the fix gives up on purpose. **Ruled ACCEPTABLE as a named limit.** The census shows no `Task` field in the library outside compiler-made async state machines, and entering a `Task` is exactly the path that broke A03 (`CancellationPromise`/`AsyncStateMachineBox` derive from `Task`). | `evidence/job-mut2-*-mKeepTask.log` |
| Suite at the head | Whole solution through the lock: **`total: 1524`, `failed: 0`, `succeeded: 1520`, `skipped: 4`**, build 0 warnings and 0 errors. | `evidence/job-all-head.log` |
| Hosted at the head | `hosted.py edaa1b70... --total 1524 --rules 476 --skipped-linux 4 --skipped-windows 19 --unit 60 --floor 60` gives **PASS**, rc 0 (run 44961278314, attempt 1, 4 check runs, 0 beside them). linux 1524/1520/4; windows 1524/1505/19; `RULES: clean (476 files)`; `Ran 60`, floor 60; the secret-scan's planted controls fired, `no leaks found` x3. The control with `--total 1523 --rules 475` gives `FAIL 5`, rc 1. Windows `skipped` lines naming `Jobs.Tests`: 0 (control: 15 lines name Jobs). | `evidence/hosted-head.txt`, `hosted-ctl.txt` |

## Findings
- **F1 (Minor, text/records): the named limits of the skip list leave out one class that I measured.** `mKeepInGone` is my mutant, scratch only. It adds one line in `OpenScan`: `_ = _spool.GoneToken(job).Register(static _ => { }, text);`, which keeps the secret's text as the state of a callback on the job's `Gone` source.
  - **At the head it SURVIVES:** the dll was rebuilt with the mutant (its lambda marker is in the dll, and absent after the clean rebuild), 120 tests, 0 failed.
  - **At HEAD2 it is RED**, with A03's message `A03: the receiver keeps the secret's text`.
  - The kit's FOR RECORDS line names only "a secret's text kept inside a `Task`". Stamp S4 names static fields, async-local values and a host `TimeProvider` subclass. D34 describes `Gone` as holding "only the cancellation callbacks the library's own linked sources register".
  - That description is true of the code today. My search found no `.Register(` in `src/Datasec.Suite.Jobs`, so nothing like this exists in the product.
  - But the general limit is wider than the records say: **the walk now sees no text kept as the state of any skipped object** (a cancellation registration's state, or a timer's state on the clock), not only text inside a `Task`.
  - Not a Major: no product byte changed, and no code path holds such a value. The trade-off is the same one already accepted for `mKeepTask`.
  - **Fix, text only:** add this case to the FOR RECORDS limits (PR body and records). No code change is needed this round.

## FOR RECORDS (not findings)
- (a) The HEAD2 loop failed 0 of 140 on this machine under load1 of about 4 to 7. Its rate depends on which other test classes are mid-receive when A03 walks. The forcing probe reproduced the mechanism 3 of 3 times. So "0 failed in 100 at the head" means something only together with the forcing probe's head result (other root 0 of 300 x 3). DERIVED.
- (b) Stamp S4's control "TimeProvider 10 in src/Datasec.Suite.Jobs": I count 9 occurrences in the `.cs` files (`grep -o`), and 14 with every file under the folder (bin/obj and README included). It is a positive control either way; nothing depends on the exact number.
- (c) My P13 at the head reached only the receiver's own graph in all 3 runs (no foreign path, 0 retries). Round 2's crash in the harness was timing-dependent; the harness is unchanged.

## NOT tested
- The W02 body cell and mReasonDisposed (Stamp S4, Q38 NO: not in this round).
- Kit B1862's eleven mutants and my round-2 mutants other than those named here. The product is unchanged (0 bytes under `src/Datasec.Suite.Jobs` from HEAD2 to the head), and my round-2 probes P07, P10, P14, P15 and P16 ran green at the head inside the P13 runs.
- The merge's restore/build chain, publishes, `release_guard.py`, `repo_rules.py`, `build/tests`, the lane I combined merge, the landing texts and deviations 1 to 6: B1888's items.
- CodeQL: NOT RUN (Tuesday's, at the pull request).
- Linux and Windows locally: only macOS arm64; the hosted legs were read by GET only.
