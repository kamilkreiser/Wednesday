# Per-tenant databases — planning document (Secuura Platform K)

**For:** Kam · **From:** a planning researcher working for Wednesday · **Date:** 2026-09-26
**Trigger:** Kam's ruling on card `secuura-ks1304-withtenant-tenant-pool-and-admin-writes`, option (c), note "start planning the database".
**Read at:** `develop` @ `df5e9f5da6d2` (2026-09-25, "KS-1120 …"). The local clone does not have this commit; the tree was read from the GitHub tarball of that exact SHA. All paths below are under `Blockchain/Dev/` unless stated otherwise.
**Nothing was changed.** No code, no tickets, no mail.

---

## 1. BLUF

1. **Today every tenant shares one database.** Isolation comes from a `tenant_id` column plus row-level security (RLS) that fails closed. A per-tenant-database path exists in the code, but it is switched off: `PROVISION_PER_TENANT_DB` is set in 0 config files.
2. **The dormant path is not safe to switch on.** Five open tickets (KS-1304, KS-1235, KS-1055, KS-1054, KS-598) each break it in a different way. KS-1055 was measured: a new tenant database comes up with RLS forced on and zero policies, so the app can read nothing from it.
3. **The docs describe a system that does not exist.** `docs/MULTI-TENANCY.md:13-17` says "each tenant has its own PostgreSQL database". It does not.
4. **Recommendation: a hybrid.** Keep one shared control plane (tenant registry, login, the verify-by-hash registry). Keep the shared database with RLS as the default tier. Offer a dedicated database as an opt-in tier. Build it in four phases, each ending in a test.
5. **The one decision Kam must make first:** *why* we want per-tenant databases. Is there a named customer or contract that needs physical separation (data residency, per-tenant restore or deletion, their own keys), or is this defence in depth? The answer decides between "build the opt-in tier" and "delete the dormant path and harden RLS".

---

## 2. What exists today (measured)

"Measured" here means read from source at `df5e9f5d` with the instrument named. Nothing was run against a live database.

### 2.1 Databases
- **Two logical databases.** `secuura` holds all tenants' business data. `secuura_platform` is the control plane (`tenants`, `tenant_config`, `tenant_contacts`, `vault_entries`, `platform_document_registry`, `platform_audit_log`). Source: the table list in `docs/MULTI-TENANCY.md:214-221` and the queries in `tenant-pool-manager.ts:300-306`.
- **Azure declares only `secuura`** (`deployment/azure/main.bicep:229-231`; a grep for `secuura_platform` in main.bicep gives 0 hits). How `secuura_platform` gets created on Azure is UNMEASURED.
- **One small server.** `main.bicep:199-216`: `Standard_B1ms`, Burstable tier, 32 GB, 7-day backups, geo-redundant backup off, HA off.
- **Local stack:** one `postgres` service plus `pgbouncer` (`docker-compose.yml:107`, `:250`). App services connect as `secuura_app` through pgbouncer, and to the platform DB directly (for example `:581-582`).
- **Note:** `docker-compose.yml` commits a default password for `secuura_app` (for example `:473`). It is a dev default, and its value is not repeated here. It matters later, because per-tenant pools reuse this one credential.

### 2.2 Shared DB with `tenant_id` and RLS (the mechanism that actually isolates)
- **Migrations:** 49 `.sql` files in `migrations/`. 16 contain `CREATE POLICY` (19 statements in total), 16 `ENABLE ROW LEVEL SECURITY`, 15 `FORCE ROW LEVEL SECURITY` (case-insensitive grep).
- **Policy set:** `038_rls_consolidate_policy.sql:39-58` lists 27 tables. `039_rls_fail_closed.sql` makes 25 of them fail closed and excludes `platform_document_registry` (public verify-by-hash) and `svc_m365_connections` (its `tenant_id` holds a Microsoft directory ID) (header at `:1-58`). This matches KS-1055's measured main DB: 25 RLS tables, 28 policies.
- **The tenant is carried in three settings (GUCs):**
  - `app.current_tenant_id` — set by `packages/shared/src/db/tenant-guc.ts:146`.
  - `app.tenant_scope_bypass='platform_admin'` — set by `tenant-guc.ts:139`, the deliberate cross-tenant scope.
  - `app.tenant_id` — used only for `rights_holders` (KS-108), set in `services/originate/src/db.ts:311`.
  - Grep for `set_config('app.` in non-test TS: 10 hits in 4 files.
