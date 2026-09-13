---
date: 2026-09-13
type: pickup
scope: DATASEC ONLY — Tuesday, on Kamils-Mac-mini (T9 drive). Secuura and general are Wednesday's, on the Studio.
source: written WHOLESALE by Tuesday s12 at ctx ~58%, 2026-09-13 17:4x AEST (s12 booted 16:48 on Kam's hand restart). The previous pickup (s11, items 0000–0037, traps 1–39, WITH KAM list, OWED list) is kept VERBATIM at `0_Brain/tasks/NEXT-PICKUP-TUESDAY.md.pre-1740`. Read its TRAPS, WITH KAM and OWED sections; its LIVE items are superseded by this file.
status: live
supersede: replace WHOLESALE at the next pickup; never append.
---

# NEXT PICKUP — Tuesday s13 (written by s12)

**On EVERY wake:** run `2_Project_Files/tools/kam_rulings_today.sh` (never `kam_msgs.sh` unfiltered) and check `[Kam -> Tuesday]` mails. List `tuesday-agent@` UNFILTERED and route on SUBJECT. Run `git status --porcelain | grep -v 0_Brain/dashboard/data/`. Rotation band is 80–90. **Verify panel messages AT ORIGIN** (`git show origin/main:0_Brain/dashboard/data/chat_tuesday.json`). **Do NOT read `0_Brain/daily/`** (Wednesday's). Kam also types straight into this terminal session: those lines are first-party.

## 🟢 s13 BOOT 19:04–19:08 (rotation successor; this block is the only s13 addition so far)
- **Rotation 19:04:15** by s12 (`--self` after renaming `%0` to tuesday): `respawned OK` + **`LIVENESS OK: 3/3 agent panes present`** (`2_Project_Files/fleet/cockpit/logs/rotate_wednesday.log`, 19:04:39). **`%0` renamed back to `wednesday` at 19:05 (rc 0)** so `arm_wake_watch` taps land.
- **Brain whole:** by-tier digest 5,437 lines (last heading asserted) + own ledger 101 rows → **ctx:37%**. WED board 27 active, 0 `lesson` (`board_count.sh`). Kam's panel today: 5 shown (view=tuesday), nothing after 18:02. Newest PROCESSED mail = S43 REPORT 08:58:40Z; nothing newer at 19:06.
- **Floor at 19:07:** `%5` S43 (claude pid 1666, ctx 68%, e2e spec-2 under the docker lock + feedback vitest), `%6` QA/HPSM-ACC (claude pid 83570, running), `%1` monitor. Shared wake runner `wake_watch.sh` pid 85562 alive (baseline 08:58).
- **s13 exiting watcher** (harness background task, dies with this seat): `watch_tuesday_exiting.sh 2026-09-13T08:58:41 23:55 1666 83570`.
- Panel note to Kam 19:08:00 (fresh seat, agents survived, fix round + live acceptance test running, nothing needed) — **VERIFIED AT ORIGIN** 19:08:40 (`git show origin/main:…/chat_tuesday.json`, row 188, origin `f1e98441cf`).
- Prep read 19:08 (read-only): no `HANDOVER-S43*` in HPSM `5_Project_History/` yet; routing has rows for HPSM, HPSM-S42, HPSM-S43 (an S44 row is still to add); the ACC report directory holds `evidence/` only, no `report.md` yet.
- 🔴 **19:1x — KAM ASKED "Did you get my instructions from the last boot?"** s13 extracted s12's human lines from its transcript (`4_Credentials/.claude/projects/-Volumes-KK-T9-External-HDD-TUESDAY/b511be06-6fe0-42f7-8fc5-eafb0c334965.jsonl`): ten lines, nine carried. **DROPPED: 19:01:39 "In the HPSM sign-in page, each of the sign-in options needs a much better description of what the options mean. Make this description in gray with a much smaller text at the bottom. Of each tile."** It was queued mid-turn and removed at the 19:04 respawn. Ledger row w=4 (the successor-boot transcript-diff rule).
  - Kam told on the panel 19:11:46 (VERIFIED AT ORIGIN). Prompt-logged.
  - **Relayed to S43 09:14:09Z** (`briefs_staged/2026-09-13_hpsm-s43-kam-signin-descriptions.md`; sent copy from tuesday-agent@, preview non-null; tapped `Datasec/HPSM-S43` with `--mail` verified, queued behind its turn). Partition: `SignIn.tsx` is in no fix lane, but `app.css` belongs to FX-S7, so it goes inside FX-S7 or after it merges; S43 names the choice and an ETA in its next STATUS. **NEXT:** confirm the STATUS names it; the sign-in change goes into the delta gate (browser leg). **Mark the relay delivered to Kam only once a READY names its artefact.**
- **S43 QUESTION 09:09:54Z (feedback product name) → (b) RULED 09:14:10Z** (`briefs_staged/2026-09-13_hpsm-s43-answer-feedback-product-name.md`): brand.ts `productName` on screen, HPSM internally. It SUPERSEDES the brief's "HPSM Policy Composer" string line, citing Kam's 16:53 words "registered against HPSM". W45-p2 stays Kam's. S43's 09:10:46Z CORRECTION (the path is `apps/web/src/brand.ts`) needs no reply; it matches what Tuesday read.
- **S43 ctx 72% at 19:1x** (70% checkpoint). Its successor S44 comes at its 80–90 wrap, via a brief plus a new pane, **never `cockpit.sh rotate`** (the wake text suggests it; trap 37).
- **Wednesday COORDINATION 09:14:50Z (DKIM pass, read whole, no reply needed):** she CLAIMS the seat-name resolver unification. The cockpit will name the coordinator pane after the seat, and `wednesday_rotate.sh`, `wake_watch.sh` and `arm_wake_watch.sh` will accept the seat name OR the legacy `wednesday`, scratch-tested for both seats before anything is armed. **Until she mails the commit sha plus the scratch-test output, the pickup's item-5 workaround stands** (rename `%0` to tuesday, `WED_AGENT=tuesday --self`, then the successor renames it back to wednesday). She will not change the pane-name contract without mailing first. She also took the statusline-publisher skip-write proposal as owed.
- **S43 STATUS 09:17:14Z (DKIM pass, read whole; no reply needed):**
  - (b) naming is relayed to F-WEB: the name comes from brand.ts, with a scan test and a mutant.
  - **Kam's sign-in descriptions → NEW lane FX-SI** (`s43/fx-si-signin`, stack pc-s43-si 23680, from caf63fd). It owns `SignIn.tsx`, a new `signInDescriptions.ts` (`Record<Role,string>`), a render test and `e2e/s43-signin-descriptions.spec.ts`.
  - FX-S7 adds ONE css rule, `.pc-choice-desc`: 11px, `--pc-text-muted`, the existing token. If axe contrast fails, the lane reports the ratio to Tuesday rather than changing the colour.
  - Content comes from `apps/api/src/authz.ts` (role-matrix comment plus the permission sets). `bridge_operator` must say the Bridge is a stub (I-37). No mention of feedback, no HP marks, and `aria-describedby` on each radio.
  - **READY ETA about 20:05–20:20 AEST;** it ships in the next rolling upgrade and goes to the delta gate (browser leg).
  - **NEXT:** on the READY, check the descriptions against authz (completion check) and the contrast result. Warn Kam on the panel before the upgrade restart.
- Panel note to Kam 19:18:24 (the sign-in change has a lane, ETA 45–60 min, next rolling upgrade). **VERIFIED AT ORIGIN** at 19:20 (row 190).
- 🔴 **19:2x — KAM (terminal): "I didn't see your response to my question whether you got the instruction before we booted and whether the agent has been advised."** Answered in the terminal, with "no" as the first word. Also posted on the panel at 19:21:41 (local API shows it).
  - **Why he did not see the 19:11 and 19:18 notes, as measured:** both are at origin, and the Studio has pushed commits since, so its copy pulled them. **But `chat.html:190` `inView()` and `cockpit.html:367` `msgInView()` show a reply ONLY when the panel's active view matches its agent.** Tuesday's rows are `agent: tuesday`, so they are **hidden on the WEDNESDAY tab**. His latest typed panel row (18:17) is `view: wednesday`.
  - **Which tab he was on is UNMEASURED** (per-browser localStorage on the Studio). Kam was told to switch to the orange TUESDAY tab.
  - **Rule until settled:** a question Kam asks in THIS terminal is answered in the terminal, with the yes/no in the first words; the panel copy is secondary.
- 🔴🔴 **19:23 — ACCEPTANCE GATE INTERIM (09:23:04Z, DKIM pass): LIVE DEMO BLOCKER on caf63fd.**
  - Through the public URL, sign-in works, and every API call after it gets 401 from the Caddy Basic gate. The app shows "Your session ended".
  - **Cause:** the gate and the API both need the `Authorization` header. Verified at source by s13: `apps/api/src/auth.ts:44` accepts only `^Bearer`, and `apps/web/src/api/client.ts:23` sends `Bearer`. The Caddy config is not in the repo under Caddyfile/sh/yaml/conf globs, so that leg is the gate's measurement.
  - **s12's 19:00 "upgraded and back up" note was verified only by a 401 challenge plus a 200 sign-in page**, never an authenticated call through the gate. Ledger row.
  - The gate is NOT creating its live tenant. Live walk-through probes 2/3/5/7/9/11/12/13 will be NOT TESTED on live and are running on its local stacks instead.
  - **Kam ASKED on the panel ~19:25: "go" or "hold" on fix (b)** (Basic stays on everything except `/api/*`; the API keeps its bearer check; `/idp/*` stays gated). **Default until he answers:** S43 prepares and measures only, nothing applied on Azure.
  - **S43 briefed 09:25:25Z** (`briefs_staged/2026-09-13_hpsm-s43-urgent-live-gate-blocker.md`; tap `--mail` verified, prompt clear). The ask: reproduce through the public URL; stage (b) on pc-lane-a with a rollback; measure `/api/*` unauthenticated answers (**a 200 with data and no bearer = STOP**); `/idp/token` still challenges; send a READY-TO-APPLY; add a public-gate browser sign-in + S1 check to every upgrade post-check.
  - **NEXT:** (1) on Kam's go, relay it verbatim (a KAM mail) and S43 applies with a head mail first; warn Kam about the restart. (2) On READY-TO-APPLY, read the `/api` exposure list before relaying anything. (3) After the fix, commission a re-run of the live half of the acceptance gate (the NOT TESTED probes).
- **s13 watcher re-armed:** `watch_tuesday_exiting.sh 2026-09-13T09:23:05 23:55 1666 83570`.

## 🟢 KAM, 18:5x AEST, terminal, verbatim: *"Keep going and finish what you can.  no matter the time.  keep going until completion"* — the successor's first jobs, in order
1. **Every wake:** the unfiltered inbox. S43's fix-round PLAN, its pre-upgrade head mail, the upgrade REPORT and READYs are answered as they land (rules in LIVE items 1–2).
2. **When S43 wraps (80–90% ctx):**
   - census `ps` for HPSM claudes;
   - brief **S44** from `HANDOVER-S43_*.md`: the fix round, the upgrade rule (by 07:00 Monday at the latest), the F-API/F-WEB feedback lanes, C11, and the credential rebuild after C11;
   - add a routing row `Datasec/HPSM-S44`, then `cockpit.sh add` a NEW pane and verify rung 5;
   - close `%5` with `pane_close.sh` only after S44 CONFIRMS its plan;
   - **never `cockpit.sh rotate` (trap 37).**
3. **After the fix round merges:** commission ONE delta tier-1 gate on `09c1591..<fix head>` (Q + W + fixes; use the combined launcher as the model). **Push to HPSM-light only on GO + Tuesday's word.**
4. **After the live-upgrade REPORT:**
   - launch the acceptance+security harness (LIVE item 3), naming the live head in the launch prompt;
   - give Kam one short panel note: upgraded, which engagements to use, and the old ones DO NOT USE.
5. **Tuesday's own rotation — ⚠ `wednesday_rotate.sh --self` REFUSES for this seat as-is (measured by reading, s12 19:1x).**
   - **Why:** line 67 finds the coordinator pane by `@cockpit_name == $SEAT` = `tuesday`, but this machine's coordinator pane `%0` is named `wednesday`. `arm_wake_watch.sh:134-146` (taps + the DEAD case) HARDCODES `^wednesday|`; `wake_watch.sh:79` uses the seat.
   - **So:** taps reach this seat only through the hardcoded name, `--self` refuses rc 2, and **a DEAD Tuesday seat cannot be auto-respawned** (`--dead` refuses too). **Never let this seat reach 90%.**
   - **PROCEDURE, only when no live upgrade is in progress** (a fleet-session loss would kill S43 mid-deploy):
     1. Pickup current and committed, HEAD in origin, tree clean.
     2. `tmux set -p -t %0 @cockpit_name tuesday`
     3. `WED_AGENT=tuesday nohup bash 2_Project_Files/fleet/cockpit/wednesday_rotate.sh --self > /dev/null 2>&1 &` (its log is `logs/rotate_wednesday.log`).
   - **The SUCCESSOR's first actions:**
     - (a) check the rotate log for `respawned OK` + `LIVENESS OK`, and that `%5` and the other agent panes survive;
     - (b) **`tmux set -p -t %0 @cockpit_name wednesday`**, so `arm_wake_watch` taps reach it again.
   - Wednesday has been told (a coordination mail proposes one naming source).
   - The ORIGINAL line follows for history: at the first safe boundary inside 80–90, with the pickup current and HEAD == origin, run `WED_AGENT=tuesday nohup bash 2_Project_Files/fleet/cockpit/wednesday_rotate.sh --self &`. Kam's words above are the authority not to wait for a hand restart; card `tuesday-seat-self-rotate-with-liveness-check` is left for him. **The new seat checks `2_Project_Files/fleet/cockpit/logs/rotate_*.log` for LIVENESS OK and that `%5` (plus any agent panes) survived.**
6. **Next Datasec lane once HPSM is stable:** NexusAI **RD-391 (High, `.dockerignore` any-depth)**. Brief it only after a fresh read-only Jira read (board_count.sh; NexusAI's own `JIRA_*`; trap 31 in `.pre-1740`). Its residue RD-392/393/394/396/397/398 partitions by file; RD-395 is Kam's product call. **The load on this Mac mini is the constraint** (gate C saw ~115–347): keep NexusAI's docker steps under the shared lock.

## 🟢 KAM ~18:5x, terminal, verbatim: *"If you don't need to wait until 2100, don't wait. Upgrade as soon as it's ready, and I'll continue doing the testing before tomorrow."*
- **S43 told (ANSWER ~08:5xZ), SUPERSEDING the 21:00 window and the 'second upgrade before 07:00' rule:**
  - upgrade NOW on `caf63fd`, keeping the dry-run; the upgrade gets the docker lock first;
  - then ROLLING upgrades as each fix lane merges GREEN, batched within ~30 min;
  - before each later upgrade S43 sends a head mail and waits ~5 min.
- **Tuesday's job on each head mail:** a short panel warning to Kam (the site restarts for a few minutes).
- **Tuesday's job on each REPORT:** a panel note with what changed, the engagement to use, and the DO NOT USE list.
- **Kam is TESTING THE LIVE SITE tonight.** No agent touches engagements or tenants it did not create. A later upgrade that would strand engagements (a content hash change) STOPS for Tuesday.

## 🟢 19:0x (s12) — LIVE UPGRADE IN PROGRESS + HARNESS READY
- **S43 HEAD mail 08:53:18Z** (DKIM pass): upgrade STARTED on `caf63fd` (Q+W, 57 commits since c2fbc36), pc-lane-a first then Azure, rollback to c2fbc36. The dry run on pc-s43-up released 1.0.0. Kam warned on the panel.
  - **Every engagement created before the upgrade (including any Kam made today) will answer 409** (the demo content changed 0030d4c6 → fd7db6b8). Kam told to use the fresh or post-upgrade engagements.
- **Acceptance + security harness RE-POINTED to `caf63fd`** (commit 'QA: acceptance+security harness re-pointed…'; `--check` rc 0):
  - range 267; report dir `…/reports/2026-09-13-composer-caf63fd-brief-acceptance-security-tier1/`; subject `… @ caf63fd (tier 1)`;
  - cards ruled; gate B/C findings listed as KNOWN fix-in-flight, with the release workaround;
  - Kam testing live concurrently; pause ≤ 15 min on upgrade restarts.
  - **LAUNCH it right after S43's upgrade REPORT lands:** `cockpit.sh add 'QA/HPSM-ACC' "bash '/Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_hpsm_composer_09c1591_brief_acceptance_security.sh'"`, then rung 5. The file name still says 09c1591; the content is caf63fd.
  - **If main moves before launch:** decide to keep caf63fd (it matches the live head) or re-point HEAD_SHA/EXPECTED_COMMITS/REPORT_DIR/SUBJECT in all three files and re-run `--check`.

## ✅ 19:0x (s12) — LIVE UPGRADE DONE, HARNESS LAUNCHED
- **S43 REPORT 08:58:40Z (DKIM pass): the live demo is UPGRADED to `caf63fd` on pc-lane-a AND Azure**, all post-checks GREEN, no rollback.
  - Azure tenant "Synthetic Customer B (demo content)" `e93302d2…` now holds two fresh engagements: A "Demo drafts, one device group (synthetic)" `3bb6fcb2…`, and B "Demo release walk-through, no device groups (synthetic)" `a9101d3f…` RELEASED 1.0.0 (version `b03aae4b…`). pc-lane-a mirrors them (A `e920ac1d…`, B `8ce21d2a…`).
  - **Azure DO NOT USE:** "Office fleet hardening (demo)" `c9bce98b…`, "Demo content proofread (synthetic)" `1ec31037…`. pc-lane-a: 9 listed in the REPORT.
  - Evidence: HPSM analysis `qa-s43/upgrade/live-caf63fd/`.
  - **Verified by s12 19:00:** / , /api/health and /idp/ answer 401 + Basic; wrong credentials 401; TLS verify 0.
  - Card `hpsm-composer-live-demo-upgrade-after-c12` marked DELIVERED 19:00:48.
  - Kam told on the panel: which engagements to use, which to avoid, and the known issues until the fix upgrade.
- **Acceptance + security harness LAUNCHED 19:00:39** in pane `%6` `QA/HPSM-ACC` (launcher `…/launch_qa_hpsm_composer_09c1591_brief_acceptance_security.sh`, content caf63fd, precheck rc 0).
  - Verdict subject: `[QA/Datasec-HPSM -> Tuesday] GATE VERDICT — Policy Composer acceptance vs original brief + security @ caf63fd (tier 1)`.
  - Report: `Testing Agent MAIN/projects/hpsm/reports/2026-09-13-composer-caf63fd-brief-acceptance-security-tier1/report.md`.
  - **NEXT on its verdict:** read the report whole, run the completion check, score, `pane_close.sh %6`, then a panel note to Kam.
- **Remaining tonight:** the fix lanes' READYs, the rolling fix upgrade (head mail, then a panel warning), and the delta gate after the fixes merge. Then S43's wrap and an S44 successor if needed.

## 🔴 LIVE — with the next action for each

1. **HPSM S43 — pane `%5` `Datasec/HPSM-S43`, launched 17:07:52 by s12 with HPSM's own `Launch_Claude.command`.**
   - Census before the launch: 0 HPSM seats.
   - Brief: `2_Project_Files/fleet/briefs_staged/2026-09-13_hpsm-s43-successor-recover-remaining-feedback.md`, sent 07:05:44Z. Verified at `datasec-hpsm@` (from tuesday-agent@, preview non-null).
   - Rung 5 verified from its transcript `~/.claude/projects/-Volumes-KK-T9-External-HDD--CODING-Datasec-HPSM/28f5c90e-….jsonl`, 07:13–07:19Z: it read HANDOVER-S42, read the NexusAI feedback files, started a remaining-work analysis subagent, and grepped the roles in authz.ts.
   - **Its job:**
     - (1) Recover S42's in-flight state. Main is `09c1591`; `s42/lane-q-d2` `0e9c865` is NOT on main; the merge worktree is detached at `3bc7471`; `s42/lane-w-d2` is at `7c31520`. Then the second READY.
     - (2) Kam ask 1: `HPSM/5_Project_History/2026-09-13_S43_remaining-work-and-product-issues.md`, measured against the Detailed Scoping Design Specification v1.1. The E8 SOW is context only.
     - (3) Kam ask 2: port NexusAI's feedback feature, registered against HPSM. Postgres table under RLS; object store; created_by from the token with name + role, no email; role-gated triage; HPSM branding. A report-only sweep whose Jira half stays UNSET, because the Composer Jira key is on HOLD with Kam.
   - **UPDATE 18:2x (s12):**
     - **Plan (07:40Z) CONFIRMED late at 08:07:30Z** (body `briefs_staged/2026-09-13_hpsm-s43-answer-plan-confirmed.md`), accepting: triage by platform_admin only; feedback = tenant data, 365 days, report-only expiry, soft delete; F-API numbers migration 0016.
       - **Amendment 1:** the seat adds compose.yaml env vars.
       - **Amendment 2 (load):** docker steps one at a time under the lock; vitest `--maxWorkers=2`; timeout-only runs re-run at most twice, then LOAD-BLOCKED; never raise a timeout; gates get the lock first.
     - **Ask-1 REPORT 08:01:19Z** at `HPSM/5_Project_History/2026-09-13_S43_remaining-work-and-product-issues.md` (a949591). The BLUF and §4 were read by s12 and summarised to Kam at origin.
     - **STATUS 08:16:15Z:**
       - the seat is re-running chain qd2-s43 on 3bc7471;
       - lane W is running (pc-s43-w 22780);
       - F-API is running (pc-s43-f 22680; contract 0.14.0 first);
       - F-WEB launches on F-API's contract commit;
       - the records subagent is folding BACKLOG/history;
       - S42's worktrees were removed cleanly.
     - **FINDING:** the Composer has NO CSP anywhere, so the brief's "don't loosen the CSP" was false. It was withdrawn by name in an ANSWER ~08:2xZ; F-WEB builds CSP-clean; BACKLOG entry.
     - **Kam RULED at 18:02 (cards recorded by s12 at 18:17):**
       - `hpsm-composer-live-demo-upgrade-after-c12` → `upgrade-fresh-with-release`;
       - `hpsm-composer-demo-release-with-device-groups` → `build-c11`.
       - Relayed at 08:14:48Z, verified at the destination (body `briefs_staged/2026-09-13_hpsm-s43-kam-ruled-upgrade-and-c11.md`).
       - **S43 OPERATES the upgrade after the Q+W merges**, which SUPERSEDES the no-deploy hold for this one upgrade. Steps: identity check; never touch datasec-sales-portal-rg; pc-lane-a first, then Azure; rollback to c2fbc36; a 10-minute check; fresh engagements, one with a group and one with zero groups taken to release through the product; old engagements untouched; REPORT.
       - C11 lane now: partition by exact file; migration 0017 if needed; propose the "unknown" support issue code.
     - **NEXT:**
       - S43's ACK on the KAM RULED mail (C11 paths, migration, issue code, upgrade window). Rule the issue code.
       - The chain verdict or LOAD-BLOCKED, then the second READY, then the upgrade REPORT, then **tell Kam at once**. He asked to be told when the HPSM agent finishes.
       - Mark both cards `--delivered` once the upgrade REPORT and C11's READY name their artefacts.

2. **Three combined tier-1 gates on `09c1591` — RESUMED by s12 at 17:05 in new panes.**
   - **UPDATE 18:5x (s12) — S43 STATUS 08:46:53Z (DKIM pass): LOCAL main fast-forwarded to `caf63fd54c3ad95384bcb7bc32d4e7b9e4a6f5c4`** (lane W F6; 267 ahead of afc10e9; NOT pushed).
     - **Chain merge-w-s43 GREEN:** host 1052+1 with 0 timeouts; DB 205; API-DB 428; upgrade e2e 58; CI GREEN; **switch-ON e2e 58/58 with 0 failures → the D1 rule is RETIRED.** Evidence: analysis f88bb73.
     - **`caf63fd` = TONIGHT'S UPGRADE TARGET** unless a fix lane merges GREEN before 21:00 (a new head mail would come first).
     - **Walk:** dry-run first on seat stack pc-s43-up 23580. Azure API calls go through an SSH tunnel to the VM's 127.0.0.1:18080 (Caddy basic auth and the bearer collide in one header); the 401 gate checks run on the public URL.
     - **Noted, no action:** S40's committed `remote-update.sh` deletes its own VM staging dirs (composer.new/prev); rollback redeploys the c2fbc36 archive through `redeploy.sh`.
     - The records fold is in (analysis 85eb6b0).

   - **UPDATE 18:5x (s12) — S43 FIX-ROUND PLAN 08:41:36Z CONFIRMED ~08:5xZ:**
     - **Lane W:** GREEN 5e173eb, merged `caf63fd` (the chain merge-w-s43 must be GREEN before main moves).
     - **Fix lanes** from caf63fd, disjoint by path:
       - FX-M1 (s43/fx-m1-approver, pc-s43-m1 23180: approver linked + 422 APPROVER_NOT_A_TENANT_MEMBER; not editable after create);
       - FX-LV (s43/fx-lv-local-values, 23280: LOCAL_VALUE_NOT_DEFINED critical + S8/S10 naming);
       - FX-R (s43/fx-r-renderers, 23380: W6-M1, m1, m2, m3);
       - FX-S7 (s43/fx-s7-layout, 23480: W5-M3 + W5-m5; SOLE owner of app.css and e2e/support).
     - **Then:** FX-PIN (W4B-m2; lifecycle/inputs/resolution.ts), then FX-ID (W4B-m1 central id normalisation, before F-API merges). C11 PAUSED until FX-LV merges.
     - **BACKLOG notes sent:** the approver picker reads idp-mock `/idp/users` (needs a real directory source); approver-edit op deferred.
     - **Timeline (S43's estimate):** W chain ~19:05; FX-S7/FX-R ~20:30–21:15; FX-M1 ~21:30; FX-LV ~22:00. **Tonight's 21:00–23:30 upgrade = Q+W + the workaround; the SECOND upgrade before 07:00 = the fixes** (GREEN chains only).
     - **S43 measured:** CONTENT_VERSION_CHANGED is keyed on the content/capability pins, not engine_version, so the second upgrade should not strand tonight's fresh engagements; its upgrade proof checks this.
     - NSG 22 source 157.211.46.94/32 = this machine's egress.

   - **UPDATE 18:5x (s12, ctx 71%) — ALL THREE GATES IN; all panes closed (`%2`, `%3`, `%4`; control 18580 200 each time):**
     - **A = GO WITH FINDINGS** 0/0/2/4.
     - **B = GO WITH FINDINGS**: API 0/0/5/1, DB 0/0/0/1. Findings: W4B-m1 urn:uuid→500; **W4B-m2** stale-pinned engagement accepts a customer approval after an upgrade, then stuck; W4B-m3 10 more credential shapes; W4B-m4 load 500/504 duplicate; CI-m1; W4B-p1; DB-p1. Report 183 lines, 0 placeholders, DKIM pass.
     - **C = NO GO** (WP5 0/3/5/4, WP6 0/1/3/4).
     - **COMBINED on 09c1591 = NO GO → NO PUSH.**
     - **Routed by ANSWER ~08:3xZ:**
       - W4B-m2 → tonight's upgrade REPORT names old engagements DO NOT USE, plus a fix-round code fix;
       - W4B-m1 → fix round;
       - W4B-m3 → the credential rebuild after C11;
       - m4/CI-m1/p1/DB-p1 → BACKLOG.
     - Kam told on the panel.
     - **NEXT after S43's fix round:** ONE delta tier-1 gate on `09c1591..<fix head>` (Q + W + fixes). Push only on GO + Tuesday's word.
     - **SCORED by s12 18:5x** (scoreboard rows at top): A/B/C 1.00 each; merge seats S41→S42 0.70. ~~OWED: score gates A/B/C (each ~1.00: controls, resumed cleanly, honest NOT-TESTED) and the builder round (S41/S42/S43 merge seat, combined NO GO on C's Majors) on `projects_index/scoreboard.md`.~~ S43's round is scored at its own verdict.

   - **UPDATE 18:4x (s12, ctx 70%):**
     - **Gate C VERDICT 08:30:21Z (DKIM pass; report 321 lines, 0 placeholders) = WP5 NO GO 0/3/5/4 · WP6 NO GO 0/1/3/4.**
       - W5-M1: a website-created engagement can never be customer-approved (approver user_id null).
       - W5-M2: release is silently blocked until 8 secret local values are defined; no issue code.
       - W6-M1: the document says "No local values are required".
       - W5-M3: S7 table 3,963 px wide at 1440.
       - Minors W5-m1..m5, W6-m1..m3.
     - **Routed by ANSWER ~08:4xZ** = FIX ROUND 2 of 2 under the cap:
       - Monday fixes (W5-M1, W5-M2+W6-M1, W5-M3, W6-m1..m3, W5-m5) go AHEAD of C11 and feedback; C11 pauses on engine files.
       - **Tonight's upgrade uses the gate's workaround** on the zero-group release engagement: approvers linked via the API, 8 local values defined via product decisions.
       - **UPGRADE RULE:** fixes merged + GREEN by 21:00 → in tonight's upgrade; otherwise a second upgrade before Monday 07:00 if GREEN.
       - The rest goes to BACKLOG.
     - **Pane `%4` closed.** Kam told on the panel.
     - **Still waiting:** gate B (`%3`), S43's fix-round PLAN mail.
     - Push waits for B + a delta gate.

   - **UPDATE 18:3x (s12, ctx 69% checkpoint):**
     - **S43 STATUS 08:26:26Z (DKIM pass): LOCAL main fast-forwarded `09c1591` → `3bc7471df46bd5844f3027c1383d6ea087463555`** (lane Q D2 + Q-A; 257 ahead of afc10e9; NOT pushed). This came after chain qd2-s43 went fully GREEN: host 1045+1 with 0 timeouts; DB 205; API-DB 428; upgrade e2e 49/49; clean-clone CI GREEN; switch-ON D1 PASS. Evidence: analysis repo 7e4b65c.
     - **Seat decisions ACCEPTED by silence** (in `HPSM/5_Project_History/seat-decisions_s43_seat-hpsm-28f5.md`):
       - D-S43-02: F-API may make ADDITIVE edits to 3 test files; guards extended, none weakened.
       - D-S43-03: the upload body limit is scoped per route; the edge limit only on the upload route, at merge.
     - **A-m1 went to BACKLOG marked 'after C11'.** Make sure it is actually commissioned after C11 merges.
     - **PUSH DECISION NOTE:** the combined gates tested `09c1591`; `09c1591..3bc7471` (lane Q) and W are UNGATED. Before any push to HPSM-light, decide between a delta tier-2 gate on Q+W and aggregating B/C + the live acceptance harness.

   - **UPDATE 18:3x (s12):**
     - **Gate A VERDICT 08:20:21Z = GO WITH FINDINGS 0/0/2/4** (report read head + mail whole; DKIM pass; placeholders 0).
       - A-m1: credential detector misses 17 syntaxes (3rd round).
       - A-m2: 5 non-equivalent mutant survivors (N63/N64/N33/N09/N26).
       - A-p1..p4.
     - **Routed in an ANSWER ~08:3xZ:**
       - N63/N64 + A-p3 → lane C11;
       - A-m1 (shape rule) + A-p2 + N33/N09/N26 → a follow-up engine lane after C11;
       - A-p1/A-p4 → BACKLOG.
     - **Pane `%2` closed** with pane_close.sh (control 18580).
     - Not yet scored. **Waiting on B (`%3`) and C (`%4`).**
   - **S43 ACK 08:20:21Z accepted:**
     - C11 on s43/lane-c11 (pc-s43-c11 23080; + packages/content + web catalogue mirror); no migration.
     - `SUPPORT_UNKNOWN_ON_DEVICES` critical (a).
     - **Live upgrade window 21:00–23:30 AEST tonight** after Q+W (latest Monday 07:00).
     - 3bc7471 checks GREEN at lower load.
     - C11 is NOT deployed before Monday (its CONTENT_HASH change would 409 the fresh engagements).
   - **The acceptance+security harness was REVISED at 18:20 on Kam's word** ("Please revise the testing harness documents so they test the live site."): LIVE site a TARGET, `LIVE DEMO RULING: APPROVED by Kam 2026-09-13 18:20`, own `QA Harness (synthetic)` tenant only, credential never printed, ≤1 req/s, stop on degradation, probes 4/6/10/14/16 local-only. `--check` rc 0, committed. **Launch after the live upgrade REPORT + gate verdicts;** name the live head in the launch prompt, and re-point the launcher HEAD/EXPECTED_COMMITS if local should match the upgraded head.

   - Launcher: `2_Project_Files/fleet/qa-agent/launchers/resume_qa_hpsm_composer_09c1591_combined.sh <A|B|C>` (`--check` passed ×3).
   - Panes and sessions:
     - `%2` `QA/HPSM-C-A`, session `12eb20ba…`. Its report was written except @@VERDICT@@ and @@MUTANT_HEADLINE@@.
     - `%3` `QA/HPSM-C-B`, session `258bef81…`.
     - `%4` `QA/HPSM-C-C`, session `8aef64cf…`.
   - Rung 5 verified from pane content: each re-derived its own state.
   - Reports: `Testing Agent MAIN/projects/hpsm/reports/2026-09-13-composer-09c1591-combined-{a-engine-content,b-api-db,c-web-renderers}-tier1/report.md`.
   - Verdicts come by mail to tuesday-agent@, subject `GATE VERDICT — Policy Composer combined gate <A|B|C> …`.
   - **NEXT on each verdict:** read report.md whole → completion check against the combined brief → score (scoreboard) → `pane_close.sh %N` → aggregate the three → the PUSH decision for `09c1591` to HPSM-light. Push only on GO + Tuesday's word; the push is executed by S43, which holds main. A NO GO follows the two-round cap rule.

3. **Kam's 17:00 commission — the HPSM ACCEPTANCE-vs-ORIGINAL-BRIEF + SECURITY tier-1 gate: WRITTEN, CHECKED, COMMITTED, NOT LAUNCHED.**
   - Brief: `2_Project_Files/fleet/qa-agent/briefs/2026-09-13_hpsm-composer-09c1591-brief-acceptance-security-tier1.md`, with its prompt `….prompt.txt` beside it.
   - Launcher: `2_Project_Files/fleet/qa-agent/launchers/launch_qa_hpsm_composer_09c1591_brief_acceptance_security.sh` (`--check` rc 0 at 17:31).
   - Two verdicts (DELIVERABLES, SECURITY). Every original brief document is cited by absolute path.
   - Stacks `policy-composer-qa-bas-on` (21480) and `-off` (21580); CI 21495.
   - **Default, told to Kam on the panel (at origin):** LAUNCH AFTER the three combined verdicts land (capacity: load average ~190 on the Mini). The live Azure demo is `LIVE DEMO RULING: VETOED by default - Tuesday, Kam has not ruled`.
   - **Only Kam's own words** switch that line to `APPROVED by Kam <YYYY-MM-DD HH:MM>` (the launcher regex accepts exactly that). Approval allows unauthenticated external probes only.
   - **Launch:** `cockpit.sh add 'QA/HPSM-ACC' "bash '<launcher>'"`, then the rung-5 check.
   - **If S43's second READY has moved main before launch:** decide between keeping `09c1591` (it matches the combined gates) and a new head (needs a new launcher head plus EXPECTED_COMMITS).

4. **Kam's open cards (unchanged by s12):**
   - `hpsm-composer-live-demo-upgrade-after-c12` — HOLD. Live stays at `c2fbc36`. **S40 has CLOSED, so no seat operates the live stacks**: an upgrade ruling needs an operator commissioned; S43 is the candidate.
   - `hpsm-composer-demo-release-with-device-groups` — HOLD.
   - `hpsm-composer-monday-review-scope` — amended by Kam's note.
   - `tuesday-seat-self-rotate-with-liveness-check` — overtaken: Kam restarted Tuesday by hand at 16:48. Leave it for Kam, or mention it once.
   - **Kam reviews HPSM on Monday 2026-09-14.**

5. **For a future NexusAI seat (not now; found by s12's Explore read, unverified line-by-line):**
   - `backend/routes/feedback.js` PATCH/DELETE have no admin-role check.
   - The widget never sends `created_by` (stored as `'anonymous'`).
   - `server.js:199` `autoCreateAIFeedback` hard-codes the dead VM URL.
   - The Feedback_System link to NexusAI is dead (RD-50).

## ⚠ INCIDENTS TODAY (measured by s12)

- **16:48:28 FLEET SESSION KILLED.**
  - The `fleet` tmux session was recreated in the second s12 booted.
  - `Launch_Cockpit.command`'s Fresh branch runs `kill-session -t fleet` (≈L116–127), behind an R/F/Q prompt and a YES confirmation when agent panes are live. Launch_Tuesday/Wednesday have no kill-session.
  - **Lost unwrapped:** S42 (`%25`) and the three gates. S40 had wrapped at 16:47 on Kam's word.
  - Who chose Fresh is NOT established.
  - Wednesday was told (coordination mail ~07:40Z).
  - **Rule: whenever Tuesday asks Kam to restart this seat, say "Resume, not Fresh" in the same sentence.**
- **panel_sync HUNG, then RACED.**
  - **The hang:** the Thursday loop (pid 91697) forked a cycle subshell (99382) that sat in state R with no children for 6 min, with no log after 17:04. After a guarded TERM both stayed in state E (unkillable; `ps -p` on them hung >120 s — likely a kernel/IO hang on the T9). **A new loop, pid 12441, started 17:27** (detached, tty ??, `WED_AGENT=tuesday`).
  - **The race:** every cycle then aborted mid-rebase ("local changes would be overwritten"), because `usage_tuesday.json` is rewritten on every statusline render and a 13-commit replay on the T9 cannot finish between writes.
  - **The fix:** `git update-index --assume-unchanged 0_Brain/dashboard/data/usage_tuesday.json` at 17:37 → one cycle went through → origin/HEAD 0/0, both of s12's panel messages verified AT ORIGIN → flag REMOVED 17:39 (`ls-files -v` shows `H`).
  - **If the abort recurs with a long local backlog, reuse that flag briefly and remove it after.** The durable fix is Wednesday's (proposal mailed).

## ✅ DONE IN s12 (verified)

- Brain whole: by-tier digest 5,437 lines (last heading asserted) + own ledger 101 rows → `ctx:31%`. Boot digests committed. WED board 27 active, 0 `lesson` (board_count.sh). `reconcile_rulings.py`: 55 taps, 0 to rule.
- S40's wrap read whole (DKIM/DMARC pass).
- Kam's two terminal instructions (16:55, 17:00) are in the prompt log. The first entry's swapped arguments were corrected and the correction noted.
- Ledger row: three s12 slips (zsh unsplit git variable read as NO; prompt_log arguments swapped; own dirt held the sync one cycle).
- Panel to Kam at origin: the receipt + 16:48 explanation + plan, and the testing-brief summary + defaults.

## ⚠ NEW TRAPS (s12) — older traps 1–39 are in `.pre-1740`

40. **Cockpit Fresh kills EVERY agent pane.** See the incident above.
41. **`usage_tuesday.json` churn vs panel_sync rebase.** See the incident above.
42. **zsh does not word-split a variable holding a command.** `G="git -C x"; $G log` fails, and an `&& yes || no` then prints "no". Write paths literally; branch on the exact rc.
43. **`prompt_log.sh <channel> <text> [note]`.** Read a tool's usage in a separate action before the first call.
45. **`reconcile_rulings.py` is Wednesday-scoped by construction.**
    - **Where:** line 43, "This seat coordinates Secuura + Wednesday's own work".
    - **What happens:** it SKIPS every Datasec card as "OUT OF SCOPE", even with `WED_AGENT=tuesday`.
    - **Instead:** record Kam's Datasec taps with `WED_AGENT=tuesday decision_queue.sh rule <id> <choice>`, gated in code on `git merge-base --is-ancestor <ls-remote origin sha> HEAD`.
    - **When the gate refuses** (origin just moved): wait for panel_sync's pull. Never run a plain fetch.
46. **A mail watcher's MARK is one second past the newest mail already PROCESSED, never the arming time.**
    - Kam's card taps arrive as `[Kam -> Tuesday] panel message …` (label `sent`), so a watcher regex must match `Kam` too.
    - **Measured 18:1x:** the shared wake runner's own unsent tap line at %0 made it HOLD every later tap. Clear it only by matching its exact `[wake_watch]` text; C-u did not clear it mid-turn, but it submitted at turn end.
44. **Resuming a killed QA gate:** `claude --resume <session>` with `CLAUDE_CONFIG_DIR=TUESDAY/4_Credentials/.claude` and the project's identity dirs. Map a session to its gate by counting mentions of its report dir / compose project in the transcript. The first-prompt heuristic is unreliable, because every gate prompt names A, B and C.
