# KS-1384 per-event anchor design, revision 2: second independent review

**Reviewer:** an independent read-only reviewer for Wednesday, 2026-10-29 (late evening AEDT).
**Reviewed:** `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-10-29_seatW-7th/KS-1384-per-event-anchor-DESIGN-rev2.md` (541 lines) and `HANDOVER.md` beside it (25 lines), read whole. I also read the first review (`../2026-10-29_ks1384-design-review/review.md`, 216 lines) whole, and I grepped rev 1 (`.../2026-10-29_seatW-6th/KS-1384-per-event-anchor-DESIGN.md`) for the sections rev 2 carries.
**Code:** develop `6d41673e0f79c0f02c2ec7b893cc960b6fa3ec10`, read only with `git show` / `git grep` / `git diff --stat` / `git log -S` in Wednesday's cache clone. Paths are under `Blockchain/Dev/services/` unless they start with `Blockchain/Dev/`.

---

## Verdict: SOUND WITH CHANGES

**Counts:** 0 blocker, 7 major, 5 minor, 4 info.

The revision answers the first review faithfully, and most of its dispositions hold up when the code is re-read. The weak part is the new F0: its money-safety claims are stronger than the mechanism behind them. F0 is the one step this design asks Kam to approve first.

## BLUF (6 lines)
1. **Most dispositions hold.** The guard-3 text clause does defeat the 09-14 retry for the node's real text. The give-up does read `created_at`. 057/058 do have to leave `migrations/`. R6 does have to compare on the encoded side. 16.9 is **CONFIRMED** at the pin.
2. **F0's input pin only works pairwise.** The pin makes the refused transaction X conflict with its first retry X′, but not with the next retry X″. If X sits in a mempool for more than about 27 minutes and then lands, the chain X → X′ refused → X″ can still put the same payload on chain twice (major 1).
3. **F0's UTxO overlay has three holes.** (a) It releases a claim when one provider read stops listing the outpoint, which is exactly the replica-lag hole the design rejected option (iii) for. (b) It holds claims of definitively refused transactions for up to 2 h (the TTL), which can starve a wallet with only a few UTxOs. (c) It cannot see a second in-process wallet spender, `POST /api/anchors/thread-mint`, which runs outside the wallet lock (majors 2-4).
4. **The new compare-and-sets have no way to report their result.** `dbUpdateAnchorStatus` returns `void` and swallows errors. The resolver's "`confirmed` stays terminal" is check-then-write, because `updateDocument` has no guard on the blob's state. Two concurrent retry-route calls can still pay twice (majors 5-6).
5. **D13 (give up on `now − updated_at`) holds at the repo level.** I found no trigger and no repeating non-transition writer. The only residual is originate's `saveAnchorToDb`, which is reachable only by calling originate directly and is removed only in E1, after F.
6. **"1(b) executes Kam's 09-14 ruling" is only PARTLY accurate.** The ruling never weighed the KS-705 "already included" text, and the input pin is a coin-selection change, which the design itself classes as Kam's. F0 goes to Kam as a card anyway, so name 1(b) on that card. It costs nothing.

---

## Q1. The dispositions of review findings 1-17, inputs 3/4/5 and F2

