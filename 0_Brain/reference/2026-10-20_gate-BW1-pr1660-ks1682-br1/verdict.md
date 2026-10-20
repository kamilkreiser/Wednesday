VERDICT: GO WITH NOTE at head 1400219cf2b8... (tier 2, round 1 of 2; landing tree ceea2e18a5b7 on develop 610570e5a757; 0 blockers, 2 notes)

## BLUF
Tier 2 holds: the three-dot diff is exactly one test file, no product, migration or config byte. W6 now reds under both of the author's tampers (and under a third of mine) while W1-W10 stay green under T1. X1, X2 and X5 each red exactly their own new cell (W7, W8, W9), G3-G7 red the stated cells, and dropping the `typeof` conjunct reds W10. The m365 suite goes 220 -> 224 cells with only W6's old title vanished, the test file type-checks in its own program, and the landing tree reproduces. Two notes: the author's "`e.secret !== ''` is unobservable at the return value" is only true for a single-entry cache (it IS observable with two entries), and W6 does not enforce "non-empty string" for a non-string registry value (type-blocked).

## Findings
- **N1 (author claim refuted in part, `e.secret !== ''`):** with TWO cache entries, one valid (`RT-GOOD`) and one with the same matching id and secret `''`, the honest selector returns `RT-GOOD`; with the clause dropped, `mine.length` is 2, the fail-closed branch fires and it returns `''`. Measured with a scratch probe (not in the PR) through the real msal cache. So the clause is pinnable at the return value by a two-entry cell, not only by the warning. Direction is fail-closed (a lost token, not a leaked one), so low severity; the header's "none can" is overstated. The author's plan to pin it via the logger in item 2 is still fine.
- **N2 (W6 scope):** W6 guards distinct + not `''` + count 9 only. Setting a registry value to `undefined` (needs an `as unknown as string` cast, so tsc blocks it normally) or a whitespace-only string leaves W6 green. Harmless, and the comment says a new cell not registered does not red it, so the author already discloses the main limit.
- No blocker. The author's other claims reproduce as stated.

## FOUND / TESTED / HOW
- **Heads:** `ls-remote` of GitHub at start (00:59Z) and end (01:03Z): #1660 = 1400219cf2b88cc60f08719bfa0295c8066c9b8c, develop = 610570e5a75790d8ebf4264c4aec3ec8bebc0609, unchanged and equal to the brief. (Local project clone's develop differs; I used GitHub via the project's read deploy key from my own scratch clone.)
- **Q1:** `git diff --name-status gh/develop...pr1660` = one line, `M Blockchain/Dev/services/m365-integration/src/__tests__/ks1682-the-account-match-is-exact.test.ts`. Merge-base f4259b8ed387 (matches the author's clone base). `merge-tree --write-tree` rc 0 = ceea2e18a5b7ca5d868558f9ac427f504476facc, equal to the author's figure.
- **Q2:** every arm below: anchor count asserted 1, tsc rc 0 (child program that includes the test file) before the arm counts, only the new file run via vitest JSON, 0-passed-and-0-failed treated as load failure (none), restore asserted by sha256 after each arm (all MATCH). Baseline: 11/11 pass, 0 red.
  - T1 `padded: ''` -> only W6 reds (`expected [ '' ] to deeply equal []`); 10 others pass, so W1-W10 green under T1 confirmed (W3 seeds that secret).
  - T2 `suffix: 'RT-PREFIX'` -> only W6 reds (`expected 8 to be 9`).
  - My tamper `uidOnly: 'RT-EXACT'` (duplicate of the control's secret) -> only W6 reds. A first own tamper (deleting a registry key) did not compile (tsc rc 2) and is inadmissible; not counted.
  - Not-red probes: `orphan: undefined` cast and `padded: ' '` leave all 11 green (N2).
- **Q3 (product selector swapped, each compiled rc 0):** G3 -> W1,W7; G4 -> W2; G5 -> W3; G6 -> W3,W4,W7,W8; G7 -> W5; X1 startsWith -> W7 only; X2 endsWith -> W8 only; X5 accept '' -> W9 only. Failures are assertion errors (`expected 'RT-PREFIX' to be ''` etc.), not load failures. Extra: X3 reverse-includes -> W1,W9. W0 and W6 pass under every product mutant.
- **Q4:** drop `typeof e.secret === 'string'` -> W10 only (`expected 12345 to be ''`). Drop `e &&` -> no cell reds (C1). Drop `e.secret !== ''` -> no cell reds (C4). Drop the id match (C2) -> W1-W5, W7-W9 red (8 cells), as claimed.
  - `e &&` unreachable: AGREE. msal-node 3.8.10 `src/cache/serializer/Deserializer.ts:159` (`homeAccountId: serializedRT.home_account_id` in `deserializeRefreshTokens`) throws; my probe reading a `{k: null}` cache got `Cannot read properties of null (reading 'home_account_id')` out of `deserialize` before any selector runs.
  - `e.secret !== ''` unobservable: REFUTE in part (N1): unobservable with one entry, observable with two.
- **Q5:** full m365 suite, vitest JSON, compared by file + fullName. develop 610570e5a757: 23 files / 220 cells / 220 passed / 0 failed. Head: 23 files / 224 cells / 224 passed / 0 failed. Vanished: exactly one, the old W6 title (`... every near-miss token above is a DISTINCT value ...`). Status changes 0. New 5 (W6 new title, W7-W10). Child tsc program (`extends` the service tsconfig, `exclude: []`, rooted at the scratch clone): 23 `__tests__` files in the child, 0 in the service program; rc 0 (service program rc 0 too).

## NOT RUN
- No Docker, platform suites, preflight legs or `audit:gate`; author's 13/16 preflight and ratchet figures not re-run. No real Microsoft sign-in or network call.
- Environment: `@electric-sql/pglite` is not declared in this package's package.json or lockfile, so two other test files (ks1673, ks1677) fail to import after a clean `npm ci`. I symlinked the package from an existing worktree's node_modules into my scratch clone (read-only source) to run them; both then passed. Pre-existing and unrelated to #1660, but worth a separate look because a clean checkout cannot run 4+ cells.
- Also set up in the scratch clone only: `npm ci --ignore-scripts`, manual `packages/shared` build, a symlink of `@secuura/shared` into the service node_modules, a probe test file (never in the PR). No logger-based check of warning text beyond the console line seen in the C4 probe.
- `core.sshCommand` in my scratch clone pointed at the project's read-capable deploy key for `ls-remote`/`fetch` only; no push, no writes to GitHub or Linear. The `pretooluse_no_cd` hook refused one `git -C $VAR fetch` form; I used literal paths afterwards. No `cd` and no `rm` used.
- `git -C /Volumes/DevMASTER/WEDNESDAY status --short` at end: ` M 0_Brain/dashboard/data/usage_wednesday.json` only (modified, not mine); no untracked paths outside the permitted folders.

## Wall-clock
00:58Z to 01:06Z 2026-10-20 UTC (11:58 to 12:06 AEDT), about 8 minutes.
sha256 (method: sed '1d;$d' verdict.md | shasum -a 256): e54e08c427d6c5724edee8b36535a1d28ae3e89143470f77fa7768151a308280
