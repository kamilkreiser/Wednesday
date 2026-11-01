# Spark operator 64, 2026-11-02: KS-1868 analytics services (1 held, 0 failed, 0 rebriefs, 3 of 4 passes SKIPPED: already guarded)

## BLUF
Held: O64-P1 (scheduledJobs.ts dbSaveAlert catch, line 91). Control CONTROL-PASS first time (08:43:04), model PASS 7/7 first time on the original brief (08:48:55), golden BYTE-IDENTICAL, strict=True.
Skipped O64-P2 exportService, O64-P3 analyticsService, O64-P4 metricsCollector, and the other two scheduledJobs sites: at the tip every one of those lines (scheduledJobs :61/:158, exportService :58/:304, analyticsService :569, metricsCollector :493) is INSIDE the already-merged inline guard (`let reason: string; try { reason = err instanceof Error ? err.message : String(err) } catch { reason = 'unreadable thrown value' }`), see catch_scan.out and the *.tip.ts files. Operator 57's screen matched the line inside the guard. The only unguarded read in the four files is scheduledJobs.ts :91.
Also found, NOT briefed: exportService.ts :166 `exportResult.error = error instanceof Error ? error.message : 'Unknown error'` (different shape, no String(); a revoked Proxy throws at `instanceof`, so `exportResult.status='failed'` is already set in memory but dbSaveExport never runs and the persisted export stays at its earlier status). Fixing it would persist a failed status that today is not persisted for an unreadable value; an ordinary non-Error already persists failed + 'Unknown error', but it touches export records and is outside the assignment: SKIP, flagged for a decision.
Tip 03977e89a343ad7362760e4fb0270602fb6da5ce at start (tip_start.out) and end (tip_end.out). Open-PR scan start 22 PRs/125 files, end 22 PRs/125 files; no PR lists analytics src (analytics only as package.json/package-lock in 575/649/948/1360); planted control services/originate = 6 entries both times (prscan_start.out, prscan_end.out).

## Held (ls night | grep O64)
READY_KS-1868-KS-1868-O64-P1_spark-dsv4flash_BRIEFED-CODEPATCH2-O64-P1-PASS-7of7_2026-11-02.diff.md

## O64-P1 scheduledJobs.ts dbSaveAlert (:90-92)
- hold_ready: `golden: BYTE-IDENTICAL; touched=2 product_plus=7 product_minus=1 red=2/4 green=4/4 suite=56->60 strict=True`. Model 36.96 s (round 128 s), 15045+1432 tokens. ONE hunk (@@ -88,6 +88,12 @@).
- Fix: inline `reason` guard above the `logger.info('DB save alert failed', ...)` line, which logs `{ error: reason }`. Same shape as dbSaveAlertRule (:58-64) and loadScheduledJobsFromDb (:155-161) in the same file. No helper.
- Test (new): src/__tests__/ks1868-scheduled-jobs-save-alert-unreadable-throw.test.ts, 4 cells: R1 revoked Proxy, R2 getter-throws Error (RED), C1 ordinary Error, C2 string (control). Real ScheduledJobs class, mocked ../db and logger; one rule added and evaluated to raise a real alert, then acknowledgeAlert. Ref shape: ks1868-scheduled-jobs-save-alert-rule-unreadable-throw.test.ts.
- Callers: dbSaveAlert is module-private with ONE caller, ScheduledJobs.acknowledgeAlert (:486) `dbSaveAlert(alert).catch(() => {})`; no analytics route calls acknowledgeAlert (git grep); cron callbacks never reach it.
- Today vs after: unreadable value today = the catch throws, dbSaveAlert rejects, the empty `.catch` swallows it: the scheduler loop and cron jobs are NOT crashed, acknowledgeAlert still returns true, the in-memory acknowledgement stands; only the INFO line is lost. After = INFO `{ error: 'unreadable thrown value' }` logged. An ordinary Error already gets the after-state (logs its message, resolves). Persisted: the INSERT failed in both, nothing written either way. No new outcome, so in scope.
- BEHAVIOUR CHANGE (PR text): an unreadable thrown value from the alert INSERT now logs a constant reason at INFO as an ordinary Error already does, instead of losing the log line to a swallowed rejection. No change for ordinary Errors or strings. Refs KS-1868, does not close it.
- Recommended tier: 3 (log-only catch, caller swallows, no money/keys/auth).

## Raise-seat notes
strict=True. Test names: `control ks1868 C1/C2`, `RED ks1868 R1/R2` (describe 'KS-1868 dbSaveAlert reads the thrown value safely'). Single hunk, so no distance concern. Module-level memActiveAlerts persists across cells, so each cell uses a fresh rule id (seq counter).

## Round log (done_rows.txt)
- Lint rc 0; dry run rc 3 BUSY (round.lock held by O63-P2 control), so the control was queued: control line appended 08:33:04 (queued behind operator 63 lines). CONTROL-PASS row 08:43:04 (419 s round), model line appended 08:43:10, model PASS 7/7 row 08:48:55 (128 s round). hold_ready rc 0 ~08:50.
- The Spark was busy on arrival (not idle), so no model time was lost to me; queue wait for the control was ~10 min.

## UNMEASURED
Whole-suite CI with the patch; eslint; whether an unreadable value is reachable in production; behaviour of exportService.ts :166 under a fix (not briefed).
Evidence: this folder (tip_*, prscan_*, open_prs*.json, catch_scan.out, *.tip.ts, lint_p1, dry_p1, hold_run.out, done_rows.txt, gen/mk64.py t64_p1.ts.txt hold64.sh).
