KS-1054 Fresh databases are FAIL-OPEN until the second boot — 039_rls_fail_closed does not apply on boot 1 (file stage runs before the CORE stage it depends on)
state In Progress

## BLUF

**On a freshly provisioned database,** `users.tenant_isolation` **is FAIL-OPEN after the first boot — an unset tenant GUC sees ALL rows.** `039_rls_fail_closed.sql` does not apply on boot 1 because the file stage runs **before** the CORE stage that creates a table it depends on. Seven file migrations fail on boot 1; all seven succeed on boot 2.

⚠ **PRODUCTION IS NOT IMPLICATED by this mechanism.** A long-lived database already has the dependency tables, so `039` applies on the first boot after deploy. **The exposure is freshly provisioned databases: new environments, CI and local stacks, DR restores, and newly provisioned tenant DBs.**

## Provenance — this is the QA gate's measurement, not mine

Measured by the cross-project QA agent on 2026-09-09 against PR #928, on a real `postgres:15-alpine` driven by **the product's own** `runStartupMigrations()` via `tsx`, `MIGRATIONS_DIR` pointed at the repo `migrations/`, a fresh database per side. Report: `2026-09-09-s161-batch-six-prs/report.md` §2, with boot transcripts in its `evidence/` directory.

**I have NOT re-run it.** Filed because §2 of that report says it bears on the deploy hold and asks for it loudly. The numbers below are relayed; the mechanism is the gate's, and the pre-deploy check is the gate's own recommendation.

## The measurement

```
after boot 1:  USING ( current_setting('app.current_tenant_id',true) IS NULL
                       OR current_setting(...) = ''
                       OR tenant_id::text = current_setting(...) )      <-- unset GUC sees ALL rows

after boot 2:  USING ( current_setting(...) IS NOT NULL AND <> ''
                       AND tenant_id::text = current_setting(...) )
                     OR current_setting('app.tenant_scope_bypass',true) = 'platform_admin'
               + policy users_auth_lookup
```

`039` fails on boot 1 with `type "oauth_apps" does not exist` — the file stage runs before the CORE_MIGRATIONS stage that creates that table.

**Seven file migrations fail on boot 1 and all seven succeed on boot 2:** `006, 008, 026, 027, 028, 039, 047`. `048_ks754_widen_processed_by_to_text.sql` **applied cleanly on boot 1.**

## Why it matters beyond the fresh DB

**Both #928 and #929 assume** `039` **is in force.** #929's whole justification is that fail-closed RLS with an unresolved tenant GUC produces a 0-row UPDATE. On a database where `039` has not applied, that condition does not arise from that cause — **and cross-tenant rows are visible.**

The same assumption runs through **KS-1052** (the credential-lifecycle guards) and the KS-963 work.

## 🔴 Pre-deploy check — put this on any deploy that touches these services

On the **target** database, confirm **both**:

1. `048` is present in `_secuura_migrations`.
2. `pg_policy` for `users.tenant_isolation` shows the `IS NOT NULL AND <> ''` form — **not** the `IS NULL OR = ''` form.

⚠ `run-migrations.sh` **exits 0 when migrations fail**, so compose's own gate does not catch this. The check has to be made against the database, not inferred from a runner's exit code.

## Related, un-driven, and probably the more serious half

**QA F-928-3 (read from source, NOT measured):** the tenant loop calls `migrateDatabase(pg, tenantConnStr, tenantDbName, CORE_MIGRATIONS)` only — **it never calls** `applyFileMigrations`. If `039` exists only as a file, **tenant databases never receive the fail-closed flip at all**, on any boot. The gate never configured `PLATFORM_DATABASE_URL` and provisioned no tenant DB, so this is a code-path reading and not a measurement. **It should be measured before it is believed, and if true it is worse than the boot-1 window** — a permanent state rather than a transient one.

## Fix shapes (not a ruling)

1. **Order the stages by dependency** — run the CORE stage before the file stage, or make `039` tolerate the absent table and re-assert later.
2. **Make boot-1 failure visible where it counts:** related to **F-928-2** (migration failure is still log-only; `runStartupMigrations()` is `Promise<void>`, so no call site can branch on `failed`). That is a design decision with deploy consequences and is **Kam's**, tracked separately.
3. **Provisioning-time assertion** — a new environment is not "ready" until the `pg_policy` shape check above passes.

## Related

* **KS-1052** — the credential-lifecycle guards that assume `039` is in force.
* PR **#928** (KS-950) — surfaced this; its `INCOMPLETE — 7 FAILED` log line is the first thing in the system that says so out loud.
* PR **#929** (KS-943).

*Filed by s162, 2026-09-09, on Wednesday's brief item 4. Numbers relayed from the QA gate and labelled as such.*
