# QA gate: Secuura Platform K PR #1490 (KS-1311)

Head: `90b45bb5c8ad44f1b000b820210d47cc2e1c6f51` (bundle sha256/16 `56732fb8812ba5ec`, verified; fetched head equals `90b45bb5c8ad`).
Base used: real `origin/develop` = `dd015e7358185feb2192719aa718161015846622` (fetched fresh from GitHub, confirmed against `ls-remote`). PR merge-base is `a28ed5d81`, 8 commits behind develop; I cherry-picked the PR commit onto `dd015e735` (clean) and ran there.

## VERDICT: GO WITH NOTE

The change is test-only and every claim the author made reproduced exactly (green under the app role in both tenancy modes, 4 red with no app role, 4 red with a superuser, both rollback cells red on the pre-KS-1263 route); two Minor gaps (RLS asserted on `documents` only; the SETUP guard is a cell, so a `-t`/`.only` filter bypasses it) do not block merge.

## By my runs

Environment: Homebrew postgresql@15 on port 55412 under my scratchpad (no Docker), built per the recipe: 11 init SQL + 49 migrations applied, 0 failed, plus `003_platform_tenancy.sql` in the same DB (for MT=true), `secuura_app` (NOSUPERUSER, NOBYPASSRLS), FORCE RLS confirmed on `documents`, `shares`, `custody_events`. Product deps copied from the shared checkout's node_modules (read only), `packages/shared` built with tsc, `prisma generate` in the scratch clone. All runs: `run.sh <out> <app|none|super> <MT> [pattern]`, which is `npx jest --config jest.integration.config.js ks1263-multi-write-rolls-back` with `TEST_DATABASE_URL` = superuser, `TEST_PLATFORM_DATABASE_URL` = same DB, and `TEST_APP_DATABASE_URL` as stated. Per-run cell lists are in `*.summary.txt` beside this file.

