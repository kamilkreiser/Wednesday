# DRAFTER-REPORT: Seat W 78th brief (KS-2366 legacy certification repair, design then build), 2026-11-27

Brief: /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-27_seatW78_ks2366_repair_design_build.md
What I touched: no box, no ssh, no keyscan, no mail, no post, no launch. GitHub reads were read-only `gh api` calls as kksecura. Under !CODING I used git read verbs only. The source files I read are saved in my scratchpad at /private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/23d4d320-ba8d-40d8-b71d-f351bda82b71/scratchpad/w78src/ and the PR census at /private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/23d4d320-ba8d-40d8-b71d-f351bda82b71/scratchpad/w78_prfiles.txt.
Size: about 37 KB, slightly over the 35 KB aim. The extra is mostly the PROVENANCE absolute paths and the code-reading section, which you asked to keep.

## COMMISSION FACTS I MEASURED AS WRONG
None is materially wrong. Three need care, and one changes a claim the seat must make.
1. **"The answer changes from false to true for 46 records" is true only on Kintsugi.** Demo runs REVISION d4ffc8308249. By gh compare, d4ffc8308249 is an ancestor of develop 4764b2cfbc28 (ahead_by 51, behind_by 0), so demo has NOT got KS-2366. Its verify still uses the presence test, so **all 37 demo certifications answer `blockchainAnchored` true TODAY**, the failed-and-simulated one included (by reading the code; not measured live). On demo the client-visible sequence depends on order:
   - deploying KS-2366 alone flips 37 from true to false;
   - deploying it together with a repair leaves 36 true and flips 1 from true to false.
   The brief states this and marks it as Kam's and Stuart's to rule.
2. **The ruling time.** The live-board row reads 2026-11-27T13:05:14.362+11:00, which matches the commission. The store's `ruled_ts` is 2026-11-27T13:05:58.078926+11:00. Both are quoted, so nobody "corrects" one to the other.
3. **"Read W 77th's brief and wrap for the mechanics"** holds, with one nuance. The best donor tree is now `s-w77-fix`: it sits at dbceb300851b with tree 6ec6995d0d0a, which equals 4764b2cfbc28's tree per the 1126 card's delivered_artefact, and porcelain reads 0. That is better than W 77th's own donor, `s-w76-dev`, which is on an older base.
- Checked and TRUE:
  - develop = 4764b2cfbc28768ef9c7b684e2af2e0f2f1438e5 (unmoved; PR 2295 merged with that merge commit; one parent 59e89c87719e);
  - the four touched originate files (plus a test, the fragments and the new module: 10 files);
  - `writeCertificationAnchorConfirmedIf` is the real name;
  - the ordinal: 78th 0, 77th 1, 76th 2; W 77th wrapped 2026-11-26;
  - S128, S129, S130 and D88 figures as the commission states them (37; 36+1; 47 same-row; 10/10; census 10/1/0 and 161/2/3; live verify false with the buckets unchanged);
  - W 77th q_plan lines 28, 44-45 and 74 say what the commission says;
  - routing row C3 reads Opus 1st.

