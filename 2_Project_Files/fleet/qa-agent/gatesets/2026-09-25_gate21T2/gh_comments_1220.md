--- comment 5826193548 by linear[bot] at 2026-09-25T03:28:57Z
<!-- linear-linkback -->
<details>
<summary><a href="https://linear.app/secuura/issue/KS-1129/anchorings-raw-pg-bigint-reaches-persisted-and-live-readers-unshaped">KS-1129 anchoring's raw pg BIGINT reaches persisted and live readers unshaped</a></summary>
<p>

## BLUF

`block_number` leaves anchoring's `buildResponse` (`services/anchoring/src/index.ts:604`) as a **string**, the KS-584 heal path in originate persists it into the document blob unshaped, and the gateway's live chain-scan reads have no shape rule at all. Three sites, one logical path: the raw `pg` value of a `BIGINT` column is passed through where every other reader of that column converts it. Found by the tier-2 gate on PR #969 (KS-1069) as F1 (the persisted half) and O1 (the live half); PR #969 merged with E7 STRICT by ruling, so this ticket carries the root fix — not the PR.

Report: `Testing Agent MAIN/projects/secuura/reports/2026-09-13-ks1069-969-fb23ca6aa-tier2-r1/report.md` — §4 (the F1 chain), FINDINGS F1, Open O1, WHAT WAS NOT TESTED item 1.

## The chain (READ ONLY from source at develop `0f69129b3`; line numbers as printed there)

