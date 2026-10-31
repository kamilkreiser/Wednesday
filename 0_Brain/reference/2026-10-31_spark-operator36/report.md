# Spark operator 36, 2026-10-31 (Secuura only). Filed by the operator.
Two more KS-1868-class sites, both PASS 7/7 on the ORIGINAL brief (no rebrief, counter untouched), both byte-identical to the golden, both HELD. Nothing raised, pushed, merged; no board touch; no git write verbs in !CODING (one attempted fetch into the cache clone was refused by the hook and not retried; the cache was already at the tip).

## Method
- Read O35 report whole. Tunnel UP. Tip: git ls-remote origin develop = cb2320368ae42fa793d81776fdd7fc8404ce312d (unchanged since O35); cache clone (spark/cache/src) already at that sha.
- Candidate scan: git grep "instanceof Error" in Blockchain/Dev/services at the tip, excluding tests and auth/oauth/mfa/token/credential/vc-issuer; then single-site files checked against the PR scan and the S9 brief.
- Generator: gen/mk36.py in this folder (reuses spark/gen/mk.py rd/udiff; prose follows the O35 P2 brief). Per task: round.sh --dry-run (rc 0), --control (golden through the checker), real round, thinking OFF, one request at a time.

## Partition evidence
- Open PRs re-run now: 43 PRs, 317 file entries (same count as O35; open_prs.json here). analytics paths in them: package.json x3 and package-lock.json x1 only; mcp-server paths: ks1410 tests x2 and src/http-server.ts (a different file; hash.ts untouched). Neither target file is in any PR. Positive control: services/auth appears in 20 lines.
- S9 security brief: 0 hits for analytics, mcp-server, metricsCollector, hash.ts (control: 27 lines contain 'services/'; it names anchoring, api-gateway, auth, enforcement, originate, security, tenant-provisioning, tokenisation, transfer). Both targets open.
- Not checked: other live seats' unpushed local work beyond PRs and that brief.

## Sites chosen (different services; no auth/credential surface; not vc-issuer; a runnable suite beside each)
- P1: analytics metricsCollector.ts:492, MetricsCollector.loadFromDb catch (boot hydration WARN; same shape as O35). Suite: analytics vitest (38 tests). Sibling analyticsService.ts:568 deliberately left out.
- P2: mcp-server tools/hash.ts:34, secuura_hash_document handler catch (variant: not a WARN but an isError result; fix is the same inline inner try with fallback 'unreadable thrown value'). Test shape from ks1541 (duck-typed server, mocked module). Suite: mcp-server vitest (30 tests). Other mcp-server sites not touched.

## Results
- P1: control PASS first time (522 s, slow analytics suite). Real round PASS 7/7, 85 s round, 28.1 s model, 14029+992 tokens. cmp patch.diff vs golden.diff identical. Diff read at source: hunk @@ -488,8 +488,14, +7/-1, WARN text and em dash unchanged, error: reason; new test 3 cells. Reds R1/R2 fail by AssertionError (expected [] to have a length of 1), C1 green; suite 38 -> 41, 0 new reds; tsc rc 0.
- P2: control PASS first time (79 s). Real round PASS 7/7, 118 s round, 25.6 s model, 9734+1070 tokens. cmp identical. Hunk @@ -31,7 +31,12, +6/-1; reds R1/R2 fail by AssertionError (expected undefined to be true) not by throw, C1 green; suite 30 -> 33, 0 new reds; tsc rc 0.
- No FAILs, so no classification needed. Failed controls: none. The first --control attempt of the batch used a nonexistent 'timeout' binary (shell error, no run); rerun normally.

## Held
- /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/READY_KS-1868-KS-1868-O36-P1_spark-dsv4flash_BRIEFED-CODEPATCH2-METRICSCOLLECTOR-PASS-7of7_2026-10-31.diff.md
- /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/READY_KS-1868-KS-1868-O36-P2_spark-dsv4flash_BRIEFED-CODEPATCH2-HASH-TOOL-PASS-7of7_2026-10-31.diff.md
- Run dirs: 2_Project_Files/local-model/runs/spark_secuura_2026-10-31_ks_1868_o36_p{1_analytics_metricscollector_loadfromdb,2_mcp_server_hash_tool}_unreadable_throw. Briefs: night/briefs/ks_1868_o36_p1_*/ and ks_1868_o36_p2_*/. done.md: 2 rows appended.
- hold_ready.py printed "golden: not compared" for both; I ran cmp myself (identical, both).

## Caveat on the HELD stamp
hold_ready.py stamps "by Wednesday" in each READY; the source reads (diffs, cmp, checker artefacts) were the operator's, not Wednesday's. Wednesday should re-read before relying on it. Both READYs close 2 more of the 253 sites; refs KS-1868, does not close it. (With O35, 4 of 253 held.)

## UNMEASURED
- eslint on the new files; real boot of analytics / the MCP server exercising these paths; the other sites (analyticsService.ts:568 and the rest); tsc beyond the checker's A7; live-lane overlap beyond open PRs and the S9 brief; the goldens are operator-authored (proved by --control, not independent); whether a real thrown value of this kind ever occurs.
