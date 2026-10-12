# QA gate: Secuura Platform K PR #1516 (KS-1508, versionedById is server-set), head 770d0f3d

- **Head under test:** `770d0f3de0743505d7c4b13b9b78679f2a5a56fb`. I fetched `refs/pull/1516/head` myself and it matched exactly. It is ONE commit (`rev-list --count` = 1) on `551dc9808aee1c89d217cd662628c17ef8ad3a0e`.
- **Delta:** 5 files, +412/-4.
  - `routes/documents.ts` +19/-4 and `routes/certifications.ts` +9/-1.
  - Two new test files: the unit file and the real-Postgres file.
  - The ks1293 manifest line.
  - `documentRepo.ts` is NOT in the delta, so `stripReservedMetadataKeys` is untouched.
- **Real develop:** `git ls-remote` returned `4ec53e1874d06636cacc08dd224d980139e5906b`. That is one commit past the PR base, and it changes one file: `services/auth/src/__tests__/ks1000-...test.ts`, which is test-only.
- **Author bundle:** sha256/16 is `54e230059e55e128`. Its head is `770d0f3d...` and it requires `551dc9808aee...`. `git bundle verify` passed in my clone. It matches the fetched ref.
- **How I got the tree:**
  - I made a `git clone --shared` of the main checkout into my scratchpad and fetched `refs/pull/1516/head`, `refs/heads/develop` and `refs/pull/1497/head` (`4ca146545f15...`) from `git@github.com:Secuura/Distributed_Secuura.git`. GIT_SSH_COMMAND was read (only) from the project's `core.sshCommand`.
  - I built the trees with `git archive` of tree objects from `git merge-tree --write-tree` (no checkout):
    - **merged** = #1516 onto develop 4ec53e18, tree `eb9d42a7`.
    - **dev** = develop 4ec53e18 (red-first).
    - **combo** = develop + #1516 + #1497, tree `876ef07d`.
    - **combo0** = develop + #1497 without #1516, tree `f156dad2` (the unfixed control).
  - node_modules is an APFS clone of my own earlier scratch `npm ci --ignore-scripts` install. It has the same `package-lock.json` (cmp identical) and the same `schema.prisma`, and its Prisma client was already generated. The `@secuura/*` links are relative, so they resolve into each scratch tree. `packages/shared` was built in each tree.
  - Nothing was written, fetched or checked out under `!CODING`.
- **Database:** my own throwaway PostgreSQL 15, TCP only on 127.0.0.1, data dir in my scratchpad.
  - Init SQL: 0 failed. Migrations: 49 applied, 0 failed, plus `003_platform_tenancy`.
  - `secuura_app` has rolsuper=f and rolbypassrls=f. FORCE RLS is t on documents, organizations, svc_api_keys and action_provenance.
  - It started on port 55516. I moved it to 55416 because `ks1263` refuses any port outside 55410-55419.
  - It is stopped now (`pg_isready` rc 2).
- **Tier:** 1 (OPUS). This is the guard in front of the destructive organisation erasure (#1497). Independent gate, 2026-10-13.

## VERDICT: GO WITH NOTE

**0 Majors. 1 Minor (non-blocking). Notes N-1 to N-8.**

I found no route, code path or body shape that still lets a caller plant a value the #1497 selector reads, in either tenancy mode.

- I planted `connector:<B's connector>` through all FIVE routes as org A, using both A's connector and A's human. I also tried 16 bypass shapes. Then I ran **org B's REAL erasure** (PR #1497's route, on the combo tree).
- Result: **0 of A's documents were blanked** in single-tenant mode and in pool mode.
- The same file on develop + #1497 *without* this PR blanked **13** of A's documents, and 14 of its 27 cells were red in both modes.

## Majors

None.

## Minor

**m-1. The published API contract does not say that the new behaviour exists.** The PR body and the commit message disclose it, but the spec does not.

- POST /api/documents now silently drops `data.versionedById`.
- On `/:id/version`, `/:id/sign-cert` and `/:id/sign-wallet`, four `metadata` keys are now reserved and silently overwritten: `versionAction`, `versionedAt`, `versionedById` and `parentDocumentId`. Before this PR the caller's value won.
- The spec still describes `metadata` as "free-form issuer metadata folded into the new doc's data blob" (`services/originate/src/originate.openapi.ts:1104-1107`, `:1134-1138`, `:1221-1222`, `:1294-1295`; the same text is in `docs/openapi/secuura-api.yaml`). It does not mention either drop.
- There is a precedent in the same file: the silent strip of `actorName`, `actorEmail` and `onBehalfOf` is documented at `originate.openapi.ts:795-800`.
- No reader depends on the old override (see the reader table), so nothing breaks. A caller who sets these keys just gets no error and no trace in the response.
- **Fix:** add one sentence to each description. This can be a follow-up and does not block.

