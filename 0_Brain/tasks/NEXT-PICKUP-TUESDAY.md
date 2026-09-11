---
date: 2026-09-11
type: pickup
scope: DATASEC ONLY — Tuesday, on Kamils-Mac-mini. Secuura and general are Wednesday's, on the Studio.
source: written by Tuesday s7 at its 50% checkpoint and refreshed at its rotation (16:5x), 2026-09-11 09:23 AEST
status: live
supersede: replace WHOLESALE at the next pickup; never append. It replaced s6's pickup (copy in the s7 session scratchpad only).
---

# NEXT PICKUP — Tuesday s8. NexusAI round-3 re-gate running (one message + a GPT-only card owed to Kam on its verdict); HPSM round-4 card defaults at 17:30.

**On EVERY wake: run `2_Project_Files/tools/kam_rulings_today.sh`; list `tuesday-agent@` UNFILTERED and route on SUBJECT (Kam's panel relays are labelled `sent`); run `git status --porcelain | grep -v 0_Brain/dashboard/data/` (any hit blocks Kam's panel sync).** Rotation band 80–90. **Kam reads the Studio: verify panel messages AT ORIGIN** (compare row count + newest row of `git show origin/main:0_Brain/dashboard/data/chat_tuesday.json` with local; a phrase grep failed once this session because the search string was wrong — use rows, not phrases).

## 🔴 LIVE (as of 16:5x, s7 rotating)
1. **NexusAI round-3 RE-GATE — headless tester pid 96425, launched 16:51** on `s51-marketplace-remediation @ b8c4646ab7d271567364876757403bfb8d23cf08` (on origin; 10 commits from `20a723b`) + DRAFT zips `NexusAI/evidence-s54-marketplace-package/DRAFT-submission-package-b8c4646/`. Launcher `qa-agent/launchers/launch_qa_nexusai_mktpkg_b8c4646.sh`; brief `qa-agent/briefs/2026-09-11_nexusai-mktpkg-b8c4646-tier1r3.md`; report due `Testing Agent MAIN/projects/nexusai/reports/2026-09-11-mktpkg-b8c4646-tier1r3/report.md`. **No round 4 without Kam.** The build seat (S54, pid 33321) has EXITED after READY FOR QA 06:49:23Z (verify 2360/2360; B1 `a5593b4`, MAJ-1/2 `bcda8d6`, MAJ-3 template `d80a8c0`, token leak closed at executeQuery + a winston redaction format `09759b2`/`5da1cf7`, proven on the image vs a red control; NOT covered: 109 direct `console.*` calls). **Its wrap mail may still arrive.**
   **OWED WHEN THE VERDICT LANDS — to Kam as ONE message, plus ONE card:** (a) ready for upload or not; (b) **the GPT-only product change** (Kam's 15:00:49 note): the package offers only GPT, but the PRODUCT defaults to Ollama/phi3 when `LLM_PROVIDER` is unset (`model-config.js:34`; `server.js` `|| 'ollama'` sites; images log `LLM adapter active: ollama (phi3:medium)`), and first-run setup lists Phi-3/Ollama as REQUIRED (`static/js/first-run-setup.js:31-32,613,727,859-866`). Source file: `NexusAI/evidence-s54-marketplace-package/ITEM5-non-GPT-AI-mentions-READONLY.txt`. Card: authorise a round 4 (product GPT-only) with rec + default. (c) B2 registry still his. **Then score S54** (strong round; disclose its two `rm`s that removed nothing, under a never-rm hold).
2. **HPSM: round-4 card `hpsm-composer-round4-commit-guard-and-forged-release` OPEN (rec round4). DEFAULT TIME 17:30 AEST, stated to Kam 16:51.** At 17:30 if still open: brief a fresh HPSM seat with the ship pattern (`briefs_staged/2026-09-11_hpsm-s35-ship-default.md`), re-pinned to push `55160dd` fast-forward from `0c3078e`, backlog R3-M1 + S3-F4b (re-graded MAJOR by the gate) + R3-m1. Launch through HPSM's own launcher (`cockpit.sh add 'Datasec/HPSM' "bash '<HPSM>/Launch_Claude.command'"`). **If Kam taps round4:** brief round 4 (pin the guard's tenant at transaction start; `released` only from `approved` with approvals bound to the manifest), RED-first, then gate from `launch_qa_hpsm_composer_55160dd.sh`. No HPSM seat is running now.
3. **Run your own exiting watcher while anything is live** (start mark = the timestamp of the last mail you PROCESSED, passed explicitly; a `now` start misses mail that arrived seconds earlier, which cost s36 12 minutes).

## 🔴 WITH KAM
1. **Full Disk Access for `/bin/bash` (card ruled `grant` 15:22; the TOGGLE is his hands).** Steps sent 15:27. **Not yet on:** a harmless launchd probe at 15:26 exited 126. To re-prove when he says done: `2_Project_Files/fleet/state/tcc_probe.sh` exists (gitignored); build a throwaway plist in YOUR scratchpad with Label `com.tuesday.tccprobe`, ProgramArguments `/bin/bash <that script>`, stdout/stderr into the scratchpad; `launchctl bootstrap` → `kickstart` → read output (`TCC_OK …` = granted; exit 126 = not) → `bootout`. **Never probe with a real ritual or `nas_sync.sh`** (the latter ignores args and would start a sync).
2. **NexusAI AI screenshot: asked 15:0x, unanswered.** Default: install nothing; `rd15-03` unchanged (the gate says its first name stays readable). Card recorded `install-ollama` (his tap), but his note points to GPT-only.
3. **NexusAI registry (B2).** Unanswered; no image built or pushed.
4. **Jira key for the Composer** (rec `HPSML` / "HPSM-light").

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
