---
date: 2026-11-01
type: pickup
scope: SECUURA + all general/generic work. Datasec is TUESDAY's (Mac mini).
status: live
supersede: REPLACED WHOLESALE 16:5x AEDT by the 14:4x successor seat. The previous version (14:4x) is kept as NEXT-PICKUP.md.pre-1101-1650. Replace wholesale; never stack.
---

# NEXT PICKUP — Sun 1 Nov 2026, 16:5x AEDT, amended 17:3x (14:4x seat, ctx ~50%)

## 17:3x UPDATE (read first; supersedes the R 70th section below where they differ)
- Gates 76/77/78 all GO WITH NOTES: #1891 (968757f1), #1892 (b17ef440), #1893 (276564a7). R 70th PATCHes the notes into the bodies, files KS-1924 (G76-F2, filed) and the pre-existing '202 for an unsaved export' defect if unticketed, then wraps. Score R 70th at its wrap.
- **SEAT B 71st LAUNCHED 17:32 (%53, Opus 5.5)** to merge #1891 -> #1892 -> #1893, one head-pinned GO each (brief `briefs_staged/2026-11-01_seatB71_ks1868_merge_1891_1893.md`). Wednesday owes: its plan confirmation, then one GO per PR after each MERGED mail (pre-GO checks as in RULES).
- After the three merge: re-run Spark O45-P1..P4 (minting.service.ts), now unblocked; then a raise seat for the held O43/O44 passes plus O45.

## Live heads (Wednesday's ls-remote 16:49)
- develop `85c56a3d1eb92c8399dcfd3d6ee2a717cf356428`.
  - Today's KS-1868 batch merged on top of b1fb5436: #1887 f8a7eb41, #1888 a781c692, #1889 4d60ec77, #1890 85c56a3d (Seat B 70th, one head-pinned GO each).
- Open on KS-1868: #1891 (R 70th, head 968757f1). Gate 76 is RUNNING (Sonnet subagent, workdir `0_Brain/reference/2026-11-01_gate76-ks1868-nft-1891`).

## RULES IN FORCE (before any GO)
- **Before a merge GO:**
  - check there is no un-MERGED GO of mine outstanding;
  - `push_queue.sh list`;
  - grep each queued seat's brief for the forward-move rule;
  - re-read the pin and the head by ls-remote.
- **Subjects:** a GO or ANSWER subject ends `(Seat <L> <N>th)`. An ANSWER subject starts `ANSWER: <mirrored topic>`. `send_brief --kind answer` adds nothing to the subject.
- **Gate launches:** every gate launch is followed by a one-line STATUS mail to the PR's author.
- **Spark claims:** a "Spark is working" claim to Kam cites a done.md row or a run dir, never `spark_status.py`. That tool only sees queue-drained rounds; hand-run operator rounds do not move it.
- **Asks to Kam:** before asking Kam anything in chat, run the prior-rulings search the card gate runs (`decision_queue.sh list ruled` plus a subject grep). On 2026-10-28 Kam ruled `wed-spark-drafting-cost-1028` = b, "Keep briefing as today": Spark operators are authorised even at 86%. Seat-brief drafting at >=80% is still Wednesday's own work (model-routing P3).
- **Receipts:** the send, the tap and the note go in separate calls, and the receipt is pasted from the output file.

## SECUURA / KINTSUGI: train deploy round (Seat D 48th, %50, Opus 5.5, ctx ~47%)
- **Disk ruling:** Kam ruled the disk card `secuura-kintsugi-disk-train-round-rollback-images-1101` = a at 15:07:20. Recorded and DELIVERED in the GO KINTSUGI mail.
- **Deletion done:** 577/577 rmi; images 537 -> 63. The k14/k13/k12 rollback sets (33 images each), `dev-*:latest` and the 35-container census are all unchanged.
- **Prune done:** reclaimed 23.75 GB. Free disk is 199,086 MB.
- **Build:** BUILD k15 launched 05:24:50Z. Target b1fb5436, NOT re-pinned: the 4 KS-1868 merges ship next round, my ruling, silence = proceed. 28 images in 14 batches, then SWAP 27 with api-gateway last. demo-service is held. New rollback set pre-20261101k15 = 33.
- **Next from D:**
  1. verify_build, contentfp, the gates;
  2. network-equality gate (originate and anchoring `CARDANO_NETWORK` equal);
  3. tenant precondition: `MULTI_TENANCY_ENABLED` plus the tenant status counts, reported before the swap;
  4. swap and verify;
  5. **STATUS B: Wednesday ACCEPTS it, then scores D.**
- **Demo is a SEPARATE step** after STATUS B, on Kam's word per the demo rules. The October deploy grant stands "until further notice", but the prune card said demo OUT.
- **After STATUS B:** a facts-only KS-1384 comment, only on Wednesday's word (D's brief).

