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

## 1. LIVE WORK (refreshed 08:0x 10-19 by the morning seat at its 70% checkpoint)
- **develop = 83ed01af70fd5ed6cca9ac66f28ddcb8a1034105.** 24 merges since 19:00 Sun. Nothing deployed.
- **GATES RUNNING (background sub-agents of THIS seat; they die if it rotates first, so relaunch from their briefs, re-reading heads):**
  - **L1** (Opus, tier 1, FULL, round 3 of 3 = Kam's last): #1568 head 09588895db75354d829df2069452c82b787d8bc8. Brief 0_Brain/reference/2026-10-19_gate-L1-pr1568-r3/GATE_BRIEF.md, own scratch l1/. A NO GO = card to Kam (his card's terms). On GO: re-hash, ls-remote, head-bound GO to the J LANE; then J corrects the KS-1612 record + replies to Stuart; then the KS-1385 (b) freeze PR.
  - **M1** (FABLE 5.1 = the routing-v1.0 decision-7 trial; compare its wall-clock and findings with the day's Opus gates and record it in fleet/specs/model-routing.md section 6): #1588 0080ac3e1552, #1587 b5b78b296c86, #1589 53cb4ec76ea7 (KS-1628, Kam ruled retire). Brief 0_Brain/reference/2026-10-19_gate-M1-pr1588-1587-1589/GATE_BRIEF.md, scratch m1/. Merge order 1588 -> 1587 -> 1589; #1587 vs #1568 share originate documents.ts (disjoint ranges): order at GO time.
- **Seat R 49th** (%5, ctx ~80%+, in its band): holding for M1; wraps at its boundary -> R 50th successor brief: M1 verdict + merges, then the EIGHT held Spark READYs (SCREEN_7 six, mail 20:1xZ; SCREEN_8 KS-1526 held + KS-1595 from its run dir, addendum 20:4xZ). OWED after #1589 merges: card Kam on KS-1632 (verifierVerificationLevel inert, three options).
- **Seat J 13th** (%6): holding for L1.
- **Seat D 20th** (%7): storage removal round 1 (293 targets / 368 GiB; clones + unregistered skipped). Expect a STATUS with df before/after -> then Wednesday removes class R (local-model run clones 2.9 GiB) herself; class-S guard change is a proposal.
- **Kam's cards open:** wed-devmaster-drive-cleanup-1019 (rec a: QA leftovers ~296 GB; models stay per his 16 Sep word; default c nothing). Survey: 0_Brain/reference/2026-10-19_dev-drive-survey/SURVEY.md. Datasec grew +43 GiB since 10-05 (Tuesday's to look at; tell her by mail, coordination only).
- **Spark:** queue EMPTY with a measured why line in local-model/spark/queue.md (pool thin after excluding live lanes). Next screen when a lane wraps.
- DONE today: gate K1 + #1586; consolidation catch-up (audit, doctor lapse check); WED-154 policy APPROVED; INDEX refresh; Kam's five taps ruled + receipted; SCREEN_7 + SCREEN_8 held.

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
