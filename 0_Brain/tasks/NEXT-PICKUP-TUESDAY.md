---
date: 2026-09-12
type: pickup
scope: DATASEC ONLY — Tuesday, on Kamils-Mac-mini. Secuura and general are Wednesday's, on the Studio.
source: written WHOLESALE by Tuesday s10 at ctx 63%, 2026-09-12 ~13:05 AEST. s10 booted 11:56.
status: live
supersede: replace WHOLESALE at the next pickup; never append.
---

# NEXT PICKUP — Tuesday s11. LIVE: RD-327 tier-1 gate `%19` · NexusAI S58 `%17` HOLDING for RD-327's merge (main `2279eeb`: RD-342, RD-382, RD-150 all merged and verified). 🔴 HPSM card `hpsm-composer-monday-review-scope` — DEFAULT FIRES AFTER THE ~04:00 SUNDAY RESET. Kam also holds the registry name (B2). ⚠ The shared allowance may run out before the reset.

**On EVERY wake:** `2_Project_Files/tools/kam_rulings_today.sh` (never `kam_msgs.sh` unfiltered — it prints Wednesday's Secuura messages) AND `[Kam -> Tuesday]` mails; list `tuesday-agent@` UNFILTERED and route on SUBJECT; `git status --porcelain | grep -v 0_Brain/dashboard/data/`. Rotation band 80–90. **Verify panel messages AT ORIGIN** (`git ls-remote`, `git fetch --no-write-fetch-head origin main`, `git show <sha>:0_Brain/dashboard/data/chat_tuesday.json`). **Do NOT read `0_Brain/daily/`.**

## 🔴 LIVE — with the next action for each
1. **RD-150 — MERGED and VERIFIED.** `main` = `2279eeba4f4d0174b6df2980b094b6e22358ec46` (parents `7a11418` + `bec76f6`; `67c2992` correctly NOT an ancestor; counts 2338/122; the merge touched exactly RD-150's 4 files) — read at source by Tuesday s10 (read verbs on `worktrees/merge-rd342-rd382-s58`). Gate GO WITH FINDINGS 0/0/2/1 (03:45:01Z), scored: gate 1.00, S55's round 0.95. RD-150 Release Ready with the deploy-behaviour BLUF (comment 37351); residue **RD-395** (Medium, `aiEnabled` display-only, two fix shapes NEITHER chosen) and **RD-396** (Low, `red_flag_enabled` `''`/`0` mismatch + log text), both `Relates` to RD-150. Kam told on the panel ~14:03 (origin check was still polling when s10 rotated — re-check at origin; RD-150 merged; any demo deploy now makes the risk-alert off switch real; live demo value unmeasured). **Before any NexusAI demo deploy: someone reads `red_flag_enabled` on the live demo and dev stores.**
2. **NexusAI S58 — pane `%17`, claude pid 17879, HOLDING for RD-327's merge.** It merged RD-342 + RD-382 (`7a11418`) and RD-150 (`2279eeb`) today, all verified at source; filed RD-392..RD-396. **Told at 03:59:19Z (delivered; tap queued) to write `NexusAI/HANDOVER-S58.md` right after its RD-150 MERGED mail and keep it current** (the shared allowance may run out). **NEXT:** at the RD-327 gate's GO, an ANSWER to merge RD-327 onto `2279eeb` (its branch is cut from `34e7fc4`: expect the counts conflict at least; use the 1/1 recipe; any other conflict STOP). Score S58 after the RD-327 gate (whole session). **S58 wrote `NexusAI/HANDOVER-S58.md` at 14:02 (117 lines, state section current; verified by Tuesday) and measured RD-327's merge onto `2279eeb`: merge-base `34e7fc4`, exactly ONE conflict (`scripts/verify-expected-counts.json`), predicted 2375/123 — use that in the RD-327 merge ANSWER.**
3. **RD-327 TIER-1 GATE — pane `%19` `QA/NexusAI-RD327`, claude pid 29295, launched ~13:46, verified at rung 5** (reading its brief). Brief `2_Project_Files/fleet/qa-agent/briefs/2026-09-12_nexusai-rd327-67c2992-tier1.md`; launcher `…/launchers/launch_qa_nexusai_rd327_67c2992.sh` (`--check` re-run and passed before launch). Verdict subject `[QA/Datasec-NexusAI -> Tuesday] GATE VERDICT — RD-327 @ 67c2992 (tier 1)`; report `…/reports/2026-09-12-rd327-67c2992-tier1/report.md`. Key asks: raw SHA on ANY unauthenticated surface = Blocker; S58's ⚑3 preload question; `github.sha` per trigger; `shasum` on the CI runner (R1b). **NEXT at the verdict:** completion check, score gate + S58 (whole session: RD-327, the ⚑1/⚑4 catches, both merges), rule; GO → ANSWER to S58 to merge RD-327 (its branch is cut from `34e7fc4`: expect the counts conflict, and more now that RD-150 is in); `pane_close.sh %19`.
4. **Kam — registry B2, and RD-391.** He ruled `publish-image` (11:34); Tuesday asked at 11:36 which registry. **Nothing is built or pushed until he names it.** **RD-391 (High, filed by S58):** `.dockerignore`'s `*.pem`/`*.key`/`.env` rules are anchored at the context root, so a gitignored key under `backend/` enters any image built from a tree that holds one — and the long-lived `NexusAI/2_Project_Files` holds `backend/ReportingDashboard_key.pem`. **Whether any past image (including the May `nexusaidevacrfa39.azurecr.io/nexusai:2.0.0` customers get today) was built from that tree is UNMEASURED.** Kam told at ~13:00 (verification at origin was polling at write time — re-check with `git show origin`). **The B2 image brief MUST require:** a fresh checkout (never `2_Project_Files`), RD-391's any-depth rules applied or the built image scanned for `*.pem`, `*.key`, `.env*` before any push, and the same READ-ONLY content check of the May image.
5. **Panel today:** 12:10 note (verified at origin `20ae0e22`); ~13:00 note on the gates + RD-391 (verified at origin `ce4a207f`); ~13:25 note on the merges and the demo-deploy approval (verified at origin `4f393e36`).

6. **🔴 HPSM — Kam asked at 13:50 (panel, `view=tuesday`, verbatim): *"how is the HPSM project going? do you think it will be ready to review by Monday?"*** Receipt posted 13:5x; answered on the panel ~13:58 (card and answer verified at origin `ba311ae0`) with card **`hpsm-composer-monday-review-scope`** (added with `--override-prior-rulings`, reason measured in its BLUF). **Measured answer:** not a working product by Monday — WP0 skeleton, WP1 content model and WP2 database layer are built (WP2 hardened over four gate rounds, pushed `afc10e9` on `datasecau/HPSM-light`); WP3 rules engine, WP4 API, WP5 screens and WP6 renderers are NOT built; the running stack still connects as the Postgres superuser, so RLS is proven in tests but not enforced when the stack runs. Options: `render-slice` (RECOMMENDED: WP3 + the WP6 renderer slice for one test policy in the HPSM Policy PowerPoint's layout, each through its test gate) · `review-as-is` · `api-first` (WP4). **DEFAULT, and this pickup is its mechanism: if Kam has not ruled, the first Tuesday seat live after the ~04:00 Sunday 7-day reset launches the render-slice HPSM seat.** Honest limit: if no seat is live at 04:00, it fires at the next boot. **Steps:** run `kam_rulings_today.sh` + `decision_queue.sh show hpsm-composer-monday-review-scope` FIRST (he may have ruled); read `HPSM/5_Project_History/history.md` newest entry + `HPSM/BACKLOG.md` open R4/S3 items + the architecture §6.1 WP3/WP6 rows (`HPSM/1_Project_Definition/Architecture/2026-09-10_policy-composer/2026-09-10_policy-composer_ARCHITECTURE.md`); brief via `send_brief.sh` with `RULED BY KAM, NOT YET IN AN ARTEFACT` (carry A-54: *"the HPSM Policy..PPT is the layout and style that the output should look like"*); verify at `datasec-hpsm@`; launch with `cockpit.sh add 'Datasec/HPSM' "bash '/Volumes/KK_T9_External_HDD/!CODING/Datasec/HPSM/Launch_Claude.command'"`; tier-1 gates at each READY. Nothing HP-facing, no deploys. Still Kam's for HPSM: Jira key (`HPSML`), R4-m2 owner option, the HPSM-40 analysis-repo remote.

## ⚠ CAPACITY — MAY RUN OUT BEFORE THE RESET
7-day allowance **91% at 13:55** (86% 10:00 → 88% 11:56 → 90% 13:05 → 91%). **Kam lifted the 95% no-new-launch line for WEDNESDAY's launches at 13:55** (relayed by Wednesday's coordination mail 03:56:39Z, spf/dkim/dmarc pass; his words were on her tab). The allowance is SHARED, so it may reach 100% before the ~04:00 Sunday reset, and then every live seat stops mid-turn, this one included. **Tuesday's own line is unchanged: launch nothing new from 95%.** S58 was told (~13:59) to write `NexusAI/HANDOVER-S58.md` right after its RD-150 MERGED mail.

**IF THE ALLOWANCE RAN OUT — recovery at the first boot after the reset:**
1. Read each pane's last output (`%17` S58, `%19` RD-327 gate) and `git ls-remote` NexusAI `main`: did RD-150 land, and is `bec76f6` an ancestor?
2. Relaunch S58's work from `NexusAI/HANDOVER-S58.md`, or from S57's handover plus this pickup if S58 never wrote it.
3. **A cut RD-327 gate:** if its report file exists, the launcher's guard refuses (rc 17). That report lives in `Testing Agent MAIN`, which is read-only to Tuesday, so re-gate under a NEW report path (a `-retry` brief and launcher) and never touch the partial file.
4. Then the HPSM default (live item 6).

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
27. **NEW (S58's recipe, adopted):** a counts-file merge conflict is resolved by writing a `1/1` placeholder, then `npm run verify -- --update-counts` — the gate refuses a `0/0` or unparseable expectation even under `--update-counts`.

## NAS — WED-149 (unchanged)
`com.tuesday.nassync` stays BOOTED OUT until the partition is built into the file/plist. Design `1_Project_Definition/Architecture/2026-09-10_nas-two-seat-sync-check.md`.

## OWED, not started
- Amend `Launch_Tuesday.command`: step 5 (no Tuesday daily note — name the pickup, this seat's ledger, `git log`) and its stale first-boot line (`FIRST-BOOT-TUESDAY.md` is in `tasks/_superseded_2026-09-09/`). Red-proof by a boot, never mid-task.
- S53's m2/m3, S54's 8 BACKLOG items and round-3 NEW-3/NEW-4 need ticketing on RD.
- Undelivered ruled HPSM cards: `hpsm-composer-round3-approver-guard`, `hpsm-credential-bearing-prd-outside-every-snapshot`.
- Raise with Wednesday (shared tool): `send_brief.sh --kind brief` could refuse a bare "No az/gh" when the target launcher runs them.
- Carried: 4 Dependabot alerts on NexusAI's default branch (RD-354 owns qs 6.15.2); three need a `gh` identity.