## Notes

- **N-1. The author's tests do not pin that the hash is computed after the strip.**
  - My mutant X1 moved the strip below `const hash = clientHash || generateContentHash(data)` (`routes/documents.ts:656`). The unit file and the real-Postgres file both stayed **green** in both modes. Only my HASH and HASH2 cells killed it.
  - The code order is correct on the head (strip at `:607-610`, hash at `:656`, thread-token `metadataHashHex` at `:787-791`), and I proved it on real Postgres (below).
  - Worth porting the two HASH cells into the author's integration file.
- **N-2. The author's real-Postgres file does not cover the fifth surface (`/certifications/issue`).** The PR body says so. My gate file covers it on real Postgres in both modes:
  - P5 (human A) stores no `versionedById` on the derived row.
  - b15 (form-encoded) and b16 (`__proto__`) are also clean.
  - Mutants A6b and X4 on that path pass the author's integration file. The unit file and my file kill them.
- **N-3. Rows that already exist are not healed, and the #1497 selector still reads them.**
  - Cell b17: a pre-existing row with `metadata.versionedById = connector:<B>` and a NULL issuer **was blanked by B's erasure** (the expected residue). A /version of it made after the fix stores the actor and survives.
  - **Every** root row (`parent_document_id IS NULL`) that carries `versionedById` was planted by a caller: no create path has ever set it server-side. So #1497 could bound arm (b) to `parent_document_id IS NOT NULL`, or a pre-deploy data check could clear the key on root rows. That would close the residue, including the one unclassified QA row `313180f3-5850-48a7-9d82-f085cac6c6d4` named in the PR body. This is for #1497's deploy, not this PR.
  - Derivative rows planted before this fix cannot be told apart from real ones by shape alone.
- **N-4. On /certifications/issue the caller's `data.versionedById` is still visible outside the derived document.**
  - It is still echoed in the 201 response's `data`.
  - It is kept in the certification's own `certification_metadata.certificationData`.
  - It is covered by the certification's `contentHash` and by the derived row's `contentHash`. `generateDocumentContentHash(data)` at `routes/certifications.ts:531-533` hashes the caller's unstripped `data`.
  - The erasure reads none of these, and before this PR the derived row's hash was already not recomputable from its stored blob. Not a regression; disclosure only.
- **N-5 (pre-existing, unrelated).** POST /certifications/issue as a **connector** with no `holderId` answers 400 "Certification payload contains values that cannot be stored". The holder defaults to `connector:...`, which is cast to uuid. Cell P5b reports it. It is the same on the unfixed tree.
- **N-6 (out of scope, pre-existing, noting only).** The legacy certify path (`documentId` without `parentDocumentId`, `routes/certifications.ts:557-575`) runs `UPDATE documents SET status='certified', certification_metadata=...` with `WHERE external_id = <caller's documentId> AND tenant_id`. It has no organisation or owner predicate. It writes `certification_metadata`, which the erasure does not read, so it does not affect KS-1508.
- **N-7.** In the first parallel run of all six originate integration files with MT=true on the merged tree, I saw 14 failures, all "Exceeded timeout of 30000 ms". This was right after I restarted the database on its new port.
  - It did not reproduce: two parallel repeats were 48/48 each, `--runInBand` was 48/48, and develop in parallel was 42/42.
  - I count it as an environment blip, not a PR effect.
- **N-8.** The author says the PR's unit file had 25 of 44 cells red first. I ran the unit file at head (46 cells) against develop and got **26 of 46 red**. That is consistent: the file grew after the author's red run.

## What I ran (all Postgres cells as `secuura_app`, in single-tenant mode and in pool mode)

Raw output is in `evidence_runs.txt`, `evidence_attack_runs.txt` and `evidence_mutations.txt`. My test file is `gate1516-attack.integration.test.ts.txt` and the mutation harness is `mut.py.txt`.

### 1. Topology

- **Merge onto develop 4ec53e18:** `merge-tree` rc 0, clean.
- **Delta:** the 5 files listed above.
- **Overlap with #1497's 10 files (head 4ca14654):**
  - #1516 vs #1497 = **0**.
  - Control, #1497 vs itself = 10.
  - Control, #1497 contains `src/db.ts` = 1 and `routes/documents.ts` = 0.
- **The full stack merges cleanly:** #1516 + #1497 on develop is rc 0 (tree `876ef07d`).

### 2. The author's files, re-run

