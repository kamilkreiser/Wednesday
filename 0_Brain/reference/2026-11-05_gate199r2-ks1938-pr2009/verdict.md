GO WITH NOTES

# Gate 199 round 2 (the cap): Secuura / Blockchain PR 2009 (KS-1938), tier 1

Gated SHA `2f10e7e060cc7265eef5fd97d74d09ad2c1e7269` (local, not pushed; read by SHA from the shared object store). Compared against round-1 head `86eb3152af46` and base `5fc5569ed96a`. Merged onto develop `cb1cadfa2ee4` as commissioned, and also onto origin develop `c9cb07738cf6`, which moved during the gate. **This verdict covers that SHA only.** If the pushed head is not exactly `2f10e7e060cc`, the verdict expires.
Gate: QA gate (Opus), findings only. Clone at `clone/` (`git clone --shared`, then a detached checkout by SHA). Every write went to this folder. Only read verbs touched the shared checkout.

## BLUF
F1 is closed. A revoked Proxy at step 12 now runs step 13 (wallet lookup + USER_ERASED publish), exactly as base does.

The full fault matrix covers 38 fault points × 10 thrown kinds × 3 revisions:
- Round-2 head equals round-1 head at **374 of 380** cells. All 6 differences are at the step-12 point (k=35).
- Every non-ordinary thrown value at round-2 head equals **base-with-an-ordinary-Error** at **340 of 342** cells. The 2 exceptions are the held line 670.
- In no cell does round-2 head do more than base-ordinary, or answer success where base-ordinary failed.

R2's falsy re-raise is in place, and it is stricter. The seat's red-proof, T1 and T4 reproduce. My own tamper is killed, and my equivalent-refactor control survives. Suites match base apart from environmental noise. Merge is clean onto both develops, with 0 shared paths.

**No findings.** The notes are below.

## Findings
None (no Blocker, Major or Minor).

## Notes
### N4 (new): two more step-12 inputs differ from base besides R2's falsy case. Both are stricter, and R1 calls for both.
MEASURED AT RUNTIME. Evidence: `ev_q2q3_table.txt`, step-12 table.
- **Thenable that settles undefined.** Base: success=**true**, completed line logged. Round-2: success=false, fan-out ran. This is the same class as R2: a failed step 12 used to read as success. The seat's fragments say for this case "base behaves the same by reading; not run at base". It is now **run at base and confirmed**, so the fragment and PR body can drop "not run at base".
- **Thenable that rejects** (my own extra kind). Base and round-1: the await rejects, so the fan-out is skipped (n=36, no publish). Round-2: the fan-out runs (n=38), then success=false.
  - This is the only cell in which round-2 runs *more* steps than base with the same value.
  - It equals base-with-an-ordinary-Error exactly, and R1 requires it ("step 13 for ANY thrown value … a thenable").
