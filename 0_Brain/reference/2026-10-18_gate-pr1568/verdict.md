VERDICT: NO GO at head 16e71610366b27276469e2215010416991b56ad5 (round 1 of 2). The fix delivers both rulings to real traffic, and the guard's decisions match what Kam ruled. But mixing the two id namespaces lets any tenant rewrite another tenant's certification identity. That is #1549's MAJ-1 again, by a new path, and on develop the same attempt is kept.
REPORT-SHA256/16: 41dc7991bc4fd6ff

# Gate verdict: PR 1568 (KS-1612 + KS-1385 (b)), round 1 of 2, Opus tier 1 full

- **Head gated:** `16e71610366b27276469e2215010416991b56ad5`. My own ls-remote returned it as `refs/pull/1568/head` at 2026-10-18T09:54:47Z and again at 10:08:10Z (`evidence/logs/receipts_lsremote_{1,2}.txt`).
- **Base:** the merge base is `d2ec786e6`, as the brief says.
- **Develop moved during the gate:**
  - It was `1197ab38` at 09:54Z and `833984fc` at 10:08Z.
  - The new commit is `833984fc`, KS-1114 (#1555, originate verify-by-title). It touches 7 files and none of them is in anchoring.
  - The e2e and lane arms ran on `1197ab38`. Its anchoring tree is byte-identical to `833984fc`'s, because no anchoring file changed. The merge prediction was re-run on `833984fc`.
- **Setup:**
  - Findings only. No git write verb was run in `!CODING`. No push. No GitHub or Linear write. No Docker.
  - Own `--shared` clone and five worktrees under `/private/tmp/claude-501/gate1568-1792317268/`.
  - Own Postgres 18 on 127.0.0.1:55623 (lsof showed it free; 55418 untouched). Repo schema loaded: `docker/init` then `migrations`. The 13 setup errors are all `_secuura_migrations` bookkeeping inserts.
  - `secuura_app` is NOSUPERUSER NOBYPASSRLS. `documents` and `users` are FORCE RLS. `documents.external_id` is globally `UNIQUE`. `anchor_store` is `UNIQUE (document_id, network)`, its `document_id` is `text`, and it has no tenant column (`evidence/logs/pg_setup.log`, `scripts/04_pg.sh`).
- **Counts:** Major 1 · Minor 2 · Info 8.
- **Evidence:** `evidence/` next to this file, split into `scripts/`, `cells/` and `logs/`.

## Why NO GO, in one paragraph
- **Why develop was safe.** It resolved an anchor's `documentId` only as `documents.id`, which is globally unique. So "this id names a document in my tenant" implied "the `anchor_store` row for this id is my document's".
- **What head changes.** It accepts the id as either `documents.external_id` or `documents.id`, each bound to the caller's tenant. `anchor_store` is one global text namespace. And nothing stops tenant B's `external_id` from equalling tenant A's **primary key**:
  - originate's own duplicate check is tenant-scoped (`routes/documents.ts:673`);
  - the `UNIQUE` on `external_id` cannot see a primary key.
- **Every certification is exposed.** Each one is anchored under its primary key, so any authenticated document-writer in any tenant can register a document with `documentUuid = <victim cert id>`. Its own issuer org then passes the guard on the victim's anchor row, and the anchored identity is replaced.
- **What I measured:**
  - The rewrite on the booted service (XT1, XT2).
  - The victim's public verify-by-hash afterwards serving tenant B's identity.
  - Originate's own repository functions accepting the colliding registration.
- **On develop**, the same sequence keeps the victim's identity.

---

## FOUND / TESTED / HOW

### MAJOR

**MAJ-1. Cross-tenant rewrite of a certification's (or any primary-key-anchored document's) anchored identity, through an external_id that equals another tenant's primary key**
- **Where:**
  - The guard:
    - `services/anchoring/src/anchorOverwriteGuard.ts:249-251`: `WHERE d.tenant_id = $2::uuid AND (d.external_id = $1 OR d.id = $3::uuid) ORDER BY (d.external_id = $1) DESC`.
    - Its decision is applied at `index.ts:1369` (`$23`) to the row `ON CONFLICT (document_id, network)` found. That row is not tenant-scoped.
  - Originate, the precondition:
    - `routes/documents.ts:458-470`: any `documents:write` caller may supply a v4 `documentUuid`.
    - `:673-679`: the shadow-pkey refusal runs on `getDocument(documentUuid, tenantId)`, so it is the caller's tenant only.
    - `documentRepo.ts:437-438`: the INSERT writes `external_id = documentUuid`.
    - `:903`: the create's own anchor body sends `documentId: id`, which is the victim's id.
  - Certifications are keyed this way by construction:
    - `certificationRepo.ts:211` writes `id = cert.id` with no `external_id`;
    - `certifications.ts:363` sets `id = uuidv4()`, which passes `UUID_V4_RE`;
    - `:452` anchors with `documentId: id`.
  - The victim's id is not secret. Public `GET /api/anchors/verify/:hash` returns it as `metadata.documentId` and `metadata.certId`, and the on-chain metadata carries it too.
  - The contradicted design claim is `anchorOverwriteGuard.ts:16-20`: "it can only ever REDUCE the set of overwrites — never add one".
