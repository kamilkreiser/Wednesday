#1332 KS-1054: a failed start-up migration shows on /health; 039 guards oauth_apps
head f5381338359da43784f01f625772abafccdf97b6

## BLUF
Two halves of one boot-1 failure, both ruled by Kam as option **a** ("Keep serving, flag it on
/health"), with the `/health` shape ruled by Wednesday.

**The stage order.** `039_rls_fail_closed.sql` declared
`auth_find_oauth_app_by_client_id … RETURNS SETOF oauth_apps`, which needs the table's row **type**
at CREATE time. On a fresh database the **file** stage runs before the **CORE** stage that creates
`oauth_apps`, so boot 1 failed with *"type oauth_apps does not exist"* and the database stayed
**fail-OPEN until boot 2**.

**`/health`.** `runStartupMigrations()` now returns its summary and records it, and `/health` plus
`/health/ready` report `startupMigrations: { ran, applied, failed, lastRunAt, error? }` — **both
keeping their status codes**, so the gateway keeps serving.

**Not deployed anywhere.** Base `develop` `0d156d12cc0f`.

## Why the guard, not a reorder (the agent-decidable half)
Reordering CORE before files would contradict the documented reason CORE runs **second** — its
column-add ALTERs must keep landing on existing deploys (`startup-migrations.ts` header) — and would
have to be proved against **every existing database** as well as a fresh one. Guarding the dependency
fixes it at its cause, uses the idiom 039 **already uses for its own policy blocks**, and is **inert
where the table exists**: the branch is taken and the function is created exactly as before. The
header now records this decision.

**Measured, which is why only ONE of the seven functions is guarded.** 039's three `RETURNS SETOF`
tables are `users`, `oauth_apps`, `svc_api_keys`. `users` is created by `001_initial-schema.sql` and
`svc_api_keys` by `002_verification-tiers.sql` — both **file** migrations that run before 039, so both
exist. `oauth_apps` is created by **no file migration at all**. Cell **S0** pins that derivation, so
S1 cannot become vacuous.

**The owner/grant loop is guarded too.** It `ALTER … OWNER`s all seven functions **by name**, so
guarding only the create would have moved the failure four statements later instead of removing it.
`to_regprocedure(fn) IS NULL` returns NULL for a missing signature rather than raising.

## Why both endpoints stay 2xx (Wednesday's ruling, on my measurement)
| surface | probes | my change |
|---|---|---|
| **compose — the LIVE path (VM + local)** | **`/health/ready`** (`docker-compose.yml:534-538`) | body only; code untouched |
| Dockerfile `:93-94` | `/health` — **overridden by compose** | body only |
| `services.bicep:688-707` (deleted estate) | `/health` **Liveness + Readiness** | body only — a 503 here would be a restart loop |
| `deploy-all.sh:281` | HTTP code only | **cannot see the flag — out of scope, named below** |
| `deploy.sh:823` | body grep `"healthy"` | still sees `healthy` |

`/health` is liveness and the process **is** serving. `/health/ready` keeps KS 1101's code (503 only
when a dependency is `down`) because **48** `service_healthy` conditions gate dependents on it.

**SET by the latest run, never latched.** `runDbBootTasks()` is `initDb`'s onReady hook and runs again
on the KS 377 background retry, so a failure the retry fixes must stop being reported. `ran: false` is
the initial state and is deliberately **not** `failed: 0` — before the first run there is nothing to
report, and reporting a clean run the process has not had would be a false claim.

## Test Evidence

**Touched:** `migrations/039_rls_fail_closed.sql` · `services/api-gateway/src/startup-migrations.ts` ·
`services/api-gateway/src/services/health.ts` ·
`services/api-gateway/src/services/startupMigrationStatus.ts` (new) ·
`services/api-gateway/src/__tests__/ks1054-startup-migration-failure-on-health.test.ts` (new) ·
four existing test files' mock annotations (see below).

