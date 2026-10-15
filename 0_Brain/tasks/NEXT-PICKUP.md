---
date: 2026-10-14
type: pickup
scope: SECUURA + all general/generic work. Datasec is TUESDAY's; FRIDAY (laptop) works both and claims before driving.
status: live
supersede: REPLACED WHOLESALE at the ~11:2x wrap of the 06:0x morning seat (Kam: "wrap up for today ... I'll continue shortly"). Replace wholesale again; never stack. The previous version is in git (`git log -p 0_Brain/tasks/NEXT-PICKUP.md`).
---

# NEXT PICKUP (Wed 14 Oct, written at the ~11:2x wrap)

## 0. FIRST ACTIONS FOR THE NEXT WEDNESDAY SEAT
1. Boot reads as the launcher says; the digest is ~605 KB: read it in chunks of ~600-800 lines (the Read tool refuses bigger slices). Then `kam_rulings_today.sh`, `kam_msgs.sh 3`, `bash 2_Project_Files/tools/newmail.sh` (never piped), `fleet_ack.sh list`, `decision_queue.sh list open`, `fleet/usage_gate.sh --check`.
2. **USAGE: weekly 92% (renews ~midday Sun 18 Oct), hard stop in force.** Kam 06:47 today: *"please move to working with the spark. going forward once we reach 80 - 90% should be the start of limited cloud model usage and a focus on you and the spark"* → `learnings/2026-10-14_80-to-90pct-limited-cloud-wednesday-and-spark.md`; usage_gate advises at 80% for SEAT=wednesday. Card secuura-92pct-stop-ready-work-waits-1014 ruled (b): the stop is NOT lifted. Above 90%: no Claude seats, gates or drafters; Wednesday writes Spark briefs by hand. (Friday expects a new account Thursday 15 Oct; whether Kam signs Wednesday in too is NOT his word yet: do not assume.)
3. MAIL hygiene unchanged: `send_brief.sh --kind answer` → verify at destination → pointer tap in a SEPARATE call (`cockpit.sh say ... --mail`) → `fleet_ack.sh answered "<lane tag + distinctive words>"` → `note_entry.sh` quoting real outputs. Datasec rows are Tuesday's: never ack. The `[Datasec/ATTIO -> Wednesday] DAILY FOLLOW-UP DIGEST` (21:00Z daily) is subject-only, no action (Tuesday's 10-02 reply).

