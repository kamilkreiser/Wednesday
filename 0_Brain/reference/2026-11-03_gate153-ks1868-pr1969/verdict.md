# QA Gate 153 verdict: Secuura/Distributed_Secuura PR 1969 (KS-1868, referral db.ts / milestoneService.ts / referralService.ts / fraudDetection.ts catches), TIER 1, round 1

## BLUF
**GO WITH NOTES. Nothing in this PR's diff has to be fixed before merge.** The class bar is met at all 12 changed sites: in every process cell, head with an unreadable value equals base with an ordinary Error (same HTTP answer, same persisted rows, same boot state).

**But the reward path this PR opens to hostile values is worse than the author measured, and it is broken for a HEALTHY database too (G153-F1, pre-existing, HIGH).** `dbSaveMilestoneProgress` does `JSON.stringify(progress.milestonesAchieved)`, and every newly achieved entry carries a BigInt `rewardAmount`. So the save throws "Do not know how to serialize a BigInt" on EVERY award, inside its own catch, and the progress row never records an achievement. With no DB failure at all, a user with one qualified referral was awarded FIRST_REFERRAL on check 1 and again on check 2: 2 CLAIMABLE rows, 200 SECURA pending (base = head). Kam's owed card should be decided on F1 + F2, not on this PR's catches.

How I measured: I booted the REAL referral service as its own Node process for every cell: node + tsx, the real `index.ts`, `db.ts` (initDb, runDbReadyHook), the real milestone / referral / fraud services, the real winston logger, the real shared `authenticate()` with an RS256 token, and the real Express routes. Only `pg` was replaced, by a preload (scripts/pgstub.cjs) that models the six referral tables in memory, autocommit per statement. That gave 89 cells over base 26955bf1 and head 15c17034, run from two worktrees (wt/base, wt/head) of my clone.

Host Node v26.8.1 throughout. Nothing was measured on Node 24.

## Heads
- START (logs/head_start.log, 21:48:35Z): PR head `15c17034b256d52ac54194912ec560a2d75f1cad` (= the pin). **develop `ddd770cab4aa`**: it had already moved past the commission's b85b7b67 when I started (ddd770ca = KS-1868 demo-service). Merge-base `26955bf1b828`. 1 commit.
- MID (logs/heads_mid.log, 21:56:29Z) and END (logs/head_end.log, 21:57:22Z): both heads unchanged.
- Clone HEAD is 15c17034 and `git status` is clean. Every product swap was sha-restored: suites_restore, static_restore, and mutants restore=True x72. The process probes swapped nothing; they ran on the worktrees.
- **PR body not read through the API** (no gh login on this seat). I used the READY mail (evidence/w21_pr1969_ready.txt) and the PR's two fragments.
- `npm ci --ignore-scripts` rc 0 on this lockfile (logs/npm_ci.log), so the `--no-package-lock` fallback was NOT needed. packages/shared build rc 0.

## 1. Diffstat (logs/diffstat.log, three-dot)
11 files, **+760/-12**, as declared:

| file | + | - |
|---|---|---|
| db.ts | 16 | 2 |
| fraudDetection.ts | 8 | 1 |
| milestoneService.ts | 42 | 5 |
| referralService.ts | 32 | 4 |
| test files (5 new) | 95 + 133 + 111 + 149 + 146 | 0 |
| flow fragment | 11 | 0 |
| cheat fragment | 17 | 0 |

Nothing outside the declared paths.

## 2. The hunks (logs/product_diff.log)
**12 identical guards.** The READY mail says "fourteen catches"; the diff has 12 (G153-F9). Each guard replaces `err?.message` (`err.message` in the pool listener) inside the log meta with this:
```
let reason; try { const m = err?.message; reason = m === undefined || m === null ? m : String(m); } catch { reason = 'unreadable thrown value'; }
```

