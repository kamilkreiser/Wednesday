---
date: 2026-09-25
type: pickup
seat: friday
scope: BOTH Secuura and Datasec, from Kam's laptop. Claim each project before driving it (wed_claim.sh)
status: live
written_by: Friday, 50% checkpoint 2026-09-25 ~10:0x (ctx 51%, 7d 77%)
supersede: replace wholesale at every wrap/checkpoint; previous = NEXT-PICKUP-FRIDAY.md.pre-0925-ckpt50
---

# NEXT PICKUP — FRIDAY

**The tree is at `/Users/kamilkreiser/1FILES TO SYNC/FRIDAY`.** Quote every path (spaces).

## 🔴 FIRST, EVERY BOOT AND EVERY CHECKPOINT
- `kam_rulings_today.sh`, then `python3 2_Project_Files/tools/reconcile_rulings.py` (then `--apply`). `chat_reply.sh` warns on stderr when taps are pending.
- **Live-board wake now exists:** `fleet/cockpit/live_chat_poll.sh --seat friday`, armed by the SHARED launcher since Wednesday's 09b28c3b6. `doctor.sh` FAILS if it's down. Kam's posts reach this pane as a "[Wednesday tap] [live-board] …" line within ~30 s.

## LIVE RIGHT NOW (Datasec/HPSM-POC; claim OPEN by Friday) — refreshed at the 65% checkpoint (~12:1x)
- **Kam ~12:0x: "Build as much as you can … showcase what we have" next week.** B09, three seats, base main 826933a:
  - A (pane Datasec/HPSM-POC-A): showcase seed data + a one-command showcase run (real-API and mock-only modes) + action-plan/finding API, contract-first.
  - B (Datasec/HPSM-POC-B): the partner screens (dashboard, action plan, revenue calculator + results with ILLUSTRATIVE content only, managed service, phase 2). Owns the nav file.
  - C (Datasec/HPSM-POC-C): the customer screens (customer management, engagement view, finding detail, firmware risk, conversation coach, document generation).
  - Briefs: `HPSM-POC/1_Project_Definition/Briefs/2026-09-25_B09_SEAT-{A,B,C}_*.md`.
  - The STATUS watcher is running (`2_Project_Files/friday/watch_status.sh`, B09 glob).
  - On each READY: review vs the brief + the mocks; open the PR; merge on green one at a time (rebase order A → B → C if they collide); send Kam screenshots beside his mocks.
- **Kam's hands (a hosted link):** the 9 Azure providers. Default: the showcase runs from a laptop with one command.
- **Composer:** PR #3 (fold) MERGED 5b9f6db, NOT deployed. Kam's 4 cards open (deploy, SOW text in the repo, internal-text plan, 360 title).
- **Spark: Wednesday's (Kam 12:0x "don't worry about the spark").** Friday's diagnosis agent was stopped; nothing more is owed by Friday. Kam ruled "yes, Secuura code can go to the Spark" and "recreate … use it going forward" (both on Wednesday's terminal; recorded on the card, in the lesson and in the handout). The recreated container still fails (tilelang); Wednesday is on it.
- **HPSM-POC PR #16 (B08) MERGED 826933a; main CI green.**

## DONE TODAY (receipts in daily_friday/2026-09-25.md)
- Card hpsmpoc-playbook-module2-readiness → b (kept separate).
- Spark handout for the Studio: `0_Brain/reference/2026-09-22_spark-deepseek-v4-flash/STUDIO_HANDOUT_2026-09-25.md`. Mailed to Wednesday as a pointer and again in full; shared in the file drawer.
- Card spark-studio-client-scope → **c: Kam decides after the Studio can connect.** Until then no client code on the Spark from the Studio. The handout's §0 carries the ruling.
- Wednesday asked about a DIRECT cable to the Studio. Answered: no known setup; no link anywhere = probably powered off; the Wi-Fi LAN is the proven path.
- **Kam's hands:**
  - the Spark's power;
  - NVIDIA Sync on the Studio;
  - (older) the 9 Azure providers;
  - the HP E8 SOW file into Composer `Source_Documents/`.
- tap_friday.sh 190→180 (Tuesday's finding). Tuesday told the Composer demo needs no redeploy.

## Left in place (never delete)
- `stash@{0}` "autostash" from the 09:2x digest conflict.
- HPSM-POC: worktrees `.tools/wt-B0*`, container `b07c-mssql` (stopped).
- Composer: compose project `pc-b03`.

## Open claims by Friday
Spark loop · Datasec/HPSM · Datasec/HPSM-POC · Datasec/Datasec Security Composer.
