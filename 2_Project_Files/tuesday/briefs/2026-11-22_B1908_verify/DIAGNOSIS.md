# B1908 DIAGNOSIS: OXPd_2 main bf6b441e, linux RED on F13

DIAGNOSIS B1908: TEST RACE. The token broker behaved correctly. The test's scripted refresher hands out its two answers in the order in which the calls reach `Answer`, not the order in which the calls began. Written 2026-11-22 19:28 +1100 by B1908 (Opus, read-only toward the project).

## FOUND
- The failure signature can come from only one interleaving. In that interleaving the broker accepts the answer of the LIVE second refresh, which is legal. Because of the test's race, that answer is the object the test calls `late`. The test then wrongly reads "the late answer was disposed" plus "the grant changed" as a broken invariant.
- The broker cannot store the answer of a timed-out refresh. The only code that replaces `state.Grant` is `AcceptLocked` (`src/Datasec.Suite.Sessions/TokenBroker.cs:481-489`). It is reached only when `error is null` (`:430-438`). A refresh that timed out sets `error = RefreshTimedOut` (`:403-406`), and its outcome is the same object that made `first` refuse with RefreshTimedOut, which the test asserted at `RefreshBoundCellTests.cs:133` before failing at `:141`. After a time-out, a late answer reaches only `DisposeWhenDone` (`:508-527`), which disposes it. `EndLocked` is excluded too: it would remove the state from `_byDevice`, so `Assert.NotNull` at `:21` would fail, not the message at `:22`.
- Confirmed at source: main = bf6b441e30900127487145c3b65b29d8cc9eb5ea, tree de9817fc3e5fc0dadef0f0ff2884af09caa0098f. Run 45001737294 is push / failure. `pulls/17/files` lists 27 files: 0 match `sessions` (case-insensitive), 22 match `registration` (the positive control for that count). The test file's only commit is 762e774. The hosted log shows `RefreshBoundCellTests.cs:22` reached from `:141` with the exact message.

## THE INTERLEAVING (file:line at bf6b441e)
1. Test `:130`. The first `GetNewTokenAsync` starts `RefreshAsync`, and `Task.Run` calls `FakeRefresher.RefreshAsync` (call 1) on the pool (`TokenBroker.cs:400`).
2. Call 1 runs `Interlocked.Increment(ref _calls)` (`Fakes.cs:50`) and records its token and renewal (`:51-55`). It is then PREEMPTED before `Answer(...)` (`:57-63`), so the test's `made` counter (`RefreshBoundCellTests.cs:119`) is still 0.
3. Test `:131`. The wait checks only `Calls == 1 && LiveTimers == 1`, and both are true. `:132` advances the clock, the bound fires (`TokenBroker.cs:401` throws TimeoutException), the outcome is RefreshTimedOut, and `state.Refresh = null` (`:424`). `:133` and `:134` pass (the token was recorded in step 2).
4. Test `:135`. The second call starts a new refresh (`TokenBroker.cs:310-315`), and call 2 enters the fake. Its `Answer` runs FIRST: `Interlocked.Increment(ref made) == 1` is true, so call 2 waits on `firstRelease` and will return `late`.
5. Call 1 resumes: `made` becomes 2, so it waits on `secondRelease` and will return `next`. `:136-138` pass (`Calls == 2`, one live timer, renewal of call 1 = Renewal(1)).
6. Test `:139`, `firstRelease.SetResult()`. Call 2, the live refresh, returns `late`, which is Access(2). `AcceptLocked` stores a copy as the held grant (`TokenBroker.cs:482-489`) and disposes `late` through `using (answer)` (`:455`).
7. Test `:140` sees `late` all-zero and passes. `:141` → `HoldsGrant(kit, 1)` finds Access(2), and `:22` fails with "F13 after the late answer: the held grant is not the expected one". This is exactly the hosted message and stack.

## TESTED
Scope: test F13 alone. The process was the xunit v3 native runner (`Datasec.Suite.Sessions.Tests -method <F13>`) on osx-arm64 with 18 cores, Release, the project's own SDK 10.0.404.
- Plain loop on the unmodified tree: 500 runs, 500 pass, **0 fail** (92 s).
- Stress on the unmodified tree: 4 parallel loops of 500 beside 14 busy-loop CPU burners (load1 reached 20.9): 2000 runs, **0 fail** (164 s).
- POSITIVE CONTROL. A `Thread.Sleep(300)` was injected into call 1 only, at step 2 (`Fakes.cs`, after the record and before `Answer`, gated by `B1908_DELAY=1`). Result: **50 of 50 FAIL**, with the hosted message at `:22` from `:141` exactly. With the same delay plus the fix sketch below (`B1908_FIX=1`): **50 of 50 pass**. With the control build and no variables set: 50 of 50 pass, so the injection is inert when off.
- NOT tested:
  - The linux-x64 hosted runner, or the MTP `dotnet test` whole-suite run (CI runs every assembly in parallel on about 4 vCPU, which makes the preemption in step 2 likelier than on 18 local cores).
  - Windows.
  - Any GitHub job: none was re-run.
  - The broker's other paths beyond reading them.
  - The latent same-shape races listed below: these were read, not exercised.
