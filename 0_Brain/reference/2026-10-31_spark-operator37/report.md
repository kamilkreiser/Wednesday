# Spark operator 37, 2026-10-31 (Secuura only). Filed by the operator.
Two more KS-1868-class sites, both PASS 7/7 on the ORIGINAL brief (no rebrief), both byte-identical to the golden, both HELD. Nothing raised, pushed, merged; no board touch; no git write verbs in !CODING (read-only git grep on the cache clone only).

## Method
- Read O36 report whole; reused its method, gen/mk36.py (copied to gen/mk37.py with new TASKS), prscan.py (from O35), round.sh dry-run, control, real round (thinking off, one request at a time), hold_ready.py --brief.
- Tunnel UP. Tip: ls-remote develop = cb2320368ae42fa793d81776fdd7fc8404ce312d, unchanged; cache clone at the same sha.
- Candidates: git grep "instanceof Error" in Blockchain/Dev/services at the tip, excluding tests and auth/oauth/mfa/token/credential/vc-issuer; then PR scan and S9 check.

## Partition evidence
- Open PRs re-run now: 43 PRs, 317 file entries (open_prs.json here). analytics paths in them: package.json + package-lock.json only; demo-service: package.json only. Neither target file is in any PR. Positive control: the same data lists many anchoring/transfer/nft-certificate paths and services/auth (as in O35/O36).
- S9 security brief: 0 hits for analyticsService, analytics, demo-service, referral, m365, nft-certificate (control in O35/O36: 27 'services/' lines). Both targets open.
- Not checked: other live seats' unpushed local work beyond PRs and that brief.

## Sites
- P1: analytics analyticsService.ts:568, AnalyticsService.loadFromDb catch (logger.warn only; fallback is the mock data already held). Sibling of the held metricsCollector pass, a different file. Suite: analytics vitest (38 -> 41).
- P2: demo-service routes/scenario.ts:113, GET /scenario/context catch (logs, answers the generic 500 'Internal server error'; the thrown text is NOT returned to the client). Not a persona/auth surface. Variant: the non-Error branch is 'Unknown error' (kept), inner try falls back to 'unreadable thrown value'. Test drives the real handler taken from scenarioRouter.stack with a request whose query getter throws the value. Suite: demo-service vitest (86 -> 89).

## Results
- Controls: both PASS first time (P1 33 s, P2 82 s). Dry-runs rc 0.
- P1 real: PASS 7/7, 64 s round, 29.8 s model, 16183+980 tok. P2 real: PASS 7/7, 67 s round, 31.5 s model, 10975+1366 tok.
- cmp out.md.checker/patch.diff vs golden.diff: identical, both (run by me; hold_ready also reported BYTE-IDENTICAL).
- Diffs read at source: P1 hunk @@ -564,8 +564,14 (+7/-1), WARN text and em dash unchanged. P2 hunk @@ -110,7 +110,12 (+6/-1), log and 500 response untouched. Reds R1/R2 fail by AssertionError (P1 'expected [] to have a length of 1'), C1 green; 0 new reds; tsc rc 0 both.
- No FAILs, no classification needed.

## Held
- /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/READY_KS-1868-KS-1868-O37-P1_spark-dsv4flash_BRIEFED-CODEPATCH2-ANALYTICSSERVICE-PASS-7of7_2026-10-31.diff.md
- /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/READY_KS-1868-KS-1868-O37-P2_spark-dsv4flash_BRIEFED-CODEPATCH2-SCENARIO-ROUTE-PASS-7of7_2026-10-31.diff.md
- Run dirs: local-model/runs/spark_secuura_2026-10-31_ks_1868_o37_p{1_analytics_analyticsservice_loadfromdb,2_demo_service_scenario_context}_unreadable_throw. Briefs: night/briefs/ks_1868_o37_p*/. done.md: 2 rows. (My first ROWID typo doubled the KS-1868 prefix in the filenames and one in-file mention; I renamed/sed-fixed both, grep for the doubled prefix is 0.)
- Source reads (diffs, cmp, checker artefacts) were the operator's, not Wednesday's; hold_ready stamps "by Wednesday". Wednesday should re-read before relying on it. With O35/O36, 6 of 253 sites held; refs KS-1868, does not close it.

## Client-returning sites (KS-1410 disclosure filing candidates, NOT touched)
Heuristic scan (catch reads instanceof Error, response body carries the variable); first-hand checked: platform.ts:1091, http-server.ts:62/135, tenant-provisioning:385, reset.ts:64-69.
- Blockchain/Dev/services/api-gateway/src/routes/platform.ts:1089-1091 (details.detail = msg)
- Blockchain/Dev/services/mcp-server/src/http-server.ts:61-62, 76-77, 110-111, 134-135 (error: message), 169-170, 182-183, 192-193, 202-203, 212-213, 265-267 (message in body; line numbers are the catch/response pairs)
- Blockchain/Dev/services/tenant-provisioning/src/index.ts:384-385, 423-424, 453-454, 514-515, 575-576, 595-596
- Blockchain/Dev/services/demo-service/src/routes/reset.ts:64-69 (message and failedStep returned; demo reset)
The scan's other matches (persona.ts, state.ts, billing webhooks.ts) return a constant string, so they are not client-returning (matched on the literal 'message:' key). Scan is a regex heuristic: other shapes (e.g. helper-built responses) may be missed. m365-integration index.ts:1594 logs only, but is an MSAL token-exchange surface, so skipped.

## UNMEASURED
- eslint on the new files; real boot of analytics / demo-service exercising these paths; the other ~246 sites; tsc beyond the checker's A7; live-lane overlap beyond open PRs and the S9 brief; goldens are operator-authored (proved by --control, not independent); whether a real thrown value of this kind ever occurs; completeness of the client-returning scan.
