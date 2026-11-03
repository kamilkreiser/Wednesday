GO WITH NOTES. HOLD-FOR-KAM (one money ruling: the AMBASSADOR 5% ongoing bonus goes live with this fix, G162-F4). Nothing is FIX-BEFORE-MERGE.

# QA GATE 162: Secuura Platform K PR 1979 (KS-1956, referral milestone awarded once; a failed read awards nothing), TIER 1, round 1

## BLUF
- **Headline: on a real PostgreSQL 15, no path I could drive awards the same user + milestone twice at head.** The highest count of reward rows for one user + milestone is **1 in every one of 18 head cells that have the rewards table with a primary key on `id`**. Base reaches 2, 3 or 4 in the same cells (table below).
- **The `ON CONFLICT (id)` dedupe needs a unique index on `id`, and the repo has no DDL for `svc_referral_milestones_rewards` at all** (G153-F4 stands). Measured: with a PK it dedupes, including two forced-concurrent checks from two processes. With no unique index the INSERT fails 42P10 on every call, at base AND head, so nothing is ever stored. Head then answers "No new milestones achieved". Base answered awards it never stored.
- **The declared behaviour change is real.** On the schema the repo DDL builds (no rewards table), head never awards a milestone: POST /check gives 200 "No new milestones achieved", 0 rows. Base answered 200 with the milestones listed and stored 0 rows. **Production: UNMEASURED.** Nothing in the repo shows production's schema.
- **Money (G162-F4, HOLD-FOR-KAM):** per-milestone amounts, status (CLAIMABLE) and recipient are unchanged. One multiplier changes. Because the progress save now works, `currentTier = AMBASSADOR` is persisted for the first time. The next `/qualify` for that referrer pays **52.5 SECURA (50 + 5%) at head against 50 SECURA at base**, measured. This is the designed rule (`ongoingBonus: 5` on the AMBASSADOR milestone), but it was dead at base and the PR does not declare it.
- Mutants: 14 run on the unit cells, **9 killed and 5 survived**. Of the 5: 2 are equivalent; 1 (an SQL-predicate change) survives only because the author's in-memory model ignores the SQL, and my real-PG R5 cell kills it; 2 are LOW display gaps.

Subject:
- Head `eeb4ab58d6d110d9bd14119d0c78c0e28e58f2d2`, equal to the pin at START (00:45:58Z) and END (01:05:31Z), in logs/head_start.log and logs/head_end.log.
- Base `66cbe4e52d5a`.
- develop was `2a827aac` at START. **At END it was `0a6575f7`**, two squashes further on (billing, transfer).
- Host Node v26.8.1 (not LTS 24; nothing was measured on Node 24). PostgreSQL 15.19 (postgres:15-alpine, the image docker-compose.yml uses).

