# Gate verdict: PR #1539 (KS-1570 PR B, the platform-only route that writes an ADMIN's organisation scope), Opus tier 1
Report sha256/16: 91e8da4021c40661 (recipe: delete this one line from the file, then sha256 of the remaining bytes, first 16 hex chars)

**Head under test:** `61c30de56f53695cd343af4a0cece151a1649e16`. My own `ls-remote` of `refs/pull/1539/head` gave the same SHA. Live develop is still `a7cffc8d9831e67d91f6dd24d0047ffe3e26c97e` (`results/lsremote.txt`).

**VERDICT: NO GO** for this head, on one finding.

**M1 (Major, in the diff, one-line fix):** two concurrent PUTs for the same ADMIN leave the UNION of their sets. The audit trail then says something different from the stored state. I reproduced it 3/3, and a one-line lock turns my cell green.

Everything else I attacked holds:
- **Who can call:** platform-only, and a tenant ADMIN cannot widen its own scope.
- **Atomicity:** holds under six injected faults and a killed connection.
- **GUC:** the tenant GUC is per transaction, and the write never runs under a platform bypass.
- **Keys:** no key is revoked or altered.
- **Spec:** regenerates byte-identical.
- **Mutants:** the author's 9 are all killed, and 13 of my 14 are killed.
- **Author's numbers:** all reproduce.

Once M1 is fixed, I expect GO WITH NOTE (the minors below). Re-gating needs only the M1 delta plus my cell E. This PR ships only in the one round with PR A, KS-1564 and KS-1584. **I do not recommend deploying anything.**

Gate: an independent Opus seat, 2026-10-13 AEDT. Read-only on the project:
- `git clone --shared` into the scratchpad, push URL `DISABLED`.
- Write verbs ran in that clone only. No GitHub or Linear writes, no remote boxes.

Database: a throwaway PG15 on 127.0.0.1:55413, TCP only. It is **stopped**, and port 55413 is not listening (checked with `lsof`). Ports 55416, 55418 and 55436 were never touched.

Raw outputs are under `evidence/results/`, the cells under `evidence/gatetests/`, and the tools under `evidence/tools/`.

## Findings

