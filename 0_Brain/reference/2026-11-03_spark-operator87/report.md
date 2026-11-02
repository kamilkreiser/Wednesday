# Spark operator 87, 2026-11-03 00:57 to 01:50 AEDT: KS-1868, 6 passes HELD

## BLUF
- HELD (6, all strict=True, golden BYTE-IDENTICAL, one model round each): O87-P1, P2, P3, P4, P5, P7. Names: ls_held.out.
- O86-P2 (auth email.ts :167,:207): model round queued as the common file says; FAIL 01:03:33 and FAIL 01:09:57 (the re-run). Both: A1-A5 and A7 PASS, patch byte-identical to golden, only A6 red = ks949 tree-walk tests ('the real person is gone from every EXECUTABLE seed site ...') failing in the AFTER suite (baseline of the same round: 0 failed in the second, 1 different ks949 failure in the first). Class HARNESS (ks949 flake). Its one rebrief was already used by operator 86: SECOND FAIL, goes to a Claude seat. NOT held. Recorded.
- Tip: develop e7a3b1fb at start (ls-remote 01:00), 73342c2f at 01:24 (P8/P9 pinned there), 8150eeb3 at end (tip_end.out). Drift e7a3b1fb..8150eeb3: 11 files, none of my product files (drift_end.out; count 0 with a positive control of 11 lines).
- Open-PR scans (planted control services/originate): start 21 PRs / 119 files, control 6 (prscan_start.out); end 20 PRs / 114 files, control 6 (prscan_end.out). No open PR lists any of my product files or the new test files (prscan_end_mine.out).

## Held (night/, ls_held.out). Tier T1 = most careful review, T3 = least.
- P1 anchoring src/db.ts :36 (1 hunk, pg pool 'error' listener `err.message` -> house guard). control PASS 01:06:01, model PASS 7/7 01:13:20, 5 cells (2 C + 3 R), suite 760->765, vitest. Tier T3 (log only; removes an uncaught-exception path). Behaviour change: pool error with unreadable/non-string message is logged instead of an uncaught exception; Symbol message logged as text.
- P2 auth src/db.ts :41 and :160 (2 hunks: pool listener; ensureUserColumns best-effort migration catch). control FAIL 01:15:53 (A6 ks949 only, HARNESS), re-run PASS 01:28:20, model PASS 7/7 01:47:53, 9 cells (4 C + 5 R), suite 1536->1545, vitest. Tier T2 (database client of the auth service). Behaviour change: listener logs instead of an uncaught exception; a hostile failure of one migration statement is logged and skipped (later statements still tried, exactly as after an ordinary Error) instead of abandoning the loop and rejecting initDb. probeDb :190 deliberately untouched.
- P3 anchoring src/anchorStatusUpdate.ts :225 (1 hunk, runAnchorStatusUpdate catch). control PASS 01:18:43, model PASS 7/7 01:31:02, 7 cells, suite 760->767, vitest. Tier T2 (anchor status write path; return value null = unknown). Behaviour change: hostile value now resolves null and logs at warn instead of rejecting.
- P4 anchoring src/cardano/threadTokenIndex.ts :73-84 (1 hunk, ONE guard before `if (STRICT_MODE)` used by both branches). control PASS 01:20:48, model PASS 7/7 01:33:57, 9 cells (4 C + 5 R, strict and non-strict), suite 760->769, vitest. Tier T1 (thread-token trust registry, STRICT_THREAD_TOKEN_INDEX). Behaviour change: non-strict resolves [] (fall back to metadata-only, same as any registry failure) instead of rejecting; strict rethrows the ORIGINAL value instead of the read error. Reviewer note: the non-strict fall back is the existing documented behaviour for any registry failure.
- P5 anchoring src/cardano/confirmation.ts :107 (1 hunk, waitForConfirmation catch, template-literal read). control PASS 01:22:52, model PASS 7/7 01:36:46, 7 cells, suite 760->767, vitest. Tier T2 (confirmation poll). Behaviour change: only for callers passing onStatusUpdate: failed attempt counted and poll continues with status 'error: unreadable thrown value' / 'error: Symbol(..)' instead of a rejection.
- P7 auth src/services/session.ts :59 and :72 (2 hunks: Redis 'error' listener; initRedisSession catch). control PASS 01:25:56, model PASS 7/7 01:44:28, 9 cells, suite 1536->1545, vitest. Tier T1 (session store; the listener fix also fixes the availability flag: today the throw precedes `redisAvailable = false`, so the flag stays true while Redis is down). Behaviour change: listener logs and marks Redis unavailable (sessions use the in-memory store); init catch resolves instead of rejecting.
Each patch was diffed against the brief's golden.diff (chk_pN.out: rc 0 = byte-identical), A1-A7 + A2a read from checker.out, and held in the same action (hold_pN.log). Auth suite baselines carry develop's own ks949 flake (attributed by the checker, not counted).

