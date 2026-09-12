---
date: 2026-09-12
type: pickup
scope: DATASEC ONLY — Tuesday, on Kamils-Mac-mini. Secuura and general are Wednesday's, on the Studio.
source: written WHOLESALE by Tuesday s10 at ctx 63%, 2026-09-12 ~13:05 AEST. s10 booted 11:56.
status: live
supersede: replace WHOLESALE at the next pickup; never append.
---

# NEXT PICKUP — Tuesday s11. LIVE: RD-150 tier-1 gate `%18` · NexusAI S58 `%17` (merging RD-342 then RD-382). STAGED: RD-327 tier-1 gate, launch when `%18` closes. Kam holds one question: which registry (B2) — and RD-391 now bears on it.

**On EVERY wake:** `2_Project_Files/tools/kam_rulings_today.sh` (never `kam_msgs.sh` unfiltered — it prints Wednesday's Secuura messages) AND `[Kam -> Tuesday]` mails; list `tuesday-agent@` UNFILTERED and route on SUBJECT; `git status --porcelain | grep -v 0_Brain/dashboard/data/`. Rotation band 80–90. **Verify panel messages AT ORIGIN** (`git ls-remote`, `git fetch --no-write-fetch-head origin main`, `git show <sha>:0_Brain/dashboard/data/chat_tuesday.json`). **Do NOT read `0_Brain/daily/`.**

## 🔴 LIVE — with the next action for each
1. **RD-150 TIER-1 GATE — pane `%18` `QA/NexusAI-RD150`, claude pid 81861, launched 12:58, verified at rung 5** ("I'll start by reading the brief in full"). Brief `2_Project_Files/fleet/qa-agent/briefs/2026-09-12_nexusai-rd150-bec76f6-tier1.md`, launcher `…/launchers/launch_qa_nexusai_rd150_bec76f6.sh` (`--check` passed; head guard red-proofed rc 6). Verdict subject `[QA/Datasec-NexusAI -> Tuesday] GATE VERDICT — RD-150 @ bec76f6 (tier 1)`; report `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-12-rd150-bec76f6-tier1/report.md`. **Key asks:** the 94 `getSetting` call sites classified (NEWLY WRONG = Major), `''` handling, `aiEnabled` through the real route, the deploy behaviour-change list, and a merge prediction onto the `main` it reads at start. **NEXT at the verdict:** read the report's findings + claims ledger, completion check, score (gate + S55's RD-150 round), rule; `pane_close.sh %18`; **then launch the RD-327 gate** (item 3).
2. **NexusAI S58 — pane `%17` `Datasec/NexusAI`, claude pid 17879.** **RD-327 READY FOR QA** at `rd-327-build-digest-s58` @ `67c2992b6202588212c68164661ca6393653e24e` (02:56:15Z; ls-remote verified), suite 2348/120, ⚑4 skipped as ruled. **It was told (ANSWER 02:55:26Z, verified delivered; pointer tap 12:58 verified with `--mail`) to MERGE RD-342 then RD-382 into `main`,** with three pre-merge readings (heads; `deploy-demo.yml` guards; both reports' GO lines), counts regenerated with `--update-counts` (expect ~2324/120 then ~2331/121, measured), push `main` with an explicit refspec, then **RD-342 and RD-382 → Release Ready with BLUF comments** (RD-382's must say `JIRA.md`'s recipes normalise only from `2_Project_Files`) **and THREE tickets:** (1) RD-342 F-1+F-2 local-scan coverage limits (merge history; `rebase --continue` runs no hook); (2) RD-342 F-3 launcher line 238 silences a broken preflight script; (3) RD-382 F-1..F-4 Jira normaliser. **NEXT on its MERGED mail:** verify `ls-remote` main == the merge SHA with `c43214e` and `d4d3bfb` both ancestors; read the three ticket keys on Jira; tell Kam on the panel (short); score S58 AFTER the RD-327 gate. **Its ctx read 34% at 12:52.**
3. **RD-327 TIER-1 GATE — STAGED, NOT LAUNCHED** (held so two gates do not boot servers on this machine at once). Brief `…/briefs/2026-09-12_nexusai-rd327-67c2992-tier1.md`, launcher `…/launchers/launch_qa_nexusai_rd327_67c2992.sh` (`--check` passed 13:0x; red-proof rc 6). **Re-run `--check` before launching** (the report must not exist; the head must still be `67c2992`). Launch: `cockpit.sh add 'QA/NexusAI-RD327' "bash '<launcher>'"`, then verify at rung 5 and watch its pid. Key asks: the raw SHA on ANY unauthenticated surface = Blocker; rule on S58's ⚑3 preload question; `github.sha` per workflow trigger; `shasum` on the CI runner for cell R1b.
4. **Kam — registry B2, and RD-391.** He ruled `publish-image` (11:34); Tuesday asked at 11:36 which registry. **Nothing is built or pushed until he names it.** **RD-391 (High, filed by S58):** `.dockerignore`'s `*.pem`/`*.key`/`.env` rules are anchored at the context root, so a gitignored key under `backend/` enters any image built from a tree that holds one — and the long-lived `NexusAI/2_Project_Files` holds `backend/ReportingDashboard_key.pem`. **Whether any past image (including the May `nexusaidevacrfa39.azurecr.io/nexusai:2.0.0` customers get today) was built from that tree is UNMEASURED.** Kam told at ~13:00 (verification at origin was polling at write time — re-check with `git show origin`). **The B2 image brief MUST require:** a fresh checkout (never `2_Project_Files`), RD-391's any-depth rules applied or the built image scanned for `*.pem`, `*.key`, `.env*` before any push, and the same READ-ONLY content check of the May image.
5. **Panel today:** 12:10 note (verified at origin `20ae0e22`); ~13:00 note on the gates + RD-391 (check origin).

## ⚠ CAPACITY
7-day allowance **90% at 13:05** (86% 10:00 → 88% 11:56 → 89% 12:52 → 90%). Two seats live, a third (RD-327 gate) queued. **From 95%: launch nothing new; live seats checkpoint and push.** At ~1%/h the line is ~18:00; with three seats sooner.

## ✅ DONE IN s10 (verified)
- Brain whole (digest 5,389 lines; own ledger 97 rows); boot digests committed (they blocked `panel_sync`).
- **RD-342 + RD-382 tier-2 gate** (one session, two verdicts): RD-342 GO WITH FINDINGS 0/0/3 (02:28:12Z), RD-382 GO WITH FINDINGS 0/0/3/1 with a measured merge prediction 2318/120 (02:51:51Z). Completion checks done; scoreboard: both gates 1.00, S55 RD-382 round 0.90, S57 RD-342 post-gate note 0.95. Pane `%16` closed, listeners 12 → 12.
- **S58 launched on RD-327** (brief refused once for RD-302 provenance, fixed); plan CONFIRMED with six rulings (⚑4 the admin raw SHA DROPPED — `/api/admin/health` is open pre-first-run); RD-327 READY.
- Ledger rows: s10's boot-hour instrument slips; the S58 brief's two defects (HOLD vs the launcher's boot `git fetch`; the admin-auth premise relayed unread).
- WED board 26 active, 0 `lesson`. Kam's 11:58 message was Wednesday's tab (Secuura): not acted on.

## 🔴 WITH KAM (asked; nothing blocks)
1. Registry B2 + RD-391's bearing on it (live item 4). 2. `brew install gitleaks` (RD-342 option E). 3. RD-281: the rebuilt Sustainability tab render. 4. Full Disk Access for `/bin/bash` (ruled `grant`; his hands). 5. HPSM: Jira key (`HPSML`), R4-m2's owner option, the HPSM-40 analysis-repo remote. 6. His vault `Notes (MASTER)` on the T9 (484 behind, 102 uncommitted). 7. RD-367's branching-model half. 8. ATTIO digest still to `wednesday-agent@` (measure `FOLLOWUP_DIGEST_TO` at the next ATTIO session, flag as a production change first). 9. `rd104-gh-identity-acceptance-false-premise` → `youcheck` still undelivered: the `demo` environment reviewer + `CI_DEPLOY_ENABLED` settings pages; it bears on every merge to NexusAI `main`. 10. **Not yet asked:** whether `/api/admin/health` being open before first-run (S58's observation) should be a ticket — Tuesday's call, pending the RD-327 gate's read.

## ⚠ TRAPS
1. 🔴 Never `git pull --rebase --autostash` here. Wedged rebase: `rebase --abort`, then `git -c core.editor=true merge origin/main`.
2. `setsid` does not exist on macOS — `nohup bash … &`.
3. Store writes: gate on `git merge-base --is-ancestor $(git ls-remote origin refs/heads/main | cut -f1) HEAD`.
4. zsh: no `PIPESTATUS`, no word-splitting of `$VAR`; loop in python.
5. `cockpit.sh say` takes the pane NAME; `pane_close.sh` and `wake_ack.sh` take the `%ID`.
6. The frozen-busy leg fires on THIS pane while a background watcher runs: check the watcher output + inbox, then `wake_ack.sh %0`.
7. Exiting watcher: `/private/tmp/claude-501/-Volumes-KK-T9-External-HDD-TUESDAY/98ea263b-c924-4f22-9fe8-945f47f2172f/scratchpad/watch_s10.sh <MARK> <HH:MM> <pid…>`; MARK = one second PAST the last processed mail.
8. Launch outputs under `fleet/briefs_staged/*.out` (gitignored).
9. Write + commit in ONE action outside `dashboard/data`; never two commits in parallel calls.
10. `decision_queue.sh add --json` cannot take `--override-prior-rulings`.
11. `kam_rulings_today.sh`'s FRESHNESS line lags Kam's taps; `[Kam -> Tuesday]` mails do not.
12. `wake_watch` wakes this seat for `view=wednesday` messages — check the view.
13. `cockpit.sh launch` cannot start Datasec projects here; use `cockpit.sh add`.
14. 🔴 Never plain `git fetch` in a verify loop.
15. QA gates and build seats in a tmux PANE, never nohup headless.
16. The card-ID send gate refuses a card id the store cannot show.
17. `send_brief.sh` subjects carry `[Wednesday -> …]` while the sender is `tuesday-agent@` — harmless.
18. `panel_sync` rebases local commits: verify by subject/content, not local SHA.
19. A probe whose found and not-found branches both exit 0 proves nothing by rc.
20. `sleep` as a foreground wait is blocked — background loops.
21. Verify a brief at the destination inbox BEFORE `cockpit.sh add`.
22. Grep the target launcher for EVERY verb and path the HOLDS name — derived from the holds text (the S58 brief's "never write 2_Project_Files" collided with the launcher's boot `git fetch`).
23. `decision_queue.sh` and `reconcile_rulings.py` live in `2_Project_Files/tools/`. Capture a tool's rc on its own line before any `| grep`.
24. AgentMail `GET …/messages/<id>` needs the id URL-encoded.
25. The send gate refuses any ticket id in the QUEUE — even inside a quoted title — without a PROVENANCE state line.
26. **NEW:** two QA gates booting local servers at once can collide on ports — stage the second, or name ports in both briefs.

## NAS — WED-149 (unchanged)
`com.tuesday.nassync` stays BOOTED OUT until the partition is built into the file/plist. Design `1_Project_Definition/Architecture/2026-09-10_nas-two-seat-sync-check.md`.

## OWED, not started
- Amend `Launch_Tuesday.command`: step 5 (no Tuesday daily note — name the pickup, this seat's ledger, `git log`) and its stale first-boot line (`FIRST-BOOT-TUESDAY.md` is in `tasks/_superseded_2026-09-09/`). Red-proof by a boot, never mid-task.
- S53's m2/m3, S54's 8 BACKLOG items and round-3 NEW-3/NEW-4 need ticketing on RD.
- Undelivered ruled HPSM cards: `hpsm-composer-round3-approver-guard`, `hpsm-credential-bearing-prd-outside-every-snapshot`.
- Raise with Wednesday (shared tool): `send_brief.sh --kind brief` could refuse a bare "No az/gh" when the target launcher runs them.
- Carried: 4 Dependabot alerts on NexusAI's default branch (RD-354 owns qs 6.15.2); three need a `gh` identity.
