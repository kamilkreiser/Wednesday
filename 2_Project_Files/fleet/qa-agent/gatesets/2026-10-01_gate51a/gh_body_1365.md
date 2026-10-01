## What this changes

Eleven POST operations across four services published a request body with no
`required: true`. A spec-driven caller therefore sent **no body at all**, and the
handler's zod schema answered 400 — a contract defect, not a handler defect. The
published contract now marks those eleven bodies required.

**This narrows KS-1364. It does not close it:** 11 of the ticket's 17 operations.

Refs KS-1364

## Shape

| part | files | numstat |
| -- | -- | -- |
| product `*.openapi.ts` (nft-certificate, analytics, billing, m365-integration) | 4 | **+11 / -6** |
| new vitest files, one per carve | 6 | **+294** |
| generated spec `docs/openapi/secuura-api.yaml` | 1 | **+11 / -0** |

Eleven added YAML lines, all the identical string `        required: true` (one
`uniq -c` group of 11). Five of the eleven product edits are replacements, six are
insertions. No `package.json`, no lockfile, no `scripts/`, no `referral.openapi.ts`.

## Test Evidence

**Touched:** `nft-certificate`, `analytics`, `billing`, `m365-integration` spec modules;
the shared generated spec.

**Ran** (all local, this branch, base `c56dd7c32edf`; every figure re-measured from a
fresh install — none of the upstream figures was carried):

| service | before | after | failed |
| -- | -- | -- | -- |
| nft-certificate | 38 | **48** | 0 |
| analytics | 28 | **32** | 0 |
| billing | 93 | **98** | 0 |
| m365-integration | 47 | **57** | 0 |

- **Red-first, by assertion, per test:** with the product hunks reverted and the six new
  tests present, **11 cells fail — exactly the 11 `RED KS-1364` cells — and 0 control
  cells fail.** Unique failing names: NR1, NR2, NV1, NV2 (nft-certificate), AR1
  (analytics), BL1, BL2 (billing), MS1, MS2, MS3, OD1 (m365-integration). The cells ran
  (44/31/96/53 passed alongside), so this is a real red, not a load failure.
- **Green after:** all four suites rc 0, 0 failed.
- `npm run check:openapi` **rc 0** — `generate-openapi --check` reports
  `CHECK PASS: on-disk YAML matches generated`, and `check-spec-examples` reports
  `405 example blocks — every published example resolves to the fixture set`.
  **Control:** with the YAML reverted to base, the same check goes **rc 1**
  (`CHECK FAIL: generated YAML differs from on-disk version`), so the rc 0 is a reading.
- `tsc --noEmit` **rc 0, 0 errors** in all four services (no-regression reading only).
- `git apply --check` rc 0 for all twelve diffs; the two carves that share a file applied
  strict on top of the first with **zero offsets**.

**NOT run** (honest gaps, and the point of this block):
- **No Schemathesis run and no live run.** That the no-body cases stop firing is a
  *prediction* from the rendered spec, not a measurement.
- The served `/api/docs/openapi.json` was not read.
- The 15 pairs baselined in `systemTest/schemathesis` against KS 255 are not touched here;
  un-baselining them is not in this change's scope.
- `tsc` base rc was not captured; head is 0 errors, which cannot be worse than base.

**Migrations + config:** none. No migration, no environment variable, no lockfile, no
`package.json`. Nothing deployable beyond the spec these four services publish.

## The six operations left, with the screen's reason for each

- `POST /api/referrals/generate` — `referral.openapi.ts` belongs to the KS 1015 lane.
- `POST /api/issuer-certs` — it lives in `auth.openapi.ts` (auth service).
- `PATCH /api/users/admin/{id}` and `POST /api/users/me/change-password` — auth surfaces.
- `PATCH /api/platform/tenants/{id}` — its `updateTenantSchema` is a partial-update schema
  that **accepts `{}`**, so the 400 comes from a "No fields to update" check, not from the
  zod schema; the ticket's clause "where the handler's Zod schema rejects an absent body"
  does not hold. It is also a platform-admin surface.
- `POST /api/v2/verification/verify` — the handler resolves one of four optional fields
  (`hash|contentHash|documentId|documentData`), not a zod object, so the shape is not
  derivable without a ruling; originate is on jest and has no spec-registry test to copy.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
