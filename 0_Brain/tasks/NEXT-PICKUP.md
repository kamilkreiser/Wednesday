---
date: 2026-10-19
type: pickup
scope: SECUURA + all general/generic work. Datasec is TUESDAY's; FRIDAY (laptop) works both and claims before driving.
status: live
supersede: REPLACED WHOLESALE by the 22:4x (10-18) Wednesday seat at ~64% ctx, 2026-10-19 ~03:5x. Replace wholesale again; never stack. Previous version: NEXT-PICKUP.md.pre-1019-0355 + git.
---

# NEXT PICKUP (Mon 19 Oct, before dawn)

## 0. FIRST ACTIONS FOR THE NEXT WEDNESDAY SEAT
1. Boot reads as the launcher says. Then kam_rulings_today.sh, reconcile_rulings.py, newmail.sh (to a file, never piped), fleet_ack.sh list, decision_queue.sh list open, fleet/usage_gate.sh --check, `local-model/spark/tunnel.sh check`.
2. **Kam's instruction in force (EXPIRING-GRANTS top row, 10-18 ~19:0x, no expiry, tied to this account):** "new account so please work on the tickets, backlog and definition of which agent to use for what. Spark connected so give it as many tickets as it can handle". Routing v1.0 IN FORCE (every launch receipt names its row). Gauge 12% at 03:5x.
3. **MONDAY 2026-10-19 (today): WED-154 storage policy** (policy + dry-run + first measured report + a card; nothing removed before Kam sees it). Include ~335 MB of regenerable Spark clones in `local-model/spark/cache/work/`. **Weekly consolidation is also due** (first session after Sunday).
4. **Morning receipt to Kam (after 06:00, panel):** lead with the overnight result: 22 Secuura PRs merged since 19:00 Sun (count from the MERGED mails: R 47th 9, J 12th 1, R 48th 12 incl. the four below once merged; re-count from develop's log before quoting), nothing deployed, the two open cards, J's API-key-in-transcript disclosure (default: no rotation), and the /model "saved as default" side effect in the Secuura seat's Claude config.
5. Commit your own files BEFORE any tool that pulls (wed_claim autostash, 10-18).

## 1. LIVE WORK (updated 05:0x at the 70% checkpoint)
- **develop = 5d1be7b06279950e3bfe176c237e5d640eb04581** (ls-remote 04:5x). H1 and H2 both GO'd and merged (#1581-#1584).
- **Seat R 49th** (Secuura/Blockchain-R, pane %5, launched 04:57 AEDT): brief fleet/briefs_staged/2026-10-19_seatR49_gateI1_1585.md. RUNG-5 CHECK OWED (pane shows the brief received) and a /model claude-opus-5-5 switch at its first idle (busy marker = the "… (" spinner line; check in its own call), told by mail. Its plan-confirmation QUESTION is the next expected mail. R 48th wrapped 17:54Z (scored 0.95, pane %4 closed); handover `!CODING/Secuura/Blockchain/5_Project_History/2026-10-18_seatR-48th/HANDOVER.md`.
- **Background sub-agents of THIS Wednesday seat (they die if it rotates before they report):**
  - GATE I1 (Opus, tier 1): #1585 KS-1626 head 664d3fd2494b. Brief 0_Brain/reference/2026-10-19_gate-I1-pr1585/GATE_BRIEF.md. On the verdict: re-hash (line 3 deleted, one-byte control), ls-remote head + develop, head-bound GO to the R LANE.
  - Spark brief-writer for KS-1627 (test-only, real redis module in fallback must give 503). Report 0_Brain/reference/2026-10-18_spark-screen/SCREEN_6.md. On a PASS: read at source, hold_ready with a bare ROWID + --title-from-brief, NEXT to R.
  - **If this seat rotated first:** relaunch GATE I1 from its brief (re-read the head first) and the KS-1627 drafter from SCREEN_5/the KS-1627 ticket.
- Overnight count from the MERGED mails: 22 Secuura PRs since 19:00 Sun (R 47th 9, J 12th 1, R 48th 12); re-count from develop's log before quoting to Kam.
- **Seat J lane:** empty. #1568 (KS-1612 + KS-1385 b) HELD at the cap on Kam's card `secuura-ks1612-third-round-after-cap-1018`.
- **Spark:** queue empty after tonight's screens (SCREEN_2/3/4.md in 0_Brain/reference/2026-10-18_spark-screen/). Next screen: re-run the SCREEN_4 method after these four merge; the pool is thin (361 enumerated, 4 briefable). Tunnel UP at 47788.

## 1a. FIRST WORK AT 06:00 (added at the 05:30 wrap)
- **Gate PR #1586 (KS-1627, test-only, tier 2 Sonnet)**, head b12f56e303ac36a3e7adecfa4aab9fdeda3c384a on develop 840ac4182d75 (ls-remote 05:3x, both equal to R 49th's 18:32Z READY). One new test file (real services/redis module in fallback -> GET /api/connector/info 503). Write the brief from 0_Brain/reference/2026-10-19_gate-G3-pr1579-pr1580/GATE_BRIEF.md's shape (own scratch subfolder named), re-hash the verdict, head-bound GO to the R LANE. R 49th was told the gate comes from the morning seat ("ANSWER: 1586 KS-1627 received - the morning seat runs its gate after 06:00").
- No background sub-agent of the overnight seat is running.

## 1b. RULED BY WEDNESDAY, STILL OPERATIVE (Secuura)
- KS-1624 F1 = (a) (export the stripped base; done, #1580 merged). F2/F3 and KS-1623 N2 UNRULED, not queued (tickets marked "needs a ruling").
- KS-1625 (declared Node floor) filed, no fix: a decision for Kam or Wednesday.
- The GO is addressed to the R LANE; links stay `contributes`; gating on 13/16 preflight legs stands.

## 2. KAM'S CARDS OPEN
Secuura: `secuura-ks1612-third-round-after-cap-1018` (rec a third round; default b hold + re-plan around KS-1384) · `secuura-ks1385-cert-holder-can-rewrite-issuer-fields-1018` (rec b, default a). Datasec: Tuesday's.

## 3. OWED BY WEDNESDAY (own tools, small)
1. wed_claim.sh: refuse to autostash when anything outside dashboard/data is dirty.
2. cockpit.sh say --mail: stamp the mail's timestamp into the pointer; `say %4` (pane id) is a silent no-op: fail loudly.
3. pretooluse_no_cd.sh blocks `git -C $W ...` when $W is a variable for WEDNESDAY (hit 3x tonight): resolve the variable or allow the literal path only.
4. Gate briefs: always name the gate's OWN scratch subfolder (G1 ran in a predecessor's scratchpad/repo clone tonight).
5. INDEX.md refresh (newest block 2026-09-23).
6. Deploy round (Kintsugi): READ-ONLY census seat first, once tasks/DEPLOY-BLOCKERS.md clears.
7. Fable 5.1 coordinator-task trial (routing decision 7) still owed.
8. stash@{0} (10-18 autostash, restored) and older stashes are KEPT, never dropped.
