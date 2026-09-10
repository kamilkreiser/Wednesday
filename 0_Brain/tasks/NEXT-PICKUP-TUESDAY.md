---
date: 2026-09-11
type: pickup
scope: DATASEC ONLY — Tuesday, on Kamils-Mac-mini. Secuura and general are Wednesday's, on the Studio.
source: written by Tuesday s7 at its 50% checkpoint, 2026-09-11 09:23 AEST
status: live
supersede: replace WHOLESALE at the next pickup; never append. It replaced s6's pickup (copy in the s7 session scratchpad only).
---

# NEXT PICKUP — Tuesday s8. Three Datasec processes are live; one answer is owed to Kam when a gate lands.

**On EVERY wake: run `2_Project_Files/tools/kam_rulings_today.sh`; list `tuesday-agent@` UNFILTERED and route on SUBJECT (Kam's panel relays are labelled `sent`); run `git status --porcelain | grep -v 0_Brain/dashboard/data/` (any hit blocks Kam's panel sync).** Rotation band 80–90. **Kam reads the Studio: verify panel messages AT ORIGIN** (compare row count + newest row of `git show origin/main:0_Brain/dashboard/data/chat_tuesday.json` with local; a phrase grep failed once this session because the search string was wrong — use rows, not phrases).

## 🔴 LIVE
1. **NexusAI round-2 tier-1 gate — pid 38898, headless, launched 09:16.** Launcher `2_Project_Files/fleet/qa-agent/launchers/launch_qa_nexusai_mktpkg_20a723b.sh`; brief `qa-agent/briefs/2026-09-11_nexusai-mktpkg-20a723b-tier1r2.md`. Subject: `s51-marketplace-remediation @ 20a723b` (on origin; main untouched `cd2b543`) **plus the DRAFT zips** at `!CODING/Datasec/NexusAI/evidence-s53-marketplace-package/DRAFT-submission-package-20a723b/`. Report will be at `Testing Agent MAIN/projects/nexusai/reports/2026-09-11-mktpkg-20a723b-tier1r2/report.md`; verdict mail subject `[QA/Datasec-NexusAI -> Tuesday] GATE VERDICT — Marketplace package @ 20a723b (tier 1, round 2)`. **ROUND 2 OF 2 — a NO GO goes to Kam as the list of what blocks upload; no round 3 without him.**
   **OWED TO KAM WHEN IT LANDS — ONE message, whole:** ready for upload or not, plus S53's three before-upload items AS THE GATE MEASURED THEM: (a) the Datasheet PDF embeds a PRE-BLUR image; (b) the deployment wizard defaults to the publisher's DEV ACR; (c) gitleaks hit at `PEN-TEST-REPORT:297`. **SUBMISSION IS KAM'S.** Kam was told at 09:17 that this answer comes as one message.
2. **HPSM session 34 — FIX ROUND, pane `%3` (tmux `fleet`), booted 09:21 through HPSM's own `Launch_Claude.command`.** Brief mailed (gate passed) 09:2x: `briefs_staged/2026-09-11_hpsm-s34-fix-round.md`. Queue: migration fixing M1–M4 with RED-first regression tests + the tester's 3 surviving mutants now RED + cheap Minors → CI green from a clean clone → **READY FOR QA, then stop.** **No push to HPSM-light until the round-2 gate GO and Tuesday's word.** Jira only on a relayed Kam key. **Owed by Tuesday: its plan confirmation (answer it), then on READY FOR QA commission the round-2 gate** — template `qa-agent/launchers/launch_qa_hpsm_composer_a06ada3.sh` (pins head + commit count; a scratch copy keeps absolute paths). **Round 2 of 2.**
3. **Tuesday's own background watchers** are session-local and die with this seat — **a successor re-arms its own** (pattern: a bash loop that EXITS on new non-sent mail after a start time, a report.md appearing, or a pid dying; the tester transcript lives under `$CLAUDE_CONFIG_DIR/projects/…Testing-Agent-MAIN/`, NOT `~/.claude`).

