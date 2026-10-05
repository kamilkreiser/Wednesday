Raised from a Wednesday-held Spark pass, re-proved end to end by Seat B 60th. One ticket, one commit.

**Refs KS-1333**
https://linear.app/secuura/issue/KS-1333

## What this pins

`services/originate/src/services/anchorStateSync.ts` has four writers that persist
`blockHeight: anchor.blockNumber || 0` without shaping the value, and `anchor.blockNumber` comes
from `GET /api/anchors/:id`. The ticket's first step is to **measure** whether that route can hand
them a raw `pg` `int8` string. Measured at source, it cannot: `rowToAnchor` converts `block_number`
through `Number()` at `services/anchoring/src/index.ts:1317`, and the handler answers the mapped
`anchor.blockNumber || null`, never the raw row. So the ticket's own rule applies — a recorded
reason and a cell pinning it, not a coercion. This is that cell.

`index.ts` calls `app.listen` at import, so no test imports it. The guard therefore reads
`index.ts` as **source text** over the two lines that make the answer a number.

## Test Evidence

**Touched**
- `services/anchoring/src/__tests__/ks1333-get-by-id-blocknumber-is-a-number.test.ts` (new, +33/-0)
- `Projects Documents/API_Security_Functional_Testing_Architecture_Flow_Diagrams.html` (+68/-1)
- `Projects Documents/QA_Tool_Cheat_Sheet_Secuura_API_Testing.html` (+35/-2)

**Ran**
- `vitest` by named binary in `services/anchoring`, full suite, base and head:
  **354 → 357 tests, 353 → 356 passed, 1 failed at both ends, 0 new reds.** The single red is
  `threadTokenMint`'s emulator round-trip, which is KS 562 and pre-existing.
- The three new cells: 3/3 green, 104–135 ms reported (0.36–0.55 s wall) over three consecutive
  runs, 2026-10-05, host Kamil's Mac Studio (2), node v24.7.0.
- **Red-first, by tamper.** Removing `Number(...)` from `index.ts:1317` turns `RED KS-1333 B1` red
  with `expected [ true, false ] to deeply equal [ true, true ]`, while `C1` and `C2` stay green
  and all three cells still *run* — so the tamper is inert to loading, not a load failure read as a
  red. The tamper anchor was proved unique first; `index.ts` was restored by content and
  re-asserted by `sha256` (`31422a6ab3c74804…` both sides) with git reporting it clean.
- Strict apply at the base rc 0; tamper control (hunk header corrupted) rc 128 `corrupt patch`.
  The applied file is byte-identical to the held golden: 33/33 `+` lines equal, and a planted
  one-character mutation reads 1.
- `pathgate55` **PASS**: 6 assertions over 3 measured paths, 0 failed, its own must-hit controls
  firing. Firing control: the same head against another PR's declared set FAILS, naming both the
  missing and the extra paths.

**NOT run**
- No live sweep (skill §5f). Nothing here was exercised against a running service, so **KS-1333
  does not move to Done on this change's account**.
- No deploy, no migration, no Docker, no `az`, no stack of any kind.
- The guard is **source text**: it pins the text of two lines, so commenting those lines out would
  leave the cells green. Closing that properly needs `index.ts` to be loadable without listening,
  which is out of this scope.
- Whether `anchorStateSync`'s four writers should use `??` rather than `|| 0` stays **open on the
  ticket for a human** — that is a question about the value `0`, not about the shape pinned here.

**Migrations + config**
- None. No migration, no schema change, no environment variable, no dependency, lockfile, manifest
  or baseline edit.

## Skill §4 — both platform-k documents, same commit

A new self-contained block in each: flow `<h2>12.`, and the cheat sheet's own unnumbered
`div class="section"` convention after its KS 1404 block.

**Timing, stated rather than added.** Measured at the base SHA `3ce8cd4026a6`: **0** stated timings
name the anchoring suite in either document, against a must-hit control of **23** (flow) and **35**
(cheat sheet) duration figures present overall — so the zero is a measurement, not a blind grep.
This change amends no stated timing row; the figure in the block is its own.

## Two edits outside this change's own block

Both were owed before this seat and are carried here on a ruling, in documents only:

- In the **KS 1404** block of the cheat sheet, the cell count beside the vitest command now reads
  36 rather than 27. Re-counted at source first: 32 plain `it(` lines plus an `it.each` with 4
  rows. Proved by character diff — same line length, exactly two differing indices, with a
  three-character control reading 3.
- In the **KS 1015** block of both documents, the closing sentence now records that the sweep covers
  28 pairs, that two are owned, and that 26 remain. Exactly one replaced line per document,
  0 deletions, measured by a line-level diff.
