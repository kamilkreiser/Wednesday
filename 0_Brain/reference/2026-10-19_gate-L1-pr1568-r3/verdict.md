VERDICT: NO GO at head 09588895db75354d829df2069452c82b787d8bc8 (round 3 of 3, so this goes to Kam). Migration 051 closes MAJ-A through all four orphan minters. But its primary-key arm refuses every certification issue and every revoke of an anchored certification (500 at head, 201 and 200 on round 2), and its census counts every certification that has been issued, so it refuses to apply on any box that holds one. MIN-A is also still open: the real Prisma 7.8 error does not have the shape the helper reads, so 050 and 051 both still answer 500 on compose's default path.
sha256/16: 92e27bf688ddaf7f

# Gate L1 verdict: PR 1568 (KS-1612 + KS-1385 (b)), round 3 of 3, Opus tier 1 full

- **Head gated:** `09588895db75354d829df2069452c82b787d8bc8`. **Develop:** `83ed01af70fd5ed6cca9ac66f28ddcb8a1034105`.
  - I ran ls-remote at 20:51:46Z and again at 21:17:09Z. Both times gave these two values, and #1587 at `b5b78b296c86`.
  - The receipts are in `l1/logs/receipts_lsremote_{1,2}.txt`.
- **Setup:** findings only.
  - No git write verb in `!CODING`. No push, no GitHub or Linear write, no Docker.
  - Own `--shared` clone and worktrees under `scratchpad/l1/`. `packages/shared` was built in each worktree (`build_shared_*.log`, rc 0).
  - Own Postgres **15.14** clusters on 127.0.0.1:
    - **55811**: head schema;
    - **55815**: round-2 schema, `767ab5758`;
    - **55816**: develop schema.
  - Each cluster was built the way compose builds one: `docker/init`, then the project's own `scripts/run-migrations.sh`. My copy changes only the glob to an absolute path.
  - Redis, anchoring and originate ran on 55812, 55813 and 55814. lsof showed every port free before use.
  - I did not read J's PGs on 55491 and 55492.
  - `secuura_app` is NOSUPERUSER NOBYPASSRLS. `documents` and `users` are FORCE RLS.
  - The Prisma path ran on an isolated copy of originate's Prisma 7.8.0, generated under `l1/prisma_rig`. The project has no `.prisma` directory, before or after.
- **Evidence:** `scratchpad/l1/` (`scripts/`, `cells/`, `logs/`). Full path: `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/ff943889-d9ba-463a-a66e-300867d673bd/scratchpad/l1/`.
- **Counts:** Major 1 new (MAJ-B). MAJ-A closed. Minor 4 (MIN-A still open; MIN-C, MIN-D, MIN-E). Info 8.

## Why NO GO, in one paragraph
- **MAJ-A is closed as designed.** All four minters J names were tested on the booted services:
  - on round 2 (`767ab5758`) every one is **REWRITTEN**;
  - on head every one is refused with 409, the victim's payload is unchanged, and the victim's verify still serves the victim's identity.
- **The same trigger breaks the certification product (MAJ-B).** `POST /api/certifications/issue` anchors first (`certifications.ts:445`) and writes the `documents` row afterwards (`:518`, `certificationRepo.ts:199`). The row's primary key is already in `anchor_store`, and no row has it as `external_id`, so 051's primary-key arm (`051:140-141`) raises.
  - Every issue answers 500. No certification row is written, and the anchor it already submitted is left as an orphan.
  - Every later `saveCertification` on an anchored certification is refused as well, because it is an `INSERT … ON CONFLICT (id)` and the BEFORE INSERT trigger fires first. That covers revoke, the expiry write and recertify.
  - The census sees the same order on every legitimately issued certification (anchor first, document second). So 051 refuses to apply on any box that has ever issued one.
- **J's cells could not see this.** They insert the document first and anchor it second. No cell in the repo runs 051 at all (MIN-E).
- **MIN-A, the other half of round 3, is not closed.** The helper reads `meta.code`, but the real error carries the code at `meta.driverAdapterError.cause.originalCode`.

