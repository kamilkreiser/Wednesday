--- comment 5834284168 by linear[bot] at 2026-09-25T14:42:39Z
<!-- linear-linkback -->
<details>
<summary><a href="https://linear.app/secuura/issue/KS-1275/published-post-lifecycle-events-description-still-enumerates-an-old">KS-1275 Published POST /lifecycle-events description still enumerates an old verb list (originate.openapi.ts:1847-1861 -&gt; secuura-api.yaml)</a></summary>
<p>

**BLUF:** the machine-readable `action` enum on `POST /api/documents/{id}/lifecycle-events` is generated from `LIFECYCLE_EVENT_ACTIONS` and is correct. The human-readable **description** hand-enumerates the accepted verbs, and that list is stale.

* It omits `share-attach-consent` (KS-534), `protect` / `unprotect` (KS-556), and now `note` / `certified` / `verified` (KS-1172 / KS-1173, #1059).
* It is generated verbatim into the published spec, `docs/openapi/secuura-api.yaml` (the gate read :28583-28593 at #1059's head).

## Where

* `Blockchain/Dev/services/originate/src/originate.openapi.ts:1847-1861` (read at develop `3c447abc7`).
* Other stale prose the gate listed, all pre-existing:
  * `documents.ts:2384-2387`, the route header comment;
  * `lifecycleEventRepo.ts:7`;
  * `migrations/037:4`. That one is an applied migration, so never edit it.

## Fix shape

Replace the enumeration with a pointer to the enum and to `docs/VOCABULARY.md`, so the prose cannot drift again. Then regenerate the yaml with `npm run generate-openapi`.

## Provenance

Batch gate `2026-09-19-batch1050-1060-tier1-r1` (report: `Testing Agent MAIN/projects/secuura/reports/2026-09-19-batch1050-1060-tier1-r1/report.md`), finding **N59-1** (Minor, pre-existing, widened by #1059). Wednesday's GO 2026-09-18 23:14:38Z. Refs KS-1172, KS-1173.
</p>
</details>
<details>
<summary><a href="https://linear.app/secuura/issue/KS-1299/openapi-v2-verify-description-still-says-v1s-legacy-bodies-keep-their">KS-1299 OpenAPI v2 verify description still says v1's legacy bodies keep their answer — it overstates, for bodies pairing hash with a document id or data</a></summary>
<p>

## BLUF

PR **#1233** (KS-1133 + KS-1229, merged `1f1da7f35040`) documented the v1/v2 hash-alias split in the served spec. **The v2 description still carries the older claim that v1's legacy bodies keep their answer** — and that is exactly the sentence #1223 had to narrow in the *code* comment on the same day, for the same reason.

**It overstates for one case:** a body pairing `hash` with a document id **or** document data now takes the hash strategy, as v2 already does. So the spec tells an integrator something the route no longer does.

## Why this one matters more than an internal comment

It is in `docs/openapi/secuura-api.yaml` — the served spec. An integrator reading it has no other source, and the S5 probe on #1233 confirmed the served yaml is byte-identical to the merged blob, so this text is what clients actually receive.

## The fix shape

Mirror the wording that #1223 landed in the code comment: v1 reads `hash` **last** and v2 **first**, by design; a body pairing `hash` with `documentId` or `documentData` takes the hash strategy on **both**. Both routes' descriptions should say the same thing, since the point of #1233 was to stop them disagreeing.

## NOT claimed

No behaviour defect and no drift: `check:openapi` passes rc 0 at the merged tree with the drift control CAUGHT, and leg 8 read 309 paths / 343 operations json==yaml rc 0. This is the spec's prose being wrong, not the spec being out of sync with the code.

## Board search before filing (team Secuura-PK, 1,286 issues incl. archived, 3,631 comments, literal match on titles, descriptions and comments)

* `v2 description` -> **0**. `hash-alias` -> **0**.
* `legacy bodies` -> 1 total / 1 open: **KS-1133**, which is the merged ticket this residue comes from, not a separate owner of it.
* Controls that fire: `KS-1229` -> 5; `consumeResetToken` -> 3; nonsense control -> 0.

`Refs KS-1133`; does not close it.

## Provenance

Tier-2c QA gate `2026-09-25-batch1218-t2c` (report sha256 `70dc4c987f04…`), raised as a **non-blocking** finding and recorded at the merge. Filed on the coordinator's instruction after the batch landed; it did not hold the merge.
</p>
</details>
<!-- linear-review-link -->
<p><a href="https://linear.app/secuura/review/ks-1275-the-lifecycle-verb-description-points-at-the-enum-not-a-list-9a2a7905a12a">Review in Linear</a></p>

