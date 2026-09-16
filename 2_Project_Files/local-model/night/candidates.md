# Ornith candidates — derived 2026-09-16 14:09 from 310 KS Backlog/Todo tickets (read-only, unpaginated)

A CENSUS for the coordinator to brief from, easy → hard (Kam 2026-09-15 16:40 / 18:19). A ticket here is a candidate, not a task: read it, read the file at the tip, write `night/briefs/<id>.md`, then queue it. Auth-shaped titles are excluded (LAST); Peter/Stuart tickets and PR-attached tickets are excluded outright.

## T1 services (vitest, one file) — 14
<!-- REJECTION TABLE, measured 2026-09-16 18:0x by a search commission — do NOT re-derive these:
     KS-746  decision-class: its own words call points 1-3 "a design sketch, not an agreed plan"; spans index.ts + a SQL migration
     KS-839  behaviour UNRULED ("pins whatever behaviour is then ruled correct") + an OAuth scope-authorisation decision surface
     KS-915  needs a ruling plus docs ("What would close it: One of: ..."), no product fix
     KS-579  identity-model FEATURE across auth + gateway + seed; gates KS-582; not one file
     KS-581  feature work (alerting, rate limit, correlation) + a GUID-shape requirement that would redden existing fixtures
     KS-627  its own BLUF: "It is not a patch" — breaking contract change, new crypto deps, WASM/ARM64
     KS-1125 already FIXED at the tip; no red possible; and no vitest mock reaches the bare CJS require('pg')
     KS-1145 needs a real PostgreSQL bash suite; not vitest-gradeable
     KS-960  FITS — briefed as TAMPER-GRADED, PASS 7/7 first sample, READY written
     KS-1173 already exists as a passing READY (READY_KS-1172-B3 covers it)
