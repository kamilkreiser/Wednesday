# QA Gate 117 verdict: Secuura/Distributed_Secuura PR 1935 (KS-1938, originate services/gdprService.ts enforceRetentionImpl, two catch sites), TIER 1 (data-destruction path)

## BLUF
**GO WITH NOTES. Nothing has to be fixed before merge.**
- **What I ran:** the REAL `enforceRetention` and the REAL `POST /api/gdpr/retention/enforce` handler, which includes the real `fail500`. I ran them on a real loopback listener, with only prisma replaced by a recorder. The recorder logs every tagged-template statement with its full SQL text and its values. Auth and the logger were stubbed.
- **The grid:** 4 policies (user_sessions delete, audit_logs anonymize, share_records delete, and one unknown type that only gets a stamp). 11 failure points plus a no-failure control. 7 thrown values: an Error, a string, and 5 unreadable shapes. Every cell went through the function and through the route, at base and at head: 156 cells per version.
- **Q1 result:** the comparator found **532 of 532 checks equal** (logs/judge.log). For every unreadable value at every failure point, head matches what an ordinary Error gets at base. That holds byte-for-byte on statements (SQL text, values, order), on the set of writes that succeed, on what the function returns, and on the route's status and body. Readable values (an Error, a string) behave identically at base and at head.
- **Q2, the headline: NO.** No path deletes or anonymises more than an ordinary Error already does today. The only writes head adds over base are the later policies' statements. An ordinary Error already runs exactly those, today and at head (the HEAD-ONLY list in logs/judge.log is a subset of the base-Error writes, checked per cell). No predicate reads `reason` or `last_enforcement_at`, and the cutoff is `Date.now() - retention_period_days`. So a stamp that is not written cannot widen the next run.
- **Re-measure:** red-first 4 of 6 by assertion; green 6 of 6, three runs; whole originate suite 180/2163 to 181/2169, with 0 vanished and 0 changed; tsc with tests 0 to 0; eslint 0; docs-fragments clean, and 4 planted defects caught; merge-tree clean onto develop at both commission and end.
- **Mutants:** 16 of 18 killed. The 2 survivors are the known readable-non-Error branch (G117-F3).

## Heads
- START (logs/head_start.log, 2026-11-02T08:31:03Z): PR head `9af830dae73a547ab1797c669cf3fb61a9e984e7` (matches the commission), develop `66a36e3f777d082c98c015348d5239ce227c9f83` (matches). One commit. Its parent is the merge-base `8f313815f415c65849210f5d3e30cae44d15a516` (matches the claimed base).
- END (logs/head_end.log, 08:44:16Z and 08:44:47Z):
  - PR head `9af830da...` is unchanged; local HEAD is the same; the working tree is clean; the product sha256 `e4ce78f26737...` equals the head blob.
  - **develop MOVED** to `91ccb1553f027c712d0d0c2d93871fd46f67dffa`, 2 commits: KS-1413 start banners and KS-1725 msal locks. Neither touches originate. I re-ran merge-tree onto it (Q6).
- Base product sha256 `287eb4302cdd...`. The product file and both callers (routes/gdpr.ts, services/retentionScheduler.ts) are byte-identical at 8f313815, 66a36e3f and 91ccb155 (git diff --quiet, rc 0).
- Diffstat (logs/diffstat.log, three-dot): 4 files, +188/-2, exactly as claimed:
  - gdprService.ts +14/-2
  - the new test +136
  - flow fragment +20
  - cheat fragment +18
- **PR body not read directly.** No gh login for Secuura is used here. I worked from the author's READY mail (evidence/e28_ready_pr1935.txt), the commit message (evidence/commit_msg.txt) and the two fragments.