## FOUND / TESTED / HOW

### MAJOR

**MAJ-B. 051's primary-key arm refuses every certification issue and every write-back to an anchored certification. Its census then refuses to apply on any database that has an issued certification. New in round 3; round 2 and develop work.**
- **Where:**
  - `migrations/051_documents_cannot_claim_a_live_anchor_id.sql:140-141`: `IF EXISTS (anchor_store.document_id = NEW.id::text) AND NOT EXISTS (documents.external_id = NEW.id::text AND id <> NEW.id) THEN RAISE`. A certification's id is its own primary key, never anyone's `external_id`, so the exemption can never apply to it.
  - The order of the issue route: `routes/certifications.ts:363` sets `id = uuidv4()`. `:445` POSTs it to anchoring, which persists the `anchor_store` row before it answers 202 (`anchoring/src/index.ts`, `await dbPersistAnchor` before `res.status(202)`). Only then does `:518` call `saveCertification`.
  - `repositories/certificationRepo.ts:199-224`: `INSERT INTO documents (id = cert.id …) ON CONFLICT (id) DO UPDATE SET status …`. A BEFORE INSERT row trigger fires before the conflict is arbitrated. So the revoke at `:952`, the expiry write at `:869` and recertify at `:1201` → `:1267` are refused too.
  - Census arm B (`051:117-118`, `a.document_id = d.id::text WHERE a.created_at < d.created_at`) is true for every certification issued this way. On round 2 the anchor was at 21:06:41.576Z and the document at 21:06:41.587Z.
- **TESTED** on booted anchoring and originate, MT=true, vouched (`cells/e2e_r3.ts`, `logs/cell_e2e_r3_{head,r2}_mt.log`), and on the Prisma path (`cells/prisma_r3.ts`, `logs/cell_prisma_r3_{headp,r2p}_single.log`):

  | Cell | Head | Round 2 `767ab5758` |
  |---|---|---|
  | L5 `POST /api/certifications/issue` (real route) | **500** `Failed to issue certification`. 0 documents rows. The anchor row for the id **exists** (a new orphan). Log: `Failed to persist certification to DB {"error":"document id is already held by an anchor record"}` | **201**, row written |
  | L5 on the Prisma path (MT unset) | **500** | **201** |
  | L6 `POST /api/certifications/:id/revoke` on an anchored certification (row first, then anchor) | **500** `Failed to revoke certification`, status stays `certified` | **200** `revoked` |
  | SQL C5: certificationRepo's upsert shape on an anchored cert, as `secuura_app` | `ERROR: document id is already held by an anchor record` | — |
  | SQL C6: control, the same upsert on an unanchored cert | `INSERT 0 1` | — |

- **Census and deploy:**
  - I upgraded the round-2 database to head with the project's runner. Result: `FAILED 051 … 051: 8 documents row(s) …`, runner rc **3** (`logs/run_migrations_r2db_upgrade.log`).
  - Census arm B lists exactly the one certification that was issued legitimately through the real route.
  - Combined with the round-2 INF-5, this has a second effect. The gateway's startup runner logs a failed migration and keeps serving. So on any box with certifications the round-3 guard would run **without** 051, with MAJ-A open.
- **Why the author's evidence misses it:** I grepped the tests at head. No cell in the repo exercises 051. J's reported SQL cells are not in the PR, and the KS-1385 matrix inserts the document before anchoring it.
- **Severity: Major.** It breaks shipped functionality that develop has, it blocks its own deployment, and through the blocked deploy it re-opens MAJ-A.

### MAJ-A, every route to it: CLOSED (gate item 2)
I booted both trees with MT=true, vouched. Tenant A mints the orphan and tenant B is the attacker: first a create with `documentUuid = <orphan>`, then a direct re-anchor with the victim's public hash.

