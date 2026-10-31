# QA GATE 54 - docs batch (KS-1807 PR-3..PR-6) - Tier 2, findings-only

Repo Secuura/Distributed_Secuura. Base: develop ddc644fb4869 (origin, ls-remote 2026-10-31). Gated by Sonnet; no fixes, pushes, comments or Linear.
Clone: shared local clone inside this dir, toplevel asserted equal to the path before any fetch; fetched with the Blockchain deploy key; clone quarantined/removed afterwards.
Heads re-pinned (ls-remote refs/pull/<n>/head, then fetched and rev-parsed): ALL FOUR EQUAL the briefed heads. None moved.

| PR | Head gated | Verdict |
|---|---|---|
| #1843 PR-3 | 263d83c909eaf462596c78cec84ece738cedcb07 | GO WITH NOTES (one sentence to fix before merge, F-3.1) |
| #1856 PR-4 | b9836472639f564af43846a4859bafe09e136ca5 (origin; queued 457afe28fd26 is NOT on origin, not gated) | GO WITH NOTES (Lucid = KNOWN; one new cell to fix before merge, F-4.1) |
| #1862 PR-5 | 5961ec9c55ee0dc86c2dcc3aab1ef541e5a24d2f | NO GO until F-5.1 (MAJOR) and F-5.2 sentences are amended |
| #1863 PR-6 | 47ea7e41147df90d357784c50b3d53007088b5fb | GO WITH NOTES (nit only) |

Step 1, scope: each PR diff vs merge-base(develop) touches exactly its listed .md files (git diff --stat): #1843 2, #1856 3, #1862 3, #1863 8. No product, test, config, OpenAPI or html. PASS x4.
V's mails say the docs were verified at older bases (85cd24d81, e43a289c1, cb2320368). Every claim below was re-checked at develop ddc644fb4869.

Instruments: `git grep` / `git show` / `ls-tree` in the clone at develop, sed on source ranges, a python -I link/path script over all added lines. Doc line numbers are the line in the PR head's file where I found it, otherwise the section.
Positive control: grep for the planted symbol `FAKE_PLANT_ENDPOINT_zzz` over Blockchain/Dev/services returned rc=1 (not found) = the planted false claim is correctly marked FALSE. Path-script control: `DEPLOY-BLOCKERS.md` is reported MISSING and the doc itself says it is not tracked (so TRUE).

---------------------------------------------------------------------
## #1843 PR-3 (docs/MULTI-TENANCY.md, docs/S-K-OWNERSHIP-CONTRACT.md) - GO WITH NOTES
30 claims sampled: 28 TRUE, 1 FALSE, 3 UNVERIFIABLE (listed as such).

