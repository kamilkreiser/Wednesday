GATE B1878: GO WITH FINDINGS @ 610bb7d on main 5bb1418 (second reader)

Round 2 of 2, delta. I am the second reader (successor of B1869). Head 610bb7d2f1f3ded9a5616fcb00bcc6bef408e2f6 = ONE fix commit C1 on 523204dd; main 5bb1418c107f61b286da9bb73795290f9c959e99. Kit B1873 as stamped; its FOR TUESDAY section's B1869 list is done in full below. Written 2026-11-21, 23:15 to 23:30 AEDT.

## BLUF
- **Round-1 Major F1 (D9) is closed.** G25 (a later check after `Forget`) gives `False`. G26 gives old `False`, new `True`. G27 gives 0 of 2000. G28 gives 0 of 1000 with the slow delete and 0 of 1000 with the instant one; its control gives 1000 of 1000. Two runs gave the same result. My new free race on rotation (G42) gave 0 of 1000 with a warm cache and 0 of 1000 with a cold one.
- **F3 is closed** (G13: 1 endpoint call, the late callers end with the first flight at about 169 ms against `RefreshTimeout` 200 ms; G14: 1 call). **F4 is closed** (G08: nothing stored, no access value, `NoRefreshValue`). G01 lost its 3-call and 4-call rows: 400 of 400 iterations made exactly 2 calls. G04 now makes 1 call in 200 of 200. G05: 0 bad of 3202 sends. G15: 0 of 300.
- D12 still holds (G30: 35 refusals, 0 touches; G31: the order is unchanged). G32 is now `BodyFailed` for all four bodies, with the buffers zeroed and no sink call. The caller's own cancellation still leaves `HandleAsync` (G32b).
- 12 mutants: my round-1 eight plus four new ones. **10 are red; 2 survive, and both are equivalent mutants** (records R2).
- Suite at the head: **1248, failed 0, skipped 4**. Hosted: `HOSTED 610bb7d2...: PASS` (1248 / 403); the control with 1247 fails.
- Records only, no Minor or above: R1 (two README sentences are a little loose at their edges), R2 (the equivalent mutants), R3 (Tuesday's item-4 limit: **I agree it is Minor or less**).

## What I ran
Every dotnet job went through the kit's `heavy.py` (sha256 `31adedc8...`, equal to the seat's copy). The lock was the mkdir of `.tools/wave1-heavy.lock.d` with `owner.txt`, released by move: 17 jobs, 17 lock folders in `/private/tmp/b1878-gate/_quarantine/locks/`. Some jobs waited for the lock (up to 9 waits) because B1877 was running.
- Clone into my session scratchpad with the deploy key; push URL `invalid://no-push`. `ls-remote` at 23:15:53: branch at 610bb7d2, main at 5bb1418c. `rev-parse HEAD^` = 523204dd, and HEAD has ONE parent. `ls-files` gives 403.
- **Scope:** `diff --name-status 523204dd 610bb7d2` gives 6 `M` (the five product files and the README) and 1 `A` (`RaceCellTests.cs`). `diff --quiet` over the slnx, `Directory.Packages.props`, `.github`, `build`, every lock file, every `.csproj`, `Generated/`, `contracts/` and `Contracts.Tests` gives rc 0; the control over the README gives rc 1.
- Restore with `-p:NuGetAudit=false`: rc 0. Build: `0 Warning(s)`, `0 Error(s)`. **Whole suite at the head, before my probe file was added: total 1248, failed 0, succeeded 1244, skipped 4.**
- **Hosted, by GET** (project GH_CONFIG_DIR; `hosted.py`, which reads logs with `--allow-escape-sequences`): `--total 1248 --rules 403 --skipped-linux 4 --skipped-windows 19 --unit 60 --floor 60` gives PASS (both legs `total: 1248` twice; `Ran 60`; `RULES: clean (403 files)`). Control `--total 1247`: FAIL 4, rc 1.
- **Merge (optional for me):** `merge-tree --write-tree 5bb1418c 610bb7d2` gives rc 0 and tree `014d6221bb64796c13230e6c21a735558f4a65ba`, which equals the seat's claim. I did NOT build or test the merged tree (that is B1877's item 5).
- **`=>` census:** 31 at the fix (17 expression-bodied members, 14 switch arms, 0 lambdas; 0 unclassified). `grep -o -F '=>'` over the same files also counts 31. G40: 33 types, 0 closure types or cached delegates.
- **words.py** (sha `6f932dc5...`, control `13 of 13`): over the 847 added lines and the commit message, every class is 0 and the result is `WORDS: clean (2 files)`. **gitleaks** 8.30.1: a planted control (built from two halves, never printed) gives `leaks found: 1`, rc 1. The added lines give `no leaks found`, and so does the message. Bytes outside printable ASCII in the added lines: 0.
- My probe class `GateB1878Probes` has 35 tests: B1869's 28, with G08 now asserting nothing stored and G32 asserting `BodyFailed`, plus 7 new ones (G41 to G47). With the lane's 57 cells that makes 92 tests. **Run 1: total 92, failed 0. Run 2: total 92, failed 0.** All values are synthetic, and the output files hold counts only.

