# Spark operator 61, 2026-11-02: KS-1868 analytics routes/analytics.ts, the nine Zod-preceded catches (3 passes HELD, 0 failed, 0 rebriefs)

## BLUF
HELD: O61-P1 (overview, certifications, verifications), O61-P2 (governance, revenue, users), O61-P3 (activity, POST exports, POST reports). Every control CONTROL-PASS first time, every model round PASS 7/7 first time on the original brief, golden BYTE-IDENTICAL, strict=True for all three. Nothing skipped: the guard shape below does not change what an ordinary ZodError or Error returns. Tip 03977e89a343ad7362760e4fb0270602fb6da5ce at start (tip_start.out) and end (tip_end.out). Open-PR scan start 21 PRs/119 files, end 22 PRs/125 files (new #1911 auth); ANALYTICS-HIT 0 at both (analytics only as package.json/package-lock in 575/649/948/1360); planted control services/originate = 6 entries both times.

## THE SHAPE (differs from O56-P2, and why)
O56-P2 put an inner try around isZod/infra flags. Here that shape fails twice: (a) the brief builder refuses a `+` line equal to a `-` line, (b) the blank line between the 400 branch and the `logger.error` line would be a blank context line in every hunk (builder refuses blank context). So the hunk is the smallest one that leaves every line after the catch head untouched:

    } catch (thrown) {
      let error: unknown = thrown;
      try {
        if (!(thrown instanceof z.ZodError)) {
          String(thrown instanceof Error ? thrown.message : thrown);
        }
      } catch {
        error = new Error('unreadable thrown value');
      }
      if (error instanceof z.ZodError) {   // unchanged from here down: 400 + details: error.errors, logger.error line, constant 500

The probe makes the same two reads the old code makes, in the same order, and for a ZodError it makes only the `instanceof` (the old code never read a ZodError's message, so a ZodError is never newly sent to the 500 path). If a read throws, `error` becomes an ordinary Error and the untouched code below runs for it.
1. Ordinary ZodError: `error === thrown`, the unchanged branch runs, so the 400 body (`details: error.errors`) is identical by construction (cell C1 asserts the exact body with `details: zerr.errors` and that nothing is logged).
2. Ordinary Error / string: identical path, same log text, same constant 500 (C2).
3. Only an unreadable value changes: from "catch throws, no response (unhandled rejection in Express 4)" to logging `{ error: 'unreadable thrown value' }` and the constant 500 each route's ordinary Error already gets (R1 revoked Proxy, R2 Error with a throwing `message` getter).
Existing tests that pin the 400 `details`: NONE at the tip. `git grep` of services/analytics: only the two ks1364 tests (`ks1364-analytics-exports-body-required`, `ks1364-analytics-reports-body-required`) mention the route, and they test the schemas / OpenAPI document, never import routes/analytics.ts (pins_grep.out, pins_grep2.out; the only importer is src/index.ts:11). So my C1 cells are the first pin of `details: error.errors`; there was nothing to keep green except the baseline suite (56 -> 68 per pass).

## Held (ls night | grep O61; held_files.txt)
- READY_KS-1868-KS-1868-O61-P1_spark-dsv4flash_BRIEFED-CODEPATCH2-BRIEFED-CODEPATCH2-ANALYTICS-ZOD-PRECHECK-CATCHES-OVERVIEW-CERTIFICATIONS-VERIFICATIONS-PASS-7of7-PASS-7of7_2026-11-02.diff.md
- READY_KS-1868-KS-1868-O61-P2_spark-dsv4flash_BRIEFED-CODEPATCH2-BRIEFED-CODEPATCH2-ANALYTICS-ZOD-PRECHECK-CATCHES-GOVERNANCE-REVENUE-USERS-PASS-7of7-PASS-7of7_2026-11-02.diff.md
- READY_KS-1868-KS-1868-O61-P3_spark-dsv4flash_BRIEFED-CODEPATCH2-BRIEFED-CODEPATCH2-ANALYTICS-ZOD-PRECHECK-CATCHES-ACTIVITY-EXPORTS-REPORTS-PASS-7of7-PASS-7of7_2026-11-02.diff.md
(The doubled BRIEFED-CODEPATCH2 / PASS-7of7 in the names comes from hold_ready adding its own tags to my label, as in O60.)

## Per pass
hold_ready line, all three verbatim: `golden: BYTE-IDENTICAL; touched=2 product_plus=27 product_minus=3 red=6/12 green=12/12 suite=56->68 strict=True`.
- O61-P1: model 60.4 s, round 103 s, 15063+2473 tok. Hunks old @@ -43,7 / -77,7 / -110,7 (catches at :46, :80, :113; GET /overview, /certifications, /verifications).
- O61-P2: model 56.9 s, round 100 s, 15062+2473 tok. Hunks old @@ -143,7 / -176,7 / -209,7 (GET /governance, /revenue, /users).
- O61-P3: model 57.0 s, round 101 s, 15078+2482 tok. Hunks old @@ -277,7 / -311,7 / -394,7 (GET /activity, POST /exports, POST /reports).
Hunk distances: inside a pass 26+ lines; P1/P2/P3 to each other 25+ lines; to O60-P1 (hunks ~242-248, ~347-356, ~369-384 around :245/:350/:372): nearest is P2 end :216 to :242 = 26 lines, P3 :283 to :242 and :317 to :347 = 30 lines. All > 3, so all four patches can sit in one PR (each adds its own test file: ks1868-analytics-routes-zod-catches-p{1,2,3}-unreadable-throw.test.ts, 12 cells each = 3 routes x R1, R2, C1, C2; shape from the merged ks1868-export-service-db-save-unreadable-throw ref).
- Callers: router mounted at /api/analytics (analytics src/index.ts :78), reached over HTTP via api-gateway proxy; no in-process caller. Routes: seven read-only GETs, plus POST /exports (creates an export) and POST /reports (generates a report); the catches write nothing, and an unreadable rejection of the service call leaves whatever the service call did exactly as it is today (same as an ordinary Error).
- Today vs after, every site: unreadable value = catch throws before logging and before any response, the async handler rejects, Express 4 does not catch it, request gets no answer and Node sees an unhandled rejection; after = logs constant reason, answers the route's existing constant 500 (INTERNAL_ERROR + the route's fixed text). An ordinary Error already gets the after-state. No site newly produces an outcome an ordinary Error does not.
- BEHAVIOUR CHANGE (PR text): an unreadable thrown value in these nine analytics route catches (revoked Proxy; Error with a throwing message getter) now logs the constant `unreadable thrown value` and answers the same constant 500 an ordinary Error gets, instead of an unanswered request plus unhandled rejection. Ordinary ZodError (400, details), ordinary Error and string behave exactly as before. Refs KS-1868, does not close it.
- Recommended tier: 3 (read-mostly analytics routes, catch-only change, no money, keys or auth).

## Raise-seat notes
strict=True (plain git apply). Cells: `RED ks1868 R1/R2 <route>` and `control ks1868 C1/C2 <route>` (describe title 'KS-1868 analytics $route catch reads the thrown value safely'). The probe reads twice (probe, then the old code reads again): a getter that throws only on its second read is not covered (synthetic). Left unhandled on purpose: a ZodError subclass whose own `errors` getter throws in the 400 branch (as today). Request schemas are pass-through mocks in the tests, so the real schemas are not exercised.

## Round log (done_rows.txt)
- 08:02 tip + open-PR scan; 08:07 P1 lint rc 0 + dry run rc 0 (40179 B); 08:07:57 P1 control queued; P2/P3 dry runs rc 0, their controls queued (queued_p23_control.txt). Model lines queued only after each control's CONTROL-PASS: P1 (queued_p1_model.txt), P2+P3 (queued_p23_model.txt).
- Controls: P1 CONTROL-PASS 08:10:04 (58 s), P2 08:10:47 (42 s), P3 08:11:31 (43 s). Models: P1 PASS 08:13:15, P2 PASS 08:14:56, P3 PASS 08:16:38. hold_ready rc 0 for all.
- Two failed BUILDER dry runs before the shape settled (no queue, no Spark time): the first diff aligned badly (difflib; I switched the golden to `git diff --patience`), then builder REFUSED `+` lines equal to `-` lines, then REFUSED blank context; the catch-head probe above resolved both.

## UNMEASURED
Whole-suite CI with the patches; eslint (a bare `String(...)` call statement in the probe is not lint-checked outside the checker); real Express 4; whether an unreadable value is reachable in production; behaviour with the real request schemas; lanes beyond open PRs.
Evidence: this folder (tip_*, prscan_*, open_prs*.json, lint_p*, dry_p*, hold_p* via hold61 output, done_rows.txt, held_files.txt, pins_grep*.out, analytics.routes.tip.ts, gen/mk61.py t61_p{1,2,3}.ts.txt hold61.sh prscan61.py mk_p*.out).
