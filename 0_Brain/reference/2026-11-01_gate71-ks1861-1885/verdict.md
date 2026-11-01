## QA GATE 71, TIER 1, ROUND 1: KS-1861 #1885 (PR 4 of 4)

**BLUF: GO WITH NOTES.** Delete now archives and nothing else, on every path and under every flag combination. I ran the real entry module with the real `pg` driver against a throwaway Postgres 15 (`gate71-pg`, built from the repo's `docker/init-platform` schema). Across 65 cells, Delete:
- deleted no row in any table;
- dropped no database: a real `secuura_tenant_<slug>` database survived 36 flag combinations;
- erased no vault row;
- revoked nothing.

The status route admits exactly the five moves the rulings allow. Archived -> suspended -> active brings back a working tenant with every row intact. On real row locks, two concurrent Deletes give exactly one 200 and one 409 with one audit row. The status change and its `tenant_archived` row commit together, including when COMMIT itself fails. The merge is clean onto develop `3d036184` and onto develop `a71479b4`, which moved again during the gate. On the merged tree, `check:openapi` passes with no regeneration, and PR 4's yaml lines are byte-identical. All 14 mutants were killed: 5 re-runs of the author's mutants and 9 of my own. The PR's own cells miss two of mine (G71-F2).

Nothing blocks the merge. There are three minor notes:
1. The status route's audit row is still not atomic with its UPDATE. That route now carries the archive reversal: on real PG, archived -> suspended with a failed audit insert answers **500 while the move has committed, with no audit row**.
2. The PR's fake-pg cells cannot see an audit row written outside the transaction, or a leaked pool connection.
3. The docs' start-up paragraph leaves out "not a regression", which the card and both fragments say.

- PR https://github.com/Secuura/Distributed_Secuura/pull/1885 · ticket KS-1861 · author Seat S 9th · commissioned by Wednesday, Sun 1 Nov 2026 · routing G1 (tier 1).
- **Head at START** (2026-11-01T00:51:34Z, `git ls-remote`, `evidence/lsremote_start.txt`): `refs/pull/1885/head` = `48d05f02ede8ee3e0941f872ba8cfd3f0cc77c6d`. develop = `3d036184d37f0ad2a46fff4e9e6e80de03441b93`, not the author's `60e59bd2`: #1874 was squash-merged as `3d036184` and touched `docs/openapi/secuura-api.yaml` (`evidence/develop_moved.txt`, 13 files).
- **Mid-gate** (01:16:37Z, `evidence/lsremote_mid.txt`): develop **moved again**, to `a71479b49bf319a6349eb1450c13ef6a9f235a77` ("KS-1906: owner-less credentials…", 12 files, all vc-issuer/docs/fragments; it does not touch the yaml, `package-lock.json`, `packages/shared` or tenant-provisioning).
- **Head at END** (2026-11-01T01:27:05Z, `evidence/lsremote_end.txt`): `refs/pull/1885/head` = `48d05f02ede8ee3e0941f872ba8cfd3f0cc77c6d`, **unchanged**. develop = `a71479b4`. Re-merged and re-verified on it (Q8).
- Clone: `0_Brain/reference/2026-11-01_gate71-ks1861-1885/repo`, cloned `--shared --no-checkout` from gate 65's clone. Push URL `no_push_qa_gate`; refs in `refs/gate/*`. `rev-parse --show-toplevel` was asserted before every fetch and write. It was left detached at `48d05f02` with `git status --porcelain` empty.
- Host: Apple Silicon Mac, shared. **Node v26.8.1, not LTS.** Node 24 LTS was not measured.

## VERDICT: GO WITH NOTES

## Rulings tested against (quoted from the live board, `0_Brain/dashboard/data/decisions.json`)
- `secuura-ks1861-archive-from-which-status-1101`, **b** (ruled 2026-11-01T10:06:43+11:00): *"As (a), and archived can go back to suspended"*.
  - (a): *"Provisioning, active or suspended can be archived by Delete; an already-archived tenant answers 409. Coming back from archived needs a database edit or a later ruling. The admin Delete keeps working."*
  - (b): *"Same as (a), plus the status route allows archived to suspended, so 'reversible' holds through the API. Archived to active stays refused, as you ruled. One extra allowed change and one test."*
- KS-1861 "Archive, not erase" (option a, "keeps every row"); KS-1860 refuses archived -> active; Wednesday's ANSWER: no DROP DATABASE anywhere, under any flag.
- `secuura-ks1860-status-refresh-fails-at-startup-1101`, **a** (ruled 10:06:40+11:00): *"Keep it as built and say so"*. Detail: *"Serve while statuses are unknown (an outage of the platform database does not take originate down), state it plainly in the docs and on the ticket. Nothing more is built."* The card's BLUF adds: *"This is not a regression… It applies only where MULTI_TENANCY_ENABLED is on."*

## Findings

**G71-F1 · minor · status route audit atomicity, now on the reversal path (follow-up; not a regression).** `services/tenant-provisioning/src/index.ts:454-456` commits the conditional UPDATE through `platformQuery` (autocommit). The `tenant_status_changed` INSERT at `:474-478` is a separate autocommit statement. If the INSERT fails, the route answers the constant 500 but the move has already committed.
- **Red, measured on real PG.** Gate cell S1 is `archived -> suspended` with the audit INSERT made to fail by a gate-only trigger. The result was `{"code":500,…,"status":"suspended","audit":[]}` (`evidence/s1_status_route_audit_fail.json`). The client is told it failed, the tenant has left `archived`, and nothing records the move. A retry then answers 409 "from suspended to suspended".
- **Scope.** This shape is unchanged since KS-1860 (#1876; gate 64 did not flag it). PR 4 does not touch these lines, but it routes the archive reversal through them.
- **Contrast.** Delete wraps its write and its audit row in one transaction (`:585-608`). The fix is the same pattern on the status route.

**G71-F2 · minor · test strength (follow-up).** Two of my mutants pass all 30 PR cells.
- **G71-M2** writes the `tenant_archived` row on the pool (`platformQuery`) instead of the transaction client. The PR fake's BEGIN snapshot includes the audit array, so a ROLLBACK silently reverts an out-of-transaction audit row too. The fake cannot tell the two apart. M2 survived my first probe as well: when the audit insert itself fails, both shapes roll back. It was killed only by gate cell **E8**, which fails COMMIT with a deferred constraint trigger. Under M2 a `tenant_archived` row survives a rolled-back archive (`evidence/mutants.json`, `evidence/mut_G71-M2_probe.log`).
- **G71-M4** drops `client.release()`. The PR fake's `release` is a no-op, so 0 PR cells go red. The real pool (max 5) is exhausted and 42 gate cells time out.
- **Fix:** a real-PG cell for the archive transaction, or a fake whose `pool.query` path is outside the snapshot and whose `release` is counted.
- Spark's first attempt circled the same weakness and was cut off for repetition ("the new test file's fake pg does not model the platformquery used for the failur…").

**G71-F3 · minor · docs, start-up paragraph (reword before merge if cheap).** `docs/MULTI-TENANCY.md:210-214`, "Status reads at start-up", states:
- serve while unknown: **yes**;
- flag-on only: **yes**;
- the stale-while-down case: **yes**.

It does **not** state that this is not a regression (before KS-1860 nothing refused a suspended tenant). The card says so, and both new fragments say so (*"This is not a regression: before KS 1860 nothing refused a suspended tenant at all."*), but the page does not. It also leaves out the two qualifiers gate 64 asked for: "per originate process", and that a tenant reactivated while the database is down stays refused. Every statement in it is true at the head.

**G71-F4 · file-only · docs precision.** `docs/MULTI-TENANCY.md:225-227` says that on failure "a `tenant_archive_failed` row is written". That is best-effort. Gate cell E6 (both audit inserts fail) gives a 500, the status unchanged and **no** audit row; the second failure is only `console.error`'d (`index.ts:628-630`). The code comment says exactly this ("Its own failure is logged, never silent"). The page could say "attempted". The status table's *Intended meaning* column still reads "Read-only, pending deletion" for `archived` (`:203`). The author kept it on purpose as the design column, but "pending deletion" now contradicts "erasure is not built".

**G71-F5 · file-only · develop moved twice; yaml condition 2.** #1874 merged (as `3d036184`), so the author's condition 2 is triggered. Measured on develop `a71479b4` + PR 4 (synthetic merge `2886097f`), and identically on `3d036184` + PR 4:
- `check:openapi` rc 0, "CHECK PASS";
- the yaml needed **no regeneration**;
- PR 4's changed yaml lines are byte-identical to its delta lines (`diff` rc 0, `evidence/yaml_hunks_merged_vs_develop.diff`): the `TenantArchived` component, the DELETE path and the status-route description, nothing else.

Separately, **#1884 now conflicts with develop on its own**: 18 paths, 2 yaml conflict blocks, caused by #1874's squash. The conflict set and the yaml conflict blocks are identical with and without PR 4 (`cmp` rc 0, conflicted-path `diff` rc 0). That is #1884's merge prep, not PR 4's.

**G71-F6 · file-only · authorisation (unchanged).** The delta touches neither the gateway nor the middleware.
- Delete and status are gated by `authenticateToken()` plus `requireSuperAdmin` at the gateway (`api-gateway/src/routes/platform.ts:64-73`, `:395-430`). Those admit `super_admin`, `SUPER_ADMIN`, `platform_admin` and `SYSTEM_ADMIN`.
- tenant-provisioning itself checks only that the JWT is valid (`index.ts:182`), with no role check. That is unchanged from develop.
- `git diff 60e59bd2 a71479b4` touches neither file.

**G71-F7 · file-only · consequences of "keeps every row" (for Kam, no action needed).**
- An archived tenant keeps its `slug` (UNIQUE), so creating a new client with the same slug now answers 409. The old Delete freed the slug.
- The admin portal still asks "Delete client …? This cannot be undone." (`frontend/admin/src pages/platform/ClientList.tsx:85`). It also offers Delete on an archived tenant, which is now a silent 409. Both are filed as KS 1912, and the warning errs in the safe direction.
- The Schemathesis fixture (G64-F2, KS 1914) still PATCHes straight to `active`, which stays 409 for an archived isolation tenant.

## Q1. The transition matrix (code at `index.ts:439-443` + `:445-485` for status; `:557` + `:559-634` for Delete)
Proved cell by cell on **real Postgres**: gate probe `scripts/gate71-realpg-probe.test.ts`, 65/65 at the head (`evidence/probe_head_v2.log`), 65/65 on the merged tree (`evidence/probe_merged_a71.log`). Each cell asserts the exact code, the exact body, the final status, the exact audit rows, and row counts of every public table, each table's rows for the tenant, the per-tenant database and the database count. The PR's cells (A1-A5, R1-R8, X1, N1) cover the same pairs on a fake.

**Status route** `PATCH /api/tenants/:id/status`. Allowed moves answer `200 {"success":true,"status":<to>}`, run one UPDATE and add one `tenant_status_changed {status}` row. Refused moves answer 409 `Cannot change tenant status from <from> to <to>`, change nothing and write no audit row. Target `provisioning` answers 400 `Invalid status` with no statement.

| from \ to | provisioning | active | suspended | archived |
|---|---|---|---|---|
| provisioning | 400 | **200** (ruled) | 409 | 409 |
| active | 400 | 409 | **200** (ruled) | 409 (ruled: suspend first; Delete is the way) |
| suspended | 400 | **200** (ruled) | 409 | **200** (ruled) |
| archived | 400 | **409** (KS-1860: refused) | **200** (Kam's b, new) | 409 |

**Delete** `DELETE /api/tenants/:id` with `{"confirm":true}`. Implied target: archived.

| from | Code / body | DB writes | Audit |
|---|---|---|---|
| provisioning | 200 `{success:true, deleted:false, archived:true, status:"archived", message}` | `UPDATE … SET status='archived' WHERE id=$1 AND status=$2` in BEGIN/COMMIT | `tenant_archived {slug, previousStatus, erased:false}`, same transaction |
| active | 200, same | same | same |
| suspended | 200, same | same | same |
| archived | 409 `Tenant is already archived` | none (no BEGIN) | none |
| unknown id | 404 | none | none |
| no confirm | 400 | none | none |
| malformed id | 400 (KS 497 guard) | none | none |
| UPDATE fails | 500 constant | rolled back | `tenant_archive_failed {erased:false}` (E4) |
| audit INSERT fails | 500 constant | rolled back (real PG) | `tenant_archive_failed` (E5) |
| COMMIT fails | 500 constant | rolled back | `tenant_archive_failed` only; no `tenant_archived` survives (E8) |
| both audits fail | 500 constant | rolled back | none; logged (E6, G71-F4) |
| lost race | 409 `Tenant status changed while archiving; nothing was changed` | rolled back | none (C2, T3) |

**Code against rulings: no cell disagrees.** Base product code (develop's `index.ts`) turns 46 of the 64 v1 probe cells red (`evidence/base_product_probe.log`). Among them are every Delete cell and `archived>suspended`.

## Q2. Keeps every row, no erase, no DROP
- **Grep is a selector; every hit was read** (`evidence/q2_grep.txt`). In the delta's non-doc lines, every DROP / DELETE FROM / vault hit is a removal (`-`), a test fake, a comment or the answer text. At the head, `index.ts` has three `DELETE FROM` hits, `:353-355`. All three are the unchanged KS-211 POST rollback of a tenant created in the same failing request; the Delete route does not call it. `DROP DATABASE` appears **0** times in `services/` and `packages/` source (non-test, non-dist) at the head. The control count is 2 in develop's `index.ts`. Delete calls only `platformQuery` and `platformPool.connect`. No admin pool, no other service, no vault or key call remains.
- **Measured on real PG:** D cells for 4 statuses × `PROVISION_PER_TENANT_DB` ∈ {true, false, unset} × `MULTI_TENANCY_ENABLED` ∈ {true, false, unset}, which is 36 cells, plus E1-E8. Each asserts identical row counts in all 9 public tables. It also asserts the tenant's own rows in `tenants`, `tenant_contacts`, `tenant_config`, `vault_entries` and `platform_document_registry`, that the real database `secuura_tenant_gate71_acme` still exists, and an unchanged `pg_database` count. All green. At base, every D cell is red: rows deleted and the database dropped.
- Neither flag is read by the Delete handler at all; `PROVISION_PER_TENANT_DB` is read only in POST (`:268`). The main database is never connected to by Delete. Nothing is revoked: no key, metering or connector call exists on the path.

## Q3. Reversal through the API
V1 on real PG: active -> Delete -> archived. Then `PATCH active` gives 409, `PATCH suspended` gives 200 and `PATCH active` gives 200. The final status is active, all row counts are identical to before Delete, GET answers 200, and the audit trail is exactly `[tenant_archived, tenant_status_changed suspended, tenant_status_changed active]`. A second Delete archives again.

**One-way side effects: none found.**
- Delete touches only `tenants.status`, `updated_at` and one audit row.
- originate's pool manager re-reads every tenant's status each refresh (`packages/shared/src/db/tenant-pool-manager.ts:300-330`). An archived tenant drops out of the pool-config map, and returns on the first refresh after it is active. This is last-known-status, as described in G64-F1/F5.
- No key revocation, pool eviction, cache, connector or scheduler acts on `archived`. A git grep for `'archived'`, `tenant_archived` and `tenant_deleted` across services, packages, admin, scripts and systemTest finds only the status check, the portal menu and these routes.

## Q4. Concurrency and idempotency (real PG row locks, `pg_stat_activity` lock-waiter polling)
- **C1, two Deletes at once:** both read `active` and both block on the row. On release the codes are `[200, 409]`, the status is archived and there is exactly one `tenant_archived` row.
- **C2, Delete racing a suspend that commits first:** Delete answers 409 "status changed while archiving", the final status is suspended and there is no audit row.
- **C3, Delete vs reactivation from suspended:** one 200 and one 409, with a final state and audit row that match the winner.
- **Already archived:** 409 with no BEGIN, no write and no audit row (D-archived ×9, X1).
- **Atomicity:** Delete is atomic with its audit row (E5, E8). The status route is not (G71-F1).
- Mutants G71-M1 (race guard dropped), G71-M7 (lost race answers 200) and G71-M8 (forced archived) were each killed by C1-C3 and by the PR's T3.

## Q5. Authorisation
Unchanged by the delta and identical on develop; see G71-F6. The status route and Delete stay super-admin-only at the gateway. Both gateway forwarders pass the upstream status and body through (`platform.ts:407`, `:426`), so the new 409 and the new 200 body reach the caller.

## Q6. The author's evidence, re-run
- **30/30 green at the head; 10/30 red at develop's `index.ts`** (`evidence/base_runs.json`, `base_head_pr.log`, `base_product_pr.log`: "Tests 10 failed | 20 passed (30)"). The 10 are exactly A1-A3, A5, F1, F2, T1-T3 and X1. The swap was restored with sha256 asserted (`restored_sha256_ok: true`).
- **Whole tenant-provisioning suite: 84/84** across 10 files at the head (`evidence/tp_full_head.log`, load1 8.29 -> 9.31), and **84/84 on the merged tree** (`evidence/tp_full_merged_a71.log`).
- **check:openapi** at the head: rc 0, "CHECK PASS", 417 example blocks OK. **Control:** the word PLANTED put into the DELETE description gives rc 1, "CHECK FAIL: generated YAML differs from on-disk version". Restored, with sha256 `da8e4e2f…04bf` equal (`evidence/check_openapi_{head,plant}.log`).
- **tsc** `--noEmit -p services/tenant-provisioning`: rc 0 (`evidence/tsc_tp.log`).
- **Mutants** (`scripts/mutants.py`, `evidence/mutants.json`, `mutants_stdout_v2.log`; each restore was sha256-asserted; the author's patch text was not available, so their mutants were rebuilt from their one-line descriptions):

| # | Mutant | PR cells red | Gate probe red | Result |
|---|---|---|---|---|
| DM2 | DROP DATABASE under `PROVISION_PER_TENANT_DB=true` | 1 (F1) | 9 | killed |
| TB1 | Kam's (b) removed | 1 (A5) | 3 | killed |
| TB2 | archived -> active admitted | 1 (R1) | 2 | killed |
| SS1 | provisioning dropped from the Delete start statuses | 1 (A3) | 9 | killed |
| SS4 | archived added to the Delete start statuses | 1 (X1) | 9 | killed |
| G71-M1 | race guard `AND status = $2` dropped | 1 (T3) | 3 | killed |
| G71-M2 | audit row written on the pool, outside the transaction | **0** | 1 (E8) | killed, **gate only** |
| G71-M3 | no ROLLBACK in the catch | 1 (T1) | 2 | killed |
| G71-M4 | `client.release()` dropped | **0** | 42 | killed, **gate only** |
| G71-M5 | `DELETE FROM vault_entries` slipped into the transaction | 6 | 28 | killed |
| G71-M6 | failure audit removed | 2 | 3 | killed |
| G71-M7 | lost race answers 200 | 1 | 3 | killed |
| G71-M8 | archive forced even when the UPDATE matched nothing | 1 | 3 | killed |
| G71-M9 | suspended -> suspended admitted | 1 (R7) | 1 | killed |

**14/14 killed; 12/14 by the PR's own cells** (G71-F2). I did not re-run the author's other 11 mutants.

## Q7. The docs (`docs/MULTI-TENANCY.md` at the head)
Read against the code and the rulings:
- **Status Transitions** `:192-208`: the diagram, the table and the route paragraph list exactly the code's five moves (`:439-443`) and the 409. **True.**
- **Status reads at start-up** `:210-214`: true, but the "not a regression" statement is missing (G71-F3).
- **Deleting a Client** `:216-236`: start statuses, 409, 404, nothing dropped or erased under either flag, the transaction, the answer body and the reversal. All true; "a `tenant_archive_failed` row is written" is best-effort (G71-F4).
- **"Before KS-1861"** `:233-236`: matches develop's code.
- **Route tables** `:302`, `:368`; **Tables list** `:324-325`; **compliance row** `:150`: true. `vault_entries` "nothing touches this copy since KS-1861" holds: a git grep finds no other writer of the platform copy, only the FK cascade in the POST rollback of a tenant created in the same request.
- **Suspending a Tenant** `:476-478`: "suspended from `active` or `archived` only" and "within one successful 60 s status refresh" are true.
- `:202-203` correctly scope the 403 to `MULTI_TENANCY_ENABLED` and to originate.

No statement describes the old delete or an unordered route outside the labelled passages. G64-F4 (stale `:202-207`, `:461`) is **resolved** by this PR.

## Q8. Merge and overlap (`evidence/merge_trees.txt`, `merge_trees_with_pr4.txt`, `merge_trees_a71479b4.txt`, `yaml_conflict_compare.txt`)
- `merge-tree --write-tree 60e59bd2 48d05f02`: rc 0, tree `91c50fde98d4c49c…`. **This equals the author's 91c50fde98d4.**
- `merge-tree --write-tree 3d036184 48d05f02`: **rc 0**, tree `18d398563aec…`. Develop + PR 4 + #1874's head: rc 0, tree `18d39856…`, the same tree, because #1874 is already in.
- `merge-tree --write-tree a71479b4 48d05f02`: **rc 0**, tree `ac4a3a22a583…`.
- #1884 (`ecfe4f07`) against develop alone gives rc 1 with 18 conflicted paths. Against develop + PR 4 it gives the **same** 18 paths and the **same** 2 yaml conflict blocks (`cmp` rc 0). **PR 4 adds 0 yaml conflicts.** The conflicts are #1874-vs-#1884 (G71-F5).
- The yaml on the merged tree: see G71-F5. check:openapi passes and the hunks are identical.

## Q9. Not covered by the author
- **Real Postgres: now covered by the gate**, with 65 cells including races and transaction faults (Q1-Q4). Not a blocker.
- **The four platform suites:** a note, not a blocker. The PR touches none of their code. The Schemathesis fixture issue (KS 1914, G64-F2) is the only known interaction and is not made worse: archived -> active stays 409.
- **Admin portal (KS 1912/1913):** a note. The portal reads only `res.ok`, so Delete keeps working and the ruling's "the admin Delete keeps working" holds. The copy over-warns and the audit-log colour is missing. Neither is a blocker.
- **Schemathesis fixture (KS 1914):** a note, as above.
- **Erasure:** out of scope. Ruled not built ("Archive, not erase").

## SPARK SHADOW AND CALIBRATION
- `spark_gate.sh` (non-pytest mode, the two KS-1861/KS-1860 files, `--node-modules` = the clone's root `node_modules`, `--work /private/tmp/gate71_spark_work`, base `develop`, `--out evidence/spark/facts`; `@secuura/shared` built first, `evidence/shared_build.log` rc 0): **rc 0 in 27 s.** It reported head 30/0, base product 20 passed / 10 failed, diff 10 files +507/-82, merge-base `60e59bd2`, base tip `a71479b4`. All match my figures; it also confirmed develop's second move.
- `spark_review.py` (`--ticket KS-1861`, `--pr-body-file evidence/commit_message.txt`): rc 0. Attempt 1 was a repetition abort ("fake pg does not model the platformquery used for the failur…"); attempt 2 was valid. 144.5 s, 128.3K prompt tokens over two attempts. **Spark verdict: GO**, with 8 Notes, 0 Minor and 0 Major. **0 of 8** carry `evidence_quote_found_in_input: true` (`evidence/spark/review/review.json`).

| # | Spark finding | Sev (Spark) | Mine | Call |
|---|---|---|---|---|
| 1 | Only mutation is the status update and the audit row, scoped by id | Note | Confirmed on real PG (Q2) | **Agree** |
| 2 | The ticket's root cause is not measured by the PR | Note | The old path is measured at base: 10 PR and 46 gate cells red, real DROP observed | **Disagree** |
| 3 | The fix does not depend on the old path's correctness | Note | True | **Agree** (no defect) |
| 4 | Tests do not pin the old path's data loss | Note | Not required; base reds show it | **Not a defect** |
| 5 | Base reds are behavioural, not absence-red | Note | True | **Agree** |
| 6 | The fake is more permissive than a real DB | Note | True, and it matters: M2 and M4 survive the PR cells | **Agree; partial = G71-F2** (Spark did not show a consequence) |
| 7 | Counts add up (12 + 18, 9 + 1) | Note | True | **Agree** |
| 8 | The answer shape is verified only on the fake | Note | Now verified on real PG | **Superseded by the gate** |
| — | — | — | G71-F1 status route audit not atomic (measured) | Spark missed |
| — | — | — | G71-F3 docs omit "not a regression" | Spark missed |
| — | — | — | G71-F5 develop moved twice, #1884 conflicts independently | Spark missed |

| | Verdict |
|---|---|
| Spark | **GO** (8 Notes, no quote verified) |
| Gate 71 | **GO WITH NOTES** |

## COUNTS
- Findings: 0 blocker · 0 major · 3 minor (F1 status-route audit atomicity, F2 PR-cell strength, F3 start-up paragraph) · 4 file-only (F4-F7).
- PR cells: 30/30 at the head; 10/30 red at base, exactly the author's set.
- Gate real-PG probe: 65/65 at the head and on the merged tree. At base, the v1 probe had 46/64 red.
- Whole tenant-provisioning suite: 84/84 at the head and 84/84 on develop `a71479b4` + PR 4.
- Mutants: 14, all killed (12 by the PR cells).

## NOT TESTED
- Node 24 LTS. A running stack, so not the real gateway -> tenant-provisioning -> originate chain. The four platform suites. Any deploy.
- **eslint:** run from a cwd outside the package it reported "File ignored because no matching configuration was supplied" (`evidence/eslint_index.log`). That is **no measurement**, and the hook forbids `cd`.
- The author's other 11 mutants (DM1, DM3-DM8, SS2, SS3, TB3, TB4).
- The GitHub PR body (no `gh` used; the commit message was read instead).
- Real-PG cells used the `docker/init-platform` schema. `migrations/003_platform_tenancy.sql` declares `platform_audit_log.target_id` as UUID and `tenants.status` without the CHECK. Both are compatible with the head's statements: ids are UUID-guarded, and the statuses written are within the set. I did not run against that variant.
- Multi-replica originate behaviour after an archive.

## HOW
- **Clone:** `git clone --shared --no-checkout` from gate 65's clone. `remote.origin.promisor` and the `blob:none` filter were set. Fetched with the Blockchain deploy key into `refs/gate/{pr1885,develop,develop_a71479b4,pr1874,pr1884,base60e}`. Synthetic merge commits `refs/gate/merged_dev_pr1885` (`2f5b9e99`) and `refs/gate/merged_a71_pr1885` (`2886097f`) were made only in this clone with `commit-tree`.
- **Install** at `Blockchain/Dev`:
  - `npm ci --ignore-scripts`: rc 0 (`evidence/npm_ci.log`).
  - `packages/shared` build: rc 0 (`evidence/shared_build.log`).
  - Prisma: a root `prisma generate` gave rc 127 (no root binary), then rc 1 with originate's binary. Originate's own `npm run generate` gave rc 0 (`evidence/prisma_generate.log`). tenant-provisioning does not use Prisma.
- **Runs:** `scripts/vt_run.sh` (whole suite, `--maxWorkers=2`) and `scripts/probe_run.sh` (single files, `--maxWorkers=1`). Both use nice 10 and wait while load1 > 8, the gate 68 pattern. `probe_run.sh` copies the probe into `src/__tests__/` and moves it back out to the scratchpad afterwards.
- **DB:** container `gate71-pg` (`postgres:15-alpine`, `127.0.0.1` random port, id in `evidence/gate71_pg_container.id`), with `docker/init-platform/01` and `02` applied (`evidence/pg_init_*.log`) and the gate-only fault triggers in `scripts/pg_faults.sql`. The password came from `openssl rand` into a 0600 scratchpad file and was scrubbed from every log. A grep of `evidence/` and `scripts/` for it finds 0 files. **Stopped** at the end (`evidence/gate71_pg_stopped.txt`: "Exited (0)"). gate65-pg, gate68-pg, gate70-pg and s-w13-pg were not touched.
- **Base and mutants:** `scripts/mutants.py base|mutants`. Each is a unique-anchor replacement (anchor count asserted == 1) with sha256 asserted after restore. The first mutant pass (v1 probe, 64 cells) left G71-M2 alive. The gate then added cell E8 (a fault at COMMIT time) and re-ran all 14 against the v2 probe. `evidence/mutants.json` is the v2 result.
- Background jobs: the base/mutant runs, spark_gate, spark_review and the merged-tree run. All exited on their own; nothing was killed by name.
