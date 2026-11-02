# QA Gate 127 verdict: Secuura/Distributed_Secuura PR 1945 (KS-1943, originate db.ts `withPlatformScopeTransaction` + gdprService.ts `enforceRetentionImpl` one unit per policy), TIER 1 (data-destruction path)

## BLUF
**GO WITH NOTES. Nothing has to be fixed before merge.**
- **What I ran:** the REAL `enforceRetention` with the REAL `db.ts`, through Prisma 7 + adapter-pg (single-tenant, "st") and the real `TenantPoolManager` (multi-tenant, "mt"). It ran on a real PostgreSQL 15 that I started myself (`g127-pg`), initialised the compose way with all 58 repo migrations (58/58 applied), as the non-superuser `secuura_app`. audit_logs has RLS forced there. I ran base (0e3a9b65cdd6 product bytes) and head (4646d14c) in both modes. Failures were injected with real database errors: BEFORE triggers at each statement, plus DEFERRABLE INITIALLY DEFERRED constraint triggers that fail at COMMIT. A per-statement trace trigger recorded txid, backend pid, the bypass GUC and the session user.
- **(a) Atomicity:**
  - **Head, 10/10 failure cells per mode, both modes:** every cell leaves the failed policy with NONE of the three effects (`-/-/-`), and the other 4 policies are complete.
  - **Base reproduces G117-F2 exactly:**
    - a failed log INSERT, or a commit-time failure on the log row, leaves `DATA/-/-` (rows deleted or anonymised, no log row);
    - a failed stamp, or a commit-time failure on the stamp, leaves `DATA/LOG/-`.
  - **Score:** base 3/11, head 11/11, in st AND mt (logs/judge_pg.log).
- **(b) Isolation:** in every cell, at base and head and in both modes, the other four policies committed completely and the sweep continued. A failed unit never rolled back another policy's unit.
- **(c) Nothing newly destroyed:** I seeded both sides of each cutoff (the 89/91, 364/366 and 2554/2556-day boundaries), NULL-user rows that the anonymise predicate excludes, and two tenants on the FORCED-RLS audit_logs. After a healthy sweep, the full row snapshots are **identical base vs head in st AND in mt**, and identical st vs mt. The changed row ids are identical per table (5/6/4/3/4), and log rows and records_affected are identical.
- **Trace:** the platform bypass GUC is `platform_admin` on all 15 traced statements, as `secuura_app`, in every version and mode. At head, each policy's 3 statements share **1 txid**; at base they used **3 txids** (one connection).
- **(d) Add-only:** db.ts is +56/-0. Every pre-existing line is byte-identical and in place (diff rc 0 after removing the 2+54 added lines). The helper has one product caller (gdprService). db.ts's other 22 non-test importers are untouched by the PR.
- **(e) The timeout:** a unit that runs out deletes nothing, and afterwards there is no idle-in-transaction backend and no held lock (measured). **But the "5000 ms" is Prisma's interactive-transaction timeout, not a statement timeout, and it exists in st only.**
  - It did not cancel a blocked DELETE. The DELETE held its row/tuple locks for 7.5 s+, and the sweep stalled until the lock was released, at about 9.06 s.
  - mt has no timeout at all.
  - Both are **identical at base**. See G127-F1. This is not a regression and not a block.
- **(f) logs.push after commit only:** a rolled-back policy is never returned at head. At base, the stamp and stamp-commit cells returned a policy whose stamp failed. Mutants M3/M3b, which push before commit, are killed.
- **(g) Logging rule:** the PR adds no log line. It adds one constant refusal `Error` and a rethrow.
- **Re-measure:**
  - red-first: 19/19 RED cells fail by assertion at base, and 9/9 controls pass;
  - green: 41/41 three times;
  - originate suite: 184/2189 to 186/2224, with 0 vanished, 35 new and 0 changed;
  - tsc with tests: 0 errors to 0 (247 to 249 files), planted control caught;
  - eslint: 0 on the 5 changed .ts files, planted control caught;
  - docs-fragments: clean, 4/4 planted defects caught;
  - merge-tree onto develop 1584c0f0: clean, 0 shared paths.
