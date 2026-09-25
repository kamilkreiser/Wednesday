KS-1159 L3b gate record F-931-G1: the ks1061 shared-mock completeness guard is a text scanner — single-quoted jest.mock( only, non-recursive readdirSync, blind to jest.doMock and double quotes (F-931-G2 tsc-excludes-tests already homed at KS-1000 / KS-1090)
state In Progress

## BLUF

The one Record from the L3b tier-2 gate on PR #931 (KS-1061, head `795307023` — GO WITH FINDINGS, no Blocker, no Major) with **no existing home**: **F-931-G1 (Minor, SHIPS-WITH — a class weakness of the new guard, not a regression).** Filed as ONE ticket on Wednesday's ADDENDUM 05:29:55Z. #931 landed as M37 `54e9b835d`. The gate's second finding, **F-931-G2**, already has a home and is NOT re-filed here (below).

Report: `/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-14-ks1061-931-795307023-tier2-r1/report.md` (140 lines, 15:24 AEST; §4 extension probes T6a/T6b/T6c/T7, §5, §8).

**Search before filing (every KS issue incl. archived, 1,148 issues, title + description + comments, literal;** `5_Project_History/2026-09-14_s225/item10/symbol_search.log`**):** `makeSharedMock` → KS-1103 (archived) and KS-485 comments only; `sharedModuleMock` / `jest.doMock` / `ROOT_MOCK` → 0 outside KS-1061; `readdirSync` → KS-1082 / KS-899 / KS-917 (other walkers, not this guard). **No home for G1.** `tsconfig excludes` / `src/__tests__` → **KS-1000 (Backlog, live: "services/auth tsconfig EXCLUDES src/tests** — every 'tsc: 0 errors' …" — the class ticket the 2026-09-14 dedupe consolidated KS-848 / KS-892 / KS-933 / KS-1122 into) and KS-1090 (Backlog, live: "api-gateway + originate: tsc never type-checks #951's three wiring tests") — G2's homes. Controls: a known title hits 1, a nonsense term 0.

## F-931-G1 — the guard's blind spots (MEASURED by the gate, verbatim)

`services/originate/src/__tests__/ks1061-shared-mock-completeness.test.ts` (blob `05fdfa88d` at M37) is a text scanner whose `ROOT_MOCK` / `VIA_HELPER` regexes match only a **single-quoted** `jest.mock(` and whose `testFiles()` is **non-recursive**, while jest's `testMatch` (`**/__tests__/**/*.test.ts`) is recursive and no lint rule pins quote style (no prettier config, no `quotes` rule in `eslint.config.mjs`). Proven at HEAD by the gate's quarantined probes: a double-quoted factory (T6b), a `jest.doMock` factory (T6c), or a factory in `__tests__/sub/` (T7) each ships a partial `secuura/shared` mock (scope sigil omitted) with the guard green, while the ordinary shape (T6a) is caught. Oracle: Purpose — the ticket's stated goal is "forgetting an export is no longer possible", and the helper file's own doc says "every `jest.mock('secuura/shared', …) (the scoped package name, sigil omitted here — 0 at-signs rule)`". Likelihood in operation: low (all 12 factories use the single-quoted top-level shape; the repo's convention is single quotes) — hence Minor.

**Fix-shape (the gate's, for the owner):** `ROOT_MOCK = /jest\.(mock|doMock)\(\s*['"]secuura\/shared['"]\s*,/g` and the same class in `VIA_HELPER`; walk the directory recursively (`fs.readdirSync(dir, { recursive: true })` on Node ≥ 20, filtering `.test.ts`). **Regression cells:** the T6b / T6c / T7 fixtures from the gate's `evidence/quarantine_zz-gate931-*.test.ts` as files the guard must name (red-first: each one green under the current guard; red under the widened one until it is named).

## F-931-G2 — indexed, not filed here (Record, no action per the gate)

`tsc --noEmit -p services/originate` is cited on PR #931 as evidence for a tests-only PR, but `originate/tsconfig.json` excludes `src/__tests__` and `src/**/*.test.ts` — `--listFilesOnly` shows 0 test files in that program, so the command type-checks none of the 14 files. The gap is covered in practice by ts-jest's per-file diagnostics (the gate demonstrated `TS2304` with `Tests: 0 total` on a broken file) and by the gate's inclusive pass (a temp tsconfig with `include: ["src/**/*"]`, 62 test files, rc 0; a planted `TS2322` fires). Worth one line in the READY template: "tsc excludes tests; ts-jest is the type gate for `__tests__`". **Home: KS-1000 (the class) / KS-1090 (originate + api-gateway instance)** — related from this ticket so the index reads both ways.

## Definition of done

One test pass (Kam's 2026-09-07 rule): the widened `ROOT_MOCK` / `VIA_HELPER` regex class + the recursive walk, with the three probe fixtures as named cells (red-first each), the existing 3 cells still green, whole originate green. G2 closes with KS-1000 / KS-1090.

**Related:** KS-1061 (#931, M37 — the guard's own ticket), KS-487 (the L3b review stream parent, #720), KS-1000 (G2's home). **Named, no relation (archived):** KS-1103 (the ks1103 fold), KS-764 (the ks764 fold), KS-862 (the stale-mock red that motivated the guard, Duplicate).

Filed by the merge seat s225 on 2026-09-14 after #931's squash (M37), before KS-1061's archive, so KS-1061's closing comment can name it.
