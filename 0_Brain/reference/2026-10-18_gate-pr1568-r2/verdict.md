VERDICT: NO GO at head 767ab575818f75b68664ddad1a511478db63c09d (round 2 of 2, the cap). Migration 050 closes round 1's MAJ-1 exactly as ruled, and MIN-1 and MIN-2 are closed. But the same guard change still lets any tenant rewrite another tenant's anchored identity through a third id namespace that 050 cannot see: anchor_store rows whose id names no documents row, which originate's own /api/anchoring/submit mints on every call. On develop, the same attempt keeps the identity.
REPORT-SHA256/16: 3486a4efab9b5d1f

# Gate verdict: PR 1568 (KS-1612 + KS-1385 (b)), round 2 of 2, Opus tier 1 full

- **Head gated:** `767ab575818f75b68664ddad1a511478db63c09d`. My own ls-remote returned it as `refs/pull/1568/head` at 11:00:01Z and again at 11:30:58Z (`evidence/logs/receipts_lsremote_{1,2}.txt`). Its commits are `7408f5ec5`, `16e716103`, `938500c80` (round 2), the merge `6c30a6df4` (develop `833984fc9`), and `767ab5758`.
- **Base:** the merge base with develop is `833984fc9`, as the brief says. Against it the PR touches exactly 9 files (`evidence/logs/diff_stat_vs_833984.txt`, `pr.patch`).
- **Develop moved during the gate:**
  - The brief named `26378a403`.
  - At 11:00Z it was `9251ae54d` (#1571), and the develop arms ran on that.
  - At 11:30Z it was `db9bd1602` (#1570), and the merge prediction ran on that.
  - None of the three commits touches anchoring, the guard, documents.ts, the repositories or migrations.
- **Setup:**
  - Findings only. No git write verb in `!CODING`, no push, no GitHub or Linear write, no Docker.
  - Own `--shared` clone and worktrees under `/private/tmp/claude-501/gate1568r2/`.
  - Own Postgres 18 on 127.0.0.1:55731 (lsof showed it free; 55418 untouched). Own redis on 55732, anchoring on 55733, originate on 55734.
  - `secuura_app` is NOSUPERUSER NOBYPASSRLS. `documents` and `users` are FORCE RLS.
  - The schema was built as compose builds it: `docker/init`, then the project's own `scripts/run-migrations.sh`. My copy changes only its `migrations/*.sql` glob to an absolute path, because I may not cd (`evidence/scripts/04_pg.sh`).
  - The Prisma path (`MULTI_TENANCY_ENABLED` unset) was run on an isolated copy of originate's installed Prisma 7.8.0, generated under my scratch. The project's `node_modules` is untouched: still no `.prisma` (`scripts/05_prisma_rig.sh`, `05b_…`, `06_headp.sh`).
- **Counts:** Major 1 · Minor 2 · Info 10.
- **Evidence:** `evidence/` next to this file, split into `scripts/`, `cells/` and `logs/`.

## Why NO GO, in one paragraph
- **What 050 fixed.** It makes the two `documents` namespaces (`id` and `external_id`) disjoint. That closes the path round 1 measured: XT1 and XT2 now get a 409, nothing lands, and public verify keeps the victim's identity.
- **What the guard really needs.** The guard's safety needs a different property: "this anchor_store row is my document's". `anchor_store.document_id` is a third namespace, global text with no tenant column, and it holds ids that are in **no** documents row:
  - originate's `POST /api/anchoring/submit` mints `documentId = uuidv4()` for every hash-only submission, and never writes a documents row;
  - originate's `POST /api/anchors` forwards any v4 the caller sends.
- **The attack.** Any document-writer in any tenant registers `documentUuid = <that id>`. 050 lets it through, because no documents row holds that value. The create's own anchor then reaches the guard. The guard resolves the attacker's fresh row by `external_id` and allows the attacker's issuer organisation, so the victim's stored payload is replaced.
- **What I measured** on the booted services:
  - The victim's public verify-by-hash afterwards serves the attacker's identity.
  - On develop, the same sequence keeps the victim's identity.
- **Why it cannot be split off.** This is round 1's MAJ-1 again, through a namespace the ruling did not cover. It comes from the same `external_id` arm that delivers Kam's rulings, so the closed instances cannot ship without it.

## What would block, plainly
- **MAJ-A is the only blocker.**
- **Shipping head as-is** ("the closed instances ship and the residue is ticketed") would ship a cross-tenant rewrite of anchored identity that live develop does not have. That is the same class of harm as round 1's MAJ-1, so it is Kam's call, not a residue.
- **Everything else below** is Minor or Info, and would not block on its own.

---

## FOUND / TESTED / HOW

### MAJOR

**MAJ-A. Cross-tenant (and cross-organisation) rewrite of the anchored identity on any `anchor_store` row whose id names no `documents` row (orphan anchors). The guard's `external_id` arm is new at head, and 050 cannot see these rows.**
- **Where:**
  - The guard:
    - `services/anchoring/src/anchorOverwriteGuard.ts:258-260`: `WHERE d.tenant_id = $2::uuid AND (d.external_id = $1 OR d.id = $3::uuid)`. It proves only that the id names a document in the caller's tenant.
    - Its decision is applied at `index.ts:1369` (`$23`) to whatever row `ON CONFLICT (document_id, network)` finds, and that row is not tenant-scoped.
  - The design claim this contradicts: guard header `:21-25`, "Each one added is a positively confirmed event of a document in the caller's own tenant … migration 050 makes that impossible database-wide".
  - Where orphan rows come from:
    - `services/originate/src/routes/anchors.ts:394` (`/submit`: `const documentId = require('uuid').v4()`, no documents row, no identity block);
    - `anchors.ts:255-262` (`POST /api/anchors` forwards the caller's `documentId` after only an `anchorExistsInDb` check).
  - The attacker's write:
    - `routes/documents.ts:658` (`id = documentUuid`);
    - `documentRepo.ts:437-438` (`external_id = documentUuid`);
    - `routes/documents.ts:918-925` (the create's anchor sends `documentId: id` plus the caller's `identity`).
  - Why 050 does not stop it: `050:80-87` checks only `documents`.
  - The id is public. `GET /api/anchors/verify/:hash` returns it as `metadata.documentId` (measured: `documentIdInBody`).
- **TESTED, with originate and anchoring both booted** (`cells/e2e_r2.ts`, `scripts/07_boot.sh`). Setup:
  - real routes, `secuura_app`, FORCE RLS, RS256, mock chain;
  - `MULTI_TENANCY_ENABLED=true` with two tenants in a platform DB;
  - the gateway's vouch header, so `x-tenant-id` is honoured.

  | Cell | Victim (tenant A) | Attacker (tenant B, its own org) | Head | Develop `9251ae54d` |
  |---|---|---|---|---|
  | XT3 | `POST /api/anchoring/submit {documentHash: H}`, the real route; anchor row U, created 11:21:59.164Z, identity none | `POST /api/documents {documentUuid: U, contentHash: H, organizationUuid: ORG_TB, identity: zTENANT_B_ATTACKER}` | 201; the **same** row (created 11:21:59.164Z) now carries `actorDid zTENANT_B_ATTACKER` and `issuerOrgId` ORG_TB. **verify-by-hash(H): `verified:true`, identity zTENANT_B_ATTACKER** | 201; identity **kept** (none); verify unchanged |
  | XT4 | `POST /api/anchors {documentId: <fresh v4>, identity: zVICTIM4}` through originate | same | 201; **REWRITTEN**. verify(H) before `zVICTIM4`, after `zTENANT_B_ATTACKER` | 201; **kept** `zVICTIM4` |

  Logs: `logs/cell_e2e_r2_head_mt.log` and `logs/cell_e2e_r2_dev_mt.log`. The stored rows are queried by `network = 'preprod'`, anchoring's row.
- **Single-tenant compose mode** (`MULTI_TENANCY_ENABLED` unset, the compose default `docker-compose.yml:583`; `logs/cell_e2e_r2_head_single.log`):
  - Every caller is in the default tenant, so the attacker is simply another organisation.
  - XT3 and XT4 are **REWRITTEN** at head.
  - Develop was not run in this mode; that it keeps rests on its guard reading the primary key only.
- **No log line.** The rewrite is an *allowed* overwrite, so the kept-payload warning never fires.
- **What the attacker needs:** a document-writer account in any tenant (or any other organisation, on a single-tenant box), plus the victim's content hash. The hash gives up the id through public verify, and the guard requires an equal `content_hash`, which the attacker supplies.
- **What I did not establish:** how many orphan uuid rows exist on kintsugi or demo. The census in 050's header does not count them. The `/submit` comment (`anchors.ts:405-410`, "one Platform-S does not send an `identity` block to" at :408) says this is a hash-only contract that Platform S uses.
- **Why the author's cells and mutants cannot see it:** every XT cell and every 050 cell gives the victim a `documents` row.
- **Residue options (findings, not a fix):**
  - The guard could refuse when the stored row predates the owning document: `anchor_store.created_at < documents.created_at`. That is the same read, and needs no cross-tenant lookup.
  - Or 050's trigger could also refuse an `external_id` that is already an `anchor_store.document_id`. That would need its own census of existing anchor rows, and a check that no flow anchors before it registers.
  - Or KS-1384 (a tenant column on `anchor_store`).
  - Each option needs a cell where the victim has no documents row.

### MINOR

**MIN-A. On compose's default configuration, migration 050's refusal answers 500, not the ruled 409. The constraint name is lost before the route sees it.**
- **Where:**
  - `utils/idNamespaceCollision.ts:14` requires `e.code === '23505' && e.constraint === …`.
  - With `MULTI_TENANCY_ENABLED` unset, `db.ts:286-291` gives the route the real PrismaClient over `@prisma/adapter-pg` (compose default, `docker-compose.yml:583`).
  - Prisma throws `PrismaClientKnownRequestError`:
    - `code: 'P2010'`;
    - `meta.driverAdapterError.cause = {originalCode:'23505', kind:'UniqueConstraintViolation'}`;
    - **no constraint field anywhere.** The adapter derives `constraint` only from a `Key (…)` detail (`@prisma/adapter-pg/dist/index.js:472-477`), and the trigger raises none.
- **TESTED:**
  - `cells/prisma_probe.ts`, `logs/prisma_probe_head.log`: saveDocument in skip and upsert mode, `isIdNamespaceCollision → false` both times, 0 rows landed.
  - The booted route in this mode answered `500 {"code":"INTERNAL_ERROR","message":"Failed to create document"}` (89 bytes) to a cross-tenant pkey collision (`logs/cell_e2e_r2_head_mtfalse.log` XT1/XT2, `originate_boot_head_mtfalse.log`: "Raw query failed. Code: `23505`").
  - With `MULTI_TENANCY_ENABLED=true` (pg pool proxy) the mapping works, byte for byte (item 1).
- **Impact:**
  - Security holds; the row is refused in both modes.
  - The contract breaks: a retryable 500 replaces a terminal 409, so a client like Platform S that retries 5xx will retry for ever.
  - On a genuinely single-tenant box this path is reached only when a row in another tenant collides, because `respondForExisting` catches same-tenant shadows first.
- **Why the cells miss it:** the author's ks1612 integration cells drive `createPoolProxy(pool)` directly in both "MT" modes, and the route cells mock a pg-shaped error.

**MIN-B. The trigger is not symmetric, so it lets in rows that 050's own census counts.**
- **Where:**
  - The forward arm casts and is case-insensitive (`050:80-81`, `~*` then `::uuid`).
  - The reverse arm is exact text (`050:85`, `d.external_id = NEW.id::text`).
  - The census is the forward relation (`050:41-46`, `:65-69`).
- **TESTED** (`cells/trigger_battery.ts`, `logs/trigger_battery.log`):
  - R2/A1: an existing `external_id = UPPER(e)`, then an INSERT of a row whose primary key is `e`, in another tenant: **allowed**, and the census goes from 0 to 1.
  - The reverse order (F2) is refused.
- **Consequence:**
  - Re-running 050 on such a database refuses.
  - The guard's primary-key arm (`d.id = $3::uuid`) would resolve the new row for an anchor keyed `UPPER(e)`.
- **Reachability:** none through today's routes. originate lowercases `documentUuid` (`documents.ts:473`), and primary keys are server-random (`documentRepo.ts:359`, `certifications.ts:363`). It needs a writer that chooses a primary key.
- **Answer to item 3 ("does its census match the trigger's rule exactly"):** no. The census is the union and the trigger is narrower in one direction.

### INFO
- **INF-1. Kam's (b) holds, unchanged** (`logs/gate_matrix_r2_side_by_side.txt`):
  - C1 (a colleague in the holder's organisation) and C2 (the holder) are REPLACED.
  - C3 (the cert's issuing organisation), C4 (another organisation), C5 and C6 (another tenant) are kept.
  - C7 and C8 answer 401.
- **INF-2. Round 1's INF-2 is unchanged.** The cert's own issuing organisation still cannot update it (C3, `document-has-no-issuer-organisation`). Kam has the card.
- **INF-3. My trigger mutant G-T1 survives the whole suite.** It makes the shape test case-sensitive (`~` for `~*`). No cell sends an upper-case id. The real trigger does refuse `UPPER(pkey)` (battery F2, F3), so this is a test gap only.
- **INF-4. Look-alike ids pass the trigger and the census.** `{pkey}` and the no-hyphen form both pass, yet Postgres casts each to the victim's uuid (battery F7, F8). Leading or trailing whitespace and `urn:uuid:` pass too, and those do not cast. None of them can reach a guard decision today:
  - originate's `UUID_V4_RE` (`documents.ts:355`) refuses them as a `documentUuid`;
  - anchoring's `documentId` regex (`anchorSchema.ts:160-163`) refuses them as an anchor id;
  - `anchor_store` keys are exact text.
- **INF-5. Deploy order.**
  - The compose runner exits 3 on a refusal (measured, M5), which blocks dependents.
  - The gateway's startup runner (`api-gateway/src/startup-migrations.ts`, KS-1054) logs the failure and **keeps serving**.
  - The anchoring guard does not check that the trigger exists.
  - So on any box where 050 refuses, whether from the census or a non-bypass migration role, the new guard runs with round 1's MAJ-1 open.
  - Azure's migration role (`services.bicep:51-55`) is a Flexible Server admin, which is not a superuser. Whether it has BYPASSRLS was not checked.
- **INF-6. Two stale authority texts remain beside the three that were fixed:**
  - `index.ts:1420-1422`: "Every condition can only REDUCE the set of overwrites … safe to ship ahead of the custody ruling".
  - `anchorOverwriteGuard.ts:229-231`: "so this needs no migration".
- **INF-7. Pre-existing, not this PR: a same-tenant `documentUuid` equal to a certification's primary key, with the same bytes, answers 200 with that cert's record.**
  - Cause: `respondForExisting` compares `existing.id`, which `fromDbRow` sets to `external_id || id` (`documentRepo.ts:168`; `documents.ts:682`). So the "a pkey shadow must refuse" comment does not hold for rows without an `external_id`.
  - Measured: `sameTenantPkeySameBytes_preexisting`.
- **INF-8. What the 409 reveals.**
  - It reveals "this v4 is some document's primary key, somewhere", and no tenant.
  - Its bytes equal the same-tenant refusal (below). The id was already public through verify.
  - The pre-existing cross-tenant `external_id` duplicate keeps its own, different 409: 117 bytes, "raced a concurrent request; retry".
- **INF-9. The race residual is confirmed as stated.** T1 inserts primary key X and holds its transaction; T2 inserts `external_id` X and is allowed; both commit; the census goes 1 → 2 (battery RACE).
- **INF-10. Harness note.** My first two runs, without the gateway vouch header, filed every originate create under the DEFAULT tenant, because `gatewayProvenance.ts` strips `x-tenant-id` when unvouched. Those logs (`*_mtfalse`, first `*_head_mt` boot) are kept only for MIN-A. Every table here comes from the vouched runs.

---

## Gate items

### 1. Round 1's MAJ-1 (XT1/XT2), colliding row in ANOTHER tenant, through booted anchoring and originate's real create route (`logs/cell_e2e_r2_head_mt.log`)

| Cell | Head | Develop + 050 (code without the mapping) |
|---|---|---|
| XT1 tenant-A cert P (NULL issuer, holder org C); tenant B `POST /api/documents {documentUuid: P}` | **409**, 115 bytes, `documentUuid is already registered with different content`. Anchor row **untouched**: tx `mock_tx_08d92d5b` and `updated_at` 11:21:37.579Z before and after, so its anchor never landed. Only A's row names P. verify keeps `zVICTIM` | 500, row untouched |
| XT1 then the KS-1603 direct `POST /api/anchors` by tenant B naming P | 202, tx overwritten (pre-existing), **identity kept** `zVICTIM` (`document-not-in-callers-tenant`) | same |
| XT2 the same, on a tenant-A document anchored under its primary key | **409**, untouched, identity kept | 500, kept |
| CTL tenant-B create with a fresh v4 | 201, row in tenant B with issuer ORG_TB, its anchor lands | — |

- **Raw INSERT as `secuura_app` in tenant B**, where the victim row is invisible (0 rows): refused `23505`, constraint `documents_id_namespaces_disjoint` (battery F1).
- **Round 1's own matrix, re-run** (`cells/gate_matrix_r2.ts`, `logs/gate_matrix_r2_side_by_side.txt`). The colliding row cannot be created now, even by the RLS-bypassing owner (refused `23505`). XT1 and XT2 then keep, at head and on develop.

### 2. The trigger (`cells/trigger_battery.ts`, `logs/trigger_battery.log`, `scripts/10_copy*.sql`, `logs/copy.log`)
- **Uncallable:**
  - by `secuura_app`: `42501` permission denied;
  - by its owner: `0A000` "trigger functions can only be called as triggers".
  - Catalogue: `prosecdef = t`, owner `secuura` (superuser), ACL `{secuura=X/secuura}`, app EXECUTE `false`, `search_path=pg_catalog, public`.
  - The app role cannot set `session_replication_role` or `DISABLE TRIGGER` (it is not the table's owner), and cannot replace the function (no CREATE on public).
- **Fires on every path:**
  - refused: INSERT (F1), UPDATE SET `external_id` (U1), UPDATE SET `id` (U2), UPDATE to an UPPER variant (U3);
  - refused: one multi-row INSERT in either order (B1, B2), INSERT … SELECT (B3), the `ON CONFLICT (external_id) DO UPDATE` upsert (B4);
  - refused: COPY FROM as the owner (`CONSTRAINT NAME: documents_id_namespaces_disjoint`). COPY FROM as `secuura_app` is impossible anyway ("COPY FROM not supported with row-level security");
  - U4, an update of another column, does not fire, by design.
- **Both directions and variants:**
  - Forward: canonical, UPPER and mixed case are refused (F1-F3).
  - Leading space, trailing space, trailing newline, braces, no hyphens and `urn:` are allowed (F4-F9, INF-4).
  - Reverse, lower case, is refused (R1). Reverse against UPPER or padded ids is allowed (R2, R3; MIN-B).
- **Race:** as stated (INF-9).
- **Bytes of the 409** (head, MT=true):
  - same-tenant shadow refusal: `409`, `application/json; charset=utf-8`, length 115;
  - 050's cross-tenant refusal: identical, the same `{"success":false,"error":{"code":"CONFLICT","message":"documentUuid is already registered with different content"}}`;
  - comparison: `equal_050_vs_sameTenant: true`.
  - Prisma mode differs (MIN-A).
- **R2 and R3, via the unit cells, reproduced 6/6:** another 23505 → 500 and the right constraint with SQLSTATE 23514 → 500 (`logs/lane_o_unit_head.json`). A real other-23505 cannot be provoked through saveDocument: the external-id duplicate is `ON CONFLICT DO NOTHING` → the pre-existing "raced" 409.

### 3. The migration (`scripts/11_migration.sh`, `logs/migration_050.log`; its own database `mig`, built without 050)
- **Fresh database:** the project's runner gives `applied=52 failed=0`, with `Applying 050…` printed after 049. The trigger is present and SECURITY DEFINER, owned by the superuser (`logs/run_migrations_head.log`). This is the author's claim, reproduced.
- **Planted collisions refuse:**
  - Two collisions planted (lower case and UPPER case), plus one padded look-alike.
  - `050: 2 existing documents row(s) …`, psql rc=3. Function 0, trigger 0: nothing created.
  - The header's census, run verbatim, lists exactly those 2 rows; the padded row is not listed.
  - The runner prints FAILED 050 and exits **3**.
- **The RLS-bypass assert fires:**
  - as `secuura_app`: `050: must run as a role that bypasses row-level security … secuura_app does not`, rc=3;
  - the same census run as `secuura_app` counts **0** over the 2 planted collisions, which is exactly the false 0 the assert exists to prevent.
- **Re-running is idempotent:**
  - After the rows were resolved by UPDATE (nothing deleted), the runner applies 050 (`applied=1`).
  - The file was applied directly twice more: rc=0 both times, and the function md5 plus the trigger count are unchanged (`12559e4e… 1`).
  - A third runner pass reports `Skipping 050 (already applied)`.
- **The census matches the trigger:** not exactly (MIN-B).

### 4. Kam's (b)
- Holds (INF-1). The behaviour behind INF-1 and INF-2 is unchanged, and C3 is still refused.

### 5. MIN-1 and MIN-2
- **MIN-1 is closed.** I booted the anchoring service on head and on develop and ran round 1's L1-L5 cells against each.
  - At head, L1 (no `organizationId`), L2 (an organisation that is not a uuid), L3 (an org-less connector token) and L4 log nothing. The service log has no `caller-has-no-organisation` or `caller-organisation-not-a-uuid` line.
  - L5 logs, as intended.
  - Develop logs nothing for L1-L5.
- **MIN-2 is closed** at the three named sites:
  - `index.ts:1406-1411`;
  - `documents.ts:909-913`;
  - the guard header `:16-25`.
  - Two residual texts remain (INF-6).

### 6. Mutants (`scripts/14_mutants.py`, `logs/mutants_run.log`, `logs/mutants/`)
- **Method:**
  - The author's 16 anchors are copied verbatim from `j12/tools/mut1612r2.py`. Mine are added on top.
  - Each mutant is an exact-count replace in worktree `mut`. Migration mutants are also re-installed in `mig`.
  - Each run executes the ks1612 integration cells (13), the 409 unit cells (6) and the ks1385 anchoring file (46).
  - Afterwards the file sha and the installed function+trigger+ACL hash were asserted equal (`8862cbda1af0cd83`). The worktree ended with 0 tracked changes.

| Mutant | Result | Red cells |
|---|---|---|
| C0 (author) comment-only, migration | survived (control) | — |
| MM1 / MM2 / MM3 / MM4 / MM5 / MM6 / MM7 / MM8 (author) | all KILLED | as the author listed (MM1 adds M1 M2; MM7 adds N3) |
| RM1 / RM2 / RM3 (author) | KILLED | R2 R3 / R1 R5 / R1 |
| QM1 / QM2 / QM3 / QM4 (author) | KILLED | Q5 / Q6 / Q8 / Q2 Q7 |
| **G-T1** (mine) shape test case-sensitive | **survived** (predicted) | — (INF-3) |
| **G-T2** (mine) trigger on INSERT only | KILLED | M1 M2 N5 |
| **G-R1** (mine) any named 23505 → 409 | KILLED | R2 |
| **G-R2** (mine) any save error on a documentUuid create → 409 | KILLED | R2 R3 R4 |
| **G-C0** (mine) comment-only, route | survived (control) | — |

- **No mutant can reach MAJ-A or MIN-A.** Both are outside every cell's model: no victim without a documents row, and no Prisma-shaped error.
- **Lanes at head on my database:**
  - ks1612 integration 13/13;
  - 409 unit 6/6;
  - anchoring integration 56/56 (`logs/lane_*_head.json`).
- **tsc `--noEmit`:** 0 errors for anchoring and for originate.
- **Red-first, database dimension, reproduced** (`scripts/16_redfirst_db.sh`; database `no050`): originate red P0 N1 N2 N3 N5 N6 U1 U2 M1 M2; anchoring red P050 X6 XT1 XT2. That is the author's predicted set exactly.

### 7. Merge prediction on live develop `db9bd1602` (`scripts/15_merge.sh`, `logs/merge_prediction.txt`)
- **Merge base:** `833984fc9`.
- **Overlap:** the PR's 9 files against develop's 6 files since the base (#1569, #1571, #1570) give **0 in common**. The planted control (the guard added to develop's list) gives 1.
- **merge-tree(develop, head):** rc=0, tree `5a75aee8`. It differs from develop in exactly the 9 PR files, which equal head's. Develop's own files are unchanged.
- **Migration numbering:** develop has no migration numbered 050 or above. Other open PRs were not checked.
- **Planted conflicting control:** a develop-side edit of the guard's WHERE line gives rc=1, `CONFLICT (content)` in `anchorOverwriteGuard.ts`.
- **Conclusion:** the merge is mechanically clean, but not safe to merge (MAJ-A).

## NOT tested
- **Preflight:** the PR body reports `13/16 legs ran, 3 SKIPPED`, legs 3, 4 and 8 (no local stack). Not run by me; Docker is off-limits.
- **No real Cardano** and **no gateway**. I sent the gateway's `x-gateway-vouch` and `x-tenant-id` myself, and did not boot the gateway.
- **Red-first, code dimension** (the new cells against `16e716103`): not reproduced.
- **Orphan rows on real boxes.** The number of uuid-keyed `anchor_store` rows with no documents row on kintsugi or demo (MAJ-A's live exposure) was not observed. 050's census does not count them.
- **Azure's migration role.** Whether it has BYPASSRLS (INF-5) was not checked.
- **Develop in single-tenant mode** for XT3/XT4: not run. Develop was measured with MT=true.
- **ESLint** was not re-run.
- **The batch anchor path** was not exercised.

Merge only on Wednesday's head-bound GO. Nothing deploys from this verdict. 050 needs the census on every box first, and MAJ-A means that census is not sufficient.

WALL-CLOCK: 37 min (10:59:40Z to 11:36Z)