- So the natural natural-reproduction count is 0 of 2500 locally. Cause is established by (a) the proof in FOUND that no product path produces this signature after the asserted RefreshTimedOut, and (b) the injected interleaving reproducing the exact signature every time.

## HOW
- Clone: `python3 -I fleet/state/s308/d1898/gate/clone.py fleet/state/s310/b1908/clone draft`. Push URL `invalid://no-push`, HEAD bf6b441e, tree de9817fc. The control is a detached worktree `fleet/state/s310/b1908/ctrl`; its diff is in `logs/control-and-fix.diff`.
- Every job ran through the gate kit's `heavy.py`, unchanged: load1 under 7 checked first, the project lock `.tools/wave1-heavy.lock.d` taken and quarantined into `b1908/_quarantine/locks/`, the closed proxy, the project's package cache, the SDK `.tools/dotnet/dotnet`.
- Steps:
  - `restore --locked-mode -p:NuGetAudit=false` passed.
  - `build -c Release --no-restore -p:NuGetAudit=false` passed with 0 warnings.
  - The loops are `b1908/scripts/loop.sh` and `stress.sh`, with summaries in `b1908/logs/loop-*/summary.txt`.
  - Failure copies are in `logs/loop-ctl-delay/fail-*.txt`.
- The clone's `git status --porcelain` is empty: the unmodified tree stayed unmodified.

## FIX SHAPE (test only, NOT applied to any branch)
Smallest change: make the first wait also require that call 1 has taken its answer slot. Answer order is then fixed before call 2 can exist.
```diff
-            await Expect.Eventually(() => kit.Refresher.Calls == 1 && kit.Clock.LiveTimers == 1, "F13: the first call entered and its bound armed");
+            await Expect.Eventually(() => kit.Refresher.Calls == 1 && Volatile.Read(ref made) == 1 && kit.Clock.LiveTimers == 1, "F13: the first call entered, took the first answer and its bound armed");
```
A sturdier alternative is to key the answer on the call's index rather than on arrival at `Answer`. For example, `FakeRefresher` passes the `Interlocked.Increment` result to an `Answer(index, token)` overload.

Red-first cell: the positive control above, kept as a test-kit seam. A `FakeRefresher.BeforeAnswer` hook (or a delay on call index 1) that F13 sets. Expected results:
- Hook set, old wait: RED with the `:141` message (shown 50 of 50).
- Hook set, new wait: GREEN (shown 50 of 50).

No product (broker) change is indicated.

## SAME WAIT PATTERN: OTHER CELLS
`Expect.Eventually(() => kit.Refresher.Calls == N && kit.Clock.LiveTimers == 1, ...)` appears in:
- this file: F13 `:131` and `:136`, F15 `:203`
- RefreshCellTests: F05 hang `:108`, F05 late `:127`, F08 `:205`, F09 `:251`
- ExpiryCellTests: E07 `:115`
- TextCellTests: L01 `:86`

Only F13 has two concurrent calls whose answers are assigned by arrival order, so only F13 has this race.

A latent, smaller race shares the same cause and was read but not tested. `FakeRefresher` increments `Calls` (`Fakes.cs:50`) BEFORE it records the token and renewal (`:51-55`). A check like `Calls == N` can therefore pass while `TokenOfCall(N-1)` or `RenewalStateOfCall(N-1)` is still unrecorded, which would throw ArgumentOutOfRangeException. This affects F05 hang `:114`, F05 late `:130`, F13 `:134` and `:138`. Fix shape: increment `_calls` inside the lock, after the two `Add` calls.

## OWNER QUESTION
For the OXPd_2 seat (via Tuesday): land the F13 test fix, either the `made == 1` wait or the index-keyed answer, together with the `Fakes.cs` change that records before counting. Should that go in one test-only pull request against main, with the red-first seam? Or should the red-first seam stay out of the shipped kit, with this diagnosis's control diff cited as the red proof instead?
