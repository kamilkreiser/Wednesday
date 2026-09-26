#1276 KS-794: declare fileSize and fileHash on the verify schemas
head 737a4069c6316b10a89fa9c499fac6c2cb20f619

## What

Both verify-file handlers return `fileSize` on every 200, and the v1 one also returns `fileHash`, while neither response schema declared any of them. Both bases are `.passthrough()`, so the responses validated and nothing went red — the contract was simply narrower than the behaviour.

**Option (1) from the ticket:** optional fields on the two BASE schemas. No new schema, no new example, no allowlist entry. The alternative — `.extend()` into new registered schemas — copies the base `example` across, and the E8 identifier-literal guard correctly refuses the copies; an allowlist entry for a schema just created would carry a justification that is false of it, which is the failure the guard exists to catch.

## Two corrections to the ticket, both measured before building

**1. `fileHash` is declared on `VerifyResponse` ONLY.** The ticket's comment says "`fileHash` needs the same treatment as `fileSize`". Measured at source: v1 verify-file returns `fileHash`; the **v2** handler computes the same sha256 over the same bytes and returns it as **`hash`**, never a `fileHash`. Declaring `fileHash` on `V2VerifyResponse` would publish a field no v2 operation emits. Neither name is being renamed — a published field rename is a breaking change and is not proposed — so the divergence is documented in both response descriptions **and asserted by a cell**, so a later reader cannot "tidy away" the asymmetry as an oversight.

**2. FIVE operations' published schemas move, not two**, because both bases are shared. Confirmed by walking the regenerated yaml (not only the source), with controls:

| schema | operation | returns `fileSize`? | returns `fileHash`? |
|---|---|---|---|
| `VerifyResponse` | `POST /api/documents/{id}/verify` | no | no |
| `VerifyResponse` | `POST /api/verification/verify` | no | no |
| `VerifyResponse` | `POST /api/verification/verify-file` | **yes** | **yes** |
| `V2VerifyResponse` | `POST /api/v2/verification/verify` | no | no |
| `V2VerifyResponse` | `POST /api/v2/verification/verify-file` | **yes** | no — it returns `hash` |

Three of the five return neither field. "Optional and absent" is an honest description of those three, and that trade is exactly what the ticket's option (1) proposes — but the ticket names only the two verify-file operations, so the other three are named here. Controls on the yaml walker: a nonexistent schema returns **0** references; `ErrorResponse` returns **2666**.

Nothing here types the published `blockchain` block (the `secuura-ks1019-blockchain-block-untyped` ruling).

## Why a cell file, when `check:openapi` is green

`check:openapi` proves the committed yaml matches what the generator emits. **It cannot prove the generator declares any particular field** — delete the two lines from the schema, regenerate, and `check:openapi` is green again on a spec that has silently lost them. That blindness is recorded on KS-811. So the properties an integrator depends on are asserted in `ks794-verify-file-fields-are-published.test.ts`.

## Test Evidence

**Touched:** `services/originate/src/originate.openapi.ts`, `docs/openapi/secuura-api.yaml` (regenerated, per the OpenAPI rule), and a new `services/originate/src/__tests__/ks794-verify-file-fields-are-published.test.ts`.

**Base:** this worktree **contains** develop `d7cdecf1d2eef7dde26dd23120e80c9db3f0e4a9` (`git merge-base --is-ancestor` → yes), so unlike my two earlier PRs this round, **these counts measure the combined tree**, not a pre-merge base.

**Ran** — `worktrees/s-b29-ks794`, `packages/shared` BUILT (88 dist files):

| arm | result |
|---|---|
| originate BARE (both files restored pre-edit, sha256-verified) | **878 passed / 878, 74 suites**, rc 0 |
| originate PATCHED, before the cell file existed | **878 passed / 878, 74 suites**, rc 0 |
| originate PATCHED, with the cell file | **881 passed / 881, 75 suites**, rc 0 (+3 cells) |
| `packages/shared`, `npx vitest run` | **941 passed / 941, 48 files**, rc 0 |
| `tsc --noEmit` in `services/originate` | rc 0 |
| `npm run check:openapi` | **rc 0** — `CHECK PASS: on-disk YAML matches generated`, and `check-spec-examples`: 405 example blocks, every published example resolves to the fixture set |

