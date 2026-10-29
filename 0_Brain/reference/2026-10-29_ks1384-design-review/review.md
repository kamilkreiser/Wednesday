# KS-1384 per-event anchor design: independent review

**Reviewer:** an independent read-only reviewer for Wednesday, 2026-10-29 (~05:3xZ, 16:3x AEDT).
**Reviewed:** `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-10-29_seatW-6th/KS-1384-per-event-anchor-DESIGN.md` (579 lines) and its `HANDOVER.md`. Also read: the brief (`/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-10-29_seatW_ks1384_per_event_design.md`) and Seat T 6th's folder (`.../5_Project_History/2026-10-29_seatT-6th/`: `evidence/a1a5_*`, `a1b_meta_*`, `a2_koios_*` (3), `b3caller_*`, `reread_TOOLTEST_*`, `rev_*`, and `mail/04_measured_body.txt`, `06_ANSWER_measured.txt`).
**Code:** pin `e4cd2e1325bacbe1fd39e549f8aaefc943485d12`. Read only with `git show` / `git grep` / `git ls-tree` / `git diff --stat` in Wednesday's cache clone. Paths below are under `Blockchain/Dev/services/` unless stated otherwise.

---

## BLUF

**Verdict: SOUND WITH CHANGES.** The data model is right: one row per event, an `eventId` key, replay-safe event rows, document rows that keep today's behaviour until PR H, reads that put the document row first, and rollback by flag. It removes the coalescing and the false attribution. **It does not remove the "never settles" half of Stuart's report.** Kam should not approve it until finding 1 is added and findings 2 and 3 are fixed.

**Top 3 issues**
1. **(BLOCKER) The design's root cause is incomplete, and per-event mode would make the rest of it more common.** The second transaction was refused because it spent an input that `b1cc72f9` had already spent. The wallet lock was released when that transaction confirmed. The next build started 1 ms later and read a stale UTxO set. The refusal path then leaves the row in `submitting` instead of retrying, because the node's real "inputs spent" text also contains "already been included" (`anchoring/src/anchorSubmission.ts:29-30`, `:112-117`, `:637-641`). Under per-event rows, a share and a transfer queue behind the upload's confirmation in exactly the same way (here they were 48 ms apart), so both event rows can rest for 24 h and then fail. **Nothing in PRs A-H changes this.**
2. **(MAJOR) "A Kam card per box" is not achievable for 057 and 058 as designed.** The compose `migrations` service and the api-gateway stage-1 runner apply every file in `migrations/` on every deploy. A RAISE in either file fails the runner with exit 3, and then anchoring, originate and the gateway do not start (they depend on `service_completed_successfully`).
3. **(MAJOR) The adopt-or-fail rule R6 can never adopt.** It compares the `fromCardanoMetadatum`-decoded on-chain payload with the typed stored payload. That decoder keeps booleans as the strings `"true"`/`"false"`, and it was the encoder that split long strings into chunks. So any payload with identity fields never compares equal, and R6 writes `failed` even when the transaction is on chain.

---

## Findings

