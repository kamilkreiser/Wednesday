# O57 screen at develop 03977e89a343ad7362760e4fb0270602fb6da5ce (ls-remote 07:2x AEDT, unchanged at start)

Method: `git grep -nE "instanceof Error \? X.message : String\(" origin/develop -- Blockchain/Dev/services` (src only, __tests__ excluded; s_ternary.out, 253 lines) plus `String\((err|error|e)\)` (s_string.out, 292 lines). Positive control: mcp-server/src/http-server.ts (known-open KS-1868 site, 11 hits) and nft-certificate minting.service.ts (merged guard `unreadable thrown value` at :94 present). Open-PR scan (prscan_start.out): 19 PRs / 108 files, planted control services/originate = 6 entries; no listed PR touches any file below except package.json/package-lock.json.

Guard helper: no shared helper exists at the tip except mcp-server http-server.ts `describeThrown` (local). House pattern = inline `let reason: string; try {..} catch { reason = 'unreadable thrown value' }` (analytics, nft-certificate, billing).

| file | ternary sites (lines) | String(x) hits | note |
|---|---|---|---|
| billing/src/routes/billing.ts | 17 (55, 327, 361, 383, 412, 449, 500, 544, 577, 600, 624, 645, 675, 698) | 17 |  |
| originate/src/routes/documents.ts | 17 (232, 364, 1092, 1237, 1285, 1366, 1451, 1860, 2507, 2726, 2933, 3027, 3166, 3196) | 17 |  |
| originate/src/routes/certifications.ts | 16 (70, 407, 585, 659, 751, 787, 820, 879, 1010, 1088, 1169, 1235, 1334, 1495) | 12 |  |
| originate/src/services/gdprService.ts | 16 (227, 242, 314, 377, 499, 503, 647, 917, 978, 988, 998, 1008, 1018, 1028) | 15 |  |
| nft-certificate/src/routes/nft.routes.ts | 15 (116, 175, 215, 260, 291, 319, 340, 386, 424, 460, 520, 548, 573, 691) | 15 |  |
| analytics/src/routes/analytics.ts | 12 (55, 88, 121, 154, 187, 220, 245, 289, 322, 350, 372, 405) | 12 |  |
| governance/src/services/governanceService.ts | 12 (167, 187, 205, 221, 263, 277, 287, 327, 362, 390, 474, 1056) | 12 |  |
| mcp-server/src/http-server.ts | 11 (37, 76, 91, 128, 153, 191, 205, 216, 227, 238, 292) | 11 | EXCLUDED (in flight) |
| tenant-provisioning/src/index.ts | 9 (342, 384, 424, 482, 544, 603, 622, 629, 651) | 7 |  |
| originate/src/routes/verification.ts | 8 (759, 880, 917, 1017, 1306, 1438, 1467, 1489) | 6 |  |
| nft-certificate/src/services/minting.service.ts | 7 (92, 137, 177, 518, 604, 688, 798) | 7 | EXCLUDED (in flight) |
| auth/src/routes/issuerCerts.ts | 6 (319, 366, 419, 511, 676, 829) | 6 |  |
| auth/src/services/issuerCertSweep.ts | 6 (66, 83, 95, 113, 155, 163) | 6 |  |
| kyc/src/index.ts | 6 (194, 210, 231, 255, 277, 353) | 6 |  |
| originate/src/repositories/certificationRepo.ts | 6 (60, 176, 200, 308, 354, 378) | 6 |  |
| originate/src/repositories/documentRepo.ts | 6 (141, 260, 292, 498, 512, 691) | 5 |  |
| tokenisation/src/index.ts | 6 (76, 108, 266, 357, 381, 396) | 6 |  |
| auth/src/services/issuerCert.ts | 5 (114, 199, 219, 349, 363) | 5 |  |
| originate/src/routes/anchors.ts | 5 (52, 91, 203, 323, 418) | 5 |  |
| analytics/src/services/scheduledJobs.ts | 3 (61, 91, 158) | 3 |  |
| api-gateway/src/routes/admin.ts | 3 (1274, 1296, 1320) | 3 |  |
| auth/src/routes/auth.ts | 3 (306, 612, 880) | 3 | EXCLUDED (in flight) |
| billing/src/routes/webhooks.ts | 3 (184, 215, 318) | 4 | EXCLUDED (in flight) |
| mcp-server/src/tools/info.ts | 3 (58, 108, 166) | 3 |  |
| mcp-server/src/tools/verify.ts | 3 (45, 87, 140) | 3 |  |
| originate/src/routes/platformOrganizations.ts | 3 (112, 145, 168) | 3 |  |
| analytics/src/services/exportService.ts | 2 (58, 304) | 2 |  |
| api-gateway/src/middleware/rateLimitEnforce.ts | 2 (277, 302) | 1 |  |
| kyc/src/providers/microsoft-entra-client.ts | 2 (100, 129) | 2 |  |
| mcp-server/src/tools/register.ts | 2 (64, 121) | 2 |  |
| nft-certificate/src/services/blockchain-verifier.service.ts | 2 (69, 109) | 2 |  |
| nft-certificate/src/services/ipfs.service.ts | 2 (487, 512) | 2 |  |
| originate/src/routes/systemErrors.ts | 2 (134, 165) | 2 |  |
| originate/src/routes/verificationV2.ts | 2 (441, 477) | 2 |  |
| originate/src/services/errorTrackingService.ts | 2 (65, 135) | 2 |  |
| originate/src/services/reanchorInFlight.ts | 2 (193, 229) | 2 |  |
| security/src/index.ts | 2 (294, 407) | 2 | EXCLUDED (in flight) |
| analytics/src/services/analyticsService.ts | 1 (569) | 1 |  |
| analytics/src/services/metricsCollector.ts | 1 (493) | 1 |  |
| api-gateway/src/middleware/audit.ts | 1 (334) | 1 |  |
| api-gateway/src/middleware/security.ts | 1 (198) | 1 |  |
| api-gateway/src/routes/platform.ts | 1 (1092) | 1 |  |
| api-gateway/src/routes/verification.ts | 1 (952) | 1 |  |
| auth/src/routes/users.ts | 1 (1030) | 1 | EXCLUDED (in flight) |
| auth/src/services/oauthState.ts | 1 (136) | 1 |  |
| billing/src/utils/email.ts | 1 (44) | 1 |  |
| m365-integration/src/index.ts | 1 (1594) | 0 |  |
| nft-certificate/src/cardano/index.ts | 1 (133) | 1 |  |
| nft-certificate/src/cardano/provider.ts | 1 (68) | 1 |  |
| nft-certificate/src/utils/mintError.ts | 1 (37) | 2 |  |
| originate/src/index.ts | 1 (76) | 0 |  |
| originate/src/repositories/lifecycleEventRepo.ts | 1 (82) | 1 |  |
| originate/src/repositories/shareRepo.ts | 1 (140) | 1 |  |
| originate/src/routes/metering.ts | 1 (129) | 1 |  |
| originate/src/services/anchorStateSync.ts | 1 (600) | 1 |  |
| originate/src/services/chargeEvents.ts | 1 (126) | 1 |  |
| originate/src/services/ownCreateClient.ts | 1 (88) | 1 |  |
| originate/src/services/retentionScheduler.ts | 1 (51) | 1 |  |
| originate/src/utils/lifecyclePayloadCodec.ts | 1 (58) | 1 |  |
| vc-issuer/src/repositories/credentialRepo.ts | 1 (439) | 1 |  |
| vc-issuer/src/routes/presentations.ts | 1 (183) | 1 |  |