| # | Rev 2 disposition | My view | Evidence re-read at the pin |
|---|---|---|---|
| 1(a) | Local UTxO overlay | **Direction right, mechanism incomplete.** See majors 2, 3, 4 | `cardano/transaction.ts:29`, `:96-99`, `:102-104`, `:122`; `cardano/provider.ts:329-340` |
| 1(b) | Drop the clause, compare-and-set, input pin | **Diagnosis correct; the safety claim is overstated.** See majors 1 and 5, and minor 11 | `anchorSubmission.ts:112-124`, `:584-590`, `:620-641`, `:654-677` |
| 1(c) | Cells (p), (q), (q′), (q2), (q3) | Sound, but add (q4) (major 1), (p2) (major 2) and (p3) (major 3) | — |
| 2 | 057/058 to a one-off folder | **Sound** (Q5). The 058 precondition is still partly read from a SHA (minor 10) | `Blockchain/Dev/scripts/run-migrations.sh:118-129`, `:149`, `:197`; `api-gateway/src/startup-migrations.ts:72-96`, `:148-151`; `originate/Dockerfile:75`; `docker-compose.yml:135-136` |
| 3 | Encode-side equality | **Sound.** The comparison must be structural, not a string compare (jsonb normalises key order). In document mode the stored payload may already be a later event's, so R6 fails closed there. That is acceptable, but say so | `cardano/cardanoMetadatum.ts`, `transaction.ts:114-119` |
| 4 | Three knock-ons moot for this document; the resolver closes the class | **Partly.** The hold is moot only for K's retry route. S's flat `POST /api/anchors` can still reset `anchor_c09c1b1f` and mint on the id that S's rows 108/109 reference (minor 7) | `anchoring/src/index.ts:1454-1465`, `:564`, `:571`; gateway `proxy.ts:898-902` |
| 5 | The resolver heals from the blob's own row, then from a bound chain fact | **Sound in design; not safe as a write** (major 6) | `anchorStateSync.ts:179-187`, `:257-275`; `documentRepo.ts:517-640` |
| 6 | `<verb>:<id>` (id ≤ 96 chars), else `<verb>:h:<sha256[:32]>`; the Stuart ask is a flip precondition | **Sound.** 17 + 1 + 96 = 114 ≤ 128; the hashed form is 52 characters | — |
| 7 | "The first pass after"; the count lives in memory | **Sound.** A restart only delays a give-up | `index.ts:2186`, `:2197-2198` |
| 8 | No-op replays return the stored `created_at`; every 202 returns `payloadTimestamp` | Sound | `index.ts:494`, `:507`, `:577` |
| 9, 11 | Complete contract table; on chain an event looks like an upload | Sound | — |
| 10 | Batch fenced | Sound. The batch submit also goes through `submitAnchor` under `withWalletLock` (`index.ts:1991`), so the overlay covers it | — |
| 12, 13 | E1 removes the whole write; 13 is out of scope with a named owner | Sound | `originate/src/routes/anchors.ts:111-132` |
| 14 | Incident code = the pin | **Confirmed.** My diff `bd6697e079fc..6d41673e0f79`, over anchoring `src` (tests excluded), `documents.ts`, `verification(V2).ts`, `anchorStateSync.ts`, `routes/anchors.ts`, `documentRepo.ts`, `run-migrations.sh` and `docker-compose.yml`, lists `anchorSchema.ts` (+58) and `anchoring.openapi.ts`. It also lists `api-gateway/src/routes/proxy.ts` (+51/−11), which the design's diff did not cover. That change adds upstream timeouts only (`UPSTREAM_FORWARD_TIMEOUT_MS`, `jsonOrEmpty`) and is not causal | `git diff --stat` |
| 15, 16 | Carried | Sound | — |
| 17 | Kam list completed | **Incomplete:** see "What Kam is being asked to approve" | — |
| In 3 | The clause was born in #805's squash; the cell paraphrased the node text | **Confirmed.** `git log -S'!ALREADY_INCLUDED_REPLY.test'` returns only `48e65c435`. In `ks726-write-ahead-tx-hash.test.ts`, the retry cell `:414` uses the short form (`:417`) and the control `:452` uses `'this transaction has already been included'` (`:453`) | — |
| In 4 | Give up on `updated_at` | **Sound** (Q3) | `reconciler.ts:98` |
| In 5 | One resolver | **Sound in intent** (Q4 and major 6) | — |
| F2 | Answered vs errored passes | **Sound.** `checkTx` = `waitForConfirmation(tx,1,0,0)` (`index.ts:2192`), which catches provider errors (`cardano/confirmation.ts:98-103`) and returns `confirmed:false` (`:110-119`). So `reconciler.ts:106-108` never sees an outage, and `:98` can fail a settled row during one | — |

---

## Findings

### 1. MAJOR: The input pin works pairwise. A retry chain can still mint the same payload twice
**Evidence.**
- Guard 3 re-polls only `known`, the row's current hash (`anchorSubmission.ts:621-624`).
- A transaction sitting in a mempool reads as "not found": `getTransaction` returns null until the transaction is in a block (`confirmation.ts:74-97`). So KS-1171's "absent" means "not in a block within ~27 minutes".
- The TTL is slot + 7200 (`transaction.ts:102-104`), about 2 h. A signed transaction can therefore still land long after its re-poll has called it absent.
- Rev 2 §3.2.3 pins the retry X′ to X's still-unspent inputs, and §3.3 releases X's claims when X is refuted.

**The sequence that still double-mints.** This is the design's own case 1, a same-hash duplicate, while X is still in a mempool.
1. X is refused with "inputs spent". The re-poll reads absent after ~27 min. Retry X′ is pinned to X's input u.
2. X′ conflicts with X in the mempool and is refused.
3. X lands. X′ re-polls absent.
4. Retry X″ pins to X′'s still-unspent inputs. That set is empty, because X spent u. X″ builds freely and lands.

