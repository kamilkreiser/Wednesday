GO WITH NOTES — MERGE (no HOLD-FOR-KAM)
# QA Gate 189 (Tier 1, round 1): PR 2001 / KS-1256 connector allow-list still fails open when the settings key is missing

## Subject
- Repo Secuura/Distributed_Secuura, PR 2001. Pinned by `git ls-remote origin` on the read-only checkout:
  - START 2026-11-04T11:57:45Z: head `74ccf8666dc2673ed863451bb8eadc9dcd299098`, develop `536642104002f506f61e2e9b6c98a32bf19c3b10`.
  - END 2026-11-04T12:18:35Z: head `74ccf8666dc2673ed863451bb8eadc9dcd299098`, develop `536642104002f506f61e2e9b6c98a32bf19c3b10`. Neither moved.
- Merge base `d92b849ece732cd04e283bfcb0ee9e8bd6989631`. `git merge-tree --write-tree 536642104002 74ccf8666dc2` (in my clone): **rc 0, tree `f61c498171e3758996c918f8a41d62942df5b053`**.
- Host: macOS, Node v26.8.1, npm 11.19.0, vitest 4.1.12 (from the head lock), TypeScript from the head lock, PostgreSQL 15.19 (Homebrew keg), Redis 8-alpine (local image `21090af93f83`, the compose image tag). NOT run on Node 24, a real deploy, kintsugi, or real clients (Platform S).
- Dependencies: `npm ci --ignore-scripts` at `Blockchain/Dev` from the head lock into my clone (1798 packages). Nothing linked from the shared checkout.

## Method
I cloned the checkout (`--shared`) into `repo/` and fetched the PR ref and develop from GitHub into my clone only. I wrote my own harnesses, not copies of the seat's. They drive the real routers over real HTTP:
- `harness/g189-matrix.test.ts` plus `harness/judge.py`: 600 cells. Redis {up, down (in-memory fallback), throws} x key {R restricted, O open, S seed, B bypass, missing} x row {R, O, S(seed), B, missing, db-down, read-throws, not-object} x reader {create-out `diploma`, create-in `SSD_DOCUMENT`, create-default (no type), info, put}. The put reader also runs a follow-up restricted create with Redis back up. The doubles honour the three SQL statements' semantics.
- `harness/g189-real.test.ts` and `g189-real2.test.ts`: the real `services/redis` (ioredis) against a throwaway `g189-redis` container (allkeys-lru), and the real `db` pool against my own Postgres cluster (`tmp/pg`, 127.0.0.1:56390). The app role gets privileges only through default privileges, as `docker/init/01-create-app-role.sh:64-71` grants them. Health is wired as `index.ts:855` wires it, with the default settingsDb.
- Base = develop 536642104002's `admin.ts`, `verification.ts` and `health.ts` swapped into the same tree, with `settingsStore.ts` moved aside. The three files are restored after each base run, and `git status` shows no diff against head.
- `harness/mutants.py`: 8 mutants of my own, scored by my matrix and by the PR's committed tests.

## Findings

### G189-F1 — MEDIUM: on a gateway with no usable DB, every settings save is refused, and a missing key refuses every connector create/info
- **FOUND:** with `isDbAvailable()` false, PUT /api/admin/settings answers 503 in every Redis/key state. Develop answers 200. With the key also missing, create and info answer 503, and no in-app path can write the key, because PUT is refused too. This is stricter, not looser: an availability regression for any env that runs the gateway without `DATABASE_URL` (db.ts:169 "running with in-memory storage only"), or during a DB outage.
- **TESTED:** matrix cells put x {up, down} x {R, O, S, missing} x db-down: head 503 with 0 Redis writes, base 200. Create/info up/missing/db-down: head 503, base 201/200. Doubles only. I did NOT measure whether any deployed env runs DB-less.
- **HOW:** `runs/matrix_head.jsonl` vs `runs/matrix_base.jsonl`, `runs/judge.out` (stricter list). Control: the same cells with row R and db `ok` answer 200 at head.

