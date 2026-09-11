---
date: 2026-09-11
type: pickup
scope: DATASEC ONLY — Tuesday, on Kamils-Mac-mini. Secuura and general are Wednesday's, on the Studio.
source: written by Tuesday s8 at 17:4x after the NexusAI round-3 verdict and the HPSM 17:30 default (s8 booted 16:5x)
status: live
supersede: replace WHOLESALE at the next pickup; never append. It replaced s7's rotation pickup (in git history at 96c967da).
---

# NEXT PICKUP — Tuesday s9. Floor EMPTY (no agents). HPSM `55160dd` shipped. NexusAI package NO GO FOR UPLOAD; two round-4 cards with Kam.

**On EVERY wake: run `2_Project_Files/tools/kam_rulings_today.sh`; list `tuesday-agent@` UNFILTERED and route on SUBJECT (Kam's panel relays are labelled `sent`); run `git status --porcelain | grep -v 0_Brain/dashboard/data/` (any hit blocks Kam's panel sync).** Rotation band 80–90. **Kam reads the Studio: verify panel messages AT ORIGIN** (row count + newest row of `git show origin/main:0_Brain/dashboard/data/chat_tuesday.json`). **Do NOT read `0_Brain/daily/`** — it holds only Wednesday's Secuura notes (ledger 2026-09-11 s8 row); Tuesday's episodic state is this file, `_ledger_laptop_datasec.md` and `git log`.