Result: X and X″ carry the same stored payload, and the platform pays two fees. KS-705's double-mint returns two steps down the chain.

The design's risk 2 ("the pin removes the second condition") holds for X′ only. §3.2 asks only whether the refused transaction can land. It never asks whether the transaction that spent the refused one's inputs is our own earlier attempt at the same payload.

**Required change.**
- Before any guard-3 retry, re-poll every hash this process signed for the anchor whose TTL has not passed. The overlay already holds them, with the claimed outpoints and the claiming transaction. If any of them is found, confirm with it and do not retry.
- Equivalent alternative: pin each retry to the union of every unexpired ancestor's still-unspent inputs.
- Add cell (q4): X in a mempool for 30 minutes, X′ refused, X lands; assert that no X″ is built. Mutant: re-poll `known` only.
- State the limit: after a restart, the overlay and the ancestor list are gone. The gap is narrow, but KS-1171 exists exactly for this kind of false negative.

### 2. MAJOR: The overlay's claim release reopens the replica-lag hole it was chosen to close
**Evidence.**
- §3.3 rejects option (iii) because "one consistent read does not make the next read consistent if requests land on different backends".
- But §3.3's release rule ends a claim "when the fetched view stops listing that outpoint". `fetchUtxos` is a bare `addressesUtxos` call with no consistency token (`provider.ts:329-340`).
- So a fresh replica can release the claim, and the next read, from a stale replica, lists the outpoint again. It becomes a candidate, and the 1 ms refusal recurs.

**Required change.**
- An outpoint spent by an own transaction known to be confirmed can never become unspent again (short of a rollback). Keep its claim for a fixed horizon, at least the spending transaction's TTL window (about 2 h), whatever the fetched view says. The memory cost is a few entries.
- Release early only for outpoints whose spender was refuted.
- Add cell (p2): the provider alternates fresh and stale views on every call. Mutant: the release-on-unlisted rule.

### 3. MAJOR: Claims of definitively refused transactions can starve the wallet for up to 2 h
**Evidence.**
- A refusal other than "inputs spent" (`ValueNotConservedUTxO`, an expired TTL, a script or fee error) falls through guard 5 (`:584-590`) and fails `isAlreadySubmittedError` (`:120-124`). It then goes straight to `failed`, `pending` and a retry 5 s later (`:654-677`). There is no re-poll, so §3.3's "refuted (refused and re-polled absent)" never happens.
- The claim on X's inputs, which are genuinely unspent, therefore lasts until the TTL (about 2 h) or until the provider stops listing them, which it never will.
- Coin selection is `LargestFirstMultiAsset` with one change output (`transaction.ts:96-99`, `:122`). That drives a wallet toward very few UTxOs.
- With one or two UTxOs, every build for up to 2 h hits the empty-candidate fallback (6 × 5 s), fails, uses up `maxRetries` (3), and ends in terminal `failed`. That is an anchoring outage caused by the fix.
- **The wallet's UTxO count on each box is UNMEASURED.**

**Required change.**
- Release a transaction's claims as soon as the node's answer is a definitive refusal (`isChainReachableError(err)`, `provider.ts:128-134`). Rely on the pin (major 1) for the "inputs spent" class.
- Add cell (p3): a one-UTxO wallet and a `ValueNotConserved` refusal; the next anchor builds at once.
- Add a census of the wallet's UTxO count on each box (a read; Kam-approved reader).

### 4. MAJOR: A second in-process wallet spender is outside the lock and invisible to the overlay
**Evidence.**
- `POST /api/anchors/thread-mint` (`anchoring/src/index.ts:1008-1065`) calls `mintAndLock`. That function builds with lucid from the same `PLATFORM_WALLET_MNEMONIC` (`cardano/threadTokenMint.ts:241-263`), reads `lucid.utxosAt` and submits (`:337-339`).
- It is not wrapped in `withWalletLock`. `git grep withWalletLock` under `anchoring/src` hits only `anchorSubmission.ts` and `index.ts:39`, `:1879`, `:1991`.
- Originate calls it only when `STATE_THREAD_NFT_ENABLED === 'true'` (`documents.ts:804-807`), but the anchoring route itself checks only for configured keys (`:1043-1048`).
- The gateway's catch-all `router.use('/api/anchors', authenticateToken(true), proxy)` (`api-gateway/src/routes/proxy.ts:911-914`) forwards it, with no scope requirement. No gateway rule names `thread-mint` (`git grep` returns 0).
- Anchoring requires only a JWT (`index.ts:469`).

