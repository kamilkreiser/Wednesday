# QA Gate 149 verdict: Secuura/Distributed_Secuura PR 1964 (KS-1868, originate routes/documents.ts: six catches on sign/request, sign, lifecycle-events, sign-cert, sign-wallet, sig-json), TIER 1, round 1

## BLUF
**GO WITH NOTES. Nothing has to be fixed before merge.**

I ran the real document routes in their own Node process (tsx) for every cell, at base, head, the merged product state, and develop-without-the-PR, each in NODE_ENV development and production with the REAL originate winston logger (production File transports included). Real: `routes/documents.ts`, `repositories/documentRepo.ts` and `lifecycleEventRepo.ts` with their own inner catches, the in-memory signing-request map, express 4 and express-validator, the real `verifyMessageSignature` against a real CIP-8 Ed25519 signature, and index.ts's `unhandledRejection` / `uncaughtException` handlers (copied verbatim, with the exit recorded instead of performed). Replaced: `../db` (the Prisma client, by an in-memory documents/lifecycle model that can reject before a write or AFTER applying it), `../middleware/auth` (a fixed authenticated user), `publishEvent` (a recorder) and the auth-service `/api/issuer-certs/sign` hop (a loopback stand-in). 1200 cells (8 runs x 150), all rc 0 (logs/probe/*.jsonl, logs/probe_table.log).

**The class bar is met at all six catches.** For every route, every injection point (driver-level L1 and repo-boundary L2, before and after the write) and both log formats, **head with any of the 6 unreadable values == base with an ordinary Error**: the same status and body code, the same persisted document/signature/derived-row state, the same signing-request (nonce) state, the same retry result, and no unhandled rejection or uncaught exception. 288 of 288 head cells compared, 0 differences. Merged == head and devnow == base in every cell.

- **Q1 (RUN): no new outcome.** A failure AFTER the write gives 500 with the write left standing, and a retry duplicates it. Head does exactly what an ordinary Error already does at base. At base an unreadable value gave the same persisted state with NO answer (or a process exit). The duplicate on retry is real and pre-existing (G149-F1, F2).
- **Q2: confirmed vacuous.** The PR's `unhandled` assertion counts 0 for a deliberate rejection (positive control). No mutant survives because of it: jest-circus fails the cell itself on a leaked rejection. The behaviour change (hang to 500) is pinned by the null-answer assertion in the 6 revoked-Proxy cells.
- **Q3: met.** Only the logged `error` text differs (the constant, or a coerced string).
- **Q4: compliant.** No changed line logs document content, a signer's identity or a key.

The author's figures all re-measure: red first 9/13 + 9/13 (18/26) by assertion, originate 2334 -> 2360 all pass, tsc with tests 0 -> 0, eslint 0, fragments clean with planted defects caught. Mutants: 48/48 killed, plus 12 re-checks (section 5).

Host Node v26.8.1 throughout. **Nothing was measured on Node 24.**

## Heads
- START (logs/head_start.log, 20:10:44Z): PR head `25c437f49fbb677db09828e4f74c5ff3230ecdc4` (= the pin), develop `26955bf1b828` (= the commission's NOW). Merge-base `4d1ab2cb6574` (= the READY's base). 1 commit.
- END (logs/head_end.log, 20:40:53Z): the PR head is unchanged. **develop moved to `7ad0dcc1`** (KS-1868 kyc + wallet-connector user-erased handlers, 6 paths, none in originate). merge-tree was re-run onto it (section 6).
- The clone's HEAD is 25c437f4 and `git status` is clean (logs/status_end.log). The product sha256 equals the head blob. Every swap was sha-restored: probes_restore OK, suites restore OK, static restore OK, and mutants `restore=True` x60.
- **PR body not read through the API** (no gh login on this seat). I used the READY mail (evidence/r76_pr1964_ready.txt), read whole.