-->
- KS-1173 (P2) Flow verbs: add `note`, `certified` and `verified` to the lifecycle vocabulary ( — `services/anchoring/src/anchorSchema.ts`
- KS-683 (P2) Anchor-status standoff: a consumer repolls anchors K reports as terminally faile — `services/anchoring/src/index.ts`
- KS-692 (P2) Security: /api/status revoke/unrevoke has no tenant ownership check — an ISSUER_ — `services/vc-issuer/src/routes/status.ts`
- KS-953 (P2) CLASS: editing api-gateway/src/index.ts silently reddens packages/shared, and no — `services/api-gateway/src/index.ts`
- KS-1168 (P3) userRepo.ts: ILIKE search on encrypted PII columns can never match — :1017 and : — `services/auth/src/repositories/userRepo.ts`
- KS-579 (P3) Per-person platform-admin identities — the shared seeded admin cannot carry attr — `services/api-gateway/src/routes/platform.ts`
- KS-581 (P3) register-connector: volume alerting, rate limit, and correlation of refused re-k — `services/api-gateway/src/routes/platform.ts`
- KS-627 (P3) Implement real wallet signature verification (CIP-8/COSE + address binding) — ne — `services/wallet-connector/src/types/index.ts`
- KS-746 (P3) Security events carry no tenant at all — KS-743 had to gate them platform-only,  — `services/security/src/index.ts`
- KS-839 (P3) Security: an allowedScopes of ['*'] bypasses the invalid_scope refusal entirely  — `services/auth/src/services/oauth.ts`
- KS-915 (P3) A clean stack has no supported way to obtain its first privileged account — `services/auth/src/routes/auth.ts`
- KS-960 (P3) Two schema sources disagree on whether users.email is unique — a statement valid — `services/auth/src/repositories/userRepo.ts`
- KS-1125 (P4) api-gateway startup-migrations: the tenant-failure guard `if (outcome.failed > 0 — `services/api-gateway/src/startup-migrations.ts`
- KS-1145 (P4) ks949 suite coverage (KS-950 / KS-962, #973): ID3's capture half has no size ass — `services/api-gateway/src/startup-migrations.ts`

## T2 tooling (systemTest/*, one file) — 0

<!-- REJECTION TABLE (T2b / T3 / T5 / set-aside re-read), measured 2026-09-16 20:07–20:40 by a search commission — do NOT re-derive these.
     FITS from that search: KS-1034 (queued 20:4x). KS-813 = ALREADY FIXED at the tip → a record-defect close for a Claude seat, not model work.
     KS-1031  run-migrations.sh exit 0 on failure is a recorded trade-off (:147-155: known-failing 002 would block compose recreate) — flipping needs a ruling; the doc half is deploy-condition guidance whose premise (target DB state) cannot be measured from here
     KS-630   decision-class ("or decide not to"); adds a leg to the shared pre-push gate
     KS-813   already FIXED at tip — preflight.sh:704-753 prints "N/15 legs ran", PREFLIGHT INCOMPLETE on skips, TOTAL_LEGS check
     KS-1019  [Question] ticket — "should it be typed?" is a decision, not a patch
     KS-1084  "READ ONLY / unverified", measure-first on a two-tenant stack; tenancy/auth surface
     KS-759   auth middleware + shared JwtPayload type (auth surface, multi-file type change)
     KS-967   needs a new line-level credential check designed across two guards plus a deliberate flip of a self-test; credential-guard surface
     KS-1153  a records ticket: each item closes "fixed or accepted with a line" (triage decision); its only code item (preflight.sh:166 TAB tail) is latent — "no such header exists today"
     KS-1051  fix shapes explicitly "not a ruling"; adds a CI/preflight gate
     KS-954   "Mechanism NOT determined. Reproduce before fixing" — needs a live gateway
     KS-1082  guard exists only on unmerged #896 head, not at 48e65c435; systemTest is Peter's; two open questions for Peter
     KS-807   "Decide first" — scan raw bodies (A) vs declare out (B)
     KS-730   gateway part already changed at tip (api-gateway/src/index.ts:1136-1143, KS-727 extracted+redacted); tokenisation/src/index.ts listens on import (:411, no in-process driver); originate parts are 46/15/6 sites (jest, not one hunk); security response surface
     KS-753   open design question for the ruling (503 vs verified:false)
     KS-658   "Filed, deliberately not fixed ... Kam's call" — demo-affecting config
     KS-1055  per-tenant RLS/migrations design; needs real Postgres; multi-file security
     KS-897   the '-' line `  ) >/dev/null 2>&1` is NOT unique at tip (:123, :543, :602); the ticket's fix `( … ) >log || exit 2` catches only the last command (subshell has no set -e) — fix shape needs design; also same file as KS-910
     KS-906   test-logic refactor with no product change (rename a case, change its precondition); a text-grep suite cannot prove the precondition is right
     KS-979   comment fix in a .ts test file: bash_patch B5a runs `bash -n` on the product, doc_patch needs markdown section headings — no tier grades it
     KS-1033  item 1 already briefed and PASS 7/7 at 20:10 (duplicate — see above); item 2 decision-class; item 3 relocation
     title-level only (not read in full; auth/security/feature/review, per skip rules): KS-485 (security review plan), KS-491 (edge/WAF review + auth.ts), KS-576 (bulk re-key feature), KS-624 (VC proof crypto), KS-526 (KMS move), KS-580 (recovery-audit feature), KS-621 (cross-org authz), KS-625 (presentation holder binding), KS-870 (erasure double-auth), KS-1174 (API-key auth failures), KS-1083 (P0 secret provisioning/rotation)
     set-aside, reason not stale, not re-read: KS-1063, KS-1076, KS-1088, KS-1111, KS-1112, KS-1113, KS-1114, KS-1119, KS-1128, KS-1129, KS-1132, KS-1135, KS-1142, KS-1159, KS-590, KS-755, KS-757, KS-777, KS-808, KS-849, KS-880, KS-889, KS-980, KS-981
     skipped per instructions: HELD list, KS-998, KS-1168, KS-1163, KS-1148, KS-1162, KS-1081 (done PASS), KS-866 (briefed), T1 rejection-table IDs
-->
## T2b bash (bash_patch — one script + a *.test.sh beside the reference) — 11
- KS-1031 (P2) KS-754 gate F-4: DEPLOY CONDITION — apply 048 BEFORE rolling the originate image — `scripts/run-migrations.sh`
- KS-1081 (P2) CONFIG DRIFT: two tracked env templates disagree by ~39 vars — bootstrap-env.sh  — `scripts/bootstrap-env.sh`
- KS-1148 (P2) CI-runner environment gaps (one class, two jobs): `Security Scanning` runs `audi — `scripts/run-shell-suites.sh`
- KS-998 (P2) KS-989 gate residue: the formatting gate fails OPEN on missing deps and reads th — `.githooks/pre-push`
- KS-1033 (P3) KS-926 residue: the three guards that could NOT be wired, and what each needs fi — `scripts/run-code-guards.sh`
- KS-1163 (P3) start-secuura.sh never waits for five default-profile, healthchecked services —  — `Start_Up/start-secuura.sh`
- KS-630 (P3) Wire the status-page XSS probe into preflight (or decide not to) — it runs today — `scripts/preflight/preflight.sh`
- KS-789 (P3) CONTRIBUTING.md justifies the hook's degradation and its --no-verify bypass with — `.githooks/pre-push`
- KS-813 (P3) "PREFLIGHT PASSED" is unconditional — step() only prints a banner, and skipped l — `scripts/preflight/preflight.sh`
- KS-866 (P3) Merge protocol: the server-side `sha=` pin protects the PR head, not the base —  — `.githooks/pre-push`
- KS-1162 (P4) Three retired GitHub workflows bake slot-2/3/4 port literals (6982/7182/6732…) i — `scripts/stack_env.sh`

