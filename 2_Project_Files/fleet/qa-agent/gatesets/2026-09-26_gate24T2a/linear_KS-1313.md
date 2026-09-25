KS-1313 KS-1226 residue: readSuiteCounts is null on real fail-only, skip-only and todo-only lines
state In Progress

Residue from the tier-2 review of PR #1241 (round 2 of 2, **NO GO at the cap** — gate report sha256 `b6b2c0f1ae210d92`). **#1241 is the unmerged attempt; KS-1226 is the parent.** Nothing from that attempt shipped.

## The defect

`readSuiteCounts` requires a `passed` segment, so it returns **null** on every real summary that has none. Captured verbatim from vitest 4.1.11, `--reporter=default`, piped:

```
      Tests  1 failed (1)      -> null   (correct: { passed: 0, failed: 1 })
      Tests  1 skipped (1)     -> null   (correct: { passed: 0, failed: 0 })
      Tests  1 todo (1)        -> null   (correct: { passed: 0, failed: 0 })
```

**Cost.** `childSuiteCounts` throws `could not read the child vitest summary` with the output tail. Loud, but it misattributes a zero-pass child as a parser defect — and a child where everything failed is exactly the case the reading must survive.

## Root cause

vitest renders the **final** summary with `getStateString` in `dist/chunks/utils.BS4fH3nR.js`, where `passed` is **conditional**:

```js
passed ? c.bold(c.green(`${passed} passed`)) : null,
```

There is a **second** `getStateString`, in `dist/chunks/index.UpGiHP7g.js`, belonging to the TTY-only live reporter, where `passed` is unconditional. The round-2 head comment quotes that one, and the "passed is always emitted" premise — and the refusal built on it — came from reading the wrong renderer.

## Also in this residue

* `tsc -p tsconfig.node.json` is **red at head**: `TS2532` at :79 and `TS2345` at :86, so `npm run lint` exits 2. `npm run lint` runs **both** tsconfigs; only `tsconfig.json` was run, and it is clean.
* The call site (:157 / :161) is **unpinned** — no cell reds if it stops calling `readSuiteCounts`.
* First-match reads an earlier `Tests  N passed (N)` console line as the summary: a silent `{5,0}` on a run that had 1 failure.

## Fix shape

Name-read with an **allowed-label set** and a **sum-equals-total** check instead of "require passed". Take the **last** `Tests` line, not the first. Narrow the indexed accesses so the stricter tsconfig passes. Correct the doc comment, C5's title, and the :156 citations.

## Regression cells

The three lines above to `{0,1}`, `{0,0}`, `{0,0}`. `      Tests  2 failed | 3 passed (5)` to `{3,2}`. A sum-not-equal-total line to null. The two-line output (an earlier `Tests  5 passed (5)`, then `      Tests  1 failed | 1 passed (2)`) to `{1,1}`. One cell that **reds when :157 stops calling** `readSuiteCounts` — for example by exposing the spawn result to a pure `readChildOutput(output)` that `childSuiteCounts` calls and a cell calls with real captured fail-only output. `tsc -p tsconfig.node.json --noEmit` rc 0.

Refs KS-1226
