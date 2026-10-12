# Gate verdict: Secuura Platform K PR #1527 (KS-1549, P1): concurrent rotates on a credential path

**VERDICT: GO WITH NOTE.** No Majors. Two Minors (m1, m2), one observation. The defect is fixed and stays fixed under every concurrency shape I tried. The approved shape is implemented as briefed, and every load-bearing step I mutated is caught by the author's cells. The Minors are narrow and are fix-shape notes, not blockers.

- **Head under test:** `a430061c9d46d24498a5c83524889dba3dc009c7`, taken from bundle `ks1549-a430061c9d46.bundle` (sha256/16 `c82bc4e328fe8589`, matches the brief). Its parent is `69878dc5`, and it was fetched into a `git clone --shared` in the gate scratchpad. `git diff --stat 69878dc5..head` gives 6 files, +440/-52, which matches the PR.
- **Develop under test:** `81ac1ea60ec684f1636a25832d9a7f3bf28470f5`. `69878dc5..81ac1ea` touches only `services/{governance,staking,transfer}/src/__tests__/db.retry.test.ts`, so the author's "zero overlap" claim holds (instrument: `git diff --stat`). For the develop runs I copied the PR's integration test and its config into a develop worktree.
- **Database:** my own PostgreSQL 15.x (`/opt/homebrew/opt/postgresql@15`), built with `initdb -U secuura --auth=trust` on 127.0.0.1:55424 with the unix socket off. I applied `docker/init/*` in order with a throwaway `APP_DB_PASSWORD`. The `00-create-platform-db.sql` dblink step failed (role lookup over dblink), so I created `secuura_platform` by hand as the brief allows. `run-migrations.sh` gave **applied=50 failed=0**. `svc_api_keys` has `relrowsecurity=t relforcerowsecurity=t`, and `secuura_app` has `rolsuper=f rolbypassrls=f`. The service connected as `secuura_app` in every cell. Postgres was stopped at the end (`pg_ctl stop`, port closed).
- **Scope:** findings only. Nothing was written to the project, nothing was pushed, there were no GitHub or Linear writes, and I contacted no remote box. `npm ci --prefer-offline` read the package registry/cache to populate the scratch clone.

## Numbers (instrument / control)

