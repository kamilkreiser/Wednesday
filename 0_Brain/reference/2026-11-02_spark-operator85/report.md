# Spark operator 85, 2026-11-02 22:57 to 2026-11-03 00:10 AEDT: KS-1868, 6 passes held (2 inherited from O84, 4 more of mine counted below = 8 held READY files in total from this seat)

## BLUF
- HELD by this seat: O84-P2, O84-P3 (inherited briefs) and O85-P1..P6 = 8 READY files. O84-P1 was already held by operator 84 (not touched). All strict=True except O84-P2 (strict=False, as printed by hold_ready).
- FAILS: 1 model-round A6 fail (O84-P3 23:01:38), class HARNESS (ks949 timeout flake), PASSED on the one re-run. 5 CONTROL-FAILs (brief/test or harness, none a model verdict): O85-P3 x2 (ks949 flake), O85-P4 x2 (test-side), O85-P6 x1 (test-side). All fixed or re-run; no model round ever ran behind a failing control.
- Tip: develop 36b967b987d2 at start, 1584c0f0ff80 from 23:06, 3043c5bcf4e9 at the end (ls-remote 00:09). Drift 36b967b9..3043c5bc on my 8 product files: EMPTY (drift_end.out, 0 bytes).
- Open-PR scans (planted control services/originate): start 22 PRs / 187 files, control 10 (prscan_start.out); end 23 PRs / 195 files, control 10 (prscan_end.out). No open PR lists any of my product files or test names.
- Stopped at 6+ held. Nothing left in the queue from this seat. No background process of mine alive.

