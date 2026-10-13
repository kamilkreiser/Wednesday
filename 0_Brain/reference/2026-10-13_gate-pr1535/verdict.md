# Gate verdict: PR #1535 (KS-1570 PR A, shape b: ADMIN bounded by an explicit organisation scope), Opus tier 1
SHA256/16: 908a786016f5c2f2 (recipe: delete this one line from the file, then sha256 of the remaining bytes, first 16 hex chars)

**VERDICT: GO WITH NOTE** for head `335dfd78b0e263ba71f2e68fc4da10265d9d5a79`. The diff is correct, it fails closed, and every claim I re-measured holds.
**THE NOTE BLOCKS THE DEPLOY ROUND, NOT THIS MERGE.** Finding **M1** is Major. It is not in this diff and it is the same on develop, but it defeats this PR's purpose. Any ADMIN, scoped or not, can still get a key that names ANY organisation of its tenant and is bound to that organisation's connector, in two calls, through a provisioning key it is allowed to mint. Until M1 is fixed, KS-1570 does not close the deploy blocker it was written for. Do not recommend deploying. The round is PR A + PR B + KS-1564, and it now needs the M1 fix too.

Gate: an independent Opus seat, 2026-10-13, AEDT. Read-only on the project: `git clone --shared` into the scratchpad, push URL `DISABLED`, write verbs only in the clone. Throwaway PG15 on 127.0.0.1:55411 (TCP only), **stopped at the end**. Other agents' clusters (55416/55436/55447/55521, brew 5432) were not touched. Raw outputs: `evidence/results/`, cells: `evidence/gatetests/`, tools: `evidence/tools/`.

## Findings

