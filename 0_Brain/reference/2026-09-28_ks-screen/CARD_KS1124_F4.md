# Card draft: KS-1124 finding F4 (a non-production certification whose anchoring failed shows "pending" forever)

**Date:** 2026-09-28 16:36 AEST (shell `date`) · **For:** Wednesday · **Client:** Secuura/Blockchain only
**Code read at:** develop `d9ce1403d1581ff1584ab799fbbf7fc6f9f8d817` (origin's develop by `ls-remote`, read 16:28), via `git show d9ce1403:<path>` / `git grep` in the no-checkout clone `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/4901153c-5db0-4cfc-bf83-c25726202b34/scratchpad/verify_clone` (`cat-file -t d9ce1403` → commit; bogus `d9ce1403ffff` → fatal). All paths are under `Blockchain/Dev/`.
**Ticket read:** KS-1124 in full from Linear (description + every comment, `comments(first:50)`, sorted client-side by `createdAt`: 1 comment, 2026-09-26 02:51Z, about O1 only). Read-only. State Backlog, P3, filed 2026-09-13 by the tier-2 gate on #967 → #968.
**Prior-ruling search:** `decision_queue.sh list ruled` (449 lines) and `list open` (4 open cards), grepped for `1124`, `pending`, `certification`, `anchor`; `decisions.json` (470 cards) full-text for `KS-1124`, `KS 1124`, `pending-onchain`, `pending_onchain`, `certification`, `F4` (control: `secuura-` 1,057 hits, so the grep can see).
**Nothing was changed.** No ticket comment, no card posted, no push.

## Verdict: Kam's (close to the line; escalated once with a recommendation, per the autonomy grant's "when genuinely unsure")
All three fixes end in the same served answer (off-chain-only instead of pending), so the direction is not in dispute. What makes it Kam's: it changes **what a third-party verifier is told about a certification**, the status vocabulary the gateway serves was set by the KS-1071 "Option B" decision, and option (c) moves that decision into the gateway itself. No ruling exists (below). If Wednesday reads it as agent-decidable instead, the recommended option is the default for a seat.

## Premises, verified at d9ce1403
- **Failure is the default, success is the exception.** `services/originate/src/routes/certifications.ts:409` sets `anchoringStatus = 'failed'`; only `if (upstream.ok)` at `:429` sets `'submitted'` (`:432`). A thrown fetch (unreachable, 10 s timeout) is caught and only logged (`:435-437`); a non-ok reply also leaves `'failed'`. **VERIFIED.**
- **Production refuses; non-production continues.** `:438-443`: `if (anchoringStatus === 'failed' && process.env.NODE_ENV === 'production')` → 503 `SERVICE_UNAVAILABLE`. Otherwise the route carries on. **VERIFIED.**
- **The failed leg persists "pending".** `:461-472`: `blockchain: { anchorId: upstreamAnchorId, txHash: null, blockHeight: null, anchoredAt: null, confidence: 'pending-onchain' (:470), anchoringStatus (:471) }`. On the failed leg `upstreamAnchorId` is `null` (`:408`, only set at `:431`). **VERIFIED.** (The ticket says `anchorId` is `undefined`; at this tip it is `null`. Same effect: falsy.)
- **The second route has the same shape.** `:1147` default `'failed'`, `:1162-1165` success, `:1170-1175` production 503, `:1200-1207` persists `confidence: 'pending-onchain'` (`:1205`) with `anchoringStatus` (`:1206`). **VERIFIED.**
- **It is copied onto documents.** `:526` puts `certification.blockchain` onto the NEW derived document at certify; `:556` writes it into the original document's metadata on the legacy path (`:547`). **VERIFIED.** (The ticket cites `:510`; the line moved.)
- **Nothing ever upgrades it.** `certifications.ts` has 0 references to `updateDocument`, `pollAnchorUntilConfirmed` or `reconcileDocumentAnchorState` (`git grep -c`, rc 1). The read-time healer returns early without an anchor id: `services/originate/src/services/anchorStateSync.ts:353` `if (!bc?.anchorId) return document;`. **VERIFIED.** (The ticket cites `:298`; the line moved.)
- **The gateway shows it as pending.** `services/api-gateway/src/routes/verification.ts:623-624` read `blockchain.confidence` and `blockchain.status`; `:746`: `persistedStatus == null && persistedConfidence === 'pending-onchain' ? 'pending-onchain'`. The failed-leg blob has no `status`, so it lands there. The gateway reads `anchoringStatus` **nowhere** (`git grep -c anchoringStatus` over `api-gateway/src` excluding tests: 0, rc 1; control: `pending-onchain` → 23 hits in `verification.ts`). **VERIFIED from source.**
- **The gateway's status mapping already says a `'failed'` status is off-chain-only.** `verification.ts:244-259` (`confidenceForAnchorStatus`): `'failed'` → `off-chain-only` (`:253-254`); anything unknown, including originate's `anchor_failed`, → `off-chain-only` (`:255-257`). **VERIFIED.** This is what option (b) relies on.

### NOT verified here
- **"Pending forever" at runtime.** The ticket says the row was DRIVEN at `1b7c03a22` (2026-09-13). Nothing was run at `d9ce1403`; the claim at this tip rests on the source read above.
- **Whether any client-reachable environment runs non-production.** Only `docker-compose.production.yml` sets `NODE_ENV=production` (`:81` and 11 others). Whether the public demo's originate runs with `NODE_ENV=production` was not measured. If it does, F4 is reachable only on dev, CI and local stacks.
- **Where "Option B" was ruled.** The ticket says Option B was "ruled" on KS-1071 (PR #967). No decision card mentions KS-1071 (`decisions.json` full-text: 0), so who ruled it was not established.
- **Co-file:** option (c) edits `verification.ts`, the same file as the KS-1129 livescan PR staged for Seat B 38th (`:606-609`; option (c) sits near `:746`, a different region). Not a conflict today; a sequencing note if (c) is chosen.

## Prior ruling
- **None.** 0 hits for `KS-1124`, `KS 1124`, `pending-onchain`, `pending_onchain` in `decisions.json`; 0 in `list ruled` / `list open` for `1124` or `pending`. The 6 `certification` hits in `decisions.json` are unrelated (an email-validation note in `secuura-four-advisories-ruled-after-measurement`; the batch-certifications route in `secuura-ks1084-part-b-…`; 4 non-Secuura cards).
- **Nearest, not a ruling on this:** `secuura-ks1171-when-is-an-anchor-absent` (c, 2026-09-25; when anchoring may declare a transaction absent); `secuura-ks1194-failed-save-answers-200` (fail-closed, 2026-09-17; Kam's precedent in spirit: a failure must not read as success-in-progress).
- KS-1124's other finding, **O1**, is NOT this card: it is a Spark pass staged for Seat B 38th (`Refs KS-1124`, O1 only). This card leaves it unaffected either way.

## The card (decision_queue.sh `add --json` shape; NOT posted)

```json
{
  "id": "secuura-ks1124-f4-failed-anchor-shows-pending",
  "client_project": "Secuura/Blockchain",
  "title": "KS-1124 F4: outside production, a certification whose blockchain anchoring failed shows 'pending' forever. How should it say it failed?",
  "bluf": "No action needed unless you disagree with the default. Outside production, when a certification's anchoring fails, originate still saves it as 'pending-onchain' (certifications.ts:470 and :1205). Nothing ever updates it, so the verify page shows 'pending' for as long as it exists (gateway verification.ts:746). Production is not affected: it refuses with a 503 instead (:438). I recommend (b): save a 'failed' status, because the gateway already turns that into off-chain-only (verification.ts:253) and the record then says what happened.",
  "options": [
    {
      "key": "a",
      "label": "Save no 'pending' label when anchoring fails",
      "detail": "Originate only, both routes (certifications.ts:470, :1205). With no label and no status, the gateway's closed default answers off-chain-only. Smallest change, but the record carries no explicit 'failed' for later readers."
    },
    {
      "key": "b",
      "label": "Save a 'failed' status the gateway already reads as off-chain-only",
      "detail": "Originate only, both routes. The gateway's existing mapping (verification.ts:253) turns 'failed' into off-chain-only, and the stale 'pending' label is then ignored (:746 applies only when there is no status). A seat proves it with a cell: a failed submission never shows pending through the gateway."
    },
    {
      "key": "c",
      "label": "Make the gateway read the existing 'failed' marker",
      "detail": "Gateway only (verification.ts:746): honour anchoringStatus, which originate already saves. Fixes the display for new and existing records, but the misleading 'pending' label stays in the saved data for any other reader, and it edits the file the KS-1129 fix is also changing."
    }
  ],
  "recommended": "b",
  "default_action": "If you do not answer: nothing changes. F4 stays open on KS-1124, failed certifications outside production keep showing 'pending', and the separate O1 fix on the same ticket goes ahead unaffected."
}
```

**Why (b) over (a) and (c):** (b) uses a mapping the gateway already has and tests (`confidenceForAnchorStatus`), so the served answer comes from an explicit rule rather than from a field being absent (a); and it corrects the saved record at its source rather than teaching one reader to see past it (c). Records already saved with the stale label are NOT fixed by (a) or (b); only (c) reaches them. That is the trade-off Kam is choosing on.
