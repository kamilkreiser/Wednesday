# Spark operator 53, 2026-11-02: KS-1868 mcp-server http-server.ts route catches (3 held, 0 failed)

*Written by Wednesday from operator 53's final message (its Write was refused as a subagent report file). Verdict lines, hold lines and held names re-read by Wednesday from the .out files and `ls night` at 07:0x.*

## BLUF
All three passes PASS 15/15 cells on the ORIGINAL brief (no rebrief); golden BYTE-IDENTICAL; control PASS after one fix to the operator's own test helper (no model call involved). Held 3, failed 0, skipped 0 (beyond :76 /hash, left out as KS-1928's class). Tip 03977e89a343ad7362760e4fb0270602fb6da5ce at start and end. Open-PR scan start/end: 19 PRs / 108 files, none lists http-server.ts or any mcp-server path; planted control `services/originate` = 6 entries both times.

## Held (ls night | grep O53)
READY_KS-1868-KS-1868-O53-P1_spark-dsv4flash_BRIEFED-CODEPATCH2-MCP-HTTP-ROUTE-CATCHES-REGISTER-REGISTER-BATCH-VERIFY-PASS-7of7_2026-11-02.diff.md
READY_KS-1868-KS-1868-O53-P2_spark-dsv4flash_BRIEFED-CODEPATCH2-MCP-HTTP-ROUTE-CATCHES-VERIFY-BATCH-DOCUMENTS-WORKFLOW-PASS-7of7_2026-11-02.diff.md
READY_KS-1868-KS-1868-O53-P3_spark-dsv4flash_BRIEFED-CODEPATCH2-MCP-HTTP-ROUTE-CATCHES-CONNECTOR-POLICY-GENERATE-PACKAGE-PASS-7of7_2026-11-02.diff.md

## Fix and passes
Delete the `const message = ... instanceof Error ...` line; log `describeThrown(err)`. 3 hunks + one new test (15 cells: R1 revoked Proxy, R2 getter-throwing Error, R3 thrown string by kind, controls C1/C2, x3 routes) per pass.
hold_ready (all three): `golden: BYTE-IDENTICAL; touched=2 product_plus=3 product_minus=6 red=9/15 green=15/15 suite=86->101 strict=True`
- P1 (/register :91 registerDocument, /register-batch outer :128, /verify :153 verifyDocument): round 104 s, model 64.485 s, 18455+2744 tok
- P2 (/verify-batch outer :191, GET /documents :205, GET /workflow/:id :216): round 173 s, model 64.262 s, 18438+2727
- P3 (GET /connector :227, GET /policy :238, POST /generate-package :292): round 113 s, model 64.14 s, 18418+2711. /generate-package still answers 500 only if `!res.headersSent` (untouched).
Batch outer catches only see `req.body`, the checks, slice or `res.json`.

## BEHAVIOUR CHANGE (each PR states it)
1. Unreadable thrown value: today the catch throws, the request gets NO response and Node sees an unhandled rejection (process-fatal on Node >= 15); after, the constant reason is logged and the route answers its existing constant 500.
2. Log text for non-Error throws: a thrown string is logged as `non-Error string thrown`, a thrown object logs its field NAMES not `[object Object]`. An Error's message is logged unchanged.
3. No response body changes (/verify keeps `{verified:false,error:...}`).

## Raise-seat notes
strict=True on all three (plain git apply). Hunks disjoint within and across passes; any order; NOT run together by the pipeline. Tests: `services/mcp-server/src/__tests__/ks1868-mcp-http-route-catches-p{1,2,3}-unreadable-throw.test.ts`. Ref pin: the ks1901 test; top-level names renamed (ks, mkRes, invoke, errLog, spy53, CONST500) to avoid the splice collision. No open PR lists the file; no KS-1868-titled PR open at the scan.

## Round log
- Control round 1 FAILED A4 on all three (06:55:59, 06:56:35, 06:57:10): R1/R2 failed by the handler rejecting, not by assertion (operator's `invoke` helper). Helper changed to swallow the rejection, re-linted; no model call, counter unspent.
- Lint rc 0 x3; dry runs OK.
- Control round 2 PASS 06:58:05, 06:58:45, 06:59:24 (~39 s each).
- Model rounds PASS 07:01:13, 07:04:06, 07:05:59 (file mtimes of rnd1_*.out).
- Hand-run, not queued (Wednesday's queue message arrived after the rounds started); done.md rows added by Wednesday 07:0x from the .out files.

## UNMEASURED
The three applied together as a whole suite; eslint; a real Express 4 end to end (no-response / unhandled-rejection read from code; cells prove the handler level); the real gateway; live lanes beyond open PRs; reachability of an unreadable value in production.

Evidence: this folder (tip, scan, lint, dry, ctl, rnd, hold outputs, held_files.txt, gen/ prscan53.py mk53.py t53_p*.ts.txt).
