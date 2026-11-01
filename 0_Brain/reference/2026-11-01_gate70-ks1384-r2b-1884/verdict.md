## QA GATE 70, TIER 1, MONEY PATH: KS-1384 R2b, #1884 (delta 31d146678...ecfe4f07f)
(Opus 5.5, Sun 1 Nov 2026, commissioned by Wednesday, model routing row G1. Findings only. Nothing was fixed, pushed, commented, approved or merged, and nothing was written to GitHub, Linear, mail or `/Volumes/DevMASTER/!CODING`. Evidence is in `evidence/`, scripts in `scripts/`.)

**BLUF: GO WITH NOTES.**
- **No money cell pays more at ecfe4f07 than at 31d146678.** I measured 82 cells on real Postgres under `secuura_app` (RLS on), each run at the head and at the base:
  - gate 65's 25 and gate 68's 25, plus my own 32 (probe70, real-shaped rows on both reads and an own-create fake answered from a modelled wallet).
  - One cell counts more POSTs on arrival: gate 65's R1-wedge (2→3), and my G-wedge, which is the same cell. That is the G65-F1 fix, not a fee. The base's two POSTs never persisted a row and the document is wedged for good (D 409). The head's third POST is the document's first and only persisted anchor (D 202; `persisted rows 0` at base, `1` at head, in the log line itself).
  - **Cells R2b targets go down:**
    - G68-F1's N-R3 1→0, N-Q3b 1→0, N-R4 2→1.
    - The landed-create cells: K-kintsugi 1→0, K-loose 1→0, K-chain 2→1, K-rec 1→0.
    - Every own-create not-answered shape 1→0.
    - With a real own-create, gate 65's R2-f3 goes 1→0 and G68-F3's H-diff-repeat 2→1.
- **The author's 47/50 reproduces exactly** with the author's copies. The three reds are explained correctly at source (Q1).
  - **The ORIGINAL probes cannot run at this head.** Their fakes have no own-create route; express answers 404, R2b turns that into 503, and every cell stops before the steps it measures (0 POSTs in every logged cell).
  - So I ran both originals and both copies, and the originals at the base. The added line is the whole diff (Q1).
