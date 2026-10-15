VERDICT: NO GO at head 80daaa78a2c7adf7196a41cdf240376d8c2bf75a (round 2 of 2). Every round-1 finding is closed, and the merge is safe (never worse than develop). One new Major: the guard looks the document up by the wrong key, so neither of Kam's rulings takes effect for any event originate sends.
REPORT-SHA256/16: 7b3442fc82c94a83

# Gate verdict: PR 1549 round 2 (KS-1385, custody option (c)), delta gate

- **Head gated:** `80daaa78a2c7adf7196a41cdf240376d8c2bf75a`. My own ls-remote showed it as `refs/pull/1549/head` at 2026-10-15T06:05:57Z and again at 06:14:37Z.
- **Develop:** `53b429ed6b4bf4d23c0721bf573b9df1c858bc06`, the live tip, read by ls-remote at the same two times.
- **Setup:**
  - Independent gate, findings only. Nothing was changed in the project.
  - All work ran in a `--shared` clone and in worktrees under `/private/tmp/claude-501/gate1549r2-170549/`.
  - Postgres was my own, 18.x, on 127.0.0.1:55621 (lsof showed the port free first; 55418 was not touched). Its schema came from the repo: `docker/init/*.sql` then `migrations/*.sql`. The 13 setup errors were all inserts into the `_secuura_migrations` bookkeeping table.
  - Roles: `secuura_app` is NOSUPERUSER NOBYPASSRLS. `documents` and `users` are FORCE RLS, and `users_auth_lookup` is a permissive policy whose condition is `true` (`logs/pg_setup.log`, `scripts/05_pg.sh`).
- **Counts:** Major 1 · Minor 1 · Info 5.
- **Evidence:** `evidence/` next to this file: `logs/`, `cells/`, `scripts/`.

## Why NO GO, in one paragraph
The round-1 fix (`fd81a7d8`) added `anchorOverwriteGuard.ts`, which looks up the document with `documents.id = $1::uuid`. Every originate site sends `documents.external_id` as the anchor's `documentId`, never `documents.id`.
- For a document originate minted, that value is `doc-<ts>-<rand>`. The guard returns `document-id-not-a-uuid`, and the code deliberately writes no log line for that reason.
- For an S-supplied `documentUuid`, it is a uuid that is not the row's primary key. The guard returns `document-not-in-callers-tenant`.

So for every real originate event the guard keeps the first payload, and head behaves exactly like develop. Kam's (b) "Latest event's identity wins" and his (c) "Issuer, or anyone in the custodian's organisation" are both dead for that traffic. I measured this on the booted service with three arms (cells X1-X3):

| Arm | Second event's identity |
|---|---|
| Head | kept (first payload stays) |
| Develop | kept |
| Round-1 head `aca6efb0` | replaced |

The author's cells, and the S1-S8 matrix in the PR body, all build their documents with a uuid primary key and anchor under that same key. No originate path does that, so the cells are green while the feature is inert.

Nothing here is unsafe; it fails closed. Under the round cap the brief's rule applies: ship the closed instances and ticket the residue (proposed residue below).

---

## FOUND / TESTED / HOW

### MAJOR

**MAJ-A. The overwrite guard keys on `documents.id`, but originate anchors under `documents.external_id`, so neither ruling reaches any originate-emitted event**
- **Where:**
  - The guard:
    - `services/anchoring/src/anchorOverwriteGuard.ts:263`: `if (!isUuidShaped(documentId)) return … 'document-id-not-a-uuid'`.
    - `:204`: the same check inside `readOwningDocument`.
    - `:227`: `WHERE d.id = $1::uuid`.
  - The caller in anchoring:
    - `index.ts:1369`: `mayOverwriteStoredMetadata(anchor.documentId, …)`.
    - `index.ts:1485`: suppresses the log line for `document-id-not-a-uuid`.
  - Originate, the write side:
    - `services/originate/src/routes/documents.ts:655`: `const id = documentUuid ?? \`doc-${Date.now()}-…\``.
    - `:902-903`: the anchor body sends `documentId: id`.
    - `repositories/documentRepo.ts:359`: `dbId = uuidv4()`.
    - `repositories/documentRepo.ts:437-438`: the INSERT writes `id = dbId` and `external_id = doc.id`.
  - The lifecycle sites (`documents.ts:1985`, `:2397`, `:2502`) send `req.params.id`. Transfer-custody itself updates `WHERE external_id = ${id}` (`:1923`, `:1944`), so that value is the external id.
  - Anchoring's own OpenAPI describes `documentId` as "doc-… external id or a UUID" (`anchoring.openapi.ts:220`).
