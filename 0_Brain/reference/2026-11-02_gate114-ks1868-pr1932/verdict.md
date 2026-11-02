# QA Gate 114 verdict (TIER 1): Secuura/Distributed_Secuura PR 1932 (KS-1868, anchoring + originate anchor READ routes, six catches)

## BLUF
**GATE 114 (TIER 1) on PR 1932 at 8bd1db3680a9: GO WITH NOTES. Nothing has to be fixed before merge.**

What I ran, at base (cd9c4a7) and head:
- anchoring: the REAL `index.ts` app (real routes, real `log()`, real shared `errorHandler`) on loopback with a real RS256 bearer;
- originate: the REAL `anchorsRouter`, the REAL originate `errorHandler` and the REAL winston logger in both formats (dev printf, production json + file transports);
- `verifyAnchorsDbReady` called directly and through a copy of its only caller's boot `Promise.all(...).catch` (index.ts:410-516).

What I replaced: `../db` (a stateful anchor_store stand-in; every INSERT/UPDATE/DELETE/CREATE/ALTER/transaction counted), and for anchoring `../cardano` (readiness and wallet switchable; `submitAnchor`/`submitAndConfirmAnchor`/`submitTransaction` counting witnesses that throw) and `cardano/provider.getProvider` (a chain stand-in). 11 thrown-value kinds x 5 anchoring cells + 3 originate cells x 2 log formats, plus positive controls = 266 records. Judge: **683 checks, 0 fails**; three planted tampers (verified:true on a failed POST verify, a write on a failed GET, a 200 on a failed originate GET) each give rc 1.

- **a) No unestablished positive answer, anywhere.** No failed lookup produced a FOUND / `verified:true` / anchored answer, at base or head, in any kind. The only `verified:true` after a failed lookup is `GET /api/anchors/verify/:hash` with the chain configured AND the chain stand-in holding the hash (`source:"chain"`), which is established by the chain and is identical for an ordinary Error (G114-F3). The originate GET never answered 404 for a fault (KS-1657 holds). **Writes: 0 and submits: 0 in every record.**
- **Head unreadable == head ordinary** (revoked Proxy, throwing getter; plus null-prototype in originate, where `String()` throws) on status, body, unhandled count and log shape, with the constant logged. Ordinary, Symbol, plain-string and every hostile-message kind are identical at base and head.
- **b) No submission / wallet / UTxO / retry path touched.** Read from the diff and the callers; the witnesses stayed at 0.
- **c) Real logger, hostile non-string message:** still crashes the logger, identically at base and head (G114-F1, recommended).
- **d) ks1346:** no new value in any log line (G114-F5).
- **e) No outbound call:** none observed (section 9).
- **f) Byte identity:** the held O75-P1 + O75-P2 passes give the PR's exact product and test blobs. Mutants: 36 of 36 killed; at the originate route-catch site 4 of 6 are killed only by a jest timeout or a jest crash (G114-F2).
- **Suites:** originate 2108 -> 2114 of 2114; anchoring 750/751 -> 759/760, the same KS-562 cell failing at both.
- **merge-tree:** clean onto develop `bc8558db` (develop moved twice during the gate).

## 1. Heads + diffstat (logs/head_start.log, head_end.log, diffstat.log, old_vs_new_head.log)
- PR head `8bd1db3680a93548bf941d581e9ba13caf8e5293` at START (07:34:39Z) and at END (08:03:39Z): unchanged.
- One commit. Parent = merge-base `cd9c4a7dd3b8`. Author Kam Kreiser <kamil.kreiser@secuura.ai>. Subject "Refs KS-1868: anchor read route catches log a constant reason for an unreadable thrown value". "Refs" only, no close word.
- The three-dot diff is exactly 6 files, **+478/-6**, all 100644. Matches the READY mail.
  - M: anchoring `src/index.ts` (+21/-3) and originate `src/routes/anchors.ts` (+21/-3).
  - A: two `ks1868-*` tests (241 and 145 lines), and one flow + one cheat fragment.
