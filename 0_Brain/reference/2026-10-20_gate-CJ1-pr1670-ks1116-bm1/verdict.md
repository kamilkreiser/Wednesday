VERDICT: GO at head 67f83d4d1ad2... (tier 2, round 1 of 2; landing tree a87a7230c5cbbd267a017cb33ef0dfc7a7e1f386 on develop c3ea4dc79af72f62ad7f211d1dbf8b9920ea094d; 0 blockers, 0 notes)

## BLUF
Tier 2 confirmed (three-dot): `git diff --name-only origin/develop...pr1670` returns exactly 1 path, the vc-issuer KS-1116 test, +6/-0; `ownership.ts` sha256 `895064d3...2270` is identical on the PR head and on live develop (zero product bytes). The patch body equals the Spark's `patch.diff` byte for byte. The three rows pin what BM1 NOTE 1 names: the two hand mutants (BM1 `startsWith`, BM1b `includes`) are GREEN on live develop (291/291) and RED on the PR (4 each, three of them the new EXTENDS cells), and the role-prefix mutant is green on develop and red on the PR (6 new cells). Cells 291 -> 300, 0 vanished, 9 new. Lint rc 0, test program type-checks. Heads unchanged start to end.

## Findings
No blockers, no notes. Observations only:
1. **Landing tree differs from the claimed one, as predicted.** Claimed `138c8f8f...` was computed on develop `f01ba49d`. On live develop `c3ea4dc7` (#1668) the landing tree is `a87a7230...` (`git merge-tree --write-tree origin/develop pr1670`, clean). Controls: it differs from the PR head tree `138c8f8f...` by exactly the two m365 files #1668 moved (`ks1682-the-account-match-is-exact.test.ts`, `ks1682-the-warnings-go-through-the-service-logger.test.ts`), and from develop's own tree `355fafd1...` by exactly the one vc-issuer test file. `develop f01ba49d..c3ea4dc7` touches only those two m365 test files: file-disjoint, verified. I also built that landing as a commit on develop and ran the suite on it: 300/300.
2. The PR head `67f83d4d1ad2` equals the claim; ls-remote at start and at end returned the same PR head and the same develop `c3ea4dc7`.
3. The author's inadmissible first conjunct mutant (TS6133) is real: I reproduced it with a role-prefix mutant that dropped the Set (tsc rc 2), and used the Set-preserving form instead.

## FOUND / TESTED / HOW

**Q1 Scope / patch identity.** Patch body (from `--- a/` on, git header lines stripped) of `git diff origin/develop...pr1670` has sha256 `98fae178ea0bdf33a042095f111d1348cc113012b72b197949c9155ed2ffe25d`, `cmp` identical to the Spark's `out.md.checker/patch.diff` (same sha). The Spark file has no `diff --git`/`index` header lines, so a whole-file cmp differs at char 1; that is the header only, the hunk is identical. The six added lines are a 3-line comment and the 3 rows: ORG_VIEWER (`{...ORG_ADMIN, role:'ORG_VIEWER'}`), SYSTEM_SERVICE (`{...SYSTEM_ADMIN, role:'SYSTEM_SERVICE'}`), ORG_ADMIN with tenant `` `${T1}0` `` (EXTENDS).

**Q2 The rows pin NOTE 1.** All mutants edit `services/vc-issuer/src/ownership.ts` (anchor count asserted == 1, `tsc -p tsconfig.json --noEmit` rc 0 before the mutant counts, restore asserted by sha256 each time). Red counted by assertion (JSON reporter status, keyed by cell name).
- BM1 `(claim(user?.tenantId) ?? '').startsWith(rowTenantId)`: tsc 0; PR **4 red / 296 pass**: the EXTENDS cell on A9 (credentials DB), A5 (presentations DB), A2 (presentations memory), plus the existing A7 cell (it loops the whole table, so it turns red on the new row). Control: the same mutant on live develop: **0 red, 291/291**. So the EXTENDS row is the only thing that catches it.
- BM1b `.includes(rowTenantId)`: identical to BM1: same 4 cell names red on the PR, 291/291 green on develop.
- Reverse direction REV `rowTenantId.startsWith(claim)` (null-guarded): tsc 0; PR **7 red**, all 7 are OLD cells: the "ORG_ADMIN / SYSTEM_ADMIN whose tenant is a strict PREFIX of the row's tenant" cells on A9, A5, A2 (6) plus A7. Zero new cells go red. This is correct: the old strict-PREFIX rows bite the reverse compare, the new EXTENDS row bites the forward one, so the pair covers both directions.
- Role-prefix RPFX2 `TENANT_ADMIN_ROLES.has(role) || role.startsWith('ORG') || role.startsWith('SYSTEM')` (Set kept so tsc is clean; the first draft that dropped the Set was inadmissible, tsc rc 2 TS6133, not counted): PR **7 red** = ORG_VIEWER and SYSTEM_SERVICE on A9, A5, A2 (6 NEW cells) + A7. On live develop: **0 red, 291/291**.

**Q3 Conjuncts of `ownership.ts:92-93`, each flipped with the others held true.**
- Role test widened (`!has(role) && false`, Set kept): **19 red** (13 old, 6 new). Names: OWNER, SUPER_ADMIN, TENANT_ADMIN, `org_admin` lower case (each x A9/A5/A2), the new ORG_VIEWER and SYSTEM_SERVICE (x3), and A7.
- `rowTenantId !== null` removed: **2 red**, both old: the A3 "ORG_ADMIN / SYSTEM_ADMIN with no tenant claim reads an owner-less row whose tenant is ALSO unknown" cells (null === null). No new cell involved, as expected.
- Tenant equality replaced by `true`: **20 red** (17 old, 3 new): ANOTHER tenant, NO tenant claim, strict PREFIX, array-holding-tenant (old, x3 tables where present), A6, A7, and the new EXTENDS cell on A9, A5, A2.

**Q4 Counts by cell NAME (JSON reporter; label = file :: full name).** vc-issuer: develop `c3ea4dc7` 18 files, 291 passed / 0 failed of 291; PR head 18 files, 300 passed / 0 failed of 300; landing commit (tree `a87a7230`) 300/0. Labels unique in all runs (291, 300, 300); reader checks the label count against the reporter totals (failed count cross-check; PARSER FAILURE / "0 total = LOAD FAILURE" guards in the script; totals were 291/300, never 0). develop -> head: **0 vanished, 9 new** (arithmetic 291 - 0 + 9 = 300). The 9 new are the 3 rows x {A2 "presentations memory path", A5 "presentations DB path", A9 "credentials DB path and memory fallback"}; develop -> landing: 0 vanished, same 9 new. 3 rows x 3 tables = 9: ratio 9/9.

**Q5 Type-check, lint, merge.**
- `tsc -p services/vc-issuer/tsconfig.json --listFilesOnly` lists **0** files under `src/__tests__` (control: the main tsconfig does exclude tests, as stated). `tsc -p services/vc-issuer/tsconfig.test.json --noEmit` (the tracked file, which leg 16 uses): **rc 0**; `--listFilesOnly` shows 32 files under vc-issuer/src, 18 of them tests, the changed test listed. Positive control: appended `const __ctl: number = 'str';` to the test: rc 2, TS2322 at the test file; file restored, sha256 asserted (`0f2cb3a6...`) and `git status` clean.
- `npm run lint --prefix services/vc-issuer`: rc 0. Positive control: appending `debugger;` and `var` to the test file gives rc 1 with `no-debugger` and `no-var` at the test file's lines, so lint reaches `src/__tests__`; restored by sha256. Direct eslint on the file: 1 file, 0 messages.
- Merge: `git merge-tree --write-tree origin/develop pr1670` -> clean tree `a87a7230...` (see finding 1).

Environment: clone `git clone --shared` of the Spark cache under the scratchpad `gate_cj1/src` (its origin repointed to GitHub with the project's read deploy key to fetch `refs/pull/1670/head` and develop); `npm ci --prefix Dev --ignore-scripts`; `npm run build --prefix packages/shared` rc 0. Originate `generate` and the m365 pglite question did not arise (no originate or m365 test was run; the m365 files were only diffed, not executed).

## NOT RUN
- The repo's pre-push gate legs 3, 4, 8 (need a local stack on :6882), per the author's own disclosure; no Docker, no local stack, no live service, no `az`.
- The four platform suites (Schemathesis, Akto, Playwright, k6): no route, spec, container or service boundary is touched.
- The Spark checker itself (single-tamper red-first instrument) was not re-run; my mutants stand in for it.
- Other services' suites (only vc-issuer was run; the diff is confined to one vc-issuer test file).
- The author's 12-mutant list was not replayed in full; I ran 7 (BM1, BM1b, REV, RPFX2 and the 3 conjunct flips) plus the develop controls.

## Wall-clock
About 3 min 15 s from clone start to the final heads check (npm ci 21 s; vitest runs about 5 s each).

## Hygiene
No temp files in /Volumes/DevMASTER/WEDNESDAY (all work in the scratchpad clone `gate_cj1`; `git status --short` there shows no untracked path outside 0_Brain/, 5_Project_History/, 2_Project_Files/local-model/, 2_Project_Files/fleet/briefs_staged/). No GitHub or Linear writes, no push.
sha256 of `sed '1d;$d' verdict.md | shasum -a 256`: 8c16af2e5767f76cbf2557a682834a15cc8362f8ff01fb4eef7c7c2b899df007