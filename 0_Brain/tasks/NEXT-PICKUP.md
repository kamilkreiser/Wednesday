---
date: 2026-10-20
type: pickup
scope: SECUURA + all general/generic work. Datasec is TUESDAY's; FRIDAY (laptop) works both and claims before driving.
status: live
supersede: REPLACED WHOLESALE by the 09:0x Wednesday seat at its 50% checkpoint (~09:30 AEDT). Replace wholesale again; never stack. Previous: NEXT-PICKUP.md.pre-1020-0930 + git.
---

# NEXT PICKUP (Tue 20 Oct, written ~09:30 AEDT, sections 0-3 refreshed 10:16 and 10:38)

## 0. FIRST ACTIONS FOR THE NEXT WEDNESDAY SEAT
1. Boot reads as the launcher says. Then kam_rulings_today.sh, reconcile_rulings.py, `bash 2_Project_Files/tools/newmail.sh` (to a file), `tools/fleet_ack.sh list`, `tools/decision_queue.sh list open`, fleet/usage_gate.sh --check, `local-model/spark/tunnel.sh check`, `tmux list-panes -t fleet:0 -F '#{pane_id} #{@cockpit_name}'`.
2. **Mail outage RESOLVED ~09:34 AEDT (403 window ~09:23-09:34, cause unmeasured); all staged answers SENT.** History: OUTBOUND MAIL WAS BROKEN (since ~22:2xZ 10-19 = ~09:2x AEDT):** every send from wednesday-agent@ returns HTTP 403 {"message":"Forbidden"}; reads (GET) are 200; the same key sends from coagent@ (400 validation on an empty probe = authorised). Last good send 22:17:48Z. Sent log: 218 sends on 2026-10-19 UTC. Cause UNMEASURED (daily cap is a guess). Kam told on the panel (bf-d7e5f45f37d8) with default "retry at checkpoints and after 00:00Z (11:00 AEDT); no sending as another inbox". **Probe without sending:** POST messages/send with `{"to":[]}` -> 403 = still blocked, 400 = recovered. **On recovery, send IN ORDER:** (a) `fleet/briefs_staged/2026-10-20_answer_seatD25_plan_confirmed_UNSENT.md` to Secuura/Blockchain-D, `--kind answer`, subject "ANSWER: plan confirmation (Seat D 25th) confirmed - model now Opus 5.5", then `fleet_ack.sh answered "Seat D 25th kintsugi"`; (b) `..._answer_seatR58_plan_confirmed_UNSENT.md` to Secuura/Blockchain-R, subject "ANSWER: plan confirmation (Seat R 58th) confirmed - build cache left alone"; tap each by cockpit NAME with --mail. Rename the files without _UNSENT after.
3. Verify every merge by fetching into `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/src` (literal path). `cockpit.sh say` takes the cockpit NAME; `pane_close.sh` takes the `%ID`. **Zoom before any raw keypress**; read a waiting seat unzoomed with `capture-pane -S -60`.
4. send_brief needs `WED_AGENT=wednesday` in this seat's shell. Subjects never carry hold/stop/checkpoint words.
5. In force: Kam 10-18 new-account grant, routing v1.0, the October deploy grant EXTENDED "until further notice", the TESTED merge grant. Gauge 66% at 09:29.

## 1. LIVE FLOOR (10:38) — develop = 11af03696c9bd966580e52605cb2a361d9c3d29b (#1652)
Merged today, each verified by Wednesday's own fetch: #1645, #1646, #1648, #1647, #1649, #1650, #1651 (e712972bccf1), #1652 (11af03696c9b) = 8. None deployed. Kintsugi runs a4187f0f6622; demo d75bfe2deb80. Seats C, R, G still on launcher claude-opus-5 (switch at a ZOOMED idle, mail it); D on 5.5.
- **GATES RUNNING (Agent, background), verdicts land in 0_Brain/reference/<folder>/verdict.md:** BN1 #1654 KS-1557 (C 31st, head db9bca740df0, tier 1 Opus; includes the KS-1688 interaction question); BO1 #1655 KS-1407 (G 12th, head 8e5308a87e14, tier 1 Opus); BP1 #1653 hygiene (R 58th, head b30e401ff208, tier 2 Sonnet). On each verdict: re-hash `sed '1d;$d'`, re-read heads, merge-tree on LIVE develop yourself (develop moves often today), GO naming head + landing, notes copied FROM THE FILE.
- **DEMO-UPGRADE IMPACT analysis** (Agent, Opus, background): Stuart asked (via Kam 10:34) whether moving demo-pk to latest K affects existing users/accounts; report -> 0_Brain/reference/2026-10-20_demo-upgrade-impact/REPORT.md. OWED TO KAM: a short WhatsApp reply built from that report's BLUF, "within the hour" promised at 10:35.
- **D 25th (%17, Opus 5.5):** kintsugi round of 89956fe92956, build healthy at +38 min (23:30Z), KS-772 heads-up POSTED. Then migrations 053/054, swaps, sweep, DEPLOYED mail with BOTH rounds' notices drafted -> Wednesday's word to post. wake_ack'd while waiting.
- **C 31st (%18):** #1652 merged; #1654 at BN1; next item (iii) stale #1619 cell PR (Refs KS-1679, tier 2).
- **R 58th (%19):** #1650 + #1651 merged; #1653 at BP1; next KS-1682 N1 exact-match cells PR (tier 2); KS-1687 + KS-1689 filed; then wrap.
- **G 12th (%20):** #1655 at BO1; next KS-1157 (tier 1), KS-1659 (tier 2, audit: no trusting reader), then ADDENDUM items KS-758 (tier 1, erasure-log identifier question) and KS-1558 (tier 2).
- **Spark:** screens 19+20 done; all held passes are in G's queue; SCREEN_20 says the remaining pool needs a deeper read or new tickets.

## 2. KAM'S CARDS (open, both with defaults)
- RULED 10:33 by Kam: Entra card = a (wait; delivered), smoke-key card = a (REVOKE key_66e82ef0 on demo: OWED as a small demo job AFTER D 25th's kintsugi round; undelivered until done, then tell Kam). KS-1688 card = a with a WhatsApp draft; Kam "sent"; Stuart "working through it, will update the ticket" (10:37): no KS-1688 build before his answer.
- Undelivered ruled: `secuura-m365-admin-setup-for-customer-org-1020` = b (05:35), lives in KS-1678's future work; deliver when the wizard ticket is worked.

## 3. OWED BY WEDNESDAY (in order)
1. Gate BL1 verdict -> GO (copy notes FROM the file; re-hash) or round 2.
2. C 31st's READYs -> gates (KS-1557 tier 1 Opus; the two test-only PRs tier 2 Sonnet).
3. G 12th's READYs -> gates (KS-1407 + KS-1157 tier 1; KS-1659 by its audit).
4. D 25th's DEPLOYED mail -> verify -> word to post the two notices (Peter KS-485, Stuart KS-772) -> report the deploy to Kam on the panel.
5. SCREEN_20 -> source reads -> hold -> raise.
6. Fable 5.1 coordinator trial (routing decision 7) still OWED.
7. KS-907 self-count (launcher preflight counts its own session): project-launcher defect, in seats' handovers; not Wednesday's to edit.
8. At the wrap: regenerate BOTH digests only if a lesson FILE was edited; the 05:30 ledger archive.
