# QA gate: Secuura Platform K PR #1497 (KS-695 ask 3 part ii)

- **Head:** `d2a88a2c2b1e2f620f90b68c774592d5290d0080` (bundle `ks695b_pr1497_d2a88a2c.bundle`, sha256/16 `aa0bb4992acddae3` confirmed; prerequisite `1158045e52b8` came from origin). Two commits: `c171b25f1` (the erasure) and `d2a88a2c2` (the role probe cell).
- **Base used:** current `origin/develop` = `8d34fbf0890a676fdfb4ebf48197382fc42328a2` (KS-1470, one commit past the PR's base `1158045e`). It touches only `api-gateway` (`index.ts`, `middleware/auth.ts`, one new test), none of this PR's files. I gated the merge tree `9f76569a` (a clean local `git merge` of the head into `8d34fbf0`, in my scratch clone).
- Gate: independent Opus, Tier 1 (destructive, GDPR path). Wednesday seat, 2026-10-12.

## VERDICT: NO GO

**Erasing organisation B blanks a document that is attributed to organisation A, and I reproduced it end to end through the real create route and the real erase route.** The selector's connector arm (b) matches `metadata.versionedById`, a field any writer can set, and unlike the lineage arm it has no guard against another organisation's issuer. A one-line fix exists and I tested it (Finding M1). Everything else is in good shape: the author's numbers reproduce exactly on the newer base, atomicity holds at every statement I could fault, and concurrency is clean.

## By my runs

All runs were on the merge tree `9f76569a`, after a fresh `npm ci --ignore-scripts`, `npm run build --workspace=packages/shared` and `cp -R ../../prisma ./prisma && npx prisma generate` in my scratch clone. The database was a throwaway Homebrew PG 15 built by the author's recipe: TCP only on port 55417, data dir in my scratchpad, init SQL applied with 0 failures, 49 migrations applied with 0 failed, and `003_platform_tenancy.sql` applied to the same DB. The product connected as `secuura_app` (`rolsuper=f`, `rolbypassrls=f`), and FORCE RLS was confirmed on `documents`, `organizations`, `svc_api_keys` and `action_provenance`. The DB was stopped at the end.

1. **Author's integration file**, `jest --config jest.integration.config.js ks695-ask3-erase-connector.integration`, run as `secuura_app`: 15/15 with `MULTI_TENANCY_ENABLED=false` and 15/15 with `=true`.
2. **Superuser stand-in** (`TEST_APP_DATABASE_URL` set to the superuser DSN): 1 failed / 14 passed. The failure is the probe cell, which names the role: `connection is "postgres" (superuser=true, bypassrls=true)`. This matches the author.
3. **originate unit** (`npx jest`, twice): 101 suites / 1176 tests, 0 failed, both runs.
4. **packages/shared** (`npx vitest run`, twice): 49 files / 954 tests, 0 failed, both runs.
5. **api-gateway** (`npx vitest run`, twice): 112 files / 1071 tests, 0 failed, both runs. The author's 111 / 1053 was on the older base; KS-1470 adds the extra file and tests.
6. **tsc `--noEmit`**: originate rc 0, shared rc 0, api-gateway rc 0. Shared's only output was an npm `.npmrc` warning.
7. **eslint** on the PR's 7 changed TS files: rc 0, empty output.
8. **`npm run check:openapi`**: rc 0. The output reads `CHECK PASS: on-disk YAML matches generated` and `414 example blocks ... OK`.
9. **My attack file** `gate1497-attack.integration.test.ts`, 12 cells, run as `secuura_app` in both modes. MT=false: 4 red. MT=true: 3 red. The extra MT=false red is the 5 s transaction timeout (Finding m2). Output is in `evidence_attack_runs.txt` and the file is attached as `.txt`.
10. **My end-to-end file** `gate1497-e2e.integration.test.ts`, which drives the real `documentsRouter` and then the real `platformOrganizationsRouter`. Red as both `secuura_app` and superuser. This is Finding M1.
11. **Scale probe** `gate1497-scale.integration.test.ts`, a flat organisation, calling `eraseConnectorOrganisation` directly, `secuura_app`:

    | Documents | MT=false (Prisma) | MT=true (pg pool) |
    |---|---|---|
    | 2,000 | 83 ms | 77 ms |
    | 20,000 | 750 ms | 772 ms |
    | 60,000 | 2,395 ms | 2,273 ms |
    | 140,000 | **error**: `Transaction API error: ... The timeout for this transaction was 5000 ms, however 7029 ms passed`; 140,000 left unblanked, key still active (a clean rollback) | completed in 5,597 ms |

12. **Mutations of my own.** Each was applied by script, proven to land (sha256/16 differs from the original `7d8aa2716e2b46e9`), and the file was restored byte-identical afterwards (sha re-checked).
    - **swallow revoke** (`.catch(() => [])` on step 5): the author's ATOMICITY cell is red in both modes (`Expected: 500, Received: 200`). Data probe `gate1497-m1`: the mutant answers `{"status":"completed","documentsBlanked":1}` while nothing was committed (`title` unchanged, `orgName` unchanged, `keyActive:true`), in both modes.
    - **M2**, `AND is_active = true` dropped from the revoke: the author's REPEAT cell is red.
    - **M3**, `lower()` dropped from the revoke's organisation predicate: **every author file is green** (integration 15/15, unit 44/44). Only my ATTACK 5 (an upper-case stored `organization_id`) is red.
    - **M5**, the tenant predicate dropped from both seed arms: every author file is green as `secuura_app` and also as superuser. It is equivalent for the writes, because the outer `UPDATE ... WHERE tenant_id` still bounds them; only the count could over-read. Not a finding.
    - **M6**, size guard disabled: the unit file is red (1 of 44) and so is my ATTACK 7. The integration file stays green.
    - **FIX1**, the issuer guard added to seed arm (b): my ATTACK 1 and the e2e cell turn green, and the author's integration file stays 15/15.

## Findings

### M1 (MAJOR): another organisation's document is blanked through the caller-controlled `metadata.versionedById`

Seed arm (b) is `d.issuer_organization_id = org OR d.metadata->>'versionedById' = 'connector:<id>'`, in both the count and the UPDATE. It has **no issuer guard**, while lineage arm (c) does have one (`c.issuer_organization_id IS NULL OR = org`). `versionedById` is not server-owned:

- On **create**, `data = { ...rawData, ... }` (`routes/documents.ts` ~line 598), and `saveDocument` stores it as `metadata`. `stripReservedMetadataKeys` removes only `blockchain`, `signatures` and `walletAddress`.
- On **/version**, `/sign-cert` and `/sign-wallet`, `...metadata` is spread **after** `versionedById: user.id` (lines 2101-2108, 2835-2842, 3029-3036), so a caller overrides it.

The connector id is `platform-s:<Organisation GUID>`, which is the externalRef, so it is knowable.

Evidence, from `evidence_attack_runs.txt`, run as `secuura_app`:
- The real create route, as A's connector with `organizationUuid: GUID_A` and `data.versionedById: "connector:platform-s:<GUID_B>"`, returned 201. The row has `issuer = ORG_A` and `vb = connector:platform-s:<GUID_B>`.
- B then erases: `200 {"status":"completed","alreadyErased":false,"documentsBlanked":1}`.
- After that, A's document reads `{"title":"[erased]","issuer":"<ORG_A>","mt":"[erased]"}`. The control document of A (no `versionedById`) is untouched.
- ATTACK 1 (a seeded row, both modes): `GATE AX after B erase {"title":"[erased]","mt":"[erased]","desc":null}`.

This contradicts the PR's own rule, "never one attributed to ANOTHER organisation", and the brief's rule. The change is irreversible: the title and description are gone.

Exploitability is limited, and I want that on record. B cannot reach A's documents on its own. The planting has to come from A's own writer (S's connector for A, or an A-org user with `documents:write`), whether by a bug (for example, S round-tripping a K document's `data`, which carries `versionedById`, into a new create) or on purpose. The same unguarded arm also lets any tenant co-resident with `documents:write` inflate an organisation's reach with NULL-issuer derivatives. That is a way to force a permanent `ORGANISATION_TOO_LARGE` 503 (or the m2 timeout) and block a dissolution.

**Fix (tested as FIX1):** in both copies of the seed CTE, use `OR (d.metadata->>'versionedById' = ${connectorUser} AND (d.issuer_organization_id IS NULL OR d.issuer_organization_id = ${organizationId}::uuid))`. A follow-up for Kam: make `versionedById` a reserved, server-set key (strip it from caller `data`/`metadata`), since this PR turns it into an erasure selector. Add a negative-control cell: an A-issued document carrying B's `versionedById`, erased by B, stays untouched.

### m1 (Minor): `completed` can be answered while the named key stays ACTIVE (erase without revoke)

The ownership check (`resolveOrganisationErasureTarget`) compares with `normaliseOrgId`, which is `trim().toLowerCase()`. The revoke UPDATE matches on `lower(organization_id) = ${organizationId}`, which does **not trim**. Nothing checks `revoked.length`.

Evidence, ATTACK 6: a key whose stored `organization_id` is `ORG_F + ' '` gives `GATE F erase 200 {"status":"completed","alreadyErased":false,...} orgName=[erased] keyActive=true`.

The design note's own invariant says: "the response must be non-terminal (5xx) if the revoke did not happen, never `completed`". I rate it Minor, not Major, because S's keys are minted by `register-connector` from `organizations.id` (a canonical uuid). Only an admin-minted key can trigger it: security's mint accepts `organizationId: z.string()` with no trim. Related test gap: mutation M3 (drop `lower()`) survives every author file.

**Fix:** use the same normaliser on both sides (`lower(btrim(organization_id))`, or re-read with the shared one). Better, after step 5, throw a 5xx unless the named key row is now `is_active = false`.

### m2 (Minor): in the default tenancy mode the 5 s Prisma transaction timeout comes before the 150,000 size guard, and the answer is 500, never 503

`withTenant`'s single-tenant branch uses `getPrismaClient().$transaction(fn)` with no `timeout`, so Prisma's 5,000 ms default applies. `MULTI_TENANCY_ENABLED` defaults to `false` in `docker-compose.yml`.

Measured on a laptop: 140,000 flat documents (under the guard) fail with `The timeout for this transaction was 5000 ms, however 7029 ms passed`. A 2,006-document deep lineage ran 4.9 s to 5.1 s in MODE F and failed on one of my runs (`GATE D erase 500 ... ms=5130`), against 0.2 s in MODE T.

The rollback is clean (nothing written, key still active). But the spec now says 500 means "failed and rolled back ... Retry", and S retries a 5xx without bound, so such an organisation is never erased and never told `ORGANISATION_TOO_LARGE`. The size of production's largest organisation is unknown (Kintsugi's is 3).

