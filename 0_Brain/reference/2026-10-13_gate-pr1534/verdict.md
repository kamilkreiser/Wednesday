# Gate verdict: Secuura PR #1534 (KS-1223 (a), the referrer wallet comes from the user's linked wallet, not the x-wallet-address header), Opus tier 1
Report sha256/16: 19608e1f74ed846b
Recipe: sha256 of this file with the single line beginning "Report sha256/16:" deleted, first 16 hex chars.

**VERDICT: GO WITH NOTE** (0 Major, 4 Minor). Bound to head 884a24ebc3b7cc80fb33c861fb11e41957481ea7. This is not a deploy recommendation.

## Head and instruments
- Head under test: `884a24ebc3b7cc80fb33c861fb11e41957481ea7`. I checked it with `ls-remote` of refs/pull/1534/head and asserted it after the fetch. Its parents: the author's `70208d33`, plus a merge of develop `7550a969`.
- Develop now: `343a7b4e2fdf81a1c69e7a2749573be108b63d1d` (ls-remote).
  - Its commit is "KS-695 ask 3 (ii): erase-connector erases in one transaction", including a "Round 6" section. It touches 11 files: originate, the spec, and one test in the ks764 guard. I did not confirm the PR number (the brief guessed 1497).
  - `git merge-tree --write-tree develop head` is clean (rc 0, tree `7b3b94f7`).
  - The merged tree differs from the head only by develop's 11 files. 0 of them are in `services/referral`, and none touch runtime code in `packages/`. My results at the head therefore hold for the merge (evidence/mergetree_vs_head.txt).
- Code: my own `git clone --shared` of 2_Project_Files into the scratchpad, with the push URL set to DISABLED. I ran `npm ci --ignore-scripts` and built `packages/shared` with tsc. The project folder was not written to, and no git write verb ran there.
- Database: a throwaway PostgreSQL 15.14 on 127.0.0.1:55413.
  - Built from `docker/init/*` in order. `00-create-platform-db.sql` was replaced by a hand `CREATE DATABASE`, because it uses dblink and needs a socket.
  - `docker/init-platform/01-platform-schema.sql` was applied to `secuura_platform`, as compose mounts it.
  - `scripts/run-migrations.sh`: applied=50 failed=0 (evidence/migrations.log.txt).
- Roles, re-asserted inside every gate file:
  - The service runs as `secuura_app`: rolsuper f, rolbypassrls f, and not a member of `secuura_auth_lookup`.
  - `users` has relrowsecurity t and relforcerowsecurity t. Its policies are `tenant_isolation` (fail-closed, text compare of `tenant_id`) and `users_auth_lookup` (only for `secuura_auth_lookup`).
- Postgres is stopped, port 55413 is no longer listening, and no stray vitest or postgres processes remain. The evidence folder has 0 hits for the app-role password (the same grep finds it in a planted control file).

## 1. The author's 10 cells, unit, tsc, eslint (FOUND / TESTED / HOW)
- **Head: 10/10 in 4 runs** (evidence/head_run1-3.txt, head_final.txt).
- **Develop: 8 red / 2 green in 3 identical runs** (evidence/dev_run1-3.txt). For this run, develop's `routes/referrals.ts` and `db.ts` were put into the same tree, with the same test file and database.
  - Green: G0 and G4.
  - Red: G1, G2, G3, G5, G6, G7, G8, G9. They fail for the right reason: G1, G3, G5, G6, G8 and G9 stored the header value; G2 stored null; G7 answered 201.
  - The author's "8 red / 2 green" is confirmed.
- Controls the harness can fail: the develop run itself, plus 18 of the 19 mutants in section 7 going red. The comment-only control stays green.
- Referral unit suite at the head: 6 files / 33 tests, rc 0. At develop: 7 files / 35 passed among the unit files. That matches the author's arithmetic: the deleted file had 1 file and 2 tests.
- tsc:
  - `tsc -p tsconfig.json --noEmit`: rc 0. A planted TS2322 in db.ts is caught (rc 2).
  - A tsconfig that includes tests and the vitest configs: rc 0.
