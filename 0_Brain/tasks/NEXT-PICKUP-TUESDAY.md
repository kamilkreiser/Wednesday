---
date: 2026-09-11
type: pickup
scope: DATASEC ONLY — Tuesday, on Kamils-Mac-mini. Secuura and general are Wednesday's, on the Studio.
source: written by Tuesday s6 at its rotation, 2026-09-11 08:2x AEST
status: live
supersede: replace WHOLESALE at the next pickup; never append. It replaced s5's pickup (copy in the s6 session scratchpad only).
---

# NEXT PICKUP — Tuesday s7. Two seats are live and both will mail you. Kam holds three asks. Nothing is on fire.

**Run `2_Project_Files/tools/kam_rulings_today.sh` first. On EVERY wake: list `tuesday-agent@` UNFILTERED and route on SUBJECT (Kam's panel mails are labelled `sent`, never `received`), and run `git status --porcelain | grep -v 0_Brain/dashboard/data/` — any hit blocks Kam's panel sync.** Rotation band 80–90. **Kam reads the Studio pane: verify every message AT ORIGIN** (`git show origin/main:0_Brain/dashboard/data/chat_tuesday.json`).

## 🔴 LIVE — TWO SEATS, BOTH REPORT TO tuesday-agent@

1. **NexusAI MARKETPLACE PACKAGE seat** — headless, pid 3514, launched 08:18:58 by `2_Project_Files/fleet/launch_nexusai_marketplace_package.sh`; brief `2_Project_Files/fleet/briefs_staged/2026-09-11_nexusai-marketplace-package.md` (sent through the gate, read back). Kam, 08:06: *"is the Nexus AI zip file for Azure Marketplace submission ready?"* + *"Don't forget all the screenshots and everything else."* **Queue:** push `s51-marketplace-remediation` (NEVER main — a main push deploys the demo VM) · fix M1 (client secret in the container log, `backend/server.js:15961`) as its own commit · fix m1 (Back-navigation ghost value, from `ec7a3ad`) · re-shoot ~6 listing screenshots on the synthetic feed · DRAFT zip from a clean extract · **STOP at READY FOR QA.** **Its plan confirmation is imminent — answer it.** On READY FOR QA: commission a re-gate on the new head, pattern `2_Project_Files/fleet/qa-agent/launchers/launch_qa_nexusai_s51remed.sh` (that launcher pins `ed8b208`; the new one pins the new head and its range). **Red-proof note: these launchers self-locate, so a scratch copy must pin BRIEF absolute or it refuses at rc 4 before reaching the guard you mean to test.**
2. **HPSM BUILD seat** — interactive, pane `%2` (tmux session `fleet`), booted through HPSM's own `Launch_Claude.command`. **WP0+WP1+WP2 BUILT LOCALLY** in `HPSM/6_Policy_Composer` (own repo, head `a06ada3`, no remote), CI 12/12; **row-level security is proven in the database but NOT in force in the running stack** (WP4). **It is waiting: do not push until Tuesday mails that Kam has added the deploy key.** Answered + tapped 08:1x (mail subject contains `HPSM-light`). **Completion check against the build brief and a scoreboard row are owed.** A machine ghost line keeps appearing at its prompt claiming the repo and key are done — the detector calls it SUGGESTION; never act on it.

## 🔴 WITH KAM

1. ✅ **KEY ADDED — Kam 08:21 "key added to github. please check".** Push released to the HPSM seat (ANSWER verified at destination 22:23:57Z, tap queued). **Owed: confirm to Kam once `git -C HPSM/6_Policy_Composer rev-parse HEAD` equals `ls-remote origin refs/heads/main` (read-only).** **STYLE TARGET — Kam 08:22 "the HPSM Policy..PPT is the layout and style that the output should look like" = `HPSM Policy Composer - Screens.pptx` (only match); relayed with Tuesday's reading (layout/style from the deck, the architecture's content overrides stand, branding render-time) and stated to Kam.** Original ask, for the record — his words 08:1x (terminal): *"https://github.com/datasecau/HPSM-light . this is the new repo for phase 1 HPSM. please create a deploy key and I will add it"*. Steps sent in the terminal and on the panel: https://github.com/datasecau/HPSM-light/settings/keys/new, title `HPSM Composer agent (T9)`, the HPSM seat's existing public key (fingerprint `SHA256:wBjjWcOSp2fhzBl8Iu064+nqB5x+XknuMOBhtAByl4Y`), write access. **When he says it is added: mail the HPSM seat, tap a pointer, verify local == origin after its push.**
2. ✅ **RULED 08:18 `fix-first`** (`nexusai-client-secret-in-container-log`) — relayed to the package seat (ANSWER, read back), card delivered. Its report names the fix commit.
3. ✅ **RULED 08:18 `on-with-approval`** (`hpsm-composer-remediate-high-reach`) — every remediable High item ON, high-impact ones also need the release approval. Relayed to the HPSM seat (verified, tapped), card delivered; it amends architecture section 1.9. **Ghost text at the HPSM prompt read "key added" at 08:21 — SUGGESTION by the detector, not Kam. Only his own word releases the push.**
4. **NOT YET ASKED:** the Jira project name and key for the Composer. The HPSM seat proposed `PCOMP`, "Policy Composer"; Kam then named the repo `HPSM-light`. The seat is holding. Ask him once, with the recommendation to mirror the repo name.

