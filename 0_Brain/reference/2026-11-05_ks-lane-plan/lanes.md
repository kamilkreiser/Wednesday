# Build lanes for the SCOPE-REMAINS tickets (2026-11-05, read-only plan)

**91 tickets in 22 lanes** (21 disjoint lanes A to R5 plus lane X, the cross-service serial lane). Source: SCOPE-REMAINS class of `../2026-11-05_ks-inprogress-postdeploy/postdeploy.tsv` (91 rows), each ticket re-read on 2026-11-05 15:xx (fresh paginated pull: newest comment, description, all comments). HUMAN-OWNED tickets (Peter/Stuart creator or assignee) are excluded and listed in `human_owned.md`; KS-911/912 and the 10 live-seat keys excluded; the 7 tickets Done today are not in the set.

## How to read this

- **Disjointness rule:** within lanes A to R5 no two lanes share a file or a `services/<svc>/src/<area>` family; the only shared directory trunks are listed under each lane. Tickets inside one lane may share files, so run them **one at a time in the listed order** unless the lane says "internally parallel-safe". Lane X tickets each touch two or more lanes: run them after the lanes they touch are idle, one at a time.
- **Route:** SPARK = one-file spelled-out fix a Spark can be briefed on once the brief names the lines; SONNET = a build needing reading and judgement; OPUS = auth, security, money or data-destroying design (Opus design/gate, Sonnet may implement).
- **Files are inferred**, from path strings in the ticket description and newest comment (frequency-ranked) plus the title. `UNMEASURED` marks a file not stated. Nothing here was opened in the repo except to confirm 6 path names exist at 07a2d62be6a0. Build summaries come from the newest comment's "Left open" paragraph (first ~420 characters), not a full read of every comment.
- Every ticket below has already shipped some part to develop; "remaining" is what its newest comment says is not done. Each build must still pass the QA gate and, for runtime changes, a deploy plus live check (nothing here authorises a deploy).

## Lane index

| lane | name | tickets | file family | routes (Spark/Sonnet/Opus) |
|---|---|---|---|---|
| A | auth service | 7 | services/auth/src/{routes,services,providers} | 3/2/2 |
| B | api-gateway: verification, allow-list, admin | 10 | services/api-gateway/src/{routes/verification.ts,routes/admin.ts,services/,index.ts} | 3/5/2 |
| C | api-gateway: startup, system-status, audit-export, middleware, image | 7 | services/api-gateway/src/{startup-migrations.ts,routes/system-status.ts,routes/audit-export.ts,middleware/} + Dockerfile | 3/3/1 |
| D1 | originate: routes, repositories, anchor sync | 5 | services/originate/src/{routes,repositories,services/anchorStateSync.ts,__tests__/ks1676-*} | 1/3/1 |
| D2 | originate: GDPR retention and connector erasure | 2 | services/originate/src/services/{gdprService,connectorOrganisationErasure}.ts | 0/1/1 |
| E | security service | 5 | services/security/src | 1/4/0 |
| F | kyc service tests | 1 | services/kyc/src/__tests__ | 0/1/0 |
| G | anchoring service | 2 | services/anchoring/src | 0/2/0 |
| H | m365-integration | 3 | services/m365-integration/src | 1/2/0 |
| I | vc-issuer | 2 | services/vc-issuer/src | 1/0/1 |
| J | governance | 2 | services/governance/src | 0/1/1 |
| K | frontend admin | 2 | frontend/admin/src/pages + packages/shared/src/__tests__/ks1564-* | 0/2/0 |
| P | packages/shared ssrf guard | 1 | packages/shared/src/security | 0/1/0 |
| M | mcp-server | 1 | services/mcp-server/src/http-server.ts | 1/0/0 |
| N | staking | 1 | services/staking/src/routes/stake.ts | 1/0/0 |
| Q | docs | 4 | docs/{openapi/secuura-api.yaml,MULTI-TENANCY.md,RLS-FAIL-CLOSED-PLAN.md,DEV-PROCESS.md} | 3/1/0 |
| R1 | preflight and audit baseline | 3 | scripts/{preflight,audit} | 2/1/0 |
| R2 | shared re-link guard | 3 | scripts/check-shared-relink.sh + scripts/__tests__/check_shared_relink* | 1/2/0 |
| R3 | launcher and stack scripts | 8 | scripts/{bootstrap-env.sh,run-*.sh,smoke-test.sh,prisma-generate.cjs,spec-examples,check-compose-stack-safety.mjs,...} | 3/5/0 |
| R4 | Testing jobs | 1 | Blockchain/Testing/jobs | 1/0/0 |
| R5 | systemTest | 7 | systemTest/{fixtures,performance,akto,playwright,__tests__,scripts} | 2/5/0 |
| X | CROSS-SERVICE (serial, last; each ticket spans the lanes above) | 14 | mixed: see per ticket | 1/11/2 |