**Impact.**
- **Any authenticated caller can make the platform wallet pay for a mint.** This is reachable by reading; I did not exercise it.
- Each such mint spends UTxOs the overlay does not know about. That is the KS-535 "foreign spender" shape, but inside one deployment.
- **Unmeasured:** `STATE_THREAD_NFT_ENABLED` per box.

**Required change.**
- F0 either routes `mintAndLock` through `withWalletLock` and the overlay, or fences the route (for example, refuse it unless the flag is on and the caller is originate's signed hop, `emitterGuard`).
- Route the fee-drain half to Wednesday as security-class, beside 16.9.

### 5. MAJOR: F0's compare-and-set cannot report its result, and it covers too few writes
**Evidence.**
- `updateStatus` is typed `Promise<void>` (`anchorSubmission.ts:187`).
- The real implementation, `dbUpdateAnchorStatus` (`index.ts:1689-1721`), returns nothing and swallows every error (`:1718-1720`). It only logs a guarded zero-row miss (`:1710-1717`).
- §3.2.2 says "zero rows matched → no retry", but as specified the submitter cannot tell a match from a miss, or from a DB error. The likely implementation reads `void` as success and retries, which bypasses the guard.
- The other terminal writes in the same catch stay unguarded:
  - the no-known fall-through and every non-"inputs spent" refusal write `failed` and then `pending` by id alone (`:656-677`);
  - the reconciler's `confirmed` and `failed` writes are by id alone (`reconciler.ts:88-102`).
- A reset row with a new transaction Y in flight can therefore be stamped `pending`, with Y left on the row, which `knownChainSubmission` does not count (`:246-247`). Or it can be stamped `confirmed` with X's block fields and Y's hash.

**Required change.**
- `updateStatus` returns the affected row count.
- The retry proceeds only on exactly 1. An error or `null` means no retry (fail closed).
- Guard every `failed`/`pending` write in the catch, and the reconciler's two writes, on `(status, transaction_hash)`.
- Extend (q3) with a DB error during the guarded write; assert no retry.

### 6. MAJOR: The resolver's "same answer whatever the order" is check-then-write, and the retry route can still pay twice
**Evidence.**
- `updateDocument` (`originate/src/repositories/documentRepo.ts:517-640`) merges the blob unconditionally. Its only guard is `ifStatusIsNot` on the row's status (`:539`, `:599-610`).
- `markDocumentAnchorFailed` reads, then writes (`anchorStateSync.ts:179-187`).
- The poller writes on every poll that carries a hash (`:257-275`).
- So "`confirmed` stays terminal" is a JavaScript check on an earlier read. A resolver call that is writing `anchor_failed` can land after another call's `confirmed`.
- The retry route's gate is also a read: `:1458`, followed by the POST at `:1474`.
  - Two concurrent calls both pass it and both POST.
  - The second upsert resets the first attempt's row to `pending` with a NULL hash (`anchoring/src/index.ts:1454-1465`), and `processAnchor` runs again (`:564`). Two transactions are paid for.
  - D14's chain lookup runs before both POSTs and finds nothing in both.

**Required change.**
- The resolver writes through a conditional UPDATE whose WHERE clause carries the blob's expected status (never overwrite `confirmed`; write `anchor_failed` only from an in-flight state).
- The retry route first claims the blob by compare-and-set, `anchor_failed`/absent → `retrying`, and only then does the lookup and the POST. A loser answers 409.
- Add a cell: two concurrent retry calls, exactly one POST. Add a cell: interleaved resolver writes never downgrade `confirmed`.

### 7. MINOR: D14's fee guard covers K's retry route only; the hold on this document is not moot
**Evidence.**
- S's flat fallback `POST /api/anchors` (gateway `proxy.ts:898-902`) and originate's emitters in document mode (rev 1 sites) reset the document row and mint (`index.ts:1454-1465`, `:564`), with no chain check.
- For `anchor_c09c1b1f`, a flat re-POST from S returns the same id (`:571`) and stamps a new transaction on the id that S's rows 108/109 reference. That is the false attribution D9 exists to avoid.
- **Unmeasured:** whether S re-POSTs a row it reads as `failed`.

**Required change.**
- Say in §5.2 that D14 closes only the K retry route.
- Keep the first review's comms line holding retries for `deb6d3c3…` until S's behaviour is measured or D9b is done. This is Kam-gated comms.

### 8. MINOR: A chain read that errors becomes a 503 loop, and that loop can feed the quota outage
**Evidence.**
- S's registrar retries every non-2xx on every tick (cited by rev 2 at `anchorOverwriteGuard.ts:428-430`).
- §5.4 caches nothing for a truncated or errored scan.
- So every tick costs up to a 4 s, 10-page wallet scan per document. Under a Blockfrost 402 (the KS-670 quota signature), that load makes the outage longer.

**Required change.** Cache errored or truncated results per document for about 60 s, and answer the 503 with `Retry-After`.

### 9. MINOR: R6 still scans from `created_at − 10 min`, which contradicts D13
**Evidence.**
- §9 R6 scans "since `created_at − 10 min`".
- `created_at` is never reset by the upsert (it is absent from the SET at `index.ts:1455-1524`). So a document row re-armed months after creation scans the wallet from creation day, exhausts its budget, and gets "next pass" every pass.
- That is a new way for a row to "never settle".

**Required change.** Use the attempt's time (`updated_at` minus a margin), the same basis as D13.

### 10. MINOR: 058's other precondition is still read from "that box's SHA"
**Evidence.**
- §8.4 moves anchoring's precondition to `/health`, but keeps "zero code writers naming `ON CONFLICT (document_id, network)` at that box's SHA".
- Originate's `saveAnchorToDb` names exactly that target (`originate/src/routes/anchors.ts:125`) and is reachable from originate's own routes (rev 1 lists `:219` inside a GET, `:343`, `:443`). E1 removes it.
- A box whose originate was not recreated keeps the old code. That is the first review's 2(c) in a different service.
- 058 is SQL, and SQL cannot read `/health`. The check must live in the one-off runner, and the window between the check and the DROP should be named.

**Required change.** Add a build marker to originate's `/health` (as PR C adds one to anchoring's). The runner checks both services, immediately before the DROP.