## FINDINGS
- **G117-F1 (INFO, pre-existing, confirmed, out of scope; the author's unfiled candidate)**
  - **What happens:** the manual route answers `200 {"success":true,"message":"Retention enforcement complete. 0 data types processed.","deletionLog":[]}` when the policy SELECT fails. Measured for an ordinary Error and a string at base and head, and for every unreadable value at head.
  - **Same thing mid-sweep:** when a policy fails mid-sweep, the route still says "complete" with `success:true`, and the count simply omits that policy. Example: an Error on DELETE user_sessions answers "2 data types processed".
  - **The count is not a policy count:** `logs.length` counts only policies with affected > 0 whose deletion-log INSERT returned a row. "0 data types processed" therefore cannot tell "nothing expired" from "the sweep could not read its policies".
  - **Scope:** this PR moves the unreadable SELECT case onto that existing answer. It is worth a card: the route could report failed policies, or answer 500 or 207. Not a merge block.
- **G117-F2 (INFO, pre-existing, base = head, measured)** The DELETE or anonymise, the deletion-log INSERT and the stamp are three autocommit statements, with no transaction. When the INSERT fails (any value, base or head), the rows are already deleted or anonymised and **no data_deletion_log row records it**. Cells `INSERT log <type>`: the DELETE succeeded, there is no log row, and the stamp is skipped. This is a GDPR audit-trail gap that ordinary Errors already reach. This PR neither causes nor widens it, but it is the real data-destruction question beside this one.
- **G117-F3 (LOW, test gap)** M6 (the readable non-Error branch `String(err)` replaced by `'x'`) SURVIVES at both sites. No committed cell throws a thrown string or other readable non-Error. My probe shows strings unchanged base to head, but nothing pins it. This is the same gap as G90-F3. An optional fix is one string-throw control per site.
- **G117-F4 (LOW, test gap)** No committed cell drives the route, and no committed cell fails a stamp or a deletion-log INSERT. The committed cells fail only `DELETE user_sessions` and `SELECT policies`. The 500-to-200 change and the INSERT/stamp failure points are pinned only by this gate's uncommitted probe (scripts/g117_probe.test.ts, a ready template).
- **G117-F5 (INFO, wording)** The fragment cites the catches as ":499" and ":503". Those are base line numbers; at head the log lines are :505 and :515. "The other 17 unguarded reads": the `instanceof Error ? / err?.message` regex over head finds 17 lines, 2 of which are the new guarded copies. That leaves 15 unguarded of those forms (logs/other_reads.log). The author may count other forms too. Either way, none of them is on the sweep.
- **G117-F6 (INFO, base was worse than the brief says, measured)** The brief's "today" for the shape `getterThrowsRevoked` (an Error whose message getter throws a revoked Proxy) is wrong in a way that matters:
  - **At base:** at EVERY failure point the inner catch throws, then the outer catch throws again, and `enforceRetention` REJECTS. The manual route answers **500 after some policies had already deleted or anonymised rows**. For example, at `STAMP p3`, 8 writes had been committed. The scheduler logs "Scheduled enforcement failed".
  - **At head:** it resolves, as an ordinary Error does.
  - **The other unreadable shapes at base:** the inner failure resolves with the later policies skipped. The SELECT failure is 500.
  - **Either way, head is no worse:** both are equal to an ordinary Error.
- **G117-F7 (INFO)** docs-fragments `check` prints the cheat ADVISORY at line 6235 both clean and after restore. That is the same pre-existing advisory as G90-F7, not this PR.

## Q1. The behaviour question (in full)
**Code (head).**
- `enforceRetention` = `runWithPlatformScope(() => enforceRetentionImpl())`. That is a plain AsyncLocalStorage run (packages/shared/src/db/tenant-guc.ts:102) and adds no catch.
- The Impl does the following:
  - SELECT policies WHERE auto_delete.
  - Per policy, inside a try: `cutoff` is computed outside the try; then the type-specific DELETE or anonymise UPDATE; if affected > 0, the deletion-log INSERT ... RETURNING; then the stamp UPDATE.
  - The inner catch logs and continues. The outer catch logs, and the function returns `logs`.
- Callers:
  - Route `POST /retention/enforce` (routes/gdpr.ts:625-635): SYSTEM_ADMIN only; 200 with `logs.length`; its catch goes to `fail500`, which is KS-1772 guarded.
  - Scheduler `runEnforcement` (retentionScheduler.ts:40-58): sums `recordsAffected`, logs; its catch is already guarded (KS-1868 p3).

**The probe.** Files:
- scripts/g117_probe.test.ts, run by scripts/probe.sh: copied into the clone, then moved to logs/_quarantine. NOT part of the PR.
- Results in logs/probe_{base,head}.json, judged by scripts/judge.py into logs/judge.log and logs/probe_table.log.
- `Date.now` is frozen, so the cutoff values compare byte-for-byte.
- Unhandled rejections: 0 at both versions.

**Today (base) vs after (head), function and route** (writes = succeeded DELETE/ANON + INSERT log + STAMP, out of 10 with no failure):

| thrown value | failure point | base | head | ordinary Error (base = head) |
|---|---|---|---|---|
| Error | any | as right column | as right column | per-policy: later policies run (7-9 writes), resolves, route 200; SELECT: 0 writes, resolves, route 200 "0 data types processed" |
| string | any | identical to head (statements, outcome, log text) | identical | (same pattern as Error) |
| revokedProxy / getterThrowsError / protoTrapThrows / toStringThrows | policy k statement, INSERT or STAMP | the inner catch throws, the outer catch logs the secondary error, **later policies skipped**, resolves, route 200 | == ordinary Error | |
| same four | SELECT policies | **rejects**, route **500** INTERNAL_ERROR (fail500 logs the secondary message) | resolves [], route **200** "0 data types processed" | == |
| getterThrowsRevoked | any | **rejects** (the outer catch throws too), route **500**, writes before the failure already committed | == ordinary Error | |

- **Log lines:** at head, an unreadable value logs `Retention enforcement failed {dataType, error:"unreadable thrown value"}` or `Retention enforcement error {error:"unreadable thrown value"}`. At base no inner line was logged; the outer line carried the secondary TypeError's text.
- **Author's claims, each verified:**
  - (a) No statement or predicate changes: **TRUE**. The product diff touches only the two catch bodies (logs/product_diff.log), and every head statement equals base for readable values and the base-Error statements for unreadable values.
  - (b) Later policies now run after an unreadable failure: **TRUE**.
  - (c) The route answers 200 instead of 500 on a SELECT failure: **TRUE**.
  - (d) Ordinary Errors and strings are unchanged: **TRUE**.
  - One addition the author did not state: for `getterThrowsRevoked`, the route also goes 500 to 200 at the per-policy points (G117-F6).

## Q2. More data deleted than an ordinary Error? **No.**
- **Statements:** for every unreadable cell, `writes(head) == writes(base, Error)` as a list and `set(writes(head)) <= set(writes(base, Error))`. 0 failures out of 532 checks.
- **Predicates:** they are built only from `cutoff` (`Date.now()` and `retention_period_days`) and `policy.id`. `reason` goes only into `logger.error`; no value is coerced into SQL.
- **Stamps:** `last_enforcement_at` is written only, never read. `git grep -i last_enforcement_at` over the whole tree at pr1935 (logs/last_enforcement_refs.log) finds only the three schema column definitions (init.sql, 01-schema.sql, 001_initial-schema.sql), the stamp UPDATE (gdprService.ts:495), and comments in the PR's own test and fragments; no code, trigger or view reads it. A missing stamp therefore cannot make a policy re-run with a wider predicate.
- **What was stopping the later DELETEs at base:** the crash of the log call inside the catch, not a guard. It was an accident, and the designed contract (the inner catch, then continue) is what an ordinary Error already gets. Head runs MORE than base for the unreadable value only: the later policies' policy-mandated retention deletes, exactly as for an ordinary Error.
- **Reachability:** prisma `$queryRaw`/`$executeRaw` reject with Prisma error classes (Error subclasses with data `message`). The parameters are server-built. No caller chooses the rejection value; the route is SYSTEM_ADMIN and the scheduler has no caller at all. Defence-in-depth, as at every other KS-1868 site.

## Q3. The two callers
- routes/gdpr.ts and services/retentionScheduler.ts are **not in the PR** (git diff 8f313815..pr1935: rc 0) and are **unchanged on develop since the base**, through 91ccb155 (rc 0).
- **Route:** it reads only `logs.length` and `logs` and answers 200 on resolve. Head's resolve-with-[] on a SELECT failure gives 200 "0 data types processed", the same as an ordinary Error (G117-F1).
- **Scheduler:** it reduces `recordsAffected` over the resolved list. A resolve with [] or a partial list logs "Enforcement complete ..." exactly as after an ordinary Error. Its catch is now reached in fewer cases (base reached it for SELECT/unreadable and getterThrowsRevoked), and it is already guarded. This is read from source, not run: `runEnforcement` is not exported. The function it awaits is the one the probe ran.

## Q4. Re-measure (Node v26.8.1 only; nothing measured on Node 24; load1 ~12-13, shared host)
- **Head, new file:** 6/6, three runs (logs/green_head{,_2,_3}.json).
- **Base product + new file:** 4 failed, 2 passed, rc 1 (logs/red_base.json). R1 to R4 each fail with `expect(received).toEqual(expected)`; C1 and C2 pass. No compile or import error.
- **Whole originate jest:**
  - base without the new file: 180 files, 2163/2163
  - head: 181 files, 2169/2169
  - per cell: 0 vanished, 6 new, 0 changed
  - the author's figures re-measure exactly
- **tsc:**
  - plain: rc 0 at both versions
  - scratch config including tests: 0 errors at both versions; originate src files in the program 243 then 244 (the author reports 271 then 272 with a different config; the delta of +1 agrees)
  - planted control: `TS2322` + `TS6133`, rc 2, restored byte-identical
  - leg 16 does not cover originate, as the author says
- **eslint:** gdprService.ts plus the new test, 0 problems, rc 0. The planted file raises `no-debugger` error and `no-unused-vars` warning, rc 1.
- **docs-fragments** (logs/frag_outer.log): rc 0, "flow 117 legacy + 80 new, cheat 112 legacy + 80 new". The planted defects each give rc 1: flow unclosed `<div>`, flow `<!--n-->.` removed, cheat unclosed `<div>`, cheat `</table>` corrupted. All four were restored by sha; rc 0 after.
- **Quoted, not re-run:** the hook "PREFLIGHT INCOMPLETE 13/16, nothing failed"; the author's 71/71 recorder (superseded by this gate's 532-check grid).

