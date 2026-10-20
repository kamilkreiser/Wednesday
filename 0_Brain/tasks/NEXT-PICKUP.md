---
date: 2026-10-20
type: pickup
scope: SECUURA + all general/generic work. Datasec is TUESDAY's; FRIDAY (laptop) works both and claims before driving.
status: live
supersede: REPLACED WHOLESALE by the 09:0x Wednesday seat at its 50% checkpoint (~09:30 AEDT). Replace wholesale again; never stack. Previous: NEXT-PICKUP.md.pre-1020-0930 + git.
---

# NEXT PICKUP (Tue 20 Oct, written ~09:30 AEDT, sections 0-3 refreshed 10:16 and 10:38 and 10:56 and 11:01 and 11:08 (rotation))

## 0. FIRST ACTIONS FOR THE NEXT WEDNESDAY SEAT
1. Boot reads as the launcher says. Then kam_rulings_today.sh, reconcile_rulings.py, `bash 2_Project_Files/tools/newmail.sh` (to a file), `tools/fleet_ack.sh list`, `tools/decision_queue.sh list open`, fleet/usage_gate.sh --check, `local-model/spark/tunnel.sh check`, `tmux list-panes -t fleet:0 -F '#{pane_id} #{@cockpit_name}'`.
2. **Mail outage RESOLVED ~09:34 AEDT (403 window ~09:23-09:34, cause unmeasured); all staged answers SENT.** History: OUTBOUND MAIL WAS BROKEN (since ~22:2xZ 10-19 = ~09:2x AEDT):** every send from wednesday-agent@ returns HTTP 403 {"message":"Forbidden"}; reads (GET) are 200; the same key sends from coagent@ (400 validation on an empty probe = authorised). Last good send 22:17:48Z. Sent log: 218 sends on 2026-10-19 UTC. Cause UNMEASURED (daily cap is a guess). Kam told on the panel (bf-d7e5f45f37d8) with default "retry at checkpoints and after 00:00Z (11:00 AEDT); no sending as another inbox". **Probe without sending:** POST messages/send with `{"to":[]}` -> 403 = still blocked, 400 = recovered. **On recovery, send IN ORDER:** (a) `fleet/briefs_staged/2026-10-20_answer_seatD25_plan_confirmed_UNSENT.md` to Secuura/Blockchain-D, `--kind answer`, subject "ANSWER: plan confirmation (Seat D 25th) confirmed - model now Opus 5.5", then `fleet_ack.sh answered "Seat D 25th kintsugi"`; (b) `..._answer_seatR58_plan_confirmed_UNSENT.md` to Secuura/Blockchain-R, subject "ANSWER: plan confirmation (Seat R 58th) confirmed - build cache left alone"; tap each by cockpit NAME with --mail. Rename the files without _UNSENT after.
3. Verify every merge by fetching into `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/src` (literal path). `cockpit.sh say` takes the cockpit NAME; `pane_close.sh` takes the `%ID`. **Zoom before any raw keypress**; read a waiting seat unzoomed with `capture-pane -S -60`.
4. send_brief needs `WED_AGENT=wednesday` in this seat's shell. Subjects never carry hold/stop/checkpoint words.
5. In force: Kam 10-18 new-account grant, routing v1.0, the October deploy grant EXTENDED "until further notice", the TESTED merge grant. Gauge 66% at 09:29.