- **TESTED, booted anchoring at head and develop** (`cells/gate_matrix.ts`, `scripts/07_e2e.sh`, `logs/gate_matrix_{head,dev}.log`, `logs/gate_matrix_side_by_side.txt`):

  | Cell | Setup | Head | Develop |
  |---|---|---|---|
  | XT0 (control) | tenant-B issuer, no colliding row in B, on tenant-A cert P | **kept** | kept |
  | XT1 | tenant-A cert P (NULL issuer, holder org C) anchored by a holder colleague; tenant B holds a document with `external_id = P` and issuer `ORG_TB`, the row originate writes for `documentUuid = P`; tenant-B issuer POSTs `documentId = P`, same hash | **REPLACED**, guard `allow: caller-is-issuer-organisation`. Stored actor `did:key:zTENANT_B_ATTACKER`, status confirmed | kept, `document-not-in-callers-tenant` |
  | XT1, public verify | `GET /api/anchors/verify/<tenant A's cert hash>` | before: `verified:true`, identity `zVICTIM_HOLDER_ORG`. **After: `verified:true`, identity `zTENANT_B_ATTACKER`** | both reads `zVICTIM_HOLDER_ORG` |
  | XT2 | the same against a tenant-A document anchored under its primary key (issuer `ORG_I`) | **REPLACED** | kept |

- **TESTED, the precondition through originate's own code** (`cells/originate_precondition.ts`, `logs/originate_precondition_head.log`). This drives `documentRepo.getDocument` and `saveDocument` through originate's `createPoolProxy`:
  - `getDocument(certPk, TENANT_B)` returns **null**, so `respondForExisting` would not refuse.
  - The control, `getDocument(certPk, TENANT_A)`, finds the cert.
  - `saveDocument({id: certPk}, TENANT_B, …, {conflictMode:'skip', issuerOrganizationId: ORG_TB})` returns **`inserted: true`**.
  - Two rows now answer to that id: A's cert (primary key) and B's document (`external_id`, `issuer_organization_id = ORG_TB`).
- **What the attacker needs:** a document-writer account in any tenant, plus the victim cert's content hash. The hash gives up the id through the public verify, and the guard requires equal `content_hash`, which the attacker supplies as `contentHash`.
- **Why the author's cells cannot see it:** X5, C-h and F5 put the stranger's tenant in the caller only. X6 builds the collision inside one tenant. No cell builds a colliding row in a second tenant.
- **Mutants cannot see it either:** it is the design of the resolution, not one condition.
- **Proposed residue (findings, not a fix):**
  - The guard must refuse when the id names a document in ANY other tenant, under either namespace. That needs a cross-tenant existence read; RLS hides those rows, so it has to be a narrowly scoped bypass or a SECURITY DEFINER lookup.
  - And/or originate must refuse a `documentUuid` that equals any document's primary key, globally, with a DB-level backstop.
  - Add a cell where the colliding row sits in another tenant.
  - Existing collided rows would survive a creation-side fix alone.
- **Scope note:** before this PR, on develop, the colliding create's anchor already lands on the victim's `anchor_store` row. It overwrites status, tx and the other 11 unconditional columns. That is pre-existing (KS-1603). Only `metadata_payload`, the identity, is new harm at head.

### MINOR

**MIN-1. The kept-payload log's quiet set is not preserved "exactly": develop-quiet keeps now log**
- **Where:**
  - `anchorOverwriteGuard.ts:280-282`: `isQuietKeep` requires `reason === 'document-not-in-callers-tenant'`.
  - But `decideMetadataOverwrite:176-179` returns `caller-has-no-organisation` or `caller-organisation-not-a-uuid` before it looks at `doc`.