## Q5. Mutants (scripts/mutants.py; product only, tests untouched, sha256 restored after every run, all `restore True`; logs/mutants_table.log)
18 runs: 16 KILLED, 2 SURVIVED. Every kill was by assertion, and every kill was in that site's own cells.

| Mutant | S1 per-policy catch | S2 outer catch |
|---|---|---|
| M0 revert to base | KILLED R1 R2 | KILLED R3 R4 |
| M1 drop inner try | KILLED R1 R2 | KILLED R3 R4 |
| M2 fallback -> String(err) | KILLED R1 R2 | KILLED R3 R4 |
| M3 rethrow only when unreadable | KILLED R1 R2 | KILLED R3 R4 |
| M4 constant for all values | KILLED C1 | KILLED C2 |
| M5 rethrow every value after the log | KILLED C1 R1 R2 | KILLED C2 R3 R4 |
| M6 readable non-Error branch -> 'x' | **SURVIVED** | **SURVIVED** (G117-F3) |
| M7 log removed | KILLED C1 R1 R2 | KILLED C2 R3 R4 |
| M8 `return logs` (stop the sweep) when unreadable | KILLED R1 R2 | KILLED R3 R4 |

M8 at S1 is the destructive-equivalence mutant: it restores "later policies skipped" for unreadable values only. It is killed by `SWEEP_CONTINUES`.

