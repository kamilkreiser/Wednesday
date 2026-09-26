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

--- comment 5843252951 by kksecura at 2026-09-26T04:43:11Z
## FIX ROUND 1 of 2 — N-1286-1 TWO-FLAGS-FALSE. New head `da5f3dd837dd5b6c706e7816bd4028070029d5e1`

**The blocking finding is mine, and it is the exact failure this PR exists to correct.**

I measured `PROVISION_PER_TENANT_DB` across `.env` / `.example` / `.yml` / `.yaml` / `.json` and found
zero. I then wrote, **twice**, that *"two flags"* are *"set in **no** configuration file"* — generalising
from a search that never looked at the second flag and never covered `.bicep` at all. A claim wider
than its measurement, written into a document I was correcting **for making claims wider than the code**.

### What is true, each citation read at the line before writing it
| flag | state | where |
|---|---|---|
| `PROVISION_PER_TENANT_DB` | **set in no configuration file** — absent from `deployment/` entirely | `tenant-pool-manager.ts:152`, `tenant-provisioning/src/index.ts:245` |
| `MULTI_TENANCY_ENABLED` | **`"true"` in dev and demo** | `deployment/azure/env.dev.json:7`, `env.demo.json:7`, `services.bicep:798` |

The distinction matters: `PROVISION_PER_TENANT_DB` is the flag that actually gates per-tenant
databases and it is off everywhere; `MULTI_TENANCY_ENABLED` enables tenant **routing**, and with the
other flag off every tenant still routes to the shared database. **The conclusion each sentence
supported is unchanged and still holds** — the per-tenant path is dormant, because the flag that gates
it is off. Only the reason was wrong.

### Also in this round — N-1286-2, the one-line citation
The onboarding step cited `startup-migrations.ts:1116-1144`, which is the boot seed of 8 fixed tenant
ids. A **new** tenant's `tenant_config` row is written by
`tenant-provisioning/src/index.ts:245-274`, the INSERT at `:271`. Both lines read before citing them.

### NOT in this round, and named rather than quietly folded in
The gate raised four more notes. The GO authorised the two sentences plus the one-line citation and
said *"change nothing else"*, so these are **not** done here:
- **N-1286-3** — *"writes **every** `tenant_config` row"* is wrong for the cited block (it is the 8
  seeded ids; provisioning writes the rest).
- **N-1286-4** — *"the only tenant isolation that exists"* is overstated: 21 non-test service files
  also filter on `tenant_id` at the application layer.
- **N-1286-5** — RLS-plan `:57`'s third bullet still reasons from per-tenant DBs, unmarked.
- **N-1286-6** — *"**The** deliberate exception"* omits 039 §3's `secuura_auth_lookup` path.

Each is a real correction and each would widen this round past what was authorised.

### Test Evidence
Docs-only: **no code, no migration, no config, no test**. Diff is **22 changed lines** across the two
documents. Base this worktree CONTAINS `00de57baeb40`; no merge-in.
Push gate `28/0 · 6/0 · 49/0 · 60 passed, 0 failed, 0 skipped (of 60)`; preflight **12/15 legs ran,
3 SKIPPED (3, 4, 8 — no local stack), nothing failed** — not quoted as a pass.
Re-swept after editing: **no surviving claim that both flags are unset**.

Refs KS-1336
