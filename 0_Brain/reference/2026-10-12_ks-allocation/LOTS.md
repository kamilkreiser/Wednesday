# KS allocation: lots and first tickets (2026-10-12, read-only)

Source: `allocation.csv` in this folder (509 open KS tickets, each read in full by an Opus reader, 10 batches). All code references below were read at **origin/develop `f8c86f859`** (2026-10-10 20:06; local checkout not fetched since, so anything merged after that is not reflected). I ran `git show` / `git grep` only. Nothing was fetched or written in the repo.

## Part A: first SPARK and SONNET tickets, sampled at source

Each fix site below was opened at origin/develop. Line numbers are the CURRENT ones; where the ticket's own number has drifted, that is noted.

| # | Ticket | Tier | File:line (as found) | Action sentence | Source check |
|---|---|---|---|---|---|
| 1 | KS-1105 | SPARK | `Blockchain/Dev/frontend/admin/src/pages/Login.tsx:81` | Replace `placeholder="admin@secuura.com"` with a neutral placeholder; snapshot/unit test asserts the new string. | CONFIRMED verbatim at :81 |
| 2 | KS-1387 | SPARK | `Blockchain/Dev/services/governance/src/routes/governance.ts:19` | Annotate `const router = Router();` as `const router: Router = Router();` (Router is already imported at :8); `tsc` build of governance decides pass/fail. | CONFIRMED. The ticket wrote `express.Router()`, but the file imports `{ Router }`. |
| 3 | KS-1438 | SPARK | `systemTest/__tests__/support/html_docs_check.mjs:120` | Replace ``import.meta.url === `file://${process.argv[1]}` `` with a comparison of resolved paths (`fileURLToPath(import.meta.url)` vs `realpathSync(process.argv[1])`); add a symlinked-invocation cell. | CONFIRMED verbatim at :120 |
| 4 | KS-1405 | SPARK | `Blockchain/Testing/ci/tools/run-schemathesis.sh:25` | `FINDINGS_DIR="${FINDINGS_DIR:-.}"` writes into the CWD. Default it to a run directory, or gitignore the artefact; a stubbed run plus `git status --porcelain` empty decides it. | CONFIRMED at :25 (output at :42-43) |
| 5 | KS-1317 | SPARK | `Blockchain/Dev/packages/shared/package.json:90` | `"test": "vitest run"`, but `vitest` is not declared anywhere in the file (2 hits, both script lines; control: `typescript` hits 1). Add vitest to devDependencies and regenerate the lock; `npm test` rc 0 vs 127 decides it. | CONFIRMED. Possibly hoisted from the workspace root, so run it in isolation. |
| 6 | KS-1391 | SPARK | `Blockchain/Dev/frontend/issuer/package.json:6-12` | Add `"test": "vitest run"` to `scripts` (the block has dev/build/preview/lint/check:bundle only); 12 passing plus one planted red. The other 5 frontends need a one-line Kam ruling, so this ticket is the issuer only. | CONFIRMED: no test script |
| 7 | KS-884 | SPARK (Opus gate advised: pre-push is every dev's gate) | `.githooks/pre-push:165` | `_refs='develop origin/develop refs/remotes/origin/develop'` uses the short name `develop`, which a tag named `develop` can shadow. Use `refs/heads/develop refs/remotes/origin/develop`; add a fixture with a tag named develop. | CONFIRMED, but the ticket's `:98-99` are now COMMENT lines; the code is at :165-169 |
| 8 | KS-1186 | SPARK (MED: auth service, but error-classification only) | `Blockchain/Dev/services/auth/src/repositories/userRepo.ts:446,512,585,594,627` | Change `return fromRow(...)` to `return await fromRow(...)` at the five sites so the surrounding catch classifies infra failures. | CONFIRMED. Ticket lines drifted by +4. Positive control: :410 already reads `return await fromRow` (KS-999). |
| 9 | KS-812 | SPARK | `Blockchain/Dev/connectors/whatsapp-bot/src/verify.ts:4` (+ log line `src/index.ts:26`) | The default `SECUURA_API_URL` is a hard-coded `secuura02-demo-api...azurecontainerapps.io` URL. Repoint it at the VM ingress or drop the fallback (fail if unset); a unit test with the env unset decides it. | CONFIRMED. The ticket said `index.ts:21`; the default actually lives in verify.ts:4. |
| 10 | KS-918 | SONNET | `Blockchain/Dev/services/auth/package.json:31` | `"vite": "7.3.6"` sits in `dependencies` (block :13-34); move it to `devDependencies` (:35+), regenerate the lock, re-measure the runtime tree. | CONFIRMED |
| 11 | KS-1453 | SONNET | `Blockchain/Dev/services/originate/package.json:26` | Remove the unused prod dependency `"handlebars": "^4.7.9"`; regenerate the lock. | CONFIRMED: `git grep -i handlebars` over originate/src = 0 hits (rc 1). Positive control: the same grep for `express` hits. The ticket's "dynamic load" check still applies. |

**Pulled from the list after the source check:** KS-1226 (was SPARK, "widen the regex ... resize 15 s budget"). `systemTest/performance/tests/unit/utils/unitSuiteSlotIndependence.test.ts` no longer has the regex: it reads the JSON report (`numPassedTests`, :127) with `timeout: 180_000` (:164), because KS-1313/KS-1326 rewrote it. Retiered to STALE (MED). Separately, KS-1326 (SONNET+OPUS_GATE) already has a `KS-1326 R1` cell at :189, so check whether it has partly landed before building.

**Pattern:** 3 of 11 sampled tickets had drifted line numbers, and 1 of 12 was already superseded. **Every SPARK brief must re-read the fix site at the current develop head first.**

## Part B: VERIFY-AND-CLOSE lots (198 tickets, 17 lots)

**Rule for each lot:** for every ticket, (1) confirm the merged PR's change is on develop (`git log --grep` / blame at the cited lines); (2) the named test exists and passes; (3) the service is deployed to Kintsugi at a sha that contains it; (4) a live check where `verify_kind` = live-api/deploy; (5) Done, with the evidence on the ticket. Any ticket where a step fails leaves the lot and is re-tiered. It is never closed on assumption.

**Disjointness:** the lots are disjoint by ticket and by primary directory. Lots L01-L04 share ONE service (api-gateway), L05-L06 share auth and L07-L08 share originate. Within those groups, run the per-file checks in parallel, but do **one Kintsugi deploy and live sweep per service**, serially. Known cross-lot read touches: KS-1234 (L01) reads gateway `index.ts` (L03); KS-1231 (L01) reads `frontend/admin` (L12); KS-1202 (L07) reads gateway `verification.ts` (L01); KS-730 (L08) cites gateway `index.ts` (L03); KS-855 (L06), KS-1351 and KS-1352 (L10) read `packages/shared` (L12); KS-1129 (L09) reads originate and gateway verification; KS-962 (L03) uses a `scripts/__tests__` test (L14); KS-1031 (L17) uses `scripts/run-migrations.sh` (L15); KS-1139 (L15) touches `deployment/azure` (L17). Verification is read and run only, so these touches do not conflict unless a ticket fails and needs a fix.

**Suggested tier for the verifier seat:** SONNET for lots that are mostly `unit` or `tooling`. Lots with security/auth logic (L02 middleware/auth, L05-L06 auth, L11 security-kyc) and the deploy-heavy L13 and L17 should get an **Opus gate** on the Done decision, per routing spec s7 q4.

Per-lot listing: ticket [confidence, verify_kind] PRs - file hint.

### L01 - api-gateway: routes/verification*.ts (10 tickets; verify: {'unit': 8, 'live-api': 2}; LOW: none)
- KS-794 [MED, unit] #1276 - verification.ts; verificationV2.ts
- KS-1072 [MED, unit] #1016 - api-gateway/src/routes/verification.ts:240-242
- KS-1073 [HIGH, unit] #1005 - api-gateway/src/__tests__/ks1057-verify-confidence-is-status-aware.test.ts
- KS-1084 [MED, live-api] #1211 - api-gateway routes/proxy.ts:554-579; verification.ts:129-176; batch.ts:146,194
- KS-1123 [MED, unit] #1168;#1002 - api-gateway/src/routes/verification.ts:597,334-342,680
- KS-1180 [MED, unit] #1150;#1029 - ks1073-tier-2-verify-has-no-statusless.test.ts:156-157; verification.ts:353
- KS-1183 [MED, unit] #1010 - api-gateway/src/routes/verification.ts:994-1012
- KS-1231 [MED, unit] #1171 - verification.ts:1212-1219; health.ts:45-52; frontend/admin/src/pages/Settings.ts
- KS-1234 [HIGH, live-api] #1128;#1108 - api-gateway src/index.ts; routes/verification.ts
- KS-1432 [HIGH, unit] #1453;#1403 - routes/verification.ts:1152; ks529-non-object-body-guard.test.ts:24-27

### L02 - api-gateway: src/middleware/* (9 tickets; verify: {'unit': 8, 'live-api': 1}; LOW: KS-801)
- KS-744 [HIGH, unit] #1028 - api-gateway/src/middleware/auth.ts:377
- KS-801 [LOW, unit] #817 - middleware/contentType.ts:91
- KS-843 [MED, live-api] #1019;#854;#845;#841 - middleware/scopes.ts
- KS-871 [HIGH, unit] #1011 - middleware/audit.ts:206,224,108,280
- KS-1165 [MED, unit] #1003;#1001 - api-gateway/src/middleware/csrf.ts:82-98
- KS-1198 [HIGH, unit] #1114 - api-gateway middleware/auth.ts:292
- KS-1205 [MED, unit] #1306 - middleware/auth.ts; middleware/rateLimitEnforce.ts:112
- KS-1207 [MED, unit] #1023 - api-gateway/src/middleware/auth.ts; index.ts:1073-1074
- KS-1215 [MED, unit] #1034 - api-gateway/src/middleware/auth.ts (getConnectorBearer)

### L03 - api-gateway: index.ts, startup-migrations, health/system-status, enforcement, redis (15 tickets; verify: {'live-api': 4, 'unit': 10, 'deploy': 1}; LOW: KS-1195, KS-1233)
- KS-864 [HIGH, live-api] #1148;#1073;#1064;#1009;#1007 - services/api-gateway/src/routes/system-status.ts:48,232,243,254
- KS-946 [HIGH, live-api] #884 - services/api-gateway/src/index.ts:1047
- KS-962 [MED, unit] #973 - startup-migrations.ts; scripts/__tests__/ks949_main_seed_idempotence.test.sh
- KS-1101 [MED, unit] #1063;#1037 - api-gateway/src/services/health.ts:132; routes/system-status.ts:333; health-dash
- KS-1128 [HIGH, unit] #1232 - api-gateway/src/startup-migrations.ts (platform seed catch)
- KS-1176 [HIGH, live-api] #1014 - api-gateway/src/services/enforcement.ts:39,53-57
- KS-1195 [LOW, unit] #1017 - api-gateway/src/index.ts:524
- KS-1204 [HIGH, unit] #1035 - api-gateway/src/services/enforcement.ts
- KS-1232 [MED, unit] #1120;#1106 - api-gateway/src/services/health.ts:58
- KS-1233 [LOW, live-api] #1038 - api-gateway/src/services/redis.ts:27,680-687
- KS-1246 [MED, unit] #1173 - services/health.ts
- KS-1248 [MED, unit] #1039 - /system/status troubleshooting
- KS-1258 [MED, unit] #1085;#1077;#1068;#1053;#1044 - api-gateway/src/routes/system-status.ts (generateTroubleshooting)
- KS-1272 [MED, deploy] #1104 - api-gateway/src/startup-migrations.ts:~1060-1093
- KS-1410 [MED, unit] #1446;#1445;#1432 - notifications.ts,batch.ts,audit-export.ts,delegations.ts,tenant-provisioning ind

### L04 - api-gateway: other routes (webhooks, admin, proxy, audit-export, platform) (14 tickets; verify: {'live-api': 5, 'unit': 9}; LOW: KS-1359)
- KS-745 [MED, live-api] #1012 - routes/audit-export.ts:138
- KS-1090 [HIGH, unit] #1305 - ks1041-vouch-mint-scope.test.ts; api-gateway/tsconfig.json
- KS-1185 [MED, unit] #1152 - createVerificationRoutes
- KS-1187 [MED, live-api] #1019 - api-gateway/src/routes/proxy.ts:726-745
- KS-1230 [MED, unit] #1100;#1097;#1092;#1086;#1080;#1074;#1069;#1054;#1045 - api-gateway/src/routes/admin.ts:1123-1129
- KS-1237 [HIGH, unit] #1156 - api-gateway/src/__tests__/ks1204-a-non-array-allow-list-fails-closed-and-documen
- KS-1244 [MED, live-api] #1127;#1114 - 
- KS-1256 [MED, unit] #1396 - platform-settings reader
- KS-1257 [MED, unit] #1175 - 
- KS-1283 [HIGH, unit] #1126;#1113 - ks1215-the-connector-branch-never-carries-the-callers-bearer.test.ts; platform.t
- KS-1341 [HIGH, live-api] #1292;#1290;#1288 - routes/webhooks.ts
- KS-1345 [HIGH, unit] #1441;#1381 - routes/webhooks.ts:196, :412
- KS-1346 [MED, unit] #1443;#1317;#1316;#1312;#1311;#1297;#1296 - fail500 helper (webhooks/gdpr/systemErrors)
- KS-1359 [LOW, live-api] #1344 - /api/platform/audit-log

### L05 - auth: src/routes/users.ts (8 tickets; verify: {'unit': 7, 'live-api': 1}; LOW: none)
- KS-938 [HIGH, unit] #1385 - services/auth/src/routes/mfa.ts:206,284; users.ts:1081
- KS-1005 [HIGH, unit] #1382 - services/auth/src/routes/users.ts:939
- KS-1006 [MED, unit] #1135;#1118 - services/auth/src/routes/users.ts:1064
- KS-1018 [MED, unit] #1015 - services/auth/src/routes/users.ts:1154,1175,1197
- KS-1050 [MED, unit] #1018 - services/auth/src/routes/users.ts:933
- KS-1194 [MED, unit] #1032 - services/auth/src/routes/users.ts saveVerificationRequest
- KS-1236 [MED, unit] #1135;#1118 - services/auth/src/routes/users.ts:1252-1254
- KS-1402 [MED, live-api] #1437;#1374 - services/auth/src/routes/users.ts:266

### L06 - auth: everything except routes/users.ts (oauth, mfa, wallet, repositories) (12 tickets; verify: {'live-api': 2, 'unit': 10}; LOW: KS-1000, KS-1188)
- KS-593 [MED, live-api] #1428;#757;#756 - 
- KS-806 [MED, unit] #819 - services/auth/src/routes/wallet.ts:171
- KS-811 [MED, unit] #1177 - 
- KS-839 [MED, unit] #1026 - services/auth/src/services/oauth.ts:352
- KS-855 [MED, unit] #1158 - services/auth/src/services/oauth.ts:57; packages/shared/src/security/scopes.ts
- KS-968 [MED, unit] #905 - services/auth/src/repositories/userRepo.ts:1363,1388
- KS-999 [MED, live-api] #1013 - getUserById; ks949-platform-admin-seed-identity.test.ts
- KS-1000 [LOW, unit] #874 - services/auth/tsconfig.json
- KS-1131 [HIGH, unit] #1230 - services/auth/src/__tests__/ks963-preauth-rethrow.test.ts:206,219,256
- KS-1188 [LOW, unit] #1178;#1163 - services/passwordLoginGate.ts:267
- KS-1193 [HIGH, unit] #1164 - services/auth/src/__tests__/ks1018-...-three-verification-store-reads.test.ts
- KS-1210 [MED, unit] #1384 - services/auth/src/routes/oauth.ts:1148,1245

### L07 - originate: routes/documents.ts, certifications.ts, adminConfig.ts (11 tickets; verify: {'unit': 11}; LOW: none)
- KS-928 [MED, unit] #1147;#874 - routes/adminConfig.ts:1824
- KS-1124 [HIGH, unit] #1333;#1324 - routes/certifications.ts:406-469; routes/documents.ts:764-774
- KS-1202 [MED, unit] #1055;#1024 - originate routes/documents.ts:1053,311; api-gateway verification.ts:546
- KS-1203 [MED, unit] #1112;#1103 - originate routes/documents.ts:565
- KS-1206 [MED, unit] #1087;#1081;#1072;#1061 - originate routes/adminConfig.ts:946
- KS-1213 [HIGH, unit] #1031 - originate routes/documents.ts (/version, sign-cert, sign-wallet)
- KS-1228 [HIGH, unit] #1052;#1043 - originate routes/documents.ts:1951,2136,1595
- KS-1263 [HIGH, unit] #1239 - originate routes/documents.ts (createShare loop, custody)
- KS-1278 [MED, unit] #1393 - documentsRouter /revoke
- KS-1291 [HIGH, unit] #1225 - originate routes/documents.ts:838-851,611
- KS-1334 [MED, unit] #1300;#1294 - routes/adminConfig.ts:113,1859,2031,2158

### L08 - originate: services/, utils/, db.ts, __tests__ harness (15 tickets; verify: {'live-api': 1, 'unit': 12, 'tooling': 2}; LOW: KS-695, KS-1311)
- KS-695 [LOW, live-api] #790;#788 - executeErasure
- KS-730 [MED, unit] #1284;#1283;#1282;#1182 - api-gateway/src/index.ts:1065,1072
- KS-980 [MED, unit] #1242 - ks597-issuer-organization-id.integration.test.ts:25-28,138-147
- KS-1028 [MED, unit] #1184 - 
- KS-1074 [MED, unit] #1281 - anchorStateSync.ts :191/:226/:299/:327
- KS-1152 [MED, unit] #1143 - 
- KS-1158 [HIGH, unit] #1238;#1172;#1153 - originate/src/services/anchorStateSync.ts:170
- KS-1159 [HIGH, unit] #1256 - originate/src/__tests__/ks1061-shared-mock-completeness.test.ts
- KS-1267 [MED, unit] #1052 - originate/src/__tests__/ks1228-a-refused-request-writes-no-provenance-row.test.t
- KS-1293 [HIGH, unit] #1261 - originate/src/__tests__ (7 files, ANCHORING_SERVICE_URL)
- KS-1305 [MED, tooling] #1395 - src/db.ts:116,329
- KS-1306 [MED, unit] #1279 - ks597-issuer-organization-id.integration.test.ts
- KS-1311 [LOW, unit] #1262 - 
- KS-1348 [HIGH, unit] #1321;#1310;#1302 - utils/logger.ts:45-46
- KS-1452 [HIGH, tooling] #1435 - 

### L09 - anchoring, timestamping, transfer, nft-certificate, wallet-connector (11 tickets; verify: {'unit': 5, 'live-api': 5, 'deploy': 1}; LOW: none)
- KS-753 [MED, unit] #1119;#1107 - timestamping/src/index.ts:445-452,466
- KS-1129 [MED, live-api] #1323;#1280;#1220;#999 - anchoring index.ts:604; originate verification.ts:338; gateway verification.ts:5
- KS-1171 [MED, unit] #1434;#1228;#1176 - anchoring/src/anchorSubmission.ts; cardano/confirmation.ts
- KS-1173 [MED, deploy] #877;#1059 - services/anchoring/src/anchorSchema.ts:18
- KS-1175 [MED, live-api] #1116;#1105 - anchoring/src/anchorSchema.ts
- KS-1284 [HIGH, live-api] #1116;#1105 - anchoring/src/cardano/transaction.ts:107; cardanoMetadatum.ts
- KS-1333 [MED, unit] #1380 - services/anchorStateSync.ts:231,266,346,382
- KS-1360 [HIGH, live-api] #1345 - 
- KS-1404 [MED, unit] #1388;#1376 - tsa/qualified-tsa.ts:365-456
- KS-1435 [HIGH, unit] #1422;#1408;#1403 - services/transfer/src/index.ts:408-412,739
- KS-1449 [HIGH, live-api] #1429 - nft-certificate openapi source (POST /api/nft/ipfs/upload)

### L10 - vc-issuer (+ packages/shared/src/vc read-only) (8 tickets; verify: {'live-api': 5, 'deploy': 1, 'unit': 2}; LOW: KS-1375)
- KS-692 [MED, live-api] #1320 - services/vc-issuer/src/routes/status.ts:35-53
- KS-1269 [MED, live-api] #1084;#1071 - 
- KS-1281 [MED, deploy] #1264;#1231 - repositories/credentialRepo.ts:28-42
- KS-1295 [MED, unit] #1267 - repositories/credentialRepo.ts store()
- KS-1351 [MED, unit] #1326 - credentialRepo.test.ts:72,142-144; credentialRepo.ts:95; packages/shared/src/vc/
- KS-1352 [MED, live-api] #1330 - packages/shared/src/vc/verifier.ts:435-449; routes/credentials.ts:338-342
- KS-1371 [MED, live-api] #1343 - systemTest/schemathesis/config/check_predicates.py:499
- KS-1375 [LOW, live-api] #1341 - services/vc-issuer/src/services/revocationResolvers.ts; verifier.ts:372-396

### L11 - security, kyc (14 tickets; verify: {'unit': 10, 'live-api': 3, 'docs': 1}; LOW: none)
- KS-629 [MED, unit] #1196 - services/kyc/src/index.ts submitSelfieSchema; kyc.openapi.ts
- KS-747 [HIGH, live-api] #1318 - security.openapi.ts; index.ts:915-919
- KS-849 [HIGH, unit] #1272 - services/kyc/src/index.ts (/document setTimeout)
- KS-851 [MED, unit] #1204 - kyc index.ts:290-293; db.ts:125-147
- KS-869 [HIGH, live-api] #880;#854 - services/security/src/index.ts:197,309
- KS-880 [MED, unit] #1133;#1124;#1110 - services/security/src/converters.ts:122
- KS-888 [MED, unit] #1337;#1334;#1327;#1322 - services/security/src/index.ts:236-238
- KS-908 [MED, live-api] #1319 - services/security/src/index.ts:345
- KS-974 [MED, unit] #1198 - index.ts:513; requestSchemas.ts:68-70
- KS-975 [MED, unit] #1216;#1161 - rateLimitScope.ts:86,118
- KS-976 [MED, unit] #1217;#1199 - services/security/src/index.ts:1267,1358,1377
- KS-1328 [MED, unit] #1430 - services/kyc/src/__tests__/db.retry.test.ts
- KS-1370 [MED, unit] #1338 - services/security/src/index.ts:1326-1369
- KS-1434 [HIGH, docs] #1448;#1403 - services/security/src/index.ts:619

### L12 - packages/shared, m365-integration, mcp-server, demo-service, referral, frontend/admin (13 tickets; verify: {'unit': 11, 'deploy': 1, 'live-api': 1}; LOW: none)
- KS-657 [MED, unit] #720;#717;#714 - 
- KS-679 [MED, unit] #922 - packages/shared/src/openapi/examples/fixtures.ts:209; docs/openapi/secuura-api.y
- KS-749 [MED, deploy] #1379;#780 - Blockchain/Dev/package.json
- KS-844 [MED, live-api] #1006 - docker-compose.yml:2117
- KS-872 [HIGH, unit] #1226 - src/crypto/jwks.ts:129
- KS-932 [MED, unit] #1004 - safeOutboundRequest
- KS-934 [MED, unit] #1274 - POST /api/teams/notify
- KS-1143 [MED, unit] #1248;#1212 - ks781-p3-3-body-parser-order.test.ts routerParserAnalysis :2318
- KS-1155 [MED, unit] #1254 - packages/shared/src/__tests__/*guard*.test.ts
- KS-1179 [MED, unit] #1275;#1224;#1201;#1157 - packages/shared/src/security/ssrf-guard.ts
- KS-1182 [HIGH, unit] #1269 - services/demo-service/src/middleware/errorHandler.ts:33-35
- KS-1223 [MED, unit] #1125;#1111 - services/referral/src/routes/referrals.ts:55; api-gateway/src/utils/trustHeaders
- KS-1335 [HIGH, unit] #1328 - services/m365-integration/src/index.ts; ks934-teams-notify-request-path-bound.te

### L13 - scripts/audit/audit-baseline.json + package-lock.json refreshes (all services) (13 tickets; verify: {'deploy': 3, 'unit': 3, 'tooling': 7}; LOW: KS-769)
- KS-528 [MED, deploy] #1377;#1340;#1214;#1025 - scripts/audit/audit-baseline.json
- KS-530 [MED, deploy] #1369;#1340;#1213 - scripts/audit/audit-baseline.json
- KS-729 [MED, unit] #1364;#1340;#1339;#883 - scripts/audit/audit-baseline.json (GHSA-mwp4-54f8-5fhr)
- KS-763 [HIGH, unit] #1036;#1033;#829;#810;#801;#798;#797;#796;#794 - scripts/audit/audit-baseline.json
- KS-769 [LOW, tooling] #1378;#1020 - scripts/audit/lock-discovery.mjs (OUT_OF_SCOPE_LOCKS)
- KS-1209 [HIGH, unit] #1057;#1041 - scripts/preflight/preflight.sh:688-702; audit/lock-discovery.mjs:255
- KS-1211 [HIGH, tooling] #1030;#1027;#1022;#1021 - scripts/audit/audit-baseline.json
- KS-1378 [HIGH, tooling] #1363;#1356;#1355;#1339 - scripts/audit/audit-baseline.json
- KS-1399 [HIGH, tooling] #1363 - scripts/audit/audit-baseline.json; 4 lockfiles
- KS-1403 [MED, tooling] #1373 - scripts/audit/audit-baseline.json
- KS-1425 [HIGH, deploy] #1397 - scripts/audit/audit-baseline.json
- KS-1426 [MED, tooling] #1450 - scripts/preflight/lockfile-cleanroom.sh:46
- KS-1437 [HIGH, tooling] #1406 - 5 package-lock.json (root, mcp-server, issuer, shared, anchoring)

### L14 - Blockchain/Dev/scripts: run-shell-suites, check-shared-relink, __tests__ (10 tickets; verify: {'tooling': 6, 'unit': 4}; LOW: none)
- KS-766 [MED, tooling] #1285 - base-image-watch.sh
- KS-930 [MED, tooling] #1121;#886;#879;#876;#874 - check-shared-relink.sh
- KS-937 [MED, tooling] #1444;#876;#874 - check-shared-relink.sh:162-241, :85
- KS-948 [MED, tooling] #879 - run-shell-suites.sh; check_shared_relink.test.sh
- KS-957 [MED, tooling] #1121 - check-shared-relink guard :375/:400/:412
- KS-1127 [HIGH, unit] #1234 - Blockchain/Dev/scripts/run-shell-suites.sh
- KS-1137 [HIGH, unit] #1117 - container_trivy_image_filter.test.sh :33 :85
- KS-1313 [MED, unit] #1409;#1245 - readSuiteCounts :157/:161
- KS-1319 [MED, unit] #1277 - vitest.config.ts setupFiles; walkTimeouts
- KS-1330 [MED, tooling] #1389 - run-shell-suites.sh

### L15 - Blockchain/Dev/scripts: preflight/, run-code-guards, run-migrations, bootstrap-env, spec-examples (14 tickets; verify: {'deploy': 1, 'unit': 8, 'tooling': 5}; LOW: KS-1033, KS-1347)
- KS-808 [MED, deploy] #1436;#1229 - scripts/run-migrations.sh
- KS-865 [MED, unit] #1229 - Blockchain/Dev/scripts/check-no-latest-tags.sh:42
- KS-998 [MED, tooling] #1442;#1422;#1407 - check-package-format.sh; .githooks/pre-push
- KS-1033 [LOW, tooling] #1209;#1185 - Blockchain/Dev/scripts/run-code-guards.sh (DEFERRED bucket)
- KS-1081 [HIGH, tooling] #1205;#1191 - scripts/bootstrap-env.sh:26; env.example
- KS-1139 [MED, unit] #1433;#1260;#1206;#1192 - deployment/azure/sync-secrets.sh; systemTest/schemathesis/validate-lint.sh
- KS-1153 [MED, unit] #1056 - run-code-guards.sh:145-148,:197-199; preflight.sh:166
- KS-1252 [MED, unit] #1227 - scripts/spec-examples/check/contract.mjs:222
- KS-1253 [MED, unit] #1227 - scripts/spec-examples/check/contract.mjs PREFIXED_UUID_RE
- KS-1296 [HIGH, unit] #1258 - Blockchain/Dev/scripts/run-migrations.sh (pg_isready probe)
- KS-1347 [LOW, unit] #1298 - scripts/openapi-examples/proxy/server.ts:31; ks732-mfa-disable-proof.test.ts:293
- KS-1355 [MED, tooling] #1454;#1431 - stack_guard.sh:105-111; dev-reload.sh:45; preflight.sh:94
- KS-1417 [HIGH, tooling] #1455;#1449 - Blockchain/Dev/env.example:361; env.local.example:56
- KS-1456 [HIGH, unit] #1447 - Blockchain/Dev/scripts/run-migrations.sh:187-188

### L16 - systemTest/ (jobs, performance, schemathesis, akto) (8 tickets; verify: {'tooling': 2, 'unit': 5, 'live-api': 1}; LOW: KS-724, KS-1015)
- KS-724 [LOW, tooling] #1412;#1411 - 
- KS-1015 [LOW, tooling] #1375;#1367 - systemTest/schemathesis/scripts/run.py:10,56; config/schemathesis-baseline.json
- KS-1098 [MED, unit] #961 - systemTest/performance/runner/k6_docker.ts:70,99; k6DockerRedaction.test.ts:178
- KS-1136 [MED, unit] #1398;#1051 - 04-container-trivy.sh:86-112; 09-aggregate-report.sh
- KS-1164 [HIGH, unit] #1423;#1271;#1200 - systemTest/performance/gate/report.ts:325,346; runner/k6_docker.ts:241
- KS-1274 [HIGH, unit] #1427 - 04-container-trivy.sh
- KS-1337 [MED, unit] #1295;#1291 - systemTest/akto/tests/preSuiteSetup.ts:36; systemTest/playwright/global-setup.ts
- KS-1436 [HIGH, live-api] #1404 - 06-tenant-isolation.sh:71

### L17 - docs/, migrations/, deployment/, Start_Up/, launcher tooling, .github (13 tickets; verify: {'live-api': 2, 'deploy': 4, 'unit': 1, 'tooling': 4, 'docs': 2}; LOW: KS-256)
- KS-256 [LOW, live-api] #782;#568;#314 - docs/openapi/secuura-api.yaml
- KS-601 [MED, deploy] #943;#707;#697 - deployment/DEPLOYMENT-ARCHITECTURE.md
- KS-663 [MED, deploy] #808 - Blockchain/Dev/package.json:43
- KS-669 [MED, unit] #725 - scripts/spec-examples/check/rules-global.mjs:67-77; docs/openapi/secuura-api.yam
- KS-911 [MED, tooling] #874 - Launch_Claude.command:244, :292, :295
- KS-912 [MED, tooling] #874 - Launch_Claude.seats.test.sh:98
- KS-965 [MED, docs] #1202 - CLI-AGENT-INSTRUCTIONS.md; USER_TESTING/*.md
- KS-972 [HIGH, tooling] #1180 - Start_Up/start-secuura.sh (banner)
- KS-1031 [MED, deploy] #1183 - scripts/run-migrations.sh; DEPLOYMENT-ARCHITECTURE.md
- KS-1049 [HIGH, docs] #1137 - PR template / docs/DEV-PROCESS.md; .githooks/pre-push
- KS-1054 [MED, deploy] #1359;#1357;#1350;#1348;#1346;#1332 - 039_rls_fail_closed.sql
- KS-1364 [MED, live-api] #1452;#1368;#1365 - *.openapi.ts -> docs/openapi/secuura-api.yaml
- KS-1388 [MED, tooling] #1387 - observability/.env.example:47; config/alerting.env.example:55