- eslint: rc 0 on db.ts, referrals.ts and the new test, and rc 0 on all of `services/referral/src`. A planted `var` fires `no-var` (rc 1). Both vitest configs are ignored by the repo's own pattern.
- Scope:
  - `git diff --stat develop...head` = 7 files, all in `services/referral` (+316/-47).
  - Against `70208d33`, the diff in `services/referral` is empty (0 lines). The head's other change versus 70208d33 is only the KS-1553 merge (security: 2 files).
  - No spec, frontend, gateway, migration or config change. That matches the PR body.

## 2. Cross-tenant (gate file zz-gate1534, 27 cells, 3 green runs at the head; 14 of them red on develop)
All cells ran as `secuura_app` against the real app with a header `x-wallet-address: HDR` where it matters. The stored value was read back as the superuser.

| cell | shape | head | develop |
|---|---|---|---|
| X1 | token tenant = another EXISTING tenant (B, row in `tenants`) for a tenant-A user | 201, null | HDR stored |
| X2 | token tenant = non-existent uuid | 201, null | HDR |
| X3 | tenantId `not-a-uuid` | 201, null (no error: policy compares text) | null |
| X4 | right tenant UPPER-CASED | 201, null (fail-closed) | null |
| X5 / X6 | tenantId array `[TA]` / 123 / object / true | 201, null each | null |
| X7 | role super_admin, no tenantId | 201, null | HDR |
| X8 | body `{userId: <victim with wallet>, walletAddress, ownerWalletAddress}` | 201, null (zod strips them) | null |
| X9 | right token + `x-tenant-id: B`; then a no-tenant token + `x-tenant-id: A` | LA, then null | null, null |
| X10 | user row status `deleted` / `suspended`, token still valid | wallet stored for both | null |
| X11 | user row with tenant_id NULL | 201, null | null |
| X12 | two users sharing one wallet, and a third with none | LA, LA, null | |
| X13 | link LA, clear the wallet, relink LB (same token) | LA, null, LB (no stale read) | |
| connector `userId` (G9 / U1) | | 201, null | |

- No shape made a code store another user's wallet or another tenant's wallet.
- The `userId` is the signed claim. The body and headers cannot change it (X8, X9).

## 3. RLS reality and GUC on pooled connections
- G0 is true. As `secuura_app`, a bare SELECT returns 0 rows; with `set_config(...,true)` inside a transaction it returns the row.
  - Mutants M3, M4 and Y8, which read without the right GUC, go red on G1, G2 and G8 and on the gate cells. So the cells catch the silent NULL.
- `queryWithTenantGuc` runs BEGIN, set_config(local), the query and COMMIT on ONE client, and rolls back on error.
- **P0**: a fresh pooled connection has `app.current_tenant_id` = ''.
- **P1 (pool max 1)**: 24 interleaved requests: A users, B users, A users with B tokens, and B users with no tenant. 0 wrong wallets. Peak clients 1. The one connection afterwards has GUC ''.
- **P2 (pool max 2)**: the same 24 requests, 0 wrong, peak 2. Both connections are GUC-free afterwards (I probed them concurrently with pg_sleep, so the two distinct pids are proven).
- **F2**: after a failed read (SELECT revoked), the pooled connections carry no GUC (3 probes: '').
- Mutant Y3 (session-wide `set_config(..., false)` on one pooled connection, query on another) is killed by P0, P1 and P2. So the leak test can fail.

## 4. Failure modes
- **F1 users table missing (renamed)**: 500 with a generic `INTERNAL_ERROR` body (no database message), and 0 new code rows. Develop: 201 and 1 row.
- **F2 SELECT revoked**: 500 and 0 rows. Develop: 201.
- **F3 DB refuses the app role** (NOLOGIN plus its backends terminated): 500 and 0 rows. `isDbAvailable()` stays true. Develop: 201 with 0 rows (the code was never persisted; `dbSaveReferralCode` swallows the error, which is older than this PR).
- **F4 users locked** (ACCESS EXCLUSIVE held by another session): **generate hangs.** The client gave up at 8.0 s. After the lock was released, the code row WAS written, with LA, even though the client had gone. Develop answers 201 at once, because it never reads users. See Minor m1.
- **D1 degraded (no DB)** (separate file; DATABASE_URL points at a closed port): `isDbAvailable` false, generate answers 201, and the helper returns null with 0 `pool.connect` calls. This is the early return the author left uncovered. It now has a test, and it behaves as described. Nothing is persisted in degraded mode; that is older than this PR.
- **UUID guard (U1)**:
  - Upper-case uuid: wallet read (201, LA). PostgreSQL uuid input ignores case; `owner_id` is stored as sent, which is older than this PR.
  - `{uuid}`, uuid with a trailing newline, `urn:uuid:`, a number: 201, null.
  - Empty string: 401.
  - **An array `[uuid]`: 500.** `UUID_RE.test([x])` coerces the array to a string and passes, and pg sends `{"..."}`, which fails the uuid cast. No minter produces this shape (auth `jwt.ts` and the gateway mint string userIds), so it is a note, not a finding.
