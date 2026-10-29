# KS-1384 rev 4: fourth review, focused on §19 (F0's mechanism)

**Reviewer:** Wednesday's design-review sub-agent. Read-only. **Date:** 2026-10-30, 07:0x-07:4x AEDT.
**Design read:** `!CODING/Secuura/Blockchain/5_Project_History/2026-10-29_seatW-9th/KS-1384-per-event-anchor-DESIGN-rev4.md` (428 lines, read whole), plus `CARD_TEXT_for_Kam.md` and `HANDOVER.md` from the same folder.
**Code read at:** develop **`7152ac669d2d`** (`git ls-remote origin refs/heads/develop` at 07:0x and again at 07:15). Rev 4 was written against `6d41673e0f79`. Develop is now **15 commits ahead** of that pin. One of those commits changes F0/R's ground: **KS-1822 (#1813, `203734468`)** adds tenant gates to both anchor GETs. Every `anchoring/src/index.ts` line after :57 has moved by +2 to +8. All other cited files are unchanged.

---

## BLUF

1. **Build F0 with the listed fixes. Do not deploy it to any box where `STATE_THREAD_NFT_ENABLED=true` until fix B1 is in.** The core mechanism works: the shared family coin, the re-poll of the whole family, the boot arm, and A1. Within one anchoring process, two transactions carrying the same payload cannot both land.
2. **Blocker B1: rev 4 sends thread-mint through the wallet lock, which rev 4 itself holds for up to about 27 minutes.** originate calls thread-mint with no timeout and treats it as fire-and-forget. So originate gives up, and anchoring still signs and pays for the mint later. The result is a paid NFT with no registry row.
3. **Four majors.** Collateral is claimed for 24 h although a valid mint never spends it, which strands up to three of the largest coins. The thread-mint seed bypasses the view. Rule M3 leaves batch and thread-mint transactions out of the view. And since KS-1822, R's in-flight check cannot tell "no row" from "refused".
4. **F0 does stop the measured stuck-anchor shape (cause a) and same-payload double fees, both within one process.** For about 2 h 10 min after every boot it still rests refusals for 24 h, as the design says. A re-POST whose payload overwrite is admitted carries a new server timestamp (`anchorSchema.ts:337`), so it starts a new family and can still pay a second fee.

---

## Findings, ranked

### BLOCKER

**B1. Thread-mint inside `withWalletLock` turns a timed-out request into a paid, orphaned mint.**
- **§3.6 / §19.7 says:** "F0 does, for S3: it runs `mintAndLock` inside `withWalletLock`." Card line 5: "Thread-mint waits its turn for the wallet."
- **Code:**
  - The single-anchor path holds that lock through the whole confirmation poll (`anchorSubmission.ts:485-516`, `confirm` = `waitForConfirmation(tx, 30, 10_000, 60_000)`, `cardano/index.ts:290-296`, about 27 min).
  - originate calls thread-mint with a bare `fetch` that has no `signal` and no timeout (`originate/src/services/threadTokenClient.ts:66-81`).
  - The call is fire-and-forget at document create (`originate/src/routes/documents.ts:804-821`, gated on `STATE_THREAD_NFT_ENABLED === 'true'`).
  - The handler does not check that the client is still connected before it signs (`anchoring/src/index.ts:1060-1077`; `threadTokenMint.ts:337-339`).
- **Failing scenario:**
  1. An anchor holds the lock in its 27-minute poll.
  2. A document is created, and thread-mint queues behind the lock.
  3. Node's fetch gives up on headers after its default of about 300 s (undici; UNMEASURED on the box image, which is `node:24-alpine`). originate logs "thread-token mint failed" and writes no `state_thread_registry` row (`threadTokenClient.ts:84-88`).
  4. Anchoring's handler keeps running. When the lock frees, it signs and submits. The NFT is minted, the initial datum is locked at the script address, and the fee is paid.
  5. Nothing records it, and no retry is coming.

  The result is one lost fee plus an orphaned one-shot thread per document created while the lock is busy. If F0's no-candidates path makes thread-mint wait up to 2 h (§3.5), it hits the same timeout.
