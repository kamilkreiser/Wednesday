#1332 KS-1054 round 2: create the CORE tables before 039 so a fresh DB is never fail-open
head f2423bf7aa6c64952cf425d4160a048a55ffaaee

## BLUF — ROUND 2 of 2

Round 1 was **NO GO** on gate38's `N-1332-1` BLOCKER. This round fixes **N-1332-1, N-1332-2 and N-1332-3 together**, and the blocker's regression is driven on a **real PostgreSQL 18.3**, under the **real unmodified `scripts/run-migrations.sh`**, three-sided.

`Refs KS-1054`. Kam's ruling, option (a), verbatim: *"The migration run returns its failed count. /health reports it, so the deploy scripts' existing /health checks (deploy-all.sh:281, deploy.sh:823) see it and the deploy reads as failed. The running service is not stopped."* The gateway does not exit and does not stop serving; `/health` and `/health/ready` both stay **200** and carry the field.

## N-1332-1 — the BLOCKER. Fix shape (b), chosen on a measurement.

On a bare database 039 skips `oauth_apps`, `svc_webhooks`, `certifications` and `charge_events` (`RAISE NOTICE 'KS 458: skipping % — table does not exist on this DB' (the key de-hyphenated from the SQL so it does not attach that ticket)`), because their only creator is the CORE stage, which runs **after** the file stage. 039 is then **recorded**, and `applyFileMigrations` never re-runs a recorded file (`:133-137`), so the OAuth lookup function, its policy and tenant isolation on those four tables never arrive on any later boot.

**Why (b) and not (a) or (c) — this is the deciding measurement, not a preference.** `scripts/run-migrations.sh` — the compose `migrations` service's own runner, **and the one a deploy actually uses** — is a single `for f in migrations/*.sql` pass with **no CORE stage at all** and the same record-then-skip shape (`:118-120` skip, `:127` `INSERT … ON CONFLICT (filename) DO NOTHING`). A second file-stage pass inside the gateway therefore fixes the gateway and leaves the container path still recording a half-applied 039. **(b) fixes both runners with one change**, because 039 then finds every table present on its only pass under either runner. It also leaves intact the header's own documented reason for CORE running second (`startup-migrations.ts:5-21`).

`migrations/038a_ks1054_core_tables_before_039.sql` sorts between `038_` and `039_` under **both** runners, which order lexically (`startup-migrations.ts:94-97` `.filter(.sql).sort()`; `run-migrations.sh:145` `for f in migrations/*.sql`).

**The DDL is derived from CORE, and the equality is proved, because (b) creates a SECOND creator of the same four tables and `CREATE TABLE IF NOT EXISTS` in whichever runs second silently keeps the other's schema.** Every statement is derived from `CORE_MIGRATIONS` at develop `215cc6875e2b`. Proof on a real PostgreSQL: `pg_dump --schema-only -t` of the four tables after **CORE's definitions alone** and after **038a alone**, on two bare databases, filtered of pg_dump 18's per-dump `\restrict` nonce — **byte-identical**. Controls: a one-character type mutation (`varying(64)`→`(63)`) differs from both, and two different tables' dumps are not equal.

### R-PG1 — the regression, on a real PostgreSQL, three-sided

PostgreSQL **18.3** (Homebrew `initdb-18`/`pg_ctl-18`), **unix socket only**: `listen_addresses = ''`, **0 inet sockets proven by `lsof`** on the postmaster pid (control: 1 unix socket), never the native `:5432`, never a container. Each row is a **bare database** and the runner is the real `scripts/run-migrations.sh`.

| tree | 039 recorded | `auth_find_oauth_app_by_client_id(text)` | `oauth_apps_auth_lookup` | `tenant_isolation` policies | the four tables |
|---|---|---|---|---|---|
| merge-base `0d156d12` | **0** — 039 itself FAILS | ABSENT | 0 | 22 | 0 |
| round-1 head `f5381338` | **1** — recorded, work skipped | **ABSENT** | 0 | 22 | 0 |
| **this commit** | **1** | **PRESENT** | **1** | **25** | **4** |

The middle row **is** the defect: 039 "succeeds" and is recorded while doing nothing for those four tables, so the lookup is absent for the life of the database. A second pass changes none of those five measures on this commit.

**Three migrations that fail forever on the other two trees now succeed**: `006_f18_webhook_secret_encryption.sql`, `008_drop_webhook_secret_legacy.sql` and `047_oauth_app_type_vocabulary.sql` — they operate on `svc_webhooks` and `oauth_apps`. That is a consequence of the fix, measured, not aimed at.