- **Old head a1bb2953:** `git fetch` of it from origin answers `not our ref`, so it is not on origin. I read it read-only (cat-file / diff / log) in the author's worktree `!CODING/Secuura/Blockchain/worktrees/s-w16-anchors`:
  - same parent, and an identical commit message;
  - the diff to 8bd1db36 is **2 lines, both fragments only** (the threadTokenMint wording now "on the author's host ... another host may read it green");
  - so product and test bytes are identical, as the author said (G114-F7).
- Develop: `c234c2388a16` at START. `466a0d6c` at 07:53Z. **`bc8558db` at END.** See section 6.
- PR body NOT read (no Secuura gh auth here). I used the READY and BUILT mails (evidence/).

## 2. The hunks (logs/product.diff)
Six catches. In each one, only the read of the thrown value moves into `try { reason = <same expression as base>; } catch { reason = 'unreadable thrown value'; }`, and the unchanged log call then takes `reason`.
- anchoring `handleAnchorVerifyByHash` step-1 catch. Expression `err?.message`, then falls through to step 2 (unchanged).
- anchoring `POST /api/anchors/verify` content-hash catch. Expression `err?.message`. `foundAnchor` stays undefined, so the answer is `verified:false` (unchanged).
- anchoring `dbGetAnchorByTx` catch. Expression `err?.message`. `return undefined` is unchanged.
- originate `verifyAnchorsDbReady` catch. Expression `err instanceof Error ? err.message : String(err)`. `throw new Error('Database is required...')` is unchanged.
- originate `getAnchorByDocumentId` warn. Same expression. `throw err` (KS-1657) is unchanged, so the ORIGINAL value still reaches the route.
- originate `GET /:documentId` route catch. Same expression. The constant 500 is unchanged.

Not changed: levels, messages, field names (`error`, plus the existing `txHash` / `documentId`), every response, every control-flow edge. The verify-by-hash OUTER catch (index.ts:786-787, `details: error?.message`) is not touched; that is the author's board candidate.

**Callers** (logs/site_callers.log, callers.log):
- `dbGetAnchorByTx` has one caller, the tx route (:1277).
- `handleAnchorVerifyByHash` is only the pre-auth GET (:473).
- `verifyAnchorsDbReady` has one caller, originate index.ts:414. That caller's `.catch` logs `err?.message` and carries on.
- `getAnchorByDocumentId` has one caller, the GET route (:175).
- originate `verification.ts` :638/:1122 and `verificationV2.ts` :101 call `GET /verify/:hash`. They act only on `resp.ok && verified === true`, so a 500 and a 404 are handled alike (read).

**Q b (KS-535 territory):** no hunk is in, or is called from, a submission, status-write, wallet, UTxO, retry, reconciler or thread-mint path. `anchorReadGate.ts` and `anchorOverwriteGuard.ts` are not in the diff. In the probe, every submit witness stayed at 0 and the provider saw only read calls (`addressesTransactions` / `txsMetadata` / `txs`).

## 3. Behaviour (scripts/g114_anch_probe.test.ts, g114_orig_probe.test.ts, probe.sh, judge.py, short.py; logs/probe_*.jsonl, short.txt, judge*.log)
HOW:
- anchoring runs under vitest 4.1.12, and originate under jest/ts-jest.
- Each probe test file was copied into the service's `__tests__` for the run, then moved to logs/_probe_copies. The product was swapped to base and sha-restored (SHA_OK, tree clean).
- Kinds: ordinary (message carrying `10.0.0.7 password=hunter2`), revokedProxy, getterThrows, nullProto, symbol, plainString, msgRevokedProxy, msgBigInt, msgSymbol, msgToStringThrows (an object message with `secretField`), msgNullProto.
- Every anchoring request has a 1.5 s client abort, so a hang is recorded as NO_RESPONSE.
- Positive controls: with nothing thrown, the stand-in answers the seeded row (tx 200, verify-by-hash `verified:true source:db`, POST verify `verified:true`, originate GET 200). An absent document gives 404. So each "not found" below is a real non-establishment, not a broken store.

