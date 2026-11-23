PR 2284: GO WITH NOTES (at head 068ce040cd64286dce78f829ce3c5176949a1470; tier 1)

# Gate 408, tier 1 (Opus), PR 2284 (KS-2275), 2026-11-23 ~10:31-10:57 AEDT (23:31-23:57Z)

Authority: Kam's card `secuura-ks2275-unverified-email-document-reads-1119` = a ("Only verified addresses open 'sent to me' documents"). I read it with `decision_queue.sh show` (status ruled, choice a). Wednesday ruled the HOW as shape B. **The deploy is Kam's and waits on the verify-email page (KS-2294). This GO covers the merge only.**

## Pins
- **First pin, 23:31:42Z** (git ls-remote): develop 58bec7985343205408db2d5ba2ac4d719bdda0c8; refs/pull/2284/head 068ce040cd64286dce78f829ce3c5176949a1470.
- **Second pin, 23:56:51Z:** the head is unchanged. **Develop had moved again, to 8389ed294629cd87956ef376cfee8574b473db86** (KS-2324).
  - That commit changes 11 files, all under `frontend/admin/`. None of them is one of the PR's 8 paths, and nothing under services, packages, migrations, docker or the package files changed.
  - `merge-tree` of the head onto 8389ed29 gives rc 0 (tree 9589d269b877). Its services, packages, migrations, docker and package files are byte-identical to the merged tree I measured.
  - **So every suite figure below, measured on develop 58bec7985343, holds for 8389ed29 too.**
- **gh pr view 2284:** OPEN, not draft, base develop, ONE commit 068ce040 (parent bb8fd11b3d1f), 8 files, +638 -14, updatedAt 23:28:00Z.
- **Develop moved twice since the build** (bb8fd11b3d1f → 58bec7985343 → 8389ed29):
  - 58bec79 is KS-2317: 5 files in packages/shared tests and mcp-server comments/fragments.
  - Neither move touches any of the PR's 8 paths (overlap 0 each time). The merge-tree onto 58bec79 gives rc 0 (tree dcfe2f9e60e1).
- **The develop I ran is 58bec7985343, for every suite and every probe.** The merged state is a local commit, 451d6312efe9 (never pushed).

