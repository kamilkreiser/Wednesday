# Spark operator 69, 2026-11-02: KS-1868 originate routes/certifications.ts route catches (3 held, 0 failed, 0 rebriefs)

## BLUF
HELD: O69-P1 (GET / list, GET /:id/lineage, GET /:id/evidence-bundle), O69-P2 (POST /:id/revoke, /:id/verify, /:id/share), O69-P3 (POST /:id/recertify). All 7 unguarded ROUTE catches in the file, each fixed with the file's own merged inline `let reason` guard (GET /:id, :1086-1094). All three controls CONTROL-PASS first time, all three model rounds PASS 7/7 on the ORIGINAL brief, golden BYTE-IDENTICAL, strict=True. SKIPPED: the whole issue route (POST /, :192-890 incl. outer catch :878 and inner catches) and the anchoring inner catch :1421, with reasons below. Not a route catch, noted only: module-load `initRepo().catch` at :70.
Tip: start (brief read) cde2dee4dffba6a61228c40d641ff567660c32b2 (spark cache); ls-remote start 09:50 c8d77dce07dca... (tip_start.out); the rounds ran at c8d77dce07dc / b887480394cc (done.md rows), end ls-remote b887480394cc67764922b0aa123027c344241ed7 (tip_end.out). Golden BYTE-IDENTICAL on every round and A-drift check on certifications.ts passed (B_ALLOW_DRIFT=0), so the file did not change across those tips.
Open-PR scan: start 22 PRs/125 files, end 22 PRs/127 files; no PR lists certifications.ts or any originate src file other than integration tests 1790/1792/1794 and package.json 575/949/1726; planted control services/auth/ present (7 entries at start, see prscan_*.out).

## Existing guard / gate answers
- Guard already merged in this file: GET /:id catch (:1065-1094, KS-1844) uses the same inline `let reason ... catch { reason = 'unreadable thrown value' }`; copied exactly. No helper exists in originate for it; none added.
- Already guarded (not briefed): GET /:id (:1065). Unguarded route catches re-derived by grep of `instanceof`/`.message` at the tip: :1010 list, :1169 revoke, :1235 verify, :1334 share, :1495 recertify, :1583 lineage, :1691 evidence bundle. All seven briefed.
- Test shape copied from `ks1844-get-certification-by-id-answers-a-hostile-throw.test.ts` (mocks certificationRepo/db/chargeEvents/notificationClient/events/documentRepo/auth/logger, NO `@secuura/shared` mock, so ks1061-shared-mock-completeness is not engaged).

## Held (ls night | grep O69; held_files.txt)
READY_KS-1868-KS-1868-O69-P1_spark-dsv4flash_BRIEFED-CODEPATCH2-O69-P1-PASS-7of7_2026-11-02.diff.md
READY_KS-1868-KS-1868-O69-P2_spark-dsv4flash_BRIEFED-CODEPATCH2-O69-P2-PASS-7of7_2026-11-02.diff.md
READY_KS-1868-KS-1868-O69-P3_spark-dsv4flash_BRIEFED-CODEPATCH2-O69-P3-PASS-7of7_2026-11-02.diff.md

All three share one product file: hunks are far apart (P1 :1010/:1583/:1691, P2 :1169/:1235/:1334, P3 :1495; P1 and P2/P3 hunks are >100 lines apart), so they combine into one PR in any order (the guard adds 6 lines per hunk, line numbers shift but contexts are distinct); the seven edits can also be split per pass.

## O69-P1: list, lineage, evidence-bundle (read routes)
- hold_ready: `golden: BYTE-IDENTICAL; touched=2 product_plus=21 product_minus=3 red=6/12 green=12/12 suite=1999->2011 strict=True`. Model 78.77 s (round 206 s). Test: src/__tests__/ks1868-certifications-read-route-catches-p1-unreadable-throw.test.ts.
- Callers: certificationsRouter mounted at /api/certifications, reached through the api-gateway.
- Today vs after: unreadable value from listCertifications / getCertification: today the handler rejects, nothing logged, NO answer (gateway timeout); after: logs `unreadable thrown value` under the same context and answers the same constant 500 an ordinary Error gets (control C1). Ordinary Error and string: unchanged (C1, C2). Persisted: unchanged. Evidence bundle writes an `evidence_export` charge event BEFORE the bundle is assembled; the catch does not touch it, so charge persistence is identical for every thrown value.
- BEHAVIOUR CHANGE for the PR: only the unreadable-value case, hang -> logged constant 500, as above.
- Recommended tier: 1 (evidence-bundle is an evidence route; per brief instruction), though the catch is log + constant 500 only.

