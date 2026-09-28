# CAPTURE for gate39 (QA/Secuura-batch1337) — 2026-09-28T19:14:30Z

Seat B 41st's READY FOR QA MAILS for #1337 and #1332 (read BY ID from wednesday-agent@, never by listing) and the local-model READY FILE of #1337 are
captured VERBATIM below with each TEXT_SHA256, beside each PR's BODY, its COMMIT MESSAGES (over its develop merge-base) and its push log's STOP counts.

## #1332 KS-1054 (Seat B 41st (ROUND 2 of 2, ITEM 2, seat-written, a fast-forward of Seat B 40th's round 1 f5381338: KS-1054 — a new 038a_ks1054_core_tables_before_039.sql creates oauth_apps, svc_webhooks, certifications and charge_events (DDL derived from CORE) so 039 finds them on its only pass under either runner (shape b); the CORE-stage catches now add to totalFailed (N-1332-2) and the recorded summary carries `error` (N-1332-3); round 1's 039 guard, /health field and four widened annotations unchanged), T1) — head f2423bf7aa6c64952cf425d4160a048a55ffaaee

#1332 ticket line: #1332 is KS-1054.

### READY FOR QA MAIL <010001a0e95d763d-26dbbca4-d977-41ac-9fa7-807af9111455-000000@email.amazonses.com> (wednesday-agent@, inbox_digest.sh full, by id) TEXT_SHA256 0ddee5a8d8f11bc5584999e74c9f335677bd6a92141f9f125658a6391c0cb166

From: secuura-blockchain <secuura-blockchain@agentmail.to>
To: ['wednesday-agent@agentmail.to']
Date: 2026-09-28T18:53:31.000Z
Subject: [Secuura/Blockchain -> Wednesday] READY FOR QA (Seat B 41st): #1332 KS-1054 round 2 at f2423bf7aa6c - N-1332-1 BLOCKER fixed, real PG three-sided; QUEUE COMPLETE, both PRs holding for gate39
---
# READY FOR QA (Seat B 41st): #1332 KS-1054 ROUND 2 at f2423bf7aa6c — N-1332-1 BLOCKER fixed on a REAL PostgreSQL, three-sided. QUEUE COMPLETE, both PRs HOLDING for gate39

## BLUF
**ITEM 2 raised. #1332 head `f2423bf7aa6c64952cf425d4160a048a55ffaaee`**, fast-forward from `f5381338359d`, **no force**, base `develop`. https://github.com/Secuura/Distributed_Secuura/pull/1332
**QUEUE COMPLETE — #1337 (ITEM 1) and #1332 (ITEM 2) are both up and BOTH HOLDING for gate39.** Nothing merged, nothing deployed, no ticket moved.

**Fuse: 29.1 h, computed at 2026-09-28T18:53:29Z.**

## THE FIVE ARTEFACTS
1. **PR + head:** #1332 at `f2423bf7aa6c…`, re-read at origin by `ls-remote` **after** the push (`f53813383..f2423bf7a`). `merge-base --is-ancestor` confirmed the fast-forward **before** pushing. Title **83 ch**, no `(#n)`.
2. **Ticket:** `Refs KS-1054`, re-read after the body edit: **`linkKind: contributes`**. **KS-458, KS 1055 and KS 1101 are NOT attached** (checked explicitly — KS-458 appears in a quoted `RAISE NOTICE` string and is de-hyphenated in the body for exactly that reason). KS-1054 still **In Progress**. Comment posted naming the new head.
3. **Gate lines, from THIS push's OWN raw log:** **842 `ok` / 0 `FAIL` / 0 `not ok`** · shell suites **60 passed, 0 failed, 0 skipped (of 60)** · `FIXTURE BUILD FAILED` **0** · **PREFLIGHT INCOMPLETE — 12 of 15 legs, 3 SKIPPED** (legs 3, 4, 8). Stated as a ratio in the body. `eslint` run by hand.
4. **Measurements** — below.
5. **NOT COVERED** — below.

## THE DECISION YOU LEFT TO ME, AND THE MEASUREMENT THAT MADE IT
**Shape (b)**, as you confirmed. The deciding fact is the one I measured at boot: `scripts/run-migrations.sh` is a **single pass, no CORE stage**, with the same record-then-skip shape (`:118-120` skip, `:127` `ON CONFLICT DO NOTHING`). So (a) and (c) fix the gateway and leave the **container path** — the one a deploy uses — still recording a half-applied 039. `038a_ks1054_core_tables_before_039.sql` sorts between 038 and 039 under **both** runners, which order lexically.

## YOUR FOUR CONDITIONS
1. **DDL derived from CORE at `215cc687`** — every statement, same columns/types/defaults/constraints/order. Said in the migration's own header, with the reason there are now two creators.
2. **`pg_dump` equality — PROVED.** CORE's definitions alone vs 038a alone, two bare databases, four tables, filtered of pg_dump 18's per-dump `\restrict` nonce: **byte-identical**. Controls: a one-character type mutation (`varying(64)`→`(63)`) differs from both; two different tables' dumps are not equal. ⚠ **Two of the three sides you named were NOT driven** — the gateway runner and the docker/init seeded path. What I proved is the equality that carries the risk (the two creators agree). Named as not-run in the PR rather than implied.
3. **The regression under the compose runner — THREE-SIDED and it discriminates.** Real PG **18.3**, `listen_addresses=''`, **0 inet sockets proven by `lsof`** on the postmaster (control: 1 unix socket), never `:5432`, never a container, real unmodified `run-migrations.sh`, bare DB each time:

| tree | 039 recorded | `auth_find_oauth_app_by_client_id(text)` | policy | `tenant_isolation` | four tables |
|---|---|---|---|---|---|
| merge-base `0d156d12` | **0** — 039 itself FAILS | ABSENT | 0 | 22 | 0 |
| round-1 head `f5381338` | **1** — recorded, work skipped | **ABSENT** | 0 | 22 | 0 |
| **mine** | **1** | **PRESENT** | **1** | **25** | **4** |

  The middle row IS the defect, reproduced. A second pass changes none of those five on mine. ⚠ **The gateway runner was not driven** for R-PG1 either — the compose runner was, because it is the one my shape argument rests on.
4. **B 40th's decision record at `:23-42`** — the migration's own header now carries what round 2 does and why, including that the NOTICE's "the next boot creates the function" was false.

## MEASURED
- **api-gateway: 88 files, 795 tests, 0 failed, rc 0** (round 1: 87/790; +1 file and +5 cells are mine).
- `tsc --noEmit` build program **rc 0**. **Tests-including program: 29 → 29, delta 0** — measured as a delta, never by file ownership. Control: that program holds **87** `__tests__` files, the build program **0**.
- **ARMS 3/3**, same-volume backup, `try/finally`, each tamper `cmp`-proved to differ, each restore sha256-verified: `totalFailed += 1` removed from the main CORE catch → **C1 reds**; `error: totalError` removed → **C2 reds**; **038a deleted → S3 reds** (10 → 8 passed / 2 failed).
- **Three migrations that fail forever on the other two trees now succeed** — 006, 008 and 047, which operate on `svc_webhooks` and `oauth_apps`. A consequence, measured, not aimed at.

