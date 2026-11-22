PR 2276: GO WITH NOTES (at head 13aa345653c03dd1b92e63ea5f46e5c4fcee626a; tier 1)

# Gate 400, tier 1 (Opus), PR 2276 (KS-2313), 2026-11-22 ~22:40-22:56 AEDT (11:40-11:56Z)

The merge GO stays Wednesday's to hold until Kam rules card `secuura-dashboard-org-delete-same-rule-1122`. This verdict covers the build of its default option a only.

## Pins
- **Pinned twice, at 11:40:51Z and 11:55:43Z**, by git ls-remote through the Secuura project's gh credential helper (read-only). The values were the same both times:
  - develop c8fd1653a5dc9b79c41f752b29afb296910831a4
  - PR 2276 head 13aa345653c03dd1b92e63ea5f46e5c4fcee626a
  - PR 2159 head 7b54e7cbb6f0
  - PR 2275 head 4c361b9cffd7
- gh pr view 2276: OPEN, not draft, MERGEABLE, base develop, 7 files, +571 -16, updatedAt 11:39:00Z (unchanged since the READY). ONE commit, whose parent is develop.
- **Merged state = the head.** `git merge-tree --write-tree origin/develop pr/2276` gives rc 0, and the tree is the head's own tree, 2fb8a0aac511.
- **PR 2275 (KS-1536) is still OPEN, so develop has SIX shared reds, not five.** The develop I ran is c8fd1653a5dc.

## How I measured
- **Clone and worktrees:**
  - My own clone is `_work/g`, cloned from GitHub (`--reference-if-able` gate 398's clone, `--dissociate`), with PRs 2276, 2159 and 2275 fetched.
  - Three worktrees: `d` (develop), `h` (head: suites, static, probe), `x` (head: red-first, mutants).
- **node_modules (APFS clones, read-only copies):**
  - The root node_modules, `packages/shared/{node_modules,dist}` came from gate 398's `h`. Between gate 397's head and develop, and in the PR, no package.json, lockfile or `packages/` file changed (diff empty both times).
  - `services/api-gateway/node_modules` (ioredis, jsonwebtoken and a few others) and `services/auth/node_modules` were copied from the seat's `s-w59-dev` tree. That is a read from `!CODING`, with nothing written there.
- Node v26.8.1 (not LTS). vitest for both suites. TMPDIR = `_work/tmp`.
- **Real PostgreSQL (Q1, Q2, Q3): no container.**
  - The engine is the machine's own Homebrew `postgres` 15.19 binary. I created the cluster with `initdb` in `_work/pg/data`, listening on 127.0.0.1:54400 only (`unix_socket_directories=''`). I started it and stopped it with `pg_ctl -D <that dir>` (postmaster pid 3296; nothing was killed by name).
  - **Role:** `secuura_app` LOGIN NOSUPERUSER NOINHERIT NOBYPASSRLS, created with startup-migrations.ts's own attributes. It is granted DML through the same default privileges as `docker/init/01-create-app-role.sh`. The owner is the separate role `g400owner`.
  - **`g400mig` (migrations-built):**
    1. the `_secuura_migrations` tracker (as `scripts/run-migrations.sh` creates it);
    2. `rights_holders` from the gateway's own boot DDL, verbatim (startup-migrations.ts:317; no migration creates it);
    3. **all 60 `migrations/*.sql` in the runner's glob order**, psql ON_ERROR_STOP per file: 58 applied, 2 failed (006 and 008, `svc_webhooks` does not exist; another service's table). Evidence: `evidence/migrate_g400mig.out`.
  - **`g400compose` (compose-built):** `docker/init/*.sql` in order (all OK except 00-create-platform-db, which needs dblink), then the same 60 migrations: 60 applied.
  - The repo's `npm run migrate` (node-pg-migrate) is NOT usable for this: it orders `038a_…` first and treats `config.js` as a migration, so it fails at uuid_generate_v4 (`evidence/migrate_whole.out`). I used the runner's own order instead.
