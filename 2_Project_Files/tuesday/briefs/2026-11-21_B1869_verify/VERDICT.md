GATE B1869: NO GO @ 523204d on main 8ae5e08 (second reader)

Second reader on D4 (the token holder), D9 (the callback credential check) and D12 (no body byte before the credential; the order of the checks). Kit B1849 as stamped, seat X25, head 523204dda0042eab2f2483257b7b0f29706c68fd on main 8ae5e08cadf6460f6f87fff091d3bafada2efe41. Written 2026-11-21, 21:58 to 22:20 AEDT.

## BLUF
- **NO GO on one Major (F1, D9).** `CallbackCredentials` re-fills its cache after an unlocked vault read, so `Forget` and `Issue` (rotation) can fail to take effect. A device whose credential was forgotten is still accepted after `Forget` returns. After a rotation, the old credential stays accepted and the new one is refused. I showed both deterministically (G25, G26). In a free race with a warm cache and a device that keeps calling, the forgotten credential was still accepted after `Forget` returned in 1000 of 1000 iterations with a slow vault delete, and in 54 of 1000 with an instant in-memory delete (G28).
- **D12 holds.** None of the 35 refusals that come before the read touched any member of the body stream (G30). The order is credential, operation, content type, declared length, parse; a vault failure is `Unavailable` and comes first (G31).
- **D4 holds on every point the grade names.** I found no second refresh for one request and no concurrent refreshes of one serial. The retry happens once, a second 401 gives `NeedsRepair`, and a new refresh value is stored before its access value is used. One Minor: a request that arrives while a refresh is in flight runs one more refresh after it (F3).
- **D9:** the comparison runs in constant time, exactly once for every input shape, and every failure is the same `false`. A vault failure is reported apart, and no clear value is stored. Two Minors: the lookup does different work for an unknown serial (F2), and a text says otherwise.
- **Deviation 3: holds** (Tuesday's ACCEPT stands). **Deviation 4: Minor (records).** No harm found (G32).

## What I ran (each dotnet job through the kit's `heavy.py`, sha256 `31adedc8...` equal to the seat's copy; mkdir lock with owner.txt, released by move; 16 jobs, 16 lock folders moved to `/private/tmp/b1869-gate/_quarantine/locks/`)
- Clone: `git clone` with the deploy key, push URL `invalid://no-push`, in my session scratchpad. `ls-remote` showed the branch at 523204dd and main at 8ae5e08c (21:58:13). The changed paths matching `Generated/`, `contracts/` or `tests/Datasec.Suite.Contracts.Tests/` count 0 (control: 33 paths match `Adapters.Oxpd2`).
- Restore with `-p:NuGetAudit=false` under the closed proxy: rc 0. Afterwards `git status` showed only my untracked probe file.
- **Suite at head (before my probe file was added): total 1234, failed 0, succeeded 1230, skipped 4.**
- **Hosted, by GET:** `hosted.py 523204dd... --total 1234 --rules 402 --skipped-linux 4 --skipped-windows 19 --unit 60 --floor 60` gave `HOSTED 523204dd...: PASS` (402 = `git ls-tree -r` count at head). Control: the same call with `--total 1233` gave FAIL 4 (rc 1).
- My probe class `GateB1869Probes` (28 tests, evidence `GateB1869Probes.cs.txt`), with the 43 tests of the lane: total 71, failed 6. The 6 reds are the finding probes G13, G14, G25, G26, G27 and G28; everything else is green (`probes-head-6.txt`). Every value is synthetic, and the outputs hold counts only.
- `=>` census of product code (outside `Generated/`, by program, `arrows.txt`): 31 in all = 17 expression-bodied members + 14 switch-expression arms; **0 lambdas**. Control: a planted file with 2 arrows counts 2; `grep -o -F '=>'` over the same files also counts 31. G40 (by reflection, Device and Callbacks namespaces, 33 types): 0 closure types (`<>c`, `DisplayClass`) and 0 static delegate fields; 7 async state machines.

## D4: the token holder
| Point | Result | Probe |
|---|---|---|
| One refresh per serial in flight | **Holds.** The highest number of concurrent endpoint calls was 1 in every iteration (G01: 400 iterations, 24 wide, with jitter). The one exception is an endpoint that ignores its token after a timeout (G07: 2): a named limit, F6. | G01, G07 |
| Concurrent 401s on one value | **Holds.** With every request holding A1 when the 401s arrive: exactly one renewal in 300 of 300 iterations, 24 wide (G15). A refused refresh: 1 call and `NeedsRepair` for all, 200 of 200 (G12). | G15, G12 |
| A request that arrives during a flight | **Minor F3.** It waits, then refreshes again instead of reusing the result. G14 (deterministic): 3 endpoint calls where 1 was expected. G01: 111 of 400 iterations made 3 or 4 calls (histogram 2:289, 3:106, 4:5); non-200 answers 0. Under a transient failure each wave makes 2 calls, not 1 (G04 200 of 200; G13 slowest 370 ms against `RefreshTimeout` 200 ms). Bounded: never more than one refresh in flight, and in my runs never more than about 2 x `RefreshTimeout`. | G14, G01, G04, G13 |
| Retry once; `NeedsRepair` after a second 401 | **Holds.** All 401s, 16 wide, 300 iterations: each request sent at most twice (most device calls in one iteration: 32, bound 32); the final state is `NeedsRepair` in every iteration; every outcome is 401 or `NeedsRepair`. | G03 |
| Rotation order (store before use) | **Holds.** Of 2821 device sends checked at send time, 0 carried an access value whose refresh value was not yet in the vault (G05, 200 iterations, concurrent, rotating). A failing vault write: 0 device calls with the new value and every outcome `VaultFailed`, 100 iterations (G06). | G05, G06 |
| Forget or Store during a flight | **Minor F4.** `Forget` while a rotating refresh is in flight: the flight writes the refresh value back into the vault and keeps an access value after `Forget` returned (G08). The `StoreRefreshValue` case is overwritten the same way (G09, a limit the seat named). | G08, G09 |

## D9: the callback credential check
| Point | Result | Probe |
|---|---|---|
| Constant-time comparison | **Holds for the comparison:** the comparer is called exactly once per `Verify` for known, unknown, invalid and null serials and for wrong, malformed and null headers (G20: 2 of 2 for each of the 7 shapes). | G20 |
| Same work for known and unknown serials | **Minor F2.** An unknown valid serial costs a vault read on EVERY call (2 of 2); a known (cached) serial costs 0, and an invalid serial 0. Median timing with the in-memory vault: known wrong 459 ns, known with the last character differing 583 ns, unknown 667 ns, invalid 417 ns (G21). With a store on disk the gap is a file read plus a decryption. This reveals which serials are enrolled, never the credential, and lets an unauthenticated caller force one vault read per request. README line 37 ("so the same work is done") is false for the lookup. | G20, G21 |
| The same `false` for every failure | **Holds.** 16 odd headers all refused: tab, NBSP, a Greek capital beta, value case flipped, `=`, `+`, `/`, fullwidth, NUL, a 100,000-character header, a doubled value. `bearer` is accepted; the serial in another letter case is refused. | G22 |
| A vault failure reported apart | **Holds:** `Unavailable` with 0 touches of the body and 0 sink calls (G23). A record of the wrong length (31 bytes) is read as "no credential" (`false`), not as a failure: records, F8. | G23 |
| No stored clear value | **Holds:** one vault record, equal to the SHA-256 of the 43 characters. None of 4 clear forms (ASCII, UTF-16, the decoded 32 bytes, base64) occurs in the vault or in any field of the instance. | G24 |
| **Revocation and rotation take effect** | **MAJOR F1** (below). | G25 to G28 |

## D12: no body byte before the credential; the order of the checks
| Point | Result | Probe |
|---|---|---|
| No body access for any refusal before the read | **Holds:** 35 refusals: 12 credential (6 headers x 2 shapes), a bad serial, another serial with my credential, 11 operations (the 7 others of the catalogue plus `post`, a lower-case target, a trailing slash, `/Registration`), 8 content types, 2 declared lengths. 0 wrong outcomes; 0 touches of ANY stream member (not only reads: `Length`, `CanSeek`, `Position`, `CanRead` and the rest counted). Control: an accepted call touches it 16 times. | G30 |
| Order | **Holds:** Unauthorized > NotHandled > UnsupportedMediaType > TooLarge > Refused; a vault failure with a wrong operation is `Unavailable`. Sink calls 0. | G31 |

## Findings
| # | Severity | Finding | Evidence | What would close it |
|---|---|---|---|---|
| F1 | **Major** | **The callback credential cache undoes `Forget` and `Issue`.** `StoredHash` (`Callbacks/CallbackCredentials.cs:147-168`) reads the vault outside the lock and then writes what it read into `_hashes` without checking whether the serial changed meanwhile. `Forget` (`:80-92`) removes the cache entry BEFORE it deletes the vault record, so a `Verify` in that window re-caches the hash it is deleting. `Issue` (`:45-64`) writes the vault and then the cache, so a `Verify` that missed the cache can overwrite the new hash with the old one. The result: the forgotten credential is accepted until restart; the rotated-away credential stays accepted and the new one is refused. That breaks the contract's property (a callback is acted on only with that device's credential) and README line 33 ("Issuing again rotates; `Forget` deletes"). The README limit at line 94 names only rotation through ANOTHER instance. | G25 deterministic (the later `Verify` after `Forget`: True); G26 deterministic (old True, new False); G27 1320 of 2000 (fresh instance, slow vault read); **G28 1000 of 1000 (warm cache, a device calling in a loop, slow delete) and 54 of 1000 with an instant in-memory delete**; control (no concurrent caller) refused 1000 of 1000 | A per-serial generation (or version) changed under `_sync` by `Issue` and `Forget`, and checked under `_sync` before `StoredHash` caches. `Forget` deletes the vault record first and clears the cache after. Cells in the shape of G25, G26 and G28 (deterministic, plus a free race with a stated count). |
| F2 | Minor (text and records) | The lookup is not the same work for an unknown serial: a vault read on every call against 0 for a cached known serial. It reveals enrolled serials and amplifies unauthenticated callbacks into vault reads; the comparison itself is constant time. README line 37 and the class summary ("so the same work is done") are false for the lookup. | G20, G21 | Correct the text. Optionally a bounded negative cache, or say plainly that the stand-in covers the comparison only. |
| F3 | Minor | A request that finds no access value while a refresh is in flight records the in-flight number (`Device/DeviceTokenHolder.cs:188`). When that flight ends it sees `Flights == observed` (`:277`) and refreshes again. This is NOT a second refresh for one request and never two refreshes in flight. It does mean extra endpoint calls (extra rotations when the endpoint rotates), and a wait of up to about 2 x `RefreshTimeout`. README lines 21-22 and the class summary ("callers that waited for another caller's refresh reuse its result") are false for this caller. | G14, G01, G04, G13 | Compare against a count of COMPLETED flights (or let a lazy caller reuse any value held when its wait ends); add a G14-shaped cell. |
| F4 | Minor | `Forget` during an in-flight rotating refresh is undone: the flight writes the refresh value back into the vault and keeps an access value (G08). This is not in the README limits; the seat named only the `StoreRefreshValue` case (G09). | G08, G09 | The F1 generation pattern applied in the holder (`RefreshAsync` checks it before its `Put` and before keeping the value), or a named limit. |
| F5 | Minor (cells) | Three of my mutants are caught by NO cell of the builder: mFailNoReuse (waiters no longer reuse a failed refresh; only G04 red), mOpFirst (the operation checked before the credential; B01 stays green; only G30 and G31 red), mPeekLength (the body's `Length` read before the credential; only G23 and G30 red). The code at head is right; these are holes in the cells. | `mutants-1.txt` | Cells in the shape of G04 (with its bound), G31 and G30 (every stream member counted). |
| F6 | Records | An endpoint that ignores its token outlives `RefreshTimeout`, so it overlaps the next refresh (G07: 2 concurrent). The holder also zeroes the refresh value that such an endpoint may still be reading. | G07 | A README limit: the endpoint must honour its token and copy the value. |
| F7 | Records | A 401 that arrives after a failed refresh reuses that failure with no endpoint call (G10). The seat's FOR TUESDAY 5 covers callers that waited, not this one. | G10 | Records. |
| F8 | Records | A vault record of the wrong length is read as a stranger (`Unauthorized`), not as `Unavailable`. | G23 | Records, or report it apart. |
| F9 | Records | The holder zeroes the array `TryGet` returns (`DeviceTokenHolder.cs:386`), and `CallbackCredentials` caches that array and later zeroes it. A host binding that returned its own stored array would have its record zeroed. The interface does not say "a fresh copy". | source | One line on `IDeviceSecretVault.TryGet` and in the README. |

## The seat's deviations
- **Deviation 3 (`SolutionTokenGrant` refuses an empty access value or a byte outside 0x21 to 0x7E): HOLDS, Tuesday's ACCEPT stands.** The constructor throws exactly `ArgumentException` for 6 of 6 bad values (empty, a space, CR LF plus an injected header, 0x7F, 0x80, NUL). The message is fixed and holds no value (0 of 6 texts hold the planted value); a good value constructs. An endpoint that builds such a grant gives the caller `DeviceTokenException(RefreshFailed)` with no inner exception, 0 device calls, state `Ready` (G11).
- **Deviation 4 (a throwing body stream escapes `HandleAsync`): Minor (records).** I found no path where it does harm. For IOException, OperationCanceledException, TimeoutException and ObjectDisposedException, thrown after 20 bytes of a card read: each escapes as the stream's OWN instance; the read buffer is zeroed after the throw (4 of 4); no text of the exception holds the credential, the context or a card byte (0); the sink is not called (0); no sequence is recorded (a good read of the same sequence afterwards is `Answered`) (G32). Notes for the records: an OperationCanceledException from the stream, with the caller's token not cancelled, looks like the caller's own cancellation to the host; how the host maps these is the host's. Since F1 forces a fix round anyway, Tuesday may choose to add `BodyFailed` in it; my grade does not require it.

## Mutants (my own, on PRODUCT code, none on the kit's list; each applied by exact replacement, the adapter test project run whole through the lock, undone from a saved copy, proved by `git diff --quiet -- src` rc 0; reds are those beyond the 6 finding probes red at head)
| Mutant | Point | Edit | Red by assertion |
|---|---|---|---|
| mFailNoReuse | D4 | waiters no longer reuse a failed flight | G04 (only) |
| mRenewClearAlways | D4 | a stale 401 clears a newer access value | G15, T04 |
| mPutSkip | D6 | the rotated refresh value never stored | G05, G06, T07 x2 |
| mRepairNotSticky | D4 | the second 401 does not set `NeedsRepair` | G03, T03 |
| mVaultFailIsFalse | D9 | a vault failure read as a stranger | A05, G23, G31 |
| mEarlyFalseMalformed | D9 | an early `false` for a malformed header (no comparison) | A03, G20 |
| mPeekLength | D12 | `Body.Length` read before the credential | G23, G30 (no builder cell: F5) |
| mOpFirst | D12 | the operation checked before the credential | G30, G31 (no builder cell: F5) |
All 8 red; each undo proved rc 0; after the last undo `git status` shows only my untracked probe file and HEAD is 523204dd.

## NOT tested (NOT RUN)
- The whole lane outside D4, D9 and D12: scope by property beyond the count above, the contract cells, H1 to H22 in full, the build's warnings, `repo_rules.py`, the merge, the landing texts (B1868's).
- CodeQL csharp: NOT RUN (cannot extract on arm64); hosted CodeQL is the only C# proof.
- Timing with a real secret store behind the vault (G21 used an in-memory vault; the F2 gap with a store on disk is DERIVED, not measured).
- The Windows leg locally (the hosted `windows` job PASS is its proof).
- Any device, simulator, real token endpoint or host binding; no socket, no listener, no request to any host but GitHub's API by GET and the clone.

## Evidence (`evidence/`)
`GateB1869Probes.cs.txt` (the probe class), `probes-head-6.txt` (the head run of all probes), `probes-head-2.txt` and `probes-head-5.txt` (the earlier runs, the same reds), `mutants-1.txt`, `mutant.py.txt`, `mutants.sh.txt`, `arrows.py.txt`, `arrows.txt`, `hosted.txt`, `hosted-control.txt`, `suite-head-summary.txt`. Logs: `/private/tmp/b1869-gate/logs/`.
