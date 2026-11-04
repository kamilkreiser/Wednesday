GO WITH NOTES — HOLD-FOR-KAM (merging arms every later demo redeploy from develop to apply 058 on demo with no gate, against Kam's "never demo"; plus head cells more permissive than base, all inside Kam's card a)
# QA Gate 190 (Tier 1, round 1): PR 2002 / KS-1401 migration 058, tenant isolation where 039 is already recorded

**Merge tree for the merge seat:** `git merge-tree --write-tree 536642104002 eec20acf0b25` → rc 0, tree `1c8e329f1233c44dde894fb217c30c73c250e691`.
**MERGE-ORDER rule versus PR 2001: none needed.** Both runners decide by "is this filename recorded", never by order, so 057 and 058 apply in either merge order (driven on both runners, G190-F5).

## Subject
- Repo Secuura/Distributed_Secuura. Clone: `git clone --shared` of the read-only checkout into `<workdir>/repo`, PR refs fetched there only.
- Pinned at START (ls-remote 12:17:55Z): PR 2002 head `eec20acf0b257d6313331d01042abcad2a1d7fb0`, develop `536642104002f506f61e2e9b6c98a32bf19c3b10`, PR 2001 head `74ccf8666dc2673ed863451bb8eadc9dcd299098`.
- Pinned at END: ls-remote 12:36:32Z: PR 2002 head `eec20acf0b257d6313331d01042abcad2a1d7fb0`, develop `536642104002f506f61e2e9b6c98a32bf19c3b10`, PR 2001 head `74ccf8666dc2673ed863451bb8eadc9dcd299098`. **Unchanged.**
- Merge-base of PR 2002 with develop: `d92b849ece73`. One commit (author Kam Kreiser, trailer Co-Authored-By Claude Opus 5.5).
- Host: macOS arm64, PostgreSQL 15.19 (Homebrew keg, `/opt/homebrew/opt/postgresql@15/bin`), Node v26.8.1, tsx from the checkout's `node_modules` (read via `NODE_PATH`, nothing written there). NOT run on: Node 24, a gateway container, `postgres:15-alpine`, kintsugi or demo data.

**Method.** One gate-owned cluster (`<workdir>/tmp/pgdata`, socket `<workdir>/tmp/s`, 127.0.0.1:55190, pid recorded and stopped at the end). The base template is develop 536642104002's `docker/init/0[1-9]*.sql` followed by the REAL `scripts/run-migrations.sh` over develop's migrations: 58 applied, 0 failed, 57 main files recorded, 039 recorded, 058 absent. The one edit to the real runner is to the copy I ran: its fixed `/tmp/migrate-err.log` path (run-migrations.sh:127-133) points into the workdir, so that I write nothing outside it. Shapes: **K** = that template bent to Seat B 50th's 2026-09-30 kintsugi reading (charge_events RLS off with 0 policies; certifications with tenant_id, FORCE, 0 policies). **D** = the run-migrations.sh shape as built (certifications has no tenant_id and no RLS). **GW** = docker/init, then the REAL `runStartupMigrations()` from the develop worktree over tsx (startup-migrations.ts is byte-identical at the head; `git diff gh/develop pr/2002 -- startup-migrations.ts run-migrations.sh docker/init migrations` shows only 058). **O** = K with the four tables and the tracker owned by `mig_owner` (NOSUPERUSER NOBYPASSRLS), with the runner connecting as that role. Planted rows per table: A, A, B, NULL. Readers: `secuura_app` (NOSUPERUSER NOBYPASSRLS) with no GUC, GUC = '' (empty), tenant A, tenant B, the default tenant, and the platform_admin bypass, plus the table owner with no GUC. Each base cell and each head cell is measured on the same database, before and after the runner applies 058. All 16 mutants go through the same runner over five scenarios (K, O, D, X = absent table, L = lock held), and each fingerprint is diffed against the real file's.

## Findings

