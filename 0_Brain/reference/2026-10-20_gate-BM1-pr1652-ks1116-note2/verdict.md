VERDICT: GO WITH NOTE at head a4d5aa81f3ba... (tier 2, round 1 of 2; landing tree a543b4ac883b752337224b840d4f6b86ea4b649f on develop cd63883c62a9bb0e66969df8cd3f02db2b9b2217; 0 blockers, 2 notes)

## BLUF
Test-only, as claimed: one file, +23/-0, `ownership.ts` blob `af65254c888d` identical at develop, base and head. JM8 and JM11 both reproduce as red by assertion (7 each, tsc rc 0), A0 fails when its fixture is broken, and the suite at the landing is 291/291 (develop 278/278, 0 develop cells missing, 13 added). Landing tree is **a543b4ac883b**, clean, tsc rc 0. No blockers. Two notes: (1) two neighbouring mutants of the same predicate, which I made up, are still green in the whole 291-test suite; they are outside what NOTE 2 asked for. (2) The brief's recipe was not literally followable for clone and fetch (see NOTE 2 below, process only).

## Findings

### Blockers
None.

### Notes
- **NOTE 1: two sibling predicate mutants survive the whole vc-issuer suite (291/291 green, tsc rc 0).** Neither is JM8 or JM11, so the PR does what it says. They are the same two predicate lines, with the same shape of gap:
  - **BM1, tenant compare reversed:** `claim(user?.tenantId).startsWith(rowTenantId)`. A tenant claim that EXTENDS the row's tenant (e.g. `ks1116-tenant-10` reading a `ks1116-tenant-1` row) would be admitted. Only a strict prefix fixture exists, which is the wrong direction for this mutant, and `T2` (`ks1116-tenant-2`) is neither. Fix would be one more row: an ORG_ADMIN whose tenant is `T1 + '0'` -> 404.
  - **BM4, role matched by prefix:** `role.startsWith('ORG') || role.startsWith('SYSTEM')`. Roles such as `ORG_VIEWER` or `SYSTEM_SERVICE` would be admitted. The table's role rows are TENANT_ADMIN, SUPER_ADMIN, OWNER and `org_admin`, and none starts with `ORG` or `SYSTEM` in capitals.
  The product code is correct on both (`===` and a Set lookup). These are regression-guard gaps, same class as BJ1 NOTE 2, not defects. Round 2 is optional; Wednesday's call whether two more rows are worth a PR.
