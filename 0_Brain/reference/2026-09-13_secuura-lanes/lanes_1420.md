# Secuura/Blockchain — four disjoint builder lanes for seats -B/-C/-D/-E (read-only, 2026-09-13 ~14:40 AEST)

develop = `721b333a6` (local `origin/develop` and live `ls-remote` agree; tip = KS-1029 #962). Open PRs on develop today: **52** (GitHub REST, 1 page). Instruments: Linear GraphQL, GitHub `/pulls` + `/files`, read-only git at `721b333a6`. Nothing fetched, checked out, written or posted. **[S]** = READ at source today · **[R]** = RELAYED (sweep / census / brief).

**Off-limits (all lanes):** `originate/src/routes/verification.ts` + `__tests__/ks1103-*` (#965) · `vc-issuer/src/routes/presentations.ts` + `__tests__/ks1020-*` (#966) · `api-gateway/src/routes/verification.ts` + `__tests__/ks1071/1070/1069/1057-*` (#967/#968/#969) · `systemTest/performance/utils/yaml.ts` + `tests/unit/utils/yamlRedaction.test.ts` (#963) — and every sibling in those `routes/`, `__tests__/`, `utils/` dirs. Standing [R, re-confirmed against today's PR files S]: `docs/openapi/secuura-api.yaml`, any `package.json`/lockfile, `.github/workflows/`, `Start_Up/`, `check-stack-safety.sh`, `CONTRIBUTING.md` (#959), `scripts/preflight/*`, `run-code-guards.sh`, `check-shared-relink.sh`, `.githooks/pre-push`.

## Lane B — api-gateway boot loader/seed: one seat owns #932 AND #928 (KS-1062 · KS-950 · KS-962)
- **Tickets [S]:** KS-1062 High · In Review · unassigned · PR #932 `c72607d58` UNGATED, clean. KS-950 High · In Review · kamil · PR #928 `e28d64b8d` GO WITH FINDINGS but HELD (Wednesday 2026-09-12 05:56: rework = loader half + KS-962 shape, re-gate). KS-962 High · Backlog · unassigned; "✅ THE RATIFIED SHAPE — remove the INSERT" (Wednesday 2026-09-07) + the required test contract.
- **Files:** `Blockchain/Dev/services/api-gateway/src/startup-migrations.ts` (the only file in BOTH PRs [S]); new `Blockchain/Dev/scripts/__tests__/ks949_main_seed_idempotence.test.sh` (named by KS-962; absent at develop [S]). develop has not touched `startup-migrations.ts` since either base `d4cf7e3cf` [S git log].
- **Why one lane:** #932 and #928 edit the SAME hunks (`migrateDatabase` :800–:840, tenant loop :952/:1024/:1108–:1116 [S diff -U0]); KS-950's READY-FOR-QA note claims the tenant `migrated++` fix that is KS-1062's whole subject. Sequence: gate #932 → merge; rebase #928, drop its duplicated loader half, seed half → KS-962 shape (delete INSERT; PK target only re-syncs `tenant_id`/`tenant_slug`), write the ks949 suite (both seeders, one real Postgres, both orders, `isEncryptedPii` NOT stubbed, control cell) → re-gate → merge. Worktrees `ks950`/`s162-ks-updateuser` mtime 2026-09-09 — no live seat [S].
- **Must NOT touch:** `api-gateway/src/routes/`, `api-gateway/src/__tests__/`, `services/tenant-provisioning/` (KS-1055), `docker/init/01-schema.sql` (#905), `migrations/` (KS-1054/1055 need Kam), lanes C/D/E paths.
- **Open-PR collisions:** #932 ↔ #928 only, both owned here; nothing else touches either file [S].
- **Outside help:** NO — Peter's hold was "seed ≠ ratified shape"; the shape is Wednesday's; Wednesday's GO at head SHA is the approval (CLAUDE.md merge flow, 2026-09-11 [S]).
- **Closes with:** #932 tier-1 gate + merge → KS-1062; reworked #928 tier-1 gate (real DB) + merge → KS-950 + KS-962. Three High.

## Lane C — auth `userRepo.ts`: rebase + re-gate #913 (KS-963 P1), then rebase + gate #930 (KS-1052)
- **Tickets [S]:** KS-963 **Urgent** · In Review · kamil · PR #913 `fdd8af79d` GO WITH FINDINGS 2026-09-09 [R], clean [S]. KS-1052 High · In Progress · kamil · PR #930 `7e5ae31d8` round 2 pushed 2026-09-09 14:14, no gate at head, **dirty** [S].
- **Files [S]:** #913 = `Blockchain/Dev/services/auth/src/repositories/userRepo.ts` + `__tests__/ks963-preauth-rethrow.test.ts`. #930 = same `userRepo.ts` + `routes/{auth,mfa,users}.ts`, `services/passwordLoginGate.ts`, tests `ks1052-*`, `ks781-login-authorize-agree`, `ks781-oauth-authorize-mfa-bypass`.
- **Rebase proof [S]:** since #913's base `f9296f9ea`, develop changed `userRepo.ts` in `a45204ac9` (KS-732 #872) and `9e13a434f` (KS-943 #929); head→develop diff on the file 77+/28−. The 09-09 gate never saw this base.
- **Why one lane:** both PRs share `userRepo.ts`; whichever merges first forces the other's rebase. #913 first (2 files, P1) → re-gate → merge; then rebase #930 → gate (its round-2 answer to the NO GO was never gated) → merge. Branch `feature/ks-963-f3-structural-cells` (`f7cb7f644`, +2 commits, "pushed for RECOVERABILITY only" [S]) — seat checks whether they answer Peter's #913 review (1 substantive + 2 housekeeping, mirrored on KS-963 09-09 12:54 [S]); not approval-class.
- **Must NOT touch:** `auth/src/routes/oauth.ts` + its tests (#881, Peter CHANGES_REQUESTED), `auth.openapi.ts`, `auth/tsconfig.json` (KS-1000), `docs/openapi/`, lanes B/D/E.
- **Open-PR collisions:** #913 ↔ #930 on `userRepo.ts`, both owned here; #881 touches other files [S].
- **Outside help:** NO (widening Kam-ruled 2026-09-09 07:08 "include" [S]).
- **Closes with:** rebased #913 re-gate + merge → KS-963; rebased #930 gate + merge → KS-1052 (KS-1050 only if the PR body covers it — verify).

## Lane D — `Blockchain/Dev/packages/shared/src/__tests__/` guard-instrument residues (10 tickets, 5 files, 1 dir)
- **Tickets [S] (all Backlog · kamil · 0 comments; files by `git grep`/`ls-tree` at 721b333a6):**
  `ks860-test-listeners-bind-loopback.test.ts` → KS-876 P3, KS-891 P3, KS-894 P4, KS-895 P4 · `ks879-no-raw-control-bytes-repo-wide.test.ts` → KS-885 P3, KS-886 P3 · `ks781-p3-3-body-parser-order.test.ts` (only file with `LEG F`/`PARSER_FACTORY_NAMES`) → KS-828 P3, KS-900 P4, KS-901 P3 · `entrypoint-corpus.test.ts` + `entrypoint-corpus.ts` → KS-924 P3.
- **Proof:** `npm test` in `packages/shared` (vitest), red-first cell per ticket.
- **Must NOT touch:** `src/security/ssrf-guard.ts` + `__tests__/ks914-shipped-path.test.ts` (#873); `src/index.ts`, `src/middleware/index.ts`, `src/security/keyRevokePolicy.ts`, `__tests__/ks764-*` (#799); `src/openapi/examples/fixtures.ts`, `__tests__/ks256-*` (#922); `package.json`; no product file anywhere (a widened walk that newly flags a product file = a finding to file, not a fix here).
- **Open-PR collisions:** none on the five files [S] (same dir as #799/#873/#922 tests, different files).
- **Outside help:** NO — every description carries its fix shape, no ruling words [S].
- **Closes with:** 3–4 PRs grouped by file + tier-2 gate + merge → up to 10 tickets. Best count-per-seat.

## Lane E — CI harness shell scripts (reserve R2; 5 × P3, fix shapes given)
- **Tickets [S] (all Backlog · kamil):** KS-922 `Blockchain/Testing/ci/orchestrate.sh:91` (+ cell in `orchestrate_jobs.test.sh`) · KS-941 `Blockchain/Dev/scripts/__tests__/orchestrate_jobs.test.sh:47` · KS-878 `Blockchain/Testing/jobs/09-aggregate-report.sh` · KS-867 `Blockchain/Testing/jobs/04-container-trivy.sh` · KS-877 `Blockchain/Dev/scripts/docker-build.sh:162`. All five present at develop; no branch for any (348 remote heads; positive control ks-1062/950/963 = 5 hits) [S].
- **Proof [R]:** `bash Blockchain/Dev/scripts/__tests__/orchestrate_jobs.test.sh` under macOS `/bin/bash` 3.2, red-first.
- **Must NOT touch:** `scripts/preflight/*`, `run-code-guards.sh`, `__tests__/run_code_guards.test.sh` (#903/#918/#924/#925); `check-shared-relink.sh` + test (#879); `scripts/spec-examples/` (#922); `check-stack-safety.sh`, `__tests__/start_secuura_slot_names.test.sh` (#959); `.githooks/` (#903); `Testing/ci/aggregate.ts`; Lane B's new `scripts/__tests__/ks949_*.sh`.
- **Open-PR collisions:** none; `Blockchain/Testing/` has zero open-PR files [S].
- **Outside help:** NO. **Closes with:** 1–3 PRs + tier-2 gate + merge → 5 tickets.

## Disjointness (shared paths)
| | B | C | D | E |
|---|---|---|---|---|
| **B** `api-gateway/src/startup-migrations.ts` · `scripts/__tests__/ks949_*.sh` (new) | — | none | none | none (same dir `scripts/__tests__/`, different named files — carve-out in both briefs) |
| **C** `services/auth/src/{repositories,routes,services,__tests__}/` (#913+#930 files) | none | — | none | none |
| **D** `packages/shared/src/__tests__/{ks860,ks879,ks781-p3-3,entrypoint-corpus}*` | none | none | — | none |
| **E** `Blockchain/Testing/{ci,jobs}/` · `scripts/docker-build.sh` · `scripts/__tests__/orchestrate_jobs.test.sh` | see B | none | none | — |

None touches the off-limits set, `systemTest/performance/`, `docs/openapi/`, `.github/workflows/`, or a lockfile. For strict directory-disjointness, swap E for R1.

## Ready spares (disjoint from B–E and each other)
- **R1 frontend:** KS-1104 P3 `frontend/verifier/src/components/VerifyPage.tsx`, KS-1105 P3 `frontend/admin/src/pages/Login.tsx:81`, KS-1106 P4 `frontend/verifier/src/components/ResultPage.tsx` [S]; open PRs on `frontend/` = dependabot `package.json` only [S]; verifier has `lint` only, no test script [S] → lint + build + a11y tree at 390×844 [R]. Closes 3.
- **R3 akto:** KS-1108 P3 `systemTest/akto/src/config/secrets.ts:40`, KS-755 P3 `src/core/runDir.ts` + `tests/unit/core/runDir.test.ts` [S]; zero open-PR files under `systemTest/akto/` [S]. Closes 2.
- **R5 kyc:** KS-849 P3 `services/kyc/src/index.ts`, KS-848 P3 `services/kyc/tsconfig.json` [S]; `vitest run` present; open PRs = dependabot only [S]. Closes 2.

## Post-merge only (seat launched after s200's merges)
- **KS-1110** P4 Backlog kamil (QA-960-2): `systemTest/performance/tests/unit/config/sheddingCeiling.test.ts`, `tests/unit/package_scripts.test.ts` + new js-yaml guard; imports `readYaml` from `utils/yaml.ts` which **#963 changes** → after #963 merges. File-disjoint from #916 (`runner/actor_manifest.ts`) and #961 [S].
- **R4 gateway health/status:** KS-1101 `api-gateway/src/services/health.ts`, KS-864 `api-gateway/src/routes/system-status.ts` (+ 09-12 comment) [S] — `routes/` is adjacent to #967–#969 → after #969.
- **KS-730** High: its sites include `api-gateway/src/routes/verification.ts` (3) and `originate/src/routes/verification.ts` (2) [S git grep]; `adminConfig.ts` (50) is in #799 → after the train.

## Rejected
- **KS-1076** P1 Todo, 0 comments [S]: not a builder lane. Item 1 (4 jsdoc errors in `systemTest/playwright/global-setup.ts`) is ALREADY on develop — `6a047445b` via #896 merge `38a919d40` 2026-09-11; `@param/@throws/@example` present at 721b333a6 [S]. Item 3 = `.github/workflows/` (Kam). Item 2 = run the suite on a named slot + report: verification-only, no edits → attach to any seat with a slot, or close on the 6a047445b evidence.
- KS-1069 (In Progress 02:44 today, #969), KS-1072/1073, KS-979, KS-1090 — off-limits files or their siblings [S].
- KS-745, 870, 871, 954, 744 — `api-gateway/src/routes/` + `middleware/` siblings of the merge files → post-merge.
- KS-810, 823, 805, 838, 938, 999, 1005, 1006 — auth files held by #930 (Lane C) / #881 (Peter CHANGES_REQUESTED).
- KS-932, 974, 975, 976, 888, 880, 887 — `ssrf-guard.ts` (#873) / `services/security/src/*` (#799/#880; KS-698 In Progress).
- KS-998, 1047, 884, 896, 897, 906, 902, 1037 — `.githooks/pre-push` (#903), `scripts/preflight/` (#903/#918/#925), `pre_push_hook_base.test.sh` beside the #903 hook change, `CONTRIBUTING.md` (#959).
- KS-528, 530, 918 — package.json/lockfile edits (dependabot, #937).
- KS-825, 1053 — flake investigations without a fix shape; `auth/src/__tests__/` is Lane C's dir.
- KS-1030, 824 — migrations / `docker/init` (KS-1054/1055 context; #905). KS-704 — `systemTest/performance/runner/`+`gate/`. KS-784, 934 — m365, size unknown.
- KS-844, 812, 865, 766, 1045, 1089 — valid singles, lower count-per-seat than D/E; fillers if a seat finishes early.

## Could not verify
- Liveness of any seat on worktrees `ks950`, `s162-ks-updateuser` etc. — mtimes only (Sep 9); `git worktree list` refused to me.
- Whether GitHub Actions still runs on PRs (CLAUDE.md: retired 2026-08-27; KS-1075/1076 describe PR jobs on 09-10) — bears on KS-1076 item 3 only.
- "#928 HELD" and "#913 needs rebase" came from the brief; both independently re-derived (Wednesday's 05:56 comment; `git log` on `userRepo.ts`).
