#1290 KS-1341 part B: route the PATCH, DELETE and rotate-secret 500s through fail500
head a53228515d25b6652b998de7279659df6b4e1c66

## BLUF

Three more of `routes/webhooks.ts`'s unconditional 500s now answer the constant body and log the thrown text server-side with the route named: **`PATCH /:id`, `DELETE /:id`, `POST /:id/rotate-secret`**. Two of those are the sites KS-1341 **measured** leaking under `NODE_ENV=production`; the third shares their shape.

`message: err.message` in this file goes **5 → 2**; `fail500(` goes **3 → 6** (one declaration, five calls). **Part C converts the last two (`:391`, `:416`) and is not in this change — the ticket stays open.**

**Origin, plainly: the patch was produced by the local model (`spark-dsv4flash`) under a Wednesday brief and re-verified by this seat.** It is raised **byte-identical** to the reviewed output — 226 lines, 10,663 bytes, sha256 `09ce3542d86b622806b48a1b7fd81b654314955cda8112944977361810f006d0`, `cmp` rc 0 against **both** the golden and the run's canonical patch. The harness's own figures are quoted as the harness's; everything under "Ran" is mine.

## This PR closes the gap part A's gate found

The part A gate measured **N-1288-2** (now **KS1344**): A1's "REACHED" assertion read `mockLoggerError.mock.calls.at(-1)` with no clear inside its four-environment loop, so a `fail500` that logged only under production would keep the cell green. **This cell does not have that gap** — `mockLoggerError.mockClear()` runs inside the loop and the assertion is over the **whole call list per environment**.

**I proved it rather than taking it on trust.** Arm R3: tamper `fail500` so it logs only under production (anchor proven unique, restored by content, restore verified by a whole-file sha256, an inert tamper refused outright). Result: **all three B1 rows red, B2 and all five controls green.** Under part A's shape that tamper would have passed.

## Test Evidence

**Environment these figures name:** worktree detached at develop `179a4f32ec0643689b55a8d7207e63f6ec3d3831`, which it **contains** (`merge-base --is-ancestor` asserted); `npm ci` at `Blockchain/Dev`; `packages/shared` **BUILT** (28 files in `dist/`). Runner: jest `--runInBand`.

**Touched:** `services/originate` — the router plus one new unit cell. Nothing else.

| check | result |
|---|---|
| strict apply at develop, per section | `git apply --check` rc 0 both; **control** (DELETE's anchor tampered) fails **1 of 3** hunks |
| RED, cell alone, product hunk absent | **6 failed / 5 passed / 11 total** — the six declared B1/B2 cells, each a `toEqual` **assertion** failure; all five controls green |
| GREEN, both files | **11 passed / 11** |
| **arm R3** (production-only logger) | **3 B1 rows red, B2 + controls green** — KS1344's weakness closed here |
| whole originate suite, BARE at develop | **81 suites, 951 tests, 0 failed** |
| whole originate suite, PATCHED | **82 suites, 962 tests, 0 failed** — `bare 951 / patched 962`, **0 new reds** by set difference on FAIL lines |
| `tsc --noEmit` | rc 0, 0 errors |
| type-check over a program that **contains** the new cell | rc 0, 0 errors (config extending `tsconfig.json` with `exclude: []`; `--listFilesOnly` shows the cell present and **87** `__tests__` files, where the bare run covers **0**) |
| `packages/shared` (`vitest run`) | **48 files, 945 tests, 0 failed** |
| `npm run lint` at develop / at this head | rc 0 both — **22 problems (0 errors, 22 warnings)** each; **14 files with problems at both**, and neither `webhooks.ts` nor the new cell among them; the two outputs are **byte-identical after normalising the worktree path** |

**`control KS-1341 B0` is the one to read.** It pins that a classified Postgres cast failure on `PATCH` still answers **400** and never reaches `fail500` — PATCH's catch classifies through `extractPgCode`, which reads `err.message` in `pgErrors.ts:70-72`. That cross-file path is real, it is why part B's fixture must not carry a classifiable code, and it is the behaviour a careless part-B cell would have broken.

**NOT run:** the local stack is not up, so nothing integration-level, no gateway, no Postgres, no container. Legs 3, 4 and 8 of the push preflight do not run without it. **Nothing deployed** — no local stack, no demo, no UAT.

**Migrations + config:** none. No migration, no `package.json`, no lockfile, nothing under `scripts/` or `.github/`.

## NOT COVERED

- **The last two sites (`:391`, `:416`) — part C.** This ticket stays In Progress.
- 🔴 **The helper's docblock still claims it is "the only place in this router that turns a caught error into a 500". Still false after part B: two `err.message` lines remain.** Unchanged here deliberately, to keep the diff byte-identical to the reviewed patch; it becomes true at part C.
- **KS1345** (the `GET /` swallow: a failed list query answering `200 []`) is untouched by this PR, and its pin `control KS-1341 A0` still asserts today's behaviour.
- **KS1344** itself — this PR shows the *new* cell does not have the gap; it does not retrofit the fix into part A's cell, which is what that ticket covers.
- An instrument note, because it nearly went into this body wrong: my first lint/type-check greps matched `ks1341b` and returned 14 and 622 — **the worktree is named `s-b31-ks1341b`, so every absolute path contains that substring.** The figures above were re-measured against the cell's real filename, with the loose pattern shown returning 14 on the *develop* run too, which predates the cell.

Refs KS-1341

## The push gate, as it ran on this head

`a53228515d25` pushed under `.push-lock-27` — taken 08:36:17Z, released 08:42:47Z by me; push rc **0**.

**`pre_push_hook_base` 28/0 · `pre_push_hook_base_fixture_guard` 6/0 · `run_shell_suites` 49/0 · shell suites 60 passed, 0 failed, 0 skipped (of 60)** — the fleet condition, met. **0** lines starting `FIXTURE BUILD FAILED`. `PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed.` — legs 3, 4, 8 **NOT run** (local stack not up). Counts parsed per suite block; the three prefix-sharing suites resolve distinctly as 28/0, 6/0 and 4/0.