| Minter (tenant A) | Round 2: create / result | Head: create / result |
|---|---|---|
| M1 anchoring `POST /api/anchors` (fresh v4, identity zVICTIM_M1) | 201 / **REWRITTEN** (verify serves zTENANT_B_DIRECT) | **409** `documentUuid is already held by an anchor record and cannot be registered` (131 bytes) / KEPT, payload md5 unchanged, verify zVICTIM_M1 |
| M2 anchoring `POST /api/anchors/batch` | 201 / **REWRITTEN** (payload md5 changed) | 409 / KEPT |
| M3 originate `POST /api/anchors/submit` (server-minted v4) | 201 / **REWRITTEN** | 409 / KEPT |
| M4 originate `POST /api/anchors/` (fresh v4, identity zVICTIM_M4) | 201 / **REWRITTEN** | 409 / KEPT |
| CTL tenant-B create with a fresh v4 | 201, auto-anchor lands | 201, auto-anchor lands |

- **J's corrections, re-checked:**
  - Anchoring's `POST /api/anchoring/submit` (`index.ts:1191-1230`) writes nothing. Confirmed.
  - Originate's `/submit` mints at `anchors.ts:393` and writes at `:442`. Confirmed: M3 leaves rows on both `preprod` and `preview`.
  - `saveAnchorToDb` (`anchors.ts:109-129`) never sets `metadata_payload`. Confirmed.
  - **One nuance:** originate mounts the same router at `/api/anchors` **and** `/api/anchoring` (`originate/src/index.ts:278-279`). So round 2's `originate /api/anchoring/submit` was the same handler, reached directly.
  - Through the gateway, `/api/anchoring` goes to anchoring (`proxy.ts:891`). Originate's `/submit` is reachable there as `/originate/api/anchors/submit` (`proxy.ts:1222`).
- **The hunt for an unnamed writer of `documents.id` or `external_id`:**
  - **Searched, all case-insensitive across `Blockchain/Dev` (`ts js sql sh py mjs cjs`, excluding tests and dist):**
    - `insert into documents`, `update documents`, `copy documents`;
    - Prisma `.document.create|update|upsert|createMany|updateMany`;
    - dynamic `INSERT INTO ${table}`;
    - `session_replication_role`, `disable trigger`, `pg_restore`, `pg_dump`;
    - `anchor_store` writers.
  - **Positive control:** `documentRepo.ts` counts 2 hits for `insert into documents`.
  - **Result:** every writer that sets `id` or `external_id` is an INSERT, which 051 covers:
    - `documentRepo.ts:432,458`;
    - `certificationRepo.ts:199`;
    - `seed-azure-dev.sql`;
    - the demo seed's `batchInsert`, which writes documents before anchors.
  - Every UPDATE site sets other columns only:
    - `documentRepo.ts:619/648`;
    - `certifications.ts:606`;
    - `documents.ts:1962`;
    - `gdprService.ts:735/786`;
    - `connectorOrganisationErasure.ts:405`;
    - `adminConfig.ts:1927`;
    - migration 011;
    - `startup-migrations.ts:710-718`.
  - There are no Prisma model writes, and nothing disables triggers.
  - **SQL battery** (`logs/battery.log`): INSERT, INSERT…SELECT, COPY, UPDATE SET `external_id` and the upsert are all refused. `secuura_app` cannot set `session_replication_role`, `DISABLE TRIGGER` or replace the function.
  - **No uncovered writer found.** The hunt found MAJ-B instead: a covered writer that 051 breaks.
- **Case variant (HC):**
  - Anchoring accepts an upper-case v4. Originate lower-cases `documentUuid`, and 051 compares exact text. So tenant B's create of `lower(X)` is allowed (201) while A's anchor is keyed `UPPER(X)`.
  - A's row is **kept** at head and on round 2, because the guard resolves exact text and nothing re-keys it.
  - Afterwards `verify-by-hash(h)` serves B's identity from B's own lower-case row, which carries the same hash.
  - That uses no guard decision: any caller can anchor a fresh id with a public hash. So I count it as pre-existing, not as this PR's. I did not measure it on develop.

