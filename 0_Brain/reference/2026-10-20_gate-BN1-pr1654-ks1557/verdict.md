VERDICT: NO GO at head db9bca740df0... (tier 1, round 1 of 2; landing tree 932c1e56fc41aa0c63475ba396a63fb6600cf991 on develop 6229a92f2480f0784c31a8d6b652298a7ac10551; 1 blocker, 5 notes)

## BLUF
The code change is right and well defended. Stuart's chain goes from 403 to 201 on both certify paths, the no-`onBehalfOf` hole is closed, the read surface does not change, and all 7 of my mutants were killed. The blocker is in **migration 055**: its "exactly one connector on the parent's `version:*` rows" rule is not fail-closed. If a parent's children were minted by more than one actor but only one actor left a `version:*` row, 055 credits every child to that one connector. Two cases do this: a `/version` sent without `onBehalfOf` writes no row, and `/sign-cert` and `/sign-wallet` write no provenance at all. A connector that did not mint the document then gains certify rights, the GET read-back and the legacy-certify UPDATE on it. I measured this on a real Postgres 15. The ruling refused (b) to avoid exactly this kind of grant. Everything else measured green.

Heads re-read at the end: refs/pull/1654/head = db9bca740df08cd961044e3515a5cf4f2f760354 (unchanged). develop MOVED from 11af03696c9b to **6229a92f2480** (#1653, KS-1677). That commit touches only BACKLOG.md and one m365 test: 0 files under originate/ or migrations/ (control: the same matcher finds the pkce test, count 1). merge-tree on live develop is clean (rc 0) and gives tree 932c1e56fc41. My runs used the landing on 11af03696c9b (tree 85cb4b1d9f71, equal to merge-tree there). The develop delta does not touch any file those runs exercised.

## BLOCKER
**B1 - 055 credits a minted document to a connector that did not mint it (fail-OPEN).** File: `Blockchain/Dev/migrations/055_ks1557_backfill_connector_create_for_versioned_documents.sql`. The LATERAL join counts `DISTINCT connector_id` over the PARENT's `version:%` rows. It never checks that the child was minted by the request that wrote that row. Three facts break the header's claim that 055 "does not GUESS an identity; it copies the one the minting request already recorded one row away":
- `recordOnBehalfOf` returns early with no `onBehalfOf` (`routes/documents.ts:124`). A `/version` sent without obo therefore writes NO parent row.
- `/:id/sign-cert` (`:2905`) and `/:id/sign-wallet` (`:3173`) mint children carrying `metadata.versionAction` ('sign-cert' / 'sign-wallet'), which matches 055's `d.metadata ? 'versionAction'`. Neither route writes any provenance row.
- So one parent can have N children and fewer than N rows, and every child inherits the single connector.

Measured on PG 15.14, fixture built and counted first (26 docs, 14 rows):
- S8: P8 was versioned by C1 with obo (row) giving K8a, and by C2 without obo (no row) giving K8b, whose `versionedById` = C2. After 055: `gx-K8b create:connector C1 ks1557-055-backfill`, so it is credited to the wrong connector.
- S9: P9 was versioned by C1 with obo giving K9a, then signed by a human via `/sign-wallet` giving K9b (`versionedById` = human uuid). After 055: `gx-K9b create:connector C1`, so it is credited to the wrong connector.
- Either connector C1 then passes `wasCreatedByConnector` on that child. That is certify on both paths, the `isCreatingConnector` GET read-back (`documents.ts:1138`), and the legacy-certify `UPDATE documents SET status='certified'` (`certifications.ts:~713`), on a document C1 did not create, possibly in another organisation.
- Exposure: demo is plausibly zero by the author's figure (31 children, 31 distinct parents, 31 rows, so one child per parent). I could not verify that, and **kintsugi is UNMEASURED**, while 055 runs wherever migrations run.
- Not prescribing a fix. Observation only: each child carries its own minter in `metadata.versionedById` (server-set since KS-1508, 2026-10-13; caller-plantable before that). It disagrees with the credited connector in both measured cases, so it is an available discriminator.

## NOTES
- **N1 (Q2, measured, policy not judged): cross-org `/version` now yields certify and read on the MINTED child; nothing on A's original.** Chain (both tenancy modes, develop arm and then landing):
  1. User A creates doc D (owner = A's user).
  2. Org B connector POSTs `/api/documents/D/version` and gets 201 on BOTH arms (KS-1688). The 201 body already echoes A's title on both arms.
  3. The child C (owner = A's user) now carries `create:connector` = B's connector.
  4. B certifies C: lineage **403 -> 201**, legacy **403 -> 201**. The legacy path moves A-owned C from status `draft` to `certified` (develop: stays `draft`).
  5. B GETs C: **404 -> 200**, and the body carries A's data.
  6. Reach into A's ORIGINAL: B GET D = 404 on both arms; B certify D = 403/403 on both arms. The original gains a child at step 2 on BOTH arms (pre-existing KS-1688, not this PR).

  So this PR widens what B can do to its own minted child, which is an A-owned row. It gives B no new reach into D. Refusals on a version-minted document, unchanged on both arms (lineage/legacy): foreign connector, other-org user, same-org non-owner user, same-org OTHER connector and an unrelated recipient are all 403/403. A human of org B who versions gets no row and stays 403/403. The minter goes 403 -> 201. A recipient whose email is in the source's `recipientEmail` (copied into the child's data) is 201/201 on BOTH arms; that is pre-existing and unchanged.
- **N2: 055 depends on the migration role bypassing RLS, and its skip report is invisible to both runners.**
  - Run as a NOBYPASSRLS role (secuura_app): rc 0, "inserted 0 ... skipped 0". With `app.tenant_scope_bypass='platform_admin'` set: 9 inserted. A runner on a non-bypass role would therefore record 055 as applied with 0 rows. The data-migration precedent 044 sets that GUC (`044_vault_entries_repair.sql:94`); 055 does not.
  - `scripts/run-migrations.sh` sends stderr to a file it shows only on failure, and the gateway's `pool.query` ignores notices. So the per-id NOTICE never reaches a deploy log. The claim's own advice to "verify the rows directly" is the only check.
- **N3:** ruling item 3 asked for a cell proving forward / idempotent / reverse. The PR commits none: 5 files, no migration test. The author's 13-assertion cell is in the quarantined probe. I measured it myself (below).
- **N4:** 055 writes `create:connector` naming a HUMAN userId when a human versioned with `onBehalfOf` (S10: `gx-K10 create:connector 99999999-...`). This is inert for access, because both predicate callers require `role === 'connector'`. It does contradict `recordConnectorProvenance`'s rule that "interactive callers write NO row".
- **N5 (scope, not Stuart's chain):** documents minted by `/sign-cert` and `/sign-wallet` still get no `create:connector`. A connector that mints through those routes is still refused certify on its own minted document. Those routes are also B1's second vector.

## FOUND / TESTED / HOW
- **Q1:** `ks1557-lineage-certify` suite is **19/19 at the landing** in BOTH `MULTI_TENANCY_ENABLED=false` and `=true`, as secuura_app (NOSUPERUSER, NOBYPASSRLS; the SETUP cell asserts it). **Develop arm** (the two source files swapped to develop's blobs 6c2386b3 / 483aa9eb, tests unchanged) is 5 failed / 14 passed in BOTH modes. The reds are exactly V1 V2 V4 V5 V6, by assertion (V1/V2 "Expected: 201 Received: 403"; V4/V5/V6 array diff). V3 and the 13 pre-existing cells are green. Restore was asserted by blob hash (d3e7e2a2 / 2cbc4aa0). The no-obo `/version` path also writes the row: in probe Q2a, B versioned without obo, the child got `create:connector`, and the certify was 201.
- **Q2:** see N1. Probe cells Q2a-e were run on both arms and both modes, with identical outcomes per mode.
- **Q3:** the `getCreationProvenance` function text (29 lines) has the same sha256 at develop and at the landing (af923f63...). GET on a version-minted doc: 200, no `createdOnBehalfOf` key, no "pseudonymised" substring. Same for a no-obo connector doc. Positive control: an obo-originated doc still echoes `createdOnBehalfOf {email, displayName, externalRef:null, resolvedUserId:null, pseudonymised:false}` on both arms.
- **Q4 (055 on a real PG 15.14,** my own instance on 127.0.0.1:55871, migrated 001..054 through docker/init + migrations as superuser **secuura**):
  - Forward: 9 inserted. The ambiguous K3a and K3b were skipped, each with its NOTICE naming the external id.
  - Twice-versioned by the same connector: K2a and K2b both got C1.
  - Pre-existing `create:connector` (K4) and literal `create` (K5) were untouched. The certify-derived child (K6, no versionAction) was untouched. A parent with no row (K11) was skipped silently.
  - The tenant comes from the document (K7 lands under T2). `organization_id` comes from `issuer_organization_id`.
  - Literal `create` rows: 1 before and 1 after.
  - Idempotent: run 2 inserted 0, and the totals did not change (23).
  - Reverse `DELETE ... action='create:connector' AND external_ref='ks1557-055-backfill'` removed exactly 9. The pre-existing K4 row survived, and the totals went back to the pre-run 14.
  - Additive: the file has one INSERT, with no UPDATE or DELETE outside the comment.
  - The adversarial S8, S9 and S10 results are B1 and N4.
- **Q5:** the ks1557 file is +107/-0 against develop, so ITEM5c and the 12 other pre-existing cells are byte-unmodified, and ITEM5c is green in both modes. The edited ks1228 cell asserts both rows precisely: `version:watermark` on SOURCE with obo, and `create:connector` with obo null on a non-source `doc-\d+-[0-9a-f]{8}` id. The ks1228 suite is 31/31.
- **Q6:** the full originate unit suite is **134/134 suites, 1568/1568** at the landing AND at develop (src plus ks1228 swapped). Compared by cell NAME, the only difference is the renamed ks1228 control (1 out, 1 in), with 0 status changes. Seven mutants, each with `tsc --noEmit` rc 0 and the restore asserted by hash afterwards:
  - M1 predicate back to create-only: V1 V2 V4 red.
  - M2 `/version` writer removed: V1 V2 V5 V6 and ks1228-two-rows red.
  - M3 writer on the source id: V1 V2 V5 V6 and ks1228 red.
  - M4 constant = literal `create`: V4 V5 V6 and ks1228 red.
  - M5 create-path writer removed: V4 red.
  - M6 predicate ignores connector_id: CREATING-connector control, V3 and V4 red.
  - M7 writer moved before the save: ks1228 "saveDocument throws: 500, no row" and two-rows red (integration green, as expected).

  All reds are assertion failures (`expect(` in each failure message). The "TypeError" lines in the integration logs are the anchoring stub's fetch-refused warnings: 15 of them also appear in the all-green landing run.
- **Q7:** merge-tree is clean on both develops (85cb4b1d at 11af036; 932c1e56 at 6229a92). `tsc --noEmit -p originate` rc 0 at the landing. The two changed test files were type-checked in their own program (scratch tsconfig, jest+node types): rc 0. Positive control: the same program reports 1 `error TS` for an injected bad file. eslint on the 4 changed TS files: rc 0.
- **HOW:** clone `--shared` of the spark cache at `<scratch>/gate_bn1/src`. The cache lacked the PR ref, so I repointed the scratch clone's origin to GitHub with a repo-local `core.sshCommand` (Secuura deploy key, read in place) and fetched develop and the PR ref only, read-only. Git writes ran from scripts with literal paths (the no-cd hook). `npm ci --ignore-scripts`, then shared build and prisma generate. Harness needs not stated in the suite header: the tenant DB needs the `tenants` table (I applied `003_platform_tenancy.sql` to it), and MT=true needs `TEST_PLATFORM_DATABASE_URL` (a scratch platform DB from `docker/init-platform/01-platform-schema.sql`). Without the latter, SETUP reds on `getTenantManager() !== null`, by assertion. Probe file `gatebn1-probe.integration.test.ts` exists only in the scratch clone and was never committed.

## NOT RUN
The PR body's reverse statement was NOT read: no `gh` use under this seat's identity. I verified the identical DELETE in the 055 header and ran it. Not run: Schemathesis, Akto, Playwright, k6. Not run against demo or kintsugi, so B1's real exposure there is unmeasured. Not built: the `migrations` image. Not run through the gateway's `startup-migrations` runner: 055 was applied via psql only. Not tested: concurrency, where a fire-and-forget row could be lost and leave a 403. Docker was not used.

## Wall-clock
10:37:14 to 10:59 AEDT 2026-10-20 (about 22 min).

sha256 (method: `sed '1d;$d' verdict.md | shasum -a 256`): f8b531a439db3f44dc5f908d92852a3cbe94ee99d5d2eafcf154fbcdd03a8853
