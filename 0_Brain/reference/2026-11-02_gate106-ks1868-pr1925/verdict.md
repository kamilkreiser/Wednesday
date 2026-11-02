# QA Gate 106 verdict: Secuura/Distributed_Secuura PR 1925 (KS-1868, originate verification: O70-P2, O70-P1 in verification.ts and O66-P1 in verificationV2.ts; 6 route catches on the public verification surface, +42/-6 product), TIER 1

## BLUF
**GO WITH NOTES. Nothing has to be fixed before merge.** I ran the real `verificationRouter` and `verificationV2Router` on a loopback listener (scripts/probe.test.ts). The v2 router ran behind the REAL `authenticate({ required: false })`; only the JWKS verifier was replaced. The probe also replaced `$queryRaw` (it returns one certified document row), the heal (`healAnchorForVerify`, which counts writes the way the real one does: only with a bearer), the lineage repo and the logger. Each version ran 297 cells: 8 routes, 6 injection points, 5 thrown values plus a success control, and 4 caller kinds (anonymous, a bearer from another tenant, the owner's bearer, a bad token). The same probe ran at base fcfa5dfd and at head (logs/probe_{base,head}.jsonl, logs/probe_table.log).
- **A (status, body, persisted state).** At all six PR sites, an unreadable value at head now gets exactly the ordinary-Error outcome. That is the route's constant 500, byte-identical body and content-type, the same db calls, the same heal-write count, and one `logger.error` line with `unreadable thrown value`. This holds for anonymous, cross-tenant and owner callers. The judge passed **273 cells, with 16 PRE-EXISTING (base == head) and 8 explained below**. At base the same requests got **NO ANSWER**: the read inside the catch threw and the handler's promise rejected. There are no audit or verification-record writes on these routes. The only write is the anchor heal, which happens before any of these catches, and an unreadable value leaves it in the same state as an ordinary Error (`healapplied` and `json` cells: w=1 for both with the owner bearer, and w=0 for both anonymously).
- **B (disclosure).** **No new disclosure.** Every PR-site response body for an unreadable value is byte-identical to the ordinary-Error body. None carries an error text, field value, tenant, organisation, holder or caller identity (leak scan over all non-success cells: none). An anonymous caller learns nothing new. It now gets a constant 500 where base left the request hanging.
- **C (verdict sites).** `git diff -U0` base..head on verification.ts shows **exactly 4 hunks, each -1/+7, at the 4 catch lines**. Every other line is byte-identical, including the four verdict reads (base :880/:917/:1017/:1306, head :886/:923/:1023/:1312; logs/verdict_sites.log). No verdict changes: every success control (verified true/false, certified, the by-id existence answer) gives base == head byte-for-byte, timestamps normalised. On any failure input the PR's catches emit only the constant 500, never a verdict.
- **D (ks1346).** The new log lines carry `reason`, which is either the same expression as before or the constant. There is no new key and no new value. The unreadable cells log only the constant.
- **E (apply order).** All three `patch.diff` sha256 values match the brief (f3d965f1…, 2376d93a…, ab35ce3e…), and section_1+section_2 equals patch.diff 3/3, with the control-dir patches identical. I applied strictly at fcfa5dfd in BOTH orders (P2,P1,O66 and P1,P2,O66): every `--check` gave rc 0 with empty output, P1 applied at offset +6 after P2 (no fuzz), and both orders gave the same write-tree `0e9a3555`, **whose Blockchain/Dev equals the PR head** (head tree e4b64c22). At 04ff5262 both orders also give one tree (`d5de4526`), with product blobs `8de6937f` and `8d538d03` identical to the head. **I could not reproduce the author's id `c468ed6e7068`:** it matches neither the full tree nor any subtree I printed (logs/apply_order_trees.log). The bytes it stands for are confirmed (G106-F6).

## Heads
- START (logs/head_start.log, 03:58:14Z): PR head `0b15f314121952b2724705f15eb47f1fdb47f5ad` (equal to the brief), develop `968f17070208`, merge-base `fcfa5dfdba9b`. One commit, Kam Kreiser <kamil.kreiser@secuura.ai>, "Refs KS-1868: originate verification route catches guard an unreadable throw".
- END (logs/head_end.log, 04:20:08Z): PR head and develop **UNCHANGED**. The clone is at 0b15f314 with a clean working tree. Product files were sha256-restored after every swap (RESTORE_OK each time, and `restore True` on 54/54 mutants).
- Diffstat (logs/diffstat.log), three-dot: **7 files, +490/-6**. That is verification.ts +28/-4, verificationV2.ts +14/-2, 3 new tests (124/133/147) and 1 fragment pair (22/22). Nothing is outside the declared paths, and this matches the author's mails.
- **PR body not read** (no Secuura gh login here). I used the author's READY and BUILT AND PROVEN mails (evidence/).

## FINDINGS
- **G106-F1 (RECOMMENDED; pre-existing, NOT in this PR; measured, base == head).** The v1 `POST /verify` inner catch at head :1437-1438 (`logger.warn('Verification lookup failed', { documentId, error: dbErr?.message })`) reads the thrown value unguarded. Every failure inside the strategy block (lookup query, heal, the response write) lands there.
  - An ordinary Error or a string answers **200 `{verified:false, error:"Verification lookup failed"}`**.
  - A revoked Proxy or a throwing getter makes `dbErr?.message` throw. The new error reaches the outer (PR) catch, which answers **500 "Verification failed"** and logs the TypeError or getter text. This is the same at base and head (16 PRE-EXISTING cells).
  - With an Error whose message getter throws an unreadable value, base gives NO ANSWER and head gives the constant 500. Those are my 8 "DIFF unreadable != ordinary" cells (v1 /verify, hash and documentId; dbpre, healapplied and json). Head improves NO ANSWER to the 500 that base already gives the other unreadable values at that point. It is not a new kind of outcome, has no verdict and discloses nothing.
  - **Fix (follow-up KS-1868 pass):** guard `dbErr?.message` at :1438 with the same pattern, so that every value gets the 200 "lookup failed" answer. The same line also logs the caller-supplied `documentId` (ks1346-adjacent, pre-existing).
- **G106-F2 (RECOMMENDED; pre-existing, NOT in this PR; measured, base == head).** In `POST /api/verification/verify` strategy 2, `return respondExistenceOnly(…)` at head :1355 is not awaited inside the inner `try`. `respondExistenceOnly` is async, so any throw inside it escapes BOTH catches, and the request gets **NO ANSWER even for an ordinary Error** (cells "v1 POST /verify (documentId) | json": NO ANSWER, escaped, at base and head for every value). At head this is the one path on these routes where an anonymous caller can still leave a handler rejected. **Fix:** `return await respondExistenceOnly(…)` (the inner catch then answers 200 "lookup failed", given G106-F1).
- **G106-F3 (INFO; pre-existing; read, not run).** The four verdict-site catches (head :886/:923/:1023/:1312) are best-effort lineage catches that read `err instanceof Error ? err.message : String(err)` unguarded. For an ordinary Error they log and return empty lineage, and the verdict stands. For an unreadable value the read throws, the throw reaches the :1437 inner catch, and the verified answer is replaced by 200 "lookup failed" or a 500. Base == head, because this PR does not touch them, by the brief. Any later pass at these sites must keep the verdict byte-identical.
- **G106-F4 (INFO; read, not run).** At base, a value that escaped a PR site reached `index.ts:75`'s `unhandledRejection` handler, which reads `reason instanceof Error` unguarded. If the escaped value is itself unreadable (my `getterThrowsProxy` cells escape as an unreadable value at base), that handler would throw, which becomes an uncaughtException and an exit for restart. **At the six PR sites head removes that path.** It remains possible through G106-F2. The author already lists index.ts:75-81 as a candidate. A real boot was not run.
- **G106-F5 (INFO, mutant tooling).** M3 (the catch rethrows) makes each test FILE fail to run, because jest's `formatNodeAssertErrors` calls `Array.isArray` on the revoked Proxy (6/6 sites; my script labels it COMPILEERR, but the log shows the IsArray crash, not a TS error). It is red, but **not by assertion**, the same as G104-F5.
- **G106-F6 (INFO).** The author's apply-order tree id `c468ed6e7068` is not reproducible as any tree I can print. Both orders give identical trees at both bases, and the product blobs equal the PR head, so the claim holds in substance. The PR body should cite a reproducible id, or the blob ids `8de6937f` / `8d538d03`.
- **G106-F7 (INFO, ks1346-adjacent, pre-existing).** An ordinary Error's message is still logged verbatim (`String(error)` / `.message`). A planted `SECRETVAL tenant-owner-x HolderBob` in a message appears in the error log at base and head alike. That behaviour is unchanged. Response bodies never carry it.
- **G106-F8 (INFO, instrument note).** The author's tests inject the failure for four of the six sites before any db call (by a `req.db` getter or the first `res.json`), as they disclose. My probe adds the db-rejection, heal-applied-then-reject and response-write positions with a write counter, so the persisted-state claim is now measured for all six sites, not only read.
- No FIX-BEFORE-MERGE item.

## Q2. The hunks
Six identical replacements. In each catch, `logger.error('<ctx>', { error: error instanceof Error ? error.message : String(error) })` becomes `let reason; try { reason = <same expression>; } catch { reason = 'unreadable thrown value'; } logger.error('<ctx>', { error: reason })`. The contexts are 'File verification error', 'Verification error', 'Hash generation error', 'Status check error', 'v2 verification error' and 'v2 file verification error'. **Unchanged:** the `res.status(500).json(<constant>)` line in every catch, every try body, every verdict read, and the router/auth wiring (`verificationV2Router.use(authenticate({ required: false }))` at :64, mounts at index.ts:279/:283).

## Q3. Behaviour, measured (logs/probe_table.log)
Method: jest, real routers, express 4.22.3 on 127.0.0.1:0, real `fetch` with a 1.5 s abort ("NO ANSWER"). A wrapper on each route handler records what ESCAPES (the request still gets no answer, as in production). Injection points:
- `reqdb`: the read of `req.db` throws.
- `dbpre`: `$queryRaw` rejects.
- `dbgetter`: it rejects with an Error whose message getter throws the value.
- `healapplied`: the heal counts its write, then rejects.
- `json`: the first `res.json` throws, after the heal write.

Values: an ordinary Error (with planted tenant and holder text), a string, a revoked Proxy, a throwing getter, and a getter that throws a revoked Proxy.

| route (injection) | ordinary Error, base = head | unreadable, base | unreadable, head |
|---|---|---|---|
| v1 POST /verify-file (dbpre / healapplied / json), anon + owner | 500 "File verification failed", heal w=0 / w=1 (owner) | NO ANSWER, same writes, no log | 500 same body, same writes, log constant |
| v1 POST /verify hash + documentId (reqdb, dbgetter) | 500 "Verification failed" | NO ANSWER | 500 same, log constant |
| v1 POST /verify (dbpre / healapplied / json inside the strategy block) | 200 "Verification lookup failed" | 500 (TypeError/getter logged); getterThrowsProxy NO ANSWER | same 500; getterThrowsProxy 500 constant (G106-F1) |
| v1 POST /verify documentId (json inside respondExistenceOnly) | **NO ANSWER, escaped** | NO ANSWER | NO ANSWER (G106-F2) |
| v1 POST /hash, GET /status (json) | 500 constant | NO ANSWER | 500 constant |
| v2 POST /verify hash + documentId, v2 /verify-file (reqdb / dbpre / json); anon, cross-tenant, owner | 500 constant | NO ANSWER | 500 constant, byte-identical |
| v2, bad bearer | 401 "Invalid or expired token" (handler not reached) | 401 | 401 |

Success controls: base == head (verified true for a hash match, false for the by-id answer, 200 for /hash and /status, and the v2 match lists for every caller). Mechanical judge (scripts/table.py): **273 OK; 16 PRE-EXISTING (base == head, G106-F1); 8 explained (G106-F1); 0 new disclosure.**

## Q4. Re-measure (Node v26.8.1; NOT measured on Node 24)
- **Red-first** (logs/red_base.json): the base product gives **12 failed of 24**, split 6/12, 2/4 and 4/8. All 12 are `RED` cells failing by `expect(`, and every control passed. This matches the author.
- **Green:** head **24/24**.
- **Whole originate suite:** base without the new files **169 files, 2035/2035**; head **172 files, 2059/2059**. Cell by cell: 24 new, 0 vanished, 0 passed -> not passed. This matches the author exactly.
- **tsc:** plain `tsconfig.json --noEmit` gives rc 0. With the tests in the program (scripts/tsconfig.tests.json) it gives rc 0 and 0 errors both at base (197 test files) and at head (200 test files, 3 of them the new ones). A planted TS2322 gives rc 2 and is reported.
- **eslint** (5 changed files): 0 problems, rc 0. A planted file gives 1 error and 1 warning, rc 1.
- **docs-fragments check:** rc 0, "75 new … OK". A planted unbalanced `<div>` in the PR's cheat fragment gives rc 1, "tags are not balanced". The fragment was restored by sha256 (FRAG_RESTORED).

## Q5. Mutants (scripts/mutants.py; product only, tests untouched, sha256 restore True 54/54; logs/mutants_run.log)
6 sites x 9 mutants. **M0, M1, M2, M4, M6, M7, M8 and M9 are KILLED at all 6 sites by assertion** (1 to 4 cells each, all `expect(`). The thrown-string control kills M6 everywhere. **M3** makes the suite crash at all 6 sites (G106-F5). **0 survivors.**

## Q6. merge-tree
Onto develop `968f1707` (START = END): rc 0, tree `36a867fc`. The result changes exactly the PR's 7 paths (SAME_PATHS). Develop changed 24 paths since base fcfa5dfd (c0f9af13, 86e12156, 968f1707), **0 of them shared** with the PR.

## Q7. Kam's ks1346 rule
Every changed line logs `reason`. That is either the pre-existing expression or the constant `unreadable thrown value`; there is no new key, no new value and no new log line. At head, the unreadable cells at PR sites logged only the constant (judge). No holder, organisation or caller identity appears in any unreadable cell's error log (probe flag false). **Compliant.** Pre-existing items: G106-F1 (documentId in the warn line) and G106-F7.

## Notes for the PR body
1. G106-F2 (recommended): name `return respondExistenceOnly(…)` (head :1355, not awaited in the try) as a follow-up. On that by-id path any thrown value, an ordinary Error included, still leaves the request without an answer at base and head.
2. G106-F1 (recommended): name the inner catch `verification.ts:1437-1438` (`dbErr?.message`) as the follow-up KS-1868 site. It is why an unreadable value inside the lookup block gets 500 where an ordinary Error gets 200 "lookup failed".
3. G106-F3 (info): the four verdict-site catches remain unguarded by design. A future pass must hold the verdict byte-identical.
4. G106-F6 (info): replace or qualify `c468ed6e7068` with a reproducible id (product blobs 8de6937f / 8d538d03; both orders identical).
5. Tier-1 statement confirmed by gate 106 through the real routes with the real optional-auth middleware, a heal-write counter, and anonymous, cross-tenant and owner callers.

## NOT TESTED
- The real PR body (no gh auth); real PostgreSQL or Prisma; the real heal (`healAnchorForVerify` replaced by a counter that writes only with a bearer, as the real one does); multi-tenant mode (`getTenantManager` null, so the cross-tenant lookups `crossTenantLookup` / `crossTenantRowsByHash` and their own inner catches were not exercised); a real boot (index.ts:75 read, not run); the gateway hop and its rate limiter; Node 24; the four platform suites; CI; the pre-push hook legs (quoted by the author only).
- G106-F3 (unreadable value in a lineage walk) was read, not run.
- Whether an unreadable thrown value can occur at any of these sites in reality. The values are synthetic.
- The Linear ticket text.
