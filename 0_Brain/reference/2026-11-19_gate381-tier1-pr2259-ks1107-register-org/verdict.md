PR 2259: GO WITH NOTES (at head a0e58b942c22e5ca7c9dff216fe17c243f2e3548; tier 1)

QA GATE 381, tier 1 (Opus), Secuura/Distributed_Secuura PR 2259 "Refs KS-1107: register refuses a caller-chosen organizationId".
Pinned by gh api at the start and again at 10:55:36Z: head a0e58b942c22e5ca7c9dff216fe17c243f2e3548, open, not merged; base and develop both 86bfeda9e3e10256e8811778621ce3390e1aa22b; one commit; 6 files +247 -4.
Findings only. Nothing posted, mailed, pushed, merged or written to Linear or GitHub. Nothing written under !CODING (git read verbs, `cp -Rc` of node_modules out of the builder's tree, and gh api reads only).

Where the evidence is: `scratch/evidence/` in this folder (t1 to t6 runs, mut_G1..G7, mutants_summary.txt, pr_body.md). Own clone: `scratch/head` (clone --shared of the builder's s-w39-ks1107, detached at a0e58b942c22) plus worktree `scratch/dev` (86bfeda9e3e1). node_modules (root, services/auth, packages/shared, services/shared) cloned with APFS clonefile from the builder's tree; `@secuura/shared` rebuilt with its own `tsc` in each of my trees (rc 0). Probe file and copied test files moved to `scratch/_quarantine/` after use; both trees `git status` clean afterwards; auth.ts blob restored to e9908ad070bc after every mutant and the planted tsc control (git hash-object).
Runtime: Node v26.8.1 (not LTS; nothing measured on Node 24), vitest 4.1.12, zod 4.6.7. Every test run at load1 under 8 (one wait for the load to drop before tsc).

## Findings, by severity

None Major. None blocks the ticket's claim.

| # | Severity | Finding |
|---|---|---|
| F1 | Minor (test gap) | The PR's 9 cells use JSON bodies only. My mutant G2 (refuse only when Content-Type is JSON) passes all 9. Only my form-body probes P1/P2 kill it. The code itself refuses form bodies (measured). Suggest adding one form-encoded cell. |
| F2 | Note (pre-existing; separate ticket candidate, for Kam) | The INVITED-stub claim (KS-74) asks for no proof that the caller owns the email. Anyone who knows an invited address can claim the stub: it becomes ACTIVE with emailVerified false, and login does not check verification. On the next refresh or login they inherit whatever organisation an admin has PATCHed onto that stub. The caller cannot choose the organisation, and stubs are created without one (`createInvitedStub`). So this is not the KS-1107 defect, but it is a second way into an organisation that skips the admin's intent. Not changed by this PR. |
| F3 | Note (pre-existing; stated in the PR body) | On a stub claim the register token carries no organisation, even when the stub row has an admin-set one (P12). Same on develop for a body without the key. Refresh re-reads the row (`auth.ts` refresh → `getUserByIdPreAuth`), so the next token is right. |
| F4 | Note (production question, for Kam) | The existing-accounts query in the PR body is a sound CANDIDATE design. It cannot be conclusive (detail under Q5). |
| F5 | Nit | The PR body says Platform S was not read twice: in the Summary and again in the NOT run list. The ruling said once. Both say the same thing. |
| F6 | Low | Of the skipped hook legs, 3 and 4 do not bear on this change. Leg 8 bears only nominally (one description string in the YAML changed); leg 1 and check:openapi did run. |

## Q1: Is the hole closed on the register route? YES

FOUND
- At head, `auth.ts:196`: `if (req.body && typeof req.body === 'object' && 'organizationId' in req.body) throw new ValidationError(...)`. It runs after the KS-82 role check (`:184`) and before `registerSchema.parse` and any read or write. `organizationId` is removed from `registerSchema` (which is `.strip()`) and from the `user` literal. The `user` object is built field by field. Nothing in it comes from `data` or the body except the names, email, password and clientType.
- zod 4.6.7, read in my clone's node_modules (`zod/v4/classic/schemas.js:872` and `v4/core/schemas.js:1055-1083`). `.strip()` sets `catchall: undefined`. The parse builds a fresh `{}` and copies only the shape's own keys (it skips `__proto__`). With no catchall it returns before `handleCatchall`. So no key that is not in the shape can reach `data`, whatever its spelling.
- The only paths from the body to the org claim were `data.organizationId` → `user.organizationId` → `generateAccessToken`/`generateRefreshToken` (`services/jwt.ts:197`, `:223`) and `createUser` (`userRepo.ts:724`). Both are gone.
- Headers. The auth service reads exactly `x-tenant-id` and `x-tenant-slug` (census of every `headers[...]`, `req.get(...)` and `req.header(...)` in auth/src, tests excluded). Those set the TENANT, not the organisation. No org header is read. The gateway strips client `x-(user|tenant|organization|org|role…)-*` headers (`api-gateway/src/utils/trustHeaders.ts`). It honours `x-tenant-override` only on an authenticated platform-role token (`middleware/auth.ts:765`), and auth never reads that header. Calling the auth service directly, bypassing the gateway, still lets the caller set x-tenant-id. That is pre-existing, marked F-04-allowed, concerns tenant not org, and is outside this PR.
- Body parsers, per auth `index.ts:90-91`: boundedJson, then `express.urlencoded({extended:true})`. The refusal does not depend on content type.

TESTED
- The PR file at head: 9/9 (`t1`). Red-first on develop with the same file copied in: 4 failed, all by assertion, with exactly the builder's messages (R1/R3 `expected '3f1c…1107' to be undefined`, R2 `expected 201 to be 422`, R4 `expected 400 to be 422`). The 5 controls passed (`t2`).
- My 22 probe cells (`t3`, file in `scratch/_quarantine/head/g381-probe.test.ts`). The harness mirrors index.ts body parsing (boundedJson and urlencoded extended), uses the real router, error handler and RS256 signer, and mocks the same repo as the PR. At head, 22/22:
  - Refused with 422: form `organizationId=ORG` (P1) and `organizationId[id]=ORG` (P2); JSON values `[ORG]`, `{id}`, `''`, `0`, `false` (P8); stub claim with a different org (P13).
  - 201 with no org in the token and none written: form `__proto__[organizationId]` (P3); JSON `"__proto__":{organizationId}` (P4); `constructor.prototype.organizationId` (P5); Object.prototype checked unpolluted after P3 to P5.
  - Same result for the spellings `organisationId`, `organization_id`, `orgId`, `org`, `tenantId`, `OrganizationId`, `organizationID`, `organization`, `" organizationId"` (P6); nested `organization:{id}` and an array `organizationIds` (P7); a query string (P9); headers `x-organization-id`, `x-org-id`, `x-tenant-override`, `x-user-organization` (P10); a text/plain body (P11).
  - Stub with an admin-set org (P12): 201, no body org written, token org undefined.
- Control: the same probe file on develop. P1, P2, P8, P13 and P14 failed, so the probes can go red, and the hole existed on form bodies too. The P6/P7/P9/P10 spelling, header and query probes pass on develop as well; the hole was only the exact key. `tokenOrg` is the PR's helper, and R1 on develop shows it detects a claim.

NOT TESTED: a booted service, the real gateway proxy or live stack; a real Postgres (the ON CONFLICT clause that keeps a stub's organization_id was read in `userRepo.ts:695-701`, not executed); multipart bodies (no multipart parser is mounted on auth, by reading).

HOW: `vitest run --reporter=verbose --root <auth> <file>` in my clone (TMPDIR /private/tmp/g381t). Develop control by copying the file into the `dev` worktree.

The legitimate invite flow still works: C2 (PR) and P12 (mine) both return 201. `updateUserOrThrow` is called once, with no org. The row's org is kept, by reading the SQL. Whether an admin-set stub org reaches a token is not tested anywhere at the database level (F3).

## Q2: Sibling doors. None with the same defect.

FOUND (census by the WRITE)
- Searched with `git grep` over head, in Blockchain/Dev/{services,packages,shared}, excluding tests: `INSERT INTO users`, `UPDATE users`, `organization_id =` assignments, and migrations for functions or triggers that set organization_id.
- Sinks found, and their callers:
  1. `userRepo.createUser` (organization_id from `user.organizationId`). Callers:
     - register (fixed);
     - `POST /api/users/admin/create` (admin only; sets no org);
     - `createInvitedStub` (no org);
     - wallet sign-up (`wallet.ts:212`, no org);
     - social sign-up (`auth.ts:1331`, no org);
     - demo seeder (no org).
  2. `userRepo.updateUser` through its fieldMap `organizationId → organization_id`. The only caller that passes organizationId is the admin `PATCH /api/users/admin/:id` (role gate at `users.ts:701`, KS-467 org-exists and same-tenant check at `:806`). `PATCH /me` copies four named fields only. The social link `updateUser({[`${providerName}Id`]: …})` is limited to the provider allow-list, which has no 'organization'.
  3. Gateway identity seed, `INSERT INTO users … organization_id` (`api-gateway/src/routes/admin.ts:1269`): constant demo rows, behind `requireAdmin` and `enableDemoSeed`.
  4. originate demo seed `INSERT INTO users` (`adminConfig.ts:2155`): no org column.
  5. Migrations: zero functions or triggers set organization_id (control: 88 organization_id lines are present).
- `internal.ts` /connector-token mints an org claim from the security service's validated sk_ key. It does not write a user, and the org comes from the key, not the caller.
- No open-to-strangers door with the same defect. The nearest relative is F2 (the stub claim without proof of the email), which is not caller-chosen.

NOT TESTED / outside the frame: Platform S (outside this repository); frontends (they write no rows); the Prisma client (no `user.create/update/upsert` found in services or packages); any database role or manual SQL in production.

## Q3: Nothing else changed. CONFIRMED

- KS-82 block: the diff adds lines only after it, so it is byte-unchanged and still runs first. C4 at head passes. My mutant G5 (organisation check first) is killed by C4.
- `users.ts` (KS-467) is not in the diff. Files changed: auth.ts, auth.openapi.ts, secuura-api.yaml (one 422 description), the new test file, and two fragments.
- The 422 body (P14, verbatim): `{"success":false,"error":{"code":"VALIDATION_ERROR","message":"organizationId is not a permitted field on /register — an account is created with no organisation and assigned to one by an admin via PATCH /api/users/admin/{id}"}}`. It names nothing internal beyond the PATCH route.
- A normal register token carries no organisation (C1, and P6/P9/P10 at head). For a body without the key this matches develop, so other services see the same null-org user as before.
- Consumer census claim, checked myself: the admin form `frontend/admin/src/pages/Users.tsx:277-306` always sends `role: formData.role`, so it is refused by KS-82 before the organisation check. `tests/e2e/tests/cross-persona-e2e.prelaunch.spec.ts:262-268` sends `role: 'issuer'` with British `organisationId`. Issuer portal `api.ts:397` and mobile `AuthContext.tsx:142` send email, password and name only. `insurance-test-runner.js:187` sends role and tenantId. systemTest sends role. The builder's census holds.

## Q4: Tests honest. YES, with F1

- Red-first and green figures are reproduced exactly (Q1).
- Whole auth suite at head, run once with cwd set to services/auth (`npm --prefix <auth> run test -- run`): **1,938 of 1,938 in 160 files**, rc 0, failure-name set empty (`t5`).
  - An earlier run with `--root` and cwd elsewhere gave 1,923/1,925 plus one file that failed to load (`t4`). All of those failures were cwd artefacts in ks1009 and ks1467 ("could not locate the Dev root", ENOENT on a cwd-relative path), not product failures.
- The develop-arm whole suite was not re-run (not commissioned); the builder reports 1,929/1,929.
- tsc `--noEmit -p services/auth/tsconfig.json` at head: rc 0, 0 lines. Planted control (`const x: number = "x"` appended to auth.ts): rc 2, TS2322 plus TS6133. Restored, blob e9908ad070bc (`t6`).
- My mutants. Each was run against the PR file and my probes, then restored (`mutants_summary.txt`, `mut_G*.txt`):

| Mutant | Killed by (PR's cells) | Killed by (my probes) |
|---|---|---|
| G1 refuse only a GUID value | R4 | P2, P8 |
| G2 refuse only on JSON content type | **none (survives)** | P1, P2 |
| G3 strip instead of refuse | R1, R2, R3, R4 | P1, P2, P8, P13, P14 |
| G4 refuse fresh registers only; stub claim copies the body org | R3 | P13 |
| G5 org check before role check | C4 | (none needed) |
| G6 400 instead of 422 | R1, R2, R3, R4 | P1, P2, P8, P13, P14 |
| G7 refuse only a non-empty string value | R4 | P2, P8 |

- The PR's cells kill 6 of 7 of my mutants. G2 survives them (F1).
- The builder's six mutants were not re-run; the record was read only.

## Q5: The PR body. Accurate

- Tier 1 named ("The tier 1 gate is next").
- Title and commit subject: "Refs KS-1107". Closing keywords (`close/fix/resolve` + KS-1107) appear 0 times in the body and 0 in the commit message. Control: 2 of 2 planted strings matched.
- The overlap waiver is stated: PRs 2073, 2099 and 2131, the spec file only, merge-tree clean with a positive control, Wednesday's waiver for this push.
- The hook's final line is quoted verbatim: "PREFLIGHT INCOMPLETE — 13/16 legs ran, 3 SKIPPED. Nothing failed.", with legs 3, 4 and 8.
- Skipped legs, from `scripts/preflight/preflight.sh`:
  - Leg 3: spec-auth conformance (unauthenticated calls to bearer operations must 401/403). Register is unauthenticated and its auth requirement is unchanged, so it does not bear.
  - Leg 4: path resolvability. No path changed, so it does not bear.
  - Leg 8: served-spec versus YAML consistency. The YAML changed by one description string, so it bears nominally. Leg 1 (spec drift) and check:openapi ran. Low (F6).
- Platform S UNREAD: stated, twice (F5).
- Existing-users query: a DESIGN, not run, and the body says production is Kam's. My judgement:
  - The tables and columns exist: `organization_members` (migration 001:75) and `organizations.tenant_id` (017:51).
  - On the fresh-register path the org was written on the row, so the query WILL list every account that joined through the hole and still holds that org. It will list them mixed with every admin-assigned user.
  - `cross_tenant = true` is a strong signal; a platform admin's PATCH can also produce it. A same-tenant joiner is indistinguishable from an admin assignment except through the app log line "Admin user update" (PATCH) for that user id. No database record separates the two, as the body says.
  - It CANNOT find stub-claim exposures. On that path only the token carried the body org (the row kept its own), so nothing durable records it, and it lasted only until the token expired or refreshed.
  - The query will find candidates, not a conclusive list (F4).

## Needs Kam
1. Production: whether anyone has already joined an organisation through this hole. Running the PR-body query (or a log search for POST /api/auth/register correlated with org assignment) on any box is Kam's decision. Stub-claim token exposures left no durable trace.
2. F2: the INVITED-stub claim takes over an invited email's stub without email verification, and the claimant inherits any organisation an admin assigned to it. Pre-existing (KS-74), not this ticket. A ticket via a board seat if Kam agrees.
