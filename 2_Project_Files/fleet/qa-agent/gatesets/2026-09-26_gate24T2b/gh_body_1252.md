#1252 KS-1275: the lifecycle-verb description points at the enum, not a list (KS-1299)
head ca7337fa04e04e5438bc79a5abe215424fcb33ef

## BLUF
Two published descriptions that had drifted from the code. **KS-1275** stops the lifecycle-verb description enumerating verbs and points it at the enum plus `docs/VOCABULARY.md`, so the prose cannot drift again. **KS-1299** mirrors the narrowing #1223 landed in the route comment but never reached the spec. The yaml is regenerated, and its diff is exactly these two descriptions.

## KS-1275 — the list is replaced by pointers, and the pin moves from the sentence to the property
The description read *"Only verbs WITHOUT a dedicated endpoint are accepted — share/transfer-custody/revoke etc. must use their own routes."* That inline list had already gone stale once, which is the whole reason this ticket exists.

It now names the two sources of truth the code comment three lines above it already named — `LIFECYCLE_EVENT_ACTIONS` in `services/originate/src/lifecycleActions.ts`, and `docs/VOCABULARY.md` — and carries **no verb name at all**. The accepted set is the property's own published enum.

**#1123's `DESCRIPTIONVERBLIST` cell pinned the sentence.** It parsed the published description (`description.split(' etc.')[0].split(' ').pop().split('/')`) and expected the literal `share/transfer-custody/revoke`. That made the prose load-bearing. Removing the list reds it **by design** — measured before changing it: 1 failed / 11 passed, the parse yielding `["re-synchronised."]`.

Replaced by two cells that pin the property and read no verb out of prose:

| cell | what it pins |
|---|---|
| `DESCRIPTIONPOINTSATSOURCE` | the description names both sources of truth **and** no verb that has its own route — the dedicated-verb set read from the registry, not hardcoded, and asserted non-empty so the cell cannot pass vacuously |
| `EXCLUSIONHOLDS` | no verb with a dedicated `POST /api/documents/{id}/<verb>` route is accepted by `LIFECYCLE_EVENT_ACTIONS` — the invariant the prose was standing in for; both sides asserted non-empty first |

`ORDERTHROUGHSPEC` (the other #1123 cell) is untouched and still green.

## KS-1299 — the spec still carried an overclaim the code comment had already dropped
The v2 verify description said v1 reads `hash` LAST *"so its legacy bodies keep their answer"*. #1223 corrected precisely that sentence in `routes/verification.ts` (KS-1118 F-3: *"NOT 'every body that worked before keeps its answer', which is what this said and is wrong"*), and the published spec was never updated.

Mirrored: a body carrying a pre-existing alias keeps its lookup value, but a body pairing `hash` with `documentId` or `documentData` takes the **hash** strategy on v1 too, where it used to take the id / data one. `documentId`-only, `documentData`-only and alias-only bodies are unchanged.

## Test Evidence

**Touched:** `services/originate/src/originate.openapi.ts`, `services/originate/src/__tests__/ks978-published-contract-organizationuuid.test.ts`, `docs/openapi/secuura-api.yaml`. 3 files, +56 −14.

**Ran (all on this head):**
- `npx jest --runInBand` (originate): **870 passed / 870, 74 suites / 74**, rc 0. Baseline 869 at `6e2a00bfe`; the +1 is accounted — one cell replaced by two. The base moved to `77c6426b9` under me, and that range adds **no** originate test cell (it is `.githooks/pre-push` plus this seat's own merged comment-only change), so 869 is the right comparison.
- **Red proofs, one arm per conjunct, five arms.** Each flips exactly one term with the others held true; each reddens **exactly one** cell and leaves the other 12 green; every restore verified by `sha256` against the pre-tamper hash:
  - A1 drop the `lifecycleActions.ts` pointer → `DESCRIPTIONPOINTSATSOURCE` red
  - A2 drop the `docs/VOCABULARY.md` pointer → `DESCRIPTIONPOINTSATSOURCE` red
  - A3 let a dedicated-route verb back into the description → `DESCRIPTIONPOINTSATSOURCE` red
  - B1 add `revoke` to `LIFECYCLE_EVENT_ACTIONS` → `EXCLUSIONHOLDS` red
  - B2 make the registry read match nothing → `EXCLUSIONHOLDS` red **rather than passing vacuously**
  - B2's anchor text is not unique (identical at `:161` in the sibling cell), so it was tampered **by line number** with the content asserted and the sibling line proved unmoved.
  - Untampered re-run after all five: 13/13, rc 0.
- `npm run lint` (= `eslint src`): rc 0.
- `npx tsc --noEmit`: rc 0. Re-run with `exclude: []` because the project tsconfig excludes `src/__tests__`, with the edited test file asserted present in the program (705 files, `--listFilesOnly`): rc 0.
- `npm test -w packages/shared`: 47 files / **928 tests** passed, rc 0.
- `npm run generate-openapi -- --check`: **CHECK PASS**. Run on the base **before** editing as well, where it also passed — so the yaml's +13/−6 is attributable to this change alone and no foreign drift rode along.

**NOT run:**
- **The push preflight was INCOMPLETE — 12/15 legs ran, 3 SKIPPED, nothing failed.** The three are **leg 3** (spec-auth conformance), **leg 4** (path resolvability) and **leg 8** (served-spec consistency), each `SKIP — local stack not up on http://localhost:6882`. A skip is not a pass. **Leg 8 is the one worth naming:** it compares the served `/api/docs/openapi.json` against the on-disk `.yaml`, which is exactly the artefact this PR regenerates — so the check most related to this change is among the three that did not run. `generate-openapi --check` covers source-vs-disk, not served-vs-disk. In-hook suites that DID run: `pre_push_hook_base` 28/0, `pre_push_hook_base_fixture_guard` 6/0, shell suites 60 passed / 0 failed / 0 skipped (of 60). No `FIXTURE BUILD FAILED`.
- No integration or e2e suite: this change has no runtime surface. Both descriptions are published metadata; the executable set of accepted verbs is unchanged (`EXCLUSIONHOLDS` asserts that).
- The served spec was not re-imported into Akto/Schemathesis; the gateway bind-mounts the yaml, so nothing was rebuilt.

**Migrations + config:** none. No migration, no env var, no dependency change. `migrations/037` untouched.

Refs KS-1275
Refs KS-1299

🤖 Generated with [Claude Code](https://claude.com/claude-code)

