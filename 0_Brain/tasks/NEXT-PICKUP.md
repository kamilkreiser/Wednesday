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

## 1. LIVE WORK (refreshed 06:5x 10-19 by the morning seat at its 50% checkpoint)
- **develop = 83ed01af70fd5ed6cca9ac66f28ddcb8a1034105** (ls-remote 06:4x). #1586 KS-1627 merged on gate K1's GO. 24 merges since 19:00 Sun (develop first-parent log). Nothing deployed.
- **Seat R 49th** (%5): holding; next = NEXT with SCREEN_7's held passes. KS-1627 stays In Progress (ruled (b): the real-module 200 control cell is SCREEN_7 item 5).
- **Seat J 13th** (%6, launched 06:47 on fleet/briefs_staged/2026-10-19_seatJ13_1568_round3_design_ks1385b_issuer_freeze.md): Kam ruled KS-1612 = a (third round, design first) and KS-1385 = b (issuer fields frozen, own PR). OWED: rung-5 check; /model claude-opus-5-5 at its first idle (told by mail); its design QUESTION is Wednesday's to RULE (Stuart's 10-18 11:42Z KS-1612 comment: (i)/(ii) break no S flow, S prefers (iii) KS-1384; a (iii) answer may need Kam).
- **Background sub-agents of THIS seat (die at rotation; relaunch from their prompts' outputs if missing):** SCREEN_7 Spark brief-writer (KS-1628 items 2-3, KS-1622, KS-1621, KS-1620, KS-1627 cell; report 0_Brain/reference/2026-10-18_spark-screen/SCREEN_7.md); WED-154 storage measurement + dry-run tool (0_Brain/reference/2026-10-19_storage-policy/MEASUREMENT.md, tools/storage_dryrun_secuura.sh); drive survey (0_Brain/reference/2026-10-19_dev-drive-survey/SURVEY.md). Consolidation catch-up DONE (learnings/_audits/2026-10-19_consolidation.md).
- **WED-154 next:** read MEASUREMENT.md + run the tool's arms yourself, write the policy at 1_Project_Definition/Policies/2026-10-19_secuura-blockchain-storage-policy.md, ONE card to Kam (with the drive survey's G-DRIVE moves), default: weekly dry-run, remove nothing until he taps. Claimed (wed_claim.sh).
- **Kam's cards open (Secuura):** secuura-ks1628-retire-deprecated-verify-route-1019 (default a: keep running, add the check).

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
9. (from the 10-19 consolidation, retro candidates filed as TOOL items) cockpit `say` "queued" case; the "next-up" stall; `stamp.sh`; a DKIM helper. Details: learnings/_audits/2026-10-19_consolidation_DRAFT.md §6.
10. PROMOTION OWED (w=21+ family, i-endorse-things-i-have-not-read): send_brief.sh --kind answer advisory for a RULED code shape with no `read <path>`/`unread` clause. Arms first. learnings/_audits/2026-10-19_consolidation.md §2.