### G189-F2 — LOW: the deploy step 3 check ("configured env reads `backfill`, fresh reads `seed`") does not tell the two apart
- **FOUND:** on a fresh env, the first miss refills Redis with the seed. The next Redis hit then runs the conditional backfill over the seed row, so a fresh env reads `origin = backfill` (seed content) from its second read on. A configured env whose key was already evicted at deploy is identical to a fresh one at every step. So the step-3 SELECT can show `backfill` while nothing configured was copied. This is not looser than develop, where a missing key already meant no restriction. It weakens the stated mitigation for candidate 5. Step 2 (check the key before deploy) is the part that actually protects.
- **TESTED:** real Redis + real Postgres + real modules, GET /api/connector/info as `index.ts` wires it. Three scenarios, two reads each.
- **HOW:** `runs/real2_head.jsonl`: fresh `seed` then `backfill`; configured with key present `backfill` (restricted) then `backfill`; evicted at deploy `seed` then `backfill`. The real sequence `runs/real_head.jsonl` step 1 also ends at `backfill` after 5 reads on a fresh env. Mechanism: `settingsStore.ts` `readPlatformSettings` refill plus `backfillSeedRow` (runs on any plain-object hit).

### G189-F3 — LOW (the seat's candidate 2, confirmed): Redis and the record can diverge after a save
- **FOUND:**
  - When the Redis write fails after the DB write, the response is 503 "Platform settings were stored but the cache could not be refreshed; save again". The row holds the new value, Redis keeps the old one, and the live answer follows Redis until the next eviction, which then flips to the row. Same class: a PUT during a Redis outage answers 200, writes the row and the in-memory store, and Redis comes back with the old value.
  - Develop in the same faults: the Redis-write fault hangs (status -1, unhandled rejection, nothing stored); during an outage the save goes to the in-memory store only.
  - Neither path is looser than develop. A save that adds a restriction and hits this fault leaves the old, looser value live until the retry the 503 asks for, as develop does.
- **TESTED:** real Redis set to `noeviction` + `maxmemory 1` (SET answers OOM, GET still works); real Postgres. Outage = the container stopped.
- **HOW:** `runs/real_head.jsonl` step 8: put 503, redis restricted (old), row open (new), create-out 403 while stale. Step 8b: after a DEL, create-out 201 and Redis refilled with open. Step 10: putDuringOutage 200, row open. Base: `runs/real_base.jsonl` step 8 put -1.

### G189-F4 — LOW: in the item-6 row, the info reader also changes. It reports the restored bypass.
- **FOUND:** Redis up / key missing / bypass row, GET /api/connector/info. Develop: `200 [] enforce`. Head: `200 ['SSD_DOCUMENT'] bypass`. The type list is stricter and `workflowPolicy` is looser. My judge counts it looser because of the policy. It grants nothing by itself, since enforcement is on the create path. It reports the same restored configuration as the accepted item-6 create cell (create-in 201 via the workflow gate at develop, 201 skipping it at head). It is in the same accepted row, so I do not write HOLD-FOR-KAM. **Wednesday to confirm it falls inside the item-6 acceptance.**
- **TESTED:** matrix only (doubles).
- **HOW:** `runs/judge.out`, "BYPASS cells that differ" (24 outcome-differences of 180; 2 ranked looser: create-in and info, both up/missing/B).

### G189-F5 — LOW: the real-engine test imports a package api-gateway does not declare
- **FOUND:** `ks1256-settings-store-statements-on-a-real-engine.test.ts:15` imports `@electric-sql/pglite`. In the lock it comes only from `node_modules/@prisma/dev`, another workspace's transitive dependency, through hoisting. With a workspace-scoped install (`--workspace=services/api-gateway --workspace=packages/shared`), 2 files fail: the import, plus KS-1090's type-check baseline gets 1 new TS2307. The suite passes with a full root `npm ci` (what ci.yml:36 runs). The gateway Dockerfile build excludes `src/__tests__`, so images are unaffected.
- **HOW:** `runs/suite_head.out` (scoped install: 152/154 files) vs `runs/suite_head2.out` (full install: 154/154 files, 1623/1623 tests). The lock was scanned for declarers of pglite: only `@prisma/dev`.

