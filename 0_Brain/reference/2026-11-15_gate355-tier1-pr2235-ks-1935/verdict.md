PR 2235: GO WITH NOTES (at head e17704c1a4329d4f9041c4ab75d9f0f19bce2aa1; tier 1)

Gate 355, tier 1, Opus. This is the re-commission: the first gate agent died at 17:31 AEDT before it wrote a verdict. This run went from 17:32 to 17:47 AEDT on 2026-11-15. Findings only: nothing was fixed, pushed, posted, commented, mailed, merged, or written to Linear or GitHub.

**About the first agent's work.** Its clone and worktrees in `scratch/` were reused only after I re-pinned (below) and found them at exactly the re-pinned SHAs with porcelain 0. Its old `out-*` logs were not used as evidence. Every figure below comes from a run made in this session. The files from this run are `pin2.out`, `pin3.out`, `out-mt2.txt`, `out-redproof-*`, `out-suite-{dev,head}-{1,2}.json`, `out-suites-summary.txt`, `out-mutants.txt`, `out-tsc-*`, and `out-pg-*`. The PostgreSQL probes printed their JSON to the session; they are reproducible with `pgprobe.sh`.

**Pins.**
- Read with `gh api` at 17:32:36, then with `git ls-remote` at 17:32:48 (`scratch/pin2.out`). Read again with `gh api` at 17:46:06 and `ls-remote` at 17:46:13 (`scratch/pin3.out`).
  - develop ce35818d50aebe7f41fc41f677ee03079c36d7ad
  - refs/pull/2235/head e17704c1a4329d4f9041c4ab75d9f0f19bce2aa1
- Neither moved during the gate. The PR is open, not merged, `mergeable_state` unstable (that is no testing claim), 6 files, +493 -23.
- The PR is ONE commit on 4e4347818772. develop has one more commit since then, ce35818d5 (KS-2144, a shared test-file comment).
- `merge-tree --write-tree` gives tree 9bc8931ae924 in both orders, rc 0 (`scratch/out-mt2.txt`).
  - Merge vs head: 1 path differs, the shared ks1974 test file.
  - The billing tree in the merge is fca3d0bdf0a5, identical to the head's.
  - So the billing service measured at the head IS the billing service at the merge.

## FOUND

**G355-2235-1 (Medium; new with this PR; fix before deploy).** A dropped database connection while the lock is held crashes the billing process.

*The cause.*
- `withCustomerCreditLock` checks a pool client out and holds it idle across three Stripe HTTP calls (retrieve, update, verify retrieve).
- pg-pool 3.13.0 removes its idle `'error'` listener on checkout (`node_modules/pg-pool/index.js:344`).
- pg 8.20.0 emits `'error'` on the Client when the connection dies with no query running (`pg/lib/client.js:387-393`).
- `creditLock.ts` attaches no listener.
- billing's `index.ts` installs only SIGTERM and SIGINT handlers. The shared `gracefulShutdown` that handles uncaughtException is not used by billing.

*Measured on PostgreSQL 15.19, with the real `creditLock.ts` and `db.ts` from the head under tsx (`probe/g355_pg.ts terminate`).*

| Case | Process exit | Uncaught | What the call did |
|---|---|---|---|
| The holder's backend is terminated inside `fn` (`pg_terminate_backend`), no process handler | **rc 1**: `Unhandled 'error' event … terminating connection due to administrator command` (`scratch/out-pg-terminate-nohandler.log`) | — | — |
| Same case, with a recording handler | — | 2 uncaught exceptions | resolved (COMMIT failed and was logged); the lock was released |
| Control: an IDLE pooled backend is terminated | rc 0 | 0 | — |

*What triggers it.* Anything that drops the connection in that window: a database failover or restart, maintenance, a network drop, or a server-side idle-in-transaction timeout.

*Why it is new.* Before this PR, billing never held a checked-out client across an await on something outside the database. `getClient` had no caller, and `queryWithTenantGuc` holds its client only across back-to-back queries.

*Money consequence (read, NOT measured end-to-end).* If the process dies inside a webhook credit:
- the KS-1933 `billing_credit_grants` row stays `'granting'`;
- Stripe's redelivery then finds the claim lost and adds nothing (`creditGrants.ts:103-113`);
- if the Stripe update had not yet landed, a PAID purchase stays uncredited until someone checks by hand. That is the ledger's documented "process died mid-credit" residual, and this PR adds a new way to reach it.

Every other request in flight on that replica is dropped too.

*The fix (one place).* Attach `client.on('error', …)` for the hold, log it with `describeThrown`, mark the client broken, and remove the listener before `release`. Add a cell that emits `'error'` on the fake client during `fn`.

**G355-2235-2 (Low; new; availability, no money effect).** One customer's burst of credits or debits takes the whole billing pool.
- Every waiter holds a pool connection while it blocks in `pg_advisory_xact_lock`. The pool is `max: 10` with `connectionTimeoutMillis: 5000` (`db.ts:26-29`), and there is no `lock_timeout`.
- Measured with `probe … flood`: fn = 600 ms, standing in for three 200 ms Stripe calls, all calls on one customer.

