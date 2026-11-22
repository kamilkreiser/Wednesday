PR 2272: GO WITH NOTES (at head fd178433fc4f6615e191a698a0c9424fbcd462b8; tier 1)

# Gate 396, tier 1 (Opus), PR 2272 (KS-2306), 2026-11-22 ~17:50-18:03 AEDT (06:50-07:03Z)

## Pins
- **Pinned twice, at 06:50:44Z and 07:03:05Z**, by git ls-remote (through the Secuura project's gh credential helper, read-only). Same values both times: PR head fd178433fc4f6615e191a698a0c9424fbcd462b8, develop 302361a30209334ad6f6fbfbab3082984fde2342.
- gh pr view: OPEN, not draft, MERGEABLE, base develop, ONE commit, 5 files, +341 -23, updatedAt 06:48:35Z.
- **Merged state = the head.** Its parent is develop. `git merge-tree --write-tree origin/develop pr/2272` gives rc 0 with tree 01520940e7bc = the head's own tree. So every "head" figure below is the merged state.

## How I measured
- Own clone `_work/g` from GitHub (`--reference-if-able` gate 395's clone, `--dissociate`), with PR 2272 fetched to `pr/2272`. Three worktrees: `h` (head: suite, static), `d` (develop: suite, ratchet arm), `x` (head: red-first, mutants).
- node_modules and `packages/shared/dist` were APFS-cloned from gate 395's `h`. Between gate 395's head (4cec1424) and this head, the diff is exactly the PR's 5 paths, with no package.json, lockfile or packages/ change.
- Node v26.8.1 (not LTS), jest, TMPDIR /private/tmp/g396t.
- Scripts in `_work/`: `run_cwd.py`, `suites.sh`, `static_g396.py` (a copy of gate 395's, re-pointed), `mutants_g396.py`, `mt_g396.py`, `pgprobe/run_g396.sh` with `extra.sql` (plus `probe_seat_copy.sql`, copied read-only from W 56th's record), and `lin_read_g396*.py` (read-only GraphQL; the key is read into memory from the Secuura credentials file, never printed).
- **Throwaway container (Q2, the commission's own allowance):**
  - Name `g396-ks2306-pgprobe`, image postgres:15 (15.20, already local, not pulled), `--network none`, `--tmpfs` data dir (no volume). Stopped and removed by that name only.
  - Before and after: 106 containers and 195 volumes. The `docker ps -a` name list and `docker volume ls` were byte-equal before and after (evidence/pgprobe/names_*.txt, vols_*.txt).
  - The Status column of the with-status listing changes with uptime, so I compared names.
- End state:
  - h, d and x each have 0 porcelain lines.
  - x's adminConfig.ts sha256 ff95c158da46… = h's (restored and sha-checked after every mutant).
  - The planted merge-tree commit 139b39c500ed exists only in my clone and was never pushed.
- Not touched: no seat tree, no !CODING write, no GitHub or Linear write, no deployed database, no other container, no mail, no launch, no cd, no rm.

## Findings

No HIGH finding against this PR. The 409 refusal and the one-unit delete hold as ruled. I measured them through the cells and on a real Postgres 15 under RLS as a non-owner role, including two concurrency races the seat did not run.

### MEDIUM (pre-existing; not a defect of this PR; for Wednesday to route)
**G396-2272-1: the organisation delete the admin dashboard actually uses (the gateway's) has neither protection, and on every database build it orphans the organisation's rights holders.**
- api-gateway `routes/admin.ts:1595-1612`, `DELETE /api/users/admin/organizations/:id`, is one statement: `DELETE FROM organizations WHERE id = $1::uuid`. It has no users check and does not delete rights holders.
- `rights_holders.organization_id` has no foreign key in ANY of its four CREATE definitions: `docker/init/07-rights-holders.sql:9`, `deployment/azure/migrate/seed-azure-dev.sql:8`, api-gateway `startup-migrations.ts:317` and originate `index.ts:444`. No migration creates it; 026-028 only alter it.
- So a successful gateway delete leaves that organisation's rights holders pointing at nothing, on a migrations-built database too. On a compose-built database it also leaves users, documents and the other referrers.
- **Measured** (probe C3): the gateway's statement as `secuura_app` under the bypass deleted the organisation (`DELETE 1`) and did not touch the 2 rights holders.
- The frontend's `frontend/admin/src/services/api.ts:908,916` calls this gateway route. Nothing in the repository calls originate's route (Q4).
- **Board:**
  - KS-2279 (read-only) is about this door's tenant bound. It never mentions rights holders, orphans or users-present (0 hits each).
  - KS-2312 names the gateway door only for the compose-built foreign-key gap.
  - KS-699 is the users foreign-key census.
  - None names the rights-holder orphaning on every build. I am not re-filing KS-2312 or KS-699. Whether this is a new ticket or an addition to KS-2279 is for Wednesday.

### LOW
**G396-2272-2: one surviving mutant, equivalent in practice.** M15 always reports the organisation deleted (`deleted: 1`, ignoring the DELETE's row count): 0 of 397 cells fail.
- Under the `FOR UPDATE` lock, in the same transaction and under the same bypass policy, the organisation's DELETE can only remove the 1 row the lock found, so the mutant is equivalent against a real database. Report only.

**G396-2272-3: the new 409 is not in the OpenAPI spec, because the whole route is absent from it.** `secuura-api.yaml` has no `/api/admin/organizations` path; its only organisation path is `/api/users/admin/organizations`. Control: `/api/gdpr/consent` matched 4 times in the same file. `check:openapi` PASS is therefore expected, and the PR body says so ("originate's `/api/admin` family is not in the spec"). This is pre-existing, as at KS-2302 (gate 393's commission Q5: no OpenAPI). It is not a defect of this PR.

**G396-2272-4: words and edges.**
1. PR body: "`rights_holders.organization_id` has no foreign key in any of its **three** definitions". There are **four** CREATE definitions (G396-2272-1). None has a foreign key, so the substance holds.
2. The count includes erased and deactivated users. `userErasedSubscriber` anonymises the row and keeps `organization_id`; `status` may be `deleted` or `deactivated` and the row stays. That is correct: where the users foreign key exists, those rows block the delete anyway. The consequence is that an organisation whose only users are erased cannot be deleted until a platform admin clears their `organization_id` (auth `users.ts:872-881` admits null for a platform caller; I read it, did not run it). Neither the PR nor KS-2306 says this. It is a product note, not a defect.
3. KS-2312's BLUF says "KS-2306 now protects the users case in **the one route** that deletes organisations". Two routes delete organisations, and the gateway's has no users check (G396-2272-1). The same ticket's body names the gateway door correctly.
4. Multi-tenant pool mode: the unit and the count run on the default pool, as the old code did, because the router sets `req.db = prisma`, adminConfig.ts:37. A users row in a separate per-tenant database would not be counted. This is unchanged behaviour and NOT MEASURED.

## The commission's questions
- **Q1 THE REFUSAL: holds.**
  - Cells, head: C1 with 1 and with 5 users answers **409** with body `{success:false,error:{code:'CONFLICT',message:'Organization still has users'}}` (the file's CONFLICT shape). Only LOCK and COUNT were issued, both inside the unit; zero deletes, zero withTenant calls.
  - **Real Postgres** (my probe; policies 027 and 039 verbatim; `secuura_app` NOBYPASSRLS):
    - (viii) Code path with a user present: the lock finds A and the count reads **1**. The state is unchanged (1/2/1/1/1/1).
    - (v) **A user of tenant B whose `organization_id` = A**: the count under the bypass reads **1**. Under tenant-A scope it reads 0. So the unit's scope sees every tenant's users rows.
    - (iv) reproduced: 1 under the bypass, 0 with no setting.
  - The bypass is the real `withPlatformScopeTransaction`'s first statement (db.ts:415); the pool branch uses `applyTenantGuc` (shared tenant-guc.ts:158).
  - Unreadable count (no row, null, non-number) answers 500, with no delete issued and nothing committed (C6). M13 (`Number(...)`) is killed by C6.
  - Soft-deleted and erased users are counted, correctly (G396-2272-4.2).
- **Q2 ALL-OR-NOTHING: holds.**
  - Every statement is on `tx`, inside `runWithPlatformScope(() => withPlatformScopeTransaction(...))`. Nothing runs on the module client or through `withTenant`: C2 asserts `issued == committed`, all via the unit, `withTenantCalls == 0`. P1 asserts `mockExecuteRaw` and `mockWithTenant` are never called.
  - C3: a throw at each of the 7 statements answers 500 with the constant body, nothing committed, 1 rollback.
  - **Real Postgres:**
    - (iii) reproduced: the FK error at the last statement rolled the unit back to the seed.
    - (i) reproduced: bypass only, rights holders 0 deleted, 2 orphaned.
    - (ii) reproduced: with `app.tenant_id`, exactly A's 2 deleted and B's kept.
  - **Transaction-local, measured (vi):** inside the unit `app.tenant_id` = A. After COMMIT the session reads `''` for both `app.tenant_id` and the bypass, and rights_holders shows 0 rows. After ROLLBACK it also reads `''`.
  - It does not reach any other policy: `current_setting('app.tenant_id'` appears only in 027 in the whole tree (control: 027 found). The later deletes in the unit use 039's bypass.
  - The 1:1 `tenant_id = organization_id` on rights_holders holds: 026 backfills it, and both insert sites (adminConfig.ts:1594, 2255) write the same id twice.
  - Container record: see How I measured.
- **Q3 THE LOCK: closes the gap where the users FK exists; no deadlock with the gateway's delete.** Measured with two concurrent sessions:
  - **C1 (FK present):** the unit held `FOR UPDATE` and slept 3 s. A users insert into A started 1 s later and **blocked** (52.408 to 54.392) until the unit committed, then failed with `users_organization_id_fkey`. End state: 0 users, 0 orphans.
  - **C4 (FK dropped, the compose-built case):** the same insert ran at once, the unit then deleted A, and **1 orphan user** was left. This confirms residual R1 exactly.
  - **C2 (unit first, gateway DELETE during it):** the gateway's DELETE waited for the unit's commit, then `DELETE 0` (the gateway answers 404). No deadlock.
  - **C3 (gateway DELETE first, unit during it):** the unit's `FOR UPDATE` waited 2.1 s for the gateway's commit, then returned **0 rows**, which in the handler is 'Not found' with nothing deleted. No deadlock.
  - Lock order: both doors take the organisation row first, so no cycle forms between them.
  - Any other cycle (a writer holding a document or member row lock and then touching the organisation's key) would be detected by Postgres and roll the unit back whole: 500, nothing deleted. That is reasoned, not run.
  - The lock wait counts against the 5000 ms single-tenant timeout (R2).
- **Q4 OTHER DOORS:** I grepped services/, packages/ and scripts/ for `DELETE FROM organizations|organization_members|rights_holders|documents|tenants` and for route deletes on organisation paths.
  - Hits:
    - originate adminConfig.ts (this PR);
    - api-gateway admin.ts:1599 (**G396-2272-1**);
    - `certificationRepo.ts:166` (one document by id and tenant; not an organisation cascade);
    - tenant-provisioning `index.ts:370` (a tenant row in the provisioning rollback; not an organisation).
  - No other route deletes an organisation or its dependants half-way.
  - Callers of originate's route: none. 0 non-test hits for `admin/organizations/` outside adminConfig.ts; control: `users/admin/organizations` in frontend/admin api.ts 5 times.
- **Q5 THE CELLS: reproduced.**
  - Head: ks2306 19/19, ks2302 31/31.
  - The head's two test files on develop's handler (in x, develop's adminConfig.ts written over the head's and restored): **ks2306 16 failed, 3 passed** (C5 x3 green); **ks2302 3 failed (P1 x3), 28 passed**. All 19 failures are assertions, none from the harness:
    - C1 x2: `409` vs `200`;
    - C2 x3: committed shape;
    - C3: the half-delete shape on the last three (+26/+18/+10 lines committed); `unitRollbacks` 1 vs 0 at rights holders; `500` vs `200` at set_config, count and lock;
    - C4: shape;
    - C6 x3: `500` vs `200`;
    - P1 x3: `not.toHaveBeenCalled` received 1.
  - **The mock is faithful on both named points:**
    - `mockInTransaction` pushes a unit's buffered statements only when `fn` returns, and drops them on a throw;
    - `withPlatformScopeTransaction` rejects when `scopeDepth === 0`, and M8 (wrapper removed) is killed by 16 cells.
  - It does not model the real unit's own bypass set_config, which is harmless.
  - Rows are keyed on SQL text, so M7 (`FOR UPDATE` removed) also dies through the lock returning no row. It dies on the LOCK shape assertions as well.
  - KS-2302's P1 mock does not refuse outside scope. C2 covers that.
- **Q6 MUTANTS** (head; the 24 originate test files that import adminConfig, 397 cells; BASE 0/397; evidence/mutants_run1.out and mutants_run2.out, mut/*.json):

  | mutant | failed | first killers |
  |---|---|---|
  | M1 rights_holders back on withTenant | 9 | C2 x3, P1 |
  | M2 documents delete on module prisma | 8 | C2, C3 |
  | M3 count removed (users = 0) | 12 | C1, C2 |
  | M4 count compared with 1 | 1 | C1 (1 user) |
  | M5 count after the first delete | 8 | C1, C2 |
  | M6 set_config removed | 7 | C2, P1 |
  | M6b set_config from the caller's tenant | 6 | C2, P1 |
  | M6c set_config not local (false) | 6 | C2, P1 |
  | M6d set_config after the rights_holders delete | 6 | C2, P1 |
  | M7 FOR UPDATE removed | 19 | C1, C2 |
  | M7b lock statement and not-found check removed | 10 | C1, C2, C4 |
  | M8 runWithPlatformScope wrapper removed | 16 | C1, C2 |
  | M9 / M9b / M9c 409 as 400 / as 200 / code ORG_HAS_USERS | 2 / 2 / 2 | C1 x2 |
  | M10 catch answers 200 | 11 | C3, C6 |
  | M11 platform guard removed | 8 | C5 x3 and KS-2302's refusal cells |
  | M12 count on the module client (outside the unit) | 16 | C1, C2 |
  | M13 null count read as 0 (`Number`) | 2 | C6 (no row, null) |
  | M14 count without the organisation bound | 8 | C1, C2 |
  | M16 member delete dropped | 7 | C2 |
  | **M15 org delete result ignored** | **0** | **survivor, equivalent (G396-2272-2)** |

  - My first M3 spelling (count and checks removed) did not compile: 17 suite errors, TS2367 on the never-taken `has_users`. It is recorded in mutants_run1.out. My first M9 spelling matched two `res.status(409)` sites in the file, and the assertion refused it before any write. I re-spelled both and re-ran them with the rest of the second batch.
  - The seat's M5 slip (P1 cannot see the order) is confirmed: P1 is not among M5's 8 killers, which are C1 x2, C2 x3 and C6 x3 (evidence/mut/M5.json).
  - The per-mutant JSON for the first batch is in evidence/mut/. Its summary file was not written because the batch stopped at the ambiguous M9 spelling.
- **Q7 WHOLE:**
  - Originate suite (default jest config, `--json`): develop **3085/3085 in 238 files**, head **3104/3104 in 239 files**. Failure sets are equal (both empty).
  - Per-test diff: 22 tests only on the head (19 ks2306 + 3 renamed P1), 3 only on develop (the old P1 names), **0 changed status**.
  - tsc 0 (planted: rc 2, 1 error).
  - eslint `--max-warnings 0` rc 0 on adminConfig.ts and both cell files, and on develop's adminConfig.ts (planted: rc 1).
  - check.cjs originate: 333 examined, 272 under `__tests__`, 0 new (planted: 1 new, rc 1). Fragments OK (planted: FAIL). check:openapi CHECK PASS (G396-2272-3).
  - Standalone ratchet: originate, auth, vc-issuer, security and m365 OK.
    - **api-gateway reports 2 new (ks815, TS2345) on BOTH arms**, identical on develop (evidence/ratchet_standalone_d.out). This is my clone's missing api-gateway install, as gate 395 found. The leg test (45/48) is that one result. **The api-gateway leg is UNMEASURED here, not red against the PR.**
  - Overlap: 19 open PRs; none other touches any of the 5 paths. Control: package-lock.json is in 11; adminConfig.ts is only in 2272. No file list reached 100.
  - merge-tree onto live develop: **rc 0** (tree = head tree). Planted control: local commit 139b39c500ed adding a comment to develop's `withTenant(... rights_holders ...)` line gives **rc 1**, CONFLICT (content) in adminConfig.ts.
- **Q8 WORDS:**
  - PR body: summary, rule, order, 409 body, behaviour change (absent organisation deletes nothing, still 200 'Not found': **stated**, and C4 pins it), callers, and the figures all reproduce: 16/3, 3/28, 19/19, 31/31, 3085/238, 3104/239, 333, the mutant list, and Postgres (i)-(iv). The one exception is G396-2272-4.1.
  - Residuals:
    - R1 is accurate (my C4 measured it).
    - R2 is accurate (db.ts:391, no options).
    - R3 is accurate; the referrer list matches 001/002's NO ACTION keys.
    - R4 is KS-2312 (Backlog, priority 3, 0 comments).
    - R5 is accurate.
    - Missing from the residuals: the gateway door (G396-2272-1). Strictly it is outside this route, but it is the used one.
  - NOT run is honest. Node 26 is disclosed. "Concurrent-insert window … reasoned, not exercised" is now exercised here (Q3).
  - KS-2306 (read-only): In Progress, priority 3. Its text predates the ruling and lists the three options neutrally. Its claim "the gateway's own delete … cannot half-delete; it fails whole when a foreign key stops it" holds for the foreign-key-bound tables but not for rights holders (G396-2272-1).
  - Facts comment defe7c85 (2,386 B; updatedAt .779Z is not after createdAt .789Z, so unedited): every sentence holds.
  - The handler's doc block holds ("a users insert takes KEY SHARE … which FOR UPDATE blocks": measured, C1). The fragments hold.

## Two-NO-GO cap
Not engaged.

## Faults, disclosed
- Two zsh-hook refusals before running: an `=====` separator, and a `git -C $W/x checkout` the hook read as pointing outside. I replaced the checkout with `git show … > file` in my own worktree. Neither ran anything.
- The first M3 spelling did not compile and the first M9 spelling was ambiguous (Q6); both were re-spelled and re-run.
- A sed slip in my Linear-read copy read KS-2306 twice before KS-2312. I re-ran it correctly; both were read-only.
- No mail, no `cut -c`, no cd, no rm.

## Not run
- A booted originate or gateway, any request over the network, any deployed database (local stack, Kintsugi, demo).
- The multi-tenant pool path (G396-2272-4.4); the four platform suites; Node 24; the api-gateway ratchet leg on a proper install.
- A Prisma interactive transaction against the real Postgres (my probe runs the unit's SQL through psql as `secuura_app`, not through Prisma).
