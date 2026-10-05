## BLUF

On a database that recorded `039_rls_fail_closed.sql` **before** `charge_events` existed, 039 is inert for ever and that table ends with row-level security **not enabled at all** — no RLS, no FORCE, no policy. Both migration runners skip any file already recorded in `_secuura_migrations` (`scripts/run-migrations.sh:118-122`; `services/api-gateway/src/startup-migrations.ts:137-141`), so no redeploy and no edit to 039 can repair it. Only a higher-numbered file can.

`049_ks1401_tenant_isolation_after_039.sql` adds `tenant_id` where absent, fills **only** rows where `tenant_id IS NULL` with the platform default tenant, ENABLEs and FORCEs RLS, and re-creates `tenant_isolation` with **039's exact text**, on `charge_events`, `certifications`, `oauth_apps` and `svc_webhooks`.

**Not applied to any database.** This PR ships the file and its proof. Migration 049 is applied **with the kintsugi deploy only and NEVER reaches demo** — Kam's card `secuura-tenant-isolation-migration-ks1401-1005`, ruled `a` on 2026-10-05: *"A Secuura seat writes and gates the migration; backfill rule: existing rows take the platform's default tenant; it lands with the kintsugi deploy card, never demo."*
**The mechanism, stated plainly, because "never demo" is a ruling and not a technical guard.** Once 049 is on `develop`, **any** box that boots the gateway image built from that `develop` applies 049 at startup — stage 1 of `startup-migrations.ts`, which is what gate61 measured in its own Boot 2. **Demo is not excluded by anything in this code.** What keeps 049 off demo is the deploy discipline: demo deploys hold at a `develop` SHA that predates 049, and the kintsugi apply is its own carded round. If someone deploys demo from a `develop` at or after this merge, 049 **will** run there. That risk is a process risk, and it is the reason the card exists.

## The defect, per table

| table | kintsugi, measured 2026-09-30 | fresh `run-migrations.sh` shape, measured 2026-10-05 | 049 leaves |
|---|---|---|---|
| `charge_events` | 8 rows, rls **false**, force **false**, **0 policies** | fine (038a creates it before 039 runs) | rls/force true, `tenant_isolation` |
| `certifications` | 0 rows, 17 cols, forced, **0 policies** | 16 cols, **no `tenant_id`, NO RLS AT ALL** | `tenant_id`, rls/force true, policy |
| `oauth_apps` | forced, 2 policies | forced, 2 policies | unchanged in effect |
| `svc_webhooks` | forced, 1 policy | forced, 1 policy | unchanged in effect |

**Source of the kintsugi column:** `5_Project_History/HANDOVER-seatB50-kintsugi-deploy.md:104-115`, measured by Seat B 50th on **2026-09-30** before and after that round's deploy, identical both times. **Not re-measured since, and not re-measured by this PR.**

**KS 1376 is two different defects by runner.** On the gateway path, CORE_MIGRATIONS creates `certifications` and its KS 4 phase-5 block (`startup-migrations.ts:751-834`) adds `tenant_id`, ENABLEs and FORCEs RLS and creates **no policy** (`:822-830`) — forced with 0 policies, i.e. default-deny, which is the state the ticket's title describes. On the `run-migrations.sh` / ks949 path there is no CORE stage, `038a` creates the table without `tenant_id`, 039 skips it, and it ends with **no RLS at all** — fail-**open**. **The second one is measured in this PR; the first is source-read only** (driving the real `runStartupMigrations()` needs a built `packages/shared`, which this PR does not do). 049 closes both.

## Test Evidence

**Touched:** `Blockchain/Dev/migrations/049_ks1401_tenant_isolation_after_039.sql` (new), `Blockchain/Dev/scripts/__tests__/ks1401_049_tenant_isolation_after_039.test.sh` (new, 100755), both platform-k documents (block `22.`).

**Ran — the new suite, on a real PostgreSQL:** `62 passed, 0 failed, 12 cells`. Measured **19 s / 18 s / 19 s** over three consecutive runs, 2026-10-05, host `Kamils-Mac-Studio`, **PostgreSQL 15.14 (Homebrew) aarch64-apple-darwin24.4.0**, socket-only cluster in the suite's own mkdtemps. It also ran **inside this push's own pre-push preflight at leg 14** and reported `53 passed, 0 failed` there.