### G190-F1 — MAJOR — HOLD-FOR-KAM: merging alone applies 058 nowhere, but it arms every LATER demo redeploy from develop to apply it, with no switch
**FOUND.** Nothing deploys on merge. Every workflow that triggers on a push to develop (`pr-platform-suites.yml`, `pr-security-gates.yml`) is a test job: deploy words (rsync, demo-pk, kintsugi, appleboy, az vm, az containerapp, ssh -i) count 0 in each, against a control of 5 and 1 `runs-on` lines. `deploy-demo.yml` and `build-images.yml` are `workflow_dispatch` only, and `deploy-demo.yml` is additionally guarded and targets the deleted Container Apps estate. The headers also record GitHub Actions as retired for this repo. The live demo is a manual rsync of a working tree followed by `docker compose` on the VM (`deployment/DEPLOYMENT-ARCHITECTURE.md:32,67`). However, once 058 is on develop, ANY such redeploy applies it, for whatever reason it is made:
- the `migrations` compose service runs `scripts/run-migrations.sh` (`docker-compose.yml:181-190`), which applies every unrecorded file (`run-migrations.sh:118-124,149-171`);
- the gateway runs `runStartupMigrations()` on every DB-ready boot with no env gate (`api-gateway/src/index.ts:1235-1241`, `startup-migrations.ts:975-1057`).

There is no flag, exclusion list or environment check that keeps 058 off demo. Kam's card a says "never demo". The PR body's only guard is a sentence: "A demo redeploy from a develop holding 058 needs Kam's word first".
**TESTED.** Read: the `on:` block of all 17 files in `.github/workflows/` and both runners' apply loops; the boot hook. The runners' "apply every unrecorded file" behaviour was driven (G190-F5). NOT driven: an actual demo deploy, and any operator tooling outside the repo.
**HOW.** `git show pr/2002:.github/workflows/*.yml` `on:` extraction; `/usr/bin/grep -ciE` deploy words with a `runs-on` control; file:line reads above. **Kam to rule** before merge: either demo redeploys from develop pause until the kintsugi apply (and demo then takes 058 too), or demo accepts 058, or the deploy card carries a hard stop. This is a deploy-discipline condition, not a code defect.

### G190-F2 — MINOR (money-adjacent; inside card a): the backfill moves formerly NULL charge_events into the DEFAULT tenant's metered usage
**FOUND.** At base on K, the default tenant's explicitly filtered read (`chargeEvents.ts:205-207` / `:273-274` shape, `WHERE tenant_id = $tenant`) returns 0 for a NULL-tenant row. At head it returns 1 (cell P5: 0 → 1 on K and on D). So after the kintsugi apply, `GET /api/metering/usage` (`routes/metering.ts:126` → `getUsageSummary`) for the default tenant counts those rows: its count, its ADA total and its derived USD total all rise. This is exactly the ruled rule ("existing rows take the platform's default tenant"), but the PR body does not name the billing-visible effect. Kintsugi's NULL count is UNMEASURED (Seat B 50th's 2026-09-30 reading: 8 rows in total, NULLs not split out).
**TESTED.** The SQL shape on a real PostgreSQL. The metering route itself was not driven over HTTP.
**HOW.** `harness/q3_q6.sh`, cells P4/P5, `runs/q3_q6.out`. Suggest the deploy card's read-only pre-measure records `count(*) WHERE tenant_id IS NULL` per table, so Kam sees the number that moves into default-tenant usage.

### G190-F3 — INFO (HOLD-FOR-KAM condition, section 6): head cells MORE permissive than base exist, and every one is the ruled repair
**FOUND.** Counting app-role read cells (4 tables × 6 contexts × 3 shapes) plus the owner and write cells, the head is more permissive than the base in exactly these places:
- (a) K / GW **certifications**, which is default-deny at base: tenant A 0 → 2, B 0 → 1, default 0 → 1 (K), platform_admin 0 → 4 (K) / 0 → 3 (GW). On GW, the base side was measured on its own boot without 058 and the same 3 planted rows (`harness/gw_base_certs.sh`, all six contexts 0). An own-tenant insert goes from refused to allowed (W7, K and GW).
- (b) **Ex-NULL rows** become visible to the default tenant: DEF 0 → 1 on charge_events, oauth_apps and svc_webhooks (K, D, GW), and certifications 0 → 1 (K).