**RAN — red first, on this worktree at base `0d156d12`:**
| run | result |
|---|---|
| api-gateway **baseline** (my file excluded) | **86 files / 781 tests, 0 failed** |
| new cells at the **UNTOUCHED tip** (product reverted, restore sha256-verified) | **8 failed / 1 passed (9)** — H0–H5, S1, S2 red **by `AssertionError`**; **S0 green** |
| after the fix | **9 passed (9)** |
| api-gateway **full, after** | **87 files / 790 tests, 0 failed** (+1 file / +9 tests = exactly my cells) |
| `tsc` build program | rc 0, **0 errors** |
| `tsc` **including `src/__tests__`** | **29 errors — identical to the pristine tip's 29**, and **0** of them in a file I touched |
| `eslint src` — **run by hand** (no LINT leg in the harness) | rc 0, **0 errors** / 36 warnings; a planted `no-control-regex` **error** in my own new module → rc 1 with exactly **1 error**, restored by sha256, clean re-run 0 errors |

S1's red names the defect precisely: `expected [ 'oauth_apps' ] to deeply equal []`.

### Tamper arms — one per decision. The predictions were the brief's; these are measurements.
Anchors asserted unique, non-inertness proven by byte comparison, restores proven by sha256, and the
untampered run proven all-green first.

| arm | tamper | predicted | **measured** |
|---|---|---|---|
| A | 039's table guard removed | S1 red | **RED S1 only** (8 passed / 1 failed) |
| B | the owner/grant loop guard removed | S2 red | **RED S2 only** (8 / 1) |
| C | the recorder LATCHES instead of overwriting | H3 red | **RED H2, H3, H4, H5** (5 / 4) — wider than predicted, and correct: once a failure latches, every later clean read is wrong too |
| D | `/health` drops the field | H0 H1 H2 H3 H5 red, H4 green | **exactly that** (4 / 5) |
| E | `/health/ready` drops the field | H4 red only | **exactly that** (8 / 1) |

No arm reds S0. After all five: 9 passed, every file sha256-equal to pristine.

**NOT RUN, and this is the half that is mocked:**
- **039 IS NEVER EXECUTED.** There is no Postgres here, so the stage-order half is a **static
  derivation** over the migration files — it reads which tables 039 depends on and which file
  migrations create them. It does **not** run 039, does not create a database, and does not prove the
  guarded SQL parses in PostgreSQL. **The two-sided fresh-DB drill the ticket asks for is NOT done.**
  §5f live sweep owed, and it is the sweep that matters most here.
- The boot-1 **7-failure** count (QA gate, 2026-09-09) is **relayed, not re-run**.
- The four platform suites (Schemathesis · Akto · Playwright · Performance/k6): **not run**.
- Whether any other open PR touches these files: **not measured**.
- `/health/services` and the aggregate endpoints do **not** carry the field; only `/health` and
  `/health/ready`, as ruled.

**Migrations + config:** 039 is an **existing** migration, edited in place; **no new migration file**,
no env var, no config default. ⚠ **The `migrations` compose service BAKES `migrations/*.sql` into its
image** — rsyncing the `.sql` alone does nothing, so any deploy of this must rebuild `migrations` and
verify the schema directly. Re-applying 039 on a database that already has it is a no-op by design
(`_secuura_migrations(filename)` tracking), and the guard is inert there.

**⚠ PREFLIGHT INCOMPLETE — the ratio is in the push gate section of the READY mail**, not implied away.

## Out of scope, named rather than silently skipped
- **`deploy-all.sh:281` reads only the HTTP code**, so it cannot see a 200-with-flag. Wednesday ruled
  it **out of scope**: making a deploy fail on the flag changes deploy outcomes, which Kam did not
  rule. It is named in the handover as a follow-up.
- The **per-tenant** stage is deliberately **not** counted in the summary — that path is **KS 1055**.
- The **42703** case gate37 raised (m365's `last_attempted_at` query on an unmigrated database) is the
  motivating example for why a failed start-up migration must be visible. **m365 is unchanged.**

## The four widened annotations are a consequence, not scope
`runStartupMigrations` now resolves a value rather than `void` — which Kam's ruling requires ("the
migration run returns its failed count"). That made `{ runStartupMigrations: () => Promise<void> }` in
four existing test files **narrower than the module**, so a program including the tests read **TS2322**
on each. Widened to `Promise<unknown>`; those cells only await the call and never read its value.
**Measured both ways:** the including program was **29** errors at the pristine tip, **33** with my
change before this fix, and **29** again after — delta zero. Without the check it would have shipped
invisibly, because the **build** program excludes `src/__tests__` and reads rc 0 either way.

Refs KS-1054