- **What develop did:** develop (`index.ts:1485` at `1197ab38`) was quiet for every keep on a non-uuid id from a caller with a tenant, whatever that caller's organisation.
- **Measured on the booted service** (`logs/run_e2e_{head,dev}.txt`). A non-uuid id naming nothing, posted twice:

  | Cell | Caller | Head | Develop |
  |---|---|---|---|
  | L1 | no `organizationId` | **logs** (`caller-has-no-organisation`) | silent |
  | L2 | `organizationId` not a uuid | **logs** | silent |
  | L3 | a **connector** token without `organizationId` | **logs** | silent |
  | L4 (control) | connector with an org | silent | silent |

- **Why L3 matters:** auth mints connector tokens with no `organizationId` whenever the key's metadata has none (`auth/src/services/jwt.ts:292`). Platform S's flat repeats on such a key would log on every event, which is the noise develop deliberately suppressed.
- **The claim this contradicts:** the PR body and the `isQuietKeep` docstring both say "a non-uuid id that names NO document in the caller's tenant stays quiet". Q1-Q4 feed hand-made decisions, and no cell drives an org-less caller.
- **The other direction:** nothing develop logged becomes quiet. Head's quiet set is a strict subset, because non-uuid with no tenant is `caller-has-no-tenant` on both sides.
- **Two more new log lines, both arguably correct:**
  - L5: an allowed caller on a non-uuid id with a different content hash. The payload is kept under MAJ-2 and now logs with reason `caller-is-issuer-organisation`.
  - A database fault on a non-uuid id now produces the guard's own warning line, because develop never read that id.
- **Text only:** no authority effect.

**MIN-2. Stale authority text in the files this PR edits**
- `index.ts:1406-1409`, the upsert's SQL comment, still says the guard "confirmed the caller's organisation is the document's issuer. Custody option (a)". This is round-2 MIN-A of #1549, still open.
- `routes/documents.ts:896-898` still says "the overwrite applies only when the caller's organisation is the document's issuer". That is now wrong twice over, (c) and (b).
- The guard header `:16-20` says "never add one", which MAJ-1 contradicts.

### INFO
- **INF-1. Kam's (b) lets the holder's organisation overwrite one column, `metadata_payload`.** The plain statement for Kam is under item 4 below.
- **INF-2. The certificate's own issuing organisation cannot update its anchor** (C3: refused, `document-has-no-issuer-organisation`).
  - Certification rows have `issuer_organization_id` NULL, so only the holder's organisation qualifies.
  - Under (b) the holder's organisation may rewrite `issuerOrgId`, `orgDid`, `orgTrust` and `orgVerified` in the anchored payload, while the organisation that actually issued the certificate may not.
  - The ruling admits this; Kam may want to know it.
- **INF-3. (c) still trusts the signed `organizationId` claim, not the caller's live `users` row.** P8 is replaced on head and on develop. This carries over from #1549 r2 INF-A.
- **INF-4. Author mutant K2 is impure.**
  - `… AND $3::uuid IS NULL OR FALSE` also kills uuid-shaped external ids: its red set includes X2 and X6, 17 cells.
  - My pure primary-key-arm drop (G3) is killed by 15 cells (X7 and the primary-key cells). The author's conclusion holds.
- **INF-5. My G1 (ORDER BY dropped) is killed only by X6, and the kill depends on row order.** On this planner the primary-key row is returned first. A different plan could let it survive.
- **INF-6. One cold-run flake.** In the first head lane run, the FORCE-RLS file's `beforeAll` timed out (10 s hook timeout, 5 cells not run). The next 10 lane runs, at head and in every mutant, loaded all 47 cells (`logs/itest_head.json`, then `itest_head_2`, `itest_head_rls`).
- **INF-7. Unit lane 370/371 at head and at develop.** The one red is `threadTokenMint.test.ts` on both, as claimed. tsc `--noEmit` for anchoring gives 0 errors on both.
- **INF-8. The author's ESLint "0/0" is not reproduced.** My eslint call without `cd` linted 0 files; that is a tooling limit, not a finding.

---

## Gate items

### 1. Diff by hunk (`logs/pr.patch`, `logs/diff_stat.txt`, `scripts/02_diff.sh`)
- **Two commits:** `7408f5ec5` (the change) and `16e716103` (`let`→`const` at `index.ts:1103`).
- **Exactly the 4 named files changed:** the guard, `index.ts`, and the two integration tests. Nothing else.
- **`index.ts` hunks:**
  - the import;
  - the `const`;
  - the log condition, swapped to `!isQuietKeep(overwrite, anchor.documentId)` at `:1487`, with its comment.