- **Mutants:** 17 run, **17 KILLED by assertion** (two needed a compiling re-form, below). That includes the four commissioned ones: the log INSERT outside the unit, the stamp dropped from the unit, push before commit, and the timeout dropped.

## Heads
- START (logs/head_start.log, 2026-11-02T12:24:34Z): PR head `4646d14c105c7efe8210eb285d7c50773fb916c0` (matches the commission), develop `1584c0f0ff808fddf35245bee41b6b5f9231054c` (matches). One commit; its parent is the merge-base `0e3a9b65cdd632fbc1783257c6cb9833934e1404` (matches the claimed base).
- MID (logs/head_mid.log, 12:40:52Z) and END (logs/head_end.log, 12:42:36Z): both refs unchanged. Local HEAD = PR head, working tree clean, and product sha256 equals the head blob (db `7533ae49777c`, gdpr `a1288b0645d3`).
- The product files, routes/gdpr.ts, retentionScheduler.ts and shared tenant-guc.ts are blob-identical at 0e3a9b65 and at develop 1584c0f0, so "base" means the same bytes against both.
- Diffstat (logs/diffstat.log, three-dot): 7 files, +680/-24, exactly as claimed:
  - db.ts +56
  - gdprService.ts +35/-24
  - the two new tests +204 and +342
  - the KS-1938 test +1 (the pass-through mock line the author declared)
  - two fragments, +22 and +20
- **PR body not read directly.** No Secuura gh login is used here. I worked from the author's READY mail (evidence/ready_e29_pr1945.txt), the commit and the fragments.

## FINDINGS
- **G127-F1 (RECOMMENDED; wording + a design card; base = head, measured)**
  - **What the approval said:** Wednesday's approved design reads "a per-unit statement timeout default 5000 ms".
  - **What is built:** Prisma's default interactive-transaction timeout. It is single-tenant only. It is checked when the NEXT query or the COMMIT is issued, so it does not cancel an in-flight statement.
  - **Measured** (logs/pgto_*.txt), with a superuser holding `FOR UPDATE` on the expired user_sessions rows:
    - st: the DELETE sat `active / Lock:transactionid` for 7.5 s+, holding RowExclusive and tuple locks, and the sweep settled only after I released the lock, at about 9.06 s. Then Prisma's "A query cannot be executed on an expired transaction" fired and the unit rolled back: 3 rows remaining, no log row, no stamp, other 4 policies stamped. Afterwards there were 0 idle-in-transaction backends and 0 app locks.
    - mt: no timeout. The unit waited, then COMMITTED after the release (3 deleted, log row, stamp).
    - Base behaves the same in both modes (at base st the per-statement transaction fails at its COMMIT: "A commit cannot be executed on an expired transaction").
  - **So:** the fail-closed property holds (a timed-out unit writes nothing). The timeout does NOT bound lock-hold time or sweep stall, and in mt it does not exist.
  - **Ask:** the PR body and fragment should say "Prisma interactive-transaction timeout (single-tenant only; does not cancel a blocked statement; multi-tenant has none, as before)".
  - **If a real bound is wanted:** that is a card, not this PR. For example `SET LOCAL statement_timeout` / `lock_timeout` right after BEGIN in both branches. That is a behaviour change in mt, so it needs a ruling.
