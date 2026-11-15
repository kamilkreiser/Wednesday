PR 2235: GO WITH NOTES (at head 19b6f52483c6514f1212be26b538df8789a17b1d; tier 1)

Gate 361, tier 1 delta (round 2 of 2), Opus. Ran 18:23 to 18:31 AEDT on 2026-11-15. Findings only: nothing was fixed, pushed, posted, commented, mailed, merged, or written to Linear or GitHub. Baseline: gate 355's verdict (GO WITH NOTES at e17704c1a432, G355-2235-1 Medium "fix before deploy"), read whole with its commission.

**Load.** Load averages 2.96 at the start, a peak of 14.36 (1 min) during the first PG probes, about 5 to 7 for the suites and mutants. Every suite run was rc 0 and stable across both runs, so load did not change any result.

**Pins.**
- `gh api` at 18:23:59: PR open, not merged, head 19b6f52483c6514f1212be26b538df8789a17b1d, 2 commits, 7 files +661 -23; develop 96aa5fc17c60.
- `ls-remote` at 18:24:20 (`scratch/pin1.out`): the same.
- Re-pinned at 18:29:53 (`gh api`) and 18:30:00 (`scratch/pin2.out`). The head did not move. **Develop moved to 9bb6c98b2c47** (KS-1105: 2 admin-frontend files).
- The head is ONE commit on e17704c1a432 (`merge-base --is-ancestor` ok; `19b6f52^` = e17704c1a432). It is a fast-forward, nothing was rewritten. The delta is 5 files, +173 -5, as the READY says.
- **merge-tree, both orders, rc 0:**
  - on develop 96aa5fc17c60: tree 120c73546388 (`out-mt1.txt`);
  - on develop 9bb6c98b2c47: tree 93bed3ea31d5 (`out-mt2.txt`).
  - The billing tree in the merge is **5f0230534cd7 on both develops**. That is NOT the head's billing tree (8df081d58b1a), because develop gained KS-1934 (`routes/webhooks.ts` plus a test). So I built the merge as a local commit (a59c4e53e5f6, never pushed; push URL DISABLED) and measured it directly. See Q5.

## G355-2235-1: CLOSED

## FOUND (this round)

**G361-2235-1 (Low; reachable only since the fix; filing, not a blocker). After a dropped connection the lock is gone, but `fn` keeps going.**
- PostgreSQL releases a transaction advisory lock when the backend dies. The fix keeps `fn` running, which is right: its Stripe write must stand. But `fn` is not told that the lock is gone.
- Measured on PG 15.19 (`probe/g361_pg.ts lockloss`, `out-pg-head-lockloss.log`):
  - Holder A terminates its own backend at t=1 ms and runs until 1002 ms.
  - Caller B on the same customer starts at 300 ms and **enters its `fn` at 307 ms, while A is still inside**.
  - Control, with no termination: B enters at 1002 ms, after A.
- So for the rest of A's `fn`, the KS-1935 lost update can happen again if a second same-customer writer arrives in that window. This part is read, not measured end-to-end. It would leave a wrong balance, and the verify would log it as an outside writer. It is never re-applied.
- **Preconditions:** a database connection drop AND a concurrent write for the same customer, inside one Stripe round trip.
- Before this round the process crashed instead, so this is strictly better.
- **Suggested filing:** expose the lost-lock state to `fn`, so `stripeService` refuses before `customers.update` once the client is broken (a throw before the update leads to the ledger's `'failed'`, then a safe redelivery).

**G361-2235-2 (Low; test thinness). A `once` listener passes every cell and still crashes on real PostgreSQL.**
- My mutant N7 changes `client.on('error', …)` to `client.once(…)`. It **SURVIVES the whole billing suite** (400/400).
- On PG 15.19, N7 gives **rc 1**: `Unhandled 'error' event … Error: Connection terminated unexpectedly` (`out-pg-N7-once.log`).
- The reason: pg emits TWO `'error'` events for one termination, which I measured as two log lines (`DatabaseError` then `Error`). No cell emits twice.
- Suggested: one cell that emits `'error'` twice during `fn`.

**G361-2235-3 (Info).**
- (a) The READY's "billing at the head = billing at the merge" was true on 240d1f664b52. It is stale on today's develop, because KS-1934 changed `webhooks.ts`. The merge is green (Q5). KS-1934 adds no new credit call site: `async_payment_succeeded` reuses `handleCheckoutComplete`, so it goes through `grantCreditsOnce` and then the lock.
- (b) The fragments say "400 tests, 22 files". The merge will be 418 tests, 23 files. That is a doc count only.
- (c) Mutants N8 (listener removed after `release`, not before) and N10 (listener attached only after BEGIN and LOCK) survive. Both are benign, or a sub-millisecond window: no query is idle between BEGIN and LOCK.

## TESTED

**Q1. G355-2235-1 reproduced and closed.**
- Setup: gate 355's probe copied verbatim (`probe/g355_pg.ts`, sha256 1714b3b46e8c5ab6, equal to gate 355's), on a throwaway Homebrew PostgreSQL 15.19. `initdb -U gate`, trust auth, 127.0.0.1:55437 only, unix sockets off. It was stopped after each use (rc 0, 0 listeners).