| Concurrent calls | ok | Refused (CreditLockUnavailableError) | Unrelated `query('select 1')` | Another customer's credit |
|---|---|---|---|---|
| 9 (control) | 9 | 0 | ok at 127 ms | ok at 137 ms |
| 30 | 18 | 12 | **FAILED at 5102 ms** ("timeout exceeded when trying to connect") | **refused at 5102 ms** |

- **Who can trigger it.** `POST /credits/use` is open to the customer's owner, so an authenticated user can do this. Whether the gateway rate-limits it is UNMEASURED.
- **The message misleads.** The refusal says "the database that serialises it is down" when the database is up and the pool is exhausted.
- **Suggested fix (for the board).** Take the lock with `SET LOCAL lock_timeout` (or `pg_try_advisory_xact_lock` with backoff), and/or give the lock its own small pool.

**G355-2235-3 (Info; Q3, as designed).** Key collisions and the lock timeout.
- **Collisions.** `hashtext` is int4.
  - In 300,000 synthetic keys I found 3 colliding pairs, for example `cus_203b7f95e887c9` and `cus_709959392eb67e` (hash -1890754520).
  - With the first held, `pg_try_advisory_xact_lock` on the second returns **f**. A non-colliding control returns t, and after release it returns t.
  - The effect is that two customers are serialised against each other. There is no money effect: each still runs its own read-update-verify.
  - The security service's locks use the two-int4 form, `pg_advisory_xact_lock(hashtext, hashtext)`, a disjoint keyspace. Measured: the same hash in the two-key form, taken while the one-key lock is held, returns t.
  - No other one-key `pg_advisory*` exists under `Blockchain/Dev` (grep across .ts, .js, .sql and .py; creditLock.ts is the positive control).
- **Lock timeout: there is none.**
  - A waiter simply waits for the holder: measured 6005 ms behind a 6 s holder, no error (`probe … nowait`).
  - The holder is bounded only by Stripe: stripe 14.25.0 with the default timeout of 80,000 ms (`stripe.core.js:17`), times three calls.
  - Getting a pool connection is bounded at 5 s and answers 503 (G355-2235-2).

**G355-2235-4 (Info; test thinness).** My 19 mutants against the whole billing suite (`scratch/out-mutants.txt`): 17 KILLED, 2 SURVIVED.
- M4: the key loses its `billing-certification-credits:` namespace. Nothing pins the namespacing claim.
- M7: `release(broken ? true : undefined)` becomes `release()`. Nothing pins destroying a broken client.

Neither changes money. The crash path in -1 and the pool pressure in -2 have no cell.

## TESTED

**Q1. The lock: acquired and released on every credit and debit path, on one connection, released on every error path, correct across replicas.**

*Read at the head.*
- `addCertificationCredits` (`stripeService.ts:228`) and `useCertificationCredits` (`:251`) each wrap their whole retrieve, update and verify in `withCustomerCreditLock`.
- These are the only billing writers of `certificationCredits`. Census by grep: the callers are routes `billing.ts:762` and `:802`, webhooks `:493` and `:546`, and the uncalled `stripeService.ts:580` and `:593`.
- `PUT /customers/:id` refuses the key via `RESERVED_CUSTOMER_METADATA` (`billing.ts:430-435`).
- BEGIN, the lock and `fn` run on one client. The error paths:
  - a throw from BEGIN, the lock or `fn` leads to ROLLBACK, then rethrow, then `release`;
  - a failed ROLLBACK destroys the client;
  - a failed COMMIT destroys the client and is logged.

*Measured on PostgreSQL 15.19 with the head's real modules.*

| Probe | Result |
|---|---|
| `held` | While `fn` runs there is exactly 1 granted advisory lock, objid = `hashtext(key)` = -905722973. A second caller shows granted=false on the same objid. After both: 0 locks, results [1, 2]. |
| `throw` | `fn` throws: rethrown, 0 locks left, the next call runs in 1 ms, pool total 1 / idle 1 / waiting 0. |
| `replicas` | **Two separate OS processes, each with its own pool, one database.** The fake Stripe balance is a row read and written outside the lock transaction, with awaits in between. 10 → +5 and +3 → **18**; 100 → 20×(+2) and 20×(−1) → **120 = expected**. |
| `replicas`, no lock (control) | Same 40 operations: 101. |
| `replicas`, my planted M1 (BEGIN removed) | 13 and 102. |

After the plant, `creditLock.ts` was restored and `hash-object` matched. The re-run gave 18 and 120.

**Q2. The ticket's interleaving, and no re-apply after a failed verify.**
- The PR's own file, reproduced by me:
  - on develop's product: **11 failed / 5 passed**, every one an AssertionError. K1 "expected 23 to be 18", K2 "7 to be 12", K1b "15 to be 18", K2b "15 to be 12", K4 "{value:104} to deeply equal {value:15}", then K5, K5b, K6, K7, R1, R2;
  - at the head: **16/16**.

  These equal the READY.