## The kit's B1869 list, item by item (expected, then measured)
| Probe | Expected (kit) | Measured at 610bb7d |
|---|---|---|
| G13 | 1 call; the late caller ends with the first flight at about 1 x `RefreshTimeout` | 1 call; all `RefreshFailed`; slowest 202 ms, late callers 168-169 ms (both runs) |
| G14 | 1 call | 1 call; Y 200, U 200 |
| G25 | a later check `False` | `False` (the check that was reading `False` too; vault record gone) |
| G26 | old `False`, new `True` | old `False`, new `True` |
| G27 | 0 of 2000 | 0 of 2000 (both runs) |
| G28 | 0 of 1000 slow, 0 of 1000 instant, control 1000 of 1000 | 0, 0, 1000 of 1000 (both runs) |
| G08 | nothing stored after `Forget` | vault entry not back, no access value, the request `NoRefreshValue`, 0 device calls |
| G09 | unchanged, a named limit | operator's value kept `False` (unchanged; D30's named limit) |
| G01 (400 iterations x 24) | the 3- and 4-call rows PREDICTED gone | histogram `0,0,400,0,...`; bad 0; max in flight 1; non-200 0 |
| G04 (200 x 12) | one call reused by the waiters | 1 call in 200 of 200 (round 1: 2 in 200 of 200) |
| G05 (200) | 0 | 0 of 3202 sends carried a value whose refresh value was not yet stored |
| G15 (300 x 24) | 0 | 0 |
| G30 / G31 | unchanged | 35 refusals, 0 touches of any stream member (control: 16); order unchanged, sink 0 |
| G32 | `BodyFailed` | `BodyFailed` for IOException, OperationCanceledException, TimeoutException and ObjectDisposedException; buffers zeroed 4 of 4; texts holding the credential or a body byte 0; sink 0; a later good read `Answered`. G32b: a stream throwing while the CALLER's token is cancelled leaves as `OperationCanceledException` |

New probes (mine, on the fix):
- **G41** (item 4): see R3.
- **G42**: a free race of `Issue` against a device that keeps calling with the old credential, 1000 iterations with a warm cache and 1000 with a cold one. After `Issue` returned, the old credential was accepted or the new one refused in 0 and 0 iterations.
- **G43**: `CallbackCredentials.Forget` with a failing vault delete. The exception propagates and the credential is still accepted, as the new summary says. A later `Forget` that works refuses it.
- **G44**: holder `Forget` during a flight with 5 waiting requests. All 6 requests end `NoRefreshValue` after 1 endpoint call and 0 device calls, and nothing is stored. After a new `StoreRefreshValue`, the next request gets 200 after 1 more endpoint call.
- **G45**: the first request cancels its own refresh while another waits. The first ends cancelled. The waiting request runs its own refresh and gets 200. Endpoint calls 2, never 2 in flight at once.
- **G46**: holder `Forget` while the rotation's vault write is held under the serial's lock. `Forget` does not finish while the write is held. Afterwards no refresh value and no access value are stored.
- **G47**: a free race, 500 iterations of 4 rotating requests against one `Forget`. A value present after the end: 0. Outcomes other than ok or `NoRefreshValue`: 0.

