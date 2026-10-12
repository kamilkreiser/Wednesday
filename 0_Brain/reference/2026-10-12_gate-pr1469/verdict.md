# QA gate: Secuura Platform K PR #1469 (KS-1131 items 3 and 4)

Head: `8f2145e1f06854549dd6d7b548e54a375a3a9604` (confirmed against GitHub `refs/pull/1469/head`).

## VERDICT: GO WITH NOTE

The test does what the PR claims. Two Minor, non-blocking residual gaps are listed below.

## By my runs

My own clone: `git clone --no-hardlinks` into the scratchpad. Seat V's deps were symlinked read-only. Nothing was written in the shared repo.

1. **Diff scope. PASS.**
   - Against the real `origin/develop` (2d151b0), the PR diff is exactly one file, +122/-23: `Blockchain/Dev/services/auth/src/__tests__/ks963-preauth-rethrow.test.ts`.
   - The PR merge commit `475927c` has the same numstat.
   - `routes/wallet.ts` is byte-identical between develop and the head, so there is no product change.
   - Trap: seat V's local `origin/develop` ref is stale (65d7722). Against it, the branch looks like 6 files, because it stacks the KS-1006, KS-1236 and KS-1194p2 commits, which are already on the real develop.

2. **Planted-mutant matrix on the real wallet.ts** (plant inserted between the allowed read and the lookup). OLD = parent version of the test, 17 cells. NEW = head, 22 cells.

| Plant | OLD | NEW |
|---|---|---|
| none (real wallet.ts) | 17/17 | 22/22 |
| `void query('INSERT..')` | green (the gap) | RED |
| `query(..).then(..)` write | green (the gap) | RED |
| `await query('INSERT..')` (control) | RED | RED |
| comment naming `userRepo.createUser(` | false RED | green |
| string naming `createUser(` | false RED | green |
| trailing comment on the closing brace | green | green |
| `await ensureWalletRow()` (helper) | RED | RED |

   - Every new RED was checked to be the wallet cell ("NOTHING is written before the lookup").
   - The seat's own log `planted_red_ks1131_real.log` agrees with my results.

3. **Suite counts and types. PASS.**
   - The full services/auth suite is 84 files and 899 tests, all passing. This matches the seat's run4 log. The base was 81 files and 875 tests.
   - tsc on the product code is clean.
   - tsc with the new test file included gives one error, TS1343 `import.meta` at line 187. The parent version has the identical error, so nothing new. A planted type error in a copy was reported, which shows the check can fail.
   - `eslint` on the test file passes.

4. **Robustness.**
   - It is still a source-text scan, but a better one. It blanks comments and strings to equal-length spaces, brace-matches the function body, and uses an allow-set over every call-shaped token before the lookup.
   - It is not tied to line numbers.
   - It fails closed on unknown verbs, and it is pinned to the function name `getOrCreateWalletUser`.
   - The invariant is what KS-1131 asks for. Item 3 is "allow-set every call regardless of await". Item 4 is "brace-match the wallet function body".
   - The F-C and P2 regression cells with synthetic sources are real and discriminating. A P2 control exists.

## Defects

### Major
None.

### Minor
1. **New false-green on a write inside a template interpolation.**
   - Test file lines 251-263 (`blankCommentsAndStrings`, template branch) blank the whole template, `${...}` included.
   - Planting `` const _s = `${await query("INSERT..")}`; `` before the lookup: OLD is RED (the `await` regex saw it), NEW is green. This is a small regression in coverage for an exotic shape.
   - Fix: recurse into `${}`.
2. **Call-shaped tokens the regex cannot see stay green** (line 290, `(?<![\w$.])` plus a dotted-name pattern).
   - All of these were measured green on NEW, and also green on OLD except the interpolation case above:
     - a tagged template, `` await query`INSERT..` ``
     - a bracket call, `await (userRepo as any)["createUser"]({})`
     - an optional invoke, `(query as any)?.(...)`
   - Their risk is very low. The bracket and optional-invoke shapes are caught only when the literal `createUser(` appears.
3. **Line 296 `toContain('SELECT * FROM auth_find_user_by_wallet')` checks the raw body, not the blanked one.**
   - Swapping the query text to an INSERT while keeping a `// SELECT * FROM auth_find_user_by_wallet` comment stays 22/22 green.
   - This already existed in the OLD version (green too). It is not introduced here.

### Notes on false reds (fail closed, intentional)
- Any harmless call before the lookup reds the cell. Examples: `walletAddress.toLowerCase()`, `logger.debug(..)`.
- Converting to an arrow function, or renaming `getOrCreateWalletUser`, reds the cell.
- OLD went red on only the rename and arrow cases, not on the harmless calls. Measured by plant: `walletAddress.toLowerCase()` and `logger.debug` left OLD at 17/17 and turned NEW red.
- This is the allow-set contract the test's own docblock states, so I am not calling it a defect.

## Not checked
- GitHub API / CI status (`gh` is unauthenticated here).
- The Linear ticket's items 1 and 2 (F-A, F-B), which belong to other PRs.

Evidence: sample logs in this directory; scripts and full logs are in the gate scratchpad.
