---
date: 2026-09-12
type: pickup
scope: DATASEC ONLY — Tuesday, on Kamils-Mac-mini. Secuura and general are Wednesday's, on the Studio.
source: written WHOLESALE by Tuesday s9 at its ctx-60% checkpoint, 2026-09-12 ~10:00 AEST. s9 booted 09:1x on s8's rotation.
status: live
supersede: replace WHOLESALE at the next pickup; never append.
---

# NEXT PICKUP — Tuesday s10. LIVE: NexusAI S57 on RD-342 (%13) · RD-372 round-2 GATE (%15). HPSM round 4 DONE and pushed. Marketplace round 4 GATE-CLEAN; one card with Kam: B2, the registry.

**On EVERY wake:** `2_Project_Files/tools/kam_rulings_today.sh` AND `[Kam -> Tuesday] panel message` mails (fresher than the local store); list `tuesday-agent@` UNFILTERED and route on SUBJECT; `git status --porcelain | grep -v 0_Brain/dashboard/data/`. Rotation band 80–90. **Kam reads the Studio: verify a panel message AT ORIGIN** (`git ls-remote` == `git rev-parse HEAD`, then `git show HEAD:0_Brain/dashboard/data/chat_tuesday.json`), never with a plain `git fetch` (trap 14). **Do NOT read `0_Brain/daily/`** (Wednesday's, Secuura).

## 🔴 LIVE — with the next action for each
1. **HPSM ROUND 4 — GATE DONE: GO WITH FINDINGS 0/0/2/2** (verdict mail 00:35:05Z; report `!CODING/Testing Agent MAIN/projects/hpsm/reports/2026-09-12-composer-afc10e9-tier1r4/report.md`). R3-M1 and S3-F4b (incl. superseded) CLOSED by its measurement. Completion check done, scored 1.00, pane `%12` closed (listeners 12 → 12).
2. **HPSM session 38 — WRAPPED 10:41, scored 1.00, pane `%10` closed (listeners 14 → 14).** Pushed `afc10e9` to HPSM-light `main` at 00:37:26Z (Tuesday verified by `ls-remote`); BACKLOG verified at source (R3-M1 + S3-F4b closed; R4-m1, R4-m2 with both options unchosen, R4-p1, R4-p2, R4-f1). Kam told on the panel at 10:39 (verified at origin `ac863262`). **No HPSM seat is live.** Next HPSM work waits on Kam: Jira key (HPSML), R4-m2's owner option, HPSM-40 analysis-repo remote.
3. **NexusAI S57 — pane `%13` (`Datasec/NexusAI`), pid 59800, launched 09:45** by `cockpit.sh add` with NexusAI's own `Launch_Claude.command`. Brief `2_Project_Files/fleet/briefs_staged/2026-09-12_nexusai-s57-brief.md`. **Plan CONFIRMED 23:58:10Z** (`…/2026-09-12_nexusai-s57-answer-plan.md`) with six rulings: ⚑1 F-5's comment on **RD-371** (not RD-148) · ⚑2 **TWO tickets** (item-5 server side; the 27-site census) — SUPERSEDES the brief · ⚑3 the untracked launcher gets ONE guarded call line (quarantine copy, prove `INITIAL_PROMPT` intact, diff in READY) · ⚑4 stub `gitleaks` for RED; rule coverage NOT tested · ⚑5 **RD-327 `build` = first 16 hex of sha256(commit SHA), NOT the raw SHA** (RD-329: an unauthenticated endpoint carries counts, never identifiers); the Marketplace path never passes the arg · ⚑6 the launcher-mandated read-only `az` feedback sweep is exempt — SUPERSEDES "No az". **Queue:** RD-372 round 2 of 2 (branch `rd-372-r2-s57` from `ae2588b`, expects 2289/119, tier 1) → RD-342 (tier 2) → RD-327 (tier 1). **NEXT at each READY:** read S57's statusline, verify at source, commission the gate. **It shares `datasec-nexusai@` with S56.** **UPDATE 10:3x:** RD-372 round 2 READY 00:29:10Z @ `a3d15b88f08fde634ccac132677152c8521ecf97` (2 commits on `ae2588b`, verified `ls-remote`; suite 2311/119; RD-388 + RD-389 filed and read by Tuesday; RD-371 comment). Tuesday answered 00:30:18Z: CONTINUE to RD-342 (S57 ctx 37%); do not push `rd-372-r2-s57` while gated. **🔴 ITS TIER-1 ROUND-2 GATE IS LIVE — pane `%15` (`QA/NexusAI-RD372-R2`), launched 10:36** from `2_Project_Files/fleet/qa-agent/launchers/launch_qa_nexusai_rd372_a3d15b8.sh` (`--check` rc 0). Verdict subject `[QA/Datasec-NexusAI -> Tuesday] GATE VERDICT — RD-372 @ a3d15b8 (tier 1, round 2)`; report `!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-12-rd372-a3d15b8-tier1r2/report.md`. **On GO:** a NexusAI seat merges `rd-372-r2-s57` to `main` with counts regenerated. **On NO GO:** round 2 of 2 — ship what is closed, ticket the rest, no round 3 without Kam.
4. **NexusAI Marketplace ROUND 4 — GATE DONE: GO WITH FINDINGS** (verdict mail 00:47:33Z; report `!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-12-mktpkg-7aa5aaf-tier1r4/report.md`). No new Blocker or Major; the package is upload-clean (GPT-only real, setup save survives restart, tenant IDs masked, zips byte-equal to git, gitleaks clean). Completion check done; the gate AND S56 scored 1.00; pane `%14` closed (listeners 15 → 15). **What still stops a WORKING deployment is B2:** `createUiDefinition.json:59` at `7aa5aaf` defaults customers to `nexusaidevacrfa39.azurecr.io/nexusai:2.0.0`, a May image with none of rounds 2–4 (Tuesday read it with `git show`). **🔴 WITH KAM: card `nexusai-marketplace-b2-registry-after-round4`** (added 10:5x with `--override-prior-rulings`, reason measured in its BLUF; rec `publish-image`; default HOLD: nothing uploaded, built or pushed). Panel message sent 10:5x. **On his ruling:** `publish-image` → he names the registry and authorises the push (his signature class), then brief a NexusAI seat to point the wizard default at it and rebuild the plan zip, then a tier-2 gate on the zip; `upload-now` → nothing for a seat, he uploads; `hold` → nothing moves. Zips: `NexusAI/evidence-s56-marketplace-package/DRAFT-submission-package-7aa5aaf/`. Still his too: MIN-4, `rd15-03`.

## 🟡 OWED GATES — HELD for capacity (Tuesday s9: Kam's round-4 re-checks take the QA slot first)
- **RD-150 @ `bec76f686de5415090350117437d11d1a49acb82`** — tier 1; two kill switches start taking effect (`red_flag_enabled`, `aiEnabled`): record the behaviour change for any deploy decision.
- **RD-382 @ `d4d3bfbf46211d93159a13d5b2e8510f11e6c425`** — tier 2.
- **Merge arithmetic:** `main` `ae2588b` = 2283/118; every merge regenerates with `npm run verify -- --update-counts`, never copied.

## ⚠ CAPACITY — the clock worth watching
7-day allowance **86% at 10:00** (81% at 07:08 → 84% at 09:11, ~1.5%/h; both seats read the same figure). Projected empty ~19:00–20:00 AEST, reset ~04:00. Kam's `wed-weekly-quota-97pct` ruling = **raise-limit, proceed normally**. Tuesday posted the projection to his panel 09:29 (verified at origin `e68d4373`) with the default: **from 95%, launch nothing new; live seats checkpoint and push.** Wednesday holds the same line (her 23:33:22Z mail).

## ✅ DONE IN s9 (verified at source or origin)
- RD-372 tier-1 gate @ `abdb136`: **NO GO 1/1/3/2** (F-1 Blocker: a 200 with non-config JSON lets one Save switch SCIM provisioning off). Completion check against the brief's 7 items; scored 1.00; pane `%9` closed (listeners 12 → 12, ports 3371/3372 dead).
- HPSM round-4 gate commissioned, guarded (`--check`), committed `550fa263`, launched, verified at rung 5.
- Delivered marks: `nexusai-marketplace-round4-gpt-only-product`, `hpsm-composer-round4-commit-guard-and-forged-release`.
- Panel: 09:29 rotation note + usage projection; 09:48 Datasec update (`0162be8e`). Both verified at origin.
- Ledger row (w=4): four defects in the S57 brief, all caught by S57 at plan confirmation.

## 🔴 WITH KAM (asked; nothing blocks)
1. `brew install gitleaks` on the Mac mini (optional; RD-342 option E).
2. **RD-281:** did he accept the rebuilt Sustainability tab render?
3. Full Disk Access for `/bin/bash` (ruled `grant` 2026-09-11; the toggle is his hands; last probe exit 126).
4. NexusAI registry (B2). 5. Jira key for the HPSM Composer (rec `HPSML`).
6. His vault `Notes (MASTER)` on the T9: 484 behind, 102 uncommitted paths from other sessions.
7. RD-367's premise is dead (told); the branching-model half is his.
8. **ATTIO follow-up digest still goes to `wednesday-agent@`** (his 09-10 `amend` ruling, card `fleet-comms-names-one-coordinator`). Recipient = env `FOLLOWUP_DIGEST_TO` (`ATTIO/2_Project_Files/src/config.js:94`) in the deployed job; app UNMEASURED. **At the next ATTIO/Vision session:** measure where it lives, flag to Kam as a production change BEFORE changing, and fix `Vision_Sales_Portal/Launch_Claude.command:263`'s wrap address too.

## ⚠ TRAPS
1. 🔴 **Never `git pull --rebase --autostash` in this tree.** Wedged rebase: `rebase --abort`, then `git -c core.editor=true merge origin/main`.
2. `setsid` does not exist on macOS — `nohup bash … &`.
3. **Store writes:** gate on `git merge-base --is-ancestor $(git ls-remote origin refs/heads/main | cut -f1) HEAD` first; a stale store refuses — wait one panel_sync cycle and retry.
4. **zsh:** no `PIPESTATUS`; no word-splitting of `$VAR` in `for f in $VAR` — loop in python; `echo =====` errors.
5. `cockpit.sh say` takes the pane NAME; `pane_close.sh` and **`wake_ack.sh` take the `%ID`** (`wake_ack.sh` refuses a name with rc 3).
6. `wake_watch` frozen-busy leg fires every ~8 min while a background watcher runs — check the watcher output + inbox, nothing more.
7. Run your own exiting watcher while anything is live: copy `scratchpad/watch_s9.sh <MARK> <deadline> <pid…>` (exits on newer inbound mail, any pid death, or deadline). MARK = last PROCESSED mail's timestamp.
8. Launch outputs go under `fleet/briefs_staged/*.out` (gitignored).
9. **Write + commit in ONE action** outside `dashboard/data`; two commits in parallel tool calls collide on `index.lock` — put them in one command.
10. `decision_queue.sh add --json` cannot take `--override-prior-rulings`; use the flag form.
11. `kam_rulings_today.sh`'s FRESHNESS line lags Kam's taps; the `[Kam -> Tuesday]` mails do not.
12. `wake_watch` wakes this seat for Kam's `view=wednesday` messages — check the view.
13. `cockpit.sh launch` cannot start Datasec projects here (`launchers.conf` pins DevMASTER); use `cockpit.sh add`.
14. 🔴 **Never plain `git fetch` in a verify loop** — it races panel_sync. Use `ls-remote` + HEAD, or `git fetch --no-write-fetch-head origin main` + `git show <sha>:<path>`, polling ≥60 s.
15. **Launch QA gates and build seats in a tmux PANE, never nohup headless.** The folder-trust dialog may appear on pane launches: "Yes, I trust this folder" (Down, Enter).
16. The card-ID send gate refuses a card id the store cannot show — copy ids from `decision_queue.sh list`.
17. `send_brief.sh` subjects carry the hard-coded `[Wednesday -> …]` prefix while the sender is correctly `tuesday-agent@` — harmless.
18. **NEW s9: `panel_sync` REBASES local commits, so the SHA you committed is not the SHA at origin.** Verify a commit reached origin by SUBJECT or content, never `merge-base --is-ancestor <local sha>` (it read a false "NOT at origin").
19. **NEW s9:** a probe whose found and not-found branches both exit 0 proves nothing by rc — read its output.
20. **NEW s9:** `sleep N` as a wait is blocked by the harness — poll in a background until-loop.
21. **NEW s9:** a launch waits for its brief — verify the brief at the destination inbox (subject + non-null preview) BEFORE `cockpit.sh add`.
22. **NEW s9:** before a builder brief leaves, grep the target launcher's FIRST ACTIONS for every verb a HOLD prohibits (the S57 "No az" collision).

## NAS — WED-149 (unchanged)
Tuesday's 23:00 leg `com.tuesday.nassync` stays BOOTED OUT until the partition is built INTO the file/plist. Design `1_Project_Definition/Architecture/2026-09-10_nas-two-seat-sync-check.md`.

## OWED, not started
- **Amend step 5 of `Launch_Tuesday.command`** (Tuesday has no daily note; name the pickup, ledger and `git log`), red-proofed by a boot — not while a seat's respawn depends on it mid-task.
- `rd104-gh-identity-acceptance-false-premise` — read before the next NexusAI MERGE brief.
- S53's m2/m3, S54's 8 BACKLOG items and round-3 NEW-3/NEW-4 need ticketing on RD.
- Undelivered ruled cards: `hpsm-composer-round3-approver-guard` (round 3 ran; mark with its artefact) and `hpsm-credential-bearing-prd-outside-every-snapshot` (structural-look; BACKLOG since s34) — mark or carry into the next HPSM brief.
- Raise with Wednesday (shared tool): `send_brief.sh --kind brief` could refuse a bare "No az/gh" when the target launcher runs them.
