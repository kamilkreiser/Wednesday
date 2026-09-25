#1223 KS-1118: pin documentHash over hash, and narrow the product comment that overclaimed
head 759726d8d046e6098e720d4768c87e114d0c363c

## BLUF

Two gaps left by #965, neither a product defect. **F-2:** the alias chain `providedHash || contentHash || documentHash || hash` was pinned at two positions out of three — moving `hash` to THIRD left the whole originate suite green. **F-3a:** the product comment still claimed *"every body that worked before keeps its answer"*, which the gate measured wrong. #1170 fixed the **test header** and left the product comment alone.

## F-2 — the missing cell, with its red-proof

A `P3` cell sends `{documentHash:A, hash:B}` with no rows and asserts **200, exactly one lookup, the lookup saw A and never B**.

**Ran and built, not predicted:**

| | result |
|---|---|
| at head, with the cell | **15 passed / 15**, rc 0 |
| with T5 planted (`hash` moved to third) | **1 failed / 14 passed / 15**, rc 1 |

The single failure is **P3 and nothing else** — the file's other 14 cells stay green under the tamper, which is exactly the gap. The product file was restored afterwards and proved **byte-identical by sha256** (`a45689f7…`); the worktree's porcelain read 2, the two files this PR touches.

## F-3a — narrowing the product comment

`routes/verification.ts` now says what the gate measured: a body pairing `hash` with `documentId` or `documentData` takes the hash strategy where it used to take the id or data one; `documentId`-only, `documentData`-only and alias-only bodies are unchanged; no caller in the repo sends that pairing.

**Correction to the round record:** the brief attributes part of this to *"#1136?"*. The test file's whole history at this base is `0dcd81d5d` (#965), `54e9b835d` (#931), `d03a5f6f4` (#1170). There is no #1136 in it.

## Test Evidence

* **Touched:** `src/__tests__/ks1103-verify-hash-field.test.ts` (+1 cell), `src/routes/verification.ts` (comment only).
* **Ran:** originate `jest --runInBand` → **74 suites / 864 tests, rc 0**. Bare serial baseline at this base is **74 / 863**, so this is **bare 863 / patched 864** — the one cell added, nothing else moved. `tsc --noEmit` rc 0. `packages/shared` `vitest run` → **46 files / 918 tests, rc 0**.
* **NOT run:** the v2 route is untouched and its own pin (`ks1133-v2-verify-hash-read-first`) was not exercised beyond its place in the full suite above. The integration config was not run (needs a live Postgres; this file is not in it). No image rebuilt — no runtime surface. The T5 tamper proves the cell bites; it does **not** prove the other two alias positions are pinned against every rearrangement, only against this one.
* **Migrations + config:** none.

Refs KS-1118

🤖 Generated with [Claude Code](https://claude.com/claude-code)