## 🔴 A CELL THAT PASSED WHEN IT SHOULD HAVE MOVED — and what it cost to find
`filesBelow()` filtered `/^\d{3}_/` and was **blind to a letter-suffixed migration**. So `S0` kept asserting `createdByFileMigrationBelow('oauth_apps', 39) === false` — **which my change had just made untrue** — and passed. The runtime is fine (both runners filter on `.sql` and sort lexically; the drill proves 038a applies), so this was a TEST-ONLY blind spot, but it is the exact shape I have been catching all round: a claim that drifts from what the code does, still green.
Consequences handled: the filter now matches the runners' own lex order; **S0 asserts the new truth**; **S1 would have gone VACUOUS** (with every table now file-created its loop `continue`s on all of them and its list is empty whatever 039 says) so it keeps the rule and gains an invented-table control that can still fail; and **S3 is new** — the round-2 invariant, and the cell that reds if anyone removes or renumbers 038a. Arm C proves S3 falsifiable.

## MY OWN INSTRUMENTS THIS ITEM — three more, all caught
1. **A non-unique tamper anchor** — the bare save line appears twice; the assertion refused and `try/finally` restored.
2. **My "mutate bottom-up so indices stay valid" comment was FALSE** — my index list was not sorted descending (1009 < 1015), so one insert landed a line early. Harmless (both read an already-computed value) but the reasoning was wrong; fixed for symmetry and disclosed.
3. **I assumed `applyFileMigrations` returned a `firstError`** because `migrateDatabase` does. It does not — tsc caught it as TS2339 ×2. I added the capture properly rather than dropping the field, so a failed file migration now carries a reason.
Also: **`KS-458` was hyphenated in my draft body and my own scanner caught it BEFORE posting** — the ITEM 1 ordering lesson applied.

## NOT COVERED (measured, not lifted)
- **N-1332-5 is NOT in this commit** — `deploy-all.sh:281` and `deploy.sh:823` still do not read the field. **UNRAISED for a successor, not dropped**, exactly as your Q2 fallback allows: the 039 fix went first and the window did not comfortably hold both.
- **N-1332-4** not commissioned, not fixed.
- The gateway runner and docker/init path (above). The four platform suites. Tenant databases (KS 1055).
- **A candidate, named not filed:** numbering the file below 006 instead of 038a would let 006/008/047 succeed on boot 1 rather than boot 2. **Not taken** — **12 migrations** reference these four tables, so an earlier number changes far more than the blocker needs.
- **The KS 764 guard reds on this branch** (`CALL_SITES`, 1 failed / 14 passed) — the pre-existing develop red that #1337 fixes, **measured identical with and without my edits**. This branch is based below that fix.
- **A deploy must rebuild BOTH the migrations image and the api-gateway image.** I deployed nothing.
- **RUNTIME change on start-up and /health: §5f live sweep owed.**

## MEANWHILE
Both PRs hold for gate39. I am writing the handover at `5_Project_History/HANDOVER-seatB41-2026-09-29.md` and will record the **real worktree path** in it and in this READY, as you instructed: `<scratchpad>/wt/s-b41-ks764guard` and `<scratchpad>/wt/s-b41-ks1054r2` on /System/Volumes/Data — a `/private/tmp` path does not survive a reboot; both branches are at origin so nothing is lost.
**The disk is still the fleet risk**: DevMASTER 1.5 GiB free of 1.8 TiB, and gate39's QA agent has no workaround.

-- Seat B 41st, Secuura/Blockchain, round 37



### PR BODY (gh_body_1332.md) TEXT_SHA256 d76cb8164e30ccb7f9ec1a6242edf487aabf0a785c34c3e13391d2fb60e19adf

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



### EVERY COMMIT MESSAGE IN THE CHAIN over 0d156d12cc0fc45fc323397c6999898565c44c54 (oldest first) TEXT_SHA256 def36563776bc819edc7d8c078cf336fe4fbf097cbed2cbee9f8bc9989eea90f

--- commit f5381338359da43784f01f625772abafccdf97b6
KS-1054: a failed start-up migration shows on /health; 039 guards oauth_apps

Two halves of one boot-1 failure.

THE STAGE ORDER. `039_rls_fail_closed.sql` declared
`auth_find_oauth_app_by_client_id ... RETURNS SETOF oauth_apps`, which needs the
table's row TYPE at CREATE time. On a fresh database the file stage runs BEFORE
the CORE stage that creates `oauth_apps`, so boot 1 failed with "type oauth_apps
does not exist" and the database stayed fail-OPEN until boot 2.

Guarded in the migration, with the table-exists idiom 039 already uses for its
own policy blocks, rather than by reordering the stages. Reordering would
contradict the documented reason CORE runs second (its column-add ALTERs must
keep landing on existing deploys) and would have to be proved against every
existing database as well as a fresh one. The guard is inert where the table
exists: the branch is taken and the function is created exactly as before.

Measured, which is why only ONE of the seven functions is guarded: 039's three
`RETURNS SETOF` tables are users, oauth_apps and svc_api_keys; `users` comes from
001_initial-schema.sql and `svc_api_keys` from 002_verification-tiers.sql, both
FILE migrations that run before 039. `oauth_apps` is created by no file migration
at all.

The owner/grant loop is guarded too. It ALTERs OWNER on all seven functions by
name, so skipping a create without it would move the failure four statements
later instead of removing it.

/health. `runStartupMigrations()` now returns its summary and records it in
`services/startupMigrationStatus`, which `/health` and `/health/ready` report as
`startupMigrations: { ran, applied, failed, lastRunAt, error? }`.

Both endpoints keep their status codes. `/health` stays 200 `healthy` because it
is liveness and the process IS serving; a non-2xx would restart the gateway
wherever an orchestrator acts on it, which is the "refuse to start" option by
another road. `/health/ready` keeps KS 1101's code (503 only when a dependency is
`down`) because the compose healthcheck probes `/health/ready` and 48
`service_healthy` conditions gate dependents on it.

SET by the latest run, never latched: `runDbBootTasks()` is `initDb`'s onReady
hook and runs again on the KS 377 background retry, so a failure the retry fixes
must stop being reported. `ran: false` is the initial state and is deliberately
not the same as `failed: 0` — before the first run there is nothing to report.

The per-tenant stage is NOT counted; that path is KS 1055.

The four widened annotations are consequences, not scope: `runStartupMigrations`
resolving a value rather than `void` made `{ runStartupMigrations: () => Promise<void> }`
narrower than the module, which read TS2322 in a program that includes the tests.
Those cells only await the call.

Refs KS-1054

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>

--- commit f2423bf7aa6c64952cf425d4160a048a55ffaaee
KS-1054 round 2: create the CORE tables before 039 so a fresh DB is never fail-open

Fixes gate38's N-1332-1 BLOCKER, plus N-1332-2 and N-1332-3.

N-1332-1, FRESH-DB-039-NEVER-COMPLETES. On a bare database 039 skips
oauth_apps, svc_webhooks, certifications and charge_events because their only
creator is the CORE stage, which runs after the file stage. 039 is then
RECORDED, and applyFileMigrations never re-runs a recorded file, so the OAuth
lookup function, its policy and tenant isolation on those four tables never
arrive on any later boot.

Fix shape (b) of the three the gate offered: a file migration numbered BEFORE
039 creates the four tables, so 039 finds them present on its only pass. Chosen
on a measurement, not a preference - scripts/run-migrations.sh, the compose
`migrations` service's own runner and the one a deploy uses, is a single pass
with no CORE stage and the same record-then-skip shape, so shapes (a) and (c)
would have fixed the gateway and left the container path still recording a
half-applied 039. Shape (b) fixes both runners with one change and leaves
intact the documented reason CORE runs second.