**Anchoring.** Cells: `tx`; `hash_nochain` (Cardano not ready); `hash_chain_miss`; `hash_chain_hit` (chain stand-in holds the hash); `verify_post`. Writes 0 and submits 0 in all records.

| cell | ordinary (base = head) | revokedProxy / getterThrows BASE | revokedProxy / getterThrows HEAD |
|---|---|---|---|
| tx | 404 NOT_FOUND | **no answer + 1 unhandled rejection** | 404 NOT_FOUND, constant logged |
| hash_nochain | 404 "Not found in local DB and Blockfrost not configured" | **500 `details`: proxy TypeError text / "getter boom"** | 404 (= ordinary) |
| hash_chain_miss | 404 "No on-chain anchor found" | 500 with details | 404 |
| hash_chain_hit | 200 verified:true **source:chain** | 500 with details | 200 verified:true source:chain (= ordinary) |
| verify_post | 200 `verified:false` | 500 INTERNAL_ERROR (shared errorHandler) | 200 `verified:false` |

nullProto, symbol, plainString, msgSymbol, msgToStringThrows and msgNullProto take the ordinary path at base and head alike: `err?.message` reads undefined or a value without throwing.

**Originate** (dev and production formats identical except where noted):

| cell | ordinary (base = head) | unreadable BASE (revoked / getter / nullProto) | unreadable HEAD |
|---|---|---|---|
| GET /:documentId, lookup throws | 500 INTERNAL_ERROR; warn + error lines with the message | 500, but **no warn line** (it threw), error line carries the TypeError / "getter boom" / "Cannot convert object to primitive value" | 500, both lines with the constant (= ordinary) |
| verifyAnchorsDbReady direct | rejects `Database is required for anchor operations` | **rejects with the TypeError / the getter's Error**, no own log | rejects with the constant Error, error line with the constant |
| boot Promise.all catch | warn "Some database connections failed" `{error:'Database is required...'}` | warn carries the raw read error text ("getter boom") | = ordinary |

Writes 0 in every originate record, and the GET never answers 404 for a fault.