- **Probe** (`_work/probes/g400-realpg-probe.test.ts`, findings-only; copies moved to `_quarantine/probe_copies` after each run):
  - **Real parts:** createAdminRoutes, requireAdmin, `db.ts` query() and transaction(), the shared tenant-GUC code, and a pg Pool connecting as `secuura_app`.
  - **Stand-ins:** the caller (test tokens through parseTestToken), and, only for the failure-injection and race cases, a wrapper around the real transaction() that throws after statement k or pauses after the count.
  - **Runs:**
    - head and develop, each on g400mig and on g400compose;
    - head on g400mig with the pool as the owner/superuser (the KS-2279 neighbourhood);
    - a re-run with `log_statement=all` on `secuura_app`, so the statement order is read from the server log.
- **Scripts in `_work/`:** `run_cwd_g400.py`, `suites_g400.sh`, `an_suites_g400.py`, `pgprobe/migrate_g400.sh`, `probe_run_g400.py`, `an_probe_g400.py`, `redfirst_g400.py`, `mutants_g400.py` (my own engine), `static_g400.py` (gate 398's, re-pointed), `mt_g400.py` and `lin_read_g400.py` (read-only GraphQL; the key is read into memory and never printed).
- **End state:**
  - d, h and x have 0 porcelain lines. x's admin.ts and db.ts were restored and sha256-checked after every mutant.
  - The postgres cluster is stopped.
  - The planted merge-tree commit 383eb22d85bf exists only in my clone and was never pushed.
  - Not touched: no `!CODING` write, no seat tree, no GitHub or Linear write, no deployed database, no container, no mail, no launch, no `cd`, no `rm`.

## Findings

There is no HIGH and no MEDIUM finding. On a real PostgreSQL built from the migrations, as the non-owner role the gateway uses, the rule holds as ruled:
- with users present: 409 and nothing deleted;
- with no users: the organisation and its rights holders go together, and CASCADE / SET NULL children follow the schema;
- a failure at any statement: nothing deleted;
- an absent organisation: 404.

### LOW
**G400-2276-1: a surviving mutant that is NOT equivalent. The cells never use a platform token that carries an organisation or tenant claim.**
- G11 sets `app.tenant_id` from the caller's claim, falling back to the id: `String(req.user?.tenantId ?? req.user?.organizationId ?? id)`. It compiles (tsc 0) and survives all 50 cells (0 failed), because every platform token in the cells has no claim, so the fallback yields the id.
- **Measured on g400mig as `secuura_app`:**
  - with G11 applied in x, a SYSTEM_ADMIN token carrying organisation/tenant B deleted organisation A with **200, and left A's 2 rights holders orphaned** (rh_a 2, orphan_rh 2);
  - the head, with the same token, deletes both (rh_a 0, orphan_rh 0; probe case P2c).
- The head is correct. The cells just do not pin "the GUC comes from the route's id, not the caller".
- Fix shape, if wanted: give U2's and E2's platform token an `organizationId`/`tenantId` claim of another organisation. U2 already asserts `s(TENANT, [OID])`.

**G400-2276-2: words that I could not reproduce here, or that are slightly loose. None is against the PR's behaviour.**
1. **"api-gateway … develop 2077/2077 and branch 2101/2101".** I measured 2068 passed + 9 skipped (develop) and 2092 + 9 skipped (head), with 0 failed assertions on both arms.
   - The 9 are `ks1128b-platform-seed-failure-warns-on-a-real-postgres`. Its own initdb cluster uses a unix socket under TMPDIR, and my absolute `_work` path exceeds the 104-byte socket limit. A relative TMPDIR fails too, because pg_ctl changes directory.
   - This is environmental and identical on both arms. The PR does not touch that file.
2. **"Test-types ratchet: OK (6 services). Ratchet leg test: 48 passed, 0 failed."**
   - In my clone the standalone ratchet is rc 1 on **auth** (2 new: `jwks.test.ts` TS2694 and `ks820-821` TS2345), **identical on develop and head**. The leg test is 45/3.
   - api-gateway itself: 15 errors, 15 in the baseline, 0 new (220 -> 221 files examined).
   - auth has no local install in any clone I could copy from. This is the same clone-install class gates 395, 397 and 398 recorded.
   - The auth leg is UNMEASURED here, not red against the PR. The PR touches no auth file.
3. **The facts comment 7f4a0237** lists 3 of the PR's 5 residuals. It omits the `rights_holders.tenant_id` premise and the spec `:id` gap. It says "named in the PR", so this is not false, only shorter.

### Info (not findings)
- **Compose-built database: a successful delete orphans more than users.** g400compose has 0 foreign keys into organizations (control: g400mig has 12). There, on both arms, a 200 delete leaves these rows pointing at nothing (probe P2/P3 on h_compose):
  - documents (P3: the document stays, and the delete answers 200 rather than the migrations-built 500);
  - organization_members, api_keys, m365_connections and signatories;
  - audit_logs (not nulled).
  This is pre-existing and part of KS-2312's drift. The PR's residual says documents and members are not deleted and that a document refuses "where the foreign keys exist", which is accurate. The compose-built consequence for documents is implied, not stated.
- **db.ts `transaction()`** issues ROLLBACK in its catch without a guard. If ROLLBACK itself throws, the original error is replaced and the client is released without its error flag. `queryWithTenantGuc` swallows that case. The route still answers 500. This is pre-existing code, now with its first caller.

## The commission's questions

- **Q1 THE UNIT, real PostgreSQL 15.19, migrations-built (g400mig), pool as `secuura_app`** (identity row: super=false, bypassrls=false, owner of organizations = g400owner). **Holds.**
  - **Users remain: 409, `{"success":false,"error":{"code":"CONFLICT","message":"Organization still has users"}}`, and nothing changes.** The before and after rows are identical across org, 2 rights holders, users, members, api_keys, m365, signatories and audit. Cases:
    - P1: 1 user, with every child kind present;
    - P1b: 5 users;
    - P1c: the only user is in **another tenant** with organization_id = A. The count under the bypass sees it, so 409;
    - P1d: SUPER_ADMIN.
  - **No users: 200.** org_a 1 -> 0 and rh_a 2 -> 0, while B and its rights holder are untouched. The CASCADE children (organization_members, api_keys, m365_connections, signatories) go 1 -> 0. audit_logs goes to SET NULL (audit_a 1 -> 0, audit_null 0 -> 1). There are 0 orphan rights holders and 0 orphan users. All of these are what the schema's 4 CASCADE and 1 SET NULL keys say. The FK census matches the seat's: 12 keys, 4 CASCADE, 1 SET NULL, 7 NO ACTION.
  - **A NO ACTION referrer (a document): 500 with the constant body, and everything is back,** including the rights holders deleted earlier in the unit (P3; log: `documents_issuer_organization_id_fkey`).
  - **Failure injected after each of the 5 route statements** (lock, count, set_config, rights-holders delete, organisation delete; each statement actually ran, then the client threw): 500 every time, and the table state is byte-identical to before (P6 @1-@5).
  - **Absent:** 404 `NOT_FOUND`, unchanged (P4). **Unwired transaction:** 500, unchanged (P8).
  - **Develop on the same database, for contrast:**
    - users present: 500 at `users_organization_id_fkey`;
    - no users: 200 with **2 rights holders orphaned**;
    - every injection: 200 with deletes (develop ignores the injected transaction).
  - **Platform scope vs tenant admin:**
    - **Platform (SYSTEM_ADMIN, SUPER_ADMIN):** the lock and the count see every tenant's rows through the 039 bypass, and the unit deletes as above.
    - **A tenant admin, including deleting its OWN organisation:**
      - **404, and it sees nothing.** P5 (own organisation, no users), P5b (own organisation, 1 user) and P5c (another tenant's organisation) all answer 404 with nothing changed.
      - The server log shows BEGIN, then the lock with no GUC, then COMMIT.
      - That is the KS-1936 / KS-2279 neighbourhood, unchanged by this PR: the router sets no tenant context, and no app-level middleware before line 937 calls runWithTenantId. Only authenticateToken and the audit middleware's own write do.
  - **The same probe with the pool as the owner/superuser** (what KS-2279 is about):
    - a tenant admin deletes its own organisation (P5) **and another tenant's organisation (P5c) with 200**, the rights holders going with it;
    - with a user present it now gets **409** (P5b).
    This matches the PR's sentence, and it is not a defect of this PR.
  - **Transaction-local GUCs:** after a successful unit, the same pooled backend (pool total 1) reads `app.tenant_id = ''` and `app.tenant_scope_bypass = ''` (P7).

- **Q2 CONCURRENCY, measured with two real connections.** The route's unit paused 1.5 s right after its COUNT. A second `secuura_app` connection, under the platform bypass, INSERTed a user into A at that moment.
  - **g400mig (foreign key present):**
    - the insert started at +1 ms and **blocked until the unit committed** (+1505 ms);
    - it then failed with `23503 users_organization_id_fkey`;
    - the route answered 200. End state: 0 users, 0 orphan users, 0 orphan rights holders.
  - **g400compose (no foreign key):**
    - the insert **completed at +2 ms**, unblocked;
    - the route then deleted A (200), leaving **1 orphan user**.
    This confirms the PR's residual exactly.
  - Reasoned, not run: an uncommitted insert that already holds KEY SHARE before the lock makes FOR UPDATE wait. The COUNT, a new READ COMMITTED snapshot, then sees the user and answers 409.

- **Q3 THE BYPASS GUC: confirmed independently, three ways.**
  1. **Code:**
     - db.ts:62-78 `transaction()`: getClient, BEGIN, `applyTenantGuc(client)`, fn, COMMIT or ROLLBACK.
     - `applyTenantGuc` sends `scopeConfigStatement()`, the same function `queryWithTenantGuc` uses: `SELECT set_config('app.tenant_scope_bypass', 'platform_admin', true)`, no values.
     - `adminScope(req, () => transaction(...))` calls transaction() inside `runWithPlatformScope`'s callback, so the store is set when applyTenantGuc reads it.
  2. **The server's own log** (`evidence/pg_statements_h_mig_app.log`, one backend pid). For every platform case the order is BEGIN, the bypass set_config, `SELECT … FOR UPDATE`, COUNT, `set_config('app.tenant_id', $1, true)`, the rights-holders DELETE, the organisations DELETE, then COMMIT or ROLLBACK. For a tenant admin it is BEGIN, the lock, COMMIT, with no GUC.
  3. **Behaviour:** without the bypass, `secuura_app` cannot see organisation A (P5's 404). With it, A is deleted (P2).
  - **Mutants:** M14b (transaction() never sends the scope GUC) is killed by 9 cells. M11b (adminScope replaced by an identity wrapper) is killed by 9.
  - **Paths where transaction() runs without the bypass:** only a non-platform role, by design (adminScope sends no scope). No platform path misses it.

- **Q4 THE CELLS: reproduced. Survivor: G11 (G400-2276-1).**
  - **Red-first** (x: develop's admin.ts and index.ts written over the head's, the head's three cell files run, then restored and sha-checked): **50 run, 19 failed, 31 passed, 0 suites failed to run.**
    - **The new file: 17 red, 7 green** (C4, C5a, C5b, C10, E0, E4, E5). Every failure is an assertion:
      - `200` vs `409` (U1);
      - `200` vs `500` (U3b, U7 x6, U8);
      - `404` vs `500` (U9);
      - the statement log 4 vs 8 entries (U2, U3a);
      - U6a/U6b shape;
      - E1 `500` vs `409`; E2 rh 2 vs 0; E3 `200` vs `409`.
    - **ks1868 C2 x2:** red (`[Array(1)]` vs the five statements).
  - **Green on the head:** 50/50.
  - **Mutants** (x; the three files, 50 cells; the no-mutant BASE fails 0; every mutant compiled, tsc 0):

    | mutant | failed |
    |---|---|
    | M1b users check never fires | 3 |
    | M2 `> 1` | 3 |
    | M3 count before the lock | 14 |
    | M4 app.tenant_id set_config dropped | 6 |
    | M5 set_config session-wide (false) | 6 |
    | M6 rights-holders delete dropped | 6 |
    | M7 rights-holders delete moved onto query() | 5 |
    | M8 fail-closed count dropped | 6 |
    | M9b one-row check never fires | 1 |
    | M10 409 answered as 200 | 3 |
    | M11b adminScope dropped | 9 |
    | M12 FOR UPDATE dropped | 16 |
    | M13 unwired falls back to the old statement | 1 |
    | M14b transaction() skips the GUC | 9 |
    | M15b absent-organisation return never fires | 2 |
    | G1b lock dropped entirely | 10 |
    | G2 count after the deletes | 14 |
    | G3 `SET app.tenant_id` (session-wide, by SET) | 6 |
    | G4a 409 message changed | 2 |
    | G4b 409 code ORG_HAS_USERS | 2 |
    | G4c 409 as 400 | 3 |
    | G5 unwired answers 200 | 1 |
    | G6 organisation deleted before its rights holders | 6 |
    | G7 count without the organisation bound | 16 |
    | G8 transaction() COMMITs in its catch | 9 |
    | G9 users check after the rights-holders delete | 3 |
    | G10 rights-holders delete by tenant_id | 6 |
    | **G11 set_config from the caller's claim** | **0, survivor** |

  - **Spelling notes:**
    - My first M11 and G1 spellings failed tsc (TS2367). They were re-spelled as M11b and G1b and re-run (`evidence/mutants_run1.out`, `mutants_run2.out`, `mut/*.json`).
    - The seat's M1, M9, M14 and M15 forms likewise do not compile. I used compiling forms throughout.

- **Q5 WHOLE:**
  - **api-gateway vitest:**
    - develop: 2077 tests in 541 files; head: 2101 in 544. 0 failed assertions on both.
    - 24 test names only on the head (the new file), 0 only on develop, 0 changed status. The two inverted C2 cells keep their names.
    - The 9 ks1128b skips are explained under G400-2276-2.1.
  - **packages/shared vitest** (develop c8fd1653a5dc, six-red develop):
    - 1730 tests, 1724 passed, 6 failed on BOTH arms. The **failing-name sets are IDENTICAL**: ks1536 G2; ks1725 F and J; ks727 corpus-2 x2; wallet-signature KS-278.
    - 0 only on the head, 0 changed status.
  - **tsc** (api-gateway, `--noEmit`): 0 (planted: rc 2, 1 error).
  - **eslint:**
    - The 3 cell files: 0 errors, 0 warnings.
    - admin.ts: 16 no-unused-vars warnings on both arms. index.ts: 2 warnings (no-namespace and an unused disable) on both arms. 0 errors.
    - Planted control: rc 1.
  - **test-types (check.cjs api-gateway):** 221 examined, 183 under `__tests__`, 15 errors, all in the baseline, 0 new (planted: 1 new, rc 1).
  - **Fragments:** OK (planted: FAIL). **check:openapi:** CHECK PASS, run with a relative TMPDIR resolving to `_work/tmp`, as gate 398 did.
  - **Ratchet:** see G400-2276-2.2.
  - **Overlap:**
    - Of 21 open PRs, only **PR 2159 touches one of the 7 paths, admin.ts**. index.ts and the other 5 paths: none.
    - Control: package-lock.json is in 11 PRs. No file list reached 100.
  - **merge-tree:**
    - head vs develop: rc 0.
    - **head vs PR 2159: rc 0** (tree b63b478cc329).
    - **Planted control:** local commit 383eb22d85bf on the head edits `const body = req.body || {};` in the settings PUT, the line PR 2159 inserts after. Merged against PR 2159 it gives **rc 1**, CONFLICT (content) in admin.ts.
    - The waiver's two conditions reproduce.

- **Q6 WORDS:**
  - **The PR body holds sentence by sentence, except G400-2276-2.1/.2.** Checked:
    - **The direction line** (the card's default, pending Kam; b drops the users check; c closes unmerged): present.
    - **What was wrong:** reproduced on develop (P2: orphaned rights holders; P1 on g400mig: 500; P1 on g400compose: 200 with orphaned users).
    - **The order, the 409 bytes, the fail-closed count and the one-row rollback:** measured.
    - **"without it a non-owner role deletes zero rights holders":** cell E0, and 027 has no FORCE and keys on `app.tenant_id` alone.
    - **"The platform bypass GUC is unchanged":** Q3.
    - **"Not changed … does not fix KS-2279":** Q1; and the superuser sentence was measured.
    - **Behaviour changes:** measured. **The inverted pin:** stated.
  - **The residuals:**
    - *the dashboard shows 'Failed to delete'*: accurate. `api.ts:915-920` returns `res.ok`, and `Organizations.tsx:111-113` shows 'Failed to delete' for any non-ok.
    - *documents and members not deleted*: accurate (see the Info note for compose-built).
    - *no FK on compose, so the race*: measured in Q2.
    - *the rights_holders.tenant_id premise*: accurate (027's text).
    - *no spec :id path*: accurate. `secuura-api.yaml` has `/api/users/admin/organizations` (line 17964) and 0 `organizations/{` paths. Control: `/api/users/admin/{id}` at 18157.
  - **NOT run:** honest. The PREFLIGHT INCOMPLETE line is stated.
  - **The facts comment 7f4a0237 on KS-2313** (read-only; 2,849 B; updatedAt .062Z is not after createdAt .079Z, so it is unedited):
    - every sentence I could check holds;
    - its figures carry the same 2077/2077 and "ratchet clean" as G400-2276-2;
    - it lists 3 of the 5 residuals (G400-2276-2.3).
  - **KS-2313:** In Progress, priority 2, 1 comment. **KS-2279:** In Progress, priority 3, 0 comments.

## Two-NO-GO cap
Not engaged.

## Faults, disclosed
- **Hook refusals, re-issued:**
  - a zsh `=` separator;
  - a `git -C $W/g worktree` flagged as outside WEDNESDAY (a variable-path false positive; I re-issued it with the literal `_work` path);
  - a zsh `$spec` that did not word-split (re-issued with explicit arguments).
  None of them ran anything.
- **Probe bug:** my first probe passed `undefined` for "unwired", which a default parameter turned into the real transaction, so P8 read 200. I fixed the probe (null sentinel), re-ran every arm, and every figure above comes from the fixed runs.
- `npm run migrate` (node-pg-migrate) was tried first. It mis-orders, fails, and rolls back on its own scratch database, which I then dropped and rebuilt. The repo's runner order was used for every result.
- The initial migration attempts without the tracker table, and without `rights_holders`, are superseded by the final build. The `g400mig` I measured is the third build of that database.
- `ALTER ROLE secuura_app SET log_statement='all'` and `ALTER SYSTEM SET log_line_prefix` were set on my own throwaway cluster only, then reset or stopped with it.
- I read the seat's `mutants_m1.json` / `mutants_m2.json` read-only for the M1-M15 descriptions. My engine and spellings are my own.
- No mail, no `cut -c`, no `cd`, no `rm`.

## Not run
- A booted gateway, any HTTP request, the dashboard in a browser, any deployed or live database, a container.
- The four platform suites. Node 24.
- The auth ratchet leg on a proper install. ks1128b's 9 cells (socket path length).
- A merged 2276+2159 tree's suite.
- The pre-lock uncommitted-insert race (reasoned, Q2).
