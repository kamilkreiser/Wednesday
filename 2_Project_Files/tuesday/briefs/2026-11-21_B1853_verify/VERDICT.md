GATE B1853: GO WITH FINDINGS @ e909559 on main 61b17ec (second reader)

This is the second reader of gate G1 round 2 of 2 (a delta review) for the session and token broker. The fix round was kit B1845, seat X18, with head `e9095598225e3ddbe7ff2ad942db44a41b815c81` on top of round 1's `70c1fad5`. My scope is the races, sign-out, the subject check and the refresh bound. Opus 5.5, in session. Written 2026-11-21, about 19:30 AEDT.

## BLUF
My round-1 Major is closed. A refresher that blocks before it returns its task is now bounded by `RefreshTimeout`. My S05 is green: the bound is armed while the refresher still blocks. My S06 is green: a 200 ms bound against a 2 s block ended in 202 ms, in 3 runs of 3. My new S14 adds 1,000 callers on a blocking refresher, over 6 seeds: every caller ended `RefreshTimedOut` at the bound, with 1 call per seed.

Round-1 finding 5 is also closed by D23. A session whose idle deadline passes during a refresh now ends; it is not renewed. Across 3 runs of my S03 (420 runs each), 46 to 50 waiters per run end `SessionExpired`. Across 160 runs of my new S16, covering every refresher outcome, 0 tokens were handed out after the deadline.

Everything else in my scope still holds under D20's thread-pool hop:
- single-flight
- sign-out during a refresh
- no write after a delete
- the subject check on every public path

Each mutant the kit assigns me reddens the builder's cells. No Major or Blocker. Two Records items remain (below).

Plain line for a non-engineer: the freeze risk is fixed, the idle rule now holds during a refresh, and nothing found blocks landing.

## Findings
| # | Severity | Finding | Recommendation |
|---|---|---|---|
| 1 | Records | **A refresher can be called AFTER its refresh has already timed out** (a side effect of D20). MEASURED by S15, in 3 runs of 3: the thread pool is saturated, so the call is queued, not run, and the test clock passes the bound. The callers end `RefreshTimedOut` at once, with 0 refresher calls at the bound. The queued call then runs with an already-cancelled token, and the renewal state it receives reads ALL ZERO: the broker's `finally` clears the array the lambda captured (`TokenBroker.cs:400` vs the `ZeroMemory(renewal)` in that `finally`). The late answer was disposed, nothing was stored and no `NewToken` was raised. In production the pool would have to be starved for the whole `RefreshTimeout` (30 s by default). No token leaves, no subject is crossed and no hang results. | One README `## Limits` line beside the D20 line: a refresher may be called after its refresh timed out, with its token cancelled and its renewal state cleared; a refresher checks its token before it uses the renewal state. Not a code change. |
| 2 | Records | **The idle check and the activity stamp read the clock separately.** `ObtainAsync` checks `IdlePassed` with one reading. `ActivityLocked` (`TokenBroker.cs:642` to `:646`) then reads the clock again for the activity instant. On my test clock, which jumps 11 s between two reads, S03 saw this once in 1,260 race runs (trigger "advance 11 s, then `Touch`" racing the waiter, in run p3-r1): the session stayed live, because the token was handed out by a check made before the deadline and stamped after the jump. With real clocks the gap is the time inside one lock section. The hand-out is legitimate (the call named a live session), so D10 and D23 hold. Round 1 counted 13 to 17 such runs per trigger; now it is 0 or 1 in 420. | None needed. If wanted, pass the check's `now` into `ActivityLocked`. Text only for the records. |

## What I re-ran (the kit's FOR TUESDAY section, my part)
The probe file `tests/B1853DeltaTests.cs` is round 1's 13 facts plus S14, S15 and S16. It ran in my scratch clone at `e9095598` only, never in the project. It was rebuilt by `tests/make_probe.py` from the round-1 file and `tests/extra.cs`.

**D20 moved the moment a refresher call starts** (a pool hop), so 5 of my round-1 lines that read `Calls` or moved the clock right after starting a refresh now first wait with `R.Eventually` until the call has entered. The lines are S01:509, S03:799, S08:1107 and S13 (twice). No assertion was removed or changed. This is the same shape as the builder's D20 waits.

