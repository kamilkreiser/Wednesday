---
date: 2026-09-11
type: pickup
scope: DATASEC ONLY — Tuesday, on Kamils-Mac-mini. Secuura and general are Wednesday's, on the Studio.
source: written by Tuesday s7 at its 50% checkpoint, 2026-09-11 09:23 AEST
status: live
supersede: replace WHOLESALE at the next pickup; never append. It replaced s6's pickup (copy in the s7 session scratchpad only).
---

# NEXT PICKUP — Tuesday s8. NexusAI round 3 building; HPSM round-3 gate running; Kam holds the FDA toggle, the AI-screenshot question, the registry and the Jira key.

**On EVERY wake: run `2_Project_Files/tools/kam_rulings_today.sh`; list `tuesday-agent@` UNFILTERED and route on SUBJECT (Kam's panel relays are labelled `sent`); run `git status --porcelain | grep -v 0_Brain/dashboard/data/` (any hit blocks Kam's panel sync).** Rotation band 80–90. **Kam reads the Studio: verify panel messages AT ORIGIN** (compare row count + newest row of `git show origin/main:0_Brain/dashboard/data/chat_tuesday.json` with local; a phrase grep failed once this session because the search string was wrong — use rows, not phrases).

## 🔴 LIVE — KAM RULED BOTH ROUND-3 CARDS AT 14:59 (verbatim in panel relay mails 04:59:31Z / 04:59:38Z)
1. **NexusAI Marketplace package ROUND 3 — headless pid 33321, launched 15:04** by `2_Project_Files/fleet/launch_nexusai_mktpkg_round3.sh`; brief `briefs_staged/2026-09-11_nexusai-mktpkg-round3.md` (sent through the gate). Queue: B1 (Kam's name out of the Datasheet PDF + video thumbnail), MAJ-1/MAJ-2 (drop the internal onboarding guide + draft ROI one-pager from the listing bundle), MAJ-3 (Log Analytics on deploy), **item 5 READ-ONLY: enumerate every non-GPT AI option in the package (Kam's 15:00 note)**, verify, rebuild zips into `evidence-s54-marketplace-package/`, push the feature branch, **READY FOR QA, stop.** B2 (registry) NOT in scope. **🔴 15:55 FINDING, owed to Kam with the verdict:** a PRE-EXISTING **Azure access token leak into container logs** (axios error `Authorization: Bearer` nested in log meta; `logger.js:36` sanitiser only unwraps top-level errors), plus full workspace/tenant IDs, reachable from the package via MAJ-3. Tuesday ruled: fix at `executeQuery` + `connectionTestLogMeta()` (seat's) **and** a logger-level deep redaction (class fix), with red cells via a non-executeQuery path plus a negative control; bound: name any transport that bypasses the formatter. **The re-gate brief must attack the logger redaction hardest** (other axios clients, transports, cycle/depth). **On READY FOR QA: commission the round-3 re-gate** from `qa-agent/launchers/launch_qa_nexusai_mktpkg_20a723b.sh` (new head, new count, round-2 report path as PRIOR ROUND).
2. **HPSM round-3 gate DONE 15:59: NO GO, 1 Major + 1 Minor** (report `Testing Agent MAIN/projects/hpsm/reports/2026-09-11-composer-55160dd-tier1r3/report.md`). Everything round 3 commissioned is confirmed FIXED. **R3-M1:** the deferred approver guard runs at COMMIT under the then-current tenant; clearing or switching tenant before commit fails OPEN (0 approvers; also via the atomic creation service). PREDATES round 3. **R3-m1:** D2's rewrite left no test on `engagement_cloned_from_version_fkey`. **Gate RE-GRADED S3-F4b to MAJOR:** a version can be INSERTed or UPDATEd straight to `released` with 0 approvals and becomes app-immutable (honesty class). **Card `hpsm-composer-round4-commit-guard-and-forged-release` filed 16:0x (rec `round4`; DEFAULT = ship: a fresh HPSM seat pushes `55160dd` fast-forward, backlogs R3-M1/F4b/R3-m1).** Kam told 16:0x. s36 scored 0.90. No HPSM seat running. **HPSM-light main is still `0c3078e`.** **Default time set by s7: 17:30 AEST** (to be stated to Kam in the next panel message, with the NexusAI result). If the card is still open at 17:30, brief a fresh HPSM seat with the ship-default pattern (`briefs_staged/2026-09-11_hpsm-s35-ship-default.md`, re-pinned to push `55160dd` fast-forward from `0c3078e` and backlog R3-M1/F4b/R3-m1).
3. **Run your own exiting watcher while either is live** (the tester transcript lives under `$CLAUDE_CONFIG_DIR/projects/`).

## 🔴 WITH KAM
1. **NexusAI AI screenshot: AMBIGUOUS, asked 15:0x.** He tapped `install-ollama` (recorded as ruled) with the note, verbatim: *"Nexus II needs to be launched to the marketplace with GPT as its only option. No need for a VM with Fire 3."* (= NexusAI / phi3). **Asked ONE question:** install Ollama+phi3 on this Mac for the screenshot, or shoot it on GPT? **Default: install nothing; `rd15-03` unchanged.** His GPT-only note may also mean a PRODUCT change (the round-3 seat's item 5 enumerates the non-GPT options; take its list to him).
2. **NexusAI registry (B2):** which registry customers pull from. Unanswered; no image is built or pushed.
3. **Card `tuesday-mac-mini-scheduler-full-disk-access`** (rec `grant`): Tuesday's 05:30/06:00/23:00 rituals exit 126 (TCC). Open.
4. **Jira key for the Composer** (rec `HPSML` / "HPSM-light"). Open since 08:3x.

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
7. **Overnight wake silence (ledger 2026-09-11 row): the ghost-residue hypothesis is REFUTED** (10:04 live test on a real ghost, with positive and negative controls: the runner strips it to empty). Whatever held every tap 22:05→06:19 was REAL non-dim text at s6's prompt, and which kind is unmeasured. **The narrowed fix, Wednesday's to agree:** log the residue text on each `tap held` line. **Until then: while a seat or gate is LIVE, run your own exiting background watcher. With NOTHING live, do not.** The runner delivered every mail wake 10:34–11:41 (runner log). An idle watcher shell only makes the frozen-busy leg wake this seat's own pane every ~8 min, which is what s7 did from 10:42 until it stopped the watcher at 12:05.
8a. 🔴 **Headless launchers INHERIT TUESDAY'S IDENTITY POINTERS (NEW, measured by the NexusAI round-3 seat 05:11Z):** `launch_nexusai_*.sh` exec `claude` from Tuesday's shell, so the seat's `AZURE_CONFIG_DIR`/`GH_CONFIG_DIR` point at `TUESDAY/4_Credentials`, not the project's own. That is safe only while the brief holds no az/gh. **Before the next NexusAI launcher: export the project's own `4_Credentials/.azure` and `.gh-config` in the launcher (the project's own `Launch_Claude.command` does), and red-proof it.**
8. **Launch outputs:** write `.out` files under `fleet/briefs_staged/` (gitignored), NOT `qa-agent/briefs/` (tracked dir, would block panel sync).
9. **Write + commit in ONE action** for anything outside `dashboard/data` — s7 left a brief uncommitted for one 60 s cycle at 08:38 and panel_sync skipped.
10. Wednesday's 08:20 note of a panel_sync `Cannot rebase onto multiple branches` was on HER log, not this machine's (checked 08:4x).

## NAS — WED-149 (unchanged from s6)
Tuesday's 23:00 leg `com.tuesday.nassync` stays BOOTED OUT until the partition is built INTO the file/plist (launchd passes no env). Kam ruled shared folders are Wednesday's leg; Tuesday syncs Datasec + its own tree only. Design `1_Project_Definition/Architecture/2026-09-10_nas-two-seat-sync-check.md`.

## Undelivered, not yet read into any brief
`rd104-gh-identity-acceptance-false-premise` (gh identity + merges to main) — read before the next NexusAI MERGE brief. Also S53's deferred items (m2 AADSTS text, m3 dockerignore names) need ticketing on RD.
