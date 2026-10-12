# QA gate: Secuura Platform K PR #1498 (KS-1477)

- **Head:** `7a6cf7a651d15346fe902544131ff057a4204ffd` (bundle sha256/16 `cac68568115778d2`, verified; ref `feature/ks-1477-verification-store-never-serves-memory-when-a-database-is-configured`; parent `17e275ad` is an ancestor of origin/develop)
- **Base used:** current `origin/develop` = `361537eed238e9886f4cc22d8a91607a96fb1508` (fetched 2026-10-12 ~22:00; the author predicted over `8d34fbf0`). The merge is clean. users.ts auto-merged with develop's KS-806 hunks, which do not touch the verification section. Merge commit in my scratch clone: `3ebb6ce4`.
- **Gate seat:** independent OPUS gate. Not the author.

## VERDICT: GO WITH NOTE

The fix does what it claims. No map read or write is left reachable when a database is configured, I found no Major, and the two Minors are test-suite issues. Neither is a product defect.

## By my runs

1. **Clone and head.** I ran `git clone --no-hardlinks` into the scratchpad, pointed origin at Secuura/Distributed_Secuura with the project's core.sshCommand (only the length was read), ran `fetch origin develop`, then `bundle verify` (rc 0) and `fetch <bundle>` (rc 0). The ref resolves to `7a6cf7a6…ffd` exactly. `diff --stat 17e275ad..head`: 4 files, +270/-8, and users.ts +28/-3 as claimed.
2. **The three touched test files.** I ran `vitest run ks1477 ks1194-a-failed ks1018-item3` with DATABASE_URL unset, on the head and on the merged tree. Both gave 3 files, 31/31 passed.
3. **Full services/auth suite on the head:** 91 files, 943/943 passed. This matches the author.
4. **Full services/auth suite on head merged over 361537ee, run twice:** 93 files and 992/992 passed both times (`merged-suite.txt`). This matches the author's predicted-merge numbers.
5. **`tsc --noEmit -p tsconfig.json` on the merged tree:** rc 0, 0 lines. Positive control: one injected `const x: number = 'x'` gave TS2322 and rc 2, and I restored the file with git checkout (status clean afterwards).
6. **`npm run check:test-types` on the merged tree:** rc 0. Result: "42 errors: 42 in the baseline, 0 new; 0 stale" (`check-test-types.txt`).
7. **eslint on the merged tree.** On the 4 touched files: rc 0 with no output (0 warnings). On `eslint src`: rc 0, with 15 warnings, all outside the touched files. Positive control: a stdin file containing `debugger` reported `no-debugger` as an error.
8. **Base-red check (G0).** Base users.ts (17e275ad) in the head tree, full suite: exactly the 6 RED-labelled ks1477 cells fail, and the 3 CONTROLs pass. This confirms the author's claim.
9. **Mutants, each against the full auth suite (943 tests).** The tree was restored after each one and its sha checked equal at the end. Script: `mut.py.txt`; results: `mutants.txt`.
   - **G1** predicate reverted to `!isDbAvailable()`: KILLED (5)
   - **G2** predicate cached at module load: KILLED (6)
   - **G3** `DATABASE_URL === ""` counts as configured: SURVIVED
   - **G4** whitespace-only DATABASE_URL counts as no database: SURVIVED
   - **G5** list 503 replaced by a 200 empty list: KILLED (1)
   - **G6** pending check 503 replaced by "none pending": **SURVIVED**
   - **G7** get-by-id 503 replaced by null/404: KILLED (1)
   - **G8** the 503 helper returns a plain Error (500): KILLED (5)
   - **G9** review route reads the store before the role check: SURVIVED
   - **G10** old behaviour with 2 holes: KILLED (2)
   - **G11** review trusts a memory-only id (map checked before the DB): KILLED (8, across 4 files)
   - The author's M1-M6 are covered by G1/G7/G10/G11 in kind. Their own table (logs6/mutants_table_v3.txt, read only) shows each of M1-M6 killed by exactly one cell.
10. **Environment sensitivity.** Full suite with `DATABASE_URL=postgresql://dev-shell/secuura` exported:
    - Head: **8 failed / 935** in 3 pre-existing files.
    - Head with it unset: 943/943.
    - Base 17e275ad with it exported: 934/934.

    Evidence: `env-sensitivity.txt`.
11. **Static reads on the merged tree:**
    - Every `memVerificationRequests` and `isDbAvailable` use in `services/auth/src`. The map is only in users.ts and is not exported.
    - Every writer of `verification_upgrade_requests` in the repo: only users.ts in code, plus 3 schema SQL files.
    - db.ts (probe and retry), health.ts (readiness), userRepo.getUserById, errorHandler.
    - Callers across frontends and systemTest.

## Findings

**Major: none.** Map reads and writes are guarded in all four store functions:
- save: lines 1205-1207 and 1227
- get: lines 1260-1264
- pending: lines 1289-1292
- list: lines 1318-1321

