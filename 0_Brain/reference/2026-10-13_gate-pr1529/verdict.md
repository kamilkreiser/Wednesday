# Gate verdict: Secuura Platform K PR #1529 (KS-1556, P2): delta on the #1527 gate's m1 and m2

**VERDICT: GO WITH NOTE.** Majors: 0. Minors: 2 (n1, n2). Observations: 3.
**Report sha256/16:** `bfd834130503059c`. This is the sha256 of this file with this field set to the literal `SHA16_PLACEHOLDER`, truncated to 16 hex characters.

Both fixes do what they claim, and I reproduced the author's red/green with my own instruments.

- **m1:** the claimed case is fixed.
- **m2:** the pin really is the first statement. It holds under REPEATABLE READ and under SERIALIZABLE, on the grace path and on the KS-577 path.

**The new Minor, n1, is introduced by this PR.** The m1 fix makes the undo restore by id. So when a legitimate operator revoke lands in the same window, the undo overwrites it:
- **One fault** (the rotate's COMMIT fails): memory and the key list say a DB-revoked key is active. Validate still refuses it.
- **Two faults** (the revoke's save also fails): the revoked key **validates `true`** in this process. This breaks KS-888 R2 in the fail-open direction.

It needs coincident faults inside a millisecond window, and the operator is told the revoke failed. That is why it is a Minor and not a Major. It is still a regression on a credential path, and the fix owner should see it before merge.

## Head and trees under test
- **Head:** `c3b66f7f312d45b5e90f2e77c847160da4fe3192`.
  - Bundle `ks1556-c3b66f7f312d.bundle`: sha256/16 `cbd728111e79e1df`, which matches the brief. `list-heads` gives c3b66f7f.
  - Its parent `af2366e7` was not in the local repo, so I fetched `refs/pull/1529/head` and `develop` read-only from GitHub into my scratch clone. I used the project's deploy key; nothing was pushed.
  - `ls-remote`: develop = `5d5aea41fecaba0dcadcbd240fa0c4196b32dc49`, pull/1529/head = `c3b66f7f…`. Both match the brief.
- **Scope:**
  - `git diff --stat af2366e7..c3b66f7f` gives exactly 3 files, +218/-5: `index.ts`, the KS-1549 integration file, and the new `ks1556-rotate-under-repeatable-read.integration.test.ts`.
  - `af2366e7..5d5aea41` touches 7 files, all under `scripts/`. The overlap with the PR's files is **0**.
  - `git merge-tree --write-tree 5d5aea41 c3b66f7f` gave rc 0 and a clean tree, `93edf7b5`.
- **Develop runs:** worktree at `5d5aea41`, with the PR's two test files (and my harness) copied in. That tree's `index.ts` differs from the head's only by the PR's 19-line hunk.
- **Database:** my own PostgreSQL **15.14** on 127.0.0.1:**55421**, with the unix socket off.
  - Built with `initdb -U secuura --auth=trust`, then `docker/init/*` in order with a throwaway `APP_DB_PASSWORD`.
  - The dblink step failed (role lookup), as in #1527, so I created `secuura_platform` by hand.
  - `run-migrations.sh` gave **applied=50 failed=0** (`_secuura_migrations` count 50).
  - `svc_api_keys` has `relrowsecurity=t`, `relforcerowsecurity=t`. `secuura_app` has `rolsuper=f`, `rolbypassrls=f`. The service ran as `secuura_app` in every cell.
  - Postgres was stopped at the end (`pg_ctl stop`, port 55421 closed). No gate triggers or rows were left before the stop: I checked with a query.
- **Limits respected:** nothing was written to the project folder, nothing was pushed, there were no GitHub or Linear writes, and I contacted no remote box. The throwaway app password was scanned for across `evidence/`: 0 hits.

## Numbers (instrument / control)

| # | What | Head | Develop | Instrument | Control that could fail independently |
|---|---|---|---|---|---|
| 1 | Author's 13 cells (KS-1549 file incl. E9 and its control, plus the m2 file) | **13/13 green, 4 of 4 runs** | **3 red / 10 green, 3 of 3 runs**: E9; m2 double-submit (9, 10, 9 of 10 trials with 2 active); m2 N=20 (16, 16, 15 of 20 retires null). `could not serialize` = 25, 26, 24 | vitest integration config, app role (`int_head_1..4`, `int_dev_1..3`) | The E9 control (no validate) is green on both trees. The m2 CONTROL (pool really RR) is green on both. Head `could not serialize` = 0 in all 4 runs. The author's 9/10, 16/20 and 25 reproduce. |
| 2 | Postgres semantics behind the pin | A late `SET TRANSACTION` **to a different level** errors: `must be called before any query`. Setting **the level already held** is a silent no-op. A first-statement pin then `COMMIT` leaves the next transaction at the session default (no leak). | — | psql against PG15.14 under all three defaults (`pg_settx_probe.txt`) | Each default is shown both refusing a change and accepting the same level. This confirms the author's claim. |
| 3 | Statement order of a real rotate (RR default) | `BEGIN` → `SET TRANSACTION ISOLATION LEVEL READ COMMITTED` → `set_config(tenant)` → `pg_advisory_xact_lock` → `INSERT` → `SAVEPOINT` → `UPDATE … RETURNING` → `RELEASE` → `COMMIT`. On failure the order is the same, followed by `ROLLBACK`. | — | `log_statement=all` for one run, then reset (`SHOW` = none). Lines for one backend pid only (`stmt_order_rotate_rr.txt`) | Code read agrees: `db.ts:59-72` runs only `BEGIN` before `fn`, and `runWithTenantId` only sets ALS. No `SET LOCAL` or query precedes the pin on this route. |
| 4 | ISO: the level each INSERT ran at (BEFORE INSERT trigger logging `current_setting('transaction_isolation')` and pid), 30 rotate+plain pairs | rotates **30/30 read committed** under RC, RR and SERIALIZABLE defaults. Plain mints **31/31 at the pool default**. 29 plain mints reused a backend that had just run a rotate, with **0 at the wrong level** (the pin does not leak) | rotates ran at the pool default (RR 30/30, SER 30/30) | gate harness `ISO` | Develop proves the log really discriminates. |
| 5 | C0: does the URL `options` default leak? | Service pool = RR or SER as configured. A separate app-role session = read committed. Superuser = read committed. `pg_db_role_setting` for `secuura_app` is empty | same | gate harness `C0` | The same cell also asserts that RLS binds (an app-role UPDATE with no GUC matches 0 rows). |
| 6 | R1: double-submit ×10, N=20, N=30 (past pool max 10), under RC, RR and SER defaults | **0 bad of 12 shapes per default**: all 201, 0 null retires, 1 active, memory == DB. Max latency 34–50 ms | **RR: 12/12 bad** (N=20 → 11 active; N=30 → 19 active). **SER: 12/12 bad** (N=30 → **30 active of 31**) | gate harness `R1` | RC on develop is clean, which isolates the isolation level as the cause. |
| 7 | R2_grace: grace 60, double-submit ×10, under RR and SER | 10/10 trials with exactly 1 unexpiring key | 10/10 bad (2 unexpiring) | gate harness | — |
| 8 | K577 forced (BEFORE UPDATE trigger raising on retire or expiry change), grace 0 and 60, under RC, RR and SER | 201, `priorKeysRevoked` null, 2 active, no expiries written, memory seed unchanged, both keys validate | same | gate harness `K577` | — |
| 9 | K888 forced (deferred trigger: sleep 2 s at COMMIT, then raise), nothing touching the key in the window, grace 0 and 60, under RC, RR and SER | 500, no key, DB holds the seed only (active, no expiry), memory seed **byte-identical** (compared before any validate), map size unchanged, seed validates | same | gate harness `K888` | — |
| 10 | **A1 (m1 claimed case)**: validate of the prior key at +300, +800 and +1500 ms inside the COMMIT window | **15/15 trials**: rotate 500, no key, DB seed active, memory seed active, 3 post validates `true` | **12/12 red**: post validates `false` | gate harness, 5 head runs, 4 develop runs | **Instrument:** the mid-window validate answered `Key revoked` and the map entry object was replaced in 15/15 (head) and 12/12 (develop) trials, which proves the race really landed. |
| 11 | A2: the map entry is DELETED in the window (test seam) | Undo does **not** resurrect it (`memApiKeys.get(id)` is undefined → return). Validate then warms from the DB → `true` | same | gate harness | — |
| 12 | **A3: operator revoke of the prior key in the window, single fault** | Revoke 200, DB seed `is_active=false`, but **memory seed `isActive=true` in 15/15** and **`GET /api/keys` lists it active in 15/15**. Validate → `false` (the KS-1370 stored read), after which memory is corrected | 12/12: memory false, list false, validate false | gate harness (`pg_stat_activity` shows the revoke's upsert waiting on the row lock: 1 waiter in every trial) | → **n1** |
| 13 | **A3b: as A3, but the revoke's save also fails** (BEFORE UPDATE trigger armed by a flag table after the rotate's retire) | **15/15 trials: the revoked key validates `true`, twice.** Revoke 500, DB active, memory active | **12/12: validate `false`** | gate harness | **CONTROL:** the same failing revoke with no rotate in flight → 500, validate `false` (head 5/5, develop 4/4). The KS-888 R2 rule works by itself, so the race is the cause. → **n1** |
| 14 | A4: rotate A fails at COMMIT; rotate B on the same connector waits on the lock and commits | Natural timing: **50/50 clean** (DB = [B], memory seed retired, B active, A absent, seed refused, B valid) | 40/40 clean | gate harness | — |
| 15 | A4 widened (W1: the undo waits 400 ms, so B's in-lock memory retire lands first) | 10/10: memory seed resurrected `isActive=true` while the DB has it retired. Validate refuses (KS-1370) | **10/10 identical** | probe patch `W1`, `probe_W1_*` | The behaviour is the same on develop, so it is **pre-existing** (observation o1), not caused by restore-by-id. |
| 16 | A5: a prior key that the DB returns but memory does not hold (another replica) | Failing rotate: undo skips it, it is not added to the map, and it validates `true`. Succeeding rotate: `priorKeysRevoked` 1, and it validates `false` | same | gate harness | — |
| 17 | Unit `services/security` | **30 files / 331 passed** | — | `npx vitest run` | `vitest list` (default config) shows 0 ks1556 and 0 ks1549 entries, against 8 ks577 entries (control) |
| 18 | `packages/shared` | **49 files / 949 passed** | — | `npm test -w packages/shared` | — |
| 19 | tsc | `-p tsconfig.json`: rc 0. The service tsconfig **excludes `src/__tests__`**, so I also compiled `index.ts` and the two changed test files with the service's own options (a temp tsconfig extending it): rc 0 | — | `tsc_head.txt`, `tsc_tests_head.txt` | An injected `const x: number = "x"` in the m2 file made the same command fail (TS2322), so the instrument can fail. |
| 20 | eslint on the 3 changed files | rc 0 | — | `eslint_head.txt` | — |
| 21 | Integration with no env, or with only TEST_DATABASE_URL | **rc=1** both times, "Refusing to run". `npm run test:integration` with no env gives rc=1 | — | `int_noenv.txt`, `int_halfenv.txt`, `int_npm_noenv.txt` | vitest counts the cells as skipped, but the file fails, so the run is never green. |

## Mutants (author's six plus my four; anchors asserted by `mut.py`, marker grep ≥1 each run, file restored and checked after each)

| Mutant | Author's 13 cells | Gate harness |
|---|---|---|
| U1 undo by captured object | **killed** (E9) | — |
| U2 no undo for retired keys | **killed** (E9 and its control) | — |
| I1 pin removed | **killed** (both m2 cells) | — |
| I2 pin after the GUC query | **killed** (both m2 cells: the late SET errors, the retire falls back to null) | — |
| I3 pin = REPEATABLE READ | **killed** (7 cells, including E1, E2, E4, E5, E6) | — |
| I4 pin = SERIALIZABLE | **killed** (7 cells) | — |
| G1 undo by id, but only if the entry is still the same object (the #1527 verdict's second fix shape) | **killed** (E9) | — |
| G2 pin moved inside the savepoint | **killed** (both m2 cells) | — |
| **G3 pin skipped on the grace path** | **SURVIVED 13/13** | **killed**: `R2_grace` under RR, 10/10 trials leave 2 unexpiring keys |
| **G4 undo restores `isActive` only (not `expiresAt`)** | **SURVIVED 13/13** | **killed**: `K888` grace 60, memory seed keeps a 60 s expiry that the DB never committed |

The author's six all reproduce as killed. G3 and G4 survive the PR's cells. → **n2**

## Findings

### n1 (Minor, introduced by this PR): the restore-by-id undo overwrites an operator revoke that lands in the rotate's window. With a failed revoke save, a revoked key validates `true`.
- **Where:** `services/security/src/index.ts:335-340` (the undo writes `prev.isActive` onto whatever object `memApiKeys.get(id)` holds now). The revoke route builds a **fresh** object from the DB row (`dbGetApiKey` → `lookupKeyForRevoke`, `:440-456`), sets `isActive=false` (`:1376`), and puts it in the map **before** its upsert (`dbSaveApiKey`, `:375`). That upsert then waits on the row lock the rotate's `UPDATE` holds. When the rotate's COMMIT fails, the undo finds the revoke's object and sets it back to active.
  - On develop, the undo wrote to the captured object, which was no longer in the map, so the revoke survived.
- **Shapes, all deterministic with the window widened by a 2 s deferred trigger:**
  1. **Single fault:**
     - Steps: seed a key on C. Rotate C, failing at COMMIT. At +800 ms, send `DELETE /api/keys/:seed` (super_admin). `pg_stat_activity` shows its upsert waiting on the lock.
     - Result: rotate 500, revoke **200**, DB `is_active=false`. In memory `isActive=true`, and `GET /api/keys` lists the key active.
     - Validate refuses it (the KS-1370 stored read, `:1447-1465`), and that read corrects memory.
     - Head 15/15, develop 0/12.
  2. **Double fault:**
     - Steps: as shape 1, but the revoke's save also fails after the rotate rolls back.
     - Result: revoke **500** "revoked in this process only" (`:1382-1391`, the KS-888 R2 contract), yet the key **validates `true`, repeatedly**. Memory says active, and the DB never stored the revoke, so "revoked if either says revoked" (`:1462`) has nothing to see.
     - Head 15/15 under RC, RR and SER. Develop 0/12. The no-rotate control holds the revoke on both trees.
- **Oracle:** KS-888 R2 ("a revoke whose SAVE failed keeps its in-memory revoke, so the key stops working in this process"), quoted in the code at `:1454-1461`. The single-fault shape also breaks the PR's own claim that the in-memory map agrees with the DB.
- **Likelihood and blast radius:** low.
  - It needs a rotate COMMIT failure and an operator revoke of that connector's prior key between the in-transaction retire and the COMMIT. Naturally that window is a few milliseconds.
  - The fail-open shape also needs the revoke's own save to fail. A transient DB fault (for example a failover) would cause both failures together, so the faults are not independent.
  - The operator is told the revoke failed (500/503) and would likely retry.
  - Blast radius: one key, one replica, until a revoke succeeds or the process restarts.
- **Severity:** Minor, ranked above m1, because the failure direction flipped from fail-closed (m1: a valid key refused) to fail-open (a revoked key honoured).
- **Fix shape (owner's call):** keep the per-id restore, but do not restore over a revoke that happened after the retire. Options:
  - a per-id revoke generation or epoch that the revoke route bumps and the undo checks;
  - or mark rotate-pending retirements so that validate's R2 rule ignores them (then nothing replaces the entry, and undo-by-object works again);
  - or have the revoke route take the same `(tenant, connector)` advisory lock.
- **Regression test the owner should add:** shape 2 above (the A3b shape in `evidence/gate1529.integration.test.ts.txt`), plus its no-rotate control.

### n2 (Minor, test gap): two load-bearing guards that no cell pins
- **G3:** a pin that skips the grace branch (`API_KEY_ROTATION_GRACE_SECONDS > 0`) passes all 13 of the author's cells. The m2 file (`ks1556-rotate-under-repeatable-read.integration.test.ts:118-144`) has no grace cell, and the KS-1549 grace cell E4 runs at READ COMMITTED. Under RR, that mutant leaves **2 unexpiring keys in 10/10 double-submits**.
- **G4:** an undo that drops the `expiresAt` restore passes all 13 cells. E9 (`ks1549-…integration.test.ts:276-317`) runs only with grace 0. With grace 60, a failed COMMIT leaves the prior key with an in-memory expiry that the DB never committed. Validate masks it with the stored row, but it breaks KS-888's "memory unchanged".
- **Minor cell hygiene in E9:** the mid-window validate's own answer is discarded (`:305`). Assert it is `Key revoked` so the cell proves its race landed. Develop's red shows that it does land today.
- **Fix:** add a grace-60 double-submit to the m2 file, and run E9 with grace 0 and 60.

### Observations (not findings)
- **o1 (pre-existing, both trees):** if a second rotate's in-lock memory retire lands before the first rotate's undo, the undo re-activates the prior key in memory while the DB has it retired. Natural timing gave 50/50 clean trials. It reproduces only with a 400 ms widening (`probe_W1_head` and `probe_W1_dev`, identical), and validate refuses the key (KS-1370). The list endpoint would show it active. This is not caused by the restore-by-id change.
- **o2 (by reading only):**
  - **Writers of `memApiKeys`:** `:301`, `:328-340`, `:375` (mint, revoke), `:428` (validate usage), `:501-504` (`loadFromDb` clear and reload, also run on KS-382 DB recovery), `:1238`, `:1451`, `:1465`, `:1487`.
  - **Writers that can interleave with an open rotate on its prior keys:** the validate refresh (`:1465`, the m1 case, fixed); the revoke route (`:375`/`:1376`, → n1); the delete on a vanished row (`:1451`, safe, A2); and `loadFromDb`. A recovery reload during the window replaces every entry with the committed state, which is pre-existing and not measured.
  - **Writers that cannot interleave:** the memory-only rotate path (`:301`, `:241-246`) never runs on the DB path, and `:1238` touches only the new key's id.
- **o3:** the m2 file's URL-`options` technique cannot run through the repo's pgbouncer. `docker/pgbouncer/pgbouncer.ini:166` `ignore_startup_parameters = extra_float_digits` would reject `options`. This matters only if someone points that file at pgbouncer. Production does not use the parameter.

## Contracts at the head (brief item 4)
- **KS-577:** holds. A failed retire gives 201, `priorKeysRevoked` null, the mint saved, the prior key live, and memory untouched. This holds for grace 0 and 60, under RC, RR and SER (row 8).
- **KS-888:** holds for the failed COMMIT itself: 5xx, no key, DB unchanged, memory byte-identical (row 9). The concurrent-validate case is fixed (row 10). The concurrent-revoke case breaks KS-888 R2 (n1).
- **Memory-only path:** the pin is unreachable there (`:299-303` returns before `transaction()`). The ks577 memory cells are part of the 331 green.

## NOT tested
- **pgbouncer: UNMEASURED.** There is no pgbouncer binary on this machine (no Homebrew formula, no file found), the Docker daemon is down, and getting it would need a network install, which is out of bounds.
  - By argument: `SET TRANSACTION` is the first statement inside an explicit `BEGIN … COMMIT` on one server connection. It is transaction-scoped (row 2 shows no leak), so it is compatible with `pool_mode = transaction` (`pgbouncer.ini:54`).
  - This is an argument, not a measurement.
- A natural, un-widened COMMIT failure. Every m1/n1 shape used the 2 s deferred-trigger widening.
- Multi-replica behaviour, the real gateway path, and real JWKS auth (all calls went direct to the service with a locally signed super_admin token).
- `loadFromDb` reload during a rotate window (o2), and Postgres versions other than 15.14.
- The four platform suites the author did not run, and a local stack or deployed check.
- CI: the integration cells still have no CI job.

## Evidence index (`evidence/`)
- `int_head_{1..4}.txt` and `int_dev_{1..3}.txt`: the author's 13 cells.
- `gate_{head,dev}_{rc,rr,ser}_*.txt` with `gate1529_*.json`: my harness. The harness source is `gate1529.integration.test.ts.txt`.
- `mut_*.txt`, `mutgate_G3_rr.txt`, `mutgate_G4.txt`, `probe_W1_{head,dev}.txt`, `mut.py.txt`, `runmut.sh.txt`: mutants and the widening probe.
- `pg_settx_probe.txt` (`pgprobe.sh.txt`) and `stmt_order_rotate_rr.txt`: the Postgres-level m2 evidence.
- `unit_head.txt`, `shared_test_head.txt`, `tsc_head.txt`, `tsc_tests_head.txt`, `eslint_head.txt`, `vitest_list_default.txt`, `int_noenv.txt`, `int_halfenv.txt`, `int_npm_noenv.txt`, `migrations.txt`, `pg_setup.sh.txt`, `migrate.sh.txt`, `runint.sh.txt`, `suites.sh.txt`, `summ.py.txt`.

## Self-corrections (public)
- **My first integration run was 13 skipped, rc 1.** `@secuura/shared` had no built `dist`. The rc 1 meant "could not run", not a product result. I built shared in both trees and re-ran. The failing log was overwritten by run 1, so it is not kept.
- **My first `tsc` over the test files used ad-hoc `nodenext` flags and reported 7 errors.** Those were an artefact of my instrument: the service is `commonjs`. I replaced it with a tsconfig that extends the service's own, and added a positive control that injects a type error and fails.
- **The first migration attempt gave applied=0.** The runner globs `migrations/*.sql` relative to the cwd. I re-ran it from the Dev directory and got applied=50.
- **Head runs 1–3 of the author's cells used the default reporter,** which lists files rather than cells. All three were 13/13 with rc 0. Run 4, and everything after it, used `--reporter=verbose`.
