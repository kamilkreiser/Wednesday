# KS-1384 rev 3: third independent review (narrow: the parts listed in §19 only)

**Reviewer:** an independent, read-only reviewer for Wednesday, 2026-10-29 (late evening AEDT).
**Reviewed:** `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-10-29_seatW-8th/KS-1384-per-event-anchor-DESIGN-rev3.md` (472 lines, read whole), `CARD_TEXT_for_Kam.md` (40 lines) and `HANDOVER.md` (38 lines) beside it. Review 2 (`../2026-10-29_ks1384-design-review-2/review.md`, 355 lines) was read whole, to see what it asked for.
**Code:** develop `6d41673e0f79c0f02c2ec7b893cc960b6fa3ec10`, read with `git show` / `git grep` / `git ls-tree` only, from Wednesday's cache clone. Paths are under `Blockchain/Dev/services/` unless they start with `Blockchain/Dev/`.
**Scope:** the seven items in rev 3 §19, plus the card. Everything reviews 1 and 2 already settled is out of scope and is not re-opened here.

---

## Verdict: SOUND WITH CHANGES

**By §19 item:** 1 SOUND (item 4), 6 SOUND WITH CHANGES (items 1, 2, 3, 5, 6, 7), 0 UNSOUND.
**Findings:** 0 blocker, 4 major, 6 minor, 3 info.

**The shared family outpoint is a real improvement on the union pin.** Every member of a family spends `u_F`, so no two members can both be in the ledger. That holds whatever the mempool does, across TTL expiry, the 24 h exclusion and the `NoSpendableUtxo` wait. It also holds when `u_F` is spent by anything else (thread-mint, nft-certificate, collateral, a change chain): once `u_F` is gone, no member can land.

**The hole is in the one place rule 4 lets a retry build without `u_F`.** Rule 4 assumes that a confirmed transaction outside the family cannot carry this payload. After a restart (or with a second replica), it can: a pre-restart same-payload transaction is "outside the family". Today the "already included" text clause blocks the retry in exactly that case. So rev 3's "no worse than today after a restart" is **not true**: F0 is worse than today there. The fix is cheap (major A).

The other three majors are liveness or money problems in the mechanisms new to rev 3:
- a 2 h wait that a restart strands invisibly (B);
- an add-back rule that a foreign spender turns into up to 24 h of refusals (C);
- a 10-minute claim expiry that is shorter than anchoring's own in-flight horizon (D).

**F0 is safe to deploy beside nft-certificate for "one payload, at most one fee" once A is fixed. It is not safe for availability until C is fixed.**

## BLUF
1. **Item 1 (major A).** `u_F` makes the members of a family mutually exclusive. Rule 4's "spent by a confirmed transaction outside the family → close the family and build freely" must first read that spender's metadata. If the spender carries this anchor's payload, the row is confirmed with it and nothing is built. Without that check, restart + mempool + front-door rebuild double-mints, and F0 makes this reachable where today's clause stops it.
2. **Item 3 (major B).** The `NoSpendableUtxo` wait can now last 2 h. It lives on a timer, and the row it leaves is `pending` with a NULL hash, which the reconciler does not select. A restart or deploy in that window strands the row with no end. D 43rd recreates anchoring tonight; that is a restart.
3. **Item 7 (major C, in the §3.3 view).** Once a foreign spender (nft-certificate, or lucid's own selection in thread-mint) consumes one of our confirmed change outputs, the add-back rule keeps offering that output as a candidate. No fetched view will ever list it again. `LargestFirst` picks it first, so builds are refused for as long as the add-back lasts, up to the 24 h confirmed window.
4. **Item 5 (major D).** A reclaim after 10 minutes can POST while the first attempt is still in flight: the 27-minute re-poll, the 2 h wait, or the 2 h TTL. The upsert resets the row to a new payload, which means a new family, and both transactions can land.
5. **Item 7, confirmed.** nft-certificate gets the same mnemonic (`docker-compose.yml:1694`, inside the `nft-certificate:` block that starts at `:1660`) and derives the same keys. By reading, it goes Cardano-ready automatically wherever the key, the mnemonic and the network line up, and the gateway proxies to it on compose boxes. D17's "keep it off" has no switch: it is a box config change.
6. **The card** overstates where review stands, mis-states the default's buildability (F depends on F0 in rev 3's own PR table), and omits the 2 h delay and the restart limit.