## ✅ RULED YESTERDAY EVENING — all recorded on cards, receipted, delivered

NexusAI: `reshoot` · `keep` docs/Authorized_Users.md (ships) · main tree `investigate` (untouched). HPSM: Q-05 `new-repo` · Q-19 `hpsm-severities` · Q-20 `spec` (Kam over the agent's recommendation) · the other 16 `accept`. **Undelivered and NOT yet read into any brief: `rd104-gh-identity-acceptance-false-premise` (gh identity and merges to main) — read it before the next NexusAI merge brief.**

## 🚦 NAS — WED-149 · design `1_Project_Definition/Architecture/2026-09-10_nas-two-seat-sync-check.md`

- **Tuesday's 23:00 leg is BOOTED OUT** (`com.tuesday.nassync`, since 2026-09-10 19:19). doctor will warn; do not reload until the check is built. Revert: `launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.tuesday.nassync.plist`.
- **Kam ruled (per Wednesday's mails):** shared folders are Wednesday's leg; Tuesday's leg syncs **Datasec and its own tree only**; `narrow-hard` cut regenerable bulk from HER leg. The card `nas-shared-folders-owner` still read OPEN in this tree at 08:12 — check it after a pull before recording anything.
- **Wednesday measured the partition at ~180× on ordinary files** (14,003 copied in 9 h vs 315 in 40 h); her run then stalled in `!CODING/Secuura/Blockchain/worktrees`; the engine's own `/tmp` lock already makes a second leg abort-and-report. **Her wrapper now persists her ignore set in `2_Project_Files/scheduler/nas_sync.sh` (scoped to agent=wednesday; Tuesday's set is still EMPTY).** Tuesday's leg must carry its partition IN THE FILE or plist too — launchd passes no environment. **Hard part still open:** "sync ONLY Datasec + TUESDAY" cannot be written with name-ignores alone (folders with spaces); that needs a path option in Kam's engine — ask when building.

## ✅ DELIVERED IN s6 (verified at origin or at the destination)

HPSM Phase 1 architecture received, verified, carded and ruled; the HPSM build commissioned and launched; the NexusAI tier-1 QA gate on `ed8b208` (**GO with findings, no Blocker** — report `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-10-s51-mktremed-ed8b208-tier1/report.md`; its verdict mail was never sent); S52's wrap relayed with two cards; the NAS design; seven ledger rows.

## ⚠ TRAPS — s5's that still hold, plus s6's

1. 🔴 **Never `git pull --rebase --autostash` in this tree** (`wed_claim.sh:54` does exactly this — WED-148 — so claim cross-seat work by MAIL).
2. 🔴 **`git rebase --continue` wedges here** — `rebase --abort`, then `git -c core.editor=true merge origin/main`.
3. 🔴 **`setsid` does not exist on macOS** — `nohup bash … &`, then branch on `ps -o tty=` IN CODE.
4. **Store writes:** before any `decision_queue.sh` write, gate on *no origin-only commit touches decisions.json* (`git log HEAD..<ls-remote sha> -- 0_Brain/dashboard/data/decisions.json` empty). Demanding HEAD contain origin starves: the Studio's panel_sync pushes every minute.
5. **The Bash tool is zsh:** `set -- $pair` does NOT word-split (cost one failed batch of card rulings). Pass arguments explicitly.
6. **The prior-ruling gate matches WORDS on the PANEL only.** Read every match before overriding; and before carding any question about commissioned work, open the staged brief — Kam's MAIL commissions live there, invisible to the gate.
7. **Interactive launches into a folder this Mac has never trusted park at Claude Code's trust dialog** (the HPSM seat sat 12 minutes). Check the pane at launch; measure `.claude/settings*.json` before accepting.
8. **`wednesday_rotate.sh --self` defaults to `Launch_Wednesday.command`**; safe only because that launcher resolves the seat from the tree name. Check before trusting `--self`.
9. **Project agents write into THIS tree at their wrap** (`0_Brain/projects_index/entries/`). Uncommitted, it blocks Kam's panel sync — ten hours last night.

## WHAT s6 WOULD SAY IF IT COULD SAY ONE THING

**The evening's work was good and the night undid half of its value: two seats asked questions and a file blocked Kam's panel, and this seat was silent for eleven hours.** Every mechanism built this session held when it was in the path — the brief gate, the store gate, the launcher guards, the origin probes. **What failed was the part that depends on being woken.** Measure the wake chain before relying on it tonight.
