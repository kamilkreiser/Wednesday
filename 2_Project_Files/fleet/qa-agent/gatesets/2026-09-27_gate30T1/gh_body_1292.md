#1292 KS-1341 part C: route the last two webhooks 500s through the fail500 helper
head ef821d2e27bf06ae1420bdb830ec7fffd7b8c732

## BLUF
`POST /:id/test` and `GET /:id/deliveries` were the last two of the seven unconditional 500s in `routes/webhooks.ts` that answered with the thrown error's own text and no `NODE_ENV` guard. Both now go through the `fail500` helper parts A (#1288) and B (#1290) introduced — both merged. This is **part C of 3**, and it finishes the seven.

Refs KS-1341

## What changed
Two files, +171/−2.

- `services/originate/src/routes/webhooks.ts` (+2/−2) — the two `res.status(500).json({ … message: err.message })` sites at `:391` and `:416` become `fail500(res, '<context>', err)`.
- `services/originate/src/__tests__/ks1341c-webhooks-500-never-answers-err-message.test.ts` (+169, new) — 5 red-first cells and 3 controls.

Measured on the patched file, by me:

| | tip | after |
|---|---|---|
| `message: err.message` | 2 | **0** |
| `fail500(` | 6 | **8** — 1 declaration (`:562`) + 7 calls (`:200 :267 :325 :337 :352 :391 :416`), each a distinct context |