1. **anchoring** `src/index.ts:604` — `blockNumber: onChain?.blockNumber || row?.block_number || null,` on the DB leg of `GET /api/anchors/verify/:hash` (`:633-647`). `onChain` is the stored `metadata_payload`, which never carries `blockNumber` (`anchorSchema.ts buildFlatAnchorMetadataPayload`, 0 hits), so the value is `row.block_number` **raw**. The column is `BIGINT` (`:181`; migrations `001:717`, `003:29`). `pg` 8.20.0 returns int8 as a string by default, and **no** `setTypeParser` **/ int8 parser exists anywhere in** `Blockchain/Dev` (non-test, non-lock: 0). The same file converts that column with `Number()` at `:1314` (`blockNumber`), `:1315` (`slot`), `:1320` (`fee`) — the control that says the authors know.
2. **originate** `src/routes/verification.ts:338` — `confirmStalePendingAnchor` (`:293-348`) composes the healed blob with `blockHeight: chain.blockNumber ?? blob.blockHeight ?? 0`, where `chain` is anchoring's reply above; `persistHealedAnchor` **(**`:359-369`**) persists it** via `updateDocument(…, { blockchain: healed })` (`:366`) when the heal moved the status to `confirmed`. Called from `POST /api/verification/verify` (`:1082-1083`) and `/verify-file` (`:657-658`). This is the KS-584 heal path (PR #666, merged 2026-08-12) — the writer the E7 ruling's census ("every originate writer stores a number") did not see.
3. **api-gateway** `src/routes/verification.ts` — the persisted tier-1 read at `:623` (head numbering; `typeof persistedBlockHeight === 'number'`, PR #969) now refuses that string, so a healed document answers `verified:false` / `off-chain-only` where develop-before-#969 said on-chain — **only while the gateway's own live scan does not answer** (`:569-585`: anchoring unreachable, the 2.5 s timeout at `:570`, token refused, or `doc.contentHash` missing); when it does, `Number()` at `:582` coerces and `liveAnchored` wins. Tier 2 is unaffected (`rowToAnchor`).
4. **The live half (O1, MEASURED + READ ONLY):** the live chain-scan path (`:579-582`, `:645`) has no shape rule — `j.verified` truthiness (a string `'false'` counts), `liveTxHash` truthiness (`1`, a placeholder), `Number(blockNum)` coercion, no sign/integer rule (`-1`, `4242.5` on-chain), `simulated` ignored. Every L row on-chain at both SHAs. Safe today only because anchoring's `buildResponse :595-598` nulls placeholders and emits the literal `verified: true` — a response-shape accident, and its `:604` raw BIGINT pass is the same root as item 1. Blast radius = anything that can answer the gateway's `/api/anchors/verify/:hash` call.

**Evidence classes, as the report states them:** READ ONLY (the chain above) + PROBED (`pg-types` `getTypeParser(20)("4242")` → `"4242"`, `typeof string`, from the checkout's `node_modules`) + MEASURED (the shape: matrix cell `G:'4242':t1` on-chain at develop, off-chain-only at head). **Not run against a database.** F1's producible path is read from source, not reproduced end-to-end.

## Checklist (one test pass; RULED 2026-09-13)

- ☐ anchoring `src/index.ts:604`: `Number(row.block_number)` as `:1314` already does (null-safe: a null row stays null).
- ☐ originate `src/routes/verification.ts:338`: `Number(chain.blockNumber)` (or coerce once where `chain` is parsed), so the heal persists a number.
- ☐ Regression cell (prose, originate): a `submitted` blob with a real 64-hex hash healed via a stubbed anchoring reply `{verified:true, txHash, blockNumber:'4242'}` persists `typeof blockHeight === 'number'`. Red at develop (`'4242'` persisted), green after.
- ☐ The live chain-scan shape rule at api-gateway `src/routes/verification.ts:579-582, :645` (O1's class): `verified === true`, the KS-522 placeholder rule on `liveTxHash`, `Number.isInteger(h) && h > 0` on the height, `simulated` read — the same three guards PR #969 gave the persisted read, applied to the live read; cells for each.
- ☐ **The JSONB round-trip, measured in BOTH directions (KS-1069 item 1 — NOT TESTED by #969 or its gate; moved here so it survives KS-1069's archive).** Source implies type preservation: originate writes `JSON.stringify({…, blockchain})::jsonb` (`documentRepo.ts:523-532`, `:545-546`) and reads back Prisma's parsed JSONB (`:162`) — a JS number should come back a number, a string a string (which is what makes the persisted string above a string). **If that expectation were false the other way (every number read back as a string), E7's guard would refuse every persisted height and every tier-1 confirmed document — the four seeded demo documents included — would answer off-chain-only: a demo-visible blast radius.** Nothing proves it either way yet; measure against a real Postgres, both directions, before or alongside the fixes above.

## Deliberately not here

* The gateway's persisted guard itself (E7 STRICT) — shipped in #969, ruled. Coercing at the gateway was option (b); the ruling kept (a): fix the root.
* The `persistedStatus == null` carve-out — KS-1073 / KS-1068 territory.
* The presentation question (a placeholder echoed in `blockchain.txHash` with `source:'persisted'`) — recorded on the #969 verdict, not raised.

## Ancestry and neighbours (named, not related — see Dedupe)

* **KS-584** (P1, "Verify by hash selects the wrong registration: certified documents report as unanchored, and tenant fields leak") is the ancestor: its fix, PR #666 (merged 2026-08-12, verified live on demo 2026-08-14, S-side confirmation 2026-08-19), introduced the heal path at item 2. **KS-584 is archived (2026-08-19T02:00Z, Deployed to UAT)**, so Linear refuses a relation to it; it is named here instead.
* **KS-590** (Peter's, Backlog, parked on KS-584 — the systemTest side of the same class); **KS-607** (GET /api/anchors/{id} vs verify status divergence — the same `buildResponse` territory, status not height); **KS-1004** (the anchor-failed guard keys off the hash; traces `block_number` writers for a different reason). A reader arriving from any of the three finds this ticket the home of the height-shape defect.

## Dedupe, before filing (s205, 2026-09-13)

Literal census over 1,118 KS issues (691 archived) and 912 comments, by SYMBOL and path — `persistHealedAnchor` 0 · `setTypeParser` 0 · `BIGINT` 0 · `liveAnchored` 0 · `confirmStalePendingAnchor` → KS-590 (comment) · `buildResponse` → KS-1119, KS-521, KS-584, KS-590 · `block_number` → KS-1004, KS-607, KS-1070, KS-1057 · `/api/anchors/verify` → KS-489, KS-590, KS-683 · `JSONB` → KS-1069, KS-1115, KS-472, KS-537, KS-593, KS-787. Every hit's description read: none names the raw BIGINT pass or the heal path's string height. Controls fired (`persistedStatus == null` → KS-1073; `crossTenantLookup` → KS-1119 + KS-584; a nonsense token → 0).

## Provenance

* Tier-2 gate on PR #969 at `fb23ca6aa`, 2026-09-13 (report path above): F1 (Minor, against the ruling's premise), O1 (Open, the class outside the ticket), NOT TESTED item 1.
* Wednesday's rulings on the verdict, 2026-09-13 16:24 AEST: E7 STRICT stands; the root fix travels here; the JSONB half of KS-1069 item 1 moves here; ONE Medium ticket, related KS-1069 (KS-584 named, not related — it is archived; ruled 16:51 AEST).
* Filed by s205 (the merge seat for #969) at the per-PR order's step 1, before KS-1069's archive.
</p>
</details>
<!-- linear-review-link -->
<p><a href="https://linear.app/secuura/review/ks-1129-bignum-the-anchoring-verify-body-reports-blocknumber-as-a-1f4a5b4c303a">Review in Linear</a></p>

