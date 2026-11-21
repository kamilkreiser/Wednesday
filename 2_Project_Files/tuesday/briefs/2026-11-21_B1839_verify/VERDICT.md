GATE B1839: NO GO @ 70c1fad on main 5e36d8d (second reader: races, sign-out, subject)

Second reader of gate G1 for the session and token broker (kit B1831, seat X18), round 1 of 2. My scope covers only F08, F09, D9 (U01 to U04) and D12 "still current". Items 1, 4, 5 and 8 belong to reader B1838. Opus 5.5, in session. Written 2026-11-21, about 17:35 AEDT.

## BLUF
One Major: the broker can hang past `RefreshTimeout`. This happens when the refresher blocks in the synchronous part of `RefreshAsync`, before it returns its task. The broker calls the refresher inline on the first caller's thread (`TokenBroker.cs:334`, then `:389`). The time bound is applied only afterwards, at `:390`. While the refresher blocks, no timer is armed. The first caller is stuck in the call itself, and every caller that joined the same refresh waits with no bound at all. The kit's REQUIRED SECTION says "whatever ... a refresher ... hands the broker ... never a hang beyond `RefreshTimeout`". The commission grades a hang past the bound as NO GO.

Everything else in my scope held under my own adversarial tests:
- single-flight
- sign-out, or any other end, during a refresh
- the subject check on every public hand-out path
- no record written after its delete
- no token decoding on these paths

Plain line for a non-engineer: the race and sign-out logic is sound. One small change is needed so that a slow token-refresh component can never freeze callers. Then a fix round.

## Findings
| # | Severity | Finding | Recommendation |
|---|---|---|---|
| 1 | **Major** | **Hang past the bound with a synchronously blocking refresher.**<br>`ObtainAsync` starts `RefreshAsync` inline (`TokenBroker.cs:334`). `RefreshAsync` calls `_refresher.RefreshAsync(...)` (`:389`) BEFORE `call.WaitAsync(_refreshTimeout, _time, ...)` (`:390`). Joined callers await `refresh!.WaitAsync(cancellationToken)` (`:337`) with no bound of their own.<br>MEASURED by S05 (test clock): 0 timers armed while the refresher blocks. With the clock moved 31 s past the call, the starter and a joined caller were both still waiting after 3 s real.<br>MEASURED by S06 (system clock): a 200 ms `RefreshTimeout` against a refresher that blocks 2 s before returning took 2002 to 2003 ms, in 5 runs of 5.<br>Control S07: an *async* hang on the same clock is bounded near 200 ms (green).<br>Whether WP1.4's refresher (Microsoft's library) can block before its first await is UNMEASURED. | Start the refresher off the caller's thread, e.g. `call = Task.Run(() => _refresher.RefreshAsync(key, renewal, user, token))`, so the bound covers the whole call.<br>MEASURED as a fix probe in my clone (mutant `fixSyncBlock`): S05 and S06 turn green. F09 and my S03 then go red only because they assert `Calls == 1` synchronously right after `GetNewTokenAsync`; they must wait for the call (Eventually) instead.<br>Add a cell for this shape (or name it a limit, if Tuesday prefers to put the contract on WP1.4). |
| 2 | Minor (test hole) | **The waiter's "still current" re-check (`TokenBroker.cs:346`) has no builder cell.** Mutant `mStaleWaiter` (the condition made never-true) leaves every builder cell green, F09 included. My S02 and S03 go red. Without it, a waiter of an ended session would be handed the zeroed bytes of the cleared grant. | Add a cell: an accepted refresh, then an end before the waiter re-enters the lock; the waiter must get `SessionNotFound`. |
| 3 | Minor (test hole) | **U03 does not isolate the answer-time subject check (`:446`).** Mutant `mSubjAnswer` leaves U03 green, because the hand-out check (`:609`) still refuses and ends the session. With `:446` removed, though, the other subject's grant is accepted, WRITTEN to the store and announced with `NewToken` before it is refused. My S01 catches this (a NewToken count and the stored record). | U03 should also assert: no `NewToken` event, and no save of the answer. |
| 4 | Minor (named limit owed) | **Single-flight holds only within `RefreshTimeout`.** Suppose a refresher ignores cancellation. After a timeout, the next `GetNewTokenAsync` starts a second refresher call while the first is still running: S13 MEASURED 2 calls in flight for one session. A late answer carrying a rotated renewal state is disposed by design (F05), so a provider that rotates renewal state may leave the held state stale (provider behaviour UNMEASURED). | README `## Limits`: one line. |
| 5 | Minor (for Tuesday) | **A hand-out after a refresh does not re-check idle.** The idle timeout can be as short as 1 s and a refresh may take up to 30 s. If the idle deadline passes while a refresh is in flight, the waiter is still handed the token and its activity renews the session. S03 MEASURED this in about 45 race runs (per run: `live-after-race` 17/14/17, 17/12/15). D10's text ("ended at the next call that names it") is met, because the call named the session before the deadline. | Tuesday decides whether the waiter re-checks idle. Item 4 (TIME) is reader B1838's. |
| 6 | Records | **A `NewToken` handler that blocks also blocks every waiter of that refresh**: `Raise` runs before `TrySetResult` (`:432` to `:433`). This follows from the synchronous events of Q16; a handler that throws is already covered (V01). | Name it a limit. |