**Fix:** pass `{ timeout, maxWait }` to the transaction (sized to the proxy budget), or set the guard from a measured MODE F ceiling. Then add a cell that crosses the timeout.

### m3 (Minor): the lineage arm ignores the selector's own counter-attribution

B's erasure blanks `WA`: a NULL-issuer derivative that **A's** connector made (`versionedById = connector:<A>`) of `YB` (B's derivative of A's own document). Evidence: `GATE lineage after B erase {"A1":"A one.pdf","YB":"[erased]","WA":"[erased]"}`.

`WA`'s title derives from A's document, so blanking it may be the wanted policy. But it is a document the selector itself would attribute to A, and nothing states the rule. Kam should decide; then pin the rule in a cell, or add `AND (c.metadata->>'versionedById' IS NULL OR c.metadata->>'versionedById' = ${connectorUser})`.

### Notes

- **N1.** The spec says "The key it authenticated with is revoked in the same request". The code revokes the **named** `keyId`, and nothing ties it to the authenticating key. Another active key of the same organisation and connector (for example a rotation-grace key) survives by design, and the author pins that in a cell. Also, after the revoke, the gateway's `apiKeyCache` honours the key for up to 60 s (per replica). Within that window the key can still create documents for the erased organisation, and those are not reached. A repeat within 60 s reaches originate and answers `alreadyErased` correctly (my ATTACK 8 and the author's REPEAT cell). This is pre-existing propagation behaviour, but the sentence in the spec overstates it.
- **N2.** The author says "swallow the failing revoke is an equivalent mutant". That is **not** so for the answer. It is data-equivalent (Postgres turns the COMMIT of an aborted transaction into a rollback), but the mutant answers `200 completed documentsBlanked:1` with **nothing** committed: the worst possible answer, because S stops on `completed`. The author's ATOMICITY cell kills it (it asserts 500), so the suite is fine. The wider hazard is `withTenant` itself: any error swallowed inside a callback commits nothing and still returns success. That is pre-existing, and worth one sentence in `db.ts`.
- **N3.** The `decideKeyRevoke` call is effectively a row-exists check for the connector role. Its tenant arm always passes, because the SELECT already binds the tenant. The real organisation and connector bound is `resolveOrganisationErasureTarget` (outside the transaction) plus the UPDATE predicates. My mutations show those predicates are redundant with the pre-check, except for the trim gap in m1. The key row is not re-checked for organisation and connector inside the transaction. That is a theoretical TOCTOU only, since a key's organisation and connector are immutable after mint.
- **N4.** The route requires role `connector` only. The gateway's `subjects:erase` scope is still in grace (KS-843), so today any key of the organisation's connector can erase it. That was the PR (i) design, but it matters now that the route destroys data.
- **N5.** `isOrganisationErased` (the GET) reads the organisation name alone. An organisation literally named `[erased]` reads as `completed`. Separately, `register-connector`'s re-registration refreshes the name (`nameRefreshed`), so S re-registering after dissolution would restore the erased name.
- **N6.** Spec: the operation's 503 description replaces the generic "dependency down" meaning, although the gateway can still answer 503 for an outage. `documentsBlanked` is additive and optional. 501 is gone. A client generated from the old spec keeps working, because S retries any 5xx and ignores unknown fields.

