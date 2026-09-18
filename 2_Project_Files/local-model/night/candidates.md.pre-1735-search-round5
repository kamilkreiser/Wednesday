# Ornith candidates — derived 2026-09-18 06:51 from 340 KS Backlog/Todo tickets (read-only, unpaginated)

A CENSUS for the coordinator to brief from, easy → hard (Kam 2026-09-15 16:40 / 18:19). A ticket here is a candidate, not a task: read it, read the file at the tip, write `night/briefs/<id>.md`, then queue it. Auth-shaped titles are excluded (LAST); Peter/Stuart tickets and PR-attached tickets are excluded outright.

## T1 services (vitest, one file) — 30
- ~~KS-1175~~ ⛔ **REJECTED for Ornith 2026-09-18 10:4x: it's a FEATURE, not a defect, and it writes to an IMMUTABLE PUBLIC LEDGER.** It adds seven identity fields to the Cardano anchor record across eight endpoints and asks for a design choice (`metadata.identity` or flat). The on-chain contract belongs to PS-869, and KS-721's similar field needed Kam's ruling plus a deploy gate. It would also redden the existing exact-key-set cells in `anchorSchema.test.ts`. **Signature class: irreversible, so it needs Kam.** (was: KS-1175 (P2) [resolved:basename, a HINT — read the file] Anchor / originate / lifecycle-event — `services/anchoring/src/anchorSchema.ts`
- KS-1233 (P2) In Redis mode platform-settings expires 24 h after the last admin write, which e — `services/api-gateway/src/services/redis.ts`
- ~~KS-678~~ ⛔ **REJECTED 10:4x: the named defect is ALREADY FIXED at the tip** (`synthesize.ts:203` now returns `https://example.com/resource`). What's left is a new rule in `scripts/spec-examples/check/rules-global.mjs`, a directory with no tests, plus two questions only PeterD can answer (whether we own `secuura.io`, and which host is acceptable). (was: KS-678 (P2) [resolved:basename, a HINT — read the file] #568 publishes 17 URLs on secuura.io — `scripts/openapi-examples/synthesize.ts`
- KS-683 (P2) Anchor-status standoff: a consumer repolls anchors K reports as terminally faile — `services/anchoring/src/index.ts`
- ~~KS-947~~ ⛔ **REJECTED 10:4x: it's about rate-limit parity on nine MFA operations, so it's AUTH (last)**, and it needs a static read of `index.ts` mount order, which is poor on reachability. (was: KS-947 (P2) [resolved:basename, a HINT — read the file] KS-733 gate blindness (F3+F4): the p — `services/api-gateway/src/routes/proxy.ts`
- KS-953 (P2) CLASS: editing api-gateway/src/index.ts silently reddens packages/shared, and no — `services/api-gateway/src/index.ts`
- KS-955 (P2) [resolved:basename, a HINT — read the file] A fresh clone cannot run the four pl — `services/auth/src/services/accountLockout.ts`
- KS-987 (P2) [resolved:route, a HINT — read the file] A deploy that rsyncs the OpenAPI spec a — `services/api-gateway/src/index.ts`
- ~~KS-1143~~ ⛔ **REJECTED 11:0x: the code to fix lives INSIDE a test file** (`routerParserAnalysis` in `packages/shared/src/__tests__/ks781-p3-3-body-parser-order.test.ts`), not in `admin.ts`, so the harness's product-file-plus-new-test shape can't express it. It's also the control-byte guard's static gate. (was: KS-1143 (P3) [resolved:basename, a HINT — read the file] ks781 LEG F guard walk: a MENTION of — `services/api-gateway/src/routes/admin.ts`
- KS-1168 (P3) userRepo.ts: ILIKE search on encrypted PII columns can never match — :1017 and : — `services/auth/src/repositories/userRepo.ts`
- ~~KS-1190~~ ⛔ **PULLED 2026-09-18 10:1x — NOT Ornith-shaped, and not a rebrief candidate.** Its fix REDDENS an existing cell, `ks1176-connector-key-level-ranks-as-none.test.ts` → *"KS-1176 C — an unknown REQUIRED level is unchanged (KS-1190, **recorded not endorsed**)"*. That test deliberately records today's behaviour as intentional, so "fixing" KS-1190 contradicts a recorded decision. **This needs a ruling on whether KS-1176's decision still stands — not another model attempt.** Evidence: `runs/2026-09-18_ks1190-ornith35b-night/checker.out` (A6 NEW reds include the KS-1176 cell). (was: api-gateway meetsVerificationLevel fails open on an unknown REQUIRED level: an o — `services/api-gateway/src/services/enforcement.ts`
- ~~KS-1222~~ ⛔ **EXHAUSTED FOR ORNITH 2026-09-18 10:33 (original + its ONE rebrief) → a CLAUDE seat if pursued.** Rebrief failed A4 with the **CONTROL cell also red at the tip** (a benign `report.pdf` JSON upload is not forwarded either), so **the harness does not reach `proxy.ts`**. That's a reachability problem through the middleware stack (`index.ts:421` json mount → `:1094` proxy, plus `authenticateToken(true)`), not a model weakness. The brief-writer named this exact residual risk in advance. **The multipart half is out of scope anyway:** the 415 comes from `contentType.ts:137`, and fixing it there would WIDEN the KS-439 defence its own KS-781 comment reserves for its owners. Evidence: `runs/2026-09-18_ks1222-ornith35b-night2/checker.out`. (was: POST /api/documents/upload never reaches the gateway's blocked-extension / MIME  — `services/api-gateway/src/routes/proxy.ts`
- KS-1230 (P3) PUT /api/admin/settings stores a connector's allowedDocumentTypes in any shape - — `services/api-gateway/src/routes/admin.ts`
- KS-1234 (P3) POST /api/v1/documents with application/json never answers, and /api/documents a — `services/api-gateway/src/index.ts`
- KS-1236 (P3) Approving a stale PENDING verification request after the subject's level rose an — `services/auth/src/routes/users.ts`
- KS-579 (P3) Per-person platform-admin identities — the shared seeded admin cannot carry attr — `services/api-gateway/src/routes/platform.ts`
- KS-581 (P3) register-connector: volume alerting, rate limit, and correlation of refused re-k — `services/api-gateway/src/routes/platform.ts`
- KS-627 (P3) Implement real wallet signature verification (CIP-8/COSE + address binding) — ne — `services/wallet-connector/src/types/index.ts`
- KS-746 (P3) Security events carry no tenant at all — KS-743 had to gate them platform-only,  — `services/security/src/index.ts`
- KS-758 (P3) [resolved:route, a HINT — read the file] Connector erasure: three permanent fail — `services/api-gateway/src/routes/proxy.ts`
- ~~KS-784~~ ⛔ **REJECTED 11:0x: nothing to fix yet.** The ticket says "no fix attempted; not investigated beyond establishing that it is real." (was: KS-784 (P3) [resolved:route, a HINT — read the file] POST /api/teams/webhook-config fails th — `services/m365-integration/src/index.ts`
- KS-837 (P3) [resolved:route, a HINT — read the file] Published prose drifts from the routes  — `services/api-gateway/src/middleware/contentType.ts`
- ~~KS-851~~ ⛔ **REJECTED 11:0x: four items across `init.sql`, `docker/init/04` and `kyc/src/index.ts`**, reachable only through the app. G-2 needs a transaction around real DB writes, and it's a KYC identity surface. (was: KS-851 (P3) [resolved:route, a HINT — read the file] KS-386 residues from the round-2 gate:  — `services/kyc/src/index.ts`
- KS-915 (P3) A clean stack has no supported way to obtain its first privileged account — `services/auth/src/routes/auth.ts`
- ~~KS-934~~ ⛔ **REJECTED 11:0x: the fix shape is an open design choice** (LIMIT/paging, an aggregate deadline, or moving dispatch off the request path), and its red-first is a TIMING bound (N rows × 10 s against a destination that never answers), the same class as KS-1234. (was: KS-934 (P3) [resolved:route, a HINT — read the file] m365 /api/teams/notify: a serial per-ro — `services/m365-integration/src/index.ts`
- KS-986 (P3) [resolved:basename, a HINT — read the file] The published admin credential survi — `services/auth/src/repositories/userRepo.ts`
- KS-1125 (P4) api-gateway startup-migrations: the tenant-failure guard `if (outcome.failed > 0 — `services/api-gateway/src/startup-migrations.ts`
- ~~KS-1145~~ ⛔ **REJECTED 10:4x: the fix is a bash suite against a real PostgreSQL** (`ks949_main_seed_idempotence.test.sh`). It's not vitest and has no direct call. (was: KS-1145 (P4) ks949 suite coverage (KS-950 / KS-962, #973): ID3's capture half has no size ass — `services/api-gateway/src/startup-migrations.ts`
- KS-1197 (P4) [resolved:basename, a HINT — read the file] A non-string verificationLevel claim — `services/auth/src/repositories/userRepo.ts`
- KS-748 (P4) [resolved:route, a HINT — read the file] svc_api_keys.organization_id is not a t — `services/security/src/index.ts`

## T2 tooling (systemTest/*, one file) — 0

## T2b bash (bash_patch — one script + a *.test.sh beside the reference) — 5
- KS-998 (P2) KS-989 gate residue: the formatting gate fails OPEN on missing deps and reads th — `.githooks/pre-push`
- KS-1163 (P3) start-secuura.sh never waits for five default-profile, healthchecked services —  — `Start_Up/start-secuura.sh`
- ~~KS-630~~ ⛔ **REJECTED 11:0x: the fix is a DECISION** (wire the XSS probe into the shared pre-push gate, "or decide not to"). It would also change the push path for Peter and Stuart, and it's a security probe. (was: KS-630 (P3) Wire the status-page XSS probe into preflight (or decide not to) — it runs today — `scripts/preflight/preflight.sh`
- KS-789 (P3) CONTRIBUTING.md justifies the hook's degradation and its --no-verify bypass with — `.githooks/pre-push`
- KS-1209 (P4) Preflight's closing verdict says a run failed on the environment even when other — `scripts/preflight/preflight.sh`

## T3 jest services (originate, governance) — 5
- KS-1019 (P3) [Question] The document's whole `blockchain` block is published as z.unknown() — — `services/originate/src/originate.openapi.ts`
- KS-1203 (P3) A connector restricted by allowedDocumentTypes can still create the default DOCU — `services/originate/src/routes/documents.ts`
- KS-1228 (P3) A refused request still writes an action_provenance row: handleOnBehalfOf runs b — `services/originate/src/routes/documents.ts`
- KS-759 (P3) tenantId is read through two `as unknown as` casts because it is not on JwtPaylo — `services/originate/src/middleware/auth.ts`
- KS-1084 (P0) READ ONLY / unverified: the gateway's own Authorization-only calls to originate  — `services/originate/src/index.ts`

## T4 docs (doc_patch) — 1
- KS-965 (P4) [resolved:docs, a HINT — the ticket MENTIONS the file] 87 documentary sites still publish the retired admin credential — wrong rather t — `docs/BROWSER-TESTING-GUIDE.md`

## T5 multi-file / later — 33
- KS-1051 (P2) develop is RED on the services/originate jest suite and NOTHING catches it — the — `scripts/preflight/preflight.sh`, `.githooks/pre-push`
- KS-1055 (P2) Per-tenant databases never receive the file migrations — CORE_MIGRATIONS FORCEs  — `services/api-gateway/src/startup-migrations.ts`, `services/tenant-provisioning/src/index.ts`
- KS-1100 (P2) [resolved:basename, a HINT — read the file] Kintsugi deploy 4554b25e2: four live — `services/auth/src/routes/mfa.ts`, `services/auth/src/repositories/userRepo.ts`, `services/anchoring/src/chainHealthStatus.ts`
- KS-1231 (P2) A connector allow-list fails open when platform-settings integrations is not a c — `services/api-gateway/src/routes/verification.ts`, `services/api-gateway/src/services/health.ts`
- KS-485 (P2) Security review — plan, methodology & handover (Platform K) — `services/api-gateway/src/routes/notifications.ts`, `services/originate/src/repositories/documentRepo.ts`, `services/originate/src/index.ts`
- KS-491 (P2) Review F — Edge, WAF, DDoS & anti-automation — `services/api-gateway/src/middleware/rateLimitEnforce.ts`, `services/auth/src/routes/auth.ts`
- KS-576 (P2) Bulk re-key: one admin-authorised rotate across a named set of externalRefs — `services/api-gateway/src/routes/platform.ts`, `services/security/src/index.ts`, `packages/shared/src/db/tenant-guc.ts`
- KS-607 (P2) [resolved:route, a HINT — read the file] GET /api/anchors/{id} and verify report — `services/api-gateway/src/middleware/csrf.ts`, `services/mcp-server/src/api-client.ts`, `services/originate/src/middleware/errorHandler.ts`
- KS-624 (P2) prism issues VCs with random bytes as the Ed25519 proof and verifies them as pas — `services/vc-issuer/src/routes/credentials.ts`, `services/prism/src/index.ts`
- KS-696 (P2) [resolved:basename, a HINT — read the file] Akto pr-scan is non-deterministic —  — `services/originate/src/routes/gdpr.ts`, `services/originate/src/routes/systemErrors.ts`
- KS-735 (P2) [resolved:route, a HINT — read the file] Verify results show the user nothing ab — `services/api-gateway/src/middleware/csrf.ts`, `services/mcp-server/src/api-client.ts`, `services/originate/src/middleware/errorHandler.ts`
- KS-753 (P2) Timestamping fail-closed: a mock TSA fallback must not report verified: true (ex — `services/timestamping/src/tsa/qualified-tsa.ts`, `services/timestamping/src/index.ts`
- KS-967 (P2) Neither credential guard can see a value in a .env.example — one scans the wrong — `scripts/check-no-default-passwords.sh`, `scripts/preflight/no-tracked-credentials.sh`
- KS-1039 (P3) [resolved:route, a HINT — read the file] tests/e2e 2.4.6 'SQL injection in regis — `services/api-gateway/src/index.ts`, `services/api-gateway/src/middleware/csrf.ts`
- KS-1116 (P3) [resolved:basename, a HINT — read the file] KS-1020 item 2: which subject OWNS a — `services/vc-issuer/src/routes/presentations.ts`, `services/vc-issuer/src/vc-issuer.openapi.ts`, `services/vc-issuer/src/routes/credentials.ts`
- KS-1174 (P3) api-gateway collapses every API-key failure into 401 'Invalid API key' — forward — `services/security/src/index.ts`, `services/api-gateway/src/middleware/auth.ts`
- KS-1189 (P3) Audit log (KS-871 gate R-3/R-5): H29 attemptedEmail is never written for proxied — `services/api-gateway/src/middleware/audit.ts`, `services/api-gateway/src/index.ts`
- KS-1200 (P3) anchor_store's (document_id, network) unique is declared only by migration 031 a — `services/api-gateway/src/startup-migrations.ts`, `services/anchoring/src/index.ts`
- KS-1223 (P3) A client x-wallet-address is forwarded past the gateway strip, and referrals.ts: — `services/api-gateway/src/utils/trustHeaders.ts`, `services/referral/src/routes/referrals.ts`, `services/api-gateway/src/routes/verification.ts`
- KS-1232 (P3) GET /api/connector/info tells a connector [] (all types permitted) for a stored  — `services/api-gateway/src/services/health.ts`, `services/mcp-server/src/tools/info.ts`, `services/mcp-server/src/http-server.ts`
- KS-526 (P3) KMS: move platform wallet mnemonic to Key Vault (KS-326 follow-up) — `services/anchoring/src/index.ts`, `services/anchoring/src/cardano/wallet.ts`, `packages/shared/src/vault/key-vault.ts`
- KS-580 (P3) Append-only recovery audit held outside the estate being recovered — `services/api-gateway/src/routes/platform.ts`, `services/security/src/index.ts`
- KS-621 (P3) Document reads are scoped by tenant and owner, never by organization — cross-org — `services/originate/src/repositories/documentRepo.ts`, `services/originate/src/routes/documents.ts`
- KS-625 (P3) /presentations/verify reports a presentation verified without checking the holde — `services/vc-issuer/src/routes/presentations.ts`, `services/vc-issuer/src/routes/credentials.ts`
- KS-658 (P3) The demo VM runs every service as NODE_ENV=development while the code names "dem — `services/auth/src/index.ts`, `services/api-gateway/src/index.ts`
- KS-807 (P3) The control-byte guard cannot see a raw body — findNulBytePath returns null for  — `services/billing/src/index.ts`, `packages/shared/src/middleware/request-limits.ts`
- KS-870 (P3) Every ADMITTED erasure authenticates twice — the door's chain and the catch-all  — `services/api-gateway/src/routes/proxy.ts`, `services/api-gateway/src/middleware/auth.ts`
- KS-954 (P3) KS-858 residue: the repeated-slash collapse does not complete for the /api/billi — `services/api-gateway/src/routes/proxy.ts`, `services/api-gateway/src/middleware/normalisePath.ts`
- KS-1082 (P4) The Playwright env guard added in #896 reads config/ only — the variable breakin — `systemTest/fixtures/provision-actors.ts`, `systemTest/playwright/global-setup.ts`
- KS-1106 (P4) [resolved:route, a HINT — read the file] Verifier shows 'Verification Failed' /  — `services/api-gateway/src/middleware/csrf.ts`, `services/mcp-server/src/api-client.ts`, `services/originate/src/middleware/errorHandler.ts`
- KS-1153 (P4) L7 gate records (#918/#924/#925): run-code-guards.sh --check-unreached advisory  — `.githooks/pre-push`, `scripts/run-code-guards.sh`, `scripts/preflight/preflight.sh`
- KS-1206 (P4) originate admin API-key mint writes no connector_id and an unclamped rate_limit: — `services/originate/src/routes/adminConfig.ts`, `services/security/src/index.ts`
- KS-1083 (P0) GATEWAY_VOUCH_SECRET: nothing provisions it and no deploy order or rotation is w — `services/api-gateway/src/routes/verification.ts`, `packages/shared/src/db/tenant-context.ts`, `scripts/bootstrap-env.sh`

## ⚠ ALSO NAMED IN A HELD READY's HEADLINE — 23 (verify before briefing; surfaced, NOT suppressed)
- KS-1004 — named in READY_KS-1158-R1_ornith35b-q4_JEST-PASS-7of7_2026-09-15.diff.md
- KS-1020 — named in READY_KS-1121_ornith35b-q4_VITEST-MODIFYINPLACE-REANCHORED-PASS-7of7_2026-09-16.diff.md
- KS-1046 — named in READY_KS-1047_ornith35b-q4_BASHPATCH-RECOUNTED-PASS-7of7_2026-09-16.diff.md
- KS-1069 — named in READY_KS-1130-E3twin_ornith35b-q4_TESTONLY-PASS-7of7_2026-09-15.diff.md
- KS-1072 — named in READY_KS-1199_ornith35b-q4_TESTONLY-TAMPER-PASS-7of7_2026-09-17.diff.md
- KS-1073 — named in READY_KS-1123-F2_ornith35b-q8_TESTONLY-PASS-7of7_2026-09-15.diff.md, READY_KS-1130-E1twin_ornith35b-q4_TESTONLY-PASS-7of7_2026-09-15.diff.md, READY_KS-1158-R1_ornith35b-q4_JEST-PASS-7of7_2026-09-15.diff.md
- KS-1092 — named in READY_KS-1097-B_ornith35b-q4_DOCPATCH-REFLOW-INFERRED-PASS-7of7_2026-09-15.diff.md
- KS-1099 — named in READY_KS-1108_ornith35b-q4_TOOLING-AKTO-PASS-7of7_2026-09-15.diff.md
- KS-1173 — named in READY_KS-1172-A3_ornith35b-q4_JEST-MODIFYINPLACE-THREE-VERBS-PASS-7of7_2026-09-15.diff.md, READY_KS-1172-B3_ornith35b-q4_MODIFYINPLACE-THREE-VERBS-PASS-7of7_2026-09-15.diff.md, READY_KS-1172-D3_ornith35b-q4_DOCPATCH-THREE-VERBS-PASS-6of6_2026-09-15.diff.md
- KS-202 — named in READY_KS-974-B_ornith35b-q4_PASS-7of7_2026-09-15.diff.md
- KS-217 — named in READY_KS-1193-F1_ornith35b-q4_TESTONLY-TAMPER-PASS-7of7_2026-09-17.diff.md
- KS-253 — named in READY_KS-999_ornith35b-q4_RECHECK-PASS-7of7_2026-09-15.diff.md
- KS-430 — named in READY_KS-629-B_ornith35b-q4_VITEST-PASS-7of7_2026-09-16.diff.md
- KS-666 — named in READY_KS-1011_ornith35b-q4_BASHPATCH-NEWTEST-PASS-7of7_2026-09-16.diff.md
- KS-691 — named in READY_KS-1047_ornith35b-q4_BASHPATCH-RECOUNTED-PASS-7of7_2026-09-16.diff.md
- KS-727 — named in READY_KS-1181-F3_ornith35b-q4_TESTONLY-TAMPER-PASS-7of7_2026-09-17.diff.md, READY_KS-1181-F3w_ornith35b-q4_comment-PASS-9of9_2026-09-17.diff.md
- KS-754 — named in READY_KS-1028_ornith35b-q4_JEST-PASS-7of7_2026-09-15.diff.md, READY_KS-1031_ornith35b-q4_BASHPATCH-NEWTEST-PASS-7of7_2026-09-16.diff.md
- KS-835 — named in READY_KS-1156-A2_ornith35b-q4_comment-PASS-9of9_2026-09-17.diff.md
- KS-869 — named in READY_KS-887_ornith35b-q4_TESTONLY-MODIFYINPLACE-PASS-7of7_2026-09-16.diff.md
- KS-930 — named in READY_KS-958_ornith35b-q4_BASHPATCH-REANCHORED-RECOUNTED-PASS-7of7_2026-09-16.diff.md
- KS-932 — named in READY_KS-1179-F1_ornith35b-q4_TESTONLY-TAMPER-PASS-7of7_2026-09-17.diff.md
- KS-966 — named in READY_KS-972_ornith35b-q4_BASHPATCH-REANCHORED-PASS-7of7_2026-09-16.diff.md
- KS-999 — named in READY_KS-1186_ornith35b-q4_AUTH-5SITE-LINEKEYED-PASS-7of7_2026-09-17.diff.md

## HELD (READY_* or done.md PASS) — 81
- KS-1009 Security: GET /api/auth/wallet/status returns userId + role to ANY anonymous cal
- KS-1011 KS-666 stack marker reads "unknown" for owner/branch/commit/started_at whenever 
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
- KS-1074 The poller/reconcile blob writers also erase threadToken — on the CONFIRM/heal p
- KS-1081 CONFIG DRIFT: two tracked env templates disagree by ~39 vars — bootstrap-env.sh 
- KS-1089 run-shell-suites.sh polish from #953's tier-2 gate: make `--list` survive a tree
- KS-1090 api-gateway + originate: tsc never type-checks #951's three wiring tests, and th
- KS-1093 check-stack-safety.sh 6f reports a FALSE red once a real Playwright run exists —
- KS-1097 Merge-rule docs after #957: the v4 footer and two gate statements gloss TESTED w
- KS-1108 Akto harness: loadSecretsYml() parses config/secrets.yml with no catch — the KS-
- KS-1117 k6 YAML loader: a BOM immediately followed by a comment is a marked syntax error
- KS-1118 POST /api/verification/verify: the `documentHash`-over-`hash` precedence is unpi
- KS-1120 GET /api/presentations/:id exact-or-404: the memory-path PREFIX class and the DB
- KS-1121 Security: credentialRepo.getById resolves a credential by SUBSTRING (LIKE '%id%'
- KS-1123 api-gateway verify: an empty-string / 0 / false anchor status is one edit (`??`→
- KS-1127 run-shell-suites.sh counts an exit-0 SKIP as `passed` — a suite that ran 0 of it
- KS-1133 verify-hash precedence: v1 hash-LAST, v2 hash-FIRST — document the split on both
- KS-1139 Bare arithmetic-command `((X++))` under `set -e` — exits 1 at 0 and bash ≥ 4.1 e
- KS-1140 ks879 guard: the 🔴 cell walks the tree on its own (`offendersUnder(DEV_ROOT)` :1
- KS-1152 L5 gate records (#799/#880/#985): jwt.ts citation ×5, security log title, dist t
- KS-1156 AUTH4 gate records (#983 r2 / #984 r2 / #986 / #987): H-limiter MACHINE_AUTH_MET
- KS-1158 L3a gate records (#912 r2 / #937): the placeholder-hash anchoredAt carry keys on
- KS-1160 originate POST /api/webhooks persists the RAW url where PATCH persists the norma
- KS-1164 gate/report.ts writeGateReport overwrites the input summary when --summary does 
- KS-1171 Guard 3's re-poll reads a MIXED window as ABSENT — one early "not found" then an
- KS-1172 Add `note` and `verified` to the lifecycle vocabulary (LIFECYCLE_VERBS + LIFECYC
- KS-1179 safeOutboundRequest tests: no cell pins DNS-layer classification, ks932 cells de
- KS-1181 KS-727 error-handler guard: corpus-1 canary cells cannot witness a hit, and the 
- KS-1182 demo-service errorHandler: unchecked err.status (NaN crashes the process, 200/30
- KS-1185 KS-1183 gate follow-ups: validate the approve forward timeout override, and pin 
- KS-1186 userRepo.ts: five sibling reads still return fromRow unawaited inside try, so a 
- KS-1188 #1013 gate findings (KS-999): the getUserById route-level 503 and its log line a
- KS-1192 ks871-real-app-canonical-audit-rows production cell does not pin production mode
- KS-1193 #1015 gate findings (KS-1018): the message-form pool timeout, the review route's
- KS-1196 admin POST /api/admin/document-types ids are dt-${Date.now()}: two creates in on
- KS-1199 ks1072 verify cells pin no verdict on a tie whose rows differ in status: a compa
- KS-1201 bootstrap_login_diagnosis.test.sh leaks its 4 login stubs on every run: start_st
- KS-1205 api-gateway per-key limiter follow-up (KS-1195 gates): a JWT claim can name a ke
- KS-1212 ks1187 tests: no cell pins that the erasure door reads its own router's caseSens
- KS-1217 ks1050 C1 pins only the helper message prefix plus a 3-phrase denylist - a not-a
- KS-1219 OAuth /authorize answers 500 server_error for an array-valued scope (repeated qu
- KS-1220 ks839 cells pin padded wildcards with ASCII separators only - a second tokenizer
- KS-1221 ks744 cells never test a falsy claim - a verificationLevel of '' or null must fo
- KS-1227 ks1072 postTier2's anchor-store witness counts every stub request, leaks its lis
- KS-1229 ks1213 cells: ten tampers stay green - a refused issue can mint a holder stub or
- KS-623 Test-token env guard is asymmetric: the gateway fails closed on an unset NODE_EN
- KS-629 kyc `livenessVideo` is accepted by spec and runtime, then silently discarded — n
- KS-692 Security: /api/status revoke/unrevoke has no tenant ownership check — an ISSUER_
- KS-730 Security: 71 inline handlers still return err.message verbatim off-production — 
- KS-747 Spec drift: GET /api/security/keys declares no parameters while the handler requ
- KS-794 verify-file returns `fileSize` on every 200 and neither response schema declares
- KS-855 The OAuth `AVAILABLE_SCOPES` list is a second, divergent scope vocabulary — deri
- KS-864 Dead-estate pointers in RUNTIME SOURCE outside deployment/azure — system-status.
- KS-865 check-no-latest-tags.sh silently skips a missing input — it scans 5 of the 6 fil
- KS-866 Merge protocol: the server-side `sha=` pin protects the PR head, not the base — 
- KS-884 pre-push resolves the bare name `develop`, so a TAG named develop beats the bran
- KS-887 KS-869 test defect (mine): the WRITE-half column-list pin can be satisfied by th
- KS-888 dbSaveApiKey SWALLOWS a failed INSERT — POST /api/keys answers 201 for a key tha
- KS-890 Runbook: a code-first deploy leg must use `docker compose up -d --no-deps <svc>`
- KS-908 connectorId persists but is invisible through the API — POST and GET both return
- KS-910 Preflight leg 12 executes ZERO suite cells — it is a reachability check, so with
- KS-928 The demo-seed gate's predicate is tested but its CALL SITE is not — delete admin
- KS-938 Security: "MFA disabled" leaves the TOTP seed and hashed backup codes in the row
- KS-944 The gateway's auth gate reads the spec's security: [] — nothing pins the four pu
- KS-958 The re-link guard matches the JS runtime name case-sensitively — every UPPERCASE
- KS-960 Two schema sources disagree on whether users.email is unique — a statement valid
- KS-972 start-secuura.sh banner prints admin@secuura.com / admin123, which has returned 
- KS-974 Published bound vs runtime bound on rate-limit scope: /check enforces code UNITS
- KS-975 rateLimitScope tri-state: a MALFORMED `sub` silently became a 403 on the ungated
- KS-976 Rate-limit refusals name the wrong field: 400 says "Key required" when the key w
- KS-979 KS-597's own bind test file repeats two claims that were corrected in the produc

## SET ASIDE with a recorded reason — 33 (re-read only if the ticket's updatedAt moved)
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
- KS-1148 — its own words: 'Fixing either is a .github/workflows/ edit — Kam-class; nothing here is changed by the seat that filed this' (updated 2026-09-14)
- KS-1159 — a guard widening with three fixture files — later tier (updated 2026-09-14)
- KS-1162 — three .github/workflows/ files (Kam-class) AND decision-class ('Fix direction: Either 1 … or …') (updated 2026-09-14)
- KS-1173 — ALREADY SHIPPED inside READY_KS-1172-B3 ('KS-1172 + KS-1173 PART B') — NOT visible to a held-check that keys on the READY filename's ticket id, which is how it keeps being re-picked (updated 2026-09-16)
- KS-1184 — decision-class: the ticket's own words are 'A design call beside KS-1087 item 2, not a fix round on #1008' with two shapes offered (updated 2026-09-16)
- KS-1191 — decision-class: 'Not built; Backlog. This is a design decision for the audit trail's owner, not a one-line fix' — two choices, and the edge behaviour is NOT TESTED (updated 2026-09-16)
- KS-590 — verification.ts, security-adjacent (updated 2026-09-13)
- KS-709 — its own 'Done means' requires reproduction from a real run, not a unit test — beyond the local model (updated 2026-09-10)
- KS-755 — diagnosis-first (which side is wrong is unmeasured) (updated 2026-09-10)
- KS-757 — blocked by the ticket's own measurement (updated 2026-09-08)
- KS-770 — not a doc edit — the body is a review-stream test pass for Peter; the docs/ path came from a MENTION, not an edit target (updated 2026-09-14)
- KS-777 — tracker ticket — all four findings FIXED on #795; a board close (updated 2026-09-05)
- KS-808 — item 1 is a recorded decision; items 2–3 need psql → a Claude seat (updated 2026-09-07)
- KS-849 — kyc has no in-process driver (app.listen at import) (updated 2026-09-06)
- KS-880 — two-file refactor (Claude seat) (updated 2026-09-06)
- KS-889 — a measurement/ruling ticket, not a patch (updated 2026-09-06)
- KS-897 — the subject IS a test file — the bash tier's B3 wants ONE new test beside a reference (updated 2026-09-06)
- KS-906 — a test file → a Claude seat (updated 2026-09-06)
- KS-980 — decision-class (a second DB role or a claim correction) (updated 2026-09-07)
- KS-981 — lives only on the frozen #892 branch (updated 2026-09-07)

## EXCLUDED by predicate — 152
- KS-1000 — has a PR attached
- KS-1003 — auth-shaped title (LAST, Kam 16:40)
- KS-1005 — auth-shaped title (LAST, Kam 16:40)
- KS-1006 — auth-shaped title (LAST, Kam 16:40)
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
- KS-1141 — names no product file (after basename/docs/route resolution)
- KS-1144 — names no product file (after basename/docs/route resolution)
- KS-1146 — auth-shaped title (LAST, Kam 16:40)
- KS-1147 — names no product file (after basename/docs/route resolution)
- KS-1149 — auth-shaped title (LAST, Kam 16:40)
- KS-1154 — names no product file (after basename/docs/route resolution)
- KS-1155 — names no product file (after basename/docs/route resolution)
- KS-1157 — auth-shaped title (LAST, Kam 16:40)
- KS-1161 — names no product file (after basename/docs/route resolution)
- KS-1177 — auth-shaped title (LAST, Kam 16:40)
- KS-1178 — names no product file (after basename/docs/route resolution)
- KS-1198 — auth-shaped title (LAST, Kam 16:40)
- KS-1208 — auth-shaped title (LAST, Kam 16:40)
- KS-1210 — auth-shaped title (LAST, Kam 16:40)
- KS-1214 — auth-shaped title (LAST, Kam 16:40)
- KS-1216 — names no product file (after basename/docs/route resolution)
- KS-1218 — names no product file (after basename/docs/route resolution)
- KS-1224 — names no product file (after basename/docs/route resolution)
- KS-1225 — auth-shaped title (LAST, Kam 16:40)
- KS-1226 — names no product file (after basename/docs/route resolution)
- KS-1235 — auth-shaped title (LAST, Kam 16:40)
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
- KS-749 — has a PR attached
- KS-752 — names no product file (after basename/docs/route resolution)
- KS-756 — auth-shaped title (LAST, Kam 16:40)
- KS-760 — names no product file (after basename/docs/route resolution)
- KS-761 — names no product file (after basename/docs/route resolution)
- KS-765 — names no product file (after basename/docs/route resolution)
- KS-766 — names no product file (after basename/docs/route resolution)
- KS-767 — names no product file (after basename/docs/route resolution)
- KS-768 — names no product file (after basename/docs/route resolution)
- KS-772 — names no product file (after basename/docs/route resolution)
- KS-782 — auth-shaped title (LAST, Kam 16:40)
- KS-783 — names no product file (after basename/docs/route resolution)
- KS-785 — names no product file (after basename/docs/route resolution)
- KS-787 — auth-shaped title (LAST, Kam 16:40)
- KS-805 — auth-shaped title (LAST, Kam 16:40)
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
- KS-872 — names no product file (after basename/docs/route resolution)
- KS-896 — names no product file (after basename/docs/route resolution)
- KS-902 — names no product file (after basename/docs/route resolution)
- KS-903 — names no product file (after basename/docs/route resolution)
- KS-918 — auth-shaped title (LAST, Kam 16:40)
- KS-919 — names no product file (after basename/docs/route resolution)
- KS-925 — auth-shaped title (LAST, Kam 16:40)
- KS-939 — names no product file (after basename/docs/route resolution)
- KS-940 — names no product file (after basename/docs/route resolution)
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


## 🔎 ORNITH-TRIAGED CANDIDATES — 30 class A, **UNVERIFIED: read the ticket before briefing** (added 2026-09-18 09:3x)

Produced by the local model (`predicate_classify`, 2 batches, 87 tickets) over the tickets this file EXCLUDED as *'names no product file'*. **Coverage checked by hand: 87 sent, 87 classified, 0 missing, 0 invented** — the run's own checker returned CHECKER_NO_RESULT because Wednesday's hand-built input lacked the `tip` key it wants, so the grading below is Wednesday's, not the harness's.

**This is a CLASSIFICATION LIST, which is a representation of the tickets and NOT an instruction** (`learnings/2026-09-07_a-classification-list-is-a-representation-not-an-instruction.md`). Every row is a lead to be checked at the ticket and the tip, never a brief input. The model's own words are kept so you can judge its reasoning rather than inherit its verdict.

⚠ **Rows whose reason names MORE THAN ONE file are flagged `[MULTI?]` — the predicate asked for exactly one, so those are the model's weakest calls.** A row naming only a `.test.` file is flagged `[TEST?]`: the predicate says a test file is not the product file unless the ticket is explicitly test-only.

- KS-1224 — root package.json with overrides.postcss pin named as single fix target
- KS-1218 — constraints.txt under systemTest/schemathesis named as sole product file to edit
- KS-1161 — Blockchain/Dev/docker-compose.yml named as single product file needing healthcheck rewrite
- KS-1154 — Blockchain/Dev/package-lock.json named as single lockfile requiring rollup-linux-x64-gnu addition
- KS-1138 — .github/workflows/pr-security-gates.yml named as workflow file to retire dormant step
- KS-1134 — Blockchain/Testing/ci/orchestrate.sh:119 bash idiom named as specific line to fix for Stage-1 JOIN crash
- KS-1131 — services/auth/src/__tests__/ks963-preauth-rethrow.test.ts named as the structural cell helper away from closing `[TEST?]`
- KS-1115 — Blockchain/Dev/migrations/001_initial-schema.sql named alongside 003_consolidate-anchors.sql as migration adding CHECK constraint `[MULTI?]`
- KS-1110 — utils/yaml.ts named as module to import readYaml into both tests in systemTest/performance
- KS-1080 — systemTest/akto/docker-compose.yml named as compose file where akto-autoheal runs as root with docker.sock RW
- KS-1030 — HERE/../044_vault_entries_repair.sql referenced as hard-wired migration path that test:migrations must take parameter instead
- KS-1023 — Blockchain/Dev/deployment/azure/migrate/init.sql and Blockchain/Dev/docker/init/01-schema.sql named alongside initial-schema.sql as three disagreeing definitions requiring reconciliation `[MULTI?]`
- KS-1010 — tests/e2e/.../happy-path-wallet.spec.ts:255 calls non-existent route with passing assertion on 404
- KS-997 — scripts/audit/audit-baseline.json carries four expired advisories needing re-triage action
- KS-990 — runner/actor_manifest.ts TS2540 error cited as pre-existing lint failure preventing quality pass in systemTest/performance
- KS-982 — systemTest/__tests__/pre_suite.test.sh silently quarantines manifest causing false green report `[TEST?]`
- KS-940 — .claude/settings.local.js mentioned alongside SECUURA_SEAT_SCAN escape hatch gap in launcher suite findings
- KS-902 — fixes comment in no-tracked-credentials.sh citing bare-path-scripts-executable.sh and action-pins-labelled.sh `[MULTI?]`
- KS-872 — names src/crypto/jwks.ts as the source file needing import or local declaration for JsonWebKey
- KS-812 — names connectors/whatsapp-bot/src/index.ts as the file whose default API URL needs repointing
- KS-768 — names Blockchain/Dev/scripts/audit/audit-locks.mjs as the hardcoded scan list to extend
- KS-752 — names systemTest/schemathesis/scripts/run.py as the file where success check skips baseline gate
- KS-738 — names scripts/run.py as the bootstrap file entering os.execv loop on symlinked venv
- KS-723 — names docs/openapi/secuura-api.yaml as the spec to declare remaining operations in
- KS-716 — names config/secrets.yml and config/secrets.example.yml as files lacking system_admin block `[MULTI?]`
- KS-638 — names secuura-extranet/ci/build-dashboard.mjs as the dashboard producing misleading red status
- KS-636 — names .github/workflows/base-image-refresh.yml as the workflow that fired unread alarm
- KS-598 — names platform_document_registry UNIQUE constraint and registerInPlatformRegistry upsert to defuse
- KS-595 — names tests/test_undeclared_method_safety.py as the test skipping closed tickets
- KS-530 — names scripts/audit/audit-baseline.js as the baseline exception file to remove after bumping @hono/node-server

**UNKNOWN (2) — the model said the text does not decide it:**
- KS-1155 — description mentions guard files but paths array empty so cannot confirm exact product file from evidence
- KS-1054 — description mentions migrations directory generally but paths array empty so cannot name specific migration file needing reorder


## 🔎 ORNITH-TRIAGED **AUTH TIER** — 9 class A, **UNVERIFIED, AND AUTH IS STILL LAST** (added 2026-09-18 09:4x)

`predicate_classify` over the 40 tickets excluded as *auth-shaped title*. **Kam's 2026-09-15 18:19 order is auth LAST, not auth NEVER** — this SORTS the tier, it does not open it. Nothing here is briefed until he says so. The predicate deliberately sent anything that changes **who may authenticate, what a token grants, or how a permission is decided** to class B even when it named one file, so class A here means *mechanical defect in an auth-adjacent file*, never *an authorisation decision*.

⚠ **COVERAGE WAS NOT CLEAN ON THIS BATCH, unlike the first two: 40 sent, 40 rows, but 1 MISSING and 1 INVENTED.** `KS-1091` was never classified and a row appeared for `KS-1101` — which was not in the batch. **That is a DIGIT TRANSPOSITION (1091 → 1101), not a hallucination from nowhere, and it is the more dangerous shape: the wrong id is a REAL ticket, so the row looks legitimate.** Treat every identifier here as needing a check against the batch before use. **KS-1091 is unclassified and must be re-run.**

- KS-1235 — state type = backlog but defect concrete in services/auth/src/db.ts with stated fix shape (route through GUC path)
- KS-1225 — single file named services/auth/src/__tests__/ks799-consent-script-csp-and-execution.test.ts with mechanical jsdom absence defect
- KS-1105 — single file named frontend/admin/src/pages/Login.tsx:81 with concrete placeholder text defect
- KS-1006 — single file named services/auth/src/routes/users.ts with concrete MFA verification skip defect and stated shape
- KS-1005 — single file named services/auth/src/repositories/userRepo.ts with USER_COLS omitting password_hash causing 404 on every user
- KS-918 — single file named services/auth/package.js with vite incorrectly placed in production dependencies dragging esbuild/fsevents
- KS-824 — two DDL defects in migration 047 affecting services/auth/src/routes/oauth.ts with concrete case-normalization fix shape
- KS-805 — single PATCH /api/oauth/apps validation missing .min(1) with stated one-line fix closing the door for Q3
- KS-756 — single write site in services/auth/src/services/session.ts:143 with zero read sites; concrete wiring-up prerequisite

**Note on KS-805:** the model rates it class A — *"single PATCH /api/oauth/apps validation missing .min(1) with stated one-line fix"*. Wednesday removed KS-805 from **seat A's** queue at 09:4x because it had been carried as blocked-on-#922 by four consecutive seats. **Those are not in conflict:** it is off the SEAT's queue because #922 is not moving, but if the fix really is a one-line validation independent of #922 it may be an ORNITH candidate. **Read the ticket before believing either framing.**


### Wednesday's read of two triaged class-A rows, 09:5x 2026-09-18 — so nobody re-reads them
- **KS-1110 — NOT Ornith-shaped despite its class A.** The fix ('import `readYaml` from `utils/yaml.ts`') touches **TWO test files and no product file**, so there is **nothing to tamper and nothing to red-proof** — the same shape already set aside as `KS-1142 (a test refactor with no product tamper)`. Its second half (a source-text guard that js-yaml is imported only by `utils/yaml.ts`) COULD be pinned, but that is a different, larger job. **Route: a Claude seat, or leave.**
- **KS-990 — one real one-line defect inside a two-package ticket.** `runner/actor_manifest.ts:140` `TS2540: Cannot assign to 'secrets' because it is a read-only property` is concrete and single-file, **but the ticket covers `systemTest/performance` AND `systemTest/akto`** and its stated purpose is that `npm run quality` cannot pass in either. **If it is briefed, brief ONLY the `actor_manifest.ts:140` defect and say so in the raise note** — do not let the model try to make `quality` pass. Note the ticket itself records a 7-line offset (`:140` on develop vs `:133` on #901) as identity evidence, so **re-read the line number at the tip before pinning a tamper.**
- **Method note for whoever picks the next one:** the triage says *class A*, which means the model thought it was one-file and mechanical. **It does not mean the tier can grade it.** Two of the first three I read fail on TIER shape (no product file to tamper), not on difficulty. Check 'can the checker red-proof this?' before writing a brief.

## → CLAUDE SEAT (routed 2026-09-18 12:5x by the 10:0x Wednesday seat)
- **KS-1228 → a Claude seat, the WHOLE fix (all four handlers), not just the `/version` slice.** Ornith round 1: **the product hunk was CORRECT** (A2/A3/A3b/A3c/A7 PASS; `runs/2026-09-18_ks1228-ornith35b-night/out.md.checker/section_1.diff` is a good starting point). But the TEST FILE failed ts-jest's type check: `TS6133 'REFUSED' declared but never read` (originate's tsconfig has `noUnusedLocals` + `noUnusedParameters` ON) and `TS2708 Cannot use namespace 'jest' as a value`. **The TS2708 cause is UNDIAGNOSED:** the test uses `jest.mock`/`jest.fn` as globals EXACTLY as the reference `ks1213-…` does (no import), so it isn't the import. The brief-writer couldn't see it (ts-jest type-check was off in its scratch). The harness retry (load-deferred via `retry_when_load_allows.sh`, which ran at 12:36) then failed A3 on a ONE-CHARACTER slip: the product `+++` header read `services/Originate/…` (capital O). **I did NOT spend the one rebrief:** without the TS2708 cause it would be a guess. A Claude seat can diagnose ts-jest inside the real tree. Remaining handlers: `POST /:id/share` (:2136), `POST /:id/transfer-custody` (:1595), the `/api/certifications/issue` pin.

## ⏸ ORNITH IDLE BY DECISION — 2026-09-18 13:0x (the 10:0x Wednesday seat)
The G7 'queue empty with seats live' tap is **expected**, and it isn't a stall. About 25 candidates were examined today (the 06:51 list + the gate-filed KS-1238..1250); **5 were Ornith-shaped and all 5 PASSED** (KS-1233/1125/1209/1248/1250; seat A 10th is raising the first four). The rest are the wrong SHAPE: a decision, multi-file, app-only reachability, auth, already-fixed, code inside a test file, or timing-bound. **KS-1228 → a Claude seat** (TS2708 undiagnosed). The only newer tickets, **KS-1251** (F6: eslint `rules: {}` on scripts/*.mjs, which is config with no Ornith tier) and **KS-1252**, were filed from #922 minutes before this note. **Don't spend another brief-writer round (a large Claude subagent) on two long-shot tickets to make the queue look busy**: that's the 09-18 morning lesson. **Refill when:** a gate files new direct-reachable tickets, or Kam names auth as eligible (the next big pool, LAST by his rule).
- **KS-1254 → a CLAUDE SEAT (routed 14:3x; NOT Ornith, the HARNESS can't express it).** It's test-only: 2 `it()` cells in place in `packages/shared/src/__tests__/ks256-spec-example-contract.test.ts` pinning `PREFIXED_UUID_RE` (`scripts/spec-examples/check/contract.mjs`, blob `07d4e9ab6`). Blocked by: (1) `build_input.sh:186-194` accepts a product only under `services/*/src` or `packages/shared/src`; (2) the checker plants ONE tamper per input, and this needs two (M2, M6). **The cells are PRE-MEASURED by the brief-writer in node:** an UPPER-case variant nibble is refused (red ONLY under M2 `[89ab]`→`[89abAB]`); `credit_<v4>` is admitted (red ONLY under M6, `cred` made a substring); controls (lower-case `a` admitted, `cred_<v4>` refused) are green under both. A seat writes them, red-proves them against the gate's M2/M6 lines (`reports/2026-09-18-ks679-922-30c773ee8-tier2-r2/evidence/tamper.out`), and raises. **Note:** it sits near the credential guard, but it's test-only and pins EXISTING behaviour.

### Search 2026-09-18 afternoon (subagent for the 14:4x Wednesday seat)
Tip `8b9c3f022bee76b79a47f1b8c5de8ad3ddb4a0ae` (ls-remote 14:5x). Read-only on Linear and the Secuura repo; red/green MEASURED in a scratch mirror (tip file via `git show` + the repo's own vitest), never in the repo. Nothing queued.
- KS-1230 — **FIT** (`night/briefs/KS-1230.md`): PUT /api/admin/settings validates `integrations[].config.allowedDocumentTypes` as string[] → 400 VALIDATION_ERROR before the write. One insert-only hunk at admin.ts:1124/1125; 4 🔴 + 2 controls through the ks719 in-process dispatch. Measured: tip 4 red / 2 green, patched 6/6, tsc clean. Build rc 0, ~27.1K prompt tokens (needs ctx=65536). ⚠ Shares trailing context `:1125` with KS-1257 — do not run both against one tip.
- KS-1258 — **FIT** (`night/briefs/KS-1258.md`, NEW ticket filed 14:38 from the #1038-1041 batch gate): a DEGRADED optional service gets read-first advice instead of "npm run dev" in system-status.ts (the KS-1248 sibling). One hunk at :581-584; 1 🔴 + 2 controls on the ks1248 harness. Measured: tip 1 red / 5 green (incl. ks1248's 3), patched 6/6, ks864a/b/c green; ks1101 not runnable in the mirror (unmeasured). Build rc 0, ~11.2K tokens.
- KS-1236 — REJECTED: services/auth verification-level review (a subject's authorisation level — an auth surface, LAST) and the fix is a choice (400 vs auto-close vs a conditional UPDATE).
- KS-1197 — REJECTED: the fix site is `middleware/auth.ts` principal construction (auth, LAST) plus a second site in verification.ts (multi-file).
- KS-955 — REJECTED: fresh-clone test-environment chain (.env.example / compose / suite preconditions); three unchosen fix shapes, and no product file.
- KS-758 — REJECTED: a dead-letter DESIGN for the erasure path ("a design, not a line"), and GDPR.
- KS-837 — REJECTED: a tooling/process ticket (a phrase check over contract sources), with a standing DO-NOT-BUILD ruling.
- KS-748 — REJECTED: DB schema integrity (a constraint in a migration), measured against real PostgreSQL; no in-process cell.
- KS-986 — REJECTED: demo seeding + a published credential; needs Kam's decision (his signature class).
- KS-1257 — REJECTED for now: same PUT handler as KS-1230 (overlapping context) and a choice (merge over defaults vs over the current value) touching GET defaults too; a gate SHIPS-WITH item for #1038.
- KS-683, KS-953, KS-579, KS-581, KS-627, KS-915, KS-746 — not re-read: already rejected with reasons in `queue.md` (lines 91-102: Platform S side / CLASS ticket / features / design / services/security).

### Search round 2, 2026-09-18 afternoon (subagent for the 14:4x Wednesday seat)
Tip `8b9c3f022`. Same method as round 1 (read-only; red/green measured in a scratch copy). File-collision check against the four in-flight PRs (ks256 test, originate documents.ts + certifications.ts, system-status.ts, admin.ts) applied before choosing. Nothing queued. **One fit this round.**
- KS-1261 — **FIT, BASH_PATCH tier** (`night/briefs/KS-1261.md`): initialise `FAILED_LEGS=""` / `fail_total=0` under `fail=0` in `scripts/preflight/preflight.sh` (one insert-only hunk, :94-96). The new suite reuses the KS-1209 harness under a poisoned caller env; 2 🔴 + 3 controls. Measured: tip 3 pass / 2 fail (both 🔴), patched 5/5; the KS-1209 suite 4/4 on both trees. `build_bash_input.sh` rc 0. No collision.
- KS-1260 — REJECTED for now: the same file as KS-1261 (the verdict region :693-705). Only one per file per round; brief it after KS-1261 lands. It's also a choice (print the ratio on the new path, or fold the message into the closing block).
- KS-1257 — SKIPPED per the coordinator: the same PUT handler as KS-1230, which is being raised now.
- KS-1251 — REJECTED: eslint config + a test tsconfig (config/tooling, two files, no product file under services/*/src).
- KS-1252 — REJECTED: the product is `scripts/spec-examples/check/contract.mjs`, which the harness can't express (the same block as KS-1254), and its cells would live in the ks256 test, a file collision with an in-flight PR.
- KS-1253 — REJECTED: the same file and harness block as KS-1252, and the ALLOW-list is a design change.
- KS-1255 — REJECTED: a decision ("decide the floor from the key formats … or add a second rule").
- KS-1259 — REJECTED: suite-wide isolation hygiene across many test files, with no product file.
- KS-1231 — REJECTED: two readers (verification.ts + health.ts) plus the admin portal; it widens connector authorisation (escalation candidate, "the owner's fix").
- KS-1232 — REJECTED: one line (health.ts:58), but what to report is an open choice that changes the published contract (`array of string`) and the MCP relay.
- KS-598 — REJECTED (triaged row): an architecture choice (re-key the registry or remove the upsert) in originate verification.ts plus a DB constraint.
- KS-1134 — REJECTED (triaged row): the fix lives inside a test file (`orchestrate_jobs.test.sh` CELL 14/15), and the red-proof needs a bash-4-only idiom tamper in `Blockchain/Testing/ci/orchestrate.sh`.
- KS-872 — REJECTED (triaged row): a type-only error (vitest can't red it) in `packages/shared/src/crypto/jwks.ts`, a JWKS/auth crypto surface.
- Rejected from the title and census row, not re-read: KS-1019 ([Question]), KS-1203 (originate `documents.ts`, a **file collision with an in-flight PR**), KS-759 and KS-1084 (auth middleware / gateway→originate auth, LAST), KS-965 (87 doc sites of a retired credential). KS-998, KS-1163 and KS-789 are not re-read: each already has ≥2 FAIL runs in done.md.

### Search round 3 (bash tier), 2026-09-18 afternoon (subagent for the 14:4x Wednesday seat)
Tip `8b9c3f022`. Method: bulk-read (read-only GraphQL) the descriptions of all 120 census rows in SET ASIDE + "names no product file" (Linear returned all 120, in batches of 100 and 20), grepped them for `*.sh`, and hand-read the shell-script candidates. Exclusions applied: preflight.sh, smoke-test.sh, the four raising PRs' files, deploy/demo/live-stack/network, auth/credentials. Red/green measured on /bin/bash 3.2.57 in a scratch tree. Nothing queued. **One fit.**
- KS-1136 (item 1 only) — **FIT, BASH_PATCH** (`night/briefs/KS-1136.md`): `Blockchain/Testing/jobs/04-container-trivy.sh`. Keep trivy's exit code; a failed or unreadable per-image scan is written `error: scan-failed` and the run exits 1 before the clean `across N` summary. Three hunks (one replaces the blank `:94` so no context line is blank); new suite on the `container_trivy_image_filter.test.sh` stubs; 2 🔴 + 1 control. Measured: tip 1 pass / 2 fail (`0 none`, `0 unparseable`), patched 3/3; the reference suite 4/4 on both trees. `build_bash_input.sh` rc 0, description == brief. **Refs, not Closes.**
- KS-1136 item 2 — NOT briefed: `09-aggregate-report.sh`, seven identical artefact-read sites (>3 edits), and the clean shape is a shared helper (a design choice). Better whole in one Claude seat than as three Ornith splits.
- KS-766 — REJECTED: a testability refactor (extract base-image-watch.sh's inline python age producer into a function). At the tip there is no function to call, so a red can only be "command not found", never an assertion; the self-test also lives inside the 838-line product script.
- KS-956 — REJECTED: its own words say the gate's fix shape was built and WITHDRAWN (it can't be expressed without denying the repo's idiom), so it's a decision.
- KS-1137 — REJECTED: test-only edits to `container_trivy_image_filter.test.sh` with no product change (and it's KS-1136 item 1's reference suite).
- The other bulk hits (not hand-read, reason from the description or the census row): KS-808 / KS-1063 / KS-1088 / KS-1135 are already SET ASIDE (psql / decision / decision / diagnosis-first); KS-896 / KS-897 / KS-982 have a test file as the subject; KS-981 lives on the frozen #892 branch; KS-785 / KS-1161 are credentials; KS-902 / KS-903 are multi-script; KS-1054 is DB migrations; KS-1138 / KS-1148 / KS-1162 are `.github/workflows` (Kam-class); KS-1048 is docs; KS-990 and KS-768 aren't shell (TS / .mjs); KS-1134 was rejected in round 2.

### Search round 4 (test_only), 2026-09-18 evening (subagent for the Wednesday seat)
Tip `52df64f844b7b3aabf7df57284c5f4e2ab8a07a2` (ls-remote, local). Contract read from `tasks/test_only/{task.md,checker.sh,build_test_only_input.sh}` and the golden `briefs/KS-1254.md`. Measured with jest + ts-jest (type-check on) in a scratch tree: originate + packages/shared at the tip via `git archive`, shared built there. Nothing queued. **One fit.**
- KS-1267 (Q1 half) — **FIT, TEST_ONLY** (`night/briefs/KS-1267.md`): one cell in `services/originate/src/__tests__/ks1228-a-refused-request-writes-no-provenance-row.test.ts` (`saveDocument` throws once on /version → 500, 0 rows). Tamper Q1 is one line at `documents.ts:2063`: record, then `versionObo.obo = null`, then save, which is equivalent to the gate's move. Measured: untouched 26/26; with the cell 27/27; Q1 with the cell → exactly {new cell} red, by assertion; Q1 without the cell → 0 red (reproduces the gate). Controls: the /version and /share `control:` cells. Build rc 0, description == brief. The Q3 (/transfer-custody) cell is left out on the ticket's own instruction (decide after KS-1263). Refs, not Closes.
- KS-1137 — REJECTED: its cells live in a bash suite (`*.test.sh`); test_only runs vitest/jest only (the builder requires `*.test.*` / `*.spec.*` JS/TS).
- KS-1110 — REJECTED: the refactor edits TWO test files, and the proposed js-yaml import guard is RED at the tip until they change, so it's not green-at-tip. It also lives in systemTest/performance, outside Blockchain/Dev.
- KS-1142 — REJECTED: a design choice (derive or keep two hand literals over one walk). No product behaviour is pinned and there's nothing to tamper.
- KS-1252 / KS-1253 — REJECTED: the "pinning half" would pin behaviour the tickets call WRONG (secret-named prefixes admitted). The fix is a product change to `contract.mjs`.
- KS-1144 — REJECTED: the code its cells guard (the J2 walk, `shapes.push`) lives INSIDE the test file, and a test_only tamper must be a product file.
- KS-1237 — REJECTED: its ARRAYLIKE row is held (PASS), X-MSG-MEMBER is parked for a Claude seat (the Ornith rounds are spent), and X-INFO is infeasible in that file (the ticket's own comment).
- Title-level, not re-read: KS-1131 / KS-1152 / KS-1205 / KS-1238 (auth); KS-1145 (bash + real PostgreSQL); KS-939 / KS-1153 (bash suites); KS-1030 (migrations, DB); KS-1266 (four test files' env hygiene, pins nothing). The other "unpinned" titles already have READY files (KS-887 / 944 / 1090 / 1118 / 1120 / 1123 / 1179 / 1185 / 1188 / 1192 / 1193 / 1199 / 1212 / 1217 / 1220 / 1221 / 1227 / 1229).
