<!-- ARCHIVE (not generated): the 2026-09-19 candidates.md as committed at 032164979, preserved 2026-09-20 03:4x by the 18:0x Wednesday seat because night_run.sh re-derives candidates.md every run and OVERWRITES the round rejection tables seats appended (rounds 1-13 of 2026-09-19). Future round notes go to night/candidates_rounds.md, never into candidates.md. -->

# Ornith candidates — derived 2026-09-19 01:38 from 364 KS Backlog/Todo tickets (read-only, unpaginated)

A CENSUS for the coordinator to brief from, easy → hard (Kam 2026-09-15 16:40 / 18:19). A ticket here is a candidate, not a task: read it, read the file at the tip, write `night/briefs/<id>.md`, then queue it. Auth-shaped titles are excluded (LAST); Peter/Stuart tickets and PR-attached tickets are excluded outright.

## T1 services (vitest, one file) — 14
- KS-683 (P2) Anchor-status standoff: a consumer repolls anchors K reports as terminally faile — `services/anchoring/src/index.ts`
- KS-953 (P2) CLASS: editing api-gateway/src/index.ts silently reddens packages/shared, and no — `services/api-gateway/src/index.ts`
- KS-1168 (P3) userRepo.ts: ILIKE search on encrypted PII columns can never match — :1017 and : — `services/auth/src/repositories/userRepo.ts`
- KS-1190 (P3) api-gateway meetsVerificationLevel fails open on an unknown REQUIRED level: an o — `services/api-gateway/src/services/enforcement.ts`
- KS-1222 (P3) POST /api/documents/upload never reaches the gateway's blocked-extension / MIME  — `services/api-gateway/src/routes/proxy.ts`
- KS-1234 (P3) POST /api/v1/documents with application/json never answers, and /api/documents a — `services/api-gateway/src/index.ts`
- KS-1236 (P3) Approving a stale PENDING verification request after the subject's level rose an — `services/auth/src/routes/users.ts`
- KS-579 (P3) Per-person platform-admin identities — the shared seeded admin cannot carry attr — `services/api-gateway/src/routes/platform.ts`
- KS-581 (P3) register-connector: volume alerting, rate limit, and correlation of refused re-k — `services/api-gateway/src/routes/platform.ts`
- KS-627 (P3) Implement real wallet signature verification (CIP-8/COSE + address binding) — ne — `services/wallet-connector/src/types/index.ts`
- KS-746 (P3) Security events carry no tenant at all — KS-743 had to gate them platform-only,  — `services/security/src/index.ts`
- KS-915 (P3) A clean stack has no supported way to obtain its first privileged account — `services/auth/src/routes/auth.ts`
- KS-1145 (P4) ks949 suite coverage (KS-950 / KS-962, #973): ID3's capture half has no size ass — `services/api-gateway/src/startup-migrations.ts`
- KS-1239 (P4) R-1: the index.ts:347 rawAuthorization capture is dead code — 0 readers — `services/api-gateway/src/index.ts`

## T2 tooling (systemTest/*, one file) — 0

## T2b bash (bash_patch — one script + a *.test.sh beside the reference) — 5
- KS-998 (P2) KS-989 gate residue: the formatting gate fails OPEN on missing deps and reads th — `.githooks/pre-push`
- KS-1163 (P3) start-secuura.sh never waits for five default-profile, healthchecked services —  — `Start_Up/start-secuura.sh`
- KS-1245 (P3) F-1: scripts/smoke-test.sh:107 fails any /health/deep check that is not 'up' — a — `scripts/smoke-test.sh`
- KS-630 (P3) Wire the status-page XSS probe into preflight (or decide not to) — it runs today — `scripts/preflight/preflight.sh`
- KS-789 (P3) CONTRIBUTING.md justifies the hook's degradation and its --no-verify bypass with — `.githooks/pre-push`

## T3 jest services (originate, governance) — 7
- KS-1019 (P3) [Question] The document's whole `blockchain` block is published as z.unknown() — — `services/originate/src/originate.openapi.ts`
- KS-1203 (P3) A connector restricted by allowedDocumentTypes can still create the default DOCU — `services/originate/src/routes/documents.ts`
- KS-1263 (P3) A partly-completed /share or /transfer-custody is now unattributed: the multi-wr — `services/originate/src/routes/documents.ts`
- KS-1264 (P3) /revoke records its action_provenance row before updateDocument: a throw there a — `services/originate/src/routes/documents.ts`
- KS-1265 (P3) POST /api/documents saves the document and its provenance row, then answers 400  — `services/originate/src/routes/documents.ts`
- KS-759 (P3) tenantId is read through two `as unknown as` casts because it is not on JwtPaylo — `services/originate/src/middleware/auth.ts`
- KS-1084 (P0) READ ONLY / unverified: the gateway's own Authorization-only calls to originate  — `services/originate/src/index.ts`

## T4 docs (doc_patch) — 0

## T5 multi-file / later — 26
- KS-1051 (P2) develop is RED on the services/originate jest suite and NOTHING catches it — the — `scripts/preflight/preflight.sh`, `.githooks/pre-push`
- KS-1055 (P2) Per-tenant databases never receive the file migrations — CORE_MIGRATIONS FORCEs  — `services/api-gateway/src/startup-migrations.ts`, `services/tenant-provisioning/src/index.ts`
- KS-1231 (P2) A connector allow-list fails open when platform-settings integrations is not a c — `services/api-gateway/src/routes/verification.ts`, `services/api-gateway/src/services/health.ts`
- KS-1262 (P2) Security: PUT /api/settings/notifications writes the same key namespace as platf — `services/api-gateway/src/services/redis.ts`, `services/api-gateway/src/routes/admin.ts`
- KS-485 (P2) Security review — plan, methodology & handover (Platform K) — `services/api-gateway/src/routes/notifications.ts`, `services/originate/src/repositories/documentRepo.ts`, `services/originate/src/index.ts`
- KS-491 (P2) Review F — Edge, WAF, DDoS & anti-automation — `services/api-gateway/src/middleware/rateLimitEnforce.ts`, `services/auth/src/routes/auth.ts`
- KS-576 (P2) Bulk re-key: one admin-authorised rotate across a named set of externalRefs — `services/api-gateway/src/routes/platform.ts`, `services/security/src/index.ts`, `packages/shared/src/db/tenant-guc.ts`
- KS-624 (P2) prism issues VCs with random bytes as the Ed25519 proof and verifies them as pas — `services/vc-issuer/src/routes/credentials.ts`, `services/prism/src/index.ts`
- KS-753 (P2) Timestamping fail-closed: a mock TSA fallback must not report verified: true (ex — `services/timestamping/src/tsa/qualified-tsa.ts`, `services/timestamping/src/index.ts`
- KS-967 (P2) Neither credential guard can see a value in a .env.example — one scans the wrong — `scripts/check-no-default-passwords.sh`, `scripts/preflight/no-tracked-credentials.sh`
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

## HELD (READY_* or done.md PASS) — 88
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
- KS-1134 orchestrate_jobs CELL 14/15 cannot tell the KS-922 fix from a crash at the Stage
- KS-1136 Audit jobs: a per-image trivy failure reads as a CLEAN image in 04 (`|| echo '{}
- KS-1139 Bare arithmetic-command `((X++))` under `set -e` — exits 1 at 0 and bash ≥ 4.1 e
- KS-1140 ks879 guard: the 🔴 cell walks the tree on its own (`offendersUnder(DEV_ROOT)` :1
- KS-1152 L5 gate records (#799/#880/#985): jwt.ts citation ×5, security log title, dist t
- KS-1153 L7 gate records (#918/#924/#925): run-code-guards.sh --check-unreached advisory 
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
- KS-1237 ks1204 cells: three tampers stay green - the array-like allow-list, the refusal 
- KS-1250 O-2: RUNBOOK §2.2 documents SMOKE_BASE_URL, but scripts/smoke-test.sh ignores it
- KS-1261 Preflight: FAILED_LEGS / fail_total are never initialised, so an exported FAILED
- KS-1267 KS-1228: two row placements are unpinned — /version's row after saveDocument and
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
- KS-1173 — ALREADY SHIPPED inside READY_KS-1172-B3 ('KS-1172 + KS-1173 PART B') — NOT visible to a held-check that keys on the READY filename's ticket id, which is how it keeps being re-picked (updated 2026-09-18)
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

## EXCLUDED by predicate — 191
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
- KS-1039 — names no product file (after basename/docs/route resolution)
- KS-1042 — on Peter/Stuart
- KS-1044 — names no product file (after basename/docs/route resolution)
- KS-1048 — names no product file (after basename/docs/route resolution)
- KS-1053 — auth-shaped title (LAST, Kam 16:40)
- KS-1054 — names no product file (after basename/docs/route resolution)
- KS-1079 — names no product file (after basename/docs/route resolution)
- KS-1080 — names no product file (after basename/docs/route resolution)
- KS-1085 — names no product file (after basename/docs/route resolution)
- KS-1091 — auth-shaped title (LAST, Kam 16:40)
- KS-1100 — names no product file (after basename/docs/route resolution)
- KS-1102 — names no product file (after basename/docs/route resolution)
- KS-1104 — names no product file (after basename/docs/route resolution)
- KS-1105 — auth-shaped title (LAST, Kam 16:40)
- KS-1106 — names no product file (after basename/docs/route resolution)
- KS-1107 — auth-shaped title (LAST, Kam 16:40)
- KS-1110 — names no product file (after basename/docs/route resolution)
- KS-1115 — names no product file (after basename/docs/route resolution)
- KS-1116 — names no product file (after basename/docs/route resolution)
- KS-1124 — auth-shaped title (LAST, Kam 16:40)
- KS-1131 — names no product file (after basename/docs/route resolution)
- KS-1137 — names no product file (after basename/docs/route resolution)
- KS-1138 — names no product file (after basename/docs/route resolution)
- KS-1141 — names no product file (after basename/docs/route resolution)
- KS-1143 — names no product file (after basename/docs/route resolution)
- KS-1144 — names no product file (after basename/docs/route resolution)
- KS-1146 — auth-shaped title (LAST, Kam 16:40)
- KS-1147 — names no product file (after basename/docs/route resolution)
- KS-1149 — auth-shaped title (LAST, Kam 16:40)
- KS-1154 — names no product file (after basename/docs/route resolution)
- KS-1155 — names no product file (after basename/docs/route resolution)
- KS-1157 — auth-shaped title (LAST, Kam 16:40)
- KS-1161 — names no product file (after basename/docs/route resolution)
- KS-1175 — names no product file (after basename/docs/route resolution)
- KS-1177 — auth-shaped title (LAST, Kam 16:40)
- KS-1178 — names no product file (after basename/docs/route resolution)
- KS-1197 — names no product file (after basename/docs/route resolution)
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
- KS-1238 — names no product file (after basename/docs/route resolution)
- KS-1240 — auth-shaped title (LAST, Kam 16:40)
- KS-1241 — names no product file (after basename/docs/route resolution)
- KS-1242 — names no product file (after basename/docs/route resolution)
- KS-1243 — names no product file (after basename/docs/route resolution)
- KS-1244 — names no product file (after basename/docs/route resolution)
- KS-1246 — names no product file (after basename/docs/route resolution)
- KS-1247 — names no product file (after basename/docs/route resolution)
- KS-1249 — names no product file (after basename/docs/route resolution)
- KS-1251 — names no product file (after basename/docs/route resolution)
- KS-1252 — names no product file (after basename/docs/route resolution)
- KS-1253 — names no product file (after basename/docs/route resolution)
- KS-1255 — names no product file (after basename/docs/route resolution)
- KS-1256 — names no product file (after basename/docs/route resolution)
- KS-1257 — names no product file (after basename/docs/route resolution)
- KS-1259 — names no product file (after basename/docs/route resolution)
- KS-1260 — names no product file (after basename/docs/route resolution)
- KS-1266 — names no product file (after basename/docs/route resolution)
- KS-1269 — names no product file (after basename/docs/route resolution)
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
- KS-607 — names no product file (after basename/docs/route resolution)
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
- KS-678 — names no product file (after basename/docs/route resolution)
- KS-696 — names no product file (after basename/docs/route resolution)
- KS-699 — names no product file (after basename/docs/route resolution)
- KS-716 — names no product file (after basename/docs/route resolution)
- KS-723 — names no product file (after basename/docs/route resolution)
- KS-724 — auth-shaped title (LAST, Kam 16:40)
- KS-725 — names no product file (after basename/docs/route resolution)
- KS-735 — names no product file (after basename/docs/route resolution)
- KS-738 — names no product file (after basename/docs/route resolution)
- KS-748 — names no product file (after basename/docs/route resolution)
- KS-749 — has a PR attached
- KS-752 — names no product file (after basename/docs/route resolution)
- KS-756 — auth-shaped title (LAST, Kam 16:40)
- KS-758 — names no product file (after basename/docs/route resolution)
- KS-760 — names no product file (after basename/docs/route resolution)
- KS-761 — names no product file (after basename/docs/route resolution)
- KS-765 — names no product file (after basename/docs/route resolution)
- KS-766 — names no product file (after basename/docs/route resolution)
- KS-767 — names no product file (after basename/docs/route resolution)
- KS-768 — names no product file (after basename/docs/route resolution)
- KS-772 — names no product file (after basename/docs/route resolution)
- KS-782 — auth-shaped title (LAST, Kam 16:40)
- KS-783 — names no product file (after basename/docs/route resolution)
- KS-784 — names no product file (after basename/docs/route resolution)
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
- KS-837 — names no product file (after basename/docs/route resolution)
- KS-838 — names no product file (after basename/docs/route resolution)
- KS-840 — auth-shaped title (LAST, Kam 16:40)
- KS-846 — names no product file (after basename/docs/route resolution)
- KS-851 — names no product file (after basename/docs/route resolution)
- KS-872 — names no product file (after basename/docs/route resolution)
- KS-896 — names no product file (after basename/docs/route resolution)
- KS-902 — names no product file (after basename/docs/route resolution)
- KS-903 — names no product file (after basename/docs/route resolution)
- KS-918 — auth-shaped title (LAST, Kam 16:40)
- KS-919 — names no product file (after basename/docs/route resolution)
- KS-925 — auth-shaped title (LAST, Kam 16:40)
- KS-934 — names no product file (after basename/docs/route resolution)
- KS-939 — names no product file (after basename/docs/route resolution)
- KS-940 — names no product file (after basename/docs/route resolution)
- KS-947 — names no product file (after basename/docs/route resolution)
- KS-948 — has a PR attached
- KS-951 — auth-shaped title (LAST, Kam 16:40)
- KS-955 — names no product file (after basename/docs/route resolution)
- KS-956 — names no product file (after basename/docs/route resolution)
- KS-957 — names no product file (after basename/docs/route resolution)
- KS-959 — names no product file (after basename/docs/route resolution)
- KS-964 — has a PR attached
- KS-965 — names no product file (after basename/docs/route resolution)
- KS-977 — auth-shaped title (LAST, Kam 16:40)
- KS-982 — names no product file (after basename/docs/route resolution)
- KS-983 — on Peter/Stuart
- KS-984 — on Peter/Stuart
- KS-985 — on Peter/Stuart
- KS-986 — names no product file (after basename/docs/route resolution)
- KS-987 — names no product file (after basename/docs/route resolution)
- KS-990 — names no product file (after basename/docs/route resolution)
- KS-995 — names no product file (after basename/docs/route resolution)
- KS-996 — names no product file (after basename/docs/route resolution)
- KS-997 — names no product file (after basename/docs/route resolution)


## Search round 2026-09-19 (morning, Wednesday's subagent)

Pinned sha `59412d0575dff3243f5f0ccd1e50608ddb920d6c` (origin develop by `ls-remote` 06:1x AEST, object local; `documents.ts` blob `b5e76dc61` = the KS-1228 merge's). Sources in order: (a) the #1042-1045 batch gate report's findings, (b) KS-1263..1267, (c) T1/T2b rows above. Held-file exclusion read from the nine READY headers (`+++ b/` lines): 5 `scripts/__tests__/*.test.sh`, `scripts/preflight/preflight.sh`, `Testing/jobs/04-container-trivy.sh`, and the ks1202 / ks1228 (originate) + ks1230 / ks1258 (api-gateway) test files. 9 tickets read on Linear (read-only, comments sorted client-side: 0 comments on all 9); 1 fit, 8 rejected; the other T1/T2b rows not re-read (verdicts on record, cited).

- KS-1264 · **FIT** · N43-3: /revoke records before updateDocument; one file (documents.ts, 3 hunks: delete the now-unused `handleOnBehalfOf` :115-126, `:2348` → `checkOnBehalfOf`, `recordOnBehalfOf` above `:2353`), jest, ks1213 harness shape · brief `night/briefs/KS-1264.md` · input `night/inputs/code_1264_brief.json` (builder rc 0, "prompt source: WEDNESDAY BRIEF", 5 must_change sites, 4 expected '+', 1 red cell, ~48.8K tokens → ctx=65536) · sha 59412d057 · PRE-MEASURED in a `--shared` scratch clone: tip = 1 failed / 3 run (the 🔴, `toHaveLength(0)` got 1, assertion; 2 controls green), after = 3/3; whole originate suite 769+1red → 770/770; tsc rc 0; **real `code_patch/checker.sh` on the brief's exact diff = PASS 7/7, A2 strict** (positive control, not a model run). NOT queued.
- KS-1265 · reject (for Ornith) · N43-4: the fix MOVES the E-01 block `:842-853` above the save, and 3 of its lines carry U+2014 (two comments AND the 400 message string) — the model will not reproduce non-ASCII '-' lines, `ascii_proxy` has no PASS on record, and an ASCII-message copy would leave a dead duplicate guard. A clean move is a Claude seat's; same file as KS-1264.
- KS-1263 · reject · N43-2: decision-class (transaction vs record-on-partial, the ticket offers both) across two handlers (/share loop + /transfer-custody).
- KS-1266 · reject · N43-5: four test files, and the defect (a DNS lookup + TCP connect) is a side effect no cell asserts — nothing reds by assertion.
- KS-1267 Q3 · reject · waits on KS-1263's ruling (the ticket's own words), and its file (the ks1228 test) is HELD by KS-1267-Q1.
- KS-1249 · reject · #1037 N-2 (the gate's carried finding): "Decide the vocabulary the aggregates accept" — decision-class, names no product file.
- KS-1145 · reject · the ks949 suite needs a REAL PostgreSQL (initdb/pg_ctl/psql); none on this machine (no Homebrew keg), so it SKIPs 0/27 — no red possible; CN-2's tamper is SQL in startup-migrations.ts.
- KS-1239 · reject · dead-code removal (the `rawAuthorization` capture, index.ts:347): "0 reds when deleted", so no red-first cell exists; also an Authorization-header surface (auth, LAST).
- KS-1245 · reject · decision-class ("Decide what the smoke test should assert for degraded") and smoke-test.sh is the file of KS-1250's held READY (Kam's).
- Gate findings not ticketed or already held (no read needed): N43-1 Q1 = held KS-1267-Q1; N43-6 = record-only, in the held ks1228 test; N44-1 = held KS-1258-N44-1; N45-1 = KS-1231 (T5, two files); N45-2 = KS-1262 (security, excluded); N45-3 / N45-4 = record / deploy check; N45-5 = held KS-1230-N45-5; KS-1201 = held.
- T1/T2b not re-read, verdict on record: KS-683 / 953 / 579 / 581 / 627 / 746 / 915 (queue.md rejections: Platform-S side, CLASS, features, design, services/security, auth); KS-1168 (reallocated to Claude, decision); KS-1190 (its own "two measurements come first"; FAIL 09-18 10:04); KS-1222 (exhausted → Claude); KS-1234 (FAIL A3 09-18 10:11); KS-1236 (auth, a choice); KS-998 / KS-1163 (two and four FAILs on record 09-16); KS-630 (preflight.sh — a held file); KS-789 (doc rebrief owed, two doc_patch FAILs).

## Search round 2026-09-19 (07:13, Wednesday's subagent, round 2)

Pinned sha `59412d0575dff3243f5f0ccd1e50608ddb920d6c` (origin develop by `ls-remote` 07:0x AEST, unchanged since round 1; object local). Order as briefed: (1) T3 KS-759 / KS-1203; (2) T5 top to bottom, skipping KS-485 / 491 / 1231 / 1262 / 1051; (3) the #1042-1045 batch gate report's unpinned tampers. 17 tickets read on Linear (read-only, comments sorted client-side); **1 fit, 16 rejected**; 6 T5 rows not re-read (verdicts on record, cited).

- KS-759 · reject · `tenantId?` is ALREADY declared on originate's `JwtPayload` (middleware/auth.ts, KS-764 docblock); the residue is the two casts in `routes/gdpr.ts:442-443` (`connectorContext`), a pure type edit with zero runtime change, so no red cell can exist (A4 needs an assertion red). The ticket's own fix is the SHARED payload type ("its own PR and its own reviewer"). Claude seat or close-as-mostly-done.
- KS-1203 · reject · decision-class: "Not built. Owner's choice: apply the allow-list to the resolved default type, or require a restricted connector to name a type" (re-confirmed 09-17 comment). Also documents.ts, the held KS-1264's file.
- KS-576 · reject · a 1-2 day feature (bulk re-key route), gated on KS-577, api-gateway platform.ts + security.
- KS-624 · reject · "fix shape deliberately blank pending that ruling" (Kam's, by-design-or-remediate).
- KS-967 · reject · two guard scripts + a self-test that must change consciously; the shape is a NEW line-level check (design), and credential-guard surface.
- KS-1174 · reject · two services (security validate reason + api-gateway `middleware/auth.ts`, the auth chain — excluded) and a Platform S contract (PS-740).
- KS-1189 · reject · decision-class ("decide whether the attempted-email capture should work at all"; R-5 = check external readers first).
- KS-1200 · reject · decision-class ("The owner decides which schema source is authoritative"), 10 schema files.
- KS-1223 · reject · "Owners measure it, then decide"; reachability UNMEASURED; two services (gateway strip + referral), a wallet-identity header.
- KS-1232 · reject · the reported value for a non-array list is unruled ("report that the list is not usable" — no shape given), MCP relays to check, and `health.ts` is KS-1231's file (Claude seat).
- KS-526 · reject · feature (Key Vault mnemonic loading + rotation), security.
- KS-580 · reject · 3-5 day feature (append-only recovery audit outside the estate).
- KS-621 · reject · tracking ticket, "fix shape is blank on purpose", Kam's ruling.
- KS-1082 · reject · the guard exists only on unmerged #896's head; `systemTest/` is Peter's authority (the ticket's own words).
- KS-1083 · reject · "Needs decisions before code" (provisioning, deploy order, rotation, production requirement).
- KS-658 · reject · Kam's call (demo-affecting config); "establish which artefact is authoritative before reconciling".
- KS-1206 · **FIT** (item 1 only: rateLimit bounds; item 2 `connectorId` is an owner decision, left out) · one file `services/originate/src/routes/adminConfig.ts`, ONE pure-insertion hunk at `:904` (4 '+' lines, trailing context `:904-906`), jest, ks764 harness shape · brief `night/briefs/KS-1206.md` · input `night/inputs/code_1206_brief.json` (builder rc 0, "prompt source: WEDNESDAY BRIEF", 0 must_change sites (a pure insertion), 4 expected '+', 3 red cells, ~35.4K tokens → ctx=65536) · PRE-MEASURED in a `--shared` scratch clone: tip = 3 failed / 6 run (the three 🔴, `toEqual` got `[201,null,1]`, assertions; 3 controls green), after = 6/6; whole originate suite 770+3red → 773/773; tsc rc 0; **real `code_patch/checker.sh` on the brief's exact diff = PASS 7/7, A2 strict** (positive control, run twice, the second on the final input). NOT queued. **Same file as the held READY_KS-730-B** (`/document-types` hunks `-184,7` / `-216,19`, net +3, no overlap): raise one at a time, the second rebases at a clean offset.
- Not re-read, verdict on record (queue.md): KS-1055 (structural, 2 services, real PostgreSQL), KS-753 (design question, 2 files), KS-625 (Kam's ruling), KS-807 ((A) vs (B), 2 files), KS-870 (auth chain), KS-954 ("Reproduce before fixing").
- Step 3 (batch gate report, test_only pins): nothing unheld. Q1 = held KS-1267-Q1; Q3 waits on KS-1263 and sits in the held ks1228 file; R10/E3 (`prior` undefined, 26/26 green) is in the held ks1228 file and "not reachable here"; N44-1 = held KS-1258-N44-1; N45-5 = held KS-1230-N45-5; #1042 L1 stays green BY DESIGN (the guard dedupes) and L2 already reds liveness; #1037 N-2 = KS-1249 (decision, rejected round 1).

## Search round 2026-09-19 (round 3, gate tampers)

Pinned sha `59412d0575dff3243f5f0ccd1e50608ddb920d6c` (origin develop by `ls-remote`, unchanged since rounds 1-2; object local). Source: every `report.md` in `Testing Agent MAIN/projects/secuura/reports/` dated 2026-09-17 / 2026-09-18 except #1042-1045, grepped for unpinned / no-cell / 0-red tamper rows. Measured in a `--shared` scratch clone (prepare_clone.sh farm, api-gateway `npx vitest run`, whole suite 613/613 at the tip). **2 fits, 24 reject rows (several group two or more gates).** Nothing queued, nothing run on the model.

- 2026-09-18-ks1101-1037-f87506f47-tier1-r1 · N-3 "a NON-required degraded service (overall stays operational)" — tampers OPTIONALDEGRADES (system-status.ts:425 `&& degradedServices === 0`) + REQUIREDCOUNTSALL (:418 `s.required &&` dropped) · **FIT** · 0 red / 613 whole suite without the cell; with it 1 red each (the new cell, AssertionError), 614 otherwise green · brief `night/briefs/KS-1101-N3.md`, input `night/inputs/test_only_1101N3.json` (builder rc 0); real test_only checker on the brief's own diff = PASS 8/8 (positive control, not a model run).
- 2026-09-17-ks864-1009-6ec0cb198-tier2-r1 · R-1 row 17 Q-nullish (`||` -> `??` on the 3 portal URLs, system-status.ts:228/237/246) · **FIT** (NEW file ks864d; ks864c is held by READY_KS-864-F1009) · 0 red / 613 per tamper without the file; with it exactly its portal cell reds · brief `night/briefs/KS-864-R1.md`, input `night/inputs/test_only_864R1.json` (builder rc 0); real test_only checker on the brief's own diff = PASS 8/8 (second run, on a reset clone; the first refused a clone left dirty by the 1101 check).
- same #1009 report · R-1 rows 15/16/18 (Q-prod, QA-6, QA-7: env-specific branches that do not exist at the tip) · reject · contrived tampers (add a NODE_ENV branch); row 17 carries the one natural regression.
- same #1009 report · F-1009-1 / F-1009-2 (Q-reset, QA-3) · reject · test-setup tampers, not product; held as READY_KS-864-F1009.
- 2026-09-18-ks1101-1037 · Q-CONSUMERS-REVERTED (admin api.ts + status index.html) · reject · frontends have no test suite; no runner to red.
- 2026-09-18-ks1101-1037 · other N-3 properties (body shapes, /health/services, /api/v1, troubleshooting text) · reject · N-2/F-2 behaviours are NOT fixed (nothing to pin); troubleshooting = held KS-1248/KS-1258; same test file as the KS-1101-N3 fit.
- 2026-09-18-ks679-922-30c773ee8-tier2-r2 · F10 M2 (variant `[89abAB]`) + M6 (`cred` substring) · reject · ALREADY PINNED by #1042 (KS-1254, `884294680`); also a Peter-reviewed PR.
- 2026-09-18-ks679-922-8664826e5-tier2-r1 · F1 Q1-Q5 loosenings · reject · closed by #922 round 2 (all red there).
- 2026-09-17-ks1176-1014r2-9ba0caf78-tier1-r2 · N-3 G-REV (`body.type || body.documentType`) · reject · pinned since #1035 (ks1204 "documentType wins over type" describe, 2 cells).
- 2026-09-17-ks1176-1014-616c766a5-tier1-r1 · F-1..F-5 · reject · product defects, not unpinned fixed behaviour; F-3 = held KS-1196; F-2/F-5 auth.
- 2026-09-18-batch1038-1041-tier1-r1 · T7 (leg 1 always excluded) · reject · = held KS-1209-N41-3; preflight.sh excluded. N38-1/N38-2/N41-1/N41-2 are open defects (N41-2 = held KS-1261).
- 2026-09-18-ks1204-1035-4b1fb0621-tier1-r1 · N-B X-MSG-MEMBER / X-INFO-ALWAYS-EMPTY / Q-ARRAYLIKE-OPEN · reject · KS-1237 (ARRAYLIKE held; MSG failed twice on record 09-18, done.md 269-270).
- 2026-09-18-ks1215-1034-e4624218b-tier1-r1 · X-BEARER-PREFIX-ONLY / X-FETCH-RAW / Q-PLATFORM254-RAW / Q-INDEX-RAW-REMOVED · reject · Authorization-header surface (auth, excluded).
- 2026-09-18-ks1194-1032 r1+r2 · F-3 unpinned rows · reject · services/auth (excluded).
- 2026-09-17-ks1018-1015-77145ce84-tier1-r1 · F1-F4 · reject · auth service; F1/F2 held KS-1193.
- 2026-09-17-ks1050-1018-efd677e98-tier2-r2 · F-1 Q-D1-DENYLIST · reject · held KS-1217; auth.
- 2026-09-17-ks1072-1016-a226d94fe-tier1-r1 · P-1016-3 G-STATUS · reject · held KS-1199.
- 2026-09-17-ks1073-1005-e5e7ff99d-tier1-r1 · P-1005-2 GL · reject · held KS-1180-P1P2P4.
- 2026-09-17-ks1087-1008-dd7086d5a-tier1-r1 · G4/G5/G6 · reject · pinned by #1010 ("the #1008 gate's F3-F6 cells").
- 2026-09-17-ks1183-1010-c3213b04e-tier1-r1 · Q-DEFAULT-0 / T4 / Q-ERR-201 · reject · held KS-1185-F1 / F4.
- 2026-09-17-ks1180-1029-cd3580e1f-tier2-r1 · D-T1-ALSO-READ / R-1029-4 D5 · reject · test-witness properties, held KS-1227.
- 2026-09-17-ks1187-1019 r1+r2 · Q-WFIX / G-HARDFALSE / F-1019-3 · reject · erasure scope door (authz); G-HARDFALSE held KS-1212.
- 2026-09-17-ks1195-1017 r1+r2 · G-OAUTH / G-UNKOPT / G-JWTCATCH / G-BUCKET-HASH / G-CLAIM-IGNORED · reject · API-key/JWT/OAuth surface; KS-1205 held.
- 2026-09-17-ks745-1012 · F-7 six identity/role-gate tampers · reject · authz (401, role gate, forwarded identity).
- 2026-09-17-ks744-1028 / ks1207-1023 / ks839-1026 / ks999-1013 / ks1213-1031 / ks1202-1024 / ks844-1006 / ks871-1011 r1+r2 · reject · auth surfaces or already held (KS-1221, KS-1220, KS-1188, KS-1229, KS-1202-NB + excluded file, KS-1181/1182, KS-1192).
- ks1211 x4 / ks528-1025 / ks763-1033 / ks769-1020 / ks864-1007 / ks1176-1014 r1 deps+audit gates · reject · no product tamper row at 0 red found BY GREP (report not read whole; dependency / baseline gates; #1007 G-2 pinned by #1009).

## Search round 2026-09-19 (round 4, gate tampers 09-14..16)

Pinned sha `59412d0575dff3243f5f0ccd1e50608ddb920d6c` (origin develop by `ls-remote` at start and end, unchanged since rounds 1-3). Source: every `report.md` in `Testing Agent MAIN/projects/secuura/reports/` dated 2026-09-14 / 15 / 16 (27 dirs), grepped for unpinned / no-cell / 0-red / GREEN tamper rows and findings, newest first. Measured in a fresh `--shared` scratch clone `clone_r4` (prepare_clone.sh farm; originate `npx jest`; bash suites `/bin/bash` from the clone root). **2 fits, 17 reject rows.** Nothing queued, nothing run on the model.

- 2026-09-14-919-ks739-tier2-r1 · F1 T4 (`documents.ts:1707` `.json().catch(() => ({}))` -> `.json()`; a non-JSON 4xx body flattened to 502) · **FIT** · 0 red / 16 file, 0 / 767 whole originate without the cell; with it exactly the new cell reds (AssertionError, got `[502, "BAD_GATEWAY"]`), 17/17 and 768/768 at the tip · brief `night/briefs/KS-739-F1.md`, input `night/inputs/test_only_739F1.json` (builder rc 0); real test_only checker on the brief's own diff = PASS 8/8 (positive control, not a model run).
- 2026-09-14-ks991-903-a4f71cde6-tier2-r2 · R-1 Tg-B (`.githooks/pre-push:163` the `!=` clause dropped; a CURRENT local develop gets the KS-991 BEHIND notice) · **FIT** (NEW bash file `pre_push_hook_current_develop.test.sh`; `pre_push_hook_base.test.sh` is held by READY_KS-910) · 0 red without the file (base suite 28/0, preflight_deps 56/0); with it `3 passed, 1 failed`, exactly its cell · brief `night/briefs/KS-991-R1.md`, input `night/inputs/test_only_991R1.json` (builder rc 0); real test_only checker = PASS 8/8.
- same #903 report · R-2 Tg-E (is-ancestor -> true) · reject · already reds CASE 6 (27/1); the "only via the prefix" weakness is a test-wording record, not a 0-red tamper. R-3 (diverged shape) · reject · stated scope, not a defect.
- 2026-09-16-ks932-1004-6d077d3fe-tier1-r1 · F-1 DNS-layer refusal unpinned · reject · = held READY_KS-1179-F1 (safeOutboundRequest DNS classification). F-2 (`203.0.113.7` hang dependence) · reject · test flakiness, no product tamper.
- 2026-09-14-ks931-873-c624c9a8d-tier1-r1 · T4 DNS-layer `'blocked'` · reject · same property, held KS-1179-F1. T5 (write/end catch -> throw, 0 reds) · reject · Peter's "unreachable" wrap, no reachable red.
- 2026-09-16-ks1165-1001-3925d4c07-tier1-r1 · F-1 T3/T4 (CSRF off outside production / protect mount moved) · reject · CSRF wiring surface; pinned by #1003's C-layers / C-401 cells (per the 09-16 #1002/#1003 gate, S-T5 reds both). R-5 (gateway suite CSRF-blind under NODE_ENV=test) · reject · pre-existing harness design.
- 2026-09-16-ks1123-1002-ks1165-1003 · Q-WRAP (CSRF mounted through anonymous arrows; census C-layers false green) · reject · contrived test-structure tamper on a census cell; CSRF surface.
- 2026-09-16-ks1130-999-ks960-1000 · item 3 P3 (shadowed `typeof`, 0 red of 364) · reject · dead clause by design, no red-first cell can exist; ks960 = held READY_KS-960.
- 2026-09-15-ks726-805-a4d182bf9-tier1-r3 · 8j (confirmed-before-polled ordering) · reject · = held READY_KS-1171-8j. 8f T8 (`:545` `ALREADY_INCLUDED_REPLY` clause) · reject · its intended outcome waits on the open F2 ruling (long-form reply rests vs retries). 8f T9 (`known === writtenAheadTxHash`) · reject · unreachable in one process (two-process race). 8k · reject · pre-existing, unreachable via a real hash.
- 2026-09-14-ks726-805-cd5e62e96-tier1-r1 · T8/T9 · reject · same as 8f above.
- 2026-09-14-L7-918r2-924-925 · R-918-A · reject · = held READY_KS-1153-R918A. R-918-B (nested guard basename resolution) · reject · pre-existing design, run_code_guards (excluded file). R-925-A / F-925-4 · reject · preflight.sh (excluded).
- 2026-09-14-ks1004-912-ks1059-937 · item 3 `inFlight &&` · reject · pinned (#937 DEFECT cell D1 reds). Tg-A / Tg-B · reject · red K2/K6/N6 and K6/K7 (pinned).
- 2026-09-14-ks1061-931-795307023-tier2-r1 · T3 completeness guard blind · reject · a test-file tamper, not product.
- 2026-09-14-ks764-577-...-6da848891-tier1-r1 · R7 (`sOrganizationUuid` fold order) · reject · a latent product record, not fixed behaviour; T6/T7 inert by design.
- 2026-09-14-ks823-983 / ks823-835-1151-1150-AUTH4 / ks835-984 / ks790-982 · reject · OAuth / JWT / refresh-token surfaces (auth, excluded).
- 2026-09-14-ks798-841-799-881 · R4 (jsdom runs text/plain script) · reject · not reproducible under the suite's jsdom; frontend.
- 2026-09-14-874-ks926 / 879-ks945 / 916-ks993-ks1026 / 939-ks1068 / 988-ks704 / ks487-720 / ks973-989 / ks791-813 · reject · no product tamper at 0 red found BY GREP (report not read whole; doc / install / baseline gates, or every tamper row red).

## Search round 2026-09-19 (round 5, gate tampers 09-10..13)

Pinned sha `59412d0575dff3243f5f0ccd1e50608ddb920d6c` (origin develop by `ls-remote` at start and end, unchanged). Source: every `report.md` in `Testing Agent MAIN/projects/secuura/reports/` dated 2026-09-10 (none exist) / 11 / 12 / 13 (35 dirs, 2 with no report.md), grepped for unpinned / 0-red / stays-green / false-green rows, newest first; code path at the tip checked FIRST (older gates). Measured in a fresh `--shared` scratch clone `clone_r5` (prepare_clone.sh farm; api-gateway `npx vitest run`). **1 fit, 26 reject rows.** Nothing queued, nothing run on the model.

- 2026-09-13-ks1062-932-c72607d58-tier1-r1 · F-1 T3 (`startup-migrations.ts:1209` tenant summary level forced `'info'`) + a sibling (`:1210` INCOMPLETE headline forced to `complete`, KS-950 #973) + T6 (`:836` first-error guard dropped, LAST error logged) · **FIT** (one ticket, three tampers; NEW file `ks1062-startup-migrations-tenant-summary-first-error.test.ts`, ks1125's file left alone because its READY is marked held) · 0 red / 613 whole api-gateway suite under each tamper without the file; with it 616/616 at the tip and exactly one red of 616 per tamper, by assertion (`firsterr` got `qa statement 39 refused`; `summary` got `[false, …]` twice) · brief `night/briefs/KS-1062-F1.md`, input `night/inputs/test_only_1062F1.json` (builder rc 0, description == brief byte for byte); real test_only checker on the brief's own diff = PASS 8/8 (positive control, not a model run).
- same #932 report · T1 / T2 / T4 / T5 · reject · pinned since by ks1125 (#1040): its ghost cell reds each (READ from the cell: T4 makes `does not exist` benign, T5 makes `failed` 39).
- 2026-09-13-ks1103-965-d63b27ab3-tier2-r1 · F-2 T5 (`hash` third in the alias chain, 0 of 575) · reject · = held READY_KS-1118-F2.
- 2026-09-13-ks1020-966-1f0d08841-tier1-r1 · F-1 T4 (memory-path prefix) / F-2 T5 (DB miss never reaches memory) · reject · = held READY_KS-1120-F1 / KS-1120-F2.
- 2026-09-13-ks1071-1070-967-968-1b7c03a22-tier2-r1 · F1 Tx (tier-2 statusless) · reject · pinned since by `ks1073-tier-2-verify-has-no-statusless.test.ts` (#1005). F2 Tb / F3 Tc · reject · pinned by KS-1123 (#1002). #968's second row · reject · superseded: tier 2 has no statusless carve-out since #1005 (READ).
- 2026-09-13-ks1069-969-fb23ca6aa-tier2-r1 · F2 (tier-2 E rows) · reject · pinned since by KS-1130 (#999, tier-2 twins E1/E7/E3). F1 (string blockHeight) · reject · an owner ruling, not fixed behaviour.
- 2026-09-13-ks950-962-973-dfed981d0-tier1-r1 · F-973-2 (IS DISTINCT FROM guard) · reject · closed in r2 by ID3.
- 2026-09-13-ks950-962-973-ca2a9109c-tier1-r2 · CN-2 Tg3 (slug arm deleted, 0 of 27) · reject · still unpinned (suite unchanged since #973), but the only home is `ks949_main_seed_idempotence.test.sh`, which needs PostgreSQL + tsx + a built packages/shared; the test_only bash runner runs on an un-farmed clone, so the suite would die at its precondition (READ, not run). CN-1 · reject · a test-internal assertion, no product tamper.
- 2026-09-13-ks963-970-ae274f7cb-tier1-r1 · F-B / F-C Tg5 · reject · auth (password-reset / wallet), excluded.
- 2026-09-13-ks1052-972-b3ce8c9e7-tier1-r1 · reject · auth / MFA / OAuth surfaces, excluded.
- 2026-09-13-ks924-901-980 (r1, r2) · T2 / Tg-D / Tg-F · reject · the guard lives in a test file (ks860); Tg-D ruled "NOT a proposal".
- 2026-09-13-ks885-886-978-13b767a7f-tier2-r1 · GF-1 Tg2 · reject · tamper on a test file (ks879 guard).
- 2026-09-13-ks876-891-894-895-976-0d5f5e6ab-tier2-r1 · R-4 / R-5 / R-6 · reject · the guard (`offendingListenSites`) is a test file; R-4 unpinned by design.
- 2026-09-13-ks828-900-981-04807ea0e-tier2-r1 · GF-1 / GF-2 / GF-3 · reject · open defects of a test-file guard walk, not fixed behaviour.
- 2026-09-13-ks1126-975-8da20edbd-tier2-r1 · Ti · reject · a test-file guard (ks781).
- 2026-09-13-ks922-941-971-c229aa256-tier2-r1 · F1 Tg (`orchestrate.sh:119`) · reject · its home `orchestrate_jobs.test.sh` is excluded (held KS-1134).
- 2026-09-13-ks878-867-974-8da602309-tier2-r1 · F-2 / Ti · reject · 04-container-trivy.sh area (excluded).
- 2026-09-13-ks877-977 (r1, r2) · Tr / Tv · reject · Tr is behaviour-inert on bash 3.2 (no red possible); Tv a suite-copy tamper.
- 2026-09-13-ks1109-963-90d7d0c75-tier2-r1 · QA-963-1 · reject · a test-helper defect, no product tamper.
- 2026-09-12-ks1099-960-0e70ed1c7-tier2-r1 · QA-960-4 (column +1) · reject · pinned since by #963 ("pin the column").
- 2026-09-12-ks1094-958-ffb285752-tier2-r1 · QA-958-3 (PASSWD) · reject · pinned since by #961 (R_pw row).
- 2026-09-12-ks1098-961-644965d90-tier2-r1 · QA-961-2 Q1 / Q2 (`k6_docker.ts:97` / `:107` cluster regexes narrowed, 0 of 1027) · reject · STILL UNPINNED at the tip (READ: k6DockerRedaction rows pin `-qe` only), but TOOLING-BLOCKED: systemTest/performance cannot be built into a test_only input today — the builder's service walk stops before checking `repo_subdir` itself, prepare_clone's tool mode farms `<repo_subdir>/node_modules`, and the checker runs `npx vitest run` without `--config vitest.unit.config.ts` (the suite needs its `globals`) (READ from source, not run). The best systemTest candidate if that is fixed.
- 2026-09-12-ks1029-962-ac6f4fa91 (r1 + relaunches) · T1-T5 · reject · every tamper red (T5 pinned N1).
- 2026-09-12-kintsugi-deploy-4554b25e2-tier1-r1 · F-2 · reject · ks1101-health-aggregates (excluded). F-4 · reject · fixed by #965 (its gate row above). Others pre-existing / UI.
- 2026-09-11-ks1086-953 (r1, r2) · QA-1 T8 · reject · closed in r2. QA-7 T13 · reject · the same lines are rewritten by held READY_KS-1089 (per-cause headline).
- 2026-09-11-ks1041-951 (r1, r2) · R2-3 · reject · gateway vouch / trust-header identity (auth surface).
- 2026-09-11-push-protocol-d2a53096 · reject · not in the Secuura repo (a 5_Project_History tool). ks597-954 / ks1095-957 / ks1092-956 · reject · GO with no 0-red tamper (docs gates / every row red) BY GREP.

## Search round 2026-09-19 (round 6, the #1050-#1060 gate's NOT-PINNED)

Pinned sha `3c447abc7714e98fbba596aa1045b7bb47a6d215` (origin develop by `ls-remote`; #1052 on top of #1060 `665cc187a`). Source: `2026-09-19-batch1050-1060-tier1-r1/report.md` § NOT-PINNED + G2. Measured in a `--shared` scratch clone (prepare_clone.sh farm; api-gateway `npx vitest run` on the ONE file). test_only locates a tamper by `Line:` + exact `From:` only (no scope-anchor field); lines pinned AT THE TIP and the scope proven. Nothing queued, nothing run on the model.

- 2026-09-19-batch1050-1060-tier1-r1 · #1053 KS-1258 YARN / YARNDEV / NODE (`system-status.ts:592`, optional block under `// KS-1258: a DEGRADED optional service…` at :581; the same `From` also at :576, the KS-1248 required block) · **FIT** (N53-1; MODIFY the ks1258 file: widen the N44-1 cell's regex by `yarn start|yarn dev|yarn run|node services`, one `-`/`+` pair; NPMSTART + COMPOSE kept as no-regression tampers) · without the hunk YARN/YARNDEV/NODE 0 red of 4; with it each of the 5 tampers reds exactly the N44-1 cell of 4, by assertion, controls green; YARN planted at :576 instead reds 0 (the wrong block grades nothing) · brief `night/briefs/KS-1258-N53-1.md`, input `night/inputs/test_only_1258N53-1.json` (builder rc 0, description == brief byte for byte, `diff_file_headers` present); real checker on the brief's own diff = PASS 8/8.
- 2026-09-19-batch1050-1060-tier1-r1 · #1054 KS-1230 NULLASEMPTY (`admin.ts:1132`, ×1; the gate's two-line To joined on ONE line for the builder) · **FIT** (N54-1; MODIFY the ks1230 file: the N45-5 cell's expect also reads the stored `allowedDocumentTypes` = `null`, one `-`/`+` pair; NULLREFUSED kept as the no-regression tamper) · without the hunk NULLASEMPTY 0 red of 7; with it NULLASEMPTY and NULLREFUSED each red exactly the N45-5 cell of 7, by assertion (`[200, 1, []]` / `[400, 0, undefined]` vs `[200, 1, null]`), controls green · brief `night/briefs/KS-1230-N54-1.md`, input `night/inputs/test_only_1230N54-1.json` (builder rc 0, description == brief byte for byte, `diff_file_headers` present); real checker on the brief's own diff = PASS 8/8.
- 2026-09-19 09:5x · KS-1260 (bash_patch, N41-1 ratio on the KS-1209 early-failure verdict, `preflight.sh:703`) · **FIT** — one hunk `@@ -702,3 +702,5 @@` (1 `-`, 3 `+`: count `n_ran` inside the early block, append ` ($n_ran/$TOTAL_LEGS legs ran)`) + NEW `scripts/__tests__/preflight_failure_verdict_keeps_ratio.test.sh` (77 lines, 3 CONTROL + 2 🔴, ref = the KS-1261 suite). Pinned `3c447abc7`. Measured: tip 3/5 (both 🔴 red by assertion `1 no`), fixed 5/5; planted `$TOTAL_LEGS/$TOTAL_LEGS` reds the skip cell only; real checker on the brief's own diff PASS 7/7 strict, B6 six siblings unchanged. Brief `night/briefs/KS-1260.md`, input `night/inputs/bash_1260.json` (description == brief bytes). Reading flagged for Wednesday: the ticket's "skipped-legs lines" were never printed on develop's pre-KS-1209 FAILED path (ratio only, blob 28d3636c1 :704) — brief restores the ratio only; raise Closes vs Refs is Wednesday's call. NOT queued.

## Search round 2026-09-19 (round 8, pre-09-10 gate reports + KS tickets filed after the 01:38 census)

Pinned sha `3c447abc7714e98fbba596aa1045b7bb47a6d215` (origin develop by `ls-remote` at start, 10:2x AEST; object local). Sources: (1) `fleet/qa-agent/gatesets/` holds NOTHING before 2026-09-14 (earliest dir `2026-09-14_gate799`, `ls`), so the pre-09-10 gates were read from `Testing Agent MAIN/projects/{secuura-blockchain,secuura-platform-k,secuura-ks969-892}/reports/` 09-07..09-10 and `secuura/reports/` 09-06/09-07, grepped for unpinned / 0-red / stays-green / no-cell rows, newest first; (2) KS tickets numbered ≥ 1255 (Linear read-only, comments `first:50`, 0 comments on every one read): KS-1272..1278 post-date the census and KS-1255/1256/1257/1259/1269 sat only under "names no product file". Measured in a `git clone --shared --revision=3c447abc7…` scratch clone (`clone_r8`, node_modules farmed by `tasks/code_patch/prepare_clone.sh`). **2 fits, 19 reject rows.** Nothing queued, nothing run on the model.

- KS-1276 · `docs/VOCABULARY.md:165-166` · **FIT** (doc_patch; one hunk `@@ -164,4 +164,4 @@`, 2 `-` / 2 `+`, the PII caveat opens with "is **encrypted at rest**"; section `## 3. Lifecycle events` :116-172; tokens `**encrypted at rest**` / `2026-07-31;` 0 before, controls `encrypted at rest` 1, `unencrypted JSONB` 1) · brief `night/briefs/KS-1276.md`, input `night/inputs/doc_1276.json` (builder rc 0, description == brief byte for byte) · real `tasks/doc_patch/checker.sh` on the brief's diff = **PASS 8/8**, D2 strict; negative control (line 166 only) = FAIL (2) D7+D8. Brief rewords rather than the ticket's literal drop (which leaves no verb) — raise wording is the reviewer's.
- KS-1269 · `vc-issuer/src/routes/status.ts:230` · **FIT** (code_patch vitest; ONE pure-insertion hunk `@@ -230,3 +230,7 @@`, 4 `+`, trailing context :230-232; NEW `ks1269-status-revoke-refuses-a-non-integer-index.test.ts`, 82 lines, 3 controls + 3 🔴, ref ks444 dispatch double) · tip: 3 failed / 6 run, exactly the 🔴, `[200, null, true]` vs `[400, 'BAD_REQUEST', false]` (assertion); after: 6/6, whole vc-issuer 114/114, tsc rc 0; planted `>= 0` wrong fix reds the -1 control only · brief `night/briefs/KS-1269.md`, input `night/inputs/code_1269_brief.json` (builder rc 0, "prompt source: WEDNESDAY BRIEF", 3 red cells declared) · real `tasks/code_patch/checker.sh` = **PASS 7/7**, A2 strict. `/revoke` only (`/unrevoke` left for the reviewer); same file as held READY_KS-692 (hunk :31-43), no overlap.
- KS-1275 · `originate.openapi.ts:1847-1861` · reject · two files (the `.ts` description + the regenerated `docs/openapi/secuura-api.yaml`); the `.ts` half alone leaves the published yaml drifted, so it does not stand alone (READ from the ticket; `check:openapi` drift not run).
- KS-1272 · `startup-migrations.ts` platform list (~:1060-1093) · reject · the red is a PostgreSQL 22P02 cast error — needs a real uuid-typed table (no PostgreSQL on this machine, round 1); plus "Decide which declaration is canonical" (decision).
- KS-1257 · platform-settings partial write after expiry · reject · decision-class ("Merge the write over the defaults (or over the current value)"), measured only over a stateful Redis double.
- KS-1255 · spec-example guard E7 floor · reject · decision ("Decide the floor … measure them"), systemTest/spec-guard surface.
- KS-1256 / 1259 / 1273 / 1274 / 1277 / 1278 · not briefed, TITLE ONLY · 1256 = the KS-1231 allow-list (Claude seat); 1259 = suite isolation (no product red); 1273/1274 = `Testing/jobs/04-container-trivy.sh` (excluded file); 1277 = `documents.ts` /revoke comments beside KS-1264's in-progress hunks; 1278 = a two-request race (no single-process red).
- 2026-09-10-pr935-round2-tier1 · F10 (`pending` tier-2 cell; open default) · reject · closed since by KS-1071: `confidenceForAnchorStatus` default returns off-chain-only (`verification.ts:256`), ks1071 test pins `map('pending')` (:259) and a tier-2 `status: 'pending'` cell (:227) (READ, `git show`). F5/F6 · reject · tier 2 can no longer enter the carve-out (`:722` KS-1073, tier-1 only). F7 (`simulated` on tier 2) · reject · a product change, not a pin, and "not reachable today". F9 · reject · = KS-1072 (queue.md history).
- 2026-09-07-ks978-897-tier2 · "case-insensitive" clause unpinned · reject · pinned since: `packages/shared/src/__tests__/ks780-normalise-org-id-one-implementation.test.ts:40-41` P2 CASE (READ). "preserved in the registration metadata" · reject · no product line named, not measurable from the report.
- 2026-09-07-ks969-item1-pr892 · F8 (`pre-suite.ts:113-115` DEGRADED to stderr, 8/0 under T4) · reject · systemTest (Peter's authority; systemTest tooling-blocked per round 5).
- 2026-09-07-ks970-894-tier1 · F-2 (malformed `sub` refusal unpinned, 179 green) · reject · JWT subject handling (auth, LAST).
- 2026-09-07-ks952 (pr890 r1, r2) · colliding-key / namespacing · reject · auth key namespace surface.
- 2026-09-07-ks597-889 (tier1, tier2, round2) · tenancy predicate deleted = 8 passed; `platform_admin` arm no cell · reject · needs a real database (report's own words) / authz policy.
- 2026-09-08-ks963-907-tier1 · `userRepo.ts:380` raw message · reject · services/auth (excluded).
- 2026-09-06-s140b-ks859-858 · F-QA-03 (`p.parent.expression === p`, 222/0) · reject · a guard-walk clause in the body-parser-order guard (report's evidence; the clause's file NOT re-read) — test-guard class, rounds 3-5 precedent.
- 2026-09-06-s140c-ks916-864 · CASE 7 stays green · reject · both halves red-proved (CASE 8 / CASE 9, the report's T1/T2).
- 2026-09-06-s140c-ks868-865 · F3 Stage-2 stub pinned by no cell · reject · a test-stub property, no product tamper.
- 2026-09-08-892-round5 / ks989-906 / 2026-09-09-ks1013-pr910 / ks963-pr913 / qa-gate-ks754-pr914 / s161-batch-six-prs / pr930-ks1052 / 2026-09-10-qa-tier1-pr935 / 2026-09-06-ks720-871 / 2026-09-07-round3-tier2 (ks969-892) · reject · no product tamper at 0 red found BY GREP (hits were stated fail-conditions, red counts, or a call-site note on a test harness; reports not read whole).
- NOT READ (stopped at 2 fits): `secuura/reports/` 2026-09-01..09-06 except the rows above (21 dirs `s96`..`s118` carry no report.md at all, `ls`); the rest of the 09-05/09-06 `s125`..`s140` gates.

## Search round 2026-09-19 (round 9, post-census tickets + the unread 09-01..09-06 secuura gates + T5 halves)

Pinned sha `3c447abc7714e98fbba596aa1045b7bb47a6d215` (origin develop by `ls-remote` at start and at end, 11:xx AEST; unchanged since round 8). Sources: (1) Linear KS `createdAt > 2026-09-18T15:38Z` (the 01:38 AEST census; Wednesday's corrected cutoff) — **7 tickets, KS-1272..1278, positive control KS-1276 present; nothing numbered above KS-1278 exists**, all 7 already carry round-8 verdicts and none has `updatedAt` after round 8 (all 2026-09-18T22:27/23:25Z); (2) `Testing Agent MAIN/projects/secuura/reports/` 2026-09-05 / 09-06 gates round 8 did not read, and the 2026-09-01..09-03 `rows-through-code` reports (they DO carry `report-*.md` files — round 8's "no report.md" was a filename miss), ranked by a case-insensitive grep for unpinned / no cell / stays green / 0 red / unasserted, then the hit sections read; (3) T5 + unverdicted census rows. Measured by `git show`/`git grep` at the pin and one scratch `git clone --shared` (`clone_r9`, nothing run in it). **0 fits.** Nothing queued, nothing run on the model.

- KS-1272..1278 · (round 8 rows) · reject · no post-census ticket beyond round 8's seven; `updatedAt` unmoved, verdicts stand.
- KS-1051 · `preflight.sh` + `.githooks/pre-push` · reject · decision-class ("Fix shapes (not a ruling)", three options); two files; preflight.sh = held KS-1260's file.
- T5 / census rows KS-491, 579, 581, 627, 746, 915, 953, 1019, 1084 · reject · verdicts already in `queue.md` history (reviews / features / design / CLASS mechanism / jest-originate L3a file); every other T5 row carries a verdict above.
- 2026-09-06-ks921-870 · `scripts/check-shared-relink.sh` F-1..F-9 · reject · fixed since: `2f6b30fde` (KS-921 gate round F-1/F-2/F-4/F-5), KS-930 x6, KS-945 `852e1fff7` (fail-closed install detector); `:108` class grep now `-i`, `:126` cross-check present, F-8 header census removed (`:31-35` READ).
- 2026-09-06-ks914-868 / seat-a-ks914 · NOT TESTED #4, `ssrf-guard.ts:486` `resolved.addresses[0]` out of several · reject · contrived tamper: every address in the list is already classified public, so which one is pinned is not a security property; the meaningful half (the pin IS a classified address, via a mocked DNS name) = held READY_KS-1179-F1 cell 5.
- 2026-09-06-s139-ks843-845-round3 · F-12 (refused-erasure audit row path `/`) · reject · fixed by KS-871 `523f283c6` (#1011, `auditPath` captured at entry `audit.ts:224`, used `:294`). Residual NOTED for Wednesday, not briefed: the catch-block warn at `audit.ts:333` still logs `path: req.path` (the trimmed remainder on a refused request) — KS-871 is **In Progress** (a seat has it; `build_input.sh:155` refuses), so it belongs to that seat.
- 2026-09-06-s136-ks832-836 · 3c/Q-3 (raw `0x7F` in the self-scanning test file, 195/195 green) · reject · test-guard class (rounds 3-5 precedent); no product tamper.
- 2026-09-06-s140c-ks899-863 · a service leaving the corpus, 22 cells green · reject · test-guard class (spec/corpus floor).
- 2026-09-06-s140b-ks857-859 · tamper (a) green on the equality leg · reject · measured by design (N-3 cell reds it, report §6); not a gap.
- 2026-09-06-s139b-ks854-855 F-1 / s140c-ks904-862 F-904-QA-02 · reject · bash-suite unasserted preconditions; F-1 closed by PR #860 (KS-881, its subject line); suite-harness, no product red.
- 2026-09-06-s137-ks386-839 F-1..F-5 · reject · F-1 needs a real DB without migration 045; F-2/F-3/F-4 guard/tsconfig; F-5 pre-existing KYC timing (decision).
- 2026-09-05 s125..s133 (ks781, ks795, ks796, ks797, ks804, ks815, ks819, ks820-821, s131-ks722, s133-f1-prose, s134-f1-round2) · reject · OAuth / MFA / credential-door surfaces (auth, excluded).
- 2026-09-05/06 s128-ks800, s131-ks800, s133-ks816-828 (x2), s134-ks827, s128-ks802, s138b-ks833-842, s137-ks833-838 · reject · body-parser-order / entrypoint guard instruments (test-guard class); ks802 F-01 = KS-801's coverage (auth pin).
- 2026-09-05 s128-ks792 F-1..F-4, s133-fuse-829 F1..F4 · reject · audit-baseline prose/policy (F2 id-only suppression = design); no product red.
- 2026-09-03-s116 report-796 F-796-01 / 02 / 03 (`scripts/audit/audit-gate.mjs`, `audit-locks.mjs`) · reject · still open at the pin (gate-exit-codes.test.mjs: 0 hits for `INDETERMINATE|AUDIT_REPORT_PATH`, 0 for `corpus could not be established`; control: 6 spawn hits) but: node `--test` .mjs tooling no checker covers (`build_input.sh` refuses non services/*|packages/shared); F-01 needs a new env seam (design); F-03 contradicts the code's own stated SKIP contract (`audit-locks.mjs:228-233` comment) — a ruling.
- 2026-09-01..09-03 rows-through-code (s96..s116: report-771/774 platform-scope mocks, 775, 783-ks708 F-6 Polish, ks764-org-arm, 785 citations) · reject · closed by later rows (774 closes 771's F-9) or Polish/test-naming; ks764 org arm = API-key revoke policy (auth).
- NOT READ (stopped with 0 fits, sources exhausted to grep depth): the 09-06 s138/s139/s140 tier-2 reports beyond their grep hits; 09-01..09-03 reports with 0 grep hits (not read whole).

## Search round 2026-09-19 (round 10, AUTH TEST-ONLY)
Pinned origin develop `3c447abc7714e98fbba596aa1045b7bb47a6d215` (ls-remote at start; measured there). At 12:46 AEST origin moved to `c8f3bbe28` (#1061 + six test-only merges, 9 files); every blob both fits depend on is identical at both tips (proxy.ts 795ae7ca3, auth.ts bf09d315a, index.ts db127dbfa, ks1215 test 75006b5cf). Boundary: TEST-ONLY, zero product lines; anything needing one product line = reject (Kam-class).
- KS-1238 (ii) · `api-gateway/src/routes/proxy.ts:677` + `:700` · **FIT** (test_only NEW file `ks1238-hand-forwarded-routes-send-no-caller-bearer.test.ts`, 115 `+`, 4 RED + 2 controls; tampers SIGRAW/TPVRAW = gate X-FETCH-RAW) · 0 red of 615 whole suite per tamper at tip; 2 red of 6 by assertion with the file · real checker PASS (8/8) · brief `night/briefs/KS-1238-F1ii.md` · input `night/inputs/test_only_1238ii.json`.
- KS-1238 (i) · `api-gateway/src/middleware/auth.ts:299` · **FIT** (test_only MODIFY `ks1215-…-callers-bearer.test.ts`, one insertion `@@ -287,2 +287,8 @@`, 6 `+`; tamper BEARERONLY = gate X-BEARER-PREFIX-ONLY) · 0 red of 615 whole suite at tip; 1 red of 21 by assertion with the cell · real checker PASS (8/8) · brief `night/briefs/KS-1238-F1i.md` · input `night/inputs/test_only_1238i.json`.
- KS-1238 (iii) · `routes/platform.ts:254` · reject · no cell can red it: the route is `requireSuperAdmin` (connector 403, gate 0 hits in 3,258 cells) and for a JWT-only super-admin `rawAuthorization` == the header (READ + gate MEASURED).
- KS-1238 (iv) · register-connector LIVE JWT on a refused exchange · reject · not unpinned: its tamper R-PLATFORM-RAW-FALLBACK already reds the REVOKED register cell (gate: 1 red); a LIVE cell adds an input, not a pin.
- KS-1205 (G-OAUTH / G-UNKOPT / G-JWTCATCH, `rateLimitEnforce.ts:61`, `auth.ts`) · reject (HELD) · KS-1205 is HELD (READY_KS-1205-F3 G-BUCKET-HASH); G-OAUTH is a distinct unpinned seam of the same ticket — Wednesday's ruling whether a held ticket's second seam may be briefed.
- ks1195-1017 r2 N-1 (G-BUCKET-HASH / G-BUCKET-RAW-2, `auth.ts:313`) · reject · already held as READY_KS-1205-F3 (tip: 0 test files name rateLimitBucket, so still unraised).
- ks1195-1017 r2 N-2 (JWT `rateLimitBucket` claim) · reject · a product defect (fix-shape changes auth.ts + rateLimitEnforce.ts) — needs a product edit, Kam-class.
- KS-745 F-7 (`routes/audit-export.ts:85`, `:91`, `:132`; gate Q-401-OPEN / Q-ADMIN-OPEN / Q-NOAUTH 0 red) · reject · the ticket's own 2026-09-17 comment: "Answer R-9 first, before building anything" (the route may be RETIRED; unreachable as shipped, index.ts:800 has no authenticateToken). Test-only and measurable, but blocked on that scope ruling — Wednesday's.
- KS-1131 (services/auth `ks963-preauth-rethrow.test.ts`) · reject · test-only, but F-A is a false RED (the fix must make cells GREEN under Tg3/Tg4) and the fix is a helper refactor across 3 structural cells; the test_only checker grades tamper→red only.
- KS-1244 (duplicated x-api-key) · reject · product defect (auth bypass; fix = refuse a repeated header in auth.ts) — needs a product edit.
- KS-1208 (token without role/userId 500s) · reject · product defect + an open shape decision (401 vs guard), per its own recommendation.
- KS-1240 / KS-1241 / KS-1242 (T-2 fetch timeout, T-4 v1 documents never answers, T-1 async middleware no catch) · reject · titles state live product defects — each needs a product edit (READ titles only).
- ks1215-1034 Q-INDEX-RAW-REMOVED (`index.ts:347`) · reject · dead code (0 readers), deletion is a product edit; = KS-1239, already rejected.

## Search round 2026-09-19 (round 11, the #1061-#1069 gate's NOT-PINNED)
Pinned origin develop `51dbedd39ade43cc511278502b2e1e190de641c7` (tree 275cff9ff; `git ls-remote origin refs/heads/develop` at start; all nine PRs merged). Source: `Testing Agent MAIN/projects/secuura/reports/2026-09-19-batch1061-1069-tier1-r1/report.md` NOT-PINNED, 15 rows. Every tamper re-located at develop by its exact `from` text (`grep -nFx`/`-nF`, one hit unless named). Measured in a `--shared` scratch clone (`clone_r11`), the harness `prepare_clone.sh` farm, the real `tasks/test_only/checker.sh`; whole-suite plants restored by bytes. 4 briefs written (cap 4), all `RESULT: PASS (8/8)` T3 strict at `51dbedd39`.
- KS-1206 NULLPASSES · `originate/src/routes/adminConfig.ts:905` (whole line ×1) · **FIT** → `briefs/KS-1206-N61-1.md` / `inputs/test_only_1206N61-1.json` (one brief, 5 cells, 20 `+`) · 0 red of 785 without the hunk; 1 red of 790 with it (the null cell, toEqual).
- KS-1206 ZEROPASSES · `adminConfig.ts:905` · **FIT** (same brief) · 0/785 without; 1/790 with (zero cell).
- KS-1206 FLOATPASSES · `adminConfig.ts:905` · **FIT** (same brief) · 0/785 without; 1/790 with (1.5 cell).
- KS-1206 LOWEROFFBYONE · `adminConfig.ts:905` · **FIT** (same brief) · 0/785 without; 1/790 with (lower-bound-1 cell, `[400,0]` vs `[201,1]`).
- KS-1206 NUMSTRPASSES · `adminConfig.ts:905` · **FIT** (same brief) · 0/785 without; 1/790 with ('100' cell).
- KS-864 ENVNULLISH · `api-gateway/src/routes/system-status.ts:446` (×1; the file's only NODE_ENV read) · **FIT** → `briefs/KS-864-N64-1.md` / `inputs/test_only_864N64-1.json` (ks864d, one cell, 10 `+`, a per-request call with NODE_ENV='' then back to 'dev') · 0 red of 624 without; 1 red of 625 with (`expected '' to be 'development'`).
- KS-1230 NULLSECOND · `api-gateway/src/routes/admin.ts:1132` (×1) · **FIT** → `briefs/KS-1230-N69-1.md` / `inputs/test_only_1230N69-1.json` (one cell, 5 `+`; + NULLREFUSED reds it with N45-5) · 0/624 without; 1/625 with (`[200,1,[null,[]]]`).
- KS-739 NOJSONCATCH_NON403 · `originate/src/routes/documents.ts:1695` (whole line ×1; `json().catch` ×3) · **FIT** → `briefs/KS-739-N66-1.md` / `inputs/test_only_739N66-1.json` (non-JSON 401 + 429, 8 `+`; + NOJSONCATCH reds it with F1) · 0/785 without; 1/786 with (`[502,BAD_GATEWAY,502,BAD_GATEWAY]`). KS-739 archived: Refs only, never reopen.
- KS-1258 N68-1 (REQUIRED block, five `to`s) · `system-status.ts:576` (the `from` is ×2: :576 under `// KS-1248: a DEGRADED required…` :564, and :592) · FIT, NOT BRIEFED (cap 4 reached) · Line+From locates :576 unambiguously for the builder; next round's first pick. Not measured beyond the relocation.
- KS-1258 N68-2 (optional block, six new shapes) · `system-status.ts:592` (under `// KS-1258: a DEGRADED optional…` :581) · FIT only as the allow-list form, NOT BRIEFED (cap) · the gate's own N68-3 says the widened regex reds on benign free text, so the regex form is rejected; allow-list form unmeasured.
- KS-1062 FAILEDMETA · `api-gateway/src/startup-migrations.ts:1213` (×1) · FIT, NOT BRIEFED (cap; heavier) · the 86-line ks1062 fixture has no path to the `skipped++` catch (:1200-1202): both summary cells assert `skipped: 0`; a SKIPPED tenant needs a new fake-Pool failure mode outside migrateDatabase's per-statement handling, unmeasured.
- KS-1101 N3SKIPPED · `api-gateway/src/__tests__/ks1101-health-aggregates-surface-degraded.test.ts:246` · reject (for test_only) · the tamper (`it` -> `it.skip`) is on the TEST FILE; the builder refuses a tamper whose file is the test file, so the checker cannot grade it. The fix (N-3 cell `RAN.add` + an `expected` entry at :255) is a two-line test edit for a Claude seat or a plain PR, not an Ornith brief.
- KS-1260 OLDFORMULA · `Blockchain/Dev/scripts/preflight/preflight.sh:705` (whole line ×1; the `($n_ran/$TOTAL_LEGS legs ran)` tail is ×2, :705/:729) · reject THIS round (cap) · needs a new `run_legs` variant driving 14 of 15 legs in `scripts/__tests__/preflight_failure_verdict_keeps_ratio.test.sh` (harness change, bash_patch/test_only on .test.sh), unmeasured.
- KS-1260 ALSOLINENOOP · `preflight.sh:707` (×1) · reject THIS round (cap) · needs a leg-1 `env_fail=1` + leg-7 failure harness path in the same suite, unmeasured.
- KS-1260 NONEDECLAREDEXIT0 · `preflight.sh:746` (`    exit 1` whole line ×4; this one directly under `This is NOT a pass.` :745) · reject THIS round (cap) · needs a harness where TOTAL_LEGS exceeds the legs driven with no skip; Line+From can anchor :746, unmeasured.
- KS-1258 N68-1 · BRIEFED (post-cap, brief subagent) · `system-status.ts:576` (REQUIRED block under `// KS-1248: a DEGRADED required…` :564; `from` ×2, :576 + :592) · **FIT** (one cell ADDED to the ks1248 test file, not the ks1258 one: its harness already stubs the REQUIRED `anchoring` host; `RED KS-1258 N68-1: the degraded required advice carries no start command in ANY common shape`, the N44-1 pattern, expect `[1, []]`; neither file has a COMPLETENESS ledger) · at `51dbedd39` whole api-gateway: tip 624/624, +hunk 625/625; WITHOUT the hunk all five at :576 red 0 of 624; WITH it each reds exactly 1 of 625 (the new cell, assertion); scope control YARN/NPMSTART at :592 reds only ks1258 N44-1 · brief `night/briefs/KS-1258-N68-1.md`, input `night/inputs/test_only_1258N68-1.json` (builder rc 0, `diff_file_headers` present); real checker on the brief's own diff = PASS 8/8, apply=strict.

## Search round 2026-09-19 (round 12, harder test-only)
Pinned origin develop `51dbedd39ade43cc511278502b2e1e190de641c7` (`git ls-remote origin refs/heads/develop` at start). Measured in a `--shared` scratch clone (`r12/clone`), the real `tasks/test_only/checker.sh`, whole api-gateway vitest suite (624 cells) or all 40 `*.test.sh` suites (742 cells); plants restored by bytes. Every file checked by path against Seat B 4th's seven open PRs and the held N68-1 file: no overlap. 3 briefs, all `RESULT: PASS (8/8)` T3 strict at `51dbedd39`.
- KS-1258 N68-2 (DOCKERRUN / BUNRUN / MAKEUP / NODEDIST / PNPMDEV / TSXWATCH) · `api-gateway/src/routes/system-status.ts:592` (optional block; `from` x2, :576/:592) · **FIT** → `briefs/KS-1258-N68-2.md` / `inputs/test_only_1258N68-2.json` (ks1258 file, one ALLOW-LIST cell `expect([b.length, b[0]?.commands]).toEqual([1, ['# Read…', 'curl -s http://billing.ks1258:1/health']])`, 6 `+`) · 0/624 without; exactly 1/625 with, per tamper; scope control DOCKERRUN/BUNRUN at :576 → 0/625 (cell green) · the allow-list reds any wording change to the two commands, by design (noted for the raise).
- KS-1062 FAILEDMETA · `api-gateway/src/startup-migrations.ts:1213` (x1) · **FIT** → `briefs/KS-1062-N67-1.md` / `inputs/test_only_1062N67-1.json` (ks1062 file; the fake Pool's constructor throws for `qa_skip`, since `new pg.Pool` :823 is outside migrateDatabase's try, reaching `skipped++` :1202; one cell `{migrated:1, failed:1, skipped:1, total:3}`; 6 `+` 1 `-`; + brief-writer tampers SKIPNOCOUNT / SKIPASFAILED at :1202) · 0/624 without; exactly 1/625 with, per tamper.
- KS-1260 OLDFORMULA / ALSOLINENOOP / NONEDECLAREDEXIT0 · `scripts/preflight/preflight.sh:705` / `:707` / `:746` (`    exit 1` x4, pinned under :745) · **FIT, one brief** → `briefs/KS-1260-N62.md` / `inputs/test_only_1260N62.json` (runner bash; `run_legs` gains optional 3rd env-fail list + 4th last-leg; 3 cells; 10 `+` 2 `-`, 4 hunks) · 0/742 across all 40 suites without; with: 745 green, each tamper exactly 1 FAIL (its own cell), all other suites rc 0.
- KS-1205 G-OAUTH · `api-gateway/src/middleware/rateLimitEnforce.ts:61` (`MACHINE_AUTH_METHODS`) · reject · a test-only pin would lock in the side of the `'oauth'`-vs-machine-set question that KS-1156 A.1 has not ruled on (no ruling recorded in candidates); and KS-1205 is HELD (READY_KS-1205-F3). The cell would also have to go through `authenticateToken` in auth.ts, which an open Seat B 4th PR touches.

## Search round 2026-09-19 (round 13, the #1070-#1076 gate's NOT-PINNED)
Pinned origin develop `f9c28a8b82874708edd9de72c40cdb9bfc6ee4cf` (`git ls-remote origin refs/heads/develop` at start; all seven PRs #1070-#1076 merged; the object is local). Source: `Testing Agent MAIN/projects/secuura/reports/2026-09-19-batch1070-1076-tier1-r1/report.md` NOT-PINNED (9 rows) + findings N71-1..N76-2. Every tamper re-located at the tip by its exact `from` (`grep -nFx`/`-cFx`). Measured in a `--shared` scratch clone (`r13/clone`), the harness `prepare_clone.sh` farm, the real `tasks/test_only/checker.sh`; whole-service suites per tamper with and without the hunk, restored by bytes. Excluded files (held READYs) checked by path: no overlap. 4 briefs buildable, all `RESULT: PASS (8/8)` apply=strict at `f9c28a8b8`; a 5th written but NOT buildable (runner detection).
- KS-1230 N74-1 MIDDLENULL · `api-gateway/src/routes/admin.ts:1132` (x1) · **FIT** → `briefs/KS-1230-N74-1.md` / `inputs/test_only_1230N74-1.json` (one cell, 5 `+`, three integrations, middle null) · 0/633 without; exactly 1/634 with (+ NULLREFUSED reds it with N45-5 + N69-1, 3/634).
- KS-1206 N72-1 FALSE/EMPTYSTR/TRUE/ARRAY/OBJECT-PASSES · `originate/src/routes/adminConfig.ts:905` (x1) · **FIT** → `briefs/KS-1206-N72-1.md` / `inputs/test_only_1206N72-1.json` (five literal cells, 20 `+`) · 0/791 each without; exactly 1/796 each with (its own cell, `[201,null,1]`).
- KS-739 N75-1 NOJSON404 / NOJSON5XX · `originate/src/routes/documents.ts:1660` / `:1722` (x1 each; the gate's inserted line re-expressed as a one-line edit of the branch opener) · **FIT** → `briefs/KS-739-N75-1.md` / `inputs/test_only_739N75-1.json` (two cells, 12 `+`) · 0/791 each without; exactly 1/793 each with. KS-739 archived: Refs only, never reopen.
- KS-1238 N76-1 RAW516 · `api-gateway/src/routes/verification.ts:516` (`from` x2, :516/:788; pinned by `:515` `// endpoint or on-chain revocation event).`) · **FIT (AUTH surface, test-only, TIER 1)** → `briefs/KS-1238-N76-1.md` / `inputs/test_only_1238N76-1.json` (ks1238 file, 4 hunks, 18 `+` 1 `-`: DOCS const, double records `/api/documents/`, `postVerify` helper, 2 RED + 1 control) · 0/633 without; exactly 2/636 with (`['user:ks1238-live']`, `['user:ks1238-revoked']`).
- KS-1269 N71-1 NULLPASSES · `vc-issuer/src/routes/status.ts:231` + `:300` (`from` x2; anchors :230 / :299 comments) · FIT by measurement, **NOT BUILDABLE** → `briefs/KS-1269-N71-1.md` (flagged do-not-queue; no input) · builder rc 2: `cannot tell the runner of …/vc-issuer` (package.json has jest+ts-jest devDeps beside vitest; no runner pin). Hand-measured: 0/119 each without; exactly 1/121 each with (split NULLPASSES-R / -U). Needs a builder runner pin (Wednesday's).
- KS-1269 N71-3 UNREVOKENEG (`/unrevoke {index:-1}`) · `status.ts:300` · reject · NON-RULED: KS-662 ruled -1 on /revoke only; pinning -1 either way on /unrevoke would make a ruling. Not pinned in N71-1's brief either.
- KS-1269 REVOKEGUARDAFTER404 / REVOKEGUARDBELOWREASON · `status.ts:230-233` · reject · the gate's tampers are 4-line block moves (builder takes a one-line From/To); and vc-issuer is unbuildable by the test_only builder (above). Polish ordering; a one-line re-expression (`&& statusListManagers.get(id)?.getIndex(credentialId) !== undefined`) is possible once the runner pin exists.
- N71-1 SHIPS-WITH facts line / N71-2 / N71-4 / N72-2 · reject · records / ticket prose / renaming an existing cell, not test cells.
- N76-2 (`verification.ts:788`, `/api/certifications/:id/verify`, no gateway auth) · reject · product defect (TICKET, originate side unmeasured); not a pin of existing-right behaviour.
- O-1 (batch/audit-export 401 in-process) · reject · curio, not graded.