- **G127-F2 (INFO, disclosed by the author)** st liveness: a policy whose unit exceeds 5 s does all its work and then rolls back on every run, so it never progresses. Base already had this for the DELETE alone; head adds the INSERT and stamp (milliseconds) to the same budget. Live table sizes are unmeasured.
- **G127-F3 (INFO)** Red-first for `ks1943-platform-scope-transaction-helper.test.ts` is by COMPILE at base (TS2339, the helper does not exist), not by assertion. That is expected for a new export. The helper's cells are pinned instead by mutants M4-M10 (all killed by assertion).
- **G127-F4 (INFO, pre-existing, out of scope)** KS-1944 / G117-F1 is unchanged: the route still answers 200 "complete" when a policy fails, now with the rolled-back policy correctly absent from `deletionLog`. Separately, `SELECT * FROM data_retention_policies` has no ORDER BY, so policy order is heap order, and I observed it differ between runs (base and head alike). This is harmless for correctness.
- **G127-F5 (INFO, edge)** The helper gates on `MULTI_TENANCY && tenantManager`, while the module `prisma` gates on `MULTI_TENANCY && defaultProxy`. They differ only if `tenantManager.init()` throws inside initDb, after the assignment at db.ts:435. In that case the sweep would use the pool path while other statements use Prisma. It is only reachable on a failed boot. Read, not run.
- **G127-F6 (INFO, pre-existing, base = head)** The readable-error branch still logs `err.message`. Measured, that includes Prisma's "Invalid `prisma.$executeRaw()` invocation ... Raw query failed. Code: P0001. Message: ..." text and the DB error text. Same as G117 Q7; no new line.
- **G127-F7 (INFO)** The KS-1938 test's db mock passes the unit through (`fn(prisma)`), so that file cannot see rollback. The author declared this.

## Q1. Atomicity, isolation, nothing newly destroyed (real PostgreSQL; read + run)
**Code (head).** The helper is in db.ts:395-418.
- It refuses unless `isPlatformScope()`.
- **mt:** `getDefaultPool().connect()`, then `BEGIN`, then `applyTenantGuc` (the bypass `set_config`, is_local), then `fn(createPoolProxy(client))` (a client with `.release`, so statements go to `client.query` on the open transaction), then `COMMIT`. On a throw: `ROLLBACK` (best-effort), rethrow, and `release` in finally.
- **st:** `getPrismaClient().$transaction(tx => set_config bypass; fn(tx))` on the REAL client, not the GUC proxy, so nothing nests.
- **gdprService:** each policy's three statements run on `tx` inside the helper, and `logs.push` happens after the helper resolves. The seven SQL templates are byte-identical to base (the head diff re-indents only the JS around them).

**Probe.** Files: scripts/pgproof_g127.mts, scripts/run_pg.sh, scripts/swap.sh (product swap with sha256 assert), judged by scripts/judge_pg.py into logs/judge_pg.log. The seed is deterministic md5 ids; failures are real `RAISE EXCEPTION` triggers; state is read on an independent superuser connection.

| failure point (both user_sessions = DELETE kind and audit_logs = anonymise kind, FORCED RLS) | base st | head st | base mt | head mt |
|---|---|---|---|---|
| none (healthy) | all 5 complete | = base | all 5 complete | = base |
| F1 at the DELETE / anonymise | -/-/- | -/-/- | -/-/- | -/-/- |
| F2 at the log INSERT | **DATA/-/-** | -/-/- | **DATA/-/-** | -/-/- |
| F3 at the stamp | **DATA/LOG/-** (returned) | -/-/- | **DATA/LOG/-** (returned) | -/-/- |
| F4 at COMMIT, deferred trigger on the stamp row | **DATA/LOG/-** (returned) | -/-/- | **DATA/LOG/-** (returned) | -/-/- |
| F5 at COMMIT, deferred trigger on the log row | **DATA/-/-** | -/-/- | **DATA/-/-** | -/-/- |

- In every cell, the other 4 policies are complete, and `enforceRetention` resolved; it never rejected.
- (c) Healthy-sweep snapshots (ids plus every non-time column, including the anonymised columns): base == head (st) True, base == head (mt) True, st == mt True. Rows left per table: 3/11/2/6/2.
- The "before DELETE" point: the unit's first statement is the bypass `set_config`. I did not fault it separately (no trigger can). F1 fails the first WRITE, and PostgreSQL's per-statement atomicity covers the rest.

## Q2. Add-only (d)
logs/addonly.log:
- db.ts numstat is 56/0, with 0 removed lines (control: 54 added non-blank lines).
- `diff base <(head minus lines 16-17 and 366-419)` gives rc 0: `createPoolProxy`, `getPrismaClient`, `wrapPrismaWithTenantGuc`, `prisma`, `getRequestPrisma`, `withTenant` and `initDb` are byte-identical and in place.
- The only module-load change is a second named import from `@secuura/shared` (`applyTenantGuc`, already exported and used by the shared module). Its use is lazy, inside the helper.
- `withPlatformScopeTransaction` is referenced only in db.ts, gdprService.ts and three test files (control: `withTenant(` 58 refs).
- 22 non-test files import db.ts; the PR changes only gdprService.ts among them.
- The whole originate suite is unchanged per cell (0 vanished, 0 changed).