**Run vs read.** RUN: the anchoring app and its routes, `log()`, the shared errorHandler; the originate router, the errorHandler, winston (both formats), `verifyAnchorsDbReady` and the boot-catch shape. READ only: the originate `index.ts` process itself (the caller's catch was copied verbatim), a real Prisma/pg, real Blockfrost, the gateway hop, and auth (stubbed in originate as in ks1657).

## 4. Real logger, hostile non-string `message` (Q c) — base = head
- **anchoring** (`log()` = `console.log(JSON.stringify(...))`).
  - msgRevokedProxy and msgBigInt make `JSON.stringify` throw INSIDE the catch, at base and head alike:
    - tx: **no answer + 1 unhandled rejection**;
    - verify-by-hash: the outer catch answers **500 with the TypeError text in `details`** ("Cannot perform 'get' on a proxy..." / "Do not know how to serialize a BigInt");
    - POST verify: 500 INTERNAL_ERROR via the shared errorHandler.
  - Never `verified:true`; 0 writes.
- **originate** (winston).
  - msgRevokedProxy: `redactSecrets` (`instanceof` on the revoked proxy) throws in both formats. The GET still answers 500 (the route catch gets winston's readable TypeError). `verifyAnchorsDbReady` rejects with the TypeError, and the boot catch logs it.
  - msgBigInt: dev format throws (same outcome as msgRevokedProxy); the production json format serialises it as `"7"` (ordinary outcome).
  - msgSymbol, msgToStringThrows and msgNullProto do not crash.
- The judge asserts base == head for every one of these. G114-F1.

## 5. Re-measure (Node v26.8.1 only; NOT measured on Node 24)
- **Install:** `npm ci --ignore-scripts` at Blockchain/Dev rc 0 (1795 packages); `packages/shared` built, rc 0.
- **Red-first** (logs/red_base_*.json, red_first_reasons.log): the new tests against the base product.
  - Anchoring **3 pass / 6 fail**: R1/R2 `expected null not to be null` (no answer), R3/R4 `expected 500 to be 404`, R5/R6 `expected 500 to be 200`. All AssertionError.
  - Originate **2 pass / 4 fail**: R1/R2 by `toEqual` (the missing warn line), R3/R4 by `rejects.toThrow`. All assertion.
  - Head: 9/9 and 6/6. Matches the author's 6/9 and 4/6.
- **Suites** (logs/suite_{base,head}_*.json):

  | service | base (new tests absent) | head |
  |---|---|---|
  | anchoring (vitest) | 54 files, 750/751 | 55 files, 759/760 |
  | originate (jest) | 177 files, 2108/2108 | 178 files, 2114/2114 |

  The one anchoring failure is the same cell at base and head: `threadTokenMint.test.ts` "emulator round-trip parameterises mint + spend" (KS-562, host layout). No cell was removed or newly failing. Matches the author.
- **tsc:** each service's own config rc 0, and a scratch config extending it with the tests (`types` node + vitest/globals or jest) rc 0 / 0 errors, at base and at head for both services. A planted unused const in each new test gives TS6133 (rc 2), and the file was restored. Configs moved to logs/_quarantine.
- **eslint** (Dev flat config) on the 2 product files + 2 new tests: **0 errors, 1 warning** (`preserve-caught-error`, anchors.ts:60, the existing `throw new Error` the author named). A planted file gives `no-debugger` rc 1 (moved to logs/_quarantine).
- **docs-fragments** (scripts/frag.sh, logs/frag_run.log):
  - clean run rc 0 ("flow 117 legacy + 79 new, cheat 112 + 79");
  - four planted defects (flow div, flow `<!--n-->.`, cheat div, cheat `</table>`) each rc 1;
  - restored by sha.
  - The cheat ADVISORY at :6235 is develop's own (as G90-F7).
- **Mutants** (scripts/mutants.py, logs/mutants.log, logs/mut/): product only, tests untouched, sha-restored after each run (all `restore_ok`, tree clean after).
  - 6 sites x 6 forms = **36 mutants, 36 killed**. The forms: revert to the base line; fallback rethrows; wrong constant `'x'`; always constant (the read dropped); fallback reads the value (`String(err)`); and per site either log dropped (anchoring) or `String()` left unguarded outside the try (originate, the G111-F2 shape).
  - All 3 anchoring sites (18 mutants): each mutant reddens only its own route's cells, **by assertion**. always-constant reddens only that route's ordinary control.
  - O1 verifyAnchorsDbReady: 5 by assertion. fallback_rethrows is red because jest's `rejects.toThrow` matcher itself throws on reading the hostile value.
  - O2 lookup warn: 6/6 by assertion.
  - **O3 route catch: wrong_constant and always_constant by assertion. revert, fallback_reads_value and string_unguarded only by the 5000 ms jest timeout** (the route throws in an async handler and never answers). **fallback_rethrows makes jest's own `formatNodeAssertErrors` crash on the revoked proxy: "Test suite failed to run", 0 tests reported** (still rc 1). Without `--forceExit`, the revert run also left jest unable to exit ("did not exit one second after"), and I had to kill that jest process (my own). G114-F2.
  - The author's "6/6 hunks, one by timeout" holds; the timeout-only kill extends to 3 of the 6 forms at that site.
- **Held passes** (logs/held_vs_pr.log, scripts/held.sh, evidence/held/):
  - Inputs: `out.md.checker/patch.diff` of the two named run dirs `spark_secuura_2026-11-02_ks_1868_o75_p1_originate_anchors_db_ready_and_get_catches_unreadable_throw` and `..._o75_p2_anchoring_read_route_catches_unreadable_throw`. Each is `SPARK RESULT: PASS (7/7)`, tip 04ff5262.
  - Each applies alone with `git apply --cached` at cd9c4a7 AND at 04ff5262, "cleanly".
  - Combined, the blobs are **byte-identical to the PR** for all four code files (index.ts `10b37f00`, anchors.ts `e2237de1`, tests `6fdeb753` / `2b9e54f6`). The held tree vs the PR tree differs only by the two fragments (the author's own).
  - A corrupted context line gives rc 1.
- Pre-push hook (13/16 legs, PREFLIGHT INCOMPLETE) and CI are the author's; I did not re-run them.

## 6. merge-tree (logs/mergetree.log, mergetree_end.log, dev_paths.log, mt_paths.log)
- Onto `466a0d6c` (07:53Z): rc 0, tree `f6d369c3`. SAME_PATHS, +478/-6, 0 of 33 develop paths shared.
- Develop re-read at END = **`bc8558db`** (PR 1929, PR 1930 and an auth KS-1868 commit merged during the gate):
  - merge-tree rc 0, tree `3f1aead6`. The result vs develop is **exactly the PR's 6 paths**, +478/-6.
  - Merged `index.ts` / `anchors.ts` = the PR's blobs.
  - 0 of 43 develop paths shared (control 43). None is in services/anchoring, originate `routes/anchors.ts` or packages/shared.
- Not re-run on the merged tree (read: 0 shared paths, identical product blobs). Develop's 3 new originate test files would join the originate suite there.

## 7. Kam's ks1346 logging rule (Q d)
- Every new or changed line logs the same field NAMES as base (`error`; the existing `txHash`, `documentId`).
  - The value is the constant for an unreadable value, or exactly what base logged for a readable one.
  - No new value, content hash or document hash reaches a log. No changed line logs the verify hash.
- At head, the unreadable values no longer put the getter's text ("getter boom") or the proxy TypeError into the verify-by-hash response `details` or into the boot warn. So head discloses LESS.
- Pre-existing and unchanged (base = head, G114-F5):
  - readable messages are logged verbatim (`password=hunter2` appears in the anchoring JSON and the originate dev/console lines);
  - an object `message` is serialised whole (msgToStringThrows: `secretField:"s3cr3t"` in the line). The production FILE transport drops a non-string `error`;
  - the outer verify-by-hash catch returns `details: error?.message` to the client.

## 8. FINDINGS
- **G114-F1 (RECOMMENDED follow-up, not FIX-BEFORE-MERGE; measured, base = head).** The guard does not coerce: `reason` keeps whatever `.message` returned.
  - A getter returning a revoked Proxy, or a BigInt, makes anchoring's `log()` (`JSON.stringify`) throw inside the catch:
    - the tx route never answers (1 unhandled rejection);
    - verify-by-hash answers 500 with the TypeError text in `details`;
    - POST verify answers 500.
  - In originate, winston throws (revoked proxy: both formats; BigInt: dev format). `verifyAnchorsDbReady` then rejects with the TypeError; the GET still answers 500.
  - Never a positive answer, 0 writes.
  - Suggested form (PR 1924's), inside the same try: `const m = <expr>; reason = typeof m === 'string' ? m : String(m);`. A `String()` throw lands in the catch, giving the constant. Add one cell per shape. This newly moves those shapes onto the ordinary path (same tier-1 class).
- **G114-F2 (RECOMMENDED, test quality; measured).** The originate test's `getAnchor()` fetch has no abort signal and does not count unhandled rejections. So at the route-catch site:
  - 3 of 6 mutants are red only by jest's 5000 ms timeout;
  - 1 (fallback rethrows a revoked proxy) crashes jest's own error formatter ("Test suite failed to run", 0 tests);
  - without `--forceExit`, the hung request keeps jest from exiting.

  The O1 fallback-rethrows mutant is red through the `rejects.toThrow` matcher throwing, not a clean assertion. Fix (optional): copy the anchoring harness's pattern, `signal: AbortSignal.timeout(1500)`, `null` on abort, assert `unhandled === 0`, and assert `verifyAnchorsDbReady`'s rejection with a `.catch((e) => e)` read inside a try. The author disclosed the timeout for the revert only.
- **G114-F3 (INFO; measured).** With the chain configured, an unreadable step-1 failure now reaches the chain scan, as an ordinary Error does:
  - a chain hit answers 200 `verified:true source:"chain"`;
  - a miss answers 404;
  - it also costs Blockfrost reads.

  The PR's cells never run step 2 (no credentials). This gate ran it with a stand-in provider. The fragment's "neither route can answer verified:true from a failed lookup" is true of the lookup; the chain can still verify, which is established, not inferred.
- **G114-F4 (INFO / card candidate; pre-existing, measured).** The anchoring read routes answer a FAILED lookup as absence:
  - tx: 404 "Anchor not found for transaction";
  - verify-by-hash without the chain: 404 "Not found in local DB";
  - POST verify: 200 `verified:false` "No confirmed anchor found".

  This is the KS-1657 class that originate's GET already fixed (fault = 500). It applies to an ordinary Error at base and head; this PR extends it to the unreadable value (instead of a hang or a 500). It is never a positive claim. Suggest a board card; not this PR's scope.
- **G114-F5 (INFO, ks1346, pre-existing).** Readable message values, and object messages in full, are logged at base and head alike; the outer verify-by-hash catch echoes `error?.message` in `details`. No new value or hash is added by this PR.
- **G114-F6 (INFO).** Develop moved twice during the gate (c234c238 -> 466a0d6c -> bc8558db). merge-tree is clean onto both, with SAME_PATHS and 0 shared paths. Tests were not re-run on the merged tree.
- **G114-F7 (INFO).** The old head a1bb2953 is not on origin. Read from the author's worktree (read-only git), it differs from 8bd1db36 by 2 fragment lines only; message, product and tests are identical. Confirmed.
- **G114-F8 (INFO).** The anchoring suite's single failure (threadTokenMint, KS-562) also fails on this gate's host, the same cell at base and head.
- **No FIX-BEFORE-MERGE item.**

## 9. NOT TESTED / UNMEASURED
- Node 24; the live PR body, the Linear ticket, CI, the pre-push legs.
- A real Postgres/Prisma (the SQL was matched by a stand-in), a real boot of either service (originate `index.ts` read; its boot catch copied), the api-gateway hop, and originate's real auth (stubbed). Anchoring auth was real (RS256 via `JWT_PUBLIC_KEY`).
- Real Blockfrost: the chain step ran against a stand-in provider. The verify-scan cache was exercised only with unique hashes per cell, not across cells.
- **Outbound network (Q e).**
  - Anchoring: `BLOCKFROST_API_KEY`, `PLATFORM_WALLET_MNEMONIC`, `DATABASE_URL`, `JWT_JWKS_URL` and `AUTH_SERVICE_URL` were unset, and the provider was replaced. A `net.Socket.connect` and `fetch` witness recorded outbound `[]`; every fetch URL was `http://127.0.0.1:<port>`.
  - Originate: the witness recorded only `localhost:undefined` (undici's sockets; host formatting is weak, as at G111/G112), outbound `[]`.
  - No leak observed; this is by construction plus the witness, not a packet capture.
- Whether a real pg/Prisma failure can produce these values (all synthetic).
- The author's own recorder (tier1_compare_pr3_w16.py) and mutant tool; this gate built its own.
- The originate production file transports wrote `logs/*.log` into this session's scratchpad (cwd moved there for the run), not into any repo or project root.
