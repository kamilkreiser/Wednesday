# QA Gate 122 verdict: Secuura/Distributed_Secuura PR 1940 (KS-1939, originate routes/verification.ts, POST /api/verification/verify: O78-P1 `return await respondExistenceOnly(` :1355, O78-P2 lookup-catch guard :1437-1444), TIER 1

## BLUF
**GO WITH NOTES (TIER 1). Nothing has to be fixed before merge.** I ran the real `verificationRouter` (public `POST /api/verification/verify`) on a loopback listener with only the db replaced by a statement recorder (plus the heal, the lineage repo and the logger as counters). The same 190-cell probe ran at base e2a2426d and at head (scripts/probe.test.ts; logs/probe_{base,head}.jsonl, logs/probe_table.log, logs/probe_verdicts.log). The cells cover 5 body kinds (by id, by id missing, hash, title, title missing), 8 injection points, 5 thrown values plus a success control, and 2 callers (anonymous, and the owner with a vouched tenant and a bearer).
- **At the two PR sites, an unreadable value at head gets exactly what an ordinary Error gets:** 200 `{"verified":false,"error":"Verification lookup failed"}`, one warn line `Verification lookup failed {documentId, error: 'unreadable thrown value'}`, the same statements and no writes. Base answered 500 `INTERNAL_ERROR "Verification failed"` (lookup catch), or gave NO ANSWER (inside the by-id existence answer, where an ordinary Error or a string also got NO ANSWER at base).
- **No new disclosure.** Every head body is one base already produced for the same body kind (0 new bodies). No failure body carries a message, stack, id, tenant, holder or organisation (leak scan: none). An anonymous caller learns nothing new. It now gets the existing constant "lookup failed" answer where it got a 500 or no answer.
- **No new verdict.** Verdict transitions base -> head over 190 cells: 500 -> LOOKUP FAILED 69, NO ANSWER -> LOOKUP FAILED 28, and everything else is unchanged: VERIFIED 20, NOT FOUND 15, FOUND (existence) 24, FOUND (title) 1, LOOKUP FAILED 33. **0 cells newly give verified, not-found or found.** The PR touches no verdict-bearing line (2 hunks only; the verdict-site catch lines :886/:923/:1023/:1312 are byte-identical).
- One place where head's unreadable outcome is not the ordinary one: G122-F1. It is the untouched verdict-site lineage catch, as the author disclosed. It is now answered ("lookup failed") where base left the request with no answer. It is not a new verdict and not a block.
- The author's numbers re-measure: held patches byte-identical (3/3 blobs); red-first 6/11 by assertion; green 11/11; suite 2163 -> 2174 (0 vanished, 0 passed->not); tsc with tests 0 errors (208 -> 210 test files); eslint 0; the author's own recorder re-run in my clone gives 14 scenarios, judge 52/52, tampers 6/6 refused, and my recordings equal theirs. Mutants: **13/13 killed by assertion** (the author ran 2). merge-tree onto 0e3a9b65 is clean with exactly the 5 PR paths, and both merge orders with PR 2 (#1941) are clean and give an identical tree.

## Heads
- START (logs/head_start.log, 2026-11-02T10:21:00Z): PR head `96208f377d1496028f7c6a4eb45a78f91428ed05` (equal to the brief), develop `0e3a9b65cdd632fbc1783257c6cb9833934e1404` (equal), merge-base/parent `e2a2426d221d8bd672e97c43c6bbcd6c4027b350` (equal). 1 commit, Kam Kreiser <kamil.kreiser@secuura.ai>, "Refs KS-1939: verify by id awaits its existence answer and guards the lookup catch's read".
- END (logs/head_end.log, 2026-11-02T10:37:00Z): PR head `96208f37...` **UNCHANGED**, develop `0e3a9b65...` **UNCHANGED**, PR 1941 `33644960bc2270f6850d82dbbf4323780b942b9f`. Local HEAD 96208f37 with a clean working tree. Product sha256 `e4e69351f741...` equals the head blob. Every product swap was sha-restored (RESTORE_OK each time; mutants `restore True` 13/13).
- Diffstat (logs/diffstat.log), three-dot: **5 files, +446/-2**. That is verification.ts +8/-2, two new tests (+195, +199) and one fragment pair (+22/+22). Nothing is outside the declared paths.
- **PR body not read** (no Secuura gh login here). I used the author's READY mail (evidence/v16_ready_pr1940.txt), the commit message (logs/commit_msg.log), and the author's evidence folder, read-only.
- **Held patches** (logs/held_patch_compare.log, scripts/held_compare.sh): O78-P1 and O78-P2 `section_1/2.diff` applied strictly at e2a2426d in a scratch worktree (wt_apply/), each "cleanly", rc 0. The resulting blobs for verification.ts (`ea010923`) and both test files (`90822d11`, `0a7cbc87`) are **IDENTICAL** to the PR head's. Both `-control` run dirs' patch.diff are byte-identical to the run's. patch.diff sha256 values match the brief (b6924d51…, c7f4c07f…).

## FINDINGS
- **G122-F1 (RECOMMENDED note for the body; pre-existing class G106-F3, the disclosed verdict-site catches; measured).** Inside `respondExistenceOnly`, the by-id lineage attach catch (:1021-1024) still reads `lineageErr instanceof Error ? …` unguarded.
  - An ordinary Error or a string there gets the 200 by-id existence answer (`FOUND`), base = head.
  - An unreadable value there (revoked Proxy, throwing getter; also getterThrowsProxy from the walk catch :883-886) got NO ANSWER at base. At head it gets 200 "Verification lookup failed" (8 cells, `OTHER_DIFF+HEAD_UNREADABLE!=ORDINARY` in logs/probe_table.log).
  - So on that path, head's unreadable outcome is not the ordinary one. It is still not a verdict, it is answered, and it is the KS-1939 design-call site the author lists as NOT covered.
  - The same holds pre-existing at the hash path's :1310 catch (owner caller). An unreadable value replaces the verified answer with "lookup failed" at base and head alike (getterThrowsProxy: 500 at base, "lookup failed" at head).
  - The body should say that the PR sites now match an ordinary Error, and that through the untouched lineage catches an unreadable value yields "lookup failed" rather than the existence or verified answer. Any later guard there must keep the verdict byte-identical (G106-F3).
- **G122-F2 (INFO, measured).** If the response is written and THEN `res.json` throws (my `jsonaftersend` cells), head's `await` routes the throw to the lookup catch. That catch logs a spurious "Verification lookup failed" warn, its own `res.json` throws ERR_HTTP_HEADERS_SENT, the outer catch logs "Verification error", and the handler still rejects, with a READABLE ERR_HTTP_HEADERS_SENT. The client already got its 200, at both versions. Base rejected with the ORIGINAL value. When that value is unreadable, index.ts:75's `String(reason)` would throw and become an uncaughtException and a process exit (read, not run; G106-F4). Head is not worse.
- **G122-F3 (INFO; read, not run).** Persisted state beyond the route: on every path where base left a rejected handler (38 by-id cells: 12 ordinary or string, 26 unreadable), the value went to index.ts:75 `unhandledRejection`, which logs message AND stack and calls `trackError(...)` (an error-tracker write). At head those paths raise no rejection (0 head `unhandled`; the only escapes are the 10 `jsonaftersend` cells of G122-F2, each a readable ERR_HTTP_HEADERS_SENT), so they write no tracker row and log one warn line without a stack. The route itself issues **no write statement** at either version: 0 INSERT/UPDATE/DELETE/MERGE in any recorded statement, 0 `$executeRaw`, 0 `updateDocument`. The only write is the anchor heal (w=1) on the owner's hash cells, equal at base and head.
- **G122-F4 (INFO, Q4: `documentId`).** The warn line still logs `documentId` verbatim (same key, pre-existing). It is the caller's OWN request field (validated `isString`, length bounded only by the body parser), not a value read from a thrown object, so Kam's ks1346 rule (about thrown objects) does not strictly reach it. It is never returned to the caller. It is a log-side concern only: an anonymous caller can put arbitrary text in a warn line, rate-limited by the gateway's verify limiter (read in the code comment, not run). Head emits that line on more paths (every throw inside the by-id answer). Not a disclosure to the caller. It is worth a line in the KS-1868 or KS-1346 follow-up list: log a length or a hash of `documentId`, or the key name only.
- **G122-F5 (INFO, ks1346).** The changed line logs `reason`, which is the pre-existing expression `dbErr?.message` or the constant. There is no new key and no new log line (keys at head are subsets of {documentId, error}, as at base). For readable values it still logs the message TEXT, a value, pre-existing as in G106-F7.
  - At head that text now also carries throws from inside the by-id answer, and the readable error produced by the untouched :1021 catch. The probe saw `getter SECRETVAL` in a "lookup failed" line for by-id `lineageq/throwingGetter`. At base that text went to the unhandledRejection line WITH a stack.
  - At the PR sites, every unreadable cell logs only the constant. This is compliant on the gates 90/106 precedent (the same expression or the constant).
- **G122-F6 (INFO).** The 3 P1 red cells at base each carry two failure messages: the escaped rejection that jest attributes to the cell, then `expect(received).toEqual` (NO ANSWER vs 200). Red is by assertion (logs/red_by_assertion.log), as the author's red_report says.
- **G122-F7 (INFO).** docs-fragments `check` prints a cheat ADVISORY at line 6235 (rc 0). It is the same advisory text gate 90 found on develop alone. I did not re-run on develop 0e3a9b65 alone, so I do not attribute it to this PR; nothing in this PR's fragment sits at that line.
- No FIX-BEFORE-MERGE item.

## Q1. Public surface, base vs head (logs/probe_table.log, logs/probe_verdicts.log)
Method: jest (`--rootDir` = my clone's originate), the real router mounted at `/api/verification` behind `express.json()`, real `fetch` with a 1.5 s abort ("NO ANSWER"). A wrapper records what escapes a handler; the request still goes unanswered, as in production. "owner" sets `req.tenantId` (the gateway-vouched tenant) and a bearer.
- **Run:** everything in routes/verification.ts, including validation, the strategy selection, `respondExistenceOnly`, `buildResponse`, `scopeTenantFields`, the catches and the response writes.
- **Replaced:** `prisma.$queryRaw/$executeRaw` (canned rows; every statement logged and scanned for write verbs), `healAnchorForVerify` (it counts a write only with a bearer, as the real one does), `walkAncestors/walkDescendants/updateDocument`, and the logger. `getTenantManager` is null, so there is no cross-tenant lookup.
- **Read only:** index.ts:75 handler, `trackError`, gateway limiter.
- Injection points:
  - `dbpre`: the main lookup query rejects.
  - `dbgetter`: it rejects with an Error whose `message` getter throws the value.
  - `rowgetter`: the found row's `status` getter throws.
  - `json`: the first `res.json` throws.
  - `jsonaftersend`: it sends, then throws.
  - `lineageq`: the by-id/hash tenant lookup inside the lineage try rejects.
  - `walk`: `walkAncestors` rejects.
  - `healapplied`: the heal counts its write, then rejects.
- Values: an ordinary Error (planted `SECRETVAL tenant-owner-x HolderBob`), a string, a revoked Proxy, a throwing getter, and a getter that throws a revoked Proxy.

| body (injection) | ordinary Error / string, base -> head | unreadable, base | unreadable, head |
|---|---|---|---|
| by id (dbpre) — PR site P2 | 200 lookup failed, warn {documentId, error: msg} / same | 500 INTERNAL_ERROR "Verification failed", no warn | 200 lookup failed, warn constant |
| by id, hash, title (dbgetter) — P2 | (all dbgetter values are unreadable) | 500 | 200 lookup failed, warn constant |
| by id (rowgetter, json) — PR site P1 | **NO ANSWER, escaped -> 200 lookup failed**, warn msg | NO ANSWER (escaped UNREADABLE) | 200 lookup failed, warn constant |
| by id (jsonaftersend) | 200 sent; escaped value -> 200 sent; escaped ERR_HTTP_HEADERS_SENT | 200 sent, escaped UNREADABLE | 200 sent, escaped readable (G122-F2) |
| by id (lineageq, walk) — untouched :1021/:886 | 200 FOUND existence answer / same | NO ANSWER (revokedProxy/throwingGetter at lineageq; getterThrowsProxy at walk); other walk values FOUND | **200 lookup failed** (G122-F1); others FOUND |
| hash, title, by-id missing, title missing (dbpre, json) | 200 lookup failed / same | 500 | 200 lookup failed |
| hash (healapplied) | 200 lookup failed, heal w=1 owner / same | 500 | 200 lookup failed, same w |
| hash owner (json, lineageq) — untouched :1310 | 200 VERIFIED (lineage dropped) / same | 200 lookup failed (getterThrowsProxy 500) | 200 lookup failed (pre-existing, G122-F1) |

Success controls (`none`): base == head byte-for-byte with verifiedAt normalised, 10/10 (by id FOUND, missing NOT FOUND, hash VERIFIED, title FOUND for the owner and NOT FOUND for anonymous, as by KS-1114's one-tenant rule). Head unhandled rejections: 0. Writes: G122-F3.

## Q2. The hunks and the verdict sites (logs/product_diff.log, logs/verdict_sites.log)
- Hunk 1 (:1355): `return respondExistenceOnly(` -> `return await respondExistenceOnly(`. Only the await is added: the arguments, the warning text and the existence answer's body are unchanged (control C2 and probe `none` are byte-identical).
- Hunk 2 (:1438): `logger.warn('Verification lookup failed', { documentId, error: dbErr?.message })` -> `let reason: string | undefined; try { reason = dbErr?.message; } catch { reason = 'unreadable thrown value'; }` + the same warn with `error: reason`. **Unchanged:** the message, level, keys, and the `return res.json({ verified: false, error: 'Verification lookup failed' })` answer.
- `diff -U0` gives exactly 2 hunks, and 0 lines differ outside them. Verdict-site reads :886/:923/:1023/:1312 are byte-identical. Counts of every verdict-bearing literal are equal base/head (`verified: true` 2/2, `verified: hashMatch` 1/1, `documentExists: false` 4/4, "not found in the registry" 2/2, "hash is not registered" 1/1, `integrityVerified:` 10/10; positive control `respondExistenceOnly` 2/2).
- **Can a head path turn a failed lookup into "verified" or "not found"?** No. Both hunks only reach the lookup catch, whose single answer is `{verified:false, error:'Verification lookup failed'}`. That is distinct from not-found (`documentExists:false`, "Document not found in the registry") and carries no `checks`. Measured: 0 of 190 cells newly give VERIFIED, NOT FOUND or FOUND. `respondExistenceOnly` is called only from strategy 2 (git grep: 2 occurrences, the definition and :1355). The title strategy deliberately does not use it.

## Q3. The author's recorder (logs/authrec.log; evidence/author_recorder/)
I copied the author's `rec_pr1_v16.test.ts` and `judge_pr1_v16.py` unmodified into evidence/ and ran the recorder in MY clone at base and head. Result: **14 scenarios** each, judge rc 0 **52/52**; on the author's own saved recordings also 52/52. Tampers 1-6 on my recordings: all rc 1 (51/52, 51/52, 51/52, 50/52, 51/52, 50/52). My recordings equal the author's (verifiedAt normalised) at both base and head. **"No write statement"**: their J5 checks `$executeRaw` only. My probe extends that to a write-verb scan of every `$queryRaw` statement, `updateDocument`, and the heal-write counter, over 190 cells: 0 writes except the equal heal w=1 (G122-F3).

## Q4. ks1346 and documentId
G122-F5 (the new line: compliant on precedent, constant at the PR sites) and G122-F4 (documentId: INFO, a log-side concern, not a disclosure to the caller).

## Q5. Overlap with PR 2 (logs/merge_orders.log)
PR 2 is **#1941**, head `33644960bc22` (ls-remote at start and end), parent e2a2426d, 1 commit, "Refs KS-1868: verification catches coerce a hostile message; v2 chain-fact read is guarded". Its verification.ts hunks are at :761, :1452, :1487 and :1515, none overlapping :1355 or :1437-1444.
- #1941 alone onto develop: clean.
- Order 1940 -> 1941: both steps rc 0, tree `23fee71f`.
- Order 1941 -> 1940: both steps rc 0, **same tree `23fee71f`**, with verification.ts blob `fc235c1f` and verificationV2.ts `c45550c5` in both.
- The union keeps `return await respondExistenceOnly(` (1) and the guarded lookup catch verbatim.

## Q6. Re-measure (Node v26.8.1; NOT measured on Node 24; logs/runs_summary.log, logs/static_outer.log)
- **Red-first** (base product + new tests): 11 run, **6 failed / 5 passed**. All 6 fail by `expect(` (the P2 reds by the assertion alone, the P1 reds as in G122-F6). Controls are green.
- **Green:** 11/11.
- **Whole originate suite:** base without the new files **180 files 2163/2163**; head **182 files 2174/2174**. Cell by cell: 11 new (exactly the two new files), 0 vanished, 0 passed->not passed.
- **tsc:** plain `tsconfig.json --noEmit` rc 0. With the tests (scripts/tsconfig.tests.json): base rc 0, 208 test files; head rc 0, 210 test files. Planted TS2322 gives rc 2 and is reported.
- **eslint** (flat config `Blockchain/Dev/eslint.config.mjs`, v10.7.0): verification.ts + 2 new tests, **0 problems, rc 0**. A planted file gives 1 error and 1 warning, rc 1.
- **docs-fragments:** rc 0, "flow 117 legacy + 84 new, cheat 112 legacy + 84 new; lint clean, render passes". A planted `<div>` in the PR's flow fragment and in its cheat fragment each give rc 1, "tags are not balanced". Both were restored by sha (FRAG_RESTORED_flow/cheat). ADVISORY: G122-F7.
- **Mutants** (scripts/mutants.py; product only, tests untouched, restore True 13/13; logs/mutants_table.log): **13/13 KILLED, every kill by assertion**.
  - P1: A0 drop the await (3 cells); A1 swallow with `.catch` that answers lookup-failed without the log (3); A2 `return void` (3).
  - P2:
    - M0 unguard/revert (3)
    - M1 drop the inner try (3)
    - M2 catch -> `String(dbErr)` (3)
    - M3 catch rethrows (3)
    - M4 constant for every value, i.e. swallow the readable (6)
    - M5 readable branch `String()`-wrapped (2)
    - M6 constant text changed (3)
    - M7 log removed (9)
    - M8 log ignores reason (7)
    - M9 unreadable -> 500 answer (3)
  - My first M8 (`error: undefined`) died by a TS6133 compile error, not an assertion. I replaced it with `reason && undefined`, which dies by assertion (run 1 kept in logs/mutants_table_run1.log).
- **merge-tree onto develop 0e3a9b65** (logs/merge_tree.log): **rc 0, tree `27b94184`, result paths == the PR's 5 (SAME_PATHS)**. Develop changed 46 paths since e2a2426d (8 commits), **0 shared** with the PR (control 46). verification.ts is UNCHANGED on develop since the base.

## Notes for the PR body
1. G122-F1 (recommended): state that through the untouched lineage catches inside the by-id answer (:1021, and :886 via the walk), an unreadable value now gets 200 "lookup failed" (base: no answer) while an ordinary Error gets the existence answer. Name it as part of the G106-F3 design call.
2. Tier-1 statement confirmed by gate 122 on the real router: at the two PR sites, unreadable = ordinary Error (200 lookup failed, constant warn, no writes). There is no new body, no new field and no new verdict for anonymous or owner callers. 500 -> lookup failed in 69 cells, no answer -> lookup failed in 28.
3. G122-F2 / F3 (info): the response-after-send edge; at head, fewer rejections reach index.ts:75 and `trackError`.
4. G122-F4 (info): `documentId` stays verbatim in the warn line, now on more paths. Follow-up candidate: log its length or a hash.
5. Both merge orders with #1941 are clean with an identical tree (`23fee71f`).

## NOT TESTED
- The real PR body (no gh auth). Real PostgreSQL or Prisma. The real heal. Multi-tenant mode (`getTenantManager` null: `crossTenantLookup` and its :557 catch were not run). A real boot (index.ts:75 and `trackError` read, not run). The gateway hop and its rate limiter. verificationV2.ts (not touched). Node 24. The four platform suites. CI. The pre-push hook legs (quoted by the author only). The Linear ticket text. Whether an unreadable thrown value occurs at these sites in reality: the values are synthetic.
- Background processes: none left. Every run was foreground (`ps` at end: 0 processes mentioning this workdir; logs/ps_end.log). The scratch worktree `wt_apply/` (held-patch compare) remains in the workdir, uncommitted. Scratch merge commits (`commit-tree`) exist only in my clone's object store.
