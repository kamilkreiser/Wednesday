# Spark operator 82, 2026-11-02: KS-1868 coercing-String follow-ups G113-F1/F2 (auth, PR 1931) and G114-F1/F2 (anchors, PR 1932) -- 6 HELD, 0 model FAILs on a real cause, 0 rebriefs

## BLUF
- HELD 6 passes (P1-P6), each model PASS 7/7 on the ORIGINAL brief, golden BYTE-IDENTICAL, strict=True. No rebriefs. Every held pass has a CONTROL-PASS row before its model line was queued.
- Environmental retries (not model faults, not rebriefs): 5 CONTROL-FAILs and 2 model FAILs, all A6 whole-suite "NEW red" from timeouts under machine load (load avg 8-15): services/auth ks949 tree-walk cells (5000 ms), ks728/ks847 at P4 model round 1; originate ks695/ks730c at P6 control 1. Each time the same brief/line was simply re-queued and passed. A4 red-first and A5 green-after passed in every one of those rows. Details in "Round log".
- Fix forms (decided per site, see table): `const m = <read>; reason = m === undefined || m === null ? m : String(m);` where the site reads a bare `.message` (auth.ts x2, internal.ts, oauth.ts x2, anchoring x3); `reason = String(err instanceof Error ? err.message : err)` where the site already stringifies a non-Error (issuerCerts x2, originate anchors x3).
- Tip: develop `66a36e3f777d082c98c015348d5239ce227c9f83` at start (tip_start.out). NOTE Wednesday's brief text had `...083c...`; the real sha is `...082c...` (the typo'd one answers "not our ref"). Fetched into the read-only clone (fetch_tip.out, rc 0, `cat-file -t` commit). Moved during the run: 91ccb155 (dry/control rows), 0e3a9b65cdd6 at end (tip_end.out, tip_end2.out). Drift 66a36e3f..0e3a9b65 on services/auth/src/routes, anchoring/src/index.ts, originate/src/routes/anchors.ts: EMPTY (drift_end.out, 0 bytes). 66a36e3f vs bc8558db stat: only PR 1932's 6 files (drift_bc85_tip.out).
- Open-PR scans (planted control services/originate): start 22 PRs / 124 files, control 8 (prscan_start.out); end 22 / 152, control 10 (prscan_end.out). No PR lists services/auth routes auth.ts, internal.ts, issuerCerts.ts, oauth.ts, anchoring src/index.ts, originate routes/anchors.ts, or any of my six new test names (only package.json entries in 575/649; users.ts in 1796/1798 which I do not touch). Live-seat territory avoided: governance, gdprService.ts (PR 1935), operator 81's security index.ts/db.ts and api-gateway admin.ts, operator 80's nft-certificate and admin.ts files: no overlap.
- Coordinator message (Seat S 13th, anchoring index.ts ~:267 `express.json({ verify: captureRawBody })` and its import at :63): my P5 hunks are at -694, -1310, -1819 (>420 lines away). Safe.

## Held (ls night | grep O82, ls_held.out; all under /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/)
READY_KS-1868-KS-1868-O82-P1_spark-dsv4flash_BRIEFED-CODEPATCH2-BRIEFED-CODEPATCH2-AUTH-LOGIN-REHASH-LOGOUT-DENYLIST-MESSAGE-COERCE-PASS-7of7-PASS-7of7_2026-11-02.diff.md
READY_KS-1868-KS-1868-O82-P2_spark-dsv4flash_BRIEFED-CODEPATCH2-BRIEFED-CODEPATCH2-AUTH-CONNECTOR-TOKEN-MESSAGE-COERCE-PASS-7of7-PASS-7of7_2026-11-02.diff.md
READY_KS-1868-KS-1868-O82-P3_spark-dsv4flash_BRIEFED-CODEPATCH2-BRIEFED-CODEPATCH2-AUTH-ISSUER-CERTS-MESSAGE-COERCE-PASS-7of7-PASS-7of7_2026-11-02.diff.md
READY_KS-1868-KS-1868-O82-P4_spark-dsv4flash_BRIEFED-CODEPATCH2-BRIEFED-CODEPATCH2-AUTH-OAUTH-AUTHORIZE-TOKEN-MESSAGE-COERCE-PASS-7of7-PASS-7of7_2026-11-02.diff.md
READY_KS-1868-KS-1868-O82-P5_spark-dsv4flash_BRIEFED-CODEPATCH2-BRIEFED-CODEPATCH2-ANCHORING-READ-ROUTE-MESSAGE-COERCE-PASS-7of7-PASS-7of7_2026-11-02.diff.md
READY_KS-1868-KS-1868-O82-P6_spark-dsv4flash_BRIEFED-CODEPATCH2-BRIEFED-CODEPATCH2-ORIGINATE-ANCHORS-MESSAGE-COERCE-PASS-7of7-PASS-7of7_2026-11-02.diff.md

