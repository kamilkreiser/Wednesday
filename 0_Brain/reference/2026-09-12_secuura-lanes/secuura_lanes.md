# Secuura/Blockchain: parallel agent lanes (read-only research for Wednesday)

Generated 2026-09-12 04:15Z. Instruments: Linear GraphQL (team KS, state.type in backlog/unstarted/started, first:100 + cursor), GitHub REST (Secuura/Distributed_Secuura pulls, per_page=100), `git -C 2_Project_Files grep/show/log/ls-tree` at `4554b25e2`, `git ls-remote origin`. Nothing was edited, fetched or checked out.

- develop tip: `git ls-remote origin refs/heads/develop` → `4554b25e21dfd01113bf40e8f6d34573345a5f37` (KS-1094 #958) — matches the expected 4554b25e2; object present locally.

- Linear paged: **4 pages, 379 issues**, archived among them: 0.
- GitHub open PRs on base develop: **48** (1 page) — kksecura 37, dependabot 10, PeterObeden 1. Open PRs on any other base: 0.

## 1. Totals

| state | count |
|---|---|
| Backlog | 259 |
| In Progress | 42 |
| In Review | 38 |
| Todo | 35 |
| Blocked | 5 |

| priority | count |
|---|---|
| Urgent | 7 |
| High | 147 |
| Medium | 189 |
| Low | 31 |
| No priority | 5 |

| class | count |
|---|---|
| A — agent-actionable now | 94 |
| B — needs Peter, Stuart or Kam | 162 |
| C — blocked / parked / not yet possible / claimed | 54 |
| D — open kksecura PR names it | 69 |

Of the A tickets, 26 are marked HOLD: agent-actionable, but their files are in an open PR or an in-flight ticket, so they cannot run in parallel now.

## 5. Proposed lanes (three, file-disjoint, priority-ordered)

**Rules shared by all three lanes.**
- Branch from origin/develop `4554b25e2`, each in its own worktree.
- Do not regenerate or edit `Blockchain/Dev/docs/openapi/secuura-api.yaml`: open PRs #922, #919, #813 and #805 all change it.
- Do not touch any `package.json` / `package-lock.json`: dependabot #945–#949, #572, #575, #635, #639, #649 and kksecura #937 change lockfiles.
- Do not touch these paths:
  - `systemTest/performance/`: PR #960 and Wednesday's KS-1098 lane.
  - `Start_Up/`, `Blockchain/Dev/scripts/check-stack-safety.sh`, `Blockchain/Dev/CONTRIBUTING.md`: Peter's draft #959.
  - `.github/workflows/`: Kam merges those.
- None of the three lanes touches `systemTest/performance/runner/`.
- `git ls-remote --heads origin` shows 340 heads and no branch for any lane or reserve ticket.

### Lane 1 — originate route input guards: KS-1029 (P2 High) then KS-1103 (P3 Medium)
- **Size:** two small fixes, each with a regression cell.
- **Yours:**
  - `Blockchain/Dev/services/originate/src/routes/gdpr.ts`: PATCH `/dsr/:dsrId` at :348 only; `UUID_PATTERN` is already defined at :39.
  - `Blockchain/Dev/services/originate/src/routes/verification.ts`: the `/verify` validator + handler, :699-734 only.
  - New files `Blockchain/Dev/services/originate/src/__tests__/ks1029-*.test.ts` and `ks1103-*.test.ts`.
- **NOT yours:**
  - originate `routes/documents.ts`, `repositories/documentRepo.ts` (#939, #919).
  - `services/anchorStateSync.ts` (#912).
  - `middleware/auth.ts`, `routes/adminConfig.ts` (#799).
  - `originate.openapi.ts` (#919, #813).
  - Every existing test file changed by #931/#926/#937/#720: `gdprService.erasure.test.ts`, `helpers/sharedModuleMock.ts`, `ks444-webhooks-create-description-guard.test.ts`, `ks445-pg-error-classification.test.ts`, `ks563-*`, `ks584-*`, `ks695-*`, `ks914-*`, `qa-f4-*`, `ks1059-*`.
  - The 15 `err.message` sites in gdpr.ts (KS-730).
  - The spec.
- **Choices the tickets already make:**
  - KS-1029: reuse `UUID_PATTERN` and answer like the KS-431 sibling (ticket: "400/404, never 500").
  - KS-1103: take "read `hash` in the handler", not "drop it from the spec".
  - If either needs a new documented status code in the spec, stop and send Wednesday a QUESTION.
- **Suite that proves it:**
  - Targeted run: `cd Blockchain/Dev/services/originate && npx jest src/__tests__/ks1029-… src/__tests__/ks1103-… src/__tests__/ks444-gdpr-dsr-update-withdraw-guards.test.ts src/__tests__/ks431-gdpr-export-id-guard.test.ts`.
  - Then full `npm test` (jest) against the develop baseline. The known pre-existing reds are the ks444-webhooks pair, which open #926 fixes; report the failing SET.
  - Tamper control: remove each guard and the new cell must red.
  - On a named local slot: the Schemathesis `pr` finding `not_a_server_error::PATCH /api/gdpr/dsr/{dsrId}` (Peter, 2026-09-11) is gone, and a `hash`-only verify body gets the same verdict as `contentHash`.
- **Overlap risk:**
  - KS-730 (A, held) edits 15 sites in the same gdpr.ts: never run it concurrently.
  - #931 rebuilds originate's `@secuura/shared` jest mocks from the real export list. New cells that mock `@secuura/shared` must use a complete factory, or wait for #931.
  - The gateway's `routes/verification.ts` (Lane 3) is a different file with the same name.

### Lane 2 — vc-issuer presentation lookup: KS-1020 (P2 High), recommendation item 1 only
- **Size:** one small-to-medium fix, plus the sibling sweep the ticket leaves open ("Whether sibling routes in vc-issuer share the fallback — not swept").
- **Yours:**
  - `Blockchain/Dev/services/vc-issuer/src/routes/presentations.ts`, `getPresentation` (:110-133): the `LIKE $1` + `%id%` fallback at :117-122 and the `includes()` scan at :129-131.
  - A new `Blockchain/Dev/services/vc-issuer/src/__tests__/ks1020-*.test.ts`.
  - A read-only sweep of the other `vc-issuer/src/routes/*.ts`. Report siblings as findings; fix one only if the identical exact-or-404 change applies.
- **NOT yours:**
  - Recommendation item 2, the ownership/tenant check. It needs an ownership model, and every stored row has `holder_id NULL`. Send it to Wednesday as a QUESTION.
  - The `/presentations/verify` logic (KS-625, Kam's ruling).
  - `routes/status.ts` (KS-692, B).
  - `vc-issuer.openapi.ts` and the spec.
  - api-gateway `routes/proxy.ts` / `__tests__/ks570-proxy-mount-auth.test.ts` (#923).
  - Any probe of demo or kintsugi: the ticket says deployed reachability "is being taken separately".
- **Suite that proves it:**
  - `cd Blockchain/Dev/services/vc-issuer && npx vitest run` (full suite). Existing presentation-touching tests: `credentialsVerify.fuzz.test.ts`, `db.retry.test.ts`, `ks444.requestSchema.test.ts`.
  - New cells: ids `0`, `abc`, `..`, `1`, `a`, `e` → 404 with a real row stored; the exact id → 200 (positive control).
  - Tamper control: restore the LIKE and the cells must red.
  - Local slot: `GET /api/presentations/0` → 404.
- **Overlap risk:**
  - No open PR touches `services/vc-issuer/`.
  - Behaviour change: a partial-id caller now gets 404. The ticket says no legitimate caller does that; state it in the Test Evidence.

### Lane 3 — api-gateway verify tier consistency: KS-1071 (P3) → KS-1070 (P3) → KS-1069 (P3); overflow KS-1072 (P4), KS-1073 (P4)
- **Size:** one medium fix — one shared status→confidence mapping used by both tiers, plus `simulated` carried into tier 2.
  - Add KS-1069 only if the session has room; re-derive the gate's F3/F4 first, because the ticket says they were relayed, not re-derived.
  - KS-1072 and KS-1073 are one cell each.
- **Yours:**
  - `Blockchain/Dev/services/api-gateway/src/routes/verification.ts`: tier-2 blob :240-283 and tier-1 predicate :570-610 only.
  - `Blockchain/Dev/services/api-gateway/src/__tests__/ks1057-verify-confidence-is-status-aware.test.ts`.
  - New `ks1069-*`, `ks1070-*`, `ks1071-*` test files in the same folder.
- **NOT yours:**
  - Other regions of `verification.ts`:
    - the workflow-instances handlers :767-960 (KS-1087, B, awaiting a ruling);
    - `/api/certifications/:id/verify` :556 (KS-834 decision);
    - the trust-header reads :1041-1042 (KS-1032, cited in #918).
  - `middleware/contentType.ts` + `__tests__/contentType.test.ts` (#813).
  - `startup-migrations.ts` (#928, #932).
  - `__tests__/ks570-proxy-mount-auth.test.ts` (#923).
  - `routes/platform.ts` (#880).
  - `services/health.ts`, `routes/system-status.ts` (reserve R4).
  - Any migration: KS-1071's optional CHECK constraint stays out; ask.
- **Suite that proves it:**
  - `cd Blockchain/Dev/services/api-gateway && npx vitest run src/__tests__/ks1057-verify-confidence-is-status-aware.test.ts src/__tests__/ks815-verification-router-guards-its-own-body.test.ts`, then the full `npx vitest run`.
  - KS-1071: a cell per tier for `pending`, `submitted` and an out-of-union status.
  - KS-1070: a tier-2 confirmed+simulated row reports off-chain-only.
  - A tamper control for each.
- **Overlap risk:**
  - Same file as KS-1087 and KS-1032, neither of which is in flight.
  - #935 (KS-1057) is merged (GitHub API, 2026-09-10), so the predicate is develop's.
  - No contact with `systemTest/performance/runner/`.

### Reserve lanes (file-disjoint from lanes 1-3 and from each other)
- **R1 frontend portals:**
  - Tickets: KS-1104 (P3, `frontend/verifier/src/components/VerifyPage.tsx:267-289`), KS-1105 (P3, `frontend/admin/src/pages/Login.tsx:81`), KS-1106 (P4, `frontend/verifier/src/components/ResultPage.tsx`).
  - Proof: verifier/admin have no unit-test script (lint only). Use `npm run lint`, a build, and an accessibility-tree check at 390×844 on a local slot.
  - Keep out of frontend package.json/lockfiles (dependabot #948 vite, #946 fluentui, #639 radix, #945 axe-core).
- **R2 CI harness scripts:**
  - Tickets, all P3: KS-922 (`Blockchain/Testing/ci/orchestrate.sh:91`), KS-878 (`Blockchain/Testing/jobs/09-aggregate-report.sh`), KS-867 (`Blockchain/Testing/jobs/04-container-trivy.sh`), KS-941 (`Blockchain/Dev/scripts/__tests__/orchestrate_jobs.test.sh:47`), KS-877 (`Blockchain/Dev/scripts/docker-build.sh:162`).
  - Proof: `bash Blockchain/Dev/scripts/__tests__/orchestrate_jobs.test.sh` under macOS /bin/bash 3.2, with red-first cells.
  - NOT yours: `scripts/preflight/*`, `scripts/run-code-guards.sh` (#918/#925/#903/#924); `scripts/check-shared-relink.sh` (#879); `check-stack-safety.sh` (#959).
- **R3 akto config:**
  - Tickets: KS-1108 (P3, `systemTest/akto/src/config/secrets.ts:40`), KS-755 (P3, `systemTest/akto/src/core/runDir.ts` + `tests/unit/core/runDir.test.ts`).
  - Proof: `npm run test:unit` in systemTest/akto.
  - No open PR touches systemTest/akto. Not `systemTest/performance/`.
- **R4 gateway health/status:**
  - Tickets: KS-1101 (P3, `api-gateway/src/services/health.ts`), KS-864 (P3, `api-gateway/src/routes/system-status.ts`).
  - Same service as Lane 3 but different files. KS-1102 (B) stays out.
- **R5 kyc:**
  - Tickets: KS-849 (P3, `services/kyc/src/index.ts` mock-flow timer), KS-848 (P3, `services/kyc/tsconfig.json`).
  - No open PR touches kyc.
- **Non-code, P1 — KS-1076:** verification only (see its row).
  - Needs a local stack slot and should edit no files, so it can run beside any lane that is not using the same slot.
  - If lint is still red at the tip, the fix stays inside `systemTest/playwright/global-setup.ts`.

### Tickets that would touch `systemTest/performance/runner/` (flag)
- **KS-1098** — Wednesday's lane (`runner/k6_docker.ts`); excluded here.
- **KS-1099 (D)** — open PR #960 (`runner/config_loader.ts`).
- **KS-704 (A, held)** — `runner/run_validity.ts` + `gate/report.ts` (git grep http_req_failed).
- **KS-990 (C)** — `runner/actor_manifest.ts:140` TS2540; that file is changed by open PR #916.
- **KS-994 (C) / KS-1026 (D, #916)** — `runner/cli.ts`, `runner/actor_manifest.ts` (git grep withGeneratedActors).

### Overlap with Peter's KS-1096 branch (#959)
#959 changes `Start_Up/start-secuura.sh`, `Blockchain/Dev/scripts/check-stack-safety.sh`, `Blockchain/Dev/CONTRIBUTING.md` and `scripts/__tests__/start_secuura_slot_names.test.sh`. Tickets that overlap it:
- **KS-972 (B)** — the start-secuura.sh banner; named in the #959 body.
- **KS-1011 (C)** — stack labels.
- **KS-1034 (D via #918 body)** — `check-stack-safety.sh:34`.
- **KS-1093 (C)** — `check-stack-safety.sh` §6f.
- **KS-1037 (A, held)** and **KS-789 (B)** — CONTRIBUTING.md.

### `.github/workflows/` — Kam merges
- **KS-1076** — item 3 (`pr-platform-suites.yml`).
- **KS-636 (B)** — `base-image-refresh.yml`.
- **KS-412 / KS-418** — Peter's.
- **Open PRs** — #940/#941 (`security-scan.yml`), #942 (`pr-security-gates.yml`), #887 (`pr-platform-suites.yml`).
- **KS-1012 (B)** — a ruleset: settings, not a file.

## 2-4. Classification

### A — agent-actionable now (directory family + files from git grep at 4554b25e2 where a symbol/file was named)

| id | P | state | assignee | title | family / files | why A (HOLD = files in an open PR or in-flight ticket) |
|---|---|---|---|---|---|---|
| KS-1076 | Urgent | Todo | — | No Playwright e2e test has run on any PR since 2026-09-07 — the suite dies at a static lint gate before any br | systemTest/playwright/ (no edit expected); .github/workflows/pr-platform-suites.yml is Kam's | Verification-only now. At 4554b25e2 `systemTest/playwright/global-setup.ts` already carries the @param/@throws/@example docblocks the ticket's 4 jsdoc errors named (commit 6a047445b, reached develop in the #896 merge 38a919d40 on 2026-09-11, after the ticket's 2026-09-10 measurement). Remaining agent work = item 2: confirm `npm run lint` is green, run the suite on a named slot, report findings. Item 3 (lint step placement in `pr-platform-suites.yml`) is a workflow change for Kam. |
| KS-730 | High | Backlog | kamil | Security: 71 inline handlers still return err.message verbatim off-production — KS-727's enumerated remainder  | api-gateway/src/index.ts (2), originate/src/routes/{adminConfig,gdpr,systemErrors}.ts, tokenisation/src/index.ts | Mechanical, 'do api-gateway first'; helper-vs-ternary is left to the implementer. HOLD: 15 of the 71 sites are in originate/src/routes/gdpr.ts (Lane 1's file). git grep of `details: { details: err.message }` also hits api-gateway/src/routes/admin.ts, which the ticket's table does not list. |
| KS-810 | High | Backlog | kamil | auth.openapi.ts cannot be imported by any test — passwordLoginGate imports z from zod directly, so a module-sc | Blockchain/Dev/services/auth/src/services/passwordLoginGate.ts, auth.openapi.ts | Recommendation named: import z from @secuura/shared at passwordLoginGate.ts:55, with care for the prototype change. HOLD: passwordLoginGate.ts is in open PR #930. |
| KS-823 | High | Todo | kamil | Security: the /api/oauth/token `refresh_token` grant authenticates NO client — a confidential app's refresh to | Blockchain/Dev/services/auth/src/routes/oauth.ts | Wednesday discharged the 'file-only' ruling 2026-09-08 ('a defect to fix'); fix shape given. HOLD: token endpoint sits in routes/oauth.ts, which open PR #881 edits. |
| KS-932 | High | Backlog | kamil | timeoutMs does not bound DNS resolution — a hung lookup leaves safeOutboundRequest pending well past its decla | Blockchain/Dev/packages/shared/src/security/ssrf-guard.ts | Fix shape given (arm the deadline before DNS resolution). HOLD: ssrf-guard.ts is in open PR #873. |
| KS-938 | High | Backlog | kamil | Security: "MFA disabled" leaves the TOTP seed and hashed backup codes in the row — updateUser skips every `und | Blockchain/Dev/services/auth/src/routes/{users,mfa}.ts, repositories/userRepo.ts | Fix shape given (send null; add mfaBackupCodes at users.ts:1081). HOLD: userRepo.ts/users.ts/mfa.ts are in open PRs #930/#913. |
| KS-947 | High | Backlog | kamil | KS-733 gate blindness (F3+F4): the parity cell misses skip:() and mount ORDER, and is purely relative so both  | Blockchain/Dev/services/api-gateway/src/__tests__/ks733-users-mfa-rate-limit-mount.test.ts, api-gateway/src/index.ts, spec | Fix shapes given for F3/F4. HOLD on the spec half: docs/openapi/secuura-api.yaml is in open PRs #922/#919/#813/#805. |
| KS-958 | High | Backlog | — | The re-link guard matches the JS runtime name case-sensitively — every UPPERCASE spelling is exempt, and ENV N | Blockchain/Dev/scripts/check-shared-relink.sh, scripts/__tests__/check_shared_relink.test.sh | Case-insensitive runtime-name match, measured with a control. HOLD: check-shared-relink.sh + suite are in open PR #879; KS-930/KS-937 (same guard) in flight. |
| KS-974 | High | Backlog | — | Published bound vs runtime bound on rate-limit scope: /check enforces code UNITS against a published code-POIN | Blockchain/Dev/services/security/src/requestSchemas.ts | Make the runtime count what the spec publishes. HOLD: security/src/requestSchemas.ts scopeField (:60-88) and possibly the spec (4 open PRs); KS-698 (In Progress) is on the same /check route. |
| KS-998 | High | Backlog | kamil | KS-989 gate residue: the formatting gate fails OPEN on missing deps and reads the WORKING TREE, not the push — | .githooks/pre-push, Blockchain/Dev/scripts/ (format gate) | Four items with concrete shapes (e.g. `< /dev/null` at :150; read the pushed tree). HOLD: .githooks/pre-push is in open PR #903. |
| KS-999 | High | Backlog | kamil | getUserById's decrypt path escapes the KS-253 classifier — `return await fromRow(...)`, and the characterisati | Blockchain/Dev/services/auth/src/repositories/userRepo.ts, __tests__/ks949-platform-admin-seed-identity.test.ts | One word (`return await fromRow`) + pinning cell + fix the characterisation cell. HOLD: userRepo.ts is in open PRs #913/#930; ticket calls it a normal-path behaviour change, so tier-1 gate it. |
| KS-1000 | High | Backlog | kamil | services/auth tsconfig EXCLUDES src/__tests__ — every 'tsc: 0 errors' on a test-only change in this service is | Blockchain/Dev/services/auth/tsconfig.json (+ scripts) | Technical shape choice only (tsconfig.test.json vs a written exclusion) + sibling sweep; no ruling named. HOLD: adding src/__tests__ to tsc may surface errors in auth test files that open PRs #930/#881/#913 edit. |
| KS-1005 | High | Backlog | — | Security/defect: POST /api/users/me/change-password returns 404 for EVERY user — USER_COLS omits password_hash | Blockchain/Dev/services/auth/src/routes/users.ts, repositories/userRepo.ts | 'The fix already exists': select password_hash for change-password instead of USER_COLS. HOLD: routes/users.ts is in open PR #930. |
| KS-1020 | High | Backlog | — | Security: GET /api/presentations/{id} returns a real stored presentation for an id that names nothing — LIKE ' | Blockchain/Dev/services/vc-issuer/src/routes/presentations.ts:110-133 (git grep: `LIKE $1` at :119) | Recommendation 1 is fully specified: delete the LIKE '%id%' fallback and the in-memory includes() scan (exact id or 404). Item 2 (ownership/tenant check) needs an ownership model and every stored row has holder_id NULL; split it out as a question, do not build it. |
| KS-1029 | High | Backlog | — | KS-754 gate F-2 (MAJOR): PATCH /api/gdpr/dsr/{dsrId} regresses a malformed id from 200 to 500 — UUID_PATTERN e | Blockchain/Dev/services/originate/src/routes/gdpr.ts (git grep UUID_PATTERN: gdpr.ts, webhooks.ts, utils/principalId.ts) | One-line fix named: apply gdpr.ts:39 UUID_PATTERN on PATCH /dsr/:dsrId (:348) so a malformed id answers 404/400, never 500; precedent at :201/:296 (KS-431). Peter reproduced it 2026-09-10/11 in comments (confirmation, not a request). |
| KS-528 | Medium | Backlog | kamil | Frontends: react-router v6 → v7 migration (3 moderate client-runtime advisories — open redirect/XSS, construct | Blockchain/Dev/frontend/{admin,issuer,verifier} | Mechanical but LARGE (react-router v6→v7 in three portals). Not a one-session lane; dependabot PRs touch the same package files. |
| KS-530 | Medium | Backlog | kamil | @hono/node-server v1->v2 major bump (GHSA-frvp) - originate + mcp-server runtime | Blockchain/Dev/services/{originate,mcp-server}/package*.json, scripts/audit/audit-baseline.json | 'Do:' list given (hono v2 in originate + mcp-server locks, remove the baseline row). Medium; lockfile + audit-baseline edits. |
| KS-704 | Medium | Todo | kamil | k6 gate reports a failure rate with no status-code breakdown - an author cannot tell a platform 4xx from a har | systemTest/performance/{gate,runner,helpers}/ (git grep http_req_failed) | Surface per-status-code counters already present in the k6 summary. FLAG runner/: http_req_failed handling spans systemTest/performance/runner/run_validity.ts + gate/report.ts, the same package as Wednesday's KS-1098 lane and PR #960. |
| KS-741 | Medium | Todo | kamil | x-emitter-internal is unstripped on the /originate/ route — the marker's safety rests on an unstated conventio | Blockchain/Dev/services/originate/src (inbound middleware) + test | Hold condition met (KS-1041 Step 2 merged as #951; comment 2026-09-11); three parts specified. HOLD: originate/src/middleware/auth.ts is in open PR #799. |
| KS-745 | Medium | Backlog | kamil | api-gateway audit export calls /api/audit/logs — a route the security service does not have, so the export 404 | Blockchain/Dev/services/api-gateway/src/routes/audit-export.ts:138 (git grep /api/audit/logs) | Call the list route that exists (GET /api/audit): 'likely one word'. |
| KS-747 | Medium | Backlog | kamil | Spec drift: GET /api/security/keys declares no parameters while the handler requires organizationId — the cont | Blockchain/Dev/services/security (openapi registration) + docs/openapi/secuura-api.yaml | Declare organizationId on GET /api/security/keys ('declare it, not drop it'). HOLD: spec regeneration collides with open PRs #922/#919/#813/#805. |
| KS-755 | Medium | Backlog | kamil | akto unit suite has a standing red: runDir resolveRunId ignores the injected clock | systemTest/akto/src/core/runDir.ts, tests/unit/core/runDir.test.ts (git grep resolveRunId) | Fix the injection or the test; do not delete the case. |
| KS-759 | Medium | Backlog | kamil | tenantId is read through two `as unknown as` casts because it is not on JwtPayload (Peter F14) | Blockchain/Dev/services/originate/src/middleware/auth.ts, routes/gdpr.ts | Declare tenantId on JwtPayload, remove the double casts. HOLD: originate/src/middleware/auth.ts is in open PR #799. |
| KS-766 | Medium | Backlog | kamil | base-image-watch self-test cannot red the DB-age PRODUCER — the F-5 clamp can be re-introduced with the suite  | Blockchain/Dev/scripts/base-image-watch.sh (ls-tree) | Make the self-test exercise the DB-age producer so reverting the clamp reds. |
| KS-784 | Medium | Backlog | kamil | POST /api/teams/webhook-config fails the Schemathesis pr sweep on every run — including develop — and is track | Blockchain/Dev/services/m365-integration (teams webhook-config) | Investigate and fix an unowned, stable sweep failure; no decision named, size unknown. |
| KS-805 | Medium | Backlog | kamil | POST /api/oauth/authorize deny emits `Location: undefined?error=…` for an app with zero registered redirect UR | Blockchain/Dev/services/auth/src/routes/oauth.ts | One .min(1) + deny/GET handling. HOLD: routes/oauth.ts is in open PR #881. |
| KS-824 | Medium | Backlog | kamil | OAuth app_type: a CASED row is neither normalised by 047 nor refused by its CHECK, and docker/init's unnamed c | Blockchain/Dev/migrations (new), docker/init | Fix-shape hypothesis (normalise case + CHECK); new migration. HOLD: docker/init/01-schema.sql is in open PR #905. |
| KS-825 | Medium | Backlog | kamil | Gate integrity: the auth suite's green is not deterministic — three head runs gave 534/0, 534/0, and 534 with  | Blockchain/Dev/services/auth/src/__tests__/ | Reproduce a red first, then de-flake (21 of 40 auth test files open a server per request). |
| KS-828 | Medium | Backlog | kamil | KS-800 scanner: LEG F cannot see the control-byte guard LEAVE a wrapped router — both KS-815 wrappers can drop | Blockchain/Dev/packages/shared/src/__tests__/ (KS-800 corpus instrument) | Fix-shape hypothesis given for LEG F; test-only. |
| KS-838 | Medium | Backlog | kamil | Make the authorize rules DATA the resolver iterates, so the GET/POST agreement guard is structural instead of  | Blockchain/Dev/services/auth/src/routes/oauth.ts | Refactor authorize rules into data. HOLD: routes/oauth.ts is in open PR #881. |
| KS-844 | Medium | Backlog | kamil | demo-service mounts no error handler — a raw 0x00 body returns express's default HTML with a stack trace and a | Blockchain/Dev/services/demo-service/src (git grep: no errorHandler) | Mount an error handler like every other service; the KS-727 class guard then covers it. |
| KS-848 | Medium | Backlog | kamil | services/kyc tsconfig excludes src/__tests__ — the project tsc never type-checks a single test in this service | Blockchain/Dev/services/kyc/tsconfig.json (git grep: excludes src/__tests__) | Harness ticket: type-check kyc tests (shape left to the implementer). |
| KS-849 | Medium | Backlog | kamil | KYC mock document flow: a 1.5s timer writes back a STALE verification and silently clobbers the selfie's liven | Blockchain/Dev/services/kyc/src/index.ts (git grep setTimeout) | Stale-closure race in the mock document flow (shape left to the implementer). |
| KS-855 | Medium | Backlog | kamil | The OAuth `AVAILABLE_SCOPES` list is a second, divergent scope vocabulary — derive it from SCOPES or pin it | Blockchain/Dev/services/auth/src/services/oauth.ts:57, packages/shared/src/security/scopes.ts | Derive AVAILABLE_SCOPES from SCOPES or pin it. HOLD: coordinate with KS-843 (In Progress, subjects:erase scope). |
| KS-864 | Medium | Backlog | kamil | Dead-estate pointers in RUNTIME SOURCE outside deployment/azure — system-status.ts hard-codes secuura-staging- | Blockchain/Dev/services/api-gateway/src/routes/system-status.ts (git grep ashypond-b460d1a1) | Replace dead-estate literals with config/live identity; the 2026-09-12 comment adds the :80 vs :8080 portal-probe defect. |
| KS-865 | Medium | Backlog | kamil | check-no-latest-tags.sh silently skips a missing input — it scans 5 of the 6 files it advertises and still pri | Blockchain/Dev/scripts/check-no-latest-tags.sh | A missing listed input is an error (or fix the path); report files examined. |
| KS-867 | Medium | Backlog | kamil | CVE scan image filter `^dev-[a-z-]+:latest$` excludes digits and uppercase — `dev-auth2:latest` is invisible t | Blockchain/Testing/jobs/04-container-trivy.sh (git grep) | Widen the image filter / derive the corpus; add a digit-name cell. |
| KS-870 | Medium | Backlog | kamil | Every ADMITTED erasure authenticates twice — the door's chain and the catch-all both run authenticateToken, do | Blockchain/Dev/services/api-gateway/src/routes/proxy.ts:677,:696 | Tester's fix shape: authenticate once on the erasure door. |
| KS-871 | Medium | Backlog | kamil | The audit log records `req.path` AFTER the response, so a REFUSED erasure is logged with the path trimmed to ` | Blockchain/Dev/services/api-gateway/src/middleware/audit.ts | Capture req.path at entry, not in res.on('finish'). |
| KS-872 | Medium | Backlog | kamil | packages/shared project tsc is RED on develop — crypto.JsonWebKey is gone in @types/node 26.1.0; a live type e | Blockchain/Dev/packages/shared/src/crypto/jwks.ts:129 (git grep) | Local JWK type or the new @types/node import. |
| KS-876 | Medium | Backlog | kamil | KS-860 guard walks services/ only — test listeners under packages/ are unguarded, including two in packages/sh | Blockchain/Dev/packages/shared/src/__tests__/ks860-test-listeners-bind-loopback.test.ts | Widen the KS-860 walk to packages/. |
| KS-877 | Medium | Backlog | kamil | docker-build.sh: an empty SERVICES_TABLE dies at `${BUILD_LIST[*]}` under bash 3.2 — three lines after the gua | Blockchain/Dev/scripts/docker-build.sh:162 (git grep) | Guard the display expansion under bash 3.2. |
| KS-878 | Medium | Backlog | kamil | 09-aggregate-report: a 04 artefact that exists but does not PARSE emits zero findings and rc 0 — the exact art | Blockchain/Testing/jobs/09-aggregate-report.sh (git grep _trivy_err) | Treat an unparseable 04 artefact as an error, not zero findings. |
| KS-880 | Medium | Backlog | kamil | Quarantine or reconcile the dead converters copy — a second rowToApiKey that maps neither tenantId nor connect | Blockchain/Dev/services/security/src/converters.ts:122, __tests__/row-converters.test.ts | Quarantine-by-rename the dead converters copy (or reconcile); both routes pre-approved by the done-when. |
| KS-885 | Medium | Backlog | kamil | KS-879 guard: the fifth control asserts a tautology — the escape's EVALUATION is untested, so the ks474 fixtur | Blockchain/Dev/packages/shared/src/__tests__/ks879-no-raw-control-bytes-repo-wide.test.ts | Assert the escape evaluates to U+0000. |
| KS-886 | Medium | Backlog | kamil | KS-879 guard says "repo-wide" but walks services/ + packages/ only — 749 of 1,242 files; all 148 under tests/  | Blockchain/Dev/packages/shared/src/__tests__/ks879-no-raw-control-bytes-repo-wide.test.ts:69 | Widen ROOTS (tests/ first) or narrow the name and docblock. |
| KS-887 | Medium | Backlog | kamil | KS-869 test defect (mine): the WRITE-half column-list pin can be satisfied by the COALESCE clause, so a statem | Blockchain/Dev/services/security/src/__tests__/ (KS-869 write-half pin) | Tighten the regex window to the column list. |
| KS-888 | Medium | Backlog | kamil | dbSaveApiKey SWALLOWS a failed INSERT — POST /api/keys answers 201 for a key that was never written; blast rad | Blockchain/Dev/services/security/src/index.ts:236-238 | Surface the INSERT failure instead of 201. HOLD: security/src/index.ts is in open PRs #880/#799. |
| KS-891 | Medium | Backlog | kamil | KS-873 limit: a mask desync that RE-SYNCHRONISES before EOF is still silent — the invariant closes the class o | Blockchain/Dev/packages/shared/src/__tests__/ks860-test-listeners-bind-loopback.test.ts | Correct the docblock claim or detect a re-synchronised desync. |
| KS-896 | Medium | Backlog | kamil | KS-881's CONTROL is satisfied when the branch does not exist — `upstream=NONE` cannot tell an absent branch fr | Blockchain/Dev/scripts/__tests__/pre_push_hook_base.test.sh | CONTROL must assert the branch exists. |
| KS-901 | Medium | Backlog | kamil | The census cell claims "the corpus misses nothing" — three further express-binding shapes are followed by neit | Blockchain/Dev/packages/shared/src/__tests__/ks781-p3-3-body-parser-order.test.ts | Soften the census title / declare the three unfollowed shapes. |
| KS-902 | Medium | Backlog | kamil | no-tracked-credentials.sh cites two scripts as "structurally immune" exemplars — both use a WORSE cwd-relative | Blockchain/Dev/scripts/preflight/no-tracked-credentials.sh:81-82 | Correct the exemplar comment. |
| KS-903 | Medium | Backlog | kamil | Audit the eleven cwd- and script-relative repo-root derivations under scripts/ and systemTest/ — one family, s | Blockchain/Dev/scripts/, systemTest/ | Audit and classify 11 root derivations, then fix. |
| KS-918 | Medium | Backlog | — | vite is a production dependency of services/auth — esbuild and fsevents ship into the runtime image, imported  | Blockchain/Dev/services/auth/package.json (+ lock) | Move vite to devDependencies after confirming no runtime use. Lockfile edit; dependabot #948 (vite) touches Blockchain/Dev lockfiles. |
| KS-922 | Medium | Backlog | kamil | KS-868 residue (F1): the empty-array `wait ""` at :91 logs a Stage-1 failure when ZERO jobs started — the same | Blockchain/Testing/ci/orchestrate.sh:91 (git grep stage1_pids) | Fix shape given (`${arr[@]+…}`) + a cell via ORCH_SH. |
| KS-924 | Medium | Backlog | kamil | KS-899 residues: the cardinality floor has a 23-file blind band that swallows 23 of 27 whole packages, and the | Blockchain/Dev/packages/shared/src/__tests__/entrypoint-corpus.test.ts (+ entrypoint-corpus.ts) | Set comparison for the SKIP pin; close the 23-file blind band. |
| KS-934 | Medium | Backlog | kamil | m365 /api/teams/notify: a serial per-row loop with no LIMIT and no aggregate bound, inside the request handler | Blockchain/Dev/services/m365-integration (teams notify) | LIMIT/paging, an aggregate deadline, or off-request dispatch (options listed). |
| KS-941 | Medium | Backlog | kamil | KS-923 harness: the subject guard uses -f not -r, and CELL 12 counts a SKIP as a PASS (12 passed / 11 run) | Blockchain/Dev/scripts/__tests__/orchestrate_jobs.test.sh:47 (git grep) | -r guard, and count SKIP as SKIP. |
| KS-944 | Medium | Backlog | kamil | The gateway's auth gate reads the spec's security: [] — nothing pins the four public wallet ops, and three sui | Blockchain/Dev/services/api-gateway/src/__tests__/ (new) | Pin the four public wallet ops' `security: []` at the gateway. |
| KS-954 | Medium | Backlog | — | KS-858 residue: the repeated-slash collapse does not complete for the /api/billing mount — leading // still 40 | Blockchain/Dev/services/api-gateway/src/routes/proxy.ts, middleware/normalisePath.ts | Leading // on /api/billing; mechanism not determined: investigate, then fix. |
| KS-975 | Medium | Backlog | — | rateLimitScope tri-state: a MALFORMED `sub` silently became a 403 on the ungated /check, and `null` still slip | Blockchain/Dev/services/security/src/rateLimitScope.ts | Decide-and-pin the tri-state arms (technical; a cell each way). HOLD: KS-698 (In Progress) owns the same rate-limit route. |
| KS-976 | Medium | Backlog | — | Rate-limit refusals name the wrong field: 400 says "Key required" when the key was fine, and 403 says "Caller  | Blockchain/Dev/services/security/src/index.ts | Correct the refusal messages. HOLD: security/src/index.ts:1358 is in open PRs #880/#799. |
| KS-1030 | Medium | Backlog | — | KS-754 gate F-3 (MINOR): migration 048 ships with ZERO automated coverage — test:migrations is hard-wired to 0 | Blockchain/Dev/migrations test harness (MIGRATION=…044_vault_entries_repair.sql) | test:migrations is hard-wired to 044; add 048 scenarios against a real DB. No decision named. |
| KS-1037 | Medium | Backlog | — | The NO-FORCE-PUSH rule exists only in .githooks/pre-push and in no .md — document it in CONTRIBUTING.md with i | Blockchain/Dev/CONTRIBUTING.md (rule text today only in .githooks/pre-push, git grep) | Documents an existing ruling (Kam's narrow-allow force-push ruling). Docs only. HOLD: Peter's draft #959 edits Blockchain/Dev/CONTRIBUTING.md. |
| KS-1045 | Medium | Backlog | kamil | KINTSUGI-DEV-SERVER-PLAN.md still says the VM "has NOT been created" — Stage B ran ~3 weeks ago and the credit | Blockchain/Dev/deployment/KINTSUGI-DEV-SERVER-PLAN.md (git grep 'has NOT been run') | Record correction with line numbers given; 'no action on the VM'. #943 touches other deployment/ files, not this one. |
| KS-1047 | Medium | Backlog | kamil | pre-push:230 names the stack-dependent legs as (3, 4, 7); measured they are 3, 4, 8 — a comment asserting a co | .githooks/pre-push:230 | One comment line (3,4,7 → 3,4,8). HOLD: .githooks/pre-push is in open PR #903. |
| KS-1053 | Medium | Backlog | kamil | FLAKE (3rd occurrence, first with a name): ks949 seed-site enumeration fails ~1 in 7 full auth runs and passes | Blockchain/Dev/services/auth/src/__tests__/ks949-platform-admin-seed-identity.test.ts | Investigation with a written start procedure; no decision. Outcome uncertain (flake). |
| KS-1069 | Medium | Backlog | kamil | Gateway verify's persistedAnchored trusts the SHAPE of its inputs — a placeholder txHash, a non-boolean `simul | Blockchain/Dev/services/api-gateway/src/routes/verification.ts (persistedAnchored, ~:570-600) | Fix shape given: apply KS-522 placeholder rules + strict boolean `simulated` in the gateway predicate; the null carve-out is explicitly out of scope. Gate findings were relayed, not re-derived: re-derive first. |
| KS-1070 | Medium | Backlog | — | Tier-2 verify drops `simulated`, so the gateway's simulated guard is structurally inert on that tier | Blockchain/Dev/services/api-gateway/src/routes/verification.ts:253-283 | Fix shape given: carry `simulated` into the tier-2 blob; one cell. |
| KS-1071 | Medium | Backlog | — | The status→confidence decision is implemented twice and the two tiers diverge — on known in-flight statuses AN | Blockchain/Dev/services/api-gateway/src/routes/verification.ts:267-279 and :596-600 (git grep pending-onchain) | Fix shape given: one exported status→confidence mapping, closed default, a cell per tier. The optional CHECK constraint is a migration: leave it out. |
| KS-1098 | Medium | Backlog | kamil | k6 runner echo mask: -e=NAME=VALUE and -qe NAME=VALUE still print the value, contrary to its JSDoc; the name s | systemTest/performance/runner/k6_docker.ts (+ redaction test) | EXCLUDED: already assigned to a lane by Wednesday. |
| KS-1101 | Medium | Backlog | kamil | Gateway health aggregates read anchoring's HTTP status only, so its degraded body (#728) never reaches /health | Blockchain/Dev/services/api-gateway/src/services/health.ts (git grep /health/deep) | Fix named: aggregates read anchoring's body status and map degraded ≠ up; regression cell. |
| KS-1103 | Medium | Backlog | kamil | POST /api/verification/verify validates the published 'hash' field but never reads it — a spec-valid body gets | Blockchain/Dev/services/originate/src/routes/verification.ts:699-734 (git grep) | Recommendation: read `hash` in the handler with the other hash fields + name accepted fields in the 400; the gate's regression cell is given. Take the handler route, NOT 'drop it from the spec' (spec collides with 4 open PRs). |
| KS-1104 | Medium | Backlog | kamil | Verifier mode tabs (Upload File / Enter ID / Scan QR) lose their accessible name at phone width — WCAG 2.1 SC  | Blockchain/Dev/frontend/verifier/src/components/VerifyPage.tsx:267-289 (git grep 'Scan QR') | aria-label or visually-hidden label on the three tabs. |
| KS-1105 | Medium | Backlog | kamil | Admin login placeholder shows the SYSTEM_ADMIN seed address admin@secuura.com (frontend/admin/src/pages/Login. | Blockchain/Dev/frontend/admin/src/pages/Login.tsx:81 (git grep) | Neutral placeholder. |
| KS-1108 | Medium | Backlog | kamil | Akto harness: loadSecretsYml() parses config/secrets.yml with no catch — the KS-1099 shape, whole-file print n | systemTest/akto/src/config/secrets.ts:40 (+ caller config/index.ts, git grep loadSecretsYml) | Measure js-yaml behaviour in the akto package, then apply the KS-1099 shape (sanitised parse error naming path/line/column). |
| KS-623 | Low | Backlog | kamil | Test-token env guard is asymmetric: the gateway fails closed on an unset NODE_ENV, the auth service fails open | Blockchain/Dev/services/auth/src/middleware/authenticate.ts, api-gateway auth middleware, packages/shared | Same allowlist ['development','test'] on both sides via one shared helper; red-proof given. |
| KS-744 | Low | Backlog | kamil | Gateway 500s on every proxied route for a token lacking verificationLevel — auth.ts:377 sets the header unguar | Blockchain/Dev/services/api-gateway/src/middleware/auth.ts:377 | Two-character guard at auth.ts:377, pattern from the line above. |
| KS-811 | Low | Backlog | kamil | Nothing asserts #815's 403 code SET against what the route actually throws | Blockchain/Dev/services/auth/src/__tests__/ (new) | Add a test deriving both 403 code sets (spec vs route). |
| KS-812 | Low | Backlog | kamil | connectors/whatsapp-bot prints the DEAD Container Apps API URL as its default target | Blockchain/Dev/connectors/whatsapp-bot/src/index.ts:21 | Repoint or drop the dead default URL (Wednesday ruled: its own PR). |
| KS-884 | Low | Backlog | kamil | pre-push resolves the bare name `develop`, so a TAG named develop beats the branch — and --quiet suppresses the ambi | .githooks/pre-push:98-99 | Fix shape given: iterate fully-qualified refs (refs/heads/develop, refs/remotes/origin/develop). Latent. HOLD: .githooks/pre-push is in open PR #903. |
| KS-894 | Low | Backlog | kamil | toHaveLength(1) on offendingListenSites is satisfied by the ANNOUNCEMENT row alone — the shape does not distin | Blockchain/Dev/packages/shared/src/__tests__/ks860-test-listeners-bind-loopback.test.ts | Assert non-announcement rows. |
| KS-895 | Low | Backlog | kamil | The mask-desync announcement blames a regex literal for every class — an unclosed ${ } is reported as a regex  | Blockchain/Dev/packages/shared/src/__tests__/ks860-test-listeners-bind-loopback.test.ts | Per-class cause sentence. |
| KS-897 | Low | Backlog | kamil | build_fixture swallows its own failure — `>/dev/null 2>&1` makes a fixture that did not build indistinguishabl | Blockchain/Dev/scripts/__tests__/pre_push_hook_base.test.sh | Stop build_fixture swallowing its failure. |
| KS-900 | Low | Backlog | kamil | The `default` export skip makes a default-only factory silent — it leaves the answer entirely instead of being | Blockchain/Dev/packages/shared/src/__tests__/ks781-p3-3-body-parser-order.test.ts | Report default-only factories by name. |
| KS-906 | Low | Backlog | kamil | CASE 6's `cd /tmp` is inert — the leg uses `git -C "$DEV_DIR"`, so the case does not test what its name says | Blockchain/Dev/scripts/__tests__/ (KS-859 suite) | Fix CASE 6's inert precondition. |
| KS-979 | Low | Backlog | — | KS-597's own bind test file repeats two claims that were corrected in the product file | Blockchain/Dev/services/originate/src/__tests__/ks597-issuer-org-bind.test.ts | Two-line comment sweep in a test file. |
| KS-1006 | Low | Backlog | — | POST /api/users/me/mfa/disable skips code verification when mfaSecret is falsy — the second door | Blockchain/Dev/services/auth/src/routes/users.ts:1064 | Verify the code whenever MFA is enabled (drop the presence guard). HOLD: users.ts is in open PR #930. |
| KS-1072 | Low | Backlog | — | The latest-anchor selector documents a `confirmedAt` tiebreak it does not implement — and since KS-1057 that s | Blockchain/Dev/services/api-gateway/src/routes/verification.ts:240-242 | Implement the documented confirmedAt tiebreak or correct the comment; one cell. |
| KS-1073 | Low | Backlog | — | Tier-2 verify has no statusless-blob cell — the carve-out is unguarded on the tier a third party reaches | Blockchain/Dev/services/api-gateway/src/__tests__/ks1057-verify-confidence-is-status-aware.test.ts | One test cell (tier-2 statusless blob). |
| KS-1089 | Low | Backlog | kamil | run-shell-suites.sh polish from #953's tier-2 gate: make `--list` survive a tree with no suites on bash 3.2 (Q | Blockchain/Dev/scripts/run-shell-suites.sh:71-74, :196-206 | Two polish items with shapes (bash 3.2 --list guard; per-cause headline). |
| KS-1090 | Low | Backlog | kamil | api-gateway + originate: tsc never type-checks #951's three wiring tests, and the mint-scope test pins 2 of 17 | Blockchain/Dev/services/{api-gateway,originate}/tsconfig.json, originate ks1041-vouch-mint-scope.test.ts | Same tsconfig class as KS-1000/KS-848 for api-gateway + originate, plus widen the mint-scope test to all 17 keys. |
| KS-1106 | Low | Backlog | kamil | Verifier shows 'Verification Failed' / 'INVALID' for an id that is not in the registry, with no next step | Blockchain/Dev/frontend/verifier/src/components/ResultPage.tsx (git grep 'Verification Failed') | Show 'not in the registry' as its own result with a next step (specified in the ticket). |
| KS-1084 | No priority | Backlog | kamil | READ ONLY / unverified: the gateway's own Authorization-only calls to originate send no x-tenant-id — single-t | Blockchain/Dev/services/api-gateway/src (direct originate calls); read/measure only | Measurement task ('measure before any fix: drive one site per shape') on a local slot; no ruling needed to measure. |

#### A — description excerpts (first 600 chars)

**KS-1076** — No Playwright e2e test has run on any PR since 2026-09-07 — the suite dies at a static lint gate before any browser opens, and the job name hides it

> **BLUF — no Playwright test has executed on any PR since 2026-09-07. The** `Playwright suite` **job goes red at a static lint gate that runs BEFORE any browser opens, so the red names the wrong subject and the coverage hole has been invisible for three days.**
> 
> This is a **test-coverage** ticket, not a CI-config ticket. It was found while measuring CI gate failures (KS-1075) but must not be closed as gate tuning: the gate is a symptom, the missing e2e coverage is the defect.
> 
> ## What happens
> 
> `Playwright suite` (job in `.github/workflows/pr-platform-suites.yml`) fails at **step 6, "Quality gat

**KS-730** — Security: 71 inline handlers still return err.message verbatim off-production — KS-727's enumerated remainder (api-gateway leaks it TWICE, at the edge)

> ## BLUF
> 
> **71 response-side sites still return** `err.message` **verbatim unless** `NODE_ENV === 'production'`**.** KS-727 fixed the two *shared* handlers — `packages/shared/src/errors` (mounted by 12 services) and `services/auth`'s own — which was the high-leverage half. These 71 are per-route **inline** handlers: the same defect, a mechanical change, but 5 files across 3 services with their own test surface, so they were enumerated rather than folded into [#767](<https://github.com/Secuura/Distributed_Secuura/pull/767>).
> 
> **Do api-gateway first.** It is the edge, and it is the worst of them.

**KS-810** — auth.openapi.ts cannot be imported by any test — passwordLoginGate imports z from zod directly, so a module-scope throw there leaves the suite green

> ## BLUF
> 
> `services/auth/src/auth.openapi.ts` **cannot be imported from a test. It throws on load —** `TypeError: MFA_CODE_ACCEPTED.optional(...).openapi is not a function` **at** `:152` **— because** `services/passwordLoginGate.ts:55` **imports** `z` **from** `'zod'` **directly, which the shared registry explicitly forbids.**
> 
> **Consequence, measured by the KS-796 re-gate: a module-scope** `throw` **in** `auth.openapi.ts` **leaves the auth suite fully GREEN.** The file is in no test's import graph, so nothing in it — 300+ schema registrations, the entire published auth contract — is covered by

**KS-823** — Security: the /api/oauth/token `refresh_token` grant authenticates NO client — a confidential app's refresh token needs no credential

> ## BLUF
> 
> **KS-820 closed the** `authorization_code` **grant. The** `refresh_token` **grant one branch over is still**
> **wide open.** The entire client-authentication block sits inside `if (grant_type === 'authorization_code')`.
> The refresh branch reads no `client_id`, calls no `getAppByClientId`, and never reaches
> `verifyClientSecret` — so **a confidential app's refresh token needs no credential at all**, and a
> **deactivated** app's refresh token keeps working while its authorization codes stop.
> 
> ## Why it is not covered by KS-820
> 
> KS-820's invariant — a code redeems only on a verified secret 

**KS-932** — timeoutMs does not bound DNS resolution — a hung lookup leaves safeOutboundRequest pending well past its declared deadline

> ## Residual, NOT a regression — and it is the same class as the defect that opened the #868 gate
> 
> ### Measured by the gate
> 
> With the lookup hung and a **300 ms** declared bound, the call was **still pending at 2503 ms**. The probe's FAIL condition was "settled", so it could have refuted the finding and did not.
> 
> ### Why it matters more than the number suggests
> 
> The total deadline added in KS-914 round 1 covers connect, TLS, request, response and drain — everything **after** name resolution. `resolvePublicAddresses` is awaited *before* the deadline is armed, so a resolver that hangs is outside 

**KS-938** — Security: "MFA disabled" leaves the TOTP seed and hashed backup codes in the row — updateUser skips every `undefined` field, so a PARTIAL update lands

> **"MFA disabled" leaves the TOTP seed and the hashed backup codes in the row.** The flag flips, the call answers `{success:true}`, and the secret survives.
> 
> ## Mechanism — measured at the wire, in this seat, before it was accepted
> 
> `userRepo.updateUser` builds its SET list with:
> 
> ```
> if (tsField in updates && updates[tsField as keyof User] !== undefined) {
> ```
> 
> `mfaSecret` and `mfaBackupCodes` **are** in `fieldMap` (`mfa_secret`, `mfa_backup_codes`), so the map is not the problem. The value guard is: the key is present, the value is `undefined`, the field is skipped — and a **partial** UPDATE 

**KS-947** — KS-733 gate blindness (F3+F4): the parity cell misses skip:() and mount ORDER, and is purely relative so both mounts can drift off the published spec

> Two MAJOR gate-blindness findings from the KS-733 (#877) tier-1 verdict. Both are about what the **new parity gate cannot see** — the change itself is correct and merged.
> 
> Same family as the tamper that earned the parity cell in #877: **asymmetry rather than absence, one level further out.**
> 
> - [ ] **F3 — the parity cell compares only** `windowMs` **and** `max`**, so two behaviour-DESTROYING edits keep the suite 4/4 green.**
>   Driven by the tester in an express app of the same shape, against a control giving `200,200,200,429,429`:
>   * adding `skip: () => true` to the users mount → **no 429 at 

**KS-958** — The re-link guard matches the JS runtime name case-sensitively — every UPPERCASE spelling is exempt, and ENV NODE_ENV is in 13 of 35 Dockerfiles

> **BLUF** — the re-link guard matches the JavaScript runtime name **case-sensitively**, so every uppercase spelling walks straight past the arm that round 3 just widened. `ENV NODE_ENV=production` **is in 13 of this repo's 35 Dockerfiles** — a stronger signal that a stage runs Node than any of the ten shapes round 3 closed.
> 
> Raised by the KS-930 round-3 tier-1 gate as F-QA-1 (Major). **NOT introduced by round 3** — the class predates it and this head is no worse than base — which is why it was ticketed rather than folded into a round Kam had capped.
> 
> **Measured independently in the round-3 sess

**KS-974** — Published bound vs runtime bound on rate-limit scope: /check enforces code UNITS against a published code-POINT maxLength, and scopeField bounds the untrimmed string

> ## BLUF
> 
> **Two places where the PUBLISHED bound does not match the bound the runtime enforces.** F-1 is MAJOR and leads: `/api/rate-limit/check` publishes `maxLength: 256` and enforces **UTF-16 code units**, on the route with **no role gate** — so the published contract is wrong for every unauthenticated integrator on the one endpoint anybody can reach.
> 
> **Correcting the grouping rationale I was handed:** these are the same **CLASS**, not the same fix. They sit in different schemas in different files and the edits differ — F-1 changes the counting UNIT, F-5 changes WHAT is counted. They are on

**KS-998** — KS-989 gate residue: the formatting gate fails OPEN on missing deps and reads the WORKING TREE, not the push — four items on one path

> ## BLUF
> 
> **[#906](<https://github.com/Secuura/Distributed_Secuura/pull/906>) shipped the KS-989 formatting gate and it works — but the QA gate found four ways it does not catch what it appears to. Two are MAJOR. One of them is the path by which instance 6 itself could still have slipped through.**
> 
> Filed as **one ticket with four items** rather than four tickets: all four are the same question — *what the new gate does and does not catch* (Kam, 2026-09-06: one larger ticket per logical path).
> 
> Parent work: [KS-989](https://linear.app/secuura/issue/KS-989). Merged as `e69fa0dc5`.
> 
> ## Items
> 
> ###

**KS-999** — getUserById's decrypt path escapes the KS-253 classifier — `return await fromRow(...)`, and the characterisation cell that cannot reach its own conclusion

> ## BLUF
> 
> `getUserById`**'s DECRYPT path still escapes the KS-253 classifier, and on an encrypted production row that is the NORMAL path.** The fix is one word — `return await fromRow(...)` — and it was deliberately kept out of [#907](<https://github.com/Secuura/Distributed_Secuura/pull/907>).
> 
> ## Why it matters more than one word suggests
> 
> `fromRow` fetches a **subject DEK — itself a DB read**. So on a normal encrypted row, pool starvation inside `fromRow` produces a raw unclassified error that never reaches the `isInfrastructureDbError` branch [#907](<https://github.com/Secuura/Distributed_Se

**KS-1000** — services/auth tsconfig EXCLUDES src/__tests__ — every 'tsc: 0 errors' on a test-only change in this service is a green that could not fail

> ## BLUF
> 
> `services/auth/tsconfig.json` **excludes** `src/__tests__`**, so** `tsc -p tsconfig.json --noEmit` **type-checks NONE of that service's test files.** Every *"*`tsc`*: 0* `error TS`*"* reported on a test-only change in this service is a **green that could not have failed**.
> 
> ## Measured
> 
> ```
> services/auth/tsconfig.json
>   include: ["src/**/*"]
>   exclude: ["node_modules", "dist", "src/__tests__"]
> ```
> 
> The gate demonstrated the consequence rather than arguing it: **a planted type error in the test file produced 0 errors, while the identical plant in** `userRepo.ts` **produced** `TS2322`**

**KS-1005** — Security/defect: POST /api/users/me/change-password returns 404 for EVERY user — USER_COLS omits password_hash

> ## BLUF
> 
> `POST /api/users/me/change-password` **returns 404 for every user, always.** Nobody can change their
> password through this endpoint. Same root cause as KS-732: `getUserById` selects `USER_COLS`, which
> deliberately omits `password_hash`, so `user.passwordHash` is `undefined` for every account — and the
> line below treats that as "no such user".
> 
> Raised by @PeterObeden as note 5 on PR #872, explicitly as *"a suspicion to confirm, not a claim"*.
> **Confirmed here by reading, on develop.** Not reproduced against a live stack — see Not-verified.
> 
> ## The chain
> 
> `services/auth/src/routes/users

**KS-1020** — Security: GET /api/presentations/{id} returns a real stored presentation for an id that names nothing — LIKE '%id%' fallback with NO ownership check

> ## BLUF
> 
> `GET /api/presentations/{id}` **resolves an UNKNOWN id to an arbitrary stored presentation, with no ownership or tenant check.** `GET /api/presentations/0` returns **200 with a real stored presentation the caller never named** — and so do `abc`, `..`, `1`, `a`, `e`.
> 
> **This is PROVED. The cross-holder half is NOT.** The distinction is load-bearing and is kept intact below.
> 
> ## What was proved
> 
> Six ids that name nothing — `0`, `abc`, `..`, `1`, `a`, `e` — each returned **200** carrying a real stored presentation. The lookup falls back from an exact match to:
> 
> ```
> LIKE '%<id>%' LIMIT 1 

**KS-1029** — KS-754 gate F-2 (MAJOR): PATCH /api/gdpr/dsr/{dsrId} regresses a malformed id from 200 to 500 — UUID_PATTERN exists in the same file and is not used on this route

> **Source:** tier-1 QA gate on PR #914, 2026-09-09. **One-line fix, and the precedent is a sibling route in the same file.**
> 
> ## Measured, driven over real HTTP against the mounted router — three cases, one run
> 
> | dsrId | base | head |
> | -- | -- | -- |
> | **malformed** (`not-a-uuid`) | 200 `{success:false,'DSR not found'}` | **500 INTERNAL_ERROR** |
> | well-formed, absent | 200 `{success:false}` | 200 `{success:false}` — *unchanged, the control* |
> | well-formed, **real** | 200 `{success:false}` ⟵ the KS-754 defect | **200** `{success:true}` ⟵ the fix working |
> 
> ## The fix
> 
> `routes/gdpr.ts:39` **a

**KS-528** — Frontends: react-router v6 → v7 migration (3 moderate client-runtime advisories — open redirect/XSS, constructor injection)

> ## Why
> 
> Three of the KS-493-baselined advisories sit on `react-router`/`react-router-dom` v6 in the three portal frontends (admin / issuer / verifier) and are **client-runtime** classes, not build tooling:
> 
> * GHSA-337j-9hxr-rhxg — arbitrary constructor injection via deserialization (moderate)
> * GHSA-wrjc-x8rr-h8h6 — open redirect via backslash in `<Link>`/`useNavigate` (moderate)
> * GHSA-jjmj-jmhj-qwj2 — open redirect leading to XSS (moderate)
> 
> npm marks the fix as `react-router-dom@7.18.2` with `isSemVerMajor: true` — a v6 → v7 migration, NOT a lockfile bump, so it cannot ride the KS-493 lock-

**KS-530** — @hono/node-server v1->v2 major bump (GHSA-frvp) - originate + mcp-server runtime

> Split from KS-493 (Review H dep-currency wave). @hono/node-server advisory GHSA-frvp-7c67-39w9 (moderate) has fix >=2.0.5 only - a semver-MAJOR v1->v2 bump, so it cannot ride a lock-regen wave.
> 
> Reached at runtime via @modelcontextprotocol/sdk (mcp-server) and pulled by @prisma/dev (dev tooling); also hoisted into the root tree. Pins: originate 1.19.11, mcp-server 1.19.14, root 1.19.17.
> 
> Do: bump to ^2.0.5 in originate + mcp-server standalone locks (root follows), verify hono v2 serve() API usage (breaking changes), rebuild + retest both targets, then remove the GHSA-frvp-7c67-39w9 baseline ex

**KS-704** — k6 gate reports a failure rate with no status-code breakdown - an author cannot tell a platform 4xx from a harness auth failure

> ## BLUF
> 
> When a k6 gate fails, the report prints a failure **rate** and nothing about **which status codes** produced it. An author who sees `100% failed` cannot tell a genuine platform 4xx/5xx from a harness auth-setup failure — and those need opposite responses (fix the platform vs re-seed the persona).
> 
> This is the **KS-700 diagnosability class**: a gate that reports a number without the evidence needed to act on it. k6 is one of only four merge gates now that Actions is retired.
> 
> ## Recommendation
> 
> Surface the per-class counters **already present in the summary** whenever a rate-based thre

**KS-741** — x-emitter-internal is unstripped on the /originate/ route — the marker's safety rests on an unstated convention, and the comment promises the wrong guarantee

> ## BLUF
> 
> `x-emitter-internal` **is non-spoofable today, but for a reason nobody has written down — and the comment that *is* written down promises a different, weaker guarantee that does not hold on one live route.** No exposure now; this is a latent refactor hazard with a false assurance sitting next to it.
> 
> Three parts, one change: **strip it in originate's own middleware · a test that a client-supplied header never reaches anchoring · correct the comment.**
> 
> ## What is true today (measured 2026-09-01, on #742's head `4ea49de47`, merged as `bb3bc5e78`)
> 
> `x-emitter-internal` marks K's own ori

**KS-745** — api-gateway audit export calls /api/audit/logs — a route the security service does not have, so the export 404s every time

> ## BLUF
> 
> **The platform audit export can never return an entry: it calls a route that does not exist. **`services/api-gateway/src/routes/audit-export.ts:138` fetches `GET ${SECURITY_SERVICE_URL}/api/audit/logs`, and the security service has **no **`/api/audit/logs` route.
> 
> ## The mechanism
> 
> The security service publishes exactly three audit routes (`services/security/src/index.ts`):
> 
> * `POST /api/audit` (:546)
> * `GET  /api/audit` (:594)
> * `GET  /api/audit/:id` (:637)
> 
> So `/api/audit/logs` matches the `:id` handler with `id = "logs"`. No audit log has that id, so the handler returns **404** `{"

**KS-747** — Spec drift: GET /api/security/keys declares no parameters while the handler requires organizationId — the contract suite can never reach its 200 branch

> ## BLUF
> 
> `GET /api/security/keys` **declares NO parameters in the published spec, while the handler requires** `organizationId` **and 400s without it.** So every spec-driven caller — including Schemathesis — is steered into a 400 and **can never reach the 200 branch**.
> 
> That is not a cosmetic drift. It is why the KS-742 cross-tenant key-enumeration defect was invisible to the contract fuzzer: the vulnerable branch was unreachable by anything generating requests from the spec.
> 
> Raised by Peter on the KS-742 review thread (2026-09-01 13:11Z); he called it "probably its own ticket rather than wid

**KS-755** — akto unit suite has a standing red: runDir resolveRunId ignores the injected clock

> ## BLUF
> 
> `systemTest/akto/tests/unit/core/runDir.test.ts` — *"stamps the injected clock (millis dropped, colons dashed) when* `AKTO_RUN_ID` *is unset"* — is **failing**, and has been for some time. It expects `2026-07-13T12-00-00Z` from an injected fixed clock and receives the wall clock instead.
> 
> ## Recommendation
> 
> Fix the test or the injection, but do not delete the case: `resolveRunId(clock)` is what freezes a sweep's run id, and a test that cannot observe the injected clock is not guarding it. Low priority as a defect, higher as a **signal** — it means the akto unit suite has a standing re

**KS-759** — tenantId is read through two `as unknown as` casts because it is not on JwtPayload (Peter F14)

> **BLUF —** `tenantId` **is not declared on** `JwtPayload`**, so every reader gets at it through two** `as unknown as` **casts. The type system is being told to look away at exactly the point tenancy is decided.**
> 
> `services/originate/src/middleware/auth.ts:15` and `routes/gdpr.ts` (`connectorContext`) both do:
> 
> ```ts
> const user = (req as unknown as { user?: JwtPayload }).user;
> const tenantId = (user as unknown as { tenantId?: string } | undefined)?.tenantId;
> ```
> 
> The value is real — `ConnectorTokenClaims` carries `tenantId?: string` and the connector exchange sets it — but it is absent from th

**KS-766** — base-image-watch self-test cannot red the DB-age PRODUCER — the F-5 clamp can be re-introduced with the suite green

> ## BLUF
> 
> `base-image-watch.sh`'s self-test can red on the **consumer** of the DB-age value but **not on the producer**. The QA F-5 fix (a future timestamp answers INDETERMINATE instead of printing "0.0h old" inside a CLEARED verdict) is therefore **half-guarded**: reverting `decide()`'s future arm reds the suite; reverting the producer clamp does **not**.
> 
> Found and stated while fixing F-5 on PR #793, rather than left as an implied coverage claim.
> 
> ## Why the producer cannot be red-proved today
> 
> `run_case` calls `decide "$tmp/report" "$ref" "$age" 72` — the age is passed **directly as a string

**KS-784** — POST /api/teams/webhook-config fails the Schemathesis pr sweep on every run — including develop — and is tracked by nothing

> ## BLUF
> 
> `POST /api/teams/webhook-config` **fails the Schemathesis** `pr` **sweep on every run, on** `develop` **as well as on feature branches, and maps to no open ticket.** Not a regression from any current PR — an unrecorded pre-existing failure, which is the shape that quietly becomes "known noise" and then becomes invisible.
> 
> Filed on Wednesday's instruction after it surfaced during #805's contract-gate run. **No fix attempted; not investigated beyond establishing that it is real, stable and unowned.**
> 
> ## Evidence — three runs, one variable
> 
> | run | branch / spec served | tests | failure

**KS-805** — POST /api/oauth/authorize deny emits `Location: undefined?error=…` for an app with zero registered redirect URIs; GET 500s on the same state; PATCH /api/oauth/apps lacks .min(1)

> Filed from the KS-797 QA pass, findings **Q3 (Minor, INTRODUCED by #814)** and **Q5 (Minor)**. Grouped because one `.min(1)` closes the door that makes Q3 reachable.
> 
> ## Q3 — introduced by #814, and stated as such
> 
> For an app with **zero** registered redirect URIs, the deny branch builds `Location: undefined?error=…`. The parent behaviour emitted `/`. Neither is right, but this is a regression introduced by the KS-797 merge and should be recorded that way rather than as pre-existing.
> 
> `GET` answers **500** for the same state.
> 
> **Deliberately not fixed inside #814.** It is a one-line fix, and #

**KS-824** — OAuth app_type: a CASED row is neither normalised by 047 nor refused by its CHECK, and docker/init's unnamed constraint defeats 047's idempotence guard

> ## BLUF
> 
> Two DDL defects left by KS-821's migration 047. **F-2 is the one that matters: a cased row such as**
> `'Public'` **is silently and permanently bricked** — it is not normalised and not refused, and the
> app's users get the false message *"Invalid or expired authorization code"* forever.
> 
> ## F-2 (Major) — the case hole survives 047 in both directions
> 
> * 047's normalisation predicate is `lower(app_type) NOT IN (...)`, so `'Public'` **does not match**
>   and is left untouched.
> * The CHECK it adds **permits** `'Public'` as well, so the row is legal forever.
> * Every consuming rule is an **exac

**KS-825** — Gate integrity: the auth suite's green is not deterministic — three head runs gave 534/0, 534/0, and 534 with 2 FAILED

> ## BLUF
> 
> **A security PR merged on one green run is merged on a sample.** The KS-820+821 gate ran the auth
> suite three times at the head and got **534/0, 534/0, and 534 with 2 FAILED** — the failing file
> (`ks431-oauth-app-update.test.ts`) is **byte-identical at both SHAs**, failing with
> `TypeError: fetch failed` plus a stale 500. The suite's green is a sample, and every gate in this
> class currently reads one draw of it as a verdict.
> 
> ## Mechanism — measured, and the same one twice
> 
> **21 of the 40 auth test files open a server per request** (`app.listen(0)`). s132's `BACKLOG.md`
> entry — `auth.i

**KS-828** — KS-800 scanner: LEG F cannot see the control-byte guard LEAVE a wrapped router — both KS-815 wrappers can drop the guard and packages/shared stays 118/118 green

> ## BLUF
> 
> **The KS-800 corpus instrument (LEG F) cannot see the control-byte guard LEAVE a wrapped router.** Dropping the `controlByteGuard(req, res, next)` call out of EITHER KS-815 wrapper — while keeping the parser it wraps — leaves `packages/shared` **118/118 GREEN**. The class is watched only by KS-815's own service-local test file at the wire, not by the platform instrument built to watch the class across every service.
> 
> Found by the KS-815 tier-1 re-gate (PR #826, round 2 of 2) as **F-05, Minor**. Ruled **not a merge blocker** — #826 merged at `469172b18`. Filed beside KS-817 rather than

**KS-838** — Make the authorize rules DATA the resolver iterates, so the GET/POST agreement guard is structural instead of textual

> **From the KS-822 tier-1 gate.** `projects/secuura/reports/2026-09-06-s136-ks822-835-pass1-04994288a-tier1/` (QA tree)
> 
> `ks804-authorize-get-post-agree-per-rule.test.ts`'s `RULES` table is a hand-maintained literal. Its header once promised that a rule added to one handler and not the other "fails here by construction, because the table below is the list of rules" — corrected in KS-822 F-8, because it is the list of rules *someone wrote down*, not the list the code has.
> 
> F-8 enforced the half that could be enforced: the table's `expected` set must equal the refusal-message set `resolveAuthoriz

**KS-844** — demo-service mounts no error handler — a raw 0x00 body returns express's default HTML with a stack trace and absolute paths

> ## BLUF
> 
> **Pre-existing product defect, NOT introduced by PR #836** — surfaced by the tier-2 gate on that PR while it was driving a real corpus service over a raw socket. `demo-service` **mounts no error handler at all**, so an unhandled error falls through to express's default handler.
> 
> ## What it returns
> 
> A **raw** `0x00` **byte in the request body** produces express's default error page: **1,324 bytes of HTML carrying a stack trace and absolute filesystem paths** (measured by the gate under `NODE_ENV=test`).
> 
> ## Priority — sized from a REPO read, and the tenant is NOT read
> 
> Express's defaul

**KS-848** — services/kyc tsconfig excludes src/__tests__ — the project tsc never type-checks a single test in this service

> ## BLUF
> 
> `Blockchain/Dev/services/kyc/tsconfig.json` sets `"exclude": ["node_modules", "dist", "src/__tests__"]`, so **the project** `tsc` **never type-checks any test in this service.** `npm run build` and `npx tsc --noEmit` both pass while a test file contains type errors, because those files are not in the program at all.
> 
> ## Measured 2026-09-06 (KS-386 #839 fix round 2)
> 
> * `npx tsc --noEmit --listFiles | grep -c ks386-no-image-payload-written` → **0** (the guard is not in the program).
> * Typechecking the same file explicitly (`npx tsc --noEmit --strict … src/__tests__/ks386-no-image-payloa

**KS-849** — KYC mock document flow: a 1.5s timer writes back a STALE verification and silently clobbers the selfie's liveness result

> ## BLUF
> 
> `POST /api/kyc/:id/document` schedules a **1.5-second** `setTimeout` that closes over the verification object it loaded, mutates it, and writes it back. `POST /api/kyc/:id/selfie` loads a **fresh** object. So a selfie that arrives within ~1.5 s of the document upload has its liveness result **silently overwritten** by the stale object when the timer fires.
> 
> ## The mechanism, read from the code at `8b91ab0ae`
> 
> 1. `/document` (`services/kyc/src/index.ts`) does `await dbSaveVerification(verification)` and then, `if (KYC_PROVIDER === 'mock')`, `setTimeout(() => { …; dbSaveVerification(ver

**KS-855** — The OAuth `AVAILABLE_SCOPES` list is a second, divergent scope vocabulary — derive it from SCOPES or pin it

> ## BLUF
> 
> `packages/shared/src/security/scopes.ts` declares itself the *"single source of truth … so the vocabulary can't drift between services"*. **That is true of the enforcement FUNCTIONS and false of the VOCABULARY.** `services/auth/src/services/oauth.ts:57` holds `AVAILABLE_SCOPES`, a **second hardcoded scope list that already diverges** — and the divergence has a live consequence for KS-843.
> 
> ## Measured (KS-843 half-1 gate, PR #841 @ `4111f409ef9f69afeda78249125281476aca19d7`)
> 
> * `AVAILABLE_SCOPES` carries **four names that are not in** `SCOPES` **at all**: `verify:read`, `webhooks:mana

**KS-864** — Dead-estate pointers in RUNTIME SOURCE outside deployment/azure — system-status.ts hard-codes secuura-staging-* hosts, westeurope and a dead URL suffix

> ## BLUF
> 
> KS-490 (3) / PR #852 closed every dead-estate pointer under `deployment/azure` — **6 of 6, and that claim is correct for that directory.** The class does not stop there: it extends into `services/`, where the pointers sit in **runtime source**, not in a template nobody consumes.
> 
> Found by the KS-490 (3) tier-2 gate. **Pre-existing at the merge base — not a defect in #852.**
> 
> ## Measured
> 
> `services/api-gateway/src/routes/system-status.ts` at `:48`, `:232`, `:243`, `:254` hard-codes `secuura-staging-{issuer,verifier,admin}`, `westeurope`, and the dead URL suffix `ashypond-b460d1a1`.
> 
> Th

**KS-865** — check-no-latest-tags.sh silently skips a missing input — it scans 5 of the 6 files it advertises and still prints OK

> ## BLUF
> 
> `Blockchain/Dev/scripts/check-no-latest-tags.sh` **cannot fail on one of the six files it claims to check**, and says nothing about it. A check that cannot fail is indistinguishable from a check that passed.
> 
> Found by the KS-490 (3) tier-2 gate on PR #852 — the same gate this script was used as evidence in, which is what makes it worth fixing.
> 
> ## Mechanism
> 
> `CHECK_FILES` lists `.github/workflows/deploy-staging.yml`. The script `cd`s to `Blockchain/Dev`, where that path **does not exist** (the workflows live at the **repo root**). Line 42's `[ -f "$f" ] || continue` skips it **silentl

**KS-867** — CVE scan image filter `^dev-[a-z-]+:latest$` excludes digits and uppercase — `dev-auth2:latest` is invisible to the scan AND to the KS-676 examined-nothing alarm

> ## BLUF
> 
> **The CVE scan's image filter is** `^dev-[a-z-]+:latest$`**, which excludes digits and uppercase — so** `dev-auth2:latest` **is invisible to the scan AND to the "examined nothing" alarm added in KS-676.** Present identically at `4b207504d` and at `81bf7b078`; pre-existing, not introduced by that PR.
> 
> ## Measured
> 
> `Blockchain/Testing/jobs/04-container-trivy.sh`, the image list:
> 
> ```
> docker images --format '{{.Repository}}:{{.Tag}}' | grep -E '^dev-[a-z-]+:latest$'
> ```
> 
> | tag | matches? |
> | -- | -- |
> | `dev-auth:latest` | ✅ |
> | `dev-api-gateway:latest` | ✅ |
> | `dev-auth2:latest` | ❌ **m

**KS-870** — Every ADMITTED erasure authenticates twice — the door's chain and the catch-all both run authenticateToken, doubling a remote key validation on a partner path

> ## BLUF
> 
> On the erasure path an **admitted** request authenticates **twice**; a refused one authenticates once. Measured fresh by the round-3 gate across 14 shapes × 2 modes: **refused = 1, admitted = 2**.
> 
> Carried out of KS-861 when #845 merged, per the ruling that F-11 is a follow-up and not a gate item. **Not a live defect — a cost defect on a partner-facing path.**
> 
> ## Mechanism
> 
> `services/api-gateway/src/routes/proxy.ts`:
> 
> * `:677` — the erasure door's chain carries `authenticateToken(true)`
> * `:696` — the catch-all `router.use('/api/gdpr', authenticateToken(true), proxy('originate', …))`

**KS-871** — The audit log records `req.path` AFTER the response, so a REFUSED erasure is logged with the path trimmed to `/` instead of /api/gdpr/erasures

> ## BLUF
> 
> `middleware/audit.ts` **gates** on `req.path` at entry but **reads it again inside** `res.on('finish')` — by which time express has left it trimmed to the mount-relative remainder. A **refused** erasure is therefore audited with the wrong path.
> 
> Found by the KS-843 round-3 gate. **Its own ticket, not KS-858's** — KS-858 is the path-normalisation class; this is a lifetime-of-`req.path` bug.
> 
> ## Measured
> 
> | request | `req.path` at entry | `req.path` at `res 'finish'` |
> | -- | -- | -- |
> | `POST /api/gdpr/erasures` refused 403 | `/api/gdpr/erasures` | `/` |
> | `GET /api/gdpr/erasures/:ref`

**KS-872** — packages/shared project tsc is RED on develop — crypto.JsonWebKey is gone in @types/node 26.1.0; a live type error no gate owns

> ## BLUF
> 
> `packages/shared`'s **project** `tsc` reports **1 error** on develop, and no gate owns it.
> 
> ```
> src/crypto/jwks.ts(129,51): TS2694 — namespace 'crypto' has no exported member 'JsonWebKey'
> ```
> 
> `crypto.JsonWebKey` was removed in `@types/node` **26.1.0**. Found by the KS-843 round-3 gate.
> 
> ## Not caused by the KS-843 work — measured
> 
> `git diff 59248bf38 e1d9d9380 -- '*packages/shared*'` is **EMPTY**. The toolchain moved under the shared install some time after 12:38; the source did not change.
> 
> ## Why nothing caught it
> 
> The push preflight's twelve legs do not include a `packages/shared`

**KS-876** — KS-860 guard walks services/ only — test listeners under packages/ are unguarded, including two in packages/shared itself

> ## BLUF
> 
> **The KS-860 guard walks** `services/` **only, so test listeners under** `packages/` **are unguarded** — including two that live in the very package the guard itself ships in.
> 
> ## Measured
> 
> `ks860-test-listeners-bind-loopback.test.ts:87`:
> 
> ```ts
> const SERVICES_ROOT = join(DEV_ROOT, 'services');
> ```
> 
> Unguarded sites today (both currently **correct**, but nothing pins them):
> 
> * `packages/shared/src/__tests__/ks727-errorhandler-class-guard.test.ts:281` — `app.listen(0, '127.0.0.1')`
> * `packages/shared/src/__tests__/ks781-p3-3-body-parser-order.test.ts:183` — `app.listen(0, '127.0.0.1')`
> 

**KS-877** — docker-build.sh: an empty SERVICES_TABLE dies at `${BUILD_LIST[*]}` under bash 3.2 — three lines after the guard added for that class

> ## BLUF
> 
> **With an empty** `SERVICES_TABLE`**,** `docker-build.sh all` **dies at** `:162` **with** `BUILD_LIST[*]: unbound variable` **— three lines after the** `[ -n ]` **guard added in KS-676 to prevent exactly this class.** The guard works; the display expansion immediately after it does not.
> 
> ## Mechanism
> 
> KS-676 added the `[ -n "$_svc" ]` guard so an empty `service_names` cannot put a single `""` into `BUILD_LIST`. It succeeds — `BUILD_LIST` is left genuinely **empty**. Then:
> 
> ```sh
> echo "  Services:  ${BUILD_LIST[*]}"      # :162
> ```
> 
> Under `set -u`, bash 3.2 treats `"${BUILD_LIST[*]}"` 

**KS-878** — 09-aggregate-report: a 04 artefact that exists but does not PARSE emits zero findings and rc 0 — the exact artefact the pre-fix code produced

> ## BLUF
> 
> **A** `04-container-trivy.json` **that EXISTS but does not parse yields ZERO findings and aggregator rc 0 — and that is precisely the artefact the pre-KS-676 code actually produced.** The KS-676 aggregator work classified the *causes* of a well-formed error artefact; it does not cover an artefact jq cannot read.
> 
> ## Mechanism
> 
> `09-aggregate-report.sh`:
> 
> ```sh
> _trivy_err=$(jq -r '.error // empty' "$RUN_DIR/04-container-trivy.json" 2>/dev/null)
> _trivy_reason=$(jq -r '.reason // empty' … 2>/dev/null)
> if [ -n "$_trivy_err" ]; then case "$_trivy_reason" in … esac; fi
> ```
> 
> When jq fails to 

**KS-880** — Quarantine or reconcile the dead converters copy — a second rowToApiKey that maps neither tenantId nor connectorId, with a passing test on it

> ## BLUF
> 
> `services/security/src/converters.ts:122` holds a **second** `rowToApiKey`, imported only by its own test and by **nothing in production**. It has already diverged from the live one, and it is the shape that silently reintroduces a whole class of defect if anyone ever "consolidates" onto it.
> 
> Found during KS-869. **Deliberately not fixed there** — fixing one field in a dead copy would have been arbitrary.
> 
> ## The divergence, measured
> 
> | field | `index.ts:309` (live) | `converters.ts:122` (dead) |
> | -- | -- | -- |
> | `tenantId` | mapped — **the load-bearing tenancy field**, NOT NULL + R

**KS-885** — KS-879 guard: the fifth control asserts a tautology — the escape's EVALUATION is untested, so the ks474 fixture can stop carrying U+0000 with every suite green

> ## BLUF
> 
> **The KS-879 guard's fifth control claims to prove "the ESCAPED spelling is not a raw byte, and still means U+0000", but it proves only the first half. It builds its string with** `String.fromCharCode(0)` **and asserts that carries U+0000 — a tautology about JavaScript, not about the escape. The bridging claim, that the six-character escape** `\u0000` **EVALUATES to U+0000, is asserted nowhere.** Consequence, measured: the ks474 fixture can stop carrying a NUL entirely and every suite stays green.
> 
> ## Where
> 
> `Blockchain/Dev/packages/shared/src/__tests__/ks879-no-raw-control-bytes-repo

**KS-886** — KS-879 guard says "repo-wide" but walks services/ + packages/ only — 749 of 1,242 files; all 148 under tests/ are outside, and tests/ is where this class has twice lived

> ## BLUF
> 
> **The guard is named and documented as "repo-wide" but walks** `services/` **and** `packages/` **only — 749 of the 1,242 tracked source files under** `Blockchain/Dev`**. 493 are outside the net, including all 148 under** `tests/`**, and a test file is exactly where this defect lived.** All 493 are clean today, so this is a claim/coverage gap, not a live escape.
> 
> ## Where
> 
> `Blockchain/Dev/packages/shared/src/__tests__/ks879-no-raw-control-bytes-repo-wide.test.ts`
> 
> * `:69` `const ROOTS = ['services', 'packages'];` — what is actually enforced.
> * `:29` the docblock: *"of 1,240 tracked .ts

**KS-887** — KS-869 test defect (mine): the WRITE-half column-list pin can be satisfied by the COALESCE clause, so a statement missing connector_id from the column list passes all six cells

> ## BLUF
> 
> **This is a defect in a test I wrote**, found by the KS-869 tier-1 gate. My WRITE-half cell claims to pin `connector_id` into the INSERT's **column list**. It does not — it can be satisfied by the `COALESCE` clause twelve characters further on.
> 
> ## The hole
> 
> ```js
> expect(code).toMatch(/INSERT INTO svc_api_keys[\s\S]{0,400}?connector_id/)
> ```
> 
> The `{0,400}` window reaches past the column list into the `ON CONFLICT … COALESCE(EXCLUDED.connector_id, …)` clause. So the assertion is satisfied by a statement that **never names** `connector_id` **in the columns at all**.
> 
> **Measured by the g

**KS-888** — dbSaveApiKey SWALLOWS a failed INSERT — POST /api/keys answers 201 for a key that was never written; blast radius is ALL key persistence, not one column

> ## BLUF
> 
> `dbSaveApiKey` catches every error from its INSERT and only logs it (`services/security/src/index.ts:236-238`). **A key that fails to persist still returns 201 with live key material.** Pre-existing; KS-869 grew its blast radius by taking the statement from 14 columns to 15.
> 
> ## Mechanism
> 
> ```ts
> } catch (err: any) {
>   logger.error('DB save API key failed', { error: err?.message });
> }
> ```
> 
> The route continues and answers 201. The key exists in `memApiKeys` and validates — until the process restarts, at which point it silently does not exist.
> 
> **KS-869's contribution:** on a schema lack

**KS-891** — KS-873 limit: a mask desync that RE-SYNCHRONISES before EOF is still silent — the invariant closes the class only when the desync survives to EOF

> ## BLUF**The KS-873 EOF invariant does NOT close the silent-false-CLEAN class. A mask desync that RE-SYNCHRONISES before end of file leaves the machine in** `code` **with an empty interpolation stack — so nothing is announced — while the listener sites it blanked on the way through stay invisible.** Reproduced against the merged guard at `db1848abf` with two controls.The guard's docblock overstates this. It says *"the next unhandled construct gets caught by this too"*. It is caught only if the desync survives to EOF.## Where`Blockchain/Dev/packages/shared/src/__tests__/ks860-test-listeners-bin

**KS-896** — KS-881's CONTROL is satisfied when the branch does not exist — `upstream=NONE` cannot tell an absent branch from a branch with no upstream

> ## BLUF**The CONTROL cell added by KS-881 asserts** `upstream=NONE`**, and that is satisfied when the branch DOES NOT EXIST AT ALL.** A fixture whose `git checkout` failed produces the same reading as a correctly-built one, so the cell certifies a shape it has not observed.Introduced by #860 (KS-881), which added that assertion. Found by its own gate.## Where`Blockchain/Dev/scripts/__tests__/pre_push_hook_base.test.sh` — the CONTROL block:`bashgit checkout -q -b feature/x --no-track origin/developup="$(git rev-parse --abbrev-ref 'feature/x@{upstream}' 2>/dev/null)"[ -n "$up" ] || up=NONE`If th

**KS-901** — The census cell claims "the corpus misses nothing" — three further express-binding shapes are followed by neither reader, pin, nor census

> ## BLUF
> 
> **The census cell's title says *"and no real service uses any of the five, so the corpus misses nothing"*. The second clause overstates it: three further shapes are followed by neither the reader, nor a pin, nor the census.** None occurs in the tree today, so this is a claim to soften and a gap to declare, not a live hole.
> 
> ## The three unfollowed shapes
> 
> * `require('express')()` — the module called directly, with no binding.
> * **assign-after-declare** — `let express; … express = require('express');`
> * `import('express').then(…)` — the promise form, as opposed to the awaited form H-a5

**KS-902** — no-tracked-credentials.sh cites two scripts as "structurally immune" exemplars — both use a WORSE cwd-relative root derivation

> ## BLUF**The comment added by #858 points the next reader at two scripts as exemplars of the safe idiom. Both use a strictly worse one.**`no-tracked-credentials.sh:81-82` says:> `bare-path-scripts-executable.sh` and `action-pins-labelled.sh` already derive their root this way and are structurally immune; this is the same idiom.Measured at the merged tip `34347a8fa`:`action-pins-labelled.sh:46          REPO_ROOT="$(cd ../.. && pwd)"bare-path-scripts-executable.sh:57  REPO_ROOT="$(cd ../.. && pwd)"`That is **cwd-relative**, not script-relative. It depends on the caller's working directory, where

**KS-903** — Audit the eleven cwd- and script-relative repo-root derivations under scripts/ and systemTest/ — one family, several blind in different ways

> ## BLUF**The** `$(cd ../.. && pwd)` **/** `$(dirname "$0")/../..` **family appears eleven times across** `scripts/` **and** `systemTest/`**, in at least three variants with different failure modes.** KS-859 fixed one of them (`no-tracked-credentials.sh`); the rest are unaudited.## ScopeEnumerate every repo-root derivation under `Blockchain/Dev/scripts/` and `systemTest/`, classify each as script-relative, cwd-relative, or git-derived, and record for each whether it is:- **layout-dependent** (breaks where the repo root is not two levels up — the KS-859 defect), and/or- **cwd-dependent** (breaks

**KS-918** — vite is a production dependency of services/auth — esbuild and fsevents ship into the runtime image, imported by nothing

> ## `vite` sits in auth's production `dependencies`, dragging esbuild and fsevents into the runtime image
> 
> Found by the #849 (KS-490) tier-2 gate as F-2, and measured before filing.
> 
> ### The measurement
> 
> | Reading | Value |
> | -- | -- |
> | `services/auth/package.json` → `dependencies.vite` | `7.3.6` |
> | `services/auth/package.json` → `devDependencies.vite` | **absent** |
> | runtime sources under `services/auth/src` importing `vite` (excluding `__tests__`) | **0** |
> | CONTROL: runtime sources importing `express` | **15** |
> 
> The control is what makes the zero mean something — the same grep shape fin

**KS-922** — KS-868 residue (F1): the empty-array `wait ""` at :91 logs a Stage-1 failure when ZERO jobs started — the same "we tried" lie eleven lines from its fix

> ## What is wrong
> 
> `Blockchain/Testing/ci/orchestrate.sh:91`
> 
> ```bash
> for pid in "${stage1_pids[@]:-}"; do wait "$pid" || log "a Stage-1 job exited non-zero (continuing)"; done
> ```
> 
> When **no** Stage-1 job started, `stage1_pids` is empty, and on **bash 3.2** `"${arr[@]:-}"` expands an empty array to **one empty word**. The loop body therefore runs once with `pid=""`, `wait ""` fails, and the run logs:
> 
> > `a Stage-1 job exited non-zero (continuing)`
> 
> No job exited non-zero. No job ran. This is the same sentence-shape KS-868 exists to delete — wrong, and wrong in the direction that reads as *"we 

**KS-924** — KS-899 residues: the cardinality floor has a 23-file blind band that swallows 23 of 27 whole packages, and the SKIP pin is order-sensitive so a no-op reorder reds it

> Two residues from the tier-2 gate on PR #865's sibling, PR #863 (KS-899). One logical path — the two guards KS-899 added — so one ticket. Every figure below reproduced against the merged tip `e1d840d8e`, not quoted from the gate.
> 
> ## 1. The floor's blind band, and why the cell's own title over-claims
> 
> `entrypoint-corpus.test.ts:257-258`
> 
> ```ts
> const files = sourceFilesUnderRoots(DEV_ROOT, ENTRYPOINT_ROOTS);
> expect(files.length).toBeGreaterThan(350);
> ```
> 
> Measured by re-implementing the walk with the same roots and the same `SKIP`:
> 
> ```
> walked .ts files under services/ + connectors/ : 374
> floor

**KS-934** — m365 /api/teams/notify: a serial per-row loop with no LIMIT and no aggregate bound, inside the request handler — N rows x the guard's 10s default

> ## No aggregate bound over an unbounded row set, in a request handler
> 
> `POST /api/teams/notify` loops over every active webhook row **serially**, inside the request handler, with **no** `LIMIT` **on the query** and **no aggregate deadline** over the loop.
> 
> The gate confirmed the call site passes **no** `timeoutMs`, so each row rides `safeOutboundRequest`'s 10 s default. Worst case is `rows x 10s` with the HTTP request held open throughout.
> 
> KS-914 improved the per-row behaviour — before it, `fetch` was called with no signal at all — but the aggregate was never bounded and still is not.
> 
> ### Fi

**KS-941** — KS-923 harness: the subject guard uses -f not -r, and CELL 12 counts a SKIP as a PASS (12 passed / 11 run)

> Two Minor findings in the KS-923 test harness, from the #869 re-gate (`PASS WITH FINDINGS`, 2026-09-06T11:55:56Z §7). Neither blocked the merge; #869 is merged at `60d1ce97e`. Both are in the **instrument**, not in `orchestrate.sh`.
> 
> Both are the same shape as the defect KS-923 fixed, one level up: **a run that looks like a complete pass while a check did not really happen.**
> 
> - [ ] **QA-923-1 — the harness's own subject guard repeats F1's shape (**`-f`**, not** `-r`**).**
>   `Blockchain/Dev/scripts/__tests__/orchestrate_jobs.test.sh:47`
> 
>   ```sh
>   [ -f "$ORCH" ] || { echo "FATAL: orchestrate.s

**KS-944** — The gateway's auth gate reads the spec's security: [] — nothing pins the four public wallet ops, and three suites stay green if one flips

> The four public wallet routes are public **at the gateway** only because their OpenAPI operations declare `security: []`. **Nothing pins those four values**, and flipping one closes a public route at the edge while every suite that could plausibly notice stays green.
> 
> This is KS-942 one layer up: that ticket closed the gap in the *service router*; this is the same property at the *gateway*, decided by a different mechanism and guarded by nothing.
> 
> ## The mechanism — measured at `066cff675`
> 
> The gateway runs a **spec-aware per-operation auth gate**:
> 
> ```
> index.ts:1021   const { matched, methods

**KS-954** — KS-858 residue: the repeated-slash collapse does not complete for the /api/billing mount — leading // still 404s where /api/governance does not

> **BLUF** — the KS-858 edge normalisation closes the repeated-slash class on 66 of the 67 declared gateway mount classes. `/api/billing` with a **leading** `//` still 404s. **Nothing got worse** — base 404 → head 404 — but this is the class fix not being uniform, on a ticket whose whole point is the class.
> 
> **Measured by the #884 tier-1 gate, deterministic 5/5 and again on a controlled repeat:**
> 
> ```
> HEAD  /api/billing/SAME     -> 401 "No token provided"   (reaches the billing upstream)
> HEAD  /api/billing//SAME    -> 401 "No token provided"   (interior // fixed)
> HEAD  //api/billing/SAME    -> 4

**KS-975** — rateLimitScope tri-state: a MALFORMED `sub` silently became a 403 on the ungated /check, and `null` still slips through explicitScope's second line

> ## BLUF
> 
> **Two arms of the ABSENT-vs-MALFORMED tri-state in** `rateLimitScope.ts` **that nothing pins.** Item 1 is a **behaviour change that already shipped on a live, ungated route** and is currently reversible without a single test going red. Item 2 is a hole in a backstop, not reachable at the wire today.
> 
> **Correcting the framing I was handed:** the grouping described both as *"unpinned arms rather than live defects"*. That is right for item 2 and **understates item 1** — item 1 changed a live response from **200 to 403** on `/api/rate-limit/check`, which has **no role gate**. Unpinned, ye

**KS-976** — Rate-limit refusals name the wrong field: 400 says "Key required" when the key was fine, and 403 says "Caller has no tenant" when the caller has one

> ## BLUF
> 
> **Every new refusal path returns a message that names the wrong thing.** A 400 says the key is missing when the key was fine; a 403 says the caller has no tenant when the caller has a perfectly good one. Charter §4d: a 4xx must not be scored as a healthy rejection without knowing *why* it was returned — and these messages actively mislead about the why.
> 
> Recoverable rather than silent: `details` carries the truth on the 400.
> 
> ## ITEM 1 — `/reset` answers 400 "Key required" for failures that have nothing to do with the key
> 
> `index.ts:1358` — the top-level message is a constant:
> 
> ```
> {"

**KS-1030** — KS-754 gate F-3 (MINOR): migration 048 ships with ZERO automated coverage — test:migrations is hard-wired to 044, so a migrations/ change fires a gate about a different migration

> **Source:** tier-1 QA gate on PR #914, 2026-09-09.
> 
> ## The gap
> 
> 048's new suite **mocks** `$executeRaw` **outright and never touches a database** — its name claims the column widening it does not exercise.
> 
> The repo's only migration-behaviour gate, `npm run test:migrations`, is **hard-wired to one file**:
> 
> ```
> MIGRATION="$HERE/../044_vault_entries_repair.sql"
> ```
> 
> The CI job gated on *"did this change touch* `migrations/`*?"* therefore runs the **044** scenarios. So a `migrations/` change fires a gate about a **different migration** — and Actions is retired for this repo anyway.
> 
> The gate driv

**KS-1037** — The NO-FORCE-PUSH rule exists only in .githooks/pre-push and in no .md — document it in CONTRIBUTING.md with its ALLOW_FORCE escape and the merge-in alternative

> ## BLUF
> 
> **The rule that refused four pushes in one session is written nowhere a person would read it.** `.githooks/pre-push` refuses any non-fast-forward push to a branch that exists at origin — and that rule appears in **no** `.md` **file in the repository**, including `CONTRIBUTING.md`, which is the document `CLAUDE.md` points at as the full branching model.
> 
> ## Measured, 2026-09-09
> 
> * `grep -rln 'NO FORCE PUSH' --include='*.md' .` -> **zero hits**. The same grep against `.githooks/` -> `.githooks/pre-push`.
> * `grep -ci force CONTRIBUTING.md` -> **2**, and **both are substring matches on "e

**KS-1045** — KINTSUGI-DEV-SERVER-PLAN.md still says the VM "has NOT been created" — Stage B ran ~3 weeks ago and the credit-expiry warning has lapsed

> ## BLUF
> 
> `Blockchain/Dev/deployment/KINTSUGI-DEV-SERVER-PLAN.md` **still says the VM has not been created. It was created about three weeks ago, and it has since run, failed, and been recovered from a 53-hour outage.** Record correction — no action on the VM.
> 
> ## The stale claims, with line numbers
> 
> **1.** `:3` **— the status line**
> 
> > *"**Status:** Stage A complete (this document). **Stage B — creating the VM — has NOT been run and needs Kam's explicit go on spend.**"*
> 
> Stage B **has** been run. Measured read-only 2026-09-09 on tenant `efc17e5f…` / sub `a0ee7d32…`:
> 
> ```
> Name                  

**KS-1047** — pre-push:230 names the stack-dependent legs as (3, 4, 7); measured they are 3, 4, 8 — a comment asserting a corpus that moved

> ## The defect
> 
> `.githooks/pre-push:230` names the preflight's stack-dependent legs as **"(3, 4, 7)"**. Measured 2026-09-09 from a real run with `GATEWAY_URL` pointed at a closed port, they are **3, 4, 8**:
> 
> ```
> PREFLIGHT INCOMPLETE — 10/13 legs ran, 3 SKIPPED. Nothing failed.
>   legs 3 4 8 — local stack not up; you can clear this by starting it.
> ```
> 
> Leg 7 is *standalone-lock advisories* (not stack-dependent); leg 8 is *served-spec consistency* (which is). A leg was inserted and the comment did not move.
> 
> ## Why it is worth a ticket rather than a quiet edit
> 
> This is **KS-1046's own failure mode

**KS-1053** — FLAKE (3rd occurrence, first with a name): ks949 seed-site enumeration fails ~1 in 7 full auth runs and passes alone — timeout hypothesis refuted

> ## BLUF
> 
> `ks949-platform-admin-seed-identity.test.ts` **fails intermittently in the FULL** `services/auth` **suite and passes on every re-run.** This is the **third** occurrence of a self-healing auth failure. It is the first one with a **name**, which is the only reason it is a ticket rather than a memory.
> 
> **Cell:** `the real person is gone from every EXECUTABLE seed site › the enumeration actually finds seed sites, including the one the gate planted in`
> 
> ## The measurement, 2026-09-09
> 
> | run | scope | result |
> | -- | -- | -- |
> | 1 | full `services/auth` suite | **FAILED** — `Error: STACK_TR

**KS-1069** — Gateway verify's persistedAnchored trusts the SHAPE of its inputs — a placeholder txHash, a non-boolean `simulated`, and a string/negative blockHeight all report on-chain

> ## BLUF
> 
> `persistedAnchored` **in the gateway's verify decides on-chain from values it never validates the SHAPE of.** Two QA-gate findings on #935 (F3 and F4) that are the same logical path: the predicate trusts *what it is handed*, so a value that is not what the field means still satisfies it.
> 
> Filed as ONE ticket because both are "the predicate accepts inputs it should reject", and a fix for either wants the same guard in the same place.
> 
> ## The predicate
> 
> `services/api-gateway/src/routes/verification.ts` (after KS-1057 / #935):
> 
> ```ts
> const persistedAnchored = Boolean(
>   persistedTxHash &

**KS-1070** — Tier-2 verify drops `simulated`, so the gateway's simulated guard is structurally inert on that tier

> **BLUF:** `persistedSimulated !== true` in the gateway's verify predicate can never be false when the document resolved via **tier 2**, because the tier-2 synthesised blob never carries a `simulated` key. The guard is present in the source and absent in effect.
> 
> **NOT a duplicate of KS-1057's F1.** F1 was the `status` field being read and dropped; this is a *different field* with a *different guard* and a *different fix*. F1 is fixed; this is not.
> 
> **Where:** `Blockchain/Dev/services/api-gateway/src/routes/verification.ts:253-283` — the tier-2 blob emits `txHash`, `blockHeight`, `status`, `con

**KS-1071** — The status→confidence decision is implemented twice and the two tiers diverge — on known in-flight statuses AND on unknown ones, with opposite open defaults

> **BLUF:** the gateway's verify endpoint decides `verificationConfidence` in **two independent places**, one per lookup tier, and they disagree. Nothing in the response says which tier answered, so the divergence is silent.
> 
> **Aggregation note (Kam's one-ticket-per-logical-path rule):** this carries the gate's **F8 and F10** together. They are the same defect — one mapping duplicated per tier — seen on known values (F8) and on unknown ones (F10). One fix closes both. The gate's F9 and F7 are separate paths and are filed separately (F9 = anchor *selection*; F7 = a different field).
> 
> **Where:**
> 
> 

**KS-1098** — k6 runner echo mask: -e=NAME=VALUE and -qe NAME=VALUE still print the value, contrary to its JSDoc; the name set and BASE_URL userinfo are open; PASSWD is unpinned (QA-958-1..3)

> ## BLUF
> 
> * PR #958 (KS-1094) masks secret values in the k6 runner's echoed docker command. Its tier-2 QA gate returned GO WITH FINDINGS at `ffb285752` and found three gaps in that mask. None sits on a path the shipping CLI takes today.
> * **QA-958-1 (Minor, latent):** two spellings docker accepts, `-e=NAME=VALUE` and the clustered `-qe NAME=VALUE`, print the value in clear. The fix's own JSDoc says "Every spelling docker accepts is covered".
> * **QA-958-2 (Polish):** credential-shaped names outside the masked word set, and a BASE_URL carrying userinfo, print in clear. No name the runner emits to

**KS-1101** — Gateway health aggregates read anchoring's HTTP status only, so its degraded body (#728) never reaches /health/deep, /system/status or the health dashboard

> ## BLUF
> 
> * **Anchoring now reports** `degraded` **honestly, but no public health surface can show it.**
>   * Since #728 (KS-671), anchoring's `/health` answers HTTP 200 with `status: 'degraded'` and `degradedReasons` when the chain is unreachable. Keeping the 200 is deliberate.
>   * All three public gateway health aggregates classify a service by HTTP status alone, so they show anchoring as `up` while it cannot reach the chain.
> * **This is the** `/health/ready` **middle path the KS-671 review offered to split out** (KS-671 comments `eba1c64d` and `0c76ac61`, 2026-09-08). It was never filed.
> * **

**KS-1103** — POST /api/verification/verify validates the published 'hash' field but never reads it — a spec-valid body gets 400 'Please provide a content hash…'

> ## BLUF
> 
> * **A spec-valid verify body is refused.** The served spec's `VerifyRequest` publishes `documentId`, `hash`, `title` and `contentHash`. A body carrying only `hash` gets 400 "Please provide a content hash (from the document file) or a documentId."
> * **The same value as** `contentHash` **works.** It gets 200 `verified:false`, "This document hash is not registered…".
> * **Cause:** the handler validates `hash` and never reads it.
> * Pre-existing, found by the kintsugi deploy gate on `4554b25e2` (finding F-4, Minor).
> 
> ## Recommendation
> 
> * Read `hash` in the handler alongside the other hash f

**KS-1104** — Verifier mode tabs (Upload File / Enter ID / Scan QR) lose their accessible name at phone width — WCAG 2.1 SC 4.1.2

> ## BLUF
> 
> * **At phone width, the verifier's three mode tabs have no accessible name.** At 390×844 on `/verify/`, Upload File, Enter ID and Scan QR render icon-only.
> * **Screen-reader users can't tell them apart.** The accessibility tree shows `tab [selected]`, `tab`, `tab` with no names. That fails WCAG 2.1 SC 4.1.2 (Name, Role, Value).
> * **Pre-existing, found by the kintsugi deploy gate on** `4554b25e2` (finding F-5, Minor). No frontend files changed in the deploy range.
> 
> ## Recommendation
> 
> * **Fix:** give each tab an `aria-label`, or replace the `display:none` label with a visually-hidden on

**KS-1105** — Admin login placeholder shows the SYSTEM_ADMIN seed address admin@secuura.com (frontend/admin/src/pages/Login.tsx:81)

> ## BLUF
> 
> * **The admin login's email field shows** `admin@secuura.com` **as its placeholder.** #896's compose comment calls that address the cross-tenant SYSTEM_ADMIN seed account, so the login page hands out the highest-value username.
> * **Pre-existing,** found by the kintsugi deploy gate on `4554b25e2` (finding F-6, Minor).
> 
> ## Recommendation
> 
> * **Use a neutral placeholder.**
> 
> ## Detail
> 
> * **Source:** `frontend/admin/src/pages/Login.tsx:81`, `placeholder="admin@secuura.com"`. The field's value is empty; only the placeholder shows the address.
> * **Mitigation already in the code:** the per-(em

**KS-1108** — Akto harness: loadSecretsYml() parses config/secrets.yml with no catch — the KS-1099 shape, whole-file print not yet measured in this package

> ## BLUF
> 
> * The Akto harness has the same unguarded YAML load that KS-1099 fixes in the k6 runner. `systemTest/akto/src/config/secrets.ts:40`, inside `loadSecretsYml()`, returns `loadYaml(fs.readFileSync(filePath, 'utf-8'))` with no catch.
> * In the k6 runner that shape printed the **whole** secrets file when the YAML was malformed. js-yaml's `YAMLException` holds the entire source in `err.mark.buffer`, and Node's uncaught-exception print inspects the error. For an unquoted value that starts with `!` or `*`, `err.reason` carries the value itself. Measured by s190 on sentinel fixtures (js-yaml 5.

**KS-623** — Test-token env guard is asymmetric: the gateway fails closed on an unset NODE_ENV, the auth service fails open

> Remediation for **KS-486 finding 5** (Review A register, listed Low). Re-verified on `develop de4781ca2` — **the finding is HALF-FIXED, and the register's stated impact is now wrong.** Recording the surviving half so it does not disappear along with the fixed half. Same shape as Review F's F-6.
> 
> ## Fixed since the register was written
> 
> The register says the auth service gates only on `NODE_ENV !== 'production'` while the gateway additionally requires `ENABLE_TEST_TOKENS`. **The auth side now requires it too** (`services/auth/src/middleware/authenticate.ts:24-27`):
> 
> ```js
> // Require explicit op

**KS-744** — Gateway 500s on every proxied route for a token lacking verificationLevel — auth.ts:377 sets the header unguarded

> ## BLUF
> 
> `api-gateway/src/middleware/auth.ts:377` **sets a proxy header from an unguarded claim.** A valid-signature JWT that lacks `verificationLevel` makes the proxy throw `ERR_HTTP_INVALID_HEADER_VALUE` and return **500 carrying the internal message**, on **every proxied route** — not one endpoint.
> 
> **Latent, not live.** Filing it because the fix is two characters of the pattern already used on the line above, and because the 500 leaks an internal error string (the KS-703 / KS-727 shape).
> 
> ## The code
> 
> ```ts
> if (decoded.organizationId) {
>   req.headers['x-organization-id'] = decoded.organiza

**KS-811** — Nothing asserts #815's 403 code SET against what the route actually throws

> ## BLUF
> 
> **The comparison that would catch a drifted refusal code exists only inside a QA evidence script, not in anything the repo runs.** #815 (KS-795, KS-781 door 2) publishes a set of 403 refusal codes in the OpenAPI spec. Nothing shipped compares that published set against the set the route can actually throw. The only place that comparison has ever been made is the two-head re-gate's own `evidence/f7-setcompare.mjs`, which lives in the QA report, not in this repo.
> 
> ## Recommendation
> 
> Add a test that derives both sets and compares them: the codes the spec publishes for the social-callback

**KS-812** — connectors/whatsapp-bot prints the DEAD Container Apps API URL as its default target

> ## BLUF
> 
> `connectors/whatsapp-bot/src/index.ts:21` **still names the decommissioned Container Apps estate as its API target default.** The line falls back to `https://secuura02-demo-api.kindtree-935b2ded.southeastasia.azurecontainerapps.io` when `SECUURA_API_URL` is unset. That host has been **dead since 2026-07-31**, when the 24 Container Apps and `secuura02-demo-env` were deleted. The live demo is the single VM behind `https://secuura02-demo.southeastasia.cloudapp.azure.com`.
> 
> ## Recommendation
> 
> Low. Repoint the default at the VM ingress, or drop the fallback so an unset `SECUURA_API_URL` fa

**KS-884** — pre-push resolves the bare name `develop`, so a TAG named develop beats the branch — and --quiet suppresses the ambiguity warning

> ## BLUF
> `git rev-parse --verify --quiet develop` **resolves a TAG named** `develop` **in preference to the branch, and** `--quiet` **suppresses the ambiguity warning that would otherwise say so. The hook would then compute its base against the tag.** Latent, not live: `git tag -l develop` is empty in this repo today.
> ## Where
> `.githooks/pre-push:98–99` — the loop's first candidate is the bare name `develop`, verified with `git rev-parse --verify --quiet "$_ref"`.
> ## Measured (git 2.51.0, isolated fixture)
> Three commits c1/c2/c3; a tag `develop` at c1, a branch `develop` at c2, `HEAD` at c

**KS-894** — toHaveLength(1) on offendingListenSites is satisfied by the ANNOUNCEMENT row alone — the shape does not distinguish found-a-site from did-not-understand

> ## BLUF**A cell asserting** `toHaveLength(1)` **on the result of** `offendingListenSites` **is satisfied by the ANNOUNCEMENT row alone** — it does not distinguish "the site was found" from "the file was not understood". Measured during #857's own tamper A: the first assertion passed while the second reddened.## Reproduced (at `db1848abf`)`offendingListenSites("const oops = 'never closes")  ->  1 rowrow[0].text starts with "mask desynchronised"       ->  true`So `toHaveLength(1)` holds with **zero** real sites.## Where`packages/shared/src/__tests__/ks860-test-listeners-bind-loopback.test.ts` — 

**KS-895** — The mask-desync announcement blames a regex literal for every class — an unclosed ${ } is reported as a regex problem

> ## BLUF
> 
> **The mask-desync announcement hard-codes one cause sentence for every class of desync**, so a template-interpolation desync is reported as a regex-literal problem.
> 
> ## Reproduced (at `db1848abf`)
> 
> `offendingListenSites('const x = \`a ${ (() => {')` emits exactly one row, whose text is:
> 
> > mask desynchronised — reached EOF in 'code' state with **tplDepth 1**, so the rest of this file was scanned blind. **A regex literal containing a quote is the known cause.** Results for this file are not a clean bill of health.
> 
> The state and depth are right; the cause sentence is wrong and will sen

**KS-897** — build_fixture swallows its own failure — `>/dev/null 2>&1` makes a fixture that did not build indistinguishable from one that did

> ## BLUF**`build_fixture` redirects its entire body to `/dev/null 2>&1`, so a fixture that fails to build is silent.** Every case downstream then asserts against a repository that may not exist, and the failure surfaces (if at all) as a confusing assertion rather than as "the fixture did not build".Pre-existing — introduced with the suite in #855 (KS-854), not by #860.## Where`Blockchain/Dev/scripts/__tests__/pre_push_hook_base.test.sh` — the closing `) >/dev/null 2>&1` of `build_fixture`. The redirect is deliberate (the fixture build is noisy: `git init`, `commit`, `push`), but it swallows fai

**KS-900** — The `default` export skip makes a default-only factory silent — it leaves the answer entirely instead of being reported as unreachable by name

> ## BLUF**The** `default` **skip added by KS-857 N-3 closes one silent case and opens a smaller one:** a parser factory exported ONLY as `export { x as default }` now contributes no name to the answer, so if it is also absent from `PARSER_FACTORY_NAMES` the equality leg is satisfied and nothing fires. No live instance — `request-limits.ts` has no export list at all.## Where`ks781-p3-3-body-parser-order.test.ts` — `addExport`'s `if (exportedAs === 'default') return;`.The skip is correct on its own terms: `"default"` is not a name a consumer can call and `PARSER_FACTORY_NAMES` could never carry i

**KS-906** — CASE 6's `cd /tmp` is inert — the leg uses `git -C "$DEV_DIR"`, so the case does not test what its name says

> ## BLUF**CASE 6 of the KS-859 suite changes directory to** `/tmp` **to simulate "outside a work tree", but the leg resolves its root with** `git -C "$DEV_DIR"` **— the process's cwd is irrelevant.** The case passes for a different reason than the one it [documents.It](<http://documents.It>) is not a false green in the dangerous direction: the case still exercises a genuine not-a-work-tree path, because the fixture directory it points `DEV_DIR` at is itself outside any repository. But the mechanism in the cell's name is wrong, and a reader copying it will write an inert precondition.## Fix shap

**KS-979** — KS-597's own bind test file repeats two claims that were corrected in the product file

> ## BLUF
> 
> **Two claims corrected in the product file during KS-597 round 2 were never swept into the PR's own new test file.** The class was fixed; this instance was not. Both are in `services/originate/src/__tests__/ks597-issuer-org-bind.test.ts`, verified still present on merged develop (`2ff0eb850`).
> 
> **These are my own errors, corrected in one place and not the other** — which is the failure mode worth recording, because a corrected comment beside an uncorrected copy of itself is *more* misleading than the original, not less: a reader who checks one of them concludes the file is trustworthy

**KS-1006** — POST /api/users/me/mfa/disable skips code verification when mfaSecret is falsy — the second door

> ## BLUF
> 
> `POST /api/users/me/mfa/disable` (`services/auth/src/routes/users.ts:1064`) **skips verification when**
> `mfaSecret` **is falsy** — the same "guarded on presence rather than on proof" shape KS-732 removes from
> the sibling door at `POST /api/auth/mfa/disable`.
> 
> Raised by @PeterObeden as note 4 on PR #872, rated Low and explicitly offered as a separate ticket
> rather than scope creep. Confirmed by reading.
> 
> ## The shape
> 
> ```
> const { code } = req.body;
> const user = await userRepo.getUserById(req.user!.userId);
> if (!user.mfaEnabled) throw new BadRequestError('MFA is not enabled');
> if (!code

**KS-1072** — The latest-anchor selector documents a `confirmedAt` tiebreak it does not implement — and since KS-1057 that selector decides the verdict

> **BLUF:** `verification.ts:240` says *"Latest = highest blockNumber, fall back to most-recent confirmedAt."* **There is no secondary key.** The sort is `(b.blockNumber || 0) - (a.blockNumber || 0)` and `confirmedAt` is never consulted.
> 
> **Where:** `Blockchain/Dev/services/api-gateway/src/routes/verification.ts:240-242`, read at PR #935 head `dd9463b37`.
> 
> **Failure scenario:** two anchors on one document with equal `blockNumber` (including the common `0`/null case, which `|| 0` collapses). Ties break only on `Array.prototype.sort` stability over whatever order anchoring returned — `ORDER BY cre

**KS-1073** — Tier-2 verify has no statusless-blob cell — the carve-out is unguarded on the tier a third party reaches

> **BLUF:** the code half of the gate's **F5**, deliberately kept off PR #935 because round 2 of 2 was spent and a new cell would have moved the gated SHA.
> 
> **What #935 shipped instead:** the comment and title corrections only (commit `dd9463b37`), which need no re-gate. This is the work that was carved out of it.
> 
> **The gap:** the legacy carve-out `persistedStatus == null` is pinned by exactly **one** cell — the tier-1 `REGRESSION: a legacy statusless blob` — measured by s165: deleting `|| persistedStatus == null` gives **1 failed / 8 passed / 9 total**, and that is the only red. There is **no 

**KS-1089** — run-shell-suites.sh polish from #953's tier-2 gate: make `--list` survive a tree with no suites on bash 3.2 (QA-8, `:72`) and give the git-list refusal a headline per cause (QA-7)

> ## BLUF
> 
> Two Polish findings from the tier-2 QA gate on PR #953 (KS-1086), both in `Blockchain/Dev/scripts/run-shell-suites.sh`. Neither blocks #953, and no gate reaches either.
> 
> - [ ] **QA-8 — pre-existing on develop.** `run-shell-suites.sh --list` on a tree with zero reached suites dies on bash 3.2 with `line 72: reached[@]: unbound variable`, rc 1. It is present on develop `2d864ae92` and unchanged by #953.
> - [ ] **QA-7 — in #953's delta.** The run-mode refusal prints the headline `FAIL — could not ask git which variables are repository-local` for every cause, including when git DID print a

**KS-1090** — api-gateway + originate: tsc never type-checks #951's three wiring tests, and the mint-scope test pins 2 of 17 non-originate keys

> ## BLUF
> 
> * **The type-check claim does not cover the tests (R2-2).** #951's Test Evidence says "`tsc --noEmit` rc 0 on both services", but that run never reads its 3 new test files.
>   * Both services' tsconfigs exclude `src/__tests__`.
>   * A type error planted in each test file returns rc 0; the same plant in `routes/proxy.ts` returns rc 2.
> * **The mint-scope test pins 2 of 17 (R2-3).** `ks1041-vouch-mint-scope.test.ts` asserts "no vouch" only at analytics and auth. An allowlist widening that spares those two keys stays green.
> * **Test-quality findings, not runtime defects.** They come from th

**KS-1106** — Verifier shows 'Verification Failed' / 'INVALID' for an id that is not in the registry, with no next step

> ## BLUF
> 
> * **Enter an id that is not registered, and the verifier shows "Verification Failed" and "INVALID" with no next step.** The API behind it said `"Document not found in the registry"`.
> * **A mistyped id reads like a document that failed verification.** Honesty holds: it never claims verified.
> * **Pre-existing,** found by the kintsugi deploy gate on `4554b25e2` (finding F-7, Polish).
> 
> ## Recommendation
> 
> * **Show "not in the registry" as its own result,** and tell the user what to do next: check the id, or verify by file instead.
> 
> ## Detail
> 
> * **Measured by the gate:**
>   * A random v4 id 

**KS-1084** — READ ONLY / unverified: the gateway's own Authorization-only calls to originate send no x-tenant-id — single-tenant originate may scope them to DEFAULT_TENANT_ID

> ## BLUF
> 
> **READ ONLY, not driven by anyone.** api-gateway calls originate directly — outside `createProxyRoutes` — at several sites and sends only `Authorization`. With no `x-tenant-id`, originate's KS-458 block (`services/originate/src/index.ts:248-256`) sets `req.tenantId` to `DEFAULT_TENANT_ID` in single-tenant mode, so those calls **may** read or write in the default tenant rather than the caller's. Independent of PR #951 (unchanged by it). Raised by the #951 tier-1 gate (round 1, Open item b) and not measured.
> 
> ## Recommendation
> 
> Measure before any fix: drive one site per shape (a read, a


### B — needs Peter, Stuart or Kam (the words that make it so)

| id | P | state | assignee | title | reason |
|---|---|---|---|---|---|
| KS-441 | Urgent | Blocked | stuart | Akto CI scan throughput: ~21 s local vs ~10 min in the isolated pr-akto stack (~28×) — investigate worker star | Assigned to Stuart: stays theirs. |
| KS-608 | Urgent | Backlog | peter | systemTest (Integration mode): GET /api/anchors/{id} and verify must not contradict each other about the same  | Assigned to Peter: stays theirs. |
| KS-61 | High | Todo | stuart | OpenAPI compliance: documentation gaps across the spec (descriptions, parameter docs, operationId) | Assigned to Stuart: stays theirs. |
| KS-188 | High | Todo | stuart | Stateful testing: declare OpenAPI `links` + `operationId` so POST→GET→DELETE chains are exercised (currently 0 | Assigned to Stuart: stays theirs. |
| KS-229 | High | In Review | kamil | [Tracker] 2026-06-10 platform assurance review — gap-analysis + remediation | Umbrella tracker (Kam). |
| KS-239 | High | Backlog | stuart | [Decision] Erasure: multi-step to trigger, but irreversible + complete once executed — confirm no recoverable  | Assigned to Stuart: stays theirs. |
| KS-304 | High | Backlog | kamil | Tokenise personal/identifying data — mint a privacy token (Platform S/K by journey origin) and thread it throu | Tokenisation design across Platform S/K. |
| KS-329 | High | Backlog | kamil | Phase 2 — JWT RS256 → hybrid (RS256 + ML-DSA-65) | 'Kam's ruling needed on a design change'. |
| KS-412 | High | Todo | peter | CI: require all systemTest (all tools) PR suites + pre-merge to block merges on failure (branch protection + s | Assigned to Peter: stays theirs. |
| KS-485 | High | Todo | kamil | Security review — plan, methodology & handover (Platform K) | Security-review hub/plan (Kam). |
| KS-491 | High | Todo | kamil | Review F — Edge, WAF, DDoS & anti-automation | Strategic WAF gap + absent Caddyfile: edge infra decisions. |
| KS-525 | High | Backlog | peter | Playwright: end-to-end flow coverage across all 310 published API operations | Assigned to Peter: stays theirs. |
| KS-568 | High | Backlog | peter | systemTest (Schemathesis): S↔K connector identity regression coverage (KS-480 Option A) — tier separation, rot | Assigned to Peter: stays theirs. |
| KS-575 | High | In Progress | peter | Schemathesis sweep locks itself out of its own account (demo@secuura.io) by fuzzing POST /api/users/me/change- | Assigned to Peter: stays theirs. |
| KS-588 | High | Backlog | peter | systemTest (Schemathesis): /api/status authorization + revoked-session regression coverage (KS-570 class — vc- | Assigned to Peter: stays theirs. |
| KS-590 | High | Backlog | peter | systemTest (Schemathesis): verify-by-hash must not resolve to an arbitrary registration — anchored-ancestor +  | Assigned to Peter: stays theirs. |
| KS-598 | High | Todo | kamil | Architecture P1: defuse the MULTI_TENANCY registry upsert — it silently collapses registrations per (hash, ten | Choice between re-keying the registry and removing the upsert, 'in the same phase' of a plan. |
| KS-602 | High | Backlog | kamil | BM-1: Certification model — certification = attestation + signing + optional watermarking; any modification →  | BM-1 epic: product model from the technical weekly (Stuart/Phil/Kam). |
| KS-603 | High | Backlog | kamil | BM-2: Verification is a configurable workflow via smart contracts — record the workflow path, not casual views | BM-2 epic: product model. |
| KS-607 | High | Backlog | kamil | GET /api/anchors/{id} and verify report different statuses for the same anchor — 91 UAT anchors read "failed"  | Question to Kam ('one authenticated call settles this'), raised from the S side. |
| KS-618 | High | Backlog | kamil | Client IP is invisible platform-wide on demo: every IP-keyed control sees 172.18.0.1 — brute-force, lockout an | Demo nginx real-IP configuration: demo-affecting. |
| KS-624 | High | Backlog | kamil | prism issues VCs with random bytes as the Ed25519 proof and verifies them as passed — the A-11 fraud pattern f | 'The by-design-or-remediate ruling is Kam's'. |
| KS-636 | High | Backlog | kamil | node:24-alpine carries a CRITICAL (CVE-2026-59873) — our own base-image watchdog flagged it on 2026-08-01 and  | 'Read CVE-2026-59873 and decide: rebuild, bump, or accept'; a rebuild 'lands behind the Kintsugi hold'. |
| KS-638 | High | Backlog | kamil | The extranet test board has never shown a green run — 0 passed in 22, and the latest red is E2E 210/0 with Sch | Extranet test board (separate project). |
| KS-655 | High | Backlog | kamil | KS-78 drift check is wrong three ways — reports 7 commits of drift where 212 exist, labels `develop` as `main` | Launcher (outside git); comment: 'Changing it is Kam's call'. |
| KS-661 | High | In Review | kamil | Rename the `certify` lifecycle verb to `declare` | 'the vocabulary is yours [Kam] … a proposal, not a decision'; requested by Stuart with a paired S ticket. |
| KS-668 | High | Backlog | kamil | Compose seeds published *123 credentials by default, and the 11 rotation vars never reach the auth container f | Compose credential defaults affecting 'every compose deploy: local, the demo VM, and Kintsugi'. |
| KS-678 | High | Backlog | kamil | #568 publishes 17 URLs on secuura.io — an unresolving, seemingly unowned domain (KS-669 class; no guard rule c | 'Calls needed from @PeterD': do we own secuura.io; is example.com acceptable. |
| KS-683 | High | Todo | kamil | Anchor-status standoff: a consumer repolls anchors K reports as terminally failed — K's labelling is already h | Fix is consumer terminal-state handling (Platform S side, Stuart). |
| KS-692 | High | Backlog | kamil | Security: /api/status revoke/unrevoke has no tenant ownership check — an ISSUER_ADMIN in any tenant can revoke | Code comment defers tenant scoping to 'the KS-539/KS-547/KS-586 joint authorization decision'; status lists have no tenant linkage, so the fix picks an ownership model. |
| KS-696 | High | Todo | kamil | Akto pr-scan is non-deterministic — three runs on near-identical code gave 1 HIGH / 1 HIGH (different endpoint | Akto non-determinism investigation: Peter's systemTest gate/report class; needs the Akto stack. |
| KS-709 | High | Backlog | kamil | Akto reports a PASS for a test that executed NOTHING — 'clean 0 / not-applicable 969 ✓' is a second false-zero | 'Peter's measurement … not independently reproduced'; Akto report logic (Peter's class). |
| KS-716 | High | Todo | kamil | The whole super-admin surface is silently unscanned — no system_admin block means the HAR replay fallback neve | Needs a system_admin block with a seeded admin credential in local secrets.yml: credentials. |
| KS-723 | High | Todo | kamil | Declare the remaining ~157 routed-but-undocumented /api operations in the OpenAPI spec — the KS-712 remainder | 'Peter-sized, and deliberately routed to him'. |
| KS-724 | High | Todo | kamil | A scan that logs in more than ten times as one user revokes its own bearer — the 10-session window evicts the  | Akto harness scan-credential design: Peter's systemTest class. |
| KS-725 | High | Todo | kamil | test:pr never re-imports the OpenAPI spec, so Akto scans a collection that has drifted from it — a declared op | 'Re-importing the spec into Akto mutates harness state … @PeterObeden has live work on it'. |
| KS-735 | High | Todo | kamil | Verify results show the user nothing about what was registered — a renamed file confirms green with no explana | 'the flat-vs-nested contract question in §2: that is Peter's call' (catalogue pass bounced it to Peter). |
| KS-753 | High | Backlog | kamil | Timestamping fail-closed: a mock TSA fallback must not report verified: true (extend KS-523 to the batch path) | 'Open design question for the ruling: refuse the write (503) or persist it with verified: false?' |
| KS-756 | High | Backlog | kamil | Wire up the opaque refresh token that createSession already mints — one write site, zero read sites (KS-329 ru | 'Transition, and this is the decision worth making explicitly' (accept both token formats vs a forced re-login). |
| KS-769 | High | Backlog | kamil | mobile/secuura-app has 81 unscanned advisories (2 critical) — nothing has ever audited that tree | 81 advisories in mobile/secuura-app: baseline acceptance is a posture decision. |
| KS-770 | High | Todo | kamil | Review stream: API contract and the four platform suites | Review stream for Peter. |
| KS-772 | High | Todo | kamil | Review stream: S<->K integration contract | Review stream for Stuart. |
| KS-775 | High | In Progress | kamil | [Decision] Own the express 4 -> 5 call before the qs fuse lapses 2026-09-10 - KS-409 was archived and nothing  | 'The decision itself is Kam's / Peter's, not the builder's'. |
| KS-785 | High | Backlog | kamil | Compose resolves the SHELL over .env while the checker resolves .env over the shell — a green credential check | 'the fix is a behaviour change' on the rotation-day credential checker Stuart and Peter rely on. |
| KS-787 | High | Backlog | kamil | S revokes that emit no lifecycle event, or emit share-permission-change, are indistinguishable on K from a doc | K-side question implied by Stuart's PS-749 split. |
| KS-835 | High | Todo | kamil | Security: OAuth consent is decorative — the granted scope never reaches the token, and the gate short-circuits | Redesign of consent scope → token authority. |
| KS-889 | High | Backlog | kamil | KS-869's COALESCE backfill has an EMPTY window — the 39 pre-existing keys never backfill, so the KS-843 cutove | Backfill design for existing keys; KS-843 cutover evidence. |
| KS-939 | High | Backlog | kamil | Launcher: the assembled boot prompt is asserted by no cell — KS-907's fix can vanish at 18/0, and the seat sen | Launcher boot prompt (by-hash launcher, outside git). |
| KS-951 | High | Backlog | kamil | The default-password CI gate catches one shape and calls it clean — 16 published passwords are exempt by desig | 'Decide whether the seedPw( exemption should survive at all'. |
| KS-953 | High | Backlog | — | CLASS: editing api-gateway/src/index.ts silently reddens packages/shared, and nothing in the touched package c | 'Shapes worth considering (not chosen: this needs a decision)'. |
| KS-955 | High | Backlog | — | A fresh clone cannot run the four platform suites, and fails in a way that reads like a product regression | Fix shapes not chosen; default seed-password credentials in .env.example. |
| KS-967 | High | Backlog | — | Neither credential guard can see a value in a .env.example — one scans the wrong roots and extensions, the oth | A new push-time credential gate over .env.example is gate policy; existing template literals are under KS-731 (In Progress). |
| KS-977 | High | Backlog | — | `setup`/`install` are exempt from the pre-suite step on a false justification — they perform a live authentica | 'Do not simply delete the exemption'; Kam's round-4 authorisation excluded it; schemathesis run.py (Peter's harness). |
| KS-983 | High | Backlog | peter | systemTest: no suite drives a path-spelling (`//`) variant — the KS-858 class is guarded only by gateway unit  | Assigned to Peter: stays theirs. |
| KS-987 | High | Backlog | — | A deploy that rsyncs the OpenAPI spec and does not restart api-gateway ships a silently stale published contra | Demo redeploy runbook. |
| KS-995 | High | Backlog | kamil | Archiving a ticket silently archives its sub-issues, including NON-TERMINAL ones — and the parent-side check c | Linear archive-cascade mechanics: board admin (Kam). |
| KS-996 | High | Backlog | kamil | 95 archived tickets sit in NON-TERMINAL states — measure whether a cascade put them there | History measurement of archived tickets: board admin (Kam). |
| KS-997 | High | Backlog | kamil | Re-triage four npm advisories that landed in the audit baseline ALREADY EXPIRED (Kam's `add-dead` ruling) | Re-triage of accepted advisories under Kam's add-dead ruling: each accept/reject is posture. |
| KS-1009 | High | Backlog | — | Security: GET /api/auth/wallet/status returns userId + role to ANY anonymous caller — enumeration surface, and | Contract change on a published unauthenticated auth endpoint; Peter raised it as a question on #802 ('Would trimming it … lose anything the sign-in flow needs?') and no answer from Peter is recorded. |
| KS-1012 | High | Backlog | kamil | The `require-pr-gates` ruleset survived the Actions retirement: 7 required checks that can never report, 0 req | GitHub ruleset/branch protection on develop+main: org admin settings (Kam). |
| KS-1024 | High | In Review | — | PUSH BLOCKER (repo-wide): two new advisories are unbaselined, so preflight 6/13 + 7/13 fail on EVERY branch —  | 'needs a ruling, not a workaround': baselining advisories is a security-posture decision. |
| KS-1025 | High | Backlog | — | Reshape the advisory gate: it is NON-DETERMINISTIC on an unchanged tree — 8 advisories in 30 min, one appeared | 'The WINDOW LENGTH is explicitly reserved for him' (Kam). |
| KS-1028 | High | Backlog | — | KS-754 gate F-1 (MAJOR): a step-12 throw skips the USER_ERASED fan-out AFTER the crypto-shred — local data des | 'The fix: either, not both': design choice on the GDPR Art.17 erasure fan-out path. |
| KS-1031 | High | Backlog | — | KS-754 gate F-4: DEPLOY CONDITION — apply 048 BEFORE rolling the originate image, or every connector erasure s | 'DEPLOY CONDITION … No deploy is authorised': deploy ordering. |
| KS-1035 | High | Backlog | — | The merge gate cannot see a WITHDRAWN approval — #813 reads approved+clean against the reviewer's written refu | Merge gate vs a withdrawn approval (Peter: 'I'll ask a maintainer to dismiss'): maintainer/admin action and process. |
| KS-1036 | High | Backlog | — | The review-stream overlay covers 57 of 114 active tickets, and DEV-PROCESS still says 'nothing left over' | Review-stream overlay Kam adopted + DEV-PROCESS.md process text. |
| KS-1044 | High | Backlog | kamil | No independent liveness signal for our own VMs — kintsugi was dead for 53 h and Azure health read `Available`  | Independent VM liveness monitoring for kintsugi: Azure infra/alerting on Kam's estate. |
| KS-1054 | High | Backlog | kamil | Fresh databases are FAIL-OPEN until the second boot — 039_rls_fail_closed does not apply on boot 1 (file stage | 'Fix shapes (not a ruling)', 'That is a design decision'; tied to a deploy hold. |
| KS-1080 | High | Backlog | — | SECURITY (local test stack): akto-autoheal runs as root with /var/run/docker.sock RW — env-scoping is only as  | 'the remedy is a decision for whoever…'; comment files it in Peter's §1b systemTest high-risk class. |
| KS-1081 | High | Backlog | — | CONFIG DRIFT: two tracked env templates disagree by ~39 vars — bootstrap-env.sh reads .env.example, CLAUDE.md  | 'No winner picked … a decision about which is authoritative'. |
| KS-1087 | High | Backlog | kamil | workflow-approve deletes the pending document and answers 200 "Document has been created" without reading orig | Item 2 ('Forward a credential originate accepts') sits on the unprovisioned GATEWAY_VOUCH_SECRET design (KS-1083/KS-1041); items 1+3 alone would turn every approval into an error on today's stacks, a visible demo-flow change. Priority was set by the coordinator, 'Kam may override'. |
| KS-1100 | High | Backlog | kamil | Kintsugi deploy 4554b25e2: four live changes have no QA gate record — #872 (KS-732), #896 (compose ADMIN_USER_ | QA-gate records for a kintsugi deploy: deploy/QA process. |
| KS-1107 | High | Backlog | kamil | POST /api/auth/register accepts a client-supplied organizationId with no existence or membership check — impac | Org trust boundary Kam ruled `bind`; 'Impact NOT traced'; 'Do not exercise it on a running environment without explicit authorisation'. |
| KS-101 | Medium | Backlog | stuart | Consolidate Platform K billing onto Platform S's Stripe integration (one company, one Stripe) | Assigned to Stuart: stays theirs. |
| KS-135 | Medium | Todo | stuart | Platform S "S+" refactor — pluggable upload/watermark/sign/certify services | Assigned to Stuart: stays theirs. |
| KS-139 | Medium | Backlog | stuart | Platform S — upload your test suite so the extranet live runner executes it (GitHub Actions) | Assigned to Stuart: stays theirs. |
| KS-263 | Medium | Backlog | kamil | Enable Code Security / GHAS so security scans populate the Security tab (currently artifact-only) | Enable GHAS/Code Security: org setting, possible cost. |
| KS-305 | Medium | Backlog | kamil | State the M365 source-document controller boundary in the customer DPA | Customer DPA wording: legal. |
| KS-418 | Medium | Blocked | peter | systemTest (all tools): enable nightly platform test suites after full AWS migration | Assigned to Peter: stays theirs. |
| KS-492 | Medium | Todo | peter | Review G — systemTest (all tools) security regression coverage | Assigned to Peter: stays theirs. |
| KS-502 | Medium | Todo | peter | systemTest (Schemathesis): skipped security regressions needing a proper harness/env (billing idempotency · se | Assigned to Peter: stays theirs. |
| KS-526 | Medium | Backlog | kamil | KMS: move platform wallet mnemonic to Key Vault (KS-326 follow-up) | Key Vault for the wallet mnemonic: Azure infra + credentials. |
| KS-533 | Medium | Todo | peter | S↔K security register: data-loss / unrecoverability scenarios + code-verified findings (extracted from KS-480  | Assigned to Peter: stays theirs. |
| KS-571 | Medium | Backlog | peter | systemTest (Schemathesis): KS-539 agent document-operation rules — onBehalfOf realignment (G-1) + R2/R4/R5/R6  | Assigned to Peter: stays theirs. |
| KS-572 | Medium | Backlog | peter | systemTest (Schemathesis): pin the KS-546 unhandledRejection posture — config drift + the mirrored KS-529 guar | Assigned to Peter: stays theirs. |
| KS-573 | Medium | In Progress | peter | systemTest (Schemathesis): assert the shared control-byte boundary is mounted in every consuming service (KS-4 | Assigned to Peter: stays theirs. |
| KS-579 | Medium | Todo | kamil | Per-person platform-admin identities — the shared seeded admin cannot carry attribution or approval | Carried from Peter's KS-480 list: identity/approval design. |
| KS-580 | Medium | Todo | kamil | Append-only recovery audit held outside the estate being recovered | Carried from Peter's KS-480 list: audit-store architecture. |
| KS-581 | Medium | Todo | kamil | register-connector: volume alerting, rate limit, and correlation of refused re-key attempts | Carried from Peter's KS-480 list: alerting/rate-limit thresholds on the highest-blast-radius admin op. |
| KS-582 | Medium | Todo | kamil | [Decision] Approval shape for bulk re-key — two approvers for a batch, one for a single-org rotation | [Decision] approval shape. |
| KS-583 | Medium | Todo | kamil | DR rehearsal: lose a key → re-key → read-back survives on pre-loss anchors → the old key is dead | DR rehearsal across environments, re-keying orgs. |
| KS-595 | Medium | Backlog | kamil | Three undeclared-verb catalogue skips cite CLOSED tickets (KS-406 / KS-421) — are the defects still live? | 'are the defects still live?' Schemathesis catalogue (Peter's harness) on a live stack. |
| KS-604 | Medium | Backlog | kamil | BM-5: System-details document for Peter & Stuart — the technical system-info doc Kam owes them | Document Kam owes Peter & Stuart; 'Kam reviews and hands it over'. |
| KS-605 | Medium | Backlog | kamil | Terminology definitions for stakeholders + lawyers — certification / verification / signing / watermarking | Terminology for lawyers; signing term 'Phil is researching'. |
| KS-606 | Medium | Backlog | peter | systemTest (Schemathesis): split scripts/run.py + scripts/runner/config.py — blocked on re-establishing the pr | Assigned to Peter: stays theirs. |
| KS-619 | Medium | Backlog | kamil | Gateway tenant resolution falls through to the caller's x-tenant-id when a token has no tenantId claim — make  | super_admin tokens carry no tenantId, so an unconditional overwrite changes super-admin behaviour; open question on the observed 404. |
| KS-621 | Medium | Backlog | kamil | Document reads are scoped by tenant and owner, never by organization — cross-org protection is emergent, not e | Tracking ticket, 'deliberately NOT a fix spec'. |
| KS-625 | Medium | Backlog | kamil | /presentations/verify reports a presentation verified without checking the holder signature — challenge/domain | 'The by-design-or-remediate ruling is Kam's'. |
| KS-627 | Medium | Backlog | kamil | Implement real wallet signature verification (CIP-8/COSE + address binding) — needs the COSE key back in the r | Breaking request-contract change + new crypto deps + real wallet vectors. |
| KS-629 | Medium | Backlog | kamil | kyc `livenessVideo` is accepted by spec and runtime, then silently discarded — no code path reads it | 'Decide which half is right'. |
| KS-630 | Medium | Backlog | kamil | Wire the status-page XSS probe into preflight (or decide not to) — it runs today only by hand | 'Wire it in … (or decide not to)'. |
| KS-651 | Medium | Backlog | kamil | [Decision] @secuura/shared is imported by 24 services and declared by 2 — the symlink pattern is invisible to  | [Decision]. |
| KS-686 | Medium | Backlog | peter | not_a_server_error flags the by-design 501 on POST /api/wallets/verify — needs the integration_5xx_guard treat | Assigned to Peter: stays theirs. |
| KS-699 | Medium | Backlog | kamil | No table references `users`: 0 of the database's 29 foreign keys point at it, across 52 user-reference columns | Foreign-key design across 52 columns. |
| KS-738 | Medium | Todo | kamil | schemathesis run.py bootstrap can os.execv-loop forever on a symlinked venv — silent, 100% CPU, indistinguisha | run.py pre-venv bootstrap: KS-606 (Peter) records that block's ordering as load-bearing. |
| KS-746 | Medium | Backlog | kamil | Security events carry no tenant at all — KS-743 had to gate them platform-only, which is a workaround for the  | Security-event tenancy data model. |
| KS-752 | Medium | Backlog | kamil | Schemathesis baseline gate is unreachable: run.py skips it whenever the sweep fails — i.e. on every run it exi | 'Peter's triage input wanted on priority'; schemathesis run.py gate semantics. |
| KS-758 | Medium | Backlog | kamil | Connector erasure: three permanent failures present as retryable and nothing dead-letters; the unresolvable pa | Retry/dead-letter contract with Platform S (Peter F6/F9). |
| KS-760 | Medium | Backlog | kamil | The GitHub integration walks Linear tickets on branch names and PR bodies — 4 unrequested state changes in one | GitHub↔Linear integration settings. |
| KS-761 | Medium | Backlog | kamil | similarity-undiscriminating FP entries have no staleness detection — a tolerance can outlive its premise and k | 'a decision in its own right' (Peter). |
| KS-765 | Medium | Backlog | kamil | Merge helper must refuse a non-read SHA and have no fallback that re-derives its own expectation — the #774 ga | Merge helper is coordinator/fleet tooling outside this repo. |
| KS-767 | Medium | Backlog | kamil | Decide the 17 baseline entries that carry no `expires` — permanent acceptance, or dated exception? | 'each one is a decision nobody has made explicitly'. |
| KS-782 | Medium | Backlog | kamil | [Decision] OAuth consent: a proper two-step MFA challenge on /api/oauth/authorize (the design half of KS-781) | [Decision] product design of a two-step OAuth MFA challenge. |
| KS-783 | Medium | Backlog | kamil | A platform admin who loses their TOTP device has no self-service recovery — TOTP-only branch, no backup codes | Platform-admin TOTP recovery design. |
| KS-789 | Medium | Backlog | kamil | CONTRIBUTING.md justifies the hook's degradation and its --no-verify bypass with "CI is the hard gate" — there | Replacement text must state what catches a bypassed push: merge/push policy. Peter's #959 also edits CONTRIBUTING.md. |
| KS-807 | Medium | Backlog | kamil | The control-byte guard cannot see a raw body — findNulBytePath returns null for every Buffer, and the doc clai | 'This ticket asks a question rather than answering it'. |
| KS-808 | Medium | Backlog | kamil | run-migrations.sh exits 0 even when a migration failed, and applied=N counts skips — the summary line cannot b | '(1) and (2) are a design decision with a written rationale' (item 3 is a trivial comment fix). |
| KS-809 | Medium | Backlog | kamil | A platform admin who loses their TOTP device cannot log in — platform_admins has no backup-code column at all | Platform-admin backup-code schema design. |
| KS-826 | Medium | Backlog | kamil | A red with no reader: originate's ks444 webhook-guard suite fails at both SHAs, and no gate ever runs the four | 'Own it or gate it': gate policy (same family as KS-1051). |
| KS-829 | Medium | Backlog | kamil | Audit gate baseline data model: an unvalidated `scope` lets a GREEN root gate advertise a row leg 7 still need | Audit baseline data-model semantics; fix shapes are the tester's hypotheses; #941 is reshaping the allow-list source. |
| KS-836 | Medium | Backlog | kamil | Publish a `request:` block for POST /api/oauth/token — the endpoint's shape is asserted nowhere, and adding it | Adding the request block 'changes what Schemathesis generates against a live auth endpoint'; the reason it was held 'still holds'. |
| KS-839 | Medium | Backlog | kamil | Security: an allowedScopes of ['*'] bypasses the invalid_scope refusal entirely — validateScopes returns the r | Whether a wildcard allowedScopes is legitimate is a product/security call. |
| KS-851 | Medium | Backlog | kamil | KS-386 residues from the round-2 gate: G-1 column ordinal drift, G-2 the second-image orphan, G-3 the in-memor | 'G-1 and G-4 are decisions as much as fixes; G-2 is the only one with real design weight'. |
| KS-890 | Medium | Backlog | kamil | Runbook: a code-first deploy leg must use `docker compose up -d --no-deps <svc>` and start `migrations` explic | Demo deploy runbook. |
| KS-910 | Medium | Backlog | kamil | Preflight leg 12 executes ZERO suite cells — it is a reachability check, so with Actions retired no shell suit | Running suites on push is gate policy / time budget. |
| KS-915 | Medium | Backlog | — | A clean stack has no supported way to obtain its first privileged account | Bootstrap of the first privileged account: design. |
| KS-919 | Medium | Backlog | — | Demo platform-admin account has mfa_enabled = false — deliberate demo posture, or a gap that outlived KS-737? | 'decision needed, not a fix': demo platform-admin MFA posture. |
| KS-925 | Medium | Backlog | kamil | Launcher boot step tells every agent session to POST /api/seen as EXTRANET_ME=kam, which clears Kam's own unre | Launcher boot step (by-hash launcher, outside git). |
| KS-940 | Medium | Backlog | kamil | Launcher suite: four side-effect and guarded-surface gaps from the KS-911/912 gate (incl. a SILENT destructive | Launcher suite (by-hash launcher). |
| KS-956 | Medium | Backlog | — | KS-930 residue: a whole app tree copied into a stage that names no JS runtime is still exempt — and the gate's | Fix shape withdrawn; needs a decision on numbers. |
| KS-960 | Medium | Backlog | — | Two schema sources disagree on whether users.email is unique — a statement valid against one is 42P10 against  | 'DO NOT RECONCILE THESE TWO FILES YET: nobody has established which source is authoritative'. |
| KS-964 | Medium | Backlog | — | 104 flat spec files in Blockchain/Dev/tests are in no runner's path — quarantine and find out, do not delete | 'Is anything running these: a person, a habit, a README?' needs people. |
| KS-972 | Medium | Backlog | kamil | start-secuura.sh banner prints admin@secuura.com / admin123, which has returned 401 since PR #888 | Named in Peter's open draft PR #959 (KS-1096 branch edits Start_Up/start-secuura.sh). |
| KS-986 | Medium | Backlog | — | The published admin credential survives in USER_TESTING docs while nothing on the demo seeds it any more — and | Restoring seeding 'suspends that account': credential/seed posture on the demo. |
| KS-1003 | Medium | Backlog | — | The OAuth token endpoint is outside the credential-stuffing rate-limit zone — /api/oauth/ is not keyed in $sec | nginx-demo.conf rate-limit zone: demo-affecting config; 'check all three before changing one'. |
| KS-1010 | Medium | Backlog | — | e2e: "CIP-30 API availability check" calls a route that does not exist, and its assertion passes on the 404 | 'OPEN QUESTION: do not change any route until this is answered'. |
| KS-1018 | Medium | Backlog | — | Security/correctness: three verification-store reads swallow EVERY DB error with a bare `catch { }` and answer | 'Decide deliberately whether the in-memory fallback should exist at all'. |
| KS-1022 | Medium | Backlog | — | CLASS: the id-format contract seam — 79 of 83 path params are untyped and ~15 siblings answer 404 for a malfor | Class-level structural guard design. |
| KS-1023 | Medium | Backlog | — | Substrate: data_subject_requests is defined in THREE files that disagreed about processed_by's foreign key — a | 'Filed rather than fixed, deliberately': open schema question. |
| KS-1042 | Medium | Backlog | peter | systemTest: no regression covers the KS-742 api-key tenancy class — and four authorization tests assert nothin | Assigned to Peter: stays theirs. |
| KS-1043 | Medium | In Review | kamil | PR #811 has no ticket — the PR-status document is a point-in-time snapshot that has gone stale; re-measure or  | PR #811 is Kam's facts-only answer to Peter; 're-measure or archive before merge' is Kam's call. |
| KS-1048 | Medium | Backlog | kamil | CLAUDE.md's "rebuild local after any merge to develop" needs its written exception — a merge with zero buildab | Wording of a CLAUDE.md rule Kam owns. |
| KS-1049 | Medium | Backlog | kamil | A PR's Test Evidence must state whether the preflight RAN — the hook skips systemTest/docs/vault-only pushes a | Test Evidence rule change ('Peter reads PRs personally'): process text. |
| KS-1063 | Medium | Backlog | — | A gate that examined NOTHING exits 0 — check-package-format reports "0 packages checked, 4 skipped" as a pass, | 'the design question comes first … that is what wants deciding'. |
| KS-1079 | Medium | Backlog | — | kintsugi lost demo-service to the KS-641 fail-closed gate — the flag is unset on BOTH boxes and enabling it is | 'a one-line decision with no owner': kintsugi demo-service flag. |
| KS-1085 | Medium | Backlog | kamil | Launcher preflight: four findings — a concurrent seat clobbers the warnings file, KS-907 miscounts sessions, F | Launcher (by-hash). |
| KS-1091 | Medium | Backlog | kamil | KS-1041 residual: the cross-tenant JWT probe on originate's direct path — reasoned, never run, not commissione | 'not commissioned and not ruled'. |
| KS-1096 | Medium | In Progress | peter | start-secuura.sh's health wait, --status and DB/Redis checks probe slot 1's container names on every slot — fa | Assigned to Peter: stays theirs. |
| KS-1102 | Medium | Backlog | kamil | Unauthenticated /system/status, /api/system/status and /api/system/health/dashboard publish internal service U | 'gate these routes behind admin auth, or serve a public variant' while keeping /status/ working, measured on internet-reachable kintsugi: an owner choice. |
| KS-339 | Low | Backlog | kamil | Grant Phil + Steve extranet access (evolve toward company source of truth) | Extranet access grants (other project; passcodes). |
| KS-648 | Low | Backlog | kamil | Frontend CSP quality: issuer alone carries 'unsafe-eval', and all three portals allow 'unsafe-inline' styles | CSP tightening may break portal libraries (issuer 'unsafe-eval'); owner judgement on residual risk. |
| KS-748 | Low | Backlog | kamil | svc_api_keys.organization_id is not a tenancy boundary and nothing keeps it coherent with tenant_id — an incoh | Integrity model for svc_api_keys organization_id vs tenant_id. |
| KS-834 | Low | Backlog | kamil | [Decision] POST /api/certifications/:id/verify has no auth handler — leave it public, or gate it? | [Decision] addressed to Kam. |
| KS-840 | Low | Backlog | kamil | The OAuth error code travels in error.message and the contract never says so; and authorize refusals answer JS | OAuth error-envelope contract change (RFC redirect vs JSON). |
| KS-846 | Low | Backlog | kamil | `@secuura/shared` `main` points at an untracked, never-built `dist/index.js` — anything outside vitest's alias | Build/dist of @secuura/shared depends on the KS-651 [Decision] on the symlink pattern. |
| KS-980 | Low | Backlog | — | The KS-597 integration suite claims two RLS-permissive paths and exercises one — platform_bypass never reaches | 'Fix-shape: a decision, not just an edit' (possibly a new connection role). |
| KS-1082 | Low | Backlog | kamil | The Playwright env guard added in #896 reads config/ only — the variable breaking the CI run is read from fixt | 'Two questions for Peter'. |
| KS-1088 | Low | Backlog | kamil | run-shell-suites.sh restores git discovery but does not isolate suites: a suite that runs git from its cwd wri | 'Decide whether the runner should enforce isolation'. |
| KS-1097 | Low | Backlog | kamil | Merge-rule docs after #957: the v4 footer and two gate statements gloss TESTED weakly, 'the reviewer' has no r | Merge-rule docs (DEV-PROCESS/CLAUDE/CONTRIBUTING): Kam's rule text. |
| KS-984 | No priority | Backlog | peter | No service exposes /metrics — the secuura-services scrape job has never collected a single series on any slot | Assigned to Peter: stays theirs. |
| KS-985 | No priority | Backlog | peter | Eight dashboards show a slot picker that filters nothing — latent today, wrong the day /metrics lands | Assigned to Peter: stays theirs. |
| KS-1083 | No priority | Backlog | kamil | GATEWAY_VOUCH_SECRET: nothing provisions it and no deploy order or rotation is written — #951's control ships  | Secret provisioning, deploy order and rotation. |

### C — blocked, parked, not yet possible, or claimed without a PR

| id | P | state | assignee | title | blocker |
|---|---|---|---|---|---|
| KS-1057 | Urgent | In Review | kamil | api-gateway verify is presence-keyed: confidence reads txHash && blockHeight and never blockchain.status, so a | Fix merged as #935 (2026-09-10, GitHub API); ticket In Review awaiting QA/close. No code work. |
| KS-365 | High | Blocked | kamil | Base-image refresh routine + track postgres CVE-2025-68121 (redis leg already done in triage) | State Blocked (postgres CVE tracking on a base-image routine). |
| KS-565 | High | Backlog | kamil | Sweeps 2026-08-05: untracked failures across 10 ops — response-schema recurrence (KS-498 residual), 3 genuine  | Umbrella over a past sweep; needs a fresh sweep and per-op triage, not a bounded fix. |
| KS-576 | High | Todo | kamil | Bulk re-key: one admin-authorised rotate across a named set of externalRefs | 'It must not ship before KS-577', and KS-577 is in open PR #880. |
| KS-591 | High | Backlog | kamil | positive_data_acceptance recurs at scale — 734 failures across 64 ops (KS-255 / KS-515 recurrence, full-2026-0 | Umbrella recurrence (734 failures / 64 ops); needs a fresh sweep and per-op triage. |
| KS-593 | High | Backlog | kamil | not_a_server_error recurs — 17 raw 5xx across 8 ops (KS-431 / KS-449 / KS-497 recurrence, full-2026-08-07 swee | Umbrella recurrence (17 raw 5xx / 8 ops); needs a fresh sweep and per-op triage. |
| KS-664 | High | In Progress | kamil | deepmerge-ts GHSA-ggr8-5vv4-36mx (high) — override to 8.0.1 in originate; hoisted root lock baselined to 2026- | In Progress, waiting on a Prisma release that pulls deepmerge-ts 8.x. |
| KS-665 | High | In Progress | kamil | KS-256 review follow-ups: 5 example-fixable 400s, the tsx transpile-only spec-gate trap (§10), and a new `user | State 'In Progress' with no open kksecura PR naming it: claimed by a seat; do not start without the owner. |
| KS-669 | High | In Progress | kamil | Published spec points integrators at 18 URLs on domains we do not own (one is for sale) — E1 only inspects ema | State 'In Progress' with no open kksecura PR naming it: claimed by a seat; do not start without the owner. |
| KS-695 | High | In Progress | kamil | S↔K (K-side): erasure by external_ref, documents.title coverage, and connector-scoped org erasure — PS-690 dep | State 'In Progress' with no open kksecura PR naming it: claimed by a seat; do not start without the owner. |
| KS-698 | High | In Progress | kamil | Security: one request permanently poisons any rate-limit key — unbounded windowMs persists an invalid resetAt, | State 'In Progress' with no open kksecura PR naming it: claimed by a seat; do not start without the owner. |
| KS-729 | High | In Progress | kamil | Upgrade ip-address off GHSA-mwp4-54f8-5fhr (high, SSRF) — express-rate-limit 8.4.1→8.5.1+ in mcp-server, @mesh | State 'In Progress' with no open kksecura PR naming it: claimed by a seat; do not start without the owner. |
| KS-731 | High | In Progress | kamil | Local slots share one Postgres/Redis credential pair — any slot can read, write and DROP another slot's databa | State 'In Progress' with no open kksecura PR naming it: claimed by a seat; do not start without the owner. |
| KS-754 | High | In Review | kamil | updateDSRStatus silently no-ops for any non-uuid actor — step 12 never marks a connector erasure completed | Fix PR #914 merged 2026-09-09 (GitHub API); In Review awaiting close. |
| KS-762 | High | Blocked | kamil | APP_DB_PASSWORD is a committed literal :- default in docker-compose.yml — 51 sites, not the ~20 the register r | State Blocked. |
| KS-763 | High | In Review | kamil | Push preflight blocks the whole repo — two qs advisories (GHSA-4mjr / GHSA-x5fp) unbaselined across 27 standal | In Review with no open PR; KS-763 work merged in #796 (GitHub API). |
| KS-768 | High | Backlog | kamil | audit-locks scans 35 of 45 lockfiles — 3 vulnerable locks have coverage from neither gate | Comment 2026-09-03: 'Delivered in PR #796' (merged per GitHub API); verify and close. |
| KS-790 | High | In Review | kamil | OAuth authorization_code token exchange uses getUserById (post-auth) in a pre-auth flow — 400 'User not found' | State 'In Review' with no open kksecura PR naming it: claimed by a seat; do not start without the owner. |
| KS-796 | High | In Progress | kamil | KS-781 door 3: POST /api/auth/wallet/verify mints a full token pair without MFA, lockout or status | State 'In Progress' with no open kksecura PR naming it: claimed by a seat; do not start without the owner. |
| KS-800 | High | In Review | kamil | CLASS: a body parser mounted AFTER the control-byte guard is unguarded — 3 route-scoped sites in the gateway ( | State 'In Review' with no open kksecura PR naming it: claimed by a seat; do not start without the owner. |
| KS-801 | High | In Progress | kamil | Security: four gateway path predicates are case-sensitive while Express routing is not — `/API/...` skips medi | State 'In Progress' with no open kksecura PR naming it: claimed by a seat; do not start without the owner. |
| KS-806 | High | In Progress | kamil | Security: the synthetic wallet email buckets on walletAddress.slice(0,8) — degenerate for every addr_test1…/st | State 'In Progress' with no open kksecura PR naming it: claimed by a seat; do not start without the owner. |
| KS-949 | High | In Progress | kamil | The seeded platform admin carries a real person's identity and a published default password — and the *123 lin | State 'In Progress' with no open kksecura PR naming it: claimed by a seat; do not start without the owner. |
| KS-962 | High | Backlog | — | The api-gateway user seed throws 42P10 on every boot and has never seeded anything — remove its INSERT, do NOT | Peter noted PR #928 (open) attempted this ground; fix constrained by Kam's `split` ruling. Wait for #928. |
| KS-966 | High | In Progress | — | Retire the published SYSTEM_ADMIN credential (Kam: rotate-properly) — a deletion, not a rotation: no new share | State 'In Progress' with no open kksecura PR naming it: claimed by a seat; do not start without the owner. |
| KS-981 | High | Backlog | — | The round-4 quarantine call throws out of a "Never throws" function, and the strict arm quarantines in silence | pre-suite.ts catch path; KS-969 (In Progress) holds the path. |
| KS-982 | High | Backlog | — | pre_suite.test.sh silently quarantines a developer's live manifest and reports 24 passed, 0 failed | pre_suite.test.sh is in open PR #927; KS-969 in flight. |
| KS-994 | High | Backlog | kamil | `withGeneratedActors()` iterates the WRAPPER, not the environments — the k6 harness has NEVER used generated a | Same defect as KS-1026, which is in open PR #916. |
| KS-174 | Medium | In Progress | — | KS-160 Step 3: set tenant GUC on checkout + admin-role exemption for cross-tenant reads + flip fail-closed (at | State 'In Progress' with no open kksecura PR naming it: claimed by a seat; do not start without the owner. |
| KS-562 | Medium | Backlog | kamil | anchoring threadTokenMint test fails only under root-visible npm install layout — nested @lucid-evolution/plut | Layout-dependent pre-existing failure; investigation, no fix shape. |
| KS-711 | Medium | Todo | kamil | systemTest/akto + systemTest/performance quality gates went red again on docs/quick_start.md — the KS-702/KS-7 | Target files were renamed to quick-start.md by 5a66ea764 (KS-682) and its only PR #758 closed unmerged; re-measure before any work. |
| KS-757 | Medium | Backlog | kamil | Connector erasure re-drive is unbounded against concurrency — and all three prescribed fixes are blocked (QA F | 'all three prescribed fixes are blocked'. |
| KS-777 | Medium | Todo | kamil | QA pass F-1/F-3/F-4/F-7: two vacuous guards, an unasserted statement tail, and an un-normalised org comparison | Retroactive tracker; 'All four are FIXED on #795': nothing to build. |
| KS-802 | Medium | In Progress | kamil | KS-781 test-quality follow-ups from re-gate (4): restore the allow-set bound, put the revert pin on a real req | State 'In Progress' with no open kksecura PR naming it: claimed by a seat; do not start without the owner. |
| KS-813 | Medium | Backlog | kamil | "PREFLIGHT PASSED" is unconditional — step() only prints a banner, and skipped legs read as passes | Same defect as KS-1046, which is in open PR #925. |
| KS-837 | Medium | Backlog | kamil | Published prose drifts from the routes it describes and nothing detects it — the phrase check, the marker conv | Wednesday ruled 'DO NOT BUILD IT NOW' (2026-09-05). |
| KS-843 | Medium | In Progress | kamil | KS-695 F5: build the dedicated `subjects:erase` scope gate on POST /api/gdpr/erasures — Kam ruled it 2026-09-0 | State 'In Progress' with no open kksecura PR naming it: claimed by a seat; do not start without the owner. |
| KS-866 | Medium | Backlog | kamil | Merge protocol: the server-side `sha=` pin protects the PR head, not the base — a 9-second race merged onto an | Record ticket; 'the fix is already ruled and in force'. |
| KS-908 | Medium | Backlog | — | connectorId persists but is invisible through the API — POST and GET both return null while the row holds the  | Depends on KS-869 (Blocked; cited in open PR #880). |
| KS-920 | Medium | In Progress | kamil | `/shared` ships the TypeScript compiler and a 267 MB dev tree into all 24 runtime images — KS-490 closed the s | State 'In Progress' with no open kksecura PR naming it: claimed by a seat; do not start without the owner. |
| KS-946 | Medium | In Review | kamil | Four path spellings dodge EVERY path-scoped gateway limiter — a CLASS across all eight mounts; first act is th | State 'In Review' with no open kksecura PR naming it: claimed by a seat; do not start without the owner. |
| KS-957 | Medium | Backlog | — | KS-930 round-2 gate residue: the guard and its suite write three claims that are false and cannot notice — a c | Re-link guard claims; the same guard is in open PR #879 and KS-930 is in flight. |
| KS-959 | Medium | Backlog | — | KS-597 fallback: resolve the issuer org from the authenticated caller org context — BLOCKED, organization_memb | 'cannot be built today, and the blocker is data': organization_members has 0 rows. |
| KS-969 | Medium | In Progress | kamil | systemTest actor/credential path: provisioning is never invoked, so the generated-actor path never resolves —  | State 'In Progress' with no open kksecura PR naming it: claimed by a seat; do not start without the owner. |
| KS-973 | Medium | Todo | kamil | KS-969 round-1 gate residue: the pre-suite step and its own test suite — six items on one path | KS-969 residue; KS-969 is In Progress. |
| KS-990 | Medium | Backlog | kamil | `npm run quality` cannot pass in systemTest/performance or systemTest/akto — two pre-existing reds unrelated t | Performance half = runner/actor_manifest.ts:140 TS2540, a file changed by open PR #916; touches systemTest/performance/runner/. |
| KS-1011 | Medium | Backlog | — | KS-666 stack marker reads "unknown" for owner/branch/commit/started_at whenever the stack is not started via s | Stack labels resolved by docker-compose.local.yml + the start script; overlaps Peter's #959 (Start_Up/start-secuura.sh). |
| KS-1014 | Medium | Backlog | — | Eight containers ran images their own tag no longer pointed at — "the stack is up" says nothing about what it  | Observation, no fix named; investigation only. |
| KS-1015 | Medium | Backlog | kamil | Sweeps 2026-09-08: 28 check/operation pairs have no live owner — 18 untriaged (the /api/auth/ + /mfa/ surface  | Umbrella (28 check/op pairs) needing per-pair triage on a sweep. |
| KS-1021 | Medium | Backlog | — | Deploy path: the local api-gateway serves the correct spec BY ACCIDENT over a DEAD bind mount — a restart woul | Local environment state (dead bind mount), not a code fix. |
| KS-749 | Low | Backlog | kamil | postcss-selector-parser 6.1.2 carries GHSA-w9m9-85wc-3x92 — baselined to unblock the preflight; the override w | Override proved inert; real fix needs an upstream tailwind/postcss path; baselined meanwhile. |
| KS-793 | Low | Backlog | kamil | BACKLOG.md:7 claims 2 of 27 auth test files fail at import — they do not on develop | Done-means requires a reproduction on a second machine. |
| KS-965 | Low | Backlog | — | 87 documentary sites still publish the retired admin credential — wrong rather than dangerous, clean up after  | Cleanup to follow KS-966 (In Progress). |
| KS-1093 | No priority | Backlog | — | check-stack-safety.sh 6f reports a FALSE red once a real Playwright run exists — git check-ignore refuses a pa | check-stack-safety.sh §6f; the file is in Peter's open draft #959; fix shape not chosen. |

### D — an open kksecura PR on develop names the id (PR, head SHA, Test Evidence heading)

| id | P | state | title | named in title | named in body only |
|---|---|---|---|---|---|
| KS-963 | Urgent | In Review | PII_PLAINTEXT_CUTOFF silently disables the auth remediation on prod-like boxes — decryptEmail throws | #913 `fdd8af79d` TE:yes | #930 `7e5ae31d8` TE:yes |
| KS-1059 | Urgent | In Review | anchorStateSync.ts:360 — removing `inFlight &&` from the KS-587 sim leg reddens 0 cells, on a line # | #937 `cf8b23366` TE:yes | — |
| KS-1078 | Urgent | In Review | SUPPLY CHAIN: the Code Security Gates job downloads an UNPINNED package from npm and executes it mid | #942 `c1676269d` TE:yes | — |
| KS-256 | High | In Progress | Add OpenAPI inline examples to all 329 operations — eliminate coverage-phase no-test-cases skips | — | #922 `2b5075e9f` TE:yes, #873 `7d8a3f0e4` TE:yes |
| KS-487 | High | In Progress | Review B — Input validation, injection, upload, XSS/SSRF & crypto | #720 `fcc611d29` TE:yes | — |
| KS-577 | High | In Review | rotate: true mints a new key but never revokes the old one — implement revoke-on-rotate and agree th | #880 `85f8263c2` TE:yes | — |
| KS-601 | High | In Progress | [Infra] New Platform K dev server "Kintsugi" — restore dev/demo split | #943 `4e1bd16ec` TE:yes | — |
| KS-643 | High | In Review | Security: DELETE /api/keys/:id revokes any tenant's key — no ownership check | — | #799 `38f6377b9` TE:yes |
| KS-663 | High | In Review | The OpenAPI spec is now a consumed contract, but nothing in CI stops it drifting — plus two known sp | — | #813 `54225cbbd` TE:yes |
| KS-693 | High | In Review | M365 routes answer 503 when ENTRA_* is unconfigured — 9 permanent Schemathesis failures on every dev | #809 `aa2270fe1` TE:yes | — |
| KS-734 | High | In Review | The e2e Playwright suite cannot run from a clean checkout — tests/e2e is not a workspace member and  | #920 `2112a99e3` TE:yes | — |
| KS-739 | High | In Review | transfer-custody maps a 401/403 from users/lookup to 502 BAD_GATEWAY — the KS-536 4xx rule was appli | #919 `d0aff46d4` TE:yes | — |
| KS-764 | High | In Progress | Security: decideKeyRevoke has no organisation arm — an ORG_ADMIN can revoke a sibling organisation's | #799 `38f6377b9` TE:yes | — |
| KS-771 | High | In Progress | Review stream: build, supply chain and release gates | — | #918 `ed954f09e` TE:yes |
| KS-798 | High | In Progress | The consent page posts the redirect URI in the client_id field — nobody can complete the OAuth flow  | #881 `787771b97` TE:yes | — |
| KS-804 | High | In Review | Security: POST /api/oauth/authorize's resolver carries ONE of the GET path's FOUR app rules — PKCE i | — | #881 `787771b97` TE:yes |
| KS-841 | High | In Progress | Security: the rendered OAuth consent page cannot POST itself back — it emits the redirect URI as cli | #881 `787771b97` TE:yes | — |
| KS-869 | High | Blocked | connectorId is never persisted — svc_api_keys.connector_id is written by nothing and read by nothing | — | #880 `85f8263c2` TE:yes |
| KS-926 | High | In Progress | 17 of 20 `check-*.sh` guards run from NO live entry point — including SQL-injection and trust-header | #918 `ed954f09e` TE:yes, #874 `6f7885602` TE:yes | #879 `79f1fcb48` TE:yes |
| KS-927 | High | In Review | ks444-webhooks-create-description-guard: 2 of 4 cells RED on develop — the mock omits assertSafeOutb | #926 `542492c41` TE:yes | #939 `481e0267f` TE:yes, #931 `f2e0cb3c1` TE:yes, #874 `6f7885602` TE:yes |
| KS-937 | High | In Progress | KS-921 residue: the re-link guard's awk parser is still case-sensitive — a lowercase `copy --from=bu | — | #874 `6f7885602` TE:yes |
| KS-945 | High | In Review | The install detector enumerates verbs and so fails OPEN — `npm add`, `npm it`, bare `yarn` and `pnpm | #879 `79f1fcb48` TE:yes | — |
| KS-950 | High | In Review | The boot seed dies permanently at boot 2 — migration 030 drops the UNIQUE its ON CONFLICT targets, a | #928 `e28d64b8d` TE:yes | — |
| KS-968 | High | In Progress | MAJOR: when both platform-admin rows exist the id-row rewrite throws 23505, the seed loop swallows i | #905 `c38040bd1` TE:yes | — |
| KS-991 | High | In Progress | A stale LOCAL `develop` runs the full platform preflight on an unrelated branch, which then fails on | #903 `a70f92d7c` TE:yes | #905 `c38040bd1` TE:yes |
| KS-993 | High | In Progress | Nothing type-checks systemTest/fixtures/ — the TypeScript that runs every suite's provisioning is co | #916 `584b12ba1` TE:yes | — |
| KS-1004 | High | In Progress | A document with a txHash can never be marked anchor-failed — NOR healed forward to confirmed; both g | #912 `ae8751f38` TE:yes | — |
| KS-1026 | High | In Progress | withGeneratedActors is a NO-OP for every consumer — the k6 suite has been running on secrets.yml cre | #916 `584b12ba1` TE:yes | — |
| KS-1032 | High | Backlog | Security: 9 trust-header reads outside auth middleware (pen-test F-04) — surfaced by wiring check-no | — | #918 `ed954f09e` TE:yes |
| KS-1038 | High | Backlog | tests/e2e auth-exhaustive races its OWN lockout — same commit gives 1 or 11 failures, so the suite c | — | #920 `2112a99e3` TE:yes |
| KS-1046 | High | In Review | `PREFLIGHT PASSED.` is printed identically whether 13 legs ran or 10 — the verdict has no skip tally | #925 `8a5aff863` TE:yes | #941 `d105e07a8` TE:yes, #940 `1aa708be9` TE:yes, #939 `481e0267f` TE:yes, #928 `e28d64b8d` TE:yes |
| KS-1051 | High | Backlog | develop is RED on the services/originate jest suite and NOTHING catches it — the suite is a blocking | — | #931 `f2e0cb3c1` TE:yes |
| KS-1052 | High | In Progress | CLASS: 21 of 24 updateUser callers discard the return — a backup-code login burns nothing and still  | #930 `7e5ae31d8` TE:yes | — |
| KS-1055 | High | Backlog | Per-tenant databases never receive the file migrations — CORE_MIGRATIONS FORCEs RLS with ZERO polici | — | #932 `c72607d58` TE:yes |
| KS-1062 | High | In Review | F-928-4: the tenant-migration counter cannot report a failure — a tenant whose database does not exi | #932 `c72607d58` TE:yes | — |
| KS-1075 | High | In Progress | CI gates: both PR security gates fail for CONFIG reasons, not findings — tsx driver missing, an EMPT | #940 `1aa708be9` TE:yes | #942 `c1676269d` TE:yes, #941 `d105e07a8` TE:yes |
| KS-1077 | High | In Progress | Two npm-audit allow-lists disagree: CI's is EMPTY and cannot express an advisory-less carrier packag | #941 `d105e07a8` TE:yes | — |
| KS-1099 | High | In Progress | A malformed k6 YAML config prints secrets-file lines to stderr: cli.ts:180 calls loadSecrets() at to | #960 `0e70ed1c7` TE:yes | — |
| KS-650 | Medium | Backlog | services/originate: POST /api/webhooks 500s on its two success-path tests — ks444 suite red on devel | — | #799 `38f6377b9` TE:yes |
| KS-657 | Medium | In Review | services/shared (@secuura/service-utils) cannot build — no tsconfig.json, so main/types point at a d | — | #720 `fcc611d29` TE:yes |
| KS-658 | Medium | Backlog | The demo VM runs every service as NODE_ENV=development while the code names "demo" as prod-like — ~6 | — | #720 `fcc611d29` TE:yes |
| KS-679 | Medium | In Review | Published Anchor.id is anc_… but anchoring only ever mints anchor_<uuid> — format-false, live on dev | #922 `2b5075e9f` TE:yes | — |
| KS-726 | Medium | In Review | Write-ahead the Cardano tx hash: persist the deterministic hash BEFORE submitting, so a lost submit  | #805 `97e2161fa` TE:yes | — |
| KS-736 | Medium | In Review | Gateway mount-auth check scores authenticateToken(false) as green — six /api mounts satisfy neither  | #923 `d127dc7d4` TE:yes | — |
| KS-773 | Medium | In Review | lockfile-cleanroom skips services/mcp-server for a reason its lock refutes — leg 2/9 claims "all loc | #924 `b85f1db24` TE:yes | #928 `e28d64b8d` TE:yes, #925 `8a5aff863` TE:yes |
| KS-780 | Medium | Todo | Two implementations of organisation-id normalisation, in two layers — move normaliseOrgId into @secu | — | #799 `38f6377b9` TE:yes |
| KS-791 | Medium | In Review | Publish verify-file (v1+v2) in the spec — coupled with the gateway 415 fix, since octet-stream is re | #813 `54225cbbd` TE:yes | — |
| KS-794 | Medium | Backlog | verify-file returns `fileSize` on every 200 and neither response schema declares it | — | #813 `54225cbbd` TE:yes |
| KS-799 | Medium | In Review | The OAuth consent page cannot submit its own form — CSRF answers 403 before the route is reached (pr | #881 `787771b97` TE:yes | — |
| KS-911 | Medium | In Progress | KS-907 launcher residues: a sentinel comment describing a test that does not exist, and a 2>/dev/nul | — | #874 `6f7885602` TE:yes |
| KS-928 | Medium | Backlog | The demo-seed gate's predicate is tested but its CALL SITE is not — delete adminConfig.ts:1824 and e | — | #874 `6f7885602` TE:yes |
| KS-930 | Medium | In Progress | KS-921 residues: five Dockerfile shapes the re-link guard cannot read, an nginx final stage it can N | — | #879 `79f1fcb48` TE:yes, #874 `6f7885602` TE:yes |
| KS-931 | Medium | In Review | safeOutboundRequest CAN throw while its own contract says it does not — and deliverWebhook lost the  | #873 `7d8a3f0e4` TE:yes | — |
| KS-933 | Medium | Backlog | `npm run build` type-checks ZERO test files in packages/shared — the tsconfig excludes src/__tests__ | — | #874 `6f7885602` TE:yes, #873 `7d8a3f0e4` TE:yes |
| KS-948 | Medium | Backlog | A backtick in a shell-suite case name executes as a command and rewrote package.json mid-run — every | — | #879 `79f1fcb48` TE:yes |
| KS-961 | Medium | In Review | The aggregate workspace suite never runs on a PR — wire it advisory (Kam: wire-nonblocking), and it  | #887 `cb7a3e3be` TE:yes | — |
| KS-992 | Medium | In Review | Both quarantine guards `rm -rf` the directory they may have failed to snapshot — an unchecked `cp` b | — | #927 `1041d2d32` TE:yes |
| KS-1017 | Medium | Backlog | Test-estate CLASS: a fixture that cannot discriminate certifies the bug — unmintable values, and fix | — | #912 `ae8751f38` TE:yes |
| KS-1019 | Medium | Backlog | [Question] The document's whole `blockchain` block is published as z.unknown() — undeclared to integ | — | #912 `ae8751f38` TE:yes |
| KS-1027 | Medium | In Review | KS-992 follow-ups from Peter's #904 review: restore()'s own cp is still unchecked, the refusal path  | #927 `1041d2d32` TE:yes | — |
| KS-1033 | Medium | Backlog | KS-926 residue: the three guards that could NOT be wired, and what each needs first — a wrong diff b | — | #918 `ed954f09e` TE:yes |
| KS-1034 | Medium | Backlog | check-stack-safety.sh resolves the WRONG repo root inside a git hook and calls present files "delete | — | #918 `ed954f09e` TE:yes |
| KS-1039 | Medium | Backlog | tests/e2e 2.4.6 'SQL injection in registration name is sanitized' asserts against an ECHO — a perman | — | #920 `2112a99e3` TE:yes |
| KS-1040 | Medium | Backlog | Push preflight leg 4 reports 'a published path is unroutable' when the real cause is an exhausted lo | — | #920 `2112a99e3` TE:yes |
| KS-1050 | Medium | Backlog | users.ts:933 answers success: true over a 0-row profile update — KS-943 changes the symptom from sta | — | #930 `7e5ae31d8` TE:yes |
| KS-1061 | Medium | In Review | F-926-2: all ten originate @secuura/shared mock factories were partial — build them from the real ex | #931 `f2e0cb3c1` TE:yes | — |
| KS-1068 | Medium | In Review | threadToken/confidence are written onto the blockchain blob with `as any` and are absent from its ty | #939 `481e0267f` TE:yes | — |
| KS-1074 | Medium | Backlog | The poller/reconcile blob writers also erase threadToken — on the CONFIRM/heal path, not just the fa | — | #939 `481e0267f` TE:yes |
| KS-912 | Low | In Progress | KS-907 suite residues: CASE 2 never asserts the pruning it is named for, a cell count printed as a l | — | #874 `6f7885602` TE:yes |

Peter/Stuart-assigned tickets are listed under B even when a PR mentions them. Peter's own draft #959 (not kksecura) names KS-1016, KS-1096, KS-256, KS-666, KS-972.

## 6. Board account (kksecura) open PRs on base develop

Paged `pulls?state=open&base=develop&per_page=100` until a short page: 1 page, 48 open PRs total, **37 by kksecura**. 'Test Evidence' = a markdown heading matching `^#+ Test Evidence` in the body.

| # | title | head SHA | updated_at | Test Evidence |
|---|---|---|---|---|
| 960 | KS-1099: a malformed k6 YAML config no longer prints its secrets file | `0e70ed1c7` | 2026-09-12T03:25:48Z | yes |
| 943 | KS-601: kintsugi rebuild runbook — and the rollback that does not exist yet | `4e1bd16ec` | 2026-09-10T09:17:16Z | yes |
| 942 | KS-1078: the tsx probe folded stderr into its own verdict — separate the streams, and stop a security gate downloading a | `c1676269d` | 2026-09-10T01:58:17Z | yes |
| 941 | KS-1077: two npm-audit allow-lists disagreed and CI's was empty — make the GHSA-keyed baseline the single source | `d105e07a8` | 2026-09-10T01:51:19Z | yes |
| 940 | KS-1075: the audit-contract gate exits 1 printing NOTHING — take it off `bash -e` so it can report its reason | `1aa708be9` | 2026-09-10T01:40:42Z | yes |
| 939 | KS-1068: declare threadToken/confidence/simulatedTxRef on the blockchain blob, remove the `as any` blindfold | `481e0267f` | 2026-09-10T01:05:17Z | yes |
| 937 | KS-1059: make the sim leg's inFlight guard a guard — its removal reddened 0 of 515 cells | `cf8b23366` | 2026-09-09T21:12:11Z | yes |
| 932 | KS-1062: the tenant-migration counter could not report a failure — a tenant whose database does not exist was logged as  | `c72607d58` | 2026-09-09T14:02:20Z | yes |
| 931 | KS-1061: build originate's @secuura/shared mocks from the real export list — an omitted export becomes impossible, not r | `f2e0cb3c1` | 2026-09-09T14:01:59Z | yes |
| 930 | KS-1052: a credential-lifecycle write that did not land is no longer reported as success — a backup-code login burned no | `7e5ae31d8` | 2026-09-09T14:18:15Z | yes |
| 928 | KS-950: the boot seed could never succeed after migration 030, and the loader that swallowed it reported success | `e28d64b8d` | 2026-09-09T11:51:20Z | yes |
| 927 | KS-1027: close Peter's four #904 follow-ups — the OTHER cp, the stash the refusal deleted, and the duplication nobody ha | `1041d2d32` | 2026-09-09T14:02:28Z | yes |
| 926 | KS-927: the mock omitted an export the route calls — both POSITIVE cells 500'd while the suite printed two ticks | `542492c41` | 2026-09-09T11:06:37Z | yes |
| 925 | KS-1046: the preflight verdict must not outlive its corpus — name the legs that ran | `8a5aff863` | 2026-09-09T13:17:49Z | yes |
| 924 | KS-773: the clean-room skip rested on a reason its own lock refutes — remove it and name the corpus | `b85f1db24` | 2026-09-09T14:02:26Z | yes |
| 923 | KS-736: the mount-auth check scored authenticateToken(false) as green, and could not see half its own surface | `d127dc7d4` | 2026-09-09T08:53:33Z | yes |
| 922 | KS-679: publish the anchor id shape the service actually mints | `2b5075e9f` | 2026-09-09T12:25:49Z | yes |
| 920 | KS-734: make tests/e2e runnable from a clean checkout, and baseline what it actually reports | `2112a99e3` | 2026-09-09T07:39:12Z | yes |
| 919 | KS-739: a 4xx from users/lookup is the caller's fault — stop flattening it to 502 | `d0aff46d4` | 2026-09-09T12:27:14Z | yes |
| 918 | KS-926: wire 14 of the 17 unreached guards, and add the census that fails the push when a guard is in no bucket | `ed954f09e` | 2026-09-09T08:04:45Z | yes |
| 916 | KS-993: systemTest typecheck entry point — and KS-1026, the no-op overlay it found | `584b12ba1` | 2026-09-09T02:07:22Z | yes |
| 913 | KS-963 (widened): getUserByIdPreAuth rethrows instead of reporting a DB failure as "no such user" — Kam ruled include | `fdd8af79d` | 2026-09-09T12:54:25Z | yes |
| 912 | KS-1004: a document carrying a txHash can now be marked anchor-failed (non-destructive write, guard narrowed to confirme | `ae8751f38` | 2026-09-09T13:44:00Z | yes |
| 905 | KS-968: warn, at the column, that comparing users.email to a literal is void | `c38040bd1` | 2026-09-08T13:28:36Z | yes |
| 903 | KS-991: skip a local develop that origin/develop provably supersedes | `a70f92d7c` | 2026-09-08T13:25:00Z | yes |
| 887 | KS-961: run the workspace suites on the PR, advisory and non-blocking — and they are RED on develop today | `cb7a3e3be` | 2026-09-09T11:04:41Z | yes |
| 881 | OAuth consent cluster: KS-798 (client_id) · KS-841 (PKCE guard) · KS-799 (CSRF submit) | `787771b97` | 2026-09-08T10:00:44Z | yes |
| 880 | KS-577: a rotate must retire the prior credential — revoke-on-rotate, with the cutover window as one value | `85f8263c2` | 2026-09-09T10:57:17Z | yes |
| 879 | KS-945: invert the install detector so it fails CLOSED, and stop the suite executing its own case names | `79f1fcb48` | 2026-09-09T02:07:24Z | yes |
| 874 | KS-926: state the family — ten checks that cannot fail, and the premise under each | `6f7885602` | 2026-09-06T13:31:28Z | yes |
| 873 | KS-931: make the no-throw contract true — http.request throws synchronously and the module said it does not | `7d8a3f0e4` | 2026-09-09T12:50:13Z | yes |
| 813 | KS-791: let verify-file receive a file, then publish it | `54225cbbd` | 2026-09-08T14:56:21Z | yes |
| 811 | docs: PR status for Peter, measured 2026-09-04 04:46Z — written, NOT sent | `6200833ff` | 2026-09-09T09:19:34Z | yes |
| 809 | KS-693 (interim): guard the 8 M365/OneDrive/Teams unconfigured-503 ops so the merge gate reads a real floor | `aa2270fe1` | 2026-09-04T22:52:11Z | yes |
| 805 | KS-726: write-ahead the Cardano tx hash so a lost submit reply cannot orphan a paid transaction (ported onto anchorSubmi | `97e2161fa` | 2026-09-08T12:06:12Z | yes |
| 799 | KS-764: close the second revoke surface in originate, and bind the organisation arm to its call sites | `38f6377b9` | 2026-09-10T07:22:00Z | yes |
| 720 | KS-487: restore the two webhook tests B-1/B-2 killed — and correct four stale BACKLOG rows, one a security exposure mark | `fcc611d29` | 2026-09-09T11:11:54Z | yes |

Other open PRs on develop: PeterObeden #959 (draft, KS-1096, head `c7b6a2475`, Test Evidence yes); dependabot #949, #948, #947, #946, #945, #649, #639, #635, #575, #572 (no Test Evidence).

## Appendix — every open KS issue (fields as gathered; description excerpt shown only for class A above)

| id | priority | state | assignee | labels | updatedAt | class | title |
|---|---|---|---|---|---|---|---|
| KS-441 | Urgent | Blocked | stuart.jamieson@secuura.ai | — | 2026-09-10T11:20:29Z | B | Akto CI scan throughput: ~21 s local vs ~10 min in the isolated pr-akto stack (~28×) — investigate worker starvation / run-pickup latency (KS-435 durable fix) |
| KS-608 | Urgent | Backlog | peter@obeden.com | — | 2026-09-11T13:45:09Z | B | systemTest (Integration mode): GET /api/anchors/{id} and verify must not contradict each other about the same anchor (KS-607 class) |
| KS-963 | Urgent | In Review | kamil.kreiser@secuura.ai | — | 2026-09-09T13:18:43Z | D | PII_PLAINTEXT_CUTOFF silently disables the auth remediation on prod-like boxes — decryptEmail throws, getUserById returns null, and the remediation reads it as no-such-row |
| KS-1057 | Urgent | In Review | kamil.kreiser@secuura.ai | — | 2026-09-10T06:50:52Z | C | api-gateway verify is presence-keyed: confidence reads txHash && blockHeight and never blockchain.status, so a failed anchor carrying a hash can report verified: true |
| KS-1059 | Urgent | In Review | kamil.kreiser@secuura.ai | — | 2026-09-09T21:07:28Z | D | anchorStateSync.ts:360 — removing `inFlight &&` from the KS-587 sim leg reddens 0 cells, on a line #912 made load-bearing |
| KS-1076 | Urgent | Todo | — | — | 2026-09-10T09:42:29Z | A | No Playwright e2e test has run on any PR since 2026-09-07 — the suite dies at a static lint gate before any browser opens, and the job name hides it |
| KS-1078 | Urgent | In Review | — | — | 2026-09-10T01:58:48Z | D | SUPPLY CHAIN: the Code Security Gates job downloads an UNPINNED package from npm and executes it mid-run — the job that checks for vulnerabilities |
| KS-61 | High | Todo | stuart.jamieson@secuura.ai | Bug | 2026-09-09T15:57:47Z | B | OpenAPI compliance: documentation gaps across the spec (descriptions, parameter docs, operationId) |
| KS-188 | High | Todo | stuart.jamieson@secuura.ai | Bug | 2026-09-09T15:57:47Z | B | Stateful testing: declare OpenAPI `links` + `operationId` so POST→GET→DELETE chains are exercised (currently 0 of 613 links covered) |
| KS-229 | High | In Review | kamil.kreiser@secuura.ai | — | 2026-09-10T21:48:13Z | B | [Tracker] 2026-06-10 platform assurance review — gap-analysis + remediation |
| KS-239 | High | Backlog | stuart.jamieson@secuura.ai | — | 2026-08-12T07:50:40Z | B | [Decision] Erasure: multi-step to trigger, but irreversible + complete once executed — confirm no recoverable off-chain link survives (incl. backups) |
| KS-256 | High | In Progress | kamil.kreiser@secuura.ai | — | 2026-09-09T15:57:47Z | D | Add OpenAPI inline examples to all 329 operations — eliminate coverage-phase no-test-cases skips |
| KS-304 | High | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-02T10:24:22Z | B | Tokenise personal/identifying data — mint a privacy token (Platform S/K by journey origin) and thread it through the APIs |
| KS-329 | High | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-02T16:59:22Z | B | Phase 2 — JWT RS256 → hybrid (RS256 + ML-DSA-65) |
| KS-365 | High | Blocked | kamil.kreiser@secuura.ai | — | 2026-09-08T12:01:18Z | C | Base-image refresh routine + track postgres CVE-2025-68121 (redis leg already done in triage) |
| KS-412 | High | Todo | peter@obeden.com | — | 2026-09-09T13:48:07Z | B | CI: require all systemTest (all tools) PR suites + pre-merge to block merges on failure (branch protection + sign-off) |
| KS-485 | High | Todo | kamil.kreiser@secuura.ai | Bug | 2026-09-12T00:07:38Z | B | Security review — plan, methodology & handover (Platform K) |
| KS-487 | High | In Progress | kamil.kreiser@secuura.ai | Bug | 2026-09-09T11:12:36Z | D | Review B — Input validation, injection, upload, XSS/SSRF & crypto |
| KS-491 | High | Todo | kamil.kreiser@secuura.ai | Bug | 2026-09-12T00:30:41Z | B | Review F — Edge, WAF, DDoS & anti-automation |
| KS-525 | High | Backlog | peter@obeden.com | — | 2026-09-09T16:02:34Z | B | Playwright: end-to-end flow coverage across all 310 published API operations |
| KS-565 | High | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-11T11:15:19Z | C | Sweeps 2026-08-05: untracked failures across 10 ops — response-schema recurrence (KS-498 residual), 3 genuine 500s, non-envelope 5xx on by-design-503 ops, undocumented status |
| KS-568 | High | Backlog | peter@obeden.com | — | 2026-09-06T00:30:30Z | B | systemTest (Schemathesis): S↔K connector identity regression coverage (KS-480 Option A) — tier separation, rotation read-back, provenance exclusion |
| KS-575 | High | In Progress | peter@obeden.com | Bug | 2026-09-09T15:57:47Z | B | Schemathesis sweep locks itself out of its own account (demo@secuura.io) by fuzzing POST /api/users/me/change-password |
| KS-576 | High | Todo | kamil.kreiser@secuura.ai | Feature | 2026-09-03T02:03:54Z | C | Bulk re-key: one admin-authorised rotate across a named set of externalRefs |
| KS-577 | High | In Review | kamil.kreiser@secuura.ai | Bug, Decision | 2026-09-09T10:59:30Z | D | rotate: true mints a new key but never revokes the old one — implement revoke-on-rotate and agree the cutover window |
| KS-588 | High | Backlog | peter@obeden.com | — | 2026-09-07T15:33:30Z | B | systemTest (Schemathesis): /api/status authorization + revoked-session regression coverage (KS-570 class — vc-issuer status lists) |
| KS-590 | High | Backlog | peter@obeden.com | — | 2026-09-06T00:30:27Z | B | systemTest (Schemathesis): verify-by-hash must not resolve to an arbitrary registration — anchored-ancestor + cross-tenant field disclosure (KS-584 class) |
| KS-591 | High | Backlog | kamil.kreiser@secuura.ai | Bug | 2026-09-10T11:18:21Z | C | positive_data_acceptance recurs at scale — 734 failures across 64 ops (KS-255 / KS-515 recurrence, full-2026-08-07 sweep) |
| KS-593 | High | Backlog | kamil.kreiser@secuura.ai | Bug | 2026-09-11T11:15:12Z | C | not_a_server_error recurs — 17 raw 5xx across 8 ops (KS-431 / KS-449 / KS-497 recurrence, full-2026-08-07 sweep) |
| KS-598 | High | Todo | kamil.kreiser@secuura.ai | — | 2026-09-03T02:03:59Z | B | Architecture P1: defuse the MULTI_TENANCY registry upsert — it silently collapses registrations per (hash, tenant) if the flag is ever enabled |
| KS-601 | High | In Progress | kamil.kreiser@secuura.ai | — | 2026-09-12T00:30:34Z | D | [Infra] New Platform K dev server "Kintsugi" — restore dev/demo split |
| KS-602 | High | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-02T10:24:25Z | B | BM-1: Certification model — certification = attestation + signing + optional watermarking; any modification → new version → mandatory re-certification |
| KS-603 | High | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-02T10:24:25Z | B | BM-2: Verification is a configurable workflow via smart contracts — record the workflow path, not casual views |
| KS-607 | High | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-02T10:24:40Z | B | GET /api/anchors/{id} and verify report different statuses for the same anchor — 91 UAT anchors read "failed" while verify says confirmed |
| KS-618 | High | Backlog | kamil.kreiser@secuura.ai | — | 2026-08-13T00:10:26Z | B | Client IP is invisible platform-wide on demo: every IP-keyed control sees 172.18.0.1 — brute-force, lockout and CSRF binding are global, and KS-613's rate limit would be too |
| KS-624 | High | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-02T10:24:41Z | B | prism issues VCs with random bytes as the Ed25519 proof and verifies them as passed — the A-11 fraud pattern fixed in vc-issuer, never fixed here |
| KS-636 | High | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-05T23:53:10Z | B | node:24-alpine carries a CRITICAL (CVE-2026-59873) — our own base-image watchdog flagged it on 2026-08-01 and the failure went unread |
| KS-638 | High | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-07T03:30:44Z | B | The extranet test board has never shown a green run — 0 passed in 22, and the latest red is E2E 210/0 with Schemathesis producing no results |
| KS-643 | High | In Review | kamil.kreiser@secuura.ai | — | 2026-09-10T11:18:21Z | D | Security: DELETE /api/keys/:id revokes any tenant's key — no ownership check |
| KS-655 | High | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-05T23:53:07Z | B | KS-78 drift check is wrong three ways — reports 7 commits of drift where 212 exist, labels `develop` as `main`, and anchors to a stock redis image |
| KS-661 | High | In Review | kamil.kreiser@secuura.ai | — | 2026-09-03T02:03:59Z | B | Rename the `certify` lifecycle verb to `declare` |
| KS-663 | High | In Review | kamil.kreiser@secuura.ai | — | 2026-09-12T00:30:36Z | D | The OpenAPI spec is now a consumed contract, but nothing in CI stops it drifting — plus two known spec/code divergences |
| KS-664 | High | In Progress | kamil.kreiser@secuura.ai | — | 2026-09-03T02:03:47Z | C | deepmerge-ts GHSA-ggr8-5vv4-36mx (high) — override to 8.0.1 in originate; hoisted root lock baselined to 2026-10-31 on reachability |
| KS-665 | High | In Progress | kamil.kreiser@secuura.ai | — | 2026-09-09T15:57:47Z | C | KS-256 review follow-ups: 5 example-fixable 400s, the tsx transpile-only spec-gate trap (§10), and a new `userAgent: Demo Issuer` instance |
| KS-668 | High | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-10T13:59:01Z | B | Compose seeds published *123 credentials by default, and the 11 rotation vars never reach the auth container from .env — every compose deploy (local, demo VM, Kintsugi) |
| KS-669 | High | In Progress | kamil.kreiser@secuura.ai | — | 2026-09-05T23:53:04Z | C | Published spec points integrators at 18 URLs on domains we do not own (one is for sale) — E1 only inspects emails, never URLs |
| KS-678 | High | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-05T05:16:06Z | B | #568 publishes 17 URLs on secuura.io — an unresolving, seemingly unowned domain (KS-669 class; no guard rule covers URLs) |
| KS-683 | High | Todo | kamil.kreiser@secuura.ai | Bug | 2026-09-09T12:47:34Z | B | Anchor-status standoff: a consumer repolls anchors K reports as terminally failed — K's labelling is already honest (KS-587), so the fix is terminal-state handling, not a new K signal |
| KS-692 | High | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-03T15:14:09Z | B | Security: /api/status revoke/unrevoke has no tenant ownership check — an ISSUER_ADMIN in any tenant can revoke another tenant’s credential (KS-586’s deferred half, now untracked) |
| KS-693 | High | In Review | kamil.kreiser@secuura.ai | — | 2026-09-09T13:58:25Z | D | M365 routes answer 503 when ENTRA_* is unconfigured — 9 permanent Schemathesis failures on every dev machine, and the local sweep is now the merge gate |
| KS-695 | High | In Progress | kamil.kreiser@secuura.ai | — | 2026-09-09T10:04:03Z | C | S↔K (K-side): erasure by external_ref, documents.title coverage, and connector-scoped org erasure — PS-690 dependency |
| KS-696 | High | Todo | kamil.kreiser@secuura.ai | — | 2026-09-10T11:20:29Z | B | Akto pr-scan is non-deterministic — three runs on near-identical code gave 1 HIGH / 1 HIGH (different endpoint) / 0 HIGH |
| KS-698 | High | In Progress | kamil.kreiser@secuura.ai | — | 2026-09-09T09:27:17Z | C | Security: one request permanently poisons any rate-limit key — unbounded windowMs persists an invalid resetAt, and every later check 500s (limiter fails open) |
| KS-709 | High | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-10T11:20:29Z | B | Akto reports a PASS for a test that executed NOTHING — 'clean 0 / not-applicable 969 ✓' is a second false-zero axis that richCaptureFailed does not catch |
| KS-716 | High | Todo | kamil.kreiser@secuura.ai | — | 2026-09-10T11:20:29Z | B | The whole super-admin surface is silently unscanned — no system_admin block means the HAR replay fallback never fires (0 of 16 endpoints, incl. KS-694's GDPR routes) |
| KS-723 | High | Todo | kamil.kreiser@secuura.ai | — | 2026-09-05T23:53:02Z | B | Declare the remaining ~157 routed-but-undocumented /api operations in the OpenAPI spec — the KS-712 remainder |
| KS-724 | High | Todo | kamil.kreiser@secuura.ai | — | 2026-09-10T11:20:29Z | B | A scan that logs in more than ten times as one user revokes its own bearer — the 10-session window evicts the token it is scanning with |
| KS-725 | High | Todo | kamil.kreiser@secuura.ai | — | 2026-09-10T11:20:29Z | B | test:pr never re-imports the OpenAPI spec, so Akto scans a collection that has drifted from it — a declared operation is not a scanned one |
| KS-729 | High | In Progress | kamil.kreiser@secuura.ai | — | 2026-09-08T12:53:28Z | C | Upgrade ip-address off GHSA-mwp4-54f8-5fhr (high, SSRF) — express-rate-limit 8.4.1→8.5.1+ in mcp-server, @meshsdk/@cardano-sdk 9.0.5 line in root + frontend/issuer |
| KS-730 | High | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-05T23:53:01Z | A | Security: 71 inline handlers still return err.message verbatim off-production — KS-727's enumerated remainder (api-gateway leaks it TWICE, at the edge) |
| KS-731 | High | In Progress | kamil.kreiser@secuura.ai | — | 2026-09-10T23:36:47Z | C | Local slots share one Postgres/Redis credential pair — any slot can read, write and DROP another slot's database as superuser |
| KS-734 | High | In Review | kamil.kreiser@secuura.ai | — | 2026-09-09T16:12:06Z | D | The e2e Playwright suite cannot run from a clean checkout — tests/e2e is not a workspace member and never gets installed; 20 of 82 fail once it does |
| KS-735 | High | Todo | kamil.kreiser@secuura.ai | — | 2026-09-12T00:30:47Z | B | Verify results show the user nothing about what was registered — a renamed file confirms green with no explanation (PS-723) |
| KS-739 | High | In Review | kamil.kreiser@secuura.ai | — | 2026-09-09T12:27:52Z | D | transfer-custody maps a 401/403 from users/lookup to 502 BAD_GATEWAY — the KS-536 4xx rule was applied to 400/422 only |
| KS-753 | High | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-07T12:57:21Z | B | Timestamping fail-closed: a mock TSA fallback must not report verified: true (extend KS-523 to the batch path) |
| KS-754 | High | In Review | kamil.kreiser@secuura.ai | — | 2026-09-09T11:05:31Z | C | updateDSRStatus silently no-ops for any non-uuid actor — step 12 never marks a connector erasure completed |
| KS-756 | High | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-05T23:52:52Z | B | Wire up the opaque refresh token that createSession already mints — one write site, zero read sites (KS-329 ruling (a) prerequisite) |
| KS-762 | High | Blocked | kamil.kreiser@secuura.ai | — | 2026-09-06T15:03:38Z | C | APP_DB_PASSWORD is a committed literal :- default in docker-compose.yml — 51 sites, not the ~20 the register records |
| KS-763 | High | In Review | kamil.kreiser@secuura.ai | — | 2026-09-05T23:52:49Z | C | Push preflight blocks the whole repo — two qs advisories (GHSA-4mjr / GHSA-x5fp) unbaselined across 27 standalone locks; fixed in qs@6.16.0 |
| KS-764 | High | In Progress | kamil.kreiser@secuura.ai | — | 2026-09-09T10:40:36Z | D | Security: decideKeyRevoke has no organisation arm — an ORG_ADMIN can revoke a sibling organisation's key inside its own tenant (QA F10) |
| KS-768 | High | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-05T23:52:47Z | C | audit-locks scans 35 of 45 lockfiles — 3 vulnerable locks have coverage from neither gate |
| KS-769 | High | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-06T01:46:49Z | B | mobile/secuura-app has 81 unscanned advisories (2 critical) — nothing has ever audited that tree |
| KS-770 | High | Todo | kamil.kreiser@secuura.ai | — | 2026-09-08T14:48:50Z | B | Review stream: API contract and the four platform suites |
| KS-771 | High | In Progress | kamil.kreiser@secuura.ai | — | 2026-09-09T13:47:09Z | D | Review stream: build, supply chain and release gates |
| KS-772 | High | Todo | kamil.kreiser@secuura.ai | — | 2026-09-12T00:15:10Z | B | Review stream: S<->K integration contract |
| KS-775 | High | In Progress | kamil.kreiser@secuura.ai | — | 2026-09-05T23:52:45Z | B | [Decision] Own the express 4 -> 5 call before the qs fuse lapses 2026-09-10 - KS-409 was archived and nothing replaced it |
| KS-785 | High | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-09T15:36:53Z | B | Compose resolves the SHELL over .env while the checker resolves .env over the shell — a green credential check over a stack running the shared literal |
| KS-787 | High | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-05T23:52:41Z | B | S revokes that emit no lifecycle event, or emit share-permission-change, are indistinguishable on K from a document that was never revoked |
| KS-790 | High | In Review | kamil.kreiser@secuura.ai | — | 2026-09-05T05:00:13Z | C | OAuth authorization_code token exchange uses getUserById (post-auth) in a pre-auth flow — 400 'User not found' for every code grant under fail-closed RLS, and it masks KS-781 |
| KS-796 | High | In Progress | kamil.kreiser@secuura.ai | — | 2026-09-08T13:17:55Z | C | KS-781 door 3: POST /api/auth/wallet/verify mints a full token pair without MFA, lockout or status |
| KS-798 | High | In Progress | kamil.kreiser@secuura.ai | — | 2026-09-08T10:03:23Z | D | The consent page posts the redirect URI in the client_id field — nobody can complete the OAuth flow from it |
| KS-800 | High | In Review | kamil.kreiser@secuura.ai | Bug | 2026-09-05T22:01:06Z | C | CLASS: a body parser mounted AFTER the control-byte guard is unguarded — 3 route-scoped sites in the gateway (1 live), and nothing structural stops a 6th service mounting them out of order |
| KS-801 | High | In Progress | kamil.kreiser@secuura.ai | Bug | 2026-09-05T05:41:06Z | C | Security: four gateway path predicates are case-sensitive while Express routing is not — `/API/...` skips media-type enforcement on EVERY path, and is still proxied |
| KS-804 | High | In Review | kamil.kreiser@secuura.ai | — | 2026-09-08T09:58:49Z | D | Security: POST /api/oauth/authorize's resolver carries ONE of the GET path's FOUR app rules — PKCE is skipped for public clients and the code is redeemable with no verifier |
| KS-806 | High | In Progress | kamil.kreiser@secuura.ai | — | 2026-09-05T06:09:02Z | C | Security: the synthetic wallet email buckets on walletAddress.slice(0,8) — degenerate for every addr_test1…/stake… address, so a colliding wallet takes the create branch and gets an object the account gate cannot reach |
| KS-810 | High | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-05T23:52:36Z | A | auth.openapi.ts cannot be imported by any test — passwordLoginGate imports z from zod directly, so a module-scope throw there leaves the suite green |
| KS-823 | High | Todo | kamil.kreiser@secuura.ai | — | 2026-09-08T08:54:06Z | A | Security: the /api/oauth/token `refresh_token` grant authenticates NO client — a confidential app's refresh token needs no credential |
| KS-835 | High | Todo | kamil.kreiser@secuura.ai | — | 2026-09-06T01:21:41Z | B | Security: OAuth consent is decorative — the granted scope never reaches the token, and the gate short-circuits on a label OAuth tokens share with logins |
| KS-841 | High | In Progress | kamil.kreiser@secuura.ai | — | 2026-09-08T10:03:23Z | D | Security: the rendered OAuth consent page cannot POST itself back — it emits the redirect URI as client_id and an empty code_challenge |
| KS-869 | High | Blocked | kamil.kreiser@secuura.ai | — | 2026-09-09T14:11:04Z | D | connectorId is never persisted — svc_api_keys.connector_id is written by nothing and read by nothing, so it dies on restart; blocks KS-577 and nulls KS-843's cutover evidence |
| KS-889 | High | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-06T08:47:32Z | B | KS-869's COALESCE backfill has an EMPTY window — the 39 pre-existing keys never backfill, so the KS-843 cutover flip still has no usable evidence |
| KS-926 | High | In Progress | kamil.kreiser@secuura.ai | — | 2026-09-10T07:25:36Z | D | 17 of 20 `check-*.sh` guards run from NO live entry point — including SQL-injection and trust-header reads; four were orphaned when Actions was retired |
| KS-927 | High | In Review | kamil.kreiser@secuura.ai | — | 2026-09-09T12:47:18Z | D | ks444-webhooks-create-description-guard: 2 of 4 cells RED on develop — the mock omits assertSafeOutboundUrl, so both POSITIVE cases 500 while the two negative ones stay green |
| KS-932 | High | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-06T11:56:14Z | A | timeoutMs does not bound DNS resolution — a hung lookup leaves safeOutboundRequest pending well past its declared deadline |
| KS-937 | High | In Progress | kamil.kreiser@secuura.ai | — | 2026-09-06T12:56:24Z | D | KS-921 residue: the re-link guard's awk parser is still case-sensitive — a lowercase `copy --from=builder … node_modules` reports 1 of 1 CLEAN, which is the #851 outage shape exactly |
| KS-938 | High | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-09T13:15:53Z | A | Security: "MFA disabled" leaves the TOTP seed and hashed backup codes in the row — updateUser skips every `undefined` field, so a PARTIAL update lands |
| KS-939 | High | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-06T12:48:47Z | B | Launcher: the assembled boot prompt is asserted by no cell — KS-907's fix can vanish at 18/0, and the seat sentence misled a live seat tonight |
| KS-945 | High | In Review | kamil.kreiser@secuura.ai | — | 2026-09-10T22:24:26Z | D | The install detector enumerates verbs and so fails OPEN — `npm add`, `npm it`, bare `yarn` and `pnpm add` are still false cleans on the #851 shape, and `pnpm i` is caught only by accident |
| KS-947 | High | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-06T13:40:16Z | A | KS-733 gate blindness (F3+F4): the parity cell misses skip:() and mount ORDER, and is purely relative so both mounts can drift off the published spec |
| KS-949 | High | In Progress | kamil.kreiser@secuura.ai | — | 2026-09-08T21:16:41Z | C | The seeded platform admin carries a real person's identity and a published default password — and the *123 lint exempts it by design |
| KS-950 | High | In Review | kamil.kreiser@secuura.ai | — | 2026-09-09T13:18:42Z | D | The boot seed dies permanently at boot 2 — migration 030 drops the UNIQUE its ON CONFLICT targets, and the migration loader does not record failures |
| KS-951 | High | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-06T21:43:44Z | B | The default-password CI gate catches one shape and calls it clean — 16 published passwords are exempt by design, and 4 of 5 canaries walk past it |
| KS-953 | High | Backlog | — | — | 2026-09-06T22:37:13Z | B | CLASS: editing api-gateway/src/index.ts silently reddens packages/shared, and nothing in the touched package can say so |
| KS-955 | High | Backlog | — | — | 2026-09-10T15:30:33Z | B | A fresh clone cannot run the four platform suites, and fails in a way that reads like a product regression |
| KS-958 | High | Backlog | — | — | 2026-09-07T00:44:09Z | A | The re-link guard matches the JS runtime name case-sensitively — every UPPERCASE spelling is exempt, and ENV NODE_ENV is in 13 of 35 Dockerfiles |
| KS-962 | High | Backlog | — | — | 2026-09-09T11:53:18Z | C | The api-gateway user seed throws 42P10 on every boot and has never seeded anything — remove its INSERT, do NOT repoint the conflict target |
| KS-966 | High | In Progress | — | — | 2026-09-11T11:35:20Z | C | Retire the published SYSTEM_ADMIN credential (Kam: rotate-properly) — a deletion, not a rotation: no new shared secret is needed |
| KS-967 | High | Backlog | — | — | 2026-09-07T03:27:23Z | B | Neither credential guard can see a value in a .env.example — one scans the wrong roots and extensions, the other excludes the file and self-tests the exclusion |
| KS-968 | High | In Progress | kamil.kreiser@secuura.ai | — | 2026-09-08T13:29:11Z | D | MAJOR: when both platform-admin rows exist the id-row rewrite throws 23505, the seed loop swallows it, and the KS-966 F3 email arm never runs — with a green cell standing over the hole |
| KS-974 | High | Backlog | — | — | 2026-09-07T10:27:23Z | A | Published bound vs runtime bound on rate-limit scope: /check enforces code UNITS against a published code-POINT maxLength, and scopeField bounds the untrimmed string |
| KS-977 | High | Backlog | — | — | 2026-09-07T11:10:12Z | B | `setup`/`install` are exempt from the pre-suite step on a false justification — they perform a live authenticated login with a seeded account |
| KS-981 | High | Backlog | — | — | 2026-09-07T11:44:37Z | C | The round-4 quarantine call throws out of a "Never throws" function, and the strict arm quarantines in silence |
| KS-982 | High | Backlog | — | — | 2026-09-10T07:25:36Z | C | pre_suite.test.sh silently quarantines a developer's live manifest and reports 24 passed, 0 failed |
| KS-983 | High | Backlog | peter@obeden.com | — | 2026-09-07T13:44:22Z | B | systemTest: no suite drives a path-spelling (`//`) variant — the KS-858 class is guarded only by gateway unit tests, and 7 rate-limited auth routes were never driven |
| KS-987 | High | Backlog | — | — | 2026-09-07T22:22:45Z | B | A deploy that rsyncs the OpenAPI spec and does not restart api-gateway ships a silently stale published contract — rsync breaks the bind mount by inode |
| KS-991 | High | In Progress | kamil.kreiser@secuura.ai | — | 2026-09-10T07:25:36Z | D | A stale LOCAL `develop` runs the full platform preflight on an unrelated branch, which then fails on `DEPS MISSING` — an environment condition presented as a gate failure |
| KS-993 | High | In Progress | kamil.kreiser@secuura.ai | — | 2026-09-09T01:38:13Z | D | Nothing type-checks systemTest/fixtures/ — the TypeScript that runs every suite's provisioning is covered by no tsconfig |
| KS-994 | High | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-11T10:51:22Z | C | `withGeneratedActors()` iterates the WRAPPER, not the environments — the k6 harness has NEVER used generated actors and silently runs on secrets.yml |
| KS-995 | High | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-08T04:07:13Z | B | Archiving a ticket silently archives its sub-issues, including NON-TERMINAL ones — and the parent-side check cannot detect it |
| KS-996 | High | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-08T00:49:07Z | B | 95 archived tickets sit in NON-TERMINAL states — measure whether a cascade put them there |
| KS-997 | High | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-08T05:07:59Z | B | Re-triage four npm advisories that landed in the audit baseline ALREADY EXPIRED (Kam's `add-dead` ruling) |
| KS-998 | High | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-08T04:05:29Z | A | KS-989 gate residue: the formatting gate fails OPEN on missing deps and reads the WORKING TREE, not the push — four items on one path |
| KS-999 | High | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-08T04:56:22Z | A | getUserById's decrypt path escapes the KS-253 classifier — `return await fromRow(...)`, and the characterisation cell that cannot reach its own conclusion |
| KS-1000 | High | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-08T11:49:08Z | A | services/auth tsconfig EXCLUDES src/__tests__ — every 'tsc: 0 errors' on a test-only change in this service is a green that could not fail |
| KS-1004 | High | In Progress | — | — | 2026-09-09T21:03:26Z | D | A document with a txHash can never be marked anchor-failed — NOR healed forward to confirmed; both guards key off the hash, and write-ahead widens the window |
| KS-1005 | High | Backlog | — | — | 2026-09-08T11:24:00Z | A | Security/defect: POST /api/users/me/change-password returns 404 for EVERY user — USER_COLS omits password_hash |
| KS-1009 | High | Backlog | — | — | 2026-09-08T13:22:38Z | B | Security: GET /api/auth/wallet/status returns userId + role to ANY anonymous caller — enumeration surface, and nothing consumes the fields |
| KS-1012 | High | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-11T11:21:32Z | B | The `require-pr-gates` ruleset survived the Actions retirement: 7 required checks that can never report, 0 required approvals, and ALWAYS bypass for admins |
| KS-1020 | High | Backlog | — | — | 2026-09-08T21:14:50Z | A | Security: GET /api/presentations/{id} returns a real stored presentation for an id that names nothing — LIKE '%id%' fallback with NO ownership check |
| KS-1024 | High | In Review | — | — | 2026-09-09T11:05:31Z | B | PUSH BLOCKER (repo-wide): two new advisories are unbaselined, so preflight 6/13 + 7/13 fail on EVERY branch — vitest GHSA-82fw and baseline-browser-mapping GHSA-w5vr |
| KS-1025 | High | Backlog | — | — | 2026-09-08T22:20:32Z | B | Reshape the advisory gate: it is NON-DETERMINISTIC on an unchanged tree — 8 advisories in 30 min, one appeared then vanished. Warn-then-fail, keyed on REACH and SEVERITY (window length is Kam's) |
| KS-1026 | High | In Progress | kamil.kreiser@secuura.ai | — | 2026-09-11T10:51:22Z | D | withGeneratedActors is a NO-OP for every consumer — the k6 suite has been running on secrets.yml credentials while believed to be running on provisioned actors |
| KS-1028 | High | Backlog | — | — | 2026-09-09T01:33:34Z | B | KS-754 gate F-1 (MAJOR): a step-12 throw skips the USER_ERASED fan-out AFTER the crypto-shred — local data destroyed, four subscribers keep theirs |
| KS-1029 | High | Backlog | — | — | 2026-09-11T11:15:05Z | A | KS-754 gate F-2 (MAJOR): PATCH /api/gdpr/dsr/{dsrId} regresses a malformed id from 200 to 500 — UUID_PATTERN exists in the same file and is not used on this route |
| KS-1031 | High | Backlog | — | — | 2026-09-09T01:33:35Z | B | KS-754 gate F-4: DEPLOY CONDITION — apply 048 BEFORE rolling the originate image, or every connector erasure shreds the DEK then aborts forever (and run-migrations.sh exits 0 when migrations fail) |
| KS-1032 | High | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-11T09:54:10Z | D | Security: 9 trust-header reads outside auth middleware (pen-test F-04) — surfaced by wiring check-no-trust-header-reads.sh in KS-926 |
| KS-1035 | High | Backlog | — | — | 2026-09-09T09:21:59Z | B | The merge gate cannot see a WITHDRAWN approval — #813 reads approved+clean against the reviewer's written refusal |
| KS-1036 | High | Backlog | — | — | 2026-09-09T03:24:42Z | B | The review-stream overlay covers 57 of 114 active tickets, and DEV-PROCESS still says 'nothing left over' |
| KS-1038 | High | Backlog | — | — | 2026-09-09T16:12:06Z | D | tests/e2e auth-exhaustive races its OWN lockout — same commit gives 1 or 11 failures, so the suite cannot gate anything |
| KS-1044 | High | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-09T10:09:13Z | B | No independent liveness signal for our own VMs — kintsugi was dead for 53 h and Azure health read `Available` the whole time |
| KS-1046 | High | In Review | kamil.kreiser@secuura.ai | — | 2026-09-09T14:07:02Z | D | `PREFLIGHT PASSED.` is printed identically whether 13 legs ran or 10 — the verdict has no skip tally |
| KS-1051 | High | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-09T14:07:03Z | D | develop is RED on the services/originate jest suite and NOTHING catches it — the suite is a blocking gate nowhere automated |
| KS-1052 | High | In Progress | kamil.kreiser@secuura.ai | — | 2026-09-09T14:14:39Z | D | CLASS: 21 of 24 updateUser callers discard the return — a backup-code login burns nothing and still succeeds, a password reset burns its token over an unchanged password |
| KS-1054 | High | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-09T13:41:51Z | B | Fresh databases are FAIL-OPEN until the second boot — 039_rls_fail_closed does not apply on boot 1 (file stage runs before the CORE stage it depends on) |
| KS-1055 | High | Backlog | — | — | 2026-09-09T13:45:28Z | D | Per-tenant databases never receive the file migrations — CORE_MIGRATIONS FORCEs RLS with ZERO policies, so a per-tenant DB is dark on 5 core tables from boot 1 (permanent) |
| KS-1062 | High | In Review | — | — | 2026-09-09T14:03:07Z | D | F-928-4: the tenant-migration counter cannot report a failure — a tenant whose database does not exist is logged as migrated |
| KS-1075 | High | In Progress | — | — | 2026-09-11T13:18:41Z | D | CI gates: both PR security gates fail for CONFIG reasons, not findings — tsx driver missing, an EMPTY npm-audit allow-list, and an audit-contract step that swallows its own diagnostic under bash -e |
| KS-1077 | High | In Progress | — | — | 2026-09-10T10:49:55Z | D | Two npm-audit allow-lists disagree: CI's is EMPTY and cannot express an advisory-less carrier package — make the GHSA-keyed local baseline the single source |
| KS-1080 | High | Backlog | — | — | 2026-09-10T10:44:33Z | B | SECURITY (local test stack): akto-autoheal runs as root with /var/run/docker.sock RW — env-scoping is only as strong as who holds the socket |
| KS-1081 | High | Backlog | — | — | 2026-09-10T22:49:09Z | B | CONFIG DRIFT: two tracked env templates disagree by ~39 vars — bootstrap-env.sh reads .env.example, CLAUDE.md documents env.example |
| KS-1087 | High | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-11T02:14:42Z | B | workflow-approve deletes the pending document and answers 200 "Document has been created" without reading originate's response — a refused forward (401, measured) loses the document |
| KS-1099 | High | In Progress | kamil.kreiser@secuura.ai | — | 2026-09-12T03:26:47Z | D | A malformed k6 YAML config prints secrets-file lines to stderr: cli.ts:180 calls loadSecrets() at top level with no catch, before the run-log tee starts (QA-958-4) |
| KS-1100 | High | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-12T02:20:18Z | B | Kintsugi deploy 4554b25e2: four live changes have no QA gate record — #872 (KS-732), #896 (compose ADMIN_USER_PASSWORD), #728 (KS-671), #808 (KS-663) |
| KS-1107 | High | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-12T02:14:07Z | B | POST /api/auth/register accepts a client-supplied organizationId with no existence or membership check — impact not traced |
| KS-101 | Medium | Backlog | stuart.jamieson@secuura.ai | — | 2026-07-14T14:11:27Z | B | Consolidate Platform K billing onto Platform S's Stripe integration (one company, one Stripe) |
| KS-135 | Medium | Todo | stuart.jamieson@secuura.ai | — | 2026-09-03T02:03:51Z | B | Platform S "S+" refactor — pluggable upload/watermark/sign/certify services |
| KS-139 | Medium | Backlog | stuart.jamieson@secuura.ai | — | 2026-09-02T10:25:27Z | B | Platform S — upload your test suite so the extranet live runner executes it (GitHub Actions) |
| KS-174 | Medium | In Progress | — | — | 2026-09-10T11:18:21Z | C | KS-160 Step 3: set tenant GUC on checkout + admin-role exemption for cross-tenant reads + flip fail-closed (atomic, dev-first) |
| KS-263 | Medium | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-05T23:53:14Z | B | Enable Code Security / GHAS so security scans populate the Security tab (currently artifact-only) |
| KS-305 | Medium | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-02T10:24:20Z | B | State the M365 source-document controller boundary in the customer DPA |
| KS-418 | Medium | Blocked | peter@obeden.com | — | 2026-09-11T13:42:46Z | B | systemTest (all tools): enable nightly platform test suites after full AWS migration |
| KS-492 | Medium | Todo | peter@obeden.com | Bug | 2026-09-11T10:51:22Z | B | Review G — systemTest (all tools) security regression coverage |
| KS-502 | Medium | Todo | peter@obeden.com | — | 2026-09-10T08:33:56Z | B | systemTest (Schemathesis): skipped security regressions needing a proper harness/env (billing idempotency · seed-demo prod-gate · webhook-SSRF residual) |
| KS-526 | Medium | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-05T23:53:14Z | B | KMS: move platform wallet mnemonic to Key Vault (KS-326 follow-up) |
| KS-528 | Medium | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-02T10:24:26Z | A | Frontends: react-router v6 → v7 migration (3 moderate client-runtime advisories — open redirect/XSS, constructor injection) |
| KS-530 | Medium | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-05T23:53:13Z | A | @hono/node-server v1->v2 major bump (GHSA-frvp) - originate + mcp-server runtime |
| KS-533 | Medium | Todo | peter@obeden.com | — | 2026-09-06T00:30:30Z | B | S↔K security register: data-loss / unrecoverability scenarios + code-verified findings (extracted from KS-480 sign-off) |
| KS-562 | Medium | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-05T23:53:12Z | C | anchoring threadTokenMint test fails only under root-visible npm install layout — nested @lucid-evolution/plutus duplicate-instance (pre-existing, layout-dependent; KS-559 A/B-cleared) |
| KS-571 | Medium | Backlog | peter@obeden.com | — | 2026-09-06T00:30:29Z | B | systemTest (Schemathesis): KS-539 agent document-operation rules — onBehalfOf realignment (G-1) + R2/R4/R5/R6 regression coverage |
| KS-572 | Medium | Backlog | peter@obeden.com | — | 2026-09-06T00:30:29Z | B | systemTest (Schemathesis): pin the KS-546 unhandledRejection posture — config drift + the mirrored KS-529 guard |
| KS-573 | Medium | In Progress | peter@obeden.com | — | 2026-09-06T00:30:28Z | B | systemTest (Schemathesis): assert the shared control-byte boundary is mounted in every consuming service (KS-471/KS-472 mount gap) |
| KS-579 | Medium | Todo | kamil.kreiser@secuura.ai | Improvement | 2026-09-03T15:28:25Z | B | Per-person platform-admin identities — the shared seeded admin cannot carry attribution or approval |
| KS-580 | Medium | Todo | kamil.kreiser@secuura.ai | Improvement | 2026-09-03T02:03:56Z | B | Append-only recovery audit held outside the estate being recovered |
| KS-581 | Medium | Todo | kamil.kreiser@secuura.ai | Improvement | 2026-09-03T02:03:57Z | B | register-connector: volume alerting, rate limit, and correlation of refused re-key attempts |
| KS-582 | Medium | Todo | kamil.kreiser@secuura.ai | Decision | 2026-09-03T02:03:58Z | B | [Decision] Approval shape for bulk re-key — two approvers for a batch, one for a single-org rotation |
| KS-583 | Medium | Todo | kamil.kreiser@secuura.ai | Improvement | 2026-09-09T08:59:01Z | B | DR rehearsal: lose a key → re-key → read-back survives on pre-loss anchors → the old key is dead |
| KS-595 | Medium | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-11T10:50:53Z | B | Three undeclared-verb catalogue skips cite CLOSED tickets (KS-406 / KS-421) — are the defects still live? |
| KS-604 | Medium | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-02T10:24:56Z | B | BM-5: System-details document for Peter & Stuart — the technical system-info doc Kam owes them |
| KS-605 | Medium | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-02T10:24:57Z | B | Terminology definitions for stakeholders + lawyers — certification / verification / signing / watermarking |
| KS-606 | Medium | Backlog | peter@obeden.com | — | 2026-09-09T15:57:47Z | B | systemTest (Schemathesis): split scripts/run.py + scripts/runner/config.py — blocked on re-establishing the pre-venv bootstrap contract first |
| KS-619 | Medium | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-10T22:49:14Z | B | Gateway tenant resolution falls through to the caller's x-tenant-id when a token has no tenantId claim — make it unconditional and fail closed |
| KS-621 | Medium | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-10T11:18:21Z | B | Document reads are scoped by tenant and owner, never by organization — cross-org protection is emergent, not enforced |
| KS-625 | Medium | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-02T10:24:41Z | B | /presentations/verify reports a presentation verified without checking the holder signature — challenge/domain compared, proof never validated |
| KS-627 | Medium | Backlog | kamil.kreiser@secuura.ai | Feature | 2026-09-10T16:48:28Z | B | Implement real wallet signature verification (CIP-8/COSE + address binding) — needs the COSE key back in the request contract |
| KS-629 | Medium | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-05T23:53:11Z | B | kyc `livenessVideo` is accepted by spec and runtime, then silently discarded — no code path reads it |
| KS-630 | Medium | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-05T23:53:10Z | B | Wire the status-page XSS probe into preflight (or decide not to) — it runs today only by hand |
| KS-650 | Medium | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-08T12:14:26Z | D | services/originate: POST /api/webhooks 500s on its two success-path tests — ks444 suite red on develop |
| KS-651 | Medium | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-05T23:53:08Z | B | [Decision] @secuura/shared is imported by 24 services and declared by 2 — the symlink pattern is invisible to every lockfile and audit gate |
| KS-657 | Medium | In Review | kamil.kreiser@secuura.ai | — | 2026-09-05T23:53:06Z | D | services/shared (@secuura/service-utils) cannot build — no tsconfig.json, so main/types point at a dist that can never exist; its src/ half is dead but types/ is live in billing |
| KS-658 | Medium | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-12T00:30:41Z | D | The demo VM runs every service as NODE_ENV=development while the code names "demo" as prod-like — ~6 production guards are silently inert, and the public API-docs exposure is one symptom |
| KS-679 | Medium | In Review | kamil.kreiser@secuura.ai | — | 2026-09-09T12:26:17Z | D | Published Anchor.id is anc_… but anchoring only ever mints anchor_<uuid> — format-false, live on develop, and #568 promotes it to the canonical fixture |
| KS-686 | Medium | Backlog | peter@obeden.com | — | 2026-09-10T16:48:28Z | B | not_a_server_error flags the by-design 501 on POST /api/wallets/verify — needs the integration_5xx_guard treatment (split from KS-684 item 7) |
| KS-699 | Medium | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-02T10:39:22Z | B | No table references `users`: 0 of the database's 29 foreign keys point at it, across 52 user-reference columns — KS-697 was this hole being exercised |
| KS-704 | Medium | Todo | kamil.kreiser@secuura.ai | — | 2026-09-09T15:38:43Z | A | k6 gate reports a failure rate with no status-code breakdown - an author cannot tell a platform 4xx from a harness auth failure |
| KS-711 | Medium | Todo | kamil.kreiser@secuura.ai | — | 2026-09-10T11:20:29Z | C | systemTest/akto + systemTest/performance quality gates went red again on docs/quick_start.md — the KS-702/KS-706 fixes held, a docs commit re-reddened both |
| KS-726 | Medium | In Review | kamil.kreiser@secuura.ai | — | 2026-09-08T12:23:58Z | D | Write-ahead the Cardano tx hash: persist the deterministic hash BEFORE submitting, so a lost submit reply can never orphan a paid transaction |
| KS-736 | Medium | In Review | kamil.kreiser@secuura.ai | — | 2026-09-09T08:53:42Z | D | Gateway mount-auth check scores authenticateToken(false) as green — six /api mounts satisfy neither leg of its own assertion |
| KS-738 | Medium | Todo | kamil.kreiser@secuura.ai | — | 2026-09-09T15:57:47Z | B | schemathesis run.py bootstrap can os.execv-loop forever on a symlinked venv — silent, 100% CPU, indistinguishable from a hang |
| KS-741 | Medium | Todo | kamil.kreiser@secuura.ai | — | 2026-09-11T09:42:02Z | A | x-emitter-internal is unstripped on the /originate/ route — the marker's safety rests on an unstated convention, and the comment promises the wrong guarantee |
| KS-745 | Medium | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-05T23:52:57Z | A | api-gateway audit export calls /api/audit/logs — a route the security service does not have, so the export 404s every time |
| KS-746 | Medium | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-05T23:52:56Z | B | Security events carry no tenant at all — KS-743 had to gate them platform-only, which is a workaround for the data model |
| KS-747 | Medium | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-09T09:21:16Z | A | Spec drift: GET /api/security/keys declares no parameters while the handler requires organizationId — the contract suite can never reach its 200 branch |
| KS-752 | Medium | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-10T16:48:28Z | B | Schemathesis baseline gate is unreachable: run.py skips it whenever the sweep fails — i.e. on every run it exists to triage |
| KS-755 | Medium | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-10T11:20:29Z | A | akto unit suite has a standing red: runDir resolveRunId ignores the injected clock |
| KS-757 | Medium | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-08T13:18:48Z | C | Connector erasure re-drive is unbounded against concurrency — and all three prescribed fixes are blocked (QA F-6) |
| KS-758 | Medium | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-08T13:18:48Z | B | Connector erasure: three permanent failures present as retryable and nothing dead-letters; the unresolvable path records no deletion log (Peter F6/F9) |
| KS-759 | Medium | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-05T23:52:51Z | A | tenantId is read through two `as unknown as` casts because it is not on JwtPayload (Peter F14) |
| KS-760 | Medium | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-05T23:52:51Z | B | The GitHub integration walks Linear tickets on branch names and PR bodies — 4 unrequested state changes in one night, all reverted by hand |
| KS-761 | Medium | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-05T23:52:50Z | B | similarity-undiscriminating FP entries have no staleness detection — a tolerance can outlive its premise and keep hiding a real finding |
| KS-765 | Medium | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-05T23:52:48Z | B | Merge helper must refuse a non-read SHA and have no fallback that re-derives its own expectation — the #774 gate could not fail |
| KS-766 | Medium | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-05T23:52:48Z | A | base-image-watch self-test cannot red the DB-age PRODUCER — the F-5 clamp can be re-introduced with the suite green |
| KS-767 | Medium | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-05T23:52:48Z | B | Decide the 17 baseline entries that carry no `expires` — permanent acceptance, or dated exception? |
| KS-773 | Medium | In Review | kamil.kreiser@secuura.ai | — | 2026-09-09T14:03:05Z | D | lockfile-cleanroom skips services/mcp-server for a reason its lock refutes — leg 2/9 claims "all locks clean-room-installable" without trying it |
| KS-777 | Medium | Todo | kamil.kreiser@secuura.ai | — | 2026-09-05T23:52:44Z | C | QA pass F-1/F-3/F-4/F-7: two vacuous guards, an unasserted statement tail, and an un-normalised org comparison (fixed on #795) |
| KS-780 | Medium | Todo | kamil.kreiser@secuura.ai | — | 2026-09-05T23:52:44Z | D | Two implementations of organisation-id normalisation, in two layers — move normaliseOrgId into @secuura/shared (the reason for keeping it local expired with KS-764) |
| KS-782 | Medium | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-05T23:52:43Z | B | [Decision] OAuth consent: a proper two-step MFA challenge on /api/oauth/authorize (the design half of KS-781) |
| KS-783 | Medium | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-07T03:25:37Z | B | A platform admin who loses their TOTP device has no self-service recovery — TOTP-only branch, no backup codes |
| KS-784 | Medium | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-09T13:58:25Z | A | POST /api/teams/webhook-config fails the Schemathesis pr sweep on every run — including develop — and is tracked by nothing |
| KS-789 | Medium | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-08T13:12:57Z | B | CONTRIBUTING.md justifies the hook's degradation and its --no-verify bypass with "CI is the hard gate" — there is no CI |
| KS-791 | Medium | In Review | kamil.kreiser@secuura.ai | — | 2026-09-10T22:24:27Z | D | Publish verify-file (v1+v2) in the spec — coupled with the gateway 415 fix, since octet-stream is refused today (KS-663 divergence 1) |
| KS-794 | Medium | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-05T23:52:39Z | D | verify-file returns `fileSize` on every 200 and neither response schema declares it |
| KS-799 | Medium | In Review | kamil.kreiser@secuura.ai | Bug | 2026-09-08T09:54:21Z | D | The OAuth consent page cannot submit its own form — CSRF answers 403 before the route is reached (pre-existing, not KS-781) |
| KS-802 | Medium | In Progress | kamil.kreiser@secuura.ai | Bug | 2026-09-08T04:07:13Z | C | KS-781 test-quality follow-ups from re-gate (4): restore the allow-set bound, put the revert pin on a real req.path, and widen the class guard's parser regex |
| KS-805 | Medium | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-05T05:25:52Z | A | POST /api/oauth/authorize deny emits `Location: undefined?error=…` for an app with zero registered redirect URIs; GET 500s on the same state; PATCH /api/oauth/apps lacks .min(1) |
| KS-807 | Medium | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-05T23:52:37Z | B | The control-byte guard cannot see a raw body — findNulBytePath returns null for every Buffer, and the doc claims otherwise |
| KS-808 | Medium | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-07T10:28:38Z | B | run-migrations.sh exits 0 even when a migration failed, and applied=N counts skips — the summary line cannot be trusted |
| KS-809 | Medium | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-07T03:25:36Z | B | A platform admin who loses their TOTP device cannot log in — platform_admins has no backup-code column at all |
| KS-813 | Medium | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-05T23:52:34Z | C | "PREFLIGHT PASSED" is unconditional — step() only prints a banner, and skipped legs read as passes |
| KS-824 | Medium | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-05T13:12:48Z | A | OAuth app_type: a CASED row is neither normalised by 047 nor refused by its CHECK, and docker/init's unnamed constraint defeats 047's idempotence guard |
| KS-825 | Medium | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-05T13:12:49Z | A | Gate integrity: the auth suite's green is not deterministic — three head runs gave 534/0, 534/0, and 534 with 2 FAILED |
| KS-826 | Medium | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-07T03:25:34Z | B | A red with no reader: originate's ks444 webhook-guard suite fails at both SHAs, and no gate ever runs the four service suites |
| KS-828 | Medium | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-05T23:52:33Z | A | KS-800 scanner: LEG F cannot see the control-byte guard LEAVE a wrapped router — both KS-815 wrappers can drop the guard and packages/shared stays 118/118 green |
| KS-829 | Medium | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-05T23:52:32Z | B | Audit gate baseline data model: an unvalidated `scope` lets a GREEN root gate advertise a row leg 7 still needs, and suppression matches by advisory id alone |
| KS-836 | Medium | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-05T23:52:31Z | B | Publish a `request:` block for POST /api/oauth/token — the endpoint's shape is asserted nowhere, and adding it moves what Schemathesis generates |
| KS-837 | Medium | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-05T23:52:31Z | C | Published prose drifts from the routes it describes and nothing detects it — the phrase check, the marker convention, and the ~306 unswept descriptions |
| KS-838 | Medium | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-05T23:52:31Z | A | Make the authorize rules DATA the resolver iterates, so the GET/POST agreement guard is structural instead of textual |
| KS-839 | Medium | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-05T23:52:30Z | B | Security: an allowedScopes of ['*'] bypasses the invalid_scope refusal entirely — validateScopes returns the request unfiltered |
| KS-843 | Medium | In Progress | kamil.kreiser@secuura.ai | — | 2026-09-08T08:18:34Z | C | KS-695 F5: build the dedicated `subjects:erase` scope gate on POST /api/gdpr/erasures — Kam ruled it 2026-09-03 and it has never been built |
| KS-844 | Medium | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-05T23:52:09Z | A | demo-service mounts no error handler — a raw 0x00 body returns express's default HTML with a stack trace and absolute paths |
| KS-848 | Medium | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-06T00:20:01Z | A | services/kyc tsconfig excludes src/__tests__ — the project tsc never type-checks a single test in this service |
| KS-849 | Medium | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-06T00:20:01Z | A | KYC mock document flow: a 1.5s timer writes back a STALE verification and silently clobbers the selfie's liveness result |
| KS-851 | Medium | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-06T00:56:30Z | B | KS-386 residues from the round-2 gate: G-1 column ordinal drift, G-2 the second-image orphan, G-3 the in-memory docstring is wrong at the wire, G-4 two write spellings the guard cannot see |
| KS-855 | Medium | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-06T01:25:20Z | A | The OAuth `AVAILABLE_SCOPES` list is a second, divergent scope vocabulary — derive it from SCOPES or pin it |
| KS-864 | Medium | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-12T00:30:37Z | A | Dead-estate pointers in RUNTIME SOURCE outside deployment/azure — system-status.ts hard-codes secuura-staging-* hosts, westeurope and a dead URL suffix |
| KS-865 | Medium | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-06T04:29:22Z | A | check-no-latest-tags.sh silently skips a missing input — it scans 5 of the 6 files it advertises and still prints OK |
| KS-866 | Medium | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-06T04:37:36Z | C | Merge protocol: the server-side `sha=` pin protects the PR head, not the base — a 9-second race merged onto an unapproved parent and invalidated the gate's predicted tree oid |
| KS-867 | Medium | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-06T04:39:13Z | A | CVE scan image filter `^dev-[a-z-]+:latest$` excludes digits and uppercase — `dev-auth2:latest` is invisible to the scan AND to the KS-676 examined-nothing alarm |
| KS-870 | Medium | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-06T04:51:14Z | A | Every ADMITTED erasure authenticates twice — the door's chain and the catch-all both run authenticateToken, doubling a remote key validation on a partner path |
| KS-871 | Medium | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-06T04:51:15Z | A | The audit log records `req.path` AFTER the response, so a REFUSED erasure is logged with the path trimmed to `/` instead of /api/gdpr/erasures |
| KS-872 | Medium | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-06T04:51:15Z | A | packages/shared project tsc is RED on develop — crypto.JsonWebKey is gone in @types/node 26.1.0; a live type error no gate owns |
| KS-876 | Medium | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-06T04:56:13Z | A | KS-860 guard walks services/ only — test listeners under packages/ are unguarded, including two in packages/shared itself |
| KS-877 | Medium | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-06T05:10:09Z | A | docker-build.sh: an empty SERVICES_TABLE dies at `${BUILD_LIST[*]}` under bash 3.2 — three lines after the guard added for that class |
| KS-878 | Medium | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-06T05:10:10Z | A | 09-aggregate-report: a 04 artefact that exists but does not PARSE emits zero findings and rc 0 — the exact artefact the pre-fix code produced |
| KS-880 | Medium | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-06T05:37:59Z | A | Quarantine or reconcile the dead converters copy — a second rowToApiKey that maps neither tenantId nor connectorId, with a passing test on it |
| KS-885 | Medium | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-06T06:08:14Z | A | KS-879 guard: the fifth control asserts a tautology — the escape's EVALUATION is untested, so the ks474 fixture can stop carrying U+0000 with every suite green |
| KS-886 | Medium | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-06T06:08:38Z | A | KS-879 guard says "repo-wide" but walks services/ + packages/ only — 749 of 1,242 files; all 148 under tests/ are outside, and tests/ is where this class has twice lived |
| KS-887 | Medium | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-06T06:19:48Z | A | KS-869 test defect (mine): the WRITE-half column-list pin can be satisfied by the COALESCE clause, so a statement missing connector_id from the column list passes all six cells |
| KS-888 | Medium | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-06T06:19:49Z | A | dbSaveApiKey SWALLOWS a failed INSERT — POST /api/keys answers 201 for a key that was never written; blast radius is ALL key persistence, not one column |
| KS-890 | Medium | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-06T06:19:50Z | B | Runbook: a code-first deploy leg must use `docker compose up -d --no-deps <svc>` and start `migrations` explicitly, last — `up -d` pulls depends_on and applied three migrations early |
| KS-891 | Medium | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-06T06:53:01Z | A | KS-873 limit: a mask desync that RE-SYNCHRONISES before EOF is still silent — the invariant closes the class only when the desync survives to EOF |
| KS-896 | Medium | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-06T07:50:17Z | A | KS-881's CONTROL is satisfied when the branch does not exist — `upstream=NONE` cannot tell an absent branch from a branch with no upstream |
| KS-901 | Medium | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-06T07:55:41Z | A | The census cell claims "the corpus misses nothing" — three further express-binding shapes are followed by neither reader, pin, nor census |
| KS-902 | Medium | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-06T07:59:40Z | A | no-tracked-credentials.sh cites two scripts as "structurally immune" exemplars — both use a WORSE cwd-relative root derivation |
| KS-903 | Medium | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-06T07:59:40Z | A | Audit the eleven cwd- and script-relative repo-root derivations under scripts/ and systemTest/ — one family, several blind in different ways |
| KS-908 | Medium | Backlog | — | — | 2026-09-06T08:43:53Z | C | connectorId persists but is invisible through the API — POST and GET both return null while the row holds the value |
| KS-910 | Medium | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-08T13:12:57Z | B | Preflight leg 12 executes ZERO suite cells — it is a reachability check, so with Actions retired no shell suite runs on a gated push |
| KS-911 | Medium | In Progress | kamil.kreiser@secuura.ai | — | 2026-09-06T12:56:24Z | D | KS-907 launcher residues: a sentinel comment describing a test that does not exist, and a 2>/dev/null placed after the append it silences |
| KS-915 | Medium | Backlog | — | — | 2026-09-06T09:24:24Z | B | A clean stack has no supported way to obtain its first privileged account |
| KS-918 | Medium | Backlog | — | — | 2026-09-06T09:52:05Z | A | vite is a production dependency of services/auth — esbuild and fsevents ship into the runtime image, imported by nothing |
| KS-919 | Medium | Backlog | — | — | 2026-09-06T09:54:49Z | B | Demo platform-admin account has mfa_enabled = false — deliberate demo posture, or a gap that outlived KS-737? |
| KS-920 | Medium | In Progress | kamil.kreiser@secuura.ai | — | 2026-09-06T11:38:18Z | C | `/shared` ships the TypeScript compiler and a 267 MB dev tree into all 24 runtime images — KS-490 closed the service tree only |
| KS-922 | Medium | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-06T11:02:27Z | A | KS-868 residue (F1): the empty-array `wait ""` at :91 logs a Stage-1 failure when ZERO jobs started — the same "we tried" lie eleven lines from its fix |
| KS-924 | Medium | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-06T10:51:34Z | A | KS-899 residues: the cardinality floor has a 23-file blind band that swallows 23 of 27 whole packages, and the SKIP pin is order-sensitive so a no-op reorder reds it |
| KS-925 | Medium | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-11T08:35:34Z | B | Launcher boot step tells every agent session to POST /api/seen as EXTRANET_ME=kam, which clears Kam's own unread flags — and the extranet is input-only |
| KS-928 | Medium | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-06T15:08:33Z | D | The demo-seed gate's predicate is tested but its CALL SITE is not — delete adminConfig.ts:1824 and every test still passes (same class as KS-914 A-2) |
| KS-930 | Medium | In Progress | kamil.kreiser@secuura.ai | — | 2026-09-08T13:11:30Z | D | KS-921 residues: five Dockerfile shapes the re-link guard cannot read, an nginx final stage it can NEVER pass, and one A_FAIL branch no test can red |
| KS-931 | Medium | In Review | kamil.kreiser@secuura.ai | — | 2026-09-09T13:00:27Z | D | safeOutboundRequest CAN throw while its own contract says it does not — and deliverWebhook lost the try/catch that used to absorb it |
| KS-933 | Medium | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-09T12:46:35Z | D | `npm run build` type-checks ZERO test files in packages/shared — the tsconfig excludes src/__tests__, so both new KS-914 test files are type-checked by no gate |
| KS-934 | Medium | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-06T11:56:14Z | A | m365 /api/teams/notify: a serial per-row loop with no LIMIT and no aggregate bound, inside the request handler — N rows x the guard's 10s default |
| KS-940 | Medium | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-06T12:42:18Z | B | Launcher suite: four side-effect and guarded-surface gaps from the KS-911/912 gate (incl. a SILENT destructive path on settings.local.json) |
| KS-941 | Medium | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-08T13:32:47Z | A | KS-923 harness: the subject guard uses -f not -r, and CELL 12 counts a SKIP as a PASS (12 passed / 11 run) |
| KS-944 | Medium | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-06T13:26:42Z | A | The gateway's auth gate reads the spec's security: [] — nothing pins the four public wallet ops, and three suites stay green if one flips |
| KS-946 | Medium | In Review | kamil.kreiser@secuura.ai | — | 2026-09-08T04:00:38Z | C | Four path spellings dodge EVERY path-scoped gateway limiter — a CLASS across all eight mounts; first act is the booted-stack experiment |
| KS-948 | Medium | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-11T02:14:38Z | D | A backtick in a shell-suite case name executes as a command and rewrote package.json mid-run — every cell still PASSED; 9 suites share the pattern |
| KS-954 | Medium | Backlog | — | — | 2026-09-06T22:37:14Z | A | KS-858 residue: the repeated-slash collapse does not complete for the /api/billing mount — leading // still 404s where /api/governance does not |
| KS-956 | Medium | Backlog | — | — | 2026-09-07T00:04:37Z | B | KS-930 residue: a whole app tree copied into a stage that names no JS runtime is still exempt — and the gate's fix-shape for it cannot be written without denying the repo's own idiom |
| KS-957 | Medium | Backlog | — | — | 2026-09-07T00:44:11Z | C | KS-930 round-2 gate residue: the guard and its suite write three claims that are false and cannot notice — a census wrong at every SHA, a clause that cannot fail, and a CONTROL that does not control |
| KS-959 | Medium | Backlog | — | — | 2026-09-09T14:11:04Z | C | KS-597 fallback: resolve the issuer org from the authenticated caller org context — BLOCKED, organization_members has 0 rows |
| KS-960 | Medium | Backlog | — | — | 2026-09-09T11:53:18Z | B | Two schema sources disagree on whether users.email is unique — a statement valid against one is 42P10 against the other, so a suite can be green on a shape that never runs |
| KS-961 | Medium | In Review | kamil.kreiser@secuura.ai | — | 2026-09-09T12:47:17Z | D | The aggregate workspace suite never runs on a PR — wire it advisory (Kam: wire-nonblocking), and it is RED on develop today |
| KS-964 | Medium | Backlog | — | — | 2026-09-09T16:12:06Z | B | 104 flat spec files in Blockchain/Dev/tests are in no runner's path — quarantine and find out, do not delete |
| KS-969 | Medium | In Progress | kamil.kreiser@secuura.ai | — | 2026-09-10T22:04:36Z | C | systemTest actor/credential path: provisioning is never invoked, so the generated-actor path never resolves — and exactly one site (the SYSTEM_ADMIN persona) can never use it |
| KS-972 | Medium | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-11T11:41:20Z | B | start-secuura.sh banner prints admin@secuura.com / admin123, which has returned 401 since PR #888 |
| KS-973 | Medium | Todo | kamil.kreiser@secuura.ai | — | 2026-09-07T23:33:30Z | C | KS-969 round-1 gate residue: the pre-suite step and its own test suite — six items on one path |
| KS-975 | Medium | Backlog | — | — | 2026-09-07T10:27:50Z | A | rateLimitScope tri-state: a MALFORMED `sub` silently became a 403 on the ungated /check, and `null` still slips through explicitScope's second line |
| KS-976 | Medium | Backlog | — | — | 2026-09-07T10:28:16Z | A | Rate-limit refusals name the wrong field: 400 says "Key required" when the key was fine, and 403 says "Caller has no tenant" when the caller has one |
| KS-986 | Medium | Backlog | — | — | 2026-09-07T21:45:49Z | B | The published admin credential survives in USER_TESTING docs while nothing on the demo seeds it any more — and the switch that would restore seeding now suspends that account |
| KS-990 | Medium | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-09T16:12:08Z | C | `npm run quality` cannot pass in systemTest/performance or systemTest/akto — two pre-existing reds unrelated to formatting |
| KS-992 | Medium | In Review | — | — | 2026-09-09T12:27:52Z | D | Both quarantine guards `rm -rf` the directory they may have failed to snapshot — an unchecked `cp` before an unconditional restore |
| KS-1003 | Medium | Backlog | — | — | 2026-09-08T11:49:08Z | B | The OAuth token endpoint is outside the credential-stuffing rate-limit zone — /api/oauth/ is not keyed in $secuura_auth_limit_key |
| KS-1010 | Medium | Backlog | — | — | 2026-09-08T12:00:22Z | B | e2e: "CIP-30 API availability check" calls a route that does not exist, and its assertion passes on the 404 |
| KS-1011 | Medium | Backlog | — | — | 2026-09-08T13:17:14Z | C | KS-666 stack marker reads "unknown" for owner/branch/commit/started_at whenever the stack is not started via start-secuura.sh |
| KS-1014 | Medium | Backlog | — | — | 2026-09-08T13:17:01Z | C | Eight containers ran images their own tag no longer pointed at — "the stack is up" says nothing about what it is running |
| KS-1015 | Medium | Backlog | kamil.kreiser@secuura.ai | Bug | 2026-09-10T11:18:21Z | C | Sweeps 2026-09-08: 28 check/operation pairs have no live owner — 18 untriaged (the /api/auth/ + /mfa/ surface has ZERO baseline coverage) and 10 citing tickets that are Done |
| KS-1017 | Medium | Backlog | — | — | 2026-09-09T13:54:06Z | D | Test-estate CLASS: a fixture that cannot discriminate certifies the bug — unmintable values, and fixtures satisfying both arms of a guard (3 instances: auth x2, originate x1) |
| KS-1018 | Medium | Backlog | — | — | 2026-09-08T20:45:19Z | B | Security/correctness: three verification-store reads swallow EVERY DB error with a bare `catch { }` and answer from an in-memory map — a DB outage reads as 'no such request' |
| KS-1019 | Medium | Backlog | — | — | 2026-09-08T21:04:47Z | D | [Question] The document's whole `blockchain` block is published as z.unknown() — undeclared to integrators, and invisible to every drift guard by construction |
| KS-1021 | Medium | Backlog | — | — | 2026-09-08T21:15:34Z | C | Deploy path: the local api-gateway serves the correct spec BY ACCIDENT over a DEAD bind mount — a restart would publish the BASE contract (KS-987/KS-659 class) |
| KS-1022 | Medium | Backlog | — | — | 2026-09-08T21:15:35Z | B | CLASS: the id-format contract seam — 79 of 83 path params are untyped and ~15 siblings answer 404 for a malformed id; needs a structural guard, not per-route .uuid() |
| KS-1023 | Medium | Backlog | — | — | 2026-09-08T21:40:57Z | B | Substrate: data_subject_requests is defined in THREE files that disagreed about processed_by's foreign key — and after KS-754 they agree for two different reasons |
| KS-1027 | Medium | In Review | kamil.kreiser@secuura.ai | — | 2026-09-09T14:03:06Z | D | KS-992 follow-ups from Peter's #904 review: restore()'s own cp is still unchecked, the refusal path deletes the partial stash, and the shared-helper item is unrecorded |
| KS-1030 | Medium | Backlog | — | — | 2026-09-09T01:33:35Z | A | KS-754 gate F-3 (MINOR): migration 048 ships with ZERO automated coverage — test:migrations is hard-wired to 044, so a migrations/ change fires a gate about a different migration |
| KS-1033 | Medium | Backlog | — | — | 2026-09-09T08:05:13Z | D | KS-926 residue: the three guards that could NOT be wired, and what each needs first — a wrong diff base, a self-contradicting default, and a whole-machine read |
| KS-1034 | Medium | Backlog | — | — | 2026-09-11T10:50:53Z | D | check-stack-safety.sh resolves the WRONG repo root inside a git hook and calls present files "deleted" — a class bug in any guard using rev-parse --show-toplevel |
| KS-1037 | Medium | Backlog | — | — | 2026-09-09T05:06:08Z | A | The NO-FORCE-PUSH rule exists only in .githooks/pre-push and in no .md — document it in CONTRIBUTING.md with its ALLOW_FORCE escape and the merge-in alternative |
| KS-1039 | Medium | Backlog | — | — | 2026-09-09T07:32:38Z | D | tests/e2e 2.4.6 'SQL injection in registration name is sanitized' asserts against an ECHO — a permanent red carrying no signal |
| KS-1040 | Medium | Backlog | — | — | 2026-09-09T07:38:35Z | D | Push preflight leg 4 reports 'a published path is unroutable' when the real cause is an exhausted login budget |
| KS-1042 | Medium | Backlog | peter@obeden.com | Bug | 2026-09-09T09:27:17Z | B | systemTest: no regression covers the KS-742 api-key tenancy class — and four authorization tests assert nothing at all |
| KS-1043 | Medium | In Review | kamil.kreiser@secuura.ai | — | 2026-09-09T09:23:46Z | B | PR #811 has no ticket — the PR-status document is a point-in-time snapshot that has gone stale; re-measure or archive before merge |
| KS-1045 | Medium | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-09T10:09:14Z | A | KINTSUGI-DEV-SERVER-PLAN.md still says the VM "has NOT been created" — Stage B ran ~3 weeks ago and the credit-expiry warning has lapsed |
| KS-1047 | Medium | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-09T15:36:53Z | A | pre-push:230 names the stack-dependent legs as (3, 4, 7); measured they are 3, 4, 8 — a comment asserting a corpus that moved |
| KS-1048 | Medium | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-09T10:47:55Z | B | CLAUDE.md's "rebuild local after any merge to develop" needs its written exception — a merge with zero buildable surface is a measured no-op |
| KS-1049 | Medium | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-09T11:11:59Z | B | A PR's Test Evidence must state whether the preflight RAN — the hook skips systemTest/docs/vault-only pushes and emits nothing at all |
| KS-1050 | Medium | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-09T11:19:48Z | D | users.ts:933 answers success: true over a 0-row profile update — KS-943 changes the symptom from stale values to undefined ones |
| KS-1053 | Medium | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-09T13:09:45Z | A | FLAKE (3rd occurrence, first with a name): ks949 seed-site enumeration fails ~1 in 7 full auth runs and passes alone — timeout hypothesis refuted |
| KS-1061 | Medium | In Review | — | — | 2026-09-09T14:03:07Z | D | F-926-2: all ten originate @secuura/shared mock factories were partial — build them from the real export list so an omission is impossible |
| KS-1063 | Medium | Backlog | — | — | 2026-09-09T20:50:08Z | B | A gate that examined NOTHING exits 0 — check-package-format reports "0 packages checked, 4 skipped" as a pass, and the hook's systemTest-only path skips in silence (third instrument in the family) |
| KS-1068 | Medium | In Review | kamil.kreiser@secuura.ai | — | 2026-09-10T01:05:15Z | D | threadToken/confidence are written onto the blockchain blob with `as any` and are absent from its type — which is why a writer could erase them with nothing complaining |
| KS-1069 | Medium | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-09T21:17:42Z | A | Gateway verify's persistedAnchored trusts the SHAPE of its inputs — a placeholder txHash, a non-boolean `simulated`, and a string/negative blockHeight all report on-chain |
| KS-1070 | Medium | Backlog | — | — | 2026-09-09T22:09:01Z | A | Tier-2 verify drops `simulated`, so the gateway's simulated guard is structurally inert on that tier |
| KS-1071 | Medium | Backlog | — | — | 2026-09-09T22:09:02Z | A | The status→confidence decision is implemented twice and the two tiers diverge — on known in-flight statuses AND on unknown ones, with opposite open defaults |
| KS-1074 | Medium | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-11T09:31:21Z | D | The poller/reconcile blob writers also erase threadToken — on the CONFIRM/heal path, not just the failure path #936 fixes |
| KS-1079 | Medium | Backlog | — | — | 2026-09-10T07:51:25Z | B | kintsugi lost demo-service to the KS-641 fail-closed gate — the flag is unset on BOTH boxes and enabling it is a one-line decision with no owner |
| KS-1085 | Medium | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-11T08:20:35Z | B | Launcher preflight: four findings — a concurrent seat clobbers the warnings file, KS-907 miscounts sessions, F-02 names a missing key, rule 7 still says extranet |
| KS-1091 | Medium | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-11T09:54:11Z | B | KS-1041 residual: the cross-tenant JWT probe on originate's direct path — reasoned, never run, not commissioned |
| KS-1096 | Medium | In Progress | peter@obeden.com | Bug | 2026-09-11T18:19:59Z | B | start-secuura.sh's health wait, --status and DB/Redis checks probe slot 1's container names on every slot — false "Timeout after 120s / PostgreSQL not accepting / Redis not responding" on slots 2–4 |
| KS-1098 | Medium | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-11T19:07:17Z | A | k6 runner echo mask: -e=NAME=VALUE and -qe NAME=VALUE still print the value, contrary to its JSDoc; the name set and BASE_URL userinfo are open; PASSWD is unpinned (QA-958-1..3) |
| KS-1101 | Medium | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-12T00:30:38Z | A | Gateway health aggregates read anchoring's HTTP status only, so its degraded body (#728) never reaches /health/deep, /system/status or the health dashboard |
| KS-1102 | Medium | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-12T00:30:40Z | B | Unauthenticated /system/status, /api/system/status and /api/system/health/dashboard publish internal service URLs, ports, versions and which third-party keys are unset |
| KS-1103 | Medium | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-12T00:30:43Z | A | POST /api/verification/verify validates the published 'hash' field but never reads it — a spec-valid body gets 400 'Please provide a content hash…' |
| KS-1104 | Medium | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-12T00:30:44Z | A | Verifier mode tabs (Upload File / Enter ID / Scan QR) lose their accessible name at phone width — WCAG 2.1 SC 4.1.2 |
| KS-1105 | Medium | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-12T00:30:45Z | A | Admin login placeholder shows the SYSTEM_ADMIN seed address admin@secuura.com (frontend/admin/src/pages/Login.tsx:81) |
| KS-1108 | Medium | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-12T03:24:00Z | A | Akto harness: loadSecretsYml() parses config/secrets.yml with no catch — the KS-1099 shape, whole-file print not yet measured in this package |
| KS-339 | Low | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-02T10:24:57Z | B | Grant Phil + Steve extranet access (evolve toward company source of truth) |
| KS-623 | Low | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-07T03:57:35Z | A | Test-token env guard is asymmetric: the gateway fails closed on an unset NODE_ENV, the auth service fails open |
| KS-648 | Low | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-05T23:53:09Z | B | Frontend CSP quality: issuer alone carries 'unsafe-eval', and all three portals allow 'unsafe-inline' styles |
| KS-744 | Low | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-05T23:52:57Z | A | Gateway 500s on every proxied route for a token lacking verificationLevel — auth.ts:377 sets the header unguarded |
| KS-748 | Low | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-05T23:52:55Z | B | svc_api_keys.organization_id is not a tenancy boundary and nothing keeps it coherent with tenant_id — an incoherent pair is storable |
| KS-749 | Low | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-07T03:57:35Z | C | postcss-selector-parser 6.1.2 carries GHSA-w9m9-85wc-3x92 — baselined to unblock the preflight; the override was inert |
| KS-793 | Low | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-05T23:52:39Z | C | BACKLOG.md:7 claims 2 of 27 auth test files fail at import — they do not on develop |
| KS-811 | Low | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-07T12:19:51Z | A | Nothing asserts #815's 403 code SET against what the route actually throws |
| KS-812 | Low | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-05T23:52:35Z | A | connectors/whatsapp-bot prints the DEAD Container Apps API URL as its default target |
| KS-834 | Low | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-05T20:03:13Z | B | [Decision] POST /api/certifications/:id/verify has no auth handler — leave it public, or gate it? |
| KS-840 | Low | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-05T23:52:30Z | B | The OAuth error code travels in error.message and the contract never says so; and authorize refusals answer JSON where RFC 6749 redirects |
| KS-846 | Low | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-05T23:52:10Z | B | `@secuura/shared` `main` points at an untracked, never-built `dist/index.js` — anything outside vitest's alias resolves to nothing |
| KS-884 | Low | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-06T06:02:28Z | A | pre-push resolves the bare name `develop`, so a TAG named develop beats the branch — and --quiet suppresses the ambiguity warning |
| KS-894 | Low | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-06T06:53:36Z | A | toHaveLength(1) on offendingListenSites is satisfied by the ANNOUNCEMENT row alone — the shape does not distinguish found-a-site from did-not-understand |
| KS-895 | Low | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-06T06:53:48Z | A | The mask-desync announcement blames a regex literal for every class — an unclosed ${ } is reported as a regex problem |
| KS-897 | Low | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-06T07:50:18Z | A | build_fixture swallows its own failure — `>/dev/null 2>&1` makes a fixture that did not build indistinguishable from one that did |
| KS-900 | Low | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-06T07:55:30Z | A | The `default` export skip makes a default-only factory silent — it leaves the answer entirely instead of being reported as unreachable by name |
| KS-906 | Low | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-06T07:59:42Z | A | CASE 6's `cd /tmp` is inert — the leg uses `git -C "$DEV_DIR"`, so the case does not test what its name says |
| KS-912 | Low | In Progress | kamil.kreiser@secuura.ai | — | 2026-09-06T12:56:24Z | D | KS-907 suite residues: CASE 2 never asserts the pruning it is named for, a cell count printed as a launcher-run count, and a grep -qc diagnostic |
| KS-965 | Low | Backlog | — | — | 2026-09-07T08:04:18Z | C | 87 documentary sites still publish the retired admin credential — wrong rather than dangerous, clean up after KS-964's code items |
| KS-979 | Low | Backlog | — | — | 2026-09-07T11:26:44Z | A | KS-597's own bind test file repeats two claims that were corrected in the product file |
| KS-980 | Low | Backlog | — | — | 2026-09-07T11:26:44Z | B | The KS-597 integration suite claims two RLS-permissive paths and exercises one — platform_bypass never reaches its own mechanism |
| KS-1006 | Low | Backlog | — | — | 2026-09-08T11:24:02Z | A | POST /api/users/me/mfa/disable skips code verification when mfaSecret is falsy — the second door |
| KS-1072 | Low | Backlog | — | — | 2026-09-09T22:09:02Z | A | The latest-anchor selector documents a `confirmedAt` tiebreak it does not implement — and since KS-1057 that selector decides the verdict |
| KS-1073 | Low | Backlog | — | — | 2026-09-09T22:09:03Z | A | Tier-2 verify has no statusless-blob cell — the carve-out is unguarded on the tier a third party reaches |
| KS-1082 | Low | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-10T22:04:35Z | B | The Playwright env guard added in #896 reads config/ only — the variable breaking the CI run is read from fixtures/ and appears in no template |
| KS-1088 | Low | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-11T02:14:36Z | B | run-shell-suites.sh restores git discovery but does not isolate suites: a suite that runs git from its cwd writes the repository it runs in (KS-1086 QA-6) |
| KS-1089 | Low | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-11T04:12:22Z | A | run-shell-suites.sh polish from #953's tier-2 gate: make `--list` survive a tree with no suites on bash 3.2 (QA-8, `:72`) and give the git-list refusal a headline per cause (QA-7) |
| KS-1090 | Low | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-11T09:34:54Z | A | api-gateway + originate: tsc never type-checks #951's three wiring tests, and the mint-scope test pins 2 of 17 non-originate keys |
| KS-1097 | Low | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-11T13:11:36Z | B | Merge-rule docs after #957: the v4 footer and two gate statements gloss TESTED weakly, 'the reviewer' has no referent, one sentence lets a person sign off (QA-957-1..5, W-2) |
| KS-1106 | Low | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-12T00:30:46Z | A | Verifier shows 'Verification Failed' / 'INVALID' for an id that is not in the registry, with no next step |
| KS-984 | No priority | Backlog | peter@obeden.com | — | 2026-09-09T16:01:48Z | B | No service exposes /metrics — the secuura-services scrape job has never collected a single series on any slot |
| KS-985 | No priority | Backlog | peter@obeden.com | — | 2026-09-09T16:01:52Z | B | Eight dashboards show a slot picker that filters nothing — latent today, wrong the day /metrics lands |
| KS-1083 | No priority | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-11T00:19:35Z | B | GATEWAY_VOUCH_SECRET: nothing provisions it and no deploy order or rotation is written — #951's control ships inert, and a gateway/originate mismatch drops gateway identity |
| KS-1084 | No priority | Backlog | kamil.kreiser@secuura.ai | — | 2026-09-11T00:19:35Z | A | READ ONLY / unverified: the gateway's own Authorization-only calls to originate send no x-tenant-id — single-tenant originate may scope them to DEFAULT_TENANT_ID |
| KS-1093 | No priority | Backlog | — | — | 2026-09-11T10:50:53Z | C | check-stack-safety.sh 6f reports a FALSE red once a real Playwright run exists — git check-ignore refuses a path beyond the latest-slot<N> symlink |

## GAPS
- **GitHub Actions status.**
  - The `check-runs` and `actions/jobs` endpoints returned HTTP 403 for GH_TOKEN.
  - So I could not see whether the "Playwright suite" job still dies at the lint step (KS-1076), nor the CI state of any PR.
  - The KS-1076 "already fixed" reading comes from `git show`/`git log --first-parent` of `global-setup.ts` at 4554b25e2 only. ESLint was not run.
- **No tests, linters or tsc were run** (read-only brief).
  - Every "red on develop" / "still live" claim is the ticket's own.
  - Exception: where a git grep at 4554b25e2 confirmed the code shape (listed in the A family column).
- **Linear comments.**
  - Read for about 150 candidates only, last 4 each, keyword-filtered; the full description was keyword-scanned for the same set.
  - The other ~230 tickets were classified from title + the first 600 chars of the description (+ state/assignee), without comments.
  - A ruling recorded only in an older comment could be missed there. Those tickets mostly landed in B/C/D, so the risk is in the conservative direction.
- **D counts body mentions.**
  - That is literal to the brief, but many PR bodies cite tickets as context: #874 is a docs catalogue, #720 edits BACKLOG.md, #918 cites KS-1032/1033/1034.
  - D(body) is not proof the fix is in flight.
- **Not read:**
  - PR review/approval state and mergeability.
  - The QA-gate reports under `Testing Agent MAIN/…/reports/` cited by several tickets.
  - Linear parent/sub-issue trees for non-candidates.
- **Peter's local work** beyond pushed #959 is unknown. Other seats' unpushed worktrees are unknown too; `ls-remote` sees pushed branches only.
- **Dependabot lockfile PRs** were not diffed per file. Lanes simply forbid lockfile edits.
- **KS-730's site table** (2026-09-01) was not re-counted. A git grep for `details: { details: err.message }` also hit `api-gateway/src/routes/admin.ts`, which the ticket's table does not list.
- **KS-1098** was not examined, per instruction.