## Mutants (on PRODUCT code at the fix; exact replacement, the adapter test project run whole through the lock, undone from a saved copy, each undo proved by `git diff --quiet -- src` rc 0; compile errors 0 every time)
| Mutant | Edit | Builder cells red | My probes red |
|---|---|---|---|
| mFailNoReuse | waiters no longer reuse a failed flight | T12 hang, T13 first start, T13 renewal (the kit's expectation) | G04, G13 |
| mRenewClearAlways | a stale 401 clears a newer value | T04 | G15 |
| mPutSkip | the rotated refresh value is never stored | T07 x2, T15 | G05, G06, G46 |
| mRepairNotSticky | the second 401 does not set `NeedsRepair` | T03 | G03 |
| mVaultFailIsFalse | a vault failure is read as a stranger | A05, B08, B09 | G23, G31 |
| mEarlyFalseMalformed | an early `false` for a malformed header | A03 | G20 |
| mPeekLength | `Body.Length` read before the credential | **B09** (the kit's expectation; round-1 F5 closed) | G23, G30 |
| mOpFirst | the operation checked before the credential | **B08** (the kit's expectation; round-1 F5 closed) | G30, G31 |
| mNoCallerCancelRethrow (new) | the caller-cancellation rethrow removed, so it becomes `BodyFailed` | S04 | G32 |
| mHolderForgetNoBump (new) | the holder's `Forget` leaves the generation alone | T14 | G08, G44, G47 |
| mFillReturnsStale (new) | a fill whose generation moved returns its own (older) read | **none** | G41 only (stricter than the contract): equivalent, R2 |
| mIssueNoBump (new) | `Issue` does not bump the generation | **none** | **none**: equivalent, R2 |

## Tuesday's item-4 limit (`CallbackCredentials.cs:178-181`, `:187-190`, `:192-198` at C1)
I read the lines and measured them (G41). A read is dropped unzeroed in three cases: (a) a 31-byte record; (b) a read that lost to `Forget` (a 32-byte array, the hash); (c) a read that lost to another fill (2 reads handed out, 0 zeroed; one of them is now the cached value). **I agree: Minor or less, and right as a named limit.** What is dropped is the SHA-256 of a 256-bit random credential, never the credential. Holding it does not let anyone build a header that passes, because that needs a SHA-256 preimage. The process already holds the same hash in its cache for its whole life, so a second unzeroed copy adds no new kind of exposure. In case (a) the array is not even a valid hash. Zeroing on these three paths would be tidy. I do not judge it a Major.

## Findings (records only; none Minor or above)
| # | Severity | Finding | Evidence |
|---|---|---|---|
| R1 | Records (text) | Two README sentences are loose at their edges, while the behaviour is safe. (a) "a refresh in flight when `Forget` runs stores nothing ... and ends `NoRefreshValue`": a refresh that is already inside its locked store step when `Forget` is called finishes, and its request is sent (G46: status 200). `Forget` waits for it and then deletes, so nothing is stored once `Forget` returns. That guarantee holds; the "ends `NoRefreshValue`" part does not hold for this refresh. (b) "it runs a refresh of its own only when no refresh completed after its wait began": on the 401 path the reference point is when the refused value was handed out, not when the wait began, so a request can reuse a flight that completed before its wait (more reuse, including round-1 F7's reused failure). | G46, source `DeviceTokenHolder.cs:197-208, 280-291` |
| R2 | Records (cells) | Two of my new mutants survive every cell, and both are equivalent. `Issue`'s `Bump` (`CallbackCredentials.cs:64`) is redundant: a fill never overwrites an entry that is already in the cache (`:192-196`), and `Issue` writes the cache under the same lock. Returning the older read when the generation moved (`:189`) only affects a check that started before `Issue` or `Forget` returned, which the stated contract allows. Neither is a hole. | `mutants.txt` |
| R3 | Records (named limit) | Tuesday's item 4, as above: Minor or less. | G41 |
| R4 | Records (carried) | Round-1 F6 (G07: an endpoint that ignores its token overlaps the next refresh), F7 (G10) and F9 (`TryGet`'s array zeroed by the holder and cached by `CallbackCredentials`) are unchanged at the fix and stay as records. The amplification half of round-1 F2 (an unknown, valid-looking serial costs a vault read on every unauthenticated call) is stated in the README only as "reads the vault on every call". | G07, G10, G20, G21 |

## The seat's deviations
They are B1877's to rule on (item 6), and I did not rule on them. My runs found nothing that contradicts the STATUS claim that the code is untouched: C1's seven files are exactly the kit's list, and the outside-scope diff is rc 0.

## NOT tested (NOT RUN)
- The merged tree's build, suite, `repo_rules.py` and `build/tests` (B1877's item 5). I ran only `merge-tree`, which was clean and gave tree `014d6221...`.
- The lane outside my points: H1 to H22 in full, B1868's 17 probes and 16 mutants, the seat's deviations, the landing texts (all B1877's).
- `repo_rules.py` locally, and `build/tests` locally (the hosted `rules` job's `RULES: clean (403 files)` and `Ran 60` are the proof I relied on).
- CodeQL csharp locally (it cannot extract on arm64). The Windows leg locally (its proof is the hosted `windows` job's PASS).
- Timing against a real secret store (G21 used an in-memory vault: known 208 ns, unknown 375 ns).
- No device, simulator, token endpoint or host binding. No socket and no listener. No host was contacted except GitHub: the clone, and the API by GET.

## Evidence (`evidence/`)
`GateB1878Probes.cs.txt`, `probes-head-1.txt`, `probes-head-2.txt`, `mutants.txt`, `mutant.py.txt`, `mutants.sh.txt`, `arrows.txt`, `hosted.txt`, `hosted-control.txt`, `suite-head-summary.txt`, `words.txt`. Logs: `/private/tmp/b1878-gate/logs/`.