- **Runtime role:** `secuura_app` is created `NOSUPERUSER NOINHERIT NOBYPASSRLS` (`services/api-gateway/src/startup-migrations.ts:890-892`). Pre-auth lookups (login by email, OAuth client, API key by hash) go through `SECURITY DEFINER` functions owned by the NOLOGIN role `secuura_auth_lookup` (`039` header, item 3).
- **Request wiring:** 10 service files mount `tenantGucContext()` (grep). The runtime binding on Azure dev and demo was reported done under KS-109 (ticket comment, 2026-05-22). It was not re-verified here.

### 2.3 The per-tenant-DB path (present, switched off)
- **Router:** `TenantPoolManager.getPool` (`packages/shared/src/db/tenant-pool-manager.ts:201-264`) returns a dedicated pool only when both are true:
  - `MULTI_TENANCY_ENABLED` is on (`:151`) and `PROVISION_PER_TENANT_DB === 'true'` (`:152`);
  - the tenant's `tenant_config` row points at a different host, port or database (`:233`, `resolvesToDefaultDb` `:106-124`).
- **Pool budget:** up to 50 pools × 5 connections, plus default 10 and platform 3 (`:66-67`, `:155-171`). That exact fan-out caused KS-213: originate starved pgbouncer on dev with about 263 possible connections. The flag gate is the KS-213 fix.
- **The flag is set nowhere.** A grep for `PROVISION_PER_TENANT_DB` over `*.yml, *.yaml, *.json, *.bicep, *.sh` in the whole repo gives **0 files**. It appears in exactly 2 source files (the pool manager and `services/tenant-provisioning/src/index.ts:245`).
- **Control, same grep for `MULTI_TENANCY_ENABLED`:**
  - 24 compose lines, all defaulting to `false`;
  - `env.dev.json:7` and `env.demo.json:7` set it `true`;
  - `services.bicep:798` sets it `true` for the originate container only.
- **Provisioning:** `tenant-provisioning/src/index.ts:245-257` calls `createTenantDatabase` only behind the flag. That function (`:62-120`) runs `CREATE DATABASE … OWNER <admin>` (`:82`) and applies `docker/init/*.sql`. Those are 12 files with **0** `CREATE POLICY` (control: 16 files in `migrations/`).
- **Migrations never reach tenant DBs properly.** The gateway's tenant loop (`startup-migrations.ts:1158-1186`) runs only the legacy `CORE_MIGRATIONS` array. `applyFileMigrations` accepts only `'main' | 'platform'` (`:86`), so a tenant DB is not even a type it admits. `CREATE POLICY` appears 0 times in `startup-migrations.ts` (grep -ci). Under KS-1055 a seat measured the result on real Postgres: a tenant DB with FORCE RLS on 5 tables and 0 policies, so the app role reads 0 rows.
- **Credentials:** a dedicated pool reuses the default URL's user and password (`tenant-pool-manager.ts:247-249`). Whether `secuura_app` gets grants inside a newly created tenant DB is UNMEASURED. KS-109 says the grants were given on `secuura` and `secuura_platform` only.

### 2.4 Who actually routes through the pool manager
- **17 services** construct a `TenantPoolManager` (grep `new TenantPoolManager`, non-test).
- **15 of them are dead wiring.** Each exposes `getTenantPool()`, which has **0 callers** outside the `db.ts` that defines it (grep over `services/`). Their `tenantManager.` usage is exactly 2 per file: `init` plus that uncalled getter.
- **Only two services really route:**
  - **originate.** Request middleware sets `req.db` to the tenant pool (`services/originate/src/index.ts:217-231`, via `extractTenantContext`, `packages/shared/src/db/tenant-context.ts:93`). Four cross-tenant fan-outs look up the registry in the platform DB and then open that tenant's pool: `routes/verification.ts:434`, `routes/verificationV2.ts:351`, `routes/documents.ts:1016`, `routes/adminConfig.ts:2065`.
  - **auth.** `services/auth/src/db.ts:53-60` sends tenant-argument queries to `getPool(tenantId).query()` with no GUC (KS-1235).

