# Gate verdict: Secuura PR #1536 (KS-1582, the four Minors of the PR 1534 gate), Sonnet tier 2 delta gate
Report sha256/16: 7306c470a243195b
Recipe: sha256 of this file with the single line beginning "Report sha256/16:" deleted, first 16 hex chars.

**VERDICT: GO WITH NOTE** (0 Major, 2 Minor, both coverage gaps in the PR's own cells; the code change itself behaved correctly in every probe). Bound to head `03edb5164b9a515bd91cdeffb777ccec801fe34d`. This is not a deploy recommendation.

## Head and instruments
- Head under test `03edb5164b9a515bd91cdeffb777ccec801fe34d`: `ls-remote` of refs/pull/1536/head, re-asserted after my fetch. Develop now `0026a43e60337d81c3d2549f36de0507edc128f4` (ls-remote, asserted). Parent of the head: `c855cfc2` (PR 1534's squash), merge-base with develop is `c855cfc2`.
- Code: my own `git clone --shared` of 2_Project_Files into the scratchpad, push URL DISABLED, two detached worktrees (head, and `c855cfc2`), `npm ci --ignore-scripts`, `packages/shared` built with tsc. The project folder got no git write verb (the fetch ran in my clone). `git status` there shows untracked systemTest/akto files that I did not create.
- Database: throwaway PostgreSQL 15.14 on 127.0.0.1:55447 (a first port, 55436, was already taken by someone else's postgres; I left it alone). Built from `docker/init/*` in order (`00-create-platform-db.sql` replaced by a hand CREATE DATABASE, as in the parent gate) plus `docker/init-platform/*.sql`. `scripts/run-migrations.sh`: applied=50 failed=0 (evidence/migrations.log.txt).
- Roles asserted: service runs as `secuura_app` (rolsuper f, rolbypassrls f, not a member of `secuura_auth_lookup`); `users` relrowsecurity t, relforcerowsecurity t; policies `tenant_isolation`, `users_auth_lookup`. The author's cells re-assert the role in `beforeAll`.
- Cleanup: postgres stopped, port 55447 no longer listening, no process left. Evidence has 0 hits for the app-role password (the same grep finds it in a planted control file).
- Where `dev` appears below it means `db.ts` of `c855cfc2` swapped into the head tree (byte-identical restore checked by sha256 after every swap and every mutant); the PR's tests are the same files on both sides.

## 1. Suites, with controls (FOUND / TESTED / HOW)
- **Integration, head: 3 files / 20 tests, green in 3 runs** (evidence/head_int_run1.txt, head_int_run2.txt, head_int_final.txt; also the mutant baselines).
- **Integration, dev (c855cfc2 db.ts): 2 red / 18 green, twice** (dev_int_run1.txt, dev_int_run2.txt). The two red cells are exactly **B1** (m1: the client abort `TimeoutError` at 12 s, the read hangs) and **the m2 RED cell** (`expected 'addr_test1qks1582bypassprobe...' to be null`, i.e. a tenant-B token read the tenant-A wallet under a BYPASSRLS role). The author's claim is confirmed, and both fail for the stated reason. The coverage cells are green on dev, as the author says.
- **Unit (default run), head: 7 files / 36 tests, rc 0, twice** (unit_head_run1/2.txt, unit_head_final.txt). The 3 header cells of `ks1582-header-ignored.test.ts` are killed by H1 and H2 (below), so that harness can fail.
- **tsc**: `tsc -p tsconfig.json --noEmit` rc 0 (planted TS2322 in db.ts: rc 2). With tests included (scratch tsconfig, `exclude` without `__tests__`, vitest globals types): rc 0, and a planted TS2322 in a test file is reported (rc 2). The PR body's "tsc rc 0 with tests included" is confirmed.
- **eslint** on the 5 touched files: rc 0; a planted `var` in db.ts fires `no-var` (rc 1). Confirmed.
- Control that the harness can fail at all: the dev runs above, and 18 of 22 mutants below going red (the other 4 survive; the comment-only control stays green).

## 2. m1: the timeout transaction (my own file `zz-gate1536.integration.test.ts`, evidence/*.txt; real app over HTTP, `secuura_app`, and the shared pool FORCED to one connection by `options.max = 1`)
All numbers below are wall-clock from the client; the head is on the left, dev (no timeout) on the right where I ran it.
- **T0 control (the probe can fail):** a session `SET statement_timeout` and a session `set_config(..., false)` left on the one connection are seen by the probe (`3s`, GUC `leak`), then cleared.
- **T1, two sequential reads on a pool of ONE:** both return the right wallet; after each, `statement_timeout` is `0`, the tenant GUC is `''`, the same backend pid, `pg_stat_activity.state = idle`, `xact_start` null. So the connection returns clean.
- **T2, `users` locked ACCESS EXCLUSIVE for 4 s:**
  - head: **500 after 3025 ms** (generic `INTERNAL_ERROR` body), 0 code rows, also 0 after the lock is released; the one connection afterwards is clean and idle; the next request on that same connection is 201 with the wallet in 5 ms.
  - dev: **201 after 4008 ms and 1 code row**: it just waits out the lock (this is the parent gate's F4, reproduced).
- **T3, SLOW BUT HEALTHY, lock released at 2 s:** head 201 after 2002 ms with the right wallet (no spurious 500). Boundary (T3b): released at 2.7 s gives 201 (2705 ms); released at 3.4 s gives **500 at 3006 ms, 0 rows** (dev: 201 at 3402 ms). So the bound is 3.0 s, applies to lock wait plus read together, and a read slower than 3 s fails closed with no code written. That is the behaviour the PR describes; it is a trade (a healthy-but-slow users read at the 3 s mark now fails the request) that the owner should be aware of.
- **T4, the bound is the read only:** after a read on the single connection, a plain `pg_sleep(3.5)` on the same pooled connection runs the full 3501 ms (not cut at 3 s). `SET LOCAL` does not leak.
- **T5, backend killed mid-read** (`pg_terminate_backend` at 0.8 s): 500 after 807 ms, 0 rows, and the next request on the pool is 201 with the wallet; the replacement connection is clean (`0`, `''`). Same on dev.
- **T6, `users` renamed away (error inside the transaction):** 500 generic body, 0 rows, connection clean and idle, next request 201.
- Is the transaction always ended? Read from the code and exercised: success path COMMIT; error and timeout path ROLLBACK then release; `release()` in `finally`. The timeout/error/killed-backend paths above all leave `state = idle` (T2, T6) or a replacement connection (T5).
- Mutants on this: Z5 (ROLLBACK removed) and Z6 (COMMIT removed) are killed; see section 4.

## 3. m2: `tenant_id::text = $2` with every shape of tenantId
- **Under `secuura_app`, 13 shapes x (user with a wallet, user without)** (M2 in my file): exact uuid, UPPER-CASE uuid, empty string, absent, `null`, `not-a-uuid`, `[uuid]` (array), `123`, `{a:1}`, another existing tenant B, uuid plus trailing space, `{uuid}` in braces, `' OR '1'='1`. Result on head: **every shape answers 201** (no 5xx, no cast error); only the exact uuid reads the wallet (LA); the user without a wallet stores null in all. The same table on dev is **identical row for row** (compared row by row with a script; evidence/gatelog_head_run1.txt vs gatelog_dev_run1.txt, line `GATELOG M2`). So there is no behaviour change where develop gave 201, and no wrong-tenant read.
- **Platform-scope-ish tokens** (role `super_admin`, `platform_admin`, `admin`, no tenantId): 201, wallet null on all (the read needs a tenant), same as dev.
- **Under a BYPASSRLS role** (my file `zz-gate1536-bypass...`; the role is created and dropped by the test), the user's wallet is LA:
  | shape | head | dev (c855cfc2) |
  |---|---|---|
  | exact tenant | LA | LA |
  | other tenant B | **null** | **LA** |
  | UPPER-CASE tenant | **null** | **LA** |
  | empty / absent / null | null | null |
  | `not-a-uuid` | **null** | **LA** |
  | `[uuid]` array | **null** | **LA** |
  | `123` | **null** | **LA** |
  | `' OR 1=1 --` | **null** | **LA** |
  Every status is 201 on head. The SQL binding closes the whole gap the parent gate called m2, for every shape, with no cast error. (Evidence: gatelog_byp_head.txt, gatelog_byp_dev.txt.)
- Note: an upper-case tenant never reads even under the app role; that is the RLS policy's text compare and is unchanged. Fail-closed.

## 4. Mutants, by cell name (each alone on the head; byte-identical restore checked; runner evidence/mutants.py.txt, results mutants_console.txt, mutants_b.txt, mutants_c.txt)
Baseline before every run: integration 20/20 and unit 3/3. Cells named by their title prefix; "RLS-bypass RED" is the m2 cell in `ks1582-tenant-bound-in-sql`; "unit pin" cells are in `ks1582-header-ignored`.

The author's nine, re-derived with my own anchors (all confirmed, plus the control):

| mutant | result | red cells |
|---|---|---|
| K1 m1 reverted (timeout line removed) | KILLED | B1 |
| K2 m2 reverted (tenant predicate removed) | KILLED | RLS-bypass RED |
| Y1 read for the BODY userId | KILLED | X8 |
| Y2 tenant from `x-tenant-id` first | KILLED | X9 |
| Y3 session-wide GUC (`is_local` false), same connection | KILLED | P |
| Y4 `undefined_table` swallowed to no wallet | KILLED | F1 |
| Y5 per-user cache | KILLED | X13, RLS-bypass RED |
| Y7 wallet lower-cased | KILLED | C2 |
| Y9 token `walletAddress` claim wins | KILLED | Y9, and all 3 unit-pin cells |
| C0 comment-only control | stays green | none |
| R0 `db.ts` fully reverted to c855cfc2 | KILLED | B1, RLS-bypass RED |

Mine (header, ordering, transaction discipline):

| mutant | result | red cells (PR's own cells) | my cells |
|---|---|---|---|
| H1 `linked or header` | KILLED | G3, G5, G6, G9 + unit pin "no linked wallet" | n/a |
| H2 `header or linked` | KILLED | G1, G3, G5, G6, G7, G8, G9 + 3 unit-pin cells | n/a |
| Z2 GUC applied AFTER the read | KILLED | G1, G2, G8, X9, X13, P, C2, Y9 | |
| Z5 ROLLBACK removed from the catch | KILLED | X8, X9, X13, P, C2, Y9 | |
| Z6 COMMIT removed | KILLED | G1-G6, G8, X8, X9, X13, P, C2, Y9, bypass CONTROL, RLS-bypass RED | |
| Z8 BEGIN removed | KILLED | G1, G2, G8, B1, X9, X13, P, C2, Y9 | |
| Z9 read error caught to null in db.ts | KILLED | G7, B1, F1 | |
| Z10 tenant predicate inverted (`<>`) | KILLED | G1, G2, G8, X9, X13, P, C2, Y9, bypass CONTROL, RLS-bypass RED | |
| **Z1 `SET statement_timeout` (session) BEFORE the transaction** (the brief's "timeout set outside the transaction") | **SURVIVES** | none | killed by T1, T2, T4, T5, T6 |
| **Z4 `SET statement_timeout` (not LOCAL) inside the transaction** | **SURVIVES** | none | killed by T1, T2, T4, T5, T6 |
| **Z3 timeout value 7000 instead of 3000** | **SURVIVES** | none | killed by T2, T3b |
| **Z7 `tenant_id = $2::uuid` instead of `::text`** (cast error for a non-uuid tenant) | **SURVIVES** | none | killed by M2 (a 5xx where develop gave 201) |

Plus Z1/Z3/Z4/Z7/K1/K2/Z6 re-run against my own two files (mutants_gate.txt): K1 killed by T2, T3b; K2 by the bypass file; Z1/Z4 by T1, T2, T4, T5, T6; Z3 by T2, T3b; Z6 by 8 cells; Z7 by M2; C0 stays green. So my cells can fail and the survivors are real survivors of the PR's cells, not equivalents.
Z6-like and Z5 prove the "transaction always ended" claim is pinned; the gaps are what the connection keeps AFTER the read.

**G8 (m4): does the rename describe what it asserts, and does it pass for the right reason?** Yes. The cell now says "a NON-DEFAULT tenant reads its wallet on the shared default pool" and its body seeds a user in a fresh random tenant and generates; the unused `tenants`/`tenant_config`/`platformPool` seeding is gone (diff read; tsc `noUnusedLocals` and eslint are clean). It depends on the GUC being applied to the read: Z2, Z8, Z10 (and Z6) turn G8 red, and H2 turns it red. A passing G8 therefore can fail for the reason it names.

## 5. Regressions the parent gate checked, on the head
All hold, by the PR's cells (G0-G9 ran green in 3 head runs) and my own:
- Header ignored: H1/H2 killed (G3, G5, G6, G9, plus the unit pin); body fields X8; token claim Y9; `x-tenant-id` X9.
- Null wallet for no linked wallet: G2, M2 (user without a wallet in every shape).
- 5xx on a failing read with no code row: T2, T5, T6, B1, F1, G7 (generic body, no database text). The parent's U1 array-`userId` 500 was not re-measured (the guard line in db.ts is unchanged; see NOT tested).
- uuid guard: G9, and `UUID_RE` line is untouched by the diff.

## 6. Scope and the live tip
- `git diff --stat develop...head` and `c855cfc2..head` are identical: **5 files, +453/-28**, all in `Blockchain/Dev/services/referral`: `db.ts` (**+35/-10, matches the PR body**), the G8 edit (+7/-18) in `ks1223-...integration.test.ts`, and the 3 new test files (71, 233, 107 lines). No spec, frontend, migration or config file (evidence/scope.txt, numstat.txt).
- Develop moved twice since `c855cfc2` (e4e320ba, 0026a43e): 10 files changed (`.githooks/pre-push`, `.gitignore`, CONTRIBUTING.md, one script test, originate: certifications.ts and 2 tests, systemTest: CLAUDE.md, package_format_gate.test.sh, check-package-format.sh). **0 are in `services/referral`.**
- `git merge-tree --write-tree develop head`: rc 0, **tree `3f7b33de7eddb8891ebc204252ab074ec3be51bc`**, equal to the author's prediction. That tree differs from develop in exactly this PR's 5 files, and its `services/referral` is byte-identical to the head's (`git diff` empty; evidence/mergetree_check.txt). My results at the head therefore hold for the merge.
- PR body claims (read from the author's local draft `5_Project_History/2026-10-13_seatV-6th/logs/pr_ks1582_body.filled.md`, not the live GitHub body; `gh` is not authenticated in this shell): every checkable claim matched (scope, +35/-10, 20 and 36 counts, red/green split on develop, B1 about 3 s, 9 of 9 and the comment control, tsc with tests, eslint). One claim is stronger than the cells: "Both settings are transaction-local, so the pooled connection is released clean (cell P checks the GUC)". The code is correct (T1 to T6), but cell P checks only the GUC, not `statement_timeout`. See m-a.

## Findings
**Major: none.**

**m-a (Minor, coverage): nothing pins that the timeout is transaction-local, or its value.**
- Where: `src/__tests__/ks1582-referrer-wallet-read-gate-cells.integration.test.ts`, cell P (probe at the end) and cell B1 (`expect(ms).toBeLessThan(8_000)`); code under test `services/referral/src/db.ts:210` (`SET LOCAL statement_timeout = ${WALLET_READ_TIMEOUT_MS}`; the constant is at db.ts:199).
- Reproducing shape: mutants Z1 (`SET statement_timeout = 3000` before `BEGIN`), Z4 (`SET` without `LOCAL` inside the transaction) and Z3 (value 7000) all leave the PR's 20 integration cells and 3 unit cells green. Z1/Z4 would put a permanent 3 s `statement_timeout` on a pooled connection that the referral service's other queries also use.
- Minimal fix: in P's connection probe, also read `current_setting('statement_timeout')` and assert `'0'` per distinct pid (my T1 does this; control T0 shows the probe can see a leak); and tighten B1 to a window around the bound (for example greater than 2500 ms and less than 4500 ms).

**m-b (Minor, coverage): the stated reason for `::text` (no cast error) is not pinned.**
- Where: `ks1582-tenant-bound-in-sql.integration.test.ts` (only exact and one other uuid tenant are exercised) and db.ts:212 (`tenant_id::text = $2`).
- Reproducing shape: mutant Z7, `tenant_id = $2::uuid`, passes all the PR's cells. With it, a token whose `tenantId` is not a uuid (`not-a-uuid`, an array, a number) makes generate answer 5xx for a signed-in user, where develop answers 201. The head answers 201 for all 13 shapes I tried; only the mutant does not.
- Minimal fix: add one cell of the M2 shape (a non-uuid, an array and a number tenantId under the app role must answer 201 with no wallet), or extend the bypass file's RED cell with a non-uuid tenant.

**Notes (no severity):**
- **N1, pre-existing, same on c855cfc2.** When the database kills the backend mid-read (T5; also a failover), the checked-out `pg` client emits an `error` event that nothing listens for; vitest reports `Uncaught Exception: Connection terminated unexpectedly` while the request itself correctly returns 500 and the next one works. The identical pattern exists in `queryWithTenantGuc` in `packages/shared` and runs the same on dev (evidence/gate_dev_run1.txt, gate_head_run1.txt). In production an uncaught exception exits the process per `packages/shared/src/utils/gracefulShutdown.ts`. Not introduced or worsened by this PR (a statement timeout is an ordinary query error, not a connection error). Fix would be a `client.on('error', ...)` while checked out, in shared code, out of this PR's scope.
- **N2.** A read slower than 3 s now fails the request closed (T3b: released at 3.4 s gives 500, dev gives 201). That is the intended trade; the bound is a product decision for the owner.
- **N3.** B1 takes about 12 s on a red run and about 3 s on a green one; fine.
- Carried from the parent gate and not changed here: U1 array `userId` gives 500, X10, W1, C1/C2, and KS-1055 per-tenant-database note.

## NOT tested
- Any deployed stack, pgbouncer itself, the gateway, the e2e specs, the four platform suites, the Schemathesis/Akto pre-merge suites (the PR leaves their boxes unticked on purpose).
- The live GitHub PR body (read the author's local draft instead).
- The parent gate's U1 (array `userId` 500) was not re-measured; the line it concerns is untouched.
- A real auth-minted token: tokens are signed with a test RS256 key against the real shared `authenticate()`, as in the author's rig.
- A pool larger than one under the lock cases (the pool of one was the stricter condition; the default pool of 10 was used by the author's P cell and the mutants).

## Evidence (evidence/)
- Suites: head_int_run1/2, head_int_final, dev_int_run1/2, unit_head_run1/2, unit_head_final, tsc_*, eslint_*.
- My cells and runs: zz-gate1536.integration.test.ts.txt, zz-gate1536-bypass.integration.test.ts.txt, gate_head_run1/2, gate_dev_run1, gate_byp_head/dev, gatelog_head_run1/2, gatelog_dev_run1, gatelog_byp_head/dev.
- Mutants: mutants_console.txt, mutants_b.txt, mutants_c.txt, mutants_gate.txt, mutants*_console.txt, mutants.py.txt, mutants_gate.py.txt.
- Scope: scope.txt, numstat.txt, mergetree_check.txt, db_ts.diff. Rig: pgsetup.sh.txt, migrations.log.txt, integ.sh.txt, unit.sh.txt, npmci.log, build_shared.log.

Merge only on Wednesday's GO bound to head 03edb516. No deploy recommendation is made.