| # | Claim | Doc loc | Instrument | Result |
|---|---|---|---|---|
| 1 | resolveTenantDb has no callers | MULTI-TENANCY:275 | git grep resolveTenantDb services: definition + own log line only | TRUE |
| 2 | requireSuperAdmin admits super_admin, SUPER_ADMIN, platform_admin, SYSTEM_ADMIN | :279 | platform.ts:65 SUPER_ROLES, :67 | TRUE |
| 3 | document-lookup is public by design (spec security: []) | :279 | platform.ts:1106 route; ks1773 test comment | TRUE |
| 4 | register-connector uses requireOrgProvisioner; erase-connector uses requireScopeOrRole | :279 | platform.ts:614-617; gateway index.ts:391 | TRUE |
| 5 | Tokenisation 4021 / provisioning 4022 not published on host | headings | docker-compose.yml:2027,2083 ("Was: 6021:4021") | TRUE |
| 6 | PROVISION_PER_TENANT_DB set in no config file | :156 | tenant-pool-manager.ts:152; repo-wide grep | TRUE |
| 7 | tenant-provisioning checks only a valid JWT (authenticate on /api), no role check | :~340 | tenant-provisioning/src/index.ts:178-181 | TRUE |
| 8 | generate-key / rotate-key need platform-admin Bearer | :~330 | tokenisation/src/index.ts:218 PLATFORM_ADMIN_ROLES | TRUE |
| 9 | Nothing on a request path calls tokenise/detokenise | :48,:330 | gateway services/tokenisation.ts defines tokeniseFields/detokeniseValues; no caller | TRUE |
| 10 | skipTokenisation read by nothing | :421 | appears only in docker/init-platform/02-seed-default-tenant.sql | TRUE |
| 11 | Default tenant UUID a0000000-0000-4000-8000-000000000001 | :250 | platform.ts:612 | TRUE |
| 12 | Seed file docker/init-platform/02-seed-default-tenant.sql exists; init script runs only 01 | :~419 | ls init-platform | TRUE (file); entrypoint behaviour UNVERIFIABLE (doc says unchecked) |
| 13 | Workflow tables svc_approval_workflows, svc_gateway_workflows, workflow_configs have no tenant_id | diagram note | migrations/002; no later ALTER | TRUE |
| 14 | 039 header "option-(a) carve-out"; secuura_auth_lookup role | :~47 | 039_rls_fail_closed.sql:31,33,146 | TRUE |
| 15 | 050 adds a SECURITY DEFINER function reading documents across tenants | :~47 | 050_...sql:22,77 | TRUE |
| 16 | Delete runs DROP DATABASE IF EXISTS secuura_tenant_<slug>; writes tenant_deleted | deletion table | tenant-provisioning index.ts:561,569 | TRUE |
| 17 | Gateway seed comment "On Azure there is a single DB; per-tenant DBs are not provisioned" | :~27 | startup-migrations.ts:1191 verbatim | TRUE |
| 18 | x-tenant-slug set from key metadata in authenticateToken | S-K:106 | gateway auth.ts:504 | TRUE |
| 19 | S_CONNECTOR_SCOPES = the nine listed scopes | S-K:~328 | platform.ts:607-611 | TRUE |
| 20 | API_KEY_ROTATION_GRACE_SECONDS defaults to 0 | S-K:~250 | security/src/index.ts:199 | TRUE |
| 21 | Lockout env vars LOGIN_LOCKOUT_THRESHOLD / _WINDOW_MS / _DURATION_MS | S-K:345-347 | accountLockout.ts:30-32 | TRUE |
| 22 | Gateway caches the valid-key check 60 s | S-K:~115 | gateway auth.ts:225-226 | TRUE |
| 23 | Admin portal role map (ADMIN, admin, super_admin, platform_admin, SYSTEM_ADMIN, OWNER -> super_admin) | MT:~361 | frontend/admin authStore.ts:23-25 | TRUE |
| 24 | PATCH /api/platform/tenants/:id and /:id/status exist | route table | platform.ts:376,395 | TRUE |
| 25 | extractTenantContext mounted only in originate | :275 | only originate/src/index.ts imports it | TRUE |
| 26 | charge_events has no RLS on kintsugi (KS-1401, PR 1383 pending) | :39 | environment fact | UNVERIFIABLE from code (doc marks it pending) |
| 27 | platform_audit_log, platform_document_registry, platform_*_templates tables | table | gateway tests + platform.ts template routes | TRUE |
| 28 | keyPending true when key generation fails; tenant still created | :183 | tenant-provisioning index.ts:48-49 | TRUE |
| 29 | Both migration runners skip an already-recorded file | :39 | not re-run | UNVERIFIABLE (doc cites KS-1401) |
| 30 | "KS-1372 records that nothing calls recordFailure, so the login lockout does not currently lock" (next to accountLockout.ts) | S-K:347-348 | auth routes/auth.ts:353,436 and services/passwordLoginGate.ts:240,307 DO call accountLockout.recordFailure | FALSE (F-3.1) |

Links: 1 of 1 relative link (TOKENISATION.md) resolves. Backticked paths 14 of 14 resolve.