Route totals: Spark 28, Sonnet 52, Opus 11.

## Lane A: auth service

File family: `services/auth/src/{routes,services,providers}`

| ticket | pri | files it would touch | build summary | route |
|---|---|---|---|---|
| KS-1150 | High | auth/src/routes/oauth.ts | R-2 refuse a replayed refresh token and denylist its jti; R-3 answer 503 (not 500) when either user lookup throws ServiceUnavailableError (OAuth /token grant hardening (measured by the #982 gate, pre-existing)) | OPUS |
| KS-1407 | High | auth/src/routes/* (password change/reset doors; exact file UNMEASURED) | finish N-1382-2 and gate note N1 left after the session-revoke change (revoke other sessions, fail closed) (a password change or reset leaves the account's other sessions live) | OPUS |
| KS-1968 | High | auth/src/routes/auth.ts, auth/src/services/password.ts | B2: refuse a breached password at change-password (waits on PRs 1798, 1796) and the other named doors (auth: the breached-password check (isPasswordBreached, pen-test F-12 i) | SONNET |
| KS-1460 | Medium | auth/src/routes/auth.ts | check the updateUser result in the six remaining discarding callers; answer 503 when the write did not land (auth: 8 of 13 non-test updateUser callers discard the result (sweep th) | SONNET |
| KS-1804 | Medium | auth/src/services/passwordLoginGate.ts | KS-1188 F3 gate note 1 (constant/message cleanup in the gate; wording not stated in the excerpt read, UNMEASURED) (services/auth passwordLoginGate: two KS-1188 F3 gate notes carried on ) | SPARK |
| KS-1858 | Medium | auth/src/providers/social/{google,facebook,linkedin,microsoft-personal}.ts | refuse a whitespace-only access_token in the four adapters (gate note G67-F3) with a cell each (auth: the Google, Facebook, LinkedIn and Microsoft sign-in adapters re) | SPARK |
| KS-1797 | Low | auth/src/routes/oauth.ts | /authorize POST half: repeated state or code_challenge as arrays answers 400 invalid_request, not 500 (OAuth /authorize: a repeated state or code_challenge answers 500, and ) | SPARK |

## Lane B: api-gateway: verification, allow-list, admin

File family: `services/api-gateway/src/{routes/verification.ts,routes/admin.ts,services/,index.ts}`

| ticket | pri | files it would touch | build summary | route |
|---|---|---|---|---|
| KS-1087 | High | services/api-gateway/src/routes/verification.ts | workflow-approve forward sends no Authorization header so originate answers 401; forward the caller auth (design choice: user token vs service identity) and keep the pending document on failure (workflow-approve deletes the pending document and answers 200 "Documen) | OPUS |
| KS-1262 | High | services/api-gateway/src/routes/admin.ts, services/redis.ts | N3/N4: per-user notification GET still returns the whole platform-settings object; separate the key namespaces (Security: PUT /api/settings/notifications writes the same key namespac) | OPUS |
| KS-1180 | Medium | services/api-gateway/src/routes/verification.ts + ks1073 cells | make the tier guard a real tier witness and pin the _source comparison (P-1005-1/2/4 residue) (ks1073 verify cells: the tier guard is not a tier witness, the _source) | SONNET |
| KS-1185 | Medium | services/api-gateway/src/routes/verification.ts | F2 idle-vs-total timer and F3 misleading forward error on a never-ending 201 body (Polish) (KS-1183 gate follow-ups: validate the approve forward timeout override) | SONNET |
| KS-1204 | Medium | services/api-gateway/src/routes/admin.ts (+ frontend/admin/src/services/api.ts UNMEASURED) | a STRING allowedDocumentTypes must not substring-match; pin documentType-over-type precedence (A STRING allowedDocumentTypes substring-matches, and no cell pins docu) | SONNET |
| KS-1237 | Medium | services/api-gateway/src/services/enforcement.ts + ks1204 test file | kill three surviving tampers: array-like allow-list, refusal message class, X-INFO-ALWAYS-EMPTY row (ks1204 cells: three tampers stay green - the array-like allow-list, th) | SONNET |
| KS-1505 | Medium | services/api-gateway/src/index.ts (hot-reload block) | part 2: stop logging reload success when the spec bytes are unchanged (Correct the spec hot-reload comment, and stop it logging success when ) | SPARK |
| KS-1539 | Low | services/api-gateway/src/routes/verification.ts:817-823 | log the thrown allow-list read in the bare catch on the create path (503 stays) (A thrown allow-list read answers 503 but logs nothing: the create path) | SPARK |
| KS-1542 | Low | services/api-gateway/src/__tests__/ks1185-f1-workflow-approve-forward-bound-is-validated.test.ts:111 | fix the BigInt cell title that still says RED KS-1518 (The approve-forward bound refusal still prints a refused array or obje) | SPARK |
| KS-1614 | Low | services/api-gateway/src/index.ts, routes/verification.ts | items 1-3: refusal message prints Map/Set/RegExp/Error as {} and a toJSON object as accepted; print them honestly (KS-1542 follow-up (PR #1554 gate): Map/Set/RegExp/Error print {}, {toJ) | SONNET |

## Lane C: api-gateway: startup, system-status, audit-export, middleware, image

File family: `services/api-gateway/src/{startup-migrations.ts,routes/system-status.ts,routes/audit-export.ts,middleware/} + Dockerfile`

| ticket | pri | files it would touch | build summary | route |
|---|---|---|---|---|
| KS-962 | High | services/api-gateway/src/startup-migrations.ts, scripts/__tests__/ks949_main_seed_idempotence.test.sh | user seed throws 42P10 on every boot: repair or remove the INSERT given pg_roles read on kintsugi (no secuuraadmin role) (The api-gateway user seed throws 42P10 on every boot and has never see) | SONNET |
| KS-1645 | High | services/api-gateway/src/routes/audit-export.ts, api-gateway.openapi.ts | audit export: page through all upstream pages, include the `to` day, validate type fully (items 1,2,4, rest of 3) (The now-live audit export is quietly wrong: at most one upstream page,) | SONNET |
| KS-736 | Medium | services/api-gateway/src/middleware/auth.ts + mount-auth check test | part (b): /api/certifications and /api/nft mounts need authenticateToken(true); depends on unmerged PR 1701 (KS-1713) (Gateway mount-auth check scores authenticateToken(false) as green — si) | OPUS |
| KS-864 | Medium | services/api-gateway/src/routes/system-status.ts | items 2,3: drop the hard-coded secuura-staging third arg from 16 of 18 getServiceUrl calls (Dead-estate pointers in RUNTIME SOURCE outside deployment/azure — syst) | SPARK |
| KS-1504 | Medium | services/api-gateway/src/middleware/rateLimitEnforce.ts tests | items 3,4: two missing test cells (item 1 landed at :181) (Write the no-allowance warning's authMethod through logField (the set ) | SPARK |
| KS-1128 | Low | services/api-gateway/src/startup-migrations.ts | log the platform tenant seed skip at warn, add real-PostgreSQL cell SEED-REALPG, pin the 200-char cut (The platform tenant seed's catch logs `Platform tenant seed skipped` a) | SONNET |
| KS-1841 | Low | services/api-gateway/Dockerfile (+ .dockerignore) | F2: keep backup files out of the build context and builder layer (api-gateway Dockerfile:35: the backup `rm -f` glob misses six name sha) | SPARK |

## Lane D1: originate: routes, repositories, anchor sync

File family: `services/originate/src/{routes,repositories,services/anchorStateSync.ts,__tests__/ks1676-*}`

| ticket | pri | files it would touch | build summary | route |
|---|---|---|---|---|
| KS-1695 | High | originate/src/routes/certifications.ts, routes/documents.ts, repositories/documentRepo.ts | gap 2: owner-less documents cloak (same-tenant read gap); gap 1 done (Security: same-tenant read gaps on certifications and owner-less docum) | OPUS |
| KS-1666 | Medium | originate/src/routes/certifications.ts + ks1666 test | eight of nine AK1 gate notes (only (d) done): row left behind when the reservation lands, etc. (KS-1633 follow-ups (PR #1623, gate AK1's nine notes): the row left beh) | SONNET |
| KS-1676 | Medium | originate/src/__tests__/ks1676-* | decide and pin the Undecided `!chain` row in the two anchor-heal functions (UNMEASURED whether it needs a ruling) (Fifteen guard clauses in the two anchor-heal functions are pinned by n) | SONNET |
| KS-1462 | Low | originate/src/routes/adminConfig.ts | item 2: per-tenant error reporting in migrate-tenant-data and a cell that the loop continues (originate migrate-tenant-data: a non-Error throw logs as [object Objec) | SPARK |
| KS-1509 | Low | originate/src/routes/documents.ts, services/anchorStateSync.ts, routes/verification.ts, routes/verificationV2.ts | six remaining sites default block height to 0 (site 1 merged) (Seven other places still default a document's block height to 0 (docum) | SONNET |

## Lane D2: originate: GDPR retention and connector erasure

File family: `services/originate/src/services/{gdprService,connectorOrganisationErasure}.ts`

| ticket | pri | files it would touch | build summary | route |
|---|---|---|---|---|
| KS-1938 | High | originate/src/services/gdprService.ts | guard the other unguarded thrown-value reads in the retention sweep file (originate retention sweep: one unreadable thrown value stops the whole) | SONNET |
| KS-758 | Medium | originate/src/services/* erasure path (exact file UNMEASURED) | F6 half: three permanent connector-erasure failures present as retryable; design the dead-letter (Connector erasure: three permanent failures present as retryable and n) | OPUS |

## Lane E: security service

File family: `services/security/src`

| ticket | pri | files it would touch | build summary | route |
|---|---|---|---|---|
| KS-908 | Medium | security/src/index.ts | PR 1319 merged 09-28 (connectorId echoed); what remains is UNMEASURED, re-read before briefing (connectorId persists but is invisible through the API — POST and GET b) | SONNET |
| KS-1377 | Medium | security/src/index.ts | validate-route follow-ups left after PR 1602 (usage_count update arms, cache-miss read fault) (validate route follow-ups from the KS-1370 gate: usage_count lost upda) | SONNET |
| KS-1525 | Medium | security/src/converters.ts, __tests__/row-converters.test.ts | remaining rowToApiKey boundary cells (3 landed) and the pre-existing defect the gate probe found (own ticket) (security converters: four rowToApiKey boundary gaps survive the whole ) | SONNET |
| KS-1568 | Medium | security/src/index.ts | behavioural cells for the remaining rotate-chain guards (M10 etc.) (KS-1556 follow-up (#1529 round-2 gate m1): four rotate-chain guards ha) | SONNET |
| KS-1602 | Medium | security/src/__tests__/ks742-keys-tenancy-route-contract.test.ts, vitest.config.ts | remaining fix shapes after PR 1703 (shapes 1,2 done): fleet-load beforeAll skip (ks742-keys-tenancy-route-contract.test.ts: the 10 s beforeAll hook lap) | SPARK |

## Lane F: kyc service tests

File family: `services/kyc/src/__tests__`

| ticket | pri | files it would touch | build summary | route |
|---|---|---|---|---|
| KS-851 | Medium | kyc/src/__tests__/ks386-no-image-payload-written.test.ts | G-1 column ordinal drift, G-2 second-image orphan, G-3 (G-4 done) (KS-386 residues from the round-2 gate: G-1 column ordinal drift, G-2 t) | SONNET |

## Lane G: anchoring service

File family: `services/anchoring/src`

| ticket | pri | files it would touch | build summary | route |
|---|---|---|---|---|
| KS-1284 | High | anchoring/src/cardano/cardanoMetadatum.ts, cardano/transaction.ts | last leg: chain-source reader verify read where the DB row is absent (no test executes the real handler) (cardano/transaction.ts: add_json_metadatum_with_schema throws on any m) | SONNET |
| KS-1171 | Medium | anchoring/src/anchorSubmission.ts, cardano/confirmation.ts | item 8k left open by comment 4e5c20d3 (MIXED-window ABSENT rule is in) (Guard 3's re-poll reads a MIXED window as ABSENT — one early "not foun) | SONNET |

## Lane H: m365-integration

File family: `services/m365-integration/src`

| ticket | pri | files it would touch | build summary | route |
|---|---|---|---|---|
| KS-1670 | Medium | m365-integration/src/index.ts | encode the two remaining reflection sites (2 and 3); site 1 done at :677 (m365-integration: three more reflection sites from gate AM1 - an unenc) | SPARK |
| KS-1687 | Medium | m365-integration/src/index.ts, src/auth/token-manager.ts | notes left after PR 1664 (rotated refresh token persisted) (m365: a rotated Microsoft refresh token can never be persisted - toTok) | SONNET |
| KS-1800 | Low | m365-integration/src/__tests__/ks1670-* | N3, N4 and the gate wire cells for the redirect encoding (m365 ks1670 source-text pin: a raw connectionId by concatenation survi) | SONNET |

## Lane I: vc-issuer

File family: `services/vc-issuer/src`

| ticket | pri | files it would touch | build summary | route |
|---|---|---|---|---|
| KS-1295 | Medium | vc-issuer/src/repositories/credentialRepo.ts | second memory-only branch: a failed DB INSERT is logged and kept in memory; throw instead (KS-1993 is the sibling) (vc-issuer credentialRepo.store() falls back to memory SILENTLY when th) | OPUS |
| KS-1898 | Low | vc-issuer ks1851 revoke test (+ shared logger spy UNMEASURED) | optional third ask: a spy on the shared logger for the owner-less refusal cells (vc-issuer ks1851 revoke test: the owner-less refusal cells assert only) | SPARK |

## Lane J: governance

File family: `services/governance/src`

| ticket | pri | files it would touch | build summary | route |
|---|---|---|---|---|
| KS-1942 | High | governance/src/routes/governance.ts, services/governanceService.ts, db.ts | an admin registering a wallet with no row creates it under a new id; settle and fix (stake is admin-set) (governance: POST /participants/register takes walletAddress and staked) | OPUS |
| KS-1733 | Low | governance/src/__tests__/ks1722-*, governance proposals route | items 1,3,4: proposals list silently unfiltered/under-validated cases (governance GET /api/governance/proposals can still be silently unfilte) | SONNET |

## Lane K: frontend admin

File family: `frontend/admin/src/pages + packages/shared/src/__tests__/ks1564-*`

| ticket | pri | files it would touch | build summary | route |
|---|---|---|---|---|
| KS-1231 | High | frontend/admin/src/pages/Settings.tsx | save body must keep integrations an array (builds an object via key.split today) + a Settings-save round-trip cell (A connector allow-list fails open when platform-settings integrations ) | SONNET |
| KS-1589 | Medium | frontend/admin/src/pages/ApiKeys.tsx, packages/shared/src/__tests__/ks1564-* | items B and C of the ks1564 source guard follow-ups (KS-1564 follow-ups (pull request 1537 round-2 gate): the ks1564 source) | SONNET |

## Lane P: packages/shared ssrf guard

File family: `packages/shared/src/security`

| ticket | pri | files it would touch | build summary | route |
|---|---|---|---|---|
| KS-1179 | Medium | packages/shared/src/security/ssrf-guard.ts tests | pin DNS-layer classification; live check on a running service owed (safeOutboundRequest tests: no cell pins DNS-layer classification, ks93) | SONNET |

## Lane M: mcp-server

File family: `services/mcp-server/src/http-server.ts`

| ticket | pri | files it would touch | build summary | route |
|---|---|---|---|---|
| KS-1410 | High | mcp-server/src/http-server.ts:60-61 | POST /hash 500 body returns thrown text; guard with the NODE_ENV rule the other 27 sites got (28 unguarded err.message values land in 500 response bodies across six) | SPARK |

## Lane N: staking

File family: `services/staking/src/routes/stake.ts`

| ticket | pri | files it would touch | build summary | route |
|---|---|---|---|---|
| KS-1544 | Low | staking/src/routes/stake.ts | the staking sibling: give the paged list a unique last ORDER BY key (id) and a class cell (platform_audit_log is paged without a tie-break (ORDER BY created_at D) | SPARK |

## Lane Q: docs

File family: `docs/{openapi/secuura-api.yaml,MULTI-TENANCY.md,RLS-FAIL-CLOSED-PLAN.md,DEV-PROCESS.md}`

| ticket | pri | files it would touch | build summary | route |
|---|---|---|---|---|
| KS-723 | High | docs/openapi/secuura-api.yaml | declare the remaining ~157 routed-but-undocumented /api operations (GET /api/anchors/{id} first) (Declare the remaining ~157 routed-but-undocumented /api operations in ) | SONNET |
| KS-1035 | High | docs/DEV-PROCESS.md + board/GitHub ops | documentation item done; remaining are board/GitHub actions (dismiss stale approvals on #813, #785); NOT a code build (The merge gate cannot see a WITHDRAWN approval — #813 reads approved+c) | SPARK |
| KS-1036 | High | docs/DEV-PROCESS.md + Linear parenting | parent the 22 PR-bearing tickets into their streams, sweep unparented active tickets; board work, NOT a code build (The review-stream overlay covers 57 of 114 active tickets, and DEV-PRO) | SPARK |
| KS-1343 | Low | docs/MULTI-TENANCY.md, docs/RLS-FAIL-CLOSED-PLAN.md | five of eight doc notes (N-1286-3,5,6,9,10) (Multi-tenancy docs: eight non-blocking overstatements and Polish notes) | SPARK |

## Lane R1: preflight and audit baseline

File family: `scripts/{preflight,audit}`

| ticket | pri | files it would touch | build summary | route |
|---|---|---|---|---|
| KS-1707 | High | scripts/audit/audit-baseline.json | five rows expire together 2026-11-30: file and do the tailwind 4 / prisma upgrades or re-date; fuse not yet filed (Six baselined advisory rows lapse 2026-10-31 and 15 stale rows need re) | SONNET |
| KS-1209 | Low | scripts/audit/lock-discovery.mjs:283, scripts/preflight/preflight.sh | report a malformed (present) expires as malformed, not missing (Preflight's closing verdict says a run failed on the environment even ) | SPARK |
| KS-1613 | Low | scripts/preflight/preflight.sh, scripts/__tests__/ks1547_* | remaining items of the step-header denominator follow-up (items 1,2 done) (KS-1547 follow-up (PR #1552 gate): the empty/non-digit denominator abo) | SPARK |

## Lane R2: shared re-link guard

File family: `scripts/check-shared-relink.sh + scripts/__tests__/check_shared_relink*`

| ticket | pri | files it would touch | build summary | route |
|---|---|---|---|---|
| KS-937 | High | scripts/check-shared-relink.sh (+ its test) | F-A,F-B (MAJOR), F-D, F-F: case-insensitive awk parser, red-proof for clause A link target (KS-921 residue: the re-link guard's awk parser is still case-sensitive) | SONNET |
| KS-930 | Medium | scripts/check-shared-relink.sh (+ its test) | five Dockerfile shapes the guard cannot read, nginx final stage; heredoc case is a stated rule (KS-921 residues: five Dockerfile shapes the re-link guard cannot read,) | SONNET |
| KS-957 | Medium | scripts/__tests__/check_shared_relink_tooling_tokens.test.sh | F5 clause that cannot change the outcome, F6 derive the hand-written census figure (KS-930 round-2 gate residue: the guard and its suite write three claim) | SPARK |

## Lane R3: launcher and stack scripts

File family: `scripts/{bootstrap-env.sh,run-*.sh,smoke-test.sh,prisma-generate.cjs,spec-examples,check-compose-stack-safety.mjs,...}`

| ticket | pri | files it would touch | build summary | route |
|---|---|---|---|---|
| KS-1081 | High | scripts/bootstrap-env.sh, env.example, scripts/__tests__/ks1081_* | reconcile the two env templates (~39 vars) which is the ticket subject (five compose keys already declared) (CONFIG DRIFT: two tracked env templates disagree by ~39 vars — bootstr) | SONNET |
| KS-1033 | Medium | scripts/run-code-guards.sh, check-no-trust-header-reads.sh | guards 2 and 3 plus two guard-1 follow-ups (TRUST_HEADER_LINT_MODE default etc.) (KS-926 residue: the three guards that could NOT be wired, and what eac) | SONNET |
| KS-1558 | Medium | scripts/check-compose-stack-safety.mjs, start/stop-environment.sh, observability.sh, systemTest/akto/scripts/* | m3 and m5 of the KS-1355 gate follow-ups (m1,m2,m4 in); exact files UNMEASURED (KS-1355 gate follow-ups (#1526): two tamper survivors, the census shap) | SONNET |
| KS-1250 | Low | scripts/smoke-test.sh | make a full remote run remote-clean (gateway half done) (O-2: RUNBOOK §2.2 documents SMOKE_BASE_URL, but scripts/smoke-test.sh ) | SPARK |
| KS-1253 | Low | scripts/spec-examples/check/contract.mjs | allow-list shape for secret-name guard E7 stays OPEN by ruling (14 names closed) (Spec-example guard E7: the secret-name deny list in PREFIXED_UUID_RE i) | SONNET |
| KS-1456 | Low | scripts/run-migrations.sh:179 | finish the cut-off WARN sentence before the corrected failed-run message (Correct the failed-run message in run-migrations.sh (:187-188): it sti) | SPARK |
| KS-1497 | Low | scripts/prisma-generate.cjs | signals skipping cleanup and the other open items (2,4 done) (prisma-generate.cjs edge cases: signals skip the cleanup, a symlinked ) | SONNET |
| KS-1745 | Low | scripts/run-shell-suites.sh + its test | cell for the EMPTY-pgid branch of the signal trap (M3/M4 survive) (run-shell-suites.sh signal trap: the guard's EMPTY-pgid branch has no ) | SPARK |

## Lane R4: Testing jobs

File family: `Blockchain/Testing/jobs`

| ticket | pri | files it would touch | build summary | route |
|---|---|---|---|---|
| KS-1136 | Medium | Blockchain/Testing/jobs/09-aggregate-report.sh (outside Dev/) | item 2: treat a scan-failed image as failed not zero findings (Audit jobs: a per-image trivy failure reads as a CLEAN image in 04 (`/) | SPARK |

## Lane R5: systemTest

File family: `systemTest/{fixtures,performance,akto,playwright,__tests__,scripts}`

| ticket | pri | files it would touch | build summary | route |
|---|---|---|---|---|
| KS-969 | Medium | systemTest/fixtures/provision-actors.ts, fixtures/generated/actors.json, scripts/setup_api_key.py, docs/setup_guide.md | rest of the actor/credential path after item 1 (systemTest actor/credential path: provisioning is never invoked, so th) | SONNET |
| KS-973 | Medium | systemTest/fixtures/provision.ts, performance/tests/unit/fixtures/ | items 1-4 of the pre-suite step residue (5,6 done) (KS-969 round-1 gate residue: the pre-suite step and its own test suite) | SONNET |
| KS-1337 | Medium | systemTest/performance/runner/cli.ts, akto/tests/preSuiteSetup.ts, playwright/global-setup.ts | k6 runner pre-suite path from URL.pathname breaks on a space in the checkout path: remaining sites (k6 runner: the pre-suite path is taken from URL.pathname, so a checkou) | SONNET |
| KS-1560 | Medium | scripts/__tests__/ks1560_*, ks1347_*, systemTest/playwright/global-setup.ts | three residues listed on the ticket (M1,M2 done) (KS-1137 F-4 census missed a fourth suite (tenant_isolation), and the K) | SONNET |
| KS-1605 | Medium | systemTest/CLAUDE.md, docs/readme.md, systemTest/scripts/check-package-format.sh | Minors 1-4 of the KS-998 gate (item 5 done): .npmrc registry redirect etc. (KS-998 item 3 gate follow-ups (#1545): the three Minors of the Opus ga) | SONNET |
| KS-1300 | Low | systemTest/performance (k6 readYaml unit suite) | item 1: wire the unit suite into a gate (items 2-4 merged) (k6 readYaml adoption: the unit suite that proves it is run by no gate,) | SPARK |
| KS-1884 | Low | systemTest/__tests__/manifest_readers_agree.test.sh | optional did-not-run report for an empty driver answer (manifest_readers_agree.test.sh drivers discard stderr, so a tool failu) | SPARK |

## Lane X: CROSS-SERVICE (serial, last; each ticket spans the lanes above)

File family: `mixed: see per ticket`

Serial. Run each after the lanes it touches are idle (the per-ticket files say which).

| ticket | pri | files it would touch | build summary | route |
|---|---|---|---|---|
| KS-1000 | High | tsconfig.json of the services other than auth (UNMEASURED which) | item 3: sibling sweep so other services type-check their tests too (services/auth tsconfig EXCLUDES src/__tests__ — every 'tsc: 0 errors' ) | SONNET |
| KS-1845 | High | kyc/src/index.ts, api-gateway routes/proxy.ts, governance routes/governance.ts, transfer routes/delegations.ts, staking routes/stake.ts | file tickets or gate the four unlisted admin-labelled routes the 10-30 comment named (UNMEASURED which routes) (POST /api/kyc/:id/review has no role or owner check: any signed-in cal) | OPUS |
| KS-528 | Medium | frontend/admin, frontend/issuer, frontend/verifier, scripts/audit/audit-baseline.json | react-router v6 to v7 migration (3 advisories) (Frontends: react-router v6 → v7 migration (3 moderate client-runtime a) | SONNET |
| KS-629 | Medium | kyc/src/kyc.openapi.ts, kyc/src/index.ts, docs/openapi/secuura-api.yaml:4599 | spec and runtime disagree on livenessVideo: remove from both or implement (kyc `livenessVideo` is accepted by spec and runtime, then silently dis) | SONNET |
| KS-745 | Medium | api-gateway/src/routes/audit-export.ts, security/src/index.ts | goal unmet: gateway audit export calls /api/audit/logs which security does not serve (api-gateway audit export calls /api/audit/logs — a route the security ) | SONNET |
| KS-1490 | Medium | 102 files: scripts/generate-openapi.ts, docs/openapi/secuura-api.yaml, scripts/api.js, outlook-addin, gmail-addon | replace the deleted Container Apps host in the main body of files (three small fixes done) (102 tracked files still name a deleted Container Apps host: 22 shipped) | SONNET |
| KS-1536 | Medium | auth/src/routes/oauth.ts, issuerCerts.ts, api-gateway routes/platform.ts, middleware/auth.ts, routes/admin.ts | unify the seven divergent role lists into one vocabulary (groundwork PR 1779 landed) (One role vocabulary, seven divergent lists: platform_admin is a super-) | OPUS |
| KS-1579 | Medium | security/src/index.ts, originate/src/originate.openapi.ts, docs/openapi/secuura-api.yaml, originate connectorOrganisationErasure.ts | items 1,2,5 of the erase-connector round-6 follow-ups (3,4 done) (KS-695 erase-connector round 6 gate follow-ups (pull request 1497): de) | SONNET |
| KS-1600 | Medium | originate/src/__tests__/ks1594-*, security/src/index.ts | items 2 and 3 of the KS-1594 follow-ups (item 1 PR 1794 done) (KS-1594 follow-up (pull request 1547 round-2 gate): the non-string and) | SONNET |
| KS-965 | Low | 87 doc sites in 55 files (*.md, *.mdc, *.txt) | remove the retired admin credential from 85 remaining documentary sites (2 of 87 done) (87 documentary sites still publish the retired admin credential — wron) | SONNET |
| KS-1485 | Low | originate/src/services/anchorStateSync.ts:190, anchoring/src/index.ts | item 1: pin the placeholder txHash carry on the failed anchor blob (authoritativeTxHash accepts mock_batch_tx_, and nothing pins the place) | SPARK |
| KS-1752 | Low | api-gateway ks1531 test; item 2 files UNMEASURED (m365 mentioned) | item 2 is untouched (item 1 the declaration-pin note landed) (api-gateway unit suite: the ks1531 U2 cell pins the authedMethods set ) | SONNET |
| KS-1788 | Low | api-gateway + auth (exchange timeout reads as 401) | items 1,2: key-exchange timeout must not read as a downstream 401; two http cases (KS-1240 gate follow-ups (#1785): exchange timeout still reads as a dow) | SONNET |
| KS-1724 | None | packages/shared/src/index.ts (boundedJson) + every service mount; whatsapp-bot connector | request-size 7-day window and the whatsapp-bot connector remain; (priority none) (Request-body arrays are uncapped: a JSON array of failing elements cos) | SONNET |

## Same-file ordering inside lanes
- Lane A: `routes/auth.ts` (KS-1460 then KS-1968), `routes/oauth.ts` (KS-1150 then KS-1797).
- Lane B: `routes/verification.ts` (KS-1087, 1180, 1185, 1539, 1614), `routes/admin.ts` (KS-1262 then KS-1204), `index.ts` (KS-1505 then KS-1614).
- Lane C: `startup-migrations.ts` (KS-962 then KS-1128).
- Lane D1: `routes/documents.ts` (KS-1695 then KS-1509), `routes/certifications.ts` (KS-1695 then KS-1666).
- Lane R2: `check-shared-relink.sh` (KS-937, 930).
- Lane R5: `playwright/global-setup.ts` (KS-1337 then KS-1560), fixtures (KS-969 then KS-973).
- Lane R3 is internally parallel-safe (eight tickets on different files; KS-1558 files UNMEASURED and it may reach systemTest/akto/scripts, which lane R5 does not touch by file (R5 uses akto/tests/preSuiteSetup.ts), so run KS-1558 first and alone).
- Lane Q is internally parallel-safe (four different files; KS-1035/1036 are mostly board work).

## Overlap check
A basename check over lanes A to R5 flagged auth.ts (lane A routes/auth.ts vs lane C middleware/auth.ts), verification.ts (lane B gateway vs lane D1 originate) and index.ts (lanes B, E, H: three different services). All three are different directories, so no shared file. No full-path overlap was found. This is a string check of the inferred file lists, not a measurement of the diffs.

## Tickets whose remaining scope is unclear (re-read before briefing)
- KS-908 (PR 1319 merged; remaining UNMEASURED), KS-1676 (an Undecided row may need a ruling), KS-1804 and KS-1497 (excerpt did not name the remaining item), KS-1035 and KS-1036 (board work, not code), KS-1558 (files for m3/m5 UNMEASURED), KS-1407 (file UNMEASURED), KS-758 (file UNMEASURED).