## 1. Diffstat (logs/diffstat.log, three-dot vs merge-base 4d1ab2cb)
5 files, **+560/-6**, as declared:

| file | + | - |
|---|---|---|
| routes/documents.ts | 42 | 6 |
| lookup test | 236 | 0 |
| signing test | 236 | 0 |
| flow fragment | 23 | 0 |
| cheat fragment | 23 | 0 |

Nothing outside the declared paths.

## 2. The hunks (logs/product_diff.log)
Six identical guards (head lines 1285, 1372, 3208, 3485, 3680, 3747). Each one replaces `error instanceof Error ? error.message : String(error)` in the catch's log call with this:
```
let reason: string; try { reason = String(error instanceof Error ? error.message : error); } catch { reason = 'unreadable thrown value'; }
```
The logged call is then `logger.error('<same message>', { error: reason })`.

What changes:
- An unreadable value is logged as the constant, and the route answers.
- A non-string message is now `String()`ed: BigInt `10n` -> `"10"`, Symbol -> `"Symbol(desc)"`. A null-prototype message becomes the constant.

What does NOT change:
- the messages, levels, status codes and bodies
- every try body, so no ordering of reads and writes moves
- the inner catches (sign-cert's fetch catch -> 502, assertNoCycle's LINEAGE_CYCLE -> 422)
- the repositories
- the GET /:id catch at :1232, which still has the unguarded read; it is not in this PR's six

## 3. Behaviour (RUN; READ where marked)
**Values:**
- ordinary: `Error('Connection terminated unexpectedly')`
- plainString
- unreadable: revokedProxy, getterThrows (the message getter throws an Error), getterThrowsRevoked (the getter throws a revoked Proxy), msgBigInt, msgNullProto, msgSymbol

