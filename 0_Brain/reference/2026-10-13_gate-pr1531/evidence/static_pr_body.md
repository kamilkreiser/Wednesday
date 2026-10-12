<!-- SOURCE: author's local copy /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-10-13_seatJ-6th/evidence/ks1557/pr1531_body_as_posted.md (sha256 9f4fd7b8860442b6); NOT the live GitHub body: gh auth failed (GH_CONFIG_DIR hosts.yml empty, rc=4) -->
## BLUF
**KS-1557, READ SIDE only.** `verify` (v1 and v2) used to present certification evidence read straight from a derived `signed` row's `metadata`, which the certify route fills from the CALLER'S `data` (the caller's keys are spread after the server's). A caller could therefore choose the certification id, the time, the type and the organisation id that verify presented, and could make a row whose hash is not its parent's count. **Measured on unfixed develop, real Postgres, as `secuura_app`, both tenancy modes:** with the caller's OWN document as parent, `certificationId: "FORGED-CERT-ID"`, `certifiedAt: 2020-01-01`, `certifiedBy: "Org B Official Registrar"` and `certifierOrganizationId` = another organisation's REAL id all came back from `verify` for another organisation's hash (evidence: `5_Project_History/2026-10-13_seatJ-5th/evidence/ks1557/`).

**KS-1557 stays OPEN after this pull request, and so does KS-1561.** The only ticket reference here is `Refs KS-1557`. No close-family keyword appears next to a ticket key anywhere in this body, deliberately: Linear re-parses the body, and the earlier wording of this very sentence was recorded with the wrong link kind, which would have shut the ticket on merge. Open after it: the write side (a parent that belongs to someone else, hash semantics, the organisation id from the actor), and the same hash registered by two organisations (KS-1561, product ruling pending).

## The rule
A derived row counts as certification evidence only when ALL hold; the presented id, type and time come from the real certification row, never from the derived row's `metadata`:
1. `status = 'signed'`, and `metadata.certificationId` is a UUID string;
2. its parent link is set, and the parent's hash equals its own (the parent is read from the same-hash set, else one lookup);
3. its external id is `doc-<ms>-<first 8 hex of the certification id>` (the route generates exactly that), so a row cannot cite someone else's genuine certification;
4. that id RESOLVES, in the row's own tenant, to a real certification row (a `documents` row `saveCertification` wrote: `certification_metadata` carries `certificationType` and `holderId`);
5. the derived row's `owner_user_id` equals the certification row's `issuer_user_id` (both a UUID for a person, both NULL for a connector principal), so a sign-cert or sign-wallet row, which is owned by the SOURCE's owner, cannot cite another actor's certification.

`certifiedBy` stays the caller-asserted display string it always was (Wednesday ruled the compatible shape). `certifierOrganizationId` is now `null` on this evidence: the certification row stores the issuer's USER id, not an organisation id, and the organisation-id fix is the write side. **Consumer census, because this field becomes `null` where it used to carry a value** (producers, the published spec and its examples, the frontend, and the Platform S contract documents under the project): the two producers are `verification.ts` (4 sites) and `verificationV2.ts` (2), both already `?? null` today, so `null` is a value this field already returns; `originate.openapi.ts:446` declares `z.string().nullable()`; the published `docs/openapi/secuura-api.yaml` `VerifyCertification` types it `["string","null"]` and lists it under `required` — required to be PRESENT, explicitly nullable — and the schema's own description says "Fields may be null for certifications issued before a given field was recorded"; `frontend/shared/src/schemas/verify.ts:121` is `z.string().nullable().optional()` and no frontend component reads the field; api-gateway never names it (0 hits); one test fixture names it (`ks563-certified-vs-anchored.test.ts:175`); the `spec-example-allowlist.json` hit is a KS-584 synthetic literal, not a consumer. Outside the repo: 34,871 text files under the project and 152 vault Secuura notes scanned, and **no Platform S contract document names it** — the only out-of-repo hits are old seat scratch copies of these same repo files and one board dump. Controls: `KS-1557` was found in 8 project files, while the British spelling and a nonsense token returned 0. **Nothing requires non-null.** Fail closed everywhere: any miss, mismatch or lookup error leaves the row out and logs one warning; at most 8 claimed rows are examined per request.

