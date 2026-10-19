VERDICT: GO WITH NOTE at head c241bb8624bc5e0f49dfb85ec135997da0864c18 (round 1 of 2, tier 1 Opus)

# Gate T1 verdict: PR 1607 (KS-1385 (b), the issuer-field freeze), anchoring BOOTED

- **Head gated:** `c241bb8624bc5e0f49dfb85ec135997da0864c18`. **Develop:** `9512cc70d8c4ad8a1214b17a39d7c48456feb531`.
  - I read both with ls-remote at 03:31:34Z and again at 03:55:21Z. The two reads match.
  - The head is one commit on develop's tip. It touches exactly 4 files, +164/-10.
  - Author and committer are `Kam Kreiser <kamil.kreiser@secuura.ai>`.
- **Setup:** findings only.
  - I made no change under `!CODING`: the project checkout has 0 tracked changes, before and after.
  - No push, no GitHub or Linear write, no Docker, no real Cardano network, no `cd`, no `rm`.
- **Scratch:** everything is under `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/c4419525-d2e2-49d0-8b3f-577263d823bb/scratchpad/t1/`, in `scripts/`, `cells/`, `logs/`, `wt/` and `repo/`.
  - My own Postgres 15 was on port 55881, built with gate P1's mkpg method. That is compose's order: `docker/init-platform`, `01-create-app-role.sh`, `docker/init/*.sql`, then the project's own `run-migrations.sh`, with its relative glob made absolute and nothing else changed. Result: `applied=53 failed=0`.
  - Redis ran on 55882 and anchoring on 55883. All three ports were free before use, and all three are stopped now. I never touched J's ports.
- **Counts:** Major 0. Minor 2 (MIN-1, MIN-2). Info 7.

## Why GO WITH NOTE
- **With anchoring booted, the ruling holds end to end:**
  - the holder organisation's re-anchor keeps the issuer's four fields;
  - verify, `GET /api/anchors/:id` and the metadatum the real submitter hands the chain layer all carry the issuer's four fields beside the holder's actor;
  - every control behaves as specified.
- **The same cell on develop shows the defect.** That is the inverted control.
- **Nothing widens who the guard admits.**
- **What keeps this from a plain GO:**
  - MIN-1: the new SQL raises on a stored `secuura` value that is not an object. No writer in the census produces such a row today.
  - MIN-2: one mutant survives the whole committed suite. Only my booted cell kills it.

