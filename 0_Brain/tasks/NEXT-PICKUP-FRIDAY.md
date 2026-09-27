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

## 🔴 STATE 2026-09-27 18:35 (Friday) — supersedes the 17:55 block where they differ
- **FLOOR EMPTY.** No agent-actionable work without Kam: HPSM-POC pool empty; HPSM readiness-only (clinic pack delivered); Composer's rest is Kam's cards or SME items.
- **Composer main = e0d8a3f** (PR #6 + #7 merged; B11/B12 closed; guide v1.3 committed 702bbf0, v1.2 8f65570). **Open Kam cards:** `composer-repeated-questions-notice` (default keep) · `composer-guide-v13-to-paul` (default nothing sent) · `composer-release-05070f1d-deploy` (rec a deploy + rebuild the two examples; default hold). **On a tap of a:** deploy the way C-06/C-08 did (VM `remote-update.sh`, a temporary key removed + proven, PREFLIGHT, /site.json, the running release = 05070f1d), then a seat rebuilds EXAMPLE A/B on it (the B10 brief shape).
- Docker stacks left up on the laptop: pc-b03 (b11 branch), pc-b11e2e (18480).

## 🔴 STATE 2026-09-27 17:55 (Friday, 50% CHECKPOINT) — supersedes everything below where they differ
**Kam's live instruction (terminal, after 16:3x): "keep working your way through tickets".** Seats run on the new account (7d 24%). No Kam rows since 17:11; reconcile 0.
1. **HPSM-POC:** main = **b1d3ec9** (PR #49 merged, HPSMPOC-81 Done). Floor empty; agent-actionable pool EMPTY (Kam cards / HP content / Azure -57).
2. **HPSM:** B04 DONE + reviewed (sweep on HPSM-39 38488; clinic pack `HPSM/1_Project_Definition/Architecture/2026-09-29_HP-meeting-clinic-pack_FOR-KAM.{md,pdf}` shared to Kam's drawer f-4a39f170f1; SOW status on 6 tickets; C-78). Kam's Tue 29 Sep 07:05 HP meeting = clinic (Friday's reading, told). HPSM-37 is Kam's after Tuesday. **HPSM stays readiness-only** until Kam says the build starts (told him; his word corrects). Pane closed.
3. **Composer (Datasec Security Composer; HPSM-light repo, NO GitHub CI — ci.sh is the gate):**
   - B11 merged as **PR #6 → main 3b9a663** (Friday opened it: the seat has no gh login; the compare URL is in the STATUS).
   - **Seat A %52 on B11 ADDENDUM-1 round 2** (Q2b approver note, Q4a required Environment, N1 hide the link on non-editable versions, Q5 content clean = new content release per C-05, NOT deployed). On READY: review at source, open the PR with `friday_as.sh datasec gh pr create`, merge head-pinned, then card Kam for the DEPLOY of the new release (say what goes read-only).
   - **Seat B %53 B12 guide v1.3** READY (61 pp, G1–G16 all_pass, cold-reader 0 guesses) BUT the v1.3 AND v1.2 folders were UNTRACKED at 17:5x while the seat was still mid-turn (secret scan). **When it shows "done", check `git -C <Composer> status -- 1_Project_Definition/User_Guide`**; if still untracked, an addendum: commit v1.3 (walk-raw is gitignored) by explicit path. Its draft "GUIDE v1.3 SHOTS" was RELEASED by the cold-reader (a deviation from "draft only"; B02 precedent; C-03 leave test engagements) → tell Kam in the review message. BACKLOG #17 → ask seat A to mark it READY FOR REVIEW. Then a card for Kam: send v1.3 to Paul? (+ 6 Needs-SME items in the STATUS).
   - Card open: `composer-repeated-questions-notice` (rec a reword; default c keep).
4. **Tooling built today:** `tools/count_list_check.sh` (advisory, ledger w=3) wired into chat_reply + decision_queue.
5. Caffeinate pid 53618 (6 h from 17:07). Watcher: re-arm `friday/watch_status.sh /tmp/claude-501/seen_composer_b11b12 "<Composer>/1_Project_Definition/Briefs/2026-09-27_B1[12]_STATUS.md"` after every wake.

## 🔴 STATE 2026-09-27 ~17:00 (Friday, ROTATION HANDOVER at 79%) — supersedes everything below where they differ
**Kam's live instruction (terminal, after 16:3x): "keep working your way through tickets".** Seats run on the new account (7d ~21%).
1. **HPSM-POC main = 1adaaa2** (15 PRs merged today, #35–#48, each head-pinned + blob-verified; main CI green).
2. **OPEN PR #49** (B47, seat A pane `Datasec/HPSM-POC-A`, head `0018541c05f0a285c5b69155da7aaef6181c4c1d`): C-29 override-after-issue + counts pinned. CI polling. On green: `friday_as.sh datasec gh pr merge 49 -R datasecau/HPSM-POC --squash --match-head-commit 0018541c05f0a285c5b69155da7aaef6181c4c1d`, then compare merge vs `1adaaa2...0018541` by blob, then an addendum (NEUTRAL filename, e.g. `…B47_SEAT-A_ADDENDUM-2_merged.md`) → HPSMPOC-81 Done; then close the pane. Seat A's B47 ADDENDUM-1 (records if not pushed + design pack 02 §3 C-29 line) is in flight.
3. **HPSM B03: REVIEWED by Friday 17:0x** (census 26/26, 3 comments 38480-38482 read back, C-77 records Kam's Jira ruling, records 1d0f94f = origin; card hpsm-jira-login-on-laptop DELIVERED). **B03 ADDENDUM-2 in flight** (seat `Datasec/HPSM`): HPSM-40 → Done; retitle HPSM-15 + -32; HPSM-20 closed as a duplicate of -25 ONLY if proven the same ask; post the HPSM-39 evidence comment. **Successor: read its `## ADDENDUM-2`, verify each write on Jira (read-only), then close the pane.** Four new Kam cards: hpsm-sow01-signed-date (AMENDED: six tickets, not five) · hpsm39-azure-region-sweep · hpsm37-scoring-model-accept · hpsm-architecture-clinic-date.
4. **Kam's standing rule (16:34): every HP ask for HPSM-POC = its own copy-ready email to Kam + the register `0_Brain/reference/2026-09-27_hpsmpoc-hp-requests/HP_REQUESTS_REGISTER.md`** (learning + auto-memory filed). HP-1 deck corrections and HP-2 slide 91 emailed 16:37 (sent copies read back). HP-3 CSMA questions already asked by Kam 09-25.
5. **Cards:** all HPSM-POC cards ruled and delivered except `hpsm-jira-login-on-laptop` (deliver after B03 records its C-number). 16:00 reminder delivered.
6. **Rules learned today (ledger rows, read them):** counts come from a read (w=2) · a seat is idle only on a `done HH:MM` line; phrase records items conditionally otherwise (w=2) · addendum filenames name content, never an outcome word (w=2) · read every tap's own output line.
7. caffeinate pid 76635 until ~19:54. Digests current (regenerated 16:3x after the new lesson file; the ledger is not an input).

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
