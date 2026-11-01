# Spark operator 40, 2026-11-01 (Secuura only). Filed by the operator.
Two KS-1868-class sites found in NON-security service code (analytics), both PASS 7/7 on the ORIGINAL briefs (no rebrief), byte-identical to the goldens, HELD. Nothing raised, pushed, merged; no board touch; no git write verbs in !CODING (the only write verb, `git fetch`, ran in the cache clone spark/cache/src under WEDNESDAY).

## Method
- Read O39 report whole; copied gen/mk39.py to gen/mk40.py (new tip, PR counts, new gen/tasks40.py); prscan.py from O35; round.sh --dry-run, --control, real round (thinking OFF, one request at a time, nice 10), hold_ready.py --brief --model-tag spark-dsv4flash (golden arg = the -control run dir, so it compared: BYTE-IDENTICAL).
- Tunnel: tunnel.sh check = UP (200). Load average ~9-10 during the work.
- Tip: fetched develop into the cache clone = 3d036184d37f0ad2a46fff4e9e6e80de03441b93 (matches Wednesday's ls-remote); round.sh confirmed the base.

## Partition evidence
- Open PRs re-run with prscan.py: 22 PRs, 237 file entries (open_prs.json). Positive control: services/auth appears in 7 file entries.
- packages/shared: only package.json in PRs 649/635/575. services/analytics and services/demo-service: only package.json (+ analytics package-lock) in 575/649/948/635; NO src file of either is in any open PR. Both chosen files are absent from all 237 entries.
- Not checked: other seats' unpushed local work beyond PRs; the S9 brief was not re-read (neither file is tenant-context.ts / tenant-pool-manager.ts, tenant-provisioning, originate, anchoring, vc-issuer).

## Screening
`git grep -c "instanceof Error"` at the tip over Blockchain/Dev (minus tests/scripts), minus services/originate|anchoring|auth|tenant-provisioning|vc-issuer and paths matching oauth, mfa, token, credential, session, kyc, identity, tenant-context, tenant-pool-manager: 61 files (cand list in scratch).
- Already held O34-O39 (excluded): presentations.ts, credentialRepo, metricsCollector, analyticsService, mcp hash.ts, demo scenario.ts, gracefulShutdown.ts, response-cache.ts, audit-logger.ts.
- Skipped: mcp-server tools info/register/verify (error text returned to the MCP client), api-gateway health.ts / routes (client-visible), billing, nft-certificate, transfer, security, governance (jest), referral, m365, frontend.
- demo-service resetService.ts:71/112 (rethrows with the message; viable but the throw goes to the reset route, left for later). exportService.ts:160 stores the message on the export record returned to clients: skipped.
- Chosen: the two startup loaders in services/analytics, the identical shape of the already-held O36/O37 loadFromDb fixes.

## Sites
- P1: services/analytics/src/services/exportService.ts:297, catch in `ExportService.loadFromDb`. `err instanceof Error ? err.message : String(err)` is read inside the logger.warn argument; a revoked Proxy or a throwing message getter makes the catch throw, so no WARN is logged and loadFromDb() rejects. Fix: inner try into `reason`, fallback 'unreadable thrown value'. Log-only. New test ks1868-export-service-load-unreadable-throw.test.ts (C1 control, R1 revoked Proxy, R2 throwing getter).
- P2: services/analytics/src/services/scheduledJobs.ts:151, catch in `loadScheduledJobsFromDb`. Same shape, same fix, same cells. New test ks1868-scheduled-jobs-load-unreadable-throw.test.ts.

## Results
- Dry-run rc 0 both. Control: CONTROL-PASS golden byte-identical (P1 70 s, P2 35 s), first time.
- Real P1: PASS 7/7, 63 s round, 28.8 s model, 12183+972 tok, think=0. Real P2: PASS 7/7, 63 s, 27.5 s model, 13471+982 tok, think=0. cmp out.md.checker/patch.diff vs golden.diff: identical (my cmp, both).
- checker.out (read by me): A2 strict apply; A4 red-first 2 failed / 3 run, controls green, assertion reds; A5 3/3 green after; A6 whole services/analytics suite 44 -> 47, no new red; A7 tsc rc 0 (baseline rc 0).
- Diff read at source (via the brief/golden): each product hunk +7/-1; log text unchanged.

## Held
- /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/READY_KS-1868-O40-P1_spark-dsv4flash_BRIEFED-CODEPATCH2-EXPORTSERVICE-LOADFROMDB-PASS-7of7_2026-11-01.diff.md
- /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/READY_KS-1868-O40-P2_spark-dsv4flash_BRIEFED-CODEPATCH2-SCHEDULEDJOBS-LOADFROMDB-PASS-7of7_2026-11-01.diff.md
- (I renamed both from hold_ready's doubled KS-1868-KS-1868 prefix to the O39 shape.) Run dirs: local-model/runs/spark_secuura_2026-11-01_ks_1868_o40_p{1,2}_* (+ -control). Briefs: night/briefs/ks_1868_o40_p{1,2}_*. Rows appended to spark/done.md; screen line to spark/queue.md.
- hold_ready stamps "by Wednesday"; the source reads were the operator's. Wednesday should re-read. With O34-O39, 11 of 253 sites held; refs KS-1868, does not close it. Neither site is security-surface, so no tier-1 gate is implied by path (Wednesday's call).

## UNMEASURED
- eslint on the new files; real service boot of analytics; the other ~242 sites; live-lane overlap beyond open PRs; goldens are operator-authored (proved by --control only); whether such a thrown value ever occurs; the S9 brief.
- Left same-shape candidates: exportService dbSaveExport:56, scheduledJobs dbSaveAlertRule:59 and dbSaveAlert:85.
- Next re-screen trigger: R2b #1884 or S9 #1885 merge.