## 1. STATE (measured 14 Oct; re-measure before quoting)
- Secuura develop = 3c0a522216258040f32d400ede433e48e683f734 (#1548; ls-remote 06:5x). Nothing merged or deployed on 14 Oct. Floor: %0 wednesday + %1 fleet-monitor only.
- Board (board_count.sh, 06:0x): KS open 597 (backlog 339, todo 28, in progress 230), done 140. The 31 Oct aim needs ~27 closes/day; not on pace while the stop holds.
- **Spark (DeepSeek V4 Flash, 127.0.0.1:47788 via the tunnel, HTTP 200 all morning). Two PASSes HELD for raising today, both briefed by Wednesday by hand, 0 rebriefs:**
  * KS-1547 (preflight step() denominator, bash_patch): `local-model/night/READY_KS-1547-PREFLIGHTDENOM-1_..._2026-10-14.diff.md`; runs 1-2 failed only at B6 on the ks884 S10/S4 flake (KS-1605 item 5), run 3 PASS 7/7.
  * KS-1542 (forward-bound refusal prints arrays/objects as JSON, code_patch): `local-model/night/READY_KS-1542-FORWARDBOUNDSHOWN-1_..._2026-10-14.diff.md`; PASS 7/7 first time.
  Both: patch body == golden (Wednesday's diff); Opus QA gate before merge; raised by a Claude seat when the allowance allows. Both READYs carry a visible CORRECTION (hold_ready labels the model "Ornith"; it was the Spark).
- Checker change today: `local-model/tasks/bash_patch/checker.sh` B6 FLAKY discriminator (re-run once; revert the hunk; 4 runs at the untouched tip; only a tip-red sibling is INFO FLAKY). Arms: a tampered golden still FAILs; the real control PASSes. **The FLAKY branch has NOT fired live yet**: watch the next bash_patch round on preflight files.
- Spark screen 06:09 (queue.md WHY line): of 367 KS backlog+todo titles, these were read and REJECTED: KS-1324 (needs a design), KS-1326 (capped PR #1245, Kam's), KS-1289 (docker rebuild), KS-1249/KS-1184 (decision-shaped). **Still briefable, not yet briefed: KS-1544** (tenant-provisioning `ORDER BY created_at DESC, id DESC`, needs a test with >200 tied rows: read `services/tenant-provisioning` test setup first). Other small gate follow-ups worth screening: KS-1543 (ESLint warnings in verification.ts; check a lint tier exists), KS-1576.

## 2. KAM'S RULINGS TODAY
- 06:47 terminal: the 80-90% rule (above). Card stop-1014 = b, delivered to the lesson file.
- 11:15:54 board: **secuura-ks1385-custodian-may-update-anchor-identity-1013 = c — "Issuer, or anyone in the custodian's organisation"** (Wednesday's rec; NOT the built default a). **UNDELIVERED.** The next J seat adds ONE condition + its cell to #1549 (head b1801721d56b35d7982cbe5b103c740113aa70b9, issuer-only today) BEFORE the round-2 Opus delta gate, and comments the ruling on KS-1385. Carry it verbatim under `RULED BY KAM, NOT YET IN AN ARTEFACT`; mark `--delivered` only after reading the PR/ticket.
- 11:16:07 "how is everything going?": answered on the panel.

## 3. WAITING FOR A CLAUDE SEAT (in this order when the allowance returns)
1. J lane: #1549 + Kam's (c) condition, then its Opus delta gate (round 2 of 2); inputs in `Blockchain/5_Project_History/2026-10-13_seatJ-10th/HANDOVER.md` §6. Scratch Postgres 55418 was left up for it. Then KS-1114 (7fdc179b pushed, no PR).
2. A raise seat: the two held Spark READYs (KS-1547, KS-1542), one PR each, Opus gate each.
3. K lane: KS-1605 (the #1545 gate follow-ups, incl. item 5 = the ks884 S10 fixture fix that would end today's flake).
4. V lane: KS-1600, KS-1601 (a DECISION), KS-1602; KS-1606 is Kam's statusline file (told; do not edit).
5. KS-1570 deploy round: all five pieces merged; blockers in `tasks/DEPLOY-BLOCKERS.md` (GATEWAY_VOUCH_SECRET on both boxes first; census; and, NEW 14 Oct, Stuart's #972 is merged on S develop aeae5ca but NOT deployed: wait for his dev-ps/uat-ps landing notes on KS-695).
Standing lines for the next Secuura briefs: each lane watcher must treat a bare "Secuura/Blockchain" subject as broadcast (J fixed its copy, K/V not); file_ticket.py's "description anchors: True" check cannot fail (V 9th).

## 4. OWED BY WEDNESDAY (own tools, small)
0. **MONDAY 2026-10-19 (Kam 2026-10-15 ~15:4x, WED-154): the storage POLICY for old Blockchain files and old tests.** Rule file learnings/2026-10-15_storage-policy-for-old-blockchain-files-and-tests-monday.md. Policy + dry-run tool + first measured report + a card to Kam; nothing removed before he sees it.
1. hold_ready.py: read the model from round.json / the run-dir prefix (spark_*), and locate a brief DIRECTORY (night/briefs/<dir>/KS-<n>.md). IMPROVEMENTS 2026-10-14.
2. cockpit.sh say --mail: stamp the mail's own timestamp into the pointer (stale queued taps; ledger 10-13).
3. INDEX.md refresh (newest block 2026-09-23).
4. The autostash `stash@{0}` (boot-generated files from the 10-14 06:0x push conflict) is KEPT, never dropped; it holds nothing that is not regenerable.

## 5. STANDING RULES IN FORCE
Done = tested + works + deployed; never idle (an empty Spark queue carries a WHY line); clear the fleet-activity flag once answered; be careful with coding files and deploys; models named at every launch; never delete (quarantine); Datasec mail by subject only. Rotation at 80-90% via `fleet/cockpit/wednesday_rotate.sh --self` DETACHED, then read the last line of `fleet/cockpit/logs/rotate_wednesday.log`.
