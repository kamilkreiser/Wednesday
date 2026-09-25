#1233 KS-1133: document the v1/v2 hash-alias split on both verify routes, and name BAD_REQUEST on sign-wallet
head 6892124d9304ae014c52f7ea08a17e9468d411bf

## BLUF

Kam ruled **`accept-split`** on 2026-09-13: v1 reads `hash` **LAST**, v2 reads it **FIRST**, and the split is *documented* rather than reconciled. This writes it where a connector author reads it — both route descriptions in the served spec — and carries **KS-1229's R-a** in the same regeneration, because they are one file and one 28k-line generated artefact.

| route | alias order |
|---|---|
| `POST /api/verification/verify` | `providedHash` → `contentHash` → `documentHash` → `hash` (**`hash` LAST**) |
| `POST /api/v2/verification/verify` | `hash` → `providedHash` → `contentHash` → `documentHash` (**`hash` FIRST**) |

Each names the other and states the divergence is by design, not omission.

## Also in this pass, because it is the same sentence and the same regeneration

* **The ticket's checklist item 4** — `VerifyRequest`'s description named a **strategy** order ("chain-first, then originate-id lookup, then hash/title") and **no alias order at all**, and omitted `providedHash` and `documentHash`, which the validator accepts. It now separates the two orders and names all six fields.
* **KS-1229 R-a** — the sign-wallet `400` named only `VALIDATION_ERROR` and `INVALID_WALLET_SIGNATURE`, not the `BAD_REQUEST` the KS-1213 relabel guard returns.

Two open PRs regenerating the same file would collide on the second merge. Grouped on Wednesday's ruling of 2026-09-25 02:20:37Z.

## A correction to the ticket

It names `services/originate/src/openapi/*.openapi.ts`. **There is no `src/openapi/` directory at this base** — the source is the single file `services/originate/src/originate.openapi.ts` (22 such files repo-wide, one per service).

The cells the checklist asks for already exist: `ks1103`'s **P1** pins v1 (`{contentHash:A, hash:B}` → A), and the v2 pin landed with #1151 (`d2be4d3cd`). Neither is re-added.

## Test Evidence

* **Touched:** the originate OpenAPI source and the generated spec. No service code.
* **Ran:** originate `jest --runInBand` → **74 suites / 863 tests, rc 0**, identical to the bare serial baseline. `tsc --noEmit` rc 0. `packages/shared` → **46 files / 918, rc 0**.
* **Spec gate:** `npm run check:openapi` **rc 0** — that is `generate-openapi --check` (the committed yaml matches its source exactly, so no drift is smuggled in) plus `check-spec-examples`: *"405 example blocks — every published example resolves to the fixture set."*
* **Drift checked, not assumed:** `git diff -U0` over the yaml is **20 insertions / 6 deletions**, and every changed line belongs to one of the four descriptions above.
* **NOT run:** legs **3, 4, 8** (local stack not up). **This PR has a served-spec surface, so they are OWED AT THE GATE** — leg 8 (served-spec consistency, `/api/docs/openapi.json` vs the yaml) is the one that matters here. Not a claim that the gate is green. The spec is bind-mounted, not baked, so no image rebuild applies. Integration config not run.
* **Migrations + config:** none.

Refs KS-1133
Refs KS-1229

🤖 Generated with [Claude Code](https://claude.com/claude-code)

