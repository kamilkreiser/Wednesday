---
date: 2026-10-20
type: pickup
scope: SECUURA + all general/generic work. Datasec is TUESDAY's; FRIDAY (laptop) works both and claims before driving.
status: live
supersede: REPLACED WHOLESALE by the 09:0x Wednesday seat at its 50% checkpoint (~09:30 AEDT). Replace wholesale again; never stack. Previous: NEXT-PICKUP.md.pre-1020-0930 + git.
---

# NEXT PICKUP (Tue 20 Oct, written ~09:30 AEDT)

## 0. FIRST ACTIONS FOR THE NEXT WEDNESDAY SEAT
1. Boot reads as the launcher says. Then kam_rulings_today.sh, reconcile_rulings.py, `bash 2_Project_Files/tools/newmail.sh` (to a file), `tools/fleet_ack.sh list`, `tools/decision_queue.sh list open`, fleet/usage_gate.sh --check, `local-model/spark/tunnel.sh check`, `tmux list-panes -t fleet:0 -F '#{pane_id} #{@cockpit_name}'`.
2. **🔴 OUTBOUND MAIL IS BROKEN (since ~22:2xZ 10-19 = ~09:2x AEDT):** every send from wednesday-agent@ returns HTTP 403 {"message":"Forbidden"}; reads (GET) are 200; the same key sends from coagent@ (400 validation on an empty probe = authorised). Last good send 22:17:48Z. Sent log: 218 sends on 2026-10-19 UTC. Cause UNMEASURED (daily cap is a guess). Kam told on the panel (bf-d7e5f45f37d8) with default "retry at checkpoints and after 00:00Z (11:00 AEDT); no sending as another inbox". **Probe without sending:** POST messages/send with `{"to":[]}` -> 403 = still blocked, 400 = recovered. **On recovery, send IN ORDER:** (a) `fleet/briefs_staged/2026-10-20_answer_seatD25_plan_confirmed_UNSENT.md` to Secuura/Blockchain-D, `--kind answer`, subject "ANSWER: plan confirmation (Seat D 25th) confirmed - model now Opus 5.5", then `fleet_ack.sh answered "Seat D 25th kintsugi"`; (b) `..._answer_seatR58_plan_confirmed_UNSENT.md` to Secuura/Blockchain-R, subject "ANSWER: plan confirmation (Seat R 58th) confirmed - build cache left alone"; tap each by cockpit NAME with --mail. Rename the files without _UNSENT after.
3. Verify every merge by fetching into `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/src` (literal path). `cockpit.sh say` takes the cockpit NAME; `pane_close.sh` takes the `%ID`. **Zoom before any raw keypress**; read a waiting seat unzoomed with `capture-pane -S -60`.
4. send_brief needs `WED_AGENT=wednesday` in this seat's shell. Subjects never carry hold/stop/checkpoint words.
5. In force: Kam 10-18 new-account grant, routing v1.0, the October deploy grant EXTENDED "until further notice", the TESTED merge grant. Gauge 66% at 09:29.

## 1. LIVE FLOOR (09:30) — develop = 89956fe92956a810f6821fdee09915f087feea7b (#1649)
Merged today (morning seats), each verified by Wednesday's own fetch: #1645, #1646, #1648, #1647, #1649. None deployed. Kintsugi runs a4187f0f6622; demo runs d75bfe2deb80 (KS-1032 vouch secret armed). C 30th WRAPPED, scored 0.95, pane closed.
- **D 25th (%17, now Opus 5.5 by Wednesday's switch):** KINTSUGI deploy round of 89956fe92956 (brief `fleet/briefs_staged/2026-10-20_seatD25_kintsugi_round.md`): Phase 0 under a NEW stamp (pre-20261020 taken), build all, migrations 053+054 before m365/vc-issuer, swaps api-gateway last, pgbouncer/nginx-gateway/demo-service held, KS-535 by hash, sweep, ONE DEPLOYED mail. m365 swap only if ENTRA unconfigured and tables empty (else QUESTION). Box writes for KS-1116/KS-1679 checks = QUESTION. Peter/Stuart notices DRAFTED to Wednesday, posted only on Wednesday's word (check whether D 22nd's 10-19 drafts were posted). DEMO NOT in this round (Stuart's uat-ps note on KS-695 absent; KS-1557 fix owed). Its plan confirmation 22:23Z is FLAGGED and UNANSWERED (mail broken); it proceeds on its fallback.
- **C 31st (%18, Opus 5, switch owed at a zoomed idle):** KS-1557 PLAN-first QUESTION (Stuart's 16e8498d: a /version-created parent is refused for the creating connector's certify), tier 1; meanwhile BJ1 NOTE 2 cells (test-only, tier 2, vc-issuer test file). Plan confirmation not yet received.
- **R 58th (%19, Opus 5, switch owed at a zoomed idle; it was busy at 09:28):** (i) DONE (probe objects removed, 910 MB in Docker, 0 MB df); (ii) BI1 NB1+NB2+NB4 test-only PR in progress; (iii) KS-1682 plan QUESTION to follow. Answer staged UNSENT.
- **Spark SCREEN_19 drafter** (background sub-agent, Sonnet) running: report lands in `0_Brain/reference/2026-10-18_spark-screen/SCREEN_19.md`; read every PASS at source, then hold_ready, then give the READYs to a raise seat (C or R, file-disjoint).

## 2. KAM'S CARDS (open, both with defaults)
- `secuura-demo-smoke-key-revoke-after-measure-1020` (rec a revoke; default b keep).
- `secuura-ks1677-entra-redirect-uri-registration-1020` (rec/default a: wait until M365 goes live).
- Undelivered ruled: `secuura-m365-admin-setup-for-customer-org-1020` = b (05:35), lives in KS-1678's future work; deliver when the wizard ticket is worked.

## 3. OWED BY WEDNESDAY (in order)
1. Mail recovery (section 0.2), then the two staged answers.
2. D 25th's DEPLOYED mail -> verify on the box's evidence -> card nothing unless a STOP; then the demo round only after Stuart's uat-ps note AND a merged KS-1557 fix.
3. C 31st's KS-1557 plan -> rule (tier-1 gate after build); BJ1 NOTE 2 READY -> tier-2 gate (Sonnet).
4. R 58th's NB PR READY -> tier-2 gate; KS-1682 plan -> rule.
5. SCREEN_19 -> source reads -> hold -> raise.
6. Fable 5.1 coordinator trial (routing decision 7) still OWED.
7. KS-907's launcher preflight counts the reader's own session (D 25th measured: 16802 -> 2698 -> 2696 = %17): a project-launcher defect, in D 25th's handover notes; not Wednesday's to edit.
8. At the wrap: regenerate BOTH boot digests only if a lesson FILE was edited; the 05:30 ledger archive.