## Answers to the author's five attack points

1. **Selector = union.** A row in two arms at once is counted once: the recursive `UNION` dedups, and my `AX` row (issuer A plus `versionedById` B) was blanked once. A lineage child with NULL issuer under another organisation's parent: B's derivative of A's document is blanked by B, which is correct. But arm (b) itself crosses organisations (M1), and lineage follows children of other connectors (m3). A cycle plus a 2,000-deep chain terminates with the correct count of 2,006, but takes about 5 s in MODE F (m2). Odd `metadata.title` shapes behave correctly: a number or an object becomes `"[erased]"`, an absent key stays absent, and NULL metadata stays NULL with the column blanked. Upper-case stored organisation ids work. Another tenant reusing the same connector id and GUID is untouched (author's cell, reproduced). There is no soft-delete column on `documents`, so that attack does not apply.
2. **Atomicity.** It holds. Forced failures at the documents UPDATE (`500`, name unchanged, key active) and at the organisation rename (`500`, document unchanged, key active) both roll back, like the author's revoke fault. Two concurrent POSTs serialise on the `FOR UPDATE` of the organisation row: `200 {blanked:1, alreadyErased:false}` and `200 {blanked:0, alreadyErased:true}`. The size guard counts **before** any write. The count and the UPDATE are separate statements under READ COMMITTED, so a document inserted between them can be blanked without being counted. That cannot make the guard unsafe, only off by the race. On "swallow the failing revoke": see N2. It is data-equivalent but not answer-equivalent, and the suite kills it.
3. **The cross-service write into `svc_api_keys`.** It is sound against the security service as it stands. KS-1370 makes validate re-read the stored row on a cache hit ("stored-revoked beats cached-active"). Validate's usage write is usage-only. The only upsert that carries `is_active` (`dbSaveApiKey`) is used by mint (new rows) and by revoke (which sets it false). I found no path that writes `true` back over this revoke. What remains is propagation: the gateway's 60 s validate cache (N1). The atomicity gain is real, and the author's ATOMICITY cell proves it under forced RLS.
4. **`decideKeyRevoke` and the bounds, read with hostility.** Correct as stated. For role `connector` the policy adds only the tenant check (N3). The organisation and connector bounds come from the pre-check and the UPDATE predicates. Wrong tenant, wrong organisation, a different connector of the same organisation, a non-connector role (ORG_ADMIN) and another organisation's `keyId` are each answered 403 with nothing written (my AUTH cell plus the author's). The single gap is m1: the trim mismatch between the pre-check and the predicate, which makes the revoke a silent no-op.
5. **Published spec changes.** Additive for a generated client: an optional `documentsBlanked`, a 503 that was already in the response set, and 501 removed. See N6 for the 503 wording, and N1 for the "key it authenticated with" sentence, which should say "the named key".

