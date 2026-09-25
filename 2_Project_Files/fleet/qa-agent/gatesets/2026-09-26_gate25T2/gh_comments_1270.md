--- comment 5838380481 by linear[bot] at 2026-09-25T19:31:59Z
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
<!-- linear-review-link -->
<p><a href="https://linear.app/secuura/review/ks-1275-point-the-lifecycle-verb-prose-at-lifecycle-event-actions-3ef322f0b88f">Review in Linear</a></p>