### Findings
- F-3.1 MEDIUM, fix before merge (one sentence). S-K-OWNERSHIP-CONTRACT.md:347-348. KS-1372 concerns the GATEWAY brute-force guard (api-gateway middleware/security.ts:176 passes `recordFailure: async () => {}`; tests ks1461 and ks1767 say so). The sentence is attached to `services/auth/src/services/accountLockout.ts`, whose recordFailure IS called on a failed password (auth.ts:353), a failed TOTP (auth.ts:436) and in passwordLoginGate.ts. So auth's (email,/24) lockout engages. The doc understates a live control (inverse of the overstatement class, hence MEDIUM) and would send a reader to "fix" a working control. Scope the sentence to the gateway guard.
- F-3.2 INFO. Facts about kintsugi RLS and migration 049 numbering cannot be checked from code; the page marks them pending/UNDECIDED, correct treatment.

UNMEASURED: environment facts (kintsugi RLS, Postgres entrypoint running the seed); ticket text; Platform S; nothing executed.

---------------------------------------------------------------------
## #1856 PR-4 (docs/ARCHITECTURE.md, docs/TOKENISATION.md, docs/METERING-USAGE-API.md) - GO WITH NOTES
Head gated: b9836472639f (origin). Queued 457afe28fd26 not gated (per V: Lucid correction + develop merge-in only).
32 claims sampled: 29 TRUE, 2 FALSE (one KNOWN), 1 UNVERIFIABLE.

KNOWN-CORRECTED, reported as known: ARCHITECTURE.md:239 "(there is no Lucid dependency)". Code: @lucid-evolution/lucid in services/anchoring/package.json:26, packages/shared/package.json:107, root package.json:121. The wallet-connector row (:60) "none found (no Lucid dependency)" is TRUE (its package.json has none) and must not be changed by the fix. ARCHITECTURE.md:46 (anchoring row) still names "Lucid-Cardano", the old library name.