| id | severity | where | what | minimal fix |
|---|---|---|---|---|
| **M1** | **Major** (in the diff) | `services/security/src/index.ts:1588-1607` (the PUT's transaction: SELECT prev, DELETE, INSERT, audit; no lock) | **A concurrent replace is a union, and the audit row's `after` is not the stored state.** See "M1 details" below the table. | Serialise writers per (tenant, user) inside the transaction, right after `applyTenantGuc`. Use `SELECT pg_advisory_xact_lock(hashtext($1), hashtext($2))` with `[tenantId, userId]`, or `SELECT … FROM users WHERE id=$1 FOR UPDATE`. KS-1549 already serialises concurrent rotates per connector in the same way. **Measured control:** with exactly that advisory-lock line applied in my scratch tree, cell E goes green (final `[A3]`, audit chain `[A1]→[A2]`, then `[A2]→[A3]`). The author's 13 cells stay 13/13 (`results/gateE_fixcontrol.txt`, `author_with_fix.txt`). Add cell E (`gatetests/gate1539-e-race.integration.test.ts`) as the regression test. |
| m1 | Minor | `index.ts:1611-1614` (catch → `next(error)` → `errorHandler`) | **An infrastructure fault answers a generic 500 `INTERNAL_ERROR`, not a retryable 503.** With the backend killed mid-transaction, PUT gives **500**. The same kill on develop's mint path gives **503**, because KS-888's classifier handles it (`results/gateC_dev.txt`). Fail-closed holds either way: nothing is written. This is the same shape as PR A's m1. | Run the transaction error through the KS-888 SQLSTATE 08/53/57 and socket classifier, and answer 503 `SERVICE_UNAVAILABLE`. |
| m2 | Minor | `index.ts:1543-1546` (the target check) | **No status check on the target.** A user with `role='ADMIN'` and `status='deleted'` can be given a scope (200, row written). Role change or deletion also does not purge existing rows; PR A's m3 raised this, and it is still open. Harmless while the user cannot log in, but the scope revives silently if the account is reactivated or re-promoted. | Add `AND status = 'active'` (or the repo's canonical liveness test), or decide explicitly that it is accepted. Track the purge-on-demotion question as a card. |
| m3 | Minor (pre-existing, outside the diff) | `services/security/src/db.ts:59-72` `transaction()` and `queryWithTenantGuc` (checked-out pg clients with no `'error'` listener) | **A backend killed under a checked-out client raises an UNCAUGHT `Connection terminated unexpectedly`.** In production this exits the process (`gracefulShutdown.ts:24`: "uncaughtException … always exits"). Measured on head through the new route (B6), and on **develop through the ordinary mint path** (`results/gateC_dev.txt`: same uncaught error, 1 of 1). So PR B adds a caller but does not introduce the class. | A separate ticket: attach an `'error'` listener to clients while they are checked out (or `release(err)` to destroy them). |
| n1 | Nit | `index.ts:1514` | The comment says "see auditInsertStatement", but the function is `systemAuditInsertStatement`. | Rename the reference. |
| n2 | Nit | `index.ts:122-135` (comment) + PR body "Why the audit row uses its own INSERT" | KS-1586 has a **third** cause the author does not list: `dbSaveAuditLog` callers build `id: 'audit_<uuid>'`, and `audit_logs.id` is `uuid`. As `secuura_app`, that insert fails on its own even without the two missing columns: "column id is of type uuid but expression is of type text" (`results/ks1586_psql.txt` step 2). | Add it to KS-1586 so that ticket's fix is complete. |
| n3 | Nit | `docs/openapi/secuura-api.yaml` (GET operation) | The GET declares 404, but the route never produces one. It answers 200 `[]` for an unknown user or a non-ADMIN (measured: ISSUER_ADMIN target gives 200 `[]`). | Drop the 404 from the GET, or document the 200 `[]`. |
| n4 | Nit (pre-existing, shared) | `packages/shared/src/security/keyRevokePolicy.ts:139-140` `isPlatformRole` (and `requireKeyAdmin`'s `toUpperCase`) | `String(role).toUpperCase()` admits `super_admın` (dotless i), `ſuper_admin` (long s) and a role **array** `["SUPER_ADMIN"]` as SUPER_ADMIN. Measured: PUT 200 and mint 201 for all three. This is reachable only by a token the auth service signs with such a role. **I did not test whether any issuer or user-management path can store or sign one.** | Compare against an exact ASCII-folded string, and reject non-string roles. |

**M1 details.** The setup: scope `{A1}`.
1. Request X sends `PUT [A2]` and is held for 1.5 s inside its transaction, after its DELETE and INSERT.
2. Request Y sends `PUT [A3]` 300 ms later.
3. Y's DELETE waits for X's row lock. Under READ COMMITTED it then re-checks, finds A1 gone, and **cannot see X's newly inserted A2**. It inserts A3.

Measured, 3 runs out of 3 (`results/gateE_ledger_{1,2,3}.json`):
- Both requests answer **200**. Y commits last.
- The **stored scope is `{A2, A3}`**.
- The last audit row says `before [A1] → after [A3]`. No audit row records A2 and A3 together.

So the ADMIN keeps an organisation that the last committed "replace" removed, and the audit trail contradicts the authorisation state. Only platform operators can trigger it, and two writes for the same ADMIN must overlap within one transaction. Two concurrent writes on the same PK instead give a 23505 → 500 (atomic, harmless).

**Why I call M1 Major rather than Minor:** this route exists to make an authorisation grant exact and audited. M1 can produce a grant **wider than any request asked for**, silently, with an audit row that misstates the result. It is in the diff, and the fix is one statement. If Wednesday rates it Minor, the head is otherwise GO WITH NOTE.

## What I measured (instrument and control for every number)

**1. Head, ancestry, merge** (`results/scope_hygiene.txt`):
- `merge-base --is-ancestor` confirms develop `a7cffc8d` is an ancestor of the head. PR A `2cdf1d7a` is also an ancestor.
- Chain `5aebd19b → acac8e5e (merge 06d0109c) → d24fe065 → 61c30de5 (merge a7cffc8d)`, exactly as the author describes.
- `git merge-tree --write-tree a7cffc8d 61c30de5` gives `6a37f961…`, which equals the head's own tree (develop is already merged in).
- **No evil merges.** I recomputed each merge commit's auto-merge tree from its two parents:
  - `61c30de5` gives `6a37f961…`, identical;
  - `acac8e5e` gives `cd7c0904…`, identical.
- The PR's own non-merge commits touch exactly 4 files. `diff --stat a7cffc8d..head` shows 4 files, +684, −0. From `2cdf1d7a`, the stat is 17 files; the other 13 are develop's own KS-1564/KS-1009/KS-1582 files, which arrived through the merges.

**2. The author's 13 cells, 3 runs each** (`results/author_head_{1,2,3}.txt`, `author_dev_{1,2,3}.txt`). Real PG15 built from `docker/init/*` + `run-migrations.sh`: rc 0, an explicit `[main] Applying 049_admin_organisation_scopes.sql...`, applied=51 failed=0 (`results/pgsetup_head.txt`). The service ran as `secuura_app`: rolsuper f, rolbypassrls f, FORCE RLS on `admin_organisation_scopes`, `audit_logs`, `users` and `organizations` (`results/catalogue.txt`).
- **Head:** 13/13, three runs out of three.
- **Develop with the cell file copied in:** **13/13 red**, three runs out of three, each for the right reason (the route is absent, so the expected 200/400/403/5xx come back as 404).
- **Config refusal:** with `TEST_DATABASE_URL` and `TEST_APP_DATABASE_URL` unset, rc 1. The suite fails in `beforeAll` naming both variables, and the cells are skipped, not passed (`results/author_head_noenv.txt`).
- The 13 cells, by name:
  1. a platform PUT sets the scope (200), the rows are written, and one audit row records it
  2. a PUT in tenant T leaves the same user's scope rows in another tenant alone
  3. end to end with PR A: the ADMIN may mint for A1, not for A3
  4. PUT replaces the set; before and after are reported
  5. duplicates and case variants collapse
  6. an empty list clears the scope
  7. the GET returns the set, to a platform role only
  8. an ADMIN cannot widen its own scope
  9. ISSUER_ADMIN and a provisioning connector get 403
  10. a non-ADMIN target is 404
  11. an organisation of another tenant is 400
  12. non-uuid ids and a missing tenantId are 400
  13. a failed audit insert gives 5xx and leaves the scope unchanged

**3. My cells A: 64 cells, real HTTP** (`gatetests/gate1539-a-route.integration.test.ts`). Head: **64/64, three runs out of three**. Develop: **54 red / 10 green**. The 10 green on develop are the seven 401s and the API-key 401 (authentication runs before routing), the observe-only cell, and the KS-1586 reproduction, which is the same on develop as intended (`results/gateA_dev.txt`). Every status is in `results/gateA_ledger_head_*.json`.
- **Item 2, who can call PUT.** The guard reads only `req.user.role` from the RS256-verified JWT (`index.ts:994-1003`, `isPlatformRole` = `toUpperCase()` ∈ {SYSTEM_ADMIN, SUPER_ADMIN}). There is no header or body read, and I found no `trust proxy`.
  - 200: `super_admin`, `SUPER_ADMIN`, `SYSTEM_ADMIN`, `system_admin`, `Super_Admin`, and a platform token with no tenantId and no userId.
  - 403, with nothing written and nothing audited (whole-table count unchanged):
    - **`ADMIN`, `admin` and `Admin` of the same tenant setting their OWN scope**;
    - ADMIN of T2, ORG_ADMIN, ISSUER_ADMIN, a provisioning connector (`organizations:register` + `*`), USER, no role, and ADMIN with no tenantId or userId;
    - `' SUPER_ADMIN'`, `'SUPER_ADMIN '`, `'SUPER_ADMIN\t'`, SUPER_ADMIN+ZWSP, `SUPER-ADMIN`, `PLATFORM_ADMIN`;
    - ADMIN plus headers `x-user-role`/`x-role`/`x-platform-admin`, and ADMIN plus body `role`/`user.role` set to SUPER_ADMIN.
  - 401: no token; no token plus `x-user-role: SUPER_ADMIN` and `x-tenant-id`; a malformed token; `alg:none`; a token signed by another key; an expired token; Basic auth; an `sk_` API key as bearer; the same key as `x-api-key`.
  - Unicode and array role probes: see n4.
- **Item 3, the write.**
  - set, add, remove, empty, duplicates `[A1,A1,A1]`, and upper-case or mixed duplicates all give 200, with canonical lower-case rows. Each response's `before` equals the previous set, and each audit row's before/after matches.
  - Every one of these spellings gives **400 with nothing written or audited**: braces, padded, NBSP-padded, tab, `urn:uuid:`, no hyphens, Kelvin sign, a fullwidth digit, `default-org`, `''`, a null element, a number, and the nil uuid (accepted by zod, then refused as not an organisation of the tenant).
  - 1001 ids, a string, null and a missing list: 400. 1000 unknown ids: 400.
  - An organisation of T2: 400, with `unknownOrganizationIds: [B1]`.
  - tenantId in upper case: 200, stored lower-case (`tenant_id::text` = T). Braces: 400. An unknown tenant: 404.
  - Targets: ISSUER_ADMIN, ORG_ADMIN, ADMIN of T2, no such user, and role `' ADMIN '` all give **404**. Role `admin` gives 200. An upper-case userId in the path gives 200, stored lower-case.
  - **Where the tenant comes from:** only `body.tenantId`, lower-cased. The target comes from the path. `granted_by` comes from the token's userId, then sub, then role. Body extras (`userId`, `grantedBy`, `granted_by`, `role`, `tenant_id`) are ignored; the stored row is `{u: U, t: T, granted_by: PLATFORM_ID}`.
  - `x-tenant-id: T2` with body T writes to T only. A platform token carrying `tenantId: T2` also writes to T: platform roles act cross-tenant by design, and no non-platform caller reaches this code.
- **Item 3b, write side vs read side (real mint).** With the scope written as `A1` in upper case, an ADMIN mint naming A1 gives 201 for exact, upper, padded and NBSP spellings, and 403 for braces and for A2. The write side does not call `normaliseOrgId`; it uses zod uuid plus `toLowerCase`, and Postgres `::uuid` canonicalises. It stores only canonical ids. The read side applies trim+lower to the request. So **they agree on every spelling the write accepts**, and the write is stricter (it refuses padded spellings) without disagreeing. ks780's exact count is unaffected: shared `keyRevokePolicy` is untouched, and `normaliseOrgId(` appears in `security/index.ts` 6 times on both develop and head.
- **Item 5, the audit row.**
  - `tenant_id` = T, `user_id` = the platform caller's uuid, `resource_id` = the target, `resource_type` = `admin_organisation_scope`.
  - `details` = `{tenantId, targetUserId, before, after, grantedBy}`, exactly.
  - `x-forwarded-for` and `x-real-ip` set to `6.6.6.6` do not reach `ip_address`. `user_agent` is the caller's UA header (normal). No `sk_` material in the row.
  - A body `grantedBy` and a body `details` are ignored.
  - A non-uuid userId gives `user_id` NULL with `grantedBy` = that string. A sub-only caller gives `grantedBy` = the sub.
  - `audit_logs.user_id` has no FK, so a platform user absent from the tenant's `users` table does not break the insert.
- **Item 6, the GET.**
  - Same role matrix: 200 for all 6 platform shapes, and every DENY row gives the same 403 or 401 as for PUT.
  - It returns only `{userId, tenantId, organizationIds}`, no user data, and only the named tenant's rows: a T2 row for the same user appears only with `?tenantId=T2`.
  - A missing tenantId, or a repeated one, gives 400.
  - **No cap:** 1500 rows seeded directly all come back, `ORDER BY organization_id::text` ascending. The PUT caps a write at 1000, but nothing caps the read.
- **Item 7, no revoke.**
  - Setup: scope {A1}. K1 = an ADMIN mint for A1, K2 = a platform mint for A1, K3 = an unqualified ADMIN mint. All 201.
  - After `PUT []`, an md5 over the `svc_api_keys` rows' (id, is_active, org, tenant, expires, hash, scopes, connector) is **identical**, with 3 active.
  - `POST /api/keys/validate` for K1 gives `valid: true`. The platform list for A1 shows K1 and K2, both active.
  - Then, at the real routes (PR A default deny): an ADMIN mint naming A1 gives **403**, an unqualified ADMIN mint gives **201**, and an ADMIN revoke of K1 gives **403**, with K1 unchanged. A platform revoke of K2 gives 200 (control that the revoke route works).
  - Harness note: my first draft hashed whole rows, and the post-validate hash differed only because validate bumps `usage_count`/`last_used_at`. The snapshot taken right after emptying (s1) was identical. I narrowed the hash to exclude those two columns.

**4. Atomicity, cells B** (`gatetests/gate1539-b-atomic.integration.test.ts`): 8/8 at pool sizes 10, 1 and 2. Pool size came from my scratch-only `GATE_POOL_MAX` patch to `db.ts`; `db.ts` was restored, sha256 identical before and after (`results/db_ts_sha_*.txt`).
- Each fault is injected as the superuser and removed in a `finally`. Each gives **500 `INTERNAL_ERROR`, rows unchanged, audit delta 0, and the next PUT 200**:
  - B1: REVOKE INSERT on `audit_logs`.
  - B2: `audit_logs` renamed away.
  - B3: a CHECK constraint refusing the row.
  - B4: a deferred constraint trigger failing **at COMMIT**, after the audit insert succeeded.
  - B5: REVOKE INSERT on `admin_organisation_scopes` (the scope write fails before the audit).
  - B5b: REVOKE DELETE.
- **B6:** `pg_terminate_backend` while the audit insert sleeps gives 500. Nothing is left behind, and 4 follow-up PUTs give 200. It also raises the uncaught exception in m3; the develop control is cell C.
- **B7:** interleaved PUTs for T (held 1.5 s in its transaction) and T2.
  - Both 200; each set lands in its own tenant, with nothing cross-tenant.
  - Pool 1: T2 is answered after 1510 ms, so it waited for the connection.
  - Pools 2 and 10: answered after 235 ms, so it ran concurrently.
  - `current_setting('app.current_tenant_id')` read through the service's own pool afterwards is `''` six times out of six.
  - **Instrument control:** at pool 1, a session-level `set_config(…, false)` through the same pool IS read back (`gate-leak-control`), so a GUC left behind would be seen.
- **Bypass, by statement log** (`log_statement=all` for `secuura_app` only, reset afterwards; parser `tools/gucparse2.py`; `results/gucparse.txt`). Over the author's cells, cells A and cell D, every statement touching the table ran with GUC = the statement's own tenant parameter and **no bypass**:
  - SELECT scopes ×79, DELETE ×54, INSERT ×51;
  - audit INSERT ×54.
  - **Positive control:** the parser counted 3 bypass `set_config` lines: cell D's platform mint without a tenantId (the reviewed `runWithPlatformScope` lookup at `index.ts:1165`), plus 2 from the pre-existing revoke key lookup.
- **One connection:** all statements in a PUT run on `transaction()`'s single client, with `applyTenantGuc` right after BEGIN (statement log, one pid per transaction).

**5. KS-1586** (`results/ks1586_psql.txt`; cell A "KS-1586 reproduction").
- At the real route, on **both develop and head**, `POST /api/audit` answers **201 and persists 0 rows** (count before and after, superuser).
- As `secuura_app`, `dbSaveAuditLog`'s statement fails for three separate reasons:
  - `column "previous_state" … does not exist`;
  - the `audit_<uuid>` id into a `uuid` column (n2);
  - `v1:…` encrypted details into `jsonb`: `invalid input syntax for type json`.
- `secuura_app` cannot widen the column: `must be owner of table audit_logs`.
- **Control:** PR B's shape (uuid id, plain JSON) inserts as `secuura_app` (`INSERT 0 1`, rolled back). The new route's rows persist in every cell, counted by the superuser.
- So the author's claim holds: KS-1586 is pre-existing, and **the new INSERT is correct on a repo-built database**.

**6. Tenancy modes.** With `MULTI_TENANCY_ENABLED=true` and `PLATFORM_DATABASE_URL` set (a second database built by the same init):
- the author's cells plus cells A give 77/77;
- security integration gives 5 files / 73.

"falling back to single-tenant" appears **0** times in the output. Control: the string exists in `services/originate/src/db.ts` (1 hit). `initTenantManager` has no caller in security outside `db.ts`, so the flag is inert for this service (code read).

**7. The author's other numbers, re-measured on the head:**
- security integration **5 files / 73**, in both modes;
- security unit **31 / 336**;
- shared unit **51 / 980**;
- `tsc --noEmit` (security) rc 0;
- eslint `--max-warnings=0` on the 3 changed `.ts` files: rc 0.

Controls: a planted file gives tsc 1 error and eslint rc 1 (`no-var`), and was removed afterwards. **All match.** I did not re-run the author's tsc-with-tests scratch config, or the 12 spec-reading files in auth and api-gateway.

**8. The spec.**
- `npm run check:openapi`: rc 0 (`CHECK PASS`, 414 example blocks resolve).
- Control: appending one byte to the YAML makes `--check` fail (`CHECK FAIL`, rc 1); restored with `git checkout` in the scratch clone.
- **I regenerated it myself:** `generate-openapi` writes a YAML whose sha256 `b2a43ae4…` equals the committed head file's, and the scratch clone's `git status` is clean.
- **KS-1009 survived:** `diff a7cffc8d..head` on the YAML is **+207 / −0**, so every develop line, including KS-1009's 4 added lines, is present unchanged.
- The new operations declare `security: [{bearerAuth: []}]`. OpenAPI cannot express "platform role"; the summaries say "platform roles only" and 403 is declared, which matches the guard. The GET declares a 404 it never produces (n3).
- **Platform suites (NOT RUN, by me or by the author):**
  - Schemathesis would fuzz both operations, but needs a **platform-role** token to get past 403 into the 200/400/404 paths.
  - Akto's BFLA/BOLA checks (a tenant ADMIN calling PUT, cross-tenant GET) are the relevant authorisation suite.
  - Playwright does not apply (no UI). k6 adds nothing material for an operator-only route.
  - Preflight legs 3/4/8 (spec-auth, path resolvability through the gateway, served spec) are the ones this spec change needs. By code read only: the gateway proxies `/api/security/*` → `/api/*` with `authenticateToken(true)` (`api-gateway/src/routes/proxy.ts:1189-1191`), so `/api/security/keys/admin-scopes/{userId}` resolves to the new route.

**9. Mutants** (`tools/mutants1539.py`; `results/mutants_run.txt`, `results/mutants.json`, per-suite JSON in `results/mut/`). Method:
- Baseline green first: author 13, A 64, B 8.
- Each mutant is applied alone to `index.ts` (each anchor must occur exactly once).
- After every mutant, `index.ts` is restored from a byte snapshot, and sha256 is identical every time.
- Red cells are recorded by suite and name; per-cell lists are in `mutants_run.txt`.

Results:
- **Author's 9, re-derived verbatim from `mutants_ks1570b_v7.py`: 9/9 KILLED.**
  - P1 (gate removed): author ×3, plus 25 A cells (every DENY 403 row, GET roles).
  - P2: author "non-ADMIN target 404", plus A "targets" and "deleted-status".
  - P3: author foreign-org cell, plus A "foreign org" and "nil uuid".
  - P4: author atomicity cell, plus B1, B2, B3 and B6.
  - P5: author ×5, plus A write/agree/norevoke.
  - P6: author dup cell, plus A "write sequence" (`dup`).
  - P7: author "other tenant's rows alone".
  - P8: author GET cell, plus A "GET roles".
  - P10: author audit cell, plus A "audit row".
- **Mine:**
  - G1 (tenant from the `x-tenant-id` header): KILLED (A "x-tenant-id header T2 …").
  - G2 (PUT behind `requireKeyAdmin`, admitting a tenant ADMIN): KILLED (author "ADMIN cannot widen", A DENY ADMIN/admin/Admin/ORG_ADMIN/ISSUER_ADMIN/T2 rows).
  - G3 (audit outside the transaction, errors not swallowed): KILLED (author atomicity, B1–B4, B6).
  - G4 (role compared case-sensitively): KILLED (A ALLOW `super_admin`/`system_admin`/`Super_Admin`, author cells).
  - G5 (organisation ids not lower-cased on write): KILLED (author dup/case, A write sequence and agree).
  - G6 (scope removal revokes keys): KILLED (A "removing a scope revokes nothing").
  - **G7 (target check without the tenant filter): SURVIVED.** It is equivalent at the behaviour level: under the tenant GUC, FORCE RLS on `users` still hides T2's ADMIN, so it still returns 404. RLS is doing the bounding. No cell can see the missing WHERE except a statement-text pin.
  - G8 (organisation check under bypass, no tenant filter): KILLED (author and A foreign-org).
  - G9 (audit tenant from the caller's token): KILLED (A "platform token carrying tenantId T2 still writes T": the audit insert fails WITH CHECK).
  - G10 (GET under bypass without the tenant filter): KILLED (A GET tenant cell).
  - G11 (granted_by from the body): KILLED (A extras, audit row).
  - G12 (transaction without the tenant GUC): KILLED (author and A, everywhere).
  - G13 (failed transaction answered 200): KILLED (author atomicity, B1–B6).
  - G14 (target role compared case-sensitively): KILLED (A targets: `admin` user).
- **C0, a comment-only control: nothing red.**
- **Totals: author 9/9; gate 13 killed, 1 survived (equivalent); 0 LOADFAIL.**

## Grants and run-as (for the deploy seat)

The route runs as the service's `DATABASE_URL` role (`secuura_app`), under the target tenant's GUC, with no platform bypass (measured, item 4). **PR B needs more than PR A's SELECT:**
- `SELECT, INSERT, DELETE` on `admin_organisation_scopes`;
- `INSERT` on `audit_logs`;
- `SELECT` on `users` and `organizations`.

It needs **no UPDATE** (no UPDATE statement). On a repo-built database, default privileges grant all four on all four tables (`results/catalogue.txt`).

**Measured:** with INSERT or DELETE on the scope table revoked, or INSERT on `audit_logs` revoked, the route answers 500 and writes nothing (B1, B5, B5b). So a missing grant fails closed, but it **disables the route**.

## PR body vs code
- **The four required statements:**
  - legs 3/4/8 NOT RUN, and the four platform suites NOT RUN: present;
  - KS-1586 named, and stated as not fixed: present;
  - "This PR revokes no keys", with the reasoning (minter unrecoverable; ops step on Kam's word): present, and **measured true**;
  - the GET is platform-only: present. The body states the platform-only rule for both routes, and the "why" is given for the route as a whole ("no ADMIN can widen its own scope"), not separately for the GET.
- **Body details that differ from the code:**
  - "details `{tenantId, before, after}`": the code also writes `targetUserId` and `grantedBy`. This is a superset and harmless.
- **Could be mistaken for done:**
  - "PUT replaces the set" is true for serial calls only (M1).
  - The deploy note mentions only SELECT; PR B needs INSERT/DELETE too (above).
- **The author's two disclosures, carried forward as the author's measurements; I did not reproduce them:**
  - preflight "INCOMPLETE — 13/16 legs ran, 3 SKIPPED (3, 4, 8, local stack not up)", which is NOT a pass;
  - one leg-14 arm SKIPPED ("historical red-proofs — commit d602a1536 not present"), and a suite count of 87, not 86.
- **Linear:** not read and not written.

## NOT tested (plainly)
- **Not run by me, and not run by the author:**
  - preflight legs 3/4/8;
  - Schemathesis, Akto, Playwright, k6;
  - the gateway in front of the service: no gateway process, no CSRF or content-type path, no served spec;
  - any live or remote environment.
- **Pushes and preflight:** I did not run the pre-push preflight or any leg-14 arm, and did not reproduce the d602a1536 measurement.
- **Author checks I did not re-run:**
  - the tsc-with-tests config;
  - the 12 spec-reading test files in auth and api-gateway;
  - `packages/shared` tsc.
- **Not probed:**
  - whether any issuer can sign a role like `ſuper_admin` or an array role (n4);
  - the gateway's own handling of PUT to `/api/security`, beyond reading the code;
  - in-memory `memAuditLogs` exposure through `GET /api/audit`.
- **M1's fix:** I measured only the advisory-lock variant, not the `FOR UPDATE` variant.
- **Deviation from the brief's init:** `00-create-platform-db.sql` (dblink) was skipped and the platform database was created by hand. Every other `docker/init` file ran in order with rc 0.
- **Scratch database state when stopped:** it held 1 scope row and 1 `audit_logs` row from a cell whose fixture user was already deleted. All gate users and triggers were gone. The database was throwaway and has been stopped.