## Q3. Timeout (e), locks and open transactions
See G127-F1. logs/pgto_{head,base}_{st,mt}.{txt,json}, from scripts/pgtimeout_g127.mts with a 9 s lock hold. In all four runs, after the release plus 3 s, the secuura_app backends were `idle` with 0 idle-in-transaction and 0 app locks.

## Q4. logs.push after commit (f)
- **Real PG:** at head, no failed policy appears in the returned list in any cell (st and mt). At base, the F3/F4 cells returned the policy, because its delete and log really committed.
- **Units:** T2 and T9b assert this.
- **Mutants:** M3 (an extra push inside the unit) and M3b (push inside, post-commit push removed) are both killed.

## Q5. Re-measure (Node v26.8.1 only; nothing measured on Node 24; load1 7-19 over the run, shared host, maxWorkers=3)
- **Green:** the three files (the 2 new ones plus the KS-1938 one) pass 41/41 three times (logs/green_head_{1,2,3}.json).
- **Red-first at base product, sweep file:** 28 cells; **19 RED fail by `expect`, 9 controls pass** (logs/red_base_sweep.json). Helper file: TS2339 compile failure (G127-F3). The KS-1938 head test on the base product passes 6/6.
- **Whole originate jest:** base without the new files gives 184 files and 2189/2189; head gives 186 files and 2224/2224. 0 vanished, 35 new (28+7), 0 changed (logs/suite_compare.log). This matches the author.
- **tsc:**
  - plain: rc 0 at both versions;
  - including tests: base (new files parked) 0 errors over 247 originate src files, head 0 errors over 249;
  - planted control: `TS2322` + `TS6133`, rc 2, restored byte-identical.
- **eslint:** the 5 changed .ts files give 0 problems, rc 0. The planted file gives `no-debugger` error and `no-unused-vars` warning, rc 1.
- **docs-fragments** (logs/frag_outer.log): rc 0 "flow 117 legacy + 91 new, cheat 112 legacy + 91 new". The planted defects each give rc 1: flow unclosed `<div>`, flow `<!--n-->.` removed, cheat unclosed `<div>`, cheat `</table>` corrupted. All four were restored by sha, rc 0 after.
- **Quoted, not re-run:** the hook line "PREFLIGHT INCOMPLETE - 13/16 legs ran, 3 SKIPPED. Nothing failed." (legs 3, 4, 8); the author's merged-tree suite 198/2318.

## Q6. Mutants
scripts/mutants.py; product only, tests untouched, sha256-restored after every run (all `restore True`). Results in logs/mutants_outer.log, mutants_m5c.log and mutants_m5d_m8b.log. The unit cells come from the 3 files; the real-PG column is the 11-cell matrix.

| Mutant | unit cells | real PG |
|---|---|---|
| M1 log INSERT on `prisma` (outside the unit) | KILLED, 24 cells (T1, T2, T3...) | st 7/11, mt 7/11 (F3, F4 red) |
| M2 stamp on `prisma` (outside the unit) | KILLED, 24 | st 9/11, mt 9/11 (F5 red: stamp persisted, data rolled back) |
| M3 push inside the unit (extra) | KILLED, 26 | st 4/11 |
| M3b push inside, post-commit push removed | KILLED, 24 | - |
| M4 timeout dropped (`{ timeout: 600000 }`) | KILLED, H2 | timeout cell: st now deletes after the lock is released (remaining 0, returned) |
| M5a / M5d helper returns `fn(prisma)` (no transaction) | M5a killed by compile only; **M5d (compiles) KILLED H2 H4 H5 H6** | st 3/11, mt 3/11 |
| M5b / M5c sweep calls `fn(prisma)` inline | M5b killed by compile only (unused import); **M5c (compiles) KILLED, 19+** | st 3/11 |
| M6a st: error swallowed inside the unit | KILLED H3 | 11/11 (PostgreSQL turns COMMIT of an aborted transaction into a rollback) |
| M6b mt: error swallowed, COMMIT sent | KILLED H5 H6 | 11/11 (same reason) |
| M7 st: bypass `set_config` dropped | KILLED H2 | st 2/11 (anonymise touches 0 rows under FORCED RLS) |
| M8 / M8b mt: `applyTenantGuc` dropped | M8 killed by compile only; **M8b (compiles) KILLED H4 H5** | mt 2/11 |
| M9 scope refusal removed | KILLED H1 x2 | - |
| M10 mt: no ROLLBACK on throw | KILLED H5 | mt 5/11 (an aborted transaction is released into the pool and poisons later units) |