| # | Claim | Doc loc | Instrument | Result |
|---|---|---|---|---|
| 1 | nginx sends /analytics/ straight to analytics, bypassing the gateway | ARCH intro | docker/nginx-gateway/nginx.conf:232-236 | TRUE |
| 2 | nginx on 6882 in compose | ARCH | compose:2296 | TRUE |
| 3 | security 4008 in compose, code default 4004 | table | compose:940; security/src/index.ts:96 | TRUE |
| 4 | analytics 4010 compose, code default 3010 | table | compose:1495; analytics/src/index.ts:35 | TRUE |
| 5 | Ports 4000,4001,4002,4004,4005,4014,4015,4017,4018,4020,4021,4030; gateway 8080 | table | compose PORT= lines | TRUE |
| 6 | Portals 6100/6101/6102 | table | vite.config.ts issuer/verifier/admin | TRUE |
| 7 | 39 services in docker-compose.yml | ARCH | regex over services: block = 39 | TRUE |
| 8 | 416 Aiken test definitions | ARCH | 32 non-build .ak files, 416 `test` lines | TRUE |
| 9 | Node 24; React 19; Prisma 7 (originate); Vitest 4; Redis 8 | tech table | FROM node:24 x9; issuer react ^19.2; originate prisma ^7.8; vitest ^4.1.9; redis:8-alpine | TRUE |
| 10 | JWT 1 h code default, 1 d in compose | ARCH | auth/services/jwt.ts:43; compose:774 | TRUE |
| 11 | PII_FIELDS env replaces the default list | TOK | tokenisation/src/index.ts:25-26 | TRUE |
| 12 | Service exits in production when KEK unset | TOK:198 | index.ts:163-168 (also exits for NODE_ENV=demo) | TRUE, incomplete (F-4.3) |
| 13 | rotate-key answer keys; body is tenantId only | TOK | index.ts:339-349 | TRUE |
| 14 | Port 6021 published by no compose file | TOK | only a commented "Was: 6021:4021" | TRUE |
| 15 | metering:read minted but no route checks it | METER:115 | grep: only tenant-provisioning/meteringKey.ts:28,62 | TRUE |
| 16 | x-tenant-override honoured for super_admin, SUPER_ADMIN, SYSTEM_ADMIN, platform_admin; allow-listed | METER | gateway auth.ts:591-592; trustHeaders.ts:41 | TRUE |
| 17 | isGatewayVouched + GATEWAY_VOUCH_SECRET in originate gatewayProvenance.ts | METER | gatewayProvenance.ts:136 | TRUE |
| 18 | originate never calls timestamping | ARCH table | grep timestamping/TIMESTAMPING_URL/4004 in originate/src non-test = 0 | TRUE |
| 19 | nft-certificate fetches originate certification without Authorization | ARCH | minting.service.ts:148,173 | TRUE |
| 20 | nft-certificate does not call anchoring | table | grep anchoring in nft-certificate/src non-test = 0 | TRUE |
| 21 | prism has no Cardano code | table | grep cardano/blockfrost prism/src = 0 | TRUE |
| 22 | billing checkout reads req.user.stripeCustomerId; auth never mints it | ARCH | billing.ts:376,420; auth/src = 0 | TRUE |
| 23 | Session-revocation check fails open | ARCH | shared session-validation.ts:46,77 | TRUE |
| 24 | Tenant rate limiter not mounted, tier from x-tenant-tier | ARCH | tenant-rate-limiter.ts:53,137; no importer | TRUE |
| 25 | Argon2id password hashing | ARCH | auth/services/password.ts:34-40 | TRUE |
| 26 | MeshSDK in portal; cardano-serialization-lib in NFT minting | ARCH:239 | issuer @meshsdk/core; nft-certificate CSL 15.0.3 | TRUE |
| 27 | Template deploys gateway + 19 backend apps (not 24) | ARCH:338 | services.bicep 26 containerApps minus pgbouncer, redis, gateway, 3 frontends, outlook add-in = 19 | TRUE |
| 28 | Template has Log Analytics not App Insights; Redis as container app | ARCH | main.bicep:239-242 | TRUE |
| 29 | Production row: "Cardano Mainnet (the template's default)" | ARCH:395 | services.bicep:1030,1191,1547 hard-set CARDANO_NETWORK 'preview'; env.dev.json preprod; deployment/cardano/config/networks.ts:146 defaults 'preview'; no mainnet value anywhere in deployment/azure except a SQL comment and a runbook line | FALSE (F-4.1) |
| 30 | "there is no Lucid dependency" | ARCH:239 | see KNOWN | FALSE - KNOWN |
| 31 | Test is TestMeteringUsage in systemTest/schemathesis/tests/test_workflows_reporting.py | METER | path resolves; class name not re-grepped | UNVERIFIABLE (class) |
| 32 | Gateway strips x-user-*, x-tenant-*, x-organization-*, x-role-* before auth, one exception | METER | trustHeaders.ts allow-list = x-tenant-override only | TRUE |

Links: ARCHITECTURE 8 of 8, TOKENISATION 3 of 3 relative links resolve. Only missing backticked path is `DEPLOY-BLOCKERS.md`, which the doc itself says is not tracked (TRUE).

### Findings
- F-4.0 KNOWN, not counted: the Lucid line. The fix touches ARCHITECTURE.md:239 only.
- F-4.1 MEDIUM, fix before merge (one cell). ARCHITECTURE.md:395 says production runs "Cardano Mainnet (the template's default)". The template's value is `preview` (services.bicep x3); nothing in deployment/azure selects mainnet. A reader would believe a template deploy anchors on mainnet (real funds). Suggest "network set per environment; the template sets preview". The queued update is said to change only the Lucid line and a merge-in, so this stays.
- F-4.2 MINOR. ARCHITECTURE.md:46 still says "Lucid-Cardano"; code uses @lucid-evolution/lucid. Fold into the queued Lucid fix.
- F-4.3 MINOR. TOKENISATION.md:198 says the KEK-unset exit is "in production"; code exits for production and demo.

UNMEASURED: which network each environment runs (doc says not described); Stripe behaviour for a customer-less checkout (doc says not traced); the "test counts 208 and 290 appear nowhere" negative; the queued head 457afe28fd26.

