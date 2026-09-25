---
date: 2026-09-25
type: pickup
seat: friday
scope: BOTH Secuura and Datasec, from Kam's laptop. Claim each project before driving it (wed_claim.sh)
status: live
written_by: Friday, successor seat, 50% checkpoint 2026-09-25 15:09 (ctx 50%, 7d 84%); predecessor rotation 14:3x
supersede: replace wholesale; previous = NEXT-PICKUP-FRIDAY.md.pre-0925-1509-ckpt50
---

# NEXT PICKUP — FRIDAY

**The tree is at `/Users/kamilkreiser/1FILES TO SYNC/FRIDAY`.** Quote every path (spaces).

## 🔴 FIRST, EVERY BOOT AND EVERY CHECKPOINT
- `kam_rulings_today.sh`, then `python3 2_Project_Files/tools/reconcile_rulings.py` (then `--apply`).
- The live-board wake is `fleet/cockpit/live_chat_poll.sh --seat friday`; the SHARED launcher arms it (09b28c3b6). Kam's posts arrive as "[Wednesday tap] [live-board] …" within ~30 s.
- **Before ANY `git pull` of this tree: commit Friday's own data files first** (`0_Brain/dashboard/data/decisions.json`, `chat_friday.json`, `0_Brain/daily_friday/.spoken.log`, the note). Today an autostash stranded a card + 15 messages (ledger w=1).
- STATUS wake: `2_Project_Files/friday/watch_status.sh <seen-file> "<glob>"` (fixed today: paths with spaces; `<…>` and ALL_CAPS placeholder READY lines ignored). Re-arm it for anything live.

## 🔴 LIVE AT THE ROTATION
1. **Composer B08: DONE 14:58.** EXAMPLE — Quollbrook Freight Co (fictional), engagement `60503ab0-1cb9-49c3-8ca6-69ba2b5c40fa`, Released 1.0.0 on `bfecdc77`; 8/8 exports; the link was given to Kam on the panel. **Card `composer-outputs-carry-no-answers` open** (F1: the outputs carry no answers; rec b = type the answers → a new release + deploy on his word + a fresh example; default nothing).
2. **Composer B07 (history rewrite): DONE and verified 14:4x.** main `7855f10` (tree `bc91671…` unchanged), 77 branches; map `…/_quarantine_2026-09-25_HPSM-light-mirror-before-rewrite/commit-map_old-to-new.txt`. Tuesday mailed (a clone on the mini is stale). **Two cards open, both Kam's:**
   - `hpsm-analysis-sow-sentences` (rec a): the same sentences are in datasecau/HPSM-analysis (Friday's 13:44 push, 5 files, 3 commits each) + the Composer folder's local analysis repo + the old clone HPSM/6_Policy_Composer. On a: a seat in the HPSM folder does the same backup → replace → rewrite → force-push, and quarantines + re-clones 6_Policy_Composer.
   - `composer-github-support-purge` (rec a): Friday drafts the Support request (4 PR refs + GC); Kam sends it at https://support.github.com/contact.
   - Also a residual (Tuesday 04:42Z): the mini's T9 clone `/Volumes/KK_T9_External_HDD/!CODING/Datasec/HPSM/6_Policy_Composer` (old history, marked STALE by her), copied by her one-way NAS sync, so the old text also sits on the T9 + the NAS. Removing it is Kam's (delete class). Not yet told to him: put it in the next panel update.
   - Residuals kept by design: the Composer 2_Project_Files reflogs (R3), the VM's old archives + composer.prev (R6), and the backup mirror + bundle (R8).
3. **HPSM-POC B11 SEAT-B** (pane `Datasec/HPSM-POC-B`, launched 14:36 by the successor seat, base main 3029930):
   - Brief: `HPSM-POC/1_Project_Definition/Briefs/2026-09-25_B11_SEAT-B_action-plan-and-dashboard-on-the-real-api.md`.
   - Scope: the action plan and the dashboard move to the real API (the B09 seats' own follow-ups), with mock mode kept; plus the Showcase records commit (build script + INDEX only; the PDF stays out by the root `.gitignore`'s `*.pdf`).
   - STATUS watcher glob: `…/HPSM-POC/1_Project_Definition/Briefs/2026-09-25_B11*STATUS*.md`.
   - **DONE: PR #20 merged 15:1x → main 149d15f (tree = the reviewed head's), pane closed.** Next: confirm main push CI green (a poll was running at the handover; re-read `gh run list --commit 149d15f`).
4. HPSM-POC showcase B09: all merged (main 3029930, CI green); the showcase pack is in Kam's file drawer. HPSM analysis repo: pushed (private `datasecau/HPSM-analysis`).

## Small, queued (not started)
- HPSM-POC, the next API+web round (Friday's decisions, v1.3; no card): one owner-role list = the union of the seed's names (Pre-sales lead, Service delivery lead) and the web's (Sales lead, Technical lead, Services delivery lead); getShowcaseSummary.actions counts the NEWEST plan only; clean the unused readiness-source.ts + content keys by quarantine/move (never delete); the contract declares 415. Waits on card hpsmpoc-plan-no-delete (option b/c adds an API delete in the same round).

## Kam's hands (asked; defaults stated)
- 9 Azure providers (a hosted HPSM-POC link; default: the laptop showcase via `scripts/showcase.sh`).
- The HP E8 SOW extract file into Composer `1_Project_Definition/Source_Documents/` (CI's one red step).

## Today's decisions (all recorded + delivered)
- HPSM-POC C-17 (keep the draft findings).
- Composer C-05 (fold deploy; content fix; clause ids; 360 accept) and C-06 (keep phrases; rewrite history now; deploy + badge + a new example).
- The Spark is Wednesday's: Kam ruled Secuura may use it, and the container was recreated. It still fails on tilelang; Wednesday is on it.

## Left in place (never delete)
- `git stash list` autostash entries in this tree.
- HPSM-POC worktrees `.tools/wt-B0*`, `wt-B10-C`; container `b07c-mssql` (stopped).
- Composer compose project `pc-b03` (up); the demo VM's `.pre-friday-*` backups and `composer.prev`; `/opt/hpsm/composer-*.tar.gz` archives (old content, a residual for the rewrite report).

## Open claims by Friday
Spark loop · Datasec/HPSM · Datasec/HPSM-POC · Datasec/Datasec Security Composer.
