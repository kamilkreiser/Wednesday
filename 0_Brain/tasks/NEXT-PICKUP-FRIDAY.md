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

## LIVE RIGHT NOW (all Datasec; claims OPEN by Friday)
- **HPSM-POC B08 Seat A (pane Datasec/HPSM-POC-A).**
  - Brief: `HPSM-POC/1_Project_Definition/Briefs/2026-09-25_B08_SEAT-A_partner-self-subject-and-ef-race-log.md`.
  - READY; REVIEWED + ACCEPTED 10:0x.
  - **PR #16** (b08/partner-self-and-race-log @ 9cb834f) is open. CI watch running; **merge head-pinned squash on green**, then watch main's push CI.
  - The seat is working ADDENDUM-1 (`…_ADDENDUM-1_analysis-repo-records.md`): commit history/BACKLOG/CLARIFICATIONS with explicit paths and push the analysis repo. Check the "ADDENDUM-1 PUSHED" line in its STATUS.
  - Then close the pane with `pane_close.sh`.
- **Composer B05 Seat B (pane Datasec/Security-Composer-B).**
  - Brief: `Datasec Security Composer/1_Project_Definition/Briefs/2026-09-25_B05_SEAT-B_s5-notices-fold-and-internal-text-inventory.md` + ADDENDUM-0.
  - Running its full e2e (idle-wake acked at the hold).
  - On READY: review the fold (≤600 px, same wording), open the PR, merge on green, then **card the DEMO DEPLOY with before/after at 390 px (no deploy without Kam's word)** and **card the internal-text inventory** (C-03 #5/#11).
- STATUS wake: `2_Project_Files/friday/watch_status.sh` (FIXED today: paths with spaces; placeholder READY lines ignored), running in the background over both projects' `2026-09-25_B0*STATUS*.md`.

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
