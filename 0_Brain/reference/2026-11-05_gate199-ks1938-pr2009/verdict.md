NO GO (F1: at head, a revoked Proxy from the step-12 DSR update skips the step-13 USER_ERASED fan-out, which ran at base; erasure steps change on a tier-1 file)

# Gate 199: Secuura / Blockchain PR 2009 (KS-1938), tier 1, round 1 of 2

Gated head `86eb3152af4638d05b287d83a3424520d131076c` against base `develop` `5fc5569ed96ac61f64823cc9e1fa841899aa1f62`. This verdict is about that SHA only.
Gate: QA gate (Opus), findings only. Clone by SHA at `clone/` in this folder. Only read verbs were used against the shared checkout.

## BLUF

The change does what it claims at all 14 sites. Every hunk is a guard around a thrown-value read, plus the `err?.code` guard. Line 670 is byte-equal to base. eslint, tsc and docs-fragments show nothing new. Every one of the seat's numbers I re-measured came out the same.

**One regression, which the seat's cells cannot see.** `updateDSRStatus` now rethrows the original value, as designed. `executeErasureImpl` captures that value at step 12 like this:

```
const step12Error = await updateDSRStatus(...).then(() => undefined, (err) => err ?? new Error(...));
```

The rejection handler **returns** the value. When the value is a revoked Proxy, promise resolution reads `.then` on it, that read throws, and the `await` rejects. Control then jumps to the outer catch, so the wallet lookup and the USER_ERASED publish (step 13) never run.

At base the same input reached step 13, because base's `updateDSRStatus` catch produced a readable TypeError. KS-1028 exists so that a failure at step 12 does not skip step 13. Measured as 1 point in an exhaustive fault matrix: 73 of 76 head-unreadable cells match base-ordinary. Of the 3 that differ, 2 are the held line 670 (expected) and 1 is this.

The fix is small. Round 2 can carry it.

## Findings