---------------------------------------------------------------------
## #1862 PR-5 (Blockchain/Dev/CONNECTORS.md, docs/CONNECTORS_PATTERN.md, services/m365-integration/SETUP.md) - NO GO until F-5.1 and F-5.2 are amended
32 claims sampled: 22 TRUE, 2 FALSE, 1 TRUE-but-incomplete, 7 UNVERIFIABLE/not re-read.

| # | Claim | Doc loc | Instrument | Result |
|---|---|---|---|---|
| 1 | Auth has no msal dependency; msal-node only in m365-integration | CONNECTORS:55 | git grep msal package.json: only services/m365-integration | TRUE |
| 2 | jsonwebtoken in auth and shared; no jose | CONNECTORS:~56 | package.json grep | TRUE |
| 3 | Six social providers incl. microsoft_personal | CONNECTORS note | providers/social/*.ts; provider-factory.ts | TRUE |
| 4 | Social routes /social/providers, /social/:provider, /callback, POST /social/link | note | auth/routes/auth.ts:966,972,1012,1347 | TRUE |
| 5 | KYC_PROVIDER defaults to mock; production guard requires ENTRA_VERIFIED_ID_TENANT_ID/_CLIENT_ID | note | kyc/src/index.ts:41,43,55 | TRUE |
| 6 | Those two variables are read by no code | note | grep outside the guard = 0 | TRUE |
| 7 | m365 on 4013; gateway maps /api/m365/* | note | compose:461,882; gateway index.ts:387 | TRUE |
| 8 | requireM365 guards init, refresh, add site, sync, onedrive, teams webhook-config, outlook exchange-token (503) | CONNECTORS+SETUP | m365 index.ts:710,830,881,1013,1152,1192,1271,1310,1565 | TRUE |
| 9 | m365 has no SERVICE_ENABLED toggle | CONNECTORS | grep = 0 | TRUE |
| 10 | SHAREPOINT_SITE_URL passed by compose, read by no service code | SETUP | compose 1 hit; m365/src 0 | TRUE |
| 11 | Auth URL uses ENTRA_REDIRECT_URI, OAUTH_REDIRECT_URI, default; code exchange uses ENTRA_REDIRECT_URI, FRONTEND_URL+/api/m365/callback | SETUP | m365 index.ts:1131 and :650 | TRUE |
| 12 | Gateway forwards /api/m365/callback without requiring a token | SETUP:15 | gateway routes/proxy.ts:962 | TRUE |
| 13 | /health returns config.m365Configured, msalReady, graphReady | SETUP | index.ts:469-487 | TRUE |
| 14 | "Every /api route except the callback needs a bearer token whose claims name an organisation" | SETUP:74 | m365 index.ts:704 `jwtAuthenticate({ publicOps: ['POST /outlook/verify-hash'] })`; GET /api/health (:490) and GET /api (:495) registered before it; gateway proxy.ts:966-970 documents verify-hash public by contract | FALSE (F-5.1) |
| 15 | Caller's organisation comes from the token; none => 403; organizationId body field ignored (KS-1673) | SETUP:74 | m365 index.ts:361-402 | TRUE |
| 16 | 20 connector test files, jest, expect(true).toBe(true); 21 registry entries; check:connectors / test:connectors scripts | PATTERN | 20 *.test.ts + 1 .example; registry parse = 21; package.json:51-52 | TRUE |
| 17 | Gate is a job in pr-security-gates.yml and security-scan.yml; DEV-PROCESS lists it | PATTERN | .github/workflows lines 59, 467; DEV-PROCESS.md:130 | TRUE |
| 18 | No service has a connectors/ directory | PATTERN:3 | ls-tree services/*/src | TRUE |
| 19 | Anchoring reads BLOCKFROST_API_KEY (+BLOCKFROST_URL), not BLOCKFROST_PROJECT_ID | PATTERN:50 | cardano/index.ts:57; threadTokenMint.ts:72,240; BUT anchoring/src/index.ts:81 enforceProductionConfig requiredEnvVars: ['BLOCKFROST_PROJECT_ID'] | TRUE for reads, omits the production guard (F-5.3) |
| 20 | "/health/deep and /health/ready exist only on the API gateway ... no service has its own" | PATTERN:228 | /health/ready exists in originate (routes/health.ts:44), auth (:83), anchoring (index.ts:400), analytics, staking, vc-issuer; compose healthchecks (e.g. :649) call http://localhost:4000/health/ready | FALSE for /health/ready, TRUE for /health/deep (F-5.2) |
| 21 | Gateway /health/deep checks Postgres, Redis, probes anchoring, auth, originate | CONNECTORS+PATTERN | gateway services/health.ts:147,241-242 | TRUE (probe list not line-checked) |
| 22 | TSA files der.ts, qualified-tsa.ts, rfc3161-client.ts, rfc3161-verify.ts; mock fallback in src/index.ts | CONNECTORS | ls tsa/; index.ts:472,649 | TRUE |
| 23 | ACS when ACS_CONNECTION_STRING + ACS_SENDER_ADDRESS; SMTP only with SMTP_ENABLED=true and SMTP_HOST | CONNECTORS | auth/services/email.ts:8-18 | TRUE |
| 24 | SSRF guard in packages/shared/src/security/ssrf-guard.ts; originate webhooks use assertSafeOutboundUrl | CONNECTORS | file exists; webhooks.ts:19 | TRUE |
| 25 | postgres:15-alpine, redis:8-alpine, yaci-cli 0.10.6 | CONNECTORS | redis:8-alpine and a yaci-cli reference seen; postgres tag and 0.10.6 not re-read | UNVERIFIABLE (partial) |
| 26 | POST /api/sites matches siteUrl, 404 with the site list | SETUP:88 | not re-read | UNVERIFIABLE |
| 27 | Default scopes User.Read, Sites.Read.All, Files.Read.All; PKCE; offline_access | SETUP:20 | not re-read | UNVERIFIABLE |
| 28 | Apple entry's variables differ from code (KS-1886) | PATTERN | not deep-checked | UNVERIFIABLE |
| 29 | isHealthy only in the unused Identus client | PATTERN:~270 | not re-grepped | UNVERIFIABLE |
| 30 | deployOutlookAddin parameter gates the add-in | CONNECTORS | outlookAddin resource in services.bicep; parameter name not read | UNVERIFIABLE (name) |
| 31 | Added backticked paths | all | script: 12 + 6 + 1, 0 missing | TRUE |
| 32 | Added relative md links | all | none added | n/a |

