---
date: 2026-10-20
type: pickup
scope: SECUURA + all general/generic work. Datasec is TUESDAY's; FRIDAY (laptop) works both and claims before driving.
status: live
supersede: REPLACED WHOLESALE by the 11:1x Wednesday seat at its 70% checkpoint (12:1x AEDT). Replace wholesale again; never stack. Previous versions: git history of this file.
---

# NEXT PICKUP (Tue 20 Oct, written 12:1x AEDT by the 11:1x seat)

## 0. FIRST ACTIONS FOR THE NEXT WEDNESDAY SEAT
1. Boot reads as the launcher says. Then kam_rulings_today.sh, reconcile_rulings.py, `tools/fleet_ack.sh list`, `tools/decision_queue.sh list open`, `fleet/usage_gate.sh --check`, `local-model/spark/tunnel.sh check`, `tmux list-panes -t fleet:0 -F '#{pane_id} #{@cockpit_name}'`.
2. Verify every merge by fetching into `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/src` with the LITERAL path (a `$VAR` path is refused by the no-cd hook; wrap multi-command git in `bash <<'EOF'`). Fetch `refs/pull/N/head` before a merge-tree on a head the clone lacks. `cockpit.sh say` takes the cockpit NAME; `pane_close.sh` takes the `%ID`. Zoom before any raw keypress.
3. send_brief/brief_and_launch need `WED_AGENT=wednesday`. Subjects never carry hold/stop/checkpoint. Send, tap and note are THREE separate calls. Push: commit own files by pathspec, `tools/safe_pull.sh`, then `git push`. A card's prior-ruling gate: plain add first, read every match, search Kam's words with `tools/kam_msgs.sh`, then `--override-prior-rulings` with the reason in the BLUF.
4. Every gate verdict: `sed '1d;$d' verdict.md | shasum -a 256` must equal its trailer (whole-file control differs). Gate briefs now say "trailer written LAST and self-verified" (BV1's failed; BX1 superseded it).
5. In force: Kam 10-18 new-account grant, routing v1.0, the October deploy grant EXTENDED "until further notice", the TESTED merge grant, merge-and-archive grant. Gauge 75% at 12:1x (80-90 band not reached).

## 1. LIVE FLOOR (12:1x) — develop = 108091b2e1c1c9d4b486213b6424ebfe88ef9332 (#1660)
Merged today, each verified by a Wednesday fetch: #1645 #1646 #1648 #1647 #1649 #1650 #1651 #1652 #1653 #1658 #1656 #1655 #1657 #1660 = 14. Kintsugi runs 89956fe92956 (D 25th, verified from outside); demo d75bfe2deb80. Demo smoke key key_66e82ef0 REVOKED (card delivered).
- **#1659 KS-1659 (G 12th): GO sent 01:15Z** at head 97eaffe0d300, landing 5633c8d50584 on 108091b2e1c1 (gate BX1 Opus tier 1, hash verified). Expect G's MERGED mail -> verify by fetch. G then files ONE **High** ticket: GET /api/certifications/:id has NO ownership check (any same-TENANT user of ANY organisation reads any certification; pre-existing, demo too) + owner-less rows skip documents.ts:1124's cloak. **Its remedy is a design on an auth read path: plan -> rule (Kam's KS-1116 ruling is the precedent) -> build tier 1. Kam told on the panel (corrected to same-TENANT).**
- **GATE RUNNING: BY1** (Sonnet, tier 2) = #1661 KS-1558 m4 (G 12th, head 7ecb3257ec69), brief `0_Brain/reference/2026-10-20_gate-BY1-pr1661-ks1558/GATE_BRIEF.md`.
- **R 59th (%21, still claude-opus-5; Sonnet switch owed at a ZOOMED idle, three attempts found it busy):** item 2 logger PR pushed (next PR number, likely #1662: it also pins `e.secret !== ''` with a two-entry cache), then BP1 NB1/NB2, then **KS-1687 build approved, tier 1** (fallback in toTokenResult; claim only "capable of persisting"). KS-1689 is on Kam's card.
- **G 12th (%20, ctx ~70%+):** #1659 merge + the High ticket, then KS-758 on default (b), then the BT1 N1 test-only PR (X1/X2/X3 + BX1 N3 cell).
- **Lanes EMPTY:** C (KS-1557 r3 and KS-1688 wait on Kam) and D (wrapped 0.93; next kintsugi round is a later decision: develop has moved past 89956fe92956).
- Scored today by this seat: R 58th 0.92, C 31st 0.88, D 25th 0.93.
- **Spark:** pool exhausted per SCREEN_20. Ornith idle: accepted (Kam 10-09).

## 2. KAM'S CARDS
- OPEN (Secuura), each with a panel line: `secuura-ks1557-055-second-nogo-round3-1020` (rec a round 3, default c HOLD); `secuura-ks758-erasure-log-subject-ref-1020` (rec c hash, default b category-only); `secuura-ks1689-m365-failed-signin-status-1020` (rec d derived flag, default d).
- On (a) for KS-1557: launch a C seat for round 3 from C 31st's handover (`!CODING/Secuura/Blockchain/5_Project_History/2026-10-20_seatC-31st/HANDOVER.md`), then an Opus delta gate. KS-1688's fix waits for #1654.
- Ruled, delivery OWED: `secuura-ks1688-org-merge-edge-which-side-1020` = a (the KS-1688 fix seat posts it); `secuura-m365-admin-setup-for-customer-org-1020` = b (KS-1678 future work).

## 3. OWED BY WEDNESDAY (in order)
1. G's #1659 MERGED -> verify; the High read-gap ticket key -> plan request when G has room.
2. BY1 verdict -> hash, merge-tree on live develop, GO or round.
3. R 59th's READYs (item 2 tier 2; KS-1687 tier 1) -> gates; Sonnet switch at an idle.
4. Kam's taps on the three open cards -> act per section 2.
5. Fable 5.1 coordinator trial (routing decision 7) still OWED.
6. At the wrap: regenerate BOTH digests only if a lesson FILE was edited (none today: ledger only); the 05:30 ledger archive.