| # | What | Head | Develop | Instrument | Control that could have failed |
|---|---|---|---|---|---|
| 1 | Author cells CONTROL, E3, E1, E2, E4, E5, E6, E8 | **8/8 green, 4 of 4 runs** | **5 red (E1, E2, E4, E5, E6), 3 green, 4 of 4 runs** | vitest, `vitest.integration.config.ts`, app role | Develop E1 shows the real defect shape: `active=[]` in 9 of 10 trials (`evidence/int_dev_1.txt`). CONTROL proves RLS binds (an app-role UPDATE without the GUC matches 0 rows). |
| 2 | Mutant M1: lock removed | E1, E2, E4, E5, E6 red | | same cells | Marker grep = 1 before each run. Anchors are asserted by `mut.py`, which fails loudly when an anchor is absent. |
| 3 | Mutant M2: INSERT through `query()` on a second pooled client (the KS-757 trap) | E2 red with 10/20 rotates **503 at 5002 ms**; E6 red with 21/30 rotates 503 | | same | Re-measures KS-757: once lock waiters fill the pool, the holder's second `connect()` times out at `connectionTimeoutMillis` 5000. |
| 4 | Mutant M3: `applyTenantGuc` removed | 7/8 red (all but CONTROL) | | same | — |
| 5 | Mutant M4: memory not told (`retireInMemory` removed) | E2, E6 red (memory != DB) | | same | — |
| 6 | Mutant M5: savepoint removed (retire error rethrown) | E8 alone red | | same | Matches the author's claim. |
| 7 | A1: mixed rotate and plain mints, N = 2, 3, 5, 10, 20, 35, 50, 3 trials each (21 trials) | **0 bad**: all 201, exactly 1 active rotate-key per trial, ≥1 active, memory == DB per row | red | gate harness `evidence/gate1527.integration.test.ts.txt`, superuser read-back | A plain mint that commits after the last rotate correctly stays active. I saw this in 2 trials (active=2, activeRot=1); it is decision D's semantics, not a defect. |
| 8 | A2: same connector id in two tenants | T2's rotate finished in **2 ms** while I held `(hashtext(T1),hashtext(c))` externally. T1's rotate stayed **blocked** (row count 1 while held). Each tenant ended with 1 active. 10/10 concurrent cross-tenant double-submit trials clean, memory == DB. | red | harness + external `pg_advisory_xact_lock` held by superuser | The T1-blocks control proves my lock key equals the code's, so the T2-not-blocked result shows real lock-key separation. |
| 9 | A3: hashtext collision | Found a real collision: `gate1527:col:365184` / `gate1527:col:91210`, both `hashtext = -1742392310` (verified with a second `SELECT hashtext`). Holding the lock on one **blocks** a rotate on the other, which proves they share a lock. 10/10 interleaved double-submit trials still leave exactly 1 active on **each** connector. | red | SQL `GROUP BY hashtext` over 400k ids | A collision only serialises; it never mis-retires, because the UPDATE filters by connector. |
| 10 | A4: lock-holding client killed mid-transaction (BEFORE INSERT trigger with `pg_sleep(20)`, then `pg_terminate_backend`) | Killed rotate → **503**, no key, row rolled back, absent from memory. The queued rotate finished **4 ms** after the kill → 201. Exactly 1 active. Memory == DB. The pool serves a fresh mint afterwards (201). 3 of 3 runs. | red (no lock, so nothing queued) | harness, `pg_stat_activity` / `pg_locks` | Control: the fast rotate was confirmed blocked (1 ungranted advisory lock) before the kill. |
| 11 | A6: KS-577 failed retire in **grace** mode, two concurrent rotates | 201/201, `priorKeysRevoked` null/null, 3 rows all active and unexpiring, **memory seed expiry untouched** | **red**: memory seed got `expiresAt` although the DB retire failed | harness, BEFORE UPDATE trigger raising on an `expires_at` change | Develop's memory-first retire diverged from the DB. **The PR fixes this.** |
| 12 | A7: KS-888 failed COMMIT (deferred constraint trigger raising at COMMIT), grace 0 and 60 | 500, no key, DB unchanged (seed only), memory seed byte-identical, memory size unchanged, seed validates true | same (green) | harness | My first run of A7 went red because **my harness** perturbed memory: I validated (which bumps `usageCount`) before comparing. I corrected it and recorded the correction (see below). |
| 13 | A8: KS-888 failed COMMIT **raced by a validate of the prior key** | **RED, 3 of 3 runs**: after the failed rotate the DB holds the prior key active, but `/api/keys/validate` answers `valid:false, "Key revoked"`, again and again | **green**: the prior key stays valid | harness, deferred trigger `pg_sleep(2)` then raise; validate at +800 ms | Control without the mid-window validate: the prior key stays valid on head (3 of 3). This isolates the race. → **m1** |
| 14 | A9: grace mode, N=10 concurrent rotates, memory vs DB expiries | 1 unexpiring key. Memory/DB null-shape identical. max abs(mem−db) = **8–9 ms** | red (memory had an expiry where DB had null) | harness | |
| 15 | A11: 50 rotates on one connector plus 20 validates of another key | drain **133–138 ms**, 0 non-201, validate max **37–41 ms**, 0 bad validates, 1 active | — | harness | FAIL bound was 5 s or any bad validate. |
| 16 | `default_transaction_isolation = 'repeatable read'` on `secuura_app` (reset afterwards) | **5 of 8 author cells red**, 55 × `could not serialize access due to concurrent update` → retire falls back to KS-577 null | — | author cells | Reset was verified (`rolconfig` empty). → **m2** |
| 17 | Unit suite, `services/security` | **30 files / 331 passed** | — | `npx vitest run` | The integration file is not in the default run (`vitest list`: 0 ks1549 entries vs 8 ks577 entries). |
| 18 | `packages/shared` | **49 files / 949 passed** | — | `npm test -w packages/shared` | — |
| 19 | tsc `--noEmit`, eslint on `index.ts` | rc 0 / rc 0 | — | — | — |
| 20 | `npm run test:integration` without env, and with only TEST_DATABASE_URL | **rc=1** both times, "Refusing to run: these cells are never skipped" | — | npm | vitest counts the 8 cells as "skipped", but the file fails and the exit is non-zero, so a missing database cannot pass as green. |

## Findings

### m1 (Minor): a failed rotate COMMIT can leave the prior key refused in this process while the DB still holds it active (violates KS-888's "memory unchanged")
- **Where:** `services/security/src/index.ts:318-326` with `:330`. The undo closure captures the **object** `m` and restores fields on it. Separately, `/api/keys/validate` at `index.ts:1447-1450` **replaces** the map entry with a fresh `rowToApiKey` object, and it carries `isActive=false` because memory said revoked ("revoked if either says revoked", KS-888 R2).
- **Mechanism:** the memory retire runs inside the transaction **before COMMIT**. If the prior key is validated during the COMMIT round trip:
  1. validate sees the memory key revoked and the stored row active.
  2. validate writes a new, sticky-revoked object into the map.
  3. COMMIT fails.
  4. undo restores the old object, which is no longer in the map.

  Result: the DB has the prior key active, this process refuses it on every call, and the rotate caller got 500/503 with no new key.
- **Reproduction (deterministic, widened window):**
  1. Seed a key on connector C (plain mint) and validate it (valid).
  2. Create a deferred constraint trigger on `svc_api_keys` that `pg_sleep(2)` then RAISEs for the rotate's row.
  3. POST a rotate on C.
  4. At +800 ms, validate the seed key: `Key revoked`.
  5. The rotate returns 500.
  6. Validate the seed twice more: both `valid:false, "Key revoked"`, while the superuser read shows the seed `is_active = true`.

  Head: 3/3 red. Develop: 3/3 green on the same steps (develop never mutated memory before COMMIT). Un-raced control on head: 3/3 green. Evidence: `gate_head{1,2,3}.txt`, `gate_harness_results_head*.json` key `A8`, `gate_dev1.txt`.
