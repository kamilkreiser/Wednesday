Refs KS-593 — https://linear.app/secuura/issue/KS-593/not-a-server-error-recurs-17-raw-5xx-across-8-ops-ks-431-ks-449-ks-497

Raised from Wednesday-held Spark passes (run dirs `spark_secuura_2026-10-05_KS-593-adminconfig-negative-offset-r2`, `spark_secuura_2026-10-05_KS-593-share-null-recipient-cp2`, `spark_secuura_2026-10-06_KS-593-signatories-non-uuid-id`), re-proved by Seat G 4th on develop `0a6177ea5482`.

## What this changes

Three passes in `Blockchain/Dev/services/originate`, one per route, each turning a malformed input that previously reached a raw `500 INTERNAL_ERROR` into the route's **existing** `400` refusal.

| Pass | File | Input that used to 500 |
|---|---|---|
| negative offset | `routes/adminConfig.ts` | `?offset=-1` on two admin list routes |
| null share recipient | `routes/documents.ts` | a non-object entry in `recipients[]` on `POST /api/documents/:id/share` |
| non-uuid signatory id | `routes/signatories.ts` | a non-uuid id on `GET /api/signatories` and `/check` |

**NARROWING — KS-593 stays OPEN and must not be moved to Done by this PR.** It covers 2 of the 6 negative-offset sites in KS 565 section 2 (the auth `users.ts` and tenant-provisioning sites are deliberately outside this carve), 1 of the 7 raw-5xx operations, and the ninth operation plus `/check`. KS 1015 finding 1 describes the same class of unowned check and operation pairs; that ticket is untouched here.

**No authorisation decision moves.** Every guard runs after authentication, the role/scope gate and the tenant-scoped read, and before any write transaction — so nothing is persisted on a refused request. An array recipient (`typeof [] === 'object'`) still falls through to the email/userId check, which answers 400.

## Test Evidence

**Touched:** `services/originate/src/routes/{adminConfig,documents,signatories}.ts`; `services/originate/src/__tests__/ks1293-originate-suite-is-hermetic.test.ts` (SUBJECTS entry only); 3 new `services/originate/src/__tests__/ks593-*.test.ts`; both platform-k HTML docs. 9 paths, +336/-4.

**Ran** (by me, on this worktree, at base `0a6177ea5482`; jest 29.7.0, ts-jest 29.4.11, typescript 5.9.3, node v24.7.0, npm 11.5.1 — versions read from `node_modules`):

| Pass | Red at base (test half only) | Green after product half |
|---|---|---|
| adminconfig | 2 failed, 3 passed (5), rc 1 | 5 passed (5), rc 0 |
| share | 2 failed, 13 passed (15), rc 1 | 15 passed (15), rc 0 |
| signatories | 3 failed, 3 passed (6), rc 1 | 6 passed (6), rc 0 |

Whole `services/originate` suite through its own `npm test`: **93 suites / 1077 tests / 0 failed** at the base, **96 suites / 1093 tests / 0 failed** with all three passes. rc 0, zero `FAIL` lines, no new reds.

The payload was split into product and test halves with a control asserting the two halves recombined are byte-identical to the input, so each red above is measured against the patch that actually ships. The staged tree is `b8ff928e2b63`, equal to the stacked-tree value measured independently before the build.

**Hermetic manifest.** The share pass adds its own new file to KS 1293's `SUBJECTS`; the other two new files are deliberately **not** listed. `MANIFEST-DRIFT` requires a `SUBJECT` only for a test file whose content mentions `ANCHORING_SERVICE_URL` — counted: share 1, adminconfig 0, signatories 0. Control: planting one such mention into the unlisted adminconfig file turns `MANIFEST-DRIFT` red (1 failed / 9 passed, `missing` non-empty); restoring it byte-identical returns 10 passed.

**NOT run:**
- **No live run.** There is no local stack, so none of the three 500s was reproduced against a real PostgreSQL. The adminconfig 500 is KS-593's 2026-08-28 live measurement of the list route; `/check`'s 500 is reasoned from the identical `::uuid` cast. **A live run is owed and the ticket stays open.**
- The four platform suites (Schemathesis, Akto, Playwright, Performance/k6) — unmeasured, no stack. Not claimed as passing.
- Whole-service `npm run lint` and prettier were not run.
- The other signatory routes (`/:id`, revoke, reinstate, update) were not screened for the same class.

**Migrations + config:** none. No migration, no env var, no spec change — the OpenAPI documents no 400 for these inputs, and adding one would be a separate change.

## Provenance note

Three of the four Spark passes behind this seat carry a HOLD REVIEW but **no READY artefact**; only `signatories-non-uuid-id` has one (`READY_KS-593-SIGNATORIES-NON-UUID-ID-1_…_2026-10-06`). Per the ruling on Q-HOLD18 these were raised from the REVIEW + `checker.out` + `patch.diff` instead, and that gap is recorded here rather than left implicit.

## Pre-existing, out of scope, not introduced here

Neither signatory GET checks that the caller belongs to the `organizationId` it is asked about: within a tenant, any authenticated user can list any org's signatories or query `/check`. Worth a separate look; it is not this ticket.
