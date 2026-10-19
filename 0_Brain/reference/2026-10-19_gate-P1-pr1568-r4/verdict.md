VERDICT: GO WITH NOTE at head d2564aeb587bcbd7d9628495e83913c710ca0043 (round 4 of 4, the last)
MAJ-A closed without the pk arm, anchoring booted: YES. With anchoring and originate booted, all six orphan-minter routes (M1, M2, M3, M4 and originate's two /api/anchoring alias routes) are refused 409 with 0 rows and the anchor kept, on both drivers; with the trigger disabled, or with only round 3's pk arm, all six are REWRITTEN.
sha256/16: 783dde90754364eb

# Gate P1 verdict: PR 1568 (KS-1612 + KS-1385 (b)), round 4 of 4, Opus tier 1 full

- **Head gated:** `d2564aeb587bcbd7d9628495e83913c710ca0043`. **Develop:** `37834600a543cb0276f427d969ac034d9df74fbd`.
  - I read both with ls-remote at 01:40:06Z, and again at about 02:06Z. Both reads gave the same values.
- **Predicted landing tree:** `524b5d203a18b65dc4db7d78d8b99e7182a8e449`.
  - Merge base `833984fc9`. merge-tree gives rc 0, with the explicit base and with the automatic one.
  - In my scratch clone this tree is commit `3ded1858e` (scratch only, never pushed).
- **Setup:** findings only.
  - No git write verb in `!CODING`. The project checkout has 0 tracked changes and no `.prisma` directory, before and after.
  - No push, no GitHub or Linear write, no Docker, no server or box.
- **My own Postgres 15 clusters:**
  - 55831: built the way gate L1 built its clusters, for the booted e2e;
  - 55841: built the way compose builds one (J's mkpg method, run from my copy), for the integration cells and the mutants;
  - 55842: develop schema, for the census.
  - Redis, anchoring and originate ran on 55832, 55833 and 55834. All six ports were free before use, and every cluster is stopped now.
  - I never touched J's ports 55493-55495.
- **Prisma:** an isolated copy of 7.8.0 (client, CLI and adapter-pg 7.8.0) under `p1/prisma_rig`, using gate L1's method.
- **Evidence:** `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/2ce15c23-3025-4dcd-9e03-2be96a0a6754/scratchpad/p1/`, in `scripts/`, `cells/`, `sql/` and `logs/`.
- **Counts:** Major 0. Minor 2 (MIN-1, MIN-2). Info 6. MAJ-A stays closed, and MAJ-B and MIN-A are closed.

## Why GO WITH NOTE, in one paragraph
- **MAJ-A, with anchoring booted:** every orphan minter is refused (409, 0 rows, the anchor row unchanged, verify still serves the victim). That includes originate's `/api/anchoring` alias, through both `/submit` and `/`, on node-pg and on Prisma. The inverted controls fire.
- **MAJ-B is closed through the real routes on both drivers:** issue 201, revoke 200, recertify 201 and the expiry write 200. On a develop box seeded through the real routes (18 anchored certifications), the census applies 050 and 051. It refuses one planted claim with "1". Round 3's 051 refuses the same box with "18", which is the control.
- **MIN-A is closed against the real Prisma 7.8.0 error.**
- **20 mutants, one or more per product hunk:** 15 of 18 product mutants are killed and both controls survive.
- **What keeps this from a plain GO:**
  - a minter the 051 header does not name (MIN-1);
  - two test gaps in the helper, plus one sentence in its comment that is untrue (MIN-2).
  - Neither reopens a Major.

## FOUND / TESTED / HOW

### Gate 1: scope
- **FOUND:**
  - `d2564aeb587b` is one commit on `09588895db75`. It touches exactly 4 files, +512/-104: 051, `utils/idNamespaceCollision.ts`, `ks1612-409-mapping-…test.ts`, and the NEW `ks1612-051-…integration.test.ts`.
  - `routes/documents.ts` and `certifications.ts` are not in the delta.
  - The tree is `39655c374f12`, as J claims.
  - Author and committer are `Kam Kreiser <kamil.kreiser@secuura.ai>`.
- **HOW:** `git diff --stat` and `git log` in my clone.

### Gate 2: MAJ-A without the pk arm, anchoring BOOTED
**TESTED:** gate L1's `e2e_r3.ts`, adapted as `cells/e2e_r4.ts`, plus the two alias minters and a full-row md5. Real anchoring and real originate booted (`scripts/07_boot.sh`), with the mock chain, RS256 and the gateway vouch. The landing tree served both services. Logs: `logs/cell_e2e_r4_{land_mt,landp_single,ctl_notrigger_mt,ctl_pkonly_mt}.log`.

| Minter (tenant A) | Landing, MT=true (node-pg) | Landing, MT unset (real Prisma) | CONTROL: trigger disabled | CONTROL: round 3's pk arm only |
|---|---|---|---|---|
| M1 anchoring `POST /api/anchors` | 409 (131 B, 051's body), 0 rows, row md5 unchanged, direct re-anchor KEPT, verify = zVICTIM_M1 | same | 201, B's row lands, **REWRITTEN** (verify = zTENANT_B_DIRECT) | 201, **REWRITTEN** |
| M2 anchoring `POST /api/anchors/batch` | 409, KEPT | 409, KEPT | 201, REWRITTEN | 201, REWRITTEN |
| M3 originate `POST /api/anchors/submit` | 409, KEPT | 409, KEPT | 201, REWRITTEN | 201, REWRITTEN |
| M4 originate `POST /api/anchors/` | 409, KEPT, verify = zVICTIM_M4 | same | 201, REWRITTEN | 201, REWRITTEN |
| **M3b originate `POST /api/anchoring/submit`** (alias, `index.ts:279`) | 409, KEPT | 409, KEPT | 201, REWRITTEN | 201, REWRITTEN |
| **M4b originate `POST /api/anchoring/`** (alias) | 409, KEPT, verify = zVICTIM_M4B | same | 201, REWRITTEN | 201, REWRITTEN |
| CTL tenant B fresh v4 | 201, auto-anchor lands | 201 | 201 | 201 |

- **This confirms by measurement:**
  - J's Q1, inverted ("the pk arm never refused MAJ-A");
  - that the external-id arm alone refuses every minter, through the real re-anchor chain and the real guard.
- **Restores verified:**
  - the trigger is back to `O`;
  - the function md5 is back to `f6d6aa8d93dcfa24ab6938c937e413b5` with `prosecdef = t` (`logs/controls.log`).

**Hunt for an unnamed writer, by symbol, across all of `Blockchain/Dev`** (ts, js, sql, sh, py, mjs, cjs; tests, dist and node_modules excluded):
- **Searched:**
  - `insert into documents`, `update documents`, `copy documents`;
  - `.document(s).create|update|upsert|createMany|updateMany`;
  - dynamic `INSERT INTO ${…}`;
  - `external_id =` and `external_id:` setters;
  - `insert into anchor_store`, `update anchor_store`, `dbPersistAnchor(`, `saveAnchorToDb(`.
- **Control:** `insert into documents` counts 2 in `documentRepo.ts`, matched case-insensitively.
- **`documents.id`:** never caller-chosen.
  - `documentRepo.ts:359` sets `dbId = uuidv4()` unconditionally.
  - `certificationRepo.ts:199` takes `cert.id` from `certifications.ts:363` (`uuidv4()`) or from recertify (`uuidv4()`). Revoke and expiry take it from `getCertification` (`WHERE id = $1::uuid`, which returns `row.id`, `certificationRepo.ts:133`).
  - The derived lineage rows use the `doc-${Date.now()}-…` shape (`certifications.ts:546`, `documents.ts:2101/2842/3036`).
- **`external_id` from caller input:** only `saveDocument`, an INSERT, which 051's trigger covers.
- **Every documents UPDATE sets other columns only:**
  - `documentRepo.ts:619/648`;
  - `certifications.ts:606`;
  - `documents.ts:1866`;
  - `adminConfig.ts:1927`;
  - `gdprService.ts:735/786`;
  - `connectorOrganisationErasure.ts:405`;
  - `startup-migrations.ts:710-718`.
  - `adminConfig.ts:1500` is `rights_holders`, not documents.
- **No new documents writer was found. One orphan minter that the header does not name was found (MIN-1).**

### Gate 3: MAJ-B through the real routes, as `secuura_app`, both drivers
These cells ran in the same booted runs as the table above (B1-B6).

| Cell | MT=true (node-pg) | MT unset (Prisma) | CONTROL: pk arm only |
|---|---|---|---|
| B1 `POST /api/certifications/issue` | **201**, 1 row, `external_id` NULL, anchor 13:624Z **older than** the row (13:633Z) | **201** | **500** `Failed to issue certification`, 0 rows |
| B2 `POST /:id/revoke` on B1's cert | **200**, the row reads `revoked` | **200** | 500 |
| B3 `POST /:id/recertify` (new id anchored, then saved) | **201**, new row `certified`, anchor older than row | **201** | 500 |
| B4 the expiry write: `GET /:id` on an anchored cert issued with a past `expiresAt` (`certifications.ts:867-869`) | **200**, status certified → **expired** in the DB | **200**, → expired | n/a (the issue failed) |
| B5 certify with `parentDocumentId` | 201, derived `doc-…` row `signed` | 201 | — |
| B6 legacy `documentId` certify (UPDATE of the named row) | 201, the named row → `certified` | 201 | — |

- **J's integration file, on the landing tree, on 55841:**
  - **17/17 on node-pg** and **17/17 on real Prisma 7.8.0**, both as `secuura_app` (`logs/int_land_{nodepg,prisma}.log`).
  - SETUP asserts the role is NOSUPERUSER NOBYPASSRLS, and that the branch taken matches the driver.
- **INF-2 is unchanged and measured (L4):**
  - the issuer anchors a fresh v4 and then registers it, and gets 409 (051), on both drivers;
  - the develop behaviour this replaces is 201.
  - It is a behaviour change for Kam to know about. It is not new in round 4.

### Gate 4: the census on a seeded box
**HOW** (`scripts/21_census.sh`, `logs/census.log`):
- I built a develop-schema cluster (`37834600a`, 51 migrations, no 050 or 051).
- I booted develop's anchoring and originate on it and seeded it through the real routes, with no attacks (`cells/seed_r4.ts`, `logs/cell_seed_r4_devseed_mt.log`).
- The seed holds:
  - **18 certifications anchored by primary key, all 18 with the anchor strictly older than the row**;
  - 3 revoked and 3 expired;
  - 5 registered documents anchored after their rows, 2 of them re-anchored by the issuer's flat anchor and lifecycle event;
  - 10 orphan anchors;
  - 26 documents in all.
- I made three template copies and ran the project's own `run-migrations.sh` on each (glob made absolute, nothing else changed).

| Copy | Result |
|---|---|
| Round 4's migrations | **rc 0, `applied=2 failed=0 skipped=51`**. Both triggers are installed, the 051 function md5 is `f6d6aa8d…`, and 050 and 051 are recorded |
| Round 4 + one planted claim (anchor 1 h older, on preprod AND preview) | **rc 3**, `051: 1 documents row(s) claim an external id whose anchor record is older than the document`. 051 is not recorded, its trigger is absent, and 050 is applied |
| CONTROL: the same box with round 3's 051 | **rc 3**, `051: 18 documents row(s) …`. This is MAJ-B's census, reproduced on the same data |

### Gate 5: MIN-A against real Prisma 7.8.0 + adapter-pg 7.8.0, and an attack on the walk
**HOW:** `cells/walk_probe.ts` (`logs/walk_probe.log`). It captures the REAL errors:
- 051 and 050 through `saveDocument` on the Prisma client;
- a 23505 on `documents_external_id_key` through the same client;
- the same refusals through node-pg.

It then feeds the landing tree's helper with those errors and with variants built from them.
- **The real shape is confirmed:** `PrismaClientKnownRequestError`, `P2010`, `meta.driverAdapterError.cause = {originalCode:'23505', originalMessage:<RAISE text>, kind:'UniqueConstraintViolation'}`, and no constraint name anywhere.

| Case | live (051) / ns (050) | Assessment |
|---|---|---|
| R1 real Prisma 051 · R4 real node-pg 051 | true / false | correct |
| R2 real Prisma 050 | false / true | correct |
| **R3 real Prisma 23505 from a DIFFERENT constraint** (`documents_external_id_key`; the cause carries `constraint:{fields:['external_id']}`) | false / false | correct: does NOT map to 051's 409 |
| R5 the same on node-pg | false / false | correct |
| R6 Prisma: 23505 + 051's exact text + ANOTHER constraint name (synthetic RAISE) | **true** / false | INF-A: inherent, because Prisma drops the constraint name. Only 051 carries the text today (grep over migrations: 051 counts 1, every other file counts 0) |
| R7 the same on node-pg | false / false | correct |
| W1 one `new Error(x,{cause})` wrapper · W3 `{a:E}` · W5 · W6 (node-pg at depth 4) | true | correct |
| **W2 two wrappers · W4 `{a:{b:E}}` · W7 (node-pg at depth 5)** | false (it would be a 500) | INF-B: the real route passes the error unwrapped (`documents.ts:742-745`, record at depth 3). The margin is one wrapper |
| G2 a throwing getter on an unrelated child | true | correct (`try` at `:74`) |
| **G1 a throwing getter on the outer `code` · G3 on the cause's `originalMessage` · G4 a Proxy whose `ownKeys` throws** | **the helper THROWS** | MIN-2 (b) |
| N1 a non-enumerable `originalCode` on the record · N3 a non-enumerable `cause` | true | correct |
| N2 the `driverAdapterError` subtree non-enumerable | false | INF-C: the real Prisma error's subtree is enumerable |
| M1 off by one character · M2 a trailing space · M3 the right text with SQLSTATE 23503 | false | correct: exact equality, SQLSTATE required |
| C1 a cycle through `meta.self` | true, terminates | correct |
| C2 a pure cycle · X1 null · X2 a bare string | false | correct |

- **Booted proof on the Prisma path:** the six minter routes each give 409 with 051's body (gate 2 table), and N2 (050's 409) is green on Prisma in J's file.

### Gate 6: the 051 header against the code
- **The CORRECTION is true.**
  - Round 3's header (`09588895:051:16-21`) said the round-2 record named the wrong path.
  - Originate mounts `anchorsRouter` at `/api/anchors` and `/api/anchoring` (`originate/src/index.ts:278-279`, unchanged on develop since the merge base).
  - I **measured** M3b (`POST /api/anchoring/submit` on originate): it mints an orphan (202) and its claim is refused.
  - Anchoring's own `POST /api/anchoring/submit` (`anchoring/src/index.ts:1191`) has no query or persist call.
- **Checked true:**
  - `anchoring index.ts:465→507` and `739→804`;
  - `anchors.ts:367`, `:442`, `:246→342`;
  - `certifications.ts:363/445/518`;
  - `certificationRepo.ts:199`;
  - `documentRepo.ts:359`;
  - anchoring persists before its 202 (`:507`);
  - "certifications never appear" (no `external_id`, measured: B1's `external_id` is NULL);
  - the runner skips by FILENAME (measured: `skipped=51`);
  - idempotence (function md5 stable across my restores).
- **Not true, or not measurable:**
  - **MIN-1:** the minter list (`051:8-17`) is presented as the set of minters, and it is incomplete.
  - INF-D, nit: `:14` says the uuid is minted at `anchors.ts:393`. It is at `:394` (round 3 and gate L1 had the same number).
  - INF-D: `:33-35` says "`documents.created_at` is the database's own NOW()". That is true for `documentRepo`, the only writer of rows with an `external_id`, so it is true for the census. It is untrue for certification rows: `certificationRepo.ts:216-217` binds `new Date()` from the originate process.
  - UNMEASURED: `:109` "no box carries its primary-key arm". I cannot observe boxes. Develop has no 051.

### Gate 7: suites on the predicted landing tree, with `packages/shared` rebuilt
- **HOW:** `scripts/13c_land_dev.sh`, `logs/suites_summary.txt`.

| Suite | Landing `524b5d20` | Develop `37834600` (base) |
|---|---|---|
| originate tsc `--noEmit` | rc 0, 0 lines | rc 0 |
| originate unit jest | **120 files, 1469/1469** | 118 files, 1450/1450 |
| anchoring unit vitest | 379/380 (`threadTokenMint.test.ts`) | 379/380 (the same file; pre-existing) |
| J's integration file, node-pg | 17/17 | — |
| J's integration file, real Prisma | 17/17 | — |

- **The delta is +19 tests, entirely the PR's two unit files:** `ks1612-409-mapping…` (13) and `ks1612-create-maps-only…` (6). No file present on develop changed its count.
- **J's 1395 was measured on an older base.** My figure is measured at the landing parent.

**Mutants on the landing tree** (`scripts/23_mutants.py`, `logs/mutants.log`, `logs/mut_*`):
- Each one ran the unit file and/or the integration file on node-pg and Prisma.
- Every run loaded all 13 or 17 cells, so no kill comes from a load failure.
- After each mutant, the file sha256 or the function md5 and `prosecdef` were verified restored.
- The 4 worktrees are clean.

| Hunk | Mutant | Result (red cells) |
|---|---|---|
| control | C0 a comment in the helper · C1 a comment in 051 | survive, survive |
| 051 function | F1 round 3's pk arm re-added | KILLED (B1, B2, N3, F1; both drivers) |
| | F2 external-id arm removed | KILLED (A M1-M4, N1, N3, E2, F1, F2) |
| | F3 NOT EXISTS exemption removed | KILLED (E1) |
| | F4 SECURITY INVOKER | KILLED (SETUP, E1) |
| 051 census | S1 DISTINCT removed | KILLED (F2) |
| | S2 never refuses | KILLED (F2) |
| | S3 census arm B re-added | KILLED (F1, F2, F3) |
| | S4 role check removed | KILLED (F3) |
| helper walk | H1 MAX_DEPTH 2 | KILLED (unit Prisma cells; A, N1, N2, N3 on Prisma) |
| | H2 no `originalCode` | KILLED |
| | H3 no `originalMessage` | KILLED |
| | H4 substring, not equality | KILLED (unit) |
| | H5 no explicit `cause` read | KILLED (unit, the non-enumerable cell) |
| | H7 no SQLSTATE check | KILLED (unit) |
| | H8 constraint arm removed | KILLED (unit; node-pg A, N1-N3) |
| | **H6 cycle guard removed** | **survived** (INF-E: the depth bound already stops a cycle, so the guard costs nothing and protects nothing) |
| | **H9 `r.constraint === null &&` removed** | **survived**: MIN-2 (a) |
| | **H10 the `try` around a child read removed** | **survived**: MIN-2 (a) |

### Gate 8: merge prediction
- **HOW:** `scripts/15_merge.sh`, `logs/merge_prediction.txt`.
- **Result:**
  - `merge-tree --write-tree` of `d2564aeb587b` onto `37834600a543`, base `833984fc9`: rc 0, **tree `524b5d203a18`**, with the explicit base and with the automatic one.
  - The merged tree differs from develop in exactly the PR's 12 files. Eleven of them are byte-equal to the head. The twelfth, `routes/documents.ts`, carries both sides.
- **Develop since gate L1's `83ed01af`:** 14 first-parent commits, not eleven. They range from `09ef0612f` to `37834600a`. J's re-prediction was onto `fae056052`; 9 commits landed after it.
- **The only file in common is `services/originate/src/routes/documents.ts`:**
  - develop's single change there is `f95ad12fe` (#1587), hunk `-1510,102`;
  - the PR's hunks are at `:29`, `:62`, `:691`, `:713`, `:894` and `:941`;
  - they are disjoint, and the merge is clean.
- No migration has been added to develop since the merge base.

## Severities

**MIN-1. The 051 header does not name one orphan minter: originate `GET /api/anchors/:documentId`, and its alias `GET /api/anchoring/:documentId`, with `SIMULATE_ANCHORING=true`.**
- **Where:**
  - `originate/src/routes/anchors.ts:168` → `:219` `saveAnchorToDb`, which **persists** a `tx_sim_` anchor under the CALLER's id when none exists;
  - `deployment/azure/RUNBOOK.md:9` says the demo deployment runs with `SIMULATE_ANCHORING=true`.
  - The header's list is at `051:8-17`.
- **Measured** (`cells/simget.ts`, `logs/cell_simget_simget_mt.log`, booted, MT=true):
  - tenant A GETs a fresh v4 (200), and 1 `anchor_store` row lands (`preview`, `simulated=t`);
  - tenant B then registers that id: **409** with 051's body, 0 rows. That holds through both mounts;
  - control: a fresh id with no GET first gives 201.
- **Effect:**
  - 051 is minter-agnostic, so MAJ-A stays closed;
  - the header's list is incomplete;
  - on a simulate box, a READ permanently blocks any later registration of that id. That is INF-2's class, and it needs the id in advance (MIN-C's predictability).
- **Severity:** Minor (documentation, and a DoS of a known id). Not blocking.

**MIN-2. Helper: two test gaps, and one sentence in its comment that is untrue.**
- **(a) Two mutants survive every cell.**
  - H9 drops `r.constraint === null &&` (`idNamespaceCollision.ts:84`). The probe's R7 shows the guard matters: a node-pg 23505 from another constraint that carries 051's text must not map to 051's 409. No cell pins it.
  - H10 drops the `try` around a child read (`:74`).
- **(b) The comment is untrue.** `:56-58` says "Nothing here throws on an unexpected shape". The probe's G1, G3 and G4 throw.
  - The cause is the property reads at `:68`, `:70` and the `Object.keys` at `:72`, which sit outside the `try`.
  - A throw there escapes the route's catch (`documents.ts:742-745`) and becomes the outer 500.
  - No real driver error has a throwing getter, so this is not reachable today.
- **Severity:** Minor. Not blocking.

**INFO**
- **INF-A:** on Prisma, any 23505 carrying 051's exact text maps to 051's 409 whatever its constraint (R6). This is inherent to Prisma dropping the name. Only 051 carries the text today.
- **INF-B:** the depth margin is one wrapper (W2 and W4 fall to 500). The route does not wrap the error today.
- **INF-C:** a non-enumerable subtree other than `cause` is not walked (N2). The real Prisma error is enumerable.
- **INF-D:** header nits: `:14` says `:393` where the code is at `:394`; `:33-35`'s NOW() claim is untrue for certification rows but true for the rows the census reads.
- **INF-E:** H6, the cycle guard, is redundant with the depth bound.
- **INF-F, pre-existing and unchanged from gate L1:**
  - HC: an upper-case anchor id, a lower-cased registration (201), then B's direct anchor of the lower-case id. Verify-by-hash serves B's identity from B's own row, on both drivers, with no guard decision involved.
  - INF-2 (L4): anchor-then-register is a permanent 409.
  - MIN-C and MIN-D are unchanged.

## NOT tested
- **Real boxes** (kintsugi, demo): their census result, whether any box carries round 3's 051 (header `:109`), and S's id generator.
- **Real Cardano**, and **the gateway** (I sent the vouch header myself). Through the gateway, `/api/anchoring` goes to anchoring, not originate; I did not re-measure that routing.
- **Preflight legs 3, 4 and 8**, and the four platform suites (no Docker).
- **Multi-host clocks** (INF-4 / KS-1630): one host, one clock.
- **ESLint** was not run.
- **The anchoring integration suites** were not run. Anchoring has no delta in round 4; I ran its unit suite only.
- **The census on a box with a seed made on multi-tenant boxes with real per-tenant databases**: every tenant shares one database (no `tenant_config` rows).
- **Develop's own e2e matrix:** develop was used as the suite baseline and as the census seed. The rewrite baseline here is the landing tree with the trigger disabled, not develop.

Merge only on Wednesday's head-bound GO. Nothing deploys from this verdict.

MODEL: claude-opus-5-5
WALL-CLOCK: 31 min (12:38 to 13:09 AEDT, 2026-10-19)
