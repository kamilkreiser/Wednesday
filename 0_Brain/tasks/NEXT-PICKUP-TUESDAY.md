---
date: 2026-09-11
type: pickup
scope: DATASEC ONLY — Tuesday, on Kamils-Mac-mini. Secuura and general are Wednesday's, on the Studio.
source: written by Tuesday s8 (booted 2026-09-11 16:5x); refreshed at its 50% checkpoint 2026-09-12 07:1x
status: live
supersede: replace WHOLESALE at the next pickup; never append. It replaced s7's rotation pickup (in git history at 96c967da).
---

# NEXT PICKUP — Tuesday s9. NexusAI S55 is cataloguing the RD board (read-only; plan confirmation due). Two round-4 cards with Kam. ATTIO digest recipient is owed.

**On EVERY wake: run `2_Project_Files/tools/kam_rulings_today.sh`; list `tuesday-agent@` UNFILTERED and route on SUBJECT (Kam's panel relays are labelled `sent`); run `git status --porcelain | grep -v 0_Brain/dashboard/data/` (any hit blocks Kam's panel sync).** Rotation band 80–90. **Kam reads the Studio: verify panel messages AT ORIGIN** (row count + newest row of `git show origin/main:0_Brain/dashboard/data/chat_tuesday.json`). **Do NOT read `0_Brain/daily/`** — it holds only Wednesday's Secuura notes (ledger 2026-09-11 s8 row); Tuesday's episodic state is this file, `_ledger_laptop_datasec.md` and `git log`.

## 🔴 LIVE (as of 2026-09-12 07:1x)
1. **NexusAI S55 — pane `%7`, launched 07:11 through NexusAI's own launcher** (sets its own `AZURE_CONFIG_DIR`/`GH_CONFIG_DIR`, so trap 8a does not apply). Brief `2_Project_Files/fleet/briefs_staged/2026-09-12_nexusai-s55-board-catalogue.md`, **verified at `datasec-nexusai@` 21:10:38Z**. Commission: ITEM 0 only — per-ticket catalogue of RD To Do (117) + In Progress (6) → `NexusAI/5_Project_History/2026-09-12_S55_rd-board-catalogue.md` → QUESTION plan confirmation with ≤5 category-1 tickets → STOP. Read-only board; Marketplace branch and stale main tree untouched. **Launch proof so far is weak** (a pane keyword hit, not the brief text) — the plan-confirmation mail is the real proof. **Owed:** read the catalogue (spot-check rows in BOTH directions), confirm or trim the queue, then its build rounds go RED-first → READY FOR QA → gate.
2. **Watcher:** `scratchpad/watch_s8.sh 2026-09-11T21:10:38Z <%7 pane pid> 10:30` running in the background.
3. **HPSM:** nothing running. `55160dd` shipped 2026-09-11 (s37 scored 1.00). Card `hpsm-composer-round4-commit-guard-and-forged-release` OPEN; if Kam taps round4, brief a fresh seat (tenant pinned at transaction start; `released` only from `approved`), RED-first, STOP at READY FOR QA.
4. **NexusAI package:** NO GO FOR UPLOAD (round-3 gate 2026-09-11 07:26:47Z). Card `nexusai-marketplace-round4-gpt-only-product` OPEN (rec round4; default hold). If Kam taps round4: a SEPARATE seat, launched through NexusAI's own launcher, on `s51-marketplace-remediation` — tell S55 first so the catalogue seat stays off it.
5. **ATTIO follow-up digest still goes to `wednesday-agent@`** (Wednesday flagged it 2026-09-12 07:02, coordination only; Tuesday ACKed 21:05Z and took the routing). It is residue of Kam's 09-10 `amend` ruling (card `fleet-comms-names-one-coordinator`, already marked delivered for the workspace CLAUDE.md). The recipient is env `FOLLOWUP_DIGEST_TO` (`ATTIO/2_Project_Files/src/config.js:94`), read by the deployed job; the ATTIO rules put Vision's prod RG under never-touch-prod, and WHICH app holds the setting is UNMEASURED. Vision's `Launch_Claude.command:263` also still names `wednesday-agent@` for wraps. **Owed:** at the next ATTIO/Vision session, brief the seat to measure where the setting lives, change it to `tuesday-agent@`, flag it to Kam as a production change BEFORE doing it, and fix the launcher line. Not carded: his ruling covers it.

## 🔴 WITH KAM
1. **NexusAI round-4 card** (above). 2. **HPSM round-4 card** (default already fired; tap still switches). 3. **Full Disk Access for `/bin/bash`** (ruled `grant` 15:22; the toggle is his hands; not on at 15:26 — probe exit 126). Re-prove with a throwaway plist in the scratchpad running `2_Project_Files/fleet/state/tcc_probe.sh` (`TCC_OK` = granted, 126 = not); never probe with a real ritual or `nas_sync.sh`. 4. **NexusAI registry (B2).** 5. **Jira key for the Composer** (rec `HPSML`). 6. **From S54, told to Kam 17:35:** any environment that ran failing Log Analytics queries with a real token may hold tokens in its log store — unmeasured. 7. MIN-4 (owner name/email in the Datasheet PDF text) is his, unchanged.
8. **Told 17:4x (panel row 127, verified at origin):** this Mac's Docker holds 81 orphaned anonymous volumes (~4.8 GB) from HPSM `test-db.sh` runs (R3-m2). Removing them is his call; nobody has pruned them.

## ✅ DONE IN s8
- 2026-09-12 morning sweep: Vision VSP 0 open (control: 64 total); NexusAI RD 117 To Do / 6 In Progress / ~296 not Done (Jira approximate-count). Marked `nexusai-marketplace-package-round3` delivered. S55 launched on the catalogue. Ledger row: a read-back listed Wednesday's inbox (a Secuura subject line shown) — verify cross-seat mail from Tuesday's own `sent` copy.
- HPSM s37 shipped `55160dd` (verified at remote), scored 1.00, pane closed; 81 orphaned HPSM test volumes told to Kam.
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