**Injection points:**
- L1 = the DB model rejects (select_doc, select_lc, walk = assertNoCycle's ancestor SELECT, update/insert = AFTER applying the write)
- L2 = the repo function the route calls rejects (getDocument, listLifecycleEvents before; updateDocument/saveDocument AFTER the real function wrote)

Every post-write cell then retries the identical request with no fault.

### Base vs head (development; production identical except as noted). HANG = no answer in 1500 ms, U = unhandled rejection, X = index.ts uncaughtException -> exit(1)
| route / injection | base: unreadable values | head: every value | base ordinary = head unreadable? |
|---|---|---|---|
| sign/request L1 select_doc | 500 for all except getterThrowsRevoked HANG-U | 500 | yes |
| sign/request L2 getDocument | revokedProxy, getterThrows, BigInt HANG-U; **getterThrowsRevoked HANG-X**; nullProto, Symbol 500 | 500 | yes |
| sign L1 select_doc / L2 getDocument | as sign/request | 500 | yes |
| **sign L1 update (post-write)** | 500 for all except getterThrowsRevoked HANG-U; signature written | 500 | yes |
| **sign L2 updateDocument (post-write)** | revokedProxy, getterThrows, BigInt HANG-U; getterThrowsRevoked HANG-X; signature written | 500 | yes |
| lifecycle L1 select_lc / L2 | revokedProxy, getterThrows, BigInt HANG-U; getterThrowsRevoked HANG-X | 500 | yes |
| sign-cert / sign-wallet L1 select_doc | getterThrowsRevoked HANG-U | 500 | yes |
| sign-cert / sign-wallet L1 walk | getterThrows, BigInt HANG-U; getterThrowsRevoked HANG-X | 500 | yes |
| **sign-cert / sign-wallet L1 insert (post-write)** | 500 for all (the repo's catches convert the value) | 500 | yes |
| **sign-cert / sign-wallet L2 saveDocument (post-write)** | revokedProxy, getterThrows, BigInt HANG-U; getterThrowsRevoked HANG-X | 500 | yes |
| sig-json L1 / L2 | as sign/request | 500 | yes |

In production format, BigInt does not hang at base: the json format serialises it. Everything else is the same (logs/probe_table.log).

### Q1: failure injected AFTER the write (RUN)
**POST /:id/sign** (getDocument -> nonce checks -> push signature -> `updateDocument` -> `deleteSigningRequest` -> 200):

| | first answer | after the first call | nonce | retry (same body) | after the retry |
|---|---|---|---|---|---|
| base ordinary | 500 | status signed, **1 signature** | still valid | **200** | **2 signatures** |
| base unreadable (reaching the catch) | **no answer** (or exit for getterThrowsRevoked) | signed, 1 signature | still valid | 200 | 2 signatures |
| head, every value | 500 | signed, 1 signature | still valid | 200 | 2 signatures |

- **Yes: a client can be told 500 while the signature is persisted, and a retry within the 5-minute nonce window appends a second signature.**
- That is **pre-existing for an ordinary Error** (and for an ambiguous commit, where the driver reports failure after a commit). It is not new in this PR. Head's after-state equals base-ordinary's in every column.
- At base the unreadable path was strictly worse: the client got no answer at all and was then just as likely to retry. → G149-F1.

**POST /:id/sign-cert and /:id/sign-wallet** (saveDocument -> logger.info -> publishEvent(document.versioned) -> 201):
- At base-ordinary and at head for every value, a failure after the INSERT gives **500 with a derived document with status `signed` persisted**, carrying the sigJson / sigWallet envelope. For sign-cert, that envelope is servable from the public GET /:id/sig-json.
- `document.versioned` is NOT published.
- A retry mints a **second** derived signed document (derived 1 -> 2, one event). Pre-existing duplicate. → G149-F2.

**POST /:id/sign/request (READ):** the only write is the synchronous `saveSigningRequest` followed by `res.json`, so there is no awaitable step after the write and no post-write injection point. An orphan nonce is harmless: it expires after 5 minutes.

**Side effects (READ + RUN):**
- None of the six routes anchors, writes a lifecycle event or sends mail. Anchoring is explicitly not auto-triggered on sign-cert/wallet (comments at the head lines 3389 and 3626 region).
- The only event is `document.versioned` after a successful save (recorder: 0 events on every failed first call, at base and head).

**Base impact was worse than "never answers" (RUN):** with getterThrowsRevoked, the route's catch throws a readable TypeError, but index.ts:79's own handler then does `reason instanceof Error`. In the getter case the rejection reason is the revoked Proxy itself, which throws inside the handler. That raises `uncaughtException`, and index.ts:86 **exits the process after 100 ms**: 10 "X" cells per base run. Head answers 500 and the process stays up. → G149-F3.

### Reachability through the real repository (RUN; logs/probe/*.jsonl "otherLog")
documentRepo's own catches read the value unguarded before rethrowing:
- getDocument :265 `err?.message?.includes(...)`
- saveDocument :501 `fkMsg.includes` and :518
- updateDocument :697

So at L1 most hostile driver values reach the route catch as a READABLE TypeError (for example "Cannot perform 'get' on a proxy that has been revoked", or "err?.message?.includes is not a function"), and base already answered 500. The values that reach the PR's guards unreadable are:
- an Error whose message getter throws an unreadable value (all six routes)
- every hostile value at lifecycle-events (`listLifecycleEvents` has no catch)
- getter or BigInt values from walkAncestors at sign-cert/wallet

The PR's cells mock the repository, so they bypass the repo's catches. The lookup test's header ("the document read itself, which has no inner catch") is accurate only for the mock. → G149-F4.

## 4. Re-measure (jest via scripts/jest.js: `-c` and `--rootDir` = the clone's originate, cwd = logs/child_cwd)
- **Red first** (base documents.ts + the two new files; logs/red_base_new.log): **18 failed | 8 passed (26)**, = the READY's 9/13 + 9/13. All 18 fail by AssertionError, with 0 crashes:
  - **6 by null answer** (the revoked-Proxy cells R1/R4/R7 in each file; base hangs)
  - **6 by `<object>`** (null-prototype message: base answered 500 and logged the object)
  - **6 by `<symbol>`**

  So 12 of the 18 red cells are log-shape cells, not behaviour cells.
- **Head:** new files 26/26.
- **Whole originate suite:**
  - base without the new files: **200 suites / 2334, rc 0**
  - head: **202 / 2360, rc 0**
- **tsc including tests** (scripts/tsconfig.tests.json; logs/tsc_summary.log):
  - head **0** (298 files, 232 under __tests__, both PR files listed)
  - base **0** (296 / 230)
  - planted: **1 TS2322**, rc 2
  - service `tsc --noEmit`: 0
- **eslint** (originate's flat config, cwd originate): the product + both test files, **0 problems**. The base product: rc 0. Planted: 1 error + 1 warning, rc 1.
- **docs-fragments `check`:** rc 0 ("flow 117 legacy + 112 new, cheat 112 + 112; lint clean, render passes"). Planted defects, each rc 1 with one finding naming KS-1868-documents-routes.html:
  - flow: unclosed div
  - flow: `<!--n-->.` removed
  - cheat: unclosed div
  - cheat: `</table>` corrupted

  Each was sha-restored; rc 0 after.
- **Q2, the positive control** (scripts/zz_g149_pc.test.ts; logs/pc_unhandled.log): with the PR's exact listener shape, `process.listenerCount('unhandledRejection')` is 1 inside the test, yet a deliberate `void Promise.reject(new Error(...))` is counted **0** times. **The `expect(unhandled).toBe(0)` assertion is vacuous.** Confirmed.

## 5. Mutants (scripts/mutants.py, mutants2.py, mutants3.py; documents.ts only, tests untouched, sha256-restored and checked after every run)
**Main table (logs/mutants_table.log): 48 mutants, 6 sites x 8: 48 killed, 0 survived.**

| mutant | each of the 6 sites |
|---|---|
| M0 revert to the base read | KILLED by assertion (null answer + log shape) |
| M1 inner catch rethrows | KILLED by null answer |
| M2 constant always | KILLED by controls C* |
| M3 wrong fallback text | KILLED |
| M4 String() dropped | KILLED |
| M5 instanceof dropped (`String(error)`) | KILLED by the controls |
| M6 log field replaced | killed by a **ts-jest compile error** (unused `reason`), not a cell; re-run as M6b `error: reason && 'x'` (logs/mutants2_table.log): **KILLED by assertion x6** |
| M7 answer 500 + `void Promise.reject(error)` | "killed" only because **jest itself crashed** ("Test suite failed to run: Cannot perform 'IsArray' on a proxy", inside jest-circus formatting the revoked Proxy); all 13 cells passed |
| M7b answer 500 + leak a READABLE rejection only on the unreadable branch (mutants3_table.log) | **KILLED x6**, by jest-circus attributing the leaked rejection to the running cell ("g149 leak" at documents.ts:1377), not by the PR's listener |

**Q2 count:** 0 mutants survive because of the vacuous assertion. The leak class is caught by jest-circus's own handling (readable leak) or by a jest crash (revoked-Proxy leak). The PR's listener plays no part in either. The behaviour change is pinned by `expect(await call(...)).toEqual({status:500,...})`, which fails with `null` when the guard is removed (M0/M1, in R1/R4/R7 of each file).

## 6. merge-tree (scripts/mergetree.sh)
**Onto `26955bf1`** (logs/merge_tree_26955bf1.log):
- rc 0, tree `ba56ded1`
- the merged-vs-develop paths == the 5 PR paths
- documents.ts in the merged tree == the head blob `0c08f8ea`

**Squashes since base:**
- 2f9f7db3 (1960, gateway redis.ts, 4 paths)
- 0b381018 (1961, originate errorTrackingService.ts + lifecyclePayloadCodec.ts, 6 paths)
- 26955bf1 (1962, transfer approvalWorkflowService.ts, 4 paths)

PR-path overlap is **0** (positive control 14).

**Does the PR read a squash path?** Yes, indirectly: `lifecycleEventRepo.ts:26` imports `decodeLifecyclePayload` from lifecyclePayloadCodec.ts (1961), on the lifecycle-events route. The "merged" probe variant (develop's two originate files + head documents.ts) == head in every cell, and "devnow" == base. errorTrackingService.ts is not imported by documents.ts.

**develop moved to `7ad0dcc1`** (KS-1868 kyc + wallet-connector, 6 paths, no originate) (logs/merge_tree_7ad0dcc1.log):
- rc 0, tree `f171de7c`
- paths == the PR's paths
- product blob equal
- overlap 0

## 7. Kam's ks1346 rule (Q4)
- No new log line, no new field name. The six changed lines keep their message and level and log only `error`.
- The constant `'unreadable thrown value'` is a type statement: compliant.
- A readable message is logged as before. That is base practice and pre-existing for the class: driver error text.
- **Does any changed line log document content, a signer's identity or a key? No.** The lines carry only the caught value's message. Driver/Prisma messages are not known to carry row values, and the signature, wallet key and cert PEM are never in a thrown value on these paths (READ).
- **Coercion changes, measured with the real logger:**
  - BigInt `10n` -> `"10"`
  - Symbol -> `"Symbol(desc)"` (base console printed `{}`, the field dropped)
  - null-prototype -> the constant (base console `{"error":{}}`)
- **In production FILES** (keepFileFields keeps `error` only when it is a string), base dropped these non-string messages from logs/error.log. Head now writes them as text (logs/child_cwd/{base,head}_production/logs/error.log). That is more message text in the files, but no new kind of content, and no secret carrier is known. Compliant, INFO (G149-F6).
- **Where the log files landed:** the production-mode probes wrote only under `logs/child_cwd/<variant>_production/logs/{error,combined}.log` (each probe chdir'd there). jest ran with cwd `logs/child_cwd`.
  - Wednesday's `/Volumes/DevMASTER/WEDNESDAY/logs/combined.log` mtime is 06:01 local. This gate started at 07:09, so it was not written.
  - No `node_modules` or `.vite` appeared in Wednesday's tree.

## 8. Notes for the PR body
- **G149-F1 (recommended follow-up, pre-existing, measured; NOT new):** POST /:id/sign is not idempotent across a failure after its write. If anything fails after `updateDocument` (an ambiguous commit, or a rejection from the repo after the UPDATE), the caller gets 500 while the signature is persisted, the status is `signed`, and the nonce is NOT consumed. A retry within 5 minutes answers 200 and appends a **second signature entry**. Base-ordinary = head-every-value (and base-unreadable, which gave no answer). **Suggested fix (own ticket):** consume the nonce before the write (delete, then write, then restore on a definite pre-commit failure), or make the append idempotent on (signerId, nonce).
- **G149-F2 (recommended follow-up, pre-existing, measured; NOT new):** for sign-cert and sign-wallet, a failure after `saveDocument` answers 500 with a derived `signed` document persisted, carrying the sigJson/sigWallet envelope (the sig-json one is publicly servable), and no `document.versioned` event. A retry mints a second derived signed document. **Suggested fix:** an idempotency key, or a deterministic derived id with `conflictMode: 'skip'` keyed on (parent, signature).
- **G149-F3 (INFO, measured; add to the body):** the base impact was worse than "never answers". For an Error whose message getter throws an unreadable value, index.ts's `unhandledRejection` handler itself throws (`reason instanceof Error`). The resulting `uncaughtException` handler **exits originate** (exit(1) after 100 ms), on all six routes. Head answers 500 and stays up.
- **G149-F4 (recommended follow-up, KS-1868 scope; INFO for this PR):** documentRepo's own catches read the value unguarded:
  - getDocument :265-266
  - listDocuments :298
  - saveDocument :501/:518
  - updateDocument :697

  Through the real repo, most hostile driver values become a readable TypeError before reaching these route catches, so the PR's guards are reached unreadable mainly via getter-throws-unreadable values, listLifecycleEvents (no catch) and walkAncestors. The repo catches are remaining KS-1868 sites. The lookup test's header sentence "the document read itself, which has no inner catch" holds only for the mock; suggest rewording it. Also still unguarded in this file: GET /:id's catch (:1232).
- **G149-F5 (recommended, test hygiene):** the `unhandledRejection` listener assertion in both files is vacuous: a positive control counts 0 while the listener is registered. It is harmless, since jest-circus fails the cell on a leaked rejection (mutant M7b killed x6), but it reads as a guarantee it does not give. Remove it, or replace it with a comment naming jest-circus as the leak detector. Also, 12 of the 18 red cells are log-shape cells (null-proto, Symbol); only the 6 revoked-Proxy cells pin the hang -> 500 change. Optionally add a getter-throws-unreadable cell, which is the one shape that reaches the guard through the real repo.
- **G149-F6 (INFO, ks1346):** non-string messages are now logged as text (BigInt, Symbol). In production log FILES the `error` field now appears for them, where base dropped it. No new field and no new content kind; compliant.
- **G149-F7 (recommended follow-up, pre-existing, READ + measured):** POST /:id/sign's signature "validation" is `signature.startsWith('mock_signature_') || signature.length > 50` (head :1343). There is no cryptographic check, so any authenticated caller with document access can record an arbitrary wallet signature and set the status to `signed`. The probe's `mock_signature_g149` was accepted with 200. Untouched by this PR. It needs its own ticket (compare sign-wallet, which verifies CIP-8 server-side).
- **G149-F8 (INFO, host):** on Node 26.8.1, `cbor@9.0.2`'s `encode` truncates arrays and maps to their header byte (measured: `encode([1,2])` -> `82`). The real `verifyMessageSignature` therefore refuses every wallet signature on this host. The probe shimmed `cbor.encode` with a minimal correct encoder (scripts/cborlite.js; decode stays real). Not measured on Node 24. The shared wallet-signature test was not run here.
- **G149-F9 (INFO):** every author figure re-measures:
  - red 18/26 by assertion
  - 2334 -> 2360
  - tsc with tests 0 -> 0
  - eslint 0
  - fragments with planted defects rc 1

  develop moved to 7ad0dcc1 during the gate; merge-tree is clean onto both heads, with 0 overlap.

## 9. NOT TESTED
- the live PR body via the API (no gh login)
- a real PostgreSQL / Prisma client: the documents and lifecycle tables are an in-memory model; the SQL is dispatched by statement shape, not executed
- a real ambiguous commit (modelled as "write applied, then reject")
- the real `authenticate()` (JWT/JWKS/session; replaced by a fixed user) and the real RBAC scopes for the sign routes (rbac ran for real)
- the gateway hop, and a booted `index.ts`: middleware such as `boundedJson`, `tenantGucContext` and overload protection were not mounted; the index.ts process handlers were copied verbatim, and exit was recorded, not performed
- a real Redis event bus (publishEvent recorder)
- the auth-service issuer-cert signer (stand-in)
- multi-tenancy pools
- the GET /:id catch (not in the PR)
- suites, tsc and fragments on the merged tree (merged product probes only)
- the four platform suites
- CI and the pre-push hook (quoted from the READY mail only)
- Node 24
- Spark shadow review (not requested)

## Processes
Every background run I started has finished:
- npm ci + shared build
- the probe matrix (8 child processes, each exited 0)
- the suites/static/positive-control/mutants chain, then mutants2 and mutants3 (foreground)

Two duplicate wait-loops I started were stopped with TaskStop. `ps` shows no process with this workdir in its command line.
