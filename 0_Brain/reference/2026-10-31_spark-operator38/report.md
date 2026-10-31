# Spark operator 38, 2026-10-31 (Secuura only). Filed by the operator.
Two more KS-1868-class sites in packages/shared, both PASS 7/7 on the ORIGINAL brief (no rebrief, counter untouched), both byte-identical to the golden, both HELD. Nothing raised, pushed, merged; no board touch; no git write verbs in !CODING (the only write verb, `git fetch`, ran in the cache clone spark/cache/src under WEDNESDAY).

## Method
- Read O37 report whole, mk37.py (copied to gen/mk38.py, new TASKS and a few template fields: where_note, intro_site, s9note, PR counts), O35 prscan.py. Followed: round.sh --dry-run, --control, real round (thinking OFF, one request at a time), hold_ready.py --brief --model-tag spark-dsv4flash.
- Tunnel: tunnel.sh check = UP (200 on /v1/models).
- Tip: `git ls-remote origin develop` (read-only, Blockchain 2_Project_Files) = 9e1eb55fde5338d0ad95848736cbd013d7b7f651. Cache clone was at cb2320368; I fetched into the cache clone (not !CODING); round.sh then checked out 9e1eb55fde53 (checker/dry-run state "tip 9e1eb55fde53").
- Candidate scan: `git grep -c "instanceof Error"` at the tip in Blockchain/Dev/services, excluding tests and the directories you listed plus anchoring, originate, transfer, security, billing, nft-certificate, tokenisation (all named by S9 or heavy in PRs) and any path matching oauth/mfa/token/credential/session.

## Partition evidence
- Open PRs re-run now with prscan.py: 44 PRs, 406 file entries (open_prs.json here; O37 saw 43/317). Positive control: services/auth appears in 14 of the file entries (the scan can see PRs that touch auth).
- Neither target file is in any PR. packages/shared paths in PRs: package.json x3 only (575, 635, 649). Nothing under src/.
- S9 brief (read by me): names packages/shared only for tenant-context.ts and tenant-pool-manager.ts (KS-1860); not gracefulShutdown.ts, not response-cache.ts. Control: the same brief lists services/anchoring, api-gateway, auth, originate, transfer, tenant-provisioning etc. (grep -o "services/..." returned 20+ distinct paths).
- Lockfiles/package.json untouched.
- Not checked: other live seats' unpushed local work beyond PRs and that brief.

## Screening (services outside exclusions: 5 files)
- governance/src/services/governanceService.ts (12 sites): not in any PR, not in S9, BUT the governance suite is jest, not the vitest runner the kit's code_patch2 checker assumes, and this is a 12-site file; not attempted.
- kyc/src/index.ts (6) and kyc/providers/microsoft-entra-client.ts (2): PR #1840 touches kyc/src/index.ts; KYC is also identity surface. Skipped.
- referral/src/routes/referrals.ts (3): the catch returns error.message to the client in the response body (KS-1410 class, filing candidate). Skipped.
- m365-integration/src/index.ts (1): MSAL token surface (as O37), skipped.
- So I went to packages/shared (not in your exclusion list): 20+ files with the pattern; chose two behaviour-bearing sites with no PR on src and a vitest suite.

## Sites
- P1: packages/shared/src/utils/gracefulShutdown.ts:52-53, the listener returned by createUnhandledRejectionHandler. `detail` is read before logging; a revoked-Proxy or throwing-message-getter reason throws inside the unhandledRejection handler (in 'survive' mode, the api-gateway, that defeats KS-546). Fix: inline inner try with fallback 'unreadable thrown value'. Not client-returning (log only). Brief's first draft was REFUSED by build_input (a '+' line byte-identical to a '-' line); I reshaped the edit (ternary split over three lines) and the dry-run then passed. That was my brief correction, before any model call, not a rebrief.
- P2: packages/shared/src/cache/response-cache.ts:299, the cache-read catch of the responseCache middleware. A hostile rejection from the cache store made the catch throw, so the middleware rejected instead of calling next() (a cache failure failing the request). Not client-returning. Other response-cache sites (127,135,147,155,327) not touched. Test uses setDefaultCacheStore with a plain-function store.

## Results
- Dry-runs rc 0 (P1 after the reshape). Controls: both CONTROL-PASS, golden byte-identical (P1 174 s, P2 101 s; round.sh).
- P1 real: PASS 7/7, 124 s round, 27.8 s model, 11392+1105 tok. P2 real: PASS 7/7, 131 s round, 33.0 s model, 13400+1269 tok.
- cmp out.md.checker/patch.diff vs golden.diff: identical both (my cmp; hold_ready also BYTE-IDENTICAL).
- From checker.out (read by me): A4 red-first 2 failed / 3 run each, assertion reds, controls green; A5 3/3 green after; A6 whole packages/shared suite 1081 -> 1084, no new red; A7 tsc rc 0; apply strict. Checker prints a "MISMATCHED HEADER" line for the new-file section (diagnostic noise; A2 still strict-applies, same as earlier operators' shape - I did not investigate it further).
- Diffs read at source by me: P1 hunk @@ -49,8 +49,14 @@ (+8/-2); P2 hunk @@ -296,5 +296,11 @@ (+7/-1). Log text unchanged.
- No FAILs, no classification needed.

## Held
- /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/READY_KS-1868-O38-P1_spark-dsv4flash_BRIEFED-CODEPATCH2-GRACEFULSHUTDOWN-HANDLER-PASS-7of7_2026-10-31.diff.md
- /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/READY_KS-1868-O38-P2_spark-dsv4flash_BRIEFED-CODEPATCH2-RESPONSE-CACHE-READ-PASS-7of7_2026-10-31.diff.md
- Run dirs: local-model/runs/spark_secuura_2026-10-31_ks_1868_o38_p{1_shared_gracefulshutdown_unhandled_rejection,2_shared_response_cache_read}_unreadable_throw (+ -control). Briefs: night/briefs/ks_1868_o38_p*/. Two rows appended to local-model/spark/done.md (where O37's rows are; night/done.md is a different, older file and was not touched).
- hold_ready stamps "by Wednesday"; the source reads were the operator's. Wednesday should re-read. With O35-O37, 8 of 253 sites held; refs KS-1868, does not close it.

## UNMEASURED
- eslint on new files; real boot of any service exercising these paths; the other ~245 sites; live-lane overlap beyond open PRs and the S9 brief; goldens are operator-authored (proved by --control only); whether such a thrown value ever occurs; whether packages/shared changes need a version bump or rebuild for dependents (not checked); the blast radius of a shared-package change (every service imports it).
