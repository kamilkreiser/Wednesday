#1241 KS-1226 SKIPPEDSUMMARY: the child-summary regex accepts an optional skipped segment
head e2d0518df40228f0a183bc4223c7a6840821253e

## BLUF

`childSuiteCounts()` (`:87-104`) runs a child vitest and reads its summary with a regex that had no place for a **skipped** segment. vitest prints one between `failed` and `passed` whenever anything is skipped — `Tests  1 failed | 1 skipped | 243 passed (245)` — so the regex returned `null` and the consumer threw *"could not read the child vitest summary"* instead of reporting counts that were sitting in the line it had just read.

**Item 2 (F5) only.** Item 1 — the 15 s budget at `:127` (F4) — is a decision about how to size a spawning matrix and is deliberately untouched.

## The one design point worth reviewing

**The skipped segment is non-capturing, and that is the whole risk of this change.** A capturing group there would push `passed` to group 3 while `:103` still reads `summary[2]` and `summary[1]` — the counts would then be **silently wrong** rather than absent, which is strictly worse than the defect being fixed. The regex still has **exactly three** groups: failed (1), passed (2), total (3). `:103` is unchanged.

Measured on the shipped literal after the change:

| input | groups |
|---|---|
| `Tests  1 failed \| 1 skipped \| 243 passed (245)` | `('1', '243', '245')` |
| `Tests  2 skipped \| 243 passed (245)` | `(None, '243', '245')` |
| `Tests  2 failed \| 243 passed (245)` | `('2', '243', '245')` |
| `Tests  245 passed` | `NULL` (still, by design) |

## How the new cells reach the regex

They do **not** call `childSuiteCounts()` — that spawns child processes. They read the regex **literal out of this file's own source** and run it on fixed strings, so they grade the shipped regex in milliseconds and keep grading it if someone edits the literal later. No new imports; `readFileSync` and `SELF` were already in scope.

## Test Evidence

**Touched:** `systemTest/performance/tests/unit/utils/unitSuiteSlotIndependence.test.ts` only (1 file, +47 / -1). This file is both the product (the regex) and the suite that grades it.

**Ran** — `vitest run --config vitest.unit.config.ts`, vitest 4.1.11:
- **Red proof, in two steps, so the red names its own cause.** With **hunk 2 alone** (the cells, no fix) at the tip: **2 failed / 6 passed (8)**. R1 and R2 fail **by assertion** — `AssertionError: expected null to deeply equal { passed: 243, failed: 1 }`. The `null` *is* the defect. C0, C1 and C2 pass on both trees.
- With **both hunks**: **8 passed (8)**.
- **Whole package, both sides, measured not inferred:** base **1085 passed (1085)**, 63 files → head **1090 passed (1090)**, 63 files. Delta **+5**, exactly the five new cells. The base figure was taken by restoring the file's base content in place and running; the restore was verified **byte-identical by blob hash** (`d9f45be175d2`) before committing.
- **Capture-group count asserted as a build-time check**, not observed by eye: the patch builder compiles both regex bodies and refuses unless the new one has exactly 3 groups and `passed` is group 2.

**NOT run:**
- **No platform preflight.** This change touches **zero** `Blockchain/Dev` files, so the pre-push hook took its documented `[ -z "$changed" ] && exit 0` early return. The only gate that ran was the KS-989 format gate: `[format-gate] systemTest/performance — format:check OK` / `1 package(s) checked, 0 skipped, 0 failed`. **That is a 9-second push and it is not a platform preflight — it is not offered as one.** The evidence above is the suites I ran directly.
- **No real child vitest run whose summary actually contains `skipped`.** The cells use fixed strings from the gate's probe table. A live child emitting a skipped segment was not produced.
- **`todo` and other segments are not covered.** vitest can print other markers; only `skipped` was specified and only `skipped` is handled. A `todo` segment would still return `null`.

**Migrations + config:** none. No `package.json`, no `package-lock.json`, no schema, no environment variable.

Refs KS-1226

---
*Raised on Wednesday's brief, tier 2. Base `aa600af94d69`.*

🤖 Generated with [Claude Code](https://claude.com/claude-code)