Results at the head, in 3 runs (`p2-r1`, `p3-r1`, `p3-r2`): each `total: 90` (74 builder cells + my 16), `failed: 0`, 0 warnings, 0 errors.
- **S05 green** (`timers before the advance 1; bounded True`). **S06 green** (202 ms, 3 of 3).
- **S01** ran 240 seeds with 87,185 concurrent callers across all 8 refresher outcomes. **S02** ran 96,000 free-running operations. **S04** used the real secret store. **S08** had 1,000 waiters and 6 seeds. **S09** used 75 subject variants. **S10** covered all 6 public hand-out paths. **S11** covered store failures. **S12** used a refresher that signs out from inside its call. All green under the pool hop.
- **S13 still measures 2 calls in flight** after a time-out (3 of 3). D21 stays a limit. The README `## Limits` line says so in plain words: "at most one more call starts per `RefreshTimeout` per session", the late answer is disposed, and a rotated renewal state is lost (UNMEASURED for the provider).
- **S03's idle race now ENDS the session.** Triggers t3, t4 and t5 at moment 1 (idle passed by `Sweep`, `Touch` and `GetToken` racing the answer) give `SessionExpired` to 13 to 19 waiters per trigger per run. Sessions left live after the race: 0, 1 and 0 per 420 runs (round 1: 39 to 45; the 1 is Records item 2).
- **S14 (new):** 6 seeds × 1,000 callers (by key and by handle) on a refresher that blocks inside its call. Results:
  - none ended before the bound (checked at 29 s on odd seeds)
  - all ended `RefreshTimedOut` with no inner exception within 3 s real time once the bound passed
  - 1 call per seed
  - the late answer was disposed and never stored, with no `NewToken`
  - the held token was still handed out
- **S15 (new):** measured Records item 1.
- **S16 (new):** 160 runs. Each run had 1 to 50 joined callers (`GetToken` and `GetNewToken`, by key and by handle) and one refresher outcome (accept, throw, null, or a hang past the bound). The idle deadline passed during the refresh, with or without a `Touch` before it. Results:
  - **without the `Touch`:** exactly 1 `SessionExpired` per run, every other caller `SessionNotFound`, 0 tokens, 1 `SignedOut` `Expired`, the store empty, neither grant left in a record, the answer cleared, and a later read `SessionNotFound`
  - **with the `Touch`:** the session lives, the accepted answer is handed to every caller, and the other outcomes give their typed reasons or the still-valid held token
  - in every run: 0 untyped exceptions and 0 saves after a delete
- **F08's and F09's D20 waits did not weaken them.** Read in the diff (`RefreshCellTests.cs:205` and `:251`): one added `Expect.Eventually(Calls == 1 && LiveTimers == 1)` line before the unchanged `Assert.Equal(1, kit.Refresher.Calls)`. The waits for F05 (×2) and L01 have the same shape. Under mRace, F08 still reddens (all 3 rows); under mLate, F09 still reddens.

## Mutants on the new head (my clone, each built and run over the Sessions test project, total 90, undone, then `git diff --quiet` rc 0)
| Mutant | The builder's cells it must redden | Red (by assertion) |
|---|---|---|
| mStaleWaiter (`:346` made never-true) | F15 | **F15**; E07 ×3; mine S02, S03, S16 |
| mSubjAnswer (`:446` made never-true) | U03 | **U03**; mine S01 |
| mTimeout (`WaitAsync` bound removed) | F05, F11, F12 | **F05 ×2, F11, F12**; F08, F09, F13, F15, E07, L01 by their waits; mine S01, S05 to S08, S10, S13 to S16 |
| mRace (single-flight removed) | F08 | **F08 ×3**; F11, F13, F15, E07; mine S01 to S03, S05, S08, S14, S16 |
| mSyncBlock (the inline call restored) | F11, F12 | **F11, F12**; the run then hit the runner's 900 s bound (rc 124), with my blocking probes caught by exactly the defect this mutant restores |
| mLate (own extra: `RefreshAsync` still-current reduced to `_disposed`) | F09 | **F09**; mine S02, S03, S04, S11, S12 |
| mIdleAfter (own: the D23 branch made never-true) | E07 | **E07 ×3**; mine S16 |

No mutant left its assigned cell green. Driver: `tests/mutants.py`; results: `tests/mutants.json`.