## O69-P2: revoke, verify, share
- hold_ready: `golden: BYTE-IDENTICAL; touched=2 product_plus=21 product_minus=3 red=6/12 green=12/12 suite=1999->2011 strict=True`. Model 80.703 s (round 215 s). Test: src/__tests__/ks1868-certifications-revoke-verify-share-route-catches-p2-unreadable-throw.test.ts (getCertification rejects before the route writes anything).
- Strict check: each catch is `logger.error` + constant 500; nothing in the catch decides a verdict, revokes, charges, shares or anchors. The revocation write, the verification verdict/charge and the share rows happen in the try, before the catch, identically for any thrown value.
- Today vs after: as P1 (hang -> constant 500 for an unreadable value only). Persisted state: unchanged by the patch.
- BEHAVIOUR CHANGE for the PR: only the unreadable-value case.
- Recommended tier: 1 (revoke and verify routes).

## O69-P3: recertify
- hold_ready: `golden: BYTE-IDENTICAL; touched=2 product_plus=7 product_minus=1 red=2/4 green=4/4 suite=1999->2003 strict=True`. Model 72.004 s (round 208 s). Test: src/__tests__/ks1868-certifications-recertify-route-catch-p3-unreadable-throw.test.ts.
- Strict check: POST /:id/recertify issues a verification certificate and calls anchoring, but its OUTER catch (:1494) is log + constant 500 only; anchoring status, save and charge are decided in the try. The inner anchoring catch (:1421, `err?.message`) is NOT touched.
- Today vs after: hang -> constant 500 for an unreadable value only; an ordinary Error unchanged. Persisted: unchanged by the patch (the save/anchor happened or not before the catch, as for an ordinary Error).
- Recommended tier: 1 (issuance route). Independent of P1/P2; can be dropped without affecting them.

## SKIPPED (certification territory)
- POST / issue route, outer catch :878: decides outcomes before any log can matter: reads `msg` and maps FK violations to 400 (with `detail: msg` in the body) and transient codes (P2024, 53300, ...) to retryable 503. A fix would newly produce a status/body for an unreadable value that an ordinary Error produces through a different path. Client-visible body and status change: SKIP, needs a human call.
- Issue route inner catches :375/379 (users/stub), :406 (errMsg), :436 (OnBehalfOfError), :502, :581-585 (reservation), :631-632 (anchoring unreachable: sets anchoring status / 503), :655-659 (delete of reserved row on failure: persisted state), :747-751 (save), :783-787 (update), :816-820 (charge), :838 (notification): each sits in the issue/anchor flow and decides a persisted state, an anchoring outcome or a client status. SKIP (strict rule).
- Recertify inner anchoring catch :1421 (`err?.message`): anchoring decision; SKIP.
- :687 `provErr.message`, :839 `err?.message`: `.catch` callbacks on provenance/notification promises; not route catches; not briefed.
- :70 `initRepo().catch((err) => logger.error(... err instanceof Error ...))`: module-load, not a route catch, not in the assignment. Same class: on an unreadable rejection the .catch callback itself rejects (unhandled rejection at import). Can be a one-hunk follow-up if Wednesday wants it; same guard.

## Raise-seat notes
strict=True all three. Hunks: see above, all > 3 lines apart. Test names start `RED ks1868 R1/R2` and `control ks1868 C1/C2`; describe titles `KS-1868 <route> catch reads the thrown value safely`. Refs KS-1868 only. TRAP (from op 63): do not run jest in the spark cache clone (stale @secuura/shared build); the harness clone counts. Operator 65's nine repository log-and-rethrow sites (names :1000 list, :1584 lineage, :1692 evidence) are now unblocked once P1 merges: those three route catches will answer instead of hanging when a guarded repository rethrows.

## Round log (spark/done.md rows; done_rows.txt)
- P1 control queued 09:52:27, CONTROL-PASS 10:00:37 (132 s). P1 model queued 10:0x (queued_model_p1.txt), PASS 10:04:45 (206 s, 78.77 s model).
- P2/P3 controls queued together after P1's CONTROL-PASS (queued_controls_p2p3.txt): P2 CONTROL-PASS 10:06:58 (132 s), P3 CONTROL-PASS 10:09:30 (151 s). P2 model PASS 10:13:06 (215 s, 80.703 s). P3 model PASS 10:16:35 (208 s, 72.004 s).
- Lint rc 0 x3; dry runs rc 3 BUSY (another round held the lock; controls queued per commission). Counter: 1 original brief each, 0 rebriefs.

## UNMEASURED
Whole-suite CI with the patches beyond the harness (suite 1999 -> 2011/2011/2003, tsc and eslint only as the checker ran them); real Postgres/repository behaviour; whether an unreadable value is reachable in production; the issue route and its inner catches' patched behaviour (read only); the rest of originate beyond this file. My own recount of services/auth in the end PR scan was non-zero (see prscan_end.out); the end scan shows ANALYTICS-HIT 1914 (an analytics PR, unrelated). Evidence: this folder (tip_*, prscan_*, open_prs_*.json, lint_*, dry_*, hold_p*.out via hold in gen/, held_files.txt, done_rows.txt, gen/mk69.py t69_p1..3.ts.txt hold69.sh prscan69.py).