## Q1. The booted scenario
**HOW:**
- **Services:** real anchoring, booted with tsx, as `secuura_app` on the FORCE-RLS schema, with RS256 JWTs. `DEMO_MODE=true`, so the real submitter path runs: `createAnchorSubmitter` → `getAnchor` (`index.ts:1770`, the stored row) → `submitAnchor`.
- **Payload capture:** a preload records the payload at `MockAnchoringProvider.submitAnchor`. It runs that payload through the expression at `transaction.ts:114` (`JSON.stringify(toCardanoMetadatum(payload))`, using the product's codec) and CSL's BasicConversions encode/decode. That gives "chain4" below.
- **Harness stub, stated:** `waitForConfirmation` is replaced by an immediate "confirmed". Without a Blockfrost provider, the real one holds the wallet lock for minutes, and no second anchor would ever be submitted.
- **Not executed:** `buildAnchorTransaction` itself, which needs UTxOs and a wallet.
- **Files:** `cells/booted.ts`, `scripts/07_boot.sh`, `scripts/capture_preload.cjs`. Logs: `logs/cell_booted_land2.log` (head) and `logs/cell_booted_dev1.log` (develop).
- **Seed:** the document carries `issuer_organization_id = ORG_ISS`. Its custodian user is in `ORG_HOLD`, and HOLDER is a colleague in `ORG_HOLD` (Kam's (c)).

| Cell | HEAD: stored four / actor | HEAD: verify-by-hash (four / actor) | HEAD: chain4 / chain actor (submission #) | DEVELOP (the control) |
|---|---|---|---|---|
| S1a issuer anchors (`org-issuer-x`, `zORGISSUER`, government, true; `zISSUERACTOR`) | the issuer's | 200 verified, the issuer's / `zISSUERACTOR` | the issuer's (`orgVerified:"true"`) / `zISSUERACTOR` (#1) | same |
| **S1b holder re-anchors (`org-holder-x`, `zORGHOLDER`, unverified, false; `zHOLDERACTOR`)** | **the issuer's four / `zHOLDERACTOR`** | **200, the issuer's four / `zHOLDERACTOR`**; GET by id: the same | **the issuer's four / `zHOLDERACTOR` (#2)** | **the holder's four everywhere, including chain4 (the defect)** |
| C1b → C1c: issuer re-anchors after a held holder event, with NEW four | replaced (`org-issuer-x2`, `zORGISSUER2`, kyc, false) | replaced | replaced (#3) | replaced |
| C2b refused third org (other four + actor) | payload md5 unchanged (`d304bfd058`) | the issuer's, unchanged | the stored (issuer's) payload (#2, see INF-2) | same |
| C3b holder sends only actor fields · C3c holder sends no identity at all | four kept · four kept, actor removed | four kept | four kept | **four ERASED** (`{}`) |
| C4a/b first anchored without the four, then the holder sends all four | stays `{}` | `{}` | `{}` | **holder's four GAINED** |
| E1 no-issuer row (every certification): holder org first-anchors, then re-anchors with different four | first four kept | kept | kept | replaced |
| B1 holder BATCH onto the single row | unchanged (single, the issuer's) | — | — | same |

- **Responses:** every POST answered 202. With anchoring booted, the answer to Q1 is **YES on every arm**. Each control fires.

## Q2. No widening
- **The guard file:** `git diff develop..head -- anchorOverwriteGuard.ts` is **+17/-0**. It adds only `ISSUER_FIELDS` (`:148`) and `holdsIssuerFields` (`:151-153`). These are byte-identical to develop, because the diff has no `-` line:
  - `decideMetadataOverwrite`, `mayOverwriteStoredMetadata`, `readOwningDocument`, `isQuietKeep`, `isUuidShaped`;
  - `CUSTODY_OPTION = 'c'`, which is the earlier custody card's (c), not this card's.
- **`index.ts`:** the only hunks are the import (`:53`), the inner `CASE` (`:1430-1441`), `RETURNING` (`:1450-1454`), the `$24`/`$25` binds (`:1489-1491`) and the log split (`:1494-1506`, `:1519`). The guard call and `overwrite.allow` are unchanged.
- **`holdsIssuerFields` only reads a decision:** it can only change what an already-admitted write stores.
- **Option (c) is not implemented.** No line admits the issuing organisation on a certification row (a no-issuer row). In E1 and in the C2b refusal it is still refused, exactly as on develop.

## Q3. Census of writers of `metadata_payload` after the first anchor
**HOW:** `git grep` over the WHOLE head tree, every service, `scripts/`, `docker/`, `migrations/`, `deployment/` and `systemTest/`, with tests included. I searched:
- `metadata_payload`, `metadataPayload`;
- `INSERT|UPDATE|COPY|MERGE … anchor_store`, case-insensitive;
- `jsonb_set|jsonb_insert`;
- the Prisma models.

**Control:** the known writer, `index.ts:1372`, is found by the same pattern.

**FOUND:** J is right. Exactly ONE statement changes `metadata_payload` after the first anchor: `index.ts:1372`, through its `CASE` at `:1426`. The others:
- `anchorStatusUpdate.ts:114` reads `metadata_payload` only in its WHERE;
- `index.ts:1789` sets `retry_count` only;
- originate `anchors.ts:109` (`saveAnchorToDb`) has no `metadata_payload` (INF-7);
- `migrations/003:45`, `docker/init/06:62` and `deployment/azure/migrate/init.sql:2081` copy `blockchain_anchors` without the payload column;
- `migrations/007:16` and `031:28` are one-time dedupe DELETEs;
- the demo seed (`demo-service/src/seed/index.ts:162`) does an initial INSERT without the payload;
- `DEPLOYMENT-ARCHITECTURE.md:119` is runbook SQL that sets `simulated` only;
- Prisma's `BlockchainAnchor` maps to `blockchain_anchors`, which those consolidations drop, and no code uses it.

**No writer was missed.**

## Q4. The SQL merge
**HOW:** `cells/q4.ts` (`logs/q4_head.log`, `logs/q4_dev.log`). It runs the product's own statement, extracted from `index.ts` as the harness extracts it, with a holder-shaped payload, against planted stored rows, on both trees.

| Stored row | holder (`$23` t, `$24` t) | issuer (`$24` f) | refused (`$23` f) | develop, all three |
|---|---|---|---|---|
| normal object | OK, held | OK | OK, kept | OK |
| SQL NULL payload · `{}` (no `secuura`) · payload a JSON array · payload a JSON string | OK: absent stays absent; the result is the incoming payload minus the four | OK | OK, except the string payload under refused: **RAISE 22023** | OK |
| **`secuura` = JSON null, a string, an array, or a number** | **RAISE 22023 `cannot call jsonb_each on a non-object`** | OK | **RAISE 22023 `cannot delete from scalar`** for null, string and number (an array is OK) | OK (202) |
| fresh INSERT whose incoming `secuura` = null | — | **RAISE** (the `RETURNING` arm runs on every row) | — | OK |

- **Answer:** yes, there are paths where it raises. A raise propagates and becomes a 5xx, because `dbPersistAnchor` has no catch.
- **No current writer produces those stored or incoming shapes:**
  - every product builder emits `secuura` as an object (`anchorSchema.ts:262-316`, batch `index.ts:779`);
  - every other writer leaves the payload NULL (Q3).
- **So it is not reachable today.** See MIN-1.

## Q5. The 202 and the one info line
- **Responses:** head and develop both answer **202** on every arm, with the same `data` key set (`contentHash, createdAt, documentId, id, message, metadataLabel, network, status`) and the same message. No refusal was introduced. Booted, `logs/cell_booted_*`.
- **Log lines** (`logs/anchoring_boot_land2.log` against `dev1`):
  - **6** info lines `KS-1385 (b): applied the update and kept the first-anchored issuer fields`. They are exactly S1b, C1b, C3b, C3c, C4b and E1b, the six held updates. Develop has 0;
  - **2** warnings `kept the stored anchor metadata`, on BOTH trees: C2b (refused) and B1b (batch onto single). So the warning still fires only for real keeps.
- **Change in Q4's shapes:** the refused-caller keep that develop answers 202 becomes a 500 (MIN-1).

## Q6. Mutants
**HOW:** `scripts/mutants.py`, `logs/mutants.log`.
- Each mutant ran the KS-1385 integration trio (all 64 cells loaded every time).
- Each "T" mutant also ran the booted cell.
- After every mutant I verified the sha256 restore: `index.ts 901932eef141…`, guard `1cdcefc552da…`. Both worktrees are clean.

| Mutant | Result |
|---|---|
| C0 comment-only control | survives (64/64) |
| M1 `$24` bound `false` | KILLED (W2) |
| M2 `$24` bound `true` | KILLED (W1, W2) |
| M3 `orgVerified` dropped from the list | KILLED (I1, I2, I4, I5, I7) |
| M4 merge takes the INCOMING four (develop's behaviour) | KILLED (I1-I4) |
| M5 the incoming four not stripped | KILLED (I3) |
| M6 `allow` ignored | KILLED (I7) |
| M7 the bind commented out | KILLED (W2) |
| M8 `rest_is_incoming` compares the whole payload | KILLED (I1) |
| T2 (mine) the hold applied to the issuer, not the custodian | KILLED (I1-I5, I7); booted S1b serves the holder's four |
| T3 (mine) `$24`/`$25` swapped in the product only | KILLED (W2); booted: every re-anchor answers **500** |
| T4 (mine) `WHEN NOT $24` | KILLED (I1-I5); booted serves the holder's four |
| **T1 (mine, aimed at the booted path) `heldIssuerFields` forced false** | **SURVIVES the whole suite (64/64)**. Killed ONLY by the booted cell (info 6 → 0, warn 2 → 8). See MIN-2 |

- **J's 8 equivalents:** 8 of 8 killed.

## Q7. The `beforeAll` timeout
- **Not reproduced.** 0 hook timeouts in **37** vitest runs of the trio, including the 5 serial head passes (64/64 each) and 13 mutant runs.
- **Root cause: UNMEASURED,** because I could not reproduce it.
- **One fact that fits:** neither `vitest.integration.config.ts` nor the file sets `hookTimeout`, so vitest's default of 10 s applies. That matches J's "10 s".
- **The suspect hook** is the FORCE-RLS file's `beforeAll` (`ks1385-guard-reads-under-force-rls…:45-72`). It does a cold dynamic `import('../anchorOverwriteGuard')`. This is a hypothesis, not measured.
- **Related artifacts (INF-5):**
  - Running three vitest processes concurrently against ONE database collides on the files' deterministic anchor ids (`anchor_store_pkey` 23505). This happens equally on develop (`logs/par_summary.txt`), so that kind of "parallel" run is not a valid lane.
  - Develop showed one R4 red in 2 serial runs (`stored-identity…:250`).

## Q8. NOT tested
- **Anchoring's other suites:** unit was RUN (head 379/380 and develop 379/380, the same red `threadTokenMint.test.ts`, KS-562); tsc rc 0 on both trees.
  - The integration lane contains only the 3 KS-1385 files, and all 3 were run.
  - Not run: ESLint, and the four platform suites (no Docker).
  - Not run: preflight legs 3, 4 and 8.
- **Originate:** not booted, and its suites were not run.
  - The PR does not touch it, but originate's anchoring hop (`x-emitter-internal` lifecycle/share/transfer emits, `documents.ts:895`) is how the holder's real events reach anchoring.
  - Through that hop, the HOLDER verbs were not driven. I posted to `/api/anchors` directly with the holder's JWT.
- **Not tested:**
  - the gateway;
  - real Cardano;
  - `buildAnchorTransaction`/CSL `add_json_metadatum_with_schema` on a real builder (I used CSL's encode and decode of the same JSON);
  - multi-tenant mode;
  - Prisma;
  - real boxes and their stored rows (MIN-1's reachability on real data).
- **The issuer-hop holder flows from Platform S** were not tested.

## Q9. Landing tree and overlap
- **Landing tree:** `merge-tree --write-tree develop head` gives rc 0, tree **`a0d111da8b18`**, equal to the head tree. That is J's prediction, while develop stays at `9512cc70d8c4`.
  - The landing commit in my scratch clone is `7ed19bde7`. It exists in the scratch clone only and was never pushed.
- **#995:** its index.ts hunk is at **-508,3** (J said -505), in the POST handler, disjoint from `:1426-1506`.
  - #995 ALREADY conflicts with develop in `originate/src/index.ts`. The conflict set is identical with or without #1607, so #1607 adds nothing to it.
- **Other PRs:**
  - #1105, #805 and #728 have the same conflict set with and without #1607;
  - the newest PRs (#1597 KS-1634, which touches `originate/routes/verification.ts`, a reader of the four fields, and #1606) merge cleanly onto develop+#1607;
  - of all 1528 PR heads fetched, the only ones not in develop that touch any of the 4 files are #1549 (10-15, superseded), #1568 (landed as squash `04a4a3393`) and #1607 itself.
- **Limit:** I cannot see which PRs are open, so I did not use GitHub's API. I did not identify "the R lane's" PRs by name. None of the PRs from 10-18 and 10-19 touches the 4 files.

## Severities

**MIN-1. The issuer-field merge and its `RETURNING` arm raise 22023 when a stored or incoming `secuura` is not an object.**
- **Where:**
  - `index.ts:1438`: `jsonb_each` on a non-object, on the holder path;
  - `index.ts:1453-1454`: `- $25::text[]` on a scalar. It sits in `RETURNING`, so it runs for EVERY caller, refused ones included, and on a fresh INSERT.
- **Effect:**
  - a legitimate holder's re-anchor answers 500 instead of applying;
  - a refused caller's re-anchor that develop answers 202 (a quiet keep) now answers 500.
- **Not reachable today:** no writer in the Q3 census produces such a row or payload. Only out-of-band or legacy data could.
- **Not blocking.** A `jsonb_typeof(...) = 'object'` guard would close it. That is the author's call.

**MIN-2. The info/warn log split is pinned by source text only.**
- **Where:** `index.ts:1497`.
- **Evidence:** mutant T1 (`heldIssuerFields` forced false) passes all 64 cells. W4 still matches the `if` line, and I1 checks the SQL flag, not the TS conjunction. Under T1, every held holder update logs the "kept the stored anchor metadata" WARNING, which is false. The booted cell measured 8 warnings against 2.
- **Severity:** a test gap. The behaviour on the head is correct, as measured.

**INFO**
- **INF-1 (for Kam's awareness, consistent with the ruling's text):**
  - on a no-issuer row, which includes every certification, the custodian organisation is the only admitted party, and it is HELD;
  - so after the first anchor, nobody can ever change the four. That includes the holder correcting its own (E1) and the issuing organisation, which stays refused because option (c) was not chosen;
  - "as first anchored" therefore means "permanently" on certifications.
- **INF-2 (pre-existing, identical on develop):** a REFUSED caller's re-anchor keeps the payload, but the upsert still resets status and `transaction_hash` (`:1378-1388`, unconditional). That triggers a fresh chain submission of the stored payload: C2b is submission #2 on both trees. This is KS-1603 territory and is not changed here.
- **INF-3:** "issuer" in the hold means `documents.issuer_organization_id`, not the payload's `issuerOrgId`. If the issuer and custodian organisations are the same, the issuer branch wins, so latest event wins.
- **INF-4:** the J nits:
  - #995 is at -508, not -505;
  - originate `anchors.ts:109` is a 10-column INSERT whose DO UPDATE sets 6 columns, including `content_hash` (not the payload);
  - the main integration file must be run with TEST_DATABASE_URL = the owner; run as `secuura_app`, its fixtures fail RLS (`logs/int_head_app_1.log`). Only the FORCE-RLS file uses `secuura_app`.
- **INF-5:** cross-process runs on one database collide (Q7). Develop's R4 (`stored-identity…:250`) failed once in 2 serial runs, and 0 times in the head's runs. A plausible cause, inferred and not measured: a same-millisecond `timestamp`, so the "rebuilt" payload equals the stored one.
- **INF-6:** `issuerName` is not anchored (KS-240, `anchorSchema.ts:277`), so it does not escape the four.
- **INF-7:** the booted run creates `anchor_batches` the way compose's api-gateway does. With `secuura_app` and no CREATE right, anchoring cannot make it itself (`index.ts:1285`), which is expected.

Merge only on Wednesday's head-bound GO. Nothing deploys from this verdict.

MODEL: claude-opus-5-5
WALL-CLOCK: 27 min (03:30Z to 03:57Z, 2026-10-19)
sha256: 39a82680531b2942367810cc3f34b3b9686079a4cd3c1350f4321e6a7268856b (of this file with its first and last lines removed: sed '1d;$d' | shasum -a 256)