- **Fix (required in F0):**
  - Acquire the lock with a bounded wait, well under the caller's timeout, for example 30 s. If the wait expires, answer 503 *before signing*.
  - Never enter rule-4 or `NoSpendableUtxo` waits for thread-mint: no candidates → 503 at once.
  - Better still: check `req.socket.destroyed` / `res.writableEnded` immediately before `sign`.
  - Cell: hold the lock 6 min, call thread-mint, assert 0 submits and a 503.
  - **The census must read `STATE_THREAD_NFT_ENABLED`** (rev 4 §15 step 2 already lists it). On any box where it is `true`, F0 deploys only with this fix.

### MAJOR

**M-1. Collateral claimed for 24 h after confirmation strands up to three of the wallet's largest coins.**
- **§3.3 says:** the view records "its inputs, **its collateral inputs** (M1…)". A confirmed spender's inputs are "claimed for **24 h** from confirmation, whatever any fetched view says".
- **Code:**
  - lucid 0.4.34 picks collateral from `walletInputs` (= `presetWalletInputs` when non-empty) through `findCollateral` → `sortUTxOs` → up to 3 inputs (`dist/index.js:1899-1902`, `:1929-1934`, `:2318-2336`).
  - It also sets a **collateral return** (`:2311-2315`).
  - Local UPLC evaluation is on by default (`localUPLCEval = true`, `:1893`), so a submitted mint almost always passes phase 2. Collateral is then **not consumed**.