## The added cost, MEASURED on the real routes
Method: `log_statement=all` on a throwaway PG15, each measured request bracketed by marker statements issued from a separate client, statements counted between the markers with the markers excluded and a wrapped multi-line statement counted once; the new head against develop `5d5aea41`, both tenancy modes, as `secuura_app`. The plain-hash shape is the **zero control**: the resolver must add nothing there, so a non-zero delta would indict the method rather than the code.

| request shape | develop | this head | ADDED statements | = lookups |
|---|---|---|---|---|
| plain hash, no derived row (zero control) | 20 | 20 | **0** | 0 |
| one genuine derived row | 24 | 28 | **+4** | 1 |
| **nine** claimed rows (the cap is 8) | 56 | 88 | **+32** | 8 |

Identical in both tenancy modes. Each **logical** lookup is logged as **four** statements — `BEGIN`, `SELECT set_config('app.current_tenant_id', $1, true)`, the `SELECT ... FROM documents WHERE id = $1::uuid AND tenant_id = ...`, `COMMIT` — because the read runs inside the tenant-GUC transaction wrapper. So "one added query per examined row" is right in logical queries and is **four logged statements** per row; stating only the logical number would understate what the database sees. **The cap is measured, not asserted:** nine claimed rows were planted and eight lookups were made.

Wall clock, **scratch-local and NOT a box number** — a throwaway PG15 on a laptop running two other agent sessions, so these carry that load. p50 ms, single-tenant N=60: plain 3.52 -> 3.63, one row 3.95 -> 4.87, nine rows 8.56 -> 13.03. Pool mode N=40: 2.55 -> 2.57, 2.94 -> 3.34, 5.79 -> 8.63. Per added lookup about (13.03 - 8.56)/8 = **0.56 ms**, so the worst case is 8 added lookups times 0.56 ms = **about 4.5 ms per request**, which is what the nine-row delta measures. **Wall-clock on a real box is NOT measured, and no figure here is from one.** Applied to every site that read the old fields: v1 `/verify`, v1 `/verify-file`, the v1 cross-tenant registry lookup, v2 `/verify` (by hash and by documentId) and v2 `/verify-file`. The parent link and owner column now reach every rowset (`d.parent_document_id`, `d.owner_user_id`).

## Behaviour changes a client can see (no migration, no backfill)
- **Historic derived rows whose `certificationId` resolves to nothing, or whose hash is not their parent's, stop counting.** Legitimate rows keep counting. Byte-identical for a genuine row except where the old value was caller-chosen.
- A derived row whose caller overrode `data.certificationId` (so it is no longer the real id) stops counting: fail closed.
- `certifierOrganizationId` on sibling evidence is `null` (before: whatever the caller put in `data.issuerId`, or `null`). Anyone who relied on a caller-supplied value there loses it; Platform S's use is asked on KS-1557 and unanswered.
- **A certification whose HOLDER was erased by GDPR no longer counts.** Erasure step 6 overwrites the holder's documents, certification rows included, with `certification_metadata = {"anonymized": true}`, which removes `certificationType` and `holderId`; the shape test then fails. Fail closed, pinned by a unit cell. Say so if you want those rows to keep counting; it is a different rule.
- A custody transfer of the DERIVED row changes its owner, which then no longer equals the issuer: it stops counting (rare).
- **Revoked certifications are not examined by this PR**: a revoked certification row still resolves and still counts, exactly as before. Not changed.

