# Ornith candidates — derived 2026-09-17 05:20 from 313 KS Backlog/Todo tickets (read-only, unpaginated)

A CENSUS for the coordinator to brief from, easy → hard (Kam 2026-09-15 16:40 / 18:19). A ticket here is a candidate, not a task: read it, read the file at the tip, write `night/briefs/<id>.md`, then queue it. Auth-shaped titles are excluded (LAST); Peter/Stuart tickets and PR-attached tickets are excluded outright.

## T1 services (vitest, one file) — 28
- KS-1173 (P2) Flow verbs: add `note`, `certified` and `verified` to the lifecycle vocabulary ( — `services/anchoring/src/anchorSchema.ts`
- KS-1175 (P2) [resolved:basename, a HINT — read the file] Anchor / originate / lifecycle-event — `services/anchoring/src/anchorSchema.ts`
- KS-1184 (P2) workflow-approve persists the instance approved before the forward, so a refused — `services/api-gateway/src/routes/verification.ts`
- KS-678 (P2) [resolved:basename, a HINT — read the file] #568 publishes 17 URLs on secuura.io — `scripts/openapi-examples/synthesize.ts`
- KS-683 (P2) Anchor-status standoff: a consumer repolls anchors K reports as terminally faile — `services/anchoring/src/index.ts`
- KS-947 (P2) [resolved:basename, a HINT — read the file] KS-733 gate blindness (F3+F4): the p — `services/api-gateway/src/routes/proxy.ts`
- KS-953 (P2) CLASS: editing api-gateway/src/index.ts silently reddens packages/shared, and no — `services/api-gateway/src/index.ts`
- KS-955 (P2) [resolved:basename, a HINT — read the file] A fresh clone cannot run the four pl — `services/auth/src/services/accountLockout.ts`
- KS-987 (P2) [resolved:route, a HINT — read the file] A deploy that rsyncs the OpenAPI spec a — `services/api-gateway/src/index.ts`
- KS-1143 (P3) [resolved:basename, a HINT — read the file] ks781 LEG F guard walk: a MENTION of — `services/api-gateway/src/routes/admin.ts`
- KS-1168 (P3) userRepo.ts: ILIKE search on encrypted PII columns can never match — :1017 and : — `services/auth/src/repositories/userRepo.ts`
- KS-1176 (P3) api-gateway: connector-key principals (verificationLevel 'api_key') fail meetsVe — `services/api-gateway/src/services/enforcement.ts`
- KS-1186 (P3) userRepo.ts: five sibling reads still return fromRow unawaited inside try, so a  — `services/auth/src/repositories/userRepo.ts`
- KS-579 (P3) Per-person platform-admin identities — the shared seeded admin cannot carry attr — `services/api-gateway/src/routes/platform.ts`
- KS-581 (P3) register-connector: volume alerting, rate limit, and correlation of refused re-k — `services/api-gateway/src/routes/platform.ts`
- KS-627 (P3) Implement real wallet signature verification (CIP-8/COSE + address binding) — ne — `services/wallet-connector/src/types/index.ts`
- KS-746 (P3) Security events carry no tenant at all — KS-743 had to gate them platform-only,  — `services/security/src/index.ts`
- KS-758 (P3) [resolved:route, a HINT — read the file] Connector erasure: three permanent fail — `services/api-gateway/src/routes/proxy.ts`
- KS-784 (P3) [resolved:route, a HINT — read the file] POST /api/teams/webhook-config fails th — `services/m365-integration/src/index.ts`
- KS-837 (P3) [resolved:route, a HINT — read the file] Published prose drifts from the routes  — `services/api-gateway/src/middleware/contentType.ts`
- KS-839 (P3) Security: an allowedScopes of ['*'] bypasses the invalid_scope refusal entirely  — `services/auth/src/services/oauth.ts`
- KS-851 (P3) [resolved:route, a HINT — read the file] KS-386 residues from the round-2 gate:  — `services/kyc/src/index.ts`
- KS-915 (P3) A clean stack has no supported way to obtain its first privileged account — `services/auth/src/routes/auth.ts`
- KS-934 (P3) [resolved:route, a HINT — read the file] m365 /api/teams/notify: a serial per-ro — `services/m365-integration/src/index.ts`
- KS-986 (P3) [resolved:basename, a HINT — read the file] The published admin credential survi — `services/auth/src/repositories/userRepo.ts`
- KS-1125 (P4) api-gateway startup-migrations: the tenant-failure guard `if (outcome.failed > 0 — `services/api-gateway/src/startup-migrations.ts`
- KS-1145 (P4) ks949 suite coverage (KS-950 / KS-962, #973): ID3's capture half has no size ass — `services/api-gateway/src/startup-migrations.ts`
- KS-748 (P4) [resolved:route, a HINT — read the file] svc_api_keys.organization_id is not a t — `services/security/src/index.ts`

## T2 tooling (systemTest/*, one file) — 0

## T2b bash (bash_patch — one script + a *.test.sh beside the reference) — 7
- KS-1148 (P2) CI-runner environment gaps (one class, two jobs): `Security Scanning` runs `audi — `scripts/run-shell-suites.sh`
- KS-998 (P2) KS-989 gate residue: the formatting gate fails OPEN on missing deps and reads th — `.githooks/pre-push`
- KS-1163 (P3) start-secuura.sh never waits for five default-profile, healthchecked services —  — `Start_Up/start-secuura.sh`
- KS-630 (P3) Wire the status-page XSS probe into preflight (or decide not to) — it runs today — `scripts/preflight/preflight.sh`
- KS-789 (P3) CONTRIBUTING.md justifies the hook's degradation and its --no-verify bypass with — `.githooks/pre-push`
- KS-813 (P3) "PREFLIGHT PASSED" is unconditional — step() only prints a banner, and skipped l — `scripts/preflight/preflight.sh`
- KS-1162 (P4) Three retired GitHub workflows bake slot-2/3/4 port literals (6982/7182/6732…) i — `scripts/stack_env.sh`

## T3 jest services (originate, governance) — 3
- KS-1019 (P3) [Question] The document's whole `blockchain` block is published as z.unknown() — — `services/originate/src/originate.openapi.ts`
- KS-759 (P3) tenantId is read through two `as unknown as` casts because it is not on JwtPaylo — `services/originate/src/middleware/auth.ts`
- KS-1084 (P0) READ ONLY / unverified: the gateway's own Authorization-only calls to originate  — `services/originate/src/index.ts`

## T4 docs (doc_patch) — 3
- KS-709 (P2) [resolved:docs, a HINT — the ticket MENTIONS the file] Akto reports a PASS for a test that executed NOTHING — 'clean 0 / not-applicable — `docs/DEV-PROCESS.md`
- KS-770 (P2) [resolved:docs, a HINT — the ticket MENTIONS the file] Review stream: API contract and the four platform suites — `docs/DEV-PROCESS.md`
- KS-965 (P4) [resolved:docs, a HINT — the ticket MENTIONS the file] 87 documentary sites still publish the retired admin credential — wrong rather t — `docs/BROWSER-TESTING-GUIDE.md`

## T5 multi-file / later — 30
- KS-1187 (P1) Security: an absolute-form request target bypasses the KS-843 erasure door's sco — `services/api-gateway/src/routes/proxy.ts`, `services/originate/src/routes/gdpr.ts`
- KS-1051 (P2) develop is RED on the services/originate jest suite and NOTHING catches it — the — `scripts/preflight/preflight.sh`, `.githooks/pre-push`
- KS-1055 (P2) Per-tenant databases never receive the file migrations — CORE_MIGRATIONS FORCEs  — `services/api-gateway/src/startup-migrations.ts`, `services/tenant-provisioning/src/index.ts`
- KS-1100 (P2) [resolved:basename, a HINT — read the file] Kintsugi deploy 4554b25e2: four live — `services/auth/src/routes/mfa.ts`, `services/auth/src/repositories/userRepo.ts`, `services/anchoring/src/chainHealthStatus.ts`
- KS-485 (P2) Security review — plan, methodology & handover (Platform K) — `services/api-gateway/src/routes/notifications.ts`, `services/originate/src/repositories/documentRepo.ts`, `services/originate/src/index.ts`
- KS-491 (P2) Review F — Edge, WAF, DDoS & anti-automation — `services/api-gateway/src/middleware/rateLimitEnforce.ts`, `services/auth/src/routes/auth.ts`
- KS-576 (P2) Bulk re-key: one admin-authorised rotate across a named set of externalRefs — `services/api-gateway/src/routes/platform.ts`, `services/security/src/index.ts`, `packages/shared/src/db/tenant-guc.ts`
- KS-607 (P2) [resolved:route, a HINT — read the file] GET /api/anchors/{id} and verify report — `services/api-gateway/src/middleware/csrf.ts`, `services/mcp-server/src/api-client.ts`, `services/originate/src/middleware/errorHandler.ts`
- KS-624 (P2) prism issues VCs with random bytes as the Ed25519 proof and verifies them as pas — `services/vc-issuer/src/routes/credentials.ts`, `services/prism/src/index.ts`
- KS-696 (P2) [resolved:basename, a HINT — read the file] Akto pr-scan is non-deterministic —  — `services/originate/src/routes/gdpr.ts`, `services/originate/src/routes/systemErrors.ts`
- KS-730 (P2) Security: 71 inline handlers still return err.message verbatim off-production —  — `services/originate/src/routes/adminConfig.ts`, `services/originate/src/routes/gdpr.ts`, `services/originate/src/routes/systemErrors.ts`
- KS-735 (P2) [resolved:route, a HINT — read the file] Verify results show the user nothing ab — `services/api-gateway/src/middleware/csrf.ts`, `services/mcp-server/src/api-client.ts`, `services/originate/src/middleware/errorHandler.ts`
- KS-753 (P2) Timestamping fail-closed: a mock TSA fallback must not report verified: true (ex — `services/timestamping/src/tsa/qualified-tsa.ts`, `services/timestamping/src/index.ts`
- KS-967 (P2) Neither credential guard can see a value in a .env.example — one scans the wrong — `scripts/check-no-default-passwords.sh`, `scripts/preflight/no-tracked-credentials.sh`
- KS-1039 (P3) [resolved:route, a HINT — read the file] tests/e2e 2.4.6 'SQL injection in regis — `services/api-gateway/src/index.ts`, `services/api-gateway/src/middleware/csrf.ts`
- KS-1116 (P3) [resolved:basename, a HINT — read the file] KS-1020 item 2: which subject OWNS a — `services/vc-issuer/src/routes/presentations.ts`, `services/vc-issuer/src/vc-issuer.openapi.ts`, `services/vc-issuer/src/routes/credentials.ts`
- KS-1174 (P3) api-gateway collapses every API-key failure into 401 'Invalid API key' — forward — `services/security/src/index.ts`, `services/api-gateway/src/middleware/auth.ts`
- KS-526 (P3) KMS: move platform wallet mnemonic to Key Vault (KS-326 follow-up) — `services/anchoring/src/index.ts`, `services/anchoring/src/cardano/wallet.ts`, `packages/shared/src/vault/key-vault.ts`
- KS-580 (P3) Append-only recovery audit held outside the estate being recovered — `services/api-gateway/src/routes/platform.ts`, `services/security/src/index.ts`
- KS-621 (P3) Document reads are scoped by tenant and owner, never by organization — cross-org — `services/originate/src/repositories/documentRepo.ts`, `services/originate/src/routes/documents.ts`
- KS-625 (P3) /presentations/verify reports a presentation verified without checking the holde — `services/vc-issuer/src/routes/presentations.ts`, `services/vc-issuer/src/routes/credentials.ts`
- KS-658 (P3) The demo VM runs every service as NODE_ENV=development while the code names "dem — `services/auth/src/index.ts`, `services/api-gateway/src/index.ts`
- KS-807 (P3) The control-byte guard cannot see a raw body — findNulBytePath returns null for  — `services/billing/src/index.ts`, `packages/shared/src/middleware/request-limits.ts`
- KS-870 (P3) Every ADMITTED erasure authenticates twice — the door's chain and the catch-all  — `services/api-gateway/src/routes/proxy.ts`, `services/api-gateway/src/middleware/auth.ts`
- KS-954 (P3) KS-858 residue: the repeated-slash collapse does not complete for the /api/billi — `services/api-gateway/src/routes/proxy.ts`, `services/api-gateway/src/middleware/normalisePath.ts`
- KS-1082 (P4) The Playwright env guard added in #896 reads config/ only — the variable breakin — `systemTest/fixtures/provision-actors.ts`, `systemTest/playwright/global-setup.ts`
- KS-1090 (P4) [resolved:basename, a HINT — read the file] api-gateway + originate: tsc never t — `services/api-gateway/src/routes/proxy.ts`, `services/originate/src/utils/gatewayProvenance.ts`
- KS-1106 (P4) [resolved:route, a HINT — read the file] Verifier shows 'Verification Failed' /  — `services/api-gateway/src/middleware/csrf.ts`, `services/mcp-server/src/api-client.ts`, `services/originate/src/middleware/errorHandler.ts`
- KS-1153 (P4) L7 gate records (#918/#924/#925): run-code-guards.sh --check-unreached advisory  — `.githooks/pre-push`, `scripts/run-code-guards.sh`, `scripts/preflight/preflight.sh`
- KS-1083 (P0) GATEWAY_VOUCH_SECRET: nothing provisions it and no deploy order or rotation is w — `services/api-gateway/src/routes/verification.ts`, `packages/shared/src/db/tenant-context.ts`, `scripts/bootstrap-env.sh`

## HELD (READY_* or done.md PASS) — 59
- KS-1011 KS-666 stack marker reads "unknown" for owner/branch/commit/started_at whenever 
- KS-1018 Security/correctness: three verification-store reads swallow EVERY DB error with
- KS-1028 KS-754 gate F-1 (MAJOR): a step-12 throw skips the USER_ERASED fan-out AFTER the
- KS-1031 KS-754 gate F-4: DEPLOY CONDITION — apply 048 BEFORE rolling the originate image
- KS-1033 KS-926 residue: the three guards that could NOT be wired, and what each needs fi
- KS-1034 check-stack-safety.sh resolves the WRONG repo root inside a git hook and calls p
- KS-1035 The merge gate cannot see a WITHDRAWN approval — #813 reads approved+clean again
- KS-1036 The review-stream overlay covers 57 of 114 active tickets, and DEV-PROCESS still
- KS-1037 The NO-FORCE-PUSH rule exists only in .githooks/pre-push and in no .md — documen
- KS-1040 Push preflight leg 4 reports 'a published path is unroutable' when the real caus
- KS-1045 KINTSUGI-DEV-SERVER-PLAN.md still says the VM "has NOT been created" — Stage B r
- KS-1047 pre-push:230 names the stack-dependent legs as (3, 4, 7); measured they are 3, 4
- KS-1049 A PR's Test Evidence must state whether the preflight RAN — the hook skips syste
- KS-1050 users.ts:933 answers success: true over a 0-row profile update — KS-943 changes 
- KS-1072 The latest-anchor selector documents a `confirmedAt` tiebreak it does not implem
- KS-1074 The poller/reconcile blob writers also erase threadToken — on the CONFIRM/heal p
- KS-1081 CONFIG DRIFT: two tracked env templates disagree by ~39 vars — bootstrap-env.sh 
- KS-1089 run-shell-suites.sh polish from #953's tier-2 gate: make `--list` survive a tree
- KS-1093 check-stack-safety.sh 6f reports a FALSE red once a real Playwright run exists —
- KS-1097 Merge-rule docs after #957: the v4 footer and two gate statements gloss TESTED w
- KS-1101 Gateway health aggregates read anchoring's HTTP status only, so its degraded bod
- KS-1108 Akto harness: loadSecretsYml() parses config/secrets.yml with no catch — the KS-
- KS-1117 k6 YAML loader: a BOM immediately followed by a comment is a marked syntax error
- KS-1118 POST /api/verification/verify: the `documentHash`-over-`hash` precedence is unpi
- KS-1120 GET /api/presentations/:id exact-or-404: the memory-path PREFIX class and the DB
- KS-1121 Security: credentialRepo.getById resolves a credential by SUBSTRING (LIKE '%id%'
- KS-1123 api-gateway verify: an empty-string / 0 / false anchor status is one edit (`??`→
- KS-1127 run-shell-suites.sh counts an exit-0 SKIP as `passed` — a suite that ran 0 of it
- KS-1133 verify-hash precedence: v1 hash-LAST, v2 hash-FIRST — document the split on both
- KS-1139 Bare arithmetic-command `((X++))` under `set -e` — exits 1 at 0 and bash ≥ 4.1 e
- KS-1158 L3a gate records (#912 r2 / #937): the placeholder-hash anchoredAt carry keys on
- KS-1160 originate POST /api/webhooks persists the RAW url where PATCH persists the norma
- KS-1164 gate/report.ts writeGateReport overwrites the input summary when --summary does 
- KS-1171 Guard 3's re-poll reads a MIXED window as ABSENT — one early "not found" then an
- KS-1172 Add `note` and `verified` to the lifecycle vocabulary (LIFECYCLE_VERBS + LIFECYC
- KS-1179 safeOutboundRequest tests: no cell pins DNS-layer classification, ks932 cells de
- KS-1180 ks1073 verify cells: the tier guard is not a tier witness, the _source compariso
- KS-1181 KS-727 error-handler guard: corpus-1 canary cells cannot witness a hit, and the 
- KS-1182 demo-service errorHandler: unchecked err.status (NaN crashes the process, 200/30
- KS-1185 KS-1183 gate follow-ups: validate the approve forward timeout override, and pin 
- KS-629 kyc `livenessVideo` is accepted by spec and runtime, then silently discarded — n
- KS-692 Security: /api/status revoke/unrevoke has no tenant ownership check — an ISSUER_
- KS-747 Spec drift: GET /api/security/keys declares no parameters while the handler requ
- KS-794 verify-file returns `fileSize` on every 200 and neither response schema declares
- KS-864 Dead-estate pointers in RUNTIME SOURCE outside deployment/azure — system-status.
- KS-865 check-no-latest-tags.sh silently skips a missing input — it scans 5 of the 6 fil
- KS-866 Merge protocol: the server-side `sha=` pin protects the PR head, not the base — 
- KS-884 pre-push resolves the bare name `develop`, so a TAG named develop beats the bran
- KS-887 KS-869 test defect (mine): the WRITE-half column-list pin can be satisfied by th
- KS-888 dbSaveApiKey SWALLOWS a failed INSERT — POST /api/keys answers 201 for a key tha
- KS-890 Runbook: a code-first deploy leg must use `docker compose up -d --no-deps <svc>`
- KS-908 connectorId persists but is invisible through the API — POST and GET both return
- KS-910 Preflight leg 12 executes ZERO suite cells — it is a reachability check, so with
- KS-958 The re-link guard matches the JS runtime name case-sensitively — every UPPERCASE
- KS-960 Two schema sources disagree on whether users.email is unique — a statement valid
- KS-972 start-secuura.sh banner prints admin@secuura.com / admin123, which has returned 
- KS-974 Published bound vs runtime bound on rate-limit scope: /check enforces code UNITS
- KS-975 rateLimitScope tri-state: a MALFORMED `sub` silently became a 403 on the ungated
- KS-976 Rate-limit refusals name the wrong field: 400 says "Key required" when the key w

## SET ASIDE with a recorded reason — 27 (re-read only if the ticket's updatedAt moved)
- KS-1063 — decision-class: its own words say the design question comes first (updated 2026-09-09)
- KS-1076 — likely already fixed at M55 (docblock present since ec61abf8e/0882f7661) — measure with eslint in a tool-mode clone; item 2 is a Claude seat's (updated 2026-09-13)
- KS-1088 — decision-class: 'filing only; decide whether the runner should enforce isolation' — a ruling, not a patch (updated 2026-09-11)
- KS-1111 — a masking guard with an unruled fix-shape (a)/(b), security-adjacent (updated 2026-09-12)
- KS-1112 — two files: option 1 reds ks1029's A1 cell (2026-09-15 18:45) (updated 2026-09-13)
- KS-1113 — an e2e spec under tests/e2e — no Playwright checker yet (updated 2026-09-13)
- KS-1114 — decision-class (spec vs implementation of a title strategy) (updated 2026-09-13)
- KS-1119 — multi-tenant security surface (updated 2026-09-13)
- KS-1128 — the seed's pg is a require inside the function (updated 2026-09-13)
- KS-1129 — three services, anchoring index.ts listens on import (updated 2026-09-16)
- KS-1132 — services/auth — security surface (Kam 16:40: auth LAST) (updated 2026-09-13)
- KS-1135 — diagnosis-first: which of the six suites spawns tsx (direct vs shared preamble) is UNMEASURED; the fix shape is prose (updated 2026-09-13)
- KS-1142 — a test refactor with no product tamper (updated 2026-09-13)
- KS-1159 — a guard widening with three fixture files — later tier (updated 2026-09-14)
- KS-590 — verification.ts, security-adjacent (updated 2026-09-13)
- KS-755 — diagnosis-first (which side is wrong is unmeasured) (updated 2026-09-10)
- KS-757 — blocked by the ticket's own measurement (updated 2026-09-08)
- KS-777 — tracker ticket — all four findings FIXED on #795; a board close (updated 2026-09-05)
- KS-808 — item 1 is a recorded decision; items 2–3 need psql → a Claude seat (updated 2026-09-07)
- KS-849 — kyc has no in-process driver (app.listen at import) (updated 2026-09-06)
- KS-880 — two-file refactor (Claude seat) (updated 2026-09-06)
- KS-889 — a measurement/ruling ticket, not a patch (updated 2026-09-06)
- KS-897 — the subject IS a test file — the bash tier's B3 wants ONE new test beside a reference (updated 2026-09-06)
- KS-906 — a test file → a Claude seat (updated 2026-09-06)
- KS-979 — comment-only: no cell can red it (updated 2026-09-07)
- KS-980 — decision-class (a second DB role or a claim correction) (updated 2026-09-07)
- KS-981 — lives only on the frozen #892 branch (updated 2026-09-07)

## EXCLUDED by predicate — 156
- KS-1000 — has a PR attached
- KS-1003 — auth-shaped title (LAST, Kam 16:40)
- KS-1005 — auth-shaped title (LAST, Kam 16:40)
- KS-1006 — auth-shaped title (LAST, Kam 16:40)
- KS-1009 — auth-shaped title (LAST, Kam 16:40)
- KS-101 — on Peter/Stuart
- KS-1010 — names no product file (after basename/docs/route resolution)
- KS-1012 — names no product file (after basename/docs/route resolution)
- KS-1014 — names no product file (after basename/docs/route resolution)
- KS-1015 — auth-shaped title (LAST, Kam 16:40)
- KS-1017 — auth-shaped title (LAST, Kam 16:40)
- KS-1022 — names no product file (after basename/docs/route resolution)
- KS-1023 — names no product file (after basename/docs/route resolution)
- KS-1025 — names no product file (after basename/docs/route resolution)
- KS-1030 — names no product file (after basename/docs/route resolution)
- KS-1032 — auth-shaped title (LAST, Kam 16:40)
- KS-1038 — auth-shaped title (LAST, Kam 16:40)
- KS-1042 — on Peter/Stuart
- KS-1044 — names no product file (after basename/docs/route resolution)
- KS-1048 — names no product file (after basename/docs/route resolution)
- KS-1053 — auth-shaped title (LAST, Kam 16:40)
- KS-1054 — names no product file (after basename/docs/route resolution)
- KS-1079 — names no product file (after basename/docs/route resolution)
- KS-1080 — names no product file (after basename/docs/route resolution)
- KS-1085 — names no product file (after basename/docs/route resolution)
- KS-1091 — auth-shaped title (LAST, Kam 16:40)
- KS-1102 — names no product file (after basename/docs/route resolution)
- KS-1104 — names no product file (after basename/docs/route resolution)
- KS-1105 — auth-shaped title (LAST, Kam 16:40)
- KS-1107 — auth-shaped title (LAST, Kam 16:40)
- KS-1110 — names no product file (after basename/docs/route resolution)
- KS-1115 — names no product file (after basename/docs/route resolution)
- KS-1124 — auth-shaped title (LAST, Kam 16:40)
- KS-1131 — names no product file (after basename/docs/route resolution)
- KS-1134 — names no product file (after basename/docs/route resolution)
- KS-1136 — names no product file (after basename/docs/route resolution)
- KS-1137 — names no product file (after basename/docs/route resolution)
- KS-1138 — names no product file (after basename/docs/route resolution)
- KS-1140 — names no product file (after basename/docs/route resolution)
- KS-1141 — names no product file (after basename/docs/route resolution)
- KS-1144 — names no product file (after basename/docs/route resolution)
- KS-1146 — auth-shaped title (LAST, Kam 16:40)
- KS-1147 — names no product file (after basename/docs/route resolution)
- KS-1149 — auth-shaped title (LAST, Kam 16:40)
- KS-1152 — auth-shaped title (LAST, Kam 16:40)
- KS-1154 — names no product file (after basename/docs/route resolution)
- KS-1155 — names no product file (after basename/docs/route resolution)
- KS-1156 — auth-shaped title (LAST, Kam 16:40)
- KS-1157 — auth-shaped title (LAST, Kam 16:40)
- KS-1161 — names no product file (after basename/docs/route resolution)
- KS-1177 — auth-shaped title (LAST, Kam 16:40)
- KS-1178 — names no product file (after basename/docs/route resolution)
- KS-135 — on Peter/Stuart
- KS-139 — on Peter/Stuart
- KS-188 — on Peter/Stuart
- KS-239 — on Peter/Stuart
- KS-263 — names no product file (after basename/docs/route resolution)
- KS-304 — has a PR attached
- KS-305 — names no product file (after basename/docs/route resolution)
- KS-329 — auth-shaped title (LAST, Kam 16:40)
- KS-339 — names no product file (after basename/docs/route resolution)
- KS-492 — on Peter/Stuart
- KS-502 — on Peter/Stuart
- KS-525 — on Peter/Stuart
- KS-528 — names no product file (after basename/docs/route resolution)
- KS-530 — names no product file (after basename/docs/route resolution)
- KS-562 — names no product file (after basename/docs/route resolution)
- KS-565 — has a PR attached
- KS-568 — on Peter/Stuart
- KS-571 — on Peter/Stuart
- KS-572 — on Peter/Stuart
- KS-582 — names no product file (after basename/docs/route resolution)
- KS-583 — names no product file (after basename/docs/route resolution)
- KS-588 — on Peter/Stuart
- KS-591 — names no product file (after basename/docs/route resolution)
- KS-593 — has a PR attached
- KS-595 — names no product file (after basename/docs/route resolution)
- KS-598 — names no product file (after basename/docs/route resolution)
- KS-602 — names no product file (after basename/docs/route resolution)
- KS-603 — names no product file (after basename/docs/route resolution)
- KS-604 — names no product file (after basename/docs/route resolution)
- KS-605 — names no product file (after basename/docs/route resolution)
- KS-608 — on Peter/Stuart
- KS-61 — on Peter/Stuart
- KS-618 — auth-shaped title (LAST, Kam 16:40)
- KS-619 — auth-shaped title (LAST, Kam 16:40)
- KS-623 — auth-shaped title (LAST, Kam 16:40)
- KS-636 — names no product file (after basename/docs/route resolution)
- KS-638 — names no product file (after basename/docs/route resolution)
- KS-648 — names no product file (after basename/docs/route resolution)
- KS-651 — names no product file (after basename/docs/route resolution)
- KS-655 — names no product file (after basename/docs/route resolution)
- KS-668 — auth-shaped title (LAST, Kam 16:40)
- KS-699 — names no product file (after basename/docs/route resolution)
- KS-716 — names no product file (after basename/docs/route resolution)
- KS-723 — names no product file (after basename/docs/route resolution)
- KS-724 — auth-shaped title (LAST, Kam 16:40)
- KS-725 — names no product file (after basename/docs/route resolution)
- KS-738 — names no product file (after basename/docs/route resolution)
- KS-744 — auth-shaped title (LAST, Kam 16:40)
- KS-749 — has a PR attached
- KS-752 — names no product file (after basename/docs/route resolution)
- KS-756 — auth-shaped title (LAST, Kam 16:40)
- KS-760 — names no product file (after basename/docs/route resolution)
- KS-761 — names no product file (after basename/docs/route resolution)
- KS-765 — names no product file (after basename/docs/route resolution)
- KS-766 — names no product file (after basename/docs/route resolution)
- KS-767 — names no product file (after basename/docs/route resolution)
- KS-768 — names no product file (after basename/docs/route resolution)
- KS-769 — names no product file (after basename/docs/route resolution)
- KS-772 — names no product file (after basename/docs/route resolution)
- KS-782 — auth-shaped title (LAST, Kam 16:40)
- KS-783 — names no product file (after basename/docs/route resolution)
- KS-785 — names no product file (after basename/docs/route resolution)
- KS-787 — auth-shaped title (LAST, Kam 16:40)
- KS-793 — auth-shaped title (LAST, Kam 16:40)
- KS-805 — auth-shaped title (LAST, Kam 16:40)
- KS-810 — auth-shaped title (LAST, Kam 16:40)
- KS-811 — names no product file (after basename/docs/route resolution)
- KS-812 — names no product file (after basename/docs/route resolution)
- KS-824 — auth-shaped title (LAST, Kam 16:40)
- KS-825 — auth-shaped title (LAST, Kam 16:40)
- KS-829 — names no product file (after basename/docs/route resolution)
- KS-834 — auth-shaped title (LAST, Kam 16:40)
- KS-836 — auth-shaped title (LAST, Kam 16:40)
- KS-838 — names no product file (after basename/docs/route resolution)
- KS-840 — auth-shaped title (LAST, Kam 16:40)
- KS-846 — names no product file (after basename/docs/route resolution)
- KS-855 — auth-shaped title (LAST, Kam 16:40)
- KS-872 — names no product file (after basename/docs/route resolution)
- KS-896 — names no product file (after basename/docs/route resolution)
- KS-902 — names no product file (after basename/docs/route resolution)
- KS-903 — names no product file (after basename/docs/route resolution)
- KS-918 — auth-shaped title (LAST, Kam 16:40)
- KS-919 — names no product file (after basename/docs/route resolution)
- KS-925 — auth-shaped title (LAST, Kam 16:40)
- KS-928 — has a PR attached
- KS-938 — auth-shaped title (LAST, Kam 16:40)
- KS-939 — names no product file (after basename/docs/route resolution)
- KS-940 — names no product file (after basename/docs/route resolution)
- KS-944 — auth-shaped title (LAST, Kam 16:40)
- KS-948 — has a PR attached
- KS-951 — auth-shaped title (LAST, Kam 16:40)
- KS-956 — names no product file (after basename/docs/route resolution)
- KS-957 — names no product file (after basename/docs/route resolution)
- KS-959 — names no product file (after basename/docs/route resolution)
- KS-964 — has a PR attached
- KS-977 — auth-shaped title (LAST, Kam 16:40)
- KS-982 — names no product file (after basename/docs/route resolution)
- KS-983 — on Peter/Stuart
- KS-984 — on Peter/Stuart
- KS-985 — on Peter/Stuart
- KS-990 — names no product file (after basename/docs/route resolution)
- KS-995 — names no product file (after basename/docs/route resolution)
- KS-996 — names no product file (after basename/docs/route resolution)
- KS-997 — names no product file (after basename/docs/route resolution)


## SEARCH 17e (11:2x commission) — block appended 2026-09-17 11:28 AEST
<!-- REJECTION TABLE, measured 2026-09-17 11:22–11:29 AEST by the search17e commission — do NOT re-derive these.
     NOTE: the 05:20 derive dropped the older rejection blocks; they survive in git 3e68f4132 (SEARCH 2) and in briefs/NEXT_SEARCH_2026-09-17{,b,c,d}.REPORT.md. The 17c/17d tables are not repeated here.
     Tip: origin develop fa887f382 (ls-remote 11:24:28, 11:28:14; did not move). Linear re-pulled 11:23:49: 34 KS Backlog/Todo updated since 2026-09-16 00:00 AEST (positive control: KS-1199 present). Open PRs 11:27:24: 21 / 107 paths.
     FITS from this search: NONE. Nothing briefed, nothing queued.
     KS-1200  owner decision: "The owner decides which schema source is authoritative for anchor_store" (10 CREATE TABLE sources); no patch until ruled · unblocks: Kam rules the authoritative source · read
     KS-1203  owner decision: "apply the allow-list to the resolved default type, or require a restricted connector to name a type"; gateway + originate default (documents.ts:565) · unblocks: that ruling · read
     KS-1185 F1  two fix shapes ("throw at construction, or fall back"); the listener-before-setTimeout half is a MOVE (re-adds a tip line, forbidden) and its failure is an unhandled 'error' event / process exit, not an assertion red; verification.ts is KS-1202's measure lane · unblocks: a ruling on throw-vs-fallback, then a Claude seat · read
     KS-1185 F2 / F3  each is an either/or (doc comment OR wall-clock bound; skip the log OR reword it) · unblocks: a pick · read
     KS-1186  4 of the 5 '-' lines are the SAME text at the tip (userRepo.ts :446 :512 :585 :627, grep -x count 4; only :594 legacy arm unique) — breaks the UNIQUE-'-'-line brief rule (the KS-1121 drift) and A3b matches sites by TEXT, so it cannot tell which of the four was edited. A :594-only partial would leave getUserByEmail's normal arm (:585, 9 lines above) unawaited in the same function, and the ticket wants one test pass + one gate on the login paths · unblocks: A3b keyed by line number (with the owed A3e line+text fix), or a Claude seat (5 one-word edits, one PR). Partition was clear: 0 open PRs and 0 held 09-16/17 READYs touch userRepo.ts (control: 45 READY test/users.ts paths) · measured
     KS-1191  design decision for the audit trail's owner (normalisation + unrouted action), edge forwarding untested · unblocks: the ruling · read
     KS-1192  no residue: READY_KS-1192 covers both rows (production witness + INSUFFICIENT_SCOPE) · read (brief report)
     KS-1193 F3  KS-1018 item 3 (does the in-memory fallback exist) still open: KS-1018 In Progress, 21:14Z comment "Nothing is built", no ruling · unblocks: item 3 closes "fallback stays" · read
     KS-1188 F3  "a product decision" (burn order vs retry wording); F1/F2 are held READYs · read
     KS-1196  routes/admin.ts:682 collides with seat A's KS-1204 (cites routes/admin.ts); also two shapes (randomUUID OR refuse an existing key) · unblocks: KS-1204 merges + a pick · measured (tip :682) + read
     KS-1190  "Do not make it fail closed yet. Two measurements come first" (stored level strings, who writes types) · unblocks: those measurements · read
     KS-1189  R-5 closed by #1011; H29 remainder is "decide whether the attempted-email capture should work at all" · unblocks: the ruling · read
     KS-1197  two files (middleware/auth.ts = open #1017, + verification.ts handler) · unblocks: #1017 merged, then a Claude seat · read
     KS-1198  middleware/auth.ts (open #1017), refuse-or-attach two shapes, connector auth surface · unblocks: #1017 + a pick · read
     KS-744   middleware/auth.ts:377 is in open #1017 (seat A merging now) · unblocks: #1017 merges; re-measure the line, then a 1-edit brief may fit · read
     KS-1194 / KS-1202 / KS-1204  seat A's queue (users.ts build; verification.ts measure-first; admin.ts) · partition
     KS-1123 KS-1129 KS-864 KS-960  PR attached / held · KS-1172 KS-1173 KS-1179 KS-1180 KS-1181 KS-1182 KS-1199 KS-1201 held (READY or reallocated) · KS-1175 KS-1177 KS-1178 KS-1184 KS-772 recorded refusals (SEARCH 2 / 17c)
     POOL STATE: all 34 recently-updated Backlog/Todo tickets are held, in seat A's lane, or carry a recorded rejection. Next search should widen to: (1) KS-744 the moment #1017 merges (one guarded header line, api-gateway vitest); (2) KS-1186 if A3b is keyed by line number; (3) the older T1 rows whose updatedAt moved since their recorded refusal.
-->

## ROUTED BY WEDNESDAY 2026-09-17 12:07 — KS-744 briefed (FITS, PASS 7/7 strict at d7e95cd9f) but NOT queued
| id | reason | what unblocks it |
|---|---|---|
| KS-744 | a PRODUCT edit to `services/api-gateway/src/middleware/auth.ts` (:389/:394 header guards): auth product edits stay out of the local-model week grant until Kam names them (EXPIRING-GRANTS, Wednesday's 09-15 reading), AND seat A's KS-1207 (B) fix edits the same file next — two agents never on one file | routed to seat A's Claude queue AFTER KS-1207 (same file, serial); the brief `night/briefs/KS-744.md` is usable by that seat as its spec; the residual (tokens missing role/userId still 500) needs a ruling — PR says "Refs KS-744" |
