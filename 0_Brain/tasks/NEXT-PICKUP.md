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

## 1. LIVE WORK (refreshed 08:2x 10-19 by the morning seat near its band)
- **develop = f95ad12fe5c22f8d037e7139d052363422463c79** (ls-remote 08:4x; #1588 + #1587 merged by R 50th on M1's GO). 26 merges since 19:00 Sun. Nothing deployed.
- **GATE M1 DONE** (Fable 5.1, 21 min, sha 8fe87e4fabd9d2dd re-hashed): #1588 GO WITH NOTE, #1587 GO, #1589 fix round (gateway removal pin + two missing README blocks + minors) then a DELTA GATE (tier 1, round 2 of 2). GO for #1588 -> #1587 SENT to the R LANE 08:2x; on R's MERGED mails verify develop at source. Trial recorded in fleet/specs/model-routing.md. **No background sub-agent of this seat is running.**
- **#1568 = NO GO at round 3** (gate L1, sha 92e27bf688ddaf7f): MAJ-A closed; MAJ-B (051 refuses certification issue/revoke; census blocks apply) + MIN-A (real Prisma error shape) open. **Kam's card secuura-ks1612-round3-nogo-1019** (rec a narrow round 4, default b hold). J 13th (%6) builds nothing; design-only prep allowed. On (a): rule J's design, then a full Opus gate.
- **Seat R 50th** (%8, brief fleet/briefs_staged/2026-10-19_seatR50_successor.md): rung 6 done (plan confirmed 21:4xZ; model switch to claude-opus-5-5 still owed at a confirmed idle). NOW: #1589 fix round onto head 53cb4ec76ea7 (no merge-in) -> READY FOR DELTA GATE -> launch a tier-1 delta gate (Opus or a 2nd Fable trial). STOP-and-mail if the KS-1129 O1 live-reply property is LOST. Queue: M1 verdict -> merges; then push the 6 bundled Spark branches + #1590, one batched READY (tier 1 KS-1628 i3 + KS-1595; tier 2 rest) -> gate it. KS-1622 HELD (ticket asks 4 shapes + the same warn line): re-brief to the Spark. R 49th scored 0.95, pane %5 closed.
- **Seat D 20th** (%7): storage removal running (T done, N ~45 min, E, then W 145; 27 squash-ambiguous + 8 clones skipped). Expect a wrap STATUS with df before/after -> then retire D's pane by hand; tell Kam the freed GB; then Wednesday removes class R (local-model run clones) herself.
- **Kam's cards open:** secuura-ks1612-round3-nogo-1019; wed-devmaster-drive-cleanup-1019 (rec a QA leftovers; models stay). OWED card after #1589 merges: KS-1632 verifierVerificationLevel.
- **Spark:** queue empty with a measured why line. Next: re-brief KS-1622 (four shapes + same warn line) and a new screen when a lane frees files.
- **Owed small tools:** fix MEASUREMENT.md section 5 (the worktree-list hook is Wednesday's); hold_ready new-file test_only gap (KS-1595, KS-1627 p1); wed_claim autostash; cockpit say %pane no-op.
- DONE today: K1 + #1586; consolidation catch-up; WED-154 policy APPROVED + dry-run squash fix (arms s/s2); INDEX refresh; Kam's five taps ruled + receipted; SCREEN_7/8 held; drive survey + card.

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