Each one now needs `!process.env.DATABASE_URL`. No other file, admin route, import path or startup code reads or writes the map. With a database configured, the only way to fill the map is to file a request while DATABASE_URL is unset and set it later. A production process cannot do that, because both db.ts and the predicate read the variable per call and nothing mutates it.

**Minor 1: test hermeticity regression.** Eight cells in three files the PR does not otherwise change now silently depend on DATABASE_URL being unset in the runner's environment:
- ks467 "verification review re-checks the subject tenant" ×3
- ks1194 "control: with no database at all…" and "nothing is kept in memory…"
- ks1018-item3 LIST / PENDING / REVIEW

Evidence (run 10): with DATABASE_URL exported the head gives 8 failed, the base gives 934/934 passed. CI is unaffected today, because no workflow exports DATABASE_URL to the unit-test step. A developer whose shell has sourced `Blockchain/Dev/.env`, or any future job that runs `npm test` with a database, gets 8 false reds pointing at code that is correct. Fix: in those files, `delete process.env.DATABASE_URL` in beforeAll and restore it in afterAll, as the new ks1477 file already does.

**Minor 2: the surviving mutant G6.** The pending check's own boot-window 503 (users.ts:1289-1290) is not pinned. Replacing it with "none pending" passes all 943 tests, because the save guard (1206) still returns 503 on the ordinary path.

The one path where it is observable is **POST /me/verification with targetLevel STANDARD and MFA enabled.** That path auto-approves before any save. Under G6, in the boot window it would raise the level without consulting the database's PENDING row. The impact is low: MFA is the auto-approve criterion anyway. Still, the duplicate-pending refusal would be skipped. One cell would close it: boot window plus STANDARD plus mfaEnabled should give 503 and leave updateUserOrThrow uncalled.

**Note 1: the operational consequence is bounded and small. This is not a lockout.**
- userRepo.getUserById (userRepo.ts:407-419) queries the database directly and is NOT gated by isDbAvailable. So while the database is genuinely down, all three routes already answer 503 at the user lookup, before the verification store is reached. That was true before this PR too.
- The new 503 is reachable only in the probe-lag gap: the database is back but `dbAvailable` has not flipped yet. db.ts retries with backoff of 1 s doubling to a 30 s cap, so the gap is at most about 30 s after recovery.
- A transient blip after boot never sets `dbAvailable` false, because only probeDb or closeDb do. Mid-life blips therefore take the existing KS-1018 infrastructure-error path (503/500), unchanged.
- There is no Retry-After header (errorHandler has none).
- `/health/ready` reports `degraded` with HTTP 200 during the boot window, so ACA routes traffic to the instance.
- No frontend or other service calls these routes. The repo-wide grep found only `systemTest/schemathesis/tests/test_user_admin_isolation.py`, which asserts that a non-admin gets 403 on review.

**Note 2: authorisation.** The review route's role check (users.ts:1407) still runs before `getVerificationRequest` (1411). A non-admin gets 403 in the boot window, never 503. The 503 body is the house body ("Authentication service temporarily unavailable, please retry", code SERVICE_UNAVAILABLE) and leaks nothing. However, no unit cell pins the ordering (G9 survived). The schemathesis 403 check pins it only outside the boot window.

**Note 3: what counts as "configured".** `!process.env.DATABASE_URL` matches db.ts exactly (`getPool` line 21, `initDb` line 230), so an empty string means memory-only in both places, consistently. A whitespace-only or malformed URL counts as configured, which means 503 for as long as the probe fails. That is the right fail-closed direction, but it is not pinned (G3 and G4 survived).

**Note 4: test model gap (pre-existing suites).** ks1193, ks1194, ks1236 and ks1018-item3 model "a configured database" as `isDbAvailable() === true` with DATABASE_URL unset, a state production cannot reach. On the head, those suites therefore run the memory-only arms of lines 1227 and 1260, not the configured arms. Only the new ks1477 file exercises the configured arms. G11 shows the old suites still bite on some faults.

**Note 5: pre-existing, outside this PR.**
- The verification routes are absent from `auth.openapi.ts`, so the new 503 is undocumented.
- Memory-only mode is probably unusable end to end anyway: with no DATABASE_URL, `userRepo.getUserById` goes through `getPool()`, which throws. In production `enforceProductionConfig` requires DATABASE_URL (index.ts:57).

## NOT tested

- No real Postgres. I used the author's in-memory table behind the db mock, and the boot window was the test toggling isDbAvailable. Docker was down.
- No live boot window and no probe-lag timing. The ≤30 s bound comes from reading db.ts, not from a run.
- No multi-replica run.
- The schemathesis or shell leg, on the head or the merged tree.
- tsc, check:test-types and eslint ran on the merged tree only, not on the bare head.
- Frontend behaviour on 503: there is no in-repo consumer to test.
- I did not re-run the author's exact M1-M6 patches. I ran my own G0-G11 and read their table.