### Findings
- F-5.1 MAJOR (security wording, the brief's class; fix before merge). services/m365-integration/SETUP.md:74: "Every `/api` route except the callback needs a bearer token whose claims name an organisation". `POST /api/outlook/verify-hash` is deliberately unauthenticated (publicOps, KS-442; also public at the gateway) and forwards to originate verification; `GET /api/health` and `GET /api` are mounted before the auth middleware. The doc overstates protection. Practical risk is low (public by contract) but the sentence is false as written. Suggest "except the callback, the health routes and POST /api/outlook/verify-hash (public by contract)".
- F-5.2 MEDIUM. CONNECTORS_PATTERN.md:228 says /health/ready exists only on the gateway and no service has its own. It exists on originate, auth, anchoring, analytics, staking, vc-issuer, and compose healthchecks depend on it. Only /health/deep is gateway-only.
- F-5.3 MINOR. CONNECTORS_PATTERN.md:50: anchoring's production startup guard still REQUIRES BLOCKFROST_PROJECT_ID (anchoring/src/index.ts:81). One clause; same guard-versus-reader class the PR already reports for kyc (KS-1886).

UNMEASURED: State / Last verified / Owner action columns (V says not re-measured); the four anchoring rows (on hold KS-1384); POST /api/sites behaviour, Graph scopes, PKCE; Apple mismatch; nothing run against Microsoft, Stripe or a TSA.

---------------------------------------------------------------------
## #1863 PR-6 (BACKLOG.md, Dev/README.md, SERVICES.md, DEVELOPMENT.md, PROJECT_OVERVIEW.md, CHANGELOG.md, docs/DEVELOPER-GUIDE.md, docs/STAKEHOLDER-GUIDES.md) - GO WITH NOTES
34 claims sampled: 28 TRUE, 1 nit, 5 UNVERIFIABLE/not re-read.

| # | Claim | Doc loc | Instrument | Result |
|---|---|---|---|---|
| 1 | Default compose publishes only postgres 127.0.0.1:6432, redis 127.0.0.1:6379, pgbouncer 127.0.0.1:6433, nginx 6882, website 6881; under profiles cardano mock 6090, devnet 6091-6094, ollama 11434 | SERVICES:62, README | every host:container mapping in docker-compose.yml (11): lines 156,217,262,330,372-375,1993,2296,2343 | TRUE (exposure claim, exact) |
| 2 | No backend publishes a host port; 6000-series only via docker-compose.dev-debug.override.yml | SERVICES:62, README:100 | override header; compose 2027,2083,877 commented "Was:" | TRUE |
| 3 | Devnet 6091->3001, 6092->8080, 6093->10000, 6094->8090 | README, SERVICES | compose:372-375 | TRUE |
| 4 | Test tokens only when NODE_ENV is development or test AND ENABLE_TEST_TOKENS=true; not staging/demo | SERVICES:244 | gateway auth.ts:122-131; rateLimitSkip.ts:32,44 | TRUE (security class, exact) |
| 5 | /health/services answers 404 unless ENABLE_PUBLIC_HEALTH_SERVICES=true | SERVICES:185 | gateway health.ts:249-254 | TRUE |
| 6 | Gateway routes /health, /health/ready, /health/deep; no /api/health route | :185 | health.ts:241-242; /api/health only in exclusion lists (audit.ts:71, versioning.ts:28) | TRUE |
| 7 | No Midnight service (no services/midnight, no compose service) | README:87, SERVICES:28 | ls services; compose | TRUE |
| 8 | /api/proofs/generate|verify and /api/midnight/selective-disclosure do not exist | SERVICES | git grep services+packages non-md non-test = 0 | TRUE |
| 9 | 22 backend services with PORT in default compose (+gateway; MCP uses MCP_HTTP_PORT); guardian, queue under phase2 | SERVICES:69 | 23 `- PORT=` lines incl. gateway 8080; mcp-server MCP_HTTP_PORT=4023; phase2 compose:1787,1839 | TRUE |
| 10 | Images build on node:24-alpine; root package.json requires >=18.0.0 | README:18 | Dockerfiles; package.json:77 | TRUE |
| 11 | DB_STATUS_TO_DOMAIN maps inactive, deleted to DEACTIVATED | BACKLOG | auth/types/index.ts:~125-135 | TRUE |
| 12 | mapDbStatus fails closed to DEACTIVATED (was `|| 'ACTIVE'`) | BACKLOG | userRepo.ts:~340 | TRUE |
| 13 | ADMIN_WRITABLE_STATUSES = active, suspended, deactivated, pending, inactive, deleted; invited absent | BACKLOG | types/index.ts:150-157 | TRUE |
| 14 | ks796q1-status-allow-list.test.ts and usersAdminStatus.test.ts exist | BACKLOG | ls auth/src/__tests__ | TRUE |
| 15 | Seven identity tiers NONE..GOVERNMENT | README:426 | auth/types/index.ts:18-33 | TRUE (STANDARD = MFA gloss not re-read) |
| 16 | No Entra or Auth0 sign-in flow in auth | README:79, CHANGELOG | msal only in m365; consistent with PR-5 | TRUE |
| 17 | Prisma schema at Blockchain/Dev/prisma/schema.prisma, not under services/originate | README:136 | ls | TRUE |
| 18 | migrations service applies SQL via scripts/run-migrations.sh; no prisma migrate | README | script not read | UNVERIFIABLE |
| 19 | env_file also loaded by m365-integration | README:179 | compose:872 in that block | TRUE |
| 20 | Ogmios off (ogmios_enabled=false) | README:286 | compose:382 | TRUE |
| 21 | env.local.example also exists | README:316 | ls Dev | TRUE |
| 22 | Per-tenant DBs only with PROVISION_PER_TENANT_DB=true; vault in main DB | README:447-449 | tenant-pool-manager.ts:152; agrees with PR-3/PR-4 | TRUE |
| 23 | DEFAULT_TENANT_ID a0000000-0000-4000-8000-000000000001 | SERVICES | constants | TRUE |
| 24 | Repo rule is Compose v2 | SERVICES:87 | repo CLAUDE.md:44 | TRUE |
| 25 | Repo CLAUDE.md records Container Apps deleted 2026-07-31, demo on a VM since 2026-07-08 | SERVICES, DEV-GUIDE | CLAUDE.md:7-25 | TRUE |
| 26 | docs/AZURE-DEMO-ACCESS.md exists | SERVICES | ls | TRUE |
| 27 | main.bicep: Redis classic no longer created; Redis container app in services.bicep | SERVICES:75 | main.bicep:239-242 | TRUE |
| 28 | Azure PostgreSQL Flexible Server in main.bicep | SERVICES | not re-read | UNVERIFIABLE |
| 29 | PROJECT_OVERVIEW tree lists a `Shared/` directory that does not exist | PROJECT_OVERVIEW:3 | lowercase Blockchain/Dev/shared/ exists with one file (types/svs-types.ts); tree describes "Shared frontend utilities" | nit (F-6.1) |
| 30 | CHANGELOG: newest release 0.15.0; no Compact contract; no Auth0 flow | CHANGELOG:3 | 0.15.0 heading not re-read; others per 7/16 | partial UNVERIFIABLE |
| 31 | POST /api/documents is JSON (title, documentType, contentHash); upload is /api/documents/upload | README curl block | route existence only | body field names UNVERIFIABLE |
| 32 | POST /api/verification/hash takes JSON {data} | README note | not re-read | UNVERIFIABLE |
| 33 | Added backticked paths | all | script: 3+2+4+3+11+10+2+2, 0 missing | TRUE |
| 34 | Added relative md links | all | none added | n/a |

### Findings
- F-6.1 NIT. PROJECT_OVERVIEW.md:3 says a `Shared/` directory does not exist; a lowercase `Blockchain/Dev/shared/` does (one types file). Say "no shared frontend-utilities directory".
- No overstated protection found. The exposure statements (host ports, test tokens, /health/services) are exact.

UNMEASURED: README request-body field names; migrations script; CHANGELOG 0.15.0 heading; Azure facts beyond main.bicep; pages V lists as not read (DATABASE-SCHEMA, ENVIRONMENT-VARIABLES, most guides, ~10 pages with dead Container Apps URLs).

---------------------------------------------------------------------
## Step 5 - contradictions
1. #1856 ARCHITECTURE:239 (no Lucid) vs #1862 CONNECTORS (Lucid Evolution 0.4.x in anchoring and shared) and develop package.json: KNOWN, #1862 is right.
2. #1862 CONNECTORS_PATTERN:228 (/health/ready gateway-only) vs develop compose healthchecks and service source: #1862 wrong (F-5.2). #1863 SERVICES:185 ("every service answers /health") is correct and does not conflict.
3. #1843 S-K:347 (login lockout does not lock) vs develop auth code: #1843 wrong (F-3.1).
4. #1856 ARCHITECTURE:395 (mainnet template default) vs bicep: #1856 wrong (F-4.1).
5. Consistent across PRs: per-tenant DB only behind PROVISION_PER_TENANT_DB (#1843, #1856, #1863); vault and tenant_keys in the main DB (#1843, #1856, #1863); JWT 1 h code / 1 d compose (#1843, #1856); tokenisation port unpublished (#1843, #1856, #1863); no Entra/Auth0 sign-in (#1862, #1863); platform-admin role set identical (#1843, #1856).

## Limits
Docs read against code only; nothing executed, no service started, no Azure/Microsoft/Stripe call; KS ticket text not read. About 128 claims sampled; long [RE-VERIFIED] notes were read to ~650 characters per added line, claims in the visible part were checked. Findings-only: no PR was commented on or modified.