---

## Item 1: the shared family outpoint (§3.4): SOUND WITH CHANGES

**What holds (checked against the builder).**
- The builder feeds every fetched UTxO to `add_inputs_from(…, LargestFirstMultiAsset)` (`anchoring/src/cardano/transaction.ts:96-99`). A preceding `add_regular_input(u_F)` is a valid way to force an input in CSL.
- So every member spends `u_F`, and every pair of members conflicts. **At most one member can be in the ledger.** That is structural, not timing.

Each scenario the brief asked about:

| Scenario | Holds? | Why |
|---|---|---|
| Crash before the write-ahead | yes | The signed transaction was never submitted, so it cannot land |
| TTL expiry | yes, if judged on the chain | A member past its own encoded TTL cannot be included. Judge "past" on the TTL value in that member's body, against an **answered** chain-tip read, never the local clock. The TTL comes from cached params (`cardano/index.ts:135-145`, `provider.ts:304`, `:318`), so it is only ever earlier, which is the safe direction |
| 24 h exclusion | yes | It concerns other outpoints. A confirmed member ends the family |
| `NoSpendableUtxo` wait | yes | The family state is kept while the attempt waits, and members only expire |
| `u_F` taken by thread-mint (`threadTokenMint.ts:263-264`, `:337`; lucid's `complete()` selects its own inputs and **collateral**), nft-certificate (`nft-certificate/src/cardano/mintTransaction.ts:41`, its own `fetchUtxos`), a change chain, or forfeited collateral | **yes, for at-most-one** | Once `u_F` is consumed by a non-member, no member can land. Rule 4 then closes the family, which is correct, **provided the spender is not itself a same-payload transaction** (below) |
| Restart | **no** (major A) | — |

### MAJOR A: rule 4's closure trusts "outside the family" to mean "not this payload". After a restart it does not, and F0 is then worse than today
**Evidence.**
- The upsert resets the row unconditionally (`status`/`transaction_hash = EXCLUDED…`, `anchoring/src/index.ts:1454-1465`) and keeps the stored payload unless KS-1385's guard admits the caller (`:1502-1523`). So after a restart, a front-door call rebuilds the **same payload** as a fresh family (Y, with `u_F'` = one of Y's inputs).
- Blockfrost's UTxO endpoint is block-indexed. If a pre-restart X is still in a mempool, Y very likely selects X's input (`LargestFirst`) and is refused with the node's real text, `All inputs are spent. Transaction has probably already been included…` (`anchorSubmission.ts:28-30`).
- **Today** the text clause makes `refusedAndAbsent` false for that text (`anchorSubmission.ts:637-641`). The row rests and **no retry is built**.
- **Under F0** the clause is gone. The family re-poll (members = {Y}) reads absent. Y′ spends `u_F'`. If `u_F'` is the input X spent, then once X lands, rule 4 sees "`u_F` not listed". The lookup says it was consumed by a **confirmed transaction outside the family** (X). The family closes, and Y″ builds freely and lands. **X and Y″ carry the same payload: two fees.** If `u_F'` is one of Y's other inputs, Y′ itself can land beside X.
- §3.4's "The limit" says that within one TTL window after boot, F0 is "no worse than today". For this sequence that is false: today's clause stops it, and F0 removes the clause without the family that was meant to replace it.

**Required change.**
1. **Before closing a family on a foreign or own non-member spender of `u_F`, read the spender's label-674 metadata** (one `txs/{hash}/metadata` read). If it carries this anchor's payload (the same structural `deepEqual` R6 uses, or at least `documentId` + `hash` + `timestamp`), **confirm the row with that transaction** (guarded, §3.7) and build nothing. Only a spender that provably carries a different payload closes the family. If the metadata cannot be read, the row rests (fail closed), as rule 4 already does when the spender lookup cannot be read.
2. **In guard 3, apply 1(b)'s retry only when every hash the row has carried for this payload is a member this process signed.** Simplest form: if the row's current hash is not in the in-memory family, keep today's behaviour (rest). This closes the post-restart window without D18.
3. Correct §3.4 "The limit" and §16 risk 2: with (1) and (2), say "no worse than today". Without them, say "worse than today for one TTL window after boot".
4. **Cell (q6):** X is in a mempool before a simulated restart; a front-door rebuild Y is refused with the real text; X lands; assert that no Y″ is built and the row is confirmed with X. Mutant: close the family on any confirmed non-member spender.

### MINOR 1: precision for rule 4
- Judge "every member past its TTL" on each member's **encoded TTL** against an answered chain-tip read.
- Close on a non-member spend only at a stated confirmation depth (for example, the reconciler's threshold, or ≥ 3 blocks). A 1-block spend can roll back. The window is narrow, but closure is the one action that removes the structural guarantee.
- The view must record **collateral inputs** too (thread-mint is a Plutus V3 mint, `threadTokenMint.ts:286-289`), and parse them from the signed body as §3.6 says.
- Choose `u_F` deterministically (for example, the first member's largest input) and pin the choice in cell (q5), so the cell does not depend on CSL's selection order.

---

## Item 2: the write-ahead's row count gates the submit (§3.7.5): SOUND WITH CHANGES

**What holds.** `submitAnchor` awaits `options.onSigned(txHash)` **before** `submitTransaction` (`anchoring/src/cardano/index.ts:254-262`). A throw there means nothing is sent. Today `onSigned` cannot fail, because `dbUpdateAnchorStatus` swallows every error and returns `void` (`anchoring/src/index.ts:1689-1721`). The submit therefore proceeds even when the guarded write matched 0 rows. That is the defect §3.7.5 closes, and gating on exactly 1 is right. The guard is jsonb structural equality (`anchorStatusUpdate.ts:107-111`), so a round-tripped payload matches. I found no DB-less mode it would newly break: with no DB, `getAnchor` reads nothing and `submitAnchorToChain` returns at `anchorSubmission.ts:380-381`.

### MINOR 2: a throw from `onSigned` lands in the ordinary catch, which retries
At the pin, an error thrown inside `deps.submit` reaches the catch with `writtenAheadTxHash` unset (`anchorSubmission.ts:476`). It is not "already submitted", so it falls through to `failed`, `pending` and `scheduleRetry` (`:654-678`). For the **0-row** case, §3.7.5 says "return quietly; the newer call owns the row". **Required change:**
- Use a typed `WriteAheadDeclined` error, checked first in the catch, that returns without any write.
- Log it at warn with the anchor id.
- Add to (q3b): "0 rows → no `failed` write, no `scheduleRetry` call".

### MINOR 3: classify a signed-but-never-submitted transaction in the ledger view
§3.3's table defines live (some submit accepted or lost) and dead (every submit refused, or TTL lookup not found). A transaction that was signed but never sent, because the write-ahead was declined or returned `null`, is neither. If the view records members at signing, such a transaction may be read as live. It then holds `u_F` against **its own family's** next retry (rule 4: "claimed by another of our own in-flight transactions → wait") until its TTL lookup, about 2 h. **Required change:**
- A transaction with zero submits is **dead at once**.
- Or record it in the view only after the write-ahead returns 1.
- Pin this in (q3b).

---

## Item 3: `NoSpendableUtxo` spends no retry (§3.5): SOUND WITH CHANGES

**What holds.** Not spending `maxRetries` (`anchorSubmission.ts:255`) on a busy wallet is right. Today an empty view throws `No UTxOs available` (`transaction.ts:30-32`) into the ordinary failed path, which turns a busy wallet into terminal failures. In-process, the wait is bounded by "up to the TTL horizon (2 h)".

### MAJOR B: a restart during the wait strands the row with no end
- The re-queue is a `setTimeout`, like `scheduleRetry` (`anchoring/src/index.ts:1877`). Anchoring has no restart re-queue (`anchorSubmission.ts:670-672`).
- During the wait the row is not `failed` (by design). Rev 3 does not say what it **is**. On the paths that reach a build, it is `pending` with a NULL hash: either a fresh upsert, or the `pending` reset at `:676`.
- The reconciler selects only rows with a real transaction hash (review 2 Q3; rev 3 §3.7.5 relies on R6 for NULL-hash rows, and R6 lives in F).
- Today the same row reaches terminal `failed` in about 15 s (two backoffs). Under F0 the exposure window grows to **2 h**, and restarts are routine: a deploy, or D 43rd's recreate tonight.
- So "can a row wait forever?" In-process, no. **Across a restart, yes:** `pending`, NULL hash, no timer, invisible to the reconciler, until a front-door call happens to arrive.

**Required change.**
1. **State the row's status during the wait** and make it durable: keep `pending`, and write `error_message = 'waiting for a spendable UTxO since <t>'`, which also bumps `updated_at`.
2. **F's reconciler** (or a boot sweep in F0) **selects `pending` rows with a NULL hash whose `updated_at` is older than the horizon plus a margin** and writes `failed`, guarded on `(pending, NULL)`, without minting. Ship F0 with F, as §14 already recommends, and make this cell part of F: (p6) restart mid-wait → the row ends `failed` after the horizon, with 0 submits.
3. **Measure the horizon from the first wait**, stored on the row, not from each re-queue. Otherwise a front-door re-POST (the upsert rewrites `updated_at`, `index.ts:1524`) restarts the clock without bound.
4. **Bound rule 4's "wait until that transaction confirms or dies"** the same way. A live claimant whose TTL lookup keeps erroring (a provider outage) otherwise keeps the family waiting indefinitely. After the horizon, rest the row for the reconciler.

---

## Item 4: "every submit refused = dead", for claim release only (§3.3): SOUND

**Checked that it really is liveness-only.** In rev 3, "dead" is used in three places:
- (a) **Releasing a refused transaction's ordinary inputs.** If that is wrong (the transaction actually sits in a mempool), another build picks an input that is already spent and is refused. That costs time, not a fee.
- (b) **Rule 2, letting other builds take `u_F` when no member is live.** If another build takes `u_F`, either it is refused (a member got there first) or it lands and consumes `u_F`, after which no member can land. Both outcomes are safe.
- (c) **The empty-candidate wait.** Liveness only.

None of these lets a member build without `u_F`. The only route that does is rule 4's closure, which rests on a **confirmed** spend or on TTL expiry, never on "refused" (subject to major A). The claim in §3.3 and §16.3 is accurate.

**INFO 1.** The per-hash `accepted`/`lost`/`refused` record is only as good as the HTTP layer's visibility. If the pinned `@blockfrost/blockfrost-js` (lock: 6.2.0, `anchoring/package-lock.json`) ever retries a POST internally, a "refused" reply can follow a hidden accept. My understanding is that the SDK's got-based retries do not cover POST by default, but **I did not read the SDK, so this is UNMEASURED.** It is safe either way under item 4's liveness-only use. Name it in §20.

---

## Item 5: the retry claim as a blob field, the revoked refusal, 409 for the loser (§6): SOUND WITH CHANGES

**What holds.**
- A compare-and-set in one UPDATE, under READ COMMITTED with WHERE re-evaluation, gives exactly one winner between two concurrent callers. The loser's 409 is correct.
- The revoked/deleted predicate is a pure narrowing. `revoked` is a real status (`documentRepo.ts:31`). `deleted` is used in SQL (`:621`, `:650`), not in the TS union. Fine.
- Not changing the blob's status means no reader meets a new state. Good.

### MAJOR D: the 10-minute expiry is shorter than anchoring's own in-flight horizon, so a reclaim can pay twice
- The claim expires after 10 minutes so that a crashed holder does not block forever. But the holder is not the only thing in flight. Once its POST has landed, **anchoring** owns the attempt. That attempt can legitimately stay unresolved for:
  - the ~27-minute guard-3 re-poll;
  - up to 2 h in the new `NoSpendableUtxo` wait (item 3);
  - up to the 2 h TTL while live.
- If the holder dies (or its step-4 write fails, which is plausible because originate writes are not retried) after the POST and before step 4, the blob stays `anchor_failed` with a stale claim.
- Ten minutes later a second caller claims it. Its own-create lookup (chain only) finds nothing, because the first attempt is still in flight. It POSTs.
- The upsert resets the row (`index.ts:1454-1465`) with a **new create payload** (a new `timestamp`, which is a new `createAttempts` entry), so it starts **a new family**. The first attempt's transaction and the second can both land: two fees.
- The same happens with no crash at all when the first attempt's step 4 wrote `anchor_failed` (a failed POST) but anchoring had in fact accepted it.

**Required change.**
- Before any POST, the claimant also reads **anchoring's row** for the document (the same tenant-checked read as `GET /api/anchors/:id`, or `own-create` extended). If that row is `pending`/`submitting`/`submitted` and newer than the claim, or carries a hash whose TTL has not passed, answer 409 or 202 with the existing anchor id, and **do not POST**.
- Or raise the expiry above anchoring's maximum in-flight horizon (TTL + re-poll + margin, about 2.5 h). That is cruder.
- **Cell (z6):** a holder crashes after its POST; 11 minutes later a second call; assert 0 additional POSTs while anchoring's row is in flight.

### MINOR 4: a crashed claimant wedges a document that had no blob
For a document with no blob, the claim writes `status: 'pending'` plus the claim (§6 step 1). The claim predicate admits only "blob absent **or** `anchor_failed`". If that holder crashes before its POST, the blob stays `pending` with no `anchorId` and a stale claim:
- no later claim can match;
- the poller has no `anchorId` to poll (its in-flight write needs a matching `anchorId`, §5.3);
- nothing moves it to `anchor_failed`.

The document can never be anchored through the route again. **Required change:** widen the predicate to "absent, or `anchor_failed`, **or** (`pending` AND no `anchorId` AND the claim is stale)". Pin it with (z7).

**Smaller points (fold into R):**
- The 503 "release the claim" write must be guarded on the token.
- Step 4 should clear `retryClaim`/`retryClaimedAt` explicitly.
- The resolver's whole-blob `confirmed` write (§5.3 sets `{blockchain}` to `$blob`) wipes a live claim. That is correct, because `confirmed` is terminal, but say so. In that case the holder's step 4 matches 0 rows **after** its POST: the lookup-then-POST race with a just-indexed create. That is a named residual, not a defect.

---

## Item 6: binding row 1 to the create (§5.2.2): SOUND WITH CHANGES

**What holds.** Before the flip, the document row carries event attempts (the upsert overwrites the payload, `index.ts:1502-1523`). An unbound "row `confirmed` → document `confirmed`" therefore attributes an event's transaction to the create. Binding row 1 to `createAttempts` or the legacy `anchoredAt` rule is the right narrowing. The conditional write never downgrades a `confirmed` blob (§5.3), so existing confirmed documents are untouched.

### MINOR 5: R needs a field that rev 3's PR plan puts in C, which needs migration 056
- §5.2.2: "This needs the anchor GET to return `payloadTimestamp`, which C adds."
- §14: R depends on "F; ideally after KS-1814", not C. C depends on A (056).
- BLUF 9 and §14 say "F0 → F → R … before any schema change".

These three cannot all hold. **Required change:** move `payloadTimestamp` on the GET (and the 202) into **F or R**. It is read from `metadata_payload`, and no column is needed. Or list C, and therefore A, as a dependency of R, and drop "before any schema change".

Also **state the outcome when a `confirmed` row is unbound and the own-create lookup answers "nothing"**. I read it as an in-flight blob going to `anchor_failed`, which is honest, but the design should say so. Name the kintsugi shape as the expected case.

---

## Item 7: nft-certificate shares the platform wallet (§3.6, D17): CONFIRMED at the pin; SOUND WITH CHANGES

**Confirmed (read at the pin):**
- `Blockchain/Dev/docker-compose.yml:1694` `PLATFORM_WALLET_MNEMONIC=${PLATFORM_WALLET_MNEMONIC:-}` lies inside the `nft-certificate:` service block (starting at `:1660`). It is the same variable anchoring gets (`:1311`), along with `BLOCKFROST_API_KEY` (`:1693`).
- The derivation is identical: m/1852'/1815'/0'/0/0 for payment and /2/0 for stake, a base address (`nft-certificate/src/cardano/wallet.ts:38-55` against `anchoring/src/cardano/wallet.ts:45-72`). **Same address.**
- **Readiness is automatic, not a separate setting.** `initCardanoNFT` sets `cardanoReady = true` when the key and mnemonic are present and protocol params fetch (`nft-certificate/src/cardano/index.ts:30-56`). It is called at boot with `CARDANO_NETWORK` (default `preprod`, `nft-certificate/src/server.ts:16`, `:49`).
- **The route is reachable on compose boxes.** The gateway sets `NFT_SERVICE_URL=http://nft-certificate:4018` (`docker-compose.yml:469`), so the "not deployed" short-circuit does not fire (`api-gateway/src/routes/proxy.ts:1184-1207`, `authenticateToken(false)`). The real path spends from its own `fetchUtxos` with no coordination (`nft-certificate/src/cardano/mintTransaction.ts:41`).
- By reading, then: **wherever a box runs this compose with real anchoring credentials, and `CARDANO_NETWORK` matches the Blockfrost key's network, nft-certificate is a live second spender.** The census still has to confirm per box. Rev 3's "UNMEASURED" is right as a box fact, but the prior should be "likely yes", not "unknown".

**Is F0 safe to deploy while the wallet is shared?**
- **For money (one payload, at most one fee): yes, once major A is fixed.** nft transactions carry CIP-25 metadata, not label 674 (`minting.service.ts:726-744`), so major A's payload check reads them as "different payload" and closure is correct. Any input nft takes is either refused (it conflicts with our live member) or consumes it, which only blocks our members.
- **For availability: not until major C is fixed.**

### MAJOR C: with a foreign spender, the add-back rule offers a dead output for up to 24 h
- §3.3: candidates = fetched − claimed **+ "every own output of a confirmed spender that the fetched view does not list and no claim covers"**. "The add-back set may shrink when a view lists the output."
- The add-back exists for replica lag: a fresh confirmed output that a stale replica has not indexed yet.
- But if nft-certificate (or thread-mint's lucid selection, or a KS-535 second deployment) **spends** that output, no view will ever list it again. The add-back never shrinks.
- It is our change output, typically the largest UTxO, so `LargestFirstMultiAsset` (`transaction.ts:96-99`) picks it first. Every build is refused with a bad-inputs ("All inputs are spent") reply. That goes through guard 3's ~27-minute re-poll, then retries, then terminal `failed`, for as long as the add-back lives. The text implies 24 h, the confirmed spender's window.
- This is the 1 ms stale-UTxO outage of §3.1, made **durable** by F0.

**Required change.**
- Bound the add-back to the replica-lag scale (for example 10 minutes from confirmation), not to the 24 h exclusion.
- **Drop an add-back output at once** when a build that included it is refused with a bad-inputs reply.
- Prefer fetched candidates over add-backs. An add-back is only needed when the wallet would otherwise be empty, so add a `CoinSelection` order or a two-pass build.
- **Cell (p7):** a foreign transaction spends our confirmed change output; assert that the next build does not use it after one refusal.

### MINOR 6: D17's interim ("keep its real-chain path off") has no switch
nft-certificate has no feature flag. Readiness follows the credentials (above). "Keep it off" therefore means removing `PLATFORM_WALLET_MNEMONIC` (or the key) from that service's environment on the box. That is a box config change, which is Kam-gated, and it must be stated as such. The card should say it, and so should D17 in §17. Alternatively, a build adds an explicit `NFT_REAL_CHAIN_ENABLED` flag.

**INFO 2.** §20's "whether `addressesUtxos` pages": in blockfrost-js 6.x, `addressesUtxos(address, pagination?)` returns one page (default count 100), and `addressesUtxosAll` walks the pages. That is from my knowledge of the SDK; I did not read it here. It matches §18.17. F0's "page explicitly" is right.

---

## The card (`CARD_TEXT_for_Kam.md`): partly accurate. Fix four things

**What is accurate:**
- the action-first BLUF;
- 1(b) named with the agreed wording;
- "MORE transactions land … one more fee per refused event";
- the cost and risk rows for steps 1-13 as rev 3 states them;
- **default (b) = build F only, F0 held for the census**, which matches rev 3's intent;
- "F moves no money". That is correct: R6 writes `failed` and never mints, and R8 is a separate Kam step.

**Fix:**
1. **"Two reviews have been through the design; … rev 3 fixes that."** That is not yet true of F0's mechanism, which changed after review 2. Replace it with: "Rev 3 changed F0's mechanism; a third review (this file) found it sound with four required changes, and the build brief carries them."
2. **Option (b) is not buildable as rev 3 states it.** §14 says F depends on F0 ("shares `anchorSubmission.ts`"), and F's guarded reconciler writes use the `expectStatus`/`expectTransactionHash` builder change that §3.7.2 puts in F0. Either F carries that builder change and is built on develop, with F0 rebasing later (say so on the card), or (b) is not a real option.
3. **Add, under "What F0 does":**
   - "Anchors may now wait up to 2 h for a spendable coin instead of failing, which Platform S will see as a longer pending";
   - and, until majors A/B are fixed, "the one-coin guarantee holds within one running process; a restart is covered only by the fixes in review 3".
   The current line "so at most one of them can ever land" is too absolute.
4. **Step 11 (D17):** add "until then, keeping nft-certificate off chain means removing the wallet from its config on each box, which is itself a box change for you". Note that by reading it is **likely already live** wherever anchoring is.

---

## TESTED / NOT TESTED
**TESTED (read, not run).** At `6d41673e0f79`, with `git show` into the session scratchpad and `git grep` in the cache clone:
- `anchoring/src/anchorSubmission.ts` (whole);
- `anchoring/src/cardano/transaction.ts:20-148`;
- `anchoring/src/cardano/index.ts:135-145`, `:200-305`;
- `anchoring/src/cardano/provider.ts:1-60`, `:100-145`, `:280-366`;
- `anchoring/src/anchorStatusUpdate.ts:60-118`;
- `anchoring/src/index.ts:1440-1530`, `:1689-1721`, `:1852-1877`;
- `anchoring/src/cardano/threadTokenMint.ts:240-345`;
- `anchoring/src/cardano/wallet.ts:40-75`;
- `nft-certificate/src/cardano/wallet.ts:25-65`, `nft-certificate/src/cardano/index.ts:18-70`, `nft-certificate/src/server.ts:14-30` and the `:49` grep hit, `mintTransaction.ts` (grep for UTxO, inputs and TTL), `minting.service.ts:700-760`;
- `Blockchain/Dev/docker-compose.yml:1300-1325`, `:469`, `:1660-1730`;
- `api-gateway/src/routes/proxy.ts:1170-1210`; `api-gateway/src/config/services.ts:165-172`;
- `originate/src/routes/documents.ts:1437-1475`; `originate/src/repositories/documentRepo.ts` (grep for status vocabulary and `preserveTerminalStatuses`);
- `anchoring/package.json`, `nft-certificate/package.json`, `anchoring/package-lock.json` (blockfrost-js entry).

**NOT TESTED / not read.**
- No cell, mutant, container, database, chain or box was run or touched. Every finding is an inference from code and from rev 3's text.
- **Not read:** the blockfrost-js and lucid-evolution sources (INFO 1 and 2 are from SDK knowledge, marked so); `reconciler.ts` and `confirmation.ts` (I relied on review 2's reading for the reconciler's NULL-hash exclusion and for mempool → 404); the batch path `index.ts:1960-2130`; `anchorStateSync.ts`; rev 2 and rev 1 (out of scope); sub-agents A, B and C's raw reports.
- **Box facts are UNMEASURED:** whether `CARDANO_NETWORK` matches the key on each box (which decides nft-certificate readiness), the UTxO count, the replica count, and whether any transaction has sat in a mempool for more than 27 minutes.
- Item 7's reachability is by reading only; no mint was exercised.

**Footprint.** Read-only everywhere. Writes: this file, and source extracts in the session scratchpad. No write under `!CODING`, no ticket, PR, branch, box, `az`, Docker or mail.