| Tree | terminate, no handler | terminate, recording handler | idle-backend control |
|---|---|---|---|
| e17704c1a432 | **rc 1**: `throw er; // Unhandled 'error' event` … `terminating connection due to administrator command` (`out-pg-old-term-nohandler-full.log`) | rc 0, **2 uncaught** ("terminating connection due to administrator command", "Connection terminated unexpectedly"), resolved "fn-returned" | rc 0, 0 uncaught |
| 19b6f52483c6 | **rc 0**, uncaughtAfterTerminate [], resolved "fn-returned", advisory after [] | rc 0, 0 uncaught, the same | rc 0, 0 uncaught |

- After all probes, `pg_locks` advisory count = 0.
- This matches the READY, including "my log line appears twice".

**Q2. The error listener.** Read at the head (`creditLock.ts:54-91`) and measured.
- **Attached only while the lock holds the client.** `client.on` sits after `getClient` and before `try`; `removeListener` is first in `finally`, before `release`. E6: a clean call leaves `listenerCount('error')` = 0.
- **What it logs.** Real PG gives `{errorType:'DatabaseError', errorFields:[length,name,severity,code,…,routine]}`, then `{errorType:'Error', errorFields:[]}`. These are names only: no message, no values, no customer id. E3 pins this with a planted detail and message text. N4, N5 and N6 are killed.
- **The client is destroyed.** The listener sets `broken`, and `release(true)` follows. In `pool-after`, the pool total is 0 after the drop (the client was destroyed, not reused), and the next call ran ("ran").
- **The ledger state after a mid-operation drop (real PG, real `creditGrants.ts`; `out-pg-head-ledger-drop*.log`).**
  - The commission's premise ("'failed' not 'granting'") is not what the code does, and the code is right.
  - **Drop, and the Stripe write lands:** the call resolves 15, and the row is **`'granted'`**, balance 15. Stripe's redelivery returns null, the row stays granted, balance 15. No second credit. Marking it 'failed' here would double-credit.
  - **Drop, and the Stripe update fails:** the call rejects, the row is **`'failed'`**, balance 10, and the ROLLBACK failure is logged. The redelivery credits once, giving **`'granted'`**, balance 15.
  - Neither case leaves `'granting'`. 0 uncaught, 0 advisory locks.
  - At e17704 with a recording handler, the ledger also ends 'granted'. Without a handler the process exits (Q1), which is the stuck-'granting' path gate 355 read.
  - Residual (read, unmeasured): if the database is wholly unreachable, `MARK_GRANTED` fails and the row stays 'granting'. That is KS-1933's documented, logged residual and is unchanged by this PR.

**Q3. Red-proof and mutants.**
- The new file on e17704c1a432's `creditLock.ts`: **5 failed, 2 passed. All 5 are AssertionError** (E1, E2, E3, E4, E7). E5 and E6 pass, as the READY says. At the head: 7/7. (`out-red-E-{old,head}.json`)
- My mutants per changed line, against the whole billing suite (`out-mutants.txt`). Each was restored and its sha256 asserted; porcelain ended at 0.