## Scope, words, secrets, decode (both readers' items)
- **Scope:** `diff --name-status 70c1fad5 e9095598` has 14 rows (2 A, 12 M, 0 D), all under `src/Datasec.Suite.Sessions/` or `tests/Datasec.Suite.Sessions.Tests/`. 0 rows outside (control: a planted `Datasec.Suite.slnx` row counted 1). 0 `.csproj`, lock-file, `slnx` or `Directory.*` rows. One parent `70c1fad5`.
- **Words:** `words.py --control` printed `CONTROL FIRED: 13 of 13`. Over the 643 added lines and the commit message: `WORDS: clean (2 files)`, with 0 bytes outside printable ASCII.
- **Secrets:** gitleaks 8.30.1 over the added lines and the commit message: rc 0. Control: a token built at run time from two halves, never printed: rc 1.
- **No token decode:** in the library there is 0 of `jwt`, `claim`, `Split('.')`, `JsonDocument` or `JsonNode`. The only base64 decodes are the record's own layer, `SessionRecord.cs:212`, `:221` and `:224` (round 1's 209, 218 and 221, shifted by this commit). `Base64Url` is used only to make handles (`:564`). `Task.Run`: exactly 1, at `TokenBroker.cs:400`. Positive control: `AcceptLocked` counted 2.
- **The D20 code read line by line** (`TokenBroker.cs:392` to `:401`). `key`, `user` and `token` are read into locals before the lambda, and nothing of `state` or `cancellation` is inside it. The bound at `:401` is armed synchronously, before `RefreshAsync` first yields. A refresher that throws from its call or returns a null task becomes a faulted or cancelled task, which falls to `catch (Exception)` → `RefreshFailed` (F14 green). The `TimeoutException` filter is unchanged. **D23** (`:350` to `:355`) sits after the subject-mismatch and still-current branches and before the hand-out, and uses both clocks through `IdlePassed`. It also applies after a refused or timed-out refresh: such a caller gets `SessionExpired` (as the seat's FOR TUESDAY says; S16 rows o1 to o3 confirm it).

## Suite and hosted
- **Whole suite at the head**, through the wave lock (`heavy.py`, sha256 equal to THE TOOLS): restore `--locked-mode -p:NuGetAudit=false` with `CI=true` rc 0, 0 log lines naming http, fetch or download, 0 changed files after. Build `0 Warning(s)`, `0 Error(s)`. **`total: 968`, `failed: 0`, `succeeded: 964`, `skipped: 4`** (run w1, before my probe file was placed). I re-ran it after the mutants and with my probe file moved out (w2, the lock taken after waiting behind another seat for 812 s): restore rc 0 with 0 changed files, build `0 Warning(s)` `0 Error(s)`, **`total: 968`, `failed: 0`, `succeeded: 964`, `skipped: 4`**, and the clone clean at `e9095598`.
- **Hosted run of e9095598, by GET** (`hosted.py ... --total 968 --rules 327 --skipped-linux 4 --skipped-windows 19`, read 18:58:56): **`HOSTED e9095598...: PASS`**. 4 jobs success; both legs `total: 968` twice; skipped 4 (linux) and 19 (windows); `RULES: clean (327 files)`; `UNIT-TEST FLOOR: ran 53, floor 53`; the secret scan's planted controls fired and printed `no leaks found`. Output: `tests/hosted-e9095598.txt`.
- **The origin by GET:** `refs/heads/b1831/wp15-token-broker` = `e9095598...`; `refs/heads/main` = `61b17ec0...`.

## The merge with main 61b17ec0
NOT RUN by me (the commission lets B1853 skip it; it is B1852's). Pull request 8's files are `build/` and `ci.yml` only (relayed by Tuesday and the seat's STATUS), none of the lane's.

## The seat's deviations
- **4** (mTimeout and mRace redden the D20-changed cells through the new wait's 10 s guard, before the cells' own assertions): **accepted.** A guard failure is an assertion, not a hang, and its condition is the property itself (`Calls == 1`, an armed bound). The original assertions are unchanged under it. I saw F08's read-beside-renew row, F11 and F12 redden by their own assertions.
- **5** (L01 also got a D20 wait, `Calls == 3`): **accepted.** It is L01's third refresher call (read in the cell), and the shape matches the others.
- **7** (R09 builds both brokers by hand, so a failing-read fake sits under the restarting constructor): **accepted.** Read at `RecordCellTests.cs` R09: `RestoreResult(0,0,2,2)`, the store emptied, 0 refresher calls. That is fail-closed as built.
- 1, 2, 3, 6 and 8 (process only: late predictions, one `sed -i` on a comment line, eleven mutants named "twelve", the E07 output helper, a gitleaks rc first read through a pipe): **accepted as records**. None touches the code, and each is visible in the reviewed diff or the seat's logs.

## NOT TESTED / NOT MINE
- The merge with `61b17ec0`, the landing texts, and B1852's items (time, the store and record writer, P04, E08, R08 to R10, B07 beyond a reading).
- The Windows leg locally; macOS arm64 only (the hosted Windows leg is green).
- C# CodeQL (not available on arm64; the hosted scan is the proof).
- A real WP1.4 refresher. Whether it blocks before its first await, depends on the caller's thread or context, or checks its token before using the renewal state is UNMEASURED.
- Under mSyncBlock I did not identify which of my probes ran into the 900 s bound. The mutant restores the round-1 defect, and F11 and F12 were already red.