### 11. MINOR: "1(b) executes Kam's 09-14 ruling; no new card" is only PARTLY accurate
**What I read** (`decision_queue.sh show secuura-805-guard5-node-rejection-retry`):
- Option `retry` (ruled 2026-09-14T20:06:54+10:00) is "fall through when `isChainReachableError(error)` is true … status_code 400 after onSigned → scheduleRetry". Its stated premise is "a refused transaction is safe to retry (no second fee)".

**Accurate:**
- The clause makes the ruled retry unreachable for the node's real text. Dropping it moves the code toward the ruling.
- KS-1171 (09-25) later conditioned "at once" on two answered polls and 60 s. The design keeps that.

**Not covered by the ruling:**
- The card never weighed the "already included" text. Wednesday's own delivery carved that text out precisely to protect against KS-705's double-mint, which is a money question.
- The input pin edits coin selection, which rev 2 itself classes as Kam/money (D12, §13.3 step 1).
- Major 1 shows that "no second fee" does not yet hold structurally.

**Required change.** F0 is a Kam card anyway, so name 1(b) on it as "drops the KS-705 text carve-out; money-relevant; implements your 09-14 retry under your 09-25 absence rule". It costs no extra decision and removes any doubt that Kam saw the change.

### 12. MAJOR (pre-existing, security-class): 16.9 is CONFIRMED; its "identity rides the payload" part is PARTLY right
**Evidence at the pin:**
- **Handler** (`originate/src/routes/documents.ts:1437-1571`):
  - it checks only that a user exists (`:1442-1445`) and that the document is found in the caller's tenant (`:1448-1453`);
  - its only state gate is the blob (`:1458`);
  - there is no role check, unlike create, share, transfer and version, which call `isAllowedByRoleOrScope(…DOCUMENT_WRITE_ROLES…)` at `:387-388`, `:1803`, `:2279`, `:2477`;
  - there is no owner or organisation check, and no `revoked` check (compare `:2681`);
  - it writes `status: 'anchored'` without `preserveTerminalStatuses` (`:1534-1537`), so **16.10 is confirmed too**.
- **Mounted middleware:**
  - originate: `documentsRouter.use(authenticate())` (`:175`); `index.ts:276` mounts it after tenant context only;
  - gateway: `router.use('/api/documents', authenticateToken(true), attachScopes, requireScope('documents:read','documents:write'), …)` (`proxy.ts:654-659`). `requireScope` admits any one of the listed scopes and lets every JWT through (`middleware/scopes.ts:36-39`, `:51`). So **an API key holding only `documents:read` can POST this route**;
  - originate then calls anchoring directly (`:1472-1474`), which **bypasses the gateway's `anchors:write`** (`proxy.ts:898-902`).
