---
date: 2026-09-12
type: pickup
scope: DATASEC ONLY — Tuesday, on Kamils-Mac-mini. Secuura and general are Wednesday's, on the Studio.
source: written WHOLESALE by Tuesday s8 at its rotation (ctx ~78%), 2026-09-12 09:1x AEST. s8 booted 2026-09-11 16:5x.
status: live
supersede: replace WHOLESALE at the next pickup; never append.
---

# NEXT PICKUP — Tuesday s9. FOUR things live: HPSM s38 round 4 · NexusAI S56 Marketplace round 4 · QA tier-1 gate on RD-372 · S57 to launch for RD-342. Nothing waits on Kam except his optional asks.

**On EVERY wake:** run `2_Project_Files/tools/kam_rulings_today.sh` AND read `[Kam -> Tuesday] panel message` mails (the mails are FRESHER than the local store — both of today's round-4 taps showed there first while the tool read 0); list `tuesday-agent@` UNFILTERED and route on SUBJECT; `git status --porcelain | grep -v 0_Brain/dashboard/data/`. Rotation band 80–90. **Kam reads the Studio: verify panel messages AT ORIGIN — never with a plain `git fetch` (trap 14).** **Do NOT read `0_Brain/daily/`** (Wednesday's, Secuura).

## 🔴 LIVE — with the next action for each
1. **HPSM session 38 — pane `%10` (`Datasec/HPSM`), ROUND 4 on Kam's tap (08:50:50, recorded on the card).** Brief `2_Project_Files/fleet/briefs_staged/2026-09-12_hpsm-s38-round4.md`. **Plan CONFIRMED 23:09:59Z** (`…/2026-09-12_hpsm-s38-answer-plan.md`): R3-M1 guard evaluates under the ROW's tenant (design received; the gate judges it) + A-45 refused at the service call; S3-F4b `released` only from `approved` with tech + customer approvals bound to the hash; **Q2 IN** (writing directly to `superseded` refused too); Q1 = the gate's `L-legit-lifecycle.sql` runs UNCHANGED (line-64 refusal = rule working) plus an L6-only copy that must give 0 errors; flag 1 = guarded removal of s38's OWN docker volumes only (the 81 stay). Expected 2 commits on `55160dd2cec6ae5eed5a040405e6abf2d2a375aa` (tests + migration `0006`). **NEXT:** READY FOR QA → tier-1 gate brief that **MUST re-seed the gate's F1 fixture** for scripts that load it (s38 names them in READY); launch the gate in a PANE (copy `qa-agent/launchers/launch_qa_nexusai_rd372_abdb136.sh`'s shape with HPSM's identity dirs); push only on GO + Tuesday's word. **No round 5 without Kam.** **Kam told the Q2 reading on the panel 09:13 (row 133)** — if he narrows it, SUPERSEDES mail to s38 before its release-rule commit.
2. **NexusAI S56 — pane `%11` (`Datasec/NexusAI-B`), Marketplace ROUND 4 on Kam's tap (08:50:53, recorded).** Worktree `NexusAI/wt-s51-mktremed`, branch `s51-marketplace-remediation` from `b8c4646ab7d271567364876757403bfb8d23cf08`. Brief `…/2026-09-12_nexusai-s56-mktpkg-round4.md`; launcher `qa-agent/launchers/launch_nexusai_s56_round4_pane.sh` (NexusAI identity dirs). **Plan CONFIRMED 23:07:23Z** (`…/2026-09-12_nexusai-s56-answer-plan.md`): ⚑A wizard AOAI fields OPTIONAL + `LLM_PROVIDER=azure-openai` unconditional in the template · ⚑B OPTION 1 — ollama/onnx adapter code stays UNREACHABLE on package deployments (Option 2 = delete 236 lines → BACKLOG); **Kam was told this reading on the panel (verified at origin, row 132) — if he says remove the code, SUPERSEDES mail before S56's item-2 edits** · ⚑C local throwaway images `s56-mktpkg:<sha7>`, no registry · push with explicit refspec ONLY (the branch tracks `main` in the shared `.git/config`). **It SHARES `datasec-nexusai@` with NexusAI seats** — its subjects say S56 / Marketplace round 4. **NEXT:** READY FOR QA → tier-1 gate (package zips + real-browser AI setup save reaches AOAI + `LLM hydrated from jsonStorage: azure-openai` after restart + K3 masking + census classes 0 with the labelled adapter-code class) → **Kam gets "ready for upload or not"**. B2 (registry) still his.
3. **QA TIER-1 GATE on RD-372 @ `abdb136f860048911fa79c54a7fbb78332b5ca0e` — pane `%9`, pid 99934, launched 08:39** from `qa-agent/launchers/launch_qa_nexusai_rd372_abdb136.sh`. Report due `!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-12-rd372-abdb136-tier1/report.md`; subject `[QA/Datasec-NexusAI -> Tuesday] GATE VERDICT — RD-372 @ abdb136 (tier 1)`. **NEXT on verdict:** completion check, score, close pane; merge only on GO (by a NexusAI seat, counts regenerated).
4. **LAUNCH S57 (NexusAI) from `NexusAI/HANDOVER-S55.md`** for **RD-342** in its RULED shape (Tuesday 22:40:18Z: `pre-merge-commit` hook scanning merges + loud-every-commit instead of the one-time sentinel + launcher preflight reports absent gitleaks; NOT fail-closed; gitleaks install is Kam's) then **RD-327** (unblocked; RD-293 merged). Launch as pane `Datasec/NexusAI` via NexusAI's OWN `Launch_Claude.command` (`cockpit.sh add`, not `launch`). Brief sections: **YOU SHARE THE INBOX WITH S56** · worktrees `--no-track`, push without `-u` (S55 proved it leaves `.git/config` untouched) · base on `main` `ae2588bfd60a1f9f22130aa794378382e3aab629` · RED-first · per-ticket READY FOR QA · Tuesday reads its statusline at each READY.

## 🟡 OWED GATES (queue, one full suite at a time where possible)
- **RD-150 @ `bec76f686de5415090350117437d11d1a49acb82`** (from `cd2b543`, 4 files) — tier 1: 94 `getSetting` sites, two kill switches now take effect (`red_flag_enabled`, `aiEnabled`). **Record the behaviour change for any deploy decision.**
- **RD-382 @ `d4d3bfbf46211d93159a13d5b2e8510f11e6c425`** (from `ae2588b`, 6 files, tooling) — tier 2 through-code.
- **Merge arithmetic:** `main` `ae2588b` = 2283/118; after RD-372 + RD-150 + RD-382 merge = **2303/121**; each merge regenerates with `npm run verify -- --update-counts`, never copied.

## ✅ DONE IN s8 (verified at source or origin)
- HPSM s37 pushed `55160dd` (fast-forward from `0c3078e`), scored 1.00. NexusAI package round 3 gated NO GO FOR UPLOAD; S54 scored 0.85.
- Morning sweep: Vision 0 open; NexusAI RD catalogued by S55 (123 = 77 cat-1 / 22 cat-2 / 16 cat-3 / 8 archive; `NexusAI/5_Project_History/2026-09-12_S55_rd-board-catalogue.md`).
- **S55 (wrapped 09:09, pane closed, listeners 14→14; scored in the scoreboard):** RD-293 merged `ae2588b` after tier-2 GO WITH FINDINGS; **RD-387** filed for its findings (verified: To Do, Relates RD-293); `NexusAI/CLAUDE.md:222(b)` corrected (verified: the old wording survives only as a quote inside the correction) with quarantined copy; RD-372/RD-150/RD-382 READY; 7 closed to Done with measurements (incl. RD-295 on `nexusai-rd296-sizing-2026-09-04`); RD-382 launcher-line comment (verified); history on branch `s55-history-docs` @ `a39e93d` (NOT merged).
- Board rulings recorded: both round-4 cards ruled; `nexusai-marketplace-package-round3` delivered.
- Panel (all verified at origin): morning note (128); 08:40 consolidated asks (129: gitleaks install optional · RD-281 acceptance question · vault drift · RD-367 dead premise); round-4 receipts (130, 131); ⚑B reading (132).

## 🔴 WITH KAM (asked; nothing blocks)
1. `brew install gitleaks` on the Mac mini (optional; RD-342 ruled not to need it).
2. **RD-281:** did he accept the rebuilt Sustainability tab render?
3. Full Disk Access for `/bin/bash` (ruled `grant` 2026-09-11; the toggle is his hands; last probe exit 126).
4. NexusAI registry (B2). 5. Jira key for the HPSM Composer (rec `HPSML`).
6. His vault `Notes (MASTER)` on the T9: 484 behind, 102 uncommitted paths from other sessions.
7. RD-367's premise is dead (told); branching-model decision half is his.
8. **ATTIO follow-up digest still goes to `wednesday-agent@`** — covered by his 09-10 `amend` ruling (card `fleet-comms-names-one-coordinator`, delivered for the workspace CLAUDE.md). Recipient = env `FOLLOWUP_DIGEST_TO` (`ATTIO/2_Project_Files/src/config.js:94`) in the deployed job; app UNMEASURED. **At the next ATTIO/Vision session:** measure where it lives, flag to Kam as a production change BEFORE changing, fix `Vision_Sales_Portal/Launch_Claude.command:263`'s wrap address too.

## ⚠ TRAPS
1. 🔴 **Never `git pull --rebase --autostash` in this tree.** Wedged rebase: `rebase --abort`, then `git -c core.editor=true merge origin/main`.
2. `setsid` does not exist on macOS — `nohup bash … &`.
3. **Store writes:** gate on `git merge-base --is-ancestor $(git ls-remote origin refs/heads/main | cut -f1) HEAD` first; a stale store refuses — wait one panel_sync cycle and retry.
4. **zsh:** no `PIPESTATUS`; **no word-splitting of `$VAR` in `for f in $VAR`** (bit s8's manual merge at 08:48) — loop in python; `echo =====` errors.
5. `cockpit.sh say` takes the pane NAME; `pane_close.sh` takes the `%ID`.
6. `wake_watch` frozen-busy leg fires every ~8 min while a background watcher runs — check the watcher output + inbox, nothing more.
7. Run your own exiting watcher while anything is live: `scratchpad/watch_s8.sh <mark> <pid> <deadline>` (exits on newer inbound mail, pid death, or deadline) — mark = last PROCESSED mail's timestamp. A successor writes its own copy.
8. Launch outputs go under `fleet/briefs_staged/*.out` (gitignored).
9. **Write + commit in ONE action** outside `dashboard/data`; **two commits in parallel tool calls collide on `index.lock`** — put both in one command.
10. `decision_queue.sh add --json` cannot take `--override-prior-rulings`; use the flag form built in python.
11. `kam_rulings_today.sh`'s FRESHNESS line counts agent rows, and its store LAGS Kam's taps; the `[Kam -> Tuesday]` mails do not.
12. `wake_watch` wakes this seat for Kam's `view=wednesday` messages — check `kam_msgs.sh`'s view.
13. `cockpit.sh launch` cannot start Datasec projects here (`launchers.conf` pins DevMASTER); use `cockpit.sh add`.
14. 🔴 **Never plain `git fetch` in a verify loop** — it races panel_sync (`Cannot rebase onto multiple branches`). Use `git ls-remote` + `git fetch --no-write-fetch-head origin main` + `git show <sha>:<path>`, polling ≥60 s.
15. **Launch QA gates and build seats in a tmux PANE, never nohup headless** — a headless turn that ends to wait is a dead gate (RD-293 gate died 08:03; resumed in a pane). **The Testing Agent MAIN / NexusAI folder-trust dialog appears on pane launches:** "Yes, I trust this folder" (Down, Enter).
16. **The card-ID send gate refuses a card id the store cannot show** — copy ids from `decision_queue.sh list`, never from a ticket comment (`nexusai-rd296-sizing` was truncated; real id `…-2026-09-04`).
17. **`send_brief.sh` subjects still carry the hard-coded `[Wednesday -> …]` prefix** while the sender is correctly `tuesday-agent@` — known, harmless; routing matches on project.

## NAS — WED-149 (unchanged)
Tuesday's 23:00 leg `com.tuesday.nassync` stays BOOTED OUT until the partition is built INTO the file/plist. Design `1_Project_Definition/Architecture/2026-09-10_nas-two-seat-sync-check.md`.

## OWED, not started
- **Amend step 5 of `Launch_Tuesday.command`** (Tuesday has no daily note; name the pickup, ledger and `git log`), red-proofed by a boot — not while a seat's respawn depends on it mid-task.
- `rd104-gh-identity-acceptance-false-premise` — read before the next NexusAI MERGE brief.
- S53's m2/m3, S54's 8 BACKLOG items and round-3 NEW-3/NEW-4 need ticketing on RD.
