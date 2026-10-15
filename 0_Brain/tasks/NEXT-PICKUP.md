---
date: 2026-10-15
type: pickup
scope: SECUURA + all general/generic work. Datasec is TUESDAY's; FRIDAY (laptop) works both and claims before driving.
status: live
supersede: REPLACED WHOLESALE at the 70% checkpoint of the 12:2x Wednesday seat (2026-10-15 ~17:0x). Replace wholesale again; never stack. The previous version is in git.
---

# NEXT PICKUP (Thu 15 Oct, written at the 70% checkpoint)

## 0. FIRST ACTIONS FOR THE NEXT WEDNESDAY SEAT
1. Boot reads as the launcher says (digest ~608 KB in ~650-line chunks). Then `kam_rulings_today.sh`, `kam_msgs.sh 3`, `newmail.sh` (never piped), `fleet_ack.sh list`, `decision_queue.sh list open`, `fleet/usage_gate.sh --check`, and **`pane_prompt_check.sh %0` (a MODAL on your own pane = a background gate asking for permission; see section 3)**.
2. **Kam's two standing words today (EXPIRING-GRANTS top rows, end = the quota reset, the pane banner says Sun 18 Oct 1pm):** (a) "Do work with the spark only until the quota resets" (all new ticket work = Spark, briefed by Wednesday by hand); (b) "if anything needs to be pushed, merged or deployed, do that first as well" (Claude seats + Opus gates past the 90% stop for push/merge/deploy ONLY, `WED_USAGE_STOP=100` naming the row). Weekly gauge 94%.
3. **MONDAY 2026-10-19: WED-154**, the storage policy for old Blockchain files and old tests (lesson 2026-10-15_storage-policy-...md). Policy + dry-run + first measured report + a card; nothing removed before Kam sees it.

## 1. LIVE LANES (Secuura/Blockchain, both on Opus 5.5)
- **J lane, Seat J 11th, pane %2.** PR 1549 (KS-1385, Kam's (c) + the null-issuer KNOWN LIMIT) head **80daaa78a2c7adf7196a41cdf240376d8c2bf75a**, READY; **round-2 delta gate RUNNING** (background Opus subagent of the Wednesday seat; brief + verdict at 0_Brain/reference/2026-10-15_gate-pr1549-r2/). Round 2 of 2 under the cap. Next for J: KS-1114 (built, develop merged in locally, push once after 1549's push; Kam's (b) "Title lookup open to anyone, one tenant").
- **R lane, Seat R 45th, pane %3.** **Gate A RUNNING** (background Opus subagent; 0_Brain/reference/2026-10-15_gate-A-pr1552-pr1554/): #1552 KS-1547 head 762d044b05c9d1943d4d857e7f99e21b5b8d7e67 + #1554 KS-1542 head 3c15af5693fa3d841182a8b4fb2258fc02f825b4. Merge order on GO: #1554 first, then KS-1543 p1 rebases on it -> gate B alone -> merge. All three are Spark patches (READYs in local-model/night/).
- **MERGED today:** PR #1553 (KS-1605 item 5, the ks884 S10+S4 fixture cure, test-only): develop **53b429ed6b4bf4d23c0721bf573b9df1c858bc06** (Wednesday's ls-remote). Gate GO WITH NOTE 6aad7fad2eeccd01. NOTE owed by R: one facts-only KS-1605 comment (the :128 comment omits cell 1; optional fixed-timestamp run).
- GO mails go to the LANE, name the head SHA, follow a gate verdict at that head + Wednesday's completion check (recompute the report hash with its stamp line deleted).

## 2. KAM'S RULINGS / CARDS
- Open for Kam: **secuura-ks724-locked-account-template-exclusion-1015** (rec a, default no change); **secuura-ks1385-null-issuer-certifications-1015** (rec a keep as built, default a; PR 1549 not held). Plus 3 Datasec cards (Tuesday's/Friday's).
- RULED BY WEDNESDAY, still operative: a seat may push from its OWN clone when it measures core.hooksPath and the hook bytes against develop in the same session (narrows the old scratch-clone ruling).

## 3. TODAY'S INCIDENT, AND THE MECHANISM NOW ARMED
A background gate's inline `bash -c` loop raised a permission dialog on Wednesday's own pane twice (~14:08-15:39 and 15:43-16:41): the gate stalled, wake_watch held every wake, Kam's panel got an escalation. Gate briefs now forbid inline bash -c and rm; a background loop runs `pane_prompt_check.sh %0` every 30 s and exits (wakes the seat) on MODAL. **Re-arm it after a rotation** (it is a session background job).

## 4. SPARK
Tunnel 127.0.0.1:47788 re-opened at boot (it had died overnight, silently). Queue empty with a WHY (13:04): KS-1543 part 2 (:1059 unused body, :1178 dead `= {}`) is ready to brief but must extend part 1's new test file, so it waits for p1's merge (test_file= pin). KS-1544 fails the predicate. Today's Spark: KS-1543 p1 PASS 7/7 first time, held, now raised.

## 5. OWED BY WEDNESDAY (own tools, small)
1. Spark tunnel: doctor.sh WARN for SEAT=wednesday on 47788 + a `spark/tunnel.sh up|check`; nothing re-opens it today.
2. cockpit.sh say --mail: stamp the mail's own timestamp into the pointer.
3. INDEX.md refresh (newest block 2026-09-23).
4. Deploy round (Kintsugi) after the merges, under the October grant, only once DEPLOY-BLOCKERS clear (GATEWAY_VOUCH_SECRET first). Not started.
5. stash@{0} from 10-14 is KEPT, never dropped.
