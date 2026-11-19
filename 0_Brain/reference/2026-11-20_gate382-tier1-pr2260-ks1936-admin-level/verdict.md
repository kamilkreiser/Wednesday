PR 2260: GO WITH NOTES (at head 55f448ff69a5edad7e9023afb5f254d38cfca7bf; tier 1)

# Gate 382, tier 1, PR 2260 (KS-1936), 2026-11-20 ~01:31 AEDT

Head re-pinned by gh api twice (before the first measurement, and again just before this verdict): 55f448ff69a5, open, not merged, not draft. Develop is d4ffc8308249 both times. PR 2159 head is 7b54e7cbb6f0.
Merge trees, re-measured by me: 2260 onto develop d4ffc8308249 gives rc 0 (tree 2b727003a821). 2260 against 2159 gives rc 0 (tree 23dba6e17613, the same tree the builder reported).
Everything ran in my own clone under scratch/ (repo = head, dev = develop d4ffc8308249). Deps were APFS-cloned from the builder's tree, which was only read; locks were byte-equal. The shared package was built in my trees. My Postgres was a throwaway container, g382-pg, bound to 127.0.0.1 and now STOPPED. I did not touch w41-ks1936-pg (still stopped).

## Verdict reasoning
The code does what it says. On this route every non-platform role gets 403 before any query. Platform roles still get 200 and the write. Nothing else changed. The tests are honest and kill the mutants that matter.
The PR's TITLE (and the fragments' H2) says "only a platform admin can set a user's verification level". That is **false at product level** (F1/F2: auth's PATCH /api/users/admin/:id still lets ORG_ADMIN set levels, and the admin UI uses it). The BODY correctly scopes the claim to "this ONE route". So the note is: retitle before merge. The sibling itself does not block.

## Q1: is the route closed to every non-platform role? YES (by assertion)
- `requirePlatformAdmin` uses `isPlatformRole` (packages/shared/src/security/keyRevokePolicy.ts:140-145). It accepts a string role only, ASCII-folded, that equals SYSTEM_ADMIN or SUPER_ADMIN.
- `requireAdmin` (admin.ts:628-664) uses `isPlatformOrOrgBoundedRole` (:153-157), which adds ORG_ADMIN and ISSUER_ADMIN under the same ASCII fold. platform_admin, PLATFORM_ADMIN, admin and ADMIN are refused at requireAdmin (KS-1536).
- `req.user` is overwritten by requireAdmin from the verified token (or the test-token payload), so nothing upstream can pre-set it.
- My own 26 cells (scratch/g382-extra.test.ts, same harness) at head: 26 of 26 pass. Positive control: 12 of 26 fail on develop.
  - Refused with 403 and 0 queries: Org_Admin, org_admin, Issuer_Admin, `SUPER_ADMIN ` (trailing space), U+017F `ſuper_admin`, U+0131 dotless-i, ['SUPER_ADMIN'] as an array, SUPERADMIN, SUPER-ADMIN, PLATFORM_ADMIN, admin, ADMIN, connector.
  - Also refused with 403 and 0 queries: ORG_ADMIN carrying scopes/isPlatform/roles/realRole claims; ORG_ADMIN with x-tenant-override, x-user-role: SUPER_ADMIN, x-platform-scope and x-impersonate headers; a body carrying role claims; trailing-slash, UPPER-CASE and ?role= path spellings.
  - A malformed JSON body gets **403, not 400**, which proves the gate runs before the body parser. An ORG_ADMIN test token is also refused.
  - Controls that pass the gate: super_admin and Super_Admin get 200 with one UPDATE. GET /api/admin/identity/users as ORG_ADMIN is not 403 (unchanged).
- There is no global body parser ahead of this router: `/api/admin` is in proxyPaths (index.ts:399, :406, :412). So the route-level parser is the only parser.
- INFO (pre-existing, not this PR): `parseTestToken` (middleware/auth.ts:125-162) builds an UNSIGNED payload with any role, including SYSTEM_ADMIN, which passes the gate.
  - It only works when NODE_ENV is development or test AND ENABLE_TEST_TOKENS is set.
  - A prod-like NODE_ENV with the flag set is FATAL at boot (index.ts:81-95).
  - No tenant role can turn platform through it unless it holds a dev/test environment.

## Q2: sibling doors (census by the WRITE)
Frame searched: `git grep` at head over Blockchain/Dev/services, packages and scripts, excluding tests, for:
- `UPDATE users`, `INSERT INTO users` and `.user.(update|upsert|create)(`;
- every `verification_level`/`verificationLevel` write;
- every requireAdmin handler in admin.ts that writes users or organizations.

Outside the frame: frontends' own state, Python/Go services, SQL in migrations/seed, other repos, and deployed configs.

Findings, one per row:
- **F2 HIGH (sibling, Kam's call): auth `PATCH /api/users/admin/:id`.** File: services/auth/src/routes/users.ts:698-830. The gateway forwards to it from admin.ts:1565 under requireAdmin, and the admin UI calls it (frontend/admin/src/pages/Users.tsx:284-291 sends `verificationLevel`).
  - ORG_ADMIN and `admin` can set `verificationLevel` for ANY user in their own tenant, across organisations. The bound is tenant equality only (:798).
  - That includes **themselves**: the KS-467 self-check at :757 covers `role` only.
  - The value is not checked against the level list. It is lowercased into a VARCHAR(20).
  - The verification-review approve path (ORG_ADMIN, same tenant) is tested, deliberate design (auth __tests__/ks467-user-admin-isolation.test.ts:401-407).
  - Found by reading plus existing tests; not run live. Whether org admins may set levels at all, and on whom, is Kam's.
- **F3 MEDIUM (sibling): originate `PATCH /api/admin/identity/users/:id/level`.** File: services/originate/src/routes/adminConfig.ts:1808-1825, under `requireRole('SYSTEM_ADMIN','ORG_ADMIN')` (:45). It writes under runWithPlatformScope with an id-only predicate, so an ORG_ADMIN can write ANY tenant's user, whatever the DB role.
  - Shadowed at the gateway's /api/admin path by mount order, by reading:
    - the /api/v1 rewrite sits at index.ts:556;
    - createAdminRoutes is mounted at :936, before createProxyRoutes at :1147;
    - the gateway handler always responds, and proxy.ts:1297 is the /api/admin/ proxy behind it.
  - **NOT shadowed via the gateway's unauthenticated `/originate/` passthrough (proxy.ts:1282).** That path forwards any route to originate, and originate verifies the JWT itself.
  - nginx returns 404 for `/originate/` in nginx.conf:224 and nginx-demo.conf:457. In nginx-production.conf it falls through to the SPA.
  - docker-compose.yml does not publish the gateway or originate ports.
  - So it is reachable only where the gateway port is reachable without nginx in front, or from inside the network. Not probed live.
- **F4 MEDIUM (sibling, MEASURED by me): gateway `PUT /api/users/admin/organizations/:id`** (admin.ts:1538-1546, by id alone, adminScope). On my g382-pg, with real router and real query, at head:
  - as secuura_app: ORG_ADMIN to another tenant's org got 404 (0 rows), and ISSUER_ADMIN to another org in the same tenant got 404. Bounded by accident, same as KS-1936;
  - as the superuser: both got **200 and the org WRITTEN** (status=suspended);
  - SYSTEM_ADMIN control: 200 and written on both roles.
  - `DELETE` (:1595-1599) and `POST` (:1514) have the same shape by reading; not measured.
- Other writers I read, none of them this class:
  - startup-migrations.ts:1092 is a migration;
  - auth userRepo seed/MFA/backfill scripts are self or ops;
  - gdprService and userErasedSubscriber handle erasure;
  - auth's create (`POST /api/users/admin/create`) sets an initial level and is already a separate KS-486/467 surface;
  - admin.ts:1296 is the demo seed INSERT.
- None of F2-F4 makes the PR's *code* claim false. F2 makes its *title* false (F1).

## Q3: nothing else changed. CONFIRMED
- The diff is +31/-3 in admin.ts: the comment, the gate definition and the one route line. No other handler is touched. The GET routes and every other route are byte-identical to develop.
- At head on my PG, both roles: SYSTEM_ADMIN gets 200 and the write; USER gets 403; no token gets 401; platform_admin gets 403.
- The rewritten KS-458 comment (admin.ts:609-621) is true: nothing on this mount calls runWithTenantId, and I measured 404 as secuura_app.
- No product caller exists. This is my own check over frontend/, scripts/, systemTest/ and e2e/:
  - `identity/users` hits only the two GETs (IdentityManagement.tsx:100, VerificationQueue.tsx:126), which are the positive control;
  - `/level` has zero hits in those trees, against a control of 8 frontend files that call `/api/admin/`.
- INFO F7: README.md:438 and docs/QUICK-REFERENCE.md:143 still list the PATCH as "Update user verification level" with no platform-only note.

## Q4: tests honest. CONFIRMED
- **Red first on develop d4ffc8308249** (newer than the builder's fb975989cee1): 5 of 12 fail, all by assertion (200 or 400 where 403 was expected). The 7 controls are green. At head: 12 of 12.
- **Real PostgreSQL** (my g382-pg: postgres:15-alpine, docker/init + init-platform staged byte-equal, run-migrations.sh with 60 applied and 0 failed, runStartupMigrations with 48 applied and 0 failed; the builder's probe and expectation, re-pathed only). 12 cells per arm, judged by assertion:

  | arm | develop | head |
  |---|---|---|
  | app (secuura_app) | 7 of 12 FAIL | 0 of 12 FAIL |
  | su (superuser) | 7 of 12 FAIL | 0 of 12 FAIL |
  | ctx (seeded tenant context) | 7 of 12 FAIL | 0 of 12 FAIL |

  This reproduces the matrix: as su every tenant cell is WRITTEN; under ctx the tenant is bounded and the organisation is not.
- **Mutants** (counted replacements on my clone, sha256 restored after each):

  | mutant | PR's 12 cells | my 26 cells |
  |---|---|---|
  | M1 drop the gate | killed, 5 | 12 |
  | M2 isPlatformOrOrgBoundedRole | killed, 5 | 12 |
  | M3 check after a query | killed, 5 (zero-query assertion) | 12 |
  | M4 case-sensitive list | killed, 1 (system_admin) | 2 |
  | M5 gate only if body.verificationLevel | killed, 5 | 12 |
  | **M6 gate after the parser, before the query** | **SURVIVES** | killed, 1 (malformed body) |
  | **M8 gate reads x-user-role first** | **SURVIVES** | killed, 1 (header cell) |
  | M7 also admit platform_admin | equivalent (requireAdmin refuses it first) | equivalent |

- **Whole api-gateway suite, sequential, load-gated** (load1 under 8 at every start):
  - develop: 2,057 of 2,057 in 180 files;
  - head: 2,069 of 2,069 in 181 files;
  - failure-name sets are equal (both empty).
- **tsc** for api-gateway at head: rc 0. Planted control: rc 2, and it names the planted file.

## Q5: PR body and waiver. CONFIRMED, with F1
- "tier 1" is named. The title is "Refs KS-1936: ..."; there is no closing keyword (regex control fired on "Closes KS-1936"). The withdrawn KS-458 intent is stated plainly, with the reason.
- The waiver `OVL_IGNORE_PRS="2159"` is stated once, with PR 2159's head 7b54e7cbb6f0 and tree 23dba6e17613 (reproduced).
- The hook's final line is quoted verbatim (13/16, legs 3 4 8 SKIPPED, "This is NOT a pass").
  - The skipped legs (preflight.sh:347, :369, :553) are spec-auth conformance, path resolvability and served-spec consistency. All three are driven by the OpenAPI spec, and this route is not in the spec.
  - Leg 3's own property (no token gets 401) is covered by a cell. **No skipped leg bears on this change.**
- The boot-role question (the runtime DATABASE_URL role on Kintsugi and demo) is stated as "NOT read". That is correct: UNMEASURED, not claimed safe.
- **F1 MEDIUM (merge note): retitle.** The title and both fragment H2s claim "only a platform admin can set a user's verification level", which F2 makes false. Suggested title: "Refs KS-1936: only a platform admin can use PATCH /api/admin/identity/users/:id/level". The body already says "this ONE route".
- F5 LOW: the PR's cells do not pin "before the body parser" or header immunity (M6 and M8 survive them). The code is right; a malformed-body cell and a header cell would pin both claims. Optional.

## Deviations and caveats (mine)
- The builder's node_modules (inherited) holds an ABSOLUTE symlink `node_modules/node_modules` pointing to `worktrees/s-w36-ks930/Blockchain/Dev/node_modules`. Through it, Node resolution loaded esbuild from that other seat's tree during my first runs (read only).
  - I moved my two clones' copies of the link to scratch/_quarantine and re-ran: the 12 cells (12/12), the whole suites, tsc, and the planted controls.
  - The real-PG probes and mutants ran before the move. Their results are behavioural, and the same esbuild version is expected.
  - INFO for the fleet: the donor trees carry a cross-seat link.
- For the probe runs I set tsx's working directory with `cd` inside a `bash -c` subprocess. That is not a shell `cd` in my session, but I am naming it.
- Nothing was posted, mailed, pushed, merged or written to Linear or GitHub. Linear and GitHub were only read.

## For Kam / Wednesday to route
- **Kam:** F2, whether organisation admins may set verification levels through auth's PATCH /api/users/admin/:id, across organisations in their tenant and on themselves. Changing what org admins can do is Kam's call.
- **Wednesday:**
  - F3: the originate sibling, reachable via `/originate/`;
  - F4: the organisations PUT (measured), plus DELETE and POST by reading;
  - the boot-role read on Kintsugi and demo (if a real gateway runs as superuser or BYPASSRLS, F4 and the pre-fix KS-1936 matrix are live there);
  - F7 docs;
  - the cross-seat node_modules link.

Evidence: scratch/evidence/ (probe_{develop,head}_{app,su,ctx}.{json,txt}, expect_*.txt, orgprobe_head_{app,su}.txt, suite_{dev,repo}.json/.out, failnames_*.txt, tsc_*.out), scratch/mutants_g382.json, scratch/cells_*.out, scratch/extra_*.out, scratch/linear_ks1936.json, scratch/pr.json.
