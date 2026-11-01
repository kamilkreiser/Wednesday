# O66: KS-1868 corrected remaining list at develop 03977e89a343ad7362760e4fb0270602fb6da5ce (tip_start.out; origin/develop of the gate89 clone = same)

Method: scan.py (scan.out) re-reads every ternary/String(x) site of O57's s_ternary.out + s_string.out from `git show origin/develop:...` and marks a site guarded when `unreadable thrown value` or `describeThrown` sits within 5 lines; then each remaining file was READ (ctx1/2/3.out: line plus 4 lines above, 3 below). "Held" = a held READY_* exists from operators 58-65 (not yet merged, so the tip still shows the sites). Excluded by Wednesday: billing.ts, nft.routes.ts, governanceService.ts, kyc, tokenisation, auth issuerCert*, gdprService, in-flight files, mcp-server tools/*.
Result of the guard check: only analytics (scheduledJobs :61/:158, exportService, analyticsService, metricsCollector), nft cardano/provider, vc-issuer (credentialRepo, presentations) were already guarded; scan.out lines "guarded_near".

| file | real unguarded sites (clean = log-only/const response, no pre-check) | area | risk |
|---|---|---|---|
| originate/src/routes/verification.ts | 8 (759, 880, 917, 1017, 1306, 1438, 1467, 1489): all log-only; 4 route catches answer constant 500, 4 are lineage-attach catches that log and fall through | public verification (read) | low; 880/917 return an empty fallback, 1017/1306 continue to res.json |
| originate/src/routes/signatories.ts | 6 clean (181, 236, 284, 357, 415, 464); :132 SKIP (an error.code check precedes it, throws first) | signatory authorisation admin routes | medium (revoke/update writes, but catch is log + constant 500) |
| originate/src/routes/thirdPartyVerifiers.ts | 6 clean (143, 193, 240, 279, 365, 397); :109 SKIP (code check precedes) | third-party verifier admin | medium (:193 approve issues an API key; log-only catch) |
| originate/src/routes/anchors.ts | 5 (52 and 91 helpers, 203, 323, 418 routes) | anchoring routes | medium (anchor create/submit; catch is log + constant 500; :52 throws a constant Error after, :91 rethrows) |
| originate/src/routes/documents.ts | 17 not read for shape | document lifecycle | high (large, not screened) |
| originate/src/routes/certifications.ts | 15 not read for shape | certification lifecycle | high (large; O65 touches certificationRepo only) |
| originate/src/routes/verificationV2.ts | 2 clean (441, 477) | public verification v2 (read) | low |
| originate/src/routes/metering.ts | 1 clean (129) | usage read | low (usage/billing-adjacent, read only) |
| originate/src/services/retentionScheduler.ts | 1 clean (51) | retention job | low-medium (retention enforcement; log-only) |
| originate/src/services/reanchorInFlight.ts | 2 (193 returns fetchError into decideInFlight; 229 local `message` helper) | re-anchor | HIGH: value feeds a decision, not a log; SKIP |
| originate/src/services/ownCreateClient.ts | 1 (88) result string returned to caller | own-create client | medium: message returned, changes a returned value |
| originate/src/utils/notificationClient.ts | 2 (56, 110) String(err) in warn logs | notifications | low; external comms path but only the log line changes |
| originate/src/services/chargeEvents.ts | 1 (126) | charge events (money) | EXCLUDE money |
| originate/src/services/anchorStateSync.ts | 1 (600) log-only | anchor state | low-medium |
| originate/src/utils/lifecyclePayloadCodec.ts | 1 (58) | decrypt of lifecycle payload | EXCLUDE (key material) |
| originate/src/repositories/shareRepo.ts, lifecycleEventRepo.ts | 1 each (140, 82): value is used for msg.includes(...) control flow | repos | SKIP: control flow, not a log |
| originate/src/repositories/documentRepo.ts, certificationRepo.ts | held O65 (verify-db-ready catch) only; other 5 each remain | repos | not scanned further; in flight area |
| originate/src/index.ts | 1 (76) unhandledRejection handler, feeds trackError | process handler | SKIP (exit path) |
| api-gateway/src/middleware/rateLimitEnforce.ts | 3 (51, 277, 302) log-only | rate limiter | medium: :51 has a different shape (`err ? String(err) : undefined`) |
| api-gateway/src/middleware/{audit,security}.ts, routes/{platform,verification,batch,notifications,audit-export}.ts, index.ts | 1 each, not read | gateway | unread; admin.ts is held by O58 |
| nft-certificate/src/services/blockchain-verifier.service.ts | 2 (69, 109) | on-chain verify | low-medium; :109 returns status 'error' |
| nft-certificate/src/utils/mintError.ts | 1 (37) message feeds classification | mint errors | SKIP (money-adjacent) |
| auth/src/routes/health.ts | 2 (41, 61): `message: String(error)` RETURNED in health JSON | health | low, but changes a returned value |
| shared/src/security/redis-security-store.ts (15), shared/src/cache/* (connection-pool 5, cache-middleware 3, compression 1, redis-client 1) | not in O57's table (shared lib); not read | shared lib | unread; shared is imported by every service, so blast radius is wide |
| analytics/src/routes/analytics.ts, tenant-provisioning, api-gateway admin.ts, nft ipfs, originate systemErrors/errorTracking | held by O58-O63; nothing left | | |
| mcp-server/src/tools/*, billing.ts, nft.routes.ts, governance, kyc, tokenisation, issuerCert*, gdprService | excluded | | |

Remaining real supply (non-excluded, not held, clean shape): verification.ts 8, signatories 6, thirdPartyVerifiers 6, anchors 5 (about 3 passes of 3 hunks each for verification.ts+signatories+thirdPartyVerifiers = 20 sites, ~7 passes), verificationV2 2, metering 1, retentionScheduler 1, notificationClient 2.