## How I measured
- **Clone and worktrees:**
  - Clone: `_work/g`, cloned from GitHub (`--reference-if-able` gate 400's clone, `--dissociate`).
  - Worktrees: `d` (develop 58bec79), `h` (the merged state: suites, static checks, probe) and `x` (the merged state: red-first and mutants).
  - Git write verbs ran only through `_work/gitx.sh`, which is hard-wired to my clone.
- **node_modules:**
  - The root node_modules, originate's node_modules and packages/shared's `node_modules` and `dist` are APFS clones of gate 398's `h`.
  - From c8fd1653 to the merged state, no package.json, package-lock or packages/shared source changed (diff empty).
  - Originate's Prisma client was generated in my own `h` and `x` (`npm run generate`).
  - Node v26.8.1 (not LTS). TMPDIR is `_work/tmp`.
- **Real PostgreSQL, no container** (I did not touch the seat's `w67-ks2275-pg`; it is still listed by `docker ps -a`):
  - The Homebrew `postgres` 15.19 binary. `initdb` in `_work/pg/data`, listening on 127.0.0.1:54408 with no unix socket; started and stopped with `pg_ctl -D`.
  - Roles: superuser `g408super` (compose's POSTGRES_USER), and `secuura_app` LOGIN NOSUPERUSER NOBYPASSRLS NOINHERIT, given DML through the same default privileges as `docker/init/01-create-app-role.sh`.
  - **`g408mig`: migrations only.** `_secuura_migrations` plus all 60 `migrations/*.sql` in the runner's glob order, single-database routing, ON_ERROR_STOP per file. 55 applied, 5 failed (006 and 008: no `svc_webhooks`; 026-028: no `rights_holders`). **Originate cannot create a document on this database:** 42P10, because `documents.external_id` has no UNIQUE. That constraint comes only from `docker/init/01-schema.sql` or the gateway's boot DDL. So no result below uses g408mig.
  - **`g408comp`: compose-built, which every result below uses.** `docker/init/*.sql` in order (all OK except `00-create-platform-db.sql`, which needs dblink: single-database layout), then the same 60 migrations whole: **60 applied, 0 failed**.
    - `users`, `documents` and `organizations` are RLS ENABLED and FORCED under 039's fail-closed `tenant_isolation`.
    - `users.id` is the primary key. `email_verified` is nullable, default false. `tenant_id` is nullable.
  - The gateway's CORE_MIGRATIONS DDL was not run. It is CREATE IF NOT EXISTS after the files, so it is a no-op for these tables.
  - Evidence: `evidence/migrate_g408{mig,comp}.out`, `init_g408comp.out`.
- **Probe** (`_work/probes/g408-realpg-probe.integration.test.ts`, findings-only; each copy was moved to `_quarantine/probe_copies` after its run; `h` has 0 porcelain lines):
  - Real parts: the documents and certifications routers, `callerEmailIsVerified`, db.ts, tenantGucContext, getRequestPrisma, and a pg connection as `secuura_app` or the superuser.
  - Stand-ins: the principal is read from a header (as the PR's own integration file does), and certificationRepo, chargeEvents and notifications are mocked.
  - **Counting users reads:** `log_statement=all` on both roles, and the server's own log is counted between SQL markers, per request. Control: a verified recipient logs exactly 1 read per path.
- **Scripts** (all in `_work/`): `run_cwd_g408.py`, `suites_g408.sh`, `an_suites_g408.py`, `integ_g408.sh`, `pgprobe/migrate_g408.sh`, `probe_run_g408.sh`, `mutants_g408.py` (my own engine; every mutant restored and sha-checked), `static_g408.py` (gate 400's, re-pointed), `lin_read_g408.py` (read-only GraphQL; the key is read into memory and never printed).
- **End state:**
  - d, h and x have 0 porcelain lines. The postgres cluster is stopped, and log_statement was reset on both roles first.
  - Local-only commits that were never pushed: the merged state 451d6312efe9 and the planted control 453c72aae9a7.

## Findings

There is no HIGH and no MEDIUM finding. On a real compose-built PostgreSQL, as `secuura_app` and as the superuser, the rule holds as ruled on all four paths:
- an unverified, NULL-flag or row-less recipient is refused;
- the SAME token is admitted on its first request after the row flips;
- a token claim never decides;
- everyone else's answers are unchanged.

### LOW
**G408-2284-1: two sentences claim slightly more than the code does. The behaviour is correct.**
1. **"So owners, platform admins, rights holders, creating connectors and ownerless documents get develop's answer with NO new query"** (PR body, line 23; facts comment b9ead05d, "How").
   - It holds for get-by-id and certify, and for a list in which every email-matching row is the caller's own.
   - **On the LIST, an owner or a rights holder still triggers ONE users read** when the tenant's page also holds a row they do not own that is addressed to their token's email. Measured on both arms: the probe's `O_owner` list showed 1 read and `O_rights_holder_list` showed 1 read, because other documents in tenant A carried their address.
   - Their own rows are listed either way; the read only decides the email-only rows. That is the design ("only when some row would be kept by the email alone", body line 23), so this is wording, not behaviour.
   - Platform admins (3 spellings), the creating connector, an ownerless get-by-id and a non-matching ORG_ADMIN: 0 reads on every path, measured.
2. **"a failing read throws to each route's existing outer catch (500)".**
   - True for the list and get-by-id.
   - The certify outer catch (certifications.ts ~984-1040) classifies errors:
     - a pool or connection failure (P2024, 53300, ECONNRESET, "Connection terminated" and so on) answers **503**;
     - a 22P02-class error answers **400**.
   - Neither is an admission, and the measured case (`REVOKE SELECT ON users`, 42501) answered 500 INTERNAL_ERROR on all four paths, with no data and the owner unaffected. The sentence just does not name the other two outcomes.

### Info (not findings)
- **The `tenant_id IS NULL` tolerance in the users read:**
  - As `secuura_app` it is dead: 039's policy compares `tenant_id::text` with the GUC, so a NULL-tenant row is never visible. Probe `Q2_null_tenant_*`: refused, 1 read.
  - On a superuser or owner connection it is live. A verified NULL-tenant row admits its owner in tenant A **and** tenant B (measured, both 200/201).
  - This is the caller's OWN row by primary key, so it does not read anyone else's mail. No current writer makes NULL-tenant users rows (039 backfilled them, and secuura_app's WITH CHECK refuses them).
  - Mutant G6 (the tolerance removed) survives every cell, unit and real-DB, on both arms.
- **A behaviour change inside the ruling (fail closed):** a connector-shaped caller (non-uuid id) whose token email equals `recipientEmail`, and which is NOT the creating connector, was admitted on develop on all three readers. It is now refused, with no query (R11 red-first; probe `Q3_other_connector…` legacy and lineage 403, 0 reads).
- **Pre-existing, untouched by this PR:**
  - An OWNERLESS document (owner_user_id and issuer_user_id NULL, which is what a connector create without onBehalfOf makes) has no 404 cloak on get-by-id. Any authenticated caller in the tenant reads it, verified or not and email or not: probe `O_ownerless_get…` 200, and another connector GETs a connector-made document with 200.
  - The list never includes the creating connector's documents.
  - Neither is this PR's subject.
- **Schema premise:** the migrations alone do not build a database originate can create documents on (see How). The seat's "built as compose builds it" is the right build. I reproduced it with docker/init + the migrations, without the gateway's CORE DDL.

## The commission's questions

- **Q1 THE RULE, real PostgreSQL 15.19, compose-built `g408comp`.** **Holds on both arms.**
  - Identity: `secuura_app` su=false, bypassrls=false. Superuser arm: su=true.
  - **The PR's three integration files** (`integ_g408.sh`):
    - **merged state: 36 of 36 on BOTH arms;**
    - **develop's product** (develop's documents.ts and certifications.ts written over the head's in x, then restored and sha-checked): **exactly I2, I4, I5, I6 red on both arms.** Each fails on an assertion (`not.toContain` received the document); ks1538 10/10 and ks1557 19/19 green.
    - **I3 reproduced:** with the recipient's row written `false` in the ks1538 and ks1557 fixtures, exactly the two "DESIGNATED RECIPIENT" controls go red, on both arms.
  - **My probe** (`evidence/probe_head_{app,super}.json`). Each tuple is list / get / legacy / lineage, then the users reads per path.

    | case | both arms |
    |---|---|
    | verified | true / 200 / 201 / 201, reads 1/1/1/1 |
    | unverified (register's values) | false / 404 / 403 / 403, reads 1/1/1/1 |
    | `email_verified` NULL | refused, same shape |
    | no users row | refused, same shape |
    | token claim `emailVerified: true` over a false row | refused |
    | flip false to true, **same token** | before: refused; after: true / 200 / 201 / 201 |
    | **lineage certify (`parentDocumentId`)** | measured on real Postgres here, not only legacy |

  - **Everyone else:**
    - owner: listed / 200 / 201 / 201, with 0 reads on get and certify (the list read is G408-2284-1);
    - system_admin, SYSTEM_ADMIN, super_admin: listed / 200 / 201 / 201, **0 reads**;
    - rights holder: listed;
    - creating connector: get 200, legacy and lineage 201, **0 reads**;
    - ownerless get: 200, **0 reads**;
    - ORG_ADMIN, not owner and email not matching: refused, **0 reads**;
    - ORG_ADMIN whose email matches: this IS the email arm, so 1 read, and refused without a verified row.

- **Q2 TENANT BINDING: measured with two tenants, A and B.** **Holds.**
  - A caller verified in A, asking for B's document sent to the same address, with the token tenant B or with the request tenant steered to B: **refused** on all four paths (its row is not in B).
  - An unverified caller in B with the same address, while A holds a verified user with that address: **refused** in B, and steered into A it is **refused** on A's document.
  - A second users row with the SAME id in another tenant: **impossible.** The insert was refused with 23505 (`users_pkey`).
  - A users row with the same email in another tenant does not make the caller verified, because the read is by the caller's id.
  - The read binds `id = $userId` AND the REQUEST's tenant, on the request's RLS-scoped connection. The unit cell R13 asserts the arguments.
  - On real Postgres:
    - M7a/b/c (the default tenant instead of the request's) fail I1 and I4 on both arms;
    - G1b (the tenant predicate dropped) fails I5 on the superuser arm and survives on `secuura_app`, because RLS is the guard there;
    - G9 (certify binds the token's tenant) survives on real Postgres, because the cells' token tenant equals the request tenant, and is killed by R13.
  - The only path to "verified" from a row outside the request's tenant is the NULL-tenant tolerance on a non-RLS connection (Info).

- **Q3 FAIL CLOSED.** **Holds.**
  - **A failing read:** `REVOKE SELECT ON users FROM secuura_app` on my cluster. List, get-by-id, legacy and lineage each answered **500 INTERNAL_ERROR**, with no documents and no `data`; the owner's get stayed 200. Certify's catch can also answer 503 or 400 by error class (G408-2284-1.2). It never admits.
  - **A non-uuid id:** no query (0 reads, from the server log), refused.
  - **Zero rows:** refused (real Postgres).
  - **"Two rows" is unreachable:** `LIMIT 1` plus `users_pkey`. Mutants G7 (`LIMIT 1` removed) and G8 (`length >= 1`) survive the unit cells and are equivalent for that reason.
  - **NULL or not-a-boolean flag:** not verified (`=== true`). G5 (truthy) survives and is equivalent, because pg returns a boolean.
  - A non-array result becomes `[]`, so not verified.
  - **No path reads an exception or a null as verified.** M8 (a throw swallowed as verified) is killed by R10.

- **Q4 THE CELLS: reproduced. No non-equivalent survivor.**
  - **Red-first** (x with develop's product, then restored and sha-checked): **51 run, 19 failed, all 19 in the new file. So 19 of 28 red; ks1538 unit 23/23 green with its fixture.** Every red fails on an assertion: 404 vs 200, 403 vs 201, the list contents, a read count of 0 for R5, R12-verified and R13, 500 vs 200 for R10. There were 0 suites with a runtime error. The 9 green are R6 ×7, R7 and R12b.
  - **Fixture-only edits confirmed by diff:** across ks1538 unit/integration and ks1557 integration there are 9 `+` lines and 1 `-` line. The only line containing "assert" is a comment; there are 0 `expect(` lines (control: ks1538 unit holds 64 `expect(`).
  - **Merged state:** 28/28 and 23/23.
  - **Mutants** (x; the ks2275 unit file plus the ks1538 unit file, 51 cells; BASE failed 0; tsc 0 for every row listed):

    | mutant | unit cells failed | real-DB kill (both arms unless noted) |
    |---|---|---|
    | M1 always verified | 19 | |
    | M2 inverted | 17 | |
    | M3 no row as verified | 4 | I5, I6 |
    | M4a claim short-circuit | 1 (R8) | |
    | M4b claim instead of row | 19 | |
    | M5a2 list ungated | 6 | |
    | M5b get ungated | 8 | |
    | M5c2 certify ungated | 6 | |
    | M6a list eager | 4 | |
    | M6b get eager | 5 | |
    | M6c certify eager (before admin/owner) | 5 | |
    | M7a/b/c default tenant | 1 each (R13) | I1, I4 (M7c also the ks1538/ks1557 recipient controls) |
    | M8 throw as verified | 1 (R10) | |
    | M9 throw as unverified | 1 (R10) | |
    | M10b uuid check removed | 2 | |
    | G1b tenant predicate dropped | 1 (R13) | I5, superuser arm only |
    | G2 list read per row | 6 | |
    | G3 list read when only own rows match | 3 | |
    | G4 get cloak skipped on an email match | 5 | |
    | G9 certify binds the token's tenant | 1 (R13) | survives |
    | G10 lineage check bypassed | 3 | |
    | **G5** truthy instead of `=== true` | **0** | equivalent |
    | **G6** NULL-tenant tolerance removed | **0** | 0, equivalent under RLS |
    | **G7** `LIMIT 1` removed | 1 (R13 text) | |
    | **G8** `length >= 1` | **0** | equivalent |

  - **Your four own-mutant shapes:**
    - the claim checked before the row = M4a (killed by R8);
    - the read moved before the admin/owner checks = M6a/b/c (killed);
    - the list read per row instead of per request = G2 (killed);
    - the cloak branch skipped = G4 (killed).
  - **Spelling notes:** my first spellings of M5a, M5c, M10 and G1 failed tsc (an unused binding, TS6133). They were re-spelled as M5a2, M5c2, M10b and G1b, which compile and are killed (`evidence/mutants_run1.out`, `mutants_run2.out`, `mutants_integ.out`, `mut/*.json`).

- **Q5 WHOLE** (develop 58bec7985343; also valid for 8389ed29, see Pins):
  - **originate jest WHOLE:**
    - develop: **3209/3209 in 244 files**; merged: **3237/3237 in 245**; 0 failed on both arms.
    - 28 names only on the merged state (the new unit file), 0 only on develop, 0 changed status.
  - **packages/shared vitest WHOLE:**
    - 1743 tests: **1742 passed and 1 failed on BOTH arms. The failing-name sets are IDENTICAL:** `wallet-signature … KS-278 accepts a valid wallet signature over the message` (Node 26).
    - 0 only on either arm, 0 changed status.
    - The seat's 1740/1741 was on bb8fd11b. KS-2317 added 2 cells.
  - **auth untouched:** all 8 paths are under `services/originate/`. 0 paths under auth, api-gateway, frontend, openapi, migrations or packages (control: 8 of 8 match originate).
  - **tsc originate:** 0 errors (planted: rc 2, 1 error).
  - **eslint:** the 8 files on the merged state: 0 messages; develop's 5: 0 (planted: rc 1).
  - **Ratchet:**
    - `check.cjs services/originate`: 341 examined, 279 under `__tests__`, 0 errors, 0 new (planted: 1 new, rc 1).
    - The standalone `test-types-ratchet.sh` exits **rc 1 on BOTH arms with identical output**: auth 2 new (`jwks.test.ts` TS2694, `ks820-821` TS2345) and api-gateway 2 new (`ks815` ×2 TS2345). This is the clone-install class gates 395-400 recorded, not the PR. The only difference between the arms is originate's examined count, 338 → 341.
    - The leg test: 43 passed, 0 failed. The seat's 48 had five real-tree cells, which KS-2322 skips when nested types are absent.
  - **Fragments:** OK (planted: FAIL). **check:openapi:** CHECK PASS; the PR has no spec change.
  - **Overlap:**
    - Of 19 other open PRs, **0 touch any of the 8 paths** (control: PR 2284's own list matches 8 of 8; package-lock appears in 11).
    - merge-tree of 2284 against PR 2274 (systemErrors, head cf24d89acb50) gives rc 0. Against PR 2276 (head now dca995028acd) it gives rc 0.
    - **Planted control:** local commit 453c72aae9a7 on 2284 rewrites the `/stats` doc-comment line PR 2274 also changes. Merged against 2274 it gives **rc 1**, CONFLICT (content) in systemErrors.ts.

- **Q6 WORDS AND DEPLOY.** **They hold, apart from G408-2284-1.**
  - **The top sentence (the deploy dependency):** present and accurate.
    - `Users.tsx:304` posts to `/api/auth/register`, and `wallet.ts:214` writes `emailVerified: false`.
    - `git grep verify-email` over `frontend/*` finds **0** (control: `auth/register` finds 2).
    - auth's routes are register, login, refresh, logout, forgot-password, reset-password, verify-email, four social and me: **no resend route.**
    - So deploying before the page closes "sent to me" documents to every unverified self-registered, wallet and dashboard-created recipient, as stated. I4 rests that consequence on a cell for the register path, and I reproduced it.
  - **Test Evidence:** honest. NOT run, Node 26 non-LTS, both ack boxes unticked, and the single-database layout are all stated.
  - **"Not claimed":** D2 (landing pages plus resend), D3 (social flags per KS-795) and D4 (reset-password on an ACTIVE row) are present. The KS-2272 claimed-invite sentence is present.
  - **Facts comment b9ead05d on KS-2275** (read-only, 3,073 B):
    - updatedAt .591Z is not after createdAt .600Z, so it is unedited;
    - every sentence I checked holds, except the same "no new query" and "500" breadth as G408-2284-1;
    - KS-2275 is In Progress, priority 2, with 1 comment.

## Two-NO-GO cap
Not engaged.

## Faults, disclosed
- **Hook refusals, none of which ran anything:**
  - two git write verbs through a variable path (re-issued through `gitx.sh` or a literal path);
  - one call with a stray `cd` (re-issued without it);
  - one `=====` zsh separator;
  - one `sleep`-then-read (replaced with an until-loop).
- **The first integration run used `g408mig`** (migrations only). Every cell failed at document create (42P10). It was diagnosed as the schema premise, and every result above comes from `g408comp`.
- **Probe bug:** my first count regex required the statement on the `execute` line, so every read count read 0 (the positive control failed). I fixed it, re-ran both arms, and every figure above comes from the fixed run.
- **`cut -c` slip:** once, I put my own ratchet-output lines through `cut -c1-160` for display. The full lines are in `evidence/ratchet_standalone_{d,h}.out` and `tmp/rs_*.txt`, and the comparison was a full `diff`. This was against the commission's `cut -c` rule; no mail was involved.
- **`gh` credentials:** one `fetch` without `GH_CONFIG_DIR` was refused by GitHub ("Repository not found"), then re-run with it.
- **Changes on my own throwaway cluster only:** `ALTER ROLE … SET log_statement='all'` (reset before the stop) and `REVOKE`/`GRANT SELECT ON users` (granted back in a finally).
- The repo's `scripts/run-migrations.sh` was not run as a script, because it writes `/tmp/migrate-err.log`. `pgprobe/migrate_g408.sh` mirrors its glob order, single-database routing and tracker.
- No mail, no `cd`, no `rm`, no container touched, no `!CODING` write, no GitHub or Linear write.

## Not run
- A booted originate or gateway, any HTTP request through the gateway, a browser.
- Any deployed or live database, any container (including w67-ks2275-pg).
- The gateway's CORE_MIGRATIONS DDL. The separate-platform-database layout. MULTI_TENANCY_ENABLED=true.
- The four platform suites. Node 24. Auth WHOLE (the service is untouched).
- A suite run on develop 8389ed29 itself (byte-identical in every service and package path; see Pins).