## Every WRITER of each field the rule trusts (grep over services, packages and scripts; non-test)
| Field | Writers (value each can write) |
|---|---|
| `documents.parent_document_id` | `saveDocument` INSERT only (`documentRepo.ts`, both conflict tails; neither `ON CONFLICT` branch updates it). Producers of `doc.parentDocumentId`: `certifications.ts` derived row (caller string; truthy), `documents.ts` `/version`, `/sign-cert`, `/sign-wallet` (the URL param). Resolved by `external_id` in the tenant: NULL when the string is empty, unknown, a connector id, or a pkey-addressed id; otherwise the uuid of an existing row. The FK `ON DELETE SET NULL` writes NULL when the parent is deleted (`adminConfig.ts` org purge). No `UPDATE` sets it. |
| `documents.content_hash` | `saveDocument` INSERT only (create: the caller's `contentHash`; `/version`: `newContentHash`; sign-cert and sign-wallet: a copy of the source's; certify derived: the caller's `data.contentHash`, ANY string, else the hash of the data). `saveCertification` INSERT (the hash of the certification's data). Neither `ON CONFLICT DO UPDATE` tail touches it; no `UPDATE` sets it. Prefix and case variants are normalised before comparing. |
| `metadata.certificationId`, `status = 'signed'` | `saveDocument` INSERT: `metadata` is the caller's `data`/`metadata` spread by create, `/version`, `/sign-cert`, `/sign-wallet` and the certify derived row (server value first, caller's keys after); `status 'signed'` is set by `certifications.ts` (derived), `documents.ts` `/sign` (the same row), `/sign-cert`, `/sign-wallet`, `anchorStateSync` (revert). The `saveDocument` `ON CONFLICT DO UPDATE` tail and `updateDocument` rewrite `status` and `metadata` of an existing row. So a caller can write any JSON in `certificationId` (string, number, null, object); the rule needs a UUID string and the four conditions that these tails do NOT rewrite. |
| `documents.external_id` | `saveDocument` INSERT only (unique). The certify route generates `doc-<ms>-<certId8>`; `/version`, `/sign-cert`, `/sign-wallet` generate `doc-<ms>-<random 8 hex>`; `POST /api/documents` accepts a caller-chosen id but sets a non-`signed` status and no parent link, and no later statement sets a parent link. So a row with a parent link AND a caller-chosen external id has no producer. |
| `documents.owner_user_id` | `saveDocument` INSERT (a UUID, or NULL when the principal is not a UUID, e.g. a connector); `transfer-custody` UPDATE (`documents.ts`); GDPR erasure leaves it. |
| the certification row (`documents.id`, `issuer_user_id`, `certification_metadata.certificationType/holderId`) | `saveCertification` INSERT and its `ON CONFLICT (id) DO UPDATE` (status and `certification_metadata`, the revoke path); `issuer_user_id` is a UUID or NULL (`toActorUuid`). Rewritten by GDPR erasure steps 6 and 6b and merged by the `adminConfig` backfill (`issuerName` only). The legacy certify `UPDATE` writes `certificationType` into a plain DOCUMENT's `certification_metadata` but never `holderId`, which is why the shape needs both. Cert rows have a NULL `external_id`, so `updateDocument` cannot address them. |
| `documents.tenant_id` | INSERT only (plus the start-up backfill). |

## Not closed here, stated plainly
- **A 32-bit residual on the external-id binding.** `/version`, `/sign-cert` and `/sign-wallet` rows carry a server-random 8-hex suffix; a person who makes N genuine certifications and M such rows can match a prefix with probability about N*M/2^32. Condition 5 (owner equals issuer) blocks this unless the attacker also owns the source or both sides are connector principals. Closing it fully needs the write side: the certification id stored in a server-only column, or the access check on those routes (KS-1559 m-family).
- **A parent that belongs to someone else** (write side): with the other organisation's document as the parent and its hash in `data.contentHash`, the derived row passes every condition above and verify still presents the caller's genuine certification of that hash, with a caller-asserted `certifiedBy`. The write-side parent access check closes it.
- The same hash registered by two organisations (KS-1561).

## Test Evidence
**Touched** — 6 files, +778 / -58. Head `1ffc0d7a4ad740a91f2c04122fb55cd44477c928`, tree `c190292a793858fcf5baa7150740fc25c51fb687`, one parent: develop `b28bfaecf24e4671440b9345289bfc368639bd11`.

| file | change |
|---|---|
| `Blockchain/Dev/services/originate/src/__tests__/ks1557-trusted-certification-evidence.test.ts` | +239 / -0 |
| `Blockchain/Dev/services/originate/src/__tests__/ks1557-verify-trusts-certification-evidence.integration.test.ts` | +328 / -0 |
| `Blockchain/Dev/services/originate/src/__tests__/ks584-p3-verify-list.test.ts` | +36 / -11 |
| `Blockchain/Dev/services/originate/src/__tests__/ks584-verify-row-selection.test.ts` | +26 / -3 |
| `Blockchain/Dev/services/originate/src/routes/verification.ts` | +133 / -26 |
| `Blockchain/Dev/services/originate/src/routes/verificationV2.ts` | +16 / -18 |


