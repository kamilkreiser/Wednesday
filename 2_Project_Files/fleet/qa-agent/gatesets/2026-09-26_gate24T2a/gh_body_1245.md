#1245 KS-1313 SUMMARYREAD: read the child vitest summary by label set and sum, not by requiring passed
head 1700b5ae7dd56ad3e30602a40b20ae6469c35350

## What this changes

`childSuiteCounts` parsed the child vitest summary with one regex that **required a `passed` segment** and
took the **first** match. vitest 4.1.11 renders the final summary with `getStateString` in
`node_modules/vitest/dist/chunks/utils.BS4fH3nR.js`, where **every** segment is `n ? … : null` — `passed`
included. There is a second `getStateString`, in `dist/chunks/index.UpGiHP7g.js`, belonging to the TTY-only
live reporter, where `passed` is unconditional; that one does not render this line.

`readSuiteCounts(output)` is now pure and exported. It takes the **last** `Tests` line, reads each segment
against a **closed label set**, rejects a repeated label, and requires the segments to **sum to the total**.
Anything it will not vouch for returns `null`, and the caller still throws loudly with the output tail.

## Captured first, then built

Every fixture is real output from vitest 4.1.11, `--reporter=default`, piped, from throwaway projects
**outside this package** (archived at `5_Project_History/2026-09-25_seatL6/evidence/vitest-capture/`):

```
      Tests  1 failed (1)
      Tests  1 skipped (1)
      Tests  1 todo (1)
      Tests  1 expected fail (1)
      Tests  1 passed (1)
      Tests  3 failed (3)
      Tests  1 failed | 2 passed | 1 skipped | 1 todo (5)
      Tests  2 failed | 2 passed | 1 expected fail | 2 skipped | 1 todo (8)
      Tests  no tests
```

**Two facts neither the ticket nor the earlier attempt carries**, read at source and confirmed by capture:

1. **`expected fail` is a two-word label.** A segment parser that reads a label as one word breaks on it.
2. **The renderer excludes `expected fail` from `passed`**, so
   `failed + passed + expected fail + skipped + todo === total`. That is what makes the sum check a real
   check rather than a restatement — and the `(8)` row above proves it on real output.

**Shapes deliberately excluded, and why:** a TTY run (the caller pipes, and ANSI is stripped
unconditionally, so the difference cannot reach the parse); a reporter other than `default` (the caller
passes `--reporter=default` explicitly); a vitest other than 4.1.11 (the label set is read from *this*
version's renderer, and an unknown label is exactly what returns `null` rather than a guess).

## Test Evidence

**Touched:** `systemTest/performance/tests/unit/utils/unitSuiteSlotIndependence.test.ts`. One file.

**Ran** (all by the author, on this head; node v24.7.0, vitest 4.1.11):

- `npm run test:unit` — **63 files / 1107 passed / 0 failed**, rc 0. Base at develop `6e2a00bfe` in this
  worktree before any edit: **63 / 1089 / 0**. +18 cells, no pre-existing red on either side.
- `npm run lint` — rc 0, **both** tsconfigs plus eslint.
- `npm run format:check` — rc 0.
- **Measured, and it is the reason the earlier attempt's TS errors went unseen:**
  `tsc -p tsconfig.node.json --noEmit --listFilesOnly` includes this file (**1** hit);
  `tsc -p tsconfig.json --noEmit --listFilesOnly` does **not** (**0** hits) — `tsconfig.json` excludes
  `tests`. So this file is type-checked **only** by the stricter config, which has
  `noUncheckedIndexedAccess` and `exactOptionalPropertyTypes`. Running `tsconfig.json` alone type-checks
  none of it.
- **Tamper matrix, one arm per conjunct** (`tamper1313.sh`; restores sha256-asserted, never `git checkout`):

| arm | what it flips | reds |
|---|---|---|
| T-1 | require a `passed` segment (the defect itself) | fail-only, skip-only, todo-only, expected-fail, all-failed — **5** |
| T-2 | take the first `Tests` line | the two-line cell — **only that one** |
| T-3 | drop the sum-equals-total check | the sum rows — **2** |
| T-4 | open the label set | the unknown-label row — **only that one** |
| T-5 | allow a repeated label | the repeat row — **only that one** |
| T-6 | call site stops going through `readSuiteCounts` | the call-site pin — **only that one** |

**T-5 initially reddened nothing**, and that is recorded in the code. With duplicates allowed the Map simply
overwrites, so `1 passed | 1 passed (2)` sums to 1 against a total of 2 and the **sum** check rejected it
anyway — the duplicate check was not load-bearing and a later edit could have dropped it in silence. The row
`2 passed | 1 passed (1)` is the shape where it *is* load-bearing (the overwrite makes the sum reach the
total), and T-5 reds on it now. A tamper that finds nothing is a statement about the corpus, not the product.

**The real call site is exercised**: the pre-existing slot matrix cell runs `childSuiteCounts` against real
child vitest runs, so `readSuiteCounts` is reached through the spawn path, not only through the fixtures.

**NOT run / NOT covered:**

- **#1241 is untouched** — not pushed to, not commented on, not closed. This is a separate branch from
  `develop`. **If #1241 is ever revived, it rebases onto this one, never the reverse**; whichever merged
  second would otherwise silently revert the other.
- This PR also delivers **ks1226 item 2**, because develop still carries the original regex — nothing from
  the earlier attempt at that ticket ever shipped. Verified at `6e2a00bfe`: `readSuiteCounts` appears **0**
  times anywhere under `systemTest/performance`.
- The ticket asks to correct "C5's title" and "the `:156` citations". Those are artefacts of the earlier
  attempt and **do not exist on develop**, so there is nothing to correct; this is a fresh implementation.
- `npm run knip` and `npm audit` not run (audit reaches the network).
- No environment, no docker, no k6. **Nothing deployed.**

**Which gate ran:** repo-root `systemTest/` change, so `.githooks/pre-push` did **not** run its 15-leg
preflight (it gates on `^Blockchain/Dev/`). The push took 9 s and printed only
`[format-gate] 1 package(s) checked, 0 skipped, 0 failed`. The fleet STOP count was **not executed** on this
branch and nothing here quotes it.

**Migrations + config:** none.

Refs KS-1313

