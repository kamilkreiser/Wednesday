# Spark operator 68, 2026-11-02: KS-1868 originate notificationClient, metering, retentionScheduler (3 held, 0 skipped, 0 failed, 0 rebriefs)

## BLUF
HELD: O68-P1 (utils/notificationClient.ts, both String(err) catches, 2 hunks), O68-P2 (routes/metering.ts GET /usage catch :129), O68-P3 (services/retentionScheduler.ts runEnforcement catch :51). All three controls CONTROL-PASS first time, all three model rounds PASS 7/7 on the ORIGINAL brief, golden BYTE-IDENTICAL, strict=True. Nothing skipped: none of the three catches does anything an ordinary Error does not already get (reasoning per pass). Tip: develop 03977e89 at start (tip_start.out); it MOVED to cde2dee4dffba6a61228c40d641ff567660c32b2 at 09:1x (tip_mid.out; the harness rounds ran at cde2dee4) and was still cde2dee4 at the end (tip_end.out). The move touched only mcp-server (tip_diff_stat.out; `git diff --stat` of Blockchain/Dev/services/originate between the two = empty, tip_diff_originate.out), so my three files and the briefs' quotes are unchanged. Open-PR scan start 22 PRs/125 files, end 23 PRs/131 files (new KS-1868 PRs 1912 security, 1913 billing); no open PR lists notificationClient, metering, retentionScheduler or an originate ks1868 test (MYFILE lines in prscan_start.out / prscan_end.out). Planted control services/auth/ = 11 entries at both scans (the scan script's label says "services/originate"; it counts services/auth/; services/originate has 6 entries, ORIGINATE-ENTRIES line).

## Held (ls night | grep O68; held_files.txt)
READY_KS-1868-KS-1868-O68-P1_spark-dsv4flash_BRIEFED-CODEPATCH2-ORIGINATE-NOTIFICATIONCLIENT-TWO-CATCHES-PASS-7of7-PASS-7of7_2026-11-02.diff.md
READY_KS-1868-KS-1868-O68-P2_spark-dsv4flash_BRIEFED-CODEPATCH2-ORIGINATE-METERING-USAGE-CATCH-PASS-7of7-PASS-7of7_2026-11-02.diff.md
READY_KS-1868-KS-1868-O68-P3_spark-dsv4flash_BRIEFED-CODEPATCH2-ORIGINATE-RETENTIONSCHEDULER-RUNENFORCEMENT-CATCH-PASS-7of7-PASS-7of7_2026-11-02.diff.md

## Gate answers (all three)
- Existing guard: grep (recon.out) found no describeThrown in originate; the only inline guard is certifications.ts :1087-1093 (`let reason: string; try {...} catch { reason = 'unreadable thrown value'; }`). All three passes copy it, keeping the original read expression so ordinary Error and string log text is unchanged. No helper added.
- No Zod pre-check site in any of the three. No existing originate suite targets the three files (notificationClient only appears as a module mock in other suites); each new test is self-contained.
- Suite baseline: harness baseline at the tip = 1999 tests (hold_ready `suite=1999->...`), controls 122/96/114 s. I did not run jest in the cache clone (stale @secuura/shared trap, per operator 63).

