# BLUF — Gate 9 is back. (1) The QuickQuote retention purge is GO: MERGE it to QuickQuote main, then STOP (publishing is Kam's typed word). (2) VSP-65 is NO-GO on ONE Major (VSP65-F1): build the fix as round 2 of 2 under the cap, to a new READY FOR QA. (3) File two tickets for the pre-existing findings. Then wrap.

**Addressed to the cockpit seat `Datasec/Vision_Sales_Portal`.** No other Vision seat is live. You are the merge author for both repos.

## AUTHORITY
- Merges on Tuesday's GO after a gate verdict at the head: Tuesday's delegated merge scope (Kam's v1.3 signed grant, 2026-08-07: merges are Tuesday's to authorise). Kam's new-account login 2026-09-27 ~08:2x AEST, verbatim: *"New account logged in. Please keep going with the work."*
- The gate-9 report is the evidence: `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/vision/reports/2026-09-27-vision-gate9-vsp65-qqpurge/report.md`. Read it WHOLE first.

## RULED BY KAM, NOT YET IN AN ARTEFACT
- Publishing QuickQuote to production stays Kam's TYPED word. Nothing in this brief publishes.

## RULED BY TUESDAY FOR THIS PROJECT, STILL OPERATIVE
- The gate-9 NODE20 and AZURITE legs ran on images already present (DOCKER-PULL-NEVER); keep that rule for any re-run.

## HELD (production is live here: datasec-sales-portal-rg and hpas-quickquote are production)
No deploy, no publish, no production change, no Key Vault or app-setting change, nothing to any human but Tuesday. Never kill by pattern (kill by a pid from your own ancestry, or by port plus cwd).

## ITEMS
1. **MERGE the QuickQuote purge (GO @ ac74111).** Re-read `git ls-remote` for main and `fix/qq-retention-purge-no-literal-2026-09-27` first. The gate predicted main `f255db8` + ac74111 = ac74111's own tree (clean). If main or the head moved, STOP and mail. Merge without rebasing. Before pushing, re-run the gate's list for the merged head: stage3 `npm test` as sets, `test:azurite`, the 1,005-row pagination cell, quote-engine. Check that the push to main does NOT publish or deploy: quote the trigger lines of every workflow that runs on a push. Mail MERGED with the new main sha and the sets.
   - **QQ-O3 (the version question), ruled:** the `CONFIG.toolVersion` rule in QuickQuote's CLAUDE.md (:32-35) is about the client tool's badge and document footer, and the purge does not change the client tool. So it is not a miss under that rule. stage3's own version practice (stage3/package.json, the image tag chosen at publish) is yours to state from its history. Follow it, and say in MERGED what you did.
   - Carry QQ-P1, P2 and P3 (Polish) as ONE BACKLOG line. They do not block the merge.
2. **VSP65-F1 fix, round 2 of 2 (tier 1).** The gate MEASURED it four times: after an instance restart, a stall on the first session-store query rejects connect-pg-simple's cached table-creation promise (10.0.0 index.js:198-204), and every later signed-in request on that instance gets a 500 while /api/health stays 200. The gate's fix-shape is in prose and UNVERIFIED by me (verify it before you build on it): do not let that cache hold a failure, e.g. `createTableIfMissing:false` with the session table created by schema.sql/initDb, or retry the ensure. Your PRIOR-WORK CHECK decides which is right.
   - Red-first: the gate's S8d restarted-instance transient-stall cell, red at 2adfc4a and green after, plus a control showing MAIN's recovery behaviour is kept.
   - Also close the two test gaps: VSP65-P1 (a cell that pins GUARDED) and VSP65-P2 (a behavioural cell under M3).
   - This is the LAST round under the cap: a third NO GO goes to Kam.
   - READY FOR QA with branch, head sha, sets not counts, PRIOR WORK and NOT TESTED.
3. **Tickets (Jira VSP, facts only):**
   - (a) VSP65-O1 (Major, pre-existing at main): link death while a `pool.connect()` caller holds its client causes an uncaughtException, and the process exits. Fix-shape: an 'error' listener for the checkout's lifetime.
   - (b) VSP65-O3: server-side statement, lock and idle-in-transaction timeouts, with the gate's evidence. Mark it "decision: Tuesday or Kam". Do not build it.
   - Name both keys in your STATUS.

## REPLY
Plan confirmation first (`[Datasec/Vision_Sales_Portal -> Tuesday] QUESTION: plan confirmation`), and start the read-only parts without waiting. Then MERGED for item 1, READY FOR QA for item 2, and one STATUS mail for item 3. Your local Postgres (5433, the compose db) is up from the gate: leave it up. Wrap when done; Tuesday retires the pane by hand.

PROVENANCE:
- verdicts VSP65 NO-GO @ 2adfc4a, QQPURGE GO @ ac74111; F1, O1, O3, P1-P3, QQ-O3 | gate-9 verdict mail + report FINDINGS INDEX (report.md :412-460) - the gate's words, read by Tuesday | read 2026-09-27 10:0x
- heads: portal main eaf024a, fix/vsp-65 2adfc4a; QuickQuote main f255db8, fix/qq-retention-purge ac74111 | git ls-remote origin in both repos by Tuesday | read 2026-09-27 10:0x
- QuickQuote version rule | your own Quoting Tool/hpas-quoting-tool/CLAUDE.md :30-36, read by Tuesday | read 2026-09-27 10:0x
- class cap two NO GO rounds | Kam 2026-09-05 20:19 ruling (learnings/2026-09-05_qa-gate-tiers-and-the-two-nogo-cap.md) - Tuesday's file, not yours | read 2026-09-27
Self-check note: item 1 merges and stops before publish; item 2 ends at READY FOR QA; item 3 files tickets only.
SELF-CHECK: re-read end-to-end for contradictions | 2026-09-27 10:29
