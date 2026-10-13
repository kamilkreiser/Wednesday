VERDICT: NO-GO
REPORT-SHA256/16: 40bdc24d2e1f07dc

# Gate verdict: PR 1549 (KS-1385, anchors carry the latest event's identity)

- **Head gated:** `aca6efb0864b11360eca90d1217d72ccd24e10ac`. It matched `refs/pull/1549/head` on my own ls-remote at 2026-10-13T11:05:40Z and again at 11:12:09Z (`evidence/receipts_merge.txt`).
- **Develop measured:** `92d1316ffe31cb13b3f7e843e7891225383b2f84`, the LIVE tip from my ls-remote. The brief said `d53d80cb`, but develop moved one commit after the brief was written (KS-1594, which touches `adminConfig.ts` plus one integration test). The PR has no file in common with that commit.
- **Gate:** independent, findings only. I made no change to the project. All work ran in a `--shared` clone and in worktrees in my scratchpad, against my own Postgres 18.3 on 127.0.0.1:55549. I checked with lsof that nothing was listening on that port first.
- **Counts:** Major 2 · Minor 3 · Info 7.

## Why NO-GO, in one paragraph
The ruling says "Latest event's identity wins". The PR implements that by making `anchor_store.metadata_payload` overwritable (`services/anchoring/src/index.ts:1385`). That one line turns a row that was write-once into one that any authenticated caller can rewrite. Anchoring's `POST /api/anchors` has never checked that the caller owns `documentId`. That gap is older than this PR, but until now the first payload stayed in place, so it could not change the stored attestation. The PR also leaves `content_hash` out of the update list, so the column and the payload's own `hash` can now disagree. I booted the real anchoring service at head and logged in as a user from a different tenant. That user rewrote another tenant's anchor. Afterwards, the public verify-by-hash for the victim's bytes returned `verified: true`, but with the stranger's content hash, organisation and "government / level 3" identity. Develop, as the control, keeps the victim's attestation. The ruling is about which legitimate event's identity is stored; it does not authorise this.

---

## FOUND / TESTED / HOW

### MAJOR

**MAJ-1. Any authenticated caller, from any tenant, can rewrite another tenant's stored anchor attestation**
- **Where:** `services/anchoring/src/index.ts:1385` (the new `metadata_payload = EXCLUDED.metadata_payload`). Path to it:
  - `index.ts:463-503`: `POST /api/anchors` parses the body and upserts on `(document_id, network)`, with no check of who owns the document or which tenant it belongs to. The `caller` object at `:474` is used only for the connector provenance row.
  - `services/api-gateway/src/routes/proxy.ts:873-878` together with `middleware/scopes.ts:36-39`: a human JWT caller skips the `anchors:write` scope check.
- **FOUND:** Before this PR, a second POST for someone else's `documentId` could only make the platform re-mint the victim's own first payload. That is a cost problem and a tx-hash churn problem, not a falsification. After this PR the second POST replaces every field in the payload: `hash`, `issuerOrgId`, `certId`, `documentType`, `occurredAt`, `identityCommitment` and all seven identity fields. The next transaction then anchors the stranger's payload on chain.
- **TESTED (end to end, real service):** `evidence/cells/http_overwrite.ts`, output in `evidence/http_overwrite.log`.
  - Setup: anchoring `src/index.ts` booted with tsx at head (port 55551) and at develop (port 55552), mock-chain mode, my Postgres, and an RS256 key pair I generated.
  - Step 1: user `1111…`, tenant-A, anchors `doc-…-http` with hash `a1…`, org `org-A`, identity `did:key:zVICTIM` level 2.
  - Step 2: user `2222…`, tenant-B, role USER, POSTs the same `documentId` with hash `b2…`, org `org-B`, identity `did:key:zSTRANGER` level 3, `orgTrust: government`.
  - **Head result:** the stranger's POST returned 202 with the victim's row id (`sameRowId: true`). The public `GET /api/anchors/verify/a1…` then returned `verified: true` with `metadata.contentHash = b2b2…` (not the hash that was requested), `issuerOrgId: org-B`, `documentType: null` and the stranger's identity. The victim's own `GET /api/anchors/:id` shows `contentHash a1a1…` next to the stranger's identity.
  - **Develop control:** the same requests leave `org-A`, `upload` and `did:key:zVICTIM` in place. The tx hash is still re-minted there, which is the older behaviour.