- **At anchoring:**
  - only KS-1603's tenant check stands in the way (`index.ts:1428-1439`);
  - the reset and the mint happen for any same-tenant caller;
  - the caller's identity fields (`documents.ts:1489`) replace the stored payload **only when** KS-1385's ownership guard admits the caller as the issuer's organisation or the custodian's (`index.ts:1445`, `:1502-1523`). Otherwise the stored payload is kept. So "the retrier's identity rides the payload" is PARTLY right.
- **Reach:** documents with `anchor_failed`, and **documents with no blob at all**. Versions and lineage documents are created unanchored by design (`documents.ts:2253`, `:2427`, `:2928`, `:3199`), so for them this is the normal anchor route.
- **The ruling it breaks:** any user in a tenant can do this across organisations, which crosses the 2026-09-07 `bind` ruling (organisation is a trust boundary inside a tenant).

**Required change.** Out of KS-1384's scope; route it as security. PR R should add the role, organisation and revoked checks while it is in this handler anyway, as a reviewed fix.

### 13. INFO: D13 verified at the repo level; residuals named
(See Q3.)

### 14. INFO: F0 changes fees and attribution in today's document mode
- With 1(b), a refused event attempt now lands about 27 minutes later. That is one fee per refused event, where today the row rests.
- The document row then records the latest event's transaction. In the kintsugi shape, that would be the transfer.
- Until the flip, row 1 of the resolver ("the row is `confirmed` → the document is `confirmed`") can confirm a document with an event's transaction, because the document row still carries event attempts.
- Rev 2 says "closed only by per-event rows". The Kam card should say plainly that F0 alone increases landed transactions.

### 15. INFO: Overlay (a) assumes the submit node has applied the confirming block
- The 1 ms build will spend the change output that was just confirmed.
- If Blockfrost's submit backend lags its indexer, the child is refused for a missing input. Then (b) recovers it about 27 minutes later.
- §3.4's "(a) alone closes the stuck row" depends on this, and it is UNMEASURED. The same full `error` capture that §17 asks for would show it.

### 16. INFO: The overlay must persist claims whichever site confirms
- §3.3 marks own outputs confirmed at `anchorSubmission.ts:488` and in the batch.
- Confirmations also happen in `reconfirmKnownSubmission` (`:282-301`) and in the reconciler (`reconciler.ts:87-95`).
- Missing those is safe, because claims still exclude the spent inputs, but it pushes builds into the wait fallback. List all four sites.

---

## Q2. Is F0 safe? Sequences that still double-spend or still stick
**Against KS-705** (the node says "already included" for a transaction that IS on chain):
- **Safe for the refused transaction itself.** A same-hash X that is in a block is found by the 27-minute re-poll (`:282-301`), and dropping the clause changes nothing there.
- **Not safe across a retry chain** when X is still in a mempool past the re-poll (major 1).

**Against the stale-UTxO 1 ms race:**
- **Closed on a single consistent backend.**
- **Not closed under replica lag**, because of the release rule (major 2).
- **Not closed while thread-mint spends the same wallet** (major 4).

**Still sticks:**
- (i) A provider error during the 27-minute re-poll leaves the row resting `'unknown'` for D13's 24 h (`:341-369`). That is accepted under KS-1171, but say it.
- (ii) A restart during the re-poll does the same, because there is no restart re-queue (`:670-672`).
- (iii) A wallet with few UTxOs after a non-"inputs spent" refusal: up to 2 h of failures (major 3).
- (iv) R6 for re-armed old rows (minor 9).

**The double-spend that remains:** X stuck in a mempool for 27 minutes or more, then landing, with X′ and then X″ retried (major 1). The guarded writes are also silently unguarded until major 5 is fixed.

**Is "executes the 09-14 ruling" accurate?** PARTLY (minor 11).

## Q3. D13: is every non-transition `updated_at` writer safe?
**Checked, every writer of `anchor_store`** (`git grep -i` for `update anchor_store` / `into anchor_store` across `Blockchain/`, tests excluded):
- `anchorStatusUpdate.ts:114` (always adds `updated_at`, `:101`);
- `index.ts:1448` (the upsert, `updated_at = EXCLUDED.updated_at` at `:1524`; it always resets the status to `pending` and then calls `processAnchor`, `:564`, so it always starts a new attempt);
- `index.ts:1874` (`retry_count` only; no `updated_at`);
- `originate/src/routes/anchors.ts:112-131`;
- `migrations/003` (INSERT only);
- a runbook line in `deployment/DEPLOYMENT-ARCHITECTURE.md:119` (manual; it also sets `simulated=true`, so the reconciler excludes the row).

