#1289 KS-1318: assert the ks781 combined default-shapes control by tag set, not by count
head 1e24633b9c196c5d3dd5bb83519bce860ca79758

## BLUF

The J2 **combined** default-shapes control in `ks781-p3-3-body-parser-order.test.ts` asserted `toHaveLength(3)` — the **count** of shapes `defaultShapesOf()` found, not **which** shapes. So it was green under any permutation of the walk, and under any relabelling that kept the cardinality, **including the two shapes the fixture exists to tell apart being detected under one another's name** — the ticket's own words. It now asserts the set of tags in source order with `toEqual`.

**One hunk, one file, +10 / −1.** Test-only: no product byte changes.

## Why this is a new PR, and what it is NOT

This hunk was first raised inside **#1268**, which carries it *and* KS1316's two hunks. #1268 failed at the two-NO-GO cap on KS1316's guard-reachability rule, so it ships nothing and stays open — **this PR does not touch it: no push to it, no close** (its disposition is not a seat's call). **#1287** carried KS1142's `entrypoint-corpus.test.ts` alone and the gate correctly amended its squash to name KS1142 alone. **So nothing of KS-1318 has merged**; on develop the cell still reads `toHaveLength(3)`.

**Nothing of KS1316 is in this PR**, and that is measured rather than asserted: a KS1316-only token (`W9`) appears **0×** in this PR's diff and **7×** in the full three-hunk diff, so the check can see the thing it reports absent. This PR's diff carries **1 hunk**; the develop→#1268 diff carries 3.

The file's blob is `e96215365a6d` at **both** #1268's merge base (`4db87c3e4b98`) and develop, so the hunk's pre-image is unchanged and it applied to develop strictly — `patch -F0` / `git apply --check` rc 0, with a control (the anchor line tampered) failing 1 of 1 hunks.

## Test Evidence

**Environment these figures name:** worktree detached at develop `e080174c86c671349c508560744644fc0ef33388`, which it **contains** (`merge-base --is-ancestor` asserted); `npm ci` at `Blockchain/Dev`; `packages/shared` **BUILT** (`npm run build`, 28 files in `dist/`). Runner: vitest.

**Touched:** `packages/shared` — one assertion in one existing test cell. No product file. No other package.

**Ran — two arms, each at BOTH trees, each red set asserted EXACTLY (not "contains"):**

| arm | at develop (`toHaveLength(3)`) | at this head (`toEqual([…])`) |
|---|---|---|
| **A — permutation:** `return shapes;` → `return shapes.reverse();` | **0 red, file 242/242 green** — the blindness this ticket reports | **1 red: the combined cell ALONE**; all three per-shape rows green |
| **B — relabel, cardinality preserved:** the default-function and alias branches swap their `shapes.push` labels | **2 red: the two per-shape rows only; the combined cell stays GREEN** | **3 red: the two rows AND the combined cell** |

Arm A proves the new assertion is **necessary**; arm B proves it does **not over-fire** (the per-shape rows behave identically at both trees — only the combined cell changes). **Both arms matched a red set predicted before the run, 2/2 at each tree.**

Every tamper: anchor uniqueness asserted **before** the edit (`count == 1`; `return shapes;` occurs exactly once, at `:4927` inside `defaultShapesOf` at `:4906`), restored **by content**, and the restore verified by a **sha256 of the whole file**. `git checkout` was not used — it reverts more than the tamper if anything else in the tree moved. The runner also refuses a 0-cell result as a load failure rather than a pass.

| suite / check | tip | this head |
|---|---|---|
| `ks781-p3-3-body-parser-order.test.ts` | **242 passed** | **242 passed** |
| whole `packages/shared` (`vitest run`) | **48 files, 945 tests, 0 failed** | **48 files, 945 tests, 0 failed** |
| `tsc -p . --noEmit` | rc 0, **0 errors** | rc 0, **0 errors** |
| `npm run lint` (`eslint src`) | rc 1 — **36 problems (1 error, 35 warnings)** | rc 1 — **36 problems (1 error, 35 warnings)** |

The cell count does not move because this edits an assertion inside an existing cell rather than adding one.

🔴 **The lint run is red at BOTH trees, and it is pre-existing, not introduced here.** The single error is `no-control-regex` on the KS703 control-byte guard at `src/middleware/index.ts:539` — a rule firing on code whose purpose is to match control bytes. It is already on the backlog (`BACKLOG.md:876`, which records it at `:521` with 31 warnings; the line has since moved to `:539` and the warnings to 35 — a count names the tree it was measured on). **The two lint outputs are byte-identical after normalising the worktree path**, and `ks781` is mentioned in neither, so this change is provably lint-neutral. The tip figure is taken from a second worktree in which this file is at develop's blob (`e96215365a6d`, asserted) with `packages/shared` clean.

**NOT run:** the local stack is not up, so nothing integration-level, no gateway, no Postgres, no container. Legs 3, 4 and 8 of the push preflight do not run without it. Nothing deployed — no local stack, no demo, no UAT.

**Migrations + config:** none. No migration, no `package.json`, no lockfile, nothing under `scripts/` or `.github/`.

## NOT COVERED

- **KS1316's two hunks** (the walk and cells W9–W13) — not in this PR, and `#1268`'s cap and disposition are not addressed here.
- Whether `defaultShapesOf`'s **walk** is correct — this change pins what the combined cell *asserts*, not the walker. The walker's correctness at this tree is what the per-shape rows and KS1144's own cells cover.
- A third arm (e.g. a branch made to fire twice) was not written; arms A and B already separate necessity from over-firing.
- Nothing integration-level, and nothing deployed.

Refs KS-1318

## The push gate, as it ran on this head

`1e24633b9c19` pushed under `.push-lock-27`, taken 06:30:10Z and released 06:36:58Z by me; push rc **0**.

**`pre_push_hook_base` 28/0 · `pre_push_hook_base_fixture_guard` 6/0 · `run_shell_suites` 49/0 · shell suites 60 passed, 0 failed, 0 skipped (of 60)** — the fleet condition, met. **0** lines starting `FIXTURE BUILD FAILED`. `PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed.` — legs 3, 4, 8 **NOT run** (local stack not up). Counts parsed per suite block by exact basename; the three prefix-sharing suites resolve distinctly as 28/0, 6/0 and 4/0, so an under-read (which would look like a missing gate) is excluded.

