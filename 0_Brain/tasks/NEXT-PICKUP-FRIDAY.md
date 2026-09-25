---
date: 2026-09-25
type: pickup
seat: friday
scope: BOTH Secuura and Datasec, from Kam's laptop. Claim each project before driving it (wed_claim.sh)
status: live
written_by: Friday, successor seat, 70% checkpoint 2026-09-25 16:3x (ctx 70%, 7d 88%)
supersede: replace wholesale; previous = NEXT-PICKUP-FRIDAY.md.pre-0925-1632-ckpt70
---

# NEXT PICKUP — FRIDAY

**The tree is at `/Users/kamilkreiser/1FILES TO SYNC/FRIDAY`.** Quote every path (spaces).

## 🔴 FIRST, EVERY BOOT AND EVERY CHECKPOINT
- `kam_rulings_today.sh`, then `python3 2_Project_Files/tools/reconcile_rulings.py` (then `--apply`).
- The live-board wake is `fleet/cockpit/live_chat_poll.sh --seat friday` (armed by the shared launcher). Kam's posts arrive as "[Wednesday tap] [live-board] …".
- **Before ANY `git pull` of this tree: commit Friday's own data files first** (decisions.json, chat_friday.json, usage_friday.json, .spoken.log, the note). When committing, use `git commit -- <paths>`: other tools stage chat_tuesday/chat_wednesday.json, and those are not Friday's.
- STATUS wake: `2_Project_Files/friday/watch_status.sh <seen-file> "<glob>"`. It keys on the COUNT of READY lines, so a seat that re-saves a finished STATUS will NOT re-fire it; check idle panes.
- Unregistered project folder (HPSM: its launcher needs DevMASTER) → `cockpit.sh add <Name> "bash '…/2_Project_Files/friday/brief_seat.sh' <client> '<dir>' '<brief>'"`. Register the pane name in `fleet/inbox_routing.conf` BEFORE a `say --mail` tap: without a line, say --mail exits 1 SILENTLY (the fix is owed).

- **The LAPTOP SLEEPS.** Arm `caffeinate -dims -t 21600` (background) in the same action as launching any seat, and check `pgrep -fl caffeinate` at boot. On 09-25 it slept at ~17:0x and cut two seats' turns. One was armed at 17:4x until ~23:4x.