## What held (my own tests; the file `tests/B1839AdversarialTests.cs`, 13 facts, run in my scratch clone only)
- **F08 single-flight.** S01 ran 240 seeds with 87,185 concurrent callers (60 of the seeds had 1,000 callers). Callers ran from 8 dedicated threads behind a barrier, mixing `GetToken` and `GetNewToken`, by key and by handle, inside and outside the margin. Every seed covered all 8 refresher outcomes: accept, throw with token text, another subject, expired, null, oversize, hang until cancelled, late answer after the bound. Results:
  - exactly 1 refresher call per flight (0 when no caller needed one)
  - every success carried this subject's bytes of the expected generation
  - every refusal was the typed reason the kit names
  - the late answer was disposed and never stored
  - 0 save-after-delete
  
  S02 ran 40 seeds, 96,000 free-running operations across 6 devices: reads, renews, sign-ins of NEW users on the same devices, sign-outs by key or handle, `Touch`, `Sweep`. 5% of refresher answers were another subject, 5% threw, 5% were expired. Results: at most 1 refresher call in flight per session, 0 foreign tokens, 0 wrong subjects passed to the refresher, 0 untyped exceptions, 0 save-after-delete, store empty at the end. S08 ran 6 seeds × 1,000 waiters on a refresher that ignores cancellation: none ended before 30 s on the test clock, all ended `RefreshTimedOut` at the bound, cancelled callers returned at once, and still 1 call.
- **F09 and D12.** S03 ran 420 runs: 7 ways to end a session (sign-out by key, by handle, a new sign-in of another user on the device, `Sweep`, `Touch` or `GetToken` after idle, `Dispose`) × 3 moments (before the answer, racing it on two threads with a random save delay, after it), with 0 to 49 joined callers. Results:
  - 0 records written after their delete
  - the ended id never left in the store
  - neither grant stored after an end
  - waiters got only `SessionNotFound` (or `ObjectDisposedException` on dispose), or this user's new token when the answer won the race
  - nothing handed out when the end came first
  - the answer zeroed
  - always exactly 1 call
  
  S04 ran 24 seeds over the REAL `LocalSecretStore`: after sign-out during a refresh, no `sessions/` name remained, and no raw, base64 or hex form of either grant, the user or the handle was in any file. S11 covered 4 store-failure modes around a refresh (delete fails at sign-out while the answer arrives; the accepted write fails, then sign-out or a new sign-in; the delete still failing at a new sign-in): no write of an ended session. S12 covered a refresher that signs the session out from inside its own call: `SessionNotFound`, answer zeroed, store empty.