- **'' and false** behave like 0 (R2's falsy family). null and undefined equal base.

Wednesday's R2 says "the falsy case is the one place head may differ". Read literally, the thenable cases are two further differences. Both are in the stricter, R1-mandated direction. I flag them for the ruling record, not as defects.

### Q3 read strictly (same thrown value, round-2 vs base): 3 of 380 cells complete more
1. k=35 thenableReject: described in N4.
2. k=37 proxy and getter (publish fault).
   - Base rejected with a TypeError. Round-2 answers success=true, the same as base-ordinary.
   - This is round 1's intended change, already present at `86eb3152af46` and gated in round 1.

Against base-ordinary, round-2 completes more at **0** cells. The step-12 failure-where-base-succeeded cells (thenable, 0, '', false) are all in the stricter direction.

### N1-N3 from round 1
- **N1: unchanged.** The r2 log scan still has exactly one marker hit for non-ordinary values, at k=12 getter (held line 670). The ordinary control fired with 38 hits.
- **N2: unchanged.** The G670 mutant (round 1's `mutate.py`) passes the seat's file **49 of 49** at round-2 head. The gate matrix still catches it: at k=12 proxy and getter, r2 gives success=false, n=13, no DEK destroyed. G670 gives success=true, n=33, DEK destroyed, published. Evidence: `ev_N2_G670_r2.txt`. It still belongs in KS-1953's test.
- **N3: unchanged.** The live PR body was not read. Round 2 is not pushed (`refs/pull/2009/head` = `86eb3152af46` at 08:00:58Z), and the seat says the round-2 body block is "owed after the push". gh was not used.

### N5: environment
My first whole-suite run had a third failing suite: `ks1868-originate-events-redis-error-listener-unreadable-throw.test.ts` (TS2451/TS2300 "cannot redeclare", cold ts-jest cache). It passed alone (5 of 5) and in a second full run. It is not in PR 2009's paths. Classified as an environmental flake. Evidence: `ev_fullsuite_r2.log`, `ev_ks1868_alone_r2.log`, `ev_fullsuite_r2_run2.log`.

## Answers
1. **Diff `86eb3152af46..2f10e7e060cc`.**
   - 2 commits in a fast-forward chain (`694586248c28` then `2f10e7e060cc`). 4 files, +100/-15: the ks1938b test file, gdprService.ts (+8/-3), and the cheat and flow fragments.
   - The gdprService.ts hunks (`ev_q1_service_diff.txt`) are exactly: 2 comment lines, the step-12 capture (`step12Failure` box with `{ err: err ?? new Error(...) }`) at `gdprService.ts:937-938`, and the reader `if (step12Failure) throw step12Failure.err;` at `:982`.
   - Nothing else in `executeErasureImpl` moved. The line-670 catch (r2 line 705) is byte-equal to base (`ev_line670_r2.txt`).
2. **Fault matrix.**
   - The harness is round 1's, copied, with 7 thrown kinds added (`gate_harness/gate199r2-erasure-fault-matrix.test.ts`).
   - Instrument control: my base and round-1 runs equal round 1's own JSON at **114 of 114** cells each.
   - Round-2 vs round-1: 374 of 380 identical. The 6 differences are all at k=35: proxy, thenable, thenableReject, 0, '', false.
   - Step-12 table (n = calls; wal = wallet lookup; pub = USER_ERASED published; dek = key destroyed):

   | thrown at step 12 | base `5fc5569ed96a` | round 1 `86eb3152af46` | round 2 `2f10e7e060cc` |
   |---|---|---|---|
   | ordinary Error | n=38 wal pub dek, false | same | same |
   | revoked Proxy | n=38 wal pub dek, false | **n=36 dek, no wal/pub, false (F1)** | n=38 wal pub dek, false (**F1 closed**) |
   | getter-throws Error | n=38 wal pub dek, false | same | same |
   | thenable → undefined | n=38 wal pub dek, **true** + completed log | **true** + completed log | n=38 wal pub dek, false |
   | thenable → rejects | n=36 dek, no wal/pub, false | same as base | n=38 wal pub dek, false |
   | undefined | n=38 wal pub dek, false | same | same |
   | null | n=38 wal pub dek, false | same | same |
   | 0 | n=38 wal pub dek, **true** + completed log | **true** + completed log | n=38 wal pub dek, false (R2) |
   | '' / false | **true** + completed log | **true** | false |

3. **Direction.**
   - Round-2 non-ordinary vs base-ordinary: **340 of 342** equal (the differences are k=12 proxy and getter, line 670 held). 0 cells complete more or answer success where base-ordinary failed.
   - Same-value r2 vs base: 3 of 380 do more (see Notes). Round-2 answers failure where base answered success at 4 cells (k=35 thenable, 0, '', false), all stricter.
4. **Red-proof** (`ev_seat_*.log`). Every source swap was sha-checked and restored to `229f5771…`.
   - Round-2 head: 49 of 49 pass.
   - Round-1 source in place (`4b15c272…`): **3 failed** (revoked Proxy, thenable, 0), all by `toEqual`. The 3 controls and the 43 older cells pass.
   - T1 (revert the fix in r2): the same 3 fail.
   - T4 (`if (step12Failure?.err)`): only the falsy cell fails.
   - My own tampers:
     - **TG1** (move the re-raise above the wallet lookup, against KS-1028's order): **all 6 fail**, killed.
     - **TG2** (equivalent try/catch box, a negative control): 49 of 49, survives as it should.
   - At base, the group fails 4. Revoked Proxy and getter-throws differ only in the logged reason, which is round 1's guard. Thenable and 0 differ in the answer.
5. **Suites at round-2 head.**
   - originate jest: 212 files / 2527 cells pass. Base in the same environment: 211 / 2478. That is +1 file and +49 cells. In both runs the same 2 suites (ks794, ks978; TS2305 `getRefId`) fail to compile. This is environmental and the same as round 1. The seat's 2545 includes those suites' cells.
   - `tsc --noEmit -p services/originate`: the same 15 TS2742 as round-1 base (the error set is identical, environmental), 0 in gdprService. A planted error was caught (TS2322 + TS6133).
   - eslint on the 2 changed .ts files: 0 errors, 0 warnings. A planted unused variable was flagged.
   - docs-fragments check: OK, with the same 2 ADVISORY lines as round 1. A planted second `<h2>` gives rc 1. Restored.
6. **Merge tree** (in my clone).
   - onto `cb1cadfa2ee4`: rc 0, tree `4186d9b24efc27f827a2d11fe49d11251f67fca1`. It differs from develop in exactly PR 2009's 4 files and from r2 in exactly PR 2007's 9 files.
   - Shared paths with PR 2007's 9: **0**. The planted control gives 1.
   - develop gdprService blob = base blob (`860bd001…`).
   - Develop moved during the gate to `c9cb07738cf6` (KS-1504, 3 api-gateway/fragment paths). Merge onto it: rc 0, tree `893020d489848d75d7c6cac6be12187650ad5a2d`, shared paths 0 (planted control 1). Evidence: `ev_mergetree.txt`, `ev_mergetree_c9cb.txt`.
7. **N1-N3:** all unchanged (see Notes).

## Readings (shared checkout read-only; branch beside each SHA)
- 07:50:02Z: checkout on `develop` at `5fc5569ed96a`. `2f10e7e060cc` and `cb1cadfa2ee4` present as commits.
- 08:00:58Z: `ls-remote origin`: develop `c9cb07738cf6` (moved from `cb1cadfa2ee4`), `refs/pull/2009/head` `86eb3152af46` (round 2 not pushed). Local branch `v21/pr2009-round2` at `2f10e7e060cc`. Checkout on `develop` at `5fc5569ed96a`.
- 08:01:29Z: same. `v21/pr2009-round2` still at `2f10e7e060cc`. The gated SHA did not move.

## NOT tested (Rule 2)
- No real Postgres, Prisma or event bus. All faults go through plain-function stand-ins, so no real driver is shown rejecting with a Proxy or a thenable.
- No booted stack, route-level call, or four platform suites.
- Node v26.8.1 only (not LTS).
- docs-fragments was not run over the merged tree.
- Pre-push hook legs were not run.
- The live PR body was not read (N3).
- Connector-erasure coverage is unchanged from round 1 (it rests on the seat's cells).
- The 5d and 6b loops ran with empty result sets.

## Environment
- `node_modules` and `packages/shared/dist` were copied from round 1's gate clone, read-only from its folder.
- Harness and scripts are in `gate_harness/`. Each run restored the clone; `git status` is empty at the end, HEAD is `2f10e7e060cc`.
