# Spark operator 78, 2026-11-02: KS-1939 originate verification.ts (G106-F2 await, G106-F1 lookup-catch guard) + one extra KS-1868 site (verificationV2.ts chain-fact catch), TIER 1 (3 held, 0 failed, 0 skipped of the assigned two)

## BLUF
- HELD 3 passes, all PASS 7/7 on the ORIGINAL brief (0 rebriefs), golden BYTE-IDENTICAL, strict=True, every control CONTROL-PASS first time. All TIER 1 (public, no-login verification surface): Claude raise seat + Opus gate.
- O78-P1 (KS-1939, G106-F2) verification.ts :1355 `return respondExistenceOnly(` -> `return await respondExistenceOnly(`. One line. Taken: an ORDINARY Error thrown inside respondExistenceOnly gets today NO ANSWER; after it gets exactly what an ordinary Error from the lookup query already gets (200 `{verified:false,error:'Verification lookup failed'}` + one warn line). Nothing new disclosed.
- O78-P2 (KS-1939, G106-F1) verification.ts :1438 lookup catch: `error: dbErr?.message` read inside its own try, constant `unreadable thrown value` on throw (the guard form #1925 merged in the same file). Taken. `documentId` key and the verbatim readable message are deliberately NOT changed (see below).
- O78-P3 (KS-1868 umbrella, the "one more pass") verificationV2.ts :111 `fetchChainFact` catch, same guard. Taken, flagged VERDICT-ADJACENT (see P3).
- SKIPPED / not briefed: the four verdict-site lineage catches (G106-F3), v2 :322 and :326, v1 :557 (reasons below).
- Tip: develop cd9c4a7dd3b8 at start (tip_start.out). At end 8f313815f415 (tip_end.out): MOVED. Drift check done through the spark cache after a dry run fetched it: `git diff` cd9c4a7..8f31381 on verification.ts and verificationV2.ts is EMPTY (drift_end.out, 0 bytes); the 6 files that moved are PR 1924's (certifications.ts, its 3 tests, 2 doc fragments; drift_all.out). All three briefs re-dry-ran OK at 8f31381 (dry_end_p1..p3.out).
- Open-PR scan start 20 PRs / 114 files, end 19 PRs / 108 files (1924 left the list = merged). Planted control (services/auth/ entries; the script label says "originate") = 7 at both ends. Start scan: originate entries were 1924 (certifications.ts + 3 tests), 1794/1792/1790 (one integration test each), package.json in 1726/949/575; NO PR lists verification.ts, verificationV2.ts or either new test name (a "verification" substring search over open_prs_start.json = 0 hits; end scan re-checked by exact filename: none).

## Held (ls night | grep O78, pasted from ls_held.out)
READY_KS-1868-KS-1868-O78-P3_spark-dsv4flash_BRIEFED-CODEPATCH2-ORIGINATE-VERIFICATION-V2-CHAIN-FACT-CATCH-PASS-7of7-PASS-7of7_2026-11-02.diff.md
READY_KS-1939-KS-1939-O78-P1_spark-dsv4flash_BRIEFED-CODEPATCH2-BRIEFED-CODEPATCH2-ORIGINATE-VERIFICATION-BYID-AWAIT-PASS-7of7_2026-11-02-PASS-7of7_2026-11-02.diff.md
READY_KS-1939-KS-1939-O78-P2_spark-dsv4flash_BRIEFED-CODEPATCH2-ORIGINATE-VERIFICATION-LOOKUP-CATCH-PASS-7of7-PASS-7of7_2026-11-02.diff.md
(Label text is doubled by my hold script's label argument; cosmetic only, content unaffected.)

## Per pass
### O78-P1 KS-1939 (Refs KS-1939): `return await respondExistenceOnly(`
- hold_ready: `golden: BYTE-IDENTICAL; touched=2 product_plus=1 product_minus=1 red=3/5 green=5/5 suite=2108->2113 strict=True` (jest, originate).
- Site read at the tip: verification.ts :1355 is inside the inner try that opens :1061 and whose catch is :1437; respondExistenceOnly is `async` (:987). The same file already uses `return await` inside a try (:882).
- Today vs after, ordinary Error thrown inside respondExistenceOnly (cells R1 first res.json throws, R3 a getter on the found row's status throws; R2 a thrown string): TODAY the returned promise leaves the try, handler rejects, NO ANSWER (client times out 1.5 s), nothing logged by the handler. AFTER 200 `{verified:false,error:'Verification lookup failed'}` + `logger.warn('Verification lookup failed',{documentId,error:<msg>})`. That is exactly what an ordinary Error from the by-id lookup query already gets (control C1, green at the tip). So no new outcome kind.
- Persisted state: none either way. respondExistenceOnly only reads (tenant SELECT, lineage walks each in their own try); this strategy has no heal or audit write. Cells assert `$executeRaw` never called.
- Disclosure: the new answer is the constant body already used by every other throw in that try; an anonymous caller gets an answer where it got none. Verdict lines byte-identical: only one line changes; success path returns the same value (control C2 pins the existence-only answer: verified:false, hashValid:false, integrityVerified:false, no `error`, warn/error never called). A throw after the response was committed would make the catch's own res.json throw and fall to the outer catch, same as any other position in that try: nothing new.
- BEHAVIOUR CHANGE (for the PR): a throw inside the by-id existence answer now produces the lookup catch's ordinary answer (200 'Verification lookup failed' + one warn line) instead of leaving the request unanswered. A value whose `message` cannot be read is NOT covered by P1 (it reaches the outer catch's constant 500 as at every other position in this try until P2 lands).
- Callers: HTTP only, `/api/verification/verify` (public; gateway rate limit). Tier 1.

### O78-P2 KS-1939 (Refs KS-1939): lookup-catch guard
- hold_ready: `golden: BYTE-IDENTICAL; touched=2 product_plus=7 product_minus=1 red=3/6 green=6/6 suite=2108->2114 strict=True`.
- Fix: `let reason: string | undefined; try { reason = dbErr?.message; } catch { reason = 'unreadable thrown value'; }` then `logger.warn('Verification lookup failed', { documentId, error: reason })`. The expression is kept EXACTLY (not the `instanceof Error ? ... : String()` form), so every readable value logs byte-identically, including `error: undefined` for a thrown string (control C2).
- Today vs after, unreadable value (revoked Proxy R1, throwing message getter R2, getter throwing a revoked Proxy R3), injected as the first by-id query rejecting: TODAY dbErr?.message throws in the catch; the outer catch answers 500 `{success:false,error:{code:'INTERNAL_ERROR',message:'Verification failed'}}` (G106-F1). AFTER 200 `{verified:false,error:'Verification lookup failed'}` and one warn line with the constant. An ordinary Error already gets the after-state (control C1). Persisted state none either way ($executeRaw never called).
- Disclosure: response body constant; no thrown text reaches the response; the unreadable cells log only the constant. Verdict lines untouched (hunk -1/+7 at the catch only; control C3 pins the success answer).
- ks1346: key set unchanged. NOT done in this pass, a deliberate scope choice for Wednesday/Kam: the line still logs the caller-supplied `documentId` and the readable message verbatim (G106-F1 second half, G106-F7). The house guard only guards the read; dropping `documentId` would change operator-visible log content and needs its own decision (same shape at :557 `Cross-tenant lookup failed`). If Kam wants it, it is a one-key edit in a follow-up pass.
- BEHAVIOUR CHANGE (for the PR): for an unreadable thrown value only, a failure inside the lookup block of POST /verify is answered 200 'Verification lookup failed' (as for an ordinary Error) instead of 500 'Verification failed'. Readable values log byte-identically. Tier 1.

### O78-P3 KS-1868 (Refs KS-1868): v2 `fetchChainFact` catch (extra pass, screen)
- hold_ready: `golden: BYTE-IDENTICAL; touched=2 product_plus=7 product_minus=1 red=3/6 green=6/6 suite=2108->2114 strict=True`.
- Site: verificationV2.ts :111 `logger.warn('v2 verify: chain-fact read failed; matches present stored state', { error: err?.message }); return null;`. Single caller matchesForHash :350 (only when the registry returns no rows), used by POST /verify (:409) and /verify-file (:474).
- Today vs after, unreadable value: TODAY fetchChainFact rejects, route catch answers the constant 500 ('Verification failed' / 'File verification failed') + error log. AFTER null -> `200 {hash,count:0,matches:[],verifiedAt}` + warn with the constant. An ordinary Error (network failure, timeout) already gets that (control C1); C3 pins the non-2xx warn line. Persisted state none (no row found, nothing healed; $executeRaw never called).
- **VERDICT-ADJACENT for the gate:** `count:0` is the route's honest "not registered" answer; an unreadable failure of the chain read now yields it exactly like every ordinary failure of that read already does (the route cannot distinguish them). Disclosure: body carries only the caller's hash, 0 and []. Opus gate should say whether it accepts 500 -> 200 count:0 for that value class.
- BEHAVIOUR CHANGE (for the PR): for an unreadable thrown value only, a failed chain-fact read is answered like an ordinary failure (200 count 0) instead of a 500. Tier 1.

## Skipped / not briefed (with reason)
- G106-F3, the four verdict-site lineage catches in verification.ts (~:886/:923/:1023/:1312): best-effort catches whose unreadable read today replaces a verified answer with 200 'lookup failed' or 500; guarding changes a verdict-bearing outcome on the public surface. SKIP (needs a design call and must hold the verdict byte-identical).
- verificationV2.ts :322 (cross-tenant rowset catch) and :326 (registry enumeration catch): the multi-tenant path needs a tenant manager and pool stand-ins that no merged suite drives; after-state would drop a tenant's matches from a public match list. Not briefed; the multi-tenant path was never measured by gate 106 either.
- verification.ts :557 (`Cross-tenant lookup failed`, `err?.message` + documentId): same family as :322 (returns null; flows to a not-found answer); read, not briefed, left for a follow-up with the documentId decision.
- Zod pre-check sites: none involved. index.ts :75-81 unhandledRejection handler: still left (operator 77 reason).

## Raise-seat notes
- All strict (plain git apply). Hunk positions: P1 @@ -1354,5 +1354,5 @@; P2 @@ -1435,6 +1435,12 @@ (same file as P1, 81 lines apart, > 3, applies independently in either order); P3 @@ -108,7 +108,13 @@ (verificationV2.ts, other file). The three applied together were NOT run.
- New tests: ks1939-verification-by-id-existence-answer-throw-is-answered.test.ts (195 lines), ks1939-verification-lookup-catch-unreadable-throw.test.ts (199), ks1868-verification-v2-chain-fact-catch-o78p3-unreadable-throw.test.ts (166). Names `control ks1939 C1..`, `RED ks1939 R1..` (P3: `control ks1868 C1..`, `RED ks1868 R1..`). Shape copied from the merged PR 1925 suites.
- Ticket keys: P1/P2 Refs KS-1939 (not the KS-1868 umbrella); P3 Refs KS-1868. P1 alone does not make an unreadable value 200; P2 alone does not fix the unanswered ordinary Error; the two together give the full G106-F1/F2 fix. G106-F2's own text ("then answers 200 lookup failed, given G106-F1") assumes both.
- Gate 106 probe positions to re-run on these: v1 POST /verify documentId | json (F2 cell) and the dbpre/healapplied/json positions for F1.

## Round log (spark/done.md row times, AEDT 2026-11-02)
- P1: control queued 15:49:44 (queue empty, Spark idle); CONTROL-PASS 15:53:38 (191 s, first control, harness proven); model PASS 7/7 15:58:54 (293 s, 82.0 s model, 33781+2629 tok).
- P2: control CONTROL-PASS 16:01:41 (166 s); model PASS 7/7 16:08:22 (205 s, 78.0 s model).
- P3: control CONTROL-PASS 16:04:55 (192 s); model PASS 7/7 16:11:30 (187 s, 59.5 s model).
- Queue discipline: one control (P1) until its CONTROL-PASS; then P1 model + P2/P3 controls together (P2/P3 dry runs had returned rc 3 BUSY behind my own control, so controls were queued per the BUSY rule); P2/P3 model lines only after their own CONTROL-PASS. Polling by grep -c on done.md (positive control: o77 rows counted 2). No recursive grep of spark/ or night/. Warm-up: a dry run of operator 77's P1 brief fetched the new tip into the spark cache (the read-only clone refuses fetch under the hook; cd9c4a7 was already in it).
- Spark was idle when I started (queue.md had no runnable lines at 15:49); after P1's control it ran back to back until 16:11:30.

## UNMEASURED
Whole-suite CI; eslint; tsc outside the checker; real Postgres/Prisma; the real heal; multi-tenant mode (tenant manager non-null); the gateway hop and rate limiter; a real boot; whether an unreadable thrown value occurs in production; P1+P2+P3 applied together; Node 24; the Linear text of KS-1939 (read from the assignment and gate 106 only); the PR bodies. The golden tests were written blind and proved only by the control runs (all first-time PASS).
Evidence: this folder (tip_*.out, tip_verification.ts, tip_verificationV2.ts, open_prs_*.json, prscan_*, lint_p*, dry_p*, dry_end_p*, drift_*.out, hold_p*.log/.out, ls_held.out, mk*.out, gen/mk78.py sites78.py t78_*.ts.txt hold78.sh).
