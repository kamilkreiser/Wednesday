# gate45 LINEAR READ — KS-1054 and KS-1374, every comment VERBATIM

Read 2026-09-29T11:05:23Z by linear_read_gate45.py (GraphQL `issue` query only; no mutation). Comments oldest first. BODY_SHA256 = sha256 of the body as served.

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

### KS-1054 comment b82bebb3-2c62-435e-b39c-24dc7a246ca4
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

## KS-1374 — Akto scans are now paced to fit the platform's rate limit — test times went up; which way should we go?
- state: In Progress
- url: https://linear.app/secuura/issue/KS-1374/akto-scans-are-now-paced-to-fit-the-platforms-rate-limit-test-times
- comments: 4

### KS-1374 comment 802df8b2-42dc-42ab-a50c-0edb4f44e4a6
- createdAt: 2026-09-29T01:42:02.350Z | updatedAt: 2026-09-29T01:42:02.338Z
- author: kamil.kreiser@secuura.ai
- BODY_SHA256: 0051fe3c227a91b60a7166ec9b852cacb2f5ee67af3a3c8101d22997c785a3b7

```
## BLUF
Thanks Peter, this is a clear write-up. **Our recommendation is option 2 plus one guard:** raise `RATE_LIMIT_MAX_REQUESTS` on **local stacks only** (to the code's own non-prod default of 10,000, which you cite at `api-gateway/src/index.ts:472-485`), leave demo and production exactly as deployed, and **add one dedicated limiter test that runs at the demo's limit** so a limiter regression still shows up locally. Coverage is unchanged; only local pacing and one config value move.

## Recommendation, answering your three questions
1. **Which option:** 2, plus the limiter test above. The harness already derives its pace from this value, so it speeds up on its own.
2. **Should local stacks match demo exactly?** A looser local limit is acceptable **for scanning**, provided one test pins the demo behaviour: at the demo figure (2,000/min), requests beyond it are refused with 429, and the read-only skip paths still skip. That keeps the realism you were worried about losing in option 2, without paying for it in every scan.
3. **Is ~20 min / ~1 h acceptable as a local gate?** No. That is slow enough that people start skipping the gate, which costs more coverage than it protects. A config change is worth it.

## Why not the others
- **3 (`DISABLE_RATE_LIMIT=true` during scans):** removes the limiter from the picture entirely and is easy to leave on by accident.
- **5 (a scanner identity with a higher budget):** a new bypass surface that has to stay airtight to non-prod; not worth it when a config value does the job.
- **4 (key the limiter per principal):** probably the right long-term design, and it overlaps KS-618 (every caller shares one address). It is a separate piece of work with security implications, so we suggest a ticket for it, not this change.
- **6:** marginal gains; the limiter still sets the floor.

## Detail
No platform code is proposed to change; demo and production limits are untouched. If you agree, either side can make the change, as you offered: the local `.env` value, and the one limiter test.
```

### KS-1374 comment 4c4b7ea6-7de8-4c3b-8656-767163422d48 — a CORRECTION
- createdAt: 2026-09-29T09:12:03.279Z | updatedAt: 2026-09-29T09:14:01.187Z
- author: kamil.kreiser@secuura.ai
- BODY_SHA256: dd920bb5efbe11ad34865e41d2ac26de7d5dec1bbed47d18d9747b4b43c646e7