## How I measured
- **Clone:** `git clone --shared` of the read-only checkout into `repo/`, then I fetched `refs/pull/1979/head` and develop into my clone. Push URL is `no_push_qa_gate`. Worktrees `wt/base` and `wt/head`.
- **node_modules:** the lockfile, root package.json, referral package.json and packages/shared are byte-identical (same blob ids) to gate 153's clone, so I copied that clone's installed node_modules (APFS clonefile, read-only on gate 153's side) and built packages/shared here (rc 0).
- **Database:** a throwaway container `g162-pg`, volume `g162-pgdata`, trust auth on 127.0.0.1 only, so there is no secret in any file.
  - Schema: the repo's referral DDL (`docker/init/04-sprint2-service-tables.sql` lines 497-576, saved as scripts/referral_ddl_from_repo.sql).
  - Plus, per variant, `svc_referral_milestones_rewards`:
    - `pk`: mirrors `svc_referral_rewards`, `id TEXT PRIMARY KEY`
    - `nouniq`: the same columns, no unique index on `id`
    - `absent`: what the repo DDL builds
  - The service connects as a non-owner role `g162_app`.
- **Service:** for every cell, the real referral service process (node + tsx, the real index.ts / db.ts / services / winston logger / shared `authenticate()` with an RS256 token, real `pg`), driven over HTTP. **Nothing in the service is stubbed.**
- **Faults are injected natively by an admin connection:**
  - `REVOKE SELECT` makes a read fail (42501).
  - A `BEFORE INSERT/UPDATE` trigger that RAISEs makes a save fail.
  - `ALTER ROLE ... NOLOGIN` + `pg_terminate_backend` refuses connections.
  - An admin transaction holding `LOCK TABLE svc_referral_milestones_rewards IN EXCLUSIVE MODE` forces the race: SELECTs pass, INSERTs wait, and I confirmed both racers were blocked on the INSERT in `pg_stat_activity` (blockedOnInsert = 2) before committing.
- **Files:** scripts/g162.cjs (driver), scripts/matrix.sh. Raw results in logs/probe/*.json, condensed in logs/probe_table.log.

## G162-F1: HEADLINE, can any path award the same user + milestone twice? (FOUND: no, at head with a PK on id. TESTED: real PG, real process. HOW: 44 cells)
"rows" = reward rows in `svc_referral_milestones_rewards`; "max" = the highest count of rows for one user + milestone.

| cell (mr = pk) | what happens | base rows / max | head rows / max | head answers |
|---|---|---|---|---|
| R3 consecutive | 1 referral, 3 checks | 3 / **3** | 1 / **1** | FIRST, none, none |
| R4 forced race, 2 processes | lock held, both checks blocked on INSERT, then released; then a 3rd check | 3 / **3** | 1 / **1** | one FIRST, one "No new"; 3rd none |
| R4 forced race, 1 process (2 pool connections) | same | 3 / 3 | 1 / 1 | one FIRST, one "No new" |
| R4 natural | 20 users x 5 referrals, 2 processes, both checks at once, no lock | 80 / 2 | **40 / 1** (answered new = 40) | |
| R5 legacy random ids | FIRST CLAIMED + BRONZE CLAIMABLE under v4 ids, no progress row, 5 referrals, 2 checks | 6 / 3 | **2 / 1** (the 2 legacy rows) | none, none; progress now records FIRST + BRONZE, total 600 SECURA |
| R6 progress read fails | REVOKE SELECT on svc_referral_milestones; FIRST already CLAIMED; 5 referrals, 2 checks | 5 / 3 | **1 / 1** | none, none |
| R7 awarded (any-status) read fails | REVOKE SELECT on the rewards table, 1 referral | 0 / 0 * | 0 / 0 | none (log: "DB read awarded milestones failed", warn "awarded nothing") |
| R8 connections refused | check (FIRST) -> NOLOGIN + terminate -> 2 checks -> LOGIN -> check | 2 / 2 | **1 / 1** | FIRST, none, none, none |
| R9 read fails between checks | check@1 (FIRST) -> +4 referrals -> progress read revoked -> check -> grant -> 2 checks | 7 / 4 | **2 / 1** | FIRST, none, BRONZE, none |
| R10 progress save fails after reward rows are written | trigger on the progress table; 2 checks, then clear, 2 checks | 4 / 4 | **1 / 1** | FIRST, none, none, none; progress row written on check 3 |
| R11 reward save fails | trigger on the rewards INSERT; check, then clear, 2 checks | 2 / 2 | **1 / 1** | none, FIRST, none |
| /qualify | 3 pending referrals qualified one by one, the 2nd with the progress read revoked | 3 / 3 | **1 / 1** | qualified x3 |
| AMBASSADOR | 1000 referrals: check, qualify 1, check | 18 / 3 | 6 / 1 | 6 new, then none |
| amounts | 999 referrals, 2 checks | 10 / 2 | 5 / 1 | 5 new, then none |

\* At base, R7 also stores nothing: PostgreSQL refuses `INSERT ... ON CONFLICT` without SELECT privilege ("permission denied"). Base still ANSWERED FIRST_REFERRAL twice.

Other points:
- **The derived id is stable across processes and runs.** User a1 + FIRST is `7b126ab8-a05b-5bcd-...` in every head cell, which is why the two-process race dedupes.
- **The racer that loses** gets `rowCount 0` from the INSERT and answers 200 "No new milestones achieved". It still records the milestone in progress, so the progress row is consistent.
- **No path awarded twice at head.** Paths I could not drive are listed under NOT tested. One of them is a reward INSERT that commits while the client sees an error. By READ, the next check finds the row in the any-status read and does not re-award. R5 and R10 measure that same mechanism.

## G162-F2: the ON CONFLICT (id) dedupe needs a unique index on id, and no DDL in the repo provides one (FOUND. TESTED: nouniq cells. HOW: real PG)
- `git grep -i svc_referral_milestones_rewards` at head finds it only in milestoneService.ts, the two milestone tests and the two KS-1956 fragments. There is no CREATE TABLE anywhere. The `svc_referral_milestones` control is in 3 SQL files.
- **With no unique index:** every INSERT fails with `there is no unique or exclusion constraint matching the ON CONFLICT specification` (42P10), at base and head alike. That gives 0 rows in consecutive, forced race, /qualify and amounts.
  - Head answers "No new milestones achieved" every time.
  - Base answered every milestone as new, every time, and stored nothing.
- So the dedupe is exactly as strong as production's constraint on `id`. If production has the table, its INSERT has only ever worked if `id` is unique (the statement is unchanged from base). That inference is the author's, and it holds. **Production's actual DDL: UNMEASURED.**

## G162-F3: the behaviour change, schema from repo DDL (FOUND: as declared. TESTED: absent cells)
- **Table absent, healthy DB:**
  - head: 3 checks, each 200 "No new milestones achieved"; 0 rows; no progress row. Log: `DB read awarded milestones failed {"error":"relation \"svc_referral_milestones_rewards\" does not exist"}` and the warn.
  - base: 3 checks, each 200 "Congratulations! ... FIRST_REFERRAL"; 0 rows stored.
- **Same with 999 referrals:** head 0 new; base 5 new twice.
- **/qualify** still qualifies and creates the referrer's 50 SECURA REFERRER_REWARD at both.
- **Production: UNMEASURED.** Nothing in the repo shows production's schema:
  - no DDL for the table
  - no migration
  - no deployment script that creates it

  If production lacks the table, milestones stop being announced there. None was ever stored there, so no stored reward is lost. If production has the table with a unique id, head awards exactly once. I do not guess which.

## G162-F4: money shape (FOUND: one undeclared multiplier change. TESTED. HOLD-FOR-KAM)
**Unchanged, base = head:**
- Per-milestone amounts, read from the stored rows: FIRST 100,000,000; BRONZE 500,000,000; SILVER 2,500,000,000; GOLD 10,000,000,000; PLATINUM 50,000,000,000; AMBASSADOR 100,000,000,000 (6 decimals, so 100 / 500 / 2,500 / 10,000 / 50,000 / 100,000 SECURA).
- type `MILESTONE_REWARD`, status `CLAIMABLE`, `user_id` = the checked user, `source_id` = the milestone id, `source_type` `MILESTONE`.
- The referrer reward on /qualify: 50,000,000, `REFERRER_REWARD`, to the referrer.
- No code path's amount or recipient is changed by the diff (READ).

**Changed:**
- **The AMBASSADOR ongoing bonus.** `referralService.qualifyReferral` adds `ongoingBonus` (5%) when `getUserProgress(referrer).currentTier === AMBASSADOR`.
  - At base the progress save threw on BigInt whenever a milestone was newly achieved (G153-F1), so `current_tier` was never written and the bonus was never paid.
  - At head the save works, and the AMBASSADOR cell measured `currentTier AMBASSADOR`, `ambassadorBonus: 5`. The next /qualify stored **REFERRER_REWARD 52,500,000 with metadata `{"ambassadorBonus":5}`**. Base stored 50,000,000 with no bonus.
  - This is the designed rule, newly live, for referrers with 1000+ qualified referrals. **Kam to rule:** accept it as intended, or hold the bonus until it is reviewed. It is not a bug in the diff.
- **Display-only effects of the same fix:**
  - GET /api/milestones/user shows the tier, the achieved list, the total and `activeBenefits` (e.g. "10% fee discount" for SILVER).
  - The leaderboard's `current_tier` is now populated.
  - I found no code in the referral service that enforces a fee discount (READ). Consumers outside the repo: NOT tested.

## G162-F5: a failed read awards nothing; what every caller returns (TESTED: real router, base vs head)
| caller, progress read failing (REVOKE) | base | head |
|---|---|---|
| POST /api/milestones/check | 200, FIRST+BRONZE re-awarded each time (5 rows) | **200 "No new milestones achieved"**, 0 new rows |
| POST /api/referrals/qualify (2nd, read revoked) | qualified; REFERRER_REWARD 50 SECURA; FIRST re-awarded | **qualified; REFERRER_REWARD 50 SECURA (no bonus); no milestone row** |
| GET /api/milestones/user (progress) | 200, tier null, 0 SECURA, achieved [] | same |
| GET /api/referrals/user (getUserStats) | 200, tier null, 0 achieved, 0 pending | same |
| ambassador bonus under a failed read | getUserProgress falls back to fresh -> 0% | same (READ: getUserProgress and dbGetUserProgress keep the null fallback) |
| GET /api/rewards/user | 4 pending (1200 SECURA): the duplicates this cell's checks minted | 0 pending: nothing was minted |

The GET rewards difference comes from the awards, not from the read path. Every read-only caller is base = head.

## G162-F6: the three changed KS-1868 cells (C1, R1, R2) and the BigInt replacer (FOUND: right reason, nothing weakened. TESTED)
**The cells:**
- The only change is the expected outcome, `OK {1,1}` -> `NOT_AWARDED {0,0}`, for a FAILED reward save.
- The log assertions are untouched: the count is still 1, and the reason is still `db boom` / `unreadable thrown value`.
- The `toEqual` is still exact.
- The reason is right: at head a reward row that is not stored is not answered as an award, and that is what makes the next check award it once (real-PG R11: none, then FIRST, then none, 1 row).
- **Red first, measured:** base milestoneService.ts under head's tests gives **17 failed | 6 passed (23)**. Every failure is an assertion: the 14 new RED cells plus the 3 changed ones. This equals the author's "17 cells failed".

**The replacer:**
- It writes the BigInt as a decimal string.
- On real PG the JSONB reads back as `milestone-first/100000000`, and GET progress shows `FIRST_REFERRAL:100 SECURA`.
- `rowToProgress` keeps it as a string. Every reader uses `Number(...)` or `String(...)`; nothing does BigInt arithmetic on the stored value (READ).

## G162-F7: mutants (TESTED. logs/mutants_table.log and logs/mutants_realpg.log, sha-restored, restore equal True)
14 product mutants, each run on the ks1956 file and both ks1868 milestone files (32 cells). **9 killed, 5 survived.**

**Killed:**
| mutant | killed by |
|---|---|
| M1 random id | R4 |
| M2 stored-rows map ignored | R5 |
| M3 failed progress read = no row | R6, R7 |
| M4 failed awarded read = empty map | R8 |
| M6 rowCount ignored | R4 |
| M7 failed save still awarded | ks1868 C1/R1/R2, ks1956 R11 |
| M8 "exists" answered as new | R4 |
| M9 replacer dropped | R1, R2, R4, R5, R10 |
| M14 id keyed on milestone only | C2 |

**Survived:**
- **M5** (`if (!read.ok || !awarded)` -> `if (!awarded)`): EQUIVALENT. `awarded` is null whenever the read failed.
- **M10** (no DB = no row): EQUIVALENT. The awarded read also returns null with no DB, as the author says.
- **M11** (the awarded read restricted to `status = 'CLAIMABLE'`): survives the unit cells because **the author's in-memory model filters in JS and ignores the SQL's WHERE clause**. **On real PG it re-awards a CLAIMED FIRST_REFERRAL: 3 rows, max 2.** The real-PG R5 cell kills it. LOW test gap: the SQL predicate is guarded only by a real database.
- **M13** (the total is not incremented when stored rows are reconciled): survives. Real PG shows GET progress total `0 SECURA` instead of `600 SECURA` after the R5 reconciliation. No cell asserts the total. LOW, display.
- **M12** (`achievedAt` = now instead of the first award time): survives. Display only. LOW.

## G162-F8: author's figures re-measured (TESTED)
**Referral suite** (vitest `--root` = the worktree's services/referral, cwd = logs/child_cwd, TMPDIR in the scratchpad):
- head **13 files / 94 cells**:
  - run 1: 1 failure, the db pool file's `control ks1868 C1` timing out at 16,220 ms. That is the known cold-import timeout (G153-F8) in a file this PR does not touch.
  - run 2: 94/94.
- base **12 / 77**, rc 0.
- That is +17, which equals the 17 new cells: C1-C3 + R1-R5 + R6 x4 + R7-R11. All of this matches the author.

**tsc:**
- With the tests included (service config, `declaration` off for the worktree symlinks): head **0** errors over 16 test files, base **0** over 15. A planted error gives 1.
- Service `tsc --noEmit`: rc 0 at head and at base.
- Without `declaration: false`, my first tests-included run showed 2 TS2742 at BOTH versions. That is a worktree-symlink path artefact, not the PR.

**Other:** the "eight mutants, 7 killed" in the fragment is consistent with my 14.

## G162-F9: develop moved, merge-tree (TESTED. logs/merge_tree.log, logs/merge_tree_2a827aac.log)
- Base 66cbe4e5 is an ancestor of develop.
- **Onto 2a827aac** (the pin): rc 0, tree `1f06759b`, 0 shared paths.
- **Onto 0a6575f7** (develop at END: 19fc6830 originate, 2a827aac governance, c6f4cc2f billing, 0a6575f7 transfer):
  - rc 0, tree `4e60e1c5`
  - **0 shared paths** with the PR's 5 (positive control: develop against itself = 19)
  - 0 develop paths under services/referral, packages/shared or package-lock
  - the merged services/referral subtree (`3110a616`), packages/shared and package-lock are **byte-identical to head's**, so every head cell stands for the merged tree
  - merged vs develop = exactly the PR's 5 paths

## G162-F10: pre-existing, not this diff's
- **HIGH (data, pre-existing; not cleaned, as the PR declares): the duplicate CLAIMABLE milestone rows already stored stay stored.**
  - GET /api/rewards/user counts them as pending with `canClaim` (G153). Head stops new duplicates; it does not remove old ones.
  - At head, the reconciliation records each milestone once in progress, but every legacy duplicate row is still a pending reward.
  - Needs a data decision and ticket (a one-off dedupe of stored rows, keeping the earliest).
- **HIGH (pre-existing, G153-F3, KS-1957 next): POST /api/milestones/check/:userId and /qualify have no owner or role check** (READ; unchanged by this diff).
  - With this fix the impact drops from "mint unlimited duplicates for anyone" to "trigger, early, an award the target is already entitled to, once".
- INFO: with the route's own `getReferralsByReferrer` failing (R8, connections refused), both versions see 0 referrals and award nothing. So the route-level "no DB" case cannot show the R9 difference; the author's unit R9 covers it.

## NOT tested
- production's schema and data (whether `svc_referral_milestones_rewards` exists, its constraint on `id`, how many duplicate rows it holds)
- a reward INSERT that commits while the client sees an error (READ only; same mechanism as R5/R10)
- the forced race on the `absent` schema: `LOCK TABLE` cannot lock a missing table. The driver errored by design; the consecutive / qualify / amounts absent cells cover that schema.
- multi-tenancy pools (`getTenantPool`)
- the api-gateway hop
- `NODE_ENV=production` boot
- consumers of `svc_referral_milestones` or the rewards table outside this repo, including any enforcement of tier perks
- /api/rewards/claim on milestone rewards (READ: it reads `svc_referral_rewards` only)
- the four platform suites, eslint, the docs-fragments checker, CI / pre-push hook
- Node 24 (host Node v26.8.1)
- the live PR body via the API (I used the READY mail)
- Spark shadow review

## Processes and cleanup
- **Container and volume:** container `g162-pg` stopped and removed, volume `g162-pgdata` removed. `docker ps -a` / `docker volume ls` show 0 `g162-*`. Nothing else was touched.
- **My processes:** 0 left with this workdir in the command line.
- **Two hung processes during the matrix:** a driver plus 2 service children, from the forced race on the absent schema (a lock client that never closed). I killed them (my own PIDs). The driver now always kills its children and exits.
- **Files:** logs/child_cwd is empty; no `.vite` in Wednesday's tree.
- **Repo state:** `git status` of the clone is clean. The worktrees show only my node_modules / dist symlinks. `wt/mut` is a symlink to `../repo`, used for the real-PG mutants.

## Plain answer for Kam
**The fix works.**

On a real database, with the rewards table keyed on its id, no path I could find pays a user the same milestone twice. I tried:
- repeated checks
- two simultaneous checks from two servers
- a read failing mid-way
- a save failing after the reward was written
- a reward write failing
- users who already hold a reward from before the fix

In each case head stores exactly one reward per user per milestone; today's code stores 2 to 4. A failed read now pays nothing and tells the caller "No new milestones achieved".

**Two things need you.**
1. **One money change.** Because progress now saves, a referrer who reaches 1,000 referrals is finally recorded as an Ambassador. From then on, each further referral pays them **5% more (52.5 instead of 50 SECURA)**. That is the published rule, but it has never actually paid out before. Say yes, or hold it.
2. **Whether the reward table exists in production.** The repo never creates that table.
   - If production lacks it, milestones simply stop being announced there. They were never really stored there anyway.
   - If production has it but without a unique id, nothing is ever stored, before or after this fix.

   Someone needs to look at production's schema. I could not.

The duplicate rewards already paid into the table stay there until someone cleans them up. The missing owner check on the award route is KS-1957, next in line.