## Held (night/, ls_held.out)
- O84-P2 auth services/issuerCertSweep.ts :106-:157 (2 hunks, EXPIRING_SOON publish .catch + startup sweep .catch). model PASS 7/7 22:54:45 (operator 84's run), held by me. Patch read against the brief: 2 files, 2 hunks, test new file, nothing else. golden BYTE-IDENTICAL, strict=False. T1 (issuer certs). READY_KS-1868-KS-1868-O84-P2_spark-dsv4flash_..._2026-11-02.diff.md
- O84-P3 auth services/oauthState.ts :131 (1 hunk, consumeOAuthState Redis catch). model PASS 7/7 23:10:22 on the re-run (first model round 23:01:38 FAIL A6, harness flake). strict=True. T1 (OAuth social-login state, fail closed: returns false + 403). READY_..._O84-P3_..._2026-11-02.diff.md
- O85-P1 auth services/accountLockout.ts :89,:119,:130 (3 hunks; isLockedOut / recordFailure / recordSuccess catches, `err?.message` form: m===undefined||null kept, else String(m), constant on throw). control PASS 23:06:18, model PASS 7/7 23:13:52, 12 cells (4 C + 8 R), strict=True, vitest, suite 1492->1504. T1 (login lockout). Behaviour change: hostile Redis error now fails open as documented instead of rejecting into the route error path.
- O85-P2 anchoring src/reconciler.ts :403,:411 (2 hunks: per-row chain-check catch, whole-pass catch; the :281 no-hash sweep catch deliberately not taken). control PASS 23:20:02, model PASS 7/7 23:38:40, 12 cells, strict=True, vitest, suite 760->772. T1 (anchor status writer). Behaviour change: after a hostile chain-check error the pass carries on with the remaining rows (as for an ordinary Error) instead of rejecting. NOTE the two hunks are 1 unchanged line apart (410): a raise seat should confirm `git apply` is clean and consider one merged hunk.
- O85-P3 auth services/password.ts :97,:142 (argon2 verify catch, HIBP catch; :65 loadArgon2 not taken). control PASS 23:53:43 (r3, after two ks949 flake CONTROL-FAILs), model PASS 7/7 00:03:21, 10 cells, strict=True, suite 1492->1502. T1 (password verification). verifyPassword now answers false (refused) and isPasswordBreached false (fail open) for a hostile value, instead of rejecting.
- O85-P4 api-gateway middleware/audit.ts :330 (1 hunk, fire-and-forget audit write catch). control PASS 23:55:39 (after 2 test-side CONTROL-FAILs), model PASS 7/7 00:07:51, 8 cells, strict=True, suite 1412->1420. T1 (audit trail). Behaviour change: failed audit write logged instead of unhandled rejection.
- O85-P5 api-gateway middleware/security.ts :194 (1 hunk, brute-force Redis catch). control PASS 23:30:23, model PASS 7/7 23:47:54, 8 cells, strict=True, suite 1412->1420. T1 (login brute-force guard). Behaviour change: hostile Redis error lets the login request through (fail open, as for an ordinary Error) instead of hanging with an unhandled rejection.
- O85-P6 originate utils/lifecyclePayloadCodec.ts :53 (1 hunk, decrypt-failed catch). control PASS 23:50:40 (after 1 test-side CONTROL-FAIL), model PASS 7/7 23:58:46, 8 cells (jest), strict=True, suite 2283->2291. T2 (read path, log + payloadUnavailable marker). Behaviour change: hostile decrypt failure returns the marker instead of throwing and failing the listing.
Full filenames: `ls /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night | grep -E 'READY.*(O84|O85)'` (saved: ls_held.out). Hold outputs: hold_p2.log, hold_p3.log (O84), hold_p1.log, hold_p2n.log, hold_p3n.log, hold_p4.log, hold_p5.log, hold_p6.log (O85). Each patch was read at source against its brief in the same action as the hold (3-line diffs match the brief byte for byte; A3x PASS).

## Fails (class)
- O84-P3 model 23:01:38 FAIL A6: patch byte-identical to golden, A1-A5/A7 PASS; ks949-platform-admin-seed-identity tree-walk cells time out (a different cell in baseline vs after). HARNESS (known op50 flake, IMPROVEMENTS line 983). One re-run: PASS 23:10:22. IMPROVEMENTS row added.
- O85-P3 --control 23:22:43 and 23:41:44 FAIL A6: the same ks949 pair; HARNESS. Third control PASS 23:53:43. IMPROVEMENTS rows added.
- O85-P4 --control 23:26:10 FAIL A4 (BRIEF/test): my `until()` helper threw on timeout so RED cells failed by a thrown Error. Fixed (helper returns, expect fails). 23:44:36 FAIL A6 (BRIEF/test): unused `vi` import tripped ks1090 type-check ratchet. Fixed. PASS 23:55:39. IMPROVEMENTS rows.
- O85-P6 --control 23:33:11 FAIL A6 (BRIEF/test): hand-written `@secuura/shared` mock factory tripped ks1061; fixed with makeSharedMock. PASS 23:50:40. IMPROVEMENTS row.
- Counter: no pass used a model rebrief (the O84-P3 re-run was the single permitted one).

## Never-brief list used
services/*/src/index.ts (PR 1944); packages/shared; files of held passes O80-O84 (held_prodfiles.out: anchoring/index.ts, api-gateway rateLimitEnforce.ts + admin.ts, auth routes auth/internal/issuerCerts/oauth + services/issuerCertSweep.ts, nft-certificate blockchain-verifier + ipfs, originate anchors.ts + documents.ts, security db.ts + index.ts); any file an open PR lists (open_prs_start.json; PR 1938 lists kyc routes/microsoft-verification.ts); the Zod pre-check sites.

## Skipped with reason
- tokenisation/src/vault.ts:81 (detokenise decrypt catch): the package is ESM ("type":"module", module Node16) and the catch calls `require('node:crypto')`, which is not defined in ESM at runtime, so an ORDINARY decrypt failure already throws ReferenceError in production; guarding the message read alone would not give the ordinary-Error outcome. Separate bug; raise it to Wednesday (not tested under vitest, whose transform provides require: UNMEASURED).
- accountLockout/password.ts/reconciler remaining sites: password.ts:65 (dynamic-import catch, module cache), reconciler.ts:281 (needs boot-grace sweep).
- issuerCertSweep.ts:163 (scheduled sweep catch): file now held by O84-P1/P2.
- originate errorTrackingService.ts:141 not briefed (time; it is a single site, log then returns empty), listed below as remaining.

## Remaining qualifying sites (not briefed)
Operator 83 screen supply minus what is now held: gateway routes/verification.ts:952 (document-create last-line-of-defence .catch, highest value, heavy harness), routes/platform.ts:1092 (clone), originate errorTrackingService.ts:141, anchorStateSync.ts:600, documents.ts other routes (file held by O83), platformOrganizations.ts:112/145/168 (hold for Seat E 29th), shared stores (25 sites, packages/shared never-brief). New from my re-screen (err?.message in logger/console arguments, screen_f.out): auth password.ts:65, auth email.ts:140/167/207, auth userErasedSubscriber.ts:100/107, auth accountLockout done, auth db.ts:41/160/190, the per-service db.ts triple (pool.on error / boot work / health, about 14 services; all `err?.message`), kyc/wallet-connector/m365 userErasedSubscriber.ts, transfer approvalWorkflowService.ts:345/356/629 (console args), anchoring reconciler.ts:281, anchoring db.ts. Supply is NOT exhausted (about 40 sites, roughly 12 passes).

## Round log (done.md row times AEDT)
O84-P3 model 23:01:38 FAIL, re-run 23:10:22 PASS. O85-P1 ctl 23:06:18, model 23:13:52. O85-P2 ctl 23:20:02, model 23:38:40. O85-P3 ctl FAIL 23:22:43, FAIL 23:41:44, PASS 23:53:43; model 00:03:21. O85-P4 ctl FAIL 23:26:10, FAIL 23:44:36, PASS 23:55:39; model 00:07:51. O85-P5 ctl 23:30:23, model 23:47:54. O85-P6 ctl FAIL 23:33:11, PASS 23:50:40; model 23:58:46. O84-P2 model row 22:54:45 (operator 84).

## Processes started and stopped
Background: watch_p3.sh (exited on the O84-P3 row), watch_rows.sh x4 (each exited on its row). Foreground cycle85.sh polls only. Nothing is running (ps check at 00:10). The Spark queue.md has no line of mine left.

## UNMEASURED
Hunk distance for O85-P2 (1 line gap) under a real raise; O85-P1..P6 applied together with O80-O84 passes; whole-repo CI/eslint; real Redis/Postgres/argon2 native; production occurrence of a hostile non-string message; vault.ts ESM `require` claim at runtime.

## Files
Scripts: gen/ (mk85.py, sites85.py, t85_p1..p6.ts.txt), hold85.sh (O84 labels), holdN85.sh (O85 labels), advance85.sh, cycle85.sh. Briefs: night/briefs/ks_1868_o85_p1..p6_*. IMPROVEMENTS.md rows appended (Operator 85 section and four bullets).