- **Sweep:** `git grep -i "external_id|externalId|external id"` over `services/anchoring/src` finds only that OpenAPI line: 0 hits in the guard and 0 in the cells. Control: `owner_user_id` has 8 hits in the guard.
- **TESTED (end to end, booted service):**
  - Setup:
    - Anchoring booted with tsx at head, on the production role `secuura_app` (FORCE RLS live).
    - Mock chain; RS256 key pair I generated.
    - `documents` rows inserted in the shape `documentRepo` writes: a random uuid `id`, with `external_id` set to either `doc-…` or an S uuid.
  - Script and cell: `scripts/07_e2e.sh`, `cells/e2e_custody.ts`.
  - Head (`logs/e2e_custody_head.log`):

    | Cell | `documentId` sent | Caller | Result | Guard reason |
    |---|---|---|---|---|
    | X1 | `doc-<ts>-<rand>` | issuer org (Kam's (b) case) | **kept**, `did:key:zFIRST14` | none; silent, 0 log lines for it |
    | X2 | S `documentUuid` | issuer org | **kept** | `document-not-in-callers-tenant` |
    | X3 | S `documentUuid` | colleague in the custodian's org (Kam's (c) case) | **kept** | `document-not-in-callers-tenant` |
    | P0-P3 | `documents.id` (the positive control) | same callers | **replaced** | — |

  - Control arms, same cell, same database:
    - **develop** (`logs/e2e_custody_dev.log`): all 16 cells kept.
    - **aca6efb0**, the round-1 gated head (`logs/e2e_custody_r1gated.log`): X1-X3 replaced. MAJ-1 is reproduced there as well (P5, other tenant: replaced).
  - So head differs from develop only when the anchor key is the `documents.id` primary key.
- **Consequence:**
  - INF-4 of round 1 (at `aca6efb0`, the share's tx carried the share's identity) is lost again for real traffic. Every later event re-mints the first payload, as on develop.
  - The PR body's "S6 is the only row that changes" holds only for a key originate never sends.
  - No security regression: every arm I measured at head is develop-or-stricter.
- **NOT established:** whether Platform S ever anchors through flat `POST /api/anchors` using a K-minted document's primary key. `documentRepo.ts:172` surfaces `documentUuid = row.id` for `doc-…` documents, so S could hold the primary key. Such a row would then be a different `anchor_store` row from the one originate's create wrote (`document_id = doc-…`). S's wire traffic was not observed.
- **Proposed residue (ticket, not a fix):**
  - Resolve the anchor's `documentId` against `documents.external_id`, falling back to `documents.id` the way `getDocument` does (`documentRepo.ts:233-245`).
  - Do not short-circuit the `doc-` form at `:263`/`:204`.
  - Add a cell that drives the product's own `saveDocument` + site-1 body, or the same key shape.

### MINOR

**MIN-A. Two product comments still describe issuer-only (option (a)) after the flip to (c)**
- `services/anchoring/src/index.ts:1406-1409`: "confirmed the caller's organisation is the document's issuer. Custody option (a); Kam holds card …". This sits inside the upsert's SQL comment block, which round 2 did not touch.
- `services/originate/src/routes/documents.ts:896-898`: "the overwrite applies only when the caller's organisation is the document's issuer, in the caller's own tenant."
- The PR body says the INF-1 correction is "named in the code so it outlives the round". These two lines contradict the shipped constant. Text only.

### INFO

- **INF-A. (c) trusts the caller's signed `organizationId` claim, not the caller's current `users` row** (cell P8).
  - Setup: a user whose `users.organization_id` is a third org, holding a validly signed token that claims the custodian's org.
  - Result: replaced.
  - The issuer branch already worked this way in round 1. The exposure is bounded by the access-token lifetime (`auth/src/services/jwt.ts:43`, `JWT_EXPIRES_IN` default `1h`).
  - The custodian's side IS read live (P7a and P7b below).
