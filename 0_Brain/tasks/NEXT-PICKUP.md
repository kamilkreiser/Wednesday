---
date: 2026-10-20
type: pickup
scope: SECUURA + all general/generic work. Datasec is TUESDAY's; FRIDAY (laptop) works both and claims before driving.
status: live
supersede: REPLACED WHOLESALE by the 09:0x Wednesday seat at its 50% checkpoint (~09:30 AEDT). Replace wholesale again; never stack. Previous: NEXT-PICKUP.md.pre-1020-0930 + git.
---

# NEXT PICKUP (Tue 20 Oct, written ~09:30 AEDT, sections 0-3 refreshed 10:16)

## 0. FIRST ACTIONS FOR THE NEXT WEDNESDAY SEAT
1. Boot reads as the launcher says. Then kam_rulings_today.sh, reconcile_rulings.py, `bash 2_Project_Files/tools/newmail.sh` (to a file), `tools/fleet_ack.sh list`, `tools/decision_queue.sh list open`, fleet/usage_gate.sh --check, `local-model/spark/tunnel.sh check`, `tmux list-panes -t fleet:0 -F '#{pane_id} #{@cockpit_name}'`.
2. **Mail outage RESOLVED ~09:34 AEDT (403 window ~09:23-09:34, cause unmeasured); all staged answers SENT.** History: OUTBOUND MAIL WAS BROKEN (since ~22:2xZ 10-19 = ~09:2x AEDT):** every send from wednesday-agent@ returns HTTP 403 {"message":"Forbidden"}; reads (GET) are 200; the same key sends from coagent@ (400 validation on an empty probe = authorised). Last good send 22:17:48Z. Sent log: 218 sends on 2026-10-19 UTC. Cause UNMEASURED (daily cap is a guess). Kam told on the panel (bf-d7e5f45f37d8) with default "retry at checkpoints and after 00:00Z (11:00 AEDT); no sending as another inbox". **Probe without sending:** POST messages/send with `{"to":[]}` -> 403 = still blocked, 400 = recovered. **On recovery, send IN ORDER:** (a) `fleet/briefs_staged/2026-10-20_answer_seatD25_plan_confirmed_UNSENT.md` to Secuura/Blockchain-D, `--kind answer`, subject "ANSWER: plan confirmation (Seat D 25th) confirmed - model now Opus 5.5", then `fleet_ack.sh answered "Seat D 25th kintsugi"`; (b) `..._answer_seatR58_plan_confirmed_UNSENT.md` to Secuura/Blockchain-R, subject "ANSWER: plan confirmation (Seat R 58th) confirmed - build cache left alone"; tap each by cockpit NAME with --mail. Rename the files without _UNSENT after.
3. Verify every merge by fetching into `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/src` (literal path). `cockpit.sh say` takes the cockpit NAME; `pane_close.sh` takes the `%ID`. **Zoom before any raw keypress**; read a waiting seat unzoomed with `capture-pane -S -60`.
4. send_brief needs `WED_AGENT=wednesday` in this seat's shell. Subjects never carry hold/stop/checkpoint words.
5. In force: Kam 10-18 new-account grant, routing v1.0, the October deploy grant EXTENDED "until further notice", the TESTED merge grant. Gauge 66% at 09:29.

## 1. LIVE FLOOR (10:15) — develop = cd63883c62a9bb0e66969df8cd3f02db2b9b2217 (#1650)
Merged today, each verified by Wednesday's own fetch: #1645, #1646, #1648, #1647, #1649, #1650 (6). None deployed. Kintsugi runs a4187f0f6622; demo d75bfe2deb80. ALL FOUR SEATS still on the launcher's claude-opus-5 except D (5.5): switch C, R, G at a ZOOMED idle and mail it.
- **D 25th (%17, Opus 5.5):** kintsugi round of 89956fe92956 (NOT #1650): Phase 0 done (stamp pre-20261020k2), source rsynced, full build detached since 22:52:38Z (~2 h). Ruled 22:5x: all defaults; m365 DORMANT (ENTRA values = repo placeholders); quiet-window rule for anchoring/nft; ONE pre-swap heads-up on KS-772 (Wednesday's word given); full notices for BOTH rounds drafted in DEPLOYED, posted only on Wednesday's word (D 22nd's 10-19 notices were never posted); + a KS-1660 sweep row. Demo NOT GO (Stuart 22:39Z: uat-ps not at aeae5ca; wants KS-1557 in the demo-pk build).
- **C 31st (%18):** KS-1557 (a') `create:connector` + migration 055 backfill BUILT, pushing -> READY then a TIER 1 Opus gate; BJ1 NOTE 2 cells (a4d5aa81f3ba) pushing -> tier 2; then a third test-only PR fixing the stale #1619 cell that #1646 made red on develop (Refs KS-1679, tier 2). 055 is C's; not in the fresh-DB bootstraps (ruled). KS-1688 (High, /version access gap) FILED -> card to Kam.
- **R 58th (%19):** #1650 merged; #1651 KS-1682 at GATE BL1 (Opus, tier 1, brief 0_Brain/reference/2026-10-20_gate-BL1-pr1651-ks1682/, landing 785b2b7cfff7 on cd63883c62a9). Next: hygiene PR (BACKLOG.md:1244 + NK1 wording), then wrap. KS-1687 (rotation never persisted) filed.
- **G 12th (%20):** raising the four held Spark passes: KS-1407 as ONE PR (tier 1; change-password revokes the caller's own session, stated), KS-1157 (tier 1), KS-1659 (Refs unless the audit says otherwise). Overlap census 0.
- **SCREEN_20 drafter** running (Sonnet): report 0_Brain/reference/2026-10-18_spark-screen/SCREEN_20.md; read every PASS at source, hold (hold_ready now accepts code_patch2 A3x: fixed + armed 2026-10-20, tests/hold_ready_a3x_arms.sh), raise via a new or existing file-disjoint seat.

## 2. KAM'S CARDS (open, both with defaults)
- `secuura-demo-smoke-key-revoke-after-measure-1020` (rec a revoke; default b keep).
- `secuura-ks1677-entra-redirect-uri-registration-1020` (rec/default a: wait until M365 goes live).
- `secuura-ks1688-ask-stuart-platform-s-version-1020` (rec a Kam asks Stuart; default c leave KS-1688 open). Added 10:1x, HTTP 201.
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