1. Scope proof: `git diff --name-status origin/develop...pr1490` lists exactly 1 file, `Blockchain/Dev/services/originate/src/__tests__/ks1263-multi-write-rolls-back.integration.test.ts`, +97/-1. No non-test file is touched. (The two-dot diff against develop shows 19 files only because the branch is 8 commits behind; none of that is the PR's.) Claim "no product file changed": PROVED.
2. App role, MT=false: 11 passed, exit 0 (`r_app_mt0.summary.txt`).
3. App role, MT=true: 11 passed, exit 0 (`r_app_mt1.summary.txt`). The MT=true guards (manager exists, seeded tenant visible to `getTenantStatus()`) held.
4. No app role (`TEST_APP_DATABASE_URL` unset), MT=false and MT=true: 4 failed, 7 passed, exit 1 both. The 4 reds are the three SETUP cells plus the RLS cell. The message names the variable: "KS-1311: TEST_APP_DATABASE_URL is not set...". Claim confirmed.
5. Superuser standing in (`TEST_APP_DATABASE_URL` = the superuser DSN), MT=false and MT=true: 4 failed, 7 passed, exit 1 both. SETUP message reads `the product's connection is "postgres" (superuser=true, bypassrls=true)`. The RLS cell reds on its own (it saw the other tenant's row), not only through the setup cell. Claim confirmed.
6. Pre-KS-1263 route under the app role: reverted the product lines of `6e2a00bfe` (KS-1263, #1239) in my scratch clone only: `git apply -R --3way` of its `shareRepo.ts` and `routes/documents.ts` hunks (patch saved as `ks1263_product_revert.patch`; I resolved one conflict where KS-1402 had moved the `db` read, and dropped the now-unused `withTenant` import so TS compiles; `tsc --noEmit` clean). Result, MT=false and MT=true: 2 failed, 9 passed. The two reds are `ROUTE-ROLLBACK` and `ROUTE-CUSTODY-ROLLBACK`, and for the right reason (`Expected: 0 Received: 1` at the share-count and custody-count assertions). SETUP and CONTROL cells stay green, so the reds are not setup noise. Claim confirmed. (A first attempt without the unused-import fix reds all 6 route cells with an empty message because the harness fails to compile; that was my revert's fault, not the PR's.)
7. Mutant M3, `ALTER ROLE secuura_app BYPASSRLS`: 4 red (3 SETUP + RLS cell). Caught.
8. Mutant M4, `ALTER TABLE documents DISABLE ROW LEVEL SECURITY`: 1 red (the RLS cell). Caught.
9. Mutant M5, `DISABLE ROW LEVEL SECURITY` on `shares` and `custody_events`: 11 passed, exit 0. NOT caught (see F1).
10. Mutant M7, `withTenant` MT path commits instead of rolling back on error (`db.ts` line 340, `ROLLBACK` to `COMMIT`), MT=true: 2 red (`D1/D2`, `C7`, the JS-throw-after-successful-INSERT cells). Caught. The two route rollback cells stayed green, which is expected and not a hole: their trigger is a Postgres error, which aborts the transaction, so COMMIT on it behaves as ROLLBACK (an equivalent mutant for those cells).
11. Filter bypass M6: superuser as the "app role", MT=false, `-t ROLLBACK`: 2 passed, 9 skipped, exit 0. The SETUP cells are skipped by the filter and the rollback cells pass as the superuser (see F2).
12. Teardown: my postgres stopped with `pg_ctl stop` (exit 0), `pg_ctl status` then reports "no server running". Nothing of the shared checkout or any remote was written; GitHub access was a read-only `git fetch origin develop`.

## Findings

- **F1 Minor.** The RLS-in-the-loop control asserts only `documents`. The file header and PR text say FORCE RLS is on `documents`, `shares` and `custody_events`, and the rollback cells write `shares` and `custody_events`, but disabling RLS on those two tables leaves all 11 cells green (run 9). Cheap closing step: assert `relforcerowsecurity` for all three tables, or add an other-tenant INSERT/UPDATE refused on each of `shares` and `custody_events`.
- **F2 Minor.** Author question (1), setup fails but later cells run: sufficient for a whole-file run (exit 1 in every wrong-role case, runs 4 and 5), and I prefer it to aborting because all the red names appear at once. But the guard is an ordinary cell, not a `beforeAll`, so any run that excludes it (`-t`, `it.only`, a single-cell watch run) executes the rollback cells as a superuser and exits 0 (run 11). Mitigation options: also assert the role inside the existing `beforeAll`, or leave as is and document that the file must be run whole. Not a CI risk today (see N1).
- **F3 Note.** Author question (2), probe inside a `withTenant` transaction: correct. It reads `current_user` and `pg_roles.rolsuper/rolbypassrls` on the same connection the transactional writes use, and it returned the superuser in MT=true when I supplied a superuser DSN (so the probe does track the default pool, not just the Prisma client). Limit: it names the role of `withTenant`'s connection only. The route harness never sets `req.tenantPool`, so request-client reads go through the default client, which shares the same DSN here; a future route that opens a different pool would not be probed.
- **F4 Note.** Author question (3), the RLS control: it is positive-controlled (own row visible, other tenant's row invisible, other tenant's UPDATE returns `[]`, superuser re-read confirms the title unchanged) and cleans up in `finally`. It reds for a BYPASSRLS role and for RLS disabled on `documents` (runs 7, 8). Scope limit is F1.
- **F5 Note.** Inconsistent with precedent: KS-597's suite also accepts `APP_DB_USER`/`APP_DB_PASSWORD` to compose the app DSN; this one needs `TEST_APP_DATABASE_URL` outright. Harmless, but someone with the KS-597 env set will hit the refusal and need to read the message.
- **N1 Note.** No silent skip: with the variable missing the suite fails by name (run 4), and the default `jest.config.js` ignores `*.integration.test.ts`. But nothing in `.github` runs the originate integration config at all (grep of `origin/develop` for `jest.integration`, `test:integration`, `TEST_DATABASE_URL` finds only an unrelated baseline file), so this gate and its predecessors are a manual instrument; the PR does not change that and does not claim to.

No Major findings.

## NOT tested

- CI: the PR's GitHub checks were not read or run (no integration job exists for this suite anyway, N1). Typecheck baseline for tests (`scripts/typecheck-tests`) not run; ts-jest compiled the file and `tsc --noEmit` is clean on the product only.
- The other originate integration suites (KS-597, KS-1124, KS-1278, KS-1310 cells outside this file), other tenancy modes beyond MT=false/true, and any non-originate service.
- Real pgbouncer transaction pooling, a Postgres other than 15, and the demo/Kintsugi/production databases (no access, by instruction).
- The author's own scratch logs under `5_Project_History/2026-10-12_seatJ-2nd/ks1311/` were not consulted; every number above is from my runs.
- My pre-KS-1263 route is a 3-way reverse-apply onto current develop with a manual conflict resolution, not the literal historical tree; the product lines reverted are the `shareRepo.ts` and `routes/documents.ts` hunks of `6e2a00bfe`.