- **G65-F1 is fixed in exactly the shape gate 65 asked for, shape (a)** (Q2). **G68-F1 is closed for money** (Q3): the network leg is gone, and all three N cells pay as on a consistent network.
- **The deploy hold (both services' `CARDANO_NETWORK` equal on each box) is still required**, for a non-money reason: G70-F1.
- **All 6 of my valid mutants are KILLED**, and 5 die on fee counts: the network leg restored, step 3's not-answered/loose/found branches removed, and G65-F1's restore dropped.
  - One more mutant did not compile and is not counted.
  - The resolver mutant M6b is fee-neutral. The retry route's own step 3 still guards when a reader's heal is broken.
- **Develop moved during the gate: R1 and R2a merged** (develop `3d036184`).
  - R2b needs re-stating onto it. Measured: with its own base `b86dcf7f5`, that is conflict-free and leaves every product source byte-identical to `ecfe4f07` (condition (c)).
- **Author's suites reproduce:** unit 160/1979, real Postgres 57/57, anchoring 749/750 and 122/122, tsc 190 files 0 errors, check:openapi rc 0.

**What is not clean:**
- **G70-F1 (MINOR, presentation, permanent).** The retry route's own-create `found` branch writes ORIGINATE's `CARDANO_NETWORK` into a `confirmed` blob (`documents.ts:1582`), and `confirmed` is now terminal in SQL.
  - Where the two services differ, the document permanently names the wrong network. Measured (N-ocnet): `blob network preprod row network preview`.
  - No reader can correct it afterwards: every confirmed write refuses a confirmed blob.
- **G70-F2 (NOTE, instrument).** Both original probes are blind at this head, because own-create 404s, so 503 comes before any step.
  - The author's one-line copies answer own-create "none", so **none of the 50 cells exercises step 3** (found, loose, not-answered).
  - Every one of R2b's new money branches is measured only by my probe70 and W's unit and route cells.
- **G70-F3 (NOTE, liveness, stated as KS 1907 and KS 1908, now bounded).** These are retries refused for good, money-safe:
  - own-create scans at most 20×100 wallet transactions, newest first, within 4 s, including label reads;
  - the loose guard refuses any document with an id+hash transaction at another time.
- **G70-F4 (NOTE, latent).** The G65-F1 restore is exactly shape (a). A marked `pending`, anchorId-less blob that holds any other key still wedges (G-keep: D 409 at head and base). I found no in-repo writer that makes that blob.
- **G70-F5 (NOTE, claims and text).** Stale "on this network" text; an unused `network` in the in-flight context; known limit 4 understates the create path's `updateDocument` writes; a body-copy placeholder.
- **G70-F6 (NOTE, outside the delta).** threadTokenMint's red is **not host-dependent.** It is deterministic from the lockfile's layout: two copies of `@lucid-evolution/plutus`, so `instanceof Constr` fails. The product mint imports the same pair.

**Merge onto develop:** develop moved during the gate, from `77fac4727758` to `3d036184` (R1 and R2a merged; see Heads). Both readings:
- **At the END develop `3d036184`, the plain merge-tree is rc 1 on 18 files** (`evidence/merge_tree_develop_end.txt`). They include the money files, but they are squash-merge artefacts. Measured from the old merge base `dc8c210c`, R2a's content arrives twice: once as develop's squash, once as R2b's stack.
- **With R2b's own stack base `b86dcf7f5` as the merge base, the merge onto `3d036184` is CLEAN, rc 0** (tree `b667b7558d2a`, `evidence/merge_tree_develop_end_base_b86d.txt`). This is what `git rebase --onto develop b86dcf7f5` would meet.
  - **50 of the 52 delta files would be byte-identical to `ecfe4f07`**, every product source among them (`evidence/rebased_tree_vs_head_delta_files.txt`).
  - The two that differ are the generated `secuura-api.yaml` (develop changed it too; it needs regenerating plus check:openapi) and the test file `ks1384-r1r3-unknown-outcome.integration.test.ts` (develop's R1 merge touched it too).
- **At the START develop `77fac4727758`:** merge-tree rc 1 on exactly the three files the author named (fb-sweep, anchoring `index.ts`, ks1293), tree `42351766c9ad` (`evidence/merge_tree_develop.txt`).
- fb-sweep and ks1293 are not in this delta.
- The `index.ts` conflict (merged lines 38-42) IS on this delta's own hunk (`@@ -37,0 +38,2`, the `createOwnCreateLookup` import). It is an add/add between two lines that develop (via merged train members) and the train both added after the merge base `dc8c210c`. The resolution is one-sided and trivial: keep the import.
- The own-create route itself (merged :914-952) merges clean (`evidence/merge_tree_conflict_vs_delta.txt`).

**Heads:**
- **START** (2026-10-31T22:48:18Z, `git ls-remote`, `evidence/lsremote_start.txt`):
  - `refs/pull/1884/head` = `ecfe4f07fdcec78b8d45d897bd4dccd4be829be7` (equals the READY mail and the brief)
  - develop = `77fac47277585ec26eea7f0f1d4631544ff054f5`
  - `refs/pull/1868/head` = `48b328c9a3e308e0519ed66cf55dc27184a4d709`
  - `refs/pull/1874/head` = `31d1466788bea96f6175b595c8fb3078229668be`
- **END** (read in the same action as this section; `evidence/lsremote_end.txt`):
  - read at 2026-11-01T00:40:34Z
  - `refs/pull/1884/head` = `ecfe4f07fdcec78b8d45d897bd4dccd4be829be7` (unchanged)
  - develop = `3d036184d37f0ad2a46fff4e9e6e80de03441b93` (MOVED since the start; both merge readings are under "Merge onto develop")
  - `refs/pull/1868/head` = `48b328c9a3e308e0519ed66cf55dc27184a4d709` (unchanged)
  - `refs/pull/1874/head` = `38e8c0d3cadca5477d40195d3a55de2b8568ecfa` (moved)
- **During the gate, R1 and R2a merged** (`evidence/heads_end_analysis.txt`):
  - R1 (#1868) landed as `60e59bd2`.
  - R2a (#1874) moved to `38e8c0d3` ("R2a merge prep, part 2 - merge develop 60e59bd2270b", which has `b86dcf7f5` as an ancestor) and landed as develop `3d036184`.
  - `38e8c0d3` is NOT an ancestor of `ecfe4f07` (rc 1). R2b is stacked on R2a's pre-merge commits, as expected.
  - develop `3d036184`'s copies of R2a's product files are **byte-identical** to `b86dcf7f5`'s, which are the files I swapped in as the base: `reanchorInFlight.ts d2f85de8004c`, `documents.ts 3951e76eaf22`, `documentRepo.ts 35e0d85d02ab`, plus `originate.openapi.ts` and anchoring `index.ts` (`evidence/heads_end_r2a_merged_compare.txt`).
  - So this gate's base measurement is also a measurement of develop as it now stands.
- This GO is a statement about **ecfe4f07** only.

## VERDICT: GO WITH NOTES
- **Fix-before-merge: none.** No cell pays more at the head than at 31d146678 (Q6).
- **Conditions** (priority is Wednesday's):
  - (a) **The train's deploy hold keeps its `CARDANO_NETWORK` equality check** (both services, each box). That stands until G70-F1 is closed, by taking the network from anchoring's answer rather than originate's environment. It is no longer a money condition (Q3).
  - (b) From now on the train's probes carry an own-create route modelled on a wallet (found, loose, none, not-answered), not a fixed "none". Without it, step 3 is unmeasured by any gate probe (G70-F2). `evidence/probe/gate70-r2b-probe.integration.test.ts` is one such harness.
  - (c) R2b must be re-stated onto develop `3d036184` (R1 and R2a landed during this gate). That produces a NEW head, which this GO does not name.
    - Measured: a rebase onto develop with `b86dcf7f5` as the base is conflict-free, and leaves every product source byte-identical to `ecfe4f07`.
    - So the new head can carry this verdict if Wednesday confirms, at the new head, (i) the blob ids of the 50 delta files equal `ecfe4f07`'s, (ii) the yaml is regenerated with check:openapi rc 0, and (iii) the r1r3 integration file is re-run.
    - Any other difference needs a re-gate.

## FINDINGS

**G70-F1 · MINOR · presentation, permanent where the networks differ (`documents.ts:1582`; terminal predicate `documentRepo.ts:994`, `:939`).** Own-create `found` confirms the blob with `network: process.env.CARDANO_NETWORK || 'preprod'`, which is originate's network, not the chain's.
- **Mechanism:**
  1. Anchoring scans ITS wallet on ITS network (anchoring's `CARDANO_NETWORK`).
  2. The route writes the transaction with originate's network label through `writeReanchorOutcome`.
  3. Since R2b, `confirmed` is terminal: `writeAnchorBlobIf('confirmed')` requires `status IS DISTINCT FROM 'confirmed'` (:994), and so does the outcome write (:939). The poller, the reconcile and the verify heal can therefore never correct the label. (Their own confirmed blob takes `row.network`, `anchorStateSync.ts` `confirmedBlobOf`, which is right.)
- **Measured** (probe70 N-ocnet, anchoring on preview, originate unset; `evidence/probe70_head_app.log`): `409 This document is already anchored on chain (9b0a9d… blob network preprod row network preview posts 0`.
- **Red-before:** at 31d146678 the same document POSTs (`N-ocnet 202 … posts 1`, `evidence/probe70_base31d1_app.log`). The wrong-label write is new with step 3.
- **Not money.** Nothing in originate's money path reads the blob's network any more (Q3). Which clients present `blockchain.network` (an explorer link, say) I did NOT trace.
- The pre-existing 202 outcome (`documents.ts:1714`) and the create path (`:946`) also label with originate's network, but those blobs are not terminal, so the poller rewrites them from the row.
- **Fix shapes (W's choice):**
  - (a) Return the network in own-create's answer (anchoring knows it) and write that.
  - (b) Or keep the deploy hold's equality check as a boot check.
- **Spark:** missed it.

**G70-F2 · NOTE · instrument (gate 65's and gate 68's probes at R2b; the author's 47/50).**
- **Originals unchanged** (sha256 `3be022f874a62e61…` and `ec9401c1d09dda6f…`):
  - probe65 at head is **4 passed / 21 failed** (`evidence/probe65_head_orig_app.log`), with `own-create answered HTTP 404` 43 times.
  - probe68 at head is **13 / 12** (`evidence/probe68_head_orig_app.log`), with 70 such lines.
  - Every logged cell reads `posts 0`: the route answers 503 Retry-After 60 before step 4.
- **The author's copies add exactly one line each** (`evidence/probe_author_copies/diff65.txt`, `diff68.txt`). The line answers `POST /api/anchors/own-create` with `{outcome:'none', loose:[]}`.
  - That makes every cell reach step 4, so the 50 cells re-measure R1, round 3 and R2a under R2b and are the right instrument for that.
  - But step 3's found, loose and not-answered branches, which are the branches that change fees in R2b, are reached by none of them.
- **What measures step 3** (red-before at 31d146678 in brackets, `evidence/probe70_base31d1_app.log`):
  - probe70's K-*, OC-*, R-* and N-R3/N-R4 (wallet) cells: K-kintsugi 0 [1], K-loose 0 [1], K-chain 1 [2], K-rec 0 [1], OC-* 0 [1 each], R-f3-wallet 0 [1], R-hdiff-repeat 1 [2];
  - my mutants G70-M3, M4 and M5 (Q2 and the mutant table);
  - W's unit cells.
- Two cells reach step 3 only with a real-shaped own-create: probe70 R-f3-wallet (G58-F3's residual) and R-hdiff-repeat (G68-F3). With the author's "none" they still pay (author's copy: R2-f3 1 POST, H-diff-repeat 2).

**G70-F3 · NOTE · liveness, stated (KS 1907, KS 1908), bounded here; money-safe (`ownCreate.ts:29-30`, `walletLabelScan.ts:82-111`, `documents.ts:1597`).**
- **The scan's bounds:**
  - It walks the platform wallet newest first, at most `maxPages: 20` × `pageSize: 100`, within `budgetMs: 4_000`.
  - Label reads go in batches of 10 for every in-window transaction.
  - The window is earliest attempt − 10 min to latest attempt + 24 h.
- **Two consequences:**
  - A document whose window is behind more than 2000 newer wallet transactions, or whose window holds more transactions than 4 s of label reads covers, is `truncated` on every retry: 503 Retry-After 60 for good. KS 1908 states the old-document half only; the busy-window half is the same mechanism.
  - The loose guard refuses any document with an id+hash transaction at another time (K-loose; OC-loose-na), until the operator path (KS 1907).
- Both refuse; neither pays. Not measured on a real wallet.

**G70-F4 · NOTE · latent (`documentRepo.ts:844-855`, `confirmReanchorClaim`).**
- The restore requires `status = 'pending'`, the marker, and NO other key. A marked pending anchorId-less blob holding, say, `createAttempts` keeps no flag. A failed POST's release strips the claim keys, which leaves `{status:'pending', createAttempts}`. No claim can take that blob (the claim's pending disjunct needs `retryClaim` or the marker): 409 for ever.
- **Measured** (G-keep): head `blob after {"status":"pending","createAttempts":[…]} D 409 A re-anchor for this document is already in progre posts 1`; the base is the same.
- So it is not a regression, and it is exactly what the PR says ("a blob with any other key is never given the flag").
- **Reach:** I found no in-repo writer of a `pending`, anchorId-less blob with other keys.
  - The 2xx-without-id outcome carries `createAttempts`, but that blob has no `status` (gate 65's Q2c-route: 400).
  - Any future writer of such a blob reopens G65-F1.

**G70-F5 · NOTE · claims and text.**
- (i) `reanchorInFlight.ts:13` (module header) and `:160` (the `anchored` reason string, logged) still say "on this network". The rule above `:118` still states the network leg before the R2b paragraph that drops it.
- (ii) `InFlightContext.network` (`:87`) is still required and still passed (`documents.ts:1631`), but nothing reads it. It is harmless, and a future reader may think it is compared.
- (iii) Known limit 4 says "the create path's `.catch` still writes through `updateDocument`". The create path's 202 write (`documents.ts:1035`) does so too. It is safe by timing (it runs within seconds of the 202 and before the poller starts; the reconcile needs 15 min of silence, and the verify heal needs a real txHash), but it is not stated.
- (iv) The PR-body copy I could read (`evidence/pr/body_seatW14_copy.md`, 14737 bytes, mtime 08:36 local) still carries a `{{HOOKLINE}}` placeholder. The READY mail says the live body is 16960 bytes, so the live body was not read (no `gh` from this seat).
- (v) "check:openapi rc 0 (314 paths)": rc 0 and `CHECK PASS` reproduce. The log prints no path count, so 314 is not checkable from it.
- (vi) `healAnchorForVerify` presents its `confirmed` decision even when the write matched 0 rows (`anchorStateSync.ts:596-603`), that is, when another writer confirmed first, possibly with another tx. That is presentation for one request only.

**G70-F6 · NOTE · outside the delta (threadTokenMint; see Q7).**
- The red is deterministic: the test's `Constr` and `applyParamsToScript`'s serializer come from different copies of `@lucid-evolution/plutus` (`evidence/q7_constr_identity.log`: `lucid.Constr === utils-plutus Constr: false`).
- The product `threadTokenMint.ts:267-269` imports the same pair (`@lucid-evolution/lucid` from the root, `@lucid-evolution/utils` from anchoring's own `node_modules`).
- Whether the anchoring image's install layout reproduces it is NOT tested. The delta touches no package file.

## Q1. Both probe files, at the head
| Run | sha256 | Result | Log |
|---|---|---|---|
| gate 65 ORIGINAL at head | `3be022f874a62e61c129984c251684cae5ada792fbd8811b9744bbb9b8d77d13` | 21 failed, 4 passed | `evidence/probe65_head_orig_app.log` |
| gate 68 ORIGINAL at head | `ec9401c1d09dda6f1441bf11e5a472b59fb1c30d698155f2d2b0d0edbdd97446` | 12 failed, 13 passed | `evidence/probe68_head_orig_app.log` |
| gate 65, W's copy, at head | `74d22ce8ea9ae442499c00bfb6863db6fea355bf8bd2df75d28bcf5e79e84cec` | **2 failed, 23 passed** | `evidence/probe65w_head_app.log` |
| gate 68, W's copy, at head | `8b808336fa671c5e5adf75af1599eec27d34f474d614499965bd89f887be1a25` | **1 failed, 24 passed** | `evidence/probe68w_head_app.log` |
| gate 65 ORIGINAL at 31d146678 | `3be022f8…` | 3 failed, 22 passed | `evidence/probe65_base31d1_app.log` |
| gate 68 ORIGINAL at 31d146678 | `ec9401c1…` | 4 failed, 21 passed | `evidence/probe68_base31d1_app.log` |

- **What the added line changes:** the two diffs are each one comment plus `fakeAnchoring.post('/api/anchors/own-create', … {outcome:'none', loose:[]})`. Without it the fake's express app 404s that route. `ownCreateClient.askOwnCreate` reads any non-200 as `not-answered/unanswered`, and the route answers 503 Retry-After 60 before step 4 (`documents.ts:1605`). With it, step 3 is a no-op and each cell measures what it measured at R2a. At the base the line is inert, because R2a never calls own-create.
- **The three reds, at source:**
  - **Q2b-past** (2 POSTs, head and base): round 3's residual 2. A's POST is held unpersisted past the lease. C's read gets 404, so `decideInFlight` returns absent, and `confirmReanchorClaim` removes the marker and C POSTs. Then A persists. With a real own-create nothing is on chain at C's time, so step 3 says none and the cell is unchanged (my S-Q2bpast-wallet: 2 at head and at base).
  - **R2-f3** (1 POST): the author's claim is TRUE. The cell holds the read and answers `ABSENT` (404) by hand (`held[0].answer(ABSENT)` in the probe). Real anchoring at this head answers a failed by-document read with 503 (`anchoring index.ts:1060`, which R2a added), and originate turns that 503 into 503 with 0 POSTs (gate 68's F-503m, 0 here too). With a wallet-backed own-create the same shape pays **0** (probe70 R-f3-wallet: the landed tx is loose, so 409; 1 at base).
  - **H-diff-repeat** (2 POSTs, head and base) is G68-F3 / KS 1919. Anchoring's upsert update list has no `content_hash`, so the row never matches. With a wallet-backed own-create it pays **1** (probe70 R-hdiff-repeat; 2 at base): the first re-anchor's transaction is on chain under this document's id and hash, so the loose guard refuses.
- **No red the author did not predict.** R1-wedge, red at R2a, is green at the head (`D 202 E 400 posts 3`); see Q2 and Q6.

## Q2. G65-F1, the narrower restore
- **It is shape (a), exactly as gate 65 wrote it** (`documentRepo.ts:844-855`, both copies). In `confirmReanchorClaim`, the CASE adds `retryClaimMadeBlob: true` only when the authoritative blob has a marker, `status = 'pending'`, and is EMPTY after removing `status`, `retryClaim`, `retryClaimedAt`, `retryPostUnknownAt`, `retryPostUnknownToken` and `retryClaimMadeBlob`.
- **The paths that reach it:** the re-check is reached only after step 3 answers none, and step 4 answers absent (`documents.ts:1681`). With a marker set, absent comes only from an unambiguous 404 or an empty `anchors` list (`reanchorInFlight.ts:135-143, :166`); any row gives maybe-landed. So the flag is restored only where anchoring has just said "no row" and this claimant has not yet POSTed, which is gate 65's own premise.
- **Each outcome after a restore:**
  - **failed POST:** the release deletes the blob, so the document is blob-less and retryable. Measured: G-wedge `D 202 … persisted rows 1` at head against `D 409 … persisted rows 0` at base. Gate 65's R1-wedge: head `blob after C null D 202 E 400`, base `blob after C {"status":"pending"} D 409 E 409`.
  - **202:** the outcome write replaces the blob, so the flag is gone (G-success: keys `anchorId, anchoredAt, blockHeight, createAttempts, txHash`).
  - **unknown again:** `markReanchorPostUnknown` drops the flag as before. The next cycle restores it again.
  - **an `anchor_failed` marked blob:** status is not pending, so no flag, and the release keeps the blob, which is correct.
  - **a pending blob with any other key:** no flag, so it wedges (G70-F4, latent, same at base).
- **Mutant G70-M2** (the restore dropped in both copies) is listed under Mutants below.

## Q3. G68-F1: the network leg
- **The rule at this head** (`reanchorInFlight.ts:119-124`): `isLandedForThisContent` compares the content hash only. The network is not read.
- **Cells** (head [base 31d146678]; POSTs on arrival):

| Cell | What | head | base |
|---|---|---|---|
| L3 (W, unit) | inverted: a confirmed row on another network is anchored | green in W's file (unit suite below) | n/a |
| f2g (W, real PG, inverted) | the same on real Postgres; W's fake now stores anchoring's own network | green (`evidence/w_integ_head_app.log`, 57/57) | n/a |
| n1, n2 (W, real PG) | gate 68's N-R3 and N-Q3b shapes | green (same log) | n/a |
| gate 68 N-R3 / N-Q3b / N-R4 | anchoring preview, originate unset | **0 / 0 / 1** | 1 / 1 / 2 |
| probe70 N-R3-none / N-Q3b-none / N-R4-none | the same with own-create "none" (step 4 alone) | **0 / 0 / 1** | 1 / 1 / 2 |
| probe70 N-R3 / N-R4 (wallet own-create) | the loose guard refuses first | **0 / 1** | 1 / 2 |
| probe70 N-hist (liveness) | confirmed row on the OLD network, anchoring and originate both mainnet | 0 (409 already anchored) | 1 |

- **Can a landed anchor be paid for twice when the networks differ? No, at this head.** Every N shape pays exactly as on a consistent network: N-ctl 0 and S-R4 1 (`evidence/probe68w_head_app.log`).
- My mutant **G70-M1** restores R2a's network comparison; see Mutants below.
- **N-hist (liveness, not money):** if anchoring is ever moved to a new network, a document with a confirmed row on the old network is refused ("already anchored") and is not re-anchored on the new one. Before R2b it POSTed once. This is the safe direction, and a network migration is an operator event.
- **Is the DEPLOY HOLD still required? Yes, but no longer for money.**
  - No originate money decision reads a network now. `network` is passed into the in-flight context (`documents.ts:1631`) but never compared (G70-F5 ii). Anchoring ignores the request's network. Own-create scans anchoring's own wallet.
  - The remaining dependency is G70-F1: own-create `found` writes originate's network into a terminal blob.
  - So the equality check still protects what a document SAYS, permanently, on the boxes where the descriptors differ (gate 68: `services.bicep`, `docker-stack.yml`, `docker-compose.production.yml` when unset; READ ONLY, unchanged in this delta).

## Q4. G68-F2: real-shaped rows
- **W's fakes** (read in the delta):
  - The r1r3 fake now returns `contentHash` and anchoring's own network; the r2a fake stores anchoring's own network (the commit message, and the cells m8/m9/f2g/n1/n2 green).
  - Neither carries `payloadTimestamp` or `transactionHash` on the by-document read (grep: 0 occurrences of each, against `contentHash` 7 and 14). The by-document read does not need them: the retry route's step 4 reads status and hash only. The readers' by-id rows are in W's unit cells (`verifyHealFetch.ts`).
- **Mine:** probe70's rows carry every field of the real by-document read (`formatAnchorResponse`) AND the by-id read (`index.ts` ~1005-1035):
  - `transactionHash` (64-hex once confirmed), `blockNumber`, `payloadTimestamp`, anchoring's own network;
  - the 202 carries `payloadTimestamp` (`index.ts:596`), and the upsert keeps `content_hash` and takes the new payload timestamp.
  - Own-create is answered from a modelled wallet with `ownCreate.ts`'s loose and bound rule.
- **Money cells with these rows** (head [base]):
  - S-R3 0 [0], S-Q3b 0 [0], S-R4 1 [1], S-P3b 1 [1], S-par 0 [0].
  - At the head the wallet's loose guard answers first ("A transaction for this document exists on chain"), where at base step 4's "already anchored" did.
  - Ten parallel retries: 0 POSTs.

## Q5. D3 as written, and KS-1918
- **D3 vs its text** (`anchorStateSync.ts:559-603`, `verification.ts:732, :1253`, `verificationV2.ts:355`):
  - v1's `confirmStalePendingAnchor` and v2's `healBlobWithChainFact` are gone, and so is `persistHealedAnchor`. Both routes call `healVerifyRow`, then `healAnchorForVerify`. TRUE.
  - It reads the blob's OWN row by `anchorId` with the caller's bearer, and lets the resolver decide. Only `confirmed` is presented and written, through `writeAnchorBlobIf('confirmed')` (:587, :598). TRUE.
  - `sameDoc` and the unconditional chain answer are dropped. TRUE (diff).
  - "A verify never fails a document": an `anchor_failed` decision returns the blob unchanged (:587). TRUE.
  - KS 1661 / KS 1676 eligibility is kept (:566-569), and a truthy `simulated` on the row refuses (:574). TRUE.
  - KS 1129's stored-height fallthrough (:592-595). TRUE.
  - "No bearer, no heal": `if (!anchorId || !input.authHeader) return blob` (:569); v2 passes `''` (`verificationV2.ts:355`). TRUE.
  - The resolver requires a 64-hex tx (`anchorResolution.ts:128`). TRUE.
  - One nit: G70-F5 vi.
- **KS-1918, bounded:** a v2 verify, or an anonymous v1 verify, presents the STORED blob.
  - A stale-pending document shows pending, not confirmed, until the GET reconcile (an authenticated read after `RECONCILE_STALE_MS`, 15 min) or the in-process poller (at most 60×10 s, while that process lives) heals it.
  - **Money risk: none.** No verify path POSTs or writes `anchor_failed`, and an unhealed pending blob is not retryable (the route lets only `anchor_failed` or an anchorId-less pending blob through, `documents.ts:1536-1537`; a heal-eligible blob has an anchorId and a txHash).
  - **Disclosure risk: none new.** It shows LESS than before R2b, which presented a chain fact from a pre-auth call. It is an under-claim on presentation.
  - **New in this delta: yes, as a presentation regression.** It is stated. The poller's real heal latency is UNMEASURED by the author and by me.

## Q6. Fee counts: base 31d146678 against head ecfe4f07 (every money cell; POSTs counted on arrival)
Base = the seven originate product files the delta modifies swapped to 31d146678 and restored, sha256-checked (`scripts/swap_base_run.sh`, `evidence/swap_base_31d1.out`, `restore-check rc=0`).
- The swap: `documents.ts`, `documentRepo.ts`, `reanchorInFlight.ts`, `anchorStateSync.ts`, `verification.ts`, `verificationV2.ts`, `originate.openapi.ts`.
- The three new files stay on disk. Only they reference each other (logged).
- probe65 and probe68: ORIGINALS at base, W's copies at head (Q1). probe70: the same file at both (sha256 `59a4a3ad76dddeba…`).

| Cell | base | head |
|---|---|---|
| probe65 P1a-e, P3a-d, Q2a-lock/par/chain/race, Q2b-in, Q2c-route, Q2c-writer, Q2d-a/b, R4-502, R2-f3 (fake 404) | 1 each | 1 each |
| probe65 P5, P5b, R3-crash | 0 | 0 |
| probe65 Q2b-past | 2 | 2 |
| probe65 **R1-wedge** | 2 (D 409 E 409; wedged) | **3** (D 202 E 400). Instrument: A `hang-no-row` and C `error500` persist no row in that fake; D is the only persisted anchor. G65-F1 fixed |
| probe68 S-R3, S-Q3b, S-par, S-again, N-ctl, N-case, H-prefix, H-nohash, H-diff-marked, O-1, O-2, O-3, O-5, F-503m, F-503u | 0 | 0 |
| probe68 S-R4, S-P3b, N-P3b, H-diff, O-4, F-404u (control) | 1 | 1 |
| probe68 **N-R3 / N-Q3b** | 1 / 1 | **0 / 0** |
| probe68 **N-R4** | 2 | **1** |
| probe68 H-diff-repeat | 2 | 2 (G68-F3, own-create "none") |
| probe70 **N-R3, N-R3-none, N-Q3b-none, N-hist, N-ocnet** | 1 each | **0 each** |
| probe70 **N-R4, N-R4-none** | 2 / 2 | **1 / 1** |
| probe70 S-R3, S-Q3b, S-par | 0 | 0 |
| probe70 S-R4, S-P3b | 1 | 1 |
| probe70 S-Q2bpast-wallet | 2 | 2 (A never persists in this fake) |
| probe70 **K-kintsugi, K-loose, K-rec** | 1 each | **0 each** |
| probe70 **K-chain** | 2 | **1** |
| probe70 **OC-truncated, -unanswered, -404, -500, -malformed-found, -hang, OC-loose-na** | 1 each | **0 each** (503 Retry-After 60 with `kind`; hang 5012 ms `deadline`; loose 409) |
| probe70 OC-other-hash (liveness control), OC-par | 1 / 1 | 1 / 1 (OC-par: one own-create call for ten retries) |
| probe70 OC-found-revoked | 0 | 0 (400 revoked, before the claim) |
| probe70 **G-wedge** | 2 (`persisted rows 0`, D 409) | **3** (`persisted rows 1`, D 202). Same instrument note as R1-wedge |
| probe70 G-keep | 1 | 1 (G70-F4) |
| probe70 G-success | 2 | 2 (A never persists) |
| probe70 **R-f3-wallet** | 1 | **0** |
| probe70 **R-hdiff-repeat** | 2 | **1** |

- **No cell pays more at the head.** The two higher on-arrival counts are proved to be POSTs that persisted nothing at base, against the document's first persisted anchor at head, in the fakes' own code and the logged `persisted rows`.
- Totals:
  - probe65: 22/25 at base, 23/25 at head;
  - probe68: 21/25 at base, 24/25 at head;
  - **probe70: 12/32 at base, 32/32 at head** (`evidence/probe70_base31d1_app.log`, `evidence/probe70_head_app.log`).

## Q7. threadTokenMint's emulator round-trip
- **Not host-dependent: disproved.** The failure is `Could not serialize the data: Error: Unsupported type` at `applyParamsToScript` (test :71), deterministic and not a timeout (gate 68's log; mine below).
- **Cause, measured** (`scripts/q7_constr_identity.mjs`, `evidence/q7_constr_identity.log`):
  - The test builds `new lucidCore.Constr(...)` from `@lucid-evolution/lucid` 0.4.34 at the repo root, which resolves `@lucid-evolution/plutus` **0.1.31** at the root.
  - `applyParamsToScript` comes from `@lucid-evolution/utils` 0.1.70 in `services/anchoring/node_modules`, which resolves `@lucid-evolution/plutus` **0.1.33** there.
  - The serializer's `instanceof Constr` sees a foreign class: `lucid.Constr === utils-plutus Constr: false`.
  - The layout is the lockfile's (`package-lock.json`: root plutus 0.1.31, anchoring plutus 0.1.33, anchoring utils 0.1.70), so every `npm ci` from this lock reproduces it.
- **Does the delta touch it? No.** No package file, lockfile, threadTokenMint file or anchoring cardano file is in the 52.
- Anchoring unit at the head: `Test Files  1 failed | 53 passed (54)`, `Tests  1 failed | 749 passed (750)` (`evidence/anchoring_unit_head.log`, vitest 2 workers). The red is the same cell with the same `Error: Could not serialize the data: Error: Unsupported type`, at 55458 ms.
- G70-F6: the product mint imports the same pair. That is outside this gate.

## Q8. R2b's own claims (the PR body copy, `evidence/pr/body_seatW14_copy.md`; G70-F5 iv), tested against the code
| Claim | Gate 70 |
|---|---|
| "No branch except none ever POSTs" (step 3) | TRUE. `documents.ts:1576-1617`: found returns 409, loose 409, not-answered 503, each before `readInFlightAnchor` (:1624). Measured: OC-* 0, K-* 0 |
| found: "confirms the blob under the claim" | TRUE. `writeReanchorOutcome(… claimToken …, 'anchored')`; on 0 rows it releases. K-kintsugi: `blob confirmed c64aa2c1 claim null` |
| loose: 409 with the transactions; not answered: 503 Retry-After 60 with `error.kind` | TRUE (OC-*: `503 60 truncated` / `unanswered` / `deadline`; OC-loose-na 409) |
| own-create runs within 4 s inside originate's 5 s bound | TRUE by code (`OWN_CREATE_CALL_TIMEOUT_MS = 5_000`, `budgetMs: 4_000`). OC-hang: `503 deadline 5012` ms |
| "Full timeout budget 30 s, 1/20 of the lease" | TRUE by code: own-create 5 s, then the read 5 s, before the re-check that renews the lease (:1681), then headers 10 s and body 10 s. Lease 600 s |
| D6: "the earliest is kept, plus the 9 newest; every rebuild writer carries it forward" | TRUE (`appendCreateAttempt` :95-100; `carriedForward` keeps it; K-chain: `attempts after A 2 … attempts kept 2`, and own-create was asked with 2 timestamps) |
| D6: "written only when there is one" (no empty list) | TRUE (`documents.ts` the 202 outcome IIFE, and the create path's `typeof … === 'string'` guards) |
| "None of them writes through updateDocument any more" (the readers) | TRUE for `anchorStateSync.ts`, `verification.ts`, `verificationV2.ts` (0 code calls). Known limit 4 understates the create path (G70-F5 iii) |
| G68-F1 closed (N-R3 0, N-Q3b 0, N-R4 1) | TRUE (Q3) |
| G65-F1 fixed (R1-wedge D 202) | TRUE (Q2) |
| "Gate 65's probe 23/25, gate 68's 24/25" | TRUE with the author's copies (Q1). The ORIGINALS are 4/25 and 13/25 at this head (G70-F2) |
| KS-1384 real Postgres 57 of 57 (six files) | TRUE: `Test Suites: 6 passed`, `Tests: 57 passed, 57 total` (`evidence/w_integ_head_app.log`) |
| originate unit 160 suites / 1979 cells | TRUE: `Test Suites: 160 passed, 160 total`, `Tests: 1979 passed, 1979 total` (`evidence/unit_head_full.log`, 2 workers). This includes W's L3 (inverted) |
| anchoring unit 54 files / 750, 749 pass; real lane 122/122 | TRUE: unit `1 failed \| 53 passed (54)`, `1 failed \| 749 passed (750)`, the red threadTokenMint (Q7; `evidence/anchoring_unit_head.log`). Real lane, app role, gate70-pg: `Test Files 10 passed (10)`, `Tests 122 passed (122)` (`evidence/anchoring_integ_head.log`). These include W's own-create cells (14 + 7) |
| tsc: product rc 0; 190 originate test files, 0 errors; a planted TS2322 is reported | TRUE. Product `rc=0` (`evidence/tsc_head.log`). Every file under `src/__tests__` (my probes excluded, none placed at the time): `rc=0` (`evidence/tsc_head_with_tests.log`), with 190 such files examined (`evidence/tsc_test_file_count.txt`; this counts `helpers/verifyHealFetch.ts`). Control: `planted.ts(1,14): error TS2322 … rc=2` (`evidence/tsc_control.log`) |
| check:openapi rc 0 | TRUE: `CHECK PASS: on-disk YAML matches generated`, 421 example blocks, rc=0 (`evidence/check_openapi.log`). Control: one planted word in the loose-guard 409 text of `originate.openapi.ts` gives `CHECK FAIL: generated YAML differs from on-disk version`, rc=1 (`evidence/check_openapi_control.log`); the file was restored with sha256 OK and `git status` was empty. "314 paths" not printed (G70-F5 v) |
| "77 new cells, each red first against its mutant; 65 mutants killed" | NOT re-run (W's mutants). My own six are below |
| The poller "in-flight write is a progress write pinned to the polled anchor"; `markDocumentAnchorFailed` "pinned to its anchorId" | TRUE by code (`documentRepo.ts:996-998` predicate; `anchorStateSync.ts` `expectAnchorId`). K-chain: the real `markDocumentAnchorFailed` wrote `anchor_failed` and kept `createAttempts` |
| The GET reconcile: own-create decides, "a GET of a document with one failed read is no longer failed unless own-create answers none" | TRUE: K-rec `blob after reconcile confirmed` at head, `anchor_failed` at base |
| own-create 404 for an absent document "byte for byte" the foreign one | TRUE by code (`index.ts:939-941`, one literal body). The gate reads the shared `documents` table, and anchoring and originate share the database in every descriptor I read (`docker-compose.yml`, `docker-compose.production.yml`, `services.bicep` `commonEnvVars` :392-397, `DATABASE_URL` secretRef `database-url`; READ ONLY, no values read) |

**Mutants** (`scripts/mutants.py`; per cell against the unmutated baseline; each anchor asserted to its exact count and the mutation asserted on disk; every product file restored from `git show ecfe4f07:` with sha256; jobs probe70 (32) and W's r2a real-PG file; `evidence/mutants_run.log`, `evidence/mut/`):

- Baseline: probe70 32/32, W's r2a 12/12 (`{"baseline": "probe70", "rc": 0, "total": 32, "red": []}`, `{"baseline": "w_r2a", "rc": 0, "total": 12, "red": []}`).
- Every mutant restored with sha256 (`"restored_sha256_ok": true`). probe70 was quarantined at the end (`{"probe_quarantined": true}`).

| Mutant | Result | Killed by |
|---|---|---|
| G70-M1: R2a's network comparison restored in `isLandedForThisContent` | KILLED, **on fee counts** | probe70 N-R3-none, N-Q3b-none, N-R4-none; W's f2g, n1, n2. (The wallet-backed N-R3 and N-R4 survive, because the loose guard refuses first: step 3 also covers G68-F1 once own-create sees the chain) |
| G70-M2: G65-F1's restore dropped (both copies) | KILLED | probe70 G-wedge. W's r2a: 0 (W's w1, w2 live in the r1r3 file, not run under this mutant) |
| G70-M3: step 3 not-answered falls through to step 4 | KILLED, **on fee counts** | probe70 OC-truncated, OC-unanswered, OC-404, OC-500, OC-malformed-found, OC-hang |
| G70-M4: step 3 loose guard removed | KILLED, **on fee counts** | probe70 K-loose, OC-loose-na, R-f3-wallet, R-hdiff-repeat |
| G70-M5: step 3 found branch removed | KILLED, **on fee counts** | probe70 K-kintsugi, K-chain, N-ocnet |
| G70-M6: resolver ignores own-create found | **INVALID, not counted**: it does not compile (`TS2339: Property 'kind' does not exist`, `evidence/mut/G70-M6.tsc.log`), so all 44 cells "failed" at suite load | Replaced by M6b |
| G70-M6b: the resolver's own-create `found` answers as if none (the compiling form) | KILLED, **fee-neutral** | W's resolver (f2), (f3), (f4) and readers (x5) (`evidence/mutants_run_M6b.log`). **No probe70 money cell**, K-rec included: with the reader's heal broken, the retry route's own step 3 still finds the bound create and pays 0. The readers decide what a document SAYS; step 3 is the money guard |

## Q9. Merge onto develop 77fac4727758 (and onto 3d036184, after develop moved)
- **At `77fac4727758`, as the brief asks:** `git merge-tree --write-tree` gives **rc 1**, tree `42351766c9ad9f3f7dc3d5ab71c4b7c2570e52d6`, conflicts on exactly the author's three files (`evidence/merge_tree_develop.txt`):
  - `ks1384-fb-sweep.test.ts` (add/add) and `ks1293-originate-suite-is-hermetic.test.ts`: neither is in this delta (`evidence/merge_tree_conflict_vs_delta.txt`).
  - anchoring `index.ts`: **one conflict, and it IS inside this delta's hunk.** It is the two-line `createOwnCreateLookup` import (delta `@@ -37,0 +38,2`; merged lines 38-42). Both sides added the neighbouring imports (`createWalletLabelScan`, `driveTimer`) after `dc8c210c`, and the ours side is empty. The resolution is one-sided: keep the import.
  - The delta's other `index.ts` hunk (the own-create route, `@@ -907,0 +910,44`) merges clean.
  - The yaml auto-merges; the author's "merge-tree tree `42351766c9ad`, not conflicted, 0 marker lines" for the yaml matches.
- **At `3d036184` (END):** see "Merge onto develop" at the top.
  - The plain merge-tree is rc 1 on 18 files (squash artefacts).
  - With `b86dcf7f5` as the base, rc 0, and 50/52 delta files byte-identical to `ecfe4f07`. Condition (c).

## SPARK (run first)
- **`spark_gate.sh`**, base `develop`, R2b's three new originate unit files (`ks1384-r2b-readers`, `-resolver`, `-verify-heals`), `--work /private/tmp/gate70_spark_work`, run AFTER the `@secuura/shared` build (rc 0). Result (`evidence/spark/spark_gate.stdout`):
  - rc 0. Merge-base `dc8c210c`, so the diff is the whole train: `{'files': 107, 'added': 12766, 'deleted': 824}`.
  - **HEAD: 32/32** (3 files).
  - BASE: `files_ok 0`, 1 passed / 6 failed. Two files do not compile, because `anchorResolution` and R2b's symbols are absent on develop. That is true, and says nothing about this delta.
- **`spark_review.py`** on the 31d1..ecfe delta, with the commit messages as the body (`gh` is not available from this seat). **Four runs, none valid:**
  - Run 1 (default per-file cap): `HTTP Error 400` (`evidence/spark/review_delta_run1_http400/`). The prompt was 2,071,781 chars; the server's `max_model_len` is 384000 tokens.
  - Run 2 (cap 40000): HTTP 400 (`…run2_cap40000_http400/`).
  - Run 3 (cap 12000, 292,909 prompt tokens): two repetition aborts (`…run3_cap12000_repetition/`).
  - Run 4 (cap 8000, 177,939 prompt tokens): two repetition aborts (`evidence/spark/review_delta/`). `SCHEMA FAILURE x2`, rc 4.
  - The cap lowering is my deviation. It truncated the full-text section; the delta diff (368,326 chars) was complete in every run.
- **Calibration** on the unique claims in the raw partial outputs (runs 3 and 4):

| Spark claim (partial, invalid run) | Gate 70 | Calibration |
|---|---|---|
| Step 3 / the resolver can confirm with a LOOSE transaction ("found without the bound check") | `ownCreate.ts` returns `found` only from `isBoundMatch`; `readOwnCreateBody` requires a 64-hex `bound.tx`, else not-answered (OC-malformed-found: 503) | Noise |
| The own-create gate does not refuse a foreign tenant (`!gate.allow` not checked) | It does: `!gate.allow ‖ …` gives 404 | Noise |
| A probe fault makes the gate fail open, so a lookup runs for any id (an oracle) | True by code, and stated in its comment. What leaks is chain facts of the platform's public wallet | Partial |
| The cache has no tenant dimension | True, but the gate runs before the cache, so only the fail-open case reaches it (as above) | Partial |
| A truncated scan, then a later complete one, pays | False: a complete scan finds the bound or loose tx and refuses (K-loose) | Noise |
| The legacy ±2 ms rule is not applied in step 3 | False: `ownCreateTimestampsOf` sends anchoredAt ±2 ms (`anchorStateSync.ts:116-122`) | Noise |
| The binding is only id, hash and timestamp | That is the design, to the millisecond | Noise |
| own-create is read-only | True | True (note) |

- **Spark missed:** G70-F1 (the only MINOR), G70-F2 (the instrument), G70-F3's busy-window half, G70-F4, and the develop conflict on this delta's hunk.
- **Score:** 1 true, 2 partial, 5 noise, from invalid runs. No verdict was produced, so there is no agreement to score.

## NOT TESTED (plain)
- **A real anchoring service end to end with originate.** Every probe uses a loopback fake. own-create's real scan (`walletLabelScan`) against a real wallet, Blockfrost latency, and the 4 s budget's real coverage were not run (G70-F3 is by code).
- **Real Cardano.** Rows were confirmed by hand. The wallet is a list in the fake. Lease expiry was forced by backdating `retryClaimedAt`.
- **The poller's real heal latency** (KS-1918), and any verify route at runtime: D3 was checked by code and by W's unit cells only.
- **Which clients present `blockchain.network`** (G70-F1's reach).
- **The anchoring image's install layout** (G70-F6).
- **The VM's `.env`** (actual `CARDANO_NETWORK` values; the secrets rule). The descriptors are as gate 68 read them, READ ONLY.
- **The live PR body.** Read from the seat's local copy only (G70-F5 iv). `gh` was not used.
- **W's 65 mutants and the red-before of W's 77 new cells.** Not re-run.
- **The scratch merge onto develop:** not built. Conflicts as in "Merge onto develop".
- **Node 24 LTS.** Everything ran on **Node v26.8.1, which is not an LTS line** (`evidence/node_version.txt`).
- eslint, the docs-fragments check, the four platform suites (Schemathesis, Akto, Playwright, k6), the shell suites, a running stack, any chain or box.
- **Concurrency of step 3 against a holder's outcome write.** Covered by one parallel shape only (OC-par).
- **The own-create cache** (found 10 min, none 30 s, not-answered 60 s) **and its key.** Not exercised at runtime.
- **A document whose `content_hash` changes in place** (G68-F3's reachability, still untraced).

## HOW
- **Clone:** `repo/`, made with `git clone --shared --no-checkout` from gate 65's clone (`evidence/clone.log`, rc 0).
  - The push URL is `no_push_qa_gate`. A promisor with filter blob:none, `core.sshCommand` = the Blockchain deploy key.
  - Refs were fetched into `refs/gate/*` (`evidence/fetch.log`).
  - `git rev-parse --show-toplevel` was asserted equal to the clone before every fetch and write. `repo/` is gitignored (`.gitignore:257`).
- **Delta measured:** `52 files changed, 3432 insertions(+), 589 deletions(-)` (`evidence/delta_stat.txt`).
  - 31d146678 and b86dcf7f5 (`b86dcf7f54ee95576882f98afc7e0c5617c27212`) are ancestors of the head: `merge-base --is-ancestor` rc 0 for both.
  - Seven commits (`evidence/delta_log.txt`, messages in `evidence/commit_msgs.txt`).
- **Install:** `npm ci --ignore-scripts` (1795 packages, rc 0), then the `@secuura/shared` build (rc 0) and the Prisma generate (rc 0), all before Spark (`evidence/npm_ci.log`, `shared_build.log`, `prisma_generate.log`).
- **DB:** container **gate70-pg** (postgres:15-alpine, `127.0.0.1` random port, `max_connections=1000`; `scripts/db_setup.sh`).
  - Init came from scratch copies of the repo's `docker/init` and `docker/init-platform`.
  - Migrations ran inside the container with the repo's `scripts/run-migrations.sh`: `applied=57, failed=0` (`evidence/migrate.log`).
  - Passwords were generated by `openssl rand` into the scratchpad `pw.env` (0600) and scrubbed from every log (counted 0 in `migrate.log` and `pg_init.log`).
  - Cells ran as `secuura_app`; the superuser was used for seeding only.
  - The container is **stopped**: `gate70-pg Exited (0)` (`evidence/pg_stop.log`). gate65-pg (`Up 7 hours`, still up from gate 65) and gate68-pg (`Exited (0)`) were not touched; gate65-pg is Wednesday's call.
- **Jest/vitest:** `scripts/jest_run.sh`, copied from gate 68 (nice 10; waits while load1 > 8, which it did for long stretches; load1 was 5-14 throughout). `--runInBand` for single files, 2 workers for the units. One job at a time, chained (`scripts/chain_probes.sh`, `scripts/queue2.sh`). No timeout-only red occurred.
- **Probes:** each was copied into `src/__tests__` for its run only by `scripts/probe_run.sh`, then moved to the scratchpad `_quarantine_2026-11-01/`. Nothing was deleted.
  - probe70's first head run failed to compile (TS6133, an unused helper in my file; `evidence/probe70_head_app_run1_TS6133.log`). That was my instrument fault. It was fixed and rerun, and the base and head runs used the same sha256.
- **Author's files** were read only from `!CODING/Secuura/Blockchain/5_Project_History/2026-10-31_seatW-14th/evidence/r2b/` and copied into this gate folder (`evidence/probe_author_copies/`, `evidence/pr/`).
- **End state:**
  - `git status --short` in the clone is empty (`status lines: 0`), and no probe file remains in `src/__tests__` (`evidence/git_status_end.txt`).
  - The quarantine holds 11 moved probe copies.
  - A scan of `evidence/`, `scripts/` and this file for either gate70 password finds **0 files**. The same grep on the scratchpad `pw.env` finds 1, so the scan can see one.
- **Time split:** setup ~20%, test design and execution ~55%, investigation ~25%.
