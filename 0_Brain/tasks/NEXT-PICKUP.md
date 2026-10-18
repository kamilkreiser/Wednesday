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

## 1. LIVE WORK (03:5x)
- **develop = 385fc288fae831f2ca15b9d091c844f33285b784** (ls-remote 03:5x).
- **Seat R 48th** (Secuura/Blockchain-R, pane %4, Opus 5.5, ctx ~65%): holding for GOs on four PRs. Handover of its predecessor: `!CODING/Secuura/Blockchain/5_Project_History/2026-10-18_seatR-47th/HANDOVER.md`.
- **At gate (background sub-agents of THIS Wednesday seat; they die if it rotates before they report):**
  - GATE H1 (Opus, tier 1): #1582 KS-1540 c86b91c5a7c2 + #1584 KS-1504 e8b4206f09d2. Brief 0_Brain/reference/2026-10-19_gate-H1-pr1582-pr1584/GATE_BRIEF.md.
  - GATE H2 (Sonnet, tier 2): #1583 KS-1485 16fc1d201fc0 + #1581 KS-1387 6b4bcaec11fa. Brief 0_Brain/reference/2026-10-19_gate-H2-pr1583-pr1581/GATE_BRIEF.md.
  - **If this seat rotated before the verdicts:** relaunch both from those two GATE_BRIEF.md files (same models), re-read the heads first. R predicts all four land tree 47a455d77dec.
  - On each verdict: re-hash (line 3 deleted, one-byte control), ls-remote heads + develop, completion check, head-bound GO per PR to the R LANE via send_brief.sh --kind answer, tap with --mail.
- **Seat J lane:** empty. #1568 (KS-1612 + KS-1385 b) HELD at the cap on Kam's card `secuura-ks1612-third-round-after-cap-1018`.
- **Spark:** queue empty after tonight's screens (SCREEN_2/3/4.md in 0_Brain/reference/2026-10-18_spark-screen/). Next screen: re-run the SCREEN_4 method after these four merge; the pool is thin (361 enumerated, 4 briefable). Tunnel UP at 47788.

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