## 1. LIVE FLOOR (10:56) — develop = 6229a92f2480f0784c31a8d6b652298a7ac10551 (#1653)
Merged today, each verified by Wednesday's own fetch: #1645 #1646 #1648 #1647 #1649 #1650 #1651 #1652 #1653 = 9. None deployed. Kintsugi runs a4187f0f6622 (round of 89956fe92956 in progress); demo d75bfe2deb80.
- **#1654 KS-1557 (C 31st): gate BN1 NO GO** (11:00; code sound, migration 055 can credit a child to the wrong connector). Round 2 of 2 under the cap sent to C: attribute from each child's own metadata.versionedById (connector-only, agree with any parent row, skip+report), N2 bypass-or-refuse, N3 committed proof on real PG, N4 no rows for humans, N5 ticket, N1 measurement as a KS-1688 comment. Verdict 0_Brain/reference/2026-10-20_gate-BN1-pr1654-ks1557/verdict.md. On READY: a DELTA gate (Opus, tier 1, round 2 of 2); a second NO GO goes to Kam. KS-1688's fix still waits for #1654 to MERGE.
- **GO'S OUT, AWAITING MERGES (no gate running; all four gates of the 09:0x seat finished):** #1656 KS-1679 stale cell (C 31st) GO at head 2e672d35fedf, landing f5386b66b067 on 6229a92f2480 (gate BQ1); #1658 KS-1682 N1 cells (R 58th) GO at head 2d1417f44c24, landing 8de5df50f813 on 6229a92f2480 (gate BR1). Both GO'd on the SAME develop with disjoint files, so WHICHEVER MERGES SECOND WILL STOP (develop moved) and needs a RE-GO: fetch refs/pull/N/head:refs/wed/prN into the cache clone, own merge-tree on live develop, re-GO naming the new landing and "supersedes". Verify each MERGED by your own fetch. R 58th then wraps (handover 352 lines + history already written; team notes at wrap): verify on disk, score, pane_close.
- **#1655 KS-1407 (G 12th): gate BO1 NO GO** (shape for round 2 RULED 10:57: route-local isRedisAvailable guard + post-write re-assert, honest distinct errors, no session.ts change; other silent-zero callers = one High ticket) (B1: reset with Redis down burns the token and revokes nothing). Round 2 of 2 under the cap commissioned to G (fail closed before the write; N3 cells; N1 OAuth refresh-grant ticket High + N2 race ticket Medium). A second NO GO ships nothing and goes to Kam. Verdict: 0_Brain/reference/2026-10-20_gate-BO1-pr1655-ks1407/verdict.md.
- **D 25th (%17, Opus 5.5):** kintsugi round of 89956fe92956: build was healthy at +38 min; then migrations 053/054, swaps, sweep, DEPLOYED mail with both rounds' notices drafted -> Wednesday's word to post (Peter KS-485, Stuart KS-772). KS-772 heads-up already posted.
- **C 31st (%18):** #1652 merged; #1654 at BN1; #1656 at BQ1; told to keep its handover current and wait for both verdicts.
- **R 58th (%19):** #1650/#1651/#1653 merged; KS-1682 N1 exact-match cells PR in flight (tier 2 Sonnet gate when READY); KS-1687, KS-1689 filed; then wrap.
- **G 12th (%20):** #1655 round 2; then KS-1157 (tier 1; sequence after #1655 if both touch session.ts), KS-1659 (tier 2), KS-758 (tier 1, erasure-log identifier question), KS-1558 (tier 2).
- **Spark:** screens 19-20 done; all held passes in G's queue; pool needs a deeper read or new tickets.
- **Demo-upgrade impact report** for Stuart's question: 0_Brain/reference/2026-10-20_demo-upgrade-impact/REPORT.md; WhatsApp draft given to Kam (10:4x); offer pending of posting the full list on KS-695 (only on his word).

## 2. KAM'S CARDS (open, both with defaults)
- RULED 10:33 by Kam: Entra card = a (wait; delivered), smoke-key card = a (REVOKE key_66e82ef0 on demo: OWED as a small demo job AFTER D 25th's kintsugi round; undelivered until done, then tell Kam). KS-1688 card = a with a WhatsApp draft; Kam "sent"; Stuart "working through it, will update the ticket" (10:37): no KS-1688 build before his answer.
- Undelivered ruled: `secuura-m365-admin-setup-for-customer-org-1020` = b (05:35), lives in KS-1678's future work; deliver when the wizard ticket is worked.

## 3. OWED BY WEDNESDAY (in order)
1. #1656 + #1658 MERGED mails -> verify; the second one STOPS -> re-GO. #1654 round-2 READY -> delta gate (Opus); after #1654 MERGES: brief the KS-1688 fix (tier 1 Opus): gate /version on the (a') create:connector provenance; post Kam's ruling on KS-1688 (card secuura-ks1688-org-merge-edge-which-side-1020 = a: S adds a 'transfer issuer' call; K builds the receiving end); Stuart's answer (KS-1688 comment 23:36:46Z) is the spec input; mark the card --delivered when the comment is posted.
2. G 12th's #1655 round-2 READY -> delta gate (Opus, tier 1, round 2 of 2).
3. R 58th's N1 cells READY -> tier-2 gate; then R wraps (verify handover + history, score, pane_close).
4. D 25th's DEPLOYED mail -> verify -> word to post the two notices -> report the deploy to Kam on the panel.
5. Demo smoke-key revoke (card secuura-demo-smoke-key-revoke-after-measure-1020 = a, undelivered): a small demo job after D 25th's round (key_66e82ef0), then tell Kam and mark delivered.
6. Model switches to claude-opus-5-5 still owed for C, R, G at a ZOOMED idle (they keep missing idles; low value now for R/C near wrap).
7. Fable 5.1 coordinator trial (routing decision 7) still OWED.
8. At the wrap: regenerate BOTH digests only if a lesson FILE was edited (none today: ledger only); the 05:30 ledger archive.
