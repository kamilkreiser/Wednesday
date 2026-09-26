--- comment 5839058277 by linear[bot] at 2026-09-25T20:23:55Z
<!-- linear-linkback -->
<details>
<summary><a href="https://linear.app/secuura/issue/KS-1314/readyaml-routing-cells-a-multi-line-import-evades-parserimportsites">KS-1314 readYaml routing cells: a multi-line import evades parserImportSites (prettier produces it), the loaders are unpinned, and the canary pays a child spawn per run</a></summary>
<p>

## BLUF

Three non-blocking findings the tier-2 gate raised against PR #1243 (KS-1300 items 2-4, merged `a9ae94edbed3`). All three are cells in the same `readYaml` routing/canary family in `systemTest/performance`, so they are **one test pass** and one ticket, per Kam's 2026-09-07 rule.

`Refs KS-1300` — this does **not** close it. KS-1300's own remaining item (READYAML-UNGATED: no gate runs this suite) is a different workload — wiring a suite into the hook or the preflight — and is deliberately left there rather than folded in here.

## The three items

1. **MULTILINE-IMPORT.** `parserImportSites()` reads four import positions — static at any indent, re-export, `require()`, dynamic `import()` — but each pattern is anchored per LINE. **A multi-line import is invisible**, and that is not hypothetical: this package's own prettier config wraps a long import across lines, so the formatter itself produces the evading shape. Measured at the merged tree: the guard's own positive control passes every single-line spelling and has no multi-line row.
2. **T2C-ROUTING-HOME.** The routing cells prove the SUITE does not import a parser directly. Nothing proves the **loaders** (`runner/config_loader.ts` and friends) reach `readYaml()` — the property the whole family exists for. The gate recorded this as homeless; this is its home.
3. **CANARY-IN-PACKAGE.** The retained canary spawns a `tsx` child to run the raw parse, because importing the parser into the suite would (correctly) trip the routing cell. That costs \~2.5 s of the suite's wall-clock. A cheaper in-package form — for example a child-free comparison against a captured raw-parse error — would keep the standing witness without the spawn.

## Done when

- ☐ `parserImportSites()` sees a multi-line parser import, with a positive-control row carrying the exact shape prettier produces
- ☐ a cell proves the loaders call `readYaml()`, so the property is pinned where it is actually relied on
- ☐ the canary keeps its guarantee without a per-run child spawn, or a line records why the spawn is the cheapest honest form

## Board search before filing

Literal match over **1,303 issues (includeArchived) and 3,677 comments**, titles + descriptions + comments: `MULTILINE-IMPORT` -> 1 (KS-1300, this finding's own record) · `T2C-ROUTING-HOME` -> 1 (same) · `CANARY-IN-PACKAGE` -> 1 (same) · `parserImportSites` -> 1 (same) · `readYamlRouting` -> 1 (same) · `multi-line import` -> 1 (same) · `multiline import` -> **0**. **Searched those seven terms, 0 open hits outside KS-1300 itself.** Controls: `readYaml` fires; a nonsense token -> 0.

## Provenance

Tier-2 gate `QA/Secuura-batch1243`, raised **non-blocking** against #1243 and recorded at the merge. Filed on the coordinator's instruction after the batch landed; it did not hold the merge.

Refs KS-1300
</p>
</details>
<!-- linear-review-link -->
<p><a href="https://linear.app/secuura/review/ks-1314-a-prettier-wrapped-parser-import-evaded-the-routing-check-pin-682b7131d124">Review in Linear</a></p>

