# Spark operator 60, 2026-11-02: KS-1868 analytics routes/analytics.ts three clean catches (1 held, 0 failed, 0 rebriefs)

## BLUF
Held: O60-P1 (GET /realtime :245, GET /exports/:id :350, GET /exports :372). Control CONTROL-PASS first time, model PASS 7/7 first time on the original brief, golden BYTE-IDENTICAL, strict=True. Skipped (not done): the other nine catches of the file (:55 overview, :88 certification, :121 verification, :154 governance, :187 revenue, :220 user metrics, :289 activity, :322 POST exports, :405 POST reports): each opens with `instanceof z.ZodError`, which throws first on a revoked Proxy, so a message-line fix is half a fix (operator 57 screen.md). Tip 03977e89a343ad7362760e4fb0270602fb6da5ce at start (tip_start.out) and end (tip_end.out). Open-PR scan start 20 PRs/113 files, end 21 PRs/119 files (new: #1910 mcp-server); no PR lists analytics src (ANALYTICS-HIT 0 in prscan_start.out and prscan_end.out; analytics only as package.json/package-lock in 575/649/948/1360); planted control services/originate = 6 entries both times.

## Held (ls night | grep O60)
READY_KS-1868-KS-1868-O60-P1_spark-dsv4flash_BRIEFED-CODEPATCH2-ANALYTICS-ROUTES-REALTIME-EXPORT-BY-ID-EXPORT-LIST-CATCHES-PASS-7of7-PASS-7of7_2026-11-02.diff.md

## O60-P1
- hold_ready: `golden: BYTE-IDENTICAL; touched=2 product_plus=21 product_minus=3 red=6/12 green=12/12 suite=56->68 strict=True`. Model 54.1 s (round 98 s). 3 hunks, at old lines ~242, ~353, ~381 (gaps 100+ and 15+ lines; disjoint by > 3).
- Fix: above each `logger.error(...)` line, `let reason: string; try { reason = <same expression> } catch { reason = 'unreadable thrown value' }`, and the log line logs `{ error: reason }`. Same inline shape and variable name as the merged analytics guards (exportService.ts :60/:306, analyticsService.ts :571, metricsCollector.ts :495, scheduledJobs.ts :63/:160). No helper. Test (new): src/__tests__/ks1868-analytics-routes-catches-p1-unreadable-throw.test.ts, 12 cells: 3 routes x (R1 revoked Proxy, R2 getter-throws Error, C1 ordinary Error, C2 string). Reused the merged O42-pair shape (ks1868-export-service-db-save-unreadable-throw.test.ts, pinned as ref).
- Callers: router mounted at /api/analytics (analytics src/index.ts :78), reached over HTTP via api-gateway routes/proxy.ts :1219; no in-process caller. All three routes are read-only GETs.
- Per site, today vs after (identical for all three): response today for an unreadable thrown value = the catch throws before logging and before the 500, the async handler rejects, Express 4 does not catch it, the request gets no response (proxy timeout) and Node sees an unhandled rejection; after = logs `{ error: 'unreadable thrown value' }` and answers the existing constant 500 (`INTERNAL_ERROR`, texts 'Failed to fetch real-time metrics' / 'Failed to fetch export' / 'Failed to list exports'). An ordinary Error already gets exactly the after-state (control C1: its own message logged, constant 500, message not echoed). Persisted state: none (no writes). No site skipped for producing a new outcome.
- BEHAVIOUR CHANGE (PR text): unreadable thrown value from the service call now logs a constant reason and answers the same constant 500 an ordinary Error gets, instead of an unanswered request plus unhandled rejection. No change in body, status or log text for ordinary Errors or strings. Refs KS-1868, does not close it.
- Recommended tier: 3 (read-only analytics routes, log-only catches, constant 500, no money, no keys, no auth).

## Raise-seat notes
strict=True (plain git apply). Test cells: `RED ks1868 R1/R2` and `control ks1868 C1/C2` per route (describe title 'KS-1868 analytics $route catch reads the thrown value safely'). First route-level test for routes/analytics.ts in the repo (git grep: nothing imports it; no text-reading pin like ks1410). Left in file, deliberate: the nine Zod-preceded catches; guarding the Zod check too needs a design call and a pin check (their 400 branch returns `details: error.errors`).

## Round log (done.md rows, done_rows.txt)
- Brief lint rc 0, dry run rc 0 (input 39160 B) at 07:52; control + model lines appended 07:52:34 (both together, before Wednesday's correction to append the model line only after CONTROL-PASS; the control passed, so no round was wasted).
- 07:58:49 CONTROL-PASS (61 s, BYTE-IDENTICAL); 08:00:28 model PASS 7/7 (98 s round, 54.1 s model, 14765+2338 tokens, BYTE-IDENTICAL). Queued behind operator 58's lines (its control FAILed 07:54:46).
- hold_ready ~08:01, rc 0.

## UNMEASURED
Whole-suite CI with the patch; eslint; real Express 4 (cells prove the handler level); whether an unreadable value is reachable in production; behaviour of the nine unfixed Zod-preceded catches (read only).
Evidence: this folder (tip_*, prscan_*, open_prs*.json, lint_p1, dry_p1, hold_p1, done_rows.txt, analytics.routes.tip.ts, gen/mk60.py t60_p1.ts.txt hold60.sh).