## Per-site decisions (today vs after; does an ordinary Error already get the after-state?)
All hostile cases are an Error whose `message` getter RETURNS a non-string (revoked Proxy, toString-throws object, null-prototype object, Symbol). "Ordinary" = an Error with a string message. Tests use stub loggers (real winston not run), so the hostile reason is pinned as "logged value is a string: the constant for the first three, `Symbol(ks1868)` for a Symbol".
| pass / site | existing read | form chosen and why | after-state equals ordinary Error? |
|---|---|---|---|
| P1 auth.ts login rehash catch (559) | `err?.message` | m-form: a thrown plain string has no message and is logged with no `error` today; a bare String would newly log the text 'undefined'. C3/C4 pin that. | yes: login still 200 with session/tokens (rehash is reached only after the full credential gate; gate 113 G113-F3 measured head-unreadable == head-ordinary) |
| P1 auth.ts logout denylist `.catch` (794) | `err?.message` | m-form (same) | yes: 200, cookie cleared, session already revoked, JTI not denylisted either way |
| P2 internal.ts connector-token (84) | `(err as Error).message` | m-form. A thrown `undefined` makes the read throw inside the try and gives the constant today and after (C2 pins G113-F2); plain string logs no `error` (C3) | yes: 502, no token |
| P3 issuerCerts list (369) / revoke (520) | `err instanceof Error ? err.message : String(err)` | String-of-whole form (the P4 form): site already stringifies non-Error throws, so non-Error output is byte-identical (C3 null-proto -> constant, C4 plain string -> its text, G113-F2) | yes: constant 500, nothing revoked, no event. Edge: an Error whose own message is `undefined` was logged with no `error` and now logs the text 'undefined' (non-ordinary value, disclosed in the PR text) |
| P4 oauth authorize (810) / token (1120) | `error.message` | m-form; thrown `undefined` -> constant (C3/C4, G113-F2), plain string -> no `error` (C5) | yes: 500 server_error, nothing minted |
| P5 anchoring verify-by-hash local lookup (699), POST verify content-hash lookup (1315), `dbGetAnchorByTx` (1824) | `err?.message` | m-form; log() is `JSON.stringify`, so a plain string correctly stays key-less (C4/C5) | yes: tx 404, verify-by-hash falls to the chain step, POST verify `verified:false`; never a positive answer from a failed lookup; with the chain configured a chain hit answers `verified:true source:chain` exactly as for an ordinary Error (G114-F3) |
| P6 originate anchors verifyAnchorsDbReady (55), getAnchorByDocumentId warn (101), GET route catch (219) | `err instanceof Error ? err.message : String(err)` (`error` at 219) | String-of-whole form: site already stringifies non-Error. Edge same as P3. | yes: both GET lines logged, constant 500 (KS-1657 rethrow untouched), `verifyAnchorsDbReady` throws the constant `Database is required...` |
No site had to be skipped for failing the acceptance rule.