The new file's DDL is derived from CORE_MIGRATIONS at develop 215cc6875e2b and
proved schema-identical to it by pg_dump on a real PostgreSQL.

N-1332-2, CORE-THROW-READS-CLEAN: both CORE-stage catches logged and never
touched totalFailed, so a stage that died was served as `failed: 0`.

N-1332-3, ERROR-FIELD-NEVER-SET: `error?` was declared and never passed.
applyFileMigrations now returns a firstError the way migrateDatabase already
did, so a failed run carries a reason and not only a count.

Refs KS-1054

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>



### PUSH LOG STOP COUNTS (READ, bounded region; /private/tmp/claude-501/-Volumes-DevMASTER--CODING-Secuura-Blockchain/2d2b5ffa-7fc1-425c-b465-7f5fe13cd889/scratchpad/push41-ks1054.rawlog)

```
{
 "log": "/private/tmp/claude-501/-Volumes-DevMASTER--CODING-Secuura-Blockchain/2d2b5ffa-7fc1-425c-b465-7f5fe13cd889/scratchpad/push41-ks1054.rawlog",
 "lines": 1302,
 "pre_push_hook_base": "28/0",
 "fixture_guard": "6/0",
 "run_shell_suites_region": "49/0",
 "run_shell_suites_prefixed": "49/0",
 "shell_suites": "60 passed, 0 failed, 0 skipped (of 60)",
 "CONTROL_absent_header": "NOT FOUND",
 "fixture_build_failed_lines": 0,
 "verdict_line": "PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed.",
 "preflight_ran": true,
 "rc": "?",
 "start": "?",
 "end": "?"
}
```

## #1337 KS-888 (Seat B 41st (ITEM 1, from a local-model READY: KS-888 / the KS 764 guard — TEST-ONLY, one file: both copies of the security revoke pattern in packages/shared ks764-key-revoke-call-site-guard.test.ts (CALL_SITES :84, REVOKE_WRITES :104) widened from an 80-character window to a pattern that admits ONLY whitespace, whole // comment lines and one try { between the flip and the save; a Spark golden, canonical patch == golden == the held checker patch), T2) — head bb0067dde82ecda05d7c8ca465715d5a897a008d

#1337 ticket line: #1337 is KS-888.

### READY FOR QA MAIL <010001a0e93f721b-48293e38-86a4-458d-ad03-274705b9a5d4-000000@email.amazonses.com> (wednesday-agent@, inbox_digest.sh full, by id) + the local-model READY file TEXT_SHA256 531beaf5be18c0876716082f756dde0cf2a04b4787c93120813d3ebdb3c257af

From: secuura-blockchain <secuura-blockchain@agentmail.to>
To: ['wednesday-agent@agentmail.to']
Date: 2026-09-28T18:20:44.000Z
Subject: [Secuura/Blockchain -> Wednesday] READY FOR QA (Seat B 41st): #1337 KS-888 KS 764 guard at bb0067dde82e - ITEM 1, develop packages/shared goes green; holding for gate39
---
# READY FOR QA (Seat B 41st): #1337 KS-888 / the KS 764 guard at bb0067dde82e — ITEM 1 of the queue, HOLDING for gate39

## BLUF
**PR #1337 is up, head `bb0067dde82ecda05d7c8ca465715d5a897a008d`, base `develop`, based on `215cc6875e2b`.** https://github.com/Secuura/Distributed_Secuura/pull/1337
**Test-only, 1 file, +9/-2, no product file, no deployable surface.** **It turns develop's `packages/shared` green.** Nothing merged. **HOLDING for gate39.**

**Fuse: 29.7 h, computed at 2026-09-28T18:20:43Z.**

## THE FIVE ARTEFACTS
1. **PR + head:** #1337 at `bb0067dde82ecda05d7c8ca465715d5a897a008d`, re-read at origin by `ls-remote` **after** the push (trap 7 — the gate being green is not the ref landing). Base `develop`, 1 changed file, +9/-2, title **76 ch** (lands 84 with ` (#1337)`, under 92), ASCII, no `(#n)` in the declared subject.
2. **Ticket:** `Refs KS-888`. **Linear re-read after the body edit: `linkKind: contributes`.** KS-703 and KS-764 are **NOT** attached (checked explicitly). KS-888 still **In Progress** — I moved no ticket.
3. **Gate lines, from THIS push's OWN raw log:** **878 `ok` / 0 `FAIL` / 0 `not ok`** · shell suites **60 passed, 0 failed, 0 skipped (of 60)** · `FIXTURE BUILD FAILED` **0** · **PREFLIGHT INCOMPLETE — 12 of 15 legs ran, 3 SKIPPED** (legs 3, 4, 8: local stack not up). **Stated as a ratio in the PR body; 12/15 is not a pass and is not quoted as one.**
4. **Measurements** — table below.
5. **NOT COVERED** — below.

## MEASURED (clean worktree detached at `215cc687`, `npm ci` rc 0, on the Data volume as you ruled)
| | untouched tip | with the change |
|---|---|---|
| guard file | **1 failed / 14 passed (15)** | **15 / 15**, rc 0 |
| whole `packages/shared` | **48 files, 1 failed / 944 (945)** | **48 files, 945 / 945**, rc 0 |
| `tsc --noEmit` | rc 0 | **rc 0** |
| `eslint src` (run by hand) | 36 problems (1 error, 35 warnings) | **36 problems (1 error, 35 warnings)** |