**Ran — cell 12, gate61 finding N-1383-1 (the twelfth cell, and the reason the totals above moved):** 049 run as a **non-bypass owner** — a `NOLOGIN` role with `rolsuper=false` and `rolbypassrls=false` owning all four listed tables — over two `tenant_id IS NULL` rows planted by a superuser, with no tenant GUC. Before the fix the file reported `had 0 NULL rows; no data was written` while a superuser `SELECT` still counted **2**; after it, the NOTICE reports **2** and **0** remain. The superuser control filled both rows on either file, so the discriminator is the role and not the file. The fix is one statement — `set_config('app.tenant_scope_bypass','platform_admin',true)` as the first statement in the `DO` block — and it is the carve-out 039's own policy already grants. The arm is falsifiable from inside the suite: `KS1401_F049_UNDER_TEST=<a pre-fix 049>` reds **exactly two** assertions (62 → 60 passed / 2 failed) while every control holds.
⚠️ **Two measurement traps this cell now guards, both found by getting them wrong first.** A `RAISE NOTICE` is **not transactional**: it reports work that a later failure rolls back, so the cell asserts the run committed (rc 0, zero `ERROR` lines) before it trusts any row count. And a fixture whose role owns only `charge_events` is **confounded** — 049 raises on `certifications` and the whole `DO` block rolls back, so the pre-fix and post-fix files both leave two NULL rows and only the NOTICE differs.

**Ran — ks949 at this head:** green, and its shape reports **50 main-DB migrations** against 49 at the base — base + 1, i.e. 049 joined the deployed shape and ks949 still passes with it.

**Ran — the reds, before 049, as `secuura_app` (NOLOGIN, `rolbypassrls=false`, `rolsuper=false`, asserted):**
- GUC = tenant A → `charge_events` returns **8** rows, of which **3 are tenant B's** (cross-tenant leak)
- no GUC → returns **8** (fail-open)
- GUC = tenant A → **0** of tenant A's own `certifications`, while the superuser control sees **1** (default-deny, and the control is what makes that 0 falsifiable)

**Ran — the same arms after 049:** B's rows **0** to A; no GUC → **0**; A reads its own certification → **1**; `platform_admin` bypass still sees all **8** (the carve-out `gdprService.ts` relies on); a cross-tenant INSERT is refused by `WITH CHECK`. Tenant A sees **5** rows, not 4 — correct: the backfill gives the one NULL-tenant row to the platform default tenant, which is tenant A in the fixture; 5 + 3 hidden = 8.

**Ran — policy fidelity, measured not asserted:** 049's `tenant_isolation` `qual` **and** `with_check` are byte-equal (md5 `3356c6ad2226…`) to the policy **039 itself created on `users` in the same database** — compared against 039's own output rather than a string copied into the new file. `oauth_apps_auth_lookup` survives untouched.

**Ran — data safety:** row count 8 → 8; every row that already carried a `tenant_id` is byte-identical by per-row md5; the ex-NULL row carries exactly the default tenant; 0 NULL-tenant rows remain.

**Ran — idempotence:** second and third applies leave schema **and** data byte-equal, and all four tables report "0 NULL rows" on re-apply, so no data is written. ⚠️ `pg_dump --schema-only` is **not** byte-deterministic: it emits a random `\restrict`/`\unrestrict` nonce per invocation, proven by hashing two dumps of the same unchanged database (`65bbd190…` vs `47eb22bb…`). The suite filters those two lines and carries a self-stability control plus a must-fail control that still catches a real `ADD COLUMN`.

**Ran — atomicity:** a sabotaged copy that raises after the last table leaves the schema dump byte-equal to before, under `psql -v ON_ERROR_STOP=1 -f` exactly as `run-migrations.sh:126` runs it (no `--single-transaction`). One `DO` block is one transaction. The clean file then changes the dump, so the equality is not trivial.

**Ran — three tampers on 049, each reddening the right arms, each restore byte-equal to sha256 `6ad3a01ac2780218` — **measured at the round-1 head `7eccb131`, whose 049 is that hash; the N-1383-1 commit changed the file, so at this head 049 is sha256 `c5dc307fbbdeca0d` and those three tampers have not been re-run against it** (unmeasured):** drop `FORCE` → the four-table reading reds; weaken the policy → all four fidelity arms red (and informatively `qual` diverges while `with_check` stays equal); drop the NULL-only backfill guard → four arms red including "a pre-existing row changed", with both fingerprints printed.