- **INF-B. ESLint "0" is 0 errors, not 0 problems.**
  - Run over the PR's 17 files: 6 warnings, 0 errors (`logs/eslint_head.log`).
  - Two of the warnings are on PR-added lines: `anchorStatusUpdate.ts:109` (no-useless-assignment) and `documents.ts:944`; the two test files account for two more.
  - Planted control: an unused `var` gives rc=1, 1 error.
- **INF-C. Mutant i5 is pinned only by a source-text cell.** i5 binds `true` instead of `overwrite.allow`. The only kill is W1, which reads `index.ts` as text; no behavioural cell catches it. My booted-service cells cover that join behaviourally (P4-P6 kept at head).
- **INF-D. The batch path still resets an existing single row to `pending` with a NULL tx.** The payload is now kept (MIN-3 closed). The status and tx reset is older than this PR (round-1 Gate item 4). Not tested end to end this round.
- **INF-E. The anchoring default lane fails 1 of 371 (`threadTokenMint.test.ts`, the per-seed policyId test).** It fails identically on develop 53b429ed (`logs/dev_threadTokenMint.log`). Not this PR.

---

## Gate items

### 1. Diff b1801721..80daaa78, by first-parent commit (`logs/diff_delta.txt`, `scripts/02_diff.sh`, `scripts/03_show.sh`)
- **ea799fd4**, the merge of develop e67e0dc1:
  - The tree equals `git merge-tree --write-tree b1801721 e67e0dc1` (2bf0566e).
  - The first-parent patch is **byte-identical** to develop's own patch `026c2d16..e67e0dc1` (cmp: 179 files).
  - The PR's side has 17 files, with 0 overlap.
- **12b87963**, round 2: 2 files.
  - `anchorOverwriteGuard.ts`: the one code line is `CUSTODY_OPTION 'a' -> 'c'` (`:72`). Every other changed line is a comment, including the `// THE ISSUER …` and `// Option (c) — SHIPS` markers.
  - The integration test: `ORG_THIRD` added; W3 split; C0 and C-d re-pinned to (c); C-c comment; C-f added.
  - Nothing else. Confirmed (`logs/diff_12b87963.patch`).
- **80daaa78**, the merge of develop 53b429ed:
  - The tree equals the merge-tree prediction (e4d73a01).
  - The first-parent patch is byte-identical to develop's `e67e0dc1..53b429ed`: one file, `ks884_pre_push_tag_named_develop.test.sh`, +2/-2.
- **Also read:** round 1's fix commits `aca6efb0..b1801721` (`fd81a7d8` guard; `b1801721` compare-and-set). Nine files; this is where MAJ-A originates.

### 2. Round-1 findings (verdict 40bdc24d2e1f07dc, gated at aca6efb0)