## SECUURA / RAISE: Seat R 70th (%52, Sonnet 5.5, ctx ~51%)
Brief: `2_Project_Files/fleet/briefs_staged/2026-11-01_seatR70_raise_ks1868_o41.md`. Three PRs, nothing merges:
- **PR 1 = #1891** nft-certificate O41-P1, tier 2, READY 05:47Z, gate 76 running.
  - Flag for the gate: `ensureFreshParams` has no try/catch; an unreadable value now keeps the cached params instead of rejecting out of the mint path. The gate is asked whether that is safe and whether tier 2 holds.
- **PR 2** demo-service state.ts O41-P2: built and proven (head b17ef440), push queued.
- **PR 3** analytics O42 x2: built and proven (head 276564a7), push queued.
  - R's caller finding (operator 42 was wrong): `dbSaveExport` has 4 callers that propagate. It is in PR 3's body for its gate.
- **Owed by Wednesday:**
  - a tier-2 Sonnet gate per READY, with a STATUS mail to R each time;
  - gate notes back to R (it PATCHes the body, no push);
  - then a lane -B MERGE seat with head-pinned GOs, one per PR (Seat B 70th's brief is the template: `briefs_staged/2026-11-01_seatB70_ks1868_merge_1887_1890.md`);
  - score R at its wrap.
- Watch R's ctx: 51% at 16:46.

## SPARK: held passes waiting for a raise (after R 70th)
- **O43-P1** demo-service persona.ts:77 (POST /persona/switch). **TIER 1** by Wednesday: demo persona login, identity territory.
- **Governance batch, ONE PR, tier 2:**
  - O43-P2 governanceService.ts:219 (first round A7 tsc 'Abort trap', re-run PASS, undiagnosed);
  - O44-P1..P4 at :255/:313/:342/:448.
  - O44-P2 is tree-identical, not byte-identical (the model dropped the first `diff --git` line).
  - No two hunks are within 3 lines. The five COMBINED are unmeasured.
  - The raise seat traces callers before claiming "never reaches a response".
- Reports: `0_Brain/reference/2026-11-01_spark-operator4{1..5}/report.md`. Wednesday wrote 43 and 44 from the operators' messages; 45's is in the note only.
- **O45-P1..P4** minting.service.ts (:129, :90, :504, :584), callers traced:
  - BLOCKED at dry-run rc 2 by #1891 (build_input refuses KS-1868 while any KS-1868 PR is open). Unproven since a template fix.
  - Re-run when R 70th's PRs merge or close.
  - dbSaveNFTCertificate (:90) is NOT a 'callers swallow' site (mintNFT's catch returns classifyMintError's message).
- **IMPROVEMENTS row (16:5x):** the per-ticket open-PR gate blocks an umbrella ticket. A file-level check for listed umbrella tickets is designed, NOT built. Build and red-proof it before arming.
- **The Spark is IDLE, blocker measured:** every KS-1868 brief is blocked by an open KS-1868 PR, and today's screens found no other class briefable.

## KAM
- **Cards waiting on Kam:** 0.
- **Ruled today:**
  - 00:18 x3;
  - 10:04 plan a;
  - 10:05 x4;
  - 14:03 third prune a;
  - 15:07 disk a.
  All delivered.
- **Told on the panel:**
  - the four merges;
  - the disk freed;
  - the Spark honest answer plus a correction (a false 'round live' line);
  - the withdrawn operators question (already ruled 10-28) plus a miscount correction.
- His 15:08 question "is the Spark constantly working?" was answered honestly: no, idle 06:21 -> 15:05. Ledger w=4 regression. **The wake on every spark/done.md row is STILL OWED (enforcement).**

## OWED (not yet done)
- **Enforcement owed (ledger w>=3):** a wake_watch leg firing on every new spark/done.md row.
- **Live test inputs to quarantine** once the train is VERIFIED on kintsugi (W 15th asked): s-w13-pg, gate65-pg, the train worktrees, /private/tmp/w14, /private/tmp/w15. Quarantine, never delete.
- spark_gate.sh: build packages/shared first. mk_wt ref-fingerprint race. Three STANDING_LINES "highest + 1" mentions.
- spark_status.py: read done.md's newest row, not only queue rounds.
- INDEX.md refresh. Linear check (not done this seat).
- **Boot finding:** the by-tier digest is 662 KB and cannot be read whole in one turn. This seat read lines 1-2998 only, plus the ledger whole.
- **No-cd hook** may not be armed in Secuura seat panes (B 70th and R 70th both used cd at boot without a refusal). Unverified.
- **Datasec/ATTIO digest** misrouted to wednesday-agent@: Tuesday's, do not read the bodies.
