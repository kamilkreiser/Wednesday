---
date: 2026-10-20
type: pickup
scope: SECUURA + all general/generic work. Datasec is TUESDAY's; FRIDAY (laptop) works both and claims before driving.
status: live
supersede: REPLACED WHOLESALE by the 11:1x Wednesday seat at its 50% checkpoint (11:2x AEDT). Replace wholesale again; never stack. Previous version: git history of this file (commit before 11:2x).
---

# NEXT PICKUP (Tue 20 Oct, written 11:2x AEDT by the 11:1x seat)

## 0. FIRST ACTIONS FOR THE NEXT WEDNESDAY SEAT
1. Boot reads as the launcher says. Then kam_rulings_today.sh, reconcile_rulings.py, `tools/fleet_ack.sh list`, `tools/decision_queue.sh list open`, `fleet/usage_gate.sh --check`, `local-model/spark/tunnel.sh check`, `tmux list-panes -t fleet:0 -F '#{pane_id} #{@cockpit_name}'`.
2. Verify every merge by fetching into `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/src` with the LITERAL path (a `$VAR` path is refused by the no-cd hook; wrap multi-command git in `bash <<'EOF'`). `cockpit.sh say` takes the cockpit NAME; `pane_close.sh` takes the `%ID`. Zoom before any raw keypress.
3. send_brief/brief_and_launch need `WED_AGENT=wednesday`. Subjects never carry hold/stop/checkpoint. Push: commit own files by pathspec, `tools/safe_pull.sh`, then `git push` (safe_push.sh takes a message + paths; it is for uncommitted files).
4. In force: Kam 10-18 new-account grant, routing v1.0, the October deploy grant EXTENDED "until further notice", the TESTED merge grant, merge-and-archive grant. Gauge 72% at 11:2x (80-90 band not reached).

## 1. LIVE FLOOR (11:2x) — develop = f4259b8ed3875316a269d3228031c198eec39edd (#1656)
Merged today, each verified by a Wednesday fetch: #1645 #1646 #1648 #1647 #1649 #1650 #1651 #1652 #1653 #1658 #1656 = 11. None deployed by today's merges. Kintsugi runs a4187f0f6622 (D 25th's round of 89956fe92956 in progress); demo d75bfe2deb80.
- **GATES RUNNING (Agent, background, Opus):** **BS1** = #1655 KS-1407 round 2 DELTA (G 12th, head 893506989ae7; round 2 of 2: a NO GO ships nothing and goes to Kam as a card), brief `0_Brain/reference/2026-10-20_gate-BS1-pr1655-ks1407-r2/GATE_BRIEF.md`; **BT1** = #1657 KS-1157 OAuth session marker (G 12th, head a7de040ab040, round 1), brief `0_Brain/reference/2026-10-20_gate-BT1-pr1657-ks1157/GATE_BRIEF.md`. On each verdict: sha check (`sed '1d;$d' | shasum -a 256` vs trailer + whole-file control), heads via ls-remote, `git status` strays (gate_stray_check runs in the GO path), own merge-tree on live develop, notes copied FROM verdict.md, then GO/ANSWER to G. #1655 and #1657 are file-disjoint (G's claim; BT1 asked to confirm): whichever merges second will STOP if develop moved, so re-GO as for #1656 today.
- **#1654 KS-1557 (C 31st):** round 2 committed cbf31d40d652 (055 attributes each child from its own versionedById; committed proof cell 12/12 on real PG; N2 bypass-or-refuse), push in its hook. On READY: DELTA gate (Opus, tier 1, round 2 of 2). Wednesday ACCEPTED C's call to credit the 6 `connector:api-key` children (forward fix writes the same value), to be named in the PR body for the gate. Verdict of round 1: `0_Brain/reference/2026-10-20_gate-BN1-pr1654-ks1557/verdict.md`. KS-1688's fix waits for #1654 to MERGE.
- **R 59th (%21, LAUNCHED 11:22, Sonnet C2):** brief `fleet/briefs_staged/2026-10-20_seatR59_successor_ks1682_round.md` (KS-1682 test-only round: W6 + startsWith/endsWith/empty-id cells; BL1 N4 logger swap; BP1 NB1/NB2; KS-1687 + KS-1689 PLAN-first, KS-1689 is a product question to card for Kam). OWED: verify at rung 5+ on its plan confirmation; switch %21 to `claude-sonnet-5-5` at a ZOOMED idle and mail it.
- **G 12th (%20):** after the two gates: KS-1659 (tier 2), KS-758 F9 (tier 1, erasure-log identifier question), KS-1558 m4 (tier 2).
- **C 31st (%18, ctx 65% at 11:1x):** #1654 round 2; then wrap when its band says.
- **D 25th (%17, Opus 5.5):** kintsugi round of 89956fe92956 (healthy +67 min at 00:00Z, 8 of 33 images); then migrations 053/054, swaps, sweep, DEPLOYED mail with both rounds' notices drafted -> Wednesday's word to post (Peter KS-485, Stuart KS-772).
- **R 58th WRAPPED** 00:13Z: scored 0.92, pane %19 closed (listeners 24 -> 24), handover `!CODING/Secuura/Blockchain/5_Project_History/2026-10-20_seatR-58th/HANDOVER.md` (381 lines).
- **Spark:** screens 19-20 done; all held passes in G's queue; pool needs a deeper read or new tickets. Ornith idle: accepted (Kam 10-09).
- **Demo-upgrade impact report** (Stuart's question): `0_Brain/reference/2026-10-20_demo-upgrade-impact/REPORT.md`; WhatsApp draft given to Kam; offer of a KS-695 comment only on his word.

## 2. KAM'S CARDS
- All of today's taps (13 rows, newest 10:52:08) are ruled and actioned; reconcile 0 at 11:25.
- Ruled, delivery OWED: `secuura-demo-smoke-key-revoke-after-measure-1020` = a (REVOKE key_66e82ef0 on demo, a small demo job AFTER D 25th's kintsugi round; then tell Kam, mark delivered). `secuura-ks1688-org-merge-edge-which-side-1020` = a (the KS-1688 fix seat posts it on KS-1688 and builds K's receiving end). `secuura-m365-admin-setup-for-customer-org-1020` = b (lives in KS-1678's future work).
- Open cards: only Datasec's composer-l05 (not this seat's).

## 3. OWED BY WEDNESDAY (in order)
1. BS1 / BT1 verdicts -> GO or round handling to G (see section 1).
2. C 31st #1654 READY -> delta gate (Opus); after #1654 MERGES: brief the KS-1688 fix (tier 1 Opus): gate /version on the (a') create:connector provenance; post Kam's ruling (a: S adds a 'transfer issuer' call; K builds the receiving end); Stuart's KS-1688 comment 23:36:46Z is the spec input.
3. R 59th plan confirmation -> rung-5 check, model switch, rule KS-1687 shape; KS-1689 options -> a card for Kam with a default.
4. D 25th DEPLOYED mail -> verify -> word to post the two notices -> report the deploy to Kam on the panel -> the demo smoke-key revoke.
5. Model switches still owed for C and G at a ZOOMED idle (low value for C near wrap).
6. Fable 5.1 coordinator trial (routing decision 7) still OWED.
7. At the wrap: regenerate BOTH digests only if a lesson FILE was edited (none so far today: ledger only); the 05:30 ledger archive.