- **Oracle:** Product/History. This is KS-888's ruled contract ("a failed COMMIT ... leaves memory unchanged"), which the PR's own comment cites at `index.ts:285-286`.
- **Likelihood and blast radius:** low likelihood. `svc_api_keys` has no deferrable constraints (grep of migrations/init: the only `DEFERRABLE` is on another table, `029_tokenisation_tenant_keys.sql:29`), so a natural COMMIT failure means a connection or server fault, and the validate must land within the COMMIT round trip. The prior key is the one in active use, though, so a concurrent validate is plausible. Blast radius is one connector on one replica, until a retried rotate succeeds or the process restarts. Severity Minor.
- **Fix shape (owner's call):** apply the memory changes **after** COMMIT succeeds rather than before-plus-undo, or have undo re-fetch `memApiKeys.get(id)` and restore by id only if the entry is still the object it changed. **Regression test the owner should add:** the A8 shape above (a deferred-trigger COMMIT failure plus a validate of the prior key inside the window, asserting the prior key is still `valid:true` afterwards).

### m2 (Minor, latent): correctness silently depends on READ COMMITTED
- **Where:** `index.ts:297-299`. The transaction is opened by `db.ts:62` (`BEGIN` with no isolation level), and `applyTenantGuc` runs before the lock, so under REPEATABLE READ the snapshot predates the lock.
- **Measured:** `ALTER ROLE secuura_app SET default_transaction_isolation='repeatable read'` turns E1, E2, E4, E5 and E6 red. That is 55 serialization failures, each degrading to `priorKeysRevoked: null` with more than one active key (`evidence/iso_rr.txt`).
- **Is the deployment exposed today?** Nothing in the repo sets a non-default isolation level (git grep), so it runs READ COMMITTED. This is a latent assumption, not a present defect. The PR comment lists "every step is load-bearing" but omits this dependency.
- **Fix shape:** `BEGIN ISOLATION LEVEL READ COMMITTED` for this transaction (a structural guard), or document the dependency next to the lock.

### Observation (not a finding): in-doubt COMMIT
If the connection dies after the server committed but before the client hears it, the caller gets a retryable 503 with no key, while the DB holds a new key nobody has and the prior key is retired. The connector has no usable key until the caller retries. This is inherent to any commit and was not measured; the retry contract (503) is the mitigation.

## Self-correction (public)
My first A7 run reported memory changed after a failed COMMIT. **That red was my harness, not the product.** I called `/api/keys/validate` before comparing the memory snapshot, and validate bumps `usageCount`/`lastUsedAt` on the same object. The reasoning error was an observation layer perturbing what it observed. I moved the comparison before the validate and re-ran: green on head 2/2 and on develop 1/1. The original failing log is kept at `evidence/gate_head1.txt`.

I caught one more instrument fault before it could be read as a result. My first mutant loop wrapped vitest in `timeout`, which macOS lacks (rc 127), so every mutant "ran" nothing. I discarded the loop and re-ran without the wrapper. The mutant numbers above come from the second loop, with markers asserted present.

## NOT tested
- **pgbouncer (brief item 5): UNMEASURED.** pgbouncer is not installed, there is no local image, and the Docker daemon is not running. Getting it would need a network install or pull, which is out of bounds. The design argument (one BEGIN…COMMIT on one client, an xact-scoped lock, `set_config(..., true)`) is consistent with `pool_mode = transaction` (`docker/pgbouncer/pgbouncer.ini:54`), but it is an argument, not a measurement.
- Multi-replica behaviour: memory is per process. Cross-replica divergence is covered by KS-1370's DB re-read on validate and was not exercised here.
- The real gateway path (`register-connector` → security) and real JWKS auth. All calls went direct to the service with a locally signed super_admin token.
- A natural, un-widened COMMIT failure (m1 was reproduced with a `pg_sleep` widening). The in-doubt-commit case.
- Lock-wait timeouts and statement timeouts (none are configured, and I did not test a holder that hangs for minutes). Long-hold pool starvation was measured only at the 133 ms drain scale (A11).
- The memory-only (no DATABASE_URL) path beyond the existing unit cells (ks577 suite, part of 331 green). The surviving "lock keyed on tenant only" mutant was not re-run; I accept it as coarser-equivalent by argument.
- Postgres versions other than 15. CI: the new integration cells have no CI job (documented by the author in DEV-PROCESS.md), so a regression here would not be caught automatically.

## Evidence index (`evidence/`)
- `int_head_{1..4}.txt` and `int_dev_{1..4}.txt`: the author's cells.
- `gate_head{1,2,3}.txt`, `gate_dev1.txt`, `gate_harness_results_*.json`, `gate1527.integration.test.ts.txt`: my harness.
- `mut_M{1..5}_*.txt`, `mut.py.txt`: mutants.
- `iso_rr.txt`: the m2 isolation probe.
- `unit_head.txt`, `shared_test_head.txt`, `tsc_head.txt`, `eslint_head.txt`, `int_noenv.txt`, `int_halfenv.txt`, `migrations.txt`, `pg_setup*.sh.txt`.

The app password was redacted and scanned for: 0 hits.