### MINOR

**MIN-A (round 2), still open. The real Prisma error does not reach the 409; both 050 and 051 answer 500 on compose's default path.**
- **Where:**
  - `utils/idNamespaceCollision.ts:53-62` reads `meta.code` and `meta.message`, then falls back to `e.code` (= `'P2010'`).
  - The real shape, Prisma 7.8.0 + PrismaPg, probed through `saveDocument` (`cells/prisma_probe_r3.ts`, `logs/prisma_probe_r3_head.log`): `meta = {driverAdapterError:{name:'DriverAdapterError', cause:{originalCode:'23505', originalMessage:'document id is already held by an anchor record', kind:'UniqueConstraintViolation'}}}`, with `meta.code` absent.
  - So `code` resolves to `'P2010'`, both arms at `:72` and `:75` fail, and both `isIdNamespaceCollision` and `isLiveAnchorIdClaim` return **false**. That holds for 050 and for 051, in skip mode and in upsert mode.
  - The cell's fixture invents a shape the installed Prisma does not produce: `__tests__/ks1612-409-mapping-survives-the-prisma-error-shape.test.ts:44`, `meta: { code, message }`.
- **Booted, MT unset** (`logs/cell_prisma_r3_headp_single.log`):
  - P050 (`documentUuid` = a foreign-tenant primary key): **500**, 89 bytes, `Failed to create document`;
  - P051 (`documentUuid` = an orphan id): **500**, 0 rows landed;
  - PCTL (fresh create): 201.
  - Round 2: P050 500, P051 201.
- **The other half of item 5 holds:**
  - the TS constants equal the live `.sql` RAISE text (the pin cells pass);
  - rewording both RAISEs (mutant S1) or the TS constant (T3) turns the pin red.
- **The pin's limit:** it uses `toContain` over the RAISE list. Rewording only **one** of 051's two RAISEs, the external-id arm that MAJ-A uses, survives (S2).
- **Security holds** (the row is refused). The contract does not: the 500 stays retryable for ever.

**MIN-C. Residual (a), reverse order: measured head-only, but conditional** (`cells/reverse_r3.ts`, `logs/cell_reverse_r3_{head,dev}_rev.log`):
- **R2 is the regression:**
  - Setup: tenant B already has a `documents` row for X, with no anchor (as when the fire-and-forget auto-anchor did not land). Tenant A anchors X with zVICTIM_REV2. Tenant B then anchors X directly with A's public hash.
  - Head: **REWRITTEN**, and verify serves zTENANT_B_REV2.
  - Develop `83ed01af`: **KEPT**.
- **R1 is pre-existing:**
  - Setup: B registers X normally, so its own auto-anchor lands first, and then A anchors X.
  - Result on both trees: A's 202 lands on B's row, B's identity is kept, and verify(A's hash) gives 404.
- **What K's own minters use** (measured from code):
  - `uuid@14.0.1` v4 (`rng.js`: `crypto.getRandomValues`): 122 random bits, from `documents.ts`, `certifications.ts:363` and originate `/submit`;
  - `crypto.randomUUID()` for `anchor_` ids;
  - `doc-${Date.now()}-${uuidv4().slice(0,8)}` (`documents.ts:663`), 32 random bits plus a millisecond time. These cannot be pre-registered, because a `documentUuid` must match `UUID_V4_RE`.
  - So none of K's own ids can be aimed at.
- **What K cannot know:** how S chooses the ids it flat-anchors. The attack needs S's id to be predictable before S anchors it, plus a registration whose own anchor did not land. No measurement inside K bounds that.