| Mutant | Result | Cells that failed |
|---|---|---|
| N1 no listener | KILLED | E1 E2 E3 E4 E7 |
| N2 no `broken` | KILLED | E4 |
| N3 never removed | KILLED | E6 |
| N4 raw error logged | KILLED | E3 |
| N5 message logged | KILLED | E3 |
| N6 no log | KILLED | E3 |
| N9 `release()` (gate 355's M7) | KILLED | E4 E5 |
| N7 `once` | **SURVIVED; crashes on real PG** | G361-2235-2 |
| N8 removed after release | SURVIVED | benign |
| N10 attached after LOCK | SURVIVED | benign |

- Every kill was an AssertionError. Gate 355's M7 is now pinned. Its M4 (key namespace) still SURVIVES, 0 of 400 failed, unchanged.

**Q4. The old KS-1935 file's fixture change.**
- The diff is only an `EventEmitter` import, two comments, `return {` changed to `return Object.assign(new EventEmitter(), {`, and `};` changed to `});`. 0 `expect` lines changed.
- `query` and `release` do not collide with EventEmitter members. Nothing emits on this fake.
- Measured:
  - new fake on the unfixed lock: 16/16;
  - old fake on the unfixed lock: 16/16;
  - new fake at the head: 16/16;
  - **old fake at the head: 12 failed, 4 passed** (`TypeError: client.on is not a function`). The change was necessary, and it weakens nothing.

**Q5. The billing suite, interleaved dev and head twice, then the merge twice.** Node v26.8.1, vitest 4.1.12.

| Tree | Run 1 | Run 2 |
|---|---|---|
| develop 96aa5fc17c60 | 21 files, 395/395, rc 0 | same |
| head 19b6f52483c6 | 22 files, 400/400, rc 0 | same |
| **merge a59c4e53e5f6 (billing 5f0230534cd7 = the merge on 9bb6c98b2c47 too)** | **23 files, 418/418, rc 0** | same |

- 395 + 16 + 7 = 418.
- The ks1933, ks1934 and ks1935 files on the merge: 63/63.
- Develop's count is 395, not the READY's 377, because develop gained KS-1934.

**tsc and eslint.**
- `tsc --noEmit -p services/billing/tsconfig.json`: rc 0 at develop, at the head, and at the merge.
- Planted TS2322: rc 2. The file was moved out and porcelain is 0.
- eslint (Dev flat config) on the 3 changed .ts files: 0 errors, 0 warnings.
- The planted no-fallthrough: 1 error.

**Q6. Gate 355's other findings.**
- The delta does not touch pool size, lock timeout, the key, or the routes.
- **G355-2235-2 stays a filing, unchanged.** The READY lists it as candidate (c).
- G355-2235-3 is unchanged.
- From G355-2235-4: M7 is now killed, and M4 still survives.

## HOW
- Clone at `scratch/clone` (`--reference` to the Blockchain object store, push DISABLED). Worktrees `wt-old` (e17704), `wt-head` (19b6f5), `wt-dev` (96aa5f) and `wt-merge` (local merge a59c4e). Each had `npm ci --ignore-scripts` and a shared build, rc 0.
- Scripts: `setup.sh`, `install.sh`, `mergewt.sh`, `mt.sh`, `suites.sh`, `mutants.py`, `lint.sh`, `pgprobe.sh`, `probe/g361_pg.ts`.
- GitHub: `gh api` GET only, with the Blockchain GH_CONFIG_DIR. No Stripe call. No writes outside this folder.

## NOT TESTED (UNMEASURED)
- Real Stripe; a booted billing service; a real webhook delivery.
- Azure PostgreSQL (idle-in-transaction timeout, failover), PgBouncer, a network-partition drop (I tested only `pg_terminate_backend`).
- Node 24; a container build; the preflight legs; the docs-fragments checker; the PR body and the KS-1935 ticket comment (not read).
- The end-to-end lost update under G361-2235-1 (the overlap is measured; the wrong balance is read).
