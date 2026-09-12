---
date: 2026-09-12
type: pickup
scope: DATASEC ONLY — Tuesday, on Kamils-Mac-mini. Secuura and general are Wednesday's, on the Studio.
source: written WHOLESALE by Tuesday s10 at its ctx-50% checkpoint, 2026-09-12 ~12:20 AEST. s10 booted 11:56 after s9 rotated at S57's wrap.
status: live
supersede: replace WHOLESALE at the next pickup; never append.
---

# NEXT PICKUP — Tuesday s11. TWO SEATS LIVE: QA gate `%16` (RD-342 + RD-382, tier 2, two verdicts) and NexusAI S58 `%17` (RD-327, plan confirmation owed). Kam holds one question: which registry (B2).

**On EVERY wake:** `2_Project_Files/tools/kam_rulings_today.sh` (it withholds the other seat's tab — **never `kam_msgs.sh` unfiltered**, it prints Wednesday's Secuura messages) AND `[Kam -> Tuesday] panel message` mails; list `tuesday-agent@` UNFILTERED and route on SUBJECT; `git status --porcelain | grep -v 0_Brain/dashboard/data/`. Rotation band 80–90. **Kam reads the Studio: verify a panel message AT ORIGIN** (`git ls-remote`, then `git fetch --no-write-fetch-head origin main` + `git show <sha>:0_Brain/dashboard/data/chat_tuesday.json`), never with a plain `git fetch`. **Do NOT read `0_Brain/daily/`** (Wednesday's, Secuura).

## 🔴 LIVE — with the next action for each
1. **QA GATE, pane `%16` `QA/NexusAI-RD342-382`, claude pid 13175, launched 12:08, verified at rung 5** (the pane showed its own step "Reading worktree heads and status at gate start"). Brief `2_Project_Files/fleet/qa-agent/briefs/2026-09-12_nexusai-rd342-c43214e-rd382-d4d3bfb-tier2.md`; launcher `2_Project_Files/fleet/qa-agent/launchers/launch_qa_nexusai_rd342_rd382_tier2.sh` (`--check` passed; head guard red-proofed rc 6 for both heads). **Two verdict mails, RD-342's first:** `[QA/Datasec-NexusAI -> Tuesday] GATE VERDICT — RD-342 @ c43214e (tier 2)`, then `… RD-382 @ d4d3bfb (tier 2)`. Reports: `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-12-rd342-c43214e-tier2/report.md` and `…/2026-09-12-rd382-d4d3bfb-tier2/report.md`. **NEXT at each verdict:** read the report whole; completion check against the brief's attack items; score the gate and the builder (RD-342 = S57, RD-382 = S55); rule. GO / GO WITH FINDINGS → the merge is done by a NexusAI seat on Tuesday's GO (S58 at a clean boundary, or a later seat), each merge regenerating counts with `npm run verify -- --update-counts`. NO GO → a round-2 brief (cap: 2). **When both verdicts are in:** `pane_close.sh %16` (it takes the `%ID`; listeners check). **Then the RD-150 tier-1 gate** (`rd-150-falsy-setting-s55` @ `bec76f686de5415090350117437d11d1a49acb82`, cut from `cd2b543`; two kill switches start taking effect, `red_flag_enabled` and `aiEnabled`: record the behaviour change).
   **Merge arithmetic:** `main` `34e7fc4` = 2311/119 · `rd-342-s57` = 2324/120 · RD-382 on top of `34e7fc4` predicts 2318/120 (the gate measures it in its own clone).
2. **NexusAI S58, pane `%17` `Datasec/NexusAI`, launched ~12:15** by `cockpit.sh add` with NexusAI's own `Launch_Claude.command`. Brief `2_Project_Files/fleet/briefs_staged/2026-09-12_nexusai-s58-brief.md`, sent 02:13:31Z **after** one gate refusal was answered (RD-302 provenance), **verified at `datasec-nexusai@` (received, from Tuesday, preview non-null) BEFORE the launch.** Queue: **RD-327 only**, the ⚑5 shape (`build` = first 16 hex of sha256 over the commit SHA; `"unknown"` fallback; never omitted; no raw SHA unauthenticated). **Rung-5 verification was still pending at this checkpoint** (background poll): if not confirmed, capture `%17`; a folder-trust dialog takes "Yes, I trust this folder" (Down, Enter). **NEXT:** its `QUESTION: plan confirmation (S58)` → check its re-derived landing lines and its preflight warnings (expect the RD-342 "not found" WARNING), answer with `send_brief.sh --kind answer` (prefix `WED_AGENT=tuesday`), verify at destination, then tap a pointer with `cockpit.sh say 'Datasec/NexusAI' '<pointer>' --mail '<subject substring>'`. READY → tier-1 gate.
3. **Kam — registry B2.** He ruled `publish-image` at 11:34; Tuesday asked at 11:36 which registry (option 1 the dev ACR `nexusaidevacrfa39`; option 2, recommended, a separate customer-facing registry he names — a new Basic ACR is money class). **Nothing is built or pushed until he names it.** On his answer: brief a NexusAI seat to build from `7aa5aaf`, push ONLY to the named registry, point `createUiDefinition.json:59` and `:71` at it, rebuild the plan zip; then a tier-2 gate on the zip; then Kam uploads. The Marketplace branch is S56's round: a separate worktree, never S58's RD-327 branch.
4. **Panel:** Kam told at 12:10 — RD-372 merged (`34e7fc4`), S57 wrapped, the RD-342 + RD-382 gate started 12:08, the registry still his. **Verified AT ORIGIN (`20ae0e22`).**

## ⚠ CAPACITY
7-day allowance **88% at 12:12** (86% at 10:00, 88% at 11:56 with one seat live; two are live now, so expect faster). Reset ~04:00. Kam's `wed-weekly-quota-97pct` ruling = raise-limit, proceed normally. **From 95%: launch nothing new; live seats checkpoint and push.** The RD-150 gate launches only after `%16` closes and below 95%.

## ✅ DONE IN s10 (verified at source or origin)
- Brain: by-tier digest read whole (5,389 lines, last heading asserted), own ledger whole (97 rows). Statusline `ctx:23%` after the digest, `45%` after the ledger and the gate reads, `50%` at this checkpoint.
- The launcher-regenerated boot digests were committed (they were blocking `panel_sync`).
- The gate above: heads, ranges, files, delete-sets and launcher hashes all read at source; both tickets read on Jira (RD-342 Testing, RD-382 Testing).
- S58 brief sent and delivery verified; S58 launched.
- The 11:58 wake was Kam's message on WEDNESDAY's tab (Secuura) — hers; not acted on, not relayed.
- WED board 26 started + unstarted (`board_count.sh`), 0 open `lesson` issues.
- Ledger row: s10's boot-hour instrument slips (four, all caught).

## 🔴 WITH KAM (asked; nothing blocks)
1. `brew install gitleaks` on the Mac mini (optional; RD-342 option E).
2. **RD-281:** did he accept the rebuilt Sustainability tab render?
3. Full Disk Access for `/bin/bash` (ruled `grant` 2026-09-11; the toggle is his hands; last probe exit 126).
4. NexusAI registry (B2) — live item 3. 5. Jira key for the HPSM Composer (rec `HPSML`); R4-m2's owner option; the HPSM-40 analysis-repo remote.
6. His vault `Notes (MASTER)` on the T9: 484 behind, 102 uncommitted paths from other sessions.
7. RD-367's premise is dead (told); the branching-model half is his.
8. **ATTIO follow-up digest still goes to `wednesday-agent@`** (his 09-10 `amend` ruling). Recipient = env `FOLLOWUP_DIGEST_TO` (`ATTIO/2_Project_Files/src/config.js:94`) in the deployed job; app UNMEASURED. At the next ATTIO/Vision session: measure it, flag to Kam as a production change BEFORE changing, and fix `Vision_Sales_Portal/Launch_Claude.command:263`'s wrap address too.
9. **`rd104-gh-identity-acceptance-false-premise` → `youcheck` (2026-09-07), still undelivered:** Kam checks two GitHub pages — the `demo` environment's required reviewer and the `CI_DEPLOY_ENABLED` variable. It bears on every merge to NexusAI `main`, because `deploy-demo.yml` is the workflow they gate. Read the card before the next NexusAI MERGE instruction.

## ⚠ TRAPS
1. 🔴 **Never `git pull --rebase --autostash` in this tree.** Wedged rebase: `rebase --abort`, then `git -c core.editor=true merge origin/main`.
2. `setsid` does not exist on macOS — `nohup bash … &`.
3. **Store writes:** gate on `git merge-base --is-ancestor $(git ls-remote origin refs/heads/main | cut -f1) HEAD` first.
4. **zsh:** no `PIPESTATUS`; no word-splitting of `$VAR`; loop in python.
5. `cockpit.sh say` takes the pane NAME; `pane_close.sh` and `wake_ack.sh` take the `%ID`.
6. `wake_watch`'s frozen-busy leg fires every ~8 min while a background watcher runs — check the watcher output and the inbox, nothing more.
7. **Run your own exiting watcher while anything is live:** `watch_s10.sh <MARK> <HH:MM> <pid…>` (copy it from `/private/tmp/claude-501/-Volumes-KK-T9-External-HDD-TUESDAY/98ea263b-c924-4f22-9fe8-945f47f2172f/scratchpad/watch_s10.sh`). **MARK = one second PAST the last processed mail's timestamp** — the compare is a string, and the API's fractional seconds sort after a bare second.
8. Launch outputs go under `fleet/briefs_staged/*.out` (gitignored).
9. **Write + commit in ONE action** outside `dashboard/data`; never two commits in parallel tool calls.
10. `decision_queue.sh add --json` cannot take `--override-prior-rulings`; use the flag form.
11. `kam_rulings_today.sh`'s FRESHNESS line lags Kam's taps; the `[Kam -> Tuesday]` mails do not.
12. `wake_watch` wakes this seat for Kam's `view=wednesday` messages — check the view, and use `kam_rulings_today.sh`, which withholds them.
13. `cockpit.sh launch` cannot start Datasec projects here (`launchers.conf` pins DevMASTER); use `cockpit.sh add`.
14. 🔴 **Never plain `git fetch` in a verify loop** — it races `panel_sync`.
15. **Launch QA gates and build seats in a tmux PANE, never nohup headless.**
16. The card-ID send gate refuses a card id the store cannot show — copy ids from `decision_queue.sh list`.
17. `send_brief.sh` subjects carry the hard-coded `[Wednesday -> …]` prefix while the sender is correctly `tuesday-agent@` — harmless.
18. `panel_sync` REBASES local commits, so a local SHA is not the SHA at origin; verify by subject or content.
19. A probe whose found and not-found branches both exit 0 proves nothing by rc — read its output (s10 wrote one again).
20. `sleep N` as a foreground wait is blocked — poll in a background loop.
21. Verify a brief at the destination inbox (subject + non-null preview) BEFORE `cockpit.sh add`.
22. Before a builder brief leaves, grep the target launcher's FIRST ACTIONS for every verb a HOLD prohibits.
23. **NEW s10:** `decision_queue.sh` and `reconcile_rulings.py` live in `2_Project_Files/tools/`, not `fleet/`. **Capture a tool's rc on its own line before any `| grep`** — a 127 piped through grep is an empty result.
24. **NEW s10:** AgentMail `GET …/messages/<id>` needs the id URL-encoded (`urllib.parse.quote(id, safe='')`), else HTTP 400.
25. **NEW s10:** the send gate refuses any ticket id named in the QUEUE — even inside a quoted title — without its own PROVENANCE state line.

## NAS — WED-149 (unchanged)
Tuesday's 23:00 leg `com.tuesday.nassync` stays BOOTED OUT until the partition is built INTO the file/plist. Design `1_Project_Definition/Architecture/2026-09-10_nas-two-seat-sync-check.md`.

## OWED, not started
- **Amend `Launch_Tuesday.command`**: step 5 (Tuesday has no daily note — name the pickup, this seat's ledger and `git log`), and its stale first-boot line (it still tells every boot to read `FIRST-BOOT-TUESDAY.md`, which sits in `tasks/_superseded_2026-09-09/`). Red-proof by a boot, never while a seat's respawn depends on it mid-task.
- S53's m2/m3, S54's 8 BACKLOG items and round-3 NEW-3/NEW-4 need ticketing on RD.
- Undelivered ruled HPSM cards: `hpsm-composer-round3-approver-guard` (mark with its artefact) and `hpsm-credential-bearing-prd-outside-every-snapshot` (BACKLOG since s34).
- Raise with Wednesday (shared tool): `send_brief.sh --kind brief` could refuse a bare "No az/gh" when the target launcher runs them.
- Carried by Tuesday: 4 Dependabot alerts on NexusAI's default branch (RD-354 owns qs 6.15.2); three unread, need a `gh` identity.