```
Correction to our comment of 29 Sep (01:42 UTC). We wrote: "The harness already derives its pace from this value, so it speeds up on its own." That was wrong for the Akto harness. On develop it does not read RATE_LIMIT_MAX_REQUESTS: systemTest/akto/src/setup/aktoRateLimit.ts:60 hard-codes PLATFORM_REQUESTS_PER_MINUTE = 2000, and derivedRateLimit() paces the pre-merge and security tiers at 0.75 of it (1,500/min) whatever the stack allows. Raising the local limit on its own would not speed the Akto scans up. (Schemathesis does read the value: systemTest/schemathesis/scripts/runner/config.py:234.)

PR #1347 (head 2c4b98253b1f) makes the change:
- the local env templates (Blockchain/Dev/env.example and .env.example) set RATE_LIMIT_MAX_REQUESTS=10000. An existing .env is not rewritten, so each local .env needs the same one-line edit;
- docker-compose.yml keeps its 2000 fallback, so the demo, which runs that compose file with its own .env, is unchanged;
- the Akto harness now takes the platform limit from RATE_LIMIT_MAX_REQUESTS, and uses 2000 when it is unset;
- one api-gateway test pins the global limiter at 2000 requests per 60 s: request 2001 is refused with 429, and the read-only paths still skip the limiter.
Demo and production limits are unchanged.
```

### KS-1374 comment f878a031-be95-4bd3-a864-c5c17f44bd6e
- createdAt: 2026-09-29T09:14:01.138Z | updatedAt: 2026-09-29T09:14:00.949Z
- author: peter@obeden.com
- BODY_SHA256: c5a11c89f68b0c048eddabcf54ac55f69630ee9c2560c133579b44852981f0be

```
Hi @kamil.kreiser

I added this yesterday as a temporary fix, as I did not want to update the codebase

* systemTest/akto/src/setup/aktoRateLimit.ts:60
```

### KS-1374 comment dc9212b5-aaec-42fc-9733-ba57737d5ae0 — THE SECOND CORRECTION (gate45 checks every factual line)
- createdAt: 2026-09-29T10:59:09.166Z | updatedAt: 2026-09-29T10:59:09.153Z
- author: kamil.kreiser@secuura.ai
- BODY_SHA256: a15971d19ae512f7eace8f5c325270f48952c4e907f00cfdc75ef845b158bafe

```
Second correction, to our comment above. Two things in it were wrong, and a review of the change found them.

First: we wrote "Demo and production limits are unchanged". That held for deployments already running, but not for a host seeded afterwards. Blockchain/Dev/docker-compose.production.yml:16 tells an operator to copy .env.example to .env, and that file's own default is RATE_LIMIT_MAX_REQUESTS:-100. The first round raised .env.example to 10000, so a production-compose host seeded from it after that change would have run at 10000. No running environment was affected, and nothing was deployed, but the statement was wrong about the seeding path.

Second: we said the Akto harness now takes the platform limit from RATE_LIMIT_MAX_REQUESTS. It did, for every scan — including a scan pointed at the demo or an Azure stack. The harness's configuration loader reads the local Blockchain/Dev/.env whatever stack is being scanned, so a local value of 10000 would have paced a demo scan (limit 2000) at 7500. That is faster than the 1500 it replaced, and it would have restored the rate-limit refusals the pacing exists to prevent.

Both are fixed at head 18bc5123ce90 of the same PR (#1347):
- Blockchain/Dev/.env.example is back to 2000, with the reason recorded in the file. Only Blockchain/Dev/env.example is raised to 10000; scripts/bootstrap-env.sh reads that one as canonical. So env.example seeds local stacks, .env.example seeds production-compose, and the two no longer move together.
- The harness reads RATE_LIMIT_MAX_REQUESTS only when the scan target is local (an unset target URL is local by construction, because the default is always a localhost port). Any other target paces at the 2000 default. AKTO_PLATFORM_REQUESTS_PER_MINUTE is an explicit override for a remote stack whose real limit an operator knows; its name is deliberately not defined by either env template, so it cannot be picked up from a local .env the way the previous value was.
- A platform limit of 1 previously derived 0, which this harness treats as unthrottled. The derived rate is now floored at 1.

Two things to be plain about. The .github/workflows/internal-audit.yml CI stack copies env.example, so CI now runs at 10000. And a remote stack reached through a localhost port-forward or tunnel still reads as local; the explicit override is the answer there, and the change does not try to detect that case.

The demo's own limit was not read at any point — its .env is not in the repository.
```