- **D9.** S09 ran 75 subject inputs: case, each of the 25 characters shifted by one, leading or trailing space, NBSP, a zero-width joiner, a Cyrillic look-alike, decomposed against composed, an embedded NUL, empty, truncated, a lone surrogate. At sign-in every one gave `SubjectMismatch` with nothing stored and no event. In a refresh answer every one ended the session, cleared the store and later gave `SessionNotFound`. Users that are equal but unusual (a lone surrogate, 10,013 characters, a decomposed form) sign in, hand out and restore without an untyped exception. S10 swapped the held grant to another subject (through internals) and tried all 6 PUBLIC hand-out paths: fast path by key and by handle; after a failed refresh by key and by handle; after a timed-out refresh; a fast read beside an in-flight renew. Each gave `SubjectMismatch`, ended the session and cleared the store. U04 reaches only the internal method; this proves the public paths. Builder's FOR TUESDAY 0 confirmed at source: `:88`, `:446`, `:609` and restore `:740`, all ordinal.
- **No token read.** The only base64 decodes in the library are `SessionRecord.cs:209`, `:218` and `:221` (the record's own layer). There is no JWT, claim, `Split('.')` or `JsonDocument` on a token. Searched with `/usr/bin/grep -i`; a positive control counted 1.

## Mutants (independent; each built and run in my clone, then undone and proved by `git diff --quiet` rc 0)
| Mutant | Red (by assertion) |
|---|---|
| mRace (single-flight removed, `:310`) | builder F08 ×3; mine S01, S02, S03, S08 |
| mLate ("still current" in `RefreshAsync` removed, `:414`) | builder F09; mine S02, S03, S04, S11, S12 |
| mSubj (hand-out comparison `:609` removed) | builder U04; mine S10 |
| mSubjAnswer (own: answer comparison `:446` removed) | mine S01 only (finding 3) |
| mStaleWaiter (own: waiter re-check `:346` removed) | mine S02, S03 only (finding 2) |
| mTimeout (`WaitAsync` bound removed, `:390`) | builder F05 ×2, L01; mine S07; the run then hit the runner's 900 s bound (rc 124): a hang, as expected |
| fixSyncBlock (the fix shape of finding 1) | S05 and S06 turn green; F09, S03 and S13 red only for the timing reason in finding 1 |

S05 and S06 are red at the head (finding 1) and therefore appear in every mutant's red list. Lists: `tests/mutants-run1.json`, `tests/mutants-run2.json`; driver `tests/mutants.py`.

## Runs (each through the wave lock by `mkdir` of `.tools/wave1-heavy.lock.d`, released by move; the runner is the kit's `heavy.py`, sha256 equal to the seat's copy)
- restore: `--locked-mode -p:NuGetAudit=false`, `CI=true`, closed proxy, rc 0
- build of the Sessions test project: 0 warnings, 0 errors
- the Sessions test project (53 builder cells + my 13) at the head, on a fresh build, 4 times: `total: 66`, `failed: 2` each time (S05, S06), 64 succeeded

One run is discarded and said so: runs 3 and 4 used binaries left by the last mutant build, which is why they showed S02 and S03 red. I rebuilt, and runs 5 to 7 were clean apart from S05 and S06. Measurement lines are in `tests/notes-run*.txt`; they hold no token, subject or handle values.

## NOT RUN / NOT MINE
- Items 1, 4, 5 and 8 (scope, time, the whole suite of 947, the hosted run, landing texts): reader B1838's.
- The Windows leg: macOS arm64 only.
- CodeQL C#: NOT RUN (it cannot extract on arm64); hosted CodeQL is the only C# proof.
- A real WP1.4 refresher: none exists, so whether it can block synchronously is UNMEASURED.
- The restore paths (R01 to R05): not mine, beyond S09's restart of the unusual users.
