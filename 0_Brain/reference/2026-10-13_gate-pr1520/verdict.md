# Gate: Secuura Platform K PR 1520 (KS-1511 part 2)

- Head under test: 38154e405237fa0bb724e72f885af10684140c0a (read live: refs/pull/1520/head, matches exactly)
- develop now: 250596098fa9c2b5e1d5930afeef882143b5f5f1 (read live); PR base 898a1ae11f3c
- Tree method: scratch clone (`git clone --shared`) + fetch of both refs, `git archive` of Blockchain/Dev + CLAUDE.md into a fresh scratch dir, node_modules as a shell of symlinks to the main checkout deps (read-only), @secuura/* links re-pointed into the scratch tree (shared -> ../../packages/shared), packages/shared built there with tsc.
- Tier: 3, through-code, test-only. Nothing written inside !CODING.

## VERDICT: GO

Majors: 0. Minors: 2 (both cosmetic, below).

## Majors
None. The cells that claim to pin the typeof guard do fail when it is removed (M1 reds Y1 and Y2), and no product line changed.

## Minors
1. Cell X packs two expectations into one `it` (?limit=5&limit=500 then ?limit[]=500). If the first fails the second is never evaluated. Harmless; it is a control kept because the ticket named it.
2. The new cells assert [status, error.code, overfetch-param] (the file's existing tuple), not the message text. That is the same standard as the other 16 cells; message text stays pinned by B10 only. A message-only mutation (not in the table) would not be caught by the new cells.

## Findings per job item
1. Topology: `git diff 898a1ae11f3c..38154e405237 --name-status` = exactly one path (M), the ks1359 test under Blockchain/Dev/services/api-gateway/src/__tests__/, +17 -0. No non-test path, no product line. routes/platform.ts blob in the extracted tree = fa85e9d6477f (hash-object equals the PR head's blob). `git merge-tree --write-tree develop pr` = clean, tree 8fbca17f49fba15163dbf1679a3f618c499d0da4 (matches builder's 8fbca17f49fb).
2. Cells: all three assert the exact tuple `[400, 'VALIDATION_ERROR', null]`: exact status, exact error.code, and null overfetch (proves the audit query never ran). They use the same harness as the other 16: real `createPlatformRoutes` on an http.Server on 127.0.0.1 behind real express and the route's real requireSuperAdmin; only authenticateToken is stubbed to a super_admin (identical to the existing cells). Not just "not 200". Real express qs parsing produces the arrays (probe below).
3. Ran the file at head: 19 passed (19). Ran the four files that build/import platform routes (ks1359, ks1510, ks843, ks480): 51 tests green in the control. Other audit-named tests (ks1410, ks1457, ks745, ks871) are covered by the full api-gateway run, not separately.
4. Tamper table (routes/platform.ts mutated in the scratch tree, restored after each run, sha256 equal to the original every time, a5f53bf552644222...; baseline GREEN 51/51 in C0 before counting kills; the four files run each time):

| id | mutation | red cells (of 51) |
|---|---|---|
| C0 | none (control) | 0 |
| M1 | typeof guard dropped | 2: Y1 (limit[]=5), Y2 (offset[]=0). X stays GREEN, confirmed |
| M2 | only a repeated key refused (`Array.isArray(v) && v.length>1`) | 2: Y1, Y2 |
| M3 | offset loses the guard | 1: Y2 only |
| M4 | limit loses the guard | 1: Y1 only |
| O5 (mine) | MAX_AUDIT_LIMIT 200 -> 500 | 5: B5, B6, B7, B10, spec-bound cell. New cells stay green (correctly; arrays are refused by the guard regardless of max) |
| O6 (mine) | arrays throw (500) instead of 400 | 3: X, Y1, Y2 (status is asserted exactly) |
| O7 (mine) | offset arrays admitted wholesale | 1: Y2 |
| O8 (mine) | refusal status 400 -> 422 | 14: all 400-cells including X, Y1, Y2 |
| O9 (mine) | refusal code VALIDATION_ERROR -> BAD_REQUEST | 13: includes X, Y1, Y2 (B10 is not red as it checks message only) |

Builder's M1-M4 reproduce exactly as claimed. All six restorations verified by sha256 and the final tree hashed to the head blob.
5. Independent check of the key finding (real express query parser, the route's exact predicate, with and without the guard):
   - ?limit=5&limit=500 -> ["5","500"]: 400 with guard, 400 without
   - ?limit[]=500 -> ["500"]: 400 with guard, 400 without (500 > 200)
   - ?limit[]=5 -> ["5"]: 400 with guard, 200 WITHOUT
   - ?offset[]=0 -> ["0"]: 400 with guard, 200 WITHOUT
   - (extra) ?offset=0&offset=0 and ?limit=5&limit=6: 400 either way.
   So the ticket's pair is refused with or without the guard; limit[]=5 and offset[]=0 are the shapes that need it. Builder's claim holds.
6. Suite and static checks, from the scratch tree:
   - api-gateway vitest, whole suite, run twice: 117 files / 1126 tests passed, 0 failed, both times (was 1123, +3).
   - eslint on the changed test file and routes/platform.ts: exit 0, no output. (No separate positive control run; the repo config is the one in the tree.)
   - `check:test-types` equivalents run for both packages: api-gateway 35 errors, all in baseline, 0 new, 0 stale; auth 42 in baseline, 0 new, 0 stale.

## Exactly what I ran
git ls-remote; shared clone + fetch; git diff/name-status; git merge-tree --write-tree; git archive; mknm-style symlink shell; tsc build of packages/shared; vitest on the ks1359 file; tamper1520.mjs (10 runs x 4 files, JSON reporter); probe1520.mjs (real express qs parsing); full vitest api-gateway x2; eslint; scripts/typecheck-tests/check.cjs for api-gateway and auth.

## NOT TESTED
- The CI pipeline and the schemathesis sweep (KS-1511 part 1, the baseline-entry retirement, is not in this PR).
- Live deployed behaviour of the route.
- Whole-repo suites outside api-gateway; the other 3 workspaces' check:test-types beyond api-gateway and auth.
- Merged result (develop + PR) was only checked by merge-tree for cleanliness; I did not run tests on the merged tree (delta since base is PR 1519's verification.ts and the ks1185-f1 test, builder claims no overlap; merge-tree agrees).
- eslint positive control.
- The audit-log tests ks1410/1457/745/871 individually (covered inside the full run).
