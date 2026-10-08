Refs KS-1449 — https://linear.app/secuura/issue/KS-1449

## What this changes

Six `nft-certificate` operations declared a `requestBody` with no `required: true`, so a
spec-driven caller (Schemathesis) sent **no body at all** and counted the request valid; each
handler's zod `safeParse` then answered 400 and the run failed `positive_data_acceptance`. Prior
behaviour: the published contract said the body was optional while every handler required one.

All six are now marked required in
`Blockchain/Dev/services/nft-certificate/src/nft-certificate.openapi.ts`, and the published
contract is **regenerated**:

| operation | pass it came from |
|---|---|
| `POST /api/nft/mint` | 2026-10-05 run dir ending `nft-mint-upload-fee` |
| `POST /api/nft/ipfs/upload` | same |
| `PUT /api/nft/admin/platform-fee` | same |
| `POST /api/nft/ipfs/pin` | 2026-10-05 run dir ending `nft-ipfs-pin-unpin-size` |
| `POST /api/nft/ipfs/unpin` | same |
| `POST /api/nft/metadata/estimate-size` | same |

Raised from two Wednesday-held Spark passes of 2026-10-05 (their run-directory names carry the
KS 591 and KS 1364 register keys, written de-hyphenated here so neither ticket attaches to this PR),
re-proved by Seat E 11th on develop `0a6177ea5482`.

## The YAML is REGENERATED — the Spark companion diffs misland and were not used

`Blockchain/Dev/docs/openapi/secuura-api.yaml` is written by
`Blockchain/Dev/scripts/generate-openapi.ts` (npm `generate-openapi` / `check:openapi`). Each Spark
pass also ships an `openapi-yaml.companion.diff`, and **those diffs are a trap at this base**: they
are cut against spec blob `52310cab1` while develop carries `146bae7edb87`, +87 lines on, and their
hunk context is generic (`security` / `requestBody:` / `content:` / `application/json:`), so
`git apply` places them by offset search on the nearest matching operation. Measured across all
twelve passes in this round's set: **every one applies rc 0 and five land `required: true` on the
wrong operation.** One of the five is this PR's own `nft-ipfs-pin-unpin-size`, which applied alone
flips `POST /api/nft/ipfs/upload` instead of `POST /api/nft/ipfs/unpin`.

So this PR applies only the `.ts` payloads and runs `npm run generate-openapi`. **No companion diff
was applied.**

### YAML PROOF (structural, not a line count)

Parse the base and head documents and compare every `paths[p][m].requestBody.required`:

- request-bodied operations: **145 before, 145 after** (none added, none removed)
- already `required: true` at base: 73
- **flipped ON: exactly the 6 operations above. Flipped OFF: 0.**
- whole-document diff: **6 added lines, 0 removed, every one a `required:` line**, in a
  40,021-line file
- `npm run check:openapi`: **rc 1** with the `.ts` change and the old YAML (the control proving the
  generator sees the change), **rc 0** after regenerating
- read back from the committed YAML, all six now read `requestBody.required = True`

A note for whoever reviews the next PR in this series: the companion route happened to produce a
**byte-identical** file for *this* PR, because the operation one companion mislands onto is in the
other pass's op set and the two displaced hunks cancel. It was right **by luck**, and nothing in the
companion route tells a reader which case they are in — which is why the proof above is structural.

## Test Evidence

**Touched:** `services/nft-certificate/src/nft-certificate.openapi.ts` ·
`services/nft-certificate/src/__tests__/ks591-nft-mint-upload-fee-body-required.test.ts` (new) ·
`services/nft-certificate/src/__tests__/ks1364-nft-ipfs-pin-unpin-estimate-size-body-required.test.ts`
(new) · `Blockchain/Dev/docs/openapi/secuura-api.yaml` (regenerated) · both platform-k HTML docs.

**Ran** (node v24.7.0, npm 11.5.1, vitest 4.1.11, typescript 5.9.3 — versions read from
`node_modules/*/package.json` in this worktree):

- `npm test` in `services/nft-certificate` (its own script, `vitest run`):
  - base, no change: **48 passed (48)**, 8 files
  - the two new test files, **no product change**: **6 failed | 54 passed (60)** — the six reds are
    NM1–NM3 and NP1–NP3 as `AssertionError`s on `requestBody.required`
  - with the product hunks: **60 passed (60)**, 10 files
- `npm run build` (tsc) in `services/nft-certificate`: rc 0
- `npm run generate-openapi` rc 0; `npm run check:openapi` rc 1 before / rc 0 after
- S-1: `npm ci --ignore-scripts` in `Blockchain/Dev` (1937 packages), `packages/shared` built with
  `dist/index.js` asserted and `require()`d, `npm ci` in all four `systemTest/*`; **0 tracked files
  modified** afterwards
- pre-push preflight on this exact head: `shell suites: 71 passed, 0 failed, 0 skipped (of 71)`,
  `OK — 13 code guards passed.`

**NOT run:**

- 🔴 **Preflight legs 3, 4 and 8 SKIPPED** — no local stack on this host
  (`SKIP — local stack not up on http://localhost:6882`). The preflight's own verdict is
  `PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed.` **Leg 8 is served-spec
  consistency (`/api/docs/openapi.json` vs `.yaml`, KS-656) — the leg an OpenAPI change most wants,
  and it did not run.** Legs 3 and 4 are spec-auth conformance and path resolvability.
- The four platform suites (Schemathesis, Akto, Playwright, Performance/k6) are **UNMEASURED** — no
  local stack. Not a pass.
- **The runtime half of both passes is READ, not driven:** each handler's own 400 on an absent body
  is read from the source; no request was issued. Live run owed.
- The served `/api/docs` was not read.

**Migrations + config:** none. No dependency, lockfile, manifest, baseline or spec-version change.

## Narrowing

This PR is the **spec half** of KS-1449. It marks **6 of 6 request-bodied `/api/nft/` operations**
required, so the nft surface for this class is complete — measured on the committed contract: **0
`/api/nft/` operations still carry an optional request body.** Across the whole contract **66
request-bodied operations remain not-required** and are OPEN; they belong to the wider register, not
to this PR. The ticket does **not** move to Done: the runtime half and a live sweep are still owed.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