- **Wallet values (W1)**: `''` gives null (`|| null`). `'   '` is stored as is (length 3). A 255-character value is stored as is (users.wallet_address is varchar(255); owner_wallet_address is text). A whitespace wallet can only come from auth's write paths, which check CIP-8 signatures. Note.
- **M10, shown with an RLS-bypassing role** (gate file zz-gate1534-bypass; the app connects as the superuser):
  - Head: no-tenant token gives null (B1). Wrong tenant gives **LA** (B2). Right tenant gives LA (B3).
  - With M10 (the `!tenantId` guard removed), B1 turns red: LA is read with no tenant at all.
  - So the guard is what keeps a tenant-less token from reading under a bypass role. Under `secuura_app` the mutant is equivalent (the author's cells and my 27 cells stay green), as declared.
  - B2 shows the second half: the SQL carries no tenant predicate, so tenant binding rests entirely on the role being non-bypass. See Minor m2.

## 5. The header
- `git grep -i x-wallet` over all tracked files at the head. The only runtime consumer left is the gateway's forward (`api-gateway/src/routes/verification.ts:1383`), which is out of scope (KS-1573).
- No service reads the header: originate, which that forward reaches, has 0 hits.
- Referral has 0 reads in any route, `/apply` included. The one hit there is a comment at referrals.ts:64.
- The remaining hits are the gateway's KS-1041/KS-1223 characterisation tests and one e2e spec that sends the header.
- The principal's `walletAddress` claim is no longer read either. No minter signs one (`auth/services/jwt.ts`: no wallet claim; connector tokens carry `userId: connector:<id>`).

## 6. Behaviour that must not change
- **S1**: an email user with no wallet gets 201. The envelope is `{success, data}`, and `data` keys are exactly id, code, shareUrl, createdAt, expiresAt, maxUses, customLabel. Stored wallet: null. Develop passes the same cell.
- The spec: `secuura-api.yaml` (`/api/referrals/generate`) and `referral.openapi.ts` declare no wallet header and already declare 500. No spec change is needed.
- The only in-repo caller, `frontend/issuer/.../ReferralDashboard.tsx:155`, sends body `{}` and no wallet header (confirmed).
- **E1**: a legacy code row stored with `addr_legacy_header_value` is unchanged after its owner generates a new code. `/apply` with that wallet still flags it (fraudCheckPassed false). The same holds on develop.
- **WALLET_COLLISION, measured through the real `/apply`:**
  - C1, referrer linked lower-case (the form wallet login stores):
    - same wallet: flagged (passed false);
    - different wallet: not flagged (true);
    - **the same wallet UPPER-CASED: not flagged (true).**
  - C2, referrer linked in mixed case (`/link` stores as sent):
    - exact value: flagged;
    - **lower-cased: not flagged.**
  - The case mismatch is real both ways. It is not this PR's defect: the referred wallet is client-asserted, so a referred user can evade the flag with any value. That is `/apply`'s problem (KS-1572). Wednesday ruled "no canonicalisation", and mutant Y7 (lower-casing) is killed by C2, so the cells hold that ruling.
  - C3, the old attack: a header-chosen referrer wallet no longer steers the flag. Stored null; on develop HDR was stored and the flag fired.

## 7. Mutants (each alone on the head; byte-identical restore checked after each; evidence/mutants.txt, mutants_y9.txt)
Runner: evidence/mutants.py.txt. Each mutant runs the author's file, my 27-cell file, and (for M3, M10 and C0) the bypass file. Before the mutants, the baseline was 10/10, 27/27 and 3/3 green.

The author's eight, re-derived with my own anchors:

| mutant | result | author's cells red | gate cells red |
|---|---|---|---|
| M1 linked \|\| header | KILLED | G3, G5, G6, G9 | X1, X2, X7, C3 |
| M2 header \|\| linked | KILLED | G1, G3, G5, G6, G7, G9, G8 | X1, X2, X7, F1, F3, C3 |
| M3 plain pool.query | KILLED | G1, G2, G8 | X9, X12, X13, P1, P2, C1, C2 |
| M4 constant default-tenant GUC | KILLED | G1, G2, G8 | the same 7 as M3 |
| M5 runWithPlatformScope | KILLED | G5 | X1, X2, X3, X5, X6, X11, P1, P2 |
| M6 caught to null | KILLED | G7 | F1, F2, F3 |
| M6b to the route's 400 catch-all | KILLED | G7 | F1, F2, F3 |
| M9 uuid guard removed | KILLED | G9 | none |
| M10 `!tenantId` guard removed | KILLED only under the bypass role | none | none; bypass cell B1 is red |

The author's "8 of 8 killed, M10 survives" is confirmed.

Mine:

| mutant | result | author's cells red | gate cells red |
|---|---|---|---|
| Y1 wallet read for the BODY userId | KILLED | **none** | X8 |
| Y2 tenant from the `x-tenant-id` header first | KILLED | **none** | X9 |
| Y3 session-wide GUC on a different pooled connection | KILLED | **none** | P0, P1, P2 |
| Y4 error swallowed only for undefined_table | KILLED | **none** | F1 |
| Y5 wallet cached per user (stale after unlink) | KILLED | **none** | X13 |
| Y6 header used when the token has no tenant | KILLED | G6 | X7 |
| Y7 wallet lower-cased (ruled out) | KILLED | **none** | C2 |
| Y8 query run before set_config (outside the transaction) | KILLED | G1, G2, G8 | the same 7 as M3 |
| **Y9 a `walletAddress` claim on the token wins** (the deleted mock test's CONTROL shape) | **SURVIVES everything** | none | none |
| C0 comment-only control | stays green, as expected | none | none |

About Y9: it is harmless while no minter signs a wallet claim (verified), but nothing pins "a token claim is ignored".

**6 of my 9 mutants (Y1, Y2, Y3, Y4, Y5, Y7) survive the author's 10 cells.** They die only on my cells. See m3.

## 8. Do the cells pin what they claim?
- **G0**: yes. It is a real rig control: the app role sees 0 rows without the GUC (also proven by M3, M4 and Y8 being killed).
- **G8**: it passes for a reason other than the one it states. I re-ran the author's file with G8's `tenants` and `tenant_config` inserts removed (evidence/zz-g8control.integration.test.ts.txt, g8_control.txt), and it is still 10/10. The referral code never consults `tenant_config`; it uses the default pool. So G8 is G2 with a fresh tenant id and pins nothing about the demo shape. See m4.
- **The deleted mock test** asserted two things:
  - the header fallback, now deliberately reversed and pinned by G3, X1, X2, X7 and C3;
  - a principal `walletAddress` winning over the header.
  - Nothing now covers the second (Y9 survives). It was also the **only KS-1223 pin in the default `npm test` run**. After this PR, the default run has none, because `vitest.config.ts` excludes `*.integration.test.ts`. This matches the repo's existing pattern: security and auth have the same split, and `ci.yml` is `workflow_dispatch` only.

## Findings
**Major: none.**

**m1 (Minor): the users read has no time bound, so code generation now hangs whenever `users` is locked.**
- Where: `services/referral/src/db.ts:191-196` (`getLinkedWalletAddress`). `getPool()` (db.ts:28-32) sets no `statement_timeout`.
- Reproducing shape: another session runs `LOCK TABLE users IN ACCESS EXCLUSIVE MODE` (for example a migration's `ALTER TABLE users`). `POST /api/referrals/generate` then never answers; the client gave up at 8 s. On release the row is written anyway, after the client has left. Develop: 201 at once (F4).
- Minimal fix: bound the read, for example `SET LOCAL statement_timeout = '3s'` in the transaction (a `queryWithTenantGuc` variant), or `statement_timeout` / `query_timeout` on this pool. On timeout the route already answers 500 with no row (F1-F3 path).

**m2 (Minor, defence in depth): the read binds the tenant only through RLS, not in its SQL.**
- Where: `db.ts:194`, `'SELECT wallet_address FROM users WHERE id = $1 LIMIT 1'`.
- Reproducing shape: under any RLS-bypassing role, a token whose `tenantId` names tenant B still reads the tenant-A row (B2 gives LA).
- Exposure today: none found. Compose connects referral as `secuura_app`, and the row read is always the caller's own (signed `userId`), so it cannot be another user's wallet.
- Minimal fix: `... WHERE id = $1 AND tenant_id::text = $2 LIMIT 1` with `[userId, tenantId]`. The text compare matches the policy and avoids a cast error on a non-uuid tenantId. That also makes M10 non-equivalent.

**m3 (Minor, coverage): the PR's own cells miss six plausible regressions, and the default run loses its only KS-1223 pin.**
- Where: `src/__tests__/ks1223-referrer-wallet-from-the-user-row.integration.test.ts`.
- Reproducing shape: mutants Y1 (body userId), Y2 (header tenant), Y3 (GUC on another connection / leak), Y4 (one error class swallowed), Y5 (stale cache) and Y7 (case canonicalisation) all leave the author's 10 cells green. Y9 survives everything.
- Minimal fix:
  - adopt equivalents of gate cells X8, X9, X13, P1/P2 (pool max 1, interleaved tenants, GUC '' afterwards), F1 and C2;
  - optionally keep a cheap default-run unit pin that the header is ignored.

**m4 (Minor, honesty of a cell): G8 "the DEMO shape" does not test the demo shape.**
- Where: the same file, cell G8.
- Reproducing shape: remove its `tenants` / `tenant_config` inserts and it still passes (control run). The code never reads `tenant_config`.
- Minimal fix: rename it to what it pins ("a non-default tenant reads its wallet on the shared default pool"), or drop the platform-row seeding.

**Notes (no severity):**
- U1: an array userId gives 500, a shape no minter produces.
- X10: deleted or suspended user rows still supply their wallet; token validity is the gate.
- W1: a whitespace wallet is stored as is.
- C1/C2: case mismatch on the collision flag, the client-asserted referred side (KS-1572).
- If `PROVISION_PER_TENANT_DB` were ever enabled, this read would return a silent null for tenants whose users live elsewhere (declared by the author; KS-1055).
- F3 is an improvement: a dead DB is now a 500 instead of a 201 for a code that was never stored.

## NOT tested
- Any deployed stack, pgbouncer itself (the transaction bundling is single-client and should be safe in transaction mode; I did not run pgbouncer), the gateway, and the e2e specs.
- The four platform suites and the Schemathesis/Akto pre-merge suites.
- A real auth-minted token: tokens were signed with a test RS256 key against the real shared `authenticate()`, as in the author's rig.
- A statement or connection timeout on the read beyond the lock hang (F4).
- The PR body: I read the author's local draft (`5_Project_History/2026-10-13_seatV-6th/logs/pr_ks1223_body.filled.md`), not the live GitHub body. Its checkable claims (scope, counts, mutants, 500 path, frontend caller, no spec change) matched what I measured, except that G8's "demo shape" is overstated (m4).

## Evidence (evidence/)
- The author's cells: head_run1-3, head_final, dev_run1-3.
- My 27 cells: gate_head_run1-3, gate_dev_run1.
- The bypass role and the degraded mode: bypass_head, bypass_dev, degraded_head.
- G8 control: g8_control.
- Unit, tsc, eslint and their planted controls: unit_head, unit_develop, tsc_*, eslint_*.
- Mutants: mutants, mutants_y9, mutants_console.
- Scope: diffstat_vs_develop, diffstat_vs_70208d33, mergetree_vs_head.
- Rig: migrations.log, and the gate test files plus scripts saved as `.txt`.

Merge only on Wednesday's GO bound to head 884a24eb. No deploy recommendation is made.