### G189-F6 — LOW: some states have no in-app recovery
- **FOUND:** with the key AND the row missing, PUT is refused (503 "could not be read"), so an admin cannot recreate the settings without SQL or a migration re-seed. With malformed bytes in the Redis key, PUT is refused (503). That case is PRE-EXISTING in effect: develop hangs on the same PUT.
- **HOW:** `runs/real_head.jsonl` steps 6 and 9; `runs/real_base.jsonl` step 9 (put -1).

### G189-F7 — INFO: one of my mutants survives the PR's tests, and it is equivalent
- **FOUND:** M5 (the `isPlainObject` guard on the row replaced by a null check) passes all 31 PR tests. My matrix kills it (7 cells). It is equivalent in production: the table's `CHECK (jsonb_typeof(settings) = 'object')` refuses a non-object row. Measured on real PG: UPDATE to `[1,2]` gives a check-constraint violation; control UPDATE to `{"a":1}` gives UPDATE 1. One caveat: `CREATE TABLE IF NOT EXISTS` would keep a pre-existing table that lacks the CHECK.

## What passed (measured)
1. **Scope:** `git diff --name-only d92b849e 74ccf866` gives 19 files, +709/-28. They are: migration 057; 13 api-gateway tests (2 new, 11 edited); `admin.ts`, `verification.ts`, `health.ts`, the new `settingsStore.ts`; the two KS-1256 doc fragments. None is outside the declared scope.
2. **Matrix, 600 cells, my harness:**
   - In-ratio (no B key, no B row): 420 cells: **0 looser**, 40 stricter, 380 same. The seat reported 47/373/0. The difference is my reader set (create-default instead of the seat's create-owner) and my put ranking (follow-up create rank, then success). The looser count agrees.
   - Bypass: 180 cells; 24 outcomes differ; 2 ranked looser (item-6 create-in, plus F4 info).
   - Positive control: the judge run with base and head swapped reports 40 looser.
3. **Real Redis + real Postgres** (head | base). Note on base step 5: base never refills, so the key was already gone and no real eviction took place at base.
   - Key present: create-out 403 | 403; create-in 201 workflow | same; info [SSD, marker] | same.
   - Key DELETED with Redis up: create-out **403** | **201** (the defect, reproduced red at base); info [SSD...] | []; Redis refilled at head.
   - REAL allkeys-lru eviction (maxmemory 3mb, 80 filler keys, `evicted_keys:18`, key gone): head create-out **403**, key refilled.
   - Key + row missing: 503/503/503 | 201/201/200.
   - Row unreadable (SELECT revoked from the app role): 503 | 201.
   - Redis down (container stopped, `isRedisAvailable()` false observed): 503 on create/info, both sides.
4. **First boot** (fresh DB with 057 applied, empty Redis, real stack): create-out/in/default 201 through the workflow gate, info `[]`, admin GET without integrations. Identical on head and base. An API-key (connector) create does not 503.
5. **PUT ordering:**
   - DB write refused (INSERT/UPDATE revoked): 503 "could not be stored; nothing was changed", Redis byte-identical before and after.
   - Redis write fails after the DB write: 503 "save again", row new, Redis stale. Graded LOW (F3).
   - Mutant M8 (Redis before DB) is killed: 72 matrix cells, and 3 PR tests fail.
6. **Migration 057:**
   - Develop 536642104002 tops out at 056; 057 is absent.
   - Across 1920 PR heads, the ones not merged into develop add these 05x+ migrations: only PR 2001 (057) and PR 2002 (058, KS-1401). Control: PR 1383's 049 found.
   - Applied twice on real PG: rc 0 both times, still 1 row, origin seed (CREATE TABLE skipped, INSERT 0 0).
   - The app role got SELECT/INSERT/UPDATE through default privileges.
   - Seed == develop's defaults (`admin.ts:1144-1149` at develop) == head `settingsStore.ts:38-43`. Compared programmatically; a control with one planted value change compares unequal.
   - Filename has no "platform", so it routes to the main DB (`startup-migrations.ts:101`).
   - No down path: 0 down files among 59 migration files.
7. **Mutants:** 8 of my own, on the DB-fallback and 503 branches plus 2 on PUT. **8/8 killed by my matrix; 7/8 by the PR's committed tests.** Survivor: M5 (equivalent, F7). M1, M2, M3, M7 and M8 match the intent of the seat's M4, M1, M2, M7 and M8. Raw table: `runs/mutants.out`. Red first: with develop's readers, the PR route test fails 14 and passes 9 (23) by assertion, and the engine test fails on import, as the READY says.
8. **No new leak:** marker `G189MARK_*` was planted in the allow-list and in malformed Redis bytes.
   - Head: 0 log lines carry it, besides the positive control `G189MARK_CTRL` (1 line found). 0 lines carry `SSD_DOCUMENT`.
   - Base: 2 lines carry it, in unhandled-rejection dumps (the ioredis SET args and the JSON.parse message).
   - Responses carrying the marker are only PUT-200 settings echoes and info-200 lists, which develop also returns. The 503 bodies carry no values.
   - Every new warning logs only the reason or errorClass.
9. **Title and body:** title "Refs KS-1256: an evicted platform-settings key reads the stored record, not no restriction" is **90 chars** (≤ 92). Body: the GitHub API is unreachable without auth (unauthenticated 404; public control 200). I read the seat's `drafts/body.md`: its sha1 without the trailing newline equals the posted `body_sha1` 55a4d097 in the seat's `pr/record.json`. It has 0 close-word-before-key hits; control: the `Refs KS-` regex finds 1. "Before this deploys" steps 1-3 are present (step 3 = the first-hit read-back, see F2). The live body is not read by me.
10. **Merge:** merge-tree on 536642104002 gives rc 0, tree f61c4981. Develop moved d92b849e..536642104002 (3 commits, 11 files); overlap with the 19 PR paths = **0**. Control: develop's list against itself = 11.

Also: the full api-gateway suite at head is 154/154 files and 1623/1623 tests (full install), equal to the READY.

## NOT tested
- Node 24; a real deploy or the `migrations` image; kintsugi; Platform S or any real client; the four platform suites.
- The real `authenticateToken` on the create path (pass-through stand-in), `enforceDocumentTypeRules` and the real workflow gate (stand-ins).
- Multi-replica gateways racing the backfill.
- Redis with `requirepass` and AOF persistence as compose runs it (my container ran without a password and without persistence).
- Whether any env runs the gateway without a DB (F1 reachability), and whether any deployed Redis has already evicted the key (F2 exposure).
- The live PR body through the GitHub API (hash-matched draft only).
- eslint/tsc for the product (I did not re-run them; the seat reports tsc rc 0).

## Plain answer for Kam
Today, if Redis quietly drops the settings entry to save memory, a connector that is restricted to some document types can register any type. With this change the settings are also kept in the database, so a dropped entry is read back from there and the restriction holds. I proved that on a real Redis by forcing a real eviction. A brand-new environment behaves exactly as it does today. Nothing in my 420-cell comparison gets more permissive. The one accepted exception (a connector configured to skip approvals keeps skipping them after an eviction) shows up as expected, and the connector info page now reports that setting too. The catches are small: a gateway running with no database can no longer save settings; the post-deploy check in the PR description can't tell a fresh environment from one that already lost its settings; and a save that half-fails tells the admin to save again, while the old value stays live until they do.
