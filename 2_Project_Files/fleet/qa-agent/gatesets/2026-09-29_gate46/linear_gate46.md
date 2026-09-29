# gate46 LINEAR READ — KS-1054, every comment VERBATIM

Read 2026-09-29T12:35:08Z by linear_read_gate46.py (GraphQL `issue` query only; no mutation). Comments oldest first. BODY_SHA256 = sha256 of the body as served.

## KS-1054 — Fresh databases are FAIL-OPEN until the second boot — 039_rls_fail_closed does not apply on boot 1 (file stage runs before the CORE stage it depends on)
- state: In Progress
- url: https://linear.app/secuura/issue/KS-1054/fresh-databases-are-fail-open-until-the-second-boot-039-rls-fail
- comments: 6

### KS-1054 comment 1c794768-e4e5-49ce-b93f-7252b4c22cc1
- createdAt: 2026-09-09T13:42:10.644Z | updatedAt: 2026-09-09T13:42:10.634Z
- author: kamil.kreiser@secuura.ai
- BODY_SHA256: 64d8a70d15619e9829b1723d1a26a79266673b1c6826b5cb0307d8b0724c0dbd

```
**F-928-3 — the section of this ticket marked UNMEASURED is now measured. Split out to KS-1055.**

**BLUF: confirmed, and it is a different defect from this one.** KS-1054 is a *window* — a fresh DB is fail-open until boot 2, then heals. What I measured on a genuinely separate tenant DB does not heal on any boot: the file-migration stage never runs against a tenant database at all, so `_secuura_migrations` **does not exist** there after three boots (control: 48 rows on the main DB, same reader).

**And the consequence is the opposite sign from this ticket's.** CORE_MIGRATIONS `ENABLE`s and `FORCE`s RLS on five tables (`startup-migrations.ts:439-440, 485-486, 551-552, 633-634`) while `CREATE POLICY` appears **0 times** in that whole file (control: 19 in `migrations/*.sql`). A tenant DB therefore lands with FORCE RLS and **zero policies** — not fail-open, **deny-all**. Measured as a `NOBYPASSRLS` non-superuser role: 0 rows from `documents`/`certifications`/`audit_logs`, and still 0 with both GUCs set, while the same role reads 1 from a non-RLS table in the same database (non-zero control) and the row is provably there under `row_security=off`.

**Scope, both directions:** latent today — `PROVISION_PER_TENANT_DB` defaults false, so every tenant points at the shared app DB, which does get the files. It goes live the moment per-tenant DBs are provisioned, i.e. exactly when KS-160 Path A ships.

**Ordering matters to whoever fixes either one:** on my fresh main DB, boot 1 failed 7 file migrations including **`039_rls_fail_closed.sql` → `type "oauth_apps" does not exist`**, and boot 2 applied them — this ticket's window, reproduced. A tenant arm added to `applyFileMigrations` without fixing that ordering just reproduces KS-1054 inside every tenant DB instead of fixing anything.

Measured by s163, 2026-09-09, on disposable local containers (removed at close). Demo, UAT and every shared database untouched.
```

### KS-1054 comment f771cdf1-9b30-4a5a-9209-f129c15c7073
- createdAt: 2026-09-28T18:52:39.688Z | updatedAt: 2026-09-28T18:52:39.672Z
- author: kamil.kreiser@secuura.ai
- BODY_SHA256: 3751ca5e58a78df1e8db922d104a603a0d64e4bdf949ce8e267fcbc46ca3dfde

```
**Round 2 of 2 pushed to #1332 — head `f2423bf7aa6c64952cf425d4160a048a55ffaaee`** (fast-forward from `f5381338359d`, base `develop`).

Round 1 was NO GO on the gate's `N-1332-1` blocker. This commit fixes N-1332-1, N-1332-2 and N-1332-3 together.

**N-1332-1 — fix shape (b), chosen on a measurement.** A new file migration `038a_ks1054_core_tables_before_039.sql` creates `oauth_apps`, `svc_webhooks`, `certifications` and `charge_events` before 039 runs, so 039 finds them present on its only pass. The deciding fact: `scripts/run-migrations.sh` — the compose `migrations` service's runner, and the one a deploy uses — is a single pass with no CORE stage and the same record-then-skip shape, so the alternatives would have fixed the gateway and left the container path still recording a half-applied 039.

**Regression on a real PostgreSQL 18.3** (unix socket only, 0 inet sockets proven by `lsof`), under the real unmodified runner, on bare databases, three-sided:

| tree | 039 recorded | `auth_find_oauth_app_by_client_id(text)` | policy | `tenant_isolation` policies | four tables |
|---|---|---|---|---|---|
| merge-base `0d156d12` | 0 (039 fails) | ABSENT | 0 | 22 | 0 |
| round-1 head `f5381338` | 1 | **ABSENT** | 0 | 22 | 0 |
| this commit | 1 | **PRESENT** | 1 | 25 | 4 |

The DDL is derived from `CORE_MIGRATIONS` at develop `215cc6875e2b` and proved schema-identical to it by `pg_dump --schema-only`, because shape (b) creates a second creator of the same tables.

**N-1332-2** — both CORE-stage catches never touched `totalFailed`, so a stage that died was served as `failed: 0`. **N-1332-3** — `error?` was declared and never passed; `applyFileMigrations` now returns a `firstError` the way `migrateDatabase` already did.

api-gateway **88 files / 795 tests, 0 failed**. Tests-including tsc **29 → 29, delta 0**. Arms **3/3** red their own cell. Push preflight **12 of 15 legs, 3 skipped** — not a pass, stated as a ratio.

**Not in this commit:** `N-1332-5` (the deploy scripts still do not read the `startupMigrations` field) — named unraised, not dropped. `N-1332-4` is not commissioned. A deploy must rebuild **both** the migrations image and the api-gateway image; nothing has been deployed.
```

### KS-1054 comment 3b6db077-b43c-420c-8b81-48ca7c341b68
- createdAt: 2026-09-28T21:20:36.817Z | updatedAt: 2026-09-28T21:20:36.805Z
- author: kamil.kreiser@secuura.ai
- BODY_SHA256: 71aca3ade25f3293bff722f1365c383a0fcf1697d8be6bd83f95d75dabb58f2f

```
Merged 0de108577e6199de3c9402c0643a2944d86aee97 (PR #1332, migrations/038a_ks1054_core_tables_before_039.sql); offline gates green; NOT Done per secuura-test-discipline §5f — live sweep owed (torn-down rebuilt stack, all containers verified up), unverified: 039 and 038a on a bare Azure database across two boots, certifications as the app role (secuura_app; default-deny N-G39-1), and the migrations image rebuild
```

### KS-1054 comment 4103f740-7333-4935-a30b-b7f202e2cad5
- createdAt: 2026-09-29T08:30:18.275Z | updatedAt: 2026-09-29T08:30:18.264Z
- author: kamil.kreiser@secuura.ai
- BODY_SHA256: 269bc5f87bbe6edc5f64ce2df21388611f23a6870d86be9d0b648cdd96af1c29

```
PR #1346 raised against `develop`, head `2075c3ec7078`, base `0aa9b52c691b`.

One predicate both deploy scripts call: `Blockchain/Dev/deployment/azure/check-startup-migrations.sh`, invoked from `deploy-all.sh` and `deploy.sh`. It reads `startupMigrations.failed` from `/health` and fails the deploy step on a non-zero count, keyed on `failed` and never on `error`. `/health` itself is unchanged — the diff carries no service code. An absent field passes and says so, so a rollback to an older image is not blocked; a non-JSON or empty body is skipped and named rather than counted as a pass; a non-integer value is refused rather than read as zero.

Evidence: the shell suite reads 11 passed / 0 failed on the branch and 0 passed / 11 failed with the test half alone (both deploy scripts reverted to `0aa9b52c691b` and the new helper removed), restored byte-identically afterwards. The helper's recorded mode is `100755`, asserted by `git ls-tree` rather than by the on-disk bit, because this repo sets `core.filemode=false` and both scripts invoke the helper directly. The branch was rebased twice and its diff is byte-identical to the diff stored before the first rebase (`cmp` rc 0, 12,296 B). Push preflight: 12/15 legs ran, 3 skipped (legs 3, 4, 8 — local stack not up), nothing failed. That is not a pass and is recorded as a ratio.

Not covered: the deploy scripts were not run against any real environment, and no migration was run against a real database. A live sweep is owed on this runtime change, so this ticket stays In Progress.
```

### KS-1054 comment 5a3d36fc-5d9c-4cbc-96e1-d8656f5964a6
- createdAt: 2026-09-29T10:32:38.090Z | updatedAt: 2026-09-29T10:32:38.078Z
- author: kamil.kreiser@secuura.ai
- BODY_SHA256: eea967599ebd1e8c50347d5d36ce305dc3cfbf79770cd7168082fde93f62a7c5

```
Merged to `develop` as PR #1346, squash `8ba2da02d980e7e8065e8ce614b034adc2b7c2eb`, tree `fd0d6bc033a9`, parent `bd740147c3d8`. Verified at source: develop equals the squash by ls-remote, the commits API reports that tree, and a contents-API blob read on all four changed paths equals the head's blob. The helper's recorded mode is `100755` in the merged tree by `git ls-tree`, with a `100644` control from the same commit.

**The squash subject was composed rather than taken from the PR title, and the reason matters.** The PR title said the deploy scripts "fail on failures". QA measured that `deploy.sh` prints an ERROR and `found 1 issue(s)` but **returns exit code 0** over failed migrations, so the deploy does not read as failed from that script — only `deploy-all.sh` fails. The landed subject says exactly that: "deploy scripts read /health startupMigrations; deploy-all fails on them". A squash subject is permanent, so it had to be true.

**What is therefore still open on this ticket:** making `deploy.sh` exit non-zero on failed migrations, which is what the ruling's "the deploy reads as failed" requires of the `deploy.sh:823` check. That is a follow-up PR, not covered here.

Also recorded by QA, none blocking: a `ran:false` body still prints a pass line in the summary; an absent, empty or non-JSON body likewise counts as a passing check; and `python3` missing from PATH reads a failed body as "not JSON — SKIPPED", a new dependency that fails open.

This changes runtime code in the deploy path and the scripts were run against no real environment, so a live sweep is owed and this ticket stays In Progress. Nothing was deployed by the merge.
```

### KS-1054 comment b82bebb3-2c62-435e-b39c-24dc7a246ca4 — THE #1348 RAISE COMMENT (gate45 checked it line by line)
- createdAt: 2026-09-29T10:46:19.057Z | updatedAt: 2026-09-29T10:46:18.988Z
- author: kamil.kreiser@secuura.ai
- BODY_SHA256: 61f665e17d13819cbe6543677b9946c2e891fd0e21ee1e6582bbc44ff7aa138c

```
PR #1348 raised against `develop`, head `1bb58b4ebb97`, base `8ba2da02d980`.

This is the half PR #1346 did not carry. `verify_deployment()` in `deploy.sh` counted its errors and then returned 0, because its last command was a log line — so the deploy read as successful over failed startup migrations. It now returns 1 when the error count is non-zero, which is the strength `deploy-all.sh` already had. One `return` is the whole change: the script runs under `set -euo pipefail` and the function is called unchecked at both call sites, so a non-zero return aborts with that status at either, and no call site needed editing.

Evidence: the shell suite reads 14 passed / 0 failed on the branch, and 13 passed / 1 failed with `deploy.sh` alone reverted to `8ba2da02d980` — the single red being the new cell, with its two companion cells still green, so the red is neither a fixture failure nor an unconditional one. The cell extracts the real summary block from `deploy.sh` by its own marker and executes it with an injected error count, rather than grepping for the fix: a grep passes on a commented-out line, and a line-number pin drifts.

Still open on this ticket, not fixed here: a `ran:false` body still prints a pass line although the gateway's own module says that is not a clean run; an absent, empty or non-JSON body still counts as a passing check in the smoke summary; and `python3` missing from PATH reads a failed body as "not JSON — SKIPPED", failing open. Each of those is about the pass LINE rather than the exit status, and passing on an absent field is deliberate, because failing closed there would block a rollback to an older image.

`deploy.sh` was not run against any real environment. A live sweep is owed and this ticket stays In Progress.
```