- **The red is a real `AssertionError` on the `CALL_SITES` cell with the other 14 cells passing** — the controls did not also fail (B 40th's trap 1).
- **eslint delta is ZERO, proven by stash-and-restore, not by file ownership** (trap 5): both runs report `539:36 ... no-control-regex`, outputs differ by **0 lines**, restore `cmp` rc 0. It is the KS 703 control-byte guard already at `BACKLOG.md:876`.
- **The guard's own drift-sweep cell passes at `215cc687`** — your "#1330 changed nothing the guard sweeps" is now measured by the cell, not a grep.
- **ARMS 3/3**, each redding **14 passed / 1 failed** (not a loadfail): A save deleted · B a statement between flip and save · C flip moved after save. Same-volume backup, `try/finally`, every tamper `cmp`-proved to differ, restore verified by sha256 `7f29bb85765e7985` after each arm; post-restore **15/15**.
- **The patch, three ways, byte-identical:** READY block (exactly ONE fenced diff, as A1 claims) == canonical == golden, all **1275 B / sha256 `34f81565ed609004`**; mutated control differs.

## TWO CORRECTIONS, both measured
- **The READY's own A4 line is wrong.** It records "**2 failed** / 15 run" at the tip; I measure **1 failed / 14 passed (15)**. Your brief's figure was right. In the PR body.
- **A hunk-offset mutation is NOT a valid control for `git apply --check`** — it searches for the offset and still returns rc 0. Only a context-line mutation discriminates (rc 1).

## 🔴 ONE OF MY OWN, CAUGHT AFTER THE PR OPENED
I wrote **`KS-703` hyphenated** in the PR body — a FOREIGN hyphenated key, which is exactly what attaches a ticket. **My own `namecheck37` C8 control exists for this and I did not run it on the final body text before opening.** Caught on the post-open link-kind read: **KS-703 was NOT in fact attached**, I de-hyphenated it to "KS 703" anyway rather than rely on that, and re-read all three tickets after the edit. Control: the scanner returns `['KS-703']` on the pre-fix text, so it would have caught it. **The lesson is the ordering — scan the FINAL text before opening, not after.**

## NOT COVERED (measured, not lifted)
- The four platform suites (Schemathesis · Akto · Playwright · Performance/k6): **no runtime surface, no route, no schema** in this change.
- Preflight legs 3, 4, 8 — local stack not up.
- **No migration, no config, no env var, no image. No deploy: nothing deployable.**
- **A candidate, named not filed** (the READY's doubt 4, pre-existing): the drift sweep's equality finds `security/src/index.ts` through the **rotate**'s `UPDATE svc_api_keys SET is_active = false`, so `REVOKE_WRITES[1]` could drift unseen.
- `startup-migrations.ts` is in this guard's `NON_REVOKE_MENTIONS` allowlist — **I will re-run this guard on ITEM 2's branch**, per the READY's coupling note.

## MEANWHILE
Starting **ITEM 2** now on shape **(b)** as you confirmed, with your schema-equality condition. Read so far: 039 (`f5381338`) loops its table list and hits `RAISE NOTICE 'KS-458: skipping % — table does not exist on this DB'` for the four tables on a bare DB, then the file is recorded; the `oauth_apps_auth_lookup` policy at `:161-165` is behind the same `IF EXISTS`. CORE's four `CREATE TABLE IF NOT EXISTS` definitions are extracted and will be the source of the new pre-039 file's DDL, with the `pg_dump --schema-only` three-way equality you require. ITEM 2's worktree goes on the Data volume too.

-- Seat B 41st, Secuura/Blockchain, round 37



### LOCAL-MODEL READY FILE /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/READY_KS-888-KS764-GUARD_spark-dsv4flash_BRIEFED-TESTONLY-KS764-GUARD-ACCEPTS-KS888-REVOKE-SHAPE-PASS-7of7_2026-09-29.diff.md TEXT_SHA256 ec12101e355733dbc6536587cc72b4c1c59aab02afd80b19dff601a5b2203245

# READY — KS-764 GUARD vs the KS-888 revoke shape (spark-dsv4flash, briefed, test-only, first round) — PASS 7/7 — HELD for QA

> **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-09-28_KS-764-GUARD-KS888-SHAPE/out.md.checker/patch.diff`**. **BYTE-IDENTICAL to the brief-writer's golden** `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-764-guard-ks888-shape/KS-888.golden.diff` (`cmp` rc 0; a mutated-golden control rc 1), measured by Wednesday.

**Held BY HAND at 00:42 2026-09-29 by Wednesday overnight seat 24014037** (hold_ready.py cannot hold a test-only run on this input; the owed defect). Source develop **3d706c21f65e** (#1331, docs only; the Dev tree is identical to db8d85dcd).

- **Why:** #1327 (KS-888 revoke, Kam-ruled default a, merged on gate37) put a comment block and a `try {` between `apiKey.isActive = false;` and `await dbSaveApiKey(`, so the packages/shared KS-764 guard's 80-character window stopped matching. Develop has carried 1 failed / 945 since then (Seat B 40th bisected it; Wednesday confirmed it with a python regex over four revisions). The product is correct; only the guard changes.
- **The fix:** both copies of the pattern (`:77` CALL_SITES, `:97` REVOKE_WRITES) admit only whitespace, whole `//` lines and one optional `try {`, so a statement in between, a moved, deleted or commented-out save, or an early return still reds the guard (the brief-writer's five arms). A loose `{0,2000}` window was measured green even with the save deleted, so it was rejected.
- **Ticket:** the files are named KS-888 because KS-764 is archived (build_input refused it). The PR Refs KS-888 (the change that caused the red) and names KS-764 in its body. No closing keyword.
- **For the gate:** `startup-migrations.ts` is on this guard's allowlist, so run the guard on any branch that touches it (Seat B 40th's KS-1054).
- Checker verdict [checker.out, verbatim]:
  - `PASS A1 output is exactly one fenced ```diff block, nothing outside it`
  - `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`
  - `PASS A3 (test-only) touched-file set == { Blockchain/Dev/packages/shared/src/__tests__/ks764-key-revoke-call-site-guard.test.ts } — the product file is untouched, as the ticket requires`
  - `PASS A3c every '+' line the brief adds is in the product hunk (9 line(s)), and no tip line is re-added as a '+' (A3d)`
  - `PASS A4 RED-FIRST: src/__tests__/ks764-key-revoke-call-site-guard.test.ts fails at the untouched tip (2 failed / 15 run; controls green; assertion reds)`
  - `PASS A5 GREEN-AFTER: src/__tests__/ks764-key-revoke-call-site-guard.test.ts passes with the product hunk (15 passed / 15 run)`
  - `PASS A6 whole packages/shared suite: no NEW red vs the untouched tip`
  - `PASS A7 tsc --noEmit for packages/shared: rc 0 after the patch (baseline rc=0)`
  - `SUMMARY files=1 +9/-2 test=src/__tests__/ks764-key-revoke-call-site-guard.test.ts red_first=yes apply_mode=strict`
  - `PASS A2a ANCHOR: every hunk's old side sits at its header's start line at the tip (SUMMARY hunks=2 ok=2 bad=0 skipped_newfile=0)`
  - `SPARK RESULT: PASS (checker rc 0 + A2a anchor OK)`

```diff
--- a/Blockchain/Dev/packages/shared/src/__tests__/ks764-key-revoke-call-site-guard.test.ts
+++ b/Blockchain/Dev/packages/shared/src/__tests__/ks764-key-revoke-call-site-guard.test.ts
@@ -76,3 +76,10 @@
     // enough to mean nothing, so each site names its own write.
-    revokeWrite: /isActive\s*=\s*false;[\s\S]{0,80}dbSaveApiKey\(/,
+    // KS-888 (#1327) put a comment block and a try between the flip and the
+    // save, which an 80-character window could not span. Between the two this
+    // admits ONLY whitespace, whole // comment lines and one try {, so a
+    // statement in between, or a save that is moved, deleted or commented out,
+    // turns the guard red. [^!-~] is any character that is not visible ASCII,
+    // which here means whitespace; [/] [{] [(] are those literal characters;
+    // ^ under the m flag is the start of a line.
+    revokeWrite: /isActive[^!-~]*=[^!-~]*false;(?:[^!-~]*^[ ]*[/][/].*)*[^!-~]*^[ ]*(?:try[^!-~]*[{][^!-~]*^[ ]*)?await[ ]+dbSaveApiKey[(]/m,
   },
@@ -96,3 +103,3 @@
   /UPDATE\s+svc_api_keys\s+SET\s+is_active\s*=\s*false/i,
-  /isActive\s*=\s*false;[\s\S]{0,80}dbSaveApiKey\(/,
+  /isActive[^!-~]*=[^!-~]*false;(?:[^!-~]*^[ ]*[/][/].*)*[^!-~]*^[ ]*(?:try[^!-~]*[{][^!-~]*^[ ]*)?await[ ]+dbSaveApiKey[(]/m,
 ];
```


### PR BODY (gh_body_1337.md) TEXT_SHA256 b2031ac5440be744467bcace8785dd5625d14ca632d42012c9671a651dc63ce9

#1337 KS-888: widen the KS 764 call-site guard to the revoke shape 1327 introduced
head bb0067dde82ecda05d7c8ca465715d5a897a008d

## BLUF
**Test-only. The product is untouched; only the guard changes.** This turns develop's `packages/shared` green — it has carried **1 failed / 945** since 1327 merged. Measured here: **1 failed / 944 passed (945) → 945 / 945**.

`Refs KS-888`. KS 764 is Done and archived, so it is named de-hyphenated as prose throughout; this PR attaches to KS-888 only, and closes nothing.

## What was wrong
1327 (KS-888 revoke, Kam-ruled option a, merged on gate37) put a five-line comment block and a `try {` between `apiKey.isActive = false;` and `await dbSaveApiKey(` in `services/security/src/index.ts` (the flip is at `:1286`, the save at `:1293`). The KS 764 guard matched the pair with an 80-character window, which cannot span that. Both copies of the pattern — `CALL_SITES` (`:77`) and `REVOKE_WRITES` (`:97`) — stopped matching.

## The fix
Between the flip and the save the pattern now admits **only** whitespace, whole `//` comment lines, and one optional `try {`. So a statement in between, or a save that is moved, deleted or commented out, still reds the guard. A loose `{0,2000}` window was rejected by the drafter because it stayed green even with the save deleted.

## Test Evidence
**Touched:** `Blockchain/Dev/packages/shared/src/__tests__/ks764-key-revoke-call-site-guard.test.ts` — 1 file, 2 hunks, **+9/-2**. No product file.

**Ran** (all in a clean worktree detached at develop `215cc6875e2bac0b6d6b38918572384fbfcbdb77`, `npm ci` rc 0):

| | untouched tip | with this change |
|---|---|---|
| the guard file | **1 failed / 14 passed (15)** | **15 passed (15)**, rc 0 |
| whole `packages/shared` | **48 files, 1 failed / 944 (945)** | **48 files, 945 / 945**, rc 0 |
| `tsc --noEmit` | rc 0 | **rc 0** |
| `eslint src` (**run by hand** — the harness has no LINT leg) | 36 problems (1 error, 35 warnings) | **36 problems (1 error, 35 warnings)** |

- **The red is a real assertion, not a broken fixture.** It is an `AssertionError` naming the old regex on the `CALL_SITES` cell, and **the other 14 cells pass** — the controls did not also fail.
- **The eslint error is pre-existing and is NOT mine — proven as a delta, not claimed by file ownership.** The change was stashed, eslint re-run at the tip, and restored (restored file byte-identical, `cmp` rc 0). Both runs report `539:36 error Unexpected control character(s) in regular expression ... no-control-regex`, and **the two outputs differ by 0 lines**. It is the KS 703 control-byte guard, already recorded at `BACKLOG.md:876`.
- **The guard's own drift-sweep cell passes at `215cc687`**, so "did anything merged since change what the guard sweeps?" is answered by the cell, not by a grep.

**Arms — 3/3 red the fixed guard**, each a tamper on `services/security/src/index.ts`, each redding **14 passed / 1 failed** (not a load failure — the other cells still run):
- **A** the save deleted;
- **B** an unrelated statement between the flip and the save;
- **C** the flip moved after the save.

Method: same-volume backup, `try/finally`, every tamper `cmp`-proved to differ before its verdict was believed, and the file restored and verified by sha256 (`7f29bb85765e7985`) after each arm and again at the end. Post-restore the guard is **15/15**. The tamper anchor is the revoke site's three-line `try` block, asserted **unique** — the bare save line appears **twice** (mint `:1141`, revoke `:1293`) and a bare anchor would have tampered the wrong call site.

**Push gate, from this push's own raw log:** **878 `ok` / 0 `FAIL` / 0 `not ok`** · shell suites **60 passed, 0 failed, 0 skipped (of 60)** · `FIXTURE BUILD FAILED` **0** · **PREFLIGHT INCOMPLETE — 12 of 15 legs ran, 3 SKIPPED** (legs 3, 4, 8 — local stack not up). **12/15 is not a pass, and is not quoted as one.**

**NOT run:** the four platform suites (Schemathesis · Akto · Playwright · Performance/k6) — this change touches no runtime surface, no route and no schema. Preflight legs 3, 4 and 8. No deploy: **this has no deployable surface.**

**Migrations + config:** none. No migration, no config, no env var, no image.

## Correction to the READY's own evidence
The held READY's `A4` line records "**2 failed** / 15 run" at the untouched tip. **Measured here: 1 failed / 14 passed (15).** The single failing cell is `CALL_SITES`. Recording it because A4 is the READY's red-first evidence line.

## Not covered, and named rather than left silent
- **A candidate, not filed:** the drift sweep's equality finds `services/security/src/index.ts` through the **rotate**'s `UPDATE svc_api_keys SET is_active = false`, so `REVOKE_WRITES[1]` could drift without the sweep noticing. Pre-existing, not introduced here, and out of this change's scope.
- `services/api-gateway/src/startup-migrations.ts` sits in this guard's `NON_REVOKE_MENTIONS` allowlist. Any branch that changes what that file mentions must re-run this guard.

🤖 Generated with [Claude Code](https://claude.com/claude-code)



### EVERY COMMIT MESSAGE IN THE CHAIN over 215cc6875e2bac0b6d6b38918572384fbfcbdb77 (oldest first) TEXT_SHA256 dd8b7662e43b77125f4cd732a819bc67358ec25302a8525a4392b95974266f1f

--- commit bb0067dde82ecda05d7c8ca465715d5a897a008d
KS-888: widen the KS 764 call-site guard to the revoke shape 1327 introduced

Test-only. The product is correct; only the guard changes.

PR 1327 (KS-888 revoke, merged on gate37) put a comment block and a `try {`
between `apiKey.isActive = false;` and `await dbSaveApiKey(` in
services/security/src/index.ts. The KS 764 guard's 80-character window could
not span that, so packages/shared has carried 1 failed / 945 on develop since.

Both copies of the pattern (CALL_SITES and REVOKE_WRITES) now admit only
whitespace, whole `//` comment lines and one optional `try {` between the flip
and the save. A statement in between, or a save that is moved, deleted or
commented out, still turns the guard red - measured, three arms.

Refs KS-888

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>



### PUSH LOG STOP COUNTS (READ, bounded region; /private/tmp/claude-501/-Volumes-DevMASTER--CODING-Secuura-Blockchain/2d2b5ffa-7fc1-425c-b465-7f5fe13cd889/scratchpad/push41-ks764.rawlog)

```
{
 "log": "/private/tmp/claude-501/-Volumes-DevMASTER--CODING-Secuura-Blockchain/2d2b5ffa-7fc1-425c-b465-7f5fe13cd889/scratchpad/push41-ks764.rawlog",
 "lines": 1345,
 "pre_push_hook_base": "28/0",
 "fixture_guard": "6/0",
 "run_shell_suites_region": "49/0",
 "run_shell_suites_prefixed": "49/0",
 "shell_suites": "60 passed, 0 failed, 0 skipped (of 60)",
 "CONTROL_absent_header": "NOT FOUND",
 "fixture_build_failed_lines": 0,
 "verdict_line": "PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed.",
 "preflight_ran": true,
 "rc": "?",
 "start": "?",
 "end": "?"
}
```

## SEAT RECORD /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-764-guard-ks888-shape/README.md TEXT_SHA256 ceb6aa90316b605f63749f4ddcc4c53e2aa3c9d3f5471fc367633b570c8bc203

# KS-764 guard, KS-888 shape: Spark brief + golden (TEST-ONLY: the product is Kam-ruled and correct; the guard's pattern is stale)

Written 00:39 AEST 2026-09-29 by a brief-writer sub-agent for Wednesday. It ran no model, raised no PR, changed no GitHub or Linear state (Linear and the state of PRs #799, #1322 and #1327 were only READ, by `build_input.sh` and one read-only GraphQL query for KS-764), mailed nobody and wrote nothing under `!CODING/`. Every git write verb ran under `scratchpad/bw764/`, a `cp -a` copy of `bw0929/base`. The original was not written.

## The finding, plainly
**develop is red in `packages/shared`: 1 failed / 945** (measured, `db8d85dcd` and `3d706c21f`). The failing cell is `CALL_SITES matches every revoke surface written in the TWO KNOWN IDIOMS` in `ks764-key-revoke-call-site-guard.test.ts`. It fails at its per-site loop (`:290`-`:293`), by assertion: `services/security/src/index.ts` no longer matches `/isActive\s*=\s*false;[\s\S]{0,80}dbSaveApiKey\(/`.
- #1327 (KS-888 revoke) put five `//` comment lines and `try {` between `:1286` `apiKey.isActive = false;` and `:1293` `await dbSaveApiKey(apiKey, { rethrow: true });`. That is about 600 characters, and the window allows 80.
- The sweep equality in the same cell still passed at the tip. It finds `security/index.ts` through the OTHER pattern: the rotate's `UPDATE svc_api_keys SET is_active = false` at `:273`. So the route's own pattern is only checked by the per-site loop. That is pre-existing (see doubt 4).

## The fix (test-only, 2 edit points, one file)
Both copies of the pattern (`:77` and `:97`) become:
```
/isActive[^!-~]*=[^!-~]*false;(?:[^!-~]*^[ ]*[/][/].*)*[^!-~]*^[ ]*(?:try[^!-~]*[{][^!-~]*^[ ]*)?await[ ]+dbSaveApiKey[(]/m
```
Seven comment lines go above `:77` to explain it.
- **What it allows:** between the flip and the save, ONLY whitespace, whole `//` comment lines and one optional `try {`. The save must start its own line (`^` with the `m` flag).
- **Why no backslashes:** the pattern uses character classes (`[^!-~]` means whitespace here; `[/]`, `[{]` and `[(]` are those literal characters). On 2026-09-16 the KS-887 model doubled a backslash in a `+` regex line and lost a round. Every brief since keeps `+` lines backslash-free.
- **Why not a wider window:** `[\s\S]{0,2000}` goes GREEN with the save deleted. It then spans from the rotate loop's `k.isActive = false;` (`:258`) to `async function dbSaveApiKey(` (`:292`). Measured, below.

## Files
- `KS-888.md` is the brief (13,784 chars). It is named for **KS-888, not KS-764** (see "Ticket id").
- `KS-888.golden.diff` is the golden, sha256 `34f81565ed60…`: 1 file, 2 hunks (`@@ -76,3 +76,10 @@`, `@@ -96,3 +103,3 @@`), 9 `+` lines and 2 `-` lines.
- **Fence rebuild:** IDENTICAL to the golden (`cmp`). Mutated control (the final `/m,` changed to `/,`): DIFFER.
- **Char lint of `+` lines:** 0 contain a backslash, a backtick or a double quote (control: a planted backslash line counted 1). 0 non-ASCII lines. 0 blank context lines.
- **The `-` lines (2) and one context line DO carry backslashes.** They are the tip's text, so this cannot be avoided. The brief says to copy each backslash once. See doubt 1.

## Ticket id
**KS-764 is Done and ARCHIVED** (2026-09-14, PR #799 merged). `build_input.sh KS-764` refused it, verbatim: `build_input: REFUSED KS-764 — archived at 2026-09-14T02:01:53.326Z`.

No other ticket names the guard. A Linear search for `ks764-key-revoke-call-site-guard` found only KS-1155, which is about timing.

So I named the brief for **KS-888**:
- It is the ticket whose ruled change (#1327) caused the red.
- It is In Progress, and #1322 and #1327 are both merged.
- The build therefore carries `started_ok=`.

The folder keeps the requested name `KS-764-guard-ks888-shape/`. If you would rather file a new ticket, rename `KS-888.md` and `KS-888.golden.diff` to it and drop `started_ok=`.

## The tamper, and why it is not on the revoke
The builder admits a `test_file=` only under the PRODUCT's own package (`build_input.sh:408`). The checker plants a tamper as a ONE-line replacement in the product file. So a guard in `packages/shared` cannot have its tamper in `services/security/src/index.ts`. Also, the new pattern needs the save on its own line, and no single-line tamper can express that.

The builder tamper is therefore `packages/shared/src/security/keyRevokePolicy.ts:17`:
- It is a doc-comment line, byte-unique (`grep -c -F -x` = 1).
- The tamper makes it contain `UPDATE svc_api_keys SET is_active = false`, which puts a revoke write in the allowlisted policy module.
- Result: 2 failed / 15, both by assertion. The red cells are `CALL_SITES matches every revoke surface` (found 3 vs 2) and `every allowlisted non-revoke really is present`.

The grip on the REAL revoke was proved by the arms below. It was not proved by the checker.

## Measured (scratch copy at `db8d85dcd`, tree `6840bc5026da`; re-measured at `3d706c21f`, tree `49211e66ba23`; `Blockchain/Dev` subtree `31f29a587038` is IDENTICAL at both; vitest 4.1.10, node 24.7.0; `packages/shared` rebuilt, porcelain 0)

| step | result |
|---|---|
| `git apply --check` / `patch -p1 -F0 --dry-run` at the tip | rc 0 / rc 0; applied result `cmp`-identical to the measured file |
| the guard file at the untouched tip (RED) | **1 failed / 15**, the CALL_SITES cell, by ASSERTION (`toMatch`), 0 Unhandled |
| with the golden (GREEN) | **15 / 15**, 0 Unhandled |
| `packages/shared` suite | tip **48 files, 1 failed / 945**; golden **48 files, 945 / 945** (at both tips) |
| sweep with the new pattern (470 non-test files) | finds `services/security/src/index.ts` only; the UPDATE pattern finds originate `adminConfig.ts` + security. **Nothing new.** The other `isActive = false;` files (auth `session.ts`, m365 `index.ts`, referral `referralService.ts`) do not match. The probe and drift cells stay green. |
| new pattern over `index.ts` at 4 commits | `63db8a383` (pre-#1327) MATCH; `ea816de19`, `0d156d12c`, `db8d85dcd` MATCH at `:1286`. The old pattern matches only at `63db8a383`, which confirms Wednesday's finding. |
| tsc (temp tsconfig including the test file) | rc 0 at the tip and with the fix. Control: planted `const bw764plant: number = 'x'` gave rc 2 (TS2322). `tsc -p packages/shared --noEmit` rc 0. |
| eslint (from `Blockchain/Dev`) on the test file | rc 0 at the tip and with the fix. Control: planted `var` + `debugger` gave rc 1 (no-var, no-debugger). |
| **the real Spark checker on the golden as model output** (`prepare_clone.sh` then `spark_checker.sh`, clone at `3d706c21f`) | **SPARK RESULT: PASS**, A1-A7 PASS in test-only mode. A4: under the tamper, 2 failed / 15 by assertion, controls green. A5: 15 / 15. A6: suite 945 with 1 failed before and 0 failed after. A7: tsc rc 0. A2a: anchors 2/2. This ran on the 13,570-char build of the brief. The final brief differs only by one added "re-measured" premise line, and it was rebuilt rc 0. |

**Arms.** Each arm changed one thing in `services/security/src/index.ts` in the scratch copy and ran the FIXED guard file. The tip was restored and `cmp`-checked after.

| arm | new pattern | loose `[\s\S]{0,2000}` in both places |
|---|---|---|
| untouched tip | 15 / 15 green | 15 / 15 green |
| flip moved after the save | **1 failed / 15** (CALL_SITES, assertion) | **15 / 15 GREEN** |
| save deleted | **1 failed / 15** | **15 / 15 GREEN** |
| save replaced by `memApiKeys.set(apiKey.id, apiKey);` (never stored) | **1 failed / 15** | not run |
| save commented out (`// await dbSaveApiKey(...)`) | **1 failed / 15** | not run |
| unrelated statement between (`apiKey.isActive = !decision.allow;`) | **1 failed / 15** | **15 / 15 GREEN** |
| early `return` between the flip and the save | **1 failed / 15** | not run |
| builder tamper (`keyRevokePolicy.ts:17`) | 2 failed / 15 (both declared cells) | not run |

0 Unhandled in every arm. With the old pattern at the tip, the builder tamper also gives 2 failed / 15.

## build_input: rc 0
```
NIGHT_EXCERPT_TRIGGER_BYTES=60000 NIGHT_SOURCE_CHECKOUT=/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/24014037-1954-4f3d-a19e-71dd4e50a1cf/scratchpad/bw764/base NIGHT_BRIEFS_DIR=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-764-guard-ks888-shape bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/build_input.sh KS-888 <out>/input.json product=Blockchain/Dev/packages/shared/src/security/keyRevokePolicy.ts ref=Blockchain/Dev/packages/shared/src/__tests__/ks780-normalise-org-id-one-implementation.test.ts test_file=Blockchain/Dev/packages/shared/src/__tests__/ks764-key-revoke-call-site-guard.test.ts line=17 ctx=65536 started_ok=revoke-1327-merged_ks764-guard-test-only-carved-2026-09-29
```
Output, verbatim:
```
ticket KS-888 · In Progress (started) · Medium · assignee=kamil.kreiser@secuura.ai · updated 2026-09-28T12:37:49.971Z
attached PR #1327 (Secuura/Distributed_Secuura): merged
attached PR #1322 (Secuura/Distributed_Secuura): merged
WARN state is In Progress (started) — ADMITTED by started_ok: revoke-1327-merged_ks764-guard-test-only-carved-2026-09-29
product file PINNED: packages/shared/src/security/keyRevokePolicy.ts (ticket names 1: ['services/security/src/index.ts'])
fix shape: WEDNESDAY BRIEF (KS-888.md) — the ticket's fix-shape/decision gates are bypassed; the brief states the change and any decision → 'The exact change'
product packages/shared/src/security/keyRevokePolicy.ts (12157 B, 247 lines) defect line 17 [pinned (line=)]: '* PURE BY CONSTRUCTION: no database, no request, no clock, no environment. The'
reference test PINNED: Blockchain/Dev/packages/shared/src/__tests__/ks780-normalise-org-id-one-implementation.test.ts
test_file PINNED (modify in place): Blockchain/Dev/packages/shared/src/__tests__/ks764-key-revoke-call-site-guard.test.ts (21258 B) — suggested_test_file = it
  named sites: no '## Where' section — checklist empty (A3b passes vacuously)
  expected '+' lines from the brief's edit blocks: 9 (A3c)
  red cells declared by the brief: 2 ['CALL_SITES matches every revoke surface', 'every allowlisted non-revoke really is present']
  TEST-ONLY tamper from the brief: packages/shared/src/security/keyRevokePolicy.ts:17 '* PURE BY CONSTRUCTION: no database, no request, no clock, n' -> '* PURE BY CONSTRUCTION: UPDATE svc_api_keys SET is_active = '
  prompt source: WEDNESDAY BRIEF /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-764-guard-ks888-shape/KS-888.md (13784 chars) — the ticket description is NOT the prompt
  suggested_test_file = the brief's `## The test` File: line Blockchain/Dev/packages/shared/src/__tests__/ks764-key-revoke-call-site-guard.test.ts (== the title slug)
contract: key set == KS-871 input (top-level, ticket, repo)
wrote /private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/24014037-1954-4f3d-a19e-71dd4e50a1cf/scratchpad/bw764/bi_888/input.json (58160 B; ~14560 prompt tokens at 4 B/token — num_ctx 65536 leaves ~50976 for the answer)
```

The builder was refused twice before this rc 0:
1. **G6 tip.** develop had moved to `3d706c21f` (#1331, KS-1365, docs only: 4 files, none under `Blockchain/Dev`), and that commit was not in the object store. I fetched `origin develop` into the SCRATCH copy only. The `Blockchain/Dev` subtree hash is the same at both commits (`31f29a587038`), so I moved the scratch base to `3d706c21f`, rebuilt `packages/shared` and re-measured.
2. **KS-764 archived** (above).

## The round command (NOT run)
```
bash /private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/24014037-1954-4f3d-a19e-71dd4e50a1cf/scratchpad/bw764/round_db8d85dc.sh KS-764-GUARD-KS888-SHAPE KS-888 /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-764-guard-ks888-shape 60000 product=Blockchain/Dev/packages/shared/src/security/keyRevokePolicy.ts ref=Blockchain/Dev/packages/shared/src/__tests__/ks780-normalise-org-id-one-implementation.test.ts test_file=Blockchain/Dev/packages/shared/src/__tests__/ks764-key-revoke-call-site-guard.test.ts line=17 ctx=65536 started_ok=revoke-1327-merged_ks764-guard-test-only-carved-2026-09-29
```
- `round_db8d85dc.sh` is a copy of `bw0929/round_0d156d12.sh` with ONLY SP, SRC and TIP changed; `diff` shows 4 lines per side, the header note included.
- **TIP is `3d706c21f…`, not `db8d85dcd`.** `prepare_clone.sh` refuses when the clone HEAD differs from the input's tip, and the input's tip is origin develop. The file keeps the `db8d85dc` name, and its header says why.
- If develop moves again before the round, both the base and TIP need moving. The script stops on a HEAD mismatch.
- The run folder name in the script still carries the date `2026-09-28` (unchanged, as instructed).

**Round counter:** this is the first brief for this red. One rebrief is allowed, then it goes to the cloud.

## UNMEASURED / doubts for Wednesday
1. **Backslashes the model must COPY.** There are 2 `-` lines and 1 context line (Edit 2's `:96`), each with 4-6 backslashes. The KS-887 failure was a doubled backslash in a `+` line. A doubled one in a `-` line fails A2 strict and lenient apply, and `reanchor.py` keys on `-` lines. This cannot be avoided: those are the lines being replaced. The brief says to copy each backslash once. If it fails this way, the cheapest fallback is a Claude seat. This is not measured on Spark.
2. **The checker's tamper does not exercise the new pattern.** It is proved only by my arms. A3c (9 byte-exact `+` lines) is what stops the model shipping a looser pattern.
3. **`started_ok=` is my assertion.** I could not see the lanes. KS-888 validate has its own brief (`KS-888-validate-logonly`) on a different file (the security `ks888` test), so the two are file-disjoint. Confirm nobody else holds KS-888.
4. **Pre-existing and not fixed:** the sweep equality finds `security/index.ts` through the rotate UPDATE (`:273`), not through the revoke pattern. `REVOKE_WRITES[1]` can therefore stop matching without the equality noticing. Only the per-site loop catches it, and that is exactly what happened here. Worth a card; outside 3 edit points.
5. The pattern is strict by design. A trailing comment on the flip line (`apiKey.isActive = false; // x`) turns it red: measured with node, no match. In the other direction, `[^!-~]` counts any non-ASCII character in the gap as whitespace: reasoned, not tested.
6. Timing: KS-1155 records these tree-walking guards exceeding vitest's 5 s default under fleet load. Here the file ran in under 1 s, unloaded.
7. **File ownership:** Seat B 40th is in `vc-issuer`, `packages/shared/src/vc/verifier.ts` and `api-gateway` `startup-migrations.ts` / `health.ts` / `index.ts`. This brief edits `packages/shared/src/__tests__/ks764-key-revoke-call-site-guard.test.ts` and tampers `keyRevokePolicy.ts` in a clone only. The two are disjoint. Note that `startup-migrations.ts` is in this guard's `NON_REVOKE_MENTIONS` allowlist: if Seat B's migration change stops mentioning `svc_api_keys` + `is_active`, the drift cell goes red. That was not measured against Seat B's branch.


## SEAT RECORD /private/tmp/claude-501/-Volumes-DevMASTER--CODING-Secuura-Blockchain/2d2b5ffa-7fc1-425c-b465-7f5fe13cd889/scratchpad/drill41.out TEXT_SHA256 38bdffccf2e1ccab288b18970530e109366e9c1c6a6970f5437e104306bc153e

CT3 — the drill must tell the sides APART, or it proves nothing.

=== TREE: base ===
    bare DB created: drill_base
    BOOT 1 runner rc=3 | Summary: applied=42 failed=7
    after boot 1           039_recorded=0  oauth_lookup_fn=ABSENT                                 policy=0  tenant_isolation_policies=22  four_tables=0
    BOOT 2 runner rc=3 | Summary: applied=42 failed=7
    after boot 2           039_recorded=0  oauth_lookup_fn=ABSENT                                 policy=0  tenant_isolation_policies=22  four_tables=0

=== TREE: head ===
    bare DB created: drill_head
    BOOT 1 runner rc=3 | Summary: applied=43 failed=6
    after boot 1           039_recorded=1  oauth_lookup_fn=ABSENT                                 policy=0  tenant_isolation_policies=22  four_tables=0
    BOOT 2 runner rc=3 | Summary: applied=43 failed=6
    after boot 2           039_recorded=1  oauth_lookup_fn=ABSENT                                 policy=0  tenant_isolation_policies=22  four_tables=0

=== TREE: mine ===
    bare DB created: drill_mine
    BOOT 1 runner rc=3 | Summary: applied=45 failed=5
    after boot 1           039_recorded=1  oauth_lookup_fn=auth_find_oauth_app_by_client_id(text) policy=1  tenant_isolation_policies=25  four_tables=4
    BOOT 2 runner rc=3 | Summary: applied=47 failed=3
    after boot 2           039_recorded=1  oauth_lookup_fn=auth_find_oauth_app_by_client_id(text) policy=1  tenant_isolation_policies=25  four_tables=4



## SEAT RECORD /private/tmp/claude-501/-Volumes-DevMASTER--CODING-Secuura-Blockchain/2d2b5ffa-7fc1-425c-b465-7f5fe13cd889/scratchpad/drill41.sh TEXT_SHA256 b9c91bbe65428b5d2577e42adcbf4bf4bf876bb07e71c7c58235aa242d776fb1

#!/bin/bash
# Seat B 41st — R-PG1. The gate38 N-1332-1 regression, on a REAL PostgreSQL,
# under the REAL unmodified scripts/run-migrations.sh (the compose runner).
set -u
SP="/private/tmp/claude-501/-Volumes-DevMASTER--CODING-Secuura-Blockchain/2d2b5ffa-7fc1-425c-b465-7f5fe13cd889/scratchpad"
SOCK="/tmp/b41s"
export PATH="$SP/pgshim:/opt/homebrew/bin:$PATH"
PSQL="psql -h $SOCK -U postgres"

measure () { # $1 = dbname, $2 = label
  local db="$1" lbl="$2"
  local rec fn pol fc tabs
  rec=$($PSQL -d "$db" -tAc "SELECT count(*) FROM _secuura_migrations WHERE filename='039_rls_fail_closed.sql'" 2>/dev/null)
  fn=$($PSQL -d "$db" -tAc "SELECT coalesce(to_regprocedure('auth_find_oauth_app_by_client_id(text)')::text,'ABSENT')" 2>/dev/null)
  pol=$($PSQL -d "$db" -tAc "SELECT count(*) FROM pg_policies WHERE policyname='oauth_apps_auth_lookup'" 2>/dev/null)
  fc=$($PSQL -d "$db" -tAc "SELECT count(*) FROM pg_policies WHERE policyname='tenant_isolation'" 2>/dev/null)
  tabs=$($PSQL -d "$db" -tAc "SELECT count(*) FROM information_schema.tables WHERE table_schema='public' AND table_name IN ('oauth_apps','svc_webhooks','certifications','charge_events')" 2>/dev/null)
  printf "    %-22s 039_recorded=%s  oauth_lookup_fn=%-38s policy=%s  tenant_isolation_policies=%-3s four_tables=%s\n" \
     "$lbl" "$rec" "$fn" "$pol" "$fc" "$tabs"
}

run_tree () { # $1 = tree name
  local t="$1" db="drill_$1"
  echo "=== TREE: $t ==="
  $PSQL -d postgres -tAc "DROP DATABASE IF EXISTS $db" >/dev/null 2>&1
  $PSQL -d postgres -tAc "CREATE DATABASE $db" >/dev/null 2>&1
  echo "    bare DB created: $db"
  ( cd "$SP/tree_$t/Blockchain/Dev" && \
    DATABASE_URL="postgresql://postgres@localhost/$db?host=$SOCK" \
    bash scripts/run-migrations.sh > "$SP/drill_${t}_boot1.log" 2>&1 )
  echo "    BOOT 1 runner rc=$? | $(/usr/bin/grep -E '^Summary:' "$SP/drill_${t}_boot1.log" | tail -1)"
  measure "$db" "after boot 1"
  ( cd "$SP/tree_$t/Blockchain/Dev" && \
    DATABASE_URL="postgresql://postgres@localhost/$db?host=$SOCK" \
    bash scripts/run-migrations.sh > "$SP/drill_${t}_boot2.log" 2>&1 )
  echo "    BOOT 2 runner rc=$? | $(/usr/bin/grep -E '^Summary:' "$SP/drill_${t}_boot2.log" | tail -1)"
  measure "$db" "after boot 2"
  echo
}

echo "CT3 — the drill must tell the sides APART, or it proves nothing."
echo
run_tree base
run_tree head
run_tree mine


