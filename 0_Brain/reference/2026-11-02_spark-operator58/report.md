# Spark operator 58, 2026-11-02: KS-1868 api-gateway routes/admin.ts identity-admin catches (O58-P1 HELD, 3 hunks)

## BLUF
HELD: O58-P1 (3 log-only catches, GET identity users :1274, GET identity organizations :1296, PATCH identity users/:id/level :1320). Skipped: none (re-derived at the tip: exactly these 3 `instanceof Error ? ... : String` sites in admin.ts; the other catch in the identity block, seedIdentityOrgsIfEmpty `(err as Error).message`, is a different shape, left). Tip 03977e89a343ad7362760e4fb0270602fb6da5ce at start (tip_start.out) and end (tip_end.out). Open-PR scan start 20 PRs/113 files, end 21 PRs/119 files (new #1910 mcp-server); no PR lists admin.ts or api-gateway src (api-gateway only package.json in 575/649); planted control services/originate = 6 both times (prscan_start.out, prscan_end.out).
Counter: the first control FAILED (my test, not the model); a model round was queued with it and FAILED the same way. Per Wednesday's correction that failed round does NOT spend the rebrief counter (brief never proven). Corrected test, control CONTROL-PASS first time, model PASS 7/7 on the first proven brief. I also queued control+model together a second time before the correction arrived; the model line was removed again about 5 s later (07:58:12, own line only) so it never ran; the model line was re-appended only after CONTROL-PASS (08:02:43).

## Held (ls night | grep O58)
READY_KS-1868-KS-1868-O58-P1_spark-dsv4flash_BRIEFED-CODEPATCH2-p1-PASS-7of7_2026-11-02.diff.md

## O58-P1
- hold_ready: `golden: BYTE-IDENTICAL; touched=2 product_plus=21 product_minus=3 red=7/14 green=14/14 suite=1373->1387 strict=True`. Model 85.3 s (round 162 s).
- Guard helper: none exists in api-gateway (no describeThrown, no 'unreadable thrown value' there). House pattern reused: inline `let reason: string; try { reason = <same expr> } catch { reason = 'unreadable thrown value' }` as merged in shared audit-logger/response-cache and analytics. The log call becomes `{ error: reason }`; log message text and the 500 untouched.
- Test: src/__tests__/ks1868-admin-identity-route-catches-p1-unreadable-throw.test.ts (14 cells: 3 routes x R1/R2/C1/C2, plus R3 and C3 for PATCH level). Handler = last function of the route taken from the router stack, called directly (requireAdmin bypassed on purpose, it is not touched). Shape ref ks1196-admin-post-api-admin-document-types.test.ts.
- Callers: admin console over HTTP behind requireAdmin; no code caller.
- Today vs after: unreadable DB rejection: today the catch throws, nothing is logged, no response (unhandled rejection, client hangs/times out); after: logs `{ error: 'unreadable thrown value' }` and answers the constant 500 an ordinary Error already gets (controls C1). Authorisation: unchanged (requireAdmin not touched; admitted/refused before the handler). Persisted state: unchanged; PATCH level's single `UPDATE users SET verification_level` runs BEFORE anything can throw and the catch writes nothing; cell R3 pins exactly one UPDATE with params ['HIGH', id] in the failure case. No credential issued/revoked. No outcome an ordinary Error does not already produce, so no site skipped.
- BEHAVIOUR CHANGE (PR text): as above; no body/status/log change for ordinary Errors or strings.
- Recommended tier: 2 (identity admin write route; Kam may promote to 1 because PATCH level changes a user's verification level, though this change does not touch that write).
- Raise-seat notes: strict=True (plain git apply). Hunks 22 and 24 lines apart (1274/1296/1320). No existing api-gateway test reads admin.ts as text for these log lines (grep of the tip src found none outside admin.ts). Not in conflict with any in-flight file. Note for the raise seat: PATCH level is reachable by ORG_ADMIN/ISSUER_ADMIN roles per ADMIN_ROLES for any user id (existing behaviour, observed, not touched, possible separate finding).

## Round log (spark/done.md; done_rows.txt)
- 07:52:29 control + model queued; 07:54:46 CONTROL-FAIL (123 s): suite A6 NEW red ks1090 (api-gateway test files type-checked against a shrinking baseline): `TS6133 'router' is declared but its value is never read` at line 15 of my new test, caused by the harness's DECL-SPLICE accommodation (it spliced `let router: Router;` from the ref because my file used the word `router` as a parameter/comment). Cells themselves were fine (A4 7 red/14, A5 14/14).
- 07:57:46 model round FAIL (same A6; golden BYTE-IDENTICAL; 179 s, model 85.4 s): not counted.
- Fix: removed the word `router` from the test (param renamed `rt`, comment reworded), regenerated, lint rc 0 (lint_p1b.out), dry run rc 3 BUSY (queued the control anyway, per the commission).
- 08:02:35 CONTROL-PASS (76 s). 08:02:43 model line appended. 08:05:39 model PASS 7/7 (162 s), BYTE-IDENTICAL. hold_ready after that.
- Lesson for later operators: avoid the identifier `router` (or any ref file-scope decl name) in a new api-gateway test; a DECL-SPLICE accommodation adds an unused decl that the ks1090 type-check baseline rejects.

## UNMEASURED
Whole-suite CI beyond the checker's api-gateway suite; eslint; a real Express 4 request path (handler-level only); whether an unreadable value is reachable in production; other admin.ts catches (not screened beyond the 3 sites).
Evidence: this folder (tip_*, prscan_*, lint_*, dry_*, mk*.out, hold_p1.out, done_rows.txt, held_files.txt, gen/mk58.py, gen/t58_p1.ts.txt, gen/KS-1868.p1.orig.md).