| Round 1 | Status at 80daaa78 | Evidence |
|---|---|---|
| MAJ-1 cross-tenant rewrite | **CLOSED** | Booted service. P5 (tenant B) and P5b (tenant B claiming the custodian's org id) are kept at head and replaced at aca6efb0. The `doc-…` stranger case of round 1 is kept by construction (X1). |
| MAJ-2 content_hash/payload split | **CLOSED** | The payload is kept when the hash differs (CASE in `index.ts:1425-1428`). My mutant i2 (equality dropped) is KILLED by H1 and W2. |
| MIN-1 race invariant | **CLOSED** | Compare-and-set (`anchorStatusUpdate.ts:107-111`; `anchorSubmission.ts:449`, `:475`, `:482`, `:503`). My mutant s1 (CAS WHERE dropped) is KILLED by R1 and R2 (product race cell, real submitter, real Postgres). |
| MIN-2 unpinned call sites | **CLOSED** | Round 1's exact k04, k05, k06 and g08 now all die: K04; K05+G08; K06; K05+K05b+G08. They all survived in round 1. |
| MIN-3 batch wipes attestation | **CLOSED** for the PR-introduced harm | The `anchor_type` equality is in the CASE. My mutant i3 is KILLED by B1 and W2. The status/tx reset is older (INF-D). |
| INF-1 consequence-set text | **CLOSED** | `documents.ts:886-887` names the correction. The new stale text is MIN-A. |
| INF-2 nothing binds identity to caller | **TICKETED, still open** (KS-1604) | Out of scope by the PR body. |
| INF-3 identity edge cases (`{}` erases) | **Unchanged, by design.** It now reaches only callers the guard admits. | Read from source. |
| INF-4 on-chain attribution bonus | **LOST for real traffic** | Consequence of MAJ-A. Holds only on the primary-key path (P0-P3). |
| INF-5 error-detail scope | Unchanged | — |
| INF-6 lane globs | Unchanged. The no-DB run refuses: rc=1, 3× "refusing to pass" (`logs/itest_nodb.log`). | — |
| INF-7 certification mocks | Unchanged | — |
| (c) vs Kam's ruling | **Superseded by Kam's (c)** for the custody narrowing, which round 1 shipped as (a). Correct where reachable (item 4); unreachable for originate keys (MAJ-A). | — |

### 3. Red-first at (a), green at (c), on my own Postgres (`scripts/mutants.py`, `scripts/06_itest.sh`)
- **Green at head:** anchoring integration lane 3 files / 30 tests, 30 passed (`logs/itest_head.*`). The FORCE-RLS file ran with `TEST_APP_DATABASE_URL=secuura_app`.
- **Red at (a):** the constant reverted to `'a'` gives 27 passed and 3 failed. The failures are W3, C0 and C-d, all in the main file (19 passed + 3 failed there). This reproduces the author's 3/19 exactly (`logs/mutants/RED-a.anchoring.json`).
- **Originate ks1385 suites:** 31 cells, all passing in both arms.
- **Other suites at head:**
  - originate full jest: **109/109 suites, 1368/1368 tests** (`logs/originate_full.summary.txt`).
  - tsc `--noEmit`: 0 errors in anchoring and in originate. Planted type-error control: rc=2, 1 error.
  - anchoring default lane: 370/371 (INF-E).

### 4. Does (c) admit only what Kam ruled? Booted service, `documents.id` key, as `secuura_app` (`logs/e2e_custody_head.log`)

| Cell | Caller | Head | Ruled |
|---|---|---|---|
| P0 / P1 | issuer org (with and without a custodian) | replaced | yes |
| P2 | the custodian user (org C) | replaced | yes |
| P3 | a colleague in custodian org C (not the custodian) | replaced | yes, (c) |
| P4 | a third org in the same tenant | kept | yes |
| P5 / P5b | tenant B / tenant B claiming org C's id | kept | yes |
| P6 | NULL issuer, colleague in C | kept | the known limit (C-f) |
| P7a | custodian moved C→N after the transfer; old colleague in C | kept | (c) reads the CURRENT org (author's Info confirmed) |
| P7b | the same, caller claiming N | replaced | as above |
| P8 | caller row says T, signed token says C | replaced | INF-A |
| P9 | token signed by a foreign key claiming C | **401** | the forged claim never reaches the guard |
| P10 | `alg: none` claiming C | **401** | as above |

- **Caller path, from source:**
  1. Client → gateway `POST /api/anchors` (`api-gateway/src/routes/proxy.ts:873-878`): `authenticateToken(true)` → `attachScopes` → `requireScope('anchors:write')`. That check short-circuits for JWT callers.
  2. `proxy('anchoring')`: `onProxyReq` forwards `Authorization` verbatim (`proxy.ts:297-299`) and sets no identity header for anchoring.
  3. Anchoring `app.use('/api', jwtAuthenticate())` (`index.ts:459`) → `packages/shared/src/middleware/index.ts:117-121`: RS256 verify via JWKS or the static key; `req.user = decoded`.
  4. `index.ts:476`: `caller = req.user` → `:507 dbPersistAnchor(anchor, caller)` → `:1369 mayOverwriteStoredMetadata(anchor.documentId, caller)` → `anchorOverwriteGuard.ts:257-273` → `readOwningDocument` (`:203-246`, tenant-bound twice) → `decideMetadataOverwrite` (`:145-192`).
  5. The decision is bound as `$23` and read only in the DO UPDATE CASE (`index.ts:1425`).
  6. Originate's six sites forward the end user's own bearer (e.g. `documents.ts:1339`). So the caller anchoring sees is the human user, and the `organizationId` is whatever auth signed.
- The gateway itself was not booted: steps 1-2 are from source. Anchoring was booted and hit directly; it verifies the token itself whichever hop it came through.

### 5. Mutation (`scripts/mutants.py`; `logs/mutants_run.log`, `logs/mutants_run2.log`)
- **Method:** one exact-once replacement per mutant, in a dedicated worktree. Each run executes originate's two ks1385 suites plus the anchoring integration lane, then restores the file with `git checkout`; the worktree was clean after both runs.
- **Kill rule:** at least one named cell fails with a non-empty message, the cell totals stay at the control's 31+30, and no suite fails to load.
- **Controls:** CTRL-none and CTRL-comment-only both stay green at 31+30.

| Mutant | Result | Killing cells |
|---|---|---|
| RED-a / author g8a (ship (a)) | KILLED | W3, C0, C-d |
| author g4 (NULL-issuer branch removed) | KILLED | M5, W3, C-f |
| author g8b (ship (b)) | KILLED | W3, C0, C-d |
| author g12 ((c) compares the custodian USER) | KILLED | W3, C0, C-c, C-e, C-d |
| author g13 ((c) also fires under (b)) | KILLED | C-b, C-c, C-d |
| m1 (mine) (c) fails open on a NULL custodian org | KILLED | M2, W3, C-c, C-e |
| m2 (mine) (c) widened to NULL-issuer rows | KILLED | M5, W3, C-f |
| m3 (mine) custodian JOIN matches any user in the tenant | KILLED | M2, C-e |
| m4 (mine) the (c) condition ignores the option | KILLED | C-b, C-c, C-d |
| i2 / i3 / i5 / s1 (mine, round-1 closures) | KILLED | H1+W2 / B1+W2 / W1 only (INF-C) / R1+R2 |
| k04 / k05 / k06 / g08 (round-1 survivors) | KILLED | K04 / K05+G08 / K06 / K05+K05b+G08 |

- **Totals:** 21 scored, 21 killed, 0 survived; controls green.
- **No mutant can see MAJ-A:** the fixtures carry the wrong key shape, so swapping `d.id` for `d.external_id` is invisible to every cell.

### 6. Merge prediction (`logs/merge_prediction.txt`, `scripts/09_merge.sh`)
- **Live tip:** develop `53b429ed` at 06:14:37Z. It is an ancestor of head, so the merge base is develop itself.
- **Overlap:** 17 PR files against 0 develop files since the merge base, so no file in common. Planted control: adding `anchorOverwriteGuard.ts` to the develop list shows 1 overlap.
- **merge-tree(develop, head):** rc=0, tree `e4d73a014c9f…`, which equals the head tree. A squash would land exactly the 17 files.
- **Planted conflicting control:** a develop commit that adds a conflicting `anchorOverwriteGuard.ts` gives rc=1, `CONFLICT (add/add)`.

## NOT tested
- **Originate was not booted.** That the six sites send `external_id` rests on source (`documents.ts:655`, `:902-903`, `:1985`, `:2397`, `:2502`; `documentRepo.ts:359`, `:437-438`). My cells reproduced the row shape `documentRepo` writes with my own INSERT, not by calling `saveDocument`.
- **The api-gateway was not booted.** Its part of the caller path is from source.
- **Platform S's real traffic was not observed:** I do not know which `documentId` S uses for K-minted documents (MAJ-A "NOT established").
- **No real Cardano.** Mock chain only. The batch path was not run end to end (INF-D).
- **Not re-run by me:** the author's in-hook 88/88 pre-push run and the remaining mutants of the author's 27 (only the named five, plus mine).
- **`packages/shared/dist`** was compiled in each worktree from that worktree's own source.

Merge only on Wednesday's head-bound GO. Nothing deploys from this verdict.
