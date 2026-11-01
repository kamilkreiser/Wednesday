# Spark operator 70: KS-1868 originate routes/verification.ts

## BLUF
- HELD 2 passes, 4 sites (all 4 route-level catches that answer a constant 500): O70-P1 (POST /verify :1438, POST /hash :1467, GET /status/:documentId :1489), O70-P2 (POST /verify-file :759). Both PASS 7/7 on the ORIGINAL brief (0 rebriefs), golden BYTE-IDENTICAL, strict=True. Controls CONTROL-PASS first time.
- SKIPPED 4 sites (strict verdict rule): :880, :917 (lineage helpers), :1017, :1306 (lineage-attach catches). Reasons below.
- Tip: develop b887480394cc67764922b0aa123027c344241ed7 at start (tip_start.out) and at end (tip_end.out). Every number below is from a saved output in this folder.
- Open PRs: start 22 PRs/127 files, end 23 PRs/131 files (prscan_*.out); no PR lists originate routes/verification.ts (grep count 0 in open_prs_start/end.json); originate only as package.json (575/949/1726) and integration tests (1790/1792/1794); planted control services/auth 7 entries. End scan shows new KS-1868 PRs 1912-1915, none on originate.

## Held files (held_files.txt; note the label doubled by my hold script argument, cosmetic)
- READY_KS-1868-KS-1868-O70-P1_spark-dsv4flash_BRIEFED-CODEPATCH2-BRIEFED-CODEPATCH2-O70-P1-PASS-7of7_2026-11-02-PASS-7of7_2026-11-02.diff.md
- READY_KS-1868-KS-1868-O70-P2_spark-dsv4flash_BRIEFED-CODEPATCH2-BRIEFED-CODEPATCH2-O70-P2-PASS-7of7_2026-11-02-PASS-7of7_2026-11-02.diff.md

## Per pass
P1 hold_ready: `golden: BYTE-IDENTICAL; touched=2 product_plus=21 product_minus=3 red=6/12 green=12/12 suite=1999->2011 strict=True`
P2 hold_ready: `golden: BYTE-IDENTICAL; touched=2 product_plus=7 product_minus=1 red=2/4 green=4/4 suite=1999->2003 strict=True`
Hunks: 1438 / 1467 / 1489 (29 and 22 lines apart) and 759 (far from all). Fix = the inline `let reason` guard merged in routes/certifications.ts :1086-1094 (also used by O66/O69); no helper.
Callers: verificationRouter mounted at src/index.ts:279 under /api/verification, public verification endpoints via the gateway.
Tests (new, one file per pass): names `RED ks1868 R1/R2 <route>` and `control ks1868 C1/C2 <route>`; describe `KS-1868 $route catch reads the thrown value safely`. Throw injection: a one-shot request hook, an accessor on `req.db` (POST /verify, POST /verify-file) or a one-shot throwing `res.json` (POST /hash, GET /status). No unused constants (TS6133 lesson); ref pin ks1133 (as O66), no clashing file-scope decl.

BEHAVIOUR CHANGE text for the PR (both): for an unreadable thrown value only, today the handler rejects, nothing is logged and the request gets no answer (gateway timeout); after, the constant reason `unreadable thrown value` is logged and the constant 500 `{success:false,error:{code:'INTERNAL_ERROR',message}}` is answered, exactly what an ordinary Error already gets. Ordinary Error and string: status, body and log unchanged (controls C1, C2). The 500 body has no `verified`/verdict field. Persisted state: none written by the catches, before or after (the three P1 routes persist nothing; for /verify-file any registry write happens in the try before the catch, identically for any thrown value). Recommended tier 1 for both (public verification file).

Raise-seat notes: strict=True both; one PR is possible (hunks > 3 lines apart; two new test files). Whole-suite counts are the checker's.

## Skipped sites (read at the tip, verification.ts.tip.ts)
- :880 walkLineageForDoc and :917 walkNewerVersionsForDoc catches: they RETURN a lineage result (empty fallback), not a constant error response. Today an unreadable value makes the helper reject to its caller; after, it returns an empty lineage: a lineage result changes. Also at :1011-1012 today the throw skips the forward walk, after it would run, so newerVersions could newly appear in the body.
- :1017 (by-id verify) and :1306 (hash verify) lineage-attach catches: log, then fall through to `res.json` carrying a verdict (`verified:false` at :1019; `base` at :1306 which is the verified response). Today an unreadable value escapes to the outer catch (:1437) and answers 500; after, the request answers 200 with the verification body. That turns an error into a verdict-bearing answer an unreadable value does not get today: SKIP.
- Not in my list, untouched: `?.message` warn sites (:345, :468, :557, :699, :1144, :1238, :1432).

## Round log (done_rows.txt, queue times in queued_*.txt)
- P1 control queued 10:2x (queued_control_p1.txt) -> CONTROL-PASS 10:24:54 (128 s). P1 model queued 10:25:07 -> PASS 10:29:44 (257 s round, 76.4 s model).
- P2 control queued 10:25:07 -> CONTROL-PASS 10:32:08 (143 s). P2 model queued 10:32:17 -> PASS 10:36:10 (202 s, 64.65 s model).
- Lint rc 0 x2; dry runs rc 0 (P1 110463 B, P2 107444 B). Counter: 1 original brief each, 0 rebriefs.

## UNMEASURED
Whole-suite CI with the patches beyond the checker (suite 1999 -> 2011/2003); tsc/eslint only as the checker ran them; real Postgres; whether an unreadable value is reachable in production; the 4 skipped sites' behaviour (read only, not run); the POST /verify outer-catch reachability via a real failing call (the test injects through `req.db`). Evidence: this folder (tip_*, prscan_*, open_prs_*.json, lint_*, dry_*, hold_run_p*.txt, done_rows.txt, held_files.txt, gen/mk70.py t70_p*.ts.txt hold70.sh prscan70.py).