**Base and overlap (condition 1), on the fresh base.** Scanned against develop `b28bfaecf24e4671440b9345289bfc368639bd11`: all **25** open pull requests, **zero** overlap with these six files. The planted control `services/originate/src/routes/certifications.ts` fired on pull request **#1525**, so the scan discriminates. Develop moved from the work-in-progress base `5d5aea41` by exactly **one** commit (`b28bfaec`, KS-998 item 3) touching only two shell test fixtures — zero overlap there too, control fired. **This is not a rebase of published history:** the branch had never been pushed, it was rebuilt on fresh develop, and the resulting tree `c190292a7938` is **byte-equal to what `git merge-tree` predicts** for merging develop into the work-in-progress commit. A deliberately wrong prediction produced a different tree, so that comparison discriminates.

**Ran, on the exact landing tree `c190292a7938`:**
- unit: **3 suites / 64 tests** (`ks1557-trusted-certification-evidence`, and the two updated `ks584` files).
- integration `ks1557-verify-trusts`: **17/17 single-tenant and 17/17 pool mode**, both as `secuura_app` against real Postgres.
- whole originate unit suite: **103 suites / 1248 tests**.
- `tsc --noEmit` rc 0 · `eslint` on the six files rc 0 · `check:openapi` rc 0 (`OK — every published example resolves to the fixture set`, 413 example blocks).
- **pre-push hook on the pushed head:** `PREFLIGHT INCOMPLETE — 13/16 legs ran, 3 SKIPPED. Nothing failed.` — legs 3, 4 and 8 skipped because the local stack is not up. The hook itself says: *"This is NOT a pass. Do not quote it as one — say which legs ran."* Shell suites **86 passed, 0 failed, 0 skipped (of 86)**, wall clock 412 s. Leg 16: 0 new test-file type errors across 3 services.
- **Mutants.** The **seven** that Seat J 5th fixed in the tests and did NOT re-run are re-run here and **all killed**: V01 (3 red), V02 (2), V03 (1), V04 (2 unit + 1 in each mode), V09 (2 unit + 1 in each mode), V10 (1), W03 (12 red in each integration mode). The comment-only control killed nothing (0 reds in all three layers). Every file restored byte-identical after every mutant; the runner reported `PROBLEMS: none`. **Honest limit:** W03 declares no unit needles, so its unit layer reads `n/a` — it is killed by the integration layers only, not by a unit cell. The other 24 of the 31 planted mutants are J 5th's run and were **not** re-run by me.

**NOT run.** Schemathesis, Akto, Playwright and k6 — all four need the local stack, which is not up (the same reason legs 3, 4 and 8 skipped). No live check on demo or Kintsugi, and **no figure here comes from a box**. No migration and no backfill. **Red-first was not run for the resolver's own 33 unit cells** (the function is new) and not re-run by me for any cell; **4 of the 17 integration cells** were written after J 5th's red run and have never been seen red. The timing and query-count probe is scratch-only and is **not** committed.

**Two defects in the measuring instrument, disclosed.** J 5th's timing probe had never been executed, and it did not survive first contact: (1) it timed the request around a helper that sleeps 300 ms **after** the response, so every latency sample would have carried that sleep — a p50 of about 303 ms would have been the sleep, not the route; I measured with a sleep-free helper. (2) It did not compile: 7 unused locals under `noUnusedLocals`. Both faults are in the scratch probe only; neither touches shipped code. The query-count method above was added by me because reading the count off the code is what the ruling forbade.

**Migrations + config.** None. No migration, no schema change, no environment variable, no compose change. Deploys the **originate** service only.

**Observed in passing, not this PR's business:** preflight leg 6 lists **15** baselined advisories that are no longer reported (an advisory CLEANUP list, not a failure).


## Merge
Not for merge until the Opus tier-1 gate returns GO on the head it names. This PR touches `verification.ts`, `verificationV2.ts` and tests only; it does not touch `certifications.ts` or any file of PR #1525. Deploys the originate service only. KS-1557 stays open.


🤖 Generated with [Claude Code](https://claude.com/claude-code)
