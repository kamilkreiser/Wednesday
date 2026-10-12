# QA gate: Secuura Platform K PR #1510 (KS-1518, TEST half only, tier 2 test-only)

- Head: `4aa440ea741ab003ac09d21f1bac356a6d7f3357`. Bundle sha256/16 `c0fb4bf922342da1`; `git bundle verify`: "The bundle requires this ref: c63cec1f6070e06009969526615011dc8734ac13 ... uses sha1"; `list-heads` = `4aa440ea... refs/heads/feature/ks-1518-approve-forward-timeout-bound-no-cell-refuses-a-bigint-and`.
- Base: develop `c63cec1f6070e06009969526615011dc8734ac13`. Real current tip (`git ls-remote origin refs/heads/develop`, read-only, deploy key): `bfd42c980891975f7427038754dea8c3097ac267` (= builder's #1509; the head is 1 commit behind it).
- How I got the tree: scratch clone `scratchpad/g1510/repo` (local clone of g1509's scratch clone, origin re-pointed to GitHub), `git fetch` of the bundle and of develop (inside the scratch clone only), detached worktrees `g1510/merged` (tip bfd42c98 + `git merge --no-ff` of the head) and `g1510/base` (c63cec1f). node_modules: root `node_modules` is a `cp -a` of g1509's (a directory of relative symlinks, so `@secuura/shared` resolves to the worktree's own `packages/shared`); `services/api-gateway/node_modules` and `services/auth/node_modules` are SYMLINKS to the project's installed ones, as earlier gates did. `packages/shared` rebuilt in both worktrees (`tsc` rc 0, 29 dist entries; before the rebuild the file failed with `Missing "./documents/default-type" specifier in "@secuura/shared"`). Caches written through the symlinks by vitest/tsc were not measured. Nothing written under `!CODING`. Scripts and raw output in `scratchpad/g1510/tools/`; raw mutant output copied beside this file as `mutants_raw.txt`.

## VERDICT: GO

The two cells reproduce as claimed (16/16 on head, 14/14 on base, 114 files / 1104 tests on the merged tree) and all 4 builder mutants plus 10 of my own redden exactly the predicted cells; -0 and 1n are real values, refused by the right guard clause.
Only Notes: the cells pin refusal and the property name, not the reason or the wording (by design), and the BigInt cell title overstates what the cell proves.

## By my runs

**1. Bundle, diff, merge, tree.**
- `git log --oneline c63cec1f..4aa440ea` = one commit, "KS-1518: pin that a BigInt and negative zero are refused as the forward bound". `git merge-base` = `c63cec1f6070e06009969526615011dc8734ac13`.
- `git diff --stat`: "1 file changed, 11 insertions(+)"; `--name-only`: only `Blockchain/Dev/services/api-gateway/src/__tests__/ks1185-f1-workflow-approve-forward-bound-is-validated.test.ts`. No product, config or doc line.
- Builder's `pr1510_full.diff` vs `git diff` of the head: `cmp` differs at char 253 (the `index` line, abbreviated hash length); with `sed 's/^index .*//'` on both, `diff` prints nothing ("identical modulo index line"). `git apply --index pr1510_full.diff` on the pristine base worktree, then `write-tree` = `b34e7fdae2fcb02b24c584e3503bb1b681c74427` = `git rev-parse 4aa440ea^{tree}` (builder's b34e7fdae2fc: match). Base worktree reset to c63cec1f afterwards.
- `git log --stat c63cec1f..bfd42c98` = 1 commit, "KS-1237: pin the refusal message of a non-array connector allow-list", file `ks1204-a-non-array-allow-list-...test.ts` only: disjoint from the PR's file.
- `git merge-tree --write-tree bfd42c98 4aa440ea` = `a0a6a211bae2979afdbcbb2894f5924a7ea9b920`, rc 0. Real `git merge --no-ff` in `merged`: "Merge made by the 'ort' strategy", tree `a0a6a211bae2979afdbcbb2894f5924a7ea9b920` (builder's prediction a0a6a211bae2: match).
- `git status --short | grep -v '^??'` printed nothing after all my runs (rc 1 = clean), in both worktrees.

**2. The guard** (`Blockchain/Dev/services/api-gateway/src/routes/verification.ts:146-153`, `resolveOriginateForwardTimeoutMs`, called at line 468 inside the route factory, so it runs at construction, before any request):
```
if (value === undefined) return ORIGINATE_FORWARD_TIMEOUT_MS;
if (Number.isInteger(value) && value > 0 && value <= MAX_FORWARD_TIMEOUT_MS) return value;
const shown = typeof value === 'string' ? JSON.stringify(value) : String(value);
throw new Error(`originateForwardTimeoutMs must be an integer from 1 to ${MAX} milliseconds (got ${shown}); omit it ...`);
```
Probe (throwaway test `zz_probe_g1510.test.ts` calling the real `createVerificationRoutes`, copied in and removed; output `scratchpad/g1510/probe_out.txt`):
```
1n          Object.is(v,-0)=false  THROWS Error: originateForwardTimeoutMs must be an int ... (got 1)
-0          Object.is(v,-0)=true   THROWS Error: originateForwardTimeoutMs must be an int ... (got 0)
+0          Object.is(v,-0)=false  THROWS ... (got 0)
0           Object.is(v,-0)=false  THROWS ... (got 0)
1                                  builds
2147483647                         builds
2147483648                         THROWS ... (got 2147483648)
NaN                                THROWS ... (got NaN)
isInteger(-0)=true  (-0>0)=false  isInteger(1n)=false
```
(Same output on head tree and base tree; the product file is identical.) So: 1n is refused by `Number.isInteger` (false for a BigInt); -0 passes `Number.isInteger` and is refused ONLY by `> 0`; the messages for 1n/1 and -0/0 print identically, which is the half of the ticket this PR does not touch.
- The cells: `ks1185-...test.ts:96-102` (`build(1n)` and `build(-0)` inside `expect(() => build(x)).toThrow(/originateForwardTimeoutMs/)`). `build` (line 77) calls `createVerificationRoutes` synchronously, so the throw asserted is the construction throw, not a request-time one; no server, no await. They assert the property-name regex, not the type (`Error`) and not the "(got ...)" text, so a prefix-equivalent assertion, not a brittle full-message one. The older cells' second assertion `toThrow('(got 0)')` is not copied, as the comment at lines 92-94 says.

**3. Runs.**
- File on the merged tree: `Test Files 1 passed (1) / Tests 16 passed (16)`. File on base worktree: `Tests 14 passed (14)`. (Builder: 16/16 and 14/14.)
- Full api-gateway suite on the merged tree (`npx vitest run` in services/api-gateway): `Test Files 114 passed (114) / Tests 1104 passed (1104)`. The builder's 1103 is on the head before #1509; #1509 added one test (gate 1509: 10 -> 11), so 1103 + 1 = 1104 is consistent. Product file sha256/16 before this run `b82b86a9d8038c57`.

**4. Mutants** (`tools/mut.py`, each applied alone to `verification.ts` on the merged tree; red set read from `--reporter=json` and compared by EQUALITY; every line printed `sha b82b86a9d8038c57=b82b86a9d8038c57 restored-identical`; control with no mutation: red = {} of 16). Raw: `mutants_raw.txt`.
- Builder's 4: B1 the gate's escaped tamper (`typeof value === 'bigint' && value > 0n` accepted) red = {BigInt cell} EXACT; B2 `-0` accepted via `Object.is(value, -0)` while +0 still refused: red = {-0 cell} EXACT (the `0 (never...)` cell stays green); B3 `> 0` to `>= 0`: red = {the `0` cell, -0 cell} EXACT; B4 BigInt coerced through `Number()` before the check: red = {BigInt cell} EXACT.
- Mine: O1 accept every bigint: {BigInt}; O2 `value === 0` accepted (both zeros): {0 cell, -0 cell}; O3 `<= MAX + 1` (2147483648 accepted): {the 2147483648 cell}; O4 `<= MAX` to `< MAX`: {the 2147483647 edge control}; O6 BigInt refused with an error NOT naming the property: {BigInt}; O7 -0 refused with an error not naming the property: {-0}; O8 `Number.isInteger(Number(value))`: {BigInt, '800', true}; O9 `> 0` to `> -1`: {0 cell, -0 cell}; O10 bigint returns a value at build: {BigInt}; O11 -0 normalised to 0 first (equivalent, still refused): {} as predicted. All EXACT.
- O5 (reject every non-number up front with `originateForwardTimeoutMs must be a number`, no "(got ...)" text): red = {null, '800', true} (the older cells that assert `(got ...)`), the BigInt cell and the -0 cell stay GREEN. My pre-set expectation was {} so the script printed DIFF; the DIFF is my expectation missing that the older cells pin the "(got" text. The point of O5 stands: see Note 1.

**5. Is the -0 cell vacuous? Is the BigInt cell?**
- -0 cell: the source literal `-0` is a real negative zero at runtime: the probe prints `Object.is(v,-0)=true` for the `-0` row and `false` for `+0`; B2 (which matches only `Object.is(value, -0)`) reddens the -0 cell and leaves the `0` cell green, which a literal `0` could not do. On the base product, `Number.isInteger(-0)` is true and `(-0) > 0` is false (probe), so the only clause that refuses -0 is `> 0`; B3/O9 (the clause loosened) redden it, O11 (-0 turned into +0 before the clause, still refused) does not, as expected. Not vacuous.
- BigInt cell: not vacuous against acceptance mutants (B1, B4, O1, O8, O10 all redden it). It IS satisfied by O5 (every non-number refused, any message containing the property name): it pins refusal, not the reason (`Number.isInteger`). That is the builder's stated limit; see Note 1.

**6. Test-type ratchet, lint, markers** (merged tree, `npm run check:test-types`, rc 0):
- `typecheck-tests: auth (tsconfig.test.json): tsc examined 144 files, 93 of them under __tests__; 42 errors: 42 in the baseline, 0 new; 0 stale baseline entries.`
- `typecheck-tests: api-gateway (tsconfig.test.json): tsc examined 149 files, 114 of them under __tests__; 35 errors: 35 in the baseline, 0 new; 0 stale baseline entries.`
- Same two lines on the base worktree: examined 144 / 149 on both, so examined rose by 0 (a file edit); baseline 42 / 35, new 0, stale 0 on both.
- `npx eslint <file>`: rc 0, no output. Planted-`debugger;` control: `140:1 error Unexpected 'debugger' statement no-debugger`, rc 1; restored via `git checkout`, sha256/16 `5dff8f43daf80374` before = after.
- `grep -nE "\.(only|skip|todo|runIf|skipIf|concurrent)\b|\bxit\b|\bxdescribe\b"` on the file: no output, rc 1. Positive control `printf 'it.only(1)\n' | grep -nE <same>` prints `1:it.only(1)`.

**7. Other.**
- Titles: the two new titles (`RED KS-1518 - a BigInt bound (1n) ...`, `RED KS-1518 - negative zero ...`) are unique; the loop titles carry `${label}` and none of the labels is BigInt or negative zero. No duplicate titles.
- State: the only file-level mutable state is `servers`, reset by `afterEach`; the new cells build without a server and touch nothing. `--sequence.shuffle --sequence.seed=1..5` on the merged tree: 16/16 green on all five. `-t KS-1518`: `2 passed | 14 skipped`, i.e. each new cell runs alone.
- Ordering dependence: none found (contrast #1509's COMPLETENESS).

## Findings

**Major**: none.

**Minor**: none.

**Note**
1. `ks1185-f1-workflow-approve-forward-bound-is-validated.test.ts:96` (the BigInt cell title): "...because Number.isInteger refuses every non-number". The cell does not prove that reason: under O5 (reject all non-numbers up front) it stays green; it proves "refused at construction with a message naming the property". The builder said this ("pins the outcome, not the mechanism", mail point 2, and the comment at lines 92-94); only the title words overstate it. Not blocking; a title edit or comment would remove the overstatement.
2. Same cells, by design: they do not assert the `(got ...)` text, so the ticket's other half (1n prints as `1`, -0 as `0`, verified in the probe) stays unpinned and KS-1518 correctly stays open. When the message is fixed, these two cells will need a "(got ...)" assertion added or they will not notice a regression of that fix.
3. Neither cell asserts the thrown type (`Error`), only the property-name regex. A mutant throwing a different error class with the same text stays green. The product has one throw site (line 150), so low risk; not mutated.
4. `0n` (BigInt zero) and a negative BigInt (`-1n`) are not covered (O1 accepted all bigint and was caught by the `1n` cell only). They are refused today by `Number.isInteger(0n) === false` (probe row for 1n shows the same clause). Out of the stated scope of the PR.

## Not measured

- The builder's own mutant files (I re-implemented the 4 shapes from the mail; B1 is the gate's escaped tamper text as quoted in the brief).
- Hook leg 16 on the branch cut (the builder's push log); I ran `check:test-types` myself on the merged tree instead.
- Schemathesis, Akto, Playwright, k6, any live/deployed check (no product change).
- Whether the file passes on Node versions other than the local one; `Number.isInteger`/`Object.is` semantics are spec-level, but I did not run another Node.
- `-1n`, `0n`, and a boxed `Object(1)`/`new Number(0)` as a bound (not asserted by the PR; not run).
- Anything about GitHub PR state (CI results, review threads): no GitHub reads beyond `ls-remote`/`fetch` of the branch develop.