**MIN-D. Residual (b), concurrency: both commit** (`scripts/11_race.sh`, `logs/race.log`):
- S1 (owner) opens a transaction, INSERTs an orphan anchor X and holds it for 3 s.
- S2 (`secuura_app`) INSERTs a document claiming X and commits **while S1 is open**. Then S1 commits.
- End state: 1 anchor and 1 claiming document. Census arm A then counts it (1).
- Control: with the anchor committed first, S2 is refused.
- As the header says, the window is larger than 050's because `external_id` is caller-supplied. It still needs the id before the anchor commits, so it reduces to MIN-C's predictability.

**MIN-E. No cell in the repo exercises 051, and five of my mutants survive every owning cell.**
- The grep at head: `documents_cannot_claim_a_live_anchor_id` or `held by an anchor record` appears in no test except the text-pin. The author's "8 SQL cells, 6 SQL mutants" are not in the PR.
- Mutants run on worktree `mut` (`scripts/14_mutants.py`, `logs/mutants.log`, `logs/mutant_r1b.log`); 0 tracked changes after:

  | Mutant | Result |
  |---|---|
  | S2 one RAISE reworded | survived |
  | S3 primary-key arm disabled | survived (and it would make L5/L6 pass) |
  | S4 NOT EXISTS exemption removed | survived |
  | S5 census never refuses | survived |
  | S6 trigger on INSERT only | survived |
  | R1b route 051→409 mapping neutralised (`&& Date.now() < 0`), **whole originate unit suite 1393/1393 green** | survived |
  | T1 / T2 / T3 / S1 | KILLED by the pin cells |
  | C0 comment-only control | survived |

  - The first R1 variant deleted the line. It "killed" only by a compile failure (unused symbols, 1010 of 1393 tests loaded), so I discarded it and replaced it with R1b.

