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

## LIVE RIGHT NOW (Datasec/HPSM-POC; claim OPEN by Friday) — refreshed at the 70% checkpoint (~13:1x)
- **Kam ~12:0x: "Build as much as you can … showcase what we have" next week.** B09 progress:
  - **B (partner screens): MERGED** #17 → main effb3cf (CI green).
  - **A (showcase seed + `scripts/showcase.sh` + contract 0.4.0): MERGED** #18 → main 98527a2.
  - **C (customer screens): PR #19** (b09/customer-screens @ 2c5e8a9) CI RED on ONE test: `[tablet] e2e/a11y.spec.ts:69` negative control (desktop passes).
- **Fix round 1 of 2:** B10 Seat C (pane Datasec/HPSM-POC-C), brief `HPSM-POC/1_Project_Definition/Briefs/2026-09-25_B10_SEAT-C_pr19-ci-a11y-negative-control-tablet.md` (rebase onto main; fix without weakening the control). The STATUS watcher is on the B10 glob.
- On B10 READY: re-review; wait for PR #19 CI; merge head-pinned; check main CI.
- **Then send Kam the showcase pack:** screenshots beside his mocks (`Briefs/B09-{A,B,C}_evidence/`) + how to run it (`scripts/showcase.sh live|mock`, README "Showcase").
- **Card open:** hpsmpoc-showcase-draft-findings (default: keep the labelled draft findings in the demo).
- **Later (small):** the action-plan screen still uses the browser store; swap it to A's API (0.4.0 is on main now). The dashboard's "Engagements by phase" → getShowcaseSummary. One web seat.
- **Kam's hands (a hosted link):** the 9 Azure providers. Default: the laptop showcase.
- **Composer:** PR #3 merged, NOT deployed; 4 cards open. **Spark:** Wednesday's.

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