Nothing else loosens. In particular:
- no shape lets tenant B read A's rows at head;
- no context without a GUC or with an empty one reads anything at head;
- every cross-tenant insert or move is refused at head (W1, W6, W8, W9);
- a cross-tenant update touches 0 rows (W5).

(a) is KS 1376 closing, and (b) is card a's backfill. Section 6 says the condition is WRITTEN, and Wednesday rules on it. My reading: Kam's card already covers both.
**TESTED / HOW.** `runs/q3_q6.out` (K and D, base vs head, same databases) and `runs/q4_gw.out` (GW). Base cells and head cells come from the same instrument.

### G190-F4 — INFO: no over-block on a live path found; the stricter head cells hit no runtime query
**FOUND.** The stricter head cells:
- K charge_events loses every no-GUC and cross-tenant read and write: no-GUC 4 → 0, A 4 → 2, B 4 → 1, DEF 4 → 1, and inserts without a matching GUC are refused;
- D certifications drops from fail-open to the default tenant only: A 2 → 0, no-GUC 2 → 0;
- the non-superuser owner without a GUC reads 0 on all four tables at head.

Runtime callers of the four tables at the head, by file:line, excluding tests and migrations:
- **originate `services/chargeEvents.ts:179-186`** (INSERT) and **`:204-208`, `:268-280`** (SELECT). These go through `prisma` (`db.ts:230-263`), whose GUC proxy wraps each raw statement in a transaction with `set_config('app.current_tenant_id', <scope>)` (`db.ts:178-199`). Every originate request is scoped by the unconditional middleware `index.ts:264-268`: `resolveRequestTenantId` falls back to DEFAULT, and `tenantGucContext` seeds the GUC. Every caller passes that same value as the row's tenant: `certifications.ts:474/537/845/848/1263/1374/1541/1623/1698/1701/1705` (`getReqTenantId` = `req.tenantId`) and `metering.ts:91,126`. So GUC = row tenant, and the insert passes WITH CHECK (cell W2: own-tenant insert allowed at head).
- **originate `services/gdprService.ts:600` and `:1037`**: inside `runWithPlatformScope` (`:581`, `:972`), so the bypass arm applies (BYP reads 4/4 at head).
- **originate `routes/webhooks.ts:197,260,313,338,353,365,520`** (svc_webhooks) and **auth `services/oauth.ts:106-221`** (oauth_apps). Both tables are already FORCE with 039's policy on every measured shape, and 058 replaces that policy with byte-identical text (policy md5 `3356c6ad…` before = after = 039's own policy on `users`). These paths are unchanged.
- **`packages/shared/src/jobs/expiry-checker.ts:137-143`** (SELECT FROM certifications with no GUC) would read 0 at head on D, against 2 at base. It has NO instantiation anywhere under `Blockchain/Dev`: `git grep -P 'new ExpiryChecker\b'` finds 1 hit, the usage docblock at `expiry-checker.ts:10`, against a control of 1 for `export class ExpiryChecker`. The re-export at `shared/src/index.ts:222` is the only other reference. It is not live.
- **originate `index.ts:473`** is `CREATE TABLE IF NOT EXISTS charge_events`, DDL that RLS does not affect.

**TESTED.** Callers enumerated by `git grep -P` over `services/*/src` and `packages/*/src` at the head (table names, then SQL verbs). The behaviour of each guard was measured in SQL. The services themselves were NOT driven, and multi-tenant mode (`MULTI_TENANCY_ENABLED=true`, `createPoolProxy` → `queryWithTenantGuc`) was read, not run.
**HOW.** `git grep` commands as in the method; cells W2/P1-P3 in `runs/q3_q6.out`.