## O68-P1 notificationClient.ts catches at :56 and :110
- hold_ready: `golden: BYTE-IDENTICAL; touched=2 product_plus=14 product_minus=2 red=4/8 green=8/8 suite=1999->2007 strict=True`. Model 54.7 s (round 264 s incl. queue-run overhead), 13636+2411 tokens. Hunks `@@ -51,9 +51,15 @@` and `@@ -105,7 +111,15 @@`, 54 lines apart.
- Test (new): src/__tests__/ks1868-notification-client-catches-p1-unreadable-throw.test.ts, 8 cells: R1/R2 (service-call catch: fetch rejects with revoked Proxy / throwing-message Error), R3/R4 (SMTP-fallback catch), controls C1/C2 (ordinary Error `Error: ...` / string, service catch), C3/C4 (same, SMTP catch). Mocks logger, ../services/email and globalThis.fetch; calls notifyDocumentCertified directly.
- Callers (recon2.out): certifications.ts :831 notifyDocumentCertified, fire-and-forget WITH a `.catch` logging err?.message; :1153 notifyDocumentRevoked and :1303 notifyDocumentShared have NO await and NO .catch (rejection = unhandled rejection). notifyDocumentVerified / notifyRightsTransferred have no caller in src.
- NOTIFICATION today vs after (unreadable value only):
  - :56 (service-call catch): today String(err) throws BEFORE `await sendSmtpFallback`, so the SMTP fallback is never attempted: the email is DROPPED and sendNotification rejects. After: reason logged, SMTP fallback IS attempted (sent if SMTP configured), resolves. An ordinary Error already gets the after state (warn then fallback). So the one new outcome is "email now sent via SMTP fallback", the same as an ordinary Error; nothing is retried.
  - :110 (SMTP-fallback catch): today sendSmtpFallback rejects (through sendNotification to the helper's caller; a non-OK-response path inside the try would route into the :56 catch and throw again, no second send either way). After: warn logged, resolves, as an ordinary Error. Nothing sent, retried or dropped differently.
- BEHAVIOUR CHANGE for the PR: for an unreadable thrown value only, (1) service-call failure: constant `unreadable thrown value` is logged and the SMTP fallback now runs instead of the notification being dropped with a rejection; (2) SMTP failure: logged and resolved instead of rejecting. Ordinary Errors and strings log exactly as before (`Error: <message>` via String(err)); pinned by C1-C4. Refs KS-1868, does not close it.
- Tier: 3 (log-only on the text; the fallback running for the hostile value matches the ordinary path). Raise seat: state that a notification email can now go out in a case where it was dropped.

## O68-P2 metering.ts GET /usage catch :129
- hold_ready: `golden: BYTE-IDENTICAL; touched=2 product_plus=7 product_minus=1 red=2/5 green=5/5 suite=1999->2004 strict=True`. Model 42.7 s (round 174 s), 13155+1815 tokens. One hunk (`@@ -126,7 +126,13 @@`).
- Test (new): src/__tests__/ks1868-metering-usage-catch-p2-unreadable-throw.test.ts: R1/R2 (500 constant body `Failed to read usage` + logged constant reason), C1 ordinary Error, C2 string, C3 success 200. Real router on a loopback listener; chargeEvents.getUsageSummary, auth, gatewayProvenance, logger replaced. Red state would be a hung request (reported as NO ANSWER after 1.5 s).
- Billing input: the route is READ-ONLY. getUsageSummary (chargeEvents.ts :261) is one SELECT with COUNT/SUM/GROUP BY over charge_events; metering.ts has one catch and no write. The catch runs after the read failed, so no recorded usage count changes either way.
- Today vs after: unreadable value: today catch throws, nothing logged, partner gets NO answer; after: constant reason logged, constant 500 `Failed to read usage` (what an ordinary Error gets). Persisted: nothing.
- BEHAVIOUR CHANGE for the PR: unreadable thrown value on the usage read now logs a constant reason and answers the existing constant 500 instead of hanging. No change for ordinary Errors or strings.
- Tier: 3.

## O68-P3 retentionScheduler.ts runEnforcement catch :51
- hold_ready: `golden: BYTE-IDENTICAL; touched=2 product_plus=7 product_minus=1 red=2/5 green=5/5 suite=1999->2004 strict=True`. Model 36.5 s (round 156 s), 11365+1559 tokens. One hunk (`@@ -48,6 +48,12 @@`).
- Test (new): src/__tests__/ks1868-retention-scheduler-run-enforcement-p3-unreadable-throw.test.ts: R1/R2, C1 ordinary Error, C2 string, C3 nothing-to-process success. Starts the scheduler with RETENTION_STARTUP_DELAY_MS=10 under jest fake timers (setImmediate/nextTick stay real so a pending rejection surfaces in its own cell), mocks gdprService.enforceRetention and logger. Ascii only (the source log line with an em dash is matched with expect.stringContaining).
- Retention/GDPR check (the SKIP criterion): the catch does NOT decide whether a retention action runs, retries or is skipped. enforceRetention() has finished or failed before the catch; the catch is the last statement, returns nothing, sets no flag, reschedules nothing. The next run comes from setInterval (:28) at a fixed interval and `timer` is assigned before any run completes (lines 26-29), regardless of outcome. Deletes/anonymisations inside enforceRetention are untouched. So which retention actions run, and when, is identical before and after for every value: no SKIP. This is derived from reading the file; the interval independence is NOT pinned by a cell (UNMEASURED).
- Callers: only the setTimeout first run (:27) and setInterval (:28); neither awaits or catches. Today unreadable value: nothing logged by the scheduler, runEnforcement rejects as an unhandled rejection; src/index.ts `process.on('unhandledRejection')` reads `reason instanceof Error` unguarded itself, so for a revoked Proxy it throws too and the uncaughtException handler exits the process for a restart (reading only, not measured). After: constant reason logged, run ends (what an ordinary Error gets). Persisted: nothing.
- BEHAVIOUR CHANGE for the PR: unreadable thrown value from enforceRetention is now logged as a constant reason by the scheduler, instead of becoming an unhandled rejection. No change to scheduling or to what is enforced. Ordinary Errors and strings unchanged.
- Tier: 2-3 (data-retention job, but log-only and ordinary-Error-equivalent). Mention to Kam only if he wants GDPR files kept out of KS-1868 batches regardless.

## Raise-seat notes
strict=True for all. Three files are disjoint, any order or one PR. P1 hunks 54 lines apart. Test names: `RED ks1868 R1..R4`, `control ks1868 C1..C4` (P1), `R1/R2`, `C1..C3` (P2, P3). Refs KS-1868 only. P3's cells use fake timers: if the raise seat runs the file with other timer-faking tests in the same worker, nothing is shared (afterEach restores real timers and clears RETENTION_STARTUP_DELAY_MS). The untouched unhandledRejection / uncaughtException handler reads in src/index.ts :75-86 are an additional unguarded site, not briefed (outside assignment, process-level handler).

## Round log (spark/done.md rows, done_rows.txt; queued_*.txt)
- Dry run rc 3 BUSY (round.lock held by o67), so controls were queued: P1 control 09:11:26, P2 and P3 controls 09:12:39.
- P1: CONTROL-PASS 09:13:50 (122 s); model queued 09:14:20; PASS 7/7 09:29:59 (264 s). Held ~09:31.
- P2: CONTROL-PASS 09:23:38 (96 s); model queued 09:23:59; PASS 7/7 09:42:46 (174 s). Held ~09:44.
- P3: CONTROL-PASS 09:25:33 (114 s); model queued 09:26:03; PASS 7/7 09:45:23 (156 s). Held ~09:46.
- Lint rc 0 x3 (lint_p*.out). Counter: 1 original brief each, 0 rebriefs. Model rounds waited behind other operators' control lines (queue order); the Spark was not idle at any poll.

## UNMEASURED
Whole-suite CI with the patches beyond the harness (suite 1999 -> 2007/2004/2004); eslint; whether an unreadable value is reachable in production; the retention interval-independence as a pinned test; the unhandledRejection handler exit behaviour (read only); real SMTP / real notification service; real Postgres.
Evidence: this folder (tip_*, prscan_*, open_prs*.json, recon*.out, lint_*, dry_p1.*, hold_p*_run.out, held_files.txt, done_rows.txt, queued_*.txt, tip_diff_*.out, gen/mk68.py tp1-3.py t68_p1-3.ts.txt prscan68.py hold68.sh).
