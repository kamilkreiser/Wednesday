#1286 docs: correct the tenancy docs to the shared database the code actually uses
head da5f3dd837dd5b6c706e7816bd4028070029d5e1

## BLUF
Both tenancy documents describe a **per-tenant-database architecture that has never existed in any
deployed environment**. A reader of either overestimates the isolation in place. The worst of them is
the **Security Considerations** table, which told anyone checking the security posture that tenants
are physically separated with *"no shared tables"*.

Every claim below is measured at `00de57baeb405d0081fe8b6f192bd40d35acef61` and cited to the source
that implements it. **Nothing here is a plan or a recommendation** — whether the dormant path is
completed or removed is Kam's decision and is deliberately not recorded.

## What is true, and where it lives
- **Every tenant resolves to one shared application database.**
  `services/api-gateway/src/startup-migrations.ts:1116-1144` writes every `tenant_config` row with a
  single `db_name`, `db_host` and `db_port` taken from `DATABASE_URL`. Its own comment reads
  *"On Azure there is a single DB; per-tenant DBs are not provisioned."*
- **Isolation inside it is `tenant_id` + row-level security, fail-closed since
  `migrations/039_rls_fail_closed.sql`.** An unset `app.current_tenant_id` returns **zero** rows,
  where before 039 it returned **all** rows. The deliberate escape is
  `app.tenant_scope_bypass = 'platform_admin'` via `runWithPlatformScope`.
- **Two carve-outs keep 038's permissive policy, both named in 039's header:**
  `platform_document_registry` (public verify-by-hash is cross-tenant by design) and
  `svc_m365_connections` (its `tenant_id` holds the Microsoft/Entra directory id, so the comparison
  could never match).
- **The per-tenant path is dormant behind two flags set in no config file:**
  `MULTI_TENANCY_ENABLED` and `PROVISION_PER_TENANT_DB` (`tenant-pool-manager.ts:151-152`).
  *Control for that zero: 25 config files do mention `DATABASE_URL`, so the search is not blind.*

## FIVE assertions corrected in `MULTI-TENANCY.md`, not the two this change set out to fix
The extra three were found by **sweeping the file for the claim** rather than trusting the line
numbers I was handed. A docs PR that corrects one false line and leaves three standing is worse than
none, because the corrected line lends the rest credibility.

| where | was |
|---|---|
| `:13` summary | "Each client (tenant) receives an isolated PostgreSQL database" |
| `:16` key point | "Each tenant has its own PostgreSQL database (`secuura_tenant_{slug}`)" |
| the architecture **diagram** | drew `secuura_tenant_{slug}` beside `secuura_platform` as though it exists |
| **onboarding steps** | "Provisions a new PostgreSQL database" — a step that does not run |
| **Security Considerations** table | "Each tenant has its own PostgreSQL database — no shared tables" |

The benefits table is kept but re-cast as **intended vs. what holds today**, because three of its five
rows (independent backups, performance isolation, per-tenant residency/deletion) are **not available**
on a shared database and a reader is entitled to know which.

## `RLS-FAIL-CLOSED-PLAN.md` — `:35`, and its neighbour
`:35` claimed *"Real isolation is per-tenant databases."* **False, and false when written.**

Its neighbouring bullet claimed RLS was *"permanently on its fail-open branch — inert today"*. That was
true on 2026-05-29 and **039 has since made it false**. Correcting `:35` alone would have left the
document contradicting its own corrected line, so both are superseded in place. **This is one bullet
wider than the change was scoped to, and it is flagged rather than absorbed** — it can be reverted.

Both are struck through and superseded rather than deleted, because the document's later sections still
reason from them and a reader needs to know **which way** they changed. Everything from "The hard
problem" onwards is unreviewed against today's tree and is left marked a proposal; `status: proposed`
in the front matter is untouched.

## Verification
- **Re-swept after editing:** no live assertion of a per-tenant database remains in either file. The
  four remaining matches are my own correction notice, the struck-through quote, and a reference to
  KS-1055. *Control: the sweep still finds 4 occurrences of `secuura_tenant_`, so it is not silently
  matching nothing.*
- Docs-only: **no code, no migration, no config, no test** changes.
- Push gate `28/0 · 6/0 · 49/0 · 60 of 60`; preflight **12/15 legs ran, 3 SKIPPED (3, 4, 8 — no local
  stack), nothing failed** — not quoted as a pass.
- Base this worktree **CONTAINS**: `00de57baeb40`, develop's tip.

## NOT covered
- The readiness work itself is **not** done here; it is tracked on the parent ticket with its five
  children.
- `docs/TOKENISATION.md` and `docs/DEPLOYMENT.md` were **not** swept for the same drift — out of scope
  for this change, and worth a look by whoever picks up the parent.
- No opinion is offered on whether to build or delete the dormant path.

Refs KS-1336