The schema-only arms reading 878 either side is the point: adding optional fields to a shared base breaks no existing cell. `packages/shared` is run because its guard suites read originate sources by TEXT.

**Planted-drift control, two-sided.** A **one-character** change to a published description in the on-disk yaml, with nothing regenerated → `check:openapi` **rc 1**, `[gen-openapi] CHECK FAIL: generated YAML differs from on-disk version`. Restored by content, sha256 identical (`bc67c11bec447622`) → **rc 0**. So the green above is a check that can fail.

**Red-proved one conjunct per arm, six arms, each reddening exactly the named cell:**

| arm | conjunct falsified | cell(s) that red |
|---|---|---|
| R1 | `fileSize` removed from `VerifyResponse` | V1PUBLISHESBOTH + NOTONLYPROSE |
| R2 | `fileHash` removed from `VerifyResponse` | V1PUBLISHESBOTH + NOTONLYPROSE |
| R3 | `fileSize` removed from `V2VerifyResponse` | V2PUBLISHESFILESIZEONLY + NOTONLYPROSE |
| R4 | the asymmetry "tidied away" — `fileHash` **added** to `V2VerifyResponse` | V2PUBLISHESFILESIZEONLY |
| R5 | v1 `fileSize` typed as a string | V1PUBLISHESBOTH |
| R6 | v1 `fileHash` made **required** | V1PUBLISHESBOTH |

**R6 is worth reading, because its first version proved nothing.** Dropping `.optional()` alone gives **TS2769 at the schema's own `.openapi({ example })`** — the published example carries no `fileHash`, so a required field makes that example fail the inferred input type, and **the suite never compiles**. A compile-breaking tamper reds with nothing having run. The runner's `LOADFAIL` verdict caught it instead of scoring it, and the arm was rewritten to fix the example too, so the file compiles and the cell is the only thing that reds. **The fact that fell out is worth keeping: optionality here is enforced by the example block at compile time, independently of any cell.**

Every tamper asserts its anchor before applying. `fileSize: z.number().int().optional().openapi({` occurs **twice** — once per schema — so those arms tamper **by line number with the surrounding content asserted**, located from a unique description line at a fixed offset; a wrong offset aborts the run rather than guessing an occurrence. Restores are by content with sha256 asserted.

**NOT run / NOT covered:**
- **Legs 3, 4 and 8 NOT run** (local stack not up): `12/15 ran; legs 3, 4, 8 NOT run (local stack not up)`. **Leg 8 is the served-spec-vs-yaml check and it is the leg closest to this change**, since this PR moves the yaml — its absence is the most significant gap here and is named rather than waved through. The yaml *is* proven to match the generator by `check:openapi`; what is unproven is that the **gateway serves** the regenerated document.
- No runtime behaviour is exercised, because none changes: the handlers already returned these fields. The claim is about the published contract.
- The v1/v2 naming divergence is **documented and asserted, not fixed**. Renaming a published field is out of scope here.

Refs KS-794

🤖 Generated with [Claude Code](https://claude.com/claude-code)

## Push gate — and this is the fleet's first measurement of the quadruple ON `d7cdecf1`

`pre_push_hook_base` **28/0** · `fixture_guard` **6/0** · `run_shell_suites` **49/0** · shell suites **60 passed / 0 failed, 0 skipped (of 60)** · `^FIXTURE BUILD FAILED` **0 times**. Preflight **INCOMPLETE — 12/15 legs ran, 3 SKIPPED (legs 3, 4, 8 — local stack not up)**. That is not a pass and is not quoted as one.

Unlike a pre-merge worktree, **this one contains the new develop**: my head's parent is `d7cdecf1d2eef7dde26dd23120e80c9db3f0e4a9` exactly. And the quadruple is attributable to that base rather than to this change — of the three files this PR touches, **0** are under `Blockchain/Dev/scripts/{__tests__,preflight,audit}/` or `.githooks/`, which is where every counted suite and everything those suites read by text lives (control: 2 of the 3 are under `services/originate/`). So the expected figures the 19:27Z fleet declaration carried as UNMEASURED are now measured.

