---
date: 2026-10-20
type: pickup
scope: SECUURA + all general/generic work. Datasec is TUESDAY's; FRIDAY (laptop) works both and claims before driving.
status: live
supersede: REPLACED WHOLESALE by the 12:5x Wednesday seat (Sonnet 5.5) at its ~50% checkpoint (13:3x AEDT, ctx 46%). Replace wholesale again; never stack. Previous versions: git history + NEXT-PICKUP.md.pre-1020-1338.
---

# NEXT PICKUP (Tue 20 Oct, written 13:3x AEDT by the 12:5x seat)

## 0. FIRST ACTIONS FOR THE NEXT WEDNESDAY SEAT
1. Boot reads as the launcher says (the by-tier digest is ~600 KB: read lines 1-2200 whole, then the headlines list `grep -n '^## '` from 2200, then the routing/merge/rotation rules near the end; the tool caps reads per turn). Then `tools/kam_rulings_today.sh`, `reconcile_rulings.py`, `tools/newmail.sh` (seen-ids persist in /private/tmp/wed_newmail), `tools/fleet_ack.sh list`, `tools/decision_queue.sh list open`, `fleet/usage_gate.sh --check`, `local-model/spark/tunnel.sh check`, `tmux list-panes -t fleet:0 -F '#{pane_id} #{@cockpit_name}'`.
2. Verify every merge by fetching into `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/src` with the LITERAL path (a `$C` variable trips the no-cd hook). Gate verdict: `sed '1d;$d' verdict.md | shasum -a 256` equals its trailer; move any stray file a gate leaves (verdict.md.tmp) to the scratchpad quarantine.
3. send_brief / brief_and_launch need `WED_AGENT=wednesday`. Subjects never carry hold/stop/checkpoint. Send, tap (`cockpit.sh say "<cockpit NAME>" "<pointer>" --mail "<subject substring>"`) and note are THREE separate calls; a note must not say posted/sent in the same command as the send (receipt guard). brief_and_launch demands: provenance `fact | source | read YYYY-MM-DD`, a ticket-state line for every ticket in the QUEUE, a `RULED BY KAM, NOT YET IN AN ARTEFACT` heading, and a SELF-CHECK line copied from the gate's own print.
4. In force: Kam 10-18 new-account grant, routing v1.0, the October deploy grant "until further notice", TESTED merge grant, merge-and-archive grant. Kam 13:0x terminal: "spark connected. please use it as well".

## 1. LIVE FLOOR (13:3x) - develop = 3a6f1810981e3e268e77d0e4721987d186b71810 (#1665); Secuura merges today 18
Merged and verified by fetch: #1645 #1646 #1648 #1647 #1649 #1650 #1651 #1652 #1653 #1658 #1656 #1655 #1657 #1660 #1659 #1661 #1662 #1665. Kintsugi at 89956fe92956 (D 25th); demo d75bfe2deb80; no deploy seat live.
- **R 59th (%21, Sonnet 5.5, ctx 70%):** #1663 round 2 GO sent (head be16bd6a4e87, landing 38200e78045e on 3a6f1810981e; subject must drop the `(#1663)` suffix) -> verify R's MERGED by own fetch. THEN KS-1687 round 2 on #1664 (gate CB1 GO WITH NOTE, I ruled round 2 with the snapshot guard, before-read inside the catch, N3 comment fix, near-miss cells with Account entities, tier-1 Opus gate, round 2 of 2), THEN the BZ1 N1-N3 follow-up (built, unpushed, worktree 8409e0291). R will cross 80% soon: rotate it with a successor brief when it wraps.
- **G 13th (%22, Opus 5, ctx ~45%):** #1665 merged. KS-758 option (b) built, push in flight (card still OPEN, default b; tier-1 gate; the GO must name the card state). OWES a High bug ticket (facts only, source-read): GET /api/gdpr/deletion-log is an unfiltered SELECT over a table with no tenant_id column, ORG_ADMIN-readable = cross-tenant. Then KS-1692 plan. Model switch to claude-opus-5-5 still owed at a zoomed idle.
- **C 32nd (%23, Opus 5, ctx ~27%):** KS-1695 PR 1 (certification reads: GET /:id, /lineage, /evidence-bundle bound to issuer/holder/platform admin; ONE new test file; tier 1). Plan confirmation answered; it files a transferee/E2E-spec ticket. Model switch to claude-opus-5-5 owed at a zoomed idle. On READY: tier-1 Opus gate (brief from PLAN section 5 and the C 32nd brief cells).
- **Spark screen 21 (Sonnet sub-agent, background):** brief 0_Brain/reference/2026-10-18_spark-screen/SCREEN_21_BRIEF.md, writes SCREEN_21.md; read every diff at source before any hold_ready.
- No gate running except none: CA1 CB1 CC1 CD1 all returned.

## 2. KAM'S CARDS (OPEN)
`secuura-ks1557-055-second-nogo-round3-1020` (rec a, default c); `secuura-ks758-erasure-log-subject-ref-1020` (rec c, default b; AMENDED 13:2x with G's deletion-log finding); `secuura-ks1689-m365-failed-signin-status-1020` (rec d, default d); `secuura-ks1695-ownerless-records-who-reads-1020` (AMENDED 13:1x after Stuart's KS-1695 comment: rec b, default c; Stuart prefers fail-closed/admins+creating connector after #1654). On KS-1557 (a): launch a C seat for round 3 (C 31st handover `!CODING/Secuura/Blockchain/5_Project_History/2026-10-20_seatC-31st/HANDOVER.md`) then an Opus delta gate. Ruled, delivery owed: `secuura-ks1688-org-merge-edge-which-side-1020` = a (KS-1688 fix seat posts it); `secuura-m365-admin-setup-for-customer-org-1020` = b (KS-1678 future work).

## 3. OWED BY WEDNESDAY (in order)
1. R's #1663 MERGED -> own-fetch verification, then score.
2. G 13th's KS-758 READY -> tier-1 gate (card state in the GO); its deletion-log ticket.
3. C 32nd READY -> tier-1 gate; then plan the gap-2 build only after Kam's KS-1695 card.
4. R's KS-1687 round 2 READY -> tier-1 Opus gate (condition: the near-miss ids at the larger cache; guard closes N1+N2).
5. Spark screen 21 result: read SCREEN_21.md whole, read each product diff, hold_ready, then a raise seat (Sonnet) + gate.
6. Model switches (G 13th, C 32nd) to claude-opus-5-5 at zoomed idles; Fable 5.1 coordinator trial (routing decision 7) still OWED.
7. STANDING_LINES line (claim via wed_claim): `searchIssues` returned 12 hits for a nonsense control term, so a hit list from it proves nothing (G 13th's catch).
8. Stuart's 10:34 message (dev-ps ahead of UAT, wants demo-pk upgraded) was answered by the demo-upgrade impact report; KS-1688 fix waits for #1654 (KS-1557).
9. At the wrap: no lesson FILE edited so far today (ledger only; ledger rows owed: nothing new from this seat yet), so no digest regeneration unless a lesson is filed; the 05:30 ledger archive.