- **NOTE 2: process only.** The brief's `git clone --shared` of the spark cache gave a clone whose origin is the cache, and the cache has no PR commit. I pointed my clone's origin at `git@github.com:Secuura/Distributed_Secuura.git` (the cache's own origin URL) with `core.sshCommand` set to the Secuura deploy key (read in place, not copied), repo-local to my scratch clone. I fetched only develop and the PR branch. No push, no GitHub write. `$VAR` paths trip the no-cd hook's write-verb check (it matches the literal text), so git writes ran from scripts with literal paths.

## FOUND / TESTED / HOW

| Q | Result | How |
|---|---|---|
| Heads | Start and end identical: #1652 `a4d5aa81f3bae82cd9d23cbdc11692052eb5a8dd` (= refs/pull/1652/head = branch), develop `cd63883c62a9bb0e66969df8cd3f02db2b9b2217`. Matches the brief. | `ls-remote` at 10:20 and 10:23 AEDT |
| 1 Test-only | Three-dot set is 1 file: `Blockchain/Dev/services/vc-issuer/src/__tests__/ks1116-presentation-and-credential-reads-bound-to-the-creator.test.ts`, numstat 23/0, 1 commit (a4d5aa81f). `ownership.ts` blob `af65254c888d` at origin/develop, at the head and at base 89956fe9 (positive control: the same `rev-parse` returns the path's blob at all three, and `ls-tree` finds the path). Landing vs develop: exactly that one file. | `diff --name-status/--numstat origin/develop...head`, `rev-parse <rev>:path` |
| 2 Cells bite | Pristine `ownership.ts` sha256/16 `895064d39beb4ff7`, KS-1116 file 131/131. **JM8** (role set widened with TENANT_ADMIN and SUPER_ADMIN): tsc rc 0, **7 red by assertion, 0 load failures** (A2 x2, A5 x2, A9 x2, A7). **JM11** (`rowTenantId.startsWith(claim)`): tsc rc 0, **7 red** (A2 x2, A5 x2, A9 x2, A7), each on the prefix rows. Restore asserted after every arm (ownership.ts and the test file byte-equal to the snapshot). My own mutants: **BM2** `rowTenantId.includes(claim)`: tsc 0, 7 red, killed. **BM3b** role `includes('ADMIN')`: tsc 0, 7 red (TENANT_ADMIN and SUPER_ADMIN rows), killed. **BM1** reversed startsWith and **BM4** role prefix: tsc 0, **131/131 green, and 291/291 green in the full suite: SURVIVED** (NOTE 1). Inadmissible first cuts (tsc rc 2, TS6133 unused `TENANT_ADMIN_ROLES`) were discarded and re-cut so they compile. **A0 can fail:** prefix fixture changed to `zz-other-tenant-`: A0 red (1 failed, 130 pass); `T1` renamed: A0 red (1 failed, 130 pass); both by assertion. | `mut.py` / `full.py` in the scratch folder, vitest JSON reporter, failing cell names listed per arm |
| 3 No weakening | Develop 278/278 in 18 files; landing **291/291 in 18 files**, KS-1116 file 131. By full cell name + file: **0 develop cells missing** at the landing, 13 added (A0 plus 12 from 4 rows x A2/A5/A9; A7 loops the table and adds no name), 0 non-passing at either. +23/-0 so no `expect(` was removed. Matches the author's 18 / 291 / 131. `packages/shared` was built first (`npm run build --workspace=packages/shared`, rc 0) from a fresh `npm ci --ignore-scripts` (rc 0, 1937 packages) in my clone. | vitest JSON on both arms, name-set diff in python |
| 4 Landing | `merge-tree --write-tree origin/develop a4d5aa81...` rc 0, **tree a543b4ac883b752337224b840d4f6b86ea4b649f**. A synthetic merge commit of that tree was checked out; `rev-parse HEAD^{tree}` gives the same sha. vc-issuer `tsc --noEmit` rc 0 at the landing (the same `tsc` returned rc 2 on a deliberately unused-variable mutant, so rc 0 is not vacuous). The landing differs from develop in exactly the test file. Landing vs PR head also carries #1650's three files (shared comment + 2 m365 tests), as the author said. | `merge-tree`, `commit-tree`, `tsc` |

## NOT RUN
- No eslint and no check.cjs ratchet at the landing (the PR adds 23 lines of test; the author reported eslint rc 0 and BJ1 ran the ratchet on the file's parent). Not independently reproduced.
- No other service's suite; no m365 tests from #1650. Nothing in the PR can reach them.
- No Docker, no real PostgreSQL, no live gateway, no push preflight (the author reported 13 of 16 legs, 3 skipped, not a pass).
- PR body, KS-1116 comment e1be72ea and the Linear board were not read (no GitHub or Linear access used).
- Only one predicate was mutated (`ownerlessRowReadable`); `mayRead`'s owner branch was not touched.

## Wall-clock
10:19 to 10:26 AEDT 2026-10-20. Scratch: /private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/2a56ac36-e9ca-49f4-8d2d-f02d4a53f9ed/scratchpad/gate_bm1/ (src clone, mut.py, full.py, q1-q5.sh, land_suite.json, dev_suite.json, vit_*.json/txt, tsc_*.txt, full_*.json, mut_results.json).
sha256 of `sed '1d;$d' verdict.md` (lines 2 to n-1, this line excluded): 06d02d4409da26dbf3188fdf29677026109f0d84b6a9b21aceb9ad7745939722
