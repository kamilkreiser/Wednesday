#1277 KS-1319: the wiring check survives a comment-out, the derivation misses nested and async walkers
head 702171eaadbeb0a9d830237ec6fd86219311477c

## BLUF

Test-only, one file. **The wiring check could be satisfied by a commented-out line** — that is item 1, and the proof that matters is the second arm: under the same tamper, the old check stays **fully green**. Item 2 widens the derivation and proves the new coverage on a fixture, because neither shape exists in this package yet. Item 3 is **recorded as accepted**, not resolved, with the measurement.

`Refs KS-1319`

> **Base:** branched from `4db87c3e4b98`; develop is now `d7cdecf1d2ee`, which this worktree does not contain. The STOP counts below describe that base plus this change.

## Item 1 — a `//` does not remove a string

The cell read the config's **source text**: `expect(config).toContain('setupFiles')`. Comment the setting out and the strings are still there, so unhooking the budget left the cell green. The config is now **imported** and its resolved `test.setupFiles` read, which no comment can fake.

| arm | result |
|---|---|
| `setupFiles` commented out, **my check** | the wiring cell **REDS** |
| `setupFiles` commented out, **the old check alone** | **7/7 fully green** |

**My first version of that second arm was worthless** — I left my own assertions in the cell beside the old ones, so it reddened either way and proved nothing about the old check. Re-run with the old substring check in isolation; that is the row above.

## Item 2 — nested and async walkers were invisible, and the fix had to be provable

The derivation was `readdirSync(TESTS_DIR)` — one level — with three synchronous markers. It is now recursive and carries async markers.

**Measured before building, and it changed the shape of the work:**
- recursion finds **nothing new** today — `support/` is the only sub-directory and holds no walker;
- the async markers match **nothing** — **zero** files under `src/__tests__` use `readdir(`, `opendir`, `fs.promises`, `node:fs/promises`, `glob(` or `globSync`.

So neither could be proven against the real corpus. **A marker that has never matched anything is a marker nobody has shown to work.** The coverage is therefore proved on a **fixture tree** — a nested sync walker, a top-level async one, and a non-walker — where the derivation must return exactly the two walkers. Removing the recursion reds that cell **and only that cell**.

A second new cell **names what is still not covered**, with the first of the three pinned on a fixture:

1. a walk reached through a **helper in another module** — not seen (pinned);
2. a walk built from a **computed string** — not seen;
3. a marker appearing only inside a **comment** — over-reports, which is the safe direction.

Closing (1) and (2) means parsing, which is a larger change than a timeout list justifies.

## Item 3 — TS1343 recorded as accepted

`import.meta.url` at `:27` is TS1343 under the package's own commonjs program. **It is not this file's problem:** 9 TS1343 across the package, 4 of them in `ks256-spec-example-contract.test.ts`, 1 here. It is invisible to `tsc -p .` for the same reason as everything on **KS-1329** — `tsconfig.json` excludes `src/__tests__` — and "fixing" it here alone would mean dropping `import.meta` in one file while eight others keep it. Carried on KS-1329.

## Test Evidence

**Touched**
- `packages/shared/src/__tests__/walkTimeouts.test.ts` — the wiring cell, the derivation, and two new cells.

**Ran**
- `packages/shared`: **941/941 bare → 943/943 patched**, 48 files, **+2 = the fixture cell and the disclosed-limits cell**. `npx vitest run --no-file-parallelism` in `s-l7-ks1319`, at base `4db87c3e4b98`, load **8.50** bare / **9.44** patched.
- **Zero `Test timed out in 5000ms`** in the run; `walkTimeouts` re-run **solo** afterwards at load 7.59, green — per this ticket's own rule about reading a timeout as a load class.
- `npx tsc -p . --noEmit` rc 0; `npm run build` rc 0.
- Both red-proof arms above; config and test file restored **byte-identical** after each.
- **Push gate:** `PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed.` (legs 3, 4, 8 — local stack not up; not quoted as a pass). STOP count with `packages/shared` built: `pre_push_hook_base` **28/0** · `fixture_guard` **6/0** · `run_shell_suites` **49/0** · shell suites **60 of 60**.

**NOT run**
- Legs 3, 4, 8.
- **The end-to-end budget proof is not a standing cell** — a 6 s cell would be paid on every run forever. The wiring is pinned by the imported config instead, which is the honest scope of what a test here can assert about its own runner.
- **The async markers are not exercised by any real suite** — by construction, since none exists. The fixture is what proves them.
- **TS1343 is not resolved**, and the three named blind spots are not closed.
- Nothing outside `src/__tests__/walkTimeouts.test.ts` is touched; `vitest.config.ts` is read, never modified.

**Migrations + config**
- **None.**