## Per pass
### O82-P1 auth.ts, 2 hunks @@ -554 and @@ -789 -- recommended TIER 1 (authentication; login path)
- `golden: BYTE-IDENTICAL; touched=2 product_plus=4 product_minus=2 red=8/12 green=12/12 suite=1492->1504 strict=True` (vitest). Test `ks1868-auth-rehash-denylist-message-coercion-unreadable-throw.test.ts` (C1-C4, R1-R8).
- Callers: POST /api/auth/login, POST /api/auth/logout.
- BEHAVIOUR CHANGE (PR text): hostile non-string message only: a login whose rehash write failed answers 200 with a session instead of 500 with none (same as an ordinary Error, after the full credential gate; no refused login issues anything); logout answers 200 and clears the cookie instead of 500; Symbol message logged as its text; string messages and no-message throws unchanged. QA gate must re-check the 500 -> 200 login row (gate 113 F3 reasoning applies).
### O82-P2 internal.ts, 1 hunk @@ -79 -- recommended TIER 1 (auth connector-token; fail-closed 502)
- `golden: BYTE-IDENTICAL; touched=2 product_plus=2 product_minus=1 red=4/7 green=7/7 suite=1492->1499 strict=True`. Test `ks1868-internal-connector-token-message-coercion-unreadable-throw.test.ts` (C1-C3, R1-R4).
- Callers: api-gateway auth middleware (non-2xx or timeout both = no Bearer). BEHAVIOUR CHANGE: hostile message only: 502 instead of hang + unhandled rejection; Symbol logged as text; thrown undefined and plain string unchanged.
### O82-P3 issuerCerts.ts, 2 hunks @@ -364 and @@ -515 -- recommended TIER 1 (issuer certificates; revoke path)
- `golden: BYTE-IDENTICAL; touched=2 product_plus=2 product_minus=2 red=8/12 green=12/12 suite=1492->1504 strict=True`. Test `ks1868-issuer-certs-message-coercion-unreadable-throw.test.ts` (C1-C4, R1-R8).
- BEHAVIOUR CHANGE: Error with hostile non-string message only: constant 500 instead of hang; nothing revoked/published either way; non-Error throws unchanged; edge: Error with own `message === undefined` now logs the text 'undefined'.
### O82-P4 oauth.ts, 2 hunks @@ -807 and @@ -1117 -- recommended TIER 1 (OAuth authorize/token)
- `golden: BYTE-IDENTICAL; touched=2 product_plus=4 product_minus=2 red=8/13 green=13/13 suite=1492->1505 strict=True`. Test `ks1868-oauth-message-coercion-unreadable-throw.test.ts` (C1-C5, R1-R8).
- BEHAVIOUR CHANGE: hostile message only: 500 server_error instead of hang; nothing minted; thrown undefined / plain string unchanged.
### O82-P5 anchoring index.ts, 3 hunks @@ -694, @@ -1310, @@ -1819 -- recommended TIER 1 (anchoring read routes; also pre-auth verify-by-hash). Tier 2 would be defensible (read-only, never a write or positive claim) but G114 ran it TIER 1 and one route is unauthenticated.
- `golden: BYTE-IDENTICAL; touched=2 product_plus=6 product_minus=3 red=12/17 green=17/17 suite=760->777 strict=True`. Test `ks1868-anchoring-message-coercion-unreadable-throw.test.ts` (C1-C5, R1-R12).
- BEHAVIOUR CHANGE: hostile message only: the three routes answer as an ordinary Error does (tx 404 / chain step / `verified:false`) instead of hanging or 500 with the error text in `details`; with the chain configured a chain hit then answers `verified:true source:chain` (established by the chain); Symbol logged as text. NOT touched: the outer verify-by-hash catch `details: error?.message` (author's board candidate), G114-F4 card.
### O82-P6 originate routes/anchors.ts, 3 hunks @@ -50, @@ -96, @@ -214 -- recommended TIER 1 (anchoring)
- `golden: BYTE-IDENTICAL; touched=2 product_plus=3 product_minus=3 red=8/12 green=12/12 suite=2189->2201 strict=True` (jest). Test `ks1868-anchors-message-coercion-unreadable-throw.test.ts` (C1-C4, R1-R8). G114-F2 addressed in the test: GET uses `AbortSignal.timeout(1500)` (hang = null answer, not a jest timeout), `verifyAnchorsDbReady` rejection read with `.then(ok, err)` (no matcher touches a hostile value), unhandled rejections counted via `process.on('unhandledRejection')` -- UNMEASURED whether jest's sandboxed `process` delivers that event, so that assertion may be vacuous; the other two measures are real.
- BEHAVIOUR CHANGE: Error with hostile non-string message only: both GET log lines carry the constant (warn line no longer lost), `verifyAnchorsDbReady` rejects with the constant error instead of the logger's own error; status never changes; edge as P3.

## Raise-seat notes
- All strict (plain git apply). Hunk distances: P1 235 lines apart; P3 151; P4 310; P5 616 and 509; P6 46 and 118; none within 3 lines. Same-file overlap with other operators' held passes: none (O80 and O81 touched admin.ts, ipfs, blockchain-verifier, security).
- P1-P4 share services/auth/src/routes/ but four different files; the passes applied together were NOT run. Each new test is a copy of the merged PR 1931/1932 harness for that file plus new cells; they share names only with the pattern `ks1868-*`.
- Cell names: `control ks1868 C<n>` / `RED ks1868 R<n> ...`. Cells compare strings via a `reasonOf` helper (typeof) so a revoked Proxy never reaches an assertion.
- Stub loggers record what they receive; real winston and the hang itself were not run. Evidence for the real-winston behaviour is gates 113/114.
- Model output header lines: golden is byte-identical in every held row, so the `--- a/`/`+++ b/` failure did not recur.

## Round log (spark/done.md row times, AEDT; done_rows.out)
- P5: ctl PASS 20:06:14 (first control; P1 had failed three times, see below); model PASS 7/7 20:16:29 (572 s round, 123.3 s model).
- P1: ctl FAIL 19:48:59, 19:54:47, 19:59:02, 20:46:56 (all A6: ks949 enumeration/seed cells timed out at 5000 ms in the AFTER suite under load 12-15; A4 red-first 8/12 and A5 green 12/12 passed every time); ctl PASS 21:00:49; model PASS 7/7 21:25:17 (336 s, 119.9 s).
- P6: ctl FAIL 20:21:54 (A6: originate ks695 and ks730c cells hit the 5000 ms jest timeout); ctl PASS 20:49:46; model PASS 7/7 21:04:36 (225 s, 69.9 s).
- P2: ctl PASS 20:31:56; model REFUSED 20:50:08 (transient GitHub RemoteDisconnected reading attached PR #1914, as operator 81 saw); re-queued, model PASS 7/7 21:08:59 (261 s, 61.8 s).
- P3: ctl PASS 20:40:13; model FAIL 20:54:47 (A1-A5, A7 passed; A6 ks949 timeout flake), re-queued same line, model PASS 7/7 21:14:18 (317 s, 85.2 s).
- P4: ctl FAIL 20:44:11 (ks949), ctl PASS 20:57:09; model FAIL 21:19:40 (A6: 5 failures, 8 suites failed, ks728/ks847 etc. under load), re-queued, model PASS 7/7 21:29:44 (265 s, 75.9 s).
- Queue discipline: ONE control (P1) until a CONTROL-PASS was due; after P1 failed on the environmental flake I queued P5's control alone (CONTROL-PASS proved the harness), then P5 model + P6/P2/P3/P4/P1 controls together. Each model line only after its own CONTROL-PASS. Polled with grep -c -i on done.md.
- Reading the ks949 flake: the cells walk the whole Dev tree (readdir + readFile) with the default 5000 ms; baseline passed after the first runs and AFTER failed consistently while load avg was 12-15, passing at load ~8. Not caused by the patch (same cells pass in P2/P3/P1/P4 retries with identical product bytes). Suggest a raise seat's CI be the real arbiter; a longer timeout on ks949 is a separate board item.

## Skipped (with reasons)
- auth.ts guards at 311, 631, 911 (older guards, not part of PR 1931's diff, not named by G113): not screened for their message read; left for a separate brief.
- security/src/index.ts rotate catches 306/419: NOT screened. Items 1 and 2 were not exhausted; the fallback was therefore not triggered.
- anchoring verify-by-hash OUTER catch (`details: error?.message`, response echo, author's board candidate), G114-F4 (failed lookup answered as absence): not log guards; separate cards.
- oauth.ts `message: error.message` response bodies (:1272 ff., G113-F6) and errorHandler.ts unguarded `err.message`: other KS-1868 sites, out of this assignment.
- Zod pre-check sites: none among mine.

## UNMEASURED
Whole-suite CI and eslint; real winston (the hang); real Postgres/Redis/JWT keys/Blockfrost; Node 24; the six passes applied together; PR bodies and Linear text; whether jest's `process.on('unhandledRejection')` fires in the P6 cells; whether a hostile non-string message occurs in production. Evidence: this folder (tip_*.out, prscan_*, open_prs_*.json, lint_p*.out, dry_p*.out, hold_p*.log, mk_p*.out, ls_held.out, done_rows.out, drift_*.out, gen/tests82.py sites82.py mk82.py hold82.sh prscan82.py t82_p*.ts.txt).