## WHAT THE CODE AT 4764b2cfbc28 SAYS (originate paths under Blockchain/Dev/services/originate/src/)
**Why an old row cannot bind**
- `services/anchorResolution.ts:107-115` `isBoundToCreate`: line 111 binds by `createAttempts` when the blob has that array. Lines 112-114 are the legacy rule: `anchoredAt` within ±2 ms of the row's `payloadTimestamp`. Old certification blobs have `anchoredAt: null` (`routes/certifications.ts:613`; the same shape at c50d033c6 per the S129 drafter report) and no createAttempts (introduced at `certifications.ts:619`, KS-2366). So the function returns false.
- `anchorResolution.ts:130-134`: a confirmed row with a 64-hex tx that is NOT bound sets `lookupIfNone = 'anchor_failed'` and goes to own-create (143).
- `services/ownCreateClient.ts:68`: with zero timestamps it returns `not-answered` at once. `anchorStateSync.ts:116-122` `ownCreateTimestampsOf` returns [] when there are no createAttempts and no anchoredAt. Result: `{write:'none'}` (152).
- `services/certificationAnchorSync.ts:76-79`: a non-confirmed decision writes nothing. The reconcile (135-148) runs only for a stale in-flight blob with a bearer, so each party GET costs one anchor read and nothing changes (gate 420's G420-1). The poller (100-128) starts only at issue and recertify (`certifications.ts:776-777`, `1688-1689`), so it never reaches an old row.

**The writer**
- `repositories/certificationRepo.ts:435-462`: `writeCertificationAnchorConfirmedIf(id, tenantId, anchorId, blob)` sets `metadata.blockchain` and `certification_metadata.blockchain` to the blob, carrying `threadToken`, and sets `updated_at = NOW()`.
- Its WHERE (456-460): `id = $id::uuid AND external_id IS NULL AND tenant_id = $t::uuid AND blob->>'status' IS DISTINCT FROM 'confirmed' AND blob->>'anchorId' = $anchorId`.
- It never touches status, writes no event and makes no charge.
- The blob is `confirmedBlobOf` (`anchorStateSync.ts:135-151`): `{threadToken?, createAttempts?, txHash, blockHeight, anchoredAt, network, status:'confirmed', anchorId}`, which drops `confidence` and `anchoringStatus`.
- For a certification, `metadata` is `{}` at insert (`certificationRepo.ts` insertCertificationRow), so the write ADDS `metadata.blockchain`.
- `saveCertification` (295-327) writes a `certification_events` ISSUE or REVOKE_DOCUMENT row on every save (304-318). A repair through it would forge an ISSUE event.

**Re-anchor: can the blob's `anchorId` go stale? No, by construction. That is exactly why the same-row agreement proves less than it seems.**
- Anchoring `services/anchoring/src/index.ts:1537-1757` `dbPersistAnchor` runs `INSERT ... ON CONFLICT (document_id, network) DO UPDATE SET` (1590). The SET list holds status, transaction_hash, block_hash, block_number, slot, fee, confirmations, confirmed_at, error_message, retry_count, simulated, a guarded `metadata_payload` CASE and updated_at.
- **`id` is not in it, and neither is `content_hash`.** `RETURNING id` (1666) hands back the EXISTING row's id. The comment at 1548-1551 says: "On a re-anchor of the same (document, network) this returns the EXISTING row's id".
- So an anchor row keeps its id for ever on one network. Any certification's blob `anchorId` and its own id will ALWAYS reach the same row, whether or not the row was later overwritten.
- **The 47-of-47 agreement therefore proves the link and nothing about which attempt or event the confirmation belongs to.** S 129th's and S 130th's "WHAT THIS CANNOT SHOW (a)" says the same thing from the data side.
- Status and transaction hash are overwritten on EVERY re-anchor. The payload is overwritten only under the KS-1385 guards (ownership guard, equal content hash, equal anchor type). The tx that `processAnchorDriven` (2046-2047) submits comes from the row's stored payload at that moment, since it reads the row by id.

**Who could re-anchor an existing certification id**
- Within `routes/certifications.ts` there are exactly two `POST /api/anchors` calls (669 issue, 1606 recertify). Both use a FRESH uuid (issue `id` at 475; recertify `newCertId` at 1614). So originate's certification routes never re-anchor an existing certification.
- NOT searched by me:
  - `documents.ts` (and whether its retry route can address a certification's primary key);
  - other services;
  - Platform S and other connectors (anchoring's KS-1603 guard refuses only a CROSS-tenant write, so a same-tenant caller can POST with any documentId);
  - anchoring's own retry, reconciler and attempt-family code.
- That list decides whether "same row confirmed" can be read as "this create confirmed". The brief makes it the seat's first Phase A job.

**Evidence that could bind an old row more tightly (my reading; each needs proof)**
- The GET `/api/anchors/:id` (972; 1022-1041) returns `documentId`, `createdAt`, `contentHash` and `payloadTimestamp`. In SQL the same value is `metadata_payload->'secuura'->>'timestamp'`. On a fresh insert, one `Date` is both the payload timestamp and the row's `created_at` (507-514).
- The issue route mints `now` at 476, before the anchoring POST (669), which is bounded by `AbortSignal.timeout(10000)` (687). So an issue-era create's payload timestamp should fall in [the certification's issuedAt, issuedAt + about 10 s] (`issuedAt` is `certified_at`). That is a candidate legacy binding, derived from code.
- What it must check: that the timeout and ordering held in every era back to 2026-07-31; that it is handled separately for recertify, whose POST has no timeout; and how it handles clock skew between containers.
- It also partly answers W 77th's A5 objection ("an event's payload can sit on it"): a replaced payload carries a LATER timestamp. It does not cover a KEPT payload with a new transaction. The seat must read `submitAnchorToChain`'s idempotency guards to settle that.

**Reach**
- A code rule heals only on a party GET with a bearer. `syncCertificationAnchor:60` refuses an empty bearer, and anchoring's GET is behind its JWT and KS-1822 gate per W 77th q_plan line 30.
- A sweep therefore needs a user token or a new service credential. The latter is a security-surface change and Kam-class.
- A data repair can join `documents` to `anchor_store` in SQL, because both live in the one `secuura` database on each box (S 129th and S 130th read both tables in one session).

**Precedents in the repo**
- `Blockchain/Dev/migrations/055_ks1557_backfill_connector_create_for_versioned_documents.sql`: a backfill done AS A MIGRATION, three gate rounds, ending in "corroboration is required" and "the child's own record is never sufficient on its own".
- `Blockchain/Dev/scripts/backfill-subject-deks.js`: `BACKFILL_DRY_RUN=true`, idempotent, log sentinels.
- The brief keeps a migration as a STOP, because a migration runs on demo and production at their next deploy.

## EVERY FACT IN THE BRIEF
| fact | source | read today? |
|---|---|---|
| Kam live row 13:05:14.362, the text | command read: kam_msgs.sh 8 --source live | yes |
| card title, BLUF, option a detail, ruled_ts 13:05:58, default b | command read: decision_queue.sh show secuura-ks2366-repair-old-stuck-certifications-1127 | yes |
| what-anchored-means card label, detail, ruled_ts, delivered artefact incl. tree 6ec6995d0d0a | command read: decision_queue.sh show secuura-ks2366-what-anchored-means-1126 | yes |
| develop 4764b2cf..., parent, 10 files; PR 2295 merged | command read: gh api commits/develop, commits/4764b2cf, pulls/2295 | yes |
| demo d4ffc830 behind develop by 51 | command read: gh api compare | yes |
| 13 open PRs, 96 rows, 0 watched hits, control 2 (PR 2099) | command read: gh api pulls and pulls/n/files, paginated | yes |
| ordinal 0/1/2, W 77th heading line 47, newest W folder 77th | command read: grep over /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/history.md; ls | yes |
| gh account kksecura | command read: gh auth status under the project GH_CONFIG_DIR | yes |
| every code line in the brief's code section | API read: gh api contents at 4764b2cf, saved under my scratchpad w78src | yes |
| backfill precedents 055 and backfill-subject-deks.js | API read: gh api contents of migrations and scripts | yes |
| W 77th's finding (q_plan 28), writer and sync (44-45), stuck rows (74), A5/A6 (72), JWT gate (30) | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-26_W77_q_plan.txt | yes |
| W 77th's licences, design approval, 10th path | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-26_W77_answer_plan.md, /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-26_W77_answer_path10.md | yes |
| hook verdict 13/16, 817 s, jest 3770/3770, KS-278 | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-26_W77_ready.txt | yes |
| trees, kit names, traps | /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-26_seatW-77th/HANDOVER.md; ls of its tools and tools/newbranch | yes |
| vault push needs a wrap licence | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-26_W77_answer_wrap.md | yes |
| s-w77-fix at dbceb300851b, tree 6ec6995d0d0a, porcelain 0 | command read: git log -1 and git --no-optional-locks status in that tree | yes |
| G420-1, -3, -4, -5, -6, -7, -8 | /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-26_gate420-tier1-ks2366-cert-anchored-confirmed/verdict.md | yes |
| demo 37 stuck, 29 document-class submitted | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-27_S128_status_number.txt | yes |
| demo 36+1, anchorId 37, createAttempts 0, same row 37 | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-27_S129_status_number.txt | yes |
| Kintsugi 10/10, census 10/1/0 and 161/2/3 | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-27_S130_status_number.txt | yes |
| live verify false, buckets unchanged, audit +1, charges 0 | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-27_D88_status_c.txt | yes |
| D 88th's wrap row 10 (G420 ticket is Wednesday's) | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-27_D88_wrap.txt | yes |
| the link derivation | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-27_seatS129_demo_anchor_read.md section 1 and its DRAFTER-REPORT | yes |
| S 130th kit path kint_anc_s130.sh | command read: ls of /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-27_seatS-130th/tools | yes |
| routing C3 line 93 (O55 1st, S55 no), C4 line 94 | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/specs/model-routing.md | yes |
| opus id claude-opus-5-5 | /Volumes/DevMASTER/WEDNESDAY/0_Brain/dashboard/data/models_latest.json | yes |
| other Secuura seats wrapped (S128, S129, S130, D88) | history.md top entries (command read) | yes; liveness not checked by ps |
| three WEDNESDAY build seats in other folders | the commission | carried, not measured |

## NOT MEASURED
- The callers that can re-anchor an existing certification id outside `routes/certifications.ts`.
- `buildFlatAnchorMetadataPayload`'s fields: whether the payload names the certification.
- The era-by-era issue code and timeout from 2026-07-31.
- The 47 stored payload timestamps against their certifications' issue times. That needs a box read; the brief routes it into the design or the script's dry-run manifest.
- Which anchoring revision Kintsugi runs and whether its GET returns `payloadTimestamp`.
- Whether any of the 10 Kintsugi certifications has expired (the G420-6 race).
- `submitAnchorToChain`'s idempotency guards.
- KS-2366's Linear state today (no Linear read; my licence covers none).
- Any test run at 4764b2cfbc28.
- Live seat processes.

## QUESTIONS FOR WEDNESDAY
1. **Demo's order of events.** Demo answers true for all 37 today (by reading). Should the brief tell the seat to design for KS-2366 and the repair reaching demo TOGETHER (36 stay true, 1 flips), and to flag that as Kam's and Stuart's? Or leave the order wholly to the later demo card?
2. **Phase A depth vs a box read.** The strongest legacy binding I can see, the stored payload timestamp inside the issue window, cannot be proven without a read-only box read of the 47 rows. Do you want Phase A to end by recommending an S-seat read first, or to build the check into the script's dry-run manifest and the code rule's refusal (no new read before Phase B)?
3. **Branch and ticket order.** Should a board seat file the repair ticket BEFORE Phase B, so the branch uses Linear's `branchName` per project CLAUDE.md? Or does the seat build under `Refs KS-2366` with the drafter-suggested branch name?
4. **The throwaway Postgres and the base-clone config writes.** The brief has the seat ASK for both in the plan QUESTION, as W 77th did. Pre-rule them in the STAMP to save a round trip?
5. **Size.** The brief is about 37 KB against your 35 KB aim. Cut the PROVENANCE code-line row or the code section further, or accept it?