| Run | Single-tenant | Pool |
|---|---|---|
| Real-Postgres file on merged | 6/6 | 6/6 |
| Same file on develop (red first) | 4/6 red: create, /version, /sign-cert, /sign-wallet | the same 4/6 red |
| All 6 originate integration files on merged | 48/48 (`--runInBand`, and 48/48 in parallel) | 48/48 (`--runInBand`, and 48/48 twice in parallel; see N-7) |
| Unit file on merged | 46/46 | — |

- The fallback-warning grep (`falling back to single-tenant`) returned **0** on every run.
- **Positive control for that grep:** pool mode with no `PLATFORM_DATABASE_URL` gave fallbackWarn=2, and the SETUP cell went red (`getTenantManager() !== null` was false). So the zeros are real.
- The gate file prints `poolBranch=true` in pool mode and `false` in single-tenant mode.

### 3. Suites and static checks on merged `eb9d42a7`

- originate `npx jest`, twice: 102 suites / 1215 tests, rc 0 both times.
- `packages/shared` vitest, twice: 49 files / 949 tests, rc 0 both times.
- `tsc --noEmit` in originate: rc 0, no output.
- eslint on the PR's 5 files: rc 0, no output.
- `npm run check:openapi`: rc 0, "CHECK PASS: on-disk YAML matches generated", 413 example blocks.
- These match the author's figures.

### 4. Re-proving the fix route by route, with org B's REAL erasure