### G190-F5 — INFO: ORDER with PR 2001's 057 — both runners apply 057 after 058, and 058 after 057; no gap
**FOUND.** Neither runner orders by the recorded set. They iterate lex-sorted files and skip only a filename already present in `_secuura_migrations`: `run-migrations.sh:118-124` (skip) and `:149` (lex glob); `startup-migrations.ts:97` (sort) and `:137-141` (skip). There is no "highest applied" check and no refusal of a lower number. 057 (`svc_gateway_settings`, sha256 `36532377e096`) touches none of 058's four tables. Results on both runners:
- 058 merged first, then 057: the next run applies 057 only (`applied=1 skipped=59`), the table exists with 1 seed row, and the recorded order is 058 < 057.
- The reverse order applies 058 only.
- A fresh database with both present applies 057 then 058 (`applied=60 failed=0`), with all four tables at rls/force true.
- Control: rerunning the same database skips all 60.

Merge order is free.
**TESTED.** The REAL run-migrations.sh (orders A, B and fresh, `runs/q4_q5.out`) and the REAL `runStartupMigrations()` (orders A and B: step-2 log lines `applied 057_…` / `applied 058_…` respectively, `runs/q4_gw.out`), using PR 2001's 057 at its head 74ccf8666dc2.

### G190-F6 — INFO: atomic, idempotent, and it fails closed
**FOUND.**
- **Re-apply** (tracker row deleted, so the runner re-runs 058 on a database that already has it): row md5 and all four policy md5s are unchanged, the NOTICEs read "had 0 NULL rows" ×4 and "REPLACED" ×4, and the tracker is back to 1.
- **The title case** (039 recorded, effects missing on two tables) is shape K: repaired.
- **Absent table** (svc_webhooks dropped; it is LAST in the loop, so three tables had already been altered in-transaction): `RC=3`, `failed=1`, 058 unrecorded, and charge_events is still `rls=false, force=false, pol=0` with its NULL still NULL. Full rollback, because the one DO block is one statement (`run-migrations.sh:128` has no `--single-transaction`, and none is needed).
- **lock_timeout**: with ACCESS SHARE held on certifications (the 2nd table) for 20 s, the runner failed in 7 s wall (5 s timeout plus runner overhead) with "canceling statement due to lock timeout", RC=3, 058 unrecorded, and charge_events rolled back. After the lock was released, the retry applied it (RC=0, recorded).
- **Gateway second boot** (CORE runs again after 058 is recorded): all four tables keep rls/force and a policy with 039's md5. CORE does not undo 058.
- **Non-superuser NOBYPASSRLS owner** (shape O): the backfill fills all four tables (NULLs 0/0/0/0), and the owner with no GUC reads 0 at head.

**TESTED / HOW.** `harness/q4_q5.sh` → `runs/q4_q5.out`, `runs/q4_gw.out`, `runs/mut_REAL.fp` (scenario O).

## Mutants (red-proof)
Raw table, counted from `runs/mut_table.out` (generated by `harness/mut_table.sh`, which diffs each fingerprint `runs/mut_<id>.fp` against `runs/mut_REAL.fp`). Mutant files are built by `harness/mkmutants.py`, which asserts that each one differs from the committed 058 (sha256 `92d368fb4ae7`, unchanged across the series).

