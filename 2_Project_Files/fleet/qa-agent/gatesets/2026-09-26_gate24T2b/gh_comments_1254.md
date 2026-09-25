--- comment 5834512992 by linear[bot] at 2026-09-25T14:56:41Z
<!-- linear-linkback -->
<details>
<summary><a href="https://linear.app/secuura/issue/KS-1155/packagesshared-tree-walking-guards-exceed-vitests-5-s-default-under">KS-1155 packages/shared tree-walking guards exceed vitest's 5 s default under fleet load — 5 cells at load 32, 9 at load 25–49, 5,243 ms alone at load 27; assertions hold (green solo / with testTimeout raised / at load 11) — a load class that costs a re-run on every merge</a></summary>
<p>

## BLUF

`packages/shared`'s repo-tree-walking guard cells exceed vitest's 5 s default `testTimeout` when the box carries the fleet's load (several seats' suites + QA gates at once). The assertions hold every time — the same cells pass solo, or with `--testTimeout` raised, or on the same tree minutes later at a lower load. So a red `Test timed out in 5000ms` in these files on a loaded box is a **load class**, not a product finding — but a merge seat cannot tell that from the run alone without a solo re-run or a raised-timeout re-run, which costs minutes on every merge. Filed so the class has a name and a home (KS-1053 names it only as context for the `services/auth` ks949 cell, a different suite).

## The measurements (all 2026-09-14, all on trees where the guard files are blob-identical to develop)

* **s224 (quoted as s224's, from its STACK READY mail 02:54:51Z):** `packages/shared` 43 files / 835 — **830 passed / 5 failed at load 32**, every failure `Test timed out in 5000ms` in the tree-walking guards (`crypto-agility.guard.test.ts`, `entrypoint-corpus.test.ts:180` the CENSUS cell, `ks727-errorhandler-class-guard.test.ts:905`, `ks764-key-revoke-call-site-guard.test.ts:263`, `ks860-test-listeners-bind-loopback.test.ts:463`); **1 at load 34**; the same cells green solo (**5,243 ms alone at load 27** — over the 5 s budget even solo, under that load).
* **s220 (the merge seat, PRED(985)** `3239e7207`**,** `item11/suite985/`**):** run at load 25–49 — **835: 822 passed / 9 failed / 4 skipped**, all nine timeouts: `crypto-agility.guard.test.ts` (5 s), `ks256-spec-example-contract.test.ts` (5 s, the positive-control cell), `ks727-errorhandler-class-guard.test.ts` ×4 (5 s: the CONTROL enumeration, the 🔴 corpus-is-the-shared-derivation cell, its CONTROL, the ROOTS-pinned cell), `ks764-key-revoke-call-site-guard.test.ts` (5 s, CALL_SITES), `ks781-p3-3-body-parser-order.test.ts` ×2 (a 10 s **hook** timeout in KS-832's ACCEPTANCE BAR + LEG C 5 s), `threadToken.test.ts` (**30 s**, `parameteriseMintPolicy` different-seeds — a crypto cell, not a walk). Solo re-runs at load 47–49: four files green; `ks727` and `ks781` still one timeout each. With `--testTimeout 120000 --hookTimeout 120000` at load ~20: `ks727` **94/94**, `ks781` **231/231**. The full suite again with the raised timeouts at load 11: **43 / 835 / 0**.
* **s203 (KS-1053's context line, 2026-09-13):** three `Test timed out in 5000ms` in the same guards at load ~20.
* Not the same subject as KS-1053 (the `services/auth` ks949 cell, 5.7–6.0 s on a 5 s budget under load, mechanism unestablished) — related as the neighbouring load-class record.

## What this costs today

Every merge-seat run of `packages/shared` on a loaded box is a coin-flip red that has to be re-run solo or with the timeout raised before it can be read (the s220 protocol did both). The tree walks themselves are the guards' point (they read the whole `services/` + `packages/` tree by design); their budget is the default 5 s.

## Fix shapes (the owner's call)

1. A per-file `testTimeout` (and `hookTimeout`) for the tree-walking guards — 30–60 s — set in the test files or a `vitest.config` `test.testTimeout` override scoped to `__tests__/*guard*.test.ts`, so a slow walk under load is a slow walk, not a red. Keep the default for everything else.
2. Share one tree walk per run (a cached corpus) instead of one per cell — `entrypoint-corpus`, `ks727`, `ks781`, `ks860`, `ks879` each walk the tree; the walk is the cost.
3. `threadToken.test.ts`'s 30 s cell is a different shape (CPU-bound crypto); its own budget line.

## Done when

- ☐ the tree-walking guard cells carry an explicit timeout budget that a loaded box meets (measured: a full `packages/shared` run at load ≥ 30 reads 0 timeouts), or the walk is shared and the cells fit the default
- ☐ the merge-seat protocol no longer needs a solo re-run to read a `packages/shared` result on a loaded box
</p>
</details>
<!-- linear-review-link -->
<p><a href="https://linear.app/secuura/review/ks-1155-walkbudget-give-the-tree-walking-guards-a-60-s-budget-from-e2d314372e87">Review in Linear</a></p>

