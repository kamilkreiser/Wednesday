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

## FLOOR at 10:18 (pane list) — ROTATION HANDOVER from the 08:07 successor seat (ctx 78%)
- **KAM'S 25-MINUTE WINDOW (opened 10:15 on the panel, bf-a7adfd373371):** Wednesday re-pinned the DEMO deploy to develop 07a2d62be6a0 (adds PR 2005 KS-1959 + PR 2004 KS-1986) on the reading that his 07:08:39 'deploy everything now ... both systems have all changes ... new demo rule takes affect after this deploy' covers anything merged before this deploy lands. If Kam objects before the swap: mail D 52nd to stay at e899463d2a0b (it holds the e899 build) — run kam_msgs.sh FIRST at boot.
- **D 52nd** %152 (Opus): demo deploy, NEW PIN 07a2d62be6a0 (ANSWER 23:15:43Z, SUPERSEDES the e899 pin). Rebuild originate + vc-issuer (~25-30 min from 23:16Z), re-rsync 5 paths, regenerate expectations; 0 new migrations; 056+057+058 with Kam's tenant-less count re-read (0 earlier); swap 27 (api-gateway last); 30-min KS-1244 watch; REVISION at 07a2d62be6a0; STATUS B. ctx 59% at 10:15. Holds GO DEMO: floor lines ride its next ACK. AFTER THIS ROUND: NO demo redeploy without Kam's word.
- **S 19th** %159 (Sonnet): filings a-f, brief briefs_staged/2026-11-05_seatS19_filings.md. Expect plan confirmation (priorities it chose; Stuart-confirmation note on item c is a NOTE in the ticket, never a contact). Verify every filing on the board before counting it.
- MERGED TODAY (all verified by ls-remote): PR 2002 (058) 4ff25fb4f2c0, PR 2003 KS-1958 e899463d2a0b, PR 2005 KS-1959 17abf8ee98a5, PR 2004 KS-1986 07a2d62be6a0 (= develop). Card 1105 ruled a + DELIVERED. KS-1991 = G192-F1.
- WRAPPED + scored this seat: B 93rd 0.93, K 14th 0.95, F 33rd 0.96, B 94th 0.94. Panes closed. No gate running.

## THEN (owed, in order)
1. KINTSUGI round (D 53rd, Opus, October grant extended) for develop 07a2d62be6a0 = 058 + PR 2003 + PR 2005 + PR 2004, AFTER D 52nd STATUS B; tenant-less charge count read before 058 and reported; post-deploy keys KS-1401, KS-1958, KS-1959, KS-1986 (all In Progress until their deploy check): a D 53rd deploy seat from D 51st/D 52nd records; tenant-less charge count read before 058, reported to Kam; kintsugi first is satisfied by prior rounds, but Kam said BOTH systems get everything now.
2. Filing seat: durable revocation 'accept and retry' (+ G194-F3 wording), KS-1958 memory-fallback readers (K 14th wrap searches). Close-out seat after D 52nd STATUS B: post-deploy keys (KS-1256, 1561, 1459, 1458, 1868 slices; KS-1234 NOT-RUN on both boxes, NODE_ENV development; KS-1233 needs the key; KS-1401 after 058 lands).
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
