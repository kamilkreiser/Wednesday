#1263 KS-1140: give the ks879 census figures their commits, or drop them (GF-3, R1)
head 3c33f936fe3985ab40b72b78bda15a6959448e18

## BLUF

**Comment-only.** KS-1140's remaining items, GF-3 and R1: the `ks879` docblock asserted a census — *"1,284 files, 12,758,153 bytes at `0f69129b3`"* — that was **stale when it was written** and is now ~11% out. It is no longer restated as current; each historical figure keeps the commit it was measured at, and the note says plainly that what the walk CONTROL asserts is the **floors**, not the census.

`Refs KS-1140`

## What changed

Two comment blocks in `Blockchain/Dev/packages/shared/src/__tests__/ks879-no-raw-control-bytes-repo-wide.test.ts`:

- the file docblock's census sentence (GF-3);
- the walk CONTROL's inline comment, which repeated the same figure as "1,284 files / 12.8 MB" (R1).

No executable line is touched. The floors `> 1_000` and `> 5_000_000` are **unchanged and unmoved**.

## The measurement that justifies dropping rather than restating

Three measurements, three values:

| files | bytes | commit | measured by |
|---|---|---|---|
| 1,284 | 12,758,153 | attributed here to `0f69129b3` | the figure this docblock asserted — and the gate found this byte total was the **HEAD** tree's, not that commit's (`0f69129b3` proper is 12,751,993 B). **GF-3.** |
| 1,288 | 12,823,398 | develop `e91eb5bda` + head | the tier-2 gate. **R1.** |
| **1,429** | **14,178,318** | **`4db87c3e4b98`** | this PR — see method below |

**+145 files and +1.4 MB against what the docblock asserted**, i.e. it was already ~11% stale. Restating it would reset a clock that ticks on every commit; the ticket offers dropping the figures explicitly, and that is what this does — while keeping each historical value attributed, because a **bare** number is what made the drift invisible.

**Method for the 1,429 row, stated so it can be re-run:** the prelude of the test file (lines 60–143, i.e. everything above `describe(`) was extracted verbatim to a copy **outside the repo**, with `describe(` asserted absent from the extract, and its own `sourceFiles`/`WALKED` run under `tsx` with `DEV_ROOT` at the worktree's `Blockchain/Dev`. So the number comes from **this file's own walk**, not a paraphrase of it. An independent re-implementation of the same `SKIP_DIRS`/`EXTS` walk in Python returned **1,429 / 14,178,318 — byte-identical**. Both were run with `node_modules` present and absent respectively, so the concurrent `npm ci` provably did not perturb the count.

## Test Evidence

**Touched**
- `Blockchain/Dev/packages/shared/src/__tests__/ks879-no-raw-control-bytes-repo-wide.test.ts` — comments only (31 changed lines, all comment lines).

**Ran**
- `packages/shared`: **941/941 bare → 941/941 patched**, 48 test files, `npx vitest run --no-file-parallelism` in worktree `s-l7-ks1140`, at develop `4db87c3e4b98`, load average **5.76** (bare) / **6.85** (patched), 38.6 s / 34.8 s. Baseline taken **before** the edit on a clean tree (0 uncommitted files).
- `npx tsc -p . --noEmit` → **rc 0**, 0 diagnostics.
- **Comment-only, proven two ways rather than asserted:**
  1. every one of the 31 changed lines in `git diff -U0` is a comment line — and the checker was **controlled** against a synthetic diff carrying `const sneaky = 1;`, which it flags;
  2. **AST-equivalence**: transpiled with `removeComments: true`, pre and post emit are byte-identical at **10,805 bytes**, 0 diagnostics. **Control:** changing `toBeGreaterThan(1_000)` → `(1_001)` reads `DIFFERENT` **at the same 10,805-byte emit size** and names the divergent line — the case a token-count instrument cannot see.
- **Push gate (this is a `Blockchain/Dev` push, so the 15-leg preflight ran):**
  `PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed.` — **legs 3, 4 and 8, local stack not up.** The preflight's own output says not to quote that as a pass, and this does not.
  Fleet STOP count, with `packages/shared` **built** in this worktree: `pre_push_hook_base` **28/0** · `fixture_guard` **6/0** · `run_shell_suites` **49/0** · shell suites **60 passed, 0 failed, 0 skipped (of 60)**. Read with a reader anchored on each suite's own `===` header and controlled against a suite whose count was already known.

**NOT run**
- **Legs 3, 4 and 8** of the preflight — the local stack is not up. Not started, per the standing verdict for test-only `packages/shared` changes.
- **No other package's suite.** The change cannot reach one: it is comment-only and the emit is byte-identical.
- **The census figure is not asserted by any test**, before or after. Nothing in this PR adds an assertion, so nothing here is pinned by a new cell — that is the point of the change, not a gap in it.
- **This does not close KS-1140's GF-1**, which was closed at #1235, nor GF-2/GF-4, closed at #1142.

**Migrations + config**
- **None.** No migration, no schema, no runtime config, no `package.json`, no lockfile, no Dockerfile, no route and no OpenAPI surface.

## Note for the reviewer

The `ks879` guard reads **every** source file under `Blockchain/Dev` by text. A merge from another lane during this round changes the census again — which is the behaviour this PR is documenting, not a problem with it. The floors are what hold.