**NOT run:** 049 has been applied to **no real database** — no kintsugi, no demo, no slot, no compose stack. The gateway-runner shape's end state is source-read, not measured. No `az`, no SSH, no Docker. The four platform suites (Schemathesis / Akto / Playwright / k6) were not run: this change adds a migration and a shell suite and touches no HTTP surface, no OpenAPI spec and no service code.

## Decisions taken, and why

- **One `DO` block.** `run-migrations.sh:126` runs `psql` without `--single-transaction`, so each top-level statement autocommits and a mid-file failure would leave earlier statements committed. One statement is the only way to get one transaction under both runners. There is no top-level `ALTER` or `CREATE` in the file.
- **`lock_timeout` 5 s** inside the block. `ENABLE`/`FORCE`/`CREATE POLICY` take ACCESS EXCLUSIVE, and on a live box originate may be mid-transaction on `charge_events`; a contended table should fail the file (unrecorded, retried next boot) rather than queue every reader behind it at gateway boot. No precedent in 040-048 — this is the first of them to touch a table a second service writes at runtime.
- **Backfill is NULL-only, to the platform default tenant**, per Kam's card. The repo's own precedent for these tables is different — 013 fills `charge_events` via `initiated_by` first, 012/CORE fill `certifications` via `issuer_user_id` then `holder_user_id` — and that precedent would give better isolation for a row whose initiator is known. It is **named here and deliberately not used**, because it is not what the card says. On kintsugi the NULL count is **unmeasured**, so the two rules may be identical there.
- **No `SET NOT NULL`.** Today a `charge_events` insert carrying a NULL tenant under the `platform_admin` bypass succeeds; NOT NULL would make it raise 23502 — a new failure mode on a billing write this defect does not require. Fail-closed RLS already hides a NULL-tenant row from every tenant.
- **An absent table RAISEs.** 039's NOTICE-and-skip was then *recorded*, and that recorded skip is the root cause of KS-1401 and KS 1054. Raising leaves 049 unrecorded so the next boot retries, and makes the gateway report `failed: 1`.
- **`038a`'s header is named, not edited.** `038a_ks1054_core_tables_before_039.sql:16-17` makes **two** false claims: that it fixes this very condition (it causes it), and that its schema equality is proved across the `docker/init` path (true for `certifications` only; it fails for `oauth_apps` and `svc_webhooks` on a pre-existing DDL difference — extra indexes and `svc_webhooks_app_id_fkey`). Both are named in 049's header. 038a is recorded on every live database, so editing it is inert there while forcing a re-run everywhere fresh.

## Not covered / owed

- **KS-1401 stays open after this merge: the live apply on kintsugi and the §5f live sweep are still owed.** KS 1376 stays open on the same grounds. Per the test-discipline skill §5f, a runtime-behaviour change is not Done on offline green.
- **Per-tenant databases get CORE only, never file migrations**, so 049 cannot reach them and they still get `certifications` forced with no policy. Named, not fixed; teaching CORE the policy is a candidate and out of this scope.
- **`packages/shared/src/jobs/expiry-checker.ts:139`** reads `certifications` with no tenant scope and returns 0 rows for a non-bypass role both before and after 049. Named, not fixed.
- **Unmeasured on kintsugi:** the 8 rows' NULL count, **whether `charge_events.tenant_id` is nullable there at all**, the connecting role and its BYPASSRLS/owner status, and `MULTI_TENANCY_ENABLED`. The nullability matters because 049 backfills NULLs and then relies on the column being populated; nobody has read the column definition on that database. **All of this is unmeasured, not assumed benign** — and because N-1383-1 showed the migration's own NOTICE can assert a falsehood, the apply round must count NULL-tenant rows with a **superuser** `SELECT` before and after the boot rather than read the log. The suite's NULL-tenant row is the **fixture's**, not a measurement of kintsugi.
- **This suite now runs on every seat's push** via `run-shell-suites.sh` at preflight leg 14, at the measured 18-19 s above.

Refs KS-1401

https://linear.app/secuura/issue/KS-1401/charge-events-has-rls-off-entirely-on-the-kintsugi-database-already