## T3 jest services (originate, governance) — 3
- KS-1019 (P3) [Question] The document's whole `blockchain` block is published as z.unknown() — — `services/originate/src/originate.openapi.ts`
- KS-759 (P3) tenantId is read through two `as unknown as` casts because it is not on JwtPaylo — `services/originate/src/middleware/auth.ts`
- KS-1084 (P0) READ ONLY / unverified: the gateway's own Authorization-only calls to originate  — `services/originate/src/index.ts`

## T4 docs (doc_patch) — 0

## T5 multi-file / later — 22
- KS-1051 (P2) develop is RED on the services/originate jest suite and NOTHING catches it — the — `scripts/preflight/preflight.sh`, `.githooks/pre-push`
- KS-1055 (P2) Per-tenant databases never receive the file migrations — CORE_MIGRATIONS FORCEs  — `services/api-gateway/src/startup-migrations.ts`, `services/tenant-provisioning/src/index.ts`
- KS-485 (P2) Security review — plan, methodology & handover (Platform K) — `services/api-gateway/src/routes/notifications.ts`, `services/originate/src/repositories/documentRepo.ts`, `services/originate/src/index.ts`
- KS-491 (P2) Review F — Edge, WAF, DDoS & anti-automation — `services/api-gateway/src/middleware/rateLimitEnforce.ts`, `services/auth/src/routes/auth.ts`
- KS-576 (P2) Bulk re-key: one admin-authorised rotate across a named set of externalRefs — `services/api-gateway/src/routes/platform.ts`, `services/security/src/index.ts`, `packages/shared/src/db/tenant-guc.ts`
- KS-624 (P2) prism issues VCs with random bytes as the Ed25519 proof and verifies them as pas — `services/vc-issuer/src/routes/credentials.ts`, `services/prism/src/index.ts`
- KS-730 (P2) Security: 71 inline handlers still return err.message verbatim off-production —  — `services/originate/src/routes/adminConfig.ts`, `services/originate/src/routes/gdpr.ts`, `services/originate/src/routes/systemErrors.ts`
- KS-753 (P2) Timestamping fail-closed: a mock TSA fallback must not report verified: true (ex — `services/timestamping/src/tsa/qualified-tsa.ts`, `services/timestamping/src/index.ts`
- KS-967 (P2) Neither credential guard can see a value in a .env.example — one scans the wrong — `scripts/check-no-default-passwords.sh`, `scripts/preflight/no-tracked-credentials.sh`
- KS-1174 (P3) api-gateway collapses every API-key failure into 401 'Invalid API key' — forward — `services/security/src/index.ts`, `services/api-gateway/src/middleware/auth.ts`
- KS-526 (P3) KMS: move platform wallet mnemonic to Key Vault (KS-326 follow-up) — `services/anchoring/src/index.ts`, `services/anchoring/src/cardano/wallet.ts`, `packages/shared/src/vault/key-vault.ts`
- KS-580 (P3) Append-only recovery audit held outside the estate being recovered — `services/api-gateway/src/routes/platform.ts`, `services/security/src/index.ts`
- KS-621 (P3) Document reads are scoped by tenant and owner, never by organization — cross-org — `services/originate/src/repositories/documentRepo.ts`, `services/originate/src/routes/documents.ts`
- KS-625 (P3) /presentations/verify reports a presentation verified without checking the holde — `services/vc-issuer/src/routes/presentations.ts`, `services/vc-issuer/src/routes/credentials.ts`
- KS-658 (P3) The demo VM runs every service as NODE_ENV=development while the code names "dem — `services/auth/src/index.ts`, `services/api-gateway/src/index.ts`
- KS-807 (P3) The control-byte guard cannot see a raw body — findNulBytePath returns null for  — `services/billing/src/index.ts`, `packages/shared/src/middleware/request-limits.ts`
- KS-870 (P3) Every ADMITTED erasure authenticates twice — the door's chain and the catch-all  — `services/api-gateway/src/routes/proxy.ts`, `services/api-gateway/src/middleware/auth.ts`
- KS-910 (P3) Preflight leg 12 executes ZERO suite cells — it is a reachability check, so with — `scripts/preflight/preflight.sh`, `scripts/run-shell-suites.sh`
- KS-954 (P3) KS-858 residue: the repeated-slash collapse does not complete for the /api/billi — `services/api-gateway/src/routes/proxy.ts`, `services/api-gateway/src/middleware/normalisePath.ts`
- KS-1082 (P4) The Playwright env guard added in #896 reads config/ only — the variable breakin — `systemTest/fixtures/provision-actors.ts`, `systemTest/playwright/global-setup.ts`
- KS-1153 (P4) L7 gate records (#918/#924/#925): run-code-guards.sh --check-unreached advisory  — `.githooks/pre-push`, `scripts/run-code-guards.sh`, `scripts/preflight/preflight.sh`
- KS-1083 (P0) GATEWAY_VOUCH_SECRET: nothing provisions it and no deploy order or rotation is w — `services/api-gateway/src/routes/verification.ts`, `packages/shared/src/db/tenant-context.ts`, `scripts/bootstrap-env.sh`

## HELD (READY_* or done.md PASS) — 52
- KS-1011 KS-666 stack marker reads "unknown" for owner/branch/commit/started_at whenever 
- KS-1018 Security/correctness: three verification-store reads swallow EVERY DB error with
- KS-1028 KS-754 gate F-1 (MAJOR): a step-12 throw skips the USER_ERASED fan-out AFTER the
- KS-1035 The merge gate cannot see a WITHDRAWN approval — #813 reads approved+clean again
- KS-1037 The NO-FORCE-PUSH rule exists only in .githooks/pre-push and in no .md — documen
- KS-1045 KINTSUGI-DEV-SERVER-PLAN.md still says the VM "has NOT been created" — Stage B r
- KS-1047 pre-push:230 names the stack-dependent legs as (3, 4, 7); measured they are 3, 4
- KS-1049 A PR's Test Evidence must state whether the preflight RAN — the hook skips syste
- KS-1050 users.ts:933 answers success: true over a 0-row profile update — KS-943 changes 
- KS-1072 The latest-anchor selector documents a `confirmedAt` tiebreak it does not implem
- KS-1073 Tier-2 verify has no statusless-blob cell — the carve-out is unguarded on the ti
- KS-1074 The poller/reconcile blob writers also erase threadToken — on the CONFIRM/heal p
- KS-1087 workflow-approve deletes the pending document and answers 200 "Document has been
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
- KS-1130 ks1069: tier-2 twin cells for E1/E7/E3 + the falsified comments (:323, :244, :61
- KS-1133 verify-hash precedence: v1 hash-LAST, v2 hash-FIRST — document the split on both
- KS-1139 Bare arithmetic-command `((X++))` under `set -e` — exits 1 at 0 and bash ≥ 4.1 e
- KS-1158 L3a gate records (#912 r2 / #937): the placeholder-hash anchoredAt carry keys on
- KS-1160 originate POST /api/webhooks persists the RAW url where PATCH persists the norma
- KS-1164 gate/report.ts writeGateReport overwrites the input summary when --summary does 
- KS-1165 api-gateway CSRF excludedPaths carries no /api/v2/verification entry — the v2 ve
- KS-1171 Guard 3's re-poll reads a MIXED window as ABSENT — one early "not found" then an
- KS-1172 Add `note` and `verified` to the lifecycle vocabulary (LIFECYCLE_VERBS + LIFECYC
- KS-629 kyc `livenessVideo` is accepted by spec and runtime, then silently discarded — n
- KS-745 api-gateway audit export calls /api/audit/logs — a route the security service do
- KS-747 Spec drift: GET /api/security/keys declares no parameters while the handler requ
- KS-794 verify-file returns `fileSize` on every 200 and neither response schema declares
- KS-844 demo-service mounts no error handler — a raw 0x00 body returns express's default
- KS-864 Dead-estate pointers in RUNTIME SOURCE outside deployment/azure — system-status.
- KS-865 check-no-latest-tags.sh silently skips a missing input — it scans 5 of the 6 fil
- KS-871 The audit log records `req.path` AFTER the response, so a REFUSED erasure is log
- KS-884 pre-push resolves the bare name `develop`, so a TAG named develop beats the bran
- KS-887 KS-869 test defect (mine): the WRITE-half column-list pin can be satisfied by th
- KS-888 dbSaveApiKey SWALLOWS a failed INSERT — POST /api/keys answers 201 for a key tha
- KS-908 connectorId persists but is invisible through the API — POST and GET both return
- KS-932 timeoutMs does not bound DNS resolution — a hung lookup leaves safeOutboundReque
- KS-958 The re-link guard matches the JS runtime name case-sensitively — every UPPERCASE
- KS-972 start-secuura.sh banner prints admin@secuura.com / admin123, which has returned 
- KS-974 Published bound vs runtime bound on rate-limit scope: /check enforces code UNITS
- KS-975 rateLimitScope tri-state: a MALFORMED `sub` silently became a 403 on the ungated
- KS-976 Rate-limit refusals name the wrong field: 400 says "Key required" when the key w
- KS-999 getUserById's decrypt path escapes the KS-253 classifier — `return await fromRow

## SET ASIDE with a recorded reason — 28 (re-read only if the ticket's updatedAt moved)
- KS-1034 — its fix flips run_code_guards.test.sh CASE 8 — two files (script + test) → a Claude seat (updated 2026-09-11)
- KS-1063 — decision-class: its own words say the design question comes first (updated 2026-09-09)
- KS-1076 — likely already fixed at M55 (docblock present since ec61abf8e/0882f7661) — measure with eslint in a tool-mode clone; item 2 is a Claude seat's (updated 2026-09-13)
- KS-1088 — decision-class: 'filing only; decide whether the runner should enforce isolation' — a ruling, not a patch (updated 2026-09-11)
- KS-1111 — a masking guard with an unruled fix-shape (a)/(b), security-adjacent (updated 2026-09-12)
- KS-1112 — two files: option 1 reds ks1029's A1 cell (2026-09-15 18:45) (updated 2026-09-13)
- KS-1113 — an e2e spec under tests/e2e — no Playwright checker yet (updated 2026-09-13)
- KS-1114 — decision-class (spec vs implementation of a title strategy) (updated 2026-09-13)
- KS-1119 — multi-tenant security surface (updated 2026-09-13)
- KS-1128 — the seed's pg is a require inside the function (updated 2026-09-13)
- KS-1129 — three services, anchoring index.ts listens on import (updated 2026-09-13)
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

## EXCLUDED by predicate — 180
<!-- REJECTION TABLE (EXCLUDED "names no product file" pool + SET ASIDE re-read), measured 2026-09-16 21:0x–21:31 by the 21:20 search commission — do NOT re-derive these.
     FITS from that search, all DOCS tier (insert-only), queued 21:31: KS-987 (item 1, DEPLOYMENT-ARCHITECTURE.md after :73), KS-890 (same file after :96), KS-1036 (item 3, DEV-PROCESS.md after :227).
     No vitest TAMPER-tier fit exists in this pool: every coverage-only ticket in it pins a file in seat A's partition (packages/shared, api-gateway, auth), a jest/python/e2e suite, or a test file as the subject.
     KS-811   coverage ask spans originate (jest) + api-gateway/src/services/enforcement.ts (seat A) + the social-callback 403s (OAuth surface)
     KS-812   connectors/whatsapp-bot has no test runner at tip (package.json scripts: build/start/dev only; no node_modules) — no tier grades it; fix shape is a two-way choice
     KS-1110  fix edits TWO existing test files (systemTest/performance sheddingCeiling.test.ts:29, package_scripts.test.ts:21) + adds a guard; no product line to tamper
     KS-1115  fix is a new SQL migration (CHECK on anchor_store.status) gated on a live-row census per environment — not gradeable by any tier
     KS-934   three alternative fix shapes (LIMIT/paging, aggregate deadline, move off the request path) — decision-class
     KS-896   the subject IS a test file (scripts/__tests__/pre_push_hook_base.test.sh CONTROL) — KS-897 class
     KS-1140  packages/shared/src/__tests__/ks879-… — raise seat A partition
     KS-1147  packages/shared/src/__tests__/ks860-… — raise seat A partition
     KS-1137  both items edit an existing .test.sh; F-4's red needs a host with no /usr/bin/jq — measured /usr/bin/jq present on this host, so no red is producible
     KS-1134  subject is orchestrate_jobs.test.sh (tamper lives in Blockchain/Testing/ci/orchestrate.sh:119) — KS-897 class
     KS-1048  the rule text is only in the project-root CLAUDE.md outside the repo (git grep "rebuild local so it stays current" 48e65c435 → 0; project CLAUDE.md:176 → 1); ticket requires both copies
     KS-1106  frontend verifier UX — no frontend/Playwright checker
     KS-1131  services/auth test cells — auth surface + seat A partition
     KS-902   premise contested at tip: action-pins-labelled.sh:55 / bare-path-scripts-executable.sh:56 `cd "$(dirname "$0")/../.."` BEFORE `REPO_ROOT="$(cd ../.. && pwd)"`, so the root IS script-derived; the remaining difference (unchecked cd) needs a wording ruling
     KS-1010  Playwright e2e + the ticket's own "OPEN QUESTION — do not change any route until this is answered"
     KS-1039  Playwright e2e (auth-exhaustive.spec.ts registration) — no checker; auth surface
     KS-982   not on develop — the suite exists only on the frozen #892 branch (the ticket's own ls-tree scope note)
     KS-1030  needs a real Postgres + a test:migrations redesign
     KS-990   item 2 already FIXED at tip (PUBLIC_BY_DESIGN_TEMPLATE_IDS gone; PublicByDesignTemplateId is a non-exported type at endpointFalsePositives.ts:80); item 1 blocked on KS-994
     KS-957   three findings the ticket says are ONE pass over check-shared-relink.sh + its suite (KS-958's file): red-proof cells + a dead clause + prose figures
     KS-784   cause NOT diagnosed ("Why it fails" not established) + a design requirement in Peter's comment
     KS-1085  Launch_Claude.command — outside the repo
     KS-939   launcher boot prompt — outside the repo
     KS-940   launcher suite — outside the repo
     KS-655   launcher drift check — outside the repo
     KS-1136  two design-level items across Blockchain/Testing/jobs 04 + 09 ("the owner's call")
     KS-738   python (schemathesis run.py) — no python tier; a fix-options list
     KS-752   python (schemathesis run.py control flow) — no python tier
     KS-595   a platform-semantics question ("are the defects still live?"), python catalogue
     KS-699   schema-wide FK design (52 columns) — decision + migrations
     KS-562   npm install-layout duplicate-instance — environment, not a patch
     KS-1014  ops recommendation with two alternative shapes — design
     KS-965   87 sites / 55 files — not one file
     KS-986   credential docs + demo seeding env decision
     KS-955   env/bootstrap chain across .env.example + compose + lockout — multi-file, seeding-credential surface
     KS-1054  api-gateway startup-migrations ordering — seat A partition; needs real Postgres
     KS-1023  "Filed rather than fixed, deliberately" — schema-authority question across three files
     KS-1079  demo env flag, "a one-line decision with no owner"
     KS-956   the gate's fix shape was withdrawn by measurement; decision on numbers
     KS-761   akto design decision (staleness detection)
     KS-851   four residues across init.sql / docker init / kyc — multi-file; fix shapes optional
     KS-947   api-gateway limiter mounts + spec binding — seat A partition
     KS-766   refactor of the inline single-quoted python block at base-image-watch.sh:795-831 (QA F-14 apostrophe hazard) into a callable + in-script self-test cases; no __tests__ reference for the script
     KS-1143  packages/shared ks781 guard — seat A partition
     KS-1144  packages/shared ks781 guard — seat A partition
     KS-765   a new committed merge-helper feature (four requirements) on the merge gate
     KS-1138  .github/workflows comment + an ubuntu-only CI red — workflows excluded; red not reproducible on macOS
     KS-607   an investigation with a semantics ruling in its comments; no fix shape
     KS-598   decision (re-key vs remove the upsert) in originate routes/verification.ts (jest)
     set-aside re-read (reason looked stale): KS-849 fix shape "not chosen … wants its own gate" (concurrency); KS-1142 packages/shared tests (seat A); KS-1128 api-gateway startup-migrations (seat A) + real PostgreSQL. All 28 SET ASIDE rows: updatedAt unchanged since recorded (Linear 21:2x).
     title-level only (ops/decision/feature/security/frontend/systemTest/seat-A, not read in full): KS-263 KS-305 KS-339 KS-528 KS-530 KS-582 KS-583 KS-591 KS-602 KS-603 KS-604 KS-605 KS-636 KS-638 KS-648 KS-651 KS-678 KS-696 KS-709 KS-716 KS-723 KS-725 KS-735 KS-748 KS-758 KS-760 KS-767 KS-768 KS-769 KS-770 KS-772 KS-783 KS-785 KS-829 KS-837 KS-838 KS-846 KS-872 KS-903 KS-919 KS-959 KS-995 KS-996 KS-997 KS-1012 KS-1022 KS-1025 KS-1044 KS-1080 KS-1090 KS-1100 KS-1102 KS-1104 KS-1116 KS-1141 KS-1154 KS-1155 KS-1161
-->
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
- KS-1036 — names no product file (after basename/docs/route resolution)
- KS-1038 — auth-shaped title (LAST, Kam 16:40)
- KS-1039 — names no product file (after basename/docs/route resolution)
- KS-1040 — auth-shaped title (LAST, Kam 16:40)
- KS-1042 — on Peter/Stuart
- KS-1044 — names no product file (after basename/docs/route resolution)
- KS-1048 — names no product file (after basename/docs/route resolution)
- KS-1053 — auth-shaped title (LAST, Kam 16:40)
- KS-1054 — names no product file (after basename/docs/route resolution)
- KS-1079 — names no product file (after basename/docs/route resolution)
- KS-1080 — names no product file (after basename/docs/route resolution)
- KS-1085 — names no product file (after basename/docs/route resolution)
- KS-1090 — names no product file (after basename/docs/route resolution)
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
- KS-1134 — names no product file (after basename/docs/route resolution)
- KS-1136 — names no product file (after basename/docs/route resolution)
- KS-1137 — names no product file (after basename/docs/route resolution)
- KS-1138 — names no product file (after basename/docs/route resolution)
- KS-1140 — names no product file (after basename/docs/route resolution)
- KS-1141 — names no product file (after basename/docs/route resolution)
- KS-1143 — names no product file (after basename/docs/route resolution)
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
- KS-607 — names no product file (after basename/docs/route resolution)
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
- KS-678 — names no product file (after basename/docs/route resolution)
- KS-696 — names no product file (after basename/docs/route resolution)
- KS-699 — names no product file (after basename/docs/route resolution)
- KS-709 — names no product file (after basename/docs/route resolution)
- KS-716 — names no product file (after basename/docs/route resolution)
- KS-723 — names no product file (after basename/docs/route resolution)
- KS-724 — auth-shaped title (LAST, Kam 16:40)
- KS-725 — names no product file (after basename/docs/route resolution)
- KS-735 — names no product file (after basename/docs/route resolution)
- KS-738 — names no product file (after basename/docs/route resolution)
- KS-744 — auth-shaped title (LAST, Kam 16:40)
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
- KS-769 — names no product file (after basename/docs/route resolution)
- KS-770 — names no product file (after basename/docs/route resolution)
- KS-772 — names no product file (after basename/docs/route resolution)
- KS-782 — auth-shaped title (LAST, Kam 16:40)
- KS-783 — names no product file (after basename/docs/route resolution)
- KS-784 — names no product file (after basename/docs/route resolution)
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
- KS-837 — names no product file (after basename/docs/route resolution)
- KS-838 — names no product file (after basename/docs/route resolution)
- KS-840 — auth-shaped title (LAST, Kam 16:40)
- KS-846 — names no product file (after basename/docs/route resolution)
- KS-851 — names no product file (after basename/docs/route resolution)
- KS-855 — auth-shaped title (LAST, Kam 16:40)
- KS-872 — names no product file (after basename/docs/route resolution)
- KS-890 — names no product file (after basename/docs/route resolution)
- KS-896 — names no product file (after basename/docs/route resolution)
- KS-902 — names no product file (after basename/docs/route resolution)
- KS-903 — names no product file (after basename/docs/route resolution)
- KS-918 — auth-shaped title (LAST, Kam 16:40)
- KS-919 — names no product file (after basename/docs/route resolution)
- KS-925 — auth-shaped title (LAST, Kam 16:40)
- KS-928 — has a PR attached
- KS-934 — names no product file (after basename/docs/route resolution)
- KS-938 — auth-shaped title (LAST, Kam 16:40)
- KS-939 — names no product file (after basename/docs/route resolution)
- KS-940 — names no product file (after basename/docs/route resolution)
- KS-944 — auth-shaped title (LAST, Kam 16:40)
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

