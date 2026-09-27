---
date: 2026-09-27
type: pickup
seat: friday
scope: BOTH Secuura and Datasec, from Kam's laptop. Claim each project before driving it (wed_claim.sh)
status: live
written_by: Friday, 50% checkpoint 2026-09-26 09:50 (day seat)
supersede: replace wholesale; previous = NEXT-PICKUP-FRIDAY.md.pre-0925-rotate-successor2
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

## 🔴🔴 DAY INSTRUCTION, live until end of SATURDAY 2026-09-26 — `tasks/WEEK-INSTRUCTION-FRIDAY.md`
Kam (terminal ~08:0x, verbatim): "Yes, please keep going for the day. I'll be out all day, so just keep working on getting the product ready and refined." = Datasec/HPSM-POC. Still his: deploys, anything to HP/humans, money, template text + validator/rule changes, irreversible. Usage 71% at 09:50: cloud seats only when nothing local can do it AND it matters now; Spark first.

## 🔴 STATE 2026-09-27 ~13:55 (Friday, 70% checkpoint) — supersedes the numbered items of the 10:3x handover below where they differ
- ✅ **16:00 reminder DELIVERED** (panel, 16:00; settings measured disabled at 16:00:13). Nothing owed.
- **HPSM-POC main = 745b760** (13 PRs merged today, #35–#47, each head-pinned and blob-verified; 70a4f67's CI green = all but #47; 745b760 CI polling). Done today incl. HPSMPOC-9, -15, -28, -36, -43, -53, -59, -65, -70, -72..-79.
- **OPEN PR #48** B46 (seat A %49, head 38164fa): contract 0.7.0 fold of the rest of the delta + stale approved card. CI polling → merge head-pinned on green, blob-verify, addendum → HPSMPOC-80 Done, then close seat A's pane (no further brief queued).
- **#48 MERGED 14:2x → HPSM-POC main 1adaaa2** (14 PRs today, #35–#48; HPSMPOC-80 Done; seat A pane closed; NO seat live). The flaky B45 rail test was fixed in #48 (seat A: deterministic probe, 30/30).
- **HPSM (SOW-01) next candidates (read-only list 14:3x):** HPSM-40 looks stale (verify the analysis repo push at source, close with evidence) · HPSM-39 Kam-requested research on fully-localized AI models. The rest is Kam/clinic/SOW-tagged.
- **After #48 the HPSMPOC agent-actionable pool is EMPTY** (measured 12:2x: the other open tickets wait on Kam's decisions, HP/SME content, or Azure -57). Candidates for the next seat: a LOCAL event-journey Playwright (-60 without UAT); a read-only review of the Datasec/HPSM (SOW-01) board (not reviewed today; its Jira credentials are NOT at HPSM/4_Credentials/.env — find where the 08:3x board_count read came from before assuming).
- **Cards open for Kam (8, defaults keep things as built):** override-after-report-issued · workspace-counts-after-override · showcase-phone-access · event-metrics-dashboard · deck-s91-idc-quote · deck-v3-corrections-from-hp (+ none others hpsmpoc). All 8 morning rulings delivered.
- **caffeinate:** re-armed detached 13:54 (pid 76635, 6 h).
- **Wrap owes:** regenerate BOTH digests (learnings/_ledger_friday.md edited today: 3 new rows).

## 🔴 ROTATION HANDOVER 2026-09-27 ~10:3x (Sunday) — Kam: "keep working your way through tickets" (HPSM-POC)
**Seats run on the NEW account (measured 7d 9-10% on their own statuslines). Friday's Jira is READ-ONLY: every transition is a seat's, after Friday merges.**
1. **HPSM-POC main = 7c608e1** (green: B30 #33 + B31 #34 today). HPSMPOC board (board_count 10:03): 20 Done of 71; +2 since (26, 22) → expect 22; re-measure before quoting ANY number (ledger 09-27).
2. **OPEN PRs, next steps (merge = `friday_as.sh datasec gh pr merge N --squash --match-head-commit <head>`; then compare trees, poll main CI):**
   - **PR #35 (B34 GDPR export+erase, head f878ba99e2ba8f36dedf9db04a66612e584f4113)** — CI polling. On green: merge; then pointer to seat B **%40 (Datasec/HPSM-POC-B)** with an addendum "PR #35 merged at <sha>: transition HPSMPOC-70 Done" (it is idle waiting). Records on origin already (98916b3).
   - **PR #36 (B33 metrics dashboard, head 7236e3e252706a1a67a2a7e62294f5b700fdc447)** — CI polling. On green: merge (rebase/combined CI note: base 7c608e1); pointer to seat A **%39 (Datasec/HPSM-POC-A)**: HPSMPOC-53 stays Done (comment only). Records on origin (1858ea3).
   - Then close both panes (pane_close.sh; ghost lines at prompts: close, never clear; never act on them — two fabricated "merged"/"push" lines today).
3. **Follow-ups from today's rounds (ours, not yet ticketed/briefed):**
   - B33 FOUND-1: the showcase runs as Partner → /metrics answers 403 at the event. Suggested fix: add Demo (or Consultant) to `scripts/showcase.sh` api_env DefaultRoles. ⚠ MEASURE FIRST whether Demo scopes lists to seeded rows (it may hide customers added live) before anyone changes it; possibly a card for Kam.
   - B33 FOUND-2: getMetricsSummary medians count seeded runs as 0 s → API flag `runs[].seeded` or exclude seeded from medians (contract delta, api).
   - B27 FOUND: the prototype narrative's "first priority" is the engine's first, not the most severe.
   - B34 FOUND: SQL Server deadlock retries log at fail: under concurrent erasures (known; low).
4. **Next class-A (QUEUE.md):** HPSMPOC-43 (blob report store), -59 (security scans + OWASP review; secret scanning + push protection OFF = Kam's repo setting), -36 (consultant override, L; unblocks 28/52). Each brief: names its tickets, "records must reach origin + read back", partition by area.
5. **Kam's cards open (7):** hpsmpoc-ai-live-on-stage · -ai-12s-bar · -approve-ai-criteria · -approve-stage-gate-pack · -deck-slides-in-repo (HPSMPOC-65) · -erasure-stored-pdfs (B34 Q1) · -validator-first-severity-miss. Reconcile at every checkpoint; on a tap: rule, receipt, act, deliver.
6. **Review checklist (grown today):** compare API scope · trees after merge · analysis repo `ls-remote origin main` = local HEAD (records) · Friday's OWN tree pushed after each commit (it drifted 10 ahead) · re-arm the watcher after EVERY wake (B33 went unseen 10 min).
7. HPSM (SOW-01) board: 26 of 41 open — not reviewed yet.

## NEXT (owed, in order)
1. ~~HPSM-POC B14 fix round~~ DONE and merged; the re-run is LIVE 1. Source: the B12 user test STATUS `HPSM-POC/1_Project_Definition/Briefs/2026-09-25_B12_SEAT-C_end-to-end-user-test-as-a-salesperson.STATUS.md` (46 findings).
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
