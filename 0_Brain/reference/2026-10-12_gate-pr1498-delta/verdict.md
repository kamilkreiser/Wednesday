# QA delta gate: Secuura Platform K PR #1498 (KS-1477) at dec362bc

- **Head:** `dec362bcdaafcad524c3857fcca0a0094e224878` (fetched from bundle `ks1477-dec362bcdaaf.bundle`, ref `feature/ks-1477-verification-store-never-serves-memory-when-a-database-is-configured`)
- **Parent:** `7a6cf7a651d15346fe902544131ff057a4204ffd` (the Opus-gated head), confirmed by `rev-parse dec362bc^`
- **Gate seat:** independent Sonnet-tier delta gate. Not the author. Clone in the session scratchpad; the project repo was only read.

## VERDICT: GO

The delta is tests only, both Opus Minors are closed as claimed, and every claim I could reproduce held (946/946 with DATABASE_URL set and unset, both new pins catch their mutants); I found no Major and no Minor.

## By my runs

1. **Clone, head, parent.** `git clone --no-hardlinks`, origin repointed to Secuura/Distributed_Secuura with the project's `core.sshCommand` (only "is set" was checked), `fetch origin develop` rc 0, bundle fetch rc 0. `rev-parse dec362bc` equals the claimed sha, `dec362bc^` equals `7a6cf7a6`, and `log 7a6cf7a6..dec362bc` shows exactly ONE commit.
2. **Tests only.** `git diff --name-status 7a6cf7a6 dec362bc` lists 4 files, all `M`, all under `Blockchain/Dev/services/auth/src/__tests__/` (ks467, ks1194, ks1018-item3, ks1477). `--stat`: 62 insertions, 2 deletions. `rev-parse 7a6cf7a6:…/routes/users.ts` and `dec362bc:…/routes/users.ts` are both `2f7dde23a3ba4be122f8c54adb1c789b84d3c4e0`, so users.ts is byte-identical (`delta-name-status.txt`).
3. **Full services/auth suite on the head, DATABASE_URL unset** (`env -u`): rc 0, 91 files, **946/946** (`full-unset-tail.txt`).
4. **Full suite, DATABASE_URL=postgresql://x:y@127.0.0.1:1/z exported:** rc 0, 91 files, **946/946** (`full-set-tail.txt`).
5. **The three touched files plus ks1477 alone**, set and unset: 4 files, 72/72 in both modes.
6. **Positive control for the hermeticity fix.** I checked out the PARENT's test files (7a6cf7a6) into my clone, left the head's users.ts, and ran the same four files with DATABASE_URL set: 3 files failed, **8 tests failed / 61 passed** (`parent-tests-env-set-tail.txt`). That reproduces the Opus Minor 1 exactly (8 cells), so the green in run 4 and 5 is the fix and not an environment that never leaked. My clone was restored to dec362bc and was clean afterwards.
7. **Restore semantics.** Code read: each of the three files captures `SAVED_DATABASE_URL` at module load (before `beforeAll`), `delete`s in `beforeAll`, and in `afterAll` either deletes (was unset) or reassigns (was set), before `server.close`. Empirical probe (two throwaway files, since moved out of the clone): file A deleted the variable in `beforeAll` and then THREW; file B ran after it in the same process (`--pool=forks --no-file-parallelism --no-isolate`) and asserted the original value. B passed with the variable set AND with it unset, so `afterAll` ran after the `beforeAll` failure and nothing leaked into the next file. (A test body that throws cannot skip `afterAll` in vitest; I did not probe that case separately.)
8. **tsc.** `tsc --noEmit -p services/auth/tsconfig.json`: rc 0, 0 lines. **Caveat:** my injected type error in a test file was NOT reported by this command, because the tsconfig does not cover `__tests__`. So this run proves only that the production tree compiles; the test files are covered by run 9.
9. **check:test-types** (run through `node` with the package's own script, cwd = Dev): rc 0, "42 errors: 42 in the baseline, 0 new; 0 stale baseline entries" (`check-test-types.txt`). Positive control: appending `const __x: number = 'x'` to ks467 made it report NEW TS2322 and TS6133 and exit 1. File restored.
10. **eslint** on the 4 touched files from the services/auth cwd: rc 0, empty output. Positive control: appending `debugger;` gave `no-debugger` error, 1 problem. (A first attempt from the wrong cwd reported "File ignored because outside of base path" and I discarded it as invalid; the numbers above are from the corrected run.)
11. **BASE check.** I put the BASE users.ts (17e275ad) into my clone and ran ks1477 against it: **7 failed / 5 passed** (12). The seven failures are the seven `RED` cells, including the new "boot window + STANDARD + MFA enabled: the PENDING CHECK refuses" cell; the five passing are the CONTROLs (`base-users-ks1477.txt`). This matches the claim of seven RED and five CONTROL.
12. **Mutants, each against the FULL auth suite (946 tests), DATABASE_URL unset.** Exact-match replace with a pattern-count assertion (count must be exactly 1), restore, final sha256 compared: **restored byte-identical: True** (`mut.py.txt`, `mutants.txt`, `mutants-p1b.txt`).
    - **P1b = the Opus G6 mutant** (pending check boot-window 503 replaced by `return null`): **KILLED, 1 failed / 945 passed**, by exactly the new cell "RED … boot window + STANDARD + MFA enabled: the PENDING CHECK refuses". Before the delta this survived all 943 tests.
    - **P1** pending check reads the map in the boot window instead of refusing: KILLED (2 cells, the new one and the older map-only-request cell).
    - **P2** pending check answers 404 (NotFoundError) instead of 503: KILLED (5 cells, including the new one).
    - **P3** pending check answers a plain Error (500): KILLED (5 cells, including the new one).
    - **G9** review route reads the store BEFORE the role check: **KILLED, 1 failed / 945 passed**, by exactly the new CONTROL "the review route checks the role before the database". Before the delta this survived.
    - **G9b** role check removed outright: KILLED by the same single CONTROL.
    - **G1** `verificationStoreIsMemoryOnly` reverted to `!isDbAvailable()`: KILLED (6 cells, the new RED among them).
    - **C1 / C2** (my "wrong reason" probes, below): both KILLED.
    - **N1** `findPendingVerificationRequest` call replaced by `null`: KILLED (12, new RED among them; also trips the KS-1000 baseline gate).
    So of my 10 mutants, 10 killed. The author's "eight mutants all killed" was not re-run patch for patch; I ran my own set, which includes both mutants Opus left alive.
13. **Can the new cells pass for the wrong reason?** I tried two ways to make the reachable-database CONTROL ("a reachable database + STANDARD + MFA auto-approves") pass without really reaching the database branch of the pending check. C1 makes that branch throw: 19 cells fail, including this CONTROL. C2 makes that branch answer "a PENDING row exists": 23 cells fail, including this CONTROL. So the control does go through the `isDbAvailable()` branch and does consume its answer. For the new RED: P1b fails it alone, and the cell also asserts `updateUserOrThrow` not called and `state.inserts === 0`, so a 503 produced by the save guard instead of the pending check would still fail the side-effect assertion... see Note 2 for the limit of that argument.

## Findings

**Major: none.**

**Minor: none.** Both Opus Minors are closed:
- Minor 1 (8 env-dependent cells): closed. Evidence: run 6 (parent's tests, variable set: 8 failed) against runs 3, 4 and 5 (head, variable set: all green, 946/946 and 72/72). The restore is correct, restores an originally-unset value by deleting it, and survives a throwing `beforeAll` (run 7).
- Minor 2 (G6 and G9 survivors): closed. G6 is killed by exactly the new RED cell and G9 by exactly the new CONTROL, each alone (run 12). The author's description of the G9 cell as a CONTROL that passes on the base is accurate and stated honestly in the cell's comment; it pins an ordering and does not claim to prove the new refusal.

**Note 1: tests-only claim holds.** 4 files, 62/2, one commit, users.ts blob unchanged (runs 1 and 2). Nothing here changes product behaviour; the product-side verdict from the Opus gate stands untouched.

**Note 2: the reachable-database CONTROL does not distinguish "DATABASE_URL set" from "unset".** With a reachable database, `isDbAvailable()` is true, so the pending check takes the database branch whether or not `DATABASE_URL` is set; the auto-approve would pass either way. That is fine for its stated purpose (proving the RED's 503 comes from the boot window and not from the setup) and run 13 shows it reaches the database branch, but it does not pin the DATABASE_URL predicate. That predicate is pinned by the other cells (G1 is killed, run 12). This is a description limit, not a gap.

**Note 3: tsc does not cover tests (run 8).** The `tsc --noEmit` the claim lists is blind to test files; `check:test-types` is the real test-type gate and it is clean (run 9). Not a defect of the PR; worth knowing when reading "tsc clean".

**Note 4: carried over from the Opus gate, untouched by this delta.** G3 (empty DATABASE_URL counts as configured) and G4 (whitespace-only URL) were survivors in the Opus gate and were not in the delta's scope; I did not re-run them. The Opus Notes 1 to 5 on operational consequence and the pre-existing test-model gap stand.

## NOT tested

- Tests-only delta on top of an Opus-gated head: I did not re-derive the product-side fix review (all four store functions, the 503 helper, db.ts). I relied on the Opus verdict for it and on users.ts being byte-identical.
- No merge over current `origin/develop` (361537ee). The Opus gate merged the parent cleanly and passed 992/992 there; I ran the head alone (91 files, 946). A develop merge of the 4 test files was not run.
- A throwing TEST BODY (as distinct from a throwing `beforeAll`) was not separately probed for the restore; it relies on vitest running `afterAll` after a failed test, which is its documented behaviour.
- Default isolated pool only was exercised on the full suite; the shared-process probe (run 7) used `--no-isolate`.
- The author's own M1 to M6 patches and the author's "twice" repeat were not re-run; I ran the full suite once per environment and each mutant once. Old Opus survivors G3 and G4 were not re-run.
- No real Postgres, no Docker, no schemathesis or shell leg, no live boot window.
- ESLint was run on the 4 touched files only, not on `eslint src`; tsc on the package config only.
