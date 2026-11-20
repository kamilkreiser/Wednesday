PR 2269: GO WITH NOTES (at head 3423d65bbad6a12be92dcd9b96b887fc7a82ed19; tier 1)

# Gate 393, tier 1 (Opus), PR 2269 (KS-2302), 2026-11-20 ~17:11-17:29 AEDT

## Pins
- **Pinned twice, at 17:12:14 and 17:28:43**, with git ls-remote and gh pr view (the Secuura project's gh credential, read-only). The values were the same both times:
  - PR 2269 OPEN, MERGEABLE, head 3423d65bbad6, ONE commit, parent = develop 90ef2cf004e3. 4 paths, +266 -1. updatedAt 06:08:16Z.
  - develop = 90ef2cf004e39676fe7afde2c12313dcf71a8995; PR 2268 head = 98d1032ffa21.
- **Merged state = the head** (it fast-forwards onto the develop tip). Every "head" figure below is the merged state.

## How I measured
- I cloned `_work/g` from GitHub (`--reference-if-able` gate 392's clone, `--dissociate`). Worktrees: `h` (head: suites, static), `x` (head: mutants and probes), `d` (develop).
- I copied in node_modules: the root tree, `packages/shared` and `services/{auth,shared}` from gate 392's `h`, and `services/originate/node_modules` from gate 388's `h`. The root and originate lockfiles, package.json and the prisma schema are byte-identical to this head.
  - My first suite run, without originate's own node_modules, failed 7 suites with "Cannot find module '@prisma/client'" on BOTH arms. That was a harness error, not a result. It was fixed and re-run.
- Node v26.8.1 (not LTS), jest, TMPDIR /private/tmp/g393t.
- Scripts in `_work/`:
  - `run_cwd_g393.py`, `suites_g393.sh`, `static_g393.py`;
  - `mutants_g393.py` (whole adminConfig cell set per mutant: 19 files, 318 cells);
  - `mt_g393.py` (merge-trees and the planted control);
  - `lin_read_g393.py` and `lin_search_g393.py` (read-only GraphQL);
  - three probes in `probes/`. Each probe writes JSONL and asserts nothing:
    - g393-probe-a: the PR's harness with a JSON role claim (25 role shapes x 9 route shapes).
    - g393-probe-b: the REAL `authenticate()`, with RS256 through `JWT_PUBLIC_KEY` and a generated keypair.
    - g393-probe-c: PUT /privacy.
- The probes were moved to `_work/_quarantine/` afterwards. End state: h, d and x each have 0 porcelain lines. x's adminConfig.ts sha256 0143defce3da… = the head blob.
- Not touched: no seat tree, no GitHub or Linear write, no database server, no container, no mail.

## Findings

No HIGH finding against this PR. The guard holds as ruled at all five sites, through the real router and the real token verifier. Nothing I tried reaches a guarded handler as platform without a platform-signed token.

### MEDIUM (not a defect of this PR; pre-existing; for Wednesday to route)
**G393-2269-1: another door with the same root cause is left open and is not in the closed list: `PUT /api/admin/privacy` lets any ORG_ADMIN rewrite the platform-wide retention policies, which the background sweep then enforces across every tenant.**
- `adminConfig.ts:1419-1446` (head) runs `UPDATE data_retention_policies SET retention_period_days, auto_delete, deletion_method, is_active … WHERE id = …`. There is no role check beyond the router gate, which admits ORG_ADMIN.
- `data_retention_policies` has no tenant column and no RLS policy: 0 hits in migrations 009, 027, 038 and 039, against 3 for `organizations` as a control.
- Reach at the edge: the gateway answers `/api/admin/settings` and `/api/admin/document-types` itself, but NOT `/api/admin/privacy`. That path falls through to the `/api/admin/` proxy (`authenticateToken` + `enforceAdminProxy`, which admits ORG_ADMIN) and on to originate.
- **Measured** (probe c, the PR's harness): an ORG_ADMIN of another organisation got 200 `{"success":true,"updatedCount":1}`. The handler issued the UPDATE with `retention_period_days = 1, auto_delete = true`, exactly as SYSTEM_ADMIN does.
- Effect, by code read only: `retentionScheduler` (started at `index.ts:524`, daily) runs `enforceRetention` (`gdprService.ts:464-535`) under platform scope. For each `auto_delete` policy it deletes or anonymises rows older than the cutoff in EVERY tenant: `DELETE FROM verification_requests`, `DELETE FROM share_records`, `DELETE FROM user_sessions`, and the anonymising UPDATEs on audit_logs and system_errors.
  - So one ORG_ADMIN request can, at the next sweep, hard-delete every tenant's verification requests and share records older than one day, and strip the PII fields from the 7-year audit log.
  - `retentionDays: 0` is ignored (`|| null`); 1 works.
- No ticket for it: Linear searches for "data_retention_policies", "PUT /api/admin/privacy" and "retention policy ORG_ADMIN" found none (evidence/lin_search.json).
- Same class, lower harm (read only, not measured): `PATCH /api/admin/pricing/:eventType` (:217) updates the global `pricing_config` for any ORG_ADMIN, and it also reaches originate through the proxy. `POST /refresh-tenants` and `POST /pricing/refresh` only reload.
- This PR neither creates nor worsens it. The ANSWER closed the list, and the fragment's "Unchanged: every other route of the router" is honest. It needs its own ticket (a product question if org admins are meant to edit privacy settings; Q5's census found no frontend caller of `/api/admin/privacy`).

### LOW
**G393-2269-2: non-equivalent mutants of the new rule that all 318 cells miss (pinning gaps; no hole at this head).**
- **G1, an ORG_ADMIN with NO organisation claim admitted** (`|| (role === 'ORG_ADMIN' && !organizationId)`): 0 failed. Every ORG_ADMIN cell carries an org (B or A). KS-2299's seeded org admins carry none, so this is the realistic shape.
- **G4 and G5, the POST /organizations and backfill guards moved after their body checks** (`name is required`, `issuerName is required`): 0 failed. Both are still before any statement, so nothing is written either way. An ORG_ADMIN sending an empty body would get 400 instead of 403. That answer depends on the body, not on the caller, which breaks the "FIRST statement" claim but is harmless.
- **G7, a PUT warning's route label wrong:** 0 failed (R5 checks only DELETE's label).
- Equivalent at this head (the router gate admits only SYSTEM_ADMIN, super_admin, SUPER_ADMIN and ORG_ADMIN): G2 (a deny-list refusing only exact `ORG_ADMIN`) and G10 (a `String().toUpperCase()` platform test). Both 0 failed, and both are unreachable differences while requireRole stays as it is.
- Fix shape: one cell with an ORG_ADMIN without an org on DELETE (kills G1); one ORG_ADMIN cell with an empty body on POST /organizations and on backfill (kills G4 and G5).

**G393-2269-3: words that do not hold exactly.**
1. "Callers: none found for any of the five routes" (PR body) and "No caller of the five routes exists in our code" (facts comment 41fd8578) are over-stated. `Blockchain/Dev/tests/e2e/` calls them:
   - `cross-persona-e2e.prelaunch.spec.ts:109,117` POST `/api/admin/organizations` and `/originate/api/admin/organizations` (a fallback chain, admin@secuura.com = SYSTEM_ADMIN);
   - `multi-tenancy.prelaunch.spec.ts:115,389` (GET and POST probes, admin token);
   - `security-bad-actor.prelaunch.spec.ts:488-500` DELETE as issuer, expecting 403.
   - The PR body's own list ("frontend, mobile, scripts, systemTest or Blockchain/Testing") does not include `Blockchain/Dev/tests/`, so its literal sentence is true. The capability premise holds anyway (Q5).
2. The test header says "SUPER_ADMIN, any letter case" (and the code comment says "any letter case"). `isPlatformRole` folds case, but the router gate admits only `SYSTEM_ADMIN`, `SUPER_ADMIN` and `super_admin`. `System_Admin`, `Super_Admin` and `system_admin` get the gate's 403 (probe a, b). The cheat fragment lists the three exact spellings correctly. This fails closed, and gate 392 made the same note.
3. "Router gate (line 45)": line 45 on develop, 46 at the head (the PR adds a comment line). Cosmetic.

## The commission's questions
- **Q1 THE GUARD: holds.**
  - `refuseUnlessPlatform` asks the shared `isPlatformRole` (keyRevokePolicy.ts:140: non-string false, ASCII fold, {SYSTEM_ADMIN, SUPER_ADMIN}).
  - At all five sites it is the first statement inside the handler's `try`: before `req.body`, `req.params.id` and `(req as any).db` are read, and before `getTenantManager()`.
  - Probe a (225 requests, evidence/probe_a_x.jsonl):
    - SYSTEM_ADMIN, SUPER_ADMIN and super_admin reach every handler (200/201, or 400 on an empty body or with multi-tenancy off).
    - ORG_ADMIN and ORG_ADMIN-own-org get 403 from the guard on all 9 route shapes, including a non-UUID id and an upper-case id. Zero statements, zero platform scope, zero getTenantManager. The warning names the route.
    - Every other shape gets 403 from requireRole first: `admin`, VERIFIER, ISSUER_ADMIN, no role, null, `""`, `Super_Admin`, `System_Admin`, `system_admin`, `SYSTEM_ADMIN `, long-s `ſuper_admin`, dotless `SYSTEM_ADMıN`, `["SYSTEM_ADMIN"]`, `["super_admin"]`, `["ORG_ADMIN"]`, an object, 1, true, `platform_admin`, `ORG_ADMIN`+ZWSP.
    - One 403 body only, byte-equal to requireRole's.
  - The zero-statement assertions are real: the mocks record `$executeRaw`/`$queryRaw`/`withTenant`/tx calls and run the platform-scope callback (the P1 control sees all 5 calls). They are not mocked away.
- **Q2 OTHER DOORS:**
  - Census of originate at this head, my own (organisation INSERT/UPDATE/DELETE, organization_members, runWithPlatformScope, tenant manager). Organisation writes: :927 POST, :946 PUT, :974/976 DELETE, :2348 inside migrate (all guarded). There is also `connectorOrganisationErasure.ts:430`, reached only through `/api/platform/organizations/erase-connector` (`requireRole(...CONNECTOR_ROLES)`), a different door not reachable by ORG_ADMIN.
  - The exclusions are as the ANSWER says:
    - seed-demo-users (:2112) is env-gated by both flags, first thing, and inserts users and a rights holder only; systemTest fixtures call it.
    - the level PATCH (:1836) is KS-2278.
    - the five reads are KS-2235 (GET /organizations, /reports, /users, /identity/users, /identity/organizations).
  - Gateway: no forward of these paths besides the `/api/admin/` proxy and the `/originate/` mount. Its own organisation DELETE/PUT is KS-2279 (known).
  - **Missed door: G393-2269-1** (PUT /privacy, cross-tenant destructive via the sweep), not in the closed list.
- **Q3 THE GATEWAY: R5 holds.**
  - The role comes only from originate's own `authenticate()`. It verifies an RS256 bearer (alg pinned, static key or JWKS) and `setUser` overwrites `req.user`. adminConfig reads no header for identity.
  - Probe b, with the real verifier, reached nothing:
    - no bearer with `x-user-role`/`x-role`/`x-test-role: SYSTEM_ADMIN`, `x-tenant-override` and a forged `x-gateway-vouch`: 401;
    - a valid ORG_ADMIN token plus the same forged headers: 403 from the guard, 0 statements;
    - `alg:none`, HS256 keyed with the public PEM, RS256 from another key, and an expired token: 401;
    - role claims `["SYSTEM_ADMIN"]`, `system_admin`, `Super_Admin`, none, `connector`, and ORG_ADMIN with an extra `roles:["SYSTEM_ADMIN"]`: 403.
    - Controls: SYSTEM_ADMIN and super_admin tokens reach the handlers.
  - The gateway strips `x-(user|tenant|organization|org|role|roles?|auth-user|policy|emitter|gateway-vouch)` on every inbound request (`trustHeaders.ts`), except `x-tenant-override`. That header confers no role. nginx (demo, production, local) answers 404 for `/originate/`.
  - **A caller cannot set its own role on the `/originate/` path.**
- **Q4 THE CELLS: reproduced.**
  - Head: 28/28.
  - Head's test file on develop's adminConfig.ts: **9 failed, 19 passed**. Every failure is an assertion: status 403 expected against 200/200/201/200/400 received for R1 on the five routes; 200 for R2 and R3; the R4 body; R5's warning undefined. No harness error.
  - Platform controls exist for every route: P1-P5 x 3 spellings. Q1 x 4 roles pins the gate.
- **Q5 THE CAPABILITY PREMISE: holds.**
  - I grepped the whole repo (frontends, mobile, sdk, scripts, connectors, systemTest, USER_TESTING, services, tests) for the five paths.
  - No real caller uses a non-platform role. The admin frontend calls `/api/users/admin/organizations` (api.ts:288-916) and `/api/admin/identity/organizations`, never these five; `ADMIN_API='/originate'` in DocumentTypes.tsx/Workflows.tsx is declared and never used.
  - The only callers are tests/e2e. Two use the SYSTEM_ADMIN seed (unchanged behaviour); one is an issuer expecting 403, which is still 403, and still from the gate. Existing originate cells that call backfill and migrate (ks730c, ks1772) use SYSTEM_ADMIN.
  - **The PR removes no working capability.** Words: G393-2269-3.1.
- **Q6 MUTANTS** (whole adminConfig cell set: 19 files, 318 cells, on the merged state; tsc 0 for every mutant; product file restored and sha256-checked after each; evidence/mutants*.out, mut/):

  | mutant | failed | killed by |
  |---|---|---|
  | M1 DELETE guard removed | 4 | R1 DELETE, R2, R4, R5 |
  | M5 inverted | 41 | 24 ks2302 + 11 ks730c + 6 ks1772 |
  | M7 PUT guard removed | 2 | R1 PUT, R3 |
  | M8 POST /organizations guard removed | 1 | R1 POST |
  | M9 backfill guard removed | 1 | R1 backfill |
  | M10b migrate guard removed (`void req`) | 1 | R1 migrate |
  | M13 refusal lets the handler run on | 9 | all refusal cells |
  | G3 own-org ORG_ADMIN admitted | 2 | R2, R3 |
  | G6 DELETE guard only for UUID-shaped ids | 1 | R4 |
  | G8 warning without role / G9 info not warn | 1 / 1 | R5 |
  | **G1, G4, G5, G7** | **0** | **survivors, non-equivalent: G393-2269-2** |
  | G2, G10 | 0 | survivors, equivalent at this head |

  BASE 318/318.
  - M5's 11 ks730c cells match the builder's "11 in the existing files". My set also includes ks1772 (+6), which is outside the builder's six files.
  - My first G4 spelling had a non-unique anchor (the script asserted and stopped). It was re-spelled and re-run.
- **Q7 WHOLE:**
  - Originate suite (default jest config): develop **2882/2882 in 235 files**, head **2910/2910 in 236 files**. The failure-name sets are equal (both empty).
  - tsc 0 (planted: rc 2, 1 error).
  - eslint `--max-warnings 0` on adminConfig.ts + the test: rc 0; adminConfig.ts on develop: rc 0 (planted: rc 1).
  - check.cjs services/originate: 330 examined, 269 under __tests__, 0 baseline, 0 new, 0 stale (planted: 1 new, rc 1).
  - Fragments: OK (planted two-h2: FAIL).
  - check:openapi: CHECK PASS. `originate.openapi.ts` has 0 `/api/admin` hits (control `/api/documents`: 31). The yaml has 0 for `/api/admin/organizations`, 1 for the control `/api/users/admin/organizations`.
  - Overlap: 20 open PRs = 19 others + this one. None touches any of the 4 paths (control: the most-touched path, package-lock.json, appears in 11). No PR lists 100 or more files, so there is no truncation.
  - PR 2268 is path-disjoint (9 auth/yaml/fragment paths). merge-tree of 2269 onto develop+2268: **rc 0** (tree d91bbe665c9d). Planted control: my local commit 0c4b3b8255e6 on 2268 rewriting the router-gate comment line, never pushed. It gave **rc 1**, CONFLICT (content) in adminConfig.ts. 2269 onto develop: rc 0.
  - Not re-run: the standalone 6-service ratchet and its leg test.
- **Q8 WORDS:**
  - PR body: summary, rule, body, placement, the 9/19 red, 28 green, 13-mutant table (every row I re-ran, M1/M5/M7/M8/M9/M10b/M13, is killed as stated), the suite figures, the static legs, 330/269, and the openapi figures all reproduce.
  - Residuals: R2, R3 (by code: `res.json({success: result > 0, … 'Not found'})` = 200), R5 (Q3) and R6 (Q2) are accurate. R1 (non-atomic cascade) and R4 (500 at the `::uuid` cast) are code/DDL readings I did not re-measure (no database). The code shows `withTenant` followed by a separate `runWithPlatformScope` block, which is consistent with R1.
  - "NOT run" is honest, and Node 26 is disclosed.
  - Exceptions: G393-2269-3.
  - KS-2302 ticket (read-only): In Progress, priority 2 (High), created 05:19:09Z. Its code lines (45, 142-161, 934-955, 913-931) match develop. It names the PUT twin as unscoped, which is now in scope by Q2.
  - Facts comment 41fd8578 (2,305 B; updatedAt .348Z is not after createdAt .367Z, so it is unedited): every measurable sentence holds except "No caller … exists" (G393-2269-3.1). Push timings are the builder's, and UNMEASURED beyond ls-remote.

## Two-NO-GO cap
Not engaged.

## Not run
- The four platform suites, a booted originate or gateway, a real Postgres (RLS, FKs, R1, R4), the retention sweep itself (G393-2269-1's effect is a code reading; the UPDATE is measured), any deployed environment, Node 24.
- The standalone 6-service ratchet and its leg test.