The 12 sites:
- **db.ts (2):** the pool 'error' listener, and runDbReadyHook's catch.
- **milestoneService.ts (5):** progress read (`return null`), pending-rewards read (`return []`), progress save, pending-reward save, and the table verify.
- **referralService.ts (4):** code by id (`null`), codes by owner (`[]`), referrals by referrer (`[]`), rewards by user (`[]`).
- **fraudDetection.ts (1):** loadFromDb ("starting empty").

What does NOT change:
- every message, level and field name
- every fallback return value
- every SQL statement
- no rethrow is added
- the nine other unguarded catches in referralService.ts (:68 :85 :99 :206 :257 :270 :286 :302 :327 at base) and db.ts probeDb :122

## 3. Behaviour (RUN: real process, only `pg` replaced; READ where marked)
Probe artefacts: logs/probe/*.result.json, *.stdout.log and *.snap.json (the store after each step); the condensed view is logs/probe_table.log.

The kinds I ran:
- `ordinary`: `new Error('db down')`
- `string`: a thrown string
- `revokedProxy`
- `throwingGetter`: an Error whose message getter throws

### Q1: REWARD (RUN)
**Setup:**
- REF has a stored progress row with all 6 milestones achieved on 2026-11-01, and 6 prior milestone-reward rows, all CLAIMED.
- REF has 999 qualified referrals. I seeded 1000, but one id collided in my stub, so AMBASSADOR (1000) is not reached and a full award is **5** milestones, not 6.

**Steps:** POST /api/milestones/check/REF twice as REF, then once as a DIFFERENT user. GET /api/rewards/user/REF.

| ver / kind | scenario | check 1 / 2 | milestone-reward rows for REF after 2 checks | progress row |
|---|---|---|---|---|
| base and head / none (healthy DB) | award_none | 200, 0 new / 0 new | 6 (all prior, CLAIMED) | unchanged |
| base ordinary, string; **head ordinary, string, revokedProxy, throwingGetter** | progress read fails | **200, 5 new / 5 new** | **16 = 6 CLAIMED + 10 new CLAIMABLE; pending 126,200 SECURA** | unchanged (the save throws on BigInt, see F1) |
| **base revokedProxy, throwingGetter** | progress read fails | **500 INTERNAL_ERROR / 500** | 6, nothing awarded | unchanged |
| same kinds | progress read AND both writes fail (award_read_wfail) | as above: 200 with 5 new for ordinary at base and for every kind at head; 500 for hostile at base | **6: nothing persisted** | unchanged |
| table `svc_referral_milestones_rewards` absent (mr=absent) | progress read fails | 200 with 5 new (ordinary at base; ordinary and revokedProxy at head); 500 (base revokedProxy) | 0: every insert fails 42P01 | unchanged |
| base = head / none, fresh user REF2 with 1 referral (award_fresh) | **healthy DB** | **200, FIRST_REFERRAL / FIRST_REFERRAL again** | **2 CLAIMABLE, 200 SECURA** (log: `DB save milestone failed {"error":"Do not know how to serialize a BigInt"}`) | never written |

**Answers:**
- **Duplicate or first award? DUPLICATE.** Milestones already awarded and already CLAIMED are awarded again as new CLAIMABLE rewards on every check. Each one gets a fresh uuid, so `ON CONFLICT (id) DO NOTHING` never dedupes.
- **Is the route owner-bound? No (pre-existing).** The third check, made by a different authenticated user against REF's id, awarded 5 more (`checkByOtherUser`).
- **What is persisted?**
  - Only the reward rows in svc_referral_milestones_rewards, and only if that table exists.
  - The progress row is NOT overwritten: the author's READ claim ("overwrite the stored progress row") is wrong, because the save throws first (F1).
  - If the writes also fail, nothing is persisted. Nothing is held in memory either: the service is DB-only and has no cache.
  - The API still answers 200 with the milestones listed, and logs "Milestone achieved" once per milestone.
- **Events and money: none in this service (READ).**
  - There is no emitter, webhook or outbound call in services/referral/src.
  - POST /api/rewards/claim reads only `svc_referral_rewards` (dbGetReward), so milestone rewards cannot be claimed through it.
  - Claim only marks a reward CLAIMED; the "initiate blockchain transfer" step is a comment.
  - GET /api/rewards/user shows the duplicates as pending with `canClaim: true`, which inflates the balance a user sees.
  - **`svc_referral_milestones_rewards` has no DDL anywhere in the repo.** A case-insensitive git grep finds it only in milestoneService.ts. The positive control: `svc_referral_milestones` is in 3 SQL files. Whether production has the table: NOT TESTED.
- **Classification:**
  - Pre-existing for an ordinary Error: **HIGH**. A failed read re-grants every qualifying milestone as a duplicate CLAIMABLE reward (F2).
  - Pre-existing for a healthy DB: also **HIGH**. Every check re-awards (F1).
  - What THIS PR newly makes reachable: for a revoked Proxy or throwing-getter value from the progress read, base answered 500 and awarded nothing; head grants the same duplicates an ordinary Error already grants. Equal to base-ordinary in every column.

### Q2: FRAUD (RUN)
**Setup:**
- svc_referral_fraud_log holds a KNOWN_FRAUD row for user BAD, plus 3 rows on IP 10.9.9.9.
- After boot, POST /api/referrals/apply applies REF's code for BAD with ipAddress 10.9.9.9.

| failure at boot | base ordinary / string | base revokedProxy / throwingGetter | head (all kinds) |
|---|---|---|---|
| none | fraud loaded (1 flagged user); BAD -> 201 INVALID, passed=false, no bonus | | same |
| **fraud load fails** | "starting empty"; BAD -> **201 PENDING, passed=true, 25 SECURA CLAIMABLE signup bonus** | "DB ready boot work failed"; **the store is also EMPTY** (the query threw before any row); BAD -> **PENDING + bonus** | "starting empty"; BAD -> PENDING + bonus |
| milestone verify fails | fraud loaded; BAD blocked | **fraud load SKIPPED**; BAD -> PENDING + bonus | **fraud loaded; BAD blocked (head strictly better)** |
| referral verify fails (:327, NOT in this PR) | fraud loaded; BAD blocked | fraud load skipped; BAD passes | **unchanged: hostile kinds still skip the load; BAD passes (base = head)** |

**Answers:**
- **Does an empty store let something through? Yes.** It lets a KNOWN_FRAUD user pass and collect the signup bonus until the next successful load. Nothing re-runs the hook while the DB stays up: the KS-382 rerun fires only after a failed probe recovers (READ).
- **Same as an ordinary Error at base? Yes.** Base did NOT keep the fraud data on a hostile value: runDbReadyHook swallowed the rejection, and the store was already empty. **No new outcome at the fraud-load site.**
- At the milestone-verify site, head newly LOADS fraud data that base skipped for hostile values.
- **Pre-existing (READ, consistent with the cells):**
  - applyCode never sets `referrerIp` or `referrerDeviceId`, so the IP and device SYBIL checks never run. Only KNOWN_FRAUD uses the loaded store; BAD's 4 rows on 10.9.9.9 raised no SYBIL flag.
  - `ipAddress` is client-supplied in the body.

### Q3: generateCode (RUN; the custom code is a valid `MKQWHZDT`, logs/probe/*-cc__*)
**Setup:** GEN already owns 5 active codes, which is the limit.

| owner read fails (gen_owner) | base ordinary | base hostile | head ordinary | head hostile |
|---|---|---|---|---|
| POST /generate {} and {customCode} | 201, 201: **7 codes (limit 5 bypassed)** | 400 `Cannot perform 'get'...` / `getter boom`; 5 codes | 201, 201: 7 codes | **201, 201: 7 codes (= base ordinary)** |

| every svc_referral_codes query fails (gen_all) | base and head ordinary | base hostile | head hostile |
|---|---|---|---|
| | 201, 201, but **5 codes: the "generated" codes were never stored** (pre-existing) | 400 + raw inner message | **still 400 + raw inner message** |

**Confirmed both:**
- (a) The active-code limit is not enforced on a failed `dbGetCodesByOwner`. Pre-existing for ordinary; newly reachable for hostile kinds, equal to ordinary.
- (b) At head, hostile kinds still REJECT. Without a custom code the rejection comes through `dbSaveReferralCode`'s catch (:68). With a valid custom code it comes through `dbGetCodeByString`'s catch (:257), the first unguarded read on that path.
  - The route maps any `Error` to 400 and **echoes the inner error's message to the client**. Pre-existing, base = head.

### Q4: the class bar, with the real logger (RUN)
All 12 sites meet it.

- **Process cells:** I compared head with an unreadable value against base with an ordinary Error at these sites: progress read, pending-rewards read (GET rewards: base hostile 500 -> head 200 with 0 pending, = ordinary), both writes (award_read_wfail), milestone verify, fraud load, codes-by-owner. Every pair was equal.
- **The other 4 referral reads, the pool listener and the hook catch:** covered by the PR's unit cells and the mutants.
- **The real logger threw in none of the cells.**
- Head log text for a hostile value: `{"error":"unreadable thrown value"}`.

## 4. Re-measure (vitest `--root` = the clone's services/referral, cwd = workdir/logs/child_cwd)
- **Red first** (base product for all 4 files + the 5 new files; logs/red_base_new.log): **26 failed | 15 passed (41)**. Every failure is an AssertionError; 0 crashes. As claimed.
- **Head, the 5 new files:** run 1 failed **1/41**: the db file's `control C1` timed out at 5000 ms (logs/head_new.log). Re-runs:
  - all 5 new files, run 2: 41/41
  - all 5 new files, run 3: 41/41
  - db file alone, run 1: 9/9
  - db file alone, run 2: 9/9

  Host load average was about 12. The author hit the same timeout twice (fragment §.1). It is a reproducible cold-import timeout on the first cell (G153-F8).
- **Whole referral suite:**
  - base without the new files: **7 files / 36, rc 0**
  - head: **12 / 77, rc 0**, in two runs
- **tsc including tests** (scripts/tsconfig.tests.json: the service config + src/** + node types; logs/tsc_summary.log):
  - head **0** (31 files, 15 under __tests__)
  - base **0** (26 / 10)
  - planted: **1 TS2322**
  - service `tsc --noEmit`: 0 at head, 0 at base
- **eslint** (Dev flat config, cwd Dev): the 4 products + 5 tests, **0 problems**. The base products: rc 0. A planted file: 1 error + 1 warning, rc 1.
- **docs-fragments `check`:** rc 0 ("flow 117+115 new, cheat 112+115 new; lint clean, render passes"). Planted defects, each rc 1 naming this fragment:
  - flow: unclosed div
  - flow: `<!--n-->.` removed
  - cheat: unclosed div
  - cheat: `</table>` corrupted

  Each was sha-restored; rc 0 after.

## 5. Mutants (scripts/mutants.py; product only, PR tests untouched, sha256-restored after each; logs/mutants_table.log)
72 mutants (6 per site x 12 sites): **63 killed, 9 survived.** Every kill is by assertion; there were 0 transform errors.

| mutant | db.ts x2 | fraud x1 | milestone x5 | referral x4 |
|---|---|---|---|---|
| M0 revert to base | K | K | K | K |
| M1 inner catch rethrows | K | K | K | K |
| M2 constant always | K | K | K (controls) | K (controls) |
| M3 String() dropped | K | K | **SURVIVED x5** | **SURVIVED x4** |
| M4 log removed | K | K | K | K |
| M5 rethrow after log | K | K | K | K |

M3 survives at milestone and referral because those two files have no cell with a non-string message, such as a Symbol or BigInt (G153-F7). The effect is log content only; outcomes are unaffected.

## 6. merge-tree (scripts/mergetree.sh, logs/merge_tree_ddd770ca.log)
**Onto `ddd770ca`** (develop at START and END):
- rc 0, tree `29e37873`
- the merged-vs-develop paths == the 11 PR paths
- the four product blobs merged == head

**Squashes since base:**
- 7ad0dcc1 (kyc / wallet-connector)
- b85b7b67 (prism / timestamping / security)
- ddd770ca (demo-service)

PR-path overlap is **0** (positive control 18). No develop path is under services/referral or packages/shared. **The merged tree's services/referral and packages/shared subtrees, and package-lock.json, are byte-identical to head's**, so every head process cell stands for the merged tree.

## 7. Kam's ks1346 rule (log type and field NAMES, never values)
- **No new log line.** All 12 lines keep their message, level and field names.
- The constant `unreadable thrown value` is a type statement: compliant.
- A readable message is logged as text, as before (pre-existing class practice): pg/DatabaseError text.
- The id fields that sit beside it (`userId`, `ownerId`, `referrerId`, `id`, `rewardId`) are pre-existing identifier values, unchanged by this PR.
- No secret carrier is known in any of these lines: compliant.
- **Pre-existing, outside the log lines:** `/generate` and `/apply` answer `400 {message: error.message}`. For a hostile value at the unguarded :68 / :257, that is the inner TypeError text, sent to the client (Q3).

## 8. Notes for the PR body
- **G153-F1 (recommended follow-up ticket, HIGH, pre-existing, measured with a HEALTHY DB, base = head):** `dbSaveMilestoneProgress` always throws `Do not know how to serialize a BigInt` whenever a milestone is newly achieved, because `AchievedMilestone.rewardAmount` is a BigInt passed to `JSON.stringify(progress.milestonesAchieved)`. Its catch swallows the error, so the progress row never records an achievement, and every `checkAndAwardMilestones` call re-awards every qualifying milestone as a new CLAIMABLE reward. That is every `/qualify` and every `POST /api/milestones/check/:userId`. In the cell, REF2 got FIRST_REFERRAL twice: 2 rows, 200 SECURA.
  - **Fix:** serialise with a replacer, e.g. `JSON.stringify(list, (_k, v) => typeof v === 'bigint' ? v.toString() : v)`. rowToProgress already reads `rewardAmount` back from JSON.
  - No BigInt `toJSON` polyfill exists in referral or packages/shared (git grep).
- **G153-F2 (recommended follow-up ticket, HIGH, pre-existing for an ordinary Error, measured):** a failed progress read becomes "no row", then the fresh default, then DUPLICATE awards of milestones already awarded and CLAIMED: 5 new CLAIMABLE per check, 126,200 SECURA pending after two checks.
  - **Fix:** dbGetUserProgress must distinguish "read failed" from "no row". On failure, checkAndAwardMilestones should award nothing (or rethrow).
  - This PR makes the hostile-value path match this outcome; at base it answered 500 and awarded nothing.
- **G153-F3 (recommended, pre-existing, measured):** `POST /api/milestones/check/:userId` has no owner or role check. Any authenticated user can trigger awards for any user id. `/api/referrals/qualify` has no role check either (READ). Combined with F1 and F2, any caller can mint duplicate CLAIMABLE milestone rewards for anyone.
- **G153-F4 (info, measured + READ):**
  - `svc_referral_milestones_rewards` has no DDL in the repo. On a schema built from repo DDL, every milestone-reward insert and read fails 42P01, so the duplicates are never persisted (mr=absent cells), and GET rewards silently shows 0 milestone rewards.
  - Milestone rewards are not claimable via `/api/rewards/claim`, which reads `svc_referral_rewards` only.
  - No events, no outbound calls, no token transfer in this service.
  - Whether the production DB has the table: unknown.
- **G153-F5 (info, measured):** fraud load: no new outcome.
  - At base a hostile value already left the fraud store empty: runDbReadyHook swallowed it, and the query had failed before any row.
  - An empty store lets a KNOWN_FRAUD user pass apply and get the 25 SECURA CLAIMABLE signup bonus (ordinary, base and head).
  - Head is strictly better when the milestone verify fails: the fraud load now runs.
  - **Remaining gap:** a hostile value in referralService.verifyDbReady (:327, not in this PR) still skips the milestone verify and the fraud load at head. It belongs in the next pass.
  - Pre-existing (READ): the IP and device SYBIL checks are dead code, because applyCode never sets `referrerIp` or `referrerDeviceId`.
- **G153-F6 (info, measured):** generateCode.
  - (a) A failed owner read bypasses the 5-active-code limit (7 codes). Pre-existing for ordinary; newly reachable for hostile kinds, equal to ordinary.
  - (b) Hostile kinds still answer 400 at head through the unguarded :68 / :257 catches, with the raw inner message in the body.
  - (c) An ordinary failed save answers 201 with a code that was never stored (pre-existing).
- **G153-F7 (recommended, test gap):** M3 (String() dropped) survives at all 9 milestone/referral sites. Add one non-string-message cell (a Symbol message, as in the db file's R2/R5) to the milestone and referral files.
- **G153-F8 (recommended, test flake):** the db file's `control C1` times out at the 5000 ms default on a cold first `import('../db')` under host load: this gate saw it 1 of 6 runs, the author 2 runs.
  - **Fix:** warm the import in a `beforeAll`, or give that describe `{ timeout: 20_000 }`. Otherwise CI under load will flake.
- **G153-F9 (info, corrections to the PR text):**
  - The READY mail's "fourteen catches" is **12**.
  - The flow fragment's "three database read catches and the table-verify catch" for milestoneService is two reads + the verify (3 sites), plus two writes.
  - The fragment's "awards every milestone the user qualifies for as new CLAIMABLE rewards" should say these are **duplicates of already-awarded milestones**, and that F1 makes the same happen with a healthy DB.
  - The mail's READ claim that a working write path would "overwrite the stored progress row" is wrong: it never writes (F1).
- **G153-F10 (info):** develop was ddd770ca at START and END, not the commission's b85b7b67. merge-tree is clean, with 0 overlap.

None of these is FIX-BEFORE-MERGE for this diff.

## 9. NOT TESTED
- the live PR body via the API (no gh login)
- a real PostgreSQL or pg: the store is a model, and SQL semantics are emulated
- whether production has `svc_referral_milestones_rewards`
- `NODE_ENV=production` boot
- the KS-382 recovery re-run of the hook (READ only)
- multi-tenancy pools
- the api-gateway hop to /api/milestones/check and /api/referrals/qualify
- the `/qualify` route driving checkAndAwardMilestones (READ: the same function as the cells)
- `/api/rewards/claim` on milestone rewards (READ only)
- the pool 'error' listener and runDbReadyHook's own guard in a process (unit cells + mutants only)
- consumers of these tables outside this repo
- the four platform suites
- CI and the pre-push hook
- Node 24
- Spark shadow review

## Processes
Every background run I started has finished:
- npm ci + shared build
- suites
- static
- the probe matrix: 89 child service processes, each SIGTERMed
- mutants: 72 runs
- the reruns

`ps` shows no process with this workdir in its command line.

**Log files:** the referral logger is console-only (no file transport), and db.ts logs via `console.log`. **No log file was written:**
- logs/child_cwd is empty.
- Wednesday's logs/combined.log mtime is 06:01 local, before this gate started at 08:47.
- No `.vite` appeared in Wednesday's tree.

The worktrees wt/base and wt/head remain inside the workdir. Their node_modules are symlinks to the clone's.