## Notes on the top candidates (read at the tip)
- tenant-provisioning/src/index.ts (9): CHOSEN. Clean (no ZodError pre-check) catches: GET /:id, PATCH /:id/status, GET /audit-log, DELETE (3 reads incl. nested). Left: POST /api/tenants (key generation), GET /api/tenants, PATCH /api/tenants/:id (each opens with `instanceof z.ZodError`, which throws first on a revoked Proxy; a message-line fix alone is half a fix; also ks1410 pins `details: err.errors` x3).
- analytics/src/routes/analytics.ts (12): only 3 clean sites (:245, :350, :372); other 9 open with `instanceof z.ZodError` (same half-fix problem). Log-only + constant 500, no open PR, route-level harness ks1364 exists.
- originate/src/routes/{documents 17, certifications 16, verification 8, anchors 5}, gdprService 16: large, originate is a heavy service; documents/certifications are document/lifecycle surfaces; not screened for clean shape.
- nft-certificate/src/routes/nft.routes.ts (15): mint / platform-fee routes, money-adjacent.
- billing/src/routes/billing.ts (17): money. governance/governanceService.ts (12) and kyc/index.ts (6): held O43/O44/O47 sites still unmerged.
- mcp-server/src/tools/{info,verify,register}.ts (8): the message is RETURNED to the MCP client; a fix changes the response (skip unless Kam rules).
- tokenisation/src/index.ts (6): token/key service, skip. auth issuerCert*: key/cert management, skip.