## 🔴 WITH KAM
1. **Jira project key for the Composer — ASKED 08:3x, unanswered.** Rec `HPSML` / "HPSM-light" (mirrors the repo); alternative the seat's `PCOMP` / "Policy Composer". Both absent from the 38 projects the HPSM Jira login lists. **Default if silent: nothing filed.** When he answers: mail HPSM s34 the key (it runs `create_composer_jira.py`).
2. **Card `nexusai-ai-screenshot-local-model`** (install Ollama + phi3:mini) — open; default keeps the old blurred AI image (S53 did so).
3. **Rules engine (WP3):** Tuesday told Kam at 08:3x it starts after the NexusAI package seat finishes, unless he says "now". **Now superseded in practice by the fix round** — WP3 waits for the round-2 GO; say so if he asks.

## ✅ DONE IN s7 (verified at destination or at origin)
- HPSM s33: completion check vs brief — items 1–3 ACCEPTED, GitHub half closed; Strict-posture reading RATIFIED (ARCHITECTURE §1.9 lines 382/388); **tier-1 gate NO GO** (4 Major / 6 Minor / 3 Polish; report `Testing Agent MAIN/projects/hpsm/reports/2026-09-11-composer-a06ada3-tier1/report.md`); M2 scope ruled by Tuesday (tenant sessions never write platform brand profiles; §3.4); s33 wrapped on a SUPERSEDES mail; pane closed via `pane_close.sh %2` (listeners 12→12); scoreboard 0.80.
- NexusAI S53: READY FOR QA @ `20a723b` + wrap received (2312/2312 verify; M1 `4e12089`, m1 `923c265`, 5 re-shots `45589c6`); round-2 gate commissioned.
- Vision swept: **0 open VSP tickets** (control: VSP issues exist, newest 2026-07-03 all Done; login + RD control fire). Nothing to launch.
- Panel: 08:3x boot report + Jira ask; 09:17 HPSM NO GO + NexusAI status — both verified at origin.

## ⚠ TRAPS — carried and new
1. 🔴 **Never `git pull --rebase --autostash` in this tree.** `rebase --continue` wedges: `rebase --abort`, then `git -c core.editor=true merge origin/main`.
2. **`setsid` does not exist on macOS** — `nohup bash … &`; check `ps -o ppid,sess,tty` (tty `??` = detached).
3. **Store writes:** before `decision_queue.sh` writes, gate on no origin-only commit touching `decisions.json`.
4. **zsh:** no `PIPESTATUS`, no word-splitting of unquoted params.
5. **Tool argument asymmetry (NEW):** `cockpit.sh say` takes the pane NAME (`Datasec/HPSM`) — given `%2` it exits **rc 1 with NO stderr**; `pane_close.sh` takes the `%ID` — given the name it refuses rc 2. Both shared tools; not edited.
6. **`wake_watch` frozen-busy leg ignores `wake_ack.sh`** (only the idle leg reads the ack; `wake_watch.sh:195-209` vs `:231`) — a pane holding on a background shell re-fires every ~8 min. Shared tool, Wednesday's to agree; not edited.
7. **Overnight wake silence (ledger 2026-09-11 row):** the runner held every tap on "text at wednesday prompt" 22:05→06:19 and went LOG-ONLY; the ghost-residue hypothesis is WEAKENED (08:44 tap went through unheld). **Test owed when a ghost is visible:** capture `-e` the prompt line and run `arm_wake_watch.sh:157-158`'s perl strip. **Until fixed: every wait carries its own exiting background job.**
8. **Launch outputs:** write `.out` files under `fleet/briefs_staged/` (gitignored), NOT `qa-agent/briefs/` (tracked dir, would block panel sync).
9. **Write + commit in ONE action** for anything outside `dashboard/data` — s7 left a brief uncommitted for one 60 s cycle at 08:38 and panel_sync skipped.
10. Wednesday's 08:20 note of a panel_sync `Cannot rebase onto multiple branches` was on HER log, not this machine's (checked 08:4x).

## NAS — WED-149 (unchanged from s6)
Tuesday's 23:00 leg `com.tuesday.nassync` stays BOOTED OUT until the partition is built INTO the file/plist (launchd passes no env). Kam ruled shared folders are Wednesday's leg; Tuesday syncs Datasec + its own tree only. Design `1_Project_Definition/Architecture/2026-09-10_nas-two-seat-sync-check.md`.

## Undelivered, not yet read into any brief
`rd104-gh-identity-acceptance-false-premise` (gh identity + merges to main) — read before the next NexusAI MERGE brief. Also S53's deferred items (m2 AADSTS text, m3 dockerignore names) need ticketing on RD.