## 🔴 LIVE AT THE HANDOVER
1. **HPSM-POC B14 SEAT-B** (pane `Datasec/HPSM-POC-B`, base main `61f6f06`): the fix round for the B12 user test's 46 findings + C-19. Brief `HPSM-POC/1_Project_Definition/Briefs/2026-09-25_B14_SEAT-B_user-test-fix-round.md`. Watcher glob `…/HPSM-POC/1_Project_Definition/Briefs/2026-09-25_B14*STATUS*.md`. On READY: review (a screenshot per F-number); open the PR as kamilDatasec; merge head-pinned on green; then commission a FRESH cold-user re-run of the B12 test (same driver: `B12-C_evidence/seat-notes/userdriver.js`). Card F-13/F-27 (product/content) from its candidates.
2. **B15 (the requirements map): DONE + DELIVERED 18:2x** to Kam's drawer (`HPSM-POC/1_Project_Definition/Analysis/2026-09-25_requirements-map/`). Its open-questions.md holds Kam's decisions (Q-K01 AI-tools clause, Q-K02 deck structure, Q-K03 interactive tools). Q-K01 is CARDED (`hpsmpoc-sow-ai-tools-clause`, rec b, default: continue as today). Q-K02/Q-K03 get cards when the next build round needs them (every decision goes to a card, per the pinned rule). Pane closed.
3. **Composer B09: MERGED 18:0x** (PR https://github.com/datasecau/HPSM-light/pull/5 → main `b0b512c`; ci.sh 18/18). NOT deployed. **Cards open:** `composer-typed-answers-deploy` (rec a: deploy the release pair draft `8fab2ed5…` / demo `efad540b…` + migration 0018, same checks as today, runbook `2_Project_Files/friday/composer_demo_deploy.md`; then a fresh example) and `composer-example-d023-choice` (default "On"). The fresh-example brief must SELECT FRAMEWORKS (E8 2023 ML2, as in B08: the replay example had none). Pane closed.
- B13 (delete) MERGED: PR #21 → main `61f6f06`, CI green (16:28).

## NEXT (owed, in order)
1. ~~HPSM-POC B14 fix round~~ LAUNCHED 16:18 (see LIVE 1). Source: the B12 user test STATUS `HPSM-POC/1_Project_Definition/Briefs/2026-09-25_B12_SEAT-C_end-to-end-user-test-as-a-salesperson.STATUS.md` (46 findings).
   - Fix every finding that is not Kam's or the SME's. FIRST: internal notes on screen, incl. the named person ("Kam/Paul Waite meeting" footer).
   - Then: the contradictions (sample customers' narrative/report pages say "No assessment yet"; question totals 16/15/14; identical 54.2); Reset demo not resetting live data; the calculator overwriting the dashboard ARR; the "Demo Consultant" header; readiness Download greyed out.
   - **Plus C-19:** showcase mode scores NEW customers with the draft rules, labelled DRAFT (outside showcase mode C-15 still refuses).
   - Then RE-RUN the cold-user test (driver `B12-C_evidence/seat-notes/userdriver.js`).
2. **Customer maturity-assessment questions:** Kam requested them from HP (16:03). They are in NO file we hold (measured across HPSM-POC Source_Documents + the whole "HP Playbook Project" folder; Tuesday measured the T9). When they arrive → load as content; the ruleset stays DRAFT (C-15/C-19). Optional frame offered to Kam: the PRD's TRUST/KNOW/PROTECT/MANAGE/GOVERN model (no change unless he says).

## Kam's hands (asked; defaults stated)
- **GitHub Support request** (in his drawer, `0_Brain/reference/2026-09-25_sow-sentence-rewrite/github-support-request.md`): purge HPSM-light's 4 PR refs + cached objects in both repos. Kam sends.
- 9 Azure providers (a hosted HPSM-POC link; default: the laptop showcase via `scripts/showcase.sh`).
- Residuals of the SOW rewrite, his to decide: the T9 + NAS copies of the old clone; Tuesday's HPSM zips in his drawer. Reflogs + bundles + mirrors are kept on purpose (the undo).

## Today (all recorded + delivered)
- Composer: B07 history rewrite (HPSM-light main `7855f10`); B08 example engagement released (EXAMPLE — Quollbrook Freight Co, `60503ab0-…`); C-07 (answers flow, Support request, copies).
- HPSM: B02 rewrite of datasecau/HPSM-analysis (main now `03afbf8`); `6_Policy_Composer` re-cloned; old clone + `added/` copies quarantined with push URLs DISABLED; C-75, C-76.
- HPSM-POC: B11 merged (#20, main `149d15f`); B12 user test; C-18, C-19.
- Files Kam shared today, filed (git-ignored, hash-verified): `HPSM/1_Project_Definition/Source_Documents/HP Playbook Project/` + 5 loose items + `HPSM_Policy_Composer_2026-09-10/` (also copied to Composer's Source_Documents for ci.sh).
- The Spark: UP (Wednesday fixed the tilelang boot-hook pin, 05:05Z). It is Wednesday's box today; claim it before any long run.

## Left in place (never delete)
- `git stash list` autostash entries in this tree.
- HPSM-POC worktrees `.tools/wt-B0*`, `wt-B1*`; container `b07c-mssql` (stopped).
- Composer compose `pc-b03`; the demo VM's `.pre-friday-*` backups, `composer.prev`, `/opt/hpsm/composer-*.tar.gz`.
- All `_quarantine_2026-09-25_*` folders in Composer and HPSM (the undo for both rewrites).

## Open claims by Friday
Spark loop · Datasec/HPSM · Datasec/HPSM-POC · Datasec/Datasec Security Composer.