**Triggers:** no `CREATE TRIGGER`, `EXECUTE format` or generic `updated_at = NOW()/NEW` loop names `anchor_store` in any `Blockchain/Dev/*.sql` file or in `startup-migrations.ts`.

**Nothing found breaks "24 h of silence" by keeping a dead attempt alive indefinitely.** Residuals:
- (a) **Originate's `saveAnchorToDb`** sets `updated_at = NOW()` with no status change, and writes anchoring's id (not a 64-hex hash) into `transaction_hash` (`:125-131`). The reconciler then skips the row entirely (`reconciler.ts:83`). It is reachable only when originate is called directly, because the gateway sends `/api/anchors` to anchoring (`proxy.ts:898-914`). But E1, which removes it, is sequenced after F. Either fold its removal into F, or have F's test evidence assert that it is unreachable.
- (b) **057 must not name `updated_at`.** If it did, it would reset every live row's clock (a delay, so the safe direction, but it would surprise).
- (c) **Hand-made live triggers are UNMEASURED.** The design says so.

## Q4. D14: is the outcome independent of reader order, and is the fee risk closed?
- **Order independence:** **yes in logic, no in writes**, until the conditional UPDATE of major 6. Nothing in today's `updateDocument` stops a late writer.
- **The fee risk:** closed for **sequential** calls to **K's retry route** only. Not closed for concurrent retry calls (major 6), S's flat path, or document-mode emitters (minor 7).
- **When the chain read errors:**
  - heals and the GET reconcile leave the document unchanged (correct);
  - the poller's "2 × failed → `anchor_failed`" path becomes a lookup, so an errored lookup leaves the document in flight. That is correct, but a cold outage leaves documents "pending" with no end;
  - the retry route answers 503 (correct, but see minor 8's loop).
- **The binding key:** the `timestamp`, plus `payloadTimestamp`, plus `createAttempts`, is sound going forward. Legacy documents bind on `anchoredAt`, which the poller rewrites from the row's `created_at` (`anchorStateSync.ts:269`, `:388`); because the upsert never touches `created_at`, that value is the original create's ±1 ms. That supports the ±2 ms rule. **How often it holds is still UNMEASURED** (one instance).

## Q5. Is moving 057/058 to a one-off runner sound?
**Yes.**
- **The compose runner** reads only `migrations/*.sql`, non-recursively (`run-migrations.sh:149`). It records by basename after success (`:118-129`) and exits 3 on any failure (`:197`).
- **The gateway runner** reads only a `migrations` directory (`startup-migrations.ts:72-96`, `readdirSync` plus `.endsWith('.sql')`) and records after success (`:148-151`).
- **Images:** both images ship only `migrations/` (`originate/Dockerfile:75`). A sibling `migrations-oneoff/` is invisible to both. A `oneoff:` prefix in `_secuura_migrations` cannot collide with either.
- **No runner race on 056:** the gateway waits for the `migrations` service (`docker-compose.yml:135-136`).

**Remaining items:**
- the 058 precondition (minor 10);
- the one-off folder is not in any image, so a seat runs it from a checkout against a box's database. That is a box write, Kam-gated;
- on a PG < 11 server, 056's `ADD COLUMN … NOT NULL DEFAULT` rewrites the table. `server_version` is still UNMEASURED.

## Q6. Security item 16.9
**CONFIRMED** for the missing owner, role and revoked checks, with the line evidence in finding 12. It is broader than stated: an API key holding only `documents:read` passes the gateway (`proxy.ts:657`, `scopes.ts:51`), and the originate→anchoring hop bypasses `anchors:write` (`proxy.ts:898-902`). **PARTLY** for "the retrier's identity fields ride the payload": that happens only when KS-1385's guard admits the caller (`index.ts:1445`, `:1502-1523`).

## Q7. New risk the revision introduces
1. **The overlay** (majors 2, 3, 4): a release rule that undoes it, starvation of wallets with few UTxOs, and a second spender it cannot see.
2. **Dropping the KS-705 text carve-out with a pairwise pin only** (major 1).
3. **More landed transactions in document mode** from 1(b) (info 14). This is the ruled direction, but Kam should see it.
4. **A new public-ish anchoring endpoint `POST /api/anchors/own-create`:** it needs the same tenant check as `GET /api/anchors/:id`. It reveals only chain facts, but it costs provider quota per call, so rate-limit it with the minor-8 cache.
5. **PR R widens the hot set** (`documents.ts`, `anchorStateSync.ts`, `verification(V2).ts`) and makes every reader depend on anchoring for the chain. A slow anchoring now affects GET latency through the 15-minute reconcile path. The deadline bounds it (§5.4); a cell should pin the deadline.

---

## What Kam is being asked to approve (every Kam-class step, with my view)
| # | Step | My view |
|---|---|---|
| 1 | **F0's UTxO-selection change (overlay) and the 1(b) guard-3 change** | **Not yet.** Fix majors 1-5 first. Present 1(b) on the same card, named as money-relevant (minor 11), and say F0 increases landed transactions in document mode (info 14) |
| 2 | Merging A = 056 applied on both boxes at the next deploy (FYI) | Agree it is FYI-class. Add `server_version` to the FYI or measure it first |
| 3 | Applying B (057) on each box | Sound once the one-off runner exists. 057 must not touch `updated_at` |
| 4 | Applying D (058), one-way, on each box | Only with originate's running build checked too (minor 10) |
| 5 | The flip on each box | Agree with the preconditions (D applied, R deployed, the Stuart ask answered), **plus** major 6's conditional writes in R |
| 6 | D9b: re-key `anchor_c09c1b1f`, then adopt `b1cc72f9` (two cards) | Sound. Until then, keep the hold/comms line for S (minor 7) |
| 7 | D2 (fees, batching), R8 (re-drive) | Unchanged; Kam's |
| 8 | Comms: the §11 contract changes and the Stuart ask | Agree. Add: "K's retry route may now answer 409/503", and the hold line from minor 7 |
| 9 | **Missing from rev 2's list:** routing majors 4 and 12 (thread-mint fee drain; the retry route's authorisation) as security | Wednesday routes them; any fix to production behaviour goes on Kam's card |
| 10 | **Missing:** the wallet UTxO census on each box (read-only, but box contact) | Needed to size major 3 |

