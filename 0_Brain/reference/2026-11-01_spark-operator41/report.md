# Spark operator 41, 2026-11-01 (Secuura only). Filed by the operator.
BLUF: two NON-security, log-only KS-1868 sites were screened and briefed (nft-certificate cardano/provider.ts:66, demo-service routes/state.ts:81), both lint rc 0, but BOTH ROUNDS WERE BLOCKED at the dry-run by the builder's open-PR gate: KS-1868 now has four OPEN attached PRs (#1887/#1888/#1889/#1890, the raised O34-O40 patches), so night/build_input.sh refuses with "attached to OPEN pull request(s) ... a lane has it". I did not work around it (no placeholder ticket, no supersedes= pin: these are new sites, not those PRs' fix round). No control, no real round, no model call, nothing held. The Spark is still idle. Wednesday must decide how a further KS-1868 site is admitted (see end).

## Method
- Read O40 report and gen whole; copied gen to gen/mk41.py + gen/tasks41.py (tip, PR counts, new tasks; the brief prose is O40's). prscan.py from O35 re-run. Tunnel: tunnel.sh check = UP (200). Load average 7.00 at 15:07 (nice 10 used for round.sh).
- Tip: git fetch origin develop into the cache clone spark/cache/src gave FETCH_HEAD b1fb543640e7a439a9344d1d96d5a62862edfcf5 (matches Wednesday's ls-remote). The only write verb run anywhere was that fetch.

## Partition evidence
- prscan.out: "23 PRs 128 files" (open_prs.json); positive control: services/auth in 7 file entries (partition.out).
- partition.out: PRs touching my areas: 1890 demo-service src/index.ts (+test, 2 doc fragments); 1889 analytics exportService.ts/scheduledJobs.ts (+2 tests); 1888 shared audit-logger.ts (+test); 1887 shared response-cache.ts, gracefulShutdown.ts (+2 tests); originate: 3 test files (1790/1792/1794) + package.json; package.json (and analytics package-lock.json) only in PRs 575, 635, 649, 948, 949, 1360, 1726. PR 1870 is no longer open (merged, shown by the builder's output in dry_p1.out; the scenario test is in the tip tree).
- Chosen files: services/nft-certificate/src/cardano/provider.ts and services/demo-service/src/routes/state.ts. grep of open_prs.json for "nft-certificate" gives only package.json and package-lock.json; no demo-service/src/routes file appears. Neither chosen file nor its test path is in any open PR.
- Not checked: other seats' unpushed local work beyond PRs; the S9 brief was not re-read (neither file is tenant-context / tenant-pool-manager / tenant-provisioning / vc-issuer).

## Screening
- `git grep -c "instanceof Error"` at b1fb543640e7 over Blockchain/Dev/**/*.ts minus tests/scripts/node_modules: 98 files (screen_all.out). Minus services/auth|tenant-provisioning|vc-issuer, and paths matching oauth, mfa, token, credential, session, kyc, identity, tenant-context, tenant-pool-manager, frontend: 81 files (screen_cand.out).
- Excluded: every file in an open PR (response-cache, audit-logger, gracefulShutdown, exportService, scheduledJobs, demo-service index.ts); already held O34-O40 (analyticsService, metricsCollector, hash.ts, scenario.ts, presentations, credentialRepo, ...); client-visible catches (routes, health, mcp tools, identus-client errorMessage, transaction.ts verified-error, service-client healthCheck, ipfs.service which rethrows a generic error but sits in a route chain, nft-certificate cardano/index.ts rethrow, wallet.ts rethrow).
- originate/anchoring screened for log-only startup/background catches: retentionScheduler.ts:51 (scheduled GDPR enforcement, log-only), errorTrackingService.ts:65 and :135 (log-only; :65 sits under the explicit "never throw from error tracking" comment), chargeEvents.ts:126 (startup DB verify, payments-adjacent, throws anyway), anchorStateSync.ts:600 (anchoring, log-only). NONE selected: non-originate sites existed, so these are left as candidates, and all are in payments/anchoring/GDPR territory for Wednesday to tier. anchorOverwriteGuard.ts:602 is a name check, not a message read: not a site.
- Also seen, not chosen: security/src/index.ts:293/:400 (credential rotation log, security surface), m365 index.ts:1594 (auth-adjacent), demo-service authClient.ts:62 (login path; returns the message), state.ts:110 and persona.ts:77 (log-only, 500 generic; same shape, left), analytics routes (client-visible).

## Sites
- P1: Blockchain/Dev/services/nft-certificate/src/cardano/provider.ts:66, catch in `fetchProtocolParams`. `err instanceof Error ? err.message : String(err)` is read inside the logger.error argument; a hostile rejection from Blockfrost makes the catch throw, so no log and the function rejects instead of its documented `return null`. Log-only: the message is not returned (the function returns ProtocolParams | null). Fix: inner try into `reason`, fallback 'unreadable thrown value'. New test ks1868-provider-fetch-protocol-params-unreadable-throw.test.ts (C1, R1 revoked Proxy, R2 throwing getter; Blockfrost and logger mocked). This service mints Cardano NFTs; it is not a payments service, but it is a chain service, so the gate tier is Wednesday's call.
- P2: Blockchain/Dev/services/demo-service/src/routes/state.ts:81, catch in the `GET /state` handler. Same shape; the message goes only to logger.error and the handler then answers res.json(inMemoryState) (the 500 body elsewhere in the file is generic). Fix: inner try into `message`, fallback 'unreadable thrown value'. New test ks1868-state-get-unreadable-throw.test.ts (shape copied from the merged ks1868-scenario-context test; ioredis and logger mocked; the handler is run from stateRouter.stack).
- Briefs: night/briefs/ks_1868_o41_p1_nftcertificate_provider_fetchprotocolparams_unreadable_throw/ and night/briefs/ks_1868_o41_p2_demoservice_state_get_unreadable_throw/ (KS-1868.md, spark.pins, golden.diff, written by gen/mk41.py).

## Results
- brief_lint.py: rc 0 for both (lint_p1.out, lint_p2.out).
- round.sh --dry-run: rc 2 for both (dry_p1.out, dry_p2.out): "REFUSED — builder rc 2: build_input: REFUSED KS-1868 — attached to OPEN pull request(s) ['#1890', '#1889', '#1888', '#1887'] — a lane has it (merged/closed PRs do not refuse)". dry_p1.out also lists PRs 1872, 1870, 1867, 1864 as merged.
- NOT RUN: --control, the real round, hold_ready.py. There is therefore NO model output, NO checker result and NO held patch; the goldens are operator-authored and untested (no CONTROL-PASS).

## Held paths
- None.

## UNMEASURED
- Whether the goldens apply and the tests go red-then-green (control not run); eslint/tsc on the new files; whether the builder's later gates (stale-brief, input size) would pass; live-lane overlap beyond open PRs; whether such a thrown value ever occurs; the S9 brief; the other ~240 sites.
- Left same-shape candidates: state.ts:110, persona.ts:77, errorTrackingService.ts:65/:135, retentionScheduler.ts:51.

## Decision for Wednesday
The builder refuses KS-1868 while any attached PR is open, and the raised O34-O40 PRs are attached to it. Options: (a) rule that these briefs may use `supersedes=1887,1888,1889,1890` (the pin exists, but is documented for a PR's own fix round or replacement, so it is a stretch and I did not use it); (b) file a per-site or follow-up ticket (a new KS id) and re-pin the briefs; (c) wait until the open PRs merge. Once decided I (or the next operator) change only the ref/pin and run --dry-run, --control and the real round; the briefs and goldens are ready.

## UNBLOCKED RUN (appended after Wednesday's 15:4x message: PRs 1887-1890 merged)
- Tip: git fetch origin develop into the cache clone gave FETCH_HEAD 85c56a3d1eb92c8399dcfd3d6ee2a717cf356428 (fetch2.out / fetch2.err). Matches Wednesday's ls-remote.
- Partition re-scan (prscan2.out): "19 PRs 108 files"; positive control services/auth in 7 entries; PRs 1887-1890 not in the open list. No open PR touches nft-certificate/src or demo-service/src (zero rows printed). Read-verb diff b1fb543640e7..85c56a3d1eb9 over services/demo-service and services/nft-certificate lists only demo-service src/index.ts and src/__tests__/ks1868-boot-gate-unreadable-throw.test.ts; provider.ts and routes/state.ts are unchanged. KS-1868's Linear attachments are read by the builder; the dry-run no longer refuses (dry2_p1.out, dry2_p2.out).
- Re-pin: mk41.py tip and PR counts changed (19 PRs / 108 files), briefs regenerated; golden.diff for both is byte-identical to the pre-pin copy (cmp, golden_before_p1.diff / golden_before_p2.diff).
- Dry-run rc 0 both (input built at 85c56a3d1eb9, 25972 B P1 / 23633 B P2). Control: CONTROL-PASS golden byte-identical (control_p1.out 73 s, control_p2.out 56 s), first time.
- Real P1 (round_p1.out): PASS 7/7, 68 s round, 27.11 s model, 11574+1076 tok, think=0. Real P2 (round_p2.out): PASS 7/7, 68 s round, 31.361 s model, 10666+1365 tok, think=0. cmp of each out.md.checker/patch.diff vs its -control run: identical.
- checker.out (read by me): A2 strict apply; A4 red-first 2 failed / 3 run, controls green, assertion reds; A5 3/3 green after; A6 whole-suite no new red; A7 tsc rc 0 (baseline rc 0); A2a anchor ok. hold_ready (hold_p1.out, hold_p2.out): P1 golden BYTE-IDENTICAL, product +7/-1, red 2/3, green 3/3, suite 134->137, strict; P2 golden BYTE-IDENTICAL, product +6/-1, red 2/3, green 3/3, suite 91->94, strict.
- Held (renamed from hold_ready's doubled prefix):
  - /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/READY_KS-1868-O41-P1_spark-dsv4flash_BRIEFED-CODEPATCH2-NFT-PROVIDER-FETCHPROTOCOLPARAMS-PASS-7of7_2026-11-01.diff.md
  - /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/READY_KS-1868-O41-P2_spark-dsv4flash_BRIEFED-CODEPATCH2-DEMO-STATE-GET-PASS-7of7_2026-11-01.diff.md
- hold_ready stamps "by Wednesday"; the source reads were the operator's. Wednesday should re-read. P1 is a Cardano-minting (chain) service, not payments; tier is Wednesday's call. The earlier "Results"/"Held paths: none" lines above describe the blocked first attempt and are superseded by this section. Still UNMEASURED: eslint on the new files, real service boot, the other sites, live-lane overlap beyond open PRs.