## 🔴 LIVE (as of 17:4x)
1. **HPSM s37 DONE, scored 1.00, pane `%6` closed 17:4x.** `ls-remote` HPSM-light main = `55160dd2cec6ae5eed5a040405e6abf2d2a375aa`, a fast-forward from `0c3078e`, verified by Tuesday. Residue is in HPSM `BACKLOG.md`: R3-M1, S3-F4 (F4b Major), R3-m1, R3-m2, U-0005 (§6). **No HPSM seat is running.** Card `hpsm-composer-round4-commit-guard-and-forged-release` stays OPEN. **If Kam taps `round4`:** brief a fresh HPSM seat for round 4 (pin the guard's tenant at transaction start; `released` only from `approved` with approvals bound to the manifest), RED-first, STOP at READY FOR QA, then gate on the `launch_qa_hpsm_composer_*.sh` pattern.
2. **NexusAI Marketplace package: round-3 gate NO GO FOR UPLOAD** (verdict 07:26:47Z, spf/dkim/dmarc pass; report `!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-11-mktpkg-b8c4646-tier1r3/report.md`). All round-3 items fixed. Stops upload: **B2 registry (carried, Kam's)**, **NEW-1 BLOCKER pre-existing: a wizard deployment runs Ollama/Phi-3 and the in-app AI setup cannot switch to Azure OpenAI GPT (`server.js:15736` ollama branch returns success before the AOAI branch `:15775`; validator rejects `gpt-4.1`)**, **NEW-2 MAJOR: tenant IDs in the log at `azureLogAnalytics.js:343`**, NEW-3/NEW-4 logger Minors. **Card `nexusai-marketplace-round4-gpt-only-product` filed 17:28 (rec round4; default hold: package stays DRAFT, findings backlogged by the next NexusAI seat).** Kam told on the panel 17:35, **verified at origin (126 rows, newest row is that message)**. S54 scored 0.85. No NexusAI seat is running. **If Kam taps round4:** brief a NexusAI seat (NEW-1 + the item-5 product changes + NEW-2; Minors to backlog), RED-first, STOP at READY FOR QA — **and fix trap 8a in its launcher first.**
3. **Watcher:** nothing is live, so no watcher is armed (trap 7). When something is, s8's pattern was `scratchpad/watch_s8.sh <mark> <pid> <deadline>` in the background (exits on inbound mail newer than mark, the pid dying, or the deadline). A successor writes its own; the mark is the timestamp of the last mail it PROCESSED.

## 🔴 WITH KAM
1. **NexusAI round-4 card** (above). 2. **HPSM round-4 card** (default already fired; tap still switches). 3. **Full Disk Access for `/bin/bash`** (ruled `grant` 15:22; the toggle is his hands; not on at 15:26 — probe exit 126). Re-prove with a throwaway plist in the scratchpad running `2_Project_Files/fleet/state/tcc_probe.sh` (`TCC_OK` = granted, 126 = not); never probe with a real ritual or `nas_sync.sh`. 4. **NexusAI registry (B2).** 5. **Jira key for the Composer** (rec `HPSML`). 6. **From S54, told to Kam 17:35:** any environment that ran failing Log Analytics queries with a real token may hold tokens in its log store — unmeasured. 7. MIN-4 (owner name/email in the Datasheet PDF text) is his, unchanged.
8. **Told 17:4x (panel row 127, verified at origin):** this Mac's Docker holds 81 orphaned anonymous volumes (~4.8 GB) from HPSM `test-db.sh` runs (R3-m2). Removing them is his call; nobody has pruned them.

## ✅ DONE IN s8
- Boot: by-tier digest whole (154 files), own ledger whole; ctx 26% after the digest, 41% at 17:3x. Linear WED active 26; `lesson` label exists and has never been used (true zero).
- NexusAI S54 wrap read (spf/dkim/dmarc pass); verdict read; card filed; S54 scored; Kam told, verified at origin.
- HPSM s37 brief staged 16:59, card still unruled at 17:30:09 → sent, verified at destination, launched (pane content shows the seat booting on the round-3 report).
- Ledger row: boot step 5 points this seat at Wednesday's Secuura daily note.

## ⚠ TRAPS — carried and new
1. 🔴 **Never `git pull --rebase --autostash` in this tree.** A wedged rebase: `rebase --abort`, then `git -c core.editor=true merge origin/main`.
2. **`setsid` does not exist on macOS** — `nohup bash … &`; check `ps -o ppid,sess,tty` (tty `??` = detached).
3. **Store writes:** before `decision_queue.sh` writes, gate on no origin-only commit touching `decisions.json`.
4. **zsh:** no `PIPESTATUS`, no word-splitting of unquoted params, and `echo =====` is an `=`-expansion error.
5. **Tool argument asymmetry:** `cockpit.sh say` takes the pane NAME (`Datasec/HPSM`; `%6` exits rc 1 with no stderr); `pane_close.sh` takes the `%ID`.
6. **`wake_watch` frozen-busy leg ignores `wake_ack.sh`** — while a background watcher runs, this pane gets a BUSY/FROZEN wake every ~8 min. Check the watcher output and the inbox; nothing else.
7. **Overnight wake silence:** the ghost-residue hypothesis is refuted; the cause is unmeasured. Run your own exiting watcher while anything is live; with nothing live, do not.
8a. 🔴 **Headless NexusAI launchers inherit Tuesday's `AZURE_CONFIG_DIR`/`GH_CONFIG_DIR`.** Export the project's own `4_Credentials/.azure` and `.gh-config` in the launcher and red-proof it before the next NexusAI launch.
8. Launch outputs go under `fleet/briefs_staged/*.out` (gitignored), not `qa-agent/briefs/`.
9. **Write + commit in ONE action** for anything outside `dashboard/data`.
10. **`decision_queue.sh add --json` cannot take `--override-prior-rulings`** (the flag loop breaks at `--json`). Use the flag form; build the argv in python from a JSON file.
11. **`kam_rulings_today.sh`'s FRESHNESS line counts agent rows** — at 17:24 its "newest 17:04:15" was Wednesday's own post, not Kam.
12. **`wake_watch` wakes this seat for Kam's `view=wednesday` messages.** Read the `view` with `kam_msgs.sh` and leave hers alone (16:55–16:58 today: Secuura, Stuart).
13. `cockpit.sh launch` cannot start Datasec projects here (`launchers.conf` pins DevMASTER); use `cockpit.sh add` with the T9 launcher path.

## NAS — WED-149 (unchanged)
Tuesday's 23:00 leg `com.tuesday.nassync` stays BOOTED OUT until the partition is built INTO the file/plist (launchd passes no env). Shared folders are Wednesday's leg; Tuesday syncs Datasec + its own tree only. Design `1_Project_Definition/Architecture/2026-09-10_nas-two-seat-sync-check.md`.

## OWED, not yet started
- **Amend step 5 of `Launch_Tuesday.command`** to name Tuesday's real episodic sources (not `0_Brain/daily/`), red-proofed by a boot; tell Wednesday by coordination mail that her daily notes are readable from the Datasec seat by instruction. Not while a seat's respawn depends on it mid-task.
- `rd104-gh-identity-acceptance-false-premise` — read before the next NexusAI MERGE brief. S53's deferred m2 (AADSTS text) and m3 (dockerignore names), plus S54's 8 BACKLOG items, need ticketing on RD.