The gate file `gate1516-attack.integration.test.ts` drives the real `documentsRouter`, `certificationsRouter` and `platformOrganizationsRouter` on combo (develop + #1516 + #1497).

- The body parsers are mounted in production order: `express.json` and then `express.urlencoded({extended:true})`, as in `index.ts:104-105`.
- A's source documents have a NULL issuer (no `organizationUuid`), because that is the shape arm (b) of the selector reaches.
- The plant is `connector:platform-s:<B GUID>`.
- After all the plants, B's connector calls `POST /api/platform/organizations/erase-connector` and the cell reads every planted A row.

**Results:**

- **combo: 27/27 in single-tenant mode, 27/27 in pool mode.**
- **combo0 (unfixed): 14/27 red in both modes.**
- B's erasure answered `200 completed`:
  - On the fixed tree: `documentsBlanked:2`. These were B's own document (the positive control, `[erased]`) and the b17 pre-existing row (N-3).
  - On the unfixed tree: `documentsBlanked:13`.

| # | Route | Caller(s) | Stored `versionedById` after the fix | Unfixed (combo0) | After B's erasure (fixed) |
|---|---|---|---|---|---|
| 1 | POST /api/documents | A connector, A human | key absent (`has_key=false`) | key = B's connector | survives |
| 2 | /:id/version (also plants `versionAction`, `versionedAt`, `parentDocumentId`) | A connector, A human | the actor (`connector:platform-s:<A>` / the human's uuid); `versionAction=watermark`; `data.parentDocumentId` = the source | B's connector | survives |
| 3 | /:id/sign-cert | both | the actor | B's connector | survives |
| 4 | /:id/sign-wallet | both | the actor | B's connector | survives |
| 5 | /certifications/issue + parentDocumentId | A human | key absent on the derived row | B's connector | survives |

- **Log cell (P1):** exactly 2 KS-1508 info lines, one per planted create. Each carries `{tenantId, userId}` only, and neither contains B's GUID.
- **HASH, create with no contentHash, on real Postgres:**
  - The planted and unplanted creates stored the **same** `content_hash` (`50bd89ae...`), which differs from `generateContentHash` of the blob with the key in it (`59bb2b52...`).
  - Control: a create with one extra benign key gets a different hash (`d39df798...`).
- **HASH2:** with `STATE_THREAD_NFT_ENABLED=true` and the mint client captured, `metadataHashHex` = sha256 of `{"title":"T","note":"n"}`, which is the stripped blob. It is not the sha256 of the blob with the key. Both cells are red on the unfixed tree.

### 5. Bypass shapes, all on real Postgres in both modes, each followed by B's erasure

| Shape | Result after the fix | Unfixed |
|---|---|---|
| b1 `VersionedById` (case) | stored as a different key; selector does not match; survives | survived (never matched) |
| b2 `"__proto__":{"versionedById":...}` raw JSON on create | own key `__proto__` stored, no top-level key; survives | survived |
| b3 duplicate `versionedById` keys, raw JSON | stripped (JSON.parse keeps one) | **blanked** |
| b4 form-encoded `data[versionedById]` | stripped | **blanked** |
| b5 unicode lookalikes (fullwidth v, a trailing ZWSP) | stored verbatim; Postgres does not normalise keys; no match; survives | survived |
| b6 nested `data.meta.versionedById` | not top-level; survives | survived |
| b7 top-level `body.versionedById` | ignored (never enters `data`) | survived |
| b8 `data` as a JSON *string* | 400, nothing stored | 400 |
| b9 array value `[...]` | stripped | stored, but `->>` of an array never matches |
| b10 legacy shape (no `data`) + top-level key | ignored | survived |
| b11 /version, form-encoded `metadata[versionedById]` | the actor | **blanked** |
| b12 /version, `__proto__` in metadata | the actor | survived |
| b13 /version, `metadata` as an array | 400 (validator), nothing stored | 400 |
| b14 /sign-cert, duplicate keys in metadata | the actor | **blanked** |
| b15 cert issue, form-encoded `data[versionedById]` | stripped from the derived row | **blanked** |
| b16 cert issue, `__proto__` in data | own `__proto__` key, no top-level key | survived |
| b17 /version of a pre-existing planted source row | the derived row gets the actor and survives; **the pre-existing row itself is blanked** (N-3) | — |

- **Copy versus original:** `data` (`routes/documents.ts:598-601`) is a shallow copy of `rawData`. It is the same object that is hashed (`:656`), placed in `document.data` (`:703`) and persisted. The strip deletes from that object.
- Mutant X2 strips a throwaway copy instead, and every layer kills it.
- The version routes overwrite after the caller's spread, so how the caller's object is shaped cannot matter there.

### 6. Mutation (combo tree; tsc rc 0 required; every file restored byte-identical by sha256)

The layers are:
- **U:** the author's unit file.
- **AF / AT:** the author's real-Postgres file, single-tenant / pool.
- **GF / GT:** my gate file, single-tenant / pool.

| Mutant | U | AF | AT | GF | GT | Result |
|---|---|---|---|---|---|---|
| A1 `delete` → `void` | R | R | R | R | R | killed |
| A2 strip block removed | R | R | R | R | R | killed |
| A3 /version order reverted | R | R | R | R | R | killed |
| A4 /sign-cert order reverted | R | R | R | R | R | killed |
| A5 /sign-wallet order reverted | R | R | R | R | R | killed |
| A6 cert spreads `...data` | — | — | — | — | — | uncompilable (TS6133), replaced by A6b |
| A6b cert re-spreads `data` after the strip | R | g | g | R | R | killed |
| A7 create log removed | R | g | g | R | R | killed |
| A8 cert log carries the value | R | g | g | g | g | killed (unit only) |
| A9 /version actor taken from metadata | R | R | R | R | R | killed |
| A10 create log without the tenant | R | g | g | g | g | killed (unit only) |
| **X1 strip moved after the hash** | **g** | **g** | **g** | R | R | killed **only by the gate** (N-1) |
| X2 strip applied to a throwaway copy | R | R | R | R | R | killed |
| X3 /version neighbours before metadata (actor kept) | R | g | g | R | R | killed |
| X4 cert strips `VersionedById` instead | R | g | g | R | R | killed |

- 14 compilable mutants, 14 killed: the author-shaped A1-A10 (with A6b) and my own X1-X4.
- The restore sha256 values are `258786f5cc09737e` (documents.ts) and `6692992be9446bbd` (certifications.ts). The before and after values were equal every time.
- The author's own 12 mutants were not given to me, so A1-A10 target the same lines.

## (3) Attack A: every writer of `documents` and every place a DocumentRecord or metadata is built

- **How I searched:**
  - A regex over services/, packages/ and connectors/ for `INSERT INTO documents`, `UPDATE documents`, prisma `.document(s).create|update|upsert`, `saveDocument(`, `updateDocument(` and `Unsafe(`.
  - A sweep of every `DocumentRecord = {` construction.
  - A list of every file outside originate that mentions `documents`, triaged one by one.
- **Positive control:** `routes/documents.ts` hit on `saveDocument(`, and the routes file list is complete (14 files).

| Writer | Where | Can a caller reach it? | Can a caller set `metadata.versionedById`? |
|---|---|---|---|
| `saveDocument` ← POST /api/documents | `routes/documents.ts:715` | yes | **no**: stripped at `:607-610` (FIXED) |
| `saveDocument` ← /:id/version | `:2128` | yes | **no**: server keys come after `...metadata` (`:2110-2120`) (FIXED) |
| `saveDocument` ← /:id/sign-cert | `:2866` | yes | **no** (`:2846-2854`) (FIXED) |
| `saveDocument` ← /:id/sign-wallet | `:3060` | yes | **no** (`:3041-3049`) (FIXED) |
| `saveLineageDocument` ← /certifications/issue + parentDocumentId | `routes/certifications.ts:541` | yes | **no**: destructured away at `:512` (FIXED) |
| `saveCertification` INSERT | `repositories/certificationRepo.ts:199` | yes (issue, revoke, share, recertify) | no: `metadata = {}`; caller data goes to `certification_metadata` |
| `updateDocument` (13 callers) | `documentRepo.ts:517` | yes, indirectly | no: rebuilds metadata from the STORED row; no caller passes `data` (grep for a `data` key in the updates: 0, control: `blockchain` 75) |
| `seedDemoDocuments` | `documentRepo.ts:930`, `documents.ts:208` | no (boot, non-production) | fixed seed content |
| transfer-custody owner flip | `documents.ts:1894` | yes | no: `owner_user_id` only |
| legacy certify UPDATE | `certifications.ts:570` | yes | no: `certification_metadata` only (N-6) |
| admin backfill | `adminConfig.ts:1856` | admin | no: `certification_metadata` only |
| GDPR erase / anonymise | `gdprService.ts:735`, `:840` | admin / DSR | no: fixed `{"anonymized":true}` |
| api-gateway startup migrations | `startup-migrations.ts:710-718` | no | `tenant_id` only |
| demo-service seed | `seed/generators/documents.ts:173` | no (seed script) | `{documentNumber}` |
| m365-integration sync | `index.ts:233` | yes | writes its own table `svc_synced_documents`, not `documents` |
| nft-certificate | `minting.service.ts:148-173` | — | reads certifications only |
| mcp-server register tool, connectors, sdk, gateway proxy | `mcp-server/src/api-client.ts:58`, etc. | yes | everything goes through POST /api/documents (fixed) |
| api-gateway batch certify | `routes/batch.ts` → POST `/api/certifications` | yes | goes through originate; no `documents.metadata` path of its own |

**There is no sixth surface.** The author's claim stands, and my search covered more ground than theirs.

## (4) Attack B: readers of the reordered or stripped keys

- **Search:** `git grep -i` over the whole repo at the PR head, including the frontend, mcp-server, docs, the OpenAPI yaml and tests.

| Key | Non-test readers | Depended on the caller overriding it? |
|---|---|---|
| `versionedById` | none in the repo outside the writers. The only reader is #1497's selector (`connectorOrganisationErasure.ts:292`, `:300`, `:317`, `:325`), which WANTS the server value | no |
| `versionAction` | none (writers only, `documents.ts:2116`, `:2851`, `:3046`) | no |
| `versionedAt` | the response fields are built from `now`, not from data (`documents.ts:2159`, `:2896`, `:3087`); the spec has a response field only (`originate.openapi.ts:1167`) | no |
| `parentDocumentId` (the copy in data) | none. Lineage readers use the column (`fromDbRow` `:182`, `parent_document_id`); the cert response echoes the request value | no |

- The repo-wide count of files naming `versionedById` or `versionAction` is 5. All are the PR's own files, and no test echoes these keys.

## (8) What the silent strip does to a legitimate caller

- **Round trip:** GET /:id returns `data` with the stored metadata spread into it, which includes `versionedById` on a derivative.
  - POSTing that `data` back into a create still answers 201. The key is dropped and logged.
  - Nothing else changes, and no test or flow in the repo echoes the key.
  - Such a round trip can still fail on the *pre-existing* `data.documentType` equality rule. That is not this PR.
- **Version routes:** a caller-supplied `versionAction`, `versionedAt`, `parentDocumentId` or `versionedById` in `metadata` is now overwritten. There is no reader of the old override, but the published contract does not say so (m-1).

## NOT TESTED / NOT RUN

- The author's push hook and preflight (13/16 legs): NOT RUN.
- The author's own 12 mutants as written: not supplied. I re-derived 10 (A1-A10) and added 4 of my own.
- Through the api-gateway (proxy, gateway auth, `sanitizeInput` skip): NOT TESTED. Originate was driven directly with a stubbed auth middleware; the gateway proxies the raw stream for /api/documents.
- `/certifications/issue` as a connector with a valid `holderId`: NOT TESTED (N-5). The fifth surface was proven with a human caller and in the author's unit file with a connector.
- Content types other than JSON and form-encoded (`text/plain`, multipart): NOT TESTED. Originate mounts only json and urlencoded, so other bodies arrive as `{}`.
- Platform S behaviour and the existing Kintsugi rows: NOT TESTED (no access, read-only brief).
- Superuser-role runs: NOT RUN. Every cell ran as `secuura_app`.
- A Schemathesis or OpenAPI fuzz of the new behaviour: NOT RUN.