`err.message` still appears twice, and **neither is in a response**: `:544` (`logger.warn('Webhook dispatch failed', …)`) and `:563` (the helper's own server-side log).

## Provenance
The patch was produced by the local model under a Wednesday brief and **re-verified by this seat, not taken on trust**. The diff block is **byte-identical** to the brief's golden and to the run's canonical patch: 188 lines, 9,564 B, sha256 `78fd00567f5f31e0a94a8508f80a82867fb437199d309cca3710e668020e24e2`, `cmp` rc 0 against both (control: `cmp` against an unrelated golden → rc 1). It applies **strictly** at `3f70224a069b` — `git apply --check -p1` per file, no `--recount`, no fuzz — and a tampered copy of each section is refused (section 1 rc 1 "patch failed … :414"; section 2 with a corrupted hunk count rc 128 "corrupt patch").

## Test Evidence
Run by the author, locally, in this worktree at head `ef821d2e27bf06ae1420bdb830ec7fffd7b8c732` (base `3f70224a069b`, confirmed an ancestor). Node/jest via the repo's own scripts; `packages/shared` built.

**Touched:** `services/originate/src/routes/webhooks.ts`, `services/originate/src/__tests__/ks1341c-webhooks-500-never-answers-err-message.test.ts`

**Ran:**
- **RED (the cell alone, product hunks reverted — revert confirmed by blob id `a2ad9e05…` = the tip):** `Tests: 5 failed, 3 passed, 8 total`. The 5 failures are exactly the declared cells, **each on its own `expect(...).toEqual` assertion**, not a crash — zero `TypeError`/`ReferenceError`/`is not a function` in the output, and 8 tests ran (0 passed + 0 failed would be a load failure, not a red):
  - `RED KS-1341 C1 POST /:id/test: the thrown message is not in the 500 body under production, development, test or unset`
  - `RED KS-1341 C1 GET /:id/deliveries: …` (same assertion, other route)
  - `RED KS-1341 C2 POST /:id/test: the thrown message is logged once, server-side, with this route named`
  - `RED KS-1341 C2 GET /:id/deliveries: …`
  - `RED KS-1341 C3 SOURCE: no response in the file carries err.message, and all seven sites use the helper with DISTINCT contexts`
  - The 3 controls stayed green, including `control KS-1341 C0: a REJECTED deliveries query is still swallowed into a 200 and never reaches the catch`.
- **GREEN (both files):** `Tests: 8 passed, 8 total`, after restoring the product patch **verified byte-identical by sha256**.
- **REACHED, per route, with the mechanism named:** `GET /:id/deliveries`'s query carries its own `.catch(() => [])` at `:412`, so a *rejected* query is swallowed into a 200 and never reaches the catch — control C0 pins exactly that. The cell therefore arms that route with a **synchronous throw** and `POST /:id/test` with a rejection. Both catches are shown reached by their reds.
- **The KS1344 lesson is closed in this cell, proven not declared.** C1 clears the logger per environment and asserts the whole call list. Tamper: make `fail500` log only under `NODE_ENV === 'production'` → `Tests: 2 failed, 6 passed, 8 total`, and the red set is **exactly the two C1 rows** by title; C2, C3 and all three controls stay green. Restored by content, verified by sha256.
- **originate suite, serial (`jest --runInBand`):** **bare 962 passed / 0 failed (82 suites)** at the tip, **patched 970 passed / 0 failed (83 suites)** at this head. **0 new reds** — the failing-suite sets are identical and both empty; the +8 is this cell.
- **`tsc --noEmit` over a program PROVEN to contain the new cell:** the service tsconfig excludes `src/__tests__`, so a bare `tsc` covers **0** test files (measured: `--listFilesOnly` finds the cell 0 times). With a config extending it and `exclude: []` the program is **715 files and contains the cell (1 occurrence, proven)** → **rc 0, 0 errors**.
- **`packages/shared` (vitest) at this head:** **48 files, 945 passed**, rc 0 — it is run because its guard suites read originate sources by text.
- **ESLint, the package's own `npm run lint` (`eslint src`), at BOTH trees:** tip **22 problems (0 errors, 22 warnings)**, head **22 problems (0 errors, 22 warnings)** — identical per-file breakdown across the same 14 files, delta 0. **Neither of my two files contributes a single problem.** Control: a planted `debugger` in the new cell produces `no-debugger` **error** at its line and rc 1, so lint does see the new file.
- **Push gate — quoting only what THIS push printed:** `pre_push_hook_base.test.sh` **28/0** · `pre_push_hook_base_fixture_guard.test.sh` **6/0** · `run_shell_suites.test.sh` **49/0** · shell suites **60 passed, 0 failed, 0 skipped (of 60)** · `OK — 13 code guards passed` · zero lines starting `FIXTURE BUILD FAILED`. Counts were parsed per suite block by exact basename: `pre_push_hook_base` is a **prefix** of two other suites (`…_fixture_guard`, `…_leg_comment` 4/0) and a prefix parser silently misreads them.
- **Preflight:** `PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed.` Legs 3, 4 and 8 did **not** run (local stack not up).

**NOT run / NOT covered:**
- No local stack, so preflight legs 3, 4 and 8 did not run, and there is **no live sweep**. This is runtime code, so under the test-discipline rule the ticket does **not** move to Done on this evidence alone — a live sweep is owed.
- No deploy of any kind: not demo, not UAT, not kintsugi.
- No integration/e2e run against a real database; the cell mocks at the route boundary.
- `tsc` invoked on the test file **directly** with ad-hoc flags reports 7 pre-existing `TS2339` errors in `webhooks.ts` at lines `221, 298, 474, 475, 480, 483, 488`. **Control: the identical 7 appear at the untouched tip** (revert confirmed by blob id), **0 are in the new cell**, and none is at a line this patch touches (`391`, `416`). They are an artefact of compiling without the project config, not a finding — the authoritative check is the program-proven `tsc` above.
- **Three sentences in the helper's docblock (`:549`–`:561`) are not corrected here, deliberately.** Part C does not touch them, and amending them would forfeit byte-identity to the golden:
  1. *"the only place in this router that turns a caught error into a 500"* — false after parts A and B, and **becomes true only with this change** (the C3 SOURCE cell pins it).
  2. *"Declared at the END of the file"* — it sits immediately before `export default webhooksRouter;` (`:567`).
  3. *"Seven catch blocks above put the thrown error's own text in the 500 body"* — after this change that describes history, not the file.
  A follow-up docs ticket is owed for the rewording.

## Review notes
- Base is `develop` at `3f70224a069b`; this branch is a fast-forward on it. No merge-in.
- Foreign keys are un-hyphenated in this title, body and commit message (`KS730`, `KS1344`). The cell's own `KS730` reference is file content and is unchanged.
- Parts A (#1288) and B (#1290) are merged; this completes the seven sites.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

