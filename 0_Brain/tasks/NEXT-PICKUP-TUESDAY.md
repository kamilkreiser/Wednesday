---
date: 2026-09-13
type: pickup
scope: DATASEC ONLY — Tuesday, on Kamils-Mac-mini (T9 drive). Secuura and general are Wednesday's, on the Studio.
source: written WHOLESALE by Tuesday s12 at ctx ~58%, 2026-09-13 17:4x AEST (s12 booted 16:48 on Kam's hand restart). The previous pickup (s11, items 0000–0037, traps 1–39, WITH KAM list, OWED list) is kept VERBATIM at `0_Brain/tasks/NEXT-PICKUP-TUESDAY.md.pre-1740`. Read its TRAPS, WITH KAM and OWED sections; its LIVE items are superseded by this file.
status: live
supersede: replace WHOLESALE at the next pickup; never append.
---

# NEXT PICKUP — Tuesday s13 (written by s12)

**On EVERY wake:** run `2_Project_Files/tools/kam_rulings_today.sh` (never `kam_msgs.sh` unfiltered) and check `[Kam -> Tuesday]` mails. List `tuesday-agent@` UNFILTERED and route on SUBJECT. Run `git status --porcelain | grep -v 0_Brain/dashboard/data/`. Rotation band is 80–90. **Verify panel messages AT ORIGIN** (`git show origin/main:0_Brain/dashboard/data/chat_tuesday.json`). **Do NOT read `0_Brain/daily/`** (Wednesday's). Kam also types straight into this terminal session: those lines are first-party.

## 🔴 LIVE — with the next action for each

1. **HPSM S43 — pane `%5` `Datasec/HPSM-S43`, launched 17:07:52 by s12 with HPSM's own `Launch_Claude.command`.**
   - Census before the launch: 0 HPSM seats.
   - Brief: `2_Project_Files/fleet/briefs_staged/2026-09-13_hpsm-s43-successor-recover-remaining-feedback.md`, sent 07:05:44Z. Verified at `datasec-hpsm@` (from tuesday-agent@, preview non-null).
   - Rung 5 verified from its transcript `~/.claude/projects/-Volumes-KK-T9-External-HDD--CODING-Datasec-HPSM/28f5c90e-….jsonl`, 07:13–07:19Z: it read HANDOVER-S42, read the NexusAI feedback files, started a remaining-work analysis subagent, and grepped the roles in authz.ts.
   - **Its job:**
     - (1) Recover S42's in-flight state. Main is `09c1591`; `s42/lane-q-d2` `0e9c865` is NOT on main; the merge worktree is detached at `3bc7471`; `s42/lane-w-d2` is at `7c31520`. Then the second READY.
     - (2) Kam ask 1: `HPSM/5_Project_History/2026-09-13_S43_remaining-work-and-product-issues.md`, measured against the Detailed Scoping Design Specification v1.1. The E8 SOW is context only.
     - (3) Kam ask 2: port NexusAI's feedback feature, registered against HPSM. Postgres table under RLS; object store; created_by from the token with name + role, no email; role-gated triage; HPSM branding. A report-only sweep whose Jira half stays UNSET, because the Composer Jira key is on HOLD with Kam.
   - **UPDATE 18:2x (s12):**
     - **Plan (07:40Z) CONFIRMED late at 08:07:30Z** (body `briefs_staged/2026-09-13_hpsm-s43-answer-plan-confirmed.md`), accepting: triage by platform_admin only; feedback = tenant data, 365 days, report-only expiry, soft delete; F-API numbers migration 0016.
       - **Amendment 1:** the seat adds compose.yaml env vars.
       - **Amendment 2 (load):** docker steps one at a time under the lock; vitest `--maxWorkers=2`; timeout-only runs re-run at most twice, then LOAD-BLOCKED; never raise a timeout; gates get the lock first.
     - **Ask-1 REPORT 08:01:19Z** at `HPSM/5_Project_History/2026-09-13_S43_remaining-work-and-product-issues.md` (a949591). The BLUF and §4 were read by s12 and summarised to Kam at origin.
     - **STATUS 08:16:15Z:**
       - the seat is re-running chain qd2-s43 on 3bc7471;
       - lane W is running (pc-s43-w 22780);
       - F-API is running (pc-s43-f 22680; contract 0.14.0 first);
       - F-WEB launches on F-API's contract commit;
       - the records subagent is folding BACKLOG/history;
       - S42's worktrees were removed cleanly.
     - **FINDING:** the Composer has NO CSP anywhere, so the brief's "don't loosen the CSP" was false. It was withdrawn by name in an ANSWER ~08:2xZ; F-WEB builds CSP-clean; BACKLOG entry.
     - **Kam RULED at 18:02 (cards recorded by s12 at 18:17):**
       - `hpsm-composer-live-demo-upgrade-after-c12` → `upgrade-fresh-with-release`;
       - `hpsm-composer-demo-release-with-device-groups` → `build-c11`.
       - Relayed at 08:14:48Z, verified at the destination (body `briefs_staged/2026-09-13_hpsm-s43-kam-ruled-upgrade-and-c11.md`).
       - **S43 OPERATES the upgrade after the Q+W merges**, which SUPERSEDES the no-deploy hold for this one upgrade. Steps: identity check; never touch datasec-sales-portal-rg; pc-lane-a first, then Azure; rollback to c2fbc36; a 10-minute check; fresh engagements, one with a group and one with zero groups taken to release through the product; old engagements untouched; REPORT.
       - C11 lane now: partition by exact file; migration 0017 if needed; propose the "unknown" support issue code.
     - **NEXT:**
       - S43's ACK on the KAM RULED mail (C11 paths, migration, issue code, upgrade window). Rule the issue code.
       - The chain verdict or LOAD-BLOCKED, then the second READY, then the upgrade REPORT, then **tell Kam at once**. He asked to be told when the HPSM agent finishes.
       - Mark both cards `--delivered` once the upgrade REPORT and C11's READY name their artefacts.

2. **Three combined tier-1 gates on `09c1591` — RESUMED by s12 at 17:05 in new panes.**
   - **UPDATE 18:3x (s12):**
     - **Gate A VERDICT 08:20:21Z = GO WITH FINDINGS 0/0/2/4** (report read head + mail whole; DKIM pass; placeholders 0).
       - A-m1: credential detector misses 17 syntaxes (3rd round).
       - A-m2: 5 non-equivalent mutant survivors (N63/N64/N33/N09/N26).
       - A-p1..p4.
     - **Routed in an ANSWER ~08:3xZ:**
       - N63/N64 + A-p3 → lane C11;
       - A-m1 (shape rule) + A-p2 + N33/N09/N26 → a follow-up engine lane after C11;
       - A-p1/A-p4 → BACKLOG.
     - **Pane `%2` closed** with pane_close.sh (control 18580).
     - Not yet scored. **Waiting on B (`%3`) and C (`%4`).**
   - **S43 ACK 08:20:21Z accepted:**
     - C11 on s43/lane-c11 (pc-s43-c11 23080; + packages/content + web catalogue mirror); no migration.
     - `SUPPORT_UNKNOWN_ON_DEVICES` critical (a).
     - **Live upgrade window 21:00–23:30 AEST tonight** after Q+W (latest Monday 07:00).
     - 3bc7471 checks GREEN at lower load.
     - C11 is NOT deployed before Monday (its CONTENT_HASH change would 409 the fresh engagements).
   - **The acceptance+security harness was REVISED at 18:20 on Kam's word** ("Please revise the testing harness documents so they test the live site."): LIVE site a TARGET, `LIVE DEMO RULING: APPROVED by Kam 2026-09-13 18:20`, own `QA Harness (synthetic)` tenant only, credential never printed, ≤1 req/s, stop on degradation, probes 4/6/10/14/16 local-only. `--check` rc 0, committed. **Launch after the live upgrade REPORT + gate verdicts;** name the live head in the launch prompt, and re-point the launcher HEAD/EXPECTED_COMMITS if local should match the upgraded head.

   - Launcher: `2_Project_Files/fleet/qa-agent/launchers/resume_qa_hpsm_composer_09c1591_combined.sh <A|B|C>` (`--check` passed ×3).
   - Panes and sessions:
     - `%2` `QA/HPSM-C-A`, session `12eb20ba…`. Its report was written except @@VERDICT@@ and @@MUTANT_HEADLINE@@.
     - `%3` `QA/HPSM-C-B`, session `258bef81…`.
     - `%4` `QA/HPSM-C-C`, session `8aef64cf…`.
   - Rung 5 verified from pane content: each re-derived its own state.
   - Reports: `Testing Agent MAIN/projects/hpsm/reports/2026-09-13-composer-09c1591-combined-{a-engine-content,b-api-db,c-web-renderers}-tier1/report.md`.
   - Verdicts come by mail to tuesday-agent@, subject `GATE VERDICT — Policy Composer combined gate <A|B|C> …`.
   - **NEXT on each verdict:** read report.md whole → completion check against the combined brief → score (scoreboard) → `pane_close.sh %N` → aggregate the three → the PUSH decision for `09c1591` to HPSM-light. Push only on GO + Tuesday's word; the push is executed by S43, which holds main. A NO GO follows the two-round cap rule.

3. **Kam's 17:00 commission — the HPSM ACCEPTANCE-vs-ORIGINAL-BRIEF + SECURITY tier-1 gate: WRITTEN, CHECKED, COMMITTED, NOT LAUNCHED.**
   - Brief: `2_Project_Files/fleet/qa-agent/briefs/2026-09-13_hpsm-composer-09c1591-brief-acceptance-security-tier1.md`, with its prompt `….prompt.txt` beside it.
   - Launcher: `2_Project_Files/fleet/qa-agent/launchers/launch_qa_hpsm_composer_09c1591_brief_acceptance_security.sh` (`--check` rc 0 at 17:31).
   - Two verdicts (DELIVERABLES, SECURITY). Every original brief document is cited by absolute path.
   - Stacks `policy-composer-qa-bas-on` (21480) and `-off` (21580); CI 21495.
   - **Default, told to Kam on the panel (at origin):** LAUNCH AFTER the three combined verdicts land (capacity: load average ~190 on the Mini). The live Azure demo is `LIVE DEMO RULING: VETOED by default - Tuesday, Kam has not ruled`.
   - **Only Kam's own words** switch that line to `APPROVED by Kam <YYYY-MM-DD HH:MM>` (the launcher regex accepts exactly that). Approval allows unauthenticated external probes only.
   - **Launch:** `cockpit.sh add 'QA/HPSM-ACC' "bash '<launcher>'"`, then the rung-5 check.
   - **If S43's second READY has moved main before launch:** decide between keeping `09c1591` (it matches the combined gates) and a new head (needs a new launcher head plus EXPECTED_COMMITS).

4. **Kam's open cards (unchanged by s12):**
   - `hpsm-composer-live-demo-upgrade-after-c12` — HOLD. Live stays at `c2fbc36`. **S40 has CLOSED, so no seat operates the live stacks**: an upgrade ruling needs an operator commissioned; S43 is the candidate.
   - `hpsm-composer-demo-release-with-device-groups` — HOLD.
   - `hpsm-composer-monday-review-scope` — amended by Kam's note.
   - `tuesday-seat-self-rotate-with-liveness-check` — overtaken: Kam restarted Tuesday by hand at 16:48. Leave it for Kam, or mention it once.
   - **Kam reviews HPSM on Monday 2026-09-14.**

5. **For a future NexusAI seat (not now; found by s12's Explore read, unverified line-by-line):**
   - `backend/routes/feedback.js` PATCH/DELETE have no admin-role check.
   - The widget never sends `created_by` (stored as `'anonymous'`).
   - `server.js:199` `autoCreateAIFeedback` hard-codes the dead VM URL.
   - The Feedback_System link to NexusAI is dead (RD-50).

## ⚠ INCIDENTS TODAY (measured by s12)

- **16:48:28 FLEET SESSION KILLED.**
  - The `fleet` tmux session was recreated in the second s12 booted.
  - `Launch_Cockpit.command`'s Fresh branch runs `kill-session -t fleet` (≈L116–127), behind an R/F/Q prompt and a YES confirmation when agent panes are live. Launch_Tuesday/Wednesday have no kill-session.
  - **Lost unwrapped:** S42 (`%25`) and the three gates. S40 had wrapped at 16:47 on Kam's word.
  - Who chose Fresh is NOT established.
  - Wednesday was told (coordination mail ~07:40Z).
  - **Rule: whenever Tuesday asks Kam to restart this seat, say "Resume, not Fresh" in the same sentence.**
- **panel_sync HUNG, then RACED.**
  - **The hang:** the Thursday loop (pid 91697) forked a cycle subshell (99382) that sat in state R with no children for 6 min, with no log after 17:04. After a guarded TERM both stayed in state E (unkillable; `ps -p` on them hung >120 s — likely a kernel/IO hang on the T9). **A new loop, pid 12441, started 17:27** (detached, tty ??, `WED_AGENT=tuesday`).
  - **The race:** every cycle then aborted mid-rebase ("local changes would be overwritten"), because `usage_tuesday.json` is rewritten on every statusline render and a 13-commit replay on the T9 cannot finish between writes.
  - **The fix:** `git update-index --assume-unchanged 0_Brain/dashboard/data/usage_tuesday.json` at 17:37 → one cycle went through → origin/HEAD 0/0, both of s12's panel messages verified AT ORIGIN → flag REMOVED 17:39 (`ls-files -v` shows `H`).
  - **If the abort recurs with a long local backlog, reuse that flag briefly and remove it after.** The durable fix is Wednesday's (proposal mailed).

## ✅ DONE IN s12 (verified)

- Brain whole: by-tier digest 5,437 lines (last heading asserted) + own ledger 101 rows → `ctx:31%`. Boot digests committed. WED board 27 active, 0 `lesson` (board_count.sh). `reconcile_rulings.py`: 55 taps, 0 to rule.
- S40's wrap read whole (DKIM/DMARC pass).
- Kam's two terminal instructions (16:55, 17:00) are in the prompt log. The first entry's swapped arguments were corrected and the correction noted.
- Ledger row: three s12 slips (zsh unsplit git variable read as NO; prompt_log arguments swapped; own dirt held the sync one cycle).
- Panel to Kam at origin: the receipt + 16:48 explanation + plan, and the testing-brief summary + defaults.

## ⚠ NEW TRAPS (s12) — older traps 1–39 are in `.pre-1740`

40. **Cockpit Fresh kills EVERY agent pane.** See the incident above.
41. **`usage_tuesday.json` churn vs panel_sync rebase.** See the incident above.
42. **zsh does not word-split a variable holding a command.** `G="git -C x"; $G log` fails, and an `&& yes || no` then prints "no". Write paths literally; branch on the exact rc.
43. **`prompt_log.sh <channel> <text> [note]`.** Read a tool's usage in a separate action before the first call.
45. **`reconcile_rulings.py` is Wednesday-scoped by construction.**
    - **Where:** line 43, "This seat coordinates Secuura + Wednesday's own work".
    - **What happens:** it SKIPS every Datasec card as "OUT OF SCOPE", even with `WED_AGENT=tuesday`.
    - **Instead:** record Kam's Datasec taps with `WED_AGENT=tuesday decision_queue.sh rule <id> <choice>`, gated in code on `git merge-base --is-ancestor <ls-remote origin sha> HEAD`.
    - **When the gate refuses** (origin just moved): wait for panel_sync's pull. Never run a plain fetch.
46. **A mail watcher's MARK is one second past the newest mail already PROCESSED, never the arming time.**
    - Kam's card taps arrive as `[Kam -> Tuesday] panel message …` (label `sent`), so a watcher regex must match `Kam` too.
    - **Measured 18:1x:** the shared wake runner's own unsent tap line at %0 made it HOLD every later tap. Clear it only by matching its exact `[wake_watch]` text; C-u did not clear it mid-turn, but it submitted at turn end.
44. **Resuming a killed QA gate:** `claude --resume <session>` with `CLAUDE_CONFIG_DIR=TUESDAY/4_Credentials/.claude` and the project's identity dirs. Map a session to its gate by counting mentions of its report dir / compose project in the transcript. The first-prompt heuristic is unreliable, because every gate prompt names A, B and C.
