#1242 KS-980 REALP1: the platform_bypass cell connects as secuura_app so P1 is its own mechanism
head a35569aa020e63b2660b60e48b4f0286c46b27fc

## BLUF

**The suite's header claimed it isolated two RLS-permissive paths. It exercised one.** `writerOn()` opened `TEST_DATABASE_URL` for **both**, and that role carries **BYPASSRLS** — so the P1 branch set `app.tenant_scope_bypass` on a connection RLS never constrained. The GUC was **inert**, and the documented platform-admin path had no coverage while the file said it did.

This is **option (1)** of the ticket's fix shape — make P1 real — and it **needed no new role, grant, migration or DB-level change**, so the ruled fallback to option (2) was never reached. `docker/init/01-create-app-role.sh` already creates `secuura_app` from `APP_DB_PASSWORD`, and `docker-compose.yml` already threads both variables. Only a second DSN was missing.

## The mechanism, measured on a live database rather than read off the schema

The policy on `organizations` is `tenant_isolation`, and it reads:

```
(current_setting('app.current_tenant_id') = tenant_id) OR (current_setting('app.tenant_scope_bypass') = 'platform_admin')
```

So the GUC is the documented admin door — **for a role the policy applies to at all**. On the disposable instance: `secuura` is `rolbypassrls=true` (the policy is never evaluated); `secuura_app` is `rolbypassrls=false`. That difference is the whole ticket.

## No credential enters the tree

The compose default password is **not** written here. A literal would be a credential in the repository, and it would silently stop matching any instance provisioned with its own value — failing as a *wrong password* rather than as a *missing setting*. Absent configuration **throws in `beforeAll`**; the suite is DB-gated and never skips silently. Verified: the diff contains zero occurrences of the compose default and zero of the throwaway used for these runs.

## Two cells that keep this true instead of describing it

- **D1** asserts P1's connection is **not** a BYPASSRLS role and P2's **is**.
- **D2** takes its connection from `writerOn()` **deliberately** — a locally built client would keep passing while the suite it guards regressed — and strips the admin GUC, which must make the other tenant's organisation disappear.

## Test Evidence

**Touched:** `Blockchain/Dev/services/originate/src/__tests__/ks597-issuer-organization-id.integration.test.ts` only (1 file, +93 / -2). **No product code changed.**

**Environment:** a disposable PostgreSQL built the way the file's own header names — `postgres:15-alpine` (the version `docker-compose.yml` pins), `docker/init` as `docker-entrypoint-initdb.d`, then `scripts/run-migrations.sh`: **applied=49, failed=0**, and the `_secuura_migrations` tracker independently reports **49** rather than trusting the runner's own summary line. Bound to `127.0.0.1` only, anonymous volume, generated throwaway credentials held outside the repository, destroyed afterwards.

**Ran** — `jest --config jest.integration.config.js --runInBand`:
- **Head: 6/6** on the target file. **Full originate integration suite (both `ks597` files): 14/14, 2 suites.**
- **Red proof, three arms, each naming why it reddens:**
  - **A + B — the ticket's own tamper** (the tenancy predicate removed from **both** `organizations` subqueries, 2/2 occurrences asserted before applying): the **P1 and P2 cells each fail**; both controls and D1/D2 stay green. Restore verified byte-identical by blob hash.
  - **C — the fix reverted** so both paths share `TEST_DATABASE_URL` again: **D1 and D2 fail** (`rolbypassrls` false vs **true**; with the GUC stripped, 0 rows vs **1**) **while the original four cells stay GREEN**. That is the ticket's claim demonstrated rather than asserted — the cells as they stood could not tell the two paths apart.
- **The DB-gate refuses loudly:** run without the app DSN, the suite exits **non-zero** naming what to set. It does not skip.
- `tsc` clean on the test file. Note: `tsc --noEmit -p tsconfig.json` does **not** cover it — the project tsconfig excludes `src/__tests__`, so it was typechecked directly.

**NOT run / NOT covered:**
- **Legs 3, 4 and 8** — the local platform stack was not started; this change has no route, spec, served-spec or runtime-config surface.
- **Not run against the shared dev stack or any deployed database.** Only a disposable instance. The file's header warns against the shared stack precisely because its schema drifts.
- **`TEST_APP_DATABASE_URL` was exercised only in its composed form** (`APP_DB_USER` + `APP_DB_PASSWORD`); the explicit-variable branch is one `if` and was not separately executed.
- **No CI wiring.** Nothing yet runs this integration config automatically, so these cells protect the property only when someone runs `test:integration` with both DSNs set.

**Migrations + config:** none added. No `package.json`, no `package-lock.json`, no schema change. The 49 migrations above were applied to a throwaway instance, not to anything shared.

Refs KS-980

---
*Raised on Wednesday's brief, tier 2, with the disposable-Postgres conditions from her 17:00 ANSWER. Base `d9515f4a06e0`.*

🤖 Generated with [Claude Code](https://claude.com/claude-code)

