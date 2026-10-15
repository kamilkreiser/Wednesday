---
date: 2026-10-15
type: pickup
scope: SECUURA + all general/generic work. Datasec is TUESDAY's; FRIDAY (laptop) works both and claims before driving.
status: live
supersede: REPLACED WHOLESALE at the 70% checkpoint of the 12:2x Wednesday seat (2026-10-15 ~17:0x). Replace wholesale again; never stack. The previous version is in git.
---

# NEXT PICKUP (Thu 15 Oct, refreshed at the ~18:1x rotation)

## 0. FIRST ACTIONS FOR THE NEXT WEDNESDAY SEAT
1. Boot reads as the launcher says (digest ~608 KB in ~650-line chunks). Then `kam_rulings_today.sh`, `kam_msgs.sh 3`, `newmail.sh` (never piped), `fleet_ack.sh list`, `decision_queue.sh list open`, `fleet/usage_gate.sh --check`, and **`pane_prompt_check.sh %0` (a MODAL on your own pane = a background gate asking for permission; see section 3)**.
2. **Kam's two standing words today (EXPIRING-GRANTS top rows, end = the quota reset, the pane banner says Sun 18 Oct 1pm):** (a) "Do work with the spark only until the quota resets" (all new ticket work = Spark, briefed by Wednesday by hand); (b) "if anything needs to be pushed, merged or deployed, do that first as well" (Claude seats + Opus gates past the 90% stop for push/merge/deploy ONLY, `WED_USAGE_STOP=100` naming the row). Weekly gauge 94%.
3. **MONDAY 2026-10-19: WED-154**, the storage policy for old Blockchain files and old tests (lesson 2026-10-15_storage-policy-...md). Policy + dry-run + first measured report + a card; nothing removed before Kam sees it.

## 1. STATE AT THE ~18:1x ROTATION (no Claude seat live; panes %0 + %1 only)
- **develop = 695388d71110f635dd8a46ddcbbe36d2acffda2a** (Wednesday's ls-remote 18:0x). **FIVE merges today:** #1553 (KS-1605 item 5, ks884 cure) 53b429ed · #1549 (KS-1385, under the two-NO-GO cap) 8cbadd8d · #1554 (KS-1542, Spark) 18de4b7c · #1552 (KS-1547, Spark) 0bb4f17c · #1556 (KS-1543 p1, Spark) 695388d7. Every gate verdict + hash: 0_Brain/reference/2026-10-15_gate-*/verdict.md. **Nothing deployed.**
- **HELD, waiting for a raise seat:** night/READY_KS-1543-UNUSEDBODY-2_spark-dsv4flash_...2026-10-15.diff.md (KS-1543 part 2, sites :1068/:1187, PASS 7/7 first time). One small lint PR: raise it with the next raise round, then a tier-2 gate.
- **HELD, waiting for Kam:** PR #1555 (KS-1114) head c85cc28d0232e5641901bfd12ca6960a9711e783, NO GO round 1 of 2 (title hit returns the full answer, so a guess can be escalated to verified). Card secuura-ks1114-title-reply-leaks-details-fix-now-or-wait-1015 (default a: fix after Sunday's reset: an existence-only reply, drafts and revoked kept out). Wednesday's earlier response-shape ruling is WITHDRAWN.
- **Waiting for the reset:** KS-1612 (MAJ-A from 1549: the guard reads documents.id but originate anchors under external_id, so Kam's KS-1385 rulings do not reach originate traffic yet; fail-closed). Its cells need a real Postgres, so not Spark-briefable as is. KS-1613 / KS-1614 (P4 follow-ups of gate A). KS-1611 (intermittent package_format_gate reds). KS-1543 site 3 (:1579 err on a 500: log like KS-1510? a judgement).
- Both seats wrapped cleanly: J 11th (handover in Blockchain/5_Project_History/2026-10-15_seatJ-11th/), R 45th. The J lane's scratch Postgres 55418 is still up by design.
- GO mails go to the LANE, name the head SHA, follow a gate verdict at that head + Wednesday's completion check (recompute the report hash with its stamp line deleted).

## 2. KAM'S CARDS OPEN
secuura-ks724-locked-account-template-exclusion-1015 (rec a) · secuura-ks1385-null-issuer-certifications-1015 (rec a) · secuura-ks1114-title-reply-leaks-details-fix-now-or-wait-1015 (rec a). Plus Datasec cards (Tuesday's/Friday's).
RULED BY WEDNESDAY, still operative: a seat may push from its OWN clone when it measures core.hooksPath and the hook bytes against develop in the same session.

## 3. TODAY'S INCIDENT, AND THE MECHANISM NOW ARMED
A background gate's inline `bash -c` loop raised a permission dialog on Wednesday's own pane twice (~14:08-15:39 and 15:43-16:41): the gate stalled, wake_watch held every wake, Kam's panel got an escalation. Gate briefs now forbid inline bash -c and rm; a background loop runs `pane_prompt_check.sh %0` every 30 s and exits (wakes the seat) on MODAL. **Re-arm it after a rotation** (it is a session background job).

## 4. SPARK
Tunnel 127.0.0.1:47788 re-opened at boot (it had died overnight, silently; owed fix in section 5). Today: KS-1543 p1 and p2 briefed by hand, both PASS 7/7 first round, 0 rebriefs; p1 merged, p2 held. Queue EMPTY after p2: the next screen should look past KS-1543 (site 3 is a judgement) to the remaining Backlog/Todo; KS-1544 fails the predicate (index.ts not importable).

## 5. OWED BY WEDNESDAY (own tools, small)
1. Spark tunnel: doctor.sh WARN for SEAT=wednesday on 47788 + a `spark/tunnel.sh up|check`; nothing re-opens it today.
2. cockpit.sh say --mail: stamp the mail's own timestamp into the pointer.
3. INDEX.md refresh (newest block 2026-09-23).
4. **Deploy round (Kintsugi), the 'deploy' half of Kam's push-first words:** five merges now sit on develop undeployed. A deploy seat under the October grant, ONLY once tasks/DEPLOY-BLOCKERS.md clears (GATEWAY_VOUCH_SECRET on the box FIRST, KS-1032's 'deployed only after the secret is set'; the census items; Stuart's #972). Start with a READ-ONLY census seat. Not started.
5. stash@{0} from 10-14 is KEPT, never dropped.
