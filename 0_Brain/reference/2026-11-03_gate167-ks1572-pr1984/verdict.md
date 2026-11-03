GO WITH NOTES — HOLD-FOR-KAM (payout path: no non-caller binds a referee and no refusal writes, but whether the caller's 25 SECURA is paid now follows the caller's LINKED wallet, not the body's wallet — measured both ways, cells 19/20)

# QA Gate 167 (Tier 1, round 1): PR 1984 / KS-1572 referral apply takes the referee from the token, never from the body

**Payout first (the brief's rule).** The amounts are unchanged: 25,000,000 base units (25 SECURA) to the referee, written once, at base and head alike. What changes is **whether** it is paid in one case: the wallet-collision fraud check now compares the referrer's wallet to the caller's **linked** wallet instead of a wallet the client typed. Measured on the real service and a real PostgreSQL:
- cell 20: a caller whose linked wallet IS the referrer's wallet, with no wallet in the body. Base paid 25 SECURA (PENDING). Head pays 0 (INVALID, WALLET_COLLISION).
- cell 19: a caller who types the referrer's wallet into the body. Base paid 0 (flagged). Head pays 25 (their real linked wallet differs).
Cell 19 is not a loosening. At base the same caller got 25 by leaving the field out (cell 18). Across every caller class I drove, head pays a subset of what base could be made to pay. The condition is written because this is the payout path. Wednesday rules on it.

## Subject
- PR 1984, head `68897dda941066459fcec2e34f667f07d46f9d8d`, parent (base) `1e6df0b6bf71844151cac575f7c33600fff3e249`. One commit, 4 files.
- ls-remote at the start (02:54:16Z): pull/1984/head = `68897dda9410…`, develop = `27fe5476526c…`. At the end (03:10:55Z): **the same two values**. The head did not move.
- merge-tree --write-tree develop `27fe5476` + head, run in my own clone: **rc 0**, tree `9930500f992bd2f8c3ef5561abb8aeca335faef9`. Merge-base `1e6df0b6`. Develop has 2 commits since the base (09884b0e6 auth, 27fe54765 security) touching 14 paths. **Paths shared with the PR: 0** (control: develop's paths against themselves = 14). services/referral in the merged tree = head's (`9f7e6868c282`). packages/shared is the same at all three (`edf16d9a69c6`). So every head measurement below holds for the merged result.
- Host: Node v26.8.1 (not an LTS line; Node 24 not run). vitest from the repo lockfile. tsc from the repo. PostgreSQL 15-alpine (container `g167-pg`, now stopped and removed). node_modules cloned (cp -c) from gate 163's clone. Lockfile, package.jsons and the packages/shared tree have the same blob ids at gate163, the PR head and develop.

**Method.** `scripts/g167.cjs` boots the **real** `services/referral/src/index.ts` once at base and once at head, with tsx. That boot includes helmet, boundedJson, rejectNulBytes, `app.use('/api', authenticate())` from @secuura/shared, the real routes, services, error handler and logger, and real `pg`. It runs against a real PostgreSQL with these pieces:
- the repo's own referral DDL (extracted from `docker/init/04-sprint2-service-tables.sql`, identical to gate 163's);
- a minimal `users` table with FORCE RLS on `app.current_tenant_id`;
- AFTER-row triggers on all 7 tables, writing to an admin-owned log;
- `log_statement=all` for the app role, bracketed per cell.

Each principal is a real RS256 JWT. Each of the 27 cells per version does a TRUNCATE plus seed and sends one request. It then measures the status, referral rows, reward rows, the code's uses, fraud-log rows, row writes, app SQL statements and the service's own log lines.

The PR's 23 cells and the whole suite ran at base and head. Q5 used a route-level cell built on the real applyCode and the real fraud service. 14 mutants of mine ran against both the PR file and the real-stack matrix. Results: `results/` (tracked). Raw logs: `logs/` (ignored by the vault's `0_Brain/reference/*/logs/` rule).

## Findings

### G167-F1 — INFO (payout, for Kam's plain answer): the wallet-collision decision now uses the caller's linked wallet, so who gets the 25 SECURA changes in two measured cases
- **FOUND**: head passes `walletAddress = getLinkedWalletAddress(caller, tenantId)` to applyCode, where base passed `body.walletAddress`. `fraudDetection.ts:172-185` (WALLET_COLLISION, weight 80, enough to fail) is the only fraud check that changes a decision here.
  - Cell 20 (linked wallet = the referrer's): base 201, 25 SECURA, PENDING. Head 201, **0 SECURA**, INVALID, plus a fraud-log row.
  - Cell 19 (body wallet = the referrer's): base 201, 0 SECURA. Head 201, **25 SECURA**.
  - The referral row's `referred_wallet_address` is now the linked wallet (addr_X), not the body value. For a caller with no linked wallet it is NULL (cell 21).
  - The PR text says "No fraud DECISION changes". That holds for ip/device. It does not hold for the wallet: the wallet now decides in the other direction, correctly.
- **TESTED**: cells 17-24 on the real stack, base vs head. NOT tested: production users' linked-wallet coverage, i.e. how many real referees have no linked wallet (for them the wallet check is skipped, exactly as at base when the body omitted the wallet).
- **HOW**: `logs/probe/{base,head}.json`, `results/matrix_table.txt` rows 17-24. Control: cell 17 (own id) 201 with 3 writes at both. Mutant M10 (body wallet restored) changes 8 of these cells, so the matrix can see the wallet source.

### G167-F2 — LOW (the stated consequence, confirmed): ip/device are no longer recorded or counted; what is lost is forensic, not a fraud decision
- **FOUND**:
  - **The fraud log.** A flagged application's `svc_referral_fraud_log` row now holds ip = NULL and device = NULL. Base wrote the body's values: cell 19 at base logged `203.0.113.7` / `dev-from-body`, and cells 20 and 22 at head logged NULL/NULL.
  - **The in-memory counters.** They are no longer fed: Q5 route cells, 6 applies with the same body ip and device, gave base `trackedIps 1, trackedDevices 1` and head `0, 0`.
  - **No pass/fail decision is lost.** The counters and the ip/device collision checks (`fraudDetection.ts:144`, `:159`) only run when `referrerIp` / `referrerDeviceId` are set, and **no code sets them**. A repo grep found only the type (`referral.types.ts:190,192`) and the two readers. Measured: 6 applies from one ip and one device at base, past `maxReferralsPerIp 3` and `maxReferralsPerDevice 2`, all `fraudCheckPassed: true`.
  - **The base values were not trustworthy either.** They were client-typed, or `req.ip`, which with no `trust proxy` in referral's index.ts is the hop address.
  - **Disposable email moves.** The flag now comes from the token's email claim instead of the body (cells 22/23). Its weight of 15 is below the pass threshold of 30, so payout is unchanged both ways.
- **TESTED**: real-stack cells 19-23 for the log columns; route-level Q5 for the counters. NOT tested: restart behaviour (loadFromDb rebuilds the counters from fraud-log ip/device, which will now be NULL; same conclusion, not driven).
- **HOW**: `results/q5_{base,head}.txt`; `scripts/g167-q5-fraud-signal.test.ts`. Its control asserts the real checkFraud ran 6 times. It was copied into each tree for the run and then quarantined to `scratch/_quarantine/`.

### G167-F3 — LOW: a token with no `tenantId` claim skips the wallet read, so the wallet-collision check is skipped for that caller
- **FOUND**: cell 24 (own id, token without tenantId): head 201, 25 SECURA, no wallet, 5 statements (no wallet read). `getLinkedWalletAddress` returns null when tenantId is missing (`db.ts:216`). This is no more permissive than base: at base any caller skipped the check by omitting the body wallet (cell 18).
- **TESTED**: real stack, one cell. NOT tested: whether the auth service ever issues a token without tenantId.
- **HOW**: matrix row 24.

### G167-F4 — LOW (not run): the Schemathesis baseline and precondition entries for `POST /api/referrals/apply` will see different statuses
- **FOUND (read only)**:
  - `schemathesis-baseline.json:338` (positive_data_acceptance, KS-591) and `:463` (status_code_conformance, KS-565) baseline this op.
  - `tests/support/state_machine_preconditions.py:103` classifies it by "referral code must be valid".
  - At head, a fuzzed body whose userId is not the token's user gets 403 before the code is looked up.
  - The baseline entries may need re-triage. This is not a defect in the PR. 403 is declared for the path (`referral.openapi.ts:529`, read, not driven).
- **TESTED**: read only. **HOW**: git grep at head.

## What passed (measured)
- **Q1 (no non-caller binds a referee).** Every non-caller cell refuses with 0 rows written and 0 SQL statements at head (real stack, real authenticate, real error handler). At base the same cells were 201 with 3 writes. The non-caller cells:
  - body userId = victim → **403** (base 201, 25 SECURA to V);
  - token userId missing (sub only), "", numeric, array → **403**;
  - SYSTEM_ADMIN or SUPER_ADMIN naming V → **403** (no platform path);
  - body userId = caller upper-cased → **403**; token userId upper-cased → **403**;
  - path `/API/Referrals/Apply` and trailing slash → **403** (same handler);
  - forged `x-user-id`/`x-user-role` headers → **403**;
  - token without tenant naming V → **403**.

  The other cells:
  - Space-padded id (both sides) → **400** (KS-444 parse first). Bad body with a victim id → **400**.
  - No Authorization header → **401** from `authenticate()` before the route. The route-level "no principal → 403" is proven only in the PR's harness (cell ii), 23/23.
  - Own id with no ip/device → **201**. applyCode receives exactly `code, userId, email, walletAddress` (PR cell v).
  - Wallet read failure (users SELECT revoked) → **500 INTERNAL_ERROR**, nothing applied. The real error handler logged `INTERNAL_ERROR: permission denied for table users` at error level; the client got the generic envelope.
  - Self-referral → 400 at both.

  Nothing reaches applyCode before the check: `/apply` is a single handler behind `app.use('/api', authenticate())`, and the case and slash variants hit the same check.
- **Q2 (refusals write nothing).** All 16 head 403/400 cells: 0 row writes, 0 app statements. 401: 0/0. 500: **0 writes, 4 statements**. Those are the wallet read's own transaction: BEGIN, the tenant GUC and the timeout set, then the failed SELECT. They are reads, by design. The PR cells assert 0 applyCode calls and 0 wallet reads on every 403/400. Positive control: the 201 cells show 3 writes.
- **Q3 (other callers of applyCode).** **1 caller** repo-wide, at head and develop: `routes/referrals.ts:169` (develop `:145`). The definition `referralService.ts:447` was found by the same case-insensitive fixed-string grep (the positive control). There were 0 dynamic forms (`['applyCode']`, `.call/.apply/.bind`). The only direct INSERTs into svc_referrals or svc_referral_rewards are in referralService.ts. The e2e fixture `recruitment-data.ts:311` defines the path, but `referral.apply` has 0 uses (control: the e2e tree has 82 `API_ENDPOINTS`/`referral.leaderboard` matches).
- **Q4 (the 201 path).** Real PostgreSQL. Own id at head: **exactly the three rows gate 163 measured, for the caller only**: `svc_referrals INSERT 1` (PENDING), `svc_referral_codes UPDATE 1` (uses 0→1) and `svc_referral_rewards INSERT 1` (caller, REFERRAL_BONUS, 25000000). The same three at base. Head sends 10 statements against base's 5; the extra 5 are the wallet-read transaction. Amount unchanged. See F1 for the two cells where whether it is paid differs.
- **Q5.** Confirmed. See F2.
- **Q6 (red first).**
  - PR file: at base **18 of 23 fail by AssertionError** (201 or 400 where 403/500 was expected, body values where the linked or token values were expected, 0 calls where 1 was expected). The 5 that pass at base are preservation controls: the harness probe, the padded 400 ×2, the order 400 and KS-444's 400. Head: **23/23**.
  - Whole referral suite: base **13 files / 102 of 102**, head **14 / 125 of 125** (+23). G153-F8 was not hit; no re-run needed.
  - tsc: service `--noEmit` 0 errors at base and head. With tests included at head, 0 errors, and the program contains the new test file (`--listFilesOnly`). Control: a planted type error was reported (rc 2, 1 error).
  - eslint: 0 problems on `routes/referrals.ts` and the new test at head, and on the full src at base and head. Control: a planted unused variable was reported as a warning.
  - These agree with the author's numbers.
- **Q7 (mutants).** 14 mine. Raw table counted (`results/mutants.json`): **12 killed by the PR file** (by assertion), **10 by my real-stack matrix**, **12 by either, 2 survivors, both equivalent**:
  - M9 (applyCode gets `body.userId`) is equivalent because it is proved `=== caller` just above.
  - M13 (wallet read uses `body.userId`) is equivalent for the same reason.

  Every mutant the brief names is killed:
  - owner check removed: PR 4 fail, matrix 9;
  - case-insensitive compare: PR 1, matrix 2;
  - check moved after applyCode: PR 4, matrix 9 (writes then 403);
  - body ip passed through: PR 1, matrix 2;
  - wallet read failure swallowed: PR 1, matrix 1.

  Also killed: principal check removed (PR 5), empty-string principal (PR 1), platform bypass (PR 2, matrix 2), body wallet restored (PR 2, matrix 8), body email restored (PR 2, matrix 2), wallet failure to the route's 400 catch (PR 1, matrix 1), 403→401 (PR 4, matrix 9). The matrix alone misses M6/M7, because real authenticate answers 401 before the route and I had no empty-principal-plus-bad-body cell; the PR file kills both. The blob was restored and re-hashed after every mutant.
- **Q8.** rc 0, tree `9930500f…`, 0 shared paths (above).

## NOT tested
- The full migration chain. `users` was a minimal table with FORCE RLS on the shared GUC, not the repo's migrated schema with its real policies.
- The api-gateway hop and real client-IP forwarding. JWKS (static `JWT_PUBLIC_KEY` only). Real tokens from the auth service: whether any lacks `tenantId` or `email`.
- Production data: how many referees have no linked wallet (F1/F3).
- Fraud-counter rebuild on restart (`loadFromDb`) after this change (read, not driven).
- The Schemathesis sweep (F4), CI, Node 24, the e2e suites.
- Concurrency (two applies racing for one caller or one code).
- `/qualify` and the payout of the referrer's 50 SECURA downstream of an applied referral (gate 163's scope).
- The fragment pair (HTML) was read, not rendered.
- The merged tree was not booted. Its referral and shared trees are byte-identical to head's, so it was not re-driven.

## Plain answer for Kam
Before this change, anyone signed in could sign someone else up under any referrer's code, and that person got a 25 SECURA welcome bonus without ever logging in. With it, a referral code can only be applied to the person who is signed in. Admins have no way around that, and every refused attempt changes nothing in the database. I checked this against the running service and a real database. The bonus amount is unchanged. One thing changes on payout: the "same wallet as the referrer" fraud check now uses the wallet actually linked to the person's account, not one they type in. So someone whose own wallet is the referrer's no longer gets the 25, which is the point of the check. We also stop recording the visitor's IP and device on flagged referrals. Those were values the client typed and never decided anything, so no protection is lost.