## Q6. merge-tree
- **Onto develop at commission, `66a36e3f`** (logs/merge_tree.log): rc 0, tree `47f919dd9541...`, clean. 7 commits and 43 paths since the base, of which 0 are shared with the PR (control: 43 against itself). The merged tree differs from develop in exactly the PR's 4 paths, +188/-2, and each merged blob equals the PR blob.
- **Onto develop at end, `91ccb155`** (logs/merge_tree_end.log): rc 0, tree `b88bd4728195...`, clean, 4 files +188/-2, SAME_PATHS. The 2 new develop commits (KS-1413, KS-1725) touch no originate path.
- I did not run docs-fragments on the merged tree. The PR's fragments are new files with unique names.

## Q7. Kam's ks1346 logging rule (log type and field NAMES of a thrown object, never values)
- **Changed lines:** `logger.error('Retention enforcement failed', { dataType: policy.data_type, error: reason })` and `logger.error('Retention enforcement error', { error: reason })`.
- **The new value is compliant:** it is the constant `'unreadable thrown value'`, which carries no value.
- `dataType` is the policy's configured data_type (server data, not a thrown value), unchanged from base.
- **Readable branch, unchanged from base (INFO):** it still logs `err.message` for an Error and `String(err)` for anything else. For a thrown plain object that gives `[object Object]` or a custom `toString()` output, which is not the rule's "type + field names" form (contrast `fail500`, routes/gdpr.ts). This PR does not introduce or widen that; it is the same pre-existing shape as the other 15 reads (G117-F5) and a KS-1346 follow-up, not a block. A Prisma error's `message` can include the failing query text; that is also pre-existing, base = head.

## Q8. Notes for the PR body
- G117-F1: card candidate. The manual route says "complete" with `success:true` when the policy read failed or a policy failed.
- G117-F2: card candidate. The DELETE, deletion-log INSERT and stamp are not in one transaction, so a failed INSERT leaves an unlogged deletion. Pre-existing.
- G117-F3, F4: optional cells. One string throw per site, one route cell, and one failure on an INSERT and on a stamp.
- G117-F5: line numbers :499/:503 refer to the base; at head they are :505/:515. "17 other reads" vs 15 counted by regex.
- G117-F6: add to the deletion-behaviour section that at base a `getterThrowsRevoked` value rejected the whole sweep (route 500) after earlier policies had already deleted. Head resolves as an ordinary Error does.
- None is FIX-BEFORE-MERGE.

## Q9. NOT TESTED
- the real PR body text
- a real PostgreSQL: the statements are recorded by a stand-in, and rows deleted are not modelled; a docker Postgres was not started
- a booted originate
- the scheduler's `runEnforcement`: read from source, not exported
- the real auth middleware: stubbed
- Node 24
- the four platform suites, CI and the pre-push hook legs: quoted only
- the Linear ticket text
- docs-fragments on the merged tree
- whether an unreadable thrown value is reachable in production: reasoned, not measured

## Tier
**TIER 1 confirmed.** The changed catches sit inside the GDPR retention sweep, which issues DELETE and anonymise statements across tenants under the platform scope. The change alters which of those statements run in a given sweep (the later policies now run after an unreadable failure), and it changes the manual route's status. That is a data-destruction path, so the Opus gate applies.