### 1. BLOCKER: The row stuck because of a stale UTxO set and a refusal path that rests. Per-event rows keep both.
**Evidence (code at the pin, plus T's measured fields):**
- **The lock's premise.** `anchorSubmission.ts:417-424` and `:485-486` assume that once a transaction confirms, "the next anchor waiting on the lock will then read UTxOs that reflect this tx". The build reads UTxOs with `fetchUtxos(wallet.address)` (`anchoring/src/cardano/transaction.ts:29`), and that view is the provider's.
- **The timeline (T, `04_measured_body.txt` A3):** `Anchor confirmed` and the KS-1385 decline at 08:56:10.146; a second `Submitting` at .147; `Node REFUSED` at .627; re-polls at .631 and .633.
- **The wallet (T, `a2_koios_wallet_*`):** no wallet transaction between `b1cc72f9` (08:55:48Z) and the control's `43549e9a` (08:57:39Z). So the only transaction that could have spent the refused transaction's input is our own `b1cc72f9`.
- **Which branch rested the row.** The design calls this UNMEASURED (§2.4 item 4, §15). The code narrows it to one exit:
  - The REFUSED line is the first arm of guard 5 (`:584-590`), which falls through.
  - Had the error not matched `isAlreadySubmittedError` (`:120-124`), the path would have written `failed` and bumped `retry_count` (`:654-660`, `index.ts:1874`). T measured `retry_count=0` and `error_message=NULL` (`a1a5_*`).
  - The lost-reply arm (`:591-614`) writes an `errorMessage`. The NULL rules it out.
  - What is left is guard 3 returning at `:641` (`if (!refusedAndAbsent) return;`), with the row in `submitting` holding the refused hash.
- **The likely cause, inferred from code and not measured (the log text was cut):** `ALREADY_INCLUDED_REPLY = /already been included/i` (`:112`) matches the node text the same file quotes as observed (`:29-30`: `"All inputs are spent. Transaction has probably already been included…"`). So `refusedAndAbsent` (`:637-640`) is false whatever the 27-minute re-poll finds. The ordinary retry ruled on 2026-09-14 cannot be reached for the measured message.
- **Under event mode the same sequence follows:** the create row confirms, then E1 (share) takes the lock 1 ms later, reads stale UTxOs, is refused and rests. E2 (transfer) follows the same way. The design's R4 fails each of them only after 24 h. The proof for those events is lost, and the cost is still one fee for the upload.

**Fix (add as a PR, and require it before the flip):**
- (a) Never build on an input that the last submitted transaction spent. Either record the spent outpoints in the process and exclude them for the length of the provider's lag, or chain from the confirmed transaction's change output, or after confirmation wait until `fetchUtxos` no longer lists the spent inputs.
- (b) Make the "inputs spent + re-poll answered absent" case reachable. A refused transaction whose inputs were consumed by a *different*, known, own transaction can never land, so retrying it cannot double-mint. This edits behaviour Kam ruled under KS-1171 and resubmits (money), so it is a **Kam card**.
- (c) Add a cell: two events queued behind one confirmation, with a fake provider whose UTxO view lags N seconds. Mutant: remove the input exclusion; the cell must go red.
- **KS-535 still binds the fix.** Any UTxO or wallet change stays one mnemonic per deployment. Splitting UTxOs inside the deployment's own wallet is fine; a second deployment sharing a wallet is never the fix.

### 2. MAJOR: Migrations auto-apply on deploy, so a "per-box Kam card" for 057/058 is illusory, and a RAISE takes the stack down
**Evidence:**
- `Blockchain/Dev/scripts/run-migrations.sh:112-135` applies every `migrations/*.sql` not yet in `_secuura_migrations`. Any failure ends in `exit 3` (tail of the file).
- `Blockchain/Dev/docker-compose.yml:1335-1336` (anchoring), and `:545`, `:667`, `:710`, `:841`, `:904`, `:959`, `:1022`, all `condition: service_completed_successfully`.
- api-gateway also applies the same files (`api-gateway/src/startup-migrations.ts:148`).
- T's `rev_*` shows both boxes take develop under the standing October deploy grant.

**Consequences:**
- (a) Merging B means 057 runs on both boxes at the next routine deploy. Merging D means 058 does. The design's table says B is "apply per box" and that the flip waits for D "applied on the box". Neither can be done per box.
- (b) 057's "refuses unless superuser/BYPASSRLS", or 058's RAISE, fails the runner, and every dependent service stays down. That outage is far worse than the defect.
- (c) Deploys measured on 28 Oct recreated only api-gateway and originate (Stuart, quoted in the brief; T's `rev_*`). The migrations service drops the index while an un-recreated anchoring still names `ON CONFLICT (document_id, network)`, and every anchor then fails with 42P10 until anchoring restarts. 058's precondition 1, "PR C deployed on that box", is not proved by a SHA.

**Fix:**
- Keep 057 and 058 out of `migrations/`: put them in a one-off script folder run by a Kam-approved seat on one box. Or make each one no-op with a NOTICE when its preconditions fail; never RAISE.
- 058's precondition must read the running anchoring's boot-check state (§6.1, row 3) on that box, not the merged SHA.
- Say plainly in §11 that a merge is an apply on both boxes.

### 3. MAJOR: R6 payload equality is specified on the decode side and cannot match
**Evidence:**
- `anchoring/src/cardano/cardanoMetadatum.ts:4-25` (the 64-byte chunking, and booleans written as the strings "true"/"false"). At `:77-78`, `fromCardanoMetadatum`: "Booleans stay as "true"/"false" here; anchorReadback.ts types them by key".
- T's `a2_koios_b1cc72f9_*` shows `orgVerified = "true"`, `actorVerified = "true"` and `identityCommitment = list len 2`.
- The stored `metadata_payload` is the logical, typed form (`:16`).
- The design's R6 (§7) says to decode with `fromCardanoMetadatum` and then "require the decoded payload to equal `metadata_payload`". For every KS-1175 identity payload that is false, so R6 writes `failed` on the crash-after-signing case it claims to cover (§7, "Not closed" item 2).

**Fix:** compare on the encoded side: `deepEqual(toCardanoMetadatum(metadata_payload), onChainJsonMetadata['674'])`. Cell (j) needs a positive control that adopts a reconstructed create payload against `b1cc72f9`'s real metadata, and a negative control (the share payload) that is refused.

### 4. MAJOR: D9 ("let it fail, do not repoint") is sound at its core, but its knock-on effects are not covered
**Not repointing is right.** S's rows 108 and 109 would be stamped with the upload's transaction.

What D9 leaves out:
- **S's upload row 107 also reads `failed`.** S polls it by the K document id, and `GET /api/anchors/:id` falls back to `dbGetAnchorsByDocument(id)[0]` (`anchoring/src/index.ts:912-914`). That is this same row. §7.1 names only 108 and 109.
- **The failure reaches the document.** Originate's state sync turns a `failed` anchor into `blockchain.status = 'anchor_failed'` on the document (`originate/src/services/anchorStateSync.ts:283`, `:343-370`).
- **That re-opens the retry route.** `POST /api/documents/:id/anchor` (`originate/src/routes/documents.ts:1458`) is allowed once the document reads `anchor_failed`. It re-POSTs on the `document` key, and today's reset on the **same id `anchor_c09c1b1f`** (`index.ts:1454-1465`) then mints a new fee-paying transaction:
  - for an upload that is already on chain;
  - recorded on the id S attributes to its share and transfer.

  That is the false attribution D9 exists to avoid. Whether S or K's UI triggers that retry automatically is unmeasured.
- **Nothing ever ties `b1cc72f9` to the upload inside K.** Recording it "in the ticket" is the only record the design leaves.

**Fix (add to D9, Kam's call):**
- (a) Until per-event mode is live, hold any retry for document `deb6d3c3…`: a comms line to Stuart, and a check of K's UI.
- (b) Once 056 exists, offer Kam an optional one-off repair, each step a card:
  - re-key `anchor_c09c1b1f` to an event key, so it stays `failed` for 108 and 109, which is true;
  - insert a document row that adopts `b1cc72f9`, after an encode-side equality check against the reconstructed create payload, so the upload reads confirmed, which is also true.

### 5. MAJOR: The heal narrowing (PR E2) together with D6 disables the stale-pending heal for any document that has a confirmed event
**Evidence:**
- `originate/src/routes/verification.ts:438-465`: the heal calls verify-by-hash, which returns ONE row, the latest confirmed (`anchoring/src/index.ts:663-665`).
- With per-event rows, that row is usually an event row. Once E2 requires `chain.anchorId === blob.anchorId`, the document blob's anchor id never matches, and `sameTx` is false, so the blob is never healed.
- The design's §5 fixes the false attribution but leaves no heal.

**Fix:** heal by the blob's own anchor, with `GET /api/anchors/{blob.anchorId}`, which is already the `anchorStateSync` pattern. Keep verify-by-hash for display only. Add a cell: a stale-pending blob with a newer confirmed event row heals to its own document row.

### 6. MAJOR: The design contradicts itself on S's `eventId`, and the prefixed key can exceed its own cap
**The contradiction.**
- §3.2 says the ask to Stuart is "material, not optional".
- §8 says "It is not needed, because originate supplies the key".
- BLUF line 3 says "S changes no code".

Under D1's default, every S re-send of a verb writes a new `custody_events` row, so it gets a new event key and pays a new fee. KS-1402 measured seven re-sends in six minutes (T's `b3caller_*`).

**The cap.** `transfer-custody:` is 17 characters. A caller `eventId` of up to 128 characters gives a 145-character key, against the 128 cap in §3.2. Anchoring answers 400, and the emitter degrades to `anchorId: null` (`documents.ts:1416-1430`). S then re-sends the verb on every tick.

**Fix:**
- Cap the caller `eventId` at 128 minus the longest prefix, or hash it (`<verb>:<sha256-hex[:32]>`).
- State in the BLUF that without S's id, every S retry costs one fee.
- Make the Stuart ask a precondition of the flip, or dedupe in originate.

### 7. MINOR: The give-up time is stated as a fact, and R4's "two consecutive passes" needs state that is not designed
- **The time.** BLUF line 2 says the row "turns to `failed` at 08:55:38Z". That is a prediction. On T's log the passes run at hh:m1:14 and hh:m6:14 (`reread_*`), so the first eligible pass is about 08:56:14Z.
- **The state.** R4 gives up only after two answered "not found" passes in a row. That needs per-row state that survives across passes, and across restarts if it is meant to hold. Neither a column nor an in-memory map is specified.
- **Fix:** say "the first pass after"; specify where R4's pass count lives.

### 8. MINOR: The replayed 202 still returns the new request's `createdAt`
`anchoring/src/index.ts:577` returns `anchor.createdAt`, the new object's, not the stored row's. §4.2 makes `status` honest but leaves this. **Fix:** return the stored row's `created_at` beside its `status`.

### 9. MINOR: §8's contract table is incomplete
Changes that are not listed there:
- `anchorId` and `eventKey` added to the verify-by-hash response (§5);
- `/api/anchors/document/{id}` now returning more than one row for one document, which changes the array's length and not only its fields;
- the published OpenAPI regeneration (§11 C);
- the public verifier's answer becoming the latest event's identity (D6, risk 6).

**Fix:** list them all in §8, so the comms to Stuart are complete.

### 10. MINOR: The batch route stays on the `document` key in event mode
The batch loop goes through `dbPersistAnchor` (`index.ts:856`), so the reset and the §13.1 defect survive the flip. **Fix:** say that batch is out of scope for event rows, and fence it until §13.1 is fixed. D2 already defers batching.

### 11. MINOR: On chain, an event transaction looks the same as an upload
The design adds no verb on chain (§3.2). Each event transaction carries `type: document` with the same `documentId` and `hash` (T's `a2_koios_b1cc72f9_*`). The chain-scan verifier (`index.ts:693-759`) then meets several transactions per hash, and which one it returns is unmeasured. Stuart's "every event is anchored" wording is true off chain only. **Fix:** say this in §8 and in the comms.

### 12. MINOR: §13.2 understates originate's `saveAnchorToDb`
Besides the anchor id written into `transaction_hash`, it also overwrites `content_hash` (`originate/src/routes/anchors.ts:128`). KS-1385 MAJ-2 relies on `content_hash` never changing (`index.ts:1488-1491`). PR E1 removes the write, so the impact is limited to the time before E1.

### 13. MINOR: `custody_events.anchored_tx_hash` is never filled
T measured it NULL (`b2diag`, per the design's §2.4). Event rows confirm, but nothing writes the hash back. This is pre-existing. **Fix:** name it as out of scope or add it to E2.

### 14. INFO: The code that ran at the incident is the pin
Kintsugi ran `bd6697e079fc` from 2026-10-28 06:08:44Z (T, `rev_*`). `git diff --stat bd6697e079fc 5dccdcb29ec2` over `services/anchoring`, `originate/src/routes/documents.ts` and `originate/src/routes/anchors.ts` is empty, and `5dccdcb2..e4cd2e13` touches only `originate/src/routes/adminConfig.ts` in code. So the design's causal reading is against the code that actually ran. The design never says so; it should.

### 15. INFO: The §13 findings are real (verified at the pin)
- **13.1, the batch route.** `index.ts:820` mints `anchor_<uuid>_<i>`, `:848` pushes it, and `:856` discards `dbPersistAnchor`'s return. `processBatchAnchor` updates only the minted ids (`:2001`, `:2012`, `:2023`, `:2060`, `:2081`, `:2094`, `:2110`, `:2122`), and the 202 lists them (`:871-875`). On a conflict, the upsert's unconditional SET (`:1455-1465`) resets the existing row. **Confirmed, read only.** Also, `:1967` reads `anchorIds[0]` back by id, which on a conflict names no row. What happens next was not traced.
- **13.2, the anchor id in `transaction_hash`.** `originate/src/routes/anchors.ts:336` and `:436` set `transactionId` to anchoring's `data.id` or `req_<hex>`. `saveAnchorToDb` (`:111-132`) writes it, plus `confirmed_at`, on `ON CONFLICT (document_id, network)` (`:125`). The stored network defaults to `'preview'` (`:256`); the forwarded one is `CARDANO_NETWORK || 'preprod'` (`:293`). The gateway sends `/api/anchors` and `/api/anchoring` to anchoring (`api-gateway/src/routes/proxy.ts:898-919`). **Confirmed.** See finding 12 for the extra column.
- **13.3, the CORE DDL.** `api-gateway/src/startup-migrations.ts:343-349` declares 11 columns (`tx_hash`, `metadata`, no `transaction_hash`) and is applied to tenant databases under `MULTI_TENANCY_ENABLED === 'true'` (`:1235`, `:1263`). **Confirmed.** Which boxes set that flag is unmeasured.

### 16. INFO: The design's other causal claims, verified at the pin
- `index.ts`:
  - `:489` mints a fresh id; the row is built `pending` with no hash (`:496-509`).
  - `:517` persists; `:564` calls `processAnchor` unconditionally; `:574` returns the status as `pending`.
  - The upsert SET is at `:1454-1465`, and the KS-1385 CASE at `:1502-1523`.
  - `:1660` orders `created_at DESC`, and `:914` takes `[0]`.
  - Verify-by-hash: `:663-665`. `POST /verify` with no ORDER BY: `:1185`. Lookup by transaction: `:1672`.
  - The retry is a `setTimeout`: `:1877`. Reconciler wiring: `:2186-2201` and `:2217-2230`.
- `reconciler.ts`:
  - The SELECT (`:65-80`) needs a non-NULL hash, so a NULL-hash row is invisible.
  - The verdict branches on `confirmation.confirmed` only (`:86-105`).
  - `checkTx` is `waitForConfirmation(tx, 1, 0, 0)` (`index.ts:2192`), which catches provider errors itself (`cardano/confirmation.ts:98-103`). **T's F2 holds.**
- `anchorSubmission.ts`:
  - guards 1 and 2: `:383-388`, `:425-432`; `knownChainSubmission`: `:244-251`;
  - the KS-1171 gate: `:314-346`; no restart re-queue: `:670-672`;
  - two processes is an open gap: `:53-57`; the KS-705 header: `:11-33`.
- `anchorStatusUpdate.ts`: the compare-and-set at `:44-60` and `:107-111`. Its own comment (`:51-58`) accepts "two genuinely different events produce two transactions". That fits the design's §2.2.
- `originate/src/routes/documents.ts`:
  - the emitter: `:1363-1431`; it degrades to null: `:1423-1430`;
  - the custody `eventId`: `:2126-2128`; the share loop: `:2574-2595`;
  - the emitter calls: `:2193`, `:2612`; the retry route's gate: `:1458`.
- `anchorSchema.ts:159` uses zod's default strip, so originate's `eventId` is safe to send ahead of PR C. The design's mixed-version claim in risk 3 holds.
- `provenance.ts:65` writes `rec.tenantId || DEFAULT_TENANT_ID`, so rule 3a is right not to trust `action_provenance.tenant_id`.
- `anchorOverwriteGuard.ts:492-525` resolves `external_id` first; `:424-443` is the KS-1603 narrowing.
- **Wallet and UTxO selection, and KS-535:** the design does not touch the wallet, the mnemonic or UTxO selection. Finding 1 says it must touch UTxO selection, inside one deployment's wallet.

### 17. Which steps need Kam (the design's list, completed)
**The design names:** B on each box, D, the flip on each box, `anchor_c09c1b1f`, D2 (fees) and R8.

**Missing from that list:**
- (a) the finding-1 fix, because it resubmits and so spends money, and it edits KS-1171 behaviour;
- (b) the fact that merging B or D is the same as applying it on both boxes (finding 2);
- (c) the D9 follow-ups: holding the retry, and the optional post-056 repair (finding 4);
- (d) the external contract change and the Stuart ask (findings 6 and 9). Comms to a human are Kam-gated.

**Production / money / irreversible:** the index drop (irreversible), every resubmission (money), and any write to the live kintsugi or demo-pk `anchor_store`.

---

## TESTED / NOT TESTED / HOW

**TESTED (read, not run).** Every `file:line` in the findings above was read at `e4cd2e13` with `git -C …/cache/src show <pin>:<path>`, extracted to the session scratchpad and read with `awk`/`sed`/Read.
- Commits present in the cache: `cat-file -t` printed `commit` for `e4cd2e13`, `5dccdcb2` and `bd6697e0`.
- Diff scope: `git diff --stat` for `5dccdcb2..e4cd2e13` gave 4 files, 1 of them code (`adminConfig.ts`); for `bd6697e0..5dccdcb2` over the anchoring and originate route paths it was empty.
- `anchorSchema.ts`: `/usr/bin/grep -i` for `.strict(`/`passthrough` found 0 strict hits; the positive control was 3 `z.object` hits in the same file.
- T's figures (row fields, Koios results, log counts, audit times) were taken from T's files as written. I did not re-measure them.

**NOT TESTED / unmeasured**
- No cell, mutant, container or database was run. Every finding is a read.
- Findings 1-3 are code inferences. In finding 1:
  - the stale-UTxO cause is **unmeasured**: the refusal text and the spent input are not in any surviving log (T, A3(c));
  - the `:641` exit is **inferred** from `retry_count=0`, `error_message=NULL` and the REFUSED line;
  - that the real reply contained "already been included" is **unmeasured**. It rests on the text quoted at `anchorSubmission.ts:29-30`, which is a demo observation from 2026-08-27, not this incident's text.
- **Unmeasured:** whether S or K's UI calls `POST /:id/anchor` on an `anchor_failed` document (finding 4).
- **Unmeasured:** what the chain-scan verifier returns when several transactions share one hash (finding 11).
- **Unmeasured:** the row's state after 08:55:38Z (T's 09:02Z re-read had not happened when this review was written).
- **Not read by me:**
  - the design's sub-agent A, B and C reports;
  - the nine DDL mirrors in §6.4;
  - migration 031;
  - `verificationV2.ts` (extracted, not reviewed line by line);
  - the §10.1 test files;
  - `systemTest/schemathesis/…/anchor_sql.py`;
  - `processBatchAnchor` beyond the listed lines.

  The design's claims that rest on those sources are **unverified** by this review.
- **Unmeasured:** the line-count estimates, the fees and queue time per event under load, the replica count, `MULTI_TENANCY_ENABLED`, and each box's `server_version`. The design labels each of these correctly.

**HOW (this review's footprint).**
- Read-only throughout: no fetch, checkout or worktree; no write under `!CODING`; no box, ticket, Docker or az.
- Writes: this file, and source extracts in the session scratchpad.