## TESTED / NOT TESTED
**TESTED (read, not run).** Every `path:line` above was read at `6d41673e0f79` with `git show` into the session scratchpad, plus `git grep`, `git diff --stat` and `git log -S` in the cache clone. Specifically:
- `anchorSubmission.ts` (whole);
- `reconciler.ts` (whole);
- `anchorStatusUpdate.ts:30-118`;
- `index.ts` `:470-593`, `:1000-1075`, `:1400-1560`, `:1689-1721`, `:1846-1900`, `:2180-2240`;
- `cardano/transaction.ts:20-148`;
- `cardano/index.ts:200-270`;
- `cardano/provider.ts:100-145`;
- `cardano/confirmation.ts` (whole);
- `originate/src/routes/documents.ts` `:160-200`, `:795-822`, `:1432-1571`;
- `anchorStateSync.ts` `:173-190`, `:242-290`, `:353-404`;
- `routes/anchors.ts:100-135`;
- `documentRepo.ts` (signatures and guards);
- `originate/src/index.ts` (mounts);
- `api-gateway/src/routes/proxy.ts` `:640-662`, `:890-915`;
- `middleware/scopes.ts:1-70`;
- `run-migrations.sh` (whole);
- `startup-migrations.ts` `:69-165`;
- the compose `migrations` and `api-gateway` blocks;
- `originate/Dockerfile`;
- `ks726-write-ahead-tx-hash.test.ts:410-460`;
- the decision-queue card (shown, exit 0).

**NOT TESTED / not read:**
- No cell, mutant, container, database or box was run or touched. Every finding is an inference from code.
- **Not read:** `verification.ts` / `verificationV2.ts` heal lines (I relied on rev 2 and its sub-agent C for those); rev 1 in full (grep only); T 6th's and D 42nd's evidence files; sub-agents A, B and C's raw reports; `anchorOverwriteGuard.ts` beyond the grep; `threadTokenMint.ts` beyond `:130-170` and the grep hits; the batch path `:1960-2130`.
- **UNMEASURED:** the wallet UTxO count per box; `STATE_THREAD_NFT_ENABLED` per box; whether `thread-mint` is ever called on a box; whether S re-POSTs a failed row; Blockfrost's replica and submit-node lag; whether any transaction ever sat in a mempool for more than 27 minutes on these networks; `server_version`; hand-made live triggers.
- **Reachability of major 4 and finding 12** is by reading only; neither was exercised.

**Footprint.** Read-only everywhere. Writes: this file, and source extracts in the session scratchpad. No write under `!CODING`, no ticket, PR, branch, box, `az`, Docker or mail.