### INFO
- **INF-1. Legitimate flows that hold, identical to round 2** (`e2e_r3`):
  - L1, issuer create: 201. Re-POST with the same bytes: **200**. Re-POST with other bytes: **409** `…registered with different content` (115 bytes). Tenant B with the same id: 409 `…raced a concurrent request; retry` (117, pre-existing). The anchor is kept.
  - L2, lifecycle event (`/:id/lifecycle-events` rename, the issuer's identity): 201, payload **replaced**.
  - L3, the issuer flat-anchors its own registered id (S's fallback path): **replaced**.
  - SQL C3: the NOT EXISTS exemption lets a re-POST-shaped `ON CONFLICT (external_id) DO NOTHING` through (`INSERT 0 0`, no error).
- **INF-2. Behaviour change, for Kam (L4).**
  - Anchoring a fresh v4 and **then** registering it, even by the same issuer with the same bytes, is now a permanent 409. On round 2 the same sequence gives 201.
  - It matters only if S ever flat-anchors before it registers, and K cannot see whether it does.
  - A hard-deleted document's id (`adminConfig.ts:868` deletes documents and leaves their anchors) also becomes unregistrable.
- **INF-3. KS-1385 (b) is unchanged.**
  - The anchoring tree is byte-identical between round 2 and head (`git diff 767ab5758 09588895d -- services/anchoring` is empty).
  - The anchoring unit suite gives 370/371 on both trees. The one red, `threadTokenMint.test.ts`, is the same on both.
  - L2 and L3 above show the issuer's replace. I did not re-run round 2's C1-C8 matrix, because the code it measures is unchanged.
- **INF-4. Residual (c), the `$21` clock.**
  - The live rule is clock-free. The function body has no `created_at`, and orphan anchors stamped 2100-01-01 and 1970-01-02 are both refused (battery C2).
  - The **census** is not clock-free:
    - with the anchor's clock 1 minute ahead of the document's, a planted violation is invisible and 051 applies over it, rc 0, with the violation still present (`logs/migration_051.log`);
    - MAJ-B's false positives come from the same clock ordering.
- **INF-5. 051's apply properties** (`scripts/12_migration.sh`, `logs/migration_051.log`; fresh PG 15, database `mig`):
  - compose order: `applied=53 failed=0`;
  - direct re-apply twice: rc 0, function md5 `71faea5e…` unchanged, 1 trigger. **Idempotent**;
  - runner second pass: `Skipping 051 (already applied)`;
  - as `secuura_app`: refused, rc 3, `must run as a role that bypasses row-level security`;
  - with a planted violation: refused, rc 3. A stub body I put in place beforehand **survived**, which proves nothing was replaced;
  - not callable: `42501` as the app role, `0A000` as the owner. EXECUTE is false for the app role and for PUBLIC. `prosecdef = t`, `search_path = pg_catalog, public`.
- **INF-6. The census counts join rows, not documents.** It reported "8 documents row(s)" for 6 distinct documents, because M3 and M4 leave both a `preview` and a `preprod` anchor row.
- **INF-7. A future-change trap (battery C4).** Any UPDATE that merely lists `external_id` (or `id`) on an anchored document is refused, because the exemption excludes the row itself (`d.id <> NEW.id`). No product code does this today: every UPDATE site was checked, listed under the hunt above.
- **INF-8. Suites, with `packages/shared` rebuilt in my clone** (`logs/suites_summary.txt`):

  | Suite | Head | Round 2 |
  |---|---|---|
  | originate unit | **1393/1393** | 1382/1382 (+11, all new; 0 new failures) |
  | anchoring unit | 370/371 | 370/371 (`threadTokenMint`, pre-existing) |

  - This reproduces the author's counts.

## Gate items, briefly
1. **Delta:** round 3 is one commit, `09588895d`, on round 2's `767ab5758`. It touches exactly the 4 named files (+364/-9, `logs/r3.patch`), and the PR as a whole touches 11 files against the merge base `833984fc9`.
2. **MAJ-A:** closed for every minter (table above). No unnamed writer was found.
3. **Legitimate flows:** INF-1 holds. **The certification path fails (MAJ-B).** Lifecycle and S-shaped events hold. KS-1385 (b) is unchanged.
4. **Residuals:** (a) MIN-C, (b) MIN-D, (c) INF-4.
5. **MIN-A:** not closed (MIN-A above).
6. **051's apply properties:** INF-5. But it **refuses on any database holding a normally issued certification** (MAJ-B).
7. **Mutants and suites:** MIN-E and INF-8.
8. **Merge prediction** on live develop `83ed01af` (`scripts/15_merge.sh`, `logs/merge_prediction.txt`):
   - 0 files in common with develop's 38 files since the merge base. `merge-tree` gives rc 0, tree `5951dafa7ae4`, and the merged tree differs from develop in exactly the PR's 11 files.
   - **#1587 (KS-1628)** shares only `routes/documents.ts`. Its hunk is `-1513,96`; this PR's hunks are at `:31`, `:64`, `:694`, `:716` and `:897-944`. Both orders are clean (rc 0) and give the **same tree**, `9880cacbda0b`.
   - No other PR head numbered #1560 or above shares a file. None adds a migration numbered 05x, and develop has none either.

## NOT tested
- **Preflight:** legs 3, 4 and 8 were not run, because there is no Docker.
- **No real Cardano** and **no gateway**: I sent the vouch header myself.
- **The integration suites** (`jest.integration.config.js`, anchoring's integration vitest) were not run. I ran the unit suites only.
- **Recertify and the expiry write:** concluded from code (the same `saveCertification` upsert as C5 and L6), not driven.
- **Real boxes:** the census on kintsugi and demo, and S's id generator, are not observable from here.
- **Develop on the e2e matrix:** develop was run only for MIN-C. Round 2 is the baseline for everything else.
- **HC's verify-by-hash** behaviour was not measured on develop.
- **Azure's migration role:** whether it has BYPASSRLS was not checked.
- **ESLint** was not run. **tsc** was not run separately; ts-jest compiled every file in the suites.

Merge only on Wednesday's head-bound GO. Round 3 of 3: this NO GO goes to Kam. Nothing deploys from this verdict.

WALL-CLOCK: 31 min (07:51 to 08:22 AEDT, 2026-10-19)
