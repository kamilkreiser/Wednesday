--- comment 5841924450 by linear[bot] at 2026-09-26T01:25:07Z
<!-- linear-linkback -->
<details>
<summary><a href="https://linear.app/secuura/issue/KS-1336/per-tenant-db-readiness-the-dormant-per-tenant-database-path-and-the">KS-1336 Per-tenant DB readiness: the dormant per-tenant-database path, and the five tickets that each break it</a></summary>
<p>

## BLUF

**Every tenant shares one database today.** Isolation comes from a `tenant_id` column plus
fail-closed RLS. A per-tenant-database path exists in the code and is **switched off**. This is the
parent for the five tickets that each break that path in a different way, so the work has one place
rather than five.

**Nothing is built by this ticket.** It exists because Kam ruled option (c) on KS-1304 — *"Leave it*
*until per-tenant databases are actually planned. Nothing changes. The ticket keeps the measurement for*
*whoever builds per-tenant databases"* (2026-09-26 07:19) — with the note **"start planning the**
**database"**. This ticket is the artefact that carries that ruling onto the board.

## Measured at `00de57baeb405d0081fe8b6f192bd40d35acef61` (develop's tip), by this seat

Re-measured here rather than carried over from the planning document, which read an older tree.

1. **The flag is set in 0 config files.** `PROVISION_PER_TENANT_DB` occurs in exactly **two source**
   **files** — `packages/shared/src/db/tenant-pool-manager.ts:152` and
   `services/tenant-provisioning/src/index.ts:245` — and in **no** `.env`, `.example`, `.yml`,
   `.yaml` or `.json` config file. *Control: 25 config files do mention* `DATABASE_URL`*, so the*
   *config-file search is not blind.*
2. **Every tenant is seeded onto the shared database, and the code says so in its own comment.**
   `services/api-gateway/src/startup-migrations.ts:1116-1144` writes all eight `tenant_config` rows
   with the same `db_name`, `db_host` and `db_port`, derived from `DATABASE_URL`. The comment at
   `:1116-1117` reads: *"Ensure all tenants have a tenant_config entry pointing to the shared*
   *'secuura' database. On Azure there is a single DB; per-tenant DBs are not provisioned."*
3. **The docs state the opposite.** `docs/MULTI-TENANCY.md:13` — *"Each client (tenant) receives an*
   *isolated PostgreSQL database"* — and `:16` — *"Each tenant has its own PostgreSQL database*
   *(*`secuura_tenant_{slug}`*)"*. `docs/RLS-FAIL-CLOSED-PLAN.md:35` — *"Real isolation is per-tenant*
   *databases."* **The second of those is internally contradictory**: the two lines immediately above
   it say RLS is *"permanently on its fail-open branch — inert today"*, so that document simultaneously
   says isolation comes from per-tenant databases and that the mechanism which would route to them is
   not in use. A reader of either doc will overestimate the isolation that exists.

A docs PR correcting both files is raised separately and links here.

## The five tickets, and why each blocks switching the path on

* **KS-1304** — `documents.ts` mixes a tenant-pool read with a default-pool write. Ruled (c): left
  until per-tenant databases are planned. `adminConfig.ts` carries 9 of the 11 `withTenant(` sites.
* **KS-1235** — auth's tenant-pool statements carry no tenant GUC.
* **KS-1055** — per-tenant databases never receive the file migrations. Measured on that ticket: a new
  tenant database comes up with RLS forced on and **zero policies**, so the app can read nothing.
* **KS-1054** — migration-runner ordering and exit status.
* **KS-598** — the MULTI_TENANCY registry upsert silently collapses. **KS-598 keeps KS-772 as its**
  **parent** (Stuart's review stream — re-parenting it would silently remove an item from a human's
  queue) and is linked here as *related* instead.

## What this ticket is NOT

* It does not choose between building the opt-in dedicated-database tier and deleting the dormant path
  and hardening RLS. **That decision is Kam's**, and it turns on whether a named customer or contract
  needs physical separation (data residency, per-tenant restore or deletion, customer-held keys) or
  whether this is defence in depth.
* It carries **facts only**. The planning document's recommendations and phasing are deliberately not
  reproduced here, so the board does not record a plan as though it were agreed.

## Search before filing

`searchIssues`, KS team, `includeArchived: true`, every page literal-matched client-side:
`per-tenant DB readiness` **0**, `tenant database readiness` **0**, `dedicated database tier` **0**;
`PROVISION_PER_TENANT_DB` returns **3** — KS-1055, KS-1304, KS-1235, i.e. the children, **no parent**;
`per-tenant database` returns 2, both children. Controls: `tenant` **49** literal hits and
`multi-tenancy` **8** (the matcher fires), a nonce token never written anywhere **0**.
</p>
</details>
<!-- linear-review-link -->
<p><a href="https://linear.app/secuura/review/docs-correct-the-tenancy-docs-to-the-shared-database-the-code-actually-3669363ed09c">Review in Linear</a></p>