- **Failing scenario:** a valid thread-mint confirms. F0 treats its collateral like inputs and claims them for 24 h. Those are coins that still exist and are the largest in the wallet. Anchors then fall to pass 2 or to `NoSpendableUtxo`. On a wallet holding two or three coins (§15 step 12's case), every anchor waits up to 2 h and then fails, for 24 h after each mint. Nothing in the design releases them.

  The reverse also holds. If phase 2 ever fails, the collateral **is** spent and the regular inputs are **not**. The view then claims the wrong set, and offers a collateral-return add-back that does not exist (the 10-minute and drop-on-refusal rules bound that part).
- **Fix:**
  - Claim collateral only while the transaction is *live*.
  - At confirmation, read `valid_contract` from the `txs` answer:
    - valid → release the collateral and claim the inputs;
    - invalid → claim the collateral, release the inputs, and use the collateral-return output as the only add-back.
  - Cell (p8): a valid mint confirms → its collateral is offered to the next build.

**M-2. The thread-mint seed is picked from a fresh provider read, not from the view.**
- **§3.6 says:** "It passes `presetWalletInputs` = the view's candidates … claimed coins are excluded there too."
- **Code:** the seed is `lucid.utxosAt(walletAddr)` followed by the first UTxO of at least 5 ADA (`threadTokenMint.ts:262-264`). It is then forced in with `.collectFrom([seed])` (`:310`). `presetWalletInputs` governs only `complete()`'s own selection and the collateral (lucid `:1899`, `:1929`), never an explicit `collectFrom`.
- **Failing scenario:**
  1. A family member X is live: accepted, poll timed out, lock released.
  2. The provider still lists X's inputs, because mempool spends are not removed from `addresses/utxos`.
  3. thread-mint's seed is `u_F`, or another of X's inputs.
  4. The mint and X conflict. If the mint lands, X is knocked out and the anchor needs another 27-minute cycle.

  No anchor pays twice: the family closes on a non-674 spender. But the claim "claimed coins are excluded" is false for the one input thread-mint always spends.
- **Fix:** choose the seed from the view's pass-1 candidates (the first candidate of at least 5 ADA), and never from `utxosAt`. Cell: a claimed `u_F` is never the seed.

**M-3. M3's admission rule leaves batch and thread-mint transactions out of the view.**
- **§3.3 / M3 says:** "A transaction enters the view only after its write-ahead returned exactly 1." §3.6 says F0 "records the inputs and the collateral from the signed body before `submit()`" for thread-mint.
- **Code:**
  - Thread-mint has **no** database row and no write-ahead (`index.ts:1016-1095` runs no query).
  - The batch write-ahead writes **N** rows, one per anchor (`index.ts:2000-2012`).
  - The batch confirms **outside** the lock (`index.ts:2024+`, `waitForConfirmation(...).then`). That is exactly the premise §3.3 says fails, so the next single build reads a page that still lists the batch's inputs.
- **Failing scenario:** built literally, neither spender is ever claimed. The next anchor picks a batch input, or a thread-mint input, from a stale page. It is refused with "All inputs are spent". Cause (a) is reopened for those two spenders. This costs time, not fees, because the family pin holds.
- **Fix:** state the rule per spender:
  - single: count = 1;
  - batch: count = N, all N matched;
  - thread-mint: enters at signing, because no row exists.

  Cells for the batch and for thread-mint.

**M-4 (R, coupled to F0's deploy). Since KS-1822, step 4's in-flight read cannot tell "no row" from "refused".**
- **§6 step 4 / §19.3 says:** read anchoring's row through `GET /api/anchors/document/:documentId`. "404, `failed`, or `confirmed` → step 5" (POST).
- **Code (new since rev 4's pin):** the route now runs `mayReadAnchorRows` and answers a refusal with `ABSENT_DOCUMENT_ANCHORS_BODY`, which is byte-identical to "no rows" by design (`anchoring/src/index.ts:989-990`; `anchorReadGate.ts:26-33`, `:146-147`). originate forwards the end user's bearer (`documents.ts:1467-1475`). The gate's gap (vi) names the admin-override shape: originate resolves the document under `X-Tenant-Override`, while the token carries the admin's own tenant (`anchorReadGate.ts:47-52`).
- **Failing scenario:**
  1. An admin with a tenant claim retries tenant A's document while A's anchor is `submitting`.
  2. Step 4 gets a 404 and goes on to POST.
  3. Today the POST is refused, because `mayWriteAnchorRows` uses the identical decision table (`anchorOverwriteGuard.ts:535-583`, `index.ts:1436-1448`). So R writes `anchor_failed` on a document whose anchor is still in flight and will confirm. That is a wrong final state, not a fee.
  4. **The money-safety of step 4 now rests on the read gate and the write gate staying in lockstep.** Any later narrowing of one without the other (KS-1652's no-tenant hole, KS-1663/1695's organisation split) turns this into a POST while a row is in flight, which means two fees.
- **Fix:**
  - Step 4 must use a read whose refusal is distinguishable from absence. Options: a service-authenticated internal read, or originate passing the `anchorId` it already holds in the blob to `GET /api/anchors/:id` under a service identity.
  - Treat an ambiguous 404 as 503, not as "absent".
  - Cell (z9): a gate refusal makes 0 POSTs.
  - **Also: rev 4 §18.21 is now KS-1822, merged.** Its §5.4 correction and the R plan should cite it.

### MINOR

**m-1. Rule 4 has no branch for "`u_F` listed, but claimed by our own *confirmed* non-member".**
- **Where:** §3.4 rule 4 bullets 2-4.
- **Reachable:** a family's members are all refused, so `u_F` is released (§3.3, "dead → released at once"). `u_F` is the largest coin, so the next anchor Z selects it (LargestFirst, `transaction.ts:96-99`). Z confirms while the family is in its 27-minute re-poll. The retry then reads a lagging page that still lists `u_F`, now claimed by confirmed Z.
- **Fix:** route this case to the "spender is our own confirmed non-member → close" branch. Never wait on it, because a confirmed claim never "confirms or dies".

**m-2. The boot arm's preconditions should be written down and pinned.** Its argument checks out against the code:
- TTL = `protocolParams.slot + 7200` (`transaction.ts:101-104`);
- the slot comes from `blocksLatest()` inside `fetchProtocolParams` (`provider.ts:303-304`, `:318`);
- the slot is cached for 5 min and kept when a refresh fails (`cardano/index.ts:30`, `:136-143`).

Three conditions it relies on are not stated:
- (a) **`S_boot` must be a positive slot from an answered read.** `fetchProtocolParams` writes `slot: tip.slot || 0` (`provider.ts:318`). A builder reusing that would set `S_boot = 0`, and 1(b) would arm at boot. Cell: a tip read with slot 0 or null never sets `S_boot`.
- (b) **The old container must be stopped before the new one's first tip read.** An overlapping old process can sign with TTL > `S_boot + 7200`. The 600-slot margin absorbs up to about 10 min of overlap minus replica lag. The census or runbook should say "recreate, no overlap".
- (c) **The arm must reuse the builder's 7200 constant**, not a copy of it.

**m-3. F-b's R6 runs at boot, and the driving set it checks is process-local.**
- **Code:** the reconciler runs once immediately at listen time (`index.ts:2233`) and then on an interval (`:2234`).
- **Scenario:** during any deploy overlap, the new process's R6 can write `failed` on a NULL-hash row that the old process still has queued in the lock for more than 10 minutes. The old process then builds against a `failed` row (guard 2 reads `failed` as no known submission, `anchorSubmission.ts:244-251`).
- **Fix:** the same "no overlap" precondition as m-2(b). Optionally, R6 skips rows for the first 10 minutes after boot.

**m-4. The in-lock `confirmed` write should expect `status IN ('submitting','submitted')`, not only `submitted`.** The `submitted` write can fail silently (it is swallowed today, `index.ts:1697-1729`; F-a returns `null`). The row then stays (`submitting`, X), the confirmed write matches 0, and F0 must not read that 0 as "a newer call owns the row". It is safe as written, because R4 confirms the row later, but it adds at least 10 minutes and an extra warning line.

**m-5. Waits and the lock.** §3.4 bullet 3 and §3.5 do not say whether the 2 h `NoSpendableUtxo` wait and the rule-4 wait hold `withWalletLock`. If they do, one document blocks the wallet for 2 h. **State that waits run outside the lock and re-queue.**

**m-6. `consumed_by_tx = null` must read as unknown.** In blockfrost-js 6.2.0's types (`@blockfrost/openapi` 0.1.92, `generated-types.d.ts:9181`), the field is optional and "null for unconsumed UTXOs". When the fetched view no longer lists `u_F` but `txsUtxos` says null, the two replicas disagree, so the row should rest. That is consistent with §3.4's "any read that fails → rest", but name null explicitly.

**m-7. The card's "one anchor" is really "one payload", and the payload carries a server timestamp.**
- **Code:** `buildFlatAnchorMetadataPayload` stamps `timestamp: new Date().toISOString()` on every POST (`anchorSchema.ts:337`). The upsert takes the new payload only when the KS-1385 guard admits it (`index.ts:~1501-1525`).
- **Scenario:** with the overwrite admitted, a re-POST of the same S event mid-flight starts a new family. X and Y have no shared coin, and both land: two fees, in one process. That matches today's behaviour and §3.9 ("more transactions land"), but card line 1 ("Every transaction we sign for one anchor spends one shared coin … at most one of them can land") reads stronger than the code.
- **Suggested card wording:** "for one request's payload".

**m-8. When `u_F` is refused while still listed, look it up before rebuilding.** Bullet 2 ("listed and unclaimed: spend it") on a lagging page can spend 27-minute cycles × 3 retries on a `u_F` that a foreign spender (nft-certificate, LargestFirst from a fresh page, `nft-certificate/src/cardano/mintTransaction.ts:41`, `:108-111`) already consumed. A cheap `consumed_by_tx` lookup after a refusal that named `u_F` avoids that. This is liveness only.

**m-9. Build note: drop `u_F` from the CSL candidate set.** `add_regular_input(u_F)` must be followed by `add_inputs_from(candidates − u_F)`. CSL may otherwise select it twice.

### Settled by this review (were UNMEASURED in rev 4 §20)
- **blockfrost-js 6.2.0**, the version that ships (`anchoring/package-lock.json`: `node_modules/@blockfrost/blockfrost-js` 6.2.0):
  - got's retry `methods` exclude POST (`lib/utils/index.js:48`);
  - `txSubmit` is a POST (`lib/endpoints/api/txs/index.js:256`);
  - `addressesUtxosAll` paginates, and an options object without `batchSize` falls back to `DEFAULT_PAGINATION_PAGE_COUNT` (`lib/utils/index.js:122-133`).
  
  Rev 4's INFO 1 and 2 hold at 6.2.0.
- **lucid 0.4.34** (`package-lock` pins 0.4.34): a non-empty `presetWalletInputs` replaces `wallet.getUtxos()`, and collateral is drawn from it (`dist/index.js:1897-1902`, `:1929-1933`). Rev 4's §3.6 statement is confirmed, apart from M-1 and M-2 above.

---

## Each §19 item: verdict

| §19 item | Verdict | Checked against |
|---|---|---|
| 1. Slot-counted boot arm | **Sound**, with m-2's three preconditions | `transaction.ts:101-104`; `provider.ts:303-304`, `:318`; `cardano/index.ts:30`, `:136-143`; the upsert nulls the hash, `index.ts:1463-1464` (was `:1455-1456`) |
| 2. B corrected (path ii keeps its hash), wait marker, driving set | **Correct.** The reset writes `{status:'pending'}` only (`anchorSubmission.ts:676`); the builder sets only the fields given (`anchorStatusUpdate.ts:79-101`); the reconciler selects pending rows with a hash (`reconciler.ts:73-74`). See m-3 for boot-time R6 | as cited |
| 3. D refuses an in-flight row of any age | **Sound in intent; broken instrument since KS-1822** (M-4) | `index.ts:989-990`; `anchorReadGate.ts` |
| 4. In-lock `confirmed` names its hash; view-first check on every build | **Correct.** The write today carries no hash, only `expectMetadataPayload` (`anchorSubmission.ts:491-504`), so a same-payload upsert leaves it `confirmed` with a NULL hash, as §18.20 says. See m-4 | as cited |
| 5. F split; F0 + F-b + R deploy together | **Right.** Add M-4's fix to R and B1's condition to the census | — |
| 6. q6's assertion (rest inside the window) | **Correct.** Note that R4's encode-equal adopt (r5) confirms with X only when the overwrite was declined; otherwise X is a different event and the row fails at 24 h, which is honest | `anchorSchema.ts:337`; upsert CASE |
| 7. Thread-mint `presetWalletInputs`, never empty | **Incomplete.** The seed bypasses it (M-2), collateral is mis-claimed (M-1), it never enters the view (M-3), and the lock wait orphans fees (B1) | `threadTokenMint.ts:262-264`, `:310`, `:337-339`; lucid as above |
| 8. Two-pass build | **Sound** | — |

## The questions asked

**Does F0 do what it claims?**
- **Double fees:** yes, for one payload within one process. Every member spends `u_F`. Rule 4 never builds while a member is live; it waits, bounded by the horizon, and each member's TTL ends before `t0` + 2 h. A1 covers pre-restart spenders after the window.
- **Stuck anchors:** yes for cause (a) within a process. For cause (b) only after the boot arm. Inside each 2 h 10 min window a refusal rests 24 h and then fails, exactly as today.

**Can it double-spend?** Not through anything in §19, given one anchoring process.
- *Remaining paths:* a second process (census), a deploy overlap (m-2b, m-3), and a re-POST with the overwrite admitted (m-7).
- *Through R:* M-4.

**Can it lose a fee?** Yes, through B1 (thread-mint). Otherwise only the KS-1385 decline, which is honest and pre-existing.

**Can it strand a UTxO?** Yes: M-1 (collateral, 24 h). `u_F` claims are bounded by TTL, and add-backs by 10 minutes.

**Can it race a concurrent pass or thread-mint (KS-1819)?**
- *Single path:* serialised by the lock. The guard-3 re-poll runs outside the lock, but any build after it must spend `u_F`, so a member landing mid-gap is caught.
- *Thread-mint:* B1, M-2 and M-3.
- **KS-1819 (any authenticated caller can mint) should land before F0 deploys.** Once thread-mint queues on the wallet lock, an unauthorised caller can also stall every anchor behind queued mints (KS-1819, read on Linear: Backlog, 0 comments).

**Can it leave a row non-final?** No, with F-a and F-b:
- path (i) → R6 at `t0` + 2 h 15 min;
- path (ii), and rows resting on a hash → R4 at 24 h on `updated_at`;
- a timer lost in a restart → R4 or R6.

The rule-4 "rest the row; it carries a real hash" line is wrong for a front-door rebuild, where the upsert left the hash NULL. R6 still ends that row, so it is a wording fix only.

**Failure and restart:** the view, the families, `t0`, the driving set, the add-backs and the arm are all in memory, and all reset on restart. The design's account of each loss is correct against the code (above). Add m-2(b) and m-3's overlap rule.

**Preconditions: anchor_store has no RLS and no tenant column.**
- F0 and F-b do not depend on tenancy. The family, view, R4 and R6 are wallet-level and payload-level, which is correct.
- R depends on tenancy twice:
  - step 4's read: M-4;
  - §5.4's own-create authorisation through `mayWriteAnchorRows`, which fails open on an absent tenant claim and on a probe fault (`anchorOverwriteGuard.ts:540-561`). Acceptable only because originate's `getDocument(id, tenantId)` (`documents.ts:1449`) is the real boundary, and R should say so.
- Flat anchors from two tenants with the same S document id still collide on one row (KS-1822 gap (i)). F0 neither relies on that nor fixes it.

## What F-a, F-b and R must carry
- **F-a:** `updateStatus` returns a count or `null`, so that F0's m-4 can tell "matched 0" from "failed". No other change.
- **F0:** B1, M-1, M-2, M-3, m-1, m-2 (a and c), m-4, m-5, m-6, m-8 and m-9, with their cells (the B1 6-minute lock cell, p8, the seed cell, the batch and thread-mint view cells, and the `S_boot` = 0 cell).
- **F-b:** m-3, either a boot grace or the documented no-overlap rule. R6's adopt scan must use the same encode path as A1.
- **R:** M-4, with cell (z9). Cite KS-1822 in place of §18.21. State that originate's tenant-scoped `getDocument` is the authorisation boundary for own-create.
- **Census / deploy card:**
  - one anchoring replica;
  - **no container overlap at recreate**;
  - read `STATE_THREAD_NFT_ENABLED` (if true, B1 must be in);
  - KS-1819 merged before F0 deploys.

---

## FOUND / TESTED / HOW
- **FOUND:** every finding above, by reading code at develop `7152ac669d2d`. I made a `git clone --shared --no-checkout` into `scratchpad/ks1384rev/repo` (toplevel asserted), ran `git show` on 16 files into `scratchpad/ks1384rev/src/` (rc 0 each), and used `sed -n` / `grep -n` on the extracts. The pin-versus-develop diff came from `git diff --stat 6d41673e 7152ac66` and `git diff` on `anchoring/src/index.ts`. The index.ts line shifts were spot-checked at nine lines on both SHAs.
- **SDKs:** I ran `npm pack --ignore-scripts` for `@blockfrost/blockfrost-js@6.2.0`, `@blockfrost/openapi@0.1.92` and `@lucid-evolution/lucid@0.4.34`, each into its own scratch directory, and only read them; nothing was executed. Versions came from `anchoring/package-lock.json` at develop.
- **Linear:** a read-only GraphQL query with the key sourced in a subshell (`set -a`), never printed. KS-1384 has 7 comments, the last `ea44c3ff`, so nothing has been added since rev 4. KS-1819 is in Backlog with 0 comments.
- **TESTED:** nothing was executed. No container, test, box, `az`, `psql` or POST.
- **UNMEASURED, with the instrument that would close each:**
  - Node 24's undici `fetch` headers timeout on the originate image (B1's 300 s): read `undici` `Agent` defaults in the image, or run the B1 cell.
  - Whether `STATE_THREAD_NFT_ENABLED` is true on kintsugi or demo: the census.
  - CSL `add_inputs_from` behaviour when an input was already added (m-9): a unit cell in F0.
  - How often phase-2-invalid mints occur (M-1's reverse case): Blockfrost `txs.valid_contract` on past mint hashes.
  - Deploy overlap at recreate on the boxes (m-2b, m-3): the census reads the compose or runbook stop order.
  - Replica lag below 600 slots: carried from rev 4 §20.
