# Spark operator 86, 2026-11-03 00:13 to 00:57 AEDT: KS-1868, 6 passes HELD

## BLUF
- HELD: O86-P1, P3, P4, P5, P6, P7 (6 READY files, all strict=True, golden BYTE-IDENTICAL, one model round each, no rebrief needed for these). Names: ls_held_full.out.
- NOT held: O86-P2 (auth email.ts): model FAIL 00:36:05 (class HARNESS: beforeAll import hook timeout 10 s, plus the ks949 A6 flake; patch was byte-identical to golden). One rebrief (explicit 60 s beforeAll timeout): control FAIL 00:49:14 (ks949 A6 only, HARNESS), control PASS 00:56:21. Model round NOT queued (stop rule: 6 held). It is ready to queue: brief dir ks_1868_o86_p2_auth_email_acs_smtp_send_catches_guard_message, control PASSed, only the model line is missing.
- Tip: develop 3043c5bc at the brief, 9a9bf869 at my first brief (pinned, 00:14), 14fd8e54 at 00:36, 1439e93e at the end (tip_end.out). Drift 9a9bf869..14fd8e54 and ..1439e93e on my 7 product files: EMPTY (drift_14fd.out, drift_end.out, 0 bytes).
- Open-PR scans (planted control services/originate): start 22 PRs / 154 files, control 9 (prscan_start.out); end 22 PRs / 126 files, control 6 (prscan_end.out). No open PR lists any of my product files. (Start scan: only PR 1947 lists governance db.ts, not mine.)
- No background process of mine alive. Spark queue.md has no line of mine left.

## Held (night/, ls_held_full.out). Tier recommendation T1 = most careful review, T3 = least.
- P1 originate src/services/errorTrackingService.ts :141 (1 hunk, getRecentErrors catch; the house guard already in trackError of the same file, expression unchanged). control PASS 00:19:45, model PASS 7/7 00:24:37, 7 cells (4 C + 3 R), suite 2318->2325, jest. Tier T3 (admin dashboard read, log + empty list). Behaviour change: an unreadable thrown value gives the empty list (and a logged text line) instead of the route's generic 500. READY ...O86-P1_..._BRIEFED-CODEPATCH2-ORIGINATE-ERROR-TRACKING-GET-RECENT-ERRORS-CATCH-MESSAGE-COERCE-PASS-7of7_2026-11-03.diff.md
- P3 kyc src/userErasedSubscriber.ts :42 (1 hunk, user.erased handler-failed catch, house `err?.message` guard, `throw err` untouched). control PASS 00:28:44, model PASS 7/7 00:38:21, 6 cells, suite 79->85, vitest. Tier T2 (GDPR erasure failure path, logging only). Behaviour change: hostile value is now logged and the ORIGINAL value rethrown to the bus (today: a different error, no log). The loop-terminated .catch (:48) deliberately NOT taken (see skipped).
- P4 wallet-connector src/userErasedSubscriber.ts :53 (same shape as P3). control PASS 00:29:40, model PASS 7/7 00:40:08, 6 cells, suite 61->67, vitest. Tier T2. Same behaviour change as P3.
- P5 transfer src/services/approvalWorkflowService.ts :345,:356,:629 (3 hunks: seed upsert catch, verifyDbReady catch, processEscalations catch; console-argument `err?.message`, house guard). control PASS 00:30:37, model PASS 7/7 00:42:49, 10 cells (4 C + 6 R), suite 120->130, vitest. Tier T2. Behaviour change: boot probe/seeding carry on and log, escalation sweep returns its counts, instead of rejecting. Hunks 11 and ~270 lines apart; strict.
- P6 analytics src/db.ts :37 and :96 (2 hunks: pg pool 'error' listener, runDbReadyHook catch). control PASS 00:31:43, model PASS 7/7 00:45:04, 9 cells, suite 108->117, vitest. Tier T2 (database client; the listener fix removes an uncaught-exception path). Behaviour change: pool error logged instead of an uncaught exception, failed onReady hook logged instead of initDb rejecting. probeDb :107 deliberately not touched (typed `error?: string`; guard would change null handling).
- P7 api-gateway src/db.ts :37 and :101 (clone of P6 for the gateway). control PASS 00:46:50, model PASS 7/7 00:53:02, 9 cells, suite 1412->1421, vitest. Tier T2. Same behaviour change as P6. Note api-gateway src/index.ts is in flight (PR 1944 area): this pass touches db.ts only.
Hold outputs: hold_p1.log .. hold_p7.log (p2 absent). Each patch was read at source against its brief in the same action as the hold (hunk headers and `+` line counts match the golden; A3x PASS, numstat as printed).