| id | severity | where | what | minimal fix |
|---|---|---|---|---|
| **M1** | **Major** (pre-existing, outside the diff, **deploy-blocking for KS-1570's purpose**) | `services/security/src/provisioningPolicy.ts:97` (KEY_ADMIN early return, any scope) + `services/security/src/index.ts:1218` (provisioner = `connector` + `organizations:register`) + `packages/shared/src/security/keyRevokePolicy.ts:170-275` (role `connector` meets neither the org arm nor the ADMIN arm) | **Two-hop escape from the scope.** Hop 1: an ADMIN mints a key with `scopes:['organizations:register']`. An unscoped ADMIN can do this as an **unqualified** key, which is the path the ruling keeps open. Hop 2: that key's connector principal mints `{organizationId: A2, connectorId: <A2's connector>}`. **Measured on head: 201, and the row stores `organization_id = A2`, `connector_id = conn_of_A2`.** This holds for an unscoped ADMIN, for an ADMIN scoped `{A1}`, and for an `ISSUER_ADMIN` with claim A1, so the KS-1533 arm 1 bound is open too. Develop gives the same result, so this PR did not introduce it. The KS-695 erasure trusts a key row's organisation and connector (`connectorOrganisationErasure.ts:125,144,333-345`), so the irreversible harm this PR targets is still reachable. | Apply KS-480 limit 1 to non-platform key admins: only a platform role may mint `organizations:register` (and wildcards). This needs **Kam's ruling** if a tenant admin legitimately provisions; then a separate ticket in the same round. Regression cell: `evidence/gatetests/gate1535-d-twohop.integration.test.ts`. It is red on head and red on develop today, and should go green. |
| m1 | Minor | `services/security/src/index.ts:1181` (mint, via the catch at :1323 → `errorHandler`) and `:1419-1421` (revoke, `next(err)`) | A scope read that hits a database **infrastructure** fault answers a generic **500**, not the retryable **503** that the KS-888 classifier gives the same fault on save. Measured with the app role cut off (connection limit 0, backends terminated): head 500/500. Develop's save path gives 503/503. Fail-closed holds either way. | Run the scope-read error through the same SQLSTATE 08/53/57 + socket classifier, and answer 503 `SERVICE_UNAVAILABLE`. |
| m2 | Minor | `scripts/rls/verify-fail-closed.sh:53` | `EXPECTED_TABLES` does not list `admin_organisation_scopes`. The script's own selector picks up the new table (measured), so every verification run prints a `DRIFT` line. | Add the table to `EXPECTED_TABLES`. |
| m3 | Minor (PR B input) | `migrations/049_admin_organisation_scopes.sql:12-13`, `:24-31` | "Rows are written only by a platform role" is an application convention, not a database guarantee. Measured as `secuura_app`: an INSERT into its own tenant under the tenant GUC succeeds, a WITH CHECK refusal fires for another tenant, and **a self-set `app.tenant_scope_bypass` lets it insert into any tenant**. This is the repo-wide model (same as 041), not a defect of 049. There are also no foreign keys. `user_id` is not checked against `users`: every scope row in my fixtures was for a user id with **no users row**, and the scope applied. `organization_id` is not checked against `organizations` of the same tenant. | PR B: validate that the organisation belongs to the tenant, and that the user exists with role ADMIN, at write time. Decide on purging rows when a user is deleted or changes role. Keep the writer route platform-only and audited, as planned. |
| n1 | Nit | `services/security/src/__tests__/ks1533-key-mint-organisation-arm.test.ts:80` | Stale docstring: "`ADMIN`: a KEY_ADMIN_ROLE the arm never engages for. UNDECIDED POLICY, KS-1535." The cell itself is rewritten correctly. | Reword to RULED (KS-1570). |
| n2 | Nit | `ks1570-admin-organisation-scope.integration.test.ts:19`; author PR body "M6" | The claim "Read under the platform bypass, another tenant's rows would count" is true only if the `WHERE tenant_id = $1` is also removed. The author's M6 removes both. My **G1** (bypass only, WHERE kept) **survives every cell**. It is equivalent at the behaviour level, because the WHERE still bounds the read. The GUC property is pinned by no cell; only my statement-log instrument sees it. | Optional: reword the comment, or add a log- or `pg_stat_activity`-based pin. |
| n3 | Nit (pre-existing) | `services/security/src/db.ts:27-33` (no `statement_timeout`) | A scope read blocked by a lock **hangs** the request. Measured: ACCESS EXCLUSIVE held for 4 s, the client aborts at 2 s, nothing is minted while locked, and after release the A2 mint is refused and the A1 mint completes legitimately. It never allows; it just waits. | Optional: a statement timeout on the pool. |

## What I measured (instrument and control for every number)

**1. Heads and merge.**
- `ls-remote`: `refs/pull/1535/head` = `335dfd78…`. **Develop has MOVED** to `0026a43e6` (KS-998 item 1: `.githooks`, `systemTest`, CONTRIBUTING; 7 files) from the commissioned `e4e320ba`.
- `git merge-tree --write-tree`:
  - vs `e4e320ba` gives `41cd1d664a5840a24d46586f8199cbdbacf4874b`, **exactly the author's predicted tree**;
  - vs live develop `0026a43e` gives `69d17898…`, clean.
  - File overlap is 0 in both (`comm` of the name lists).
- `diff --stat c855cfc2..head`: 12 files, +621/−28, exactly the 12 named. `90bfa9ce..head` is the referral merge only (7 referral files). → `results/mergetree.txt`, `diffstat_*.txt`.

**2. The author's cells, 3 runs each, head vs develop.** Develop here is `0026a43e`, with develop's own shared rebuilt; the build control is `isScopedAdminRole` in dist: head 3, develop 0.
- Shared `ks1570-admin-organisation-scope.test.ts`: head **17/17** ×3; develop **8 red / 9 green** ×3, the same 8 cells each time.
- Security integration `ks1570-…integration.test.ts`, on PG15 as `secuura_app` (rolsuper f, rolbypassrls f): head **16/16** ×3; develop **8 red** ×3.
- `MULTI_TENANCY_ENABLED=true` + `PLATFORM_DATABASE_URL`: head 16/16, develop 8 red.
  - "falling back to single-tenant" appears 0 times in the security output. Control: the string exists in originate's `db.ts` (1 hit).
  - `initTenantManager` has 0 callers outside `db.ts`, so **security never starts a tenant manager** (confirmed by code read).
- Wider suites, head:
  - shared full **50 files / 971**;
  - security unit **31 / 336**;
  - security integration **4 / 60**, in both tenancy modes;
  - originate related (4 jest files) **110**;
  - `tsc --noEmit` 0 errors in shared and security;
  - eslint `--max-warnings=0` rc 0 on the 11 changed `.ts` files.
  - Controls: a planted file gives tsc 2 errors and eslint rc 1. **All match the author's numbers.**
- **The rewritten pins, run against develop's code:** ks1533 RULED cell red, ks764 SCOPE-bounded cell red, ks780 S2 (count 4) red. Each fails only on the rewritten cell (2 of 31 and 1 of 7 red).

**3. Migration 049.**
- Fresh `docker/init/*` + `run-migrations.sh`: rc 0, an explicit `[main] Applying 049_admin_organisation_scopes.sql...`, applied=51 failed=0.
- With `PLATFORM_DATABASE_URL` on a second pair of databases, 049 lands in **main only**: table and tracker 1 in main, 0 in platform. Routing control: 1 `[platform]` line in the same log.
- Catalogue: `relrowsecurity t`, `relforcerowsecurity t`, owner `secuura`; one policy `tenant_isolation` (cmd `*`, USING = WITH CHECK, fail-closed + bypass, as 041). PK `(tenant_id,user_id,organization_id)` plus the `(tenant_id,user_id)` index. `secuura_app` holds SELECT/INSERT/UPDATE/DELETE through default privileges, with no GRANT in 049.
- **Idempotence on a database with rows:** 2 rows seeded, then applied twice with rc 0/0; count and md5 of the rows are identical before and after (`2 d6b9d7b8…`). The runner re-run skips it (`skipped=51`).
- RLS as the app role: no GUC 0 rows; wrong tenant 0; right tenant 1; bypass 1.
- Numbering: 048 was the highest; 003 and 038 are duplicated (`uniq -d`); 049 is new. The filename has no "platform". The table is referenced only by 049, `adminScope.ts`, the policy comment and tests. The ROLLBACK line holds. **Deploy:** the `migrations` image bakes `.sql` (compose `command: sh scripts/run-migrations.sh`), so the deploy seat must rebuild it and look for the explicit `Applying 049` line.

**4. Adversarial HTTP cells** (`gatetests/gate1535-a-adversarial.integration.test.ts`): **58/58 on head, 33 red on develop**. Per-cell head vs develop: `results/gateA_head_vs_dev.txt`. They run at the real `POST /api/keys` and `DELETE /api/keys/:id`, and store state is read back as the superuser.
- **ADMIN `{A1}` naming A2:** exact, upper, padded, NBSP, tab, braces, Kelvin, `default-org`, `urn:uuid:`, no hyphens → **403 every time, nothing minted** (develop 201 every time).
- **Naming A1:** exact, upper, NBSP, tab → 201, **stored normalised `A1`**; braces, fullwidth, no hyphens → 403.
- **Unscoped ADMIN** naming A1 in 4 spellings → 403. Unqualified (absent, `''`, whitespace+NBSP) → 201 with the stored org NULL.
- A body field `adminOrganisationScope` and a header naming a scope are ignored: 403. zod strips the field; there is no header read.
- **Roles:** `ADMIN`/`admin`/`Admin`/`aDmIn` are all bound (A2 403, A1 201). `' ADMIN'`, `'ADMIN '`, `'\tADMIN'`, `'ADMIN​'` are refused at the role gate (403, nothing minted; develop identical).
- **Token shapes:**
  - no tenantId → 403 even unqualified;
  - no userId/sub → naming 403, unqualified 201;
  - `sub` only → the fallback resolves (A1 201, A2 403);
  - non-uuid `userId` → 403;
  - upper-case `userId` resolves;
  - upper-case tenantId → 403 (fail closed).
- **Cross-tenant:** U_A1's `{A2}` row in T2 does not count in T (403). As an ADMIN of T2 it does (201). ADMIN of T with body tenant T2 → 403. `x-tenant-id: T2` → 403.
- **Other roles:**
  - ISSUER_ADMIN with a stray scope row `{A2}`: not widened (A2 403, A1 201);
  - ORG_ADMIN unchanged;
  - `super_admin`/`SYSTEM_ADMIN`/`SUPER_ADMIN` → 201 cross-org;
  - a non-provisioning connector → 403;
  - an ADMIN naming `connectorId`/`rotate` → 403.
- **Revoke:**
  - `{A1}` on A2 → 403, key active;
  - on A1 → 200;
  - already-revoked A1 → 200 (idempotent);
  - already-revoked A2 → 403;
  - org-less key → 200 for both scoped and unscoped ADMINs (Kam 2026-09-03);
  - unscoped on A1 → 403;
  - lowercase `admin` bound;
  - another tenant's key → 403;
  - legacy stored forms: upper A1 200, padded A1 200, upper A2 403, **blank 200 (KS-1577)**, `default-org` 403;
  - unknown id 404;
  - a role with whitespace → 403.
- Develop: every bounded cell was 200/201.
- **Update paths:** PATCH/PUT `/api/keys/:id` → 404. The re-POST cannot reuse an id (the id is chosen server-side, and the INSERT's ON CONFLICT never updates `organization_id`). The originate mint (`adminConfig.ts:960`) is behind an exact `requireRole('SYSTEM_ADMIN','ORG_ADMIN')`. So **an unqualified key cannot be turned into an organisation key by update**. The list does not show it under any organisation (KS-1581). A scoped ADMIN still LISTS A2's keys, 200 (KS-1574, as the PR body says).
- **What an unqualified key can do** (code read, plus measured in M1): at the gateway it becomes role `connector` with `organizationId ''` and the scopes the ADMIN chose. decideMint lets a key admin choose ANY scope. The KS-695 erasure refuses an org-less caller (`connectorOrganisationErasure.ts:125`). **But with `organizations:register` it is a provisioner, and that is M1.**
- All 58 cells are **identical in both tenancy modes** (ledger byte-compare).

**5. Fail-closed** (`gate1535-c-failclosed…`). Head 5/5; **develop 4 red**, which is the control that these cells can fail.
- **Table DROPPED:** mint A1 → **500**, 0 minted; revoke an A1 key → **500**, key active; unqualified mint 201. Develop: 201 / 1 minted / 200 revoked.
- **App role cut off:** mint 500, revoke 500, 0 minted, key active.
- **SELECT revoked**, on a key held in memory: revoke 500, key active (develop 200).
- **Lock:** no allow while locked (see n3).
- After every case the table was restored from the migration file itself and FORCE RLS read back as `t`.

**6. RLS and the GUC** (`gate1535-b-guc…`, the service's own `pg.Pool` forced to **max 1 and max 2** via `vi.mock`, with the size asserted).
- 80 interleaved mints for two tenants and two ADMINs give 0 wrong verdicts. Develop pool 1: red (control).
- Server statement log (`log_statement=all` for `secuura_app`, parsed per backend pid) shows **160/160 scope reads in the same transaction, on the same connection, as `set_config('app.current_tenant_id', <the WHERE tenant>, true)`, 0 under the bypass**, over 3 backends.
- **Instrument control:** with mutant G1 applied, the same parser reports **80/80 MISMATCH+bypass**.
- No GUC is left behind: `current_setting` on the pool afterwards is empty or null, at both pool sizes.
- `runWithTenantId` replaces the async store, so the read can never run under an outer platform scope (code: `tenant-guc.ts:90-95`).

**7. Callers of the policy** (`git grep decideTenantAccess(|decideKeyRevoke(`, non-test):
- `security/index.ts:1183` (mint) and `:1424` (revoke): both resolve the scope.
- `originate/routes/adminConfig.ts:1057`: exact-match `requireRole('SYSTEM_ADMIN','ORG_ADMIN')` at `:38`, **not reachable by any ADMIN spelling**; passes no scope, so an ADMIN would be refused there (policy cell).
- `originate/services/connectorOrganisationErasure.ts:333`: hard-coded role `connector`.
- No other caller and no alias import. **No path hands the policy a scope from the request.** Both sites build it only from `getAdminOrganisationScope`. My mutant G2, which makes the body field honoured, is killed by the injection cell.

**8. Mutants** (`tools/mutants.py`). Each mutant runs alone on a green baseline (17 / 16 / 58 / 5). Every file is restored, the restore is checked with sha256 (all `restored=True`), and shared `dist` is rebuilt around every policy mutant (final dist = a clean build, `diff -r`). Raw logs: `results/mut/`, `results/mutants.json`.

| mutant | result | killed by (cell names) |
|---|---|---|
| M1 the ADMIN arm removed | KILLED | shared 8; author security 6 ("…naming A2 is refused 403…", "…NO scope rows…", "lowercase 'admin'…", "a scope row in ANOTHER tenant…", revoke ×2); gate A 33; gate C 2 |
| M2 the revoke site does not resolve the scope | KILLED | "an ADMIN scoped to {A1} revoking A1's key succeeds", "a scope read that FAILS on revoke…"; gate A 4; gate C "TABLE DROPPED", "SELECT revoked" |
| M3 raw compare | KILLED | shared "the comparison is normalised on BOTH sides…"; "the scope comparison is normalised…(201)"; gate A 4 (nbsp/tab/upper) |
| M4 absent scope = allow | KILLED | shared "an ABSENT scope is REFUSED…", "an ADMIN revoke with NO resolved scope…" (security unaffected, as expected: the sites always resolve) |
| M5 read without the GUC | KILLED | author 4 (A1 201 cells, revoke A1); gate A 15; gate C 2 |
| M6 bypass + no tenant WHERE (author's compound) | KILLED | "a scope row in ANOTHER tenant does not count", "{A1} naming A2", lowercase, revoke A2; gate A 14 |
| M7 case-sensitive role | KILLED | shared + author "lowercase 'admin'…"; gate A role admin/Admin/aDmIn, revoke lowercase |
| M8 failed read → empty scope | KILLED | author "a scope read that FAILS…" (mint and revoke); gate C 3 |
| M8b failed revoke read proceeds | KILLED | author "…FAILS on revoke is a 5xx…"; gate C 2 |
| M10 empty scope grants all | KILLED | shared 2, author 2 ("NO scope rows" mint and revoke), gate A 10 |
| M11 wrong user (tenant id twice) | KILLED | author 3, gate A 11, gate C 2 |
| **G1 bypass only, WHERE kept** | **SURVIVED** (equivalent; see n2) | none; only the statement-log instrument |
| G2 a body field pre-resolves the scope | KILLED | gate A "a body field naming a pre-resolved scope is ignored (403)" |
| G3 `sub` preferred over `userId` | KILLED | author 4, gate A 10 |
| G4 uuid guard removed | KILLED | gate A "userId non-uuid … grants nothing (403)" (500 under the mutant) |
| G5 a scoped ADMIN skips the tenant floor | KILLED | shared "the tenant floor still comes first…"; gate A cross-tenant cell |
| G6 decideKeyRevoke drops the scope | KILLED (tsc TS6133, but emitted) | shared 2, author "…revoking A1's key succeeds", gate A 4 |
| G7 failed revoke read → 403 | KILLED | author "…FAILS on revoke is a 5xx…", gate C "TABLE DROPPED", "SELECT revoked" |
| G8 mint resolves only for `'ADMIN'` | KILLED | author "lowercase 'admin'…", gate A Admin/aDmIn/admin |
| G9 mint reads on the raw truthy org | SURVIVED (equivalent: a whitespace org still decides `same-tenant`; it only adds a read) | none |
| C0 comment only | CONTROL OK | none |

**The author's 10 (plus M1) are re-derived and all killed. 7 of my 9 are killed; 2 equivalent survivors are named.**

**9. The three rewritten pins.**
- ks1533 RULED cell: 403, with `/admin organisation scope/`. With no database, `isDbAvailable()` false gives `[]`, so it fails for the right reason ("outside admin organisation scope").
- ks764: unresolved → refused; `{ORG_1}` → ORG_2 refused; `{ORG_2}` → allowed. The token claim plays no part.
- ks780 2 → 4: the two new calls are `normaliseOrgId(organisationScope.targetOrganizationId)` and `normaliseOrgId(o ?? null)` in the ADMIN arm. Both are correct and both go through the one implementation.
- **No existing cell still asserts the old reach.** grep of security and shared tests: `ks578-ks643` `ADMIN` cells use an org-less key, which stays allowed; `ks480` checks role admission only. The one stale text is n1.

**10. PR body.** I read the author's local body draft `5_Project_History/2026-10-13_seatV-6th/logs/pr_ks1570a_body.md` (placeholders `HEADSHA`/`PREFLIGHT_LINE`), **not the live GitHub body** (no `gh` call from this seat).
- Every number in it re-measured equal.
- The NOT-changed list is honest: the list is unbounded (KS-1574), the role vocabulary (KS-1536), the Admin Dashboard `default-org` mint will 403 for ADMINs (KS-1564), and "Do not deploy A alone".
- **What a reader could mistake for done:** the BLUF says an ADMIN "now mints … only for the organisations in its scope", and calls the erasure-trust hazard the reason. A reader would conclude the deploy blocker is closed by A+B+KS-1564. **M1 says it is not.**

## NOT tested
- The live PR body on GitHub.
- The gateway hop for M1 end-to-end. I built the connector bearer exactly from auth's `generateConnectorToken` claims (`auth/src/services/jwt.ts:281-297`) and this service's own `/api/keys/validate` output. The gateway proxies `/api/security/*` → security `/api/*` behind `authenticateToken` (`api-gateway/src/routes/proxy.ts:1189-1191`), which turns a valid `sk_` into that principal (`middleware/auth.ts:378-430`). The spec method allow-list was not exercised.
- The KS-695 erasure actually running against an M1 hop-2 key. That step is a code read only.
- Originate's full suite; the Admin Dashboard; any deployed stack; pgbouncer transaction pooling.
- A database shaped like production. The migration role and grants on Azure were not checked: the deploy seat must confirm that `secuura_app` has SELECT on the new table, or every org-naming ADMIN mint and revoke will 500 (fail closed, but an outage of that feature).