### 2.5 `withTenant` and the admin-config router (the KS-1304 question)
- **`withTenant` always uses the shared pool.** `services/originate/src/db.ts:302-339` checks out from `tenantManager.getDefaultPool()` (`:308`) and sets both GUCs.
- **11 non-test call sites** (grep `withTenant(`), which confirms the seat's count:
  - **9 in `routes/adminConfig.ts`:** `:834, 1252, 1295, 1330, 1392, 1417, 1467, 1475, 1987`. All 9 touch `rights_holders`. **6 are writes** (834, 1330, 1392, 1417, 1475, 1987) and **3 are reads** (1252, 1295, 1467). The card said "9 admin-config writes"; the measured split is 6 plus 3.
  - **2 in `routes/documents.ts`:** `:1830` and `:2264` (`/share`, `/transfer-custody`, from KS-1263 / #1239).
- **The admin router is shared-DB by design:** `adminConfig.ts:28-35` sets `(req as any).db = prisma // Always shared DB` and says the admin tenant selector is "for SETUP/CONFIG, not for browsing client data".
- **So KS-1304 is really a classification question.** Is `rights_holders` control-plane config, or tenant business data? The answer decides which pool those 9 calls belong on.

### 2.6 Documentation drift
- `docs/MULTI-TENANCY.md:13-17, 83-99` (dated 2026-03-09) states that every tenant has `secuura_tenant_{slug}`.
- `docs/RLS-FAIL-CLOSED-PLAN.md:35` says "Real isolation is per-tenant databases."
- Both are false at `df5e9f5d`: every tenant resolves to the shared DB (`startup-migrations.ts:1116-1144` seeds every `tenant_config` row pointing at the shared DB). Anyone reading those docs will overestimate the isolation.

### 2.7 The board (Linear, team KS)
- **Instrument:** full pagination of `issues(includeArchived:true, filter team KS)` with `comments(first:100)`. That was 27 pages, **1,323 issues and 3,759 comments**. The largest comment count on one issue is 71, so no issue was truncated. Search was a local case-insensitive regex over title, description and every comment.

| term | total | open | open IDs |
|---|---|---|---|
| per-tenant db/database | 8 | 3 | KS-1235, 1055, 1054 |
| `PROVISION_PER_TENANT_DB` | 6 | 4 | KS-1304, 1235, 1055, 1054 |
| dedicated (tenant) db | 1 | 1 | KS-1304 |
| database-per-tenant / schema-per-tenant | 0 / 0 | — | — |
| tenant isolation | 44 | 7 | KS-955, 748, 745, 696, 492, 485, 229 |
| RLS (word) | 104 | 31 | (incl. KS-1311, 1306, 1235, 1055, 1054, 1050, 968, 699) |
| TenantPoolManager | 11 | 3 | KS-1304, 1235, 174 |
| `MULTI_TENANCY_ENABLED` | 16 | 10 | incl. KS-598, 1119, 1305, 174 |
| nonsense control `zqxjvkwplm` | 0 | 0 | — |

- **KS-1304** (Backlog, Minor) has 0 comments and no linked relations.
- **The KS-160 epic is Done.** Its "Path A" (2026-05-29) was **RLS fail-closed, not per-tenant DBs**. Its child **KS-174** is still In Progress.
- **No ticket owns the per-tenant-DB build itself.** The five open defects sit on the dormant path with no epic above them.

---

## 3. Options

"WP" = a ticket-sized work package (one PR, one QA gate). "Isolation" means what stops tenant A's rows reaching tenant B when code forgets a filter.

| | **A. Shared DB + RLS, hardened** | **B. Schema per tenant** | **C. Database per tenant (everyone)** | **D. Hybrid: shared control plane + shared tier + opt-in dedicated DB** |
|---|---|---|---|---|
| **Isolation** | Logical. RLS fail-closed on 25 tables, one role, one GUC. Strong against forgotten filters; weak against a bad bypass call or a superuser path. | Medium. `search_path` per request; one bad path reads another schema. RLS is still needed as a backstop. | Strong. A wrong pool is a failed connection, not a leak. Separate backup, restore and drop per tenant. | Strong for dedicated tenants, same as A for the rest. |
| **Migration cost** | Low. Nothing moves. | High. Every query and migration must become schema-aware; none are today (0 hits for schema-per-tenant on the board or in the code). | High. About 100 tenants on dev (KS-213, relayed) move to about 100 DBs. `users` and login must stay shared or login breaks. | Medium. Nothing moves by default; a tenant moves only when it buys the tier. |
| **Operational cost** | One DB, one backup, one migration run. | One DB, but N schemas to migrate; catalog bloat. | N DBs to migrate, back up, monitor and grant. Azure PITR restores whole servers, not one DB (vendor behaviour, not measured), so per-tenant restore means logical dumps. The B1ms tier's connection ceiling will not hold 50 × 5 pools (see Risk R1). | N is small (only paying tenants). Needs the same tooling as C, at smaller scale. |
| **What breaks** | Nothing new. Delete the dormant path (17 managers, provisioning branch) or leave it rotting. | Prisma client, raw SQL, every migration file. | Cross-tenant verify-by-hash (4 fan-out sites), admin views, joins to `users`, the KS-598 registry upsert, every open defect in §2.3. | The same as C, but only on the opt-in path. |
| **Effort (rough)** | 4–6 WPs | 12–18 WPs | 18–25 WPs plus a data migration | 12–16 WPs over four phases (§4) |

**Option A detail (for the default):**
1. Delete the dead wiring in 15 services.
2. Fix KS-1235 or remove the tenant-pool branch in auth.
3. Close KS-1054 (boot order) and KS-174.
4. Correct the two docs.
5. Add a fail-closed regression suite as `secuura_app`.

---

## 4. Recommendation and phased plan

**Recommend D, built on A.**

**Why:**
- The code already assumes D. `resolvesToDefaultDb` (`tenant-pool-manager.ts:106-124`) lets shared and dedicated tenants live side by side.
- The control plane already lives in its own database (`secuura_platform`).
- Every phase-1 fix below is also a fix that A needs, so nothing is wasted if Kam later picks A.
- Moving everyone (C) buys little for demo and test tenants and multiplies the operations load on one Burstable server.
- Schemas (B) would rewrite every query for weaker isolation than C.

**Phase 0 — decisions (Kam, with Wednesday relaying).**
- Settle the decisions in §6.
- A seat produces a **table classification** for every table: *control plane* (platform DB), *tenant data* (tenant DB), or *global by design* (registry, login directory). This is a doc-only PR, like KS-172's inventory.
- It must rule on `rights_holders`. That ruling decides KS-1304.
- **Test:** Kam signs the classification. Wednesday opens one epic and links KS-1304, 1235, 1055, 1054 and 598 under it.

**Phase 1 — groundwork, flag still off, no behaviour change (6–7 WPs).**
1. One routing chokepoint. `withTenant` takes its pool from `getPool(tenantId)` for tables classified as tenant data, and from the shared pool for control plane (KS-1304's fix shape). Cell: with a stub where `getPool(t) !== getDefaultPool()`, both writes land on `getPool(t)`.
2. Migration runner for tenant DBs. `applyFileMigrations` accepts a tenant target and the tenant loop calls it (KS-1055). Fix the boot-1 order (KS-1054). Make the runner exit non-zero on failure (KS-1054 notes `run-migrations.sh` exits 0).
3. Provisioning completes the job:
   - `CREATE DATABASE`, then full file migrations, then `secuura_app` grants inside the new DB, then record the schema version in `tenant_config`;
   - deprovisioning drops the database cleanly.
4. auth: add the GUC to the tenant-pool branch, or remove it (KS-1235).
5. Registry upsert re-keyed on document UUID (KS-598). This is needed before `MULTI_TENANCY_ENABLED` is trusted anywhere.
6. Delete the dead `TenantPoolManager` wiring in the 15 non-routing services, or route them. Their data would otherwise stay in the shared DB for a dedicated tenant.
7. Correct `docs/MULTI-TENANCY.md` and `RLS-FAIL-CLOSED-PLAN.md`.

**Test:** a new CI job runs with the flag on and three tenants: one on the shared DB and two on dedicated DBs.
- The full suite passes.
- `systemTest/schemathesis/tests/test_tenant_isolation.py` passes.
- A new cell runs as `secuura_app` against each tenant DB. `pg_policy` must be greater than 0, and a no-GUC read must return 0 rows while a scoped read returns the rows.

**Phase 2 — dev pilot (2–3 WPs).**
- Provision one synthetic tenant on a dedicated DB on the dev server.
- Measure the connection budget through pgbouncer, with a per-database pool size and a lower `maxPools`.
- **Test:**
  - e2e v2 is green for both tenants;
  - the cross-tenant verify-by-hash finds a document held in the dedicated DB;
  - measured peak connections stay under the server's ceiling, with the number recorded.

**Phase 3 — operations (3–4 WPs).**
- Per-tenant logical backup and restore (`pg_dump` per DB on a schedule, into the existing backup storage).
- A migration fan-out status table: which DB is at which version, with alerts on drift.
- A tenant **move** tool (shared to dedicated) with a row-count reconciliation.
- **Test:** a restore drill and a move drill on dev. Row counts must match before and after; isolation cells must stay green.

**Phase 4 — first real tenant (1–2 WPs, approval-class).**
- Only for a named customer, only with Kam's explicit go.
- Only after a demo-environment rehearsal.
- Production is never touched without that approval.
- **Test:** the same drills on the target environment, with the pre-deploy checks from KS-1054 run against the database.

---

## 5. Risks and unknowns

| # | Risk | Proof that retires it |
|---|---|---|
| R1 | **Connection ceiling.** The B1ms tier is small (Azure documents about 50 user connections for B1ms; not measured here). The default budget is 50 × 5 plus 13. KS-213 already starved pgbouncer once. | Phase 2 measured peak; `maxPools` and pool size set from that number. |
| R2 | **Migration drift across N DBs.** A tenant DB silently behind is how KS-1055 happened. | Phase 1 cell plus the Phase 3 version table and alert. |
| R3 | **Cross-DB integrity.** `users` stays shared while documents move, so no foreign keys are possible (KS-699 already reports 0 FKs to `users`). | The classification doc names every cross-DB reference; a Phase 2 e2e covers each. |
| R4 | **Login is pre-tenant** (the `039` SECURITY DEFINER carve-out). Moving `users` would break login. | Decision 3 below keeps login in the control plane. |
| R5 | **Live config unknown.** `services.bicep:798` turns multi-tenancy on for originate, while the K-side plan sheet (`1_Project_Definition/architecture/2026-08-07_K-side-plan-sheet.md:39-40`) says it is off on local and demo. If it is on, KS-598 and KS-1235 may already be live. | An `az` read-only check of the originate container env on dev and demo by the Secuura seat, under the Secuura tenant only. |
| R6 | **Grants in new DBs.** If `secuura_app` has no rights in a created DB, the tenant is dark. | Phase 1 provisioning cell. |
| R7 | **One shared credential** for every tenant DB (`tenant-pool-manager.ts:247-249`), so dedicated DBs do not add credential isolation. | Decision 4; per-tenant roles are a later WP if a contract needs them. |
| R8 | **Cost.** Dedicated servers per tenant multiply the Azure bill. | Decision 4 defaults to the same server. |

---

## 6. Decisions only Kam can make

1. **Why per-tenant DBs?**
   - Options: (a) a named customer or contract requirement; (b) a general sales and security posture; (c) no current driver.
   - **Recommend (a) or (b):** build Phases 0–2 now and stop before Phase 4 until a named tenant exists.
   - **Default if no answer:** (b), Phases 0–2 only.
2. **Who gets a dedicated DB?**
   - Options: everyone (C), or opt-in per tenant (D).
   - **Recommend opt-in. Default:** opt-in.
3. **Where does login and identity live?**
   - Options: shared control plane, or per tenant.
   - **Recommend shared** (login cannot know the tenant before it runs). **Default:** shared.
4. **Where do dedicated DBs run?**
   - Options: same Azure server; separate server per tenant; a larger shared server.
   - **Recommend the same server** until a contract demands a separate one, with a server SKU review at Phase 2 (R1). **Default:** same server.
5. **Is `rights_holders` (the 9 `withTenant` calls) control plane or tenant data?**
   - Options: control plane (the admin router stays "always shared DB"; KS-1304 becomes a docs fix plus the 2 documents calls), or tenant data (all 11 calls follow the tenant pool).
   - **Recommend tenant data.** Rights holders are a tenant's customers, and `rights_holders` already carries a tenant GUC and RLS (027). **Default:** decided by the Phase 0 classification doc.
6. **What happens to the five open defects now?**
   - Options: one epic now; or leave them in Backlog.
   - **Recommend one epic**, with KS-1304, 1235, 1055, 1054 and 598 as Phase 1 work. **Default:** epic.
7. **What happens to the dead pool-manager wiring in 15 services?**
   - Options: delete; route it; leave it.
   - **Recommend delete in Phase 1** unless the classification puts their tables in tenant DBs. **Default:** delete.

---

## 7. NOT measured

- **No live database, no `az`, no running service.** Every claim is from source at `df5e9f5d` or relayed from tickets.
- **Relayed, not re-run here:** the numbers from KS-1055, KS-1054 and KS-213.
- **The live value of `MULTI_TENANCY_ENABLED`** and `PLATFORM_DATABASE_URL` on Azure dev and demo, and whether deploy consumes `env.*.json`.
- **How `secuura_platform` is created on Azure.**
- **Whether `secuura_app` gets grants in a newly created tenant DB.**
- **The real tenant count per environment.** About 100 on dev comes from KS-213's log, dated 2026-06-09.
- **The B1ms connection limit.** It comes from vendor documentation, not this repo.
- **Azure per-database restore behaviour** (vendor behaviour, not tested).
- **A full census of auth callers that pass `tenantId`.** A single-line regex found 1; KS-1235 read 2. Neither is a census.
- **Effort figures** are judgement, not measurement.