## N-1332-2 — CORE-THROW-READS-CLEAN
Both CORE-stage catches (`Main DB migrations failed`, `Platform DB migrations failed`) logged and **never touched `totalFailed`**, so a stage that died was served as `failed: 0`. Both now add to the count and record a reason.

## N-1332-3 — ERROR-FIELD-NEVER-SET
`error?` was declared on the status record and never passed. `applyFileMigrations` now returns a `firstError` the way `migrateDatabase` already did (`:853`, `:863`), and the single call site passes it. The field is bounded to 200 characters.

## Test Evidence

**Touched by ROUND 2's commit (`f2423bf7aa`):** 4 files, **+293/−9** — the new migration, `startup-migrations.ts`, the existing KS-1054 test file, and a new test file. **The PR as a whole now shows 11 files, +691/−13** across both rounds; round 1's set is unchanged by this commit.

**Ran** (worktree detached at `f5381338`, `npm ci` rc 0):
- **api-gateway suite: 88 files, 795 tests, 0 failed, rc 0** (round 1 measured 87/790; +1 file and +5 cells are this commit's).
- `tsc --noEmit` (build program): **rc 0, 0 errors**.
- **tests-including tsc program: 29 → 29, delta 0**, measured as a delta against the tip, never by file ownership. Control: that program contains **87** `__tests__` files; the build program contains **0**, so it really does see them.
- R-PG1 and the `pg_dump` equality above.

**Push gate, from this push's own raw log:** **842 `ok` / 0 `FAIL` / 0 `not ok`** · shell suites: 60 passed, 0 failed, 0 skipped (of 60) · `FIXTURE BUILD FAILED` **0** · **PREFLIGHT INCOMPLETE — 12 of 15 legs ran, 3 SKIPPED** (legs 3, 4, 8 — local stack not up). **12/15 is not a pass and is not quoted as one.** `eslint` run by hand.

**Arms — 3/3 red their own cell**, same-volume backups, `try/finally`, every tamper `cmp`-proved to differ, every restore verified by sha256:
- `totalFailed += 1` removed from the **main CORE catch** → C1 reds (4 → 3 passed / 1 failed);
- `error: totalError` removed from the record call → C2 reds;
- **038a deleted** → S3 reds (10 → 8 passed / 2 failed).

**Cells changed in the existing file, with the reason:**
- `filesBelow()` filtered `/^\d{3}_/` and was therefore **blind to a letter-suffixed migration**. `S0` asserted `createdByFileMigrationBelow('oauth_apps', 39) === false` and kept passing while that had stopped being true. The filter now matches the runners' own lex order. **This was found because the cell passed when it should have moved.**
- `S0` now asserts the new truth (`oauth_apps` **is** created below 039).
- **`S1` would have become vacuous**: with every table 039 needs now file-created, its loop `continue`s on all of them and its list is empty no matter what 039 says. It keeps the rule and gains a control — an invented table that no migration creates and 039 does not guard — so the rule can still fail.
- **`S3` is new** and is the round-2 invariant: every table 039 needs is created by a file migration below it, and `038a` is in `filesBelow(39)`. It is the cell that reds if anyone removes or renumbers the migration.

**NOT run / NOT covered, measured rather than assumed:**
- **`N-1332-5` is NOT in this commit.** `deploy-all.sh:281` and `deploy.sh:823` still do not read the `startupMigrations` field. Named UNRAISED for a successor, not dropped.
- **`N-1332-4`** (the run-to-record wiring is unpinned) is not commissioned and is not fixed here.
- The **gateway runner** and the **docker/init seeded path** were not driven for the `pg_dump` equality; the proof is CORE-alone vs 038a-alone on bare databases, which is the equality that matters (the two creators agree). The compose-runner database additionally carries the `oauth_apps_app_type_vocabulary` CHECK that `047` adds — a later migration doing its job, not a schema disagreement.
- The four platform suites (Schemathesis · Akto · Playwright · Performance/k6) were not run.
- **A candidate, named not filed:** numbering the new file below `006` instead of `038a` would let `006`/`008`/`047` succeed on boot 1 rather than boot 2. **Not taken** — 12 migrations reference these four tables, so an earlier number changes far more behaviour than the blocker needs, and each would need its own verification.
- **The KS 764 guard reds on this branch** (`CALL_SITES`, 1 failed / 14 passed). It is the pre-existing develop red that a separate PR fixes, **not this change**: measured identical with and without this commit's edits. This branch is based below that fix.
- Tenant databases are KS 1055's, not this PR's.
- **A deploy must rebuild BOTH the `migrations` image and the api-gateway image** — the migration `.sql` files are baked into the migrations image. **Nothing is deployed from here.**
- **RUNTIME change on gateway start-up and `/health`: the §5f live sweep is owed.**

🤖 Generated with [Claude Code](https://claude.com/claude-code)