### F1: MAJOR. A revoked Proxy at step 12 skips the step-13 fan-out at head (it ran at base)
- **Where:** `Blockchain/Dev/services/originate/src/services/gdprService.ts:935-936` at head (the `.then(() => undefined, (err) => err ?? …)` capture). The trigger comes from the change at `:396-416`, where `updateDSRStatus` now rethrows the original value instead of a TypeError.
- **Oracle:** Product (KS-1028's own comment at `:934`: "a step-12 throw must not skip the step-13 fan-out") and History (base runs step 13 for this input). It also breaks the commission's Q3 condition: "the set of steps that run [is] identical."
- **Evidence (MEASURED AT RUNTIME, replicated twice):**
  - `ev_q2q3q4_table.txt` row k=35. Base proxy: 38 calls, DEK destroyed, published, `success=false`. Head proxy: 36 calls, DEK destroyed, **not published**, `success=false`. Head getter: identical to base.
  - Call tails are in `ev_matrix_head.json` / `ev_matrix_base.json`. At head the sequence ends at `UPDATE data_subject_requests`. At base it continues with `SELECT wallet_address` and `BUS:publish`.
  - Minimal repro: `gate_harness/thenable_repro.js`, run twice with the same output. Base shape: "captured TypeError; fan-out runs". Head shape: "AWAIT THREW TypeError: Cannot perform 'get' on a proxy that has been revoked -> fan-out skipped".
- **Impact:** originate's data steps 1 to 11 have run and the subject's key is destroyed. Downstream services (auth, kyc, m365, wallet-connector, security) never get `user.erased` on this attempt. `success` is false at both base and head, so the route and the connector retry path behave the same. Only the cascade is lost, until a retry gets past step 12.
- **Likelihood:** the same premise as the whole ticket: a DB layer rejecting with a revoked Proxy. A getter-throws Error is not affected.
- **What the seat's suite misses:** S04 tests `updateDSRStatus` alone ("rejects with the thrown value itself", correct). S05 and S06 never make step 12 reject. The PR body and the flow fragment both say the `updateDSRStatus` and step-13 rows answer "as for an ordinary Error", which is not true for this input.
- **Fix-shape:** make the step-12 capture independent of what the thrown value is. For example, box it: `.then(() => null, (err) => ({ err }))`, then `if (box) throw box.err ?? new Error(...)`. Never resolve a promise *with* the raw thrown value. Update the PR body and fragment rows to match.
- **Regression test the owner should add:** whole-erasure driver where the `UPDATE data_subject_requests` (step 12) rejects with (a) an ordinary Error, (b) a revoked Proxy, (c) a getter-throws Error. Assert in all three that `SELECT wallet_address` and the publish both run, the DEK is destroyed and `success === false`. Cell (b) must fail on the current head.

### N1: NOTE. Line 670 (held) logs the getter's own thrown message at both base and head
In the PII scan, the only hit for an unreadable value (1 hit over 105 logged arguments) is fault point k=12 (step 5c, line 670) with a getter-throws value. The getter's inner `Error('… MARKER … email')` escapes the unguarded catch, and the outer "Erasure failed" line logs it, because it is a readable Error. Base gives the same result. Excluding line 670, the scan finds **0 hits**. The positive control fired: an ordinary Error with the marker in its message gave 38 hits. This is not a PR 2009 finding (line 670 is held by ruling). Pass it to KS-1953 as a consideration. Evidence: `ev_q2q3q4_table.txt` (Q4 line).

### N2: NOTE. Nothing in the PR pins line 670, so a later guard there would pass the PR's suite
The G670 mutant (the same guard added at line 670) passed **45 of 45** (the seat's 43 cells plus my 2 harness runners, which collect data and do not assert). The gate's fault matrix does catch it. At k=12 with an unreadable value, base and head give `success=false`, 13 calls, DEK not destroyed. G670 gives `success=true`, 33 calls, DEK destroyed, published. That is exactly V's step table: steps 5d, 5f and 5g skipped, steps 7 to 13 run. Evidence: `mutants/G670_pin.txt`. This is by ruling, not a finding. It belongs in KS-1953's test.

### N3: NOTE. PR body was not read live
`gh` is not logged in on this host, and I did not use another project's GitHub identity. I read the seat's local draft (`…/Blockchain/5_Project_History/2026-11-05_seatV-20th/drafts/pr_body_ks1938.md`, 17:57) instead of the live body. The draft contains:
- the held line 670 with its pointer, written as plain words "KS 1953" (the seat says this is deliberate),
- the per-site table,
- Node v26.8.1, not LTS, with no Node 24 on the host,
- the NOT-run list: no real Postgres or stack, no four platform suites, hook legs 3, 4 and 8 skipped.

Whether the live body matches the draft is UNVERIFIED.

## Answers to the commission's questions

1. **Scope.**
   - Files: exactly the 4 paths, +549/-15, in one commit whose parent is the base.
   - `gdprService.ts`: 17 hunks. All 15 removed lines are thrown-value reads inside log calls. Every added non-comment line is either a `try { reason = … } catch { reason = 'unreadable thrown value' }` guard, the `code` guard, or the same log call (same level, same message) taking `reason`/`code`. No SQL, step order, transaction boundary or return shape changed (`ev_service_diff_U0.txt`).
   - Inside the erasure function, the only change is the two log-guard hunks (`ev_erasure_fn_diff.txt`).
   - Site count, from the source (not the seat's figures):
     - base: 17 catch blocks bind the thrown value, 2 of them guarded (the retention ones, `:509`/`:519`). That is 15 unguarded.
     - head: 17 binding catches, 16 guarded, plus the `code` guard.
     - The only unguarded one at head is line 704 (= base 668/670).
     - The 9 `catch {}` blocks that bind nothing are the same at base and head.
     - `:936`'s rejection handler reads `err ??`, which does not trigger a Proxy trap. Not counted, but see F1.
2. **Behaviour.**
   - Seat's file at head: 43 of 43 pass. At base: 28 fail and 15 pass. All 28 are `expect()` mismatches, and none is a control (`ev_newfile_*.log`).
   - My own cells (`ev_q2q3q4_table.txt` "extra cells"), comparing base to head:
     - export, each of the 6 sections × {proxy, getter}: base rejects, head leaves the section out, the same as ordinary.
     - recordConsent: proxy/getter reject "Failed to record consent", as for ordinary.
     - withdrawConsent: `false`.
     - createDSR: wrapped error.
     - updateDSRStatus: rejects with the value itself.
     - erasure: 38 fault points.
3. **Erasure.**
   - Fault injection at every one of the 38 calls (DB, DEK and publish) of a full erasure, × {ordinary, proxy, getter}, at base and at head.
   - head-unreadable equals base-ordinary in outcome, call sequence, DEK and publish at **73 of 76**.
   - The differences:
     - k=12 proxy and getter: line 670, held, the same as base-unreadable.
     - k=35 proxy: **F1**.
   - Paths where head completes MORE than base-ordinary: **0**. Head returns `success=true` where base-ordinary returned false at **0** points.
   - Control: base-ordinary equals head-ordinary at 38 of 38.
4. **Logging.** 0 marker or PII hits from the new line over every logged argument (deep-walked), excluding the held line 670 (N1). The control fired with 38 hits.
5. **Mutants** (`mutants/`). Every tamper asserted present and source sha256 restored after each run (`4b15c272…`).
   - Seat's S02, S06 and S13 tampers (guard turned into a rethrow): each fails exactly its own 2 cells.
   - (i) G670: the seat's suite stays green. The gate matrix catches it (N2).
   - (ii) SWALLOW (outer catch returns `success:true` for an unreadable value): the seat's S06 cells fail (2). The gate matrix shows 69 points completing more than base.
6. **Suites.** Each check was run at base and at head, with a planted defect as control.

   | Check | base | head | planted defect |
   |---|---|---|---|
   | originate jest | 211 files / 2478 cells | 212 / 2521 | n/a |
   | `tsc --noEmit` over the service | 15 TS2742 | the same 15 | TS2322 + TS6133 caught |
   | eslint on the changed files | n/a | 0 errors, 0 warnings | unused var flagged |
   | `docs-fragments.mjs check` | OK (156 new) | OK (157 new) | second `<h2>` gives rc 1 |

   - **jest:** the delta is +1 file and +43 cells, matching the seat. In both runs 2 suites (`ks794-…`, `ks978-…`) fail to compile: TS2305 `getRefId`, the same on base. This is environmental, from this gate's copied `node_modules`. It is why my cell totals are lower than the seat's 2496/2539.
   - **tsc:** the TS2742 errors are environmental: the `packages/shared` deps were installed fresh in my clone, because the hook refused to copy them. None is in `gdprService.ts`, and the error sets at base and head are identical.
   - **eslint:** run through the ESLint API with cwd `Blockchain/Dev`. **Retracted in the open:** my first eslint run passed `-c` from the wrong cwd, so the flat config matched no file. It reported "file ignored" and a parse error, which reflected my instrument and not the code.
   - **docs-fragments:** 2 ADVISORY lines about the committed pages, the same at base.
7. **Merge tree** (in my clone): `git merge-tree --write-tree 5fc5569e 86eb3152` gives rc 0, tree `ffc09c366d7a4eb7869c8435a3998db1dce84e6f`, identical to the head's own tree (base is an ancestor).
8. **PR body:** see N3 (draft read, not the live body).

## Readings (shared checkout, read-only; branch beside each SHA)
- 07:02:04Z: shared checkout on `develop` at `5fc5569e`.
- 07:16:34Z: `ls-remote` gives develop `5fc5569e`, `refs/pull/2009/head` `86eb3152`. Checkout on `develop` at `5fc5569e`.
- 07:17:45Z: the same refs. The head did not move during the gate.

## NOT tested (Rule 2)
- Real Postgres, Prisma or event bus. All faults go through plain-function stand-ins, so whether a real driver ever rejects with a revoked Proxy is not shown.
- No booted stack, no route-level erasure call, no Schemathesis, Akto, Playwright or k6.
- Node v26.8.1 only. This is not LTS and there is no Node 24 on the host.
- The connector-erasure function: my "connector-hash" cells ended at the ref-never-seen early return, so they exercised nothing. Connector coverage rests on the seat's S13/S14 cells and on the S13 mutant.
- Inside the erasure matrix, the lifecycle 5d decode loop and the 6b row loops ran with empty result sets, so only their SELECTs were fault points.
- Audit gates and the pre-push hook were not re-run.

## Environment / tooling notes
- Clone: `clone/`, made by a local clone of the shared checkout and checkout by SHA in the clone.
- `node_modules`: copied from the shared checkout (`Blockchain/Dev` and `services/originate`).
- `packages/shared`: the guard hook refused `cp` and `tar` reads of the shared tree (false positives), so I ran `npm ci` and `npm run build` inside the clone (`ev_shared_*.log`). A first self-build that lacked the nested deps is quarantined in `_quarantine_2026-11-05/`.
- The gate's own harness (`gate_harness/`) ran inside the clone only, then moved to quarantine before the full-suite runs. Nothing was written to the shared checkout or to any other project.