## Fails (class)
- O86-P2 model 01:03:33 FAIL and 01:09:57 FAIL: A6 only, ks949 tree-walk tests, HARNESS (patch byte-identical to golden). Second fail of the pass: Claude seat.
- O87-P2 control 01:15:53 FAIL: A6 only (ks949), HARNESS; re-run PASS 01:28:20 (one re-run per the O86 trap note).
- O87-P6 control 01:23:32 REFUSED builder rc 2: 'BLANK CONTEXT line' in a single hunk spanning events.ts :95 and :101 (a blank line sits between the two sites). Brief-side defect, fixed by narrowing to the init catch :101 only (new dir ks_1868_o87_p6_auth_events_init_catch_guard_message; old dir moved to _quarantine_2026-11-03/). New control PASS 01:41:08.
- Process slip (mine): advance87.sh was first generated with a stale key regex and queued the P1 model line twice; the duplicate (my own, still queued) was removed from queue.md before it ran.

## Pending / not held (stop rule: 6 held)
- O87-P8 kyc src/db.ts :36 (clone of P1): control PASS 01:37:46; its model line was queued and may still be running or have a row in done.md; NOT read or held by me.
- O87-P9 nft-certificate src/db.ts :36,:96 (clone of O86-P6): control PASS 01:38:50; model line removed from the queue unrun.
- O87-P6 auth events.ts :101 init catch: control PASS 01:41:08; model line removed from the queue unrun. Ready to queue.
- O87-P10 transfer db.ts and P11 wallet-connector db.ts are defined in gen/sites87.py (clones of O86-P6) but never generated.

## Never-brief list used
services/*/src/index.ts, packages/shared, governance.ts and governance db.ts, auth routes users.ts/auth.ts/issuerCerts.ts/oauth.ts/internal.ts, security index.ts, tokenisation vault.ts, product files of held O80-O86 (held_o80_86.out), every file an open PR lists (open_prs_start.json, open_prs_end.json), Zod pre-check sites.

## Skipped with reason
- anchoring cardano/provider.ts catches (:321,:393,:414,:432): initProvider always wraps the client in instrumentProvider, whose rejection handler (recordChainOutcome -> recordChainFailure reads err.status_code / err.message) throws first on a hostile value, so the catch sees a readable TypeError; a red cell cannot be built through the module's public path. :358 also reads err?.status_code before the message (half fix).
- api-gateway errorHandler.ts :72/:84: reads err.statusCode, err.stack and err.message unguarded in one terminal handler; needs a design decision, not a one-line guard.
- api-gateway routes/proxy.ts, verification.ts, platform.ts: heavy express/http-proxy harness; not attempted.
- auth providers/social/*.ts `unavailable()`: already wrapped in try/catch (false positive of the screen).
- auth events.ts :95 listener: left (blank interior context); needs a listener-only pass.

## Remaining sites
kyc/timestamping/staking/m365/referral/prism/billing/vc-issuer/transfer/wallet-connector/nft-certificate db.ts pool listeners (+ ready hook where present; clones of P1 / O86-P6); originate events.ts :89; auth events.ts :95; shared redis-client (never-brief); demo-service routes/state.ts :44; api-gateway services/redis.ts :92,:117-121; probeDb catches; auth userRepo.ts (many); userErasedSubscriber loop catches; startup-migrations.ts; anchoring cardano/index.ts :115. Not exhausted (about 25 sites).

## Round log (done.md row times AEDT)
O86-P2 model FAIL 01:03:33, FAIL 01:09:57. P1 ctl 01:06:01, model 01:13:20. P2 ctl FAIL 01:15:53, ctl PASS 01:28:20, model 01:47:53. P3 ctl 01:18:43, model 01:31:02. P4 ctl 01:20:48, model 01:33:57. P5 ctl 01:22:52, model 01:36:46. P6 ctl REFUSED 01:23:32, ctl PASS 01:41:08 (no model). P7 ctl 01:25:56, model 01:44:28. P8 ctl 01:37:46. P9 ctl 01:38:50.

## Processes started and stopped
loop87.sh (background poll of advance87.sh, stop file STOP): exited on its own (task bxemzqkxz completed). One earlier nohup loop died at once (never ran). tick87.sh foreground/background polls: finished. ps check 01:50: 0 matching processes. The Spark was fed continuously from 01:00.

## UNMEASURED
The six passes applied together or with O80-O86 (P2 and P7 both edit auth but different files; P3/P4/P5/P1 are four anchoring files); whole-repo CI/eslint; real pg/Redis/ioredis; production occurrence of a hostile non-string message; the P8 model round (not read).

## Files
gen/ (mk87.py, sites87.py, t87_p1..p9.ts.txt, prscan84.py), hold87.sh, chk87.sh, advance87.sh, loop87.sh, tick87.sh, briefs in night/briefs/ks_1868_o87_p1..p9_*, chk_pN.out, hold_pN.log.
