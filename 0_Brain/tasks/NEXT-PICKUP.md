---
date: 2026-11-05
type: pickup
scope: SECUURA + all general/generic work. Datasec is TUESDAY's (Mac mini).
status: live
supersede: REPLACED WHOLESALE 07:14 AEDT 2026-11-05 by the 06:00 morning seat (70% checkpoint). Previous kept as NEXT-PICKUP.md.pre-1105-0714. Replace wholesale; never stack.
---

# NEXT PICKUP — Thu 5 Nov 2026, 07:14 (the 06:00 morning seat)

## KAM TODAY (live board, view=wednesday, read with kam_msgs.sh; all three RULED in the store, HTTP 200)
- 07:07:25 "Decision wed-morning-fleet-activity-1105: a — Plan stands" -> KS-1986's merge hold RELEASED (merges after its tier-1 gate + Wednesday's GO). Delivered into the F 32nd brief before send (verified at the destination inbox).
- 07:08:03 "Decision secuura-ks1401-058-merge-demo-billing-1104: a — Merge; I stop every demo redeploy until you say".
- 07:08:39 "but deploy everything now.  so both systems have all changes.  new demo rule takes affect after this deploy".
- WEDNESDAY'S READING (panel bf-e8c5f03ff094, correction offered, none yet): merge PR 2002 now; THIS round brings BOTH kintsugi and demo to everything merged INCLUDING 058; the demo stop starts after this round; each box reads its tenant-less charge_events count before 058 and it is reported with the deploy (not waited on).
- AFTER THIS ROUND: NO demo redeploy without Kam's word. Write that STOP into every later Secuura deploy brief.
- Standing: Spark IGNORED until he says (11-04 16:42); October deploy grant extended until further notice; 11-04 09:16 'clear and close as many in progress tickets as possible'.

## FLOOR at 07:5x (pane list) — ROTATION HANDOVER (80% band)
- **D 52nd** %152 (Opus): demo deploy. Built the 28 at 035685291b9d (14 batches; ~3 pairs done by 07:37, slow on demo). NEW PIN 4ff25fb4f2c05192be178f941d746175d609471f SENT ~20:50Z (PR 2002 squash, tree 2286e8f66d227a11b19aa7ffacf488a91d9665c7, 1 parent 035685291b9d): rebuild only the 1-squash delta's images (expect migrations + originate), re-rsync --checksum, read demo's tenant-less charge_events count BEFORE 058, apply 056+057+058 (tracker 56 -> 59), swap 27 api-gateway last, 30-min KS-1244 watch with instant rollback, STATUS B. This pin only. demo-service excluded; Stripe test; floor stop = card Kam for a one-off demo cache prune. Its ctx was 51% at ~07:17: if it nears 75% before the swap, it finishes the swap or rolls back, then a D 53rd takes over from its HANDOVER.
- **B 93rd** %155 (Sonnet, ctx 64% at 07:52): PR 2002 MERGED (squash 4ff25fb4f2c0, 20:48:29Z); PR 1383 CLOSED after it (comment 6641773758). Now PR 2003 (KS-1958, head 8b140178276457116714892fe0cf73b9f1e92c8c): recompute onto develop 4ff25fb4f2c0, Gate 191 notes (F1 inside the cost; F2 = KS-1959 pre-existing; F3 filing candidate; F4 noted), READY TO MERGE -> Wednesday's GO 'GO: merge PR 2003 at 8b1401782764 on develop <pin12> (Seat B 93rd)' with the expected tree from its READY. Pre-GO: ls-remote + kam_rulings_today + gate_stray_check + no outstanding GO. Wraps at ~80%.
- **GATE 192** (Opus Agent subagent, background, TIER 1) on PR 2004 (KS-1986, head 577f668f478679a3e4965a28fba6b96a9e2212d6, built on 035685291b9d; develop 4ff25fb4f2c0): workdir 0_Brain/reference/2026-11-05_gate192-ks1986-pr2004/ (commission.md, ready_2004.txt). **A ROTATION KILLS IT. If verdict.md is ABSENT when you boot, RE-COMMISSION it from commission.md (same Agent prompt shape as gate 191's: read commission whole, workdir only, verdict.md line 1).** On GO WITH NOTES: QUEUE PR 2004 to the merge seat (B 93rd or its successor B 94th) after PR 2003, and REQUIRE the squash message to EXCLUDE the commit body's stale 'HOLD: do not merge ...' line (read back after the merge). Kam already RELEASED the hold (07:07:25). On HOLD-FOR-KAM: card him.
- F 31st 0.93, F 32nd 0.96 FINAL, both panes closed.

## THEN (owed, in order)
1. KINTSUGI round for the new develop (PR 2002's 058 + any later merges): a D 53rd deploy seat from D 51st/D 52nd records; tenant-less charge count read before 058, reported to Kam; kintsugi first is satisfied by prior rounds, but Kam said BOTH systems get everything now.
2. Close-out seat after D 52nd STATUS B: post-deploy keys (KS-1256, 1561, 1459, 1458, 1868 slices; KS-1234 NOT-RUN on both boxes, NODE_ENV development; KS-1233 needs the key; KS-1401 after 058 lands).
3. KS-1959 fail-closed FIX (gate 191 F2, HIGH pre-existing: a revoke whose DB UPDATE fails answers 200 and still verifies true; same family as Kam's 1103 rulings): a build seat, tier-1 gate. Also a filing seat: (c) verify-file passes 'sha256:<hex>' to crossTenantLookup vs registry content_hash (production form UNMEASURED; F 32nd, verification.ts:900/934/783); gate 191 F3 (by-hash 500 on a hostile value, LOW); E 35th's five gate-189 candidates (0_Brain/reference/2026-11-04_gate189-ks1256-pr2001/ready_2001.txt) + F 31st's two (vc-issuer sibling read catches; certifierOrganizationId on existing cross-tenant paths, KS-590 a).
4. KS-1990 fresh-stack run. KS-911/912 launcher by-hash. CONTRIBUTING N/13 vs 16 (Stuart's KS-1366, Kam's call).
5. Carried: @azure/msal-node baseline dies MON 2026-11-09 (check its ticket); WED-155 (inbox_digest key in argv); INDEX.md refresh (last 10-27); stash@{0} never drop.

## SCORED TODAY
- F 31st 0.93 FINAL (PR 2003 raised; PR-B handed over). %153 closed.

## RULES APPLIED THIS SEAT
- A Kam ruling that changes a staged brief is written INTO the brief before it sends, and the sent copy is checked at the destination inbox.
- A Kam scope change mid-round goes to the running seat as a SUPERSEDES mail naming the mail and items it replaces; an earlier mail overtaken within minutes is named too.
- Subjects never carry stop/hold/checkpoint after the leading token (send_brief refuses).
- Launch at FULL = a waiter with rc on its own line (scratchpad f32_waiter.sh shape), never a chained launch.