- **Downstream:** originate's public file-verify shows `issuer: chain.metadata.issuerName || issuerOrgId` and `documentType` from this response (`originate/src/routes/verification.ts:709,712`; `verificationV2.ts:247,252`). The overwritten values therefore reach public verifiers.
- **NOT tested:** this exact path through the booted api-gateway. The gateway's reachability is from reading the code only (proxy.ts and scopes.ts as cited).

**MAJ-2. `content_hash` is kept while `metadata_payload.hash` is replaced, so verify-by-hash confirms one set of bytes with a transaction that attests another**
- **Where:** `index.ts:1385`, with `content_hash` deliberately left out of the update list. The verify query at `index.ts:628` matches on `content_hash`, and the response builder sets `metadata.contentHash = sec.hash` at `anchorReadback.ts:144`.
- **FOUND:** Suppose an upsert on an existing `(document_id, network)` carries a different `contentHash`. After it:
  - `content_hash` still holds the OLD hash;
  - the payload, and therefore the next transaction the submitter builds from the row (`anchorSubmission.ts:436`, `current.metadataPayload`), carries the NEW hash.
  - So verify(OLD) returns `verified: true` with a transaction whose anchored hash is NEW, and verify(NEW) gets 0 rows from the DB.
  - The PR's own comment says this exclusion is "unruled". The exclusion is exactly what makes the row contradict itself.
  - On develop the row stays consistent: OLD everywhere. The new hash was never anchored there, but nothing was falsified.
- **TESTED:**
  - `evidence/cells/upsert_cell.ts`, output in `evidence/upsert_cell.log`. It runs the product's own extracted upsert SQL, the product's payload builder and the product's verify builder, against real Postgres.
  - Step E4, head: `content_hash: aaaa`, `payload_hash: bbbb`. `verify-by-hash(HASH_A)` returns `verified: true`, `metadata_contentHash: bbbb`, `issuerOrgId: org-other`. `verify-by-hash(HASH_B)` finds 0 DB rows.
  - Develop arm: `payload_hash: aaaa`, consistent.
  - Confirmed on the booted service as well (MAJ-1).
- **NOT established:** whether any LEGITIMATE flow sends a different `contentHash` for an existing `documentId`. Originate's six sites always send that document's own hash (it is fixed per document id; versions are separate rows, per migration 031). The proven trigger is MAJ-1's path and any flat-anchor caller.

### MINOR

**MIN-1. The invariant "the stored identity is the identity of the event that produced the stored tx" does not hold under concurrency, and the author's cell G2 does not model the real flow**
- **Where:** the upsert at `index.ts:1359-1385` and the submitter at `anchorSubmission.ts:430-465`.
- **What happens:** the upsert resets the row to `status = 'pending'` and `transaction_hash = NULL`, and the submitter later writes the tx. If event 2's upsert lands while event 1 is between "read payload inside the wallet lock" and "write `submitting`/`submitted` + tx1", then:
  - the row ends with payload 2 next to tx1, whose on-chain payload is event 1's;
  - event 2's own submit sees `submitted` + tx1 and does not mint (`submits: 1`).
- **TESTED:** `evidence/cells/race_cell.ts`, output in `evidence/race_cell.log`. It uses the real `createAnchorSubmitter` (real lock and guards), real Postgres and the product's upsert; only the chain is faked.
  - **Head race:** `storedActor: did:key:zSHARER`, `actorInTheTxOnChain: did:key:zUPLOADER`, `invariantHolds: false`.
  - **Head serial (control):** holds.
  - **Develop race and serial (control):** both hold.
- **Why the author's cell misses it:** G2 (`…latest-events-metadata.integration.test.ts:118-127`) "proves" the invariant by writing `transaction_hash` in the same upsert, and the product never does that. The window is the build/sign/submit time, which is short but real.