## GDPR read (what is NOT reached, honestly)

On the documents the selector reaches, the erasure blanks `documents.title`, `documents.description`, `metadata.title` and `metadata.description`, plus `organizations.name`. Measured on my K1 row after the erasure: `{"title":"[erased]","issuerName":"Org K Legal Name Pty Ltd","recipientEmail":"holder@example.test","sIdentity":{"userUuid":...}}`.

What is not reached:

- `metadata.issuerName`, which is **the organisation's name**: S sends `issuerName` top-level per PS-496 and KS-549 stores it in every document. Verify serves `issuer` from it, so after dissolution the erased name is still served on verification.
- `metadata.recipientEmail` (a holder's email).
- `metadata.sIdentity`.
- Every other caller-supplied `data` key.
- `certification_metadata` (it can carry `issuerName`).
- `document_lifecycle_events.payload`, `share_records` / `shares`, `action_provenance` (retained by design), `audit_logs` details, `document_versions`, `svc_analytics_events` target names and webhook payloads.
- Anything anchored on chain (S's Cardano metadatum carries a Title).
- Unattributable documents: the stated limitation.

For comparison, the subject erasure (`gdprService` step 6) replaces the whole `metadata` with `{"anonymized": true}` and scrubs `issuerName` from `certification_metadata`. The PR claims only the four fields plus the name, so this is not a false claim. But the published LIMITATION names only unattributable documents. It should also list `issuerName` and the other copies above, or the erasure should blank `metadata.issuerName` too (I would ask Kam).

## NOT tested

- Any live, Kintsugi, demo or production stack; real S traffic; the real gateway plus security plus auth chain (validate cache, connector-token mint, the KS-1470 front door). The 60 s propagation (N1) is read from code, not measured.
- The `register-connector` path end to end (its uuid-only `organizationId` is read from code), and admin key minting with whitespace through the security service (I seeded the row directly).
- Disk, WAL and RLS cost at production scale; my timings are from a laptop. Behaviour under pgbouncer.
- The integration file of my own under superuser for every cell (the e2e ran both ways; attack and scale ran as `secuura_app`). Schemathesis, Playwright, preflight legs.
- Whether S treats a gateway 401 on a repeat as Confirmed (design Q1, Kam's to put to S).
- The author's five planted mutations themselves (I ran six of my own plus FIX1 instead).
