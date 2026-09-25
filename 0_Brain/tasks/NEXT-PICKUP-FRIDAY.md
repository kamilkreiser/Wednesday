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

## 🔴 OWED FIRST — HPSM analysis repo to GitHub (Kam to Tuesday, terminal ~13:35: "upload everything to GitHub"; Tuesday's mail 03:36Z)
- **Measured on the laptop, 13:4x:**
  - The HPSM ROOT repo (`/Users/kamilkreiser/1FILES TO SYNC/HPSM/.git`) has NO remote: main 389 commits, `s50/toolkit-r2`, 41 changed or untracked (mostly unison `(conflict_on_…)` copies; do NOT commit those).
  - Its `.gitignore` excludes `Source_Documents/`, the secrets and `4_Credentials/`. 3,901 tracked files; the only tracked document is Datasec's own `2026-08-13_HPSM-MVP_client-presentation_v1.pptx`.
  - `datasecau/HPSM-analysis` does NOT exist (the planned HPSM-40 name).
  - The code repo `2_Project_Files` = GitHub `datasecau/HPSM` main 580d7a2 (in sync).
  - The four "held" Composer branches ARE on GitHub (answered to Tuesday).
- **Plan:**
  1. `friday_as.sh datasec gh repo create datasecau/HPSM-analysis --private`.
  2. A seat IN HPSM adds the remote and pushes `--all`. Friday's hooks rightly refuse git writes outside FRIDAY.
     - The HPSM launcher (`HPSM/Launch_Claude.command`) expects DevMASTER (`WORKSPACE_DIR`/`VAULT_DIR`), and launchers.conf `Datasec/HPSM` points at `/Volumes/DevMASTER/...`: add a laptop entry (e.g. `Datasec/HPSM-L|/Users/kamilkreiser/1FILES TO SYNC/HPSM/Launch_Claude.command`) and check the launcher runs without DevMASTER.
     - Or brief a seat another way.
  3. Deploy key or ssh: the laptop has no ssh identity for datasecau/HPSM*; use gh over HTTPS as kamilDatasec, or a deploy key like HPSM-POC's.
  4. Tell Tuesday "done <sha>" (she reports to Kam).

## LIVE RIGHT NOW — refreshed ~13:4x
- **HPSM-POC showcase: ALL MERGED.** #17 (partner) · #18 (seed + scripts/showcase.sh + contract 0.4.0) · #19 (customer + the B10 a11y fix) → main 3029930, CI green.
  - The showcase pack (18 pages) is DELIVERED to Kam's file drawer: `HPSM-POC/1_Project_Definition/Showcase/2026-09-25_showcase-pack.pdf`. The Showcase folder is untracked in the analysis repo; commit it with the next records pass.
  - Later (small): swap the action-plan screen to A's API; the dashboard phase chart → getShowcaseSummary.
- **Composer content fix RUNNING:** B06 SEAT-B (pane Datasec/Security-Composer-B), brief `Datasec Security Composer/1_Project_Definition/Briefs/2026-09-25_B06_SEAT-B_internal-text-and-sow-clause-ids.md` (C-05: rows 1–15 in screens + content = a new content release; SOW sentences → clause ids). The STATUS watcher is on the B06 glob.
  - On READY: review, open the PR, merge on green (no GitHub CI on HPSM-light; the seat's own runs are the gate), then CARD the demo deploy (it switches the demo to the new release; engagements pinned to the old one go read-only).
- **Composer fold DEPLOYED** 13:2x (5b9f6db, CSS index-BifC5jzu). The runbook step-2 note: today the laptop IP was the standing ssh rule's source, so no NSG rule was needed.
- **Kam's hands:** the 9 Azure providers (a hosted HPSM-POC link). **Spark:** Wednesday's.

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
