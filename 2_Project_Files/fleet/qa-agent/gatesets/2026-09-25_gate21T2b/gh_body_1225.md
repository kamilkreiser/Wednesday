#1225 KS-1291: remove the post-save issuerName guard that is unreachable since the early guard landed
head 120420a2e7b1a0d10dd41ee4320f7e88bc1529c6

## BLUF

`#1174` (KS-1265) moved the E-01 `@` refusal above `saveDocument` so a refused create writes nothing, and said so in its own merge message:

> *"The older post-save guard is now unreachable for that case and can be removed in a later cleanup."*

That cleanup was never filed. This removes the dead branch — **after proving it dead three ways**, because a removal justified by an unproven check is not justified.

## Arm 1 — static

Both guards compute the same value from the same field:

| line | expression |
|---|---|
| `:612` | `typeof req.body?.issuerName === 'string' ? req.body.issuerName.trim() : ''` |
| `:838` | `req.body && typeof req.body.issuerName === 'string' ? req.body.issuerName.trim() : ''` |

The field is never reassigned — a regex for an assignment to `req.body` / `req.body.issuerName` scores **0** across the file. **Controls both ways:** the same instrument scores **1** on the real assignment at `:623` (`data.issuerName = …`), and **0** on a planted `===` comparison, so it is neither blind nor fooled by an equality test. Brace depth is **2** at `:612`, `:616`, `:837` and `:844` — same block, early guard first on every path that reaches the late one.

## Arm 2 — a canary, with its own control

A `throw` planted in each guard's taken branch, whole originate suite each time:

| canary in | result | reading |
|---|---|---|
| the **early** guard (control) | **1 failed / 862 passed** | the failure is the ks549 E-01 cell — the right target |
| the **late** guard (measured) | **74 suites / 863 tests, all passed** | never executed |

A canary that reddens nothing was never reached. The control is what makes that green evidence rather than an absence of testing. File restored between arms and proved byte-identical by sha256.

## Arm 3 — paired mutation, on the post-removal tree

| | result |
|---|---|
| post-removal, `ks549` | **4 passed / 4** |
| then delete the early guard | **1 failed / 3** — the E-01 cell |

So the check that survives is the one doing the work. Restored byte-identical afterwards; porcelain back to the one file this PR touches.

## A comment is left where the guard was — deliberately

A bare deletion invites the next reader to put it back, which would answer 400 for a document already saved: the exact defect KS-1265 fixed. The early guard's own comment also pointed at the removed block (*"The E-01 no-emails guard **below**"*) and is re-pointed in the same commit — leaving it would have manufactured the next KS-1277.

## Test Evidence

* **Touched:** `services/originate/src/routes/documents.ts`. No test file changed — the witness cell already exists, added by #1174.
* **Ran:** originate `jest --runInBand` → **74 suites / 863 tests, rc 0**, identical to the bare serial baseline at this base (**74 / 863**), so removing this branch reddens nothing. `tsc --noEmit` rc 0. `packages/shared` `vitest run` → **46 files / 918 tests, rc 0**. Plus the three arms above.
* **A red that was not real, and how it was resolved:** the first `packages/shared` run on this head returned **4 files failed**, every failure `Test timed out in 5000ms` and **no assertion failure**, in four repo-walk guards taking ~8 s against vitest's 5 s default at load 10.15. Three arms: the four files pass on this tree at `--testTimeout=60000` (**69/69**); pass on a different tree at the default; and **the exact failing command, re-run unchanged on this tree, passes 46/918 with 0 timeouts**. Recorded on **KS-1155**, which already owns that class. Both runs are reported rather than only the green one.
* **NOT run:** the integration config (`jest.integration.config.js`) — needs a live Postgres. No image rebuilt.
* **Preflight legs:** 12/15 ran; legs **3, 4, 8 NOT run** (local stack not up). **This PR DOES have a route-handler surface, so those legs are OWED AT THE GATE.** The arm worth exercising there: `POST /api/documents` with an `@`-carrying `issuerName` must still answer **400 BAD_REQUEST**, now from `:616`, with nothing saved. This is **not** a claim that the gate is green.
* **Migrations + config:** none.

Refs KS-1291

🤖 Generated with [Claude Code](https://claude.com/claude-code)

