#1278 KS-1314: a prettier-wrapped parser import evaded the routing check; pin the loaders; record the canary spawn
head 18cca0a7e0fe1baddcd71cc26f8a10b032da9bd8

## BLUF

Test-only, two files. **A parser import that prettier has wrapped evaded the routing check entirely** — and the fixture proving it is *captured from this package's own prettier*, because my first attempt at writing one by hand didn't wrap at all. Plus a cell pinning the product loaders, and the canary's spawn recorded with its measured cost.

`Refs KS-1314`

> **Base:** branched from `4db87c3e4b98`. This is a `systemTest/` path, so **no preflight ran** and **no fleet STOP count was executed or is quoted**.

## Item 1 — a wrapped import hides the specifier from every line-anchored pattern

`parserImportSites()` matches line by line. When prettier wraps a statement the first line is `import {` and the module name only appears on the **last** line, `} from '<parser>';`. No pattern sees it.

**Measured before the fix:** `parserImportSites(PRETTIER_WRAPPED_IMPORT)` → `[]`, while the **identical single-line import was caught**.

**The fixture is captured, not typed**, and this mattered: my first candidate was a 99-character import, and **prettier left it on one line** — `printWidth` here is 120. A hand-written "wrapped import" can be wrapped at the wrong column and pin a shape prettier never emits. The real shape came from `npx prettier --stdin-filepath` on a 136-character import: 12 lines, `tabWidth: 4`.

Multi-line `import`/`export` statements are now collapsed onto one logical line before matching, **bounded at 40 lines** so an unterminated statement cannot swallow the file.

**Controls in the cell:** a wrapped import of *something else* is not a hit; an unterminated statement yields at most one.

## Item 2 — nothing pinned the thing the property is about

The routing cells read only **this suite's own source**. The suite could be perfectly routed while `runner/config_loader.ts` parsed the file itself. A new cell pins that every product loader calls `readYaml()` and imports no parser.

**Its control is the load-bearing part:** `utils/yaml.ts` is asserted to be the **one** module that *does* import the parser. If that ever reads `[]`, the instrument has stopped seeing real imports and every other assertion in the cell is vacuous.

## Item 3 — the spawn stays, recorded with its cost

**Measured: 193 ms of the file's 220 ms.** Each alternative is worse:

- **import the parser in-process** — it would (correctly) trip the routing cell, so the only way is a computed specifier: deliberately evading this suite's own guard in order to test it;
- **capture the raw error once as a fixture** — it stops being a live witness the moment js-yaml changes its message, which is exactly how the original canary was lost;
- **drop the raw half** — the claim is comparative ("the raw parser prints the file, `readYaml` does not"), and half a comparison proves nothing.

193 ms is the cheapest honest form, and the file now says so rather than leaving it to be re-litigated.

## Red-proof, re-run against the FINAL bytes

The first pass predated prettier reformatting both files, so it was re-run rather than quoted from a draft.

| arm | result |
|---|---|
| collapse removed | the **wrapped-import cell reds, alone** |
| a loader imports `js-yaml` | the **loaders cell reds** |
| a loader drops `readYaml()` | the **loaders cell reds** |
| restored | **0 red** |

`runner/config_loader.ts` restored **byte-identical** after each arm.

## Test Evidence

**Touched**
- `tests/unit/support/readYamlRouting.ts` — the collapse, and `PRETTIER_WRAPPED_IMPORT`.
- `tests/unit/config/sheddingCeiling.test.ts` — two new cells, and the canary's recorded rationale.

**No product file is in this PR.**

**Ran**
- `npm run test:unit` in `s-l7-ks1314/systemTest/performance`, at base `4db87c3e4b98`: **1104/1104 bare → 1106/1106 patched**, 63 files, **+2 = exactly these cells**. Load **9.01** bare / **7.65** patched.
- `npm run lint` → **rc 0** (both tsconfigs and eslint). It caught three things I had not: two prettier wraps and a missing `curly` brace.
- All four red-proof arms above.
- Push: **12 s**, `[format-gate] 1 package(s) checked, 0 skipped, 0 failed`.

**NOT run**
- **No preflight, no fleet STOP count** — `systemTest/` path.
- **KS-1300 item 1 (READYAML-UNGATED) is deliberately out of scope**: wiring this suite into a gate touches the push gate, which is not in this lane. So these cells are still executed only by hand.
- **The collapse is text-level, not a parser.** A parser import assembled from a computed string still evades it, as does one reached through a helper in another module.
- The canary's 193 ms is measured on this box at this load; it is a cost, not a budget.

**Migrations + config**
- **None.**

