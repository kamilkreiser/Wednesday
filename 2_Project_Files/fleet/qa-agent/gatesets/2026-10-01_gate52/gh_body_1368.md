Refs KS-1364

Two of the remaining six operations from the sweep. **This does not close the ticket**:
13 of its 17 operations are covered once this lands, and four are left.

## The two operations, and why each is safe to mark
Both handlers already refuse an absent or empty body with a 400, so declaring the body
required makes the contract agree with the runtime rather than changing behaviour.

**PATCH /api/platform/tenants/{id}** — the handler builds its SET list from whichever
fields are present and answers `400 BAD_REQUEST "No fields to update"` when none are
(`services/tenant-provisioning/src/index.ts:455-457`). An empty object is already refused.

**POST /api/v2/verification/verify** — the handler requires at least one of `documentId`,
a content hash, or `documentData`, and answers `400 BAD_REQUEST` otherwise
(`services/originate/src/routes/verificationV2.ts:452-456`). It accepts **four** spellings
of the hash — `hash`, `providedHash`, `contentHash` and `documentHash` — coalesced at
`:450-451`. Each is individually optional, which is exactly why the request *schema* is
unchanged here and only the body-level `required` flag moves.

## What is NOT in this PR, and why — POST /api/referrals/generate
It is deliberately left unmarked. `generateCodeSchema` has four `.optional()` fields
(`services/referral/src/routes/referrals.ts:16-21`) and the route calls
`generateCodeSchema.parse(req.body)` directly (`:61`), so `{}` satisfies the schema and a
body genuinely is not required. Marking it would make the spec disagree with the handler.
An absent-body probe answered 201 for this route, against a replica of the gate rather
than the running app.

The other three left are auth surfaces, excluded by scope: `POST /api/issuer-certs`,
`PATCH /api/users/admin/{id}` and `POST /api/users/me/change-password`.

## What changed — 5 files
- `services/tenant-provisioning/src/tenant-provisioning.openapi.ts` (+1/-0): one
  `required: true` on the PATCH request body.
- `services/originate/src/originate.openapi.ts` (+1/-0): the same on the v2 verify body.
- Two new tests (+48 and +46), one per operation, each rendering the generated document
  and asserting the flag, with three controls apiece.
- `docs/openapi/secuura-api.yaml` (+2/-0): regenerated, taking the count of
  `required: true` body flags from 71 to 73. Not hand-edited.

## Test Evidence

**Touched:** the two `*.openapi.ts` files above, two new tests under each service's
`src/__tests__/`, and `docs/openapi/secuura-api.yaml`.

**Ran** (all local, on this branch's head, after `npm ci --ignore-scripts` at the
`Blockchain/Dev` workspace root plus `npm run build` in `packages/shared`):
- `vitest run` in `services/tenant-provisioning`: BEFORE on a pristine tree at the base
  commit **3 files / 13 tests / 13 passed**; AFTER **4 files / 17 tests / 17 passed**. rc 0 both.
- `jest` in `services/originate`: BEFORE **89 suites / 1058 tests / 1058 passed**; AFTER
  **90 suites / 1062 tests / 1062 passed**. rc 0 both.
- Red-first, by assertion, per operation with only that product hunk reverted:
  tenant-provisioning **1 failed | 3 passed (4)**, originate **1 failed, 3 passed, 4 total**.
  Each red is a real assertion failure and each total stays at 4, so both files load — a
  0-passed-and-0-failed result would have been a load failure rather than a red. Green
  after: 4/4 and 4/4.
- `npm run generate-openapi` rc 0. The regenerated YAML is byte-identical to an independent
  `patch(1)` reconstruction of the same two changes onto the base YAML
  (39,862 lines, sha256 `39f027b63d4aa804`).
- `npm run check:openapi` rc 0 — `CHECK PASS`, and `check-spec-examples` reports 405 example
  blocks all resolving. Control: with the YAML reverted to base the same check goes rc 1
  (`CHECK FAIL`), so the pass is a reading. `--check` wrote nothing.
- `tsc --noEmit` rc 0 for both services, reported as a no-regression reading only.
- Both applied diffs were compared byte-for-byte against an independent `patch(1)` apply of
  the same changes, and each strict `git apply --check` was paired with a tamper that was
  measured to make it fail.
- The pre-push preflight ran in-hook with no `--no-verify`.

**NOT run / NOT covered:**
- No Schemathesis run and no live run against a running stack. The claim is about the
  document the generator publishes, not a response observed on the wire.
- The absent-body behaviour cited above was measured against a **replica** of each gate at
  `body-parser` 1.20.6. The version these services actually lock is **1.20.8** (root,
  originate and tenant-provisioning locks all resolve `body-parser` 1.20.8), so the probe
  and the shipped parser are not the same build.
- The served `/api/docs/openapi.json` was not read; only the generated YAML was compared.
- `tsc` type-checks **neither** new test: tenant-provisioning excludes `src/__tests__`, and
  originate excludes `src/__tests__`, `src/**/*.test.ts` and `src/**/*.integration.test.ts`.
- The four remaining operations are untouched.
- The KS 255 Schemathesis baseline is not re-baselined here, and that estate is not this
  PR's to change.

**Migrations + config:** none. No migration, no schema change, no environment variable, no
lockfile change, no dependency change, no audit-baseline change.

## Sequencing
Lands after PR A (#1367). Both PRs are cut from the same base commit as siblings — this one
is not built on A's branch and is not rebased onto A's merge. Both touch
`docs/openapi/secuura-api.yaml`, but their hunks sit at roughly YAML lines 28,969 / 32,174 /
35,544, so the nearest pair is 3,205 lines apart and their edits never share context.

The tree this PR lands as after A is **`48f5f8afa6ef1f03f2d64e4afa24fd9f75213ad7`**, proved
rather than assumed: `git merge-tree --write-tree` of the two heads reports no conflicts, and
independently assembling that tree (A's head plus this PR's full diff) produces a YAML whose
object id equals the merge-tree's YAML blob exactly, at 39,891 lines and 73 `required: true`
body flags, with `check:openapi` rc 0 on it.

Foreign keys in this description are deliberately written without a hyphen (KS 1015, KS 255,
KS 442) so they neither move nor attach.
