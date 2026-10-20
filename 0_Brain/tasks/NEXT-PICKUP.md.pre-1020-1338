---
date: 2026-10-20
type: pickup
scope: SECUURA + all general/generic work. Datasec is TUESDAY's; FRIDAY (laptop) works both and claims before driving.
status: live
supersede: REPLACED WHOLESALE by the 11:1x Wednesday seat at its rotation (~12:5x AEDT, ctx 79-80%). Replace wholesale again; never stack. Previous versions: git history of this file.
---

# NEXT PICKUP (Tue 20 Oct, written ~12:5x AEDT by the 11:1x seat at rotation)

## 0. FIRST ACTIONS FOR THE NEXT WEDNESDAY SEAT
1. Boot reads as the launcher says. Then kam_rulings_today.sh, reconcile_rulings.py, `tools/fleet_ack.sh list` (re-run `fleet_ack.sh answered "plan confirmation - Seat G 13th" "G13 plan"` once collected), `tools/decision_queue.sh list open`, `fleet/usage_gate.sh --check`, `local-model/spark/tunnel.sh check`, `tmux list-panes -t fleet:0 -F '#{pane_id} #{@cockpit_name}'`.
2. Verify every merge by fetching into `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/src` with the LITERAL path; fetch `refs/pull/N/head` before a merge-tree on a head the clone lacks. Two-landing GOs (a synthetic commit with the first PR's landing tree as tree and live develop as parent, then merge-tree) worked twice today: use them whenever two disjoint GOs are out at once. `cockpit.sh say` takes the cockpit NAME; `pane_close.sh` takes the `%ID`. Zoom before any raw keypress.
3. send_brief/brief_and_launch need `WED_AGENT=wednesday`. Subjects never carry hold/stop/checkpoint. Send, tap and note are THREE separate calls (and never write "answered"/"sent" in a note in the same call as the tool). Push: commit own files by pathspec, `tools/safe_pull.sh`, then `git push`. Cards: plain add first, read the matches, search Kam's words with `tools/kam_msgs.sh`, then `--override-prior-rulings` with the reason in the BLUF.
4. Every gate verdict: `sed '1d;$d' verdict.md | shasum -a 256` must equal its trailer; gate briefs say "trailer written LAST and self-verified".
5. In force: Kam 10-18 new-account grant, routing v1.0, the October deploy grant EXTENDED "until further notice", the TESTED merge grant, merge-and-archive grant. Gauge 76% at 12:4x (80-90 band not reached).

## 1. LIVE FLOOR (12:5x) — develop = 7e3b9362e08b1b5b2c418f43e05c9bd0616f896e (#1662)
Merged today, each verified by a Wednesday fetch: #1645 #1646 #1648 #1647 #1649 #1650 #1651 #1652 #1653 #1658 #1656 #1655 #1657 #1660 #1659 #1661 #1662 = **17**. Kintsugi runs 89956fe92956 (D 25th); demo d75bfe2deb80; demo smoke key REVOKED (card delivered). **No gate running at handover.**
- **R 59th (%21, claude-sonnet-5-5 since ~12:3x, switched by Wednesday at an idle):** building **KS-1687 shape B (fallback + forceCache)**, ruled 12:4x; on READY -> a **tier-1 OPUS gate** that must prove each account gets its own token at the larger forceCache-populated cache size (KS-1682's defect came from that same shared cache) and fail closed on a shared id. Then item 3 (BP1 NB1/NB2 test-only), then the BZ1 N1-N3 test-only follow-up. KS-1689 on Kam's card.
- **G 13th (%22, claude-opus-5; switch to claude-opus-5-5 owed at a zoomed idle):** #1661 merged (item 0). Building item 2 (test-only PR: BT1 X1/X2/X3 + BX1 N3 cells, tier 2); then KS-758 on default (b) (card still OPEN at 12:4x; it re-asks before finalising; no merge without a GO naming the card state); then KS-1692 PLAN (wait for Wednesday's ruling before building).
- **KS-1695 (High, filed by G 12th):** same-tenant read gaps (GET /api/certifications/:id has no ownership check; owner-less rows skip documents.ts:1124's cloak). Remedy = a design on an auth read path: commission a PLAN (Opus seat or drafter), then card Kam, KS-1116's ruling as the precedent. Kam already told on the panel.
- **Lanes empty:** C (KS-1557 r3 + KS-1688 wait on Kam's card), D (next kintsugi round is a later decision: develop is well past 89956fe92956 now, 17 merges today; consider proposing a deploy round to kintsugi under the October grant once the open gates settle).
- Scored today by this seat: R 58th 0.92, C 31st 0.88, D 25th 0.93, G 12th 0.89.
- **Spark:** pool exhausted per SCREEN_20; Ornith idle accepted (Kam 10-09).

## 2. KAM'S CARDS
- OPEN (Secuura), each with a panel line: `secuura-ks1557-055-second-nogo-round3-1020` (rec a round 3, default c HOLD); `secuura-ks758-erasure-log-subject-ref-1020` (rec c hash, default b category-only); `secuura-ks1689-m365-failed-signin-status-1020` (rec d derived flag, default d).
- On (a) for KS-1557: launch a C seat for round 3 from C 31st's handover (`!CODING/Secuura/Blockchain/5_Project_History/2026-10-20_seatC-31st/HANDOVER.md`), then an Opus delta gate. KS-1688's fix waits for #1654.
- Ruled, delivery OWED: `secuura-ks1688-org-merge-edge-which-side-1020` = a (the KS-1688 fix seat posts it); `secuura-m365-admin-setup-for-customer-org-1020` = b (KS-1678 future work).

## 3. OWED BY WEDNESDAY (in order)
1. R 59th's KS-1687 READY -> tier-1 Opus gate with the cross-account condition above.
2. G 13th's item-2 READY -> tier-2 gate; KS-758 card state when it re-asks; KS-1692 plan -> rule.
3. KS-1695 plan commission -> card to Kam.
4. Kam's taps on the three open cards -> act per section 2.
5. Model switch for G 13th to claude-opus-5-5 at a zoomed idle.
6. Fable 5.1 coordinator trial (routing decision 7) still OWED.
7. At the wrap: no lesson FILE edited today (ledger only), so no digest regeneration; the 05:30 ledger archive.