**MIN-2. Three of `emitLifecycleAnchor`'s four call sites are not pinned by any cell, including `share`, the case the ruling was made for**
- **Where:** `documents.ts:1973` (transfer-custody), `:2385` (share), `:2490` (revoke).
- **TESTED:** `evidence/cells/mutants.py`, raw output in `evidence/mutants_run.log`. All 28 cells (24 originate + 4 anchoring) stay green for each of these mutants:
  - k04: delete the `identity:` line at transfer-custody;
  - k05: delete it at share;
  - k06: delete it at revoke;
  - g08: at share, forward `(req as any).user` (the caller's JWT object) instead of the body's block.
- Only the generic `/lifecycle-events` caller is exercised (cell C8; k07 killed).
- The author's "14/14 killed" therefore does not hold for an enumeration of the PR's own listed sites (see the mutant table).

**MIN-3. A batch item for an already-anchored document now wipes the stored attestation and leaves a hybrid row**
- **Where:** `index.ts:772-792`. The batch path persists each item through the same upsert with a batch-shaped payload and ignores the returned id.
- **TESTED:** `evidence/cells/batch_cell.ts`, output in `evidence/batch_cell.log`.
  - **Head:** the row keeps `anchor_type: single`, label 674 and `merkle_root: null`, but its payload becomes `type: batch` with `hash` ABSENT and `actorDid` ABSENT. Status is `pending` and the tx is null. The batch item's id finds 0 rows, so `processBatchAnchor` returns early. That early return is older than this PR.
  - **Develop:** the payload, hash and identity are kept.

### INFO

- **INF-1. The claimed consequence set is inaccurate.** The PR body, the comment at `index.ts:1378` and the comment at `documents.ts:881` say "documentType and signatureHash" are overwritten.
  - `signatureHash` does not exist in the anchored payload. It has 0 hits in anchoring and originate non-test source apart from these new comments (instrument: `git grep -n -i signatureHash`; control: `documentType` has 8 hits in `anchorSchema.ts`).
  - What is actually overwritten is the whole `secuura` object: `hash`, `certId`, `issuerOrgId`, `timestamp`, `environment`, `occurredAt`, `identityCommitment` (KS-721; S compares it for equality) and the seven identity fields.
  - K-internal emits never send `metadata.documentType` (`anchorSchema.ts:177`), so any originate-site event after an S flat anchor resets `documentType` to null (upsert cell E2, head arm).
- **INF-2. Whose identity is it?** Nothing binds the forwarded block to the authenticated caller. The helper forwards the body verbatim, and anchoring checks only its shape (`anchorSchema.ts:109-118` says outright that "K proves SHAPE … never SEMANTICS").
  - At all six sites any authenticated caller, not just S's connector, can assert any DID and the highest trust level (`evidence/identity_edges.log`, case "different actor, max claims": all seven fields anchored).
  - Anchoring's direct path has allowed this since KS-1175. This PR adds six more ways in.
  - Kam's ruling decides whose identity wins, not who may assert one; this is left for Wednesday to rule on.
- **INF-3. Identity edge cases.** Instruments: the product helper plus `anchorDocumentSchema` (`identity_edges.log`).

  | Input | What the helper does | What anchoring does |
  |---|---|---|
  | absent / `null` | drops the key | byte-identical body |
  | string, number, `false`, array | forwards it | 400 "Expected object" |
  | `{}` | forwards it | 202 with no identity fields, which **erases** the stored identity under latest-wins |
  | 513-char DID | forwards it | 400; 512 is accepted |
  | extra keys (`actorName`, `actorEmail`, `nested`) | forwards them | stripped |
  | `actorLevel: 4` | forwards it | 400 |

  A malformed block used to be dropped silently. Now it fails the anchor:
  - site 1: the document is marked `anchor_failed` (fail-closed, retryable; `documents.ts:~960-980`);
  - site 3: the event is recorded without an anchor;
  - sites 6/7: `anchoringStatus` is `failed`.

  This is the intended behaviour per `utils/anchorIdentity.ts:10-13`.
- **INF-4. Bonus fix the PR does not claim.** On develop, every later event re-mints the FIRST payload on chain: in the race-cell serial develop arm, the share's tx carries `did:key:zUPLOADER`. At head the share's tx carries the share's identity, so on-chain attribution improves as well.
- **INF-5. Scope note.** `documents.ts:925-935` now stores up to 500 characters of anchoring's error body in `blockchain.error` (cell C7). It is outside the identity ruling, but small, bounded and related.
- **INF-6. Lane globs (pointer 3) are correct.** Planted always-red files were collected as follows (`lane_globs.txt`, from `vitest list`):
  - `zzgate-unit.test.ts`: default lane only;
  - `zzgate-planted.integration.test.ts` and `gatesub/zzgate-nested.integration.test.ts`: integration lane only;
  - `src/zzgate-outside.integration.test.ts`, outside `__tests__`: neither lane, the same as the default include before this PR.

  The default lane totals 371 at both head and develop, so the integration file is not in it. With no DB URL, the integration lane exits with rc=1 and "refusing to pass".
- **INF-7. Pointer 1 (certifications mocks).** I found no early return that would make the site-6/7 cells pass without exercising anything:
  - C17 and C18 require a recorded anchor POST that carries the block;
  - k10 and k11 each fail exactly their cell;
  - C17b and C18b would fail with `hit` undefined if the route returned early.

  Pointer 2 is confirmed: the upsert cell pins the statement, not `dbPersistAnchor`'s parameters. It also uses a made-up payload shape (`{identity:{…}, documentType}` instead of the real `{secuura:{actorDid,…}}`). My cells use the product's real builder instead.

---

## Gate items

1. **Diff by file:** 12 files and 26 hunks (counted with `git diff 026c2d16..aca6efb0`), nothing outside the 12.
   - **Product:** `anchoring/src/index.ts` (1 hunk: upsert + comment); `originate/src/utils/anchorIdentity.ts` (new helper); `routes/anchors.ts` (3 hunks: import, site 4, site-5 exclusion comment); `routes/certifications.ts` (3 hunks: import, sites 6 and 7); `routes/documents.ts` (11 hunks: import, site 1 + comment, error detail [INF-5], `emitLifecycleAnchor` param/destructure/spread, site 2, four call sites).
   - **Test infrastructure:** `anchoring/package.json` (script), `vitest.config.ts` (exclude), `vitest.integration.config.ts` (new).
   - **Tests:** 3 new suites, plus the `ks1293` SUBJECTS list (2 lines).
2. **POST /api/anchors sites:** I swept every non-test source file (`git grep -F '/api/anchors\`'` plus `fetch(anchorUrl`; `evidence/sites.txt`). There are exactly 7 in originate:
   - `documents.ts:838/918` (site 1), `:1401` (site 2), `:1322` (site 3);
   - `anchors.ts:283` (site 4), `:400` (site 5);
   - `certifications.ts:445` (site 6), `:1201` (site 7).

   `anchorIdentityFields(` is called exactly 6 times in `routes/`, and site 5 has no call. No other service POSTs to anchoring's `/api/anchors`. The gateway's `proxy.ts:873` passes S's own flat call straight through, and `threadTokenClient.ts:65` goes to `/api/anchors/thread-mint`, a different schema. Sweep control: the same pattern family finds the `/api/anchors/...` fetches in 4 files.
3. **Identity block:** INF-2 and INF-3.
4. **Upsert:** MAJ-2 and the upsert cell.
   - **Overwritten:** status, tx (reset to NULL), block fields, error, retry count, simulated flag, `updated_at` and now `metadata_payload`.
   - **Kept:** `id`, `content_hash`, `created_at`, `anchor_type`, `merkle_root`/`merkle_proof`, `metadata_label`.
   - **Same event replayed (E3):** the payload `timestamp` changes, the tx resets and a fresh tx is minted for a duplicate event. The re-mint is older than this PR.
   - **The invariant:** holds when events are serial, fails under the MIN-1 race, and is broken by MAJ-2 when the hash differs.
5. **Consumers of `metadata_payload`:** I swept with `git grep -i "metadata_payload|metadataPayload"` across the repo. The overwrite effect on each reader:

   | Reader | Effect of an overwrite |
   |---|---|
   | `anchoring/index.ts:635` verify-by-hash DB path → `anchorReadback.ts:99-160` | every `metadata.*` reflects the latest event; `contentHash` can disagree with the lookup key (MAJ-2) |
   | `index.ts:890` `GET /api/anchors/:id` | latest identity and commitment, next to the original `contentHash` column |
   | `index.ts:1671` submitter (`anchorSubmission.ts:436`) | the chain now anchors the latest payload (INF-4); race in MIN-1 |
   | `index.ts:1790` `processBatchAnchor` (`firstAnchor.metadataPayload`) | MIN-3 |
   | `index.ts:1321` `rowToAnchor` → `formatAnchorResponse` (`:1569`) | exposes only the label; no effect |
   | downstream via verify-by-hash: `originate/routes/verification.ts:435,700-712`, `verificationV2.ts:140,240-252` | `documentId`/`certId` matching still works because `documentId` is the key; issuer/org and `documentType` shown to the public come from the latest writer (MAJ-1) |
   | `api-gateway/routes/verification.ts:633` | reads only txHash, block and confirmedAt; unaffected |
   | `anchorStateSync.ts` | 0 hits on identity/metadata fields (control: the same grep hit `verification.ts`); unaffected |
   | `systemTest/schemathesis/.../anchor_sql.py:114`, `provenance_exclusion.py` | assert the payload key set on a row the test itself wrote; unaffected unless a document id is reused |
   | `prisma BlockchainAnchor.metadataPayload` | maps to the `blockchain_anchors` table (dropped by migration 003), not `anchor_store`; no reader |

   The reconciler has 0 payload references (it reads status only).
6. **Mutants:** in the table below.
7. **Merge:** I re-read develop live and found `92d1316f` (`receipts_merge.txt`).
   - Overlap scan of PR files against develop files since `026c2d16`: 0 files in common. Planted control: adding `documents.ts` to the develop list makes it show up.
   - `merge-tree` on the live tip gives tree `dbdbdf0184d0d06b655ff0da7260007ef59e3b6e`, clean. The author's `55252322` on `d53d80cb` reproduces exactly.
   - Negative control: develop plus a planted edit on `documents.ts` gives `CONFLICT (content)`, rc=1.
   - Tests on `dbdbdf01`:
     - originate jest: **109/109 suites, 1361/1361 tests**;
     - tsc `--noEmit`: 0 errors in originate and in anchoring (planted-type-error control → errors);
     - anchoring default lane: 370 passed + 1 failed, `threadTokenMint.test.ts`, which fails identically on develop (`dev_anchoring_default.log`);
     - anchoring integration: **4/4**.
   - At head alone: originate 107/1345 and anchoring integration 4/4, both matching the PR body.

## Mutant table
Instrument: `evidence/cells/mutants.py`. Each mutant is one exact text replacement, applied once, in a dedicated worktree. For each one I ran originate jest on both ks1385 suites (`--json`) and the anchoring integration lane (vitest JSON) against port 55549, then restored the file with `git checkout`, and the worktree was confirmed clean afterwards.

A kill counts only if a named cell fails with a non-empty message, the cell count stays at 24+4 and no suite fails to load.

The author's own list of 14 mutants is not in the commit and I had no access to the PR body (gh is not authenticated for this repo; the API returned 404). The k-series below is therefore my reconstruction from the sites the commit itself lists.

| Mutant | Result | Failing cells |
|---|---|---|
| CTRL-none / CTRL-comment-only | 0 failed, 24+4 | — (controls) |
| k01 site 1 spread deleted | KILLED | C1, C2, C4, C5, C9, C10 |
| k02 site 2 | KILLED | C11 |
| k03 emitLifecycleAnchor spread neutralised (compile-valid) | KILLED | C8 |
| k04 transfer-custody `identity` dropped | **SURVIVED** | — |
| k05 share `identity` dropped | **SURVIVED** | — |
| k06 revoke `identity` dropped | **SURVIVED** | — |
| k07 lifecycle-events `identity` dropped | KILLED | C8 |
| k08 site 4 spread deleted | load failure (unused import, TS6133), **not counted** | — |
| k08b site 4 neutralised (compile-valid) | KILLED | C15 |
| k09 site 5 spread added | KILLED | C16 |
| k10 site 6 | KILLED | C17 |
| k11 site 7 | KILLED | C18 |
| k12 upsert line deleted | KILLED | G1, G2, G4 |
| k13 helper forwards null | KILLED | C6, C12 |
| k14 error detail dropped | KILLED | C7 |
| g01 site 1 forwards the CALLER's identity | KILLED | C2, C3, C5, C6, C9, C10 |
| g02 site 5 forwards the raw body key (not via helper) | KILLED | C16 |
| g03 upsert also overwrites `content_hash` | KILLED | G1, G4 |
| g04 helper drops identity when another field is present | KILLED | C1, C2, C4, C5, C9, C10, C15, C17, C18 |
| g05 helper clones the block | KILLED | C13 |
| g06 upsert COALESCE (keep the first payload) | KILLED | G1, G2, G4 |
| g07 helper truthiness | KILLED | C13 |
| g08 share forwards the caller's JWT user object | **SURVIVED** | — |

Totals: 22 scored mutants, of which 18 were killed and 4 survived (k04, k05, k06, g08). k08 was a load failure and is not scored; its compile-valid version k08b is in the 22. Both controls stayed green.

## NOT tested
- The gateway was not booted. MAJ-1's route through the gateway rests on reading `proxy.ts:873-878` and `scopes.ts:36-39`; it was proven against anchoring directly.
- Real Cardano / Blockfrost was not used. The chain was mock or faked in every cell, so the MIN-1 window length on a real network was not measured.
- Platform S's actual wire traffic was not observed, so I do not know whether S's legitimate flat calls ever reuse a `documentId` with a different `contentHash` (MAJ-2's legitimate reachability).
- The author's exact 14 mutants and the PR body were not available (see the mutant table).
- The full originate integration lane (`jest.integration.config.js`) was not run, and no service other than anchoring was booted.
- The scratch-built `packages/shared/dist` was compiled from each worktree's own source, not from a published build.

Merge only on Wednesday's head-bound GO. Nothing deploys from this verdict.
