---
date: 2026-09-12
type: pickup
scope: DATASEC ONLY — Tuesday, on Kamils-Mac-mini. Secuura and general are Wednesday's, on the Studio.
source: written WHOLESALE by Tuesday s11 at ctx ~42%, 2026-09-12 ~14:45 AEST (s11 booted 14:24 on s10's rotation); HPSM + capacity sections refreshed 15:3x at the 50% checkpoint (ctx 53%).
status: live
supersede: replace WHOLESALE at the next pickup; never append.
---

# NEXT PICKUP — Tuesday s12. LIVE: HPSM S39 `%20` building MVP A on Kam's 15:24 ruling + his terminal 'start the build' — answer its PLAN CONFIRMATION, gate each WP. Kam still holds the registry name (B2). Allowance 94%; running out ACCEPTED by Kam.

**On EVERY wake:** `2_Project_Files/tools/kam_rulings_today.sh` (never `kam_msgs.sh` unfiltered) AND `[Kam -> Tuesday]` mails; list `tuesday-agent@` UNFILTERED and route on SUBJECT; `git status --porcelain | grep -v 0_Brain/dashboard/data/`. Rotation band 80–90. **Verify panel messages AT ORIGIN** (`git show origin/main:0_Brain/dashboard/data/chat_tuesday.json` on the ref `panel_sync` fetches; `git ls-remote` HUNG 9 min in this tree at 14:28 — bound any network read with a timeout). **Do NOT read `0_Brain/daily/`** (Wednesday's).

## 🔴 LIVE — with the next action for each
1. **HPSM S39 — pane `%20`, launched 15:31:34 on Kam's word, BUILDING MVP A: WP3 engine → WP4 API (RLS in force in the running stack) → WP5 website (Screens 1–10, deck style A-54) → WP6 renderers.** Kam's note on card `hpsm-composer-monday-review-scope` at 15:24:26 (panel, `view=tuesday`), verbatim: *"build the full website and fully functioning engine"*; then typed into Tuesday's terminal ~15:30: *"start the buld.  Claude credits resume in 12 hours so even if we run out it will be temporary"*. **The card is AMENDED, not ruled** (his note names no option key): his words in the amendment reason, default replaced with `SUPERSEDED BY KAM'S 15:24:26 NOTE…` — it stays `open` in the store by design; **never fire a default on it.** `hpsm-composer-round3-approver-guard` marked delivered (history s36/s37). Brief `2_Project_Files/fleet/briefs_staged/2026-09-12_hpsm-s39-mvpa.md` sent 05:31:07Z, verified at `datasec-hpsm@` (from tuesday-agent@, preview non-null); launch verified at rung 5 (pane named S39 and was reading BACKLOG WP3–6; ctx 8%; preflight clean). HPSM-light `main` = `afc10e98c51505be1f1943335370cf2de3b47d44` (Tuesday `ls-remote` 15:2x). Panel: receipt 15:25 verified at origin `a6c2434b`; launch note ~15:34 — its origin check was still running at write time: `git show origin/main:0_Brain/dashboard/data/chat_tuesday.json | grep 'running as session 39'`. Coordination mail to Wednesday 05:31:44Z (sent copy verified). **4am cron `d54df852` CANCELLED** after the launch verified (it would have re-fired on the card). **NEXT, on its plan-confirmation mail:** check it against the brief — its reading of Kam's words, the WP order, the vault hold superseding launcher step 4, where R4-f1 lands, whether R4-m1/R4-p1 enter WP4's definition of done, and the preflight lines — then CONFIRMED + rulings via `send_brief.sh --kind answer`, verify at `datasec-hpsm@`, tap a pointer. **At each READY FOR QA:** tier-1 gate in a tmux PANE (the s38 round-4 gate's launcher pattern in `Testing Agent MAIN`), completion check, score, push only on GO + Tuesday's word. Watcher: `2_Project_Files/fleet/cockpit/watch_tuesday_exiting.sh 2026-09-12T05:31:45 23:00 5200` (5200 = `%20`'s pane pid). Still Kam's for HPSM: Jira key (`HPSML`), R4-m2's owner option, the HPSM-40 analysis-repo remote.
2. **Kam — registry B2, and RD-391.** He ruled `publish-image` (11:34); Tuesday asked 11:36 which registry. **Nothing is built or pushed until he names it.** **RD-391 (High):** `.dockerignore`'s `*.pem`/`*.key`/`.env` rules are anchored at the context root; the long-lived `NexusAI/2_Project_Files` holds `backend/ReportingDashboard_key.pem`. **Whether any past image (incl. the May `nexusaidevacrfa39.azurecr.io/nexusai:2.0.0`) was built from that tree is UNMEASURED.** **The B2 image brief MUST require:** a fresh checkout (never `2_Project_Files`), RD-391's any-depth rules applied or the built image scanned for `*.pem`, `*.key`, `.env*` before any push, and the same READ-ONLY content check of the May image.
3. **NexusAI — no seat; today's commissioned RD queue is DONE.** `main` = `c469ae9b62810086627545a75b73d53d72974809` (RD-327 merge; verified at source by s11 with read verbs: parents `2279eeb` + `67c2992`, counts 2338/122 → 2375/123, `deploy-demo.yml` +1 build-arg line, both `CI_DEPLOY_ENABLED` conditions + `environment: demo` intact). Jira read by s11: RD-327 Release Ready (comment 37352, O-2 note) · RD-302 comment 37353 (O-3) · RD-397 + RD-398 filed, Medium, linked. S58 wrap 04:37:28Z (DKIM/DMARC pass); pane `%17` closed, listeners 12 → 12. Kam told on the panel ~14:40 (**verified at origin `6a946bde`**). Entry card `projects_index/entries/Datasec__NexusAI.md` updated from S58's index card. **🔴 Before ANY demo deploy of `main`:** read `red_flag_enabled` on the live demo AND dev stores (RD-150); Kam's check of the demo environment reviewer + `CI_DEPLOY_ENABLED` settings pages (card `rd104-gh-identity-acceptance-false-premise` → `youcheck`, undelivered). Residue for a future seat: RD-391 (High), RD-395 product call, RD-392/393/394/396/397/398, unmerged `s55-/s57-/s58-history-docs` (merge not authorised), 7 worktrees left (`rd-327-s58` holds node_modules — remove last).

## ⚠ CAPACITY
7-day allowance **94% at 15:31** (renews ~04:00 Sun). **Kam, in Tuesday's terminal ~15:30: running out is acceptable — *"even if we run out it will be temporary"*.** If it reaches 100%, every live seat on both machines stops mid-turn. **Recovery at the first boot after the reset:** read `%20`'s last output and `HPSM/5_Project_History/HANDOVER-S39.md` (the brief requires it at every WP boundary and at its 50% checkpoint); `ls-remote` HPSM-light `main`; relaunch S40 from the handover carrying the S39 brief's RULED sections; a cut gate re-runs under a NEW report path, never over a partial one.

## ✅ DONE IN s11 (verified)
- Brain whole: by-tier digest 5,389 lines (last line asserted) + own ledger 99 rows → `ctx:11% → 39%`. Boot digests committed (`de1dd220`, at origin) — they were holding `panel_sync` in SKIP from 14:26.
- WED board 26 active (board_count.sh), 0 `lesson`. `reconcile_rulings.py`: 53 taps, 0 to rule.
- RD-327 merge + S58 wrap verified and closed out (live item 3). Ledger row: the watcher's parse-error false wake + the hung `ls-remote` verifier.
- **Kam's HPSM ruling (15:24) received, receipt at origin; card amended; S39 briefed, launched and rung-5 verified (live item 1).**
- **Watcher now TRACKED:** `2_Project_Files/fleet/cockpit/watch_tuesday_exiting.sh <MARK> <HH:MM> <pid…>` — retries a non-JSON listing, wakes on 3 in a row as `WAKE listing-broken`. MARK = one second past the last processed mail (last processed: `2026-09-12T04:37:28`).

## 🔴 WITH KAM (asked; nothing blocks)
1. Registry B2 + RD-391's bearing on it. 2. `brew install gitleaks` (RD-342 option E; every local NexusAI commit today skipped the scan). 3. RD-281: the rebuilt Sustainability tab render. 4. Full Disk Access for `/bin/bash` (ruled `grant`; his hands). 5. HPSM: Jira key (`HPSML`), R4-m2's owner option, the HPSM-40 analysis-repo remote. 6. His vault `Notes (MASTER)` on the T9 (484 behind, 102 uncommitted). 7. RD-367's branching-model half. 8. ATTIO digest still to `wednesday-agent@` (measure `FOLLOWUP_DIGEST_TO` at the next ATTIO session, flag as a production change first). 9. `rd104-gh-identity-acceptance-false-premise` → `youcheck` still undelivered (the demo environment reviewer + `CI_DEPLOY_ENABLED` pages). 10. **Not yet asked:** whether `/api/admin/health` being open before first-run (S58's observation) should be a ticket — the RD-327 gate measured it pre-first-run and found no raw SHA there; Tuesday's call.

## ⚠ TRAPS
1. 🔴 Never `git pull --rebase --autostash` here. Wedged rebase: `rebase --abort`, then `git -c core.editor=true merge origin/main`.
2. `setsid` does not exist on macOS — `nohup bash … &`.
3. Store writes: gate on `git merge-base --is-ancestor <origin sha> HEAD`.
4. zsh: no `PIPESTATUS`, no word-splitting of `$VAR`; loop in python.
5. `cockpit.sh say` takes the pane NAME; `pane_close.sh` and `wake_ack.sh` take the `%ID`.
6. The frozen-busy leg fires on THIS pane while a background watcher runs: check the watcher output + inbox, then `wake_ack.sh %0`.
7. Exiting watcher: see DONE (tracked path now).
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
22. Grep the target launcher for EVERY verb and path the HOLDS name — derived from the holds text.
23. `decision_queue.sh` and `reconcile_rulings.py` live in `2_Project_Files/tools/`. Capture a tool's rc on its own line before any `| grep`.
24. AgentMail `GET …/messages/<id>` needs the id URL-encoded.
25. The send gate refuses any ticket id in the QUEUE without a PROVENANCE state line.
26. Two QA gates booting local servers at once can collide on ports — stage the second, or name ports in both briefs.
27. A counts-file merge conflict: `1/1` placeholder, then `npm run verify -- --update-counts`.
28. **NEW:** a watcher/probe must give "the read failed" its own branch — s10's watcher woke on a PARSE-ERROR as if it were mail.
29. **NEW:** `git ls-remote origin` in this tree hung ~9 min at 14:28 with no output (cause unmeasured) — bound network reads (`subprocess.run(..., timeout=)`), prefer the ref `panel_sync` already fetched.
30. **NEW:** CronCreate jobs are SESSION-ONLY — a rotation or crash deletes them. s11's `d54df852` was cancelled at 15:3x after the HPSM launch; nothing is scheduled now.
31. NexusAI's Jira env: `JIRA_SITE` is scheme-less (prefix `https://`); vars `JIRA_EMAIL` / `JIRA_API_TOKEN` in NexusAI's own `4_Credentials/.env` (read-only grant; parse only `JIRA_*`, never source the whole file).

## NAS — WED-149 (unchanged)
`com.tuesday.nassync` stays BOOTED OUT until the partition is built into the file/plist. Design `1_Project_Definition/Architecture/2026-09-10_nas-two-seat-sync-check.md`.

## OWED, not started
- Amend `Launch_Tuesday.command`: step 5 (no Tuesday daily note — name the pickup, this seat's ledger, `git log`) and its stale first-boot line (`FIRST-BOOT-TUESDAY.md` is in `tasks/_superseded_2026-09-09/`). Red-proof by a boot, never mid-task.
- S53's m2/m3, S54's 8 BACKLOG items and round-3 NEW-3/NEW-4 need ticketing on RD (a NexusAI seat's job).
- Raise with Wednesday (shared tool, coordination only): `send_brief.sh --kind brief` could refuse a bare "No az/gh" when the target launcher runs them.
- `TASKS.md`'s NEXT PICKUP pointer names Wednesday's `NEXT-PICKUP.md` — shared file; mention to Wednesday rather than edit.
- Carried: 4 Dependabot alerts on NexusAI's default branch (RD-354 owns qs 6.15.2); three need a `gh` identity.
