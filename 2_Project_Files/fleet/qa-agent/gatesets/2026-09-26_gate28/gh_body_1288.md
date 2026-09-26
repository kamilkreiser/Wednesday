#1288 KS-1341 part A: route the webhooks GET / and POST / 500s through a fail500 helper
head cb58d3a59c8921a3a1caede3c6acfb4b599bf959

## BLUF

`routes/webhooks.ts` answered **500 with the thrown error's own text on seven unconditional sites, with no `NODE_ENV` guard**, so internal detail reached the client in every environment including production. **This is part A of 3:** it adds the file's `fail500` helper and converts the first two sites (`GET /` and `POST /`). **Parts B and C convert the remaining five and are NOT in this change** — the ticket stays In Progress after this merges.

Same helper shape already merged three times for this family under KS730 (`routes/gdpr.ts`, `routes/systemErrors.ts`): log the thrown text server-side with the route named, answer a constant body.

**Origin, stated plainly: the patch was produced by the local model (`spark-dsv4flash`) under a Wednesday brief, and re-verified by this seat.** The harness's own figures are quoted below as the harness's; every figure under "ran" is mine, measured in the environment named.

## What changed

| file | change |
|---|---|
| `Blockchain/Dev/services/originate/src/routes/webhooks.ts` | +20 / −2 — a `fail500(res, context, err)` helper, and `GET /` + `POST /` routed through it |
| `Blockchain/Dev/services/originate/src/__tests__/ks1341a-webhooks-500-never-answers-err-message.test.ts` | new, 173 lines — 4 red-first cells + 4 controls |

`message: err.message` in this file: **7 → 5** (the five are parts B and C). `fail500(` appears **3 times** — one declaration, two calls.

## Test Evidence

**Environment these figures name:** worktree detached at develop `e080174c86c671349c508560744644fc0ef33388`, which the worktree **contains** (`merge-base --is-ancestor` asserted); `npm ci` at `Blockchain/Dev`; **`packages/shared` BUILT** (`npm run build`, 28 files in `dist/`). Without that build 60 of 80 originate suites fail on `Cannot find module '@secuura/shared'` — that is the environment, not a regression, and every count below is from the built tree.

**Touched:** `services/originate` (product + a new unit cell). Read-only consumers: `packages/shared`, whose guards read originate sources by text.

**Ran:**

| check | command | result |
|---|---|---|
| red-first, cell alone (product hunks NOT applied) | `jest --runInBand <cell>` | **4 failed / 4 passed / 8 total** — the 4 declared cells red, all 4 controls green |
| green, both files | `jest --runInBand <cell>` | **8 passed / 8 total** |
| whole originate suite, BARE at the tip | `jest --runInBand` | **80 suites, 943 tests, 0 failed** |
| whole originate suite, PATCHED at this head | `jest --runInBand` | **81 suites, 951 tests, 0 failed** — `bare 943 / patched 951`, **0 new reds** (set difference on FAIL lines) |
| project type-check | `tsc --noEmit` | rc 0, no output |
| type-check **including the test file** | `tsc -p <extends tsconfig, exclude:[]>` | **rc 0, 0 errors** |
| `packages/shared` | `vitest run` | **48 files, 945 tests, 0 failed** |
| lint at the tip | `npm run lint` (`eslint src`) | rc 0 — **22 problems (0 errors, 22 warnings)**; `webhooks.ts` mentioned 0× |
| lint at this head | `npm run lint` | rc 0 — **22 problems (0 errors, 22 warnings)**; `webhooks.ts` 0×, the new cell 0× |

**Each red proved it reached the code under test, not merely that the body was clean.** The A1 reds fail with `"leaked": true` — the thrown text *is* in the 500 body at the tip. The A2 reds fail because the logger was never called with the route's context. All four are `toEqual` assertion failures; none is a load failure or a mock crash. **0 passed and 0 failed would have been a load failure, not a pass** — 4 passing controls in the same run prove the file loaded.

**The `GET /` trap is handled and pinned.** `GET /`'s list query carries `.catch((e) => { logger.warn(...); return []; })`, so a *rejected* `$queryRaw` is swallowed into a 200 with an empty list and never reaches the catch under test. The cell therefore makes `$queryRaw` throw **synchronously**, and `control KS-1341 A0` pins the swallowing branch so it cannot come back silently. Measured separately: **no catch block in this file tests error text at all** (no `includes(`, no `.code ===`), so no fixture string can be routed down a benign branch here.

**Two zeros that were controlled rather than asserted:**
- **The lint zeros.** `eslint src` covers **137 files, 86 of them under `__tests__`**, and the new cell is in that set. A planted `debugger` + unused variable in the cell yields **1 error and 1 warning** — so the instrument fires on this exact file. The file was then restored and the restore verified by sha256.
- **The type-check zero.** The project's own `tsconfig.json` **excludes `src/__tests__`**, so `tsc --noEmit` rc 0 covers 626 files and **zero** test files — it says nothing about the new cell. `--listFilesOnly` on a config that extends it with `exclude: []` shows the cell present and 86 test files in the program; that run is the rc 0 quoted above.

**NOT run:** the local stack is not up, so nothing integration-level, no gateway, no Postgres, no container. No deploy of any kind — not local, not demo, not UAT.

**Migrations + config:** none. No migration, no `package.json`, no lockfile, no `.github/`, nothing under `scripts/`.

## NOT COVERED — and one comment that is wrong at this PR

🔴 **The helper's docblock opens: *"KS-1341: the only place in this router that turns a caught error into a 500."* That sentence is FALSE at this PR.** After part A, **5** response lines in this file still carry `message: err.message`. It becomes true only once parts B and C land. It is raised this way deliberately: the diff is **byte-identical** to the local model's reviewed output (sha256 `65720c1d4caa05f503f4d331cd3b4588b9d60b09b94647f8e3c8c4ab6ca9d67b`, `cmp` rc 0 against both the golden and the run's canonical patch), and that provenance is worth more than a tidier comment parts B and C will make accurate. The same docblock's *"Declared at the END of the file"* was checked and **is** accurate — the helper sits at the end, immediately before the file's last line.

Also not covered: the other **five** `err.message` sites in this file (parts B and C); whether any further file in this family remains unswept (the ticket says that was not swept); and any behaviour of the five routes this change does not touch.

Refs KS-1341

## The push gate, as it actually ran on this head

`cb58d3a59c89` pushed under `.push-lock-27`; the in-hook preflight ran for ~6.5 min.

- **`pre_push_hook_base` 28/0 · `pre_push_hook_base_fixture_guard` 6/0 · `run_shell_suites` 49/0 · shell suites 60 passed, 0 failed, 0 skipped (of 60)** — the declared fleet condition, now **measured** on this tree (it was declared, not measured, at `e080174c86c6`: develop had moved 13 commits since the last measurement, one of them a `.sh` file).
- **0** lines starting `FIXTURE BUILD FAILED`.
- **`PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed.`** — 12/15 ran; legs 3, 4 and 8 **NOT run** (local stack not up on `http://localhost:6882`; all three skip lines say so). A skip is not a pass, which is why the verdict line says INCOMPLETE rather than PASSED.

Counts were parsed by **exact basename per suite block**, because `pre_push_hook_base` is a prefix of both `pre_push_hook_base_fixture_guard` and `pre_push_hook_base_leg_comment` — read loosely it reports 6/0 or 4/0 where the truth is 28/0, and an under-reported count reads as a missing gate. The three resolve distinctly: 28/0, 6/0, 4/0. The log carries **two** count-line formats (26 bare-indented, 25 name-prefixed), so each figure was confirmed in whichever form its own suite uses.

