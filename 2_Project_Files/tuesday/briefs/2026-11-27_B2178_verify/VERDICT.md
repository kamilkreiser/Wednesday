GATE B2178: GO WITH FINDINGS @ 09b6050 on main 760e1a6

Gate G1, ROUND 1 OF 2 of lane OX-C kit 2 part 2 (owed 137, the Server tests' per-cell bound on the host's start and
stop; owed 121, the README-line option), one Opus reader (claude-opus-5-5), in-session, read-only, for Tuesday s335.
Kit B2170 (seat X89; stamp S4: Q1 "a" and Q3 "a" in words, Q8 S4 re-frozen as one clock and one question, every
other Q the default; S8 the canonical runner 31adedc8; every choice the coordinator's, none the product owner's).
Head `09b605070263d863b72043b7a2e48e781b5e4998` on `b2170/lane-c-kit2-part2-r2`, ONE commit, one parent = main
`760e1a644ce9a419cf1b9132d0776e9e5eac1cac` (PR 58's squash), tree `760295e34a25342af686251b9d72f69e549f6959`, 679
files. Main and the branch did NOT move during the gate (gh api -X GET at 21:53:57 and 22:07:04 AEDT; open pull
requests 0 both times; open code-scanning alerts 0). Measured 2026-11-27 21:53 to 22:07 AEDT in my scratch
`fleet/state/s335/g2178/`: `clone` (clone.py draft: push URL `invalid://no-push`, no identity, detached at the head;
the seven mutants ran here) and worktree `probe` (the head plus ONE probe file of mine,
`tests/Datasec.Suite.Server.Tests/GateProbeTests.cs`, seven cells, never committed, never pushed). Every heavy job
through my copy of the kit's `heavy.py` (11 of 11 tool hashes equal to THE TOOLS; heavy.py `31adedc8...` = S8) under
the OXPd wave lock, one at a time, lock waits 0 each; released lock folders are mine in `g2178/_quarantine/locks/`;
no other holder's lock touched; the lock folder absent at the end; no process of mine left. Nothing to any printer
or device; no Jira; no Azure; no write to the project checkout, the seat's lane or GitHub.

## Grades (round 1 of 2): Blocker 0, Major 1, Minor 1, Info 7. Nothing blocks landing the code.

**F1 MAJOR (records, does NOT block landing): the bound did not catch the one hang this lane met, and the three
samples of owed 137's hang show a shape no await-bound can end.** The seat's first whole-solution `dotnet test` at
this head hung in `Datasec.Suite.Server.Tests` for the runner's 1800 s with no cell red and no `did not end within`
line (its STATUS, `.tools/b2170/logs/chain-test.log`, RELAYED and re-read by me). I read the three native samples of
the hang (PR 51's seat `.tools/b2067/logs/hang-server-tests-sample.txt`, PR 57's `.tools/b2134/logs/
orphan-server-tests-sample.txt`, this seat's `.tools/b2170/logs/orphan-server-tests-sample.txt`; read only): in ALL
THREE exactly one thread is abnormal, a `.NET TP Worker` blocked in `Monitor_Enter_Slowpath` (a contended lock)
reached through `RuntimeMethodHandle_InvokeMethod` (a method invoked by reflection), with about 400 unnamed managed
frames below the invoke and 46, 46 and 54 above it (each count MEASURED by program over each file; one
`Monitor_Enter_Slowpath` and one `RuntimeMethodHandle_InvokeMethod` per file; the main thread in `Monitor_Wait`; one
`Kestrel Timer`, i.e. one Kestrel server not yet disposed). That is a blocked call (kit row R7), not an await: my
probe G03 MEASURED that a step blocking its caller is not ended by the bound (a 2500 ms blocking step with a 1 s
bound returned the timeout only after 2502 ms, and the outer `WaitAsync` could not start before it either). DERIVED
from the code: had the hung wait been an await inside either bounded step, the timer thread would have cancelled the
token at 60 s and an idle worker (three were idle in the sample) would have thrown `Late`, a red cell; none came.
Which method, which lock and who holds it are UNMEASURED (the managed frames are unnamed); every hang so far was under
`dotnet test` (the MTP `--server dotnettestcli` mode), never in the executable run alone (seat 5 runs; mine 3 plus 7
mutant runs). **So the kit's FOR RECORDS line "Owed item 137 closed by its first named form ... so a start or stop
that does not end is a red cell" is true of what it names but must not be read as the hang being caught: FOR-RECORDS.md
here gives the corrected wording and proposes a new owed item for the uncaught hang with this evidence.**

**F2 MINOR (named limit, does not block): the "start" bound covers `app.StartAsync(token)` only.** In
`HostRig.StartAsync` the temporary folder, the RSA key and certificate, the PEM writes and `ServerHost.Build(...)`
(configuration, the service container) run BEFORE `BoundedAsync` (`HostRig.cs:74` to `:117` at the head), and the
`HostRig` constructor's `IServer` read runs after it (`:40`); in `DisposeAsync` the `Directory.Delete` runs after the
bounded step (`:205`). A hang in any of these is not bounded. The kit's "every Server cell's host start" is wider
than the code by these lines; the PR body and FOR-RECORDS.md name it.

**F3 INFO (Tuesday's point a): no leak per call.** When the step ends first, the pending `Task.Delay(Infinite, token)`
and its registration are only reachable from the disposed source; disposing the source disposes its timer (DERIVED;
.NET source reading, not printed here). MEASURED by probe G01 (the collection run alone, no parallel cells): 40000
calls (20000 synchronous ends, 20000 `Task.Yield` ends) at a 60 s bound: `Timer.ActiveCount` 17 before, 16 after;
`GC.GetTotalMemory(true)` 5636880 before, 5203888 after. At 13 hosts (26 calls) per run it does not matter.

**F4 INFO (Tuesday's point b): H18 shape 3 cannot race and cannot delete twice.** DERIVED from the head's code: the
first `DisposeAsync` runs the step synchronously up to `await BeforeStop(token)`, which reads `BeforeStop` at that
moment and parks on `never.Task`, a local never set, so that step never reaches `_app.StopAsync`; setting
`BeforeStop = null` afterwards does not reach it. `Late` is thrown out of `BoundedAsync` before
`Directory.Delete(_folder, ...)`, so the first call deletes nothing and the second call (BeforeStop null, 60 s) stops,
disposes and deletes once. Probe G04 MEASURED the same order with two hosts in one cell (A's stop late at 1 s; B
answers `/health` 200 with its own 60 s; A then stopped for good; green).

**F5 INFO (Tuesday's point c): an unobserved task exception fails nothing here.** xunit v3 4.0.3's assemblies
(`xunit.v3.core`, `xunit.v3.runner.common`, `xunit.v3.runner.inproc.console`, `xunit.v3.mtp-v2`) hold 0 references
to `UnobservedTaskException` (byte count, MEASURED); Microsoft.Testing.Platform 2.5.2 holds a handler
(`ServerTestHost.OnTaskSchedulerUnobservedTaskException`, `UnhandledExceptionHandler.OnTaskSchedulerUnobservedTask
Exception`, a resource named `UnobservedTaskExceptionWarningMessage`); no `xunit.runner.json` in the tree. Probe G05
MEASURED a step that faults 300 ms after its 1 s bound: the event fired once for it and the executable's run read
`Failed: 0`. The same under `dotnet test` (MTP server mode): NOT RUN. In the new cells no `Late` path leaves a faulted
task (H17 shapes 2 and H18 1 and 3 never complete; shape 3's step ends cancelled; 3b's is `Task.FromCanceled`), so no
event arises from H17 or H18 at all (DERIVED).

**F6 INFO: the transport's README line is not wider than the code but is more cautious than it.** T1 calls a
revocation-list fetch UNMEASURED while the same handler sets `CertificateRevocationCheckMode =
X509RevocationMode.NoCheck` (`HttpIppTransport.cs:43`). UNMEASURED is not a claim of a fetch; no change asked.

**F7 INFO: mutant `mDecideByStepEnd` is caught deterministically by shape 3b.** In both the seat's and my mutant run
H17 broke at shape 3 first. My probe tree with that mutant applied: G06 (shape 3b) red on its FIRST of 15 rounds
(`TaskCanceledException` against `Assert.ThrowsAsync<TimeoutException>`), and G07 (shape 3 fifteen times) counted
order O4 in 14 of 15 and O3 in 1; on the head G06 late 15 of 15 and G07 late 15 of 15 (MEASURED). Under the same
mutant G03 threw nothing: the head's one question is what makes order O6 a timeout (the kit's R3b, as stated).

**F8 INFO: H18 leaves things behind by design.** Shape 1's host is built and never started or disposed (its
temporary folder and built services stay until the process ends); the control rig is not under `await using`, so a
failed assertion between its start and shape 3 would leave a running host. Kit row R8's kind; no effect on green
runs (every run of the head green).

**F9 INFO: `StepBound` takes any value.** Zero cancels at once (every step `Late`); `Timeout.InfiniteTimeSpan`
removes the bound; other negatives throw. No cell sets anything but 1 s or the 60 s default (`grep`: H18 and the
start's own `stepBound` only). Not a limit of any landed cell.

## THE KIT'S GATE LIST, each measured
- `BASE..head` read whole: five rows, all `M` (`git diff --name-status`; compare `ahead_by` 1, `behind_by` 0, five
  files `modified`, GET 21:53): `src/Datasec.Suite.Adapters.Oxpd1/README.md` +4 -0, `src/Datasec.Suite.Jobs.Transport/
  README.md` +3 -0, `src/Datasec.Suite.Lab/README.md` +3 -0, `tests/Datasec.Suite.Server.Tests/HostCellTests.cs` +69 -0,
  `tests/Datasec.Suite.Server.Tests/HostRig.cs` +61 -5. The four frozen files: `apply_c3.py ... check` prints
  `FROZEN` for each (`49dd4356...`, `d53b64a1...`, `ed9587a4...`, `67be0414...`, equal to `edits_c3.json`). No landed
  line of `HostCellTests.cs` removed (0 deletions). The five removed lines of `HostRig.cs` are the old signature, the
  two old start lines and the two old stop lines.
- The head locally (my clone): locked restore rc 0; build `0 Warning(s)`, `0 Error(s)`; the Server executable whole
  `Total: 18, Errors: 0, Failed: 0, Time: 9.992s` (`g2178/logs/g-server.log`).
- The seven mutants re-run by me (`mutants_c3.py run`, my lane, the frozen rows sha256 `230408e7...`): `MUTANTS: 7 of
  7 MATCH, 7 of 7 undone equal`, rc 0; after it `status --porcelain` 0 lines and the four files `FROZEN`. Reds, from
  my logs: mWaitDropped and mTokenNeverCancelled: H17 (shape 2 message) and H18 (shape 1 message), Actual "The
  operation has timed out." (45.1 s and 44.5 s: the outer 20 s waits, no hang); mDecideByStepEnd: H17
  `TaskCanceledException` against `TimeoutException`; mOwnEndWrapped: H17 `Assert.Same` (Actual the helper's
  timeout); mStepEndDropped: H17 "No exception was thrown"; mStartUnbounded: H18 start message; mStopUnbounded: H18
  stop message. H01 to H16 green under every mutant (Failed equals the listed reds).
- **Whether ANY landed Server cell's start or stop escapes the bound:** the 13 host-starting lines
  (`HostCellTests.cs:30, 44, 57, 83, 99, 144, 159, 175, 232, 269, 289, 304, 340`) are each `await using HostRig rig =
  await HostRig.StartAsync(`; the only `WebApplication` in the assembly is `HostRig._app` (`ServerHost.Build` at
  `HostRig.cs:106`), started only at `:126` inside `BoundedAsync` and stopped only at `:200` and `:201` inside it; no
  cell disposes a rig another way. Escapes: the unbounded lines of F2, and a blocked call (R7, F1, probe G03).
- **Whether the helper can turn a step's OWN exception into a timeout:** only when the token is cancelled at the read
  (orders O5 and O6; R3b). A step that throws before returning a task leaves its own exception, `Assert.Same`, both
  directly and through the start's seam (probe G02, MEASURED). A step that ends cancelled by ANOTHER token, its own
  timeout, another exception: H17 shapes 4 to 6 green.
- **Whether any order of the step's end and the bound escapes the one question (O1 to O6):** none. The arm
  `Task.Delay(Infinite, cancel.Token)` completes only after the source's state is set to cancelled, and the source
  is cancelled only by its own timer (it is not linked and the step holds only its token), so an arm that ended means
  the read is yes; once yes it stays yes; the read is after the wait and before the `using` disposal (DERIVED). No
  `catch`, no filter, no second clock. MEASURED: shapes 3 and 3b green in every head run (mine: g-server, p1-server
  with 15 rounds of each); under `mDecideByStepEnd` both orders O3 and O4 occurred and the kit's form failed (F7).
- **Whether H17 and H18 can hang on any mutant:** no. Every wait is under `.WaitAsync(20 s, Ct)` (shape 3's last wait
  10 s; 3b's `WaitOne` 10 s); the slowest mutant run took 45.1 s for 18 cells; every mutant run ended with a Total.
- **Whether the seams can change anything when null:** both are read once, `is not null`, and skipped; the only other
  change on a null-seam path is the token passed to `app.StartAsync(token)` and `_app.StopAsync(token)`, cancelled at
  60 s and not before. What the host does with a token cancelled mid-start or mid-stop is UNMEASURED (the outcome does
  not depend on it: `Late` either way). H01 to H16 green on the head in my run and under every mutant.
- **Whether any README line is wider than the handlers of this tree:** no. `grep` over the three modules' `.cs`:
  one `SocketsHttpHandler` each (`HttpIppTransport.cs:33`, `Oxpd1Client.cs:49`, `DeviceChannel.cs:52`), no
  `CertificateChainPolicy`, `DisableCertificateDownloads`, `X509ChainPolicy` or `new X509Chain` on any line; the lab
  makes no other handler (its `.cs` files use `Datasec.Suite.Adapters.Oxpd2` on 0 lines; `UniversalPrint.Ipp` is the
  encoder only and that module has no handler); the contrast `DeviceTokenClient.cs:73`. F6 is the one nuance.
- Hosted run of the head (my `hosted3.py`, no `--wait`, push run 45984983632): `HOSTED 09b60507...: PASS` at `--total
  2433 --rules 679`; control `--total 2434` printed `FAIL 4` rc 1. `failed Datasec.` lines 0 and 0, `did not end
  within` 0 and 0 (colour codes stripped). The Server assembly: head linux `7s 477ms`, windows `9s 472ms`; BASE linux
  `2s 994ms`, windows `2s 827ms` (RELAYED from the seat's hosted-base read): the two new cells add about 5 to 7 s,
  their 1 s bounds.

## ADVERSARIAL (three shapes outside each property; each covered or a named limit)
- P1 (late step is the timeout): a step that blocks its caller and never returns (NAMED LIMIT R7; G03 shows the
  bound ends it only when it returns; F1's hang has this shape); a bound of zero or infinite (F9, no cell); a step
  that turns the bound's cancellation into another exception (covered by design: the question ignores the step's end,
  O4; H17 3b).
- P2 (an early end is unchanged): a step that throws before returning a task (COVERED, G02); a step that ends in the
  last instant and is read after the bound (NAMED LIMIT R3b, G03 shows the same order with a blocking step); a step
  that returns a null task (`Task.WhenAny` refuses it with an `ArgumentException` out of the helper: not unchanged,
  but both steps of the tree are async lambdas and never return null; DERIVED, Info).
- P3 (every start and stop bounded): the build, key and folder work before the start and the folder delete after the
  stop (F2, NAMED LIMIT); a rig never disposed (F8, R8); **a cell that starts two hosts: COVERED, each its own bound
  (G04)**; **a host whose start throws synchronously before returning a Task: COVERED, its own exception unchanged
  (G02 through the start seam, the same position as `app.StartAsync(token)` inside the async step)**.
- P4 (README no wider): a handler made by another module the lab uses (COVERED: none, grep); a validation callback
  that builds its own chain (COVERED: no `new X509Chain` in the three modules); the platforms (NAMED, "UNMEASURED ...
  on every platform").
- P5 (landed cells unchanged and green): removed lines 0 (COVERED); the null-seam token change (COVERED above, green);
  the assembly's wall time doubles locally (4.65 s to 10.0 s, RELAYED BASE figure; Info).

## SCANS
- gitleaks 8.30.1: planted control first (a token built by a program, outside every clone): `dir` rc 1, folder moved
  to `g2178/_quarantine/`; `gitleaks git <clone> --log-opts=760e1a64..09b60507` rc 0, `1 commits scanned`, `no leaks
  found`; the added lines (140), the commit message and the five head blobs under neutral names (7 files): rc 0.
- `words.py --control`: `CONTROL FIRED: 13 of 13`; `words.py` over the added lines and the commit message: `WORDS:
  clean (2 files)`, rc 0; `B2[0-9]{3}` 0 and 0 (control: this commission 5).
- CodeQL: NOT RUN locally (the C# extractor is x86_64; RELAYED from the kit's FACTS 6); the branch push carried no
  Analyze rows (`check runs beside the four: 0`); main's baseline at 760e1a64: csharp, python, actions each
  results_count 0 (GET 21:54); open alerts 0. The pull request's own run is the check (landing.txt).

## NOT RUN
CodeQL locally; the whole solution by me (the seat's `chain-test-2` and `green-whole` RELAYED, its hung `chain-test`
read from its log); F5 under `dotnet test`; a managed stack read of any hang (no tool on this machine names the
frames; none downloaded). Nothing against any printer or device.

## Evidence (scratch, not committed): `fleet/state/s335/g2178/logs/` (g-restore, g-build, g-server, mutants-run.out,
mb-*/mt-*, p-restore, p-build, p1-server, p2-build, p2-server, hosted, hosted-ctl), `scratch/added.txt`,
`scratch/message.txt`, `scratch/scan.py`, `scratch/reds.py`, `probe/tests/Datasec.Suite.Server.Tests/GateProbeTests.cs`.
