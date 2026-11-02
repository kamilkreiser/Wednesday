# QA Gate 137 verdict (TIER 1): Secuura/Distributed_Secuura PR 1955 (KS-1868, anchoring read routes + originate anchors: coerce an unreadable thrown message inside the guard; held Spark passes O82-P5/P6)

## BLUF
**GATE 137 (TIER 1) on PR 1955 at 35742c744fbd: GO WITH NOTES. Nothing has to be fixed before merge.**

This PR is the G114-F1 follow-up. Gate 114 found that a message which can be READ but cannot be PRINTED still crashed the logger inside the catch. All six guards now coerce the message inside the same try. I ran:
- anchoring: the REAL `index.ts` app (real routes, real `log()`, real shared errorHandler, real RS256 auth) on loopback. The verify-by-hash cells were sent with NO bearer, which is the unauthenticated route.
- originate: the REAL `anchorsRouter`, errorHandler and **REAL winston**, in `development` (printf) and `production` (json + both file transports).

Both ran at base `9a9bf86967e3` and at head. Replaced: `../db` (a stateful stand-in, writes counted), `../cardano` and the Blockfrost provider (a chain stand-in, submits counted). Kinds: 19 thrown-value kinds (gate 114's 11, plus 8 new ones: message `undefined` / `null` / number / plain object / custom toString / non-idempotent getter, a message-less object, and `new Error()`). Cells: 5 anchoring, 3 originate x 2 formats. The judge ran **1434 checks with 0 fails**, and three planted tampers each gave rc 1.

- **Q1/Q2:**
  - At head, every hostile kind gets exactly the ordinary-Error answer: same status, same body, unhandled 0, and the same chain calls.
  - **No kind produced `verified:true` where an ordinary Error does not.** That holds at base and at head (judge check).
  - The only `verified:true` after a failed local lookup is the chain hit (`source:"chain"`). The ordinary Error gets it too, at base and at head (G114-F3, re-proven).
  - What changed is the hostile kinds `msgRevokedProxy` and `msgBigInt`:
    - base: verify-by-hash answered **500 with the TypeError text in `details`**; the tx route **never answered and left 1 unhandled rejection**; POST verify answered 500.
    - head: the ordinary answer.
  - Writes 0 and submits 0 in every record.
- **Q3 (real winston, both formats):** an Error whose own `message` is `undefined` now logs `"error":"undefined"`; `null` logs `"null"`.
  - This shows on the console in both formats AND in the production FILE transports, where base wrote no `error` key at all.
  - It is originate only. Anchoring keeps undefined/null as before, and `new Error()` still logs `""`. G137-F1, info.
- **Q4:** the originate (jest) unhandled counter measured **0 of 1** with a planted rejection. Its `expect(unhandled).toBe(0)` in the 6 `route()` cells (C1, C3, R1-R4) cannot fail. Jest itself does fail the test on that rejection. The anchoring (vitest) counter measured **1 of 1**, so it is live. G137-F3.
- **Q5:** the unused `UNREADABLE` (line 46 of the held anchoring test) gives TS6133 under a tests tsconfig and an eslint warning. **No gate runs on it**:
  - anchoring is not in `check:test-types`;
  - no lint uses `--max-warnings`.

  Recommended: a test-only follow-up commit, on Wednesday's ruling. Not a merge block. G137-F4.
- **Q6:**
  - The 1953+1955 merge-tree is clean, tree `76a52d1dde0d` (= the author's).
  - A planted control on 1953 at 1955's POST-verify site gives rc 1 (CONFLICT).
  - The closest hunks are **48 lines apart**: 1955 :1315 vs 1953 :1363 in base coordinates, with 47 untouched lines between.
  - I ran the pair proof on that tree (zod 4.6.7): anchoring 776/777, the same single failure; originate's new file 12/12; anchoring tsc 0.
- **Q7:** threadTokenMint "emulator round-trip parameterises mint + spend" fails identically at base, at head and on the pair tree ("Could not serialize the data: Error: Unsupported type").
- **Re-measure:**
  - red-first 20/29, all by AssertionError (12/17 + 8/12);
  - green 29/29;
  - anchoring 759/760 -> 776/777;
  - originate **2318/2318 (198 files) -> 2330/2330 (199 files)**. The author's 2200 -> 2212 was measured before develop was merged in (G137-F5);
  - held O82-P5 + P6 byte-identical to the PR at 9a9bf869;
  - mutants **38/39 killed, all by assertion**. The one survivor is a missing control at the POST-verify site (G137-F2).
- **merge-tree:** develop moved during the gate to `9d7e871f` (PR 1951). The merge-tree onto it is clean, tree `fedd9994`, and changes exactly the PR's 6 paths.

## 1. Heads + diffstat (logs/head_start.log, head_end.log, diffstat.log)
- START 2026-11-02T15:54:20Z:
  - `refs/pull/1955/head` = `35742c744fbdec9e32f408162776d2bf9c8a511b` (as briefed);
  - develop `8150eeb3802b`;
  - 1953 `ea6d924eb5de`.
- END 16:09:00Z:
  - PR head **unchanged**; local HEAD = PR head; tree clean; product blobs = PR blobs;
  - 1953 unchanged;
  - **develop moved to `9d7e871fb771`** (one commit: KS-1868 nft-certificate, PR 1951). It shares 0 paths with this PR (logs/develop_moved.log).
- Commits: `3e125ffe` (the change, parent 3e688ee2) and `35742c74`, which merges develop `9a9bf869` in. Merge-base with develop = `9a9bf86967e3`. Author Kam Kreiser <kamil.kreiser@secuura.ai>. The message is "Refs KS-1868: ...", with no close word.
- Three-dot diff: **6 files, +522/-6**, all within the declared paths:
  - anchoring `src/index.ts` +6/-3;
  - originate `src/routes/anchors.ts` +3/-3;
  - two new tests (+270, +199);
  - one fragment pair (+21 cheat, +23 flow).

  This matches the READY mail.
- Base product = develop-now product: both blobs are identical at 9a9bf869 and 8150eeb3.
- **Held passes** (logs/held_vs_pr.log, scripts/held.sh): the canonical `out.md.checker/patch.diff` of O82-P5 and O82-P6, applied with `git apply --cached` at 9a9bf869, rc 0,0. All four code blobs are **EQUAL** to the PR: index.ts `4d6fa4f8`, anchors.ts `46207715`, tests `bb2b594e` / `6133fb03`. The held tree vs the PR differs only by the author's two fragments. Control: a corrupted context line gives rc 1.
- PR body NOT read: no Secuura gh auth was used. I used the READY mail (evidence/ready_batch.txt) and the commit message (logs/commit_message.log).

## 2. The hunks (logs/product.diff)
- **anchoring**, 3 sites: verify-by-hash step-1 catch :698, POST /api/anchors/verify content-hash catch :1315, `dbGetAnchorByTx` :1825.
  - `reason = err?.message;` becomes `const m = err?.message; reason = m === undefined || m === null ? m : String(m);`, inside the existing `try { } catch { reason = 'unreadable thrown value'; }`.
- **originate**, 3 sites: `verifyAnchorsDbReady`, the `getAnchorByDocumentId` warn, the GET `/:documentId` route catch.
  - `reason = X instanceof Error ? X.message : String(X);` becomes `reason = String(X instanceof Error ? X.message : X);`.
- Unchanged: log levels, messages, field names, every response, every control-flow edge.
  - The fall-through to the chain step, `verified:false`, `return undefined` and the 404 stay.
  - `throw err` (KS-1657), the constant 500 and `throw new Error('Database is required...')` stay.
- Behaviour change: a message that reads but cannot be printed (revoked Proxy, throwing toString, null-prototype object) now becomes the constant. A Symbol becomes its text. Number, BigInt and objects become `String()` text.
- The message is read **once** at every site; a non-idempotent getter shows getterReads 1 in anchoring (scripts/g137_anch_probe.test.ts).

## 3. Behaviour (scripts/g137_anch_probe.test.ts, g137_orig_probe.test.ts, probe.sh, judge.py, short.py; logs/probe_*.jsonl, short.txt, judge_*.log)
HOW:
- The probe files were copied into each service's `__tests__` for the run, then moved to logs/_probe_copies. The product was swapped to base and restored by sha (SHA_OK both).
- Every request carried a 1.5 s abort, so a hang is recorded as NO_RESPONSE.
- Anchoring controls:
  - an unauthenticated tx request gives 401 (the anon path really is anonymous);
  - an unauthenticated verify-by-hash with a seeded row gives 200 `source:"db"`;
  - each cell's seeded row answers 200 when nothing throws.
- Originate controls: found 200, absent 404.

**Anchoring** (base -> head; ordinary is identical at both):

| cell | ordinary | msgRevokedProxy / msgBigInt BASE | same, HEAD |
|---|---|---|---|
| tx | 404 NOT_FOUND | **NO_RESPONSE + 1 unhandled** | 404 (= ordinary), constant / "7" logged |
| hash_nochain (anon) | 404 "Blockfrost not configured" | **500 `details`: TypeError text** | 404 (= ordinary) |
| hash_chain_miss (anon) | 404 "No on-chain anchor found" | 500 + details | 404 |
| hash_chain_hit (anon) | **200 verified:true source:chain** | 500 + details | **200 verified:true source:chain (= ordinary)** |
| verify_post | 200 `verified:false` | 500 INTERNAL_ERROR | 200 `verified:false` |

For msgSymbol, msgToStringThrows, msgNullProto, msgNumber, msgPlainObject and msgCustomToString, the responses are identical at base and head; only the logged `error` changes (to the constant or to text). msgUndefined, msgNull, emptyMsgError, plainString, plainObjectNoMsg and msgNonIdempotent are byte-identical at base and head.

**Q2: can an unreadable value produce `verified:true` where an ordinary Error would not?**
- **No.** Measured over 19 kinds x 5 cells at both versions. The judge asserts that any `verified:true` after a failed lookup is only in `hash_chain_hit`, only with `source:"chain"`, and only where the ordinary Error in the same cell is also `verified:true`. Planted tampers (a hostile kind verified on a chain MISS, and a `source:db` verified on hash_nochain) each give rc 1.
- What did move: at base the hostile message made the step-1 catch's `log()` throw, so the OUTER catch answered 500 even when the chain held the hash. At head the request reaches the chain step, exactly as an ordinary Error has always done. That base 500 was fail-closed by accident (the logger crashed), not by design.
- Reachability: the rejection value comes from the pg driver via `query()`, and `:hash` is validated as 64-hex before any read. An unauthenticated caller chooses neither, so this is defence-in-depth.
- The chain answer is established by the chain stand-in's 674 metadata hash match, not inferred from the failed lookup. Read-only provider calls happen at head exactly as for an ordinary Error (judge: providerCalls equal).

**Originate** (development and production; responses identical across formats):

| cell | ordinary (base = head) | hostile BASE | HEAD |
|---|---|---|---|
| GET /:documentId, lookup throws | 500 INTERNAL_ERROR; warn + error lines | msgRevokedProxy / msgBigInt: 500, but the **warn line is lost** (winston threw) and the error line carries the TypeError text. **msgNonIdempotent: NO_RESPONSE (hang)**, because the route catch's 2nd read gives a revoked Proxy and winston throws in the async handler | 500, both lines carry a string (= ordinary) |
| verifyAnchorsDbReady direct | rejects "Database is required for anchor operations" | msgRevokedProxy / msgBigInt: **rejects with the winston TypeError**, no own line | rejects with the constant Error (= ordinary) |
| boot `Promise.all().catch` shape | warn `{error:'Database is required...'}` | warn carries the TypeError text | = ordinary |

- Writes 0 everywhere. The GET never answers 200 or 404 for a fault (KS-1657 holds).
- RUN: both apps' routes, `log()`, the errorHandlers, winston, `verifyAnchorsDbReady`.
- READ only: originate `index.ts`'s real boot (its catch was copied); a real pg/Prisma; Blockfrost; the gateway hop.

## 4. Real winston: the message `undefined` edge (Q3; logs/msg_undefined_lines.log)
| env / transport | base | head |
|---|---|---|
| development console | `Failed to get anchor {}` / warn `{"documentId":...}` | `Failed to get anchor {"error":"undefined"}` / warn `{...,"error":"undefined"}` |
| production console (json) | no `error` key | `"error":"undefined"` |
| production files (error.log, combined.log) | no `error` key (keepFileFields keeps only a string) | `"error":"undefined"` |

- `null` behaves the same way, giving `"null"`. `new Error()` logs `""` at both. Only an own `message` set to undefined or null gives these texts.
- Anchoring passes undefined/null through unchanged; its C4/C5 cells pin that a message-less throw is logged with no `error` key.
- Originate does not, and no committed originate cell pins it. G137-F1.

## 5. Re-measure (Node v26.8.1 only; NOT measured on Node 24; load 10-12)
- Install: `npm ci --ignore-scripts` rc 0 (1798 packages); `packages/shared` built rc 0.
- **Red-first** (logs/red_first_reasons.log): anchoring 12 of 17 fail, originate 8 of 12 fail, every one by AssertionError.
  - anchoring R1 `expected null not to be null` (the tx hang);
  - R5 a 500 body;
  - R9 `expected 500 to be 200`;
  - the others `'<object>'` / `'<undefined>'` vs the expected text.
  - Originate reds by `toBe` on the logged reason. With the committed stub logger, base does not crash; it passes the object through.
- **Green:** 17/17 and 12/12.
- **Suites** (logs/runs_summary.log):

  | service | base (new tests parked) | head |
  |---|---|---|
  | anchoring (vitest) | 55 files, 759/760 | 56 files, 776/777 |
  | originate (jest) | 198 files, 2318/2318 | 199 files, 2330/2330 |

  The single anchoring failure is the same threadTokenMint cell at both (Q7).
- **tsc:**
  - each service's own config: rc 0 / 0 errors.
  - with the tests: originate 0; anchoring **1** (TS6133 `UNREADABLE`, test :46).
  - planted unused const: +1 error each, restored.
  - `check:test-types` (leg 16) does not include anchoring (package.json:44).
- **eslint** on the 4 changed code files: 0 errors, 2 warnings: the `UNREADABLE` unused var, and the existing `preserve-caught-error` at anchors.ts:60. Planted `debugger` gives rc 1. No lint config uses `--max-warnings`.
- **docs-fragments** (logs/frag_outer.log):
  - clean rc 0 ("flow 117 legacy + 98 new, cheat 112 + 98");
  - 4 planted defects, each rc 1;
  - restored by sha, rc 0 after.
  - The cheat ADVISORY at :6235 is develop's own (as G90-F7).

## 6. Mutants (scripts/mutants.py; logs/mutants_table.log, logs/mut/)
- Setup: one site and one form per run; product only, tests untouched; sha256 restored after every run (39/39 `True`); worktree clean after.
- Result: **39 runs, 38 killed, every kill by AssertionError (none by timeout).**
- Forms:
  - M0 revert to the base line;
  - M1 `String(m)` for all (anchoring only);
  - M2 fallback rethrows;
  - M3 wrong constant;
  - M4 always constant;
  - M5 fallback reads the value (`String(err)`);
  - M6 template literal instead of `String()` (Symbol).
- M0 reddens exactly 4 cells at each of the 6 sites (the fragment's claim holds). M6 dies only on the Symbol cell. M4 dies on the controls.
- **Survivor:** anchoring site 2 (POST verify content-hash), M1. No message-less control exists at that site; C4/C5 cover tx and verify-by-hash only. G137-F2.

## 7. merge-tree (logs/mergetree_develop.log, mergetree_develop_end.log, pair_mergetree.log, pair_run.out)
- Onto `8150eeb3`: rc 0, tree `702179d692b4` (= the author's), SAME_PATHS, +522/-6, 0 of 63 develop paths shared.
- Onto `9d7e871f` (END): rc 0, tree `fedd99949c9a`, SAME_PATHS, +522/-6, 0 of 69 shared. The merged product blobs = the PR's.
- **Pair with open PR 1953** (head `ea6d924e`, merge-base with 1955 = 9a9bf869):
  - The only shared path is `Blockchain/Dev/services/anchoring/src/index.ts`.
  - merge-tree rc 0, tree **`76a52d1dde0d`** (= the author's).
  - The merged index.ts contains all 11 of 1953's `+` lines and all 6 of 1955's.
  - merged vs 1953 head = exactly 1955's 6 paths.
- **Planted control:** a commit on 1953 that edits 1955's POST-verify line (1953 coordinates :1320). merge-tree gives **rc 1, CONFLICT in index.ts**.
- **Line distance:** 1953 hunks (base coordinates) are at :13, :69, :302, :604, :908, :943, :1108 and :1363. 1955's are at :699, :1315 and :1824.
  - Closest pair: :1315 (1955, content-hash catch) vs :1363 (1953, the same route's ZodError `details`), **48 lines apart, 47 untouched lines between**.
  - Next closest: :604 vs :699 (95 apart).
- **Pair proof** (a local commit of that tree, never pushed; worktree `merged/`; `npm ci` gives zod 4.6.7):
  - anchoring whole suite 776/777, the same threadTokenMint cell;
  - originate `ks1868-anchors-message-coercion` 12/12;
  - anchoring tsc 0.
  - No semantic interaction: 1953 changes only the 400 ZodError branch, which runs before the lookup.

## 8. Kam's ks1346 logging rule
- No new field name or log line. Every value now logged is either what base logged, the constant, or `String()` of the message.
- Head logs LESS:
  - an object message is no longer serialised whole (base logged `{"secretField":"s3cr3t"}`; head logs `[object Object]` or the constant);
  - the TypeError text no longer reaches verify-by-hash `details`.
- A message whose own `toString` returns text now logs that text (msgCustomToString). Base logged the object's fields instead.
- Readable string messages are logged verbatim at base and head alike (pre-existing, G114-F5).

## 9. FINDINGS (notes for the PR body)
- **G137-F1 (INFO, measured with real winston, both formats):** originate now logs `"error":"undefined"` / `"null"` for an Error whose own message is undefined/null, including in the production files, where base wrote no key. Anchoring keeps them key-less. The values are harmless and unreachable by a caller, but inconsistent and not pinned. Optional: copy anchoring's pass-through into originate, or pin the current text with a cell.
- **G137-F2 (RECOMMENDED, test gap, measured):** mutant M1 (`String(m)` for every message) survives at the POST /api/anchors/verify site, because there is no message-less control there. Fix (test only): add `it('control ks1868 C6 content-hash verify: a thrown plain string ... no error key', () => verifyHash('plain boom', '<undefined>'))`.
- **G137-F3 (INFO, test quality, measured):** in jest, the originate test's `process.on('unhandledRejection')` counter saw 0 of 1 planted rejections. So `expect(unhandled).toBe(0)` in the 6 `route()` cells (C1, C3, R1-R4) is vacuous; jest's own handler is what fails such a cell. The anchoring (vitest) counter saw 1 of 1 and is live in all 17 cells. The `writes` assertions in both files guard routes that have no write path (tripwires, not vacuous by error). The author disclosed this.
- **G137-F4 (RECOMMENDED, Q5):** the held anchoring test declares `const UNREADABLE` (line 46) and never uses it: TS6133 under a tests tsconfig, plus an eslint warning. No current gate checks it. Recommendation: Wednesday rules a test-only second commit deleting line 46. It is safe to delete: `UNREADABLE` occurs once in the file, at its declaration (grep count 1; control `LOOKUP_DOWN` count 4). Merge without it is acceptable. The seat must not edit the held test without that ruling.
- **G137-F5 (INFO, correction to fragment and body):** the flow fragment cites the anchoring blob `1f8f9e2de6b9`. That is the blob at 3e125ffe, before the develop merge; the head blob is **`4d6fa4f8dfaf`**. Its originate figures "186 files, 2200 -> 187 files, 2212" are pre-merge too; at head they are **198 files, 2318 -> 199 files, 2330**. The anchoring figures and the originate blob `462077155343` are right.
- **G137-F6 (INFO, Q2, measured):** at head, a hostile message on the unauthenticated verify-by-hash reaches the chain step. A chain hit answers 200 `verified:true source:"chain"`, exactly as an ordinary Error does at base and at head. Base answered 500 with the TypeError text in `details` (an accidental fail-closed, plus a leak of internal text). No kind produces a verified answer that the ordinary Error does not, and a caller cannot choose the rejection value.
- **G137-F7 (INFO, pre-existing, read not run; KS-1868 site list):** 16 `error: x?.message` log reads remain in anchoring index.ts. Two of them are on the pre-auth verify-by-hash route:
  - :753, the chain metadata-fetch catch. A hostile Blockfrost rejection makes `log()` throw there, so `Promise.all` rejects and the outer catch answers 500. That is fail-closed, never verified;
  - :789, the outer catch, which also echoes `error?.message` in `details` (the author's disclosed board candidate).
- **G137-F8 (INFO, measured):** originate base HUNG the GET for a non-idempotent message getter (NO_RESPONSE). Head answers the ordinary 500. Head is strictly better.
- **G137-F9 (INFO):** develop moved during the gate to `9d7e871f` (PR 1951). merge-tree is clean, with SAME_PATHS and 0 shared paths. Suites were not re-run on that merged tree.
- **G137-F10 (INFO, Q7):** the threadTokenMint emulator cell fails identically at base, at head and on the 1953+1955 pair tree.
- **No FIX-BEFORE-MERGE item.**

## 10. NOT TESTED
- Node 24; CI; the live PR body; the Linear ticket; the pre-push legs (quoted from the author only).
- A real Postgres/Prisma or pg driver: all thrown values are synthetic, and whether pg can produce them is read, not run.
- Real Blockfrost: the chain step used a stand-in, with unique hashes per cell, so the cache was not exercised across cells.
- A booted originate `index.ts`: its boot catch was copied, not run.
- Originate auth: stubbed, as in the committed test.
- The four platform suites. Suites on the develop-9d7e871f merged tree.
- The other suites on the 1953 pair tree (only anchoring whole + the originate new file + anchoring tsc).
- Spark shadow review: not commissioned for this gate.
- Outbound: the anchoring and originate socket/fetch witnesses recorded no outbound connection (network records, judge). That rests on construction plus the witness, not a packet capture.
- Production file transports wrote `logs/*.log` under this session's scratchpad (g137cwd), not into any repo.