No mutant survived. M6a and M6b survive on real PostgreSQL only by server semantics; the unit cells kill both.

## Q7. merge-tree (logs/merge_tree.log)
- **Onto develop `1584c0f0`:** rc 0, tree `5fe9665bed60...`, clean.
- **Shared paths:** develop has 29 new paths since the base, 0 shared with the PR (control: 7 against itself).
- **Merged tree vs develop:** exactly the PR's 7 paths, +680/-24, and every merged blob equals the PR blob.
- **Develop's moves:** the 5 moved commits (KS-1868 x3, KS-1939, KS-1940) contain 0 references to gdprService, enforceRetention, withPlatformScope or retentionScheduler (control: 3 in gdprService itself).
- I did not run the suite on the merged tree.

## Q8. Kam's ks1346 logging rule
- **Added product lines** naming logger/console/throw: the refusal `throw new Error('withPlatformScopeTransaction refused: no platform scope is active (KS-1943)')` (a constant, no value) and `throw err` (a rethrow). No new logger call; 0 removed (logs/logging_rule.log).
- **Existing lines:** the per-policy catch is unchanged from PR 1935: an unreadable value logs a constant, and a readable one logs `err.message` (pre-existing, G127-F6).

## Notes for the PR body
- **G127-F1:** correct the 5000 ms wording (Prisma interactive-transaction timeout, single-tenant only, does not cancel a blocked statement; multi-tenant has none, as before). Card candidate if a real bound is wanted. RECOMMENDED.
- **G127-F2, F3, F4, F5, F6, F7:** INFO.
- None is FIX-BEFORE-MERGE.

## NOT TESTED
- the real PR body text
- pgbouncer in the path
- a booted originate
- the real route and scheduler on real PG: the route and scheduler are run only in the author's unit cells (T9/T10, green here); read from source
- Node 24
- CI, the four platform suites and the pre-push hook legs: quoted only
- the suite on the merged tree
- per-tenant-database mode (`perTenantDb=true`): the sweep covers the default pool's database only, as before
- a fault at the bypass `set_config` itself
- a lost COMMIT acknowledgement (committed at the server, error at the client): reasoned only; the log row would exist in the database and the in-memory return would omit it
- concurrent sweeps (route plus scheduler at once): reasoned, no lock cycle (each unit locks its own table's rows and then its own policy row)
- live table sizes for G127-F2

## Housekeeping
- **My container:** `g127-pg` (postgres:15-alpine, label gate=g127, loopback port 60477), started 12:28Z and stopped and removed at 12:42Z.
- **Its two anonymous volumes:**
  - `58857344…`: PG data; confirmed mine by `postmaster.opts` = `postgres -c max_connections=200`.
  - `6642fab7…`: empty; created by my first `docker run`, which failed at mount time and whose container I removed.
  - Both removed (logs/pg_teardown.log).
- **Not touched:** `s-e29-pg`, `gate65-pg` and `s-w13-pg`.
- **Leftover in my clone:** the bind mount left an empty `repo/Blockchain/Dev/docker/init/platform/` directory (untracked, invisible to git).
- **Credentials:** the throwaway DB passwords were random and lived only in `/tmp/g127/pg/env` (outside this workdir), never in a log.
- **Background runs:** all of them completed (install, jest chain, mutants, monitor); nothing is left running.

## Tier
**TIER 1 confirmed.** The PR changes the transaction framing of the GDPR retention sweep, which deletes and anonymises rows across tenants under the platform scope.
