# QA Gate 146 verdict: Secuura/Distributed_Secuura PR 1962 (KS-1868, transfer approvalWorkflowService.ts: seed catch, boot-probe catch, escalation-sweep catch), TIER 1, round 1

## BLUF
**GO WITH NOTES. Nothing has to be fixed before merge.**

I booted the REAL transfer service as its own Node process for every cell: node + the tsx loader, the real `index.ts`, the real `db.ts` (initDb, runDbReadyHook), the real `approvalWorkflowService`, the real shared `authenticate()` with an RS256 token, and the real Express routes. Only the `pg` module was replaced, by a preload (scripts/pgstub.cjs) that models svc_approval_workflows and svc_approval_step_instances as one in-memory store with a unique `id` and ON CONFLICT upsert, autocommit per statement. 120 cells: base, head, the merged tree, and develop alone (logs/probe_table.log, logs/probe/*.result.json).

In every cell, **head with an unreadable value == base with an ordinary Error**: the same HTTP answers, the same persisted rows, the same process state. The class bar is met at all three sites.

- **Q1 boot: no new outcome.** At base an unreadable probe failure was not fatal and did not cause degraded mode. db.ts's runDbReadyHook caught the rejection, logged "DB ready boot work failed", and skipped only `verifyDelegationDb` (a `SELECT 1` plus a warn, with no seed and no state). Head = base-ordinary.
- **Q2 seed: no new outcome.** Head attempts all 4 workflows, exactly as an ordinary Error does at base. The upsert is idempotent (ON CONFLICT (id)).
- **Q3 sweep: no new outcome at head, and head is strictly better than base.** At base an unreadable value in the sweep **crashed the whole transfer service process** (exit 1, uncaught rejection out of an Express 4 async handler), with rows 1..k-1 already committed. Head answers 200 with partial counts, the same as an ordinary Error. Approval bypass: none. Double escalation: none (measured over two POSTs).

The author's figures all re-measure:
- red first 6/10, all by assertion
- transfer suite 120 -> 130
- tsc with tests 0 -> 0
- eslint 0
- fragments clean, and planted defects caught

Mutants: 24/28 killed. The seed loop's "all 4 attempted" is NOT pinned by the PR's cells (G146-F2, recommended).

Host Node v26.8.1 throughout. Nothing was measured on Node 24.

## Heads
- START (logs/head_start.log, 19:30:52Z): PR head `dba0813c64d00a002c89660a74988754cdbcc40c` (= the pin), develop `4d1ab2cb6574` (= the commission's NOW). Merge-base `cc33e702bfd5`. 1 commit.
- END (logs/head_end.log, 19:44:00Z): the PR head is unchanged. **develop moved to `2f9f7db3`** (KS-1868 gateway redis.ts, 4 api-gateway/fragment paths). merge-tree was re-run onto it (section 6).
- The local HEAD is dba0813c, `git status` is clean, and the product sha256 equals the head blob. Every swap restored: probes_restore, suites_restore, static_restore, tsc2 restore, and mutants restore=True x28.
- **PR body not read through the API** (no gh login on this seat). I used the READY mail (evidence/r76_pr1962_ready.txt) and the two fragments in the PR.

## 1. Diffstat (logs/diffstat.log, three-dot)
4 files, **+225/-3**, as declared:

| file | + | - |
|---|---|---|
| approvalWorkflowService.ts | 24 | 3 |
| test file | 156 | 0 |
| flow fragment | 23 | 0 |
| cheat fragment | 22 | 0 |

Nothing outside the declared paths.

## 2. The hunks (logs/product_diff.log)
Three identical guards. Each one replaces `err?.message` in the log call with this:
```
let reason; try { const m = err?.message; reason = m === undefined || m === null ? m : String(m); } catch { reason = 'unreadable thrown value'; }
```
The guarded log calls are:
- seed catch: `console.error(\`...Failed to seed workflow ${wf.id}:\`, reason)`
- probe catch: `console.warn('...DB tables not ready:', reason)`
- sweep catch: `console.error('...processEscalations error:', reason)`

What does NOT change:
- the messages and levels
- the loop structure
- no rethrow anywhere
- the return of `{escalatedCount, timedOutCount}`
- every SQL statement
- `dbGetActiveWorkflows` / `findWorkflowByStepId`'s bare catches
- the route
- db.ts

## 3. Behaviour (RUN: real process, only `pg` replaced; READ where marked)

### Q1: boot (RUN)
**Trace (READ, head = base for these lines):**
- `initDb(runDbBootTasks)` (index.ts:1079) -> probe `SELECT 1 AS ok` -> `runDbReadyHook()` (db.ts:90-98)
- The hook awaits `runDbBootTasks` (index.ts:1072-1076): `loadFromDb`, then `verifyWorkflowDb`, then `verifyDelegationDb`.
- The hook's catch logs "DB ready boot work failed" and returns. **It never exits the process and never un-flags `dbAvailable`.**
- `app.listen` (index.ts:1083) is independent of all of this.

So a rejection at base meant only that `verifyDelegationDb` was skipped. That function (delegationService.ts:165-172) is just `SELECT 1 FROM svc_transfer_delegations` plus a warn; it seeds nothing.

| ver | probe failure | log | delegation probe ran | connected | /health | GET /api/workflows | process |
|---|---|---|---|---|---|---|---|
| base | ordinary / string / BigInt-message | `DB tables not ready: db down` | yes | true | 200 | [] | up |
| **base** | **revokedProxy / throwingGetter** | **`DB ready boot work failed` {error:"Cannot perform 'get' on a proxy that has been revoked" / "getter boom"}** | **no** | true | 200 | [] | up |
| head | ordinary / string | same as base | yes | true | 200 | [] | up |
| **head** | **revokedProxy / throwingGetter** | `DB tables not ready: unreadable thrown value` | **yes** | true | 200 | [] | up |
| merged (develop db.ts + PR) | all | = head | = head | | | | |
| devnow (develop db.ts, base product) | all | = base | = base | | | | |

**Answer.** At base a rejection produced neither a process exit nor degraded mode. It produced one hook-failure line and a skipped delegation probe. At head the unreadable case serves **the same state an ordinary Error already produces at base**: connected, the workflows table unseeded, the delegation probe run, health 200, the same workflow list.

**Does the PR depend on develop's 1957 db.ts change? No.** 1957 changed only the pool 'error' listener and runDbReadyHook's catch. At base the hook's catch receives a readable TypeError (thrown from inside verifyDbReady's catch), so 1957 does not change that path (devnow = base, measured). At head the hook's catch is not reached at all. The product imports only `query` and `isDbAvailable` from db.ts, and 1957 did not touch them.

### Q2: seed (RUN)
| ver | first upsert fails (seed1) | every upsert fails (seedall) |
|---|---|---|
| base ordinary / string / BigInt-message | 4 upserts attempted, 3 workflows served | 4 attempted, 0 served, 4 lines |
| **base revokedProxy / throwingGetter** | **1 attempted, 0 served**; logged as `DB tables not ready: Cannot perform 'get'...` (the seed catch threw and verifyDbReady's catch took it; verifyDbReady still resolved) | 1 attempted, 0 served |
| head ordinary / string | = base | = base |
| **head revokedProxy / throwingGetter** | **4 attempted, 3 served** | 4 attempted, 0 served, 4 lines `unreadable thrown value` |

**Answer:** yes, this is exactly what an ordinary Error does at base.

**Duplicate or partial-seed risk (READ):**
- The upsert is `INSERT ... ON CONFLICT (id) DO UPDATE` keyed on fixed ids (`simple-transfer` and the rest). A re-run, including the KS-382 recovery re-run of the hook, updates and never duplicates.
- Partial seeding is a pre-existing state, reachable at base by an ordinary Error. Head merely seeds MORE of the set (3 of 4 instead of 0).
- `created_by`/`created_at` are not in the DO UPDATE list, so a re-seed keeps them.

### Q3: escalation sweep, failure in the middle of the loop (RUN; logs/probe_table.log rows `*-k2`, `*-k3`, `sweep_select`)
**Setup:**
- 4 overdue pending steps: I1 and I3 on a custom step with `autoEscalate` + `escalateTo: boss-user` + `timeoutHours: 1`; I2 and I4 on default `step-1`, which times out.
- POST /api/workflows/escalate as SUPER_ADMIN through the real auth and the KS-1881 gate.
- The k-th step-instance write of the FIRST sweep fails. A second POST runs with no failure.

| ver / kind | k | POST 1 | process | after POST 1 | POST 2 | after POST 2 |
|---|---|---|---|---|---|---|
| base / ordinary / string / BigInt-message | 3 | 200 {esc 1, timedOut 1} | up | I1 escalated, I2 timed_out, **I3 pending**, I4 pending | 200 {1,1} | I1 esc, I2 t/o, I3 esc, I4 t/o (each exactly once) |
| **base / revokedProxy / throwingGetter** | 3 | **no response (fetch failed)** | **EXITED code 1**: `TypeError: Cannot perform 'get' on a proxy that has been revoked` at approvalWorkflowService.ts:629, uncaught | I1 esc, I2 t/o committed, I3/I4 pending | not reachable (service down) | n/a |
| head / ordinary / string | 3 | 200 {1,1} | up | = base ordinary | 200 {1,1} | = base ordinary |
| **head / revokedProxy / throwingGetter** | 3 | **200 {1,1}** | up | **= base ordinary** | 200 {1,1} | **= base ordinary** |
| k=2 (the time-out write fails), all versions | 2 | same pattern: base unreadable crashes; head unreadable = base ordinary (200 {1,0}, then {1,2}) | | | | |
| overdue SELECT fails (`sweep_select`) | – | base unreadable crashes; head and ordinary: 200 {0,0}, nothing written, POST 2 does all 4 | | | | |
| merged-k3 | | = head | | | | |
| devnow-k3 | | = base | | | | |

**Answer:**
- **Is head's outcome new? No.** Head unreadable = base ordinary in every column.
- **Approval bypass: none.**
  - The failed row stays `pending` and is processed exactly once by the next sweep.
  - Escalated rows get a future `due_at` (`timeoutHours`), so they are not re-selected. Without `timeoutHours`, `due_at` is null and the row is also not re-selected (READ).
  - `timed_out` rows are not re-selected, and `processApproval` refuses a non-pending step (READ, :476).
  - No double escalation in any cell; the `!instance.escalatedAt` guard is also present.
  - The transfer's own approve/execute path does not read workflow step instances: `/api/transfers/:id/execute` gates on `memTransfers` `status === 'approved'` (index.ts:802-814, READ). So no state written by the sweep can let a transfer proceed.
- **Atomicity:** each row is its own autocommit `pool.query`. Rows 1..k-1 stay written at base and at head, for ordinary and unreadable alike. That is the pre-existing design, not new.
- **What the PR does change** is base's process crash on an unreadable value. Head is strictly better.

**Reachability (READ):** the rejection value is whatever node-postgres rejects with, which is an Error/DatabaseError. The route is platform-admin only (KS-1881). An unreadable value needs a pg defect, a wrapper or a test double. Defence-in-depth, as with every KS-1868 site.

### Pre-existing sweep finding, measured (sweep_wfread, base = head, every kind including ordinary)
If the workflow reads inside `findWorkflowByStepId` fail (the bare `catch { return [] }` / `catch {}`, :235-243 and :695-698), then `stepDef` is undefined. **Every overdue step, including I1 and I3, which should escalate to boss-user, is marked `timed_out`** (200 {0,4}). This is terminal: POST 2 cannot repair it, and processApproval refuses non-pending steps. It fails closed for approval, but the escalation is lost. Untouched by this PR (G146-F3).

### Log files
The transfer logger is console-only (utils/logger.ts has no file transport), and db/index log through `console.log`. **No log file was written anywhere:**
- `logs/child_cwd/` (every child process's cwd and vitest's cwd) is empty.
- Wednesday's `/Volumes/DevMASTER/WEDNESDAY/logs/combined.log` mtime is 06:01 local, before this gate started at 06:29.
- No `.vite`/`node_modules` appeared in Wednesday's tree.

## 4. Re-measure (vitest `--root` = the clone's transfer service, cwd = workdir/logs/child_cwd)
- **Red first** (base product + the new file; logs/red_base_new.log): **6 failed | 4 passed (10)**.
  - R1, R3, R5 fail by AssertionError: rejected, or 0 lines.
  - R2, R4, R6 fail by AssertionError `'<symbol>'` vs `'Symbol(ks1868)'`. At base a Symbol message did not throw, so these three are log-type cells, not behaviour cells.
  - 0 crashes. As claimed.
- **Head, new file:** 10/10.
- **Whole transfer suite:**
  - base without the new file: **9 files / 120, rc 0**
  - head: **10 / 130, rc 0** (runs 2 and 3)

  The first head run (logs/head_whole.log) failed in `transfer.test.ts`'s beforeAll ("Hook timed out in 10000ms", 28 skipped) at load average ~12 on this shared host. Two reruns gave 130/130, and transfer.test.ts alone gave 55/55. That is a load flake, not the PR (G146-F7).
- **tsc including tests.** Transfer has no tsconfig.test.json, so I used scripts/tsconfig.tests.json (service config + src/** + types node):
  - head **0** (20 files, 10 under __tests__, the PR file listed)
  - base **0** (19 / 9)
  - planted: **1 TS2322**
  - service `tsc --noEmit`: 0

  My first run hit TS2688 'node' (typeRoots resolved from scripts/). That was a harness error, kept as logs/tsc_summary_run1_TS2688.log, and fixed. Transfer is not in the test-types ratchet.
- **eslint** (Dev flat config, cwd Dev): the product + the test file, **0 problems**. The base product: rc 0. A planted file: 1 error + 1 warning, rc 1.
- **docs-fragments `check`:** rc 0, "flow 117+109 new, cheat 112+109 new; lint clean, render passes". Planted defects, each rc 1 with a finding naming this file:
  - flow: unclosed div
  - flow: `<!--n-->.` removed
  - cheat: unclosed div
  - cheat: `</table>` corrupted

  Each was sha-restored; rc 0 after.

## 5. Mutants (scripts/mutants.py; product only, the PR's test file, sha256-restored after each; logs/mutants_table.log)
28 mutants: **24 killed, 4 survived.** Every kill is by assertion.

| mutant | seed | probe | sweep |
|---|---|---|---|
| M0 revert to base | KILLED R3 R4 | KILLED R1 R2 | KILLED R5 R6 |
| M1 inner catch rethrows | KILLED R3 | KILLED R1 | KILLED R5 |
| M2 constant always | KILLED C2 R4 | KILLED C1 R2 | KILLED C3 C4 R6 |
| M3 wrong fallback text | KILLED | KILLED | KILLED |
| M4 String() dropped | KILLED R4 | KILLED R2 | KILLED R6 |
| M5 log removed | KILLED | KILLED | KILLED |
| M6 undefined/null -> String() always | **SURVIVED** | **SURVIVED** | KILLED C4 |
| M7 rethrow after logging (every value) | **SURVIVED** | KILLED | KILLED |
| M8 seed: `return` after the first failure (stop the loop) | **SURVIVED** | | |
| M9 rethrow only when unreadable | KILLED R3 | KILLED R1 | KILLED R5 |

- **Seed M7/M8 survive.** The seed cells assert `lines == upserts > 0`, never `upserts == 4`, so a seed loop that stops after the first failure (base's unreadable shape, for every value) passes C2, R3 and R4. The PR's headline seed claim ("attempts all 4") is pinned only by this gate's process probe (head seed1: 4 attempted, 3 served).
- M6 survives at seed and probe because no cell there has an `undefined`/`null` message (only the sweep has C4, a plain string).

## 6. merge-tree (scripts/mergetree.sh)
**Onto `4d1ab2cb`** (logs/merge_tree_4d1ab2cb.log):
- rc 0, tree `8ec0ac38`
- the merged-vs-develop paths == the 4 PR paths
- the product blob in the merged tree == the head blob (`a8967474`)

**Squashes since base:**
- 0bd5e7bf (1957, five db.ts)
- 35d23ac6 (1958, anchoring)
- 4d1ab2cb (1959, auth events)

PR-path overlap is **0** (positive control 23). The only transfer paths among them are `transfer/src/db.ts` and its new test.
- **Is db.ts read by the PR's code paths?** Yes: `query`/`isDbAvailable`, and runDbReadyHook wraps the boot hook.
- **Does the behaviour depend on the 1957 change? No.** That change touched only the pool listener and the hook's catch. The merged-tree boot and sweep cells (db.ts from develop + the PR product) equal head in every cell, and devnow equals base.

**develop moved during the gate to `2f9f7db3`** (KS-1868 gateway redis.ts, 4 paths, none in transfer) (logs/merge_tree_2f9f7db3.log):
- rc 0, tree `2d5cad82`
- paths == the PR's paths
- product blob equal
- overlap 0

Suites were not re-run on the merged tree; the merged process probes were run instead.

## 7. Kam's ks1346 rule (log type and field NAMES, never values)
- No new log line. The three existing lines keep their message and level.
- The constant `'unreadable thrown value'` is a type statement: compliant.
- A readable message is logged as before (base practice, pre-existing for the class): pg/DatabaseError text, plus the seed line's workflow id (a fixed seed id, not PII).
- **Coercion changes, measured in the real process (console):**
  - a BigInt message: `10n` -> `10`
  - a Symbol message: passed as a Symbol -> `Symbol(desc)` string
  - an undefined/null message: unchanged
- The cyclic-object -> `[object Object]` change is READ, not run. It logs LESS content than base's util.inspect of the object.
- No secret carrier is known in any of these, so the lines are compliant.

## 8. Notes for the PR body
- **G146-F1 (INFO, measured; add to the body):** the base impact was worse than "the sweep rejected". Through the real route, an unreadable value in the sweep **crashed the transfer service process** (exit 1, an uncaught rejection out of the Express 4 async handler; no response), with the rows already escalated or timed out left committed. At boot the base effect was mild: the db.ts hook catch logged "DB ready boot work failed" and only the delegation probe was skipped, with no exit and no degraded mode. Head = base-ordinary at all three sites (gate 146's process probe, 120 cells).
- **G146-F2 (recommended, test gap):** pin the seed loop's 4-of-4. Add `expect(h.upserts).toBe(4)` to C2, R3 and R4. Without it, mutants M7 (rethrow after logging) and M8 (stop the loop after the first failure) survive. Optionally add an `undefined`-message cell at the seed and probe sites (M6).
- **G146-F3 (recommended follow-up, pre-existing, measured, base = head for every value including an ordinary Error):** in processEscalations, a failed workflow read (the bare catches in `dbGetActiveWorkflows`/`findWorkflowByStepId`) leaves `stepDef` undefined, so every overdue step is marked `timed_out`, including steps configured to auto-escalate. The state is terminal: no later sweep or approval can repair it. It is fail-closed for the transfer, but escalations are silently lost. This needs its own ticket: skip the row (leave it pending) when the workflow cannot be resolved, rather than time it out.
- **G146-F4 (INFO, pre-existing):** a sweep that fails part-way answers `200 success:true` with partial counts and no error indicator. It did so at base for an ordinary Error, and now does so for an unreadable value too. The admin caller cannot tell the sweep was incomplete; only the log line says so.
- **G146-F5 (INFO, measured):** the mid-loop failure the author left unmeasured, measured here at k=2 and k=3. No approval bypass and no double escalation. The failed row stays pending and the next POST processes it exactly once. Transfer execution gates on the transfer record, not on step instances (READ).
- **G146-F6 (INFO):** every author figure re-measures:
  - red 6/10 by assertion
  - 120 -> 130
  - tsc with tests 0 -> 0
  - eslint 0
  - fragments with planted defects rc 1

  Note that R2/R4/R6 are log-type cells: a Symbol message never threw at base.
- **G146-F7 (INFO, harness):** one whole-suite head run hit a transfer.test.ts beforeAll timeout under host load ~12. Two reruns gave 130/130. This is not PR-caused, but transfer.test.ts's 10 s hook is load-sensitive.
- **G146-F8 (INFO):** develop moved to 2f9f7db3 during the gate. merge-tree is clean onto both develop heads, with 0 overlap.

## 9. NOT TESTED
- the live PR body via the API (no gh login)
- a real PostgreSQL: the store is a model with unique id upsert, and the real SQL WHERE/ON CONFLICT semantics are emulated, not executed
- pgbouncer, or a mid-statement connection loss
- the api-gateway hop to /api/workflows/escalate (the gateway has its own redis workflow routes; whether and how escalate is proxied is not traced)
- `NODE_ENV=production` boot
- multi-tenancy pools
- the cyclic-message log line (READ only)
- the KS-382 background-retry re-run of the hook (READ: the same hook, same code)
- suites, tsc and fragments on the merged tree (process probes only)
- the four platform suites
- CI and the pre-push hook (quoted from the READY mail only)
- Node 24
- Spark shadow review (not requested)

## Processes
Every background run I started has finished:
- npm ci + shared build
- the probe matrix: 120 child service processes, each SIGTERMed, or exited by itself in the base crash cells
- the suites/static/mutants chain
- the reruns and tsc2

`ps` shows no process with this workdir in its command line.