| mutant | behaviour | policy text | scenarios that kill it |
|---|---|---|---|
| M1 drop the NULL guard | KILLED | same | K, O, D (A/B rows rewritten to default, A=0 B=0 DEF=4) |
| M2 drop FORCE | KILLED | same | K, O, D |
| M3 drop DROP POLICY | KILLED | differs | K, O, D (CREATE fails where a policy exists) |
| M4 default tenant off by one digit | KILLED | same | K, O, D |
| M5 drop the bypass GUC | KILLED | same | O only (NULLs stay 1/1/1/1 under a NOBYPASSRLS owner) |
| M6 backfill before the policy (PR 1383's order) | KILLED | same | O only (certifications NULL stays, DEF 1 -> 0) |
| M7 drop lock_timeout | KILLED | same | L (waits for the lock, then applies: rc 0, not fail-fast) |
| M8 absent table CONTINUE instead of RAISE | KILLED | same | X (rc 0 and RECORDED, the 039 defect again) |
| MC1 drop `IS NOT NULL` | survived | differs | none: behaviourally EQUIVALENT (unset and '' GUC both read 0) |
| MC2 drop `<> ''` | survived | differs | none: behaviourally EQUIVALENT |
| MC3 drop `tenant_id::text = GUC` | KILLED | differs | K, O, D (every tenant reads all 4) |
| MC4 drop the platform_admin OR arm | KILLED | differs | K, O, D (BYP 4 -> 0) |
| G1 (gate's own) drop ADD COLUMN | KILLED | same | D (rc 3: certifications has no tenant_id there) |
| G2 (gate's own) drop WITH CHECK | survived | differs | none: EQUIVALENT (PostgreSQL applies USING as the check) |
| G3 (gate's own) drop certifications from the list | KILLED | differs | K, O, D |
| G4 (gate's own) policy AS RESTRICTIVE | KILLED | differs | K, O, D |

**Counts:** 16 mutants. 13 are killed by behaviour. 3 (MC1, MC2, G2) differ only in policy text, and for those 3 the seat's equivalence claim holds: all are behaviourally equivalent on every cell, including an EMPTY-string GUC. They are caught only by the text-equality-to-039 check (policy md5 `3356c6ad…` versus the mutant's). Seat's 12: 12/12 reproduced as killed, 10 by behaviour plus MC1 and MC2 by text, which matches the READY. Survivors as behaviour: MC1, MC2, G2, all equivalent.

**Note on M5 and M6:** both are killed ONLY when the runner connects as a non-superuser, NOBYPASSRLS table owner (scenario O). Compose's `migrations` service and the gateway's `MIGRATION_DATABASE_URL` both connect as `POSTGRES_USER` (`docker-compose.yml:194,484`), and that is a superuser in the postgres image, for which order and bypass make no difference. So the order fix protects a managed-Postgres or least-privilege owner, not the compose stacks as configured. It is correct either way.

## What passed (measured)
- **Q1 scope:** `git diff --name-status d92b849ece73 eec20acf0b25` = 4 added files, +759/-0, exactly the READY's list. The 058 blob sha256 is `92d368fb4ae7…` (match), 268 lines; the suite has mode 100755.
- **Q2 058 read whole (lines 139-253, one DO block).** For each of charge_events, certifications, oauth_apps and svc_webhooks, in order:
  - RAISE if absent (`:170-174`);
  - ADD `tenant_id UUID` if missing (`:181-186`);
  - ENABLE and FORCE RLS (`:197-198`);
  - DROP POLICY IF EXISTS `tenant_isolation` (`:204`);
  - CREATE POLICY `tenant_isolation`, PERMISSIVE, TO public, with USING = WITH CHECK = `(GUC IS NOT NULL AND GUC <> '' AND tenant_id::text = GUC) OR app.tenant_scope_bypass = 'platform_admin'` (`:210-228`, md5 equal to 039's policy on `users`);
  - then UPDATE `tenant_id = 'a0000000-0000-4000-8000-000000000001' WHERE tenant_id IS NULL` (`:237-238`).

  Before the loop, two transaction-local settings: `app.tenant_scope_bypass = platform_admin` (`:157`) and `lock_timeout = 5s` (`:166`). There is no NOT NULL, no delete, no tracker insert, and no "platform" in the name. **An app connection that is not platform_admin and has no GUC:**
  - K: before, charge_events read/write ALL (4/4 rows, any tenant insert OK), certifications 0 and refused, oauth_apps and svc_webhooks 0 and refused. After: 0 and refused on all four.
  - D: before, certifications read ALL (no RLS), the other three 0. After: 0 on all four.
- **Q3 real PG15:** NULL rows now carry the default tenant (NULLs 1/1/1/1 → 0/0/0/0, DEF rows 0 → 1 each; D certifications 2 → 2). Non-NULL rows are byte-identical (md5 `7c92b5d0` before = after on K). Tenant A reads exactly its own 2 rows per table, NOT the default tenant's (the policy is an equality, with no default-tenant arm). B reads 0 of A's rows (P3: K 1 → 0). The bypass reads all 4. Writes with the wrong tenant are refused (W1/W6/W8/W9). P-cells: A reads both of its own charge_events (`g-a1,g-a2`) and its own certifications (K `a1,a2`; GW A=2). No over-block of a tenant's own rows.
- **Q4:** G190-F5. **Q5:** G190-F6. **Q6:** G190-F3 / F4. **Q7:** G190-F1.
- **Q9:** the title "Refs KS-1401: migration 058 restores tenant isolation where 039 is already recorded" is 83 characters (≤ 92). Close-word-before-key count: 0 across title, body and commit message (a planted control `Closes KS-1401` counts 1). The body carries the apply plan: kintsugi only, never demo; DEFAULT_TENANT_ID read before the apply, STOP and card Kam if different; pre-measure; rebuild the migrations image; require the explicit "Applying 058…" line. **Body source:** the seat's `push/pr_body.md` (13,523 bytes) plus its `create_pr.out` read-back. The API read with the Secuura gh identity answered 404, so the body as it now stands on GitHub is UNMEASURED.
- **Q10:** `merge-tree --write-tree 536642104002 eec20acf0b25` rc 0, tree `1c8e329f1233…`. Develop moved 11 files since the merge-base, none in `migrations/` (`git diff gh/develop pr/2002 -- migrations` = only 058).

## NOT tested
- Kintsugi's real data: its four tables today, NULL-tenant counts, the policy TEXT actually on its oauth_apps and svc_webhooks (if either carries 012's older permissive text rather than 039's, 058 tightens it there: unmeasured), and its runtime DEFAULT_TENANT_ID.
- Demo's state, and any demo deploy.
- A real gateway or originate container; the services over HTTP; pgbouncer transaction pooling; multi-tenant mode; Node 24; `postgres:15-alpine`.
- The seat's own 92-assertion suite was NOT re-run. My cells are independent of it.
- The PR body as currently on GitHub (API 404 with the identity available to me).
- The KS-1401 ticket and comment.
- Whether any operator tooling outside the repo deploys from develop automatically.

## Plain answer for Kam
This change adds one database script that locks four tables so each customer only sees its own rows, and gives every row with no owner to the platform's default customer, as you ruled. I ran it on a real database in every shape I could build. It does what it says, it never touches a row that already has an owner, and if anything goes wrong it undoes itself completely and tries again next boot. It does not clash with the other open database change (PR 2001), whichever merges first. Merging does not change any live system by itself. But once it is merged, the next time anyone redeploys the demo from the main branch, for any reason, this script will run on demo too, and you ruled "never demo", so that needs your decision before merge. One visible side effect on kintsugi: any charge records that had no owner will start counting in the default customer's usage and billing totals.

## Housekeeping
- **Background processes started and stopped:**
  - postmaster pid 6869 (`pg_ctl -D <workdir>/tmp/pgdata stop`, confirmed gone, port 55190 free);
  - the lock-holder psql (pid 48696), which exited on its own and was confirmed gone;
  - the mutant loop and its watcher, both finished.

  No other seat's or gate's cluster, port or container was touched.
- **Stray-file check:** every one of my 26 runner copies points its error log at `<workdir>/tmp/migrate-err.log` (3 of 3 occurrences rewritten, 0 that still name `/tmp`). The `/tmp/migrate-err.log` on the host (mtime 23:23:25 local, 0 bytes) was therefore not written by this gate. The tsx cache and HOME live under `<workdir>/tmp` and `<workdir>/home`, and the checkout's `node_modules` was read through `NODE_PATH` only.
- **Tracked:** `harness/`, `runs/`, `verdict.md`. **Ignored:** `repo/` (clone and worktree), `scratch/`, `mut/`, `tmp/`, `home/`, `cwd/`.