## Fails (class)
- O86-P2 model 00:36:05 FAIL (A4: Hook timed out in 10000ms in beforeAll dynamic import; A6: ks949 flake). HARNESS (cold import under load) with a brief-side mitigation (60 s hook timeout). IMPROVEMENTS rows added.
- O86-P2 --control (rebrief) 00:49:14 FAIL A6 only: ks949 flake, HARNESS. Third control PASS 00:56:21.
- Counter: P2 used its one rebrief. No other pass failed anywhere (all other 5 controls and 5 model rounds PASS first time).

## Never-brief list used
services/*/src/index.ts (PR 1944), packages/shared, governance.ts and governance db.ts (PR 1947, Seat S 13th), services/auth/src/routes/users.ts, tokenisation vault.ts, the product files of held O80-O85 (anchoring index.ts, reconciler.ts; api-gateway rateLimitEnforce.ts, admin.ts, audit.ts, security.ts; auth routes auth/internal/issuerCerts/oauth, services issuerCertSweep.ts, oauthState.ts, accountLockout.ts, password.ts; nft-certificate blockchain-verifier, ipfs; originate anchors.ts, documents.ts, lifecyclePayloadCodec.ts; security db.ts, index.ts), every file an open PR lists (open_prs_start.json, open_prs_end.json), Zod pre-check sites.

## Skipped with reason
- userErasedSubscriber `.catch` loop-terminated sites (auth :107, kyc :48, wallet-connector :59, m365 :44): a hostile value there is an UNHANDLED REJECTION in the handler itself; vitest reports unhandled errors as a run failure, so the checker's red/green split would be muddied. Needs a harness decision, not a brief.
- auth userErasedSubscriber :100 (handler-failed): needs the platform-scope query, subjectDeks and session revocation stubbed; not attempted for time.
- auth email.ts :140 (ACS init dynamic-import catch): needs an import failure; left in P2.
- originate anchorStateSync.ts :600 (verify-heal write catch): needs the resolver fixtures; not attempted.
- analytics/api-gateway/anchoring db.ts probeDb catch (`return { ok: false, error: err?.message }`): typed `error?: string`; guard changes null handling; left for a Claude seat.

## Remaining sites
O86-P2 (email.ts :167,:207, control PASSed, model line to queue); anchoring db.ts (:36 listener, :91 probe); analytics/api-gateway/others probeDb catches; the loop-terminated catches above; auth userErasedSubscriber :100; anchorStateSync.ts :600; platform.ts :1092 / :995; gateway routes/proxy.ts :208,:513,:545,:629 and routes/verification.ts :605,:943; auth db.ts :41/:160/:190; auth userErasedSubscriber; kyc/wallet-connector listed; shared stores (packages/shared, never-brief); anchoring cardano provider.ts / confirmation.ts / threadTokenIndex.ts and anchorStatusUpdate.ts :225 (screen_f.out of operator 85). Not exhausted (about 30 sites).

## Round log (done.md row times AEDT)
P1 ctl 00:19:45, model 00:24:37. P2 ctl 00:27:45, model FAIL 00:36:05, ctl FAIL 00:49:14, ctl PASS 00:56:21 (no model). P3 ctl 00:28:44, model 00:38:21. P4 ctl 00:29:40, model 00:40:08. P5 ctl 00:30:37, model 00:42:49. P6 ctl 00:31:43, model 00:45:04. P7 ctl 00:46:50, model 00:53:02.

## Processes started and stopped
Background: one cycle86.sh poll (exited on its own). Foreground tick.sh/advance86.sh polls only. Nothing running (ps check 00:57). The Spark was fed continuously from 00:15 to 00:57.

## UNMEASURED
All six held passes applied together or with O80-O85; whole-repo CI/eslint; real pg/Redis/nodemailer/ACS; the hunk distance for P3/P4 with the loop catch fixed later; production occurrence of a hostile non-string message.

## Files
gen/ (mk86.py, sites86.py, t86_p1..p7.ts.txt, mkt_cascade.py), hold86.sh, advance86.sh, cycle86.sh, tick.sh, briefs in night/briefs/ks_1868_o86_p1..p7_*, IMPROVEMENTS.md (Operator 86 section appended).