- **Guard hunks:**
  - the header text;
  - `document-id-not-a-uuid` removed from the type;
  - `hasIssuer` and the reason moved after the custody block (`:183-204`);
  - `readOwningDocument` with the new WHERE, ORDER BY and the `$3` uuid parameter;
  - `isQuietKeep` added;
  - the early non-uuid return removed from `mayOverwriteStoredMetadata`.
- **Guard re-read whole.** The pure decision and the read are as J describes. The flaw is MAJ-1, not a mismatch with getDocument.

### 2. Authority matrix through the real route (booted anchoring, `secuura_app`, FORCE RLS, RS256; `logs/gate_matrix_side_by_side.txt`)
Each cell is a first anchor, then the caller under test. The table gives the guard's decision (the product function, same tree and database) and the stored actor afterwards.

| Cell | Anchor key | Second caller | Head | Develop |
|---|---|---|---|---|
| D1 | doc, `external_id` `doc-…` | issuer org | REPLACED (`caller-is-issuer-organisation`) | kept (`document-id-not-a-uuid`) |
| D2 / D3 | doc | colleague in the custodian org / the custodian himself | REPLACED (`caller-shares-custodian-organisation`) | kept |
| D4 | doc, NULL issuer | custodian-org colleague | REPLACED | kept |
| D5 | doc | another org, same tenant | kept (`caller-is-not-the-issuer-organisation`) | kept |
| D6 / D7 | doc | other tenant / other tenant claiming org C | kept (`document-not-in-callers-tenant`, quiet) | kept |
| D8 / D9 | doc | forged key / expired token | **401**, kept | 401, kept |
| C1 / C2 | cert, primary key, NULL issuer, owner = holder in C | holder-org colleague / the holder | **REPLACED** (Kam's (b)) | kept (`document-has-no-issuer-organisation`) |
| C3 | cert | the cert's issuing user's org | kept | kept |
| C4 | cert | another org | kept | kept |
| C5 / C6 | cert | other tenant / other tenant claiming C | kept | kept |
| C7 / C8 | cert | forged / expired | **401**, kept | 401, kept |
| N1 / N2 | non-uuid id naming nothing | same caller / other tenant | kept, quiet | kept, quiet |
| XT1 / XT2 | tenant-A primary key, tenant-B row with that `external_id` | tenant-B issuer | **REPLACED** (MAJ-1) | kept |

- **Stored row after each:** one row per id. The actor is as shown. Status is pending, or confirmed after the mock confirms.
- **The #1549 r2 e2e cell, re-run** (copied from J's evidence; sha256/16 `7efe3e50a12abda0`, byte-identical to the r2 gate's copy):
  - Head: X1-X3 replaced, P6 replaced. The other 12 P-cells are as before, with P9 and P10 answering 401.
  - Develop: X1-X3 kept, P6 kept.
  - Kept-payload lines during that cell: head 4, develop 7.
  - J's table is reproduced exactly (`logs/run_e2e_{head,dev}.txt`).

### 3. Resolution
- **R1, same-tenant collision.** Row E has `external_id = S`; row P has primary key `S`.
  - E's issuer is replaced; P's issuer is kept.
  - So the external id wins, as `getDocument` resolves it (`documentRepo.ts:238-250`).
  - Develop did the reverse, because it only knew the primary key.
- **R2, an id that exists only in tenant B:**
  - by `external_id`: kept, not-found;
  - by primary key, with the caller claiming B's org: kept, not-found.
- **R3, variants** (the guard function directly):

  | Variant | Head |
  |---|---|
  | external id, canonical | resolved |
  | external id, UPPER, padded, `{}`, no hyphens | **not** resolved; exact match, as getDocument does |
  | primary key, UPPER, space-padded, tab/newline-padded | resolved; the `::uuid` cast plus `trim` |
  | primary key, `{}`, no hyphens, `urn:uuid:` | not resolved |

  - Through the route, `UPPER(pk)` lands on a **separate** `anchor_store` row (text key). A variant cannot reach the canonical row (R3r).
- **The cross-tenant collision is MAJ-1.**

### 4. Kam's (b), plainly
**The plain statement for Kam:**

> Anyone whose signed token claims the certificate holder's current organisation (in the same tenant) can now replace that certification's anchored metadata (`metadata_payload`) on any later anchor of the same bytes.
>
> That covers the whole `secuura` block, which public verify-by-hash returns and the next chain transaction carries:
> - the seven identity fields: `actorDid`, `actorLevel`, `actorSource`, `actorVerified`, `orgDid`, `orgTrust`, `orgVerified`;
> - `issuerOrgId`, `environment`, `documentType`, `occurredAt`, `identityCommitment` and `certId`, all as the caller sends them.
>
> They cannot change the content hash, because the payload is kept unless the hashes and the `anchor_type` match. The certificate's own issuing organisation cannot do the same (INF-2).

- **Measured:** C1, C2 and D4.
- **From source:** the payload goes to the chain via `anchorSubmission.ts:449-453`.
- **Not new:** the 12 other columns in the DO UPDATE list (`status`, `transaction_hash`, block fields, `confirmations`, `confirmed_at`, `error_message`, `retry_count`, `simulated`, `updated_at`) were already writable by any caller on develop (KS-1603).

### 5. Mutation (`scripts/09_mutants.py`, `logs/mutants_run.log`, `logs/mutants/`)
- **Method:**
  - Each mutant is one exact-once replacement in a dedicated worktree.
  - Each run executes the whole anchoring integration lane on my Postgres.
  - The file is then restored, and its sha256 is asserted.
  - At the end the worktree had 0 tracked changes.
- **Results:**

  | Mutant | Result | Lane | Red cells |
  |---|---|---|---|
  | CTRL-none | green | 47/47 | — |
  | CTRL-comment-only | green | 47/47 | — |
  | K2 (author) | KILLED | 30/47 | 17 (INF-4) |
  | K3 (author) | KILLED | 46/47 | X6 |
  | K5 (author) | KILLED | 43/47 | F4 X1 X3 X4 |
  | N3 (author) | survived | — | — |
  | G1 (mine) ORDER BY dropped | KILLED | 46/47 | X6 (INF-5) |
  | G2 (mine) (b) over-widened to any caller in the tenant | KILLED | 44/47 | C-g M5 W3 |
  | G3 (mine) pure primary-key-arm drop | KILLED | 32/47 | 15 cells |

- **N3 is a true equivalent.**
  - When `hasIssuer` is false, `issuerOrganizationId` is null or blank.
  - `sameUuid` returns false for a non-string or a trimmed-empty side (`:142-147`).
  - So the guarded and unguarded conditions agree on every input.

### 6. The isQuietKeep seam
- **Quiet set:** not preserved exactly (MIN-1). It holds for the org-bearing callers, and nothing develop logged becomes quiet.
- **The red-first shim.** J's literal shim did not survive in his scratch: his `devbase` tree is now clean and re-pointed to `54f07feae`. So I rebuilt a faithful one: develop `1197ab38`, plus head's two test files, plus `isQuietKeep = (d) => d.reason === 'document-id-not-a-uuid'`, which is exactly develop's `index.ts:1485` condition (`scripts/11_redfirst.sh`).
- **Result:**
  - 34/47 pass and **13 red**: M4, C-f, C-i, X1-X6, Q1, W4, F4, F5. That is J's predicted set exactly (`logs/redfirst_run.txt`).
  - My reconstruction is consistent with his. The byte-identity of his own shim is unverifiable.

### 7. Merge prediction on live develop `833984fc` (`scripts/10_merge.sh`, `logs/merge_prediction.txt`)
- **Merge base:** `d2ec786e6`.
- **Overlap:** the PR's 4 files against develop's 11 files since the merge base gives **0 in common**. Planted control (the guard added to develop's list): 1.
- **merge-tree(develop, head):** rc=0, tree `7f22f6e3`. The tree differs from develop in exactly the 4 PR files, which equal head's.
- **Planted conflicting control:** a develop-side edit of the same guard line gives rc=1, `CONFLICT (content)` in `anchorOverwriteGuard.ts`.
- **Conclusion:** the merge is mechanically clean. It is not safe to merge (MAJ-1).

## NOT tested
- **Preflight legs 3, 4 and 8** (Docker or stack) were not run, by me or by the author. Docker is off-limits here.
- **The originate route was not booted, and neither was the gateway.** MAJ-1's precondition was driven through originate's repository functions (`getDocument`, `saveDocument`). That the create's anchor body sends `documentId: id` (`documents.ts:903`), and that the route's `respondForExisting` uses `getDocument` (`:673`), rests on source. The anchoring half of MAJ-1 was driven through the booted service.
- **No real Cardano.** Mock chain only. That the rewritten payload reaches the next chain transaction rests on source (`anchorSubmission.ts:449-453`).
- **Batch path:** not exercised.
- **J's literal red-first shim:** not recovered (item 6).
- **J's remaining mutants** (K1, K4, N1, N2, Q-a..Q-d): not re-run by me.
- **ESLint:** not reproduced (INF-8).
- **Platform S's real connector keys:** whether they carry `organizationId` (which decides MIN-1's live volume) was not observed.

Merge only on Wednesday's head-bound GO. Nothing deploys from this verdict.
