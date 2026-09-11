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
1. **NexusAI round-2 gate — DONE 09:50: NO GO FOR UPLOAD** (2 Blocker · 3 Major · 5 Minor; report `Testing Agent MAIN/projects/nexusai/reports/2026-09-11-mktpkg-20a723b-tier1r2/report.md`). Code held (M1 fixed in the container vs a red control; 2312/2312; zips byte-equal to git). **B1** Kam's full name legible in the Datasheet PDF's embedded image AND the video thumbnail (the thumbnail was not in S53's list) · **B2** wizard default `nexusaidevacrfa39.azurecr.io/nexusai:2.0.0`: the DEV registry, May image, none of the fixes · **MAJ-1** internal Confidential onboarding guide (VM plan) in the listing bundle · **MAJ-2** ROI one-pager is a marked draft with a garbled example · **MAJ-3** a deploy never sets `USE_AZURE_LOG_ANALYTICS`, so the dashboard reads zeros (pre-existing since May). **Delivered to Kam 09:51 as ONE message + card `nexusai-marketplace-package-round3` (rec `round3`: B1+MAJ-1/2/3, no push/image; default nothing changes). His open QUESTION: which registry customers pull from (B2).** Cap spent: round 3 only on his tap. On `round3`: brief a NexusAI seat (pattern `briefs_staged/2026-09-11_nexusai-marketplace-package.md` + its guarded launcher), then re-gate from `launch_qa_nexusai_mktpkg_20a723b.sh`.
2. **HPSM round-2 tier-1 gate — pid 70475, launched 10:01** on local main `0c3078e8398d016cbbf250712da56585938d734f` (6 commits reachable; NOT pushed, HPSM-light still `a06ada3`). Launcher `qa-agent/launchers/launch_qa_hpsm_composer_0c3078e.sh`; brief `qa-agent/briefs/2026-09-11_hpsm-composer-0c3078e-tier1r2.md`; report due at `Testing Agent MAIN/projects/hpsm/reports/2026-09-11-composer-0c3078e-tier1r2/report.md`. **ROUND 2 OF 2.** HPSM s34 delivered READY FOR QA 23:59:45Z (M1–M4 + label key + m2–m5; RED 18/20 at a06ada3, GREEN 60/60, clean-clone CI 13/13; evidence `HPSM/1_Project_Definition/Architecture/2026-09-10_policy-composer/qa-round2/README.md`) and was told to WRAP at 10:0x. **Tuesday ruled BACKLOG (WP4)** on the caller-supplied-PK existence oracle. **On GO:** tell s34's successor to push `0c3078e` to HPSM-light and verify with ls-remote, score s34, and tell Kam in one line. **On NO GO:** the residue list goes to Kam; no round 3 without him.
3. **Tuesday's own background watchers** are session-local and die with this seat — **a successor re-arms its own** (pattern: a bash loop that EXITS on new non-sent mail after a start time, a report.md appearing, or a pid dying; the tester transcript lives under `$CLAUDE_CONFIG_DIR/projects/…Testing-Agent-MAIN/`, NOT `~/.claude`).

## 🔴 WITH KAM
1. **Jira project key for the Composer — ASKED 08:3x, unanswered.** Rec `HPSML` / "HPSM-light" (mirrors the repo); alternative the seat's `PCOMP` / "Policy Composer". Both absent from the 38 projects the HPSM Jira login lists. **Default if silent: nothing filed.** When he answers: mail HPSM s34 the key (it runs `create_composer_jira.py`).
2. **Card `nexusai-ai-screenshot-local-model`** (install Ollama + phi3:mini) — open; default keeps the old blurred AI image (S53 did so).
3. **Card `tuesday-mac-mini-scheduler-full-disk-access` (filed 09:3x, rec `grant`):** Tuesday's `com.tuesday.shiftchange/.wake/.close` are LOADED and exit **126 'Operation not permitted'** on every fire (launchctl list; `~/Library/Logs/tuesday_*.err`), which is the PORTABILITY item 15 macOS privacy grant (Full Disk Access for `/bin/bash`), still Kam's on this Mac. **Tuesday's NAS leg has NEVER run here** (09-09 23:00, same error). If he grants it: `launchctl kickstart gui/$(id -u)/com.tuesday.close` is NOT the proof, because it spawns a ritual; read the `.err` after the next natural fire instead. Wednesday was told (coordination-only mail 23:32Z, verified at her inbox) and holds the `nas_sync.sh` counter fix.
4. **Rules engine (WP3):** Tuesday told Kam at 08:3x it starts after the NexusAI package seat finishes, unless he says "now". **Now superseded in practice by the fix round** — WP3 waits for the round-2 GO; say so if he asks.

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
