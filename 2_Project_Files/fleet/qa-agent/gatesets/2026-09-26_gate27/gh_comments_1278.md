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

--- comment 5842516204 by kksecura at 2026-09-26T02:48:25Z
## FIX ROUND 1 of 2 — B-1278-1, M-1278-a, P-1278-b. New head `18cca0a7e0fe1baddcd71cc26f8a10b032da9bd8`

Fast-forward on this branch; the author has wrapped, so this round is another seat's work and the
history before this commit stays its author's. **No merge-in** — the base this worktree **contains**
is the graded head `c321bcce2a9a`.

## B-1278-1 — and why the AST, not either cheaper repair
Round 1 read the **text**: four line-anchored patterns over a joiner that collapsed a wrapped
statement *"until one line carries the `;`"*. A **semicolon inside a comment** ended the join before
the `} from …` line, so the whole statement read as **no hit at all** — and a loader importing the
parser directly kept the cell green at 11/11.

The gate offered three shapes. **I measured the two cheaper ones before taking the third:**

| shape | S6b / S6d | wrapped re-export | wrapped `require(` | wrapped dynamic `import(` |
|---|---|---|---|---|
| round 1 (today) | ✗ missed | ✗ | ✗ | ✗ |
| end the join at `} from '…'` | **✗ still missed** | ✗ | ✗ | ✗ |
| strip comments before the `;` test | ✓ | ✓ | **✗ still missed** | **✗ still missed** |
| **the AST** | ✓ | ✓ | ✓ | ✓ |

- *"End the join at `} from '…'`"* **does not fix the blocking finding**: the join still breaks at the
  `;` in the comment **before** it reaches the `}` line.
- *"Strip comments"* fixes the two reported shapes, but the joiner only ever **opened** on a line
  starting with `import`/`export`, and the line pattern needed the specifier on that same line — so a
  wrapped `require(` or dynamic `import(` stays invisible under every text repair.

`parserImportSites` now asks the compiler: `ImportDeclaration`, `ExportDeclaration`, `require()` and
dynamic `import()` are four node shapes rather than four regexes, and a comment, a string, a wrap
point and a spelling stop being things to reason about. The reported unit is the **statement**, so the
positive-control rows keep their contract. `typescript` is already a dependency of this package.

**The text joiner is removed, not left unused** — a dead helper is a compile error here *and* a
reader's trap describing a rule the module no longer applies.

## M-1278-a — the pin now asserts the CALL
`src.includes('readYaml(')` is satisfied by a **doc comment**. The gate's A2c probe deleted the only
real call and the suite stayed green at 11/11 because two comments above it still spell it. It now
asserts a real `CallExpression`.

## P-1278-b — the figure carries its conditions
The comment claimed *"193 ms of the file's 220 ms"* with no conditions; the gate measured the same
cell at **2089 of 2116 ms under load ~18.7**. Both are now stated with their load, because the
**ratio** is the stable part and a bare number from a quiet box is not a measurement anyone can use.

## Test Evidence
Base this worktree **CONTAINS**: `c321bcce2a9a`.

| suite | result |
|---|---|
| `sheddingCeiling.test.ts` | **14 / 14** (was 11) |
| `systemTest/performance` unit, **BARE** at `c321bcce2a9a` | **63 files / 1106 tests / 0 failed** |
| `systemTest/performance` unit, **PATCHED** | **63 files / 1109 tests / 0 failed** |
| `tsc --noEmit` | **rc 0** |

**⚠ NO COUNT — and it is evidenced, not asserted.** This change is entirely under `systemTest/`, so the
hook takes its early return and runs **no preflight**. Measured in the push log: `pre_push_hook_base`,
`fixture_guard`, `run_shell_suites`, `shell suites:` and `PREFLIGHT` each occur **0 times**; the only
gate that ran was `[format-gate] systemTest/performance — format:check OK`. Control: **0 files outside
`systemTest/`** in this commit. The fleet quadruple is **not** quoted for this push.

**Red proofs — 3 arms, all behaved, zero LOADFAIL, each red set asserted EXACTLY:**

| arm | tamper | result |
|---|---|---|
| **textreader** | restore round 1's text reader | **RED — exactly the 3 new routing cells** |
| **a2c** | the gate's A2c plant (drop the only real `readYaml()` call, comments left) | **RED — exactly LOADERS** |
| **a2c_oldpin** | **the same plant WITH the old `includes()` pin** | **GREEN 14/14** |

**The third arm is the load-bearing one.** Without it, `a2c` only shows that a plant reds something.
The pair shows the **pin change** is what catches it — and it reproduces the gate's own A2c finding
exactly: same plant, old pin, still green.

## Fixtures captured, not typed
The two semicolon-in-braces shapes were produced by piping through **this package's own prettier** and
verified **idempotent** under it, so both pass the format gate and can really appear. After the format
gate rejected my first push and prettier re-quoted those literals, I re-checked that the fixture
**values** are still byte-identical to the captured files (with a control proving that comparison can
fail) — a re-quote must not silently become a re-capture.

## A refused push, fixed at the root
The first push was **refused by the format gate** (`1 failed`) and **the ref did not move**. Fixed by
running prettier on my own file only, then re-running `tsc`, the suite **and all three red arms**,
because a reflowed line can silently invalidate a tamper anchor. No `--no-verify`. The amend changed
the SHA; the push stayed pinned to origin's head, not mine.

## NOT covered
- The loader list is still hand-written with two entries (the gate's other half of M-1278-a): deriving
  it from the product files that read `.yml` is a wider change than this round.
- Legs 3, 4, 8 N/A — no `Blockchain/Dev` preflight runs for this path.
- No database, no deploy.

Refs KS-1314

