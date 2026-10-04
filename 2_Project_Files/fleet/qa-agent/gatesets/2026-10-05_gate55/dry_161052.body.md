SIM — written by the gate55 drafter from Seat B 58th's brief (ITEM 3 step 3) and its 15:37Z / 15:44Z STATUS mails. NOT the PR body: the PR is not raised. Exercise input only.

## What this does

Narrows KS 1015, does not close it: the published contract for `GET /api/delegations/{id}` now declares the `{ success, data: { delegation, chain } }` envelope its handler (`routes/delegations.ts`, `GET /:id`) returns, instead of a bare `Delegation`. The spec follows the runtime.

PR A (#1374, KS 1402) merged as `2d85b84e1012`; this PR was stacked on its pre-squash head `aa16f3256dbf86e654076a31ace1eb1b79a31e69` and is rebased onto develop.

## Evidence

- `npm run generate-openapi` reproduces the committed YAML byte-identically (sha256 `373ef7805f8896aa…`); with the YAML reverted to its base blob, `npm run generate-openapi -- --check` returns rc 1 and writes nothing.
- `npm run check:openapi` rc 0.
- Red-first: D1-D3 red at base by AssertionError, C1-C3 green; 6/6 green at head. transfer suite 4 files / 70 tests -> 5 / 76.
- pathgate53: 5 declared paths, 0 of PR 0's files, 0 co-tenant paths.

## Docs (skill §4)

One new KS 1015 block in each platform-k doc, after the KS 1402 block, additions only. Timing: at base `2d85b84e1012`, `services/transfer`, `generate-openapi` and `check:openapi` each hit 1 per doc and every hit sits inside the KS 1402 block, so 0 hits outside the KS 1402 block; must-hit control `auth` 68 / 67. No timing row changed.

## NOT COVERED

- Skill §5f: no live sweep.
- No live call to the delegation GET.
- No live S+K pair run. No Schemathesis, no Akto.
- No deploy.
- `tsc` in `services/transfer` excludes `src/__tests__` (tsconfig.json:27), so the new test file is not type-checked.

Branch adopted from Seat B 55th, carried by Seats B 56th and B 57th, finished by Seat B 58th.

Refs KS-1015
