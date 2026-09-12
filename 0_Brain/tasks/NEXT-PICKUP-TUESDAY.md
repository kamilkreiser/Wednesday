---
date: 2026-09-12
type: pickup
scope: DATASEC ONLY — Tuesday, on Kamils-Mac-mini. Secuura and general are Wednesday's, on the Studio.
source: written WHOLESALE by Tuesday s11 at ctx ~42%, 2026-09-12 ~14:45 AEST. s11 booted 14:24 on s10's rotation.
status: live
supersede: replace WHOLESALE at the next pickup; never append.
---

# NEXT PICKUP — Tuesday s12. FLOOR EMPTY: no Datasec agent live (S58 wrapped + closed 14:4x). 🔴 HPSM card `hpsm-composer-monday-review-scope` — DEFAULT FIRES AFTER THE ~04:00 SUNDAY RESET. Kam also holds the registry name (B2).

**On EVERY wake:** `2_Project_Files/tools/kam_rulings_today.sh` (never `kam_msgs.sh` unfiltered) AND `[Kam -> Tuesday]` mails; list `tuesday-agent@` UNFILTERED and route on SUBJECT; `git status --porcelain | grep -v 0_Brain/dashboard/data/`. Rotation band 80–90. **Verify panel messages AT ORIGIN** (`git show origin/main:0_Brain/dashboard/data/chat_tuesday.json` on the ref `panel_sync` fetches; `git ls-remote` HUNG 9 min in this tree at 14:28 — bound any network read with a timeout). **Do NOT read `0_Brain/daily/`** (Wednesday's).

## 🔴 LIVE — with the next action for each
1. **HPSM DEFAULT (card `hpsm-composer-monday-review-scope`, unruled at 14:45).** Kam asked 13:50 (panel): *"how is the HPSM project going? do you think it will be ready to review by Monday?"* — answered ~13:58 (verified at origin `ba311ae0`). Measured answer: not a working product by Monday — WP0/WP1/WP2 built (WP2 hardened over four gates, pushed `afc10e9` on `datasecau/HPSM-light`); WP3 rules engine, WP4 API, WP5 screens, WP6 renderers NOT built; the running stack still connects as the Postgres superuser. Options: `render-slice` (RECOMMENDED: WP3 + the WP6 renderer slice for one test policy in the HPSM Policy PowerPoint's layout, each through its gate) · `review-as-is` · `api-first`. **MECHANISM: s11 armed a ONE-SHOT CronCreate job `d54df852` for 04:07 Sun 13 Sep — SESSION-ONLY, it dies with s11. A successor seat MUST re-arm it (`CronList` first) or run the steps at its boot if past 04:00.** Steps: confirm the 7d figure has RESET on the statusline (if not, wait) → `kam_rulings_today.sh` + `decision_queue.sh show hpsm-composer-monday-review-scope` + unfiltered inbox (he may have ruled) → read `HPSM/5_Project_History/history.md` newest + `HPSM/BACKLOG.md` open R4/S3 + architecture §6.1 WP3/WP6 rows (`HPSM/1_Project_Definition/Architecture/2026-09-10_policy-composer/2026-09-10_policy-composer_ARCHITECTURE.md`) → brief via `send_brief.sh` with `RULED BY KAM, NOT YET IN AN ARTEFACT` (carry A-54: *"the HPSM Policy..PPT is the layout and style that the output should look like"*) and the undelivered HPSM cards `hpsm-composer-round3-approver-guard`, `hpsm-credential-bearing-prd-outside-every-snapshot` → verify at `datasec-hpsm@` → `cockpit.sh add 'Datasec/HPSM' "bash '/Volumes/KK_T9_External_HDD/!CODING/Datasec/HPSM/Launch_Claude.command'"` → rung-5 launch check → tier-1 gates at each READY. Nothing HP-facing, no deploys. Still Kam's for HPSM: Jira key (`HPSML`), R4-m2 owner option, the HPSM-40 analysis-repo remote.
2. **Kam — registry B2, and RD-391.** He ruled `publish-image` (11:34); Tuesday asked 11:36 which registry. **Nothing is built or pushed until he names it.** **RD-391 (High):** `.dockerignore`'s `*.pem`/`*.key`/`.env` rules are anchored at the context root; the long-lived `NexusAI/2_Project_Files` holds `backend/ReportingDashboard_key.pem`. **Whether any past image (incl. the May `nexusaidevacrfa39.azurecr.io/nexusai:2.0.0`) was built from that tree is UNMEASURED.** **The B2 image brief MUST require:** a fresh checkout (never `2_Project_Files`), RD-391's any-depth rules applied or the built image scanned for `*.pem`, `*.key`, `.env*` before any push, and the same READ-ONLY content check of the May image.
3. **NexusAI — no seat; today's commissioned RD queue is DONE.** `main` = `c469ae9b62810086627545a75b73d53d72974809` (RD-327 merge; verified at source by s11 with read verbs: parents `2279eeb` + `67c2992`, counts 2338/122 → 2375/123, `deploy-demo.yml` +1 build-arg line, both `CI_DEPLOY_ENABLED` conditions + `environment: demo` intact). Jira read by s11: RD-327 Release Ready (comment 37352, O-2 note) · RD-302 comment 37353 (O-3) · RD-397 + RD-398 filed, Medium, linked. S58 wrap 04:37:28Z (DKIM/DMARC pass); pane `%17` closed, listeners 12 → 12. Kam told on the panel ~14:40 (**verified at origin `6a946bde`**). Entry card `projects_index/entries/Datasec__NexusAI.md` updated from S58's index card. **🔴 Before ANY demo deploy of `main`:** read `red_flag_enabled` on the live demo AND dev stores (RD-150); Kam's check of the demo environment reviewer + `CI_DEPLOY_ENABLED` settings pages (card `rd104-gh-identity-acceptance-false-premise` → `youcheck`, undelivered). Residue for a future seat: RD-391 (High), RD-395 product call, RD-392/393/394/396/397/398, unmerged `s55-/s57-/s58-history-docs` (merge not authorised), 7 worktrees left (`rd-327-s58` holds node_modules — remove last).

## ⚠ CAPACITY
7-day allowance **92% at 14:37** (renews ~04:00 Sun). Kam lifted the 95% no-new-launch line for WEDNESDAY's launches (13:55, via her coordination mail). The allowance is SHARED; if it hits 100% every seat stops mid-turn. **Tuesday's own line unchanged: launch nothing new from 95%.** Nothing is running on the Datasec floor, so there is nothing to recover if it runs out.

## ✅ DONE IN s11 (verified)
- Brain whole: by-tier digest 5,389 lines (last line asserted) + own ledger 99 rows → `ctx:11% → 39%`. Boot digests committed (`de1dd220`, at origin) — they were holding `panel_sync` in SKIP from 14:26.
- WED board 26 active (board_count.sh), 0 `lesson`. `reconcile_rulings.py`: 53 taps, 0 to rule.
- RD-327 merge + S58 wrap verified and closed out (live item 3). Ledger row: the watcher's parse-error false wake + the hung `ls-remote` verifier.
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
30. **NEW:** CronCreate jobs are SESSION-ONLY — a rotation or crash deletes them; re-arm from this pickup.
31. NexusAI's Jira env: `JIRA_SITE` is scheme-less (prefix `https://`); vars `JIRA_EMAIL` / `JIRA_API_TOKEN` in NexusAI's own `4_Credentials/.env` (read-only grant; parse only `JIRA_*`, never source the whole file).

## NAS — WED-149 (unchanged)
`com.tuesday.nassync` stays BOOTED OUT until the partition is built into the file/plist. Design `1_Project_Definition/Architecture/2026-09-10_nas-two-seat-sync-check.md`.

## OWED, not started
- Amend `Launch_Tuesday.command`: step 5 (no Tuesday daily note — name the pickup, this seat's ledger, `git log`) and its stale first-boot line (`FIRST-BOOT-TUESDAY.md` is in `tasks/_superseded_2026-09-09/`). Red-proof by a boot, never mid-task.
- S53's m2/m3, S54's 8 BACKLOG items and round-3 NEW-3/NEW-4 need ticketing on RD (a NexusAI seat's job).
- Raise with Wednesday (shared tool, coordination only): `send_brief.sh --kind brief` could refuse a bare "No az/gh" when the target launcher runs them.
- `TASKS.md`'s NEXT PICKUP pointer names Wednesday's `NEXT-PICKUP.md` — shared file; mention to Wednesday rather than edit.
- Carried: 4 Dependabot alerts on NexusAI's default branch (RD-354 owns qs 6.15.2); three need a `gh` identity.