- Across processes on real PostgreSQL the ticket's example ends at 18 (Q1).
- **No re-apply after a failed verify.** My M10 (a mismatch re-applies the credit), M11 (the test inverted), M12 (the verify read dropped) and M16 (returns the verify read, not the value it wrote) are each KILLED by K4.

**Q3.** See G355-2235-3: collisions serialise only, and there is no lock timeout. G355-2235-2 shows what a pool wait answers: 503 after 5 s.

**Q4. Migrations and schema.** None.
- 6 changed paths, 0 matching migration, .sql, schema or prisma (control: 6 of 6 match "billing").
- 0 added lines with CREATE TABLE, ALTER TABLE, CREATE INDEX or DROP in services (control: 5 added `pg_advisory` lines).
- The advisory lock needs no schema.

**Q5. Money semantics vs Wednesday's ANSWER option (a)** (read whole from agentmail, sent 04:40:27Z; the body was not stored on disk). Every point matches:
- a per-customer `pg_advisory_xact_lock(hashtext(...))` on its own client, in one transaction, around retrieve → update → verify, for BOTH methods;
- the verify stays, and a mismatch logs `logger.error(…, { customerId })` only, with no amount and no email;
- it returns the value it wrote (M16 killed);
- fail-closed 503 on `POST /admin/credits` and `POST /credits/use` (M17, M18, M19 killed, and M8 and M9 for the refusal itself);
- both operations already document 503 (`billing.openapi.ts`, `503: commonErrorResponses[503]` in the registrations at lines 953 and 981), so no OpenAPI change is needed;
- (c), the balance in PostgreSQL, is not attempted. It is filed as a HANDOVER candidate (6b).

One addition goes beyond the ANSWER: a COMMIT that fails after `fn` is logged, not thrown. I find it justified, because it stops the KS-1933 ledger re-crediting a write that landed. It is pinned by K9 (M6 killed).

**KS-1897 (Kam, 17:09: "credit email-only checkouts by matching the email").** I checked it against this PR. The lock is keyed on a resolved customer id, inside `addCertificationCredits`. An email-matched credit would resolve the customer before calling it and take the same lock. Nothing in this PR conflicts with that ruling, so I recorded no routing note.

**Whole billing suite**, interleaved dev → head ×2, Node v26.8.1, vitest 4.1.12:

| Tree | Run 1 | Run 2 |
|---|---|---|
| develop ce35818d50ae | 20 files, 377/377, rc 0 | same |
| head (= the merge's billing tree) | 21 files, 393/393, rc 0 | same |

377 + 16 = 393, equal to the READY.

**tsc and eslint.**
- `tsc --noEmit -p services/billing/tsconfig.json`: rc 0 at both trees. A planted TS2322 gives rc 2, and the file was restored (hash matched).
- eslint (ESLint API, Dev root flat config) on the 4 changed .ts files: **0 errors**, 2 warnings. Both are pre-existing `no-unused-vars` in `stripeService.ts`; develop has the same 2 at :154 and :540. The planted control (no-fallthrough plus debugger) gives 2 errors. The plant file was moved to `scratch/probe/moved/`, and porcelain is 0.

## HOW
- **Clone:** `scratch/clone` (`--reference` to the Blockchain object store; push URL DISABLED, shown in pin2 and pin3). Worktrees `wt-dev` at ce35818d50ae and `wt-head` at e17704c1a432, sparse on `Blockchain/Dev`. The root `npm ci` came from the first agent, and I verified it by running the suites. `packages/shared` was rebuilt in both this session, rc 0.
- **PostgreSQL:** a throwaway Homebrew PostgreSQL 15.19, `initdb` into `scratch/pgdata`, TCP 127.0.0.1:55435 only, trust auth. It was stopped at the end (rc 0).
- **Probes:** `scratch/probe/g355_pg.ts`, run by `scratch/pgprobe.sh`.
- **Mutants:** `scratch/mutants.py`. Each mutant is restored with `git checkout HEAD --` and its sha256 asserted; porcelain ended at 0.
- **GitHub:** `gh api` GET only, with the project GH_CONFIG_DIR. The PR body is in `scratch/pr2235_body.md`.
- **The ANSWER:** one read-only agentmail GET (`scratch/am.py`). The key was read from Wednesday's `4_Credentials/.env` and never printed.
- **No writes outside this folder.**

## NOT TESTED (UNMEASURED)
- Real Stripe; a booted billing service; a real webhook delivery through `grantCreditsOnce` under `CreditLockUnavailableError` or under the -1 crash (the stuck `'granting'` row is read, not measured); real Azure PostgreSQL (its `idle_in_transaction_session_timeout` and failover behaviour); PgBouncer.
- The gateway's rate limiting on `/credits/use`.
- Node 24; a container build; Schemathesis, Akto, Playwright, k6; preflight legs; the docs-fragments checker and `check:test-types` (billing is not in its list). The fragments were read only for their claims.
- Linear: KS-1935's state and comment were not read.
