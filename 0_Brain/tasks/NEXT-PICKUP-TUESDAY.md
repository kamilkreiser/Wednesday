---
date: 2026-09-13
type: pickup
scope: DATASEC ONLY — Tuesday, on Kamils-Mac-mini (T9 drive). Secuura and general are Wednesday's, on the Studio.
source: drafted for Tuesday s13 by a subagent, REVIEWED AND AMENDED by s13 at 20:32 (S44 state to 10:30Z, watcher MARK, panel-note verification, Monday-list item). Built from s12's pickup plus its s13 blocks, `NEXT-PICKUP-TUESDAY.md.pre-1740` (traps, WITH KAM, OWED), the 2026-09-13 rows of `_ledger_laptop_datasec.md`, the four `briefs_staged/2026-09-13_hpsm-s44-*.md` mails, HANDOVER-S43 S1 plus addendum 1, and Kam's lines extracted from transcripts b511be06 (s12) and 886e95a5 (s13).
status: live
supersede: replace WHOLESALE at the next pickup; never append.
---

# NEXT PICKUP — Tuesday s14 (written by s13)

**BLUF.** **One decision waits on Kam: go or hold on live gate fix "b-tight".** Until he answers, the public demo URL is unusable past sign-in.
- **S44 (pane `%7`) is merging the fix round** toward one rolling upgrade. S43 and every QA pane are CLOSED; the acceptance+security gate is scored and routed.
- **Tuesday s14 first:** the rotation checks, then the transcript diff (below), then the unfiltered inbox.

## ON EVERY WAKE
- Run `2_Project_Files/tools/kam_rulings_today.sh`, **never `kam_msgs.sh` unfiltered** (it prints Wednesday's tab); check `[Kam -> Tuesday]` mails; list `tuesday-agent@` UNFILTERED and route on SUBJECT.
- Run `git status --porcelain | grep -v 0_Brain/dashboard/data/`. Rotation band is 80–90.
- **Verify every panel message AT ORIGIN:** `git show origin/main:0_Brain/dashboard/data/chat_tuesday.json`.
- **Do NOT read `0_Brain/daily/`** (Wednesday's). **Kam types straight into this terminal; those lines are first-party.**
- **Kam sees Tuesday's panel replies ONLY on the orange TUESDAY tab** (`chat.html:190` `inView`, `cockpit.html:367` `msgInView`). Which tab he uses is UNMEASURED, so say where the reply is.
- **When Kam asks something in the terminal, Tuesday answers in the terminal, with the literal yes or no as the first word.** The panel copy is secondary.

## SUCCESSOR FIRST ACTIONS (Tuesday s14, in order)
1. **(a)** Read `2_Project_Files/fleet/cockpit/logs/rotate_wednesday.log` for `respawned OK` and `LIVENESS OK`. Then check that `%7` (S44) and `%1` (monitor) survived.
2. **(b)** `tmux set -p -t %0 @cockpit_name wednesday`. The pane is renamed `tuesday` only for the rotation, and `arm_wake_watch` taps match the hardcoded name.
3. **(c) NEW RULE (ledger w=4):** before the first report to Kam, extract every human-origin line from the PREDECESSOR's transcript and diff it against this pickup.
   - Transcript: `/Volumes/KK_T9_External_HDD/TUESDAY/4_Credentials/.claude/projects/-Volumes-KK-T9-External-HDD-TUESDAY/886e95a5-f138-4e94-b819-4a03523bfe14.jsonl` (s13).
   - Keep records `type: user` with text content (skip tool results, `<task-notification>` and `[wake_watch]` lines) and `queue-operation` with `operation: enqueue`, from this pickup's commit time onward. Print them in AEST.
   - An `enqueue` followed by a `remove` with no assistant turn that mentions the line is the drop signature.
   - **Why:** at 19:01:39 a Kam instruction was dropped across s12's rotation exactly this way. s13 then told Kam everything had carried over, on panel and mail evidence alone.
   - s13's human lines up to 20:23 were 19:10:08 and 19:21:13, and both were answered.
4. **(d)** Re-arm the exiting watcher, detached:
   - command: `2_Project_Files/fleet/cockpit/watch_tuesday_exiting.sh <MARK> 23:55 39799`;
   - MARK = one second past the newest mail s13 PROCESSED. At the s13 review (20:3x) that was S44's QUESTION 10:28:41Z, so `2026-09-13T10:28:42`. **If s13 processed later mail, the pickup's newest s13 line says so; take the MARK from there.**
5. **(e)** Then the normal boot: brain, the board (`2_Project_Files/fleet/board_count.sh`), the inbox, and a short panel note to Kam, verified at origin.

## ROTATION PROCEDURE (this seat)
- **Why it is needed:** `wednesday_rotate.sh --self` finds the coordinator pane by `@cockpit_name == $SEAT` (`tuesday`), but `%0` is named `wednesday`. Without the rename `--self` refuses (rc 2), `--dead` refuses too, and a dead Tuesday seat cannot auto-respawn. **Never let this seat reach 90%.**
- **Only when no live upgrade or gate apply is in progress.** A fleet-session loss would kill S44 mid-deploy.
  1. Re-read OWN transcript for human input received after this pickup was written, and relay it or add it here (ledger w=4, rule b).
  2. Check the pickup is committed, HEAD is in origin (the script gates on `merge-base --is-ancestor HEAD origin/main`), and the tree is clean.
  3. `tmux set -p -t %0 @cockpit_name tuesday`
  4. `WED_AGENT=tuesday nohup bash 2_Project_Files/fleet/cockpit/wednesday_rotate.sh --self > /dev/null 2>&1 &` (log `logs/rotate_wednesday.log`). `WED_AGENT=tuesday` resolves `Launch_Tuesday.command` (fixed `313325e7b`).
  5. The successor renames `%0` back to `wednesday` (first action b).
- **Wednesday's seat-name resolver fix is BUILT and STAGED, NOT installed** (COORDINATION 10:40:21Z, DKIM pass, read whole):
  - Location: `2_Project_Files/fleet/cockpit/staged/resolver-20260913/` at origin `59ec89ddf`.
  - Contents: a new `seat_resolve.sh` plus patched `wednesday_rotate.sh`, `wake_watch.sh` and `arm_wake_watch.sh`, with `DIFF.md` and `resolver_test.sh`/.out (22 PASS, including seat=tuesday + pane `wednesday` found through the legacy fallback, and the DEAD line carrying `WED_AGENT`).
  - **Installing it on the mini is Tuesday's call. s13 did NOT install it tonight:** the install means stopping the running `wake_watch.sh` loop, copying the four files together and re-arming, at a boundary with no seat mid-turn, and S44 is live mid-merge. Install at a quiet boundary; `seat_resolve.sh` must sit beside the three.
  - **The second half, not built (Wednesday claims it):** `cockpit.conf`/`cockpit.sh up`, `apply_layout` (:90), `rotate` (:389) and `Launch_Cockpit.command:104` all hold the literal `wednesday`.
  - **The live rotate already renames the pane to `$SEAT` after a respawn (line 151)**, which is why the successor must rename `%0` back to `wednesday`.
  - **Until both halves are installed, the rename workaround above stands.**

## KAM'S WORDS TODAY (verbatim, AEST; T = terminal transcript, P = panel)
- **09:17:37 P (tuesday view), standing rule:** *"this is a new standing rule for all projects - please spin up as many agents as possible to complete the task as long as multiple agents do not create a problem with development through multiple agents working on the same code base."*
- **16:53:31 T** (the prompt log says 16:55): *"Please get the HPSM agent to identify what else is left to complete and whether there are any issues with the product.   Also get the agent to add the feedback feature as deployed in Nexus AI to the HPSM project. Naturally change all settings so that any feedback is registered against HPSM and works properly."*
- **16:54:18 T** (prompt log 17:00): the acceptance+security harness commission, *"…test the platform from a security perspective as well as from a deliverables perspective against the original brief…"*
- **17:48:22 T, standing:** *"tell me when the HPSM agent finishes and where the testing briefs are located"*
- **18:02:05 / 18:02:28 P, card rulings:** `hpsm-composer-live-demo-upgrade-after-c12` → `upgrade-fresh-with-release` (DELIVERED 19:00:48); `hpsm-composer-demo-release-with-device-groups` → `build-c11`.
- **18:18:03 T** (the prompt log and the harness's APPROVED line say 18:20): *"Please revise the testing harness documents so they test the live site."*
- **18:37:52 T:** *"Keep going and finish what you can.  no matter the time.  keep going until completion"*
- **18:51:31 T:** *"If you don't need to wait until 2100, don't wait. Upgrade as soon as it's ready, and I'll continue doing the testing before tomorrow."*
- **19:01:39 T** (queued into s12, dropped at 19:04:11): *"In the HPSM sign-in page, each of the sign-in options needs a much better description of what the options mean. Make this description in gray with a much smaller text at the bottom. Of each tile."*
- **19:10:08 T (s13):** *"Did you get my instructions from the last boot?"*
- **19:21:13 T (s13):** *"I didn't see your response to my question whether you got the instruction before we booted and whether the agent has been advised."* (He re-quoted the 19:01 instruction after it.)
- Questions s12 answered: 18:13:30 (live site link for the harness), 18:49:22 (where HPSM is at), 18:52:15 (harness updated for the live site?).
- Times come from the transcripts. Where s12's pickup or the prompt log differ (18:5x, 18:38, 18:52, 19:14), the transcript time is used.

## 🔴 22:24 — S44 AT 82% (band 80-90): CHECKPOINT SENT; S45 SUCCESSOR OWED after S44's wrap
- **S44 statusline ctx:82% at 22:22**, mid step-8 live upgrade (3 shells running). **CHECKPOINT mail sent 12:23:36Z, verified at the sent copy** (`briefs_staged/2026-09-13_hpsm-s44-checkpoint-82.md`): safe boundary = AFTER the step-8 REPORT (never mid-deploy) → `5_Project_History/HANDOVER-S44_seat-hpsm-375c.md` + wrap to tuesday-agent@ → stay at prompt; no step 9-10 merge, no new lane; successor section lists live heads, lanes (C11 HOLD, C11-PINS), shells/subagents, queue, toolkit base arg (D-S44-30), and every Tuesday ANSWER timestamp (09:56:56Z … 12:20:03Z).
- **Routing row `Datasec/HPSM-S45|datasec-hpsm@agentmail.to|yes` ADDED** (trap 38).
- **ON S44's WRAP MAIL (the sequence, never `cockpit.sh rotate`, trap 37):**
  1. read HANDOVER-S44 whole;
  2. `ps` census for `claude .*project 'HPSM'` across all terminals (trap 32);
  3. draft the S45 brief by a subagent from `briefs_staged/2026-09-13_hpsm-s44-successor-merge-seat.md` + HANDOVER-S44; review it, then `send_brief.sh --kind brief`; verify at the destination;
  4. `cockpit.sh add 'Datasec/HPSM-S45' "bash '/Volumes/KK_T9_External_HDD/!CODING/Datasec/HPSM/Launch_Claude.command'"` (confirm the launch form S44 used first);
  5. rung 5, excluding every pre-existing HPSM session id; its first user record must come after launch; match "session 45";
  6. answer S45's plan confirmation;
  7. `pane_close.sh %7` only after S45 CONFIRMS.
- Tuesday ctx 58% at 22:23 (checkpoint band for this seat is 70; rotation 80-90 — **do not rotate while S44→S45 is in flight or a live upgrade is running**).

## 🟠 22:21 — LIVE-DELTA QA VERDICT SCORED 1.00; STEP-8 LIVE UPGRADE to `9b8ea76` from ~12:24:22Z
- **QA VERDICT 12:17:51Z (DKIM pass; report 230 lines read whole): DELIVERABLES (LIVE) GO WITH FINDINGS · SECURITY (LIVE) GO WITH FINDINGS.** D-B1 RESOLVED (measured live, disclosure controls); full walk-through to release 1.0.0 in `QA Harness (synthetic) 2026-09-13 11:40` = `9cffd104…` (B = `59878bd4…`), left in place; W5-M1 CLOSED, W5-M2 + W6-M1 resolved; D-M1/D-M2 still present; W4B-m3, W4B-m1 (urn 500, FX-ID closes at step 8), S-m1, S-m2, S-p1 unchanged; **NEW S-p2 Polish** (trailing `/api/…%5c` reaches the API 404, not Basic; no disclosure). NOT TESTED: no browser (FX-SI/FX-REL/W5-M3 not rendered), probe-12 negative half, W4B-m2, the local half at the newer head. **Scored 1.00 on the scoreboard** (committed). Pane `%8` CLOSED (listeners 14 → 14).
- **Kam told 22:19:39** (result, the two Majors queued, no browser so he checks the visuals himself, QA Harness tenants on live, report folder named). Origin verify running. **Kam's 17:48 ask ("where the testing briefs are located") answered for this gate.**
- **S44 NOTICE sent 12:20:03Z, VERIFIED at the sent copy** (`briefs_staged/2026-09-13_hpsm-s44-notice-live-delta-verdict.md`): confirmations, still-present list, **S-p2 → BACKLOG beside S-m1/S-m2 under the durable gate redesign (no live Caddy change without Kam)**, and the local half owed as ONE delta tier-1 gate after READY FOR QA.
- **S44 HEAD 12:19:03Z (DKIM pass, read whole): upgrade to `9b8ea76` (S-m3 + FX-PIN/Q1 + FX-ID) from ~12:24:22Z**, base/rollback **87c0026**; **PINS UNCHANGED**, both prechecks NO STOP; my ACCEPT conditions applied. **S44 caught its own toolkit hard-coding caf63fd as base AND rollback** (a failure would have rolled live back past tonight's fixes); base is now a required argument with controls (D-S44-30). **Kam WARNED on the panel ~22:21** (restart window; DO NOT USE engagements now show a red Conflict banner = W4B-m2 fixed; A/B unchanged).
- **ON THE REPORT:** panel note (public check named public; tunnel named tunnel); W4B-m1 closure (urn → 404) if the post-check shows it.
- **Watcher MARK now `2026-09-13T12:19:04`.**

## 🟡 22:00 — CHECKPOINT (Tuesday ctx 51%; band 80-90) · C11 FINISHED GREEN and HELD off main
- **S44 QUESTION 11:57:37Z (DKIM pass, read whole):** C11 GREEN at `s44/lane-c11 bfce726` (one-group synthetic release reachable; SUPPORT_UNKNOWN_ON_DEVICES critical; demo CONTENT_HASH fd7db6b8… → **2971ffc4…**; release-draft unchanged). Merging now would make every later upgrade a content-hash STOP and stale-pin A/B.
- **Tuesday ANSWER sent 11:59:52Z, VERIFIED at the sent copy** (`briefs_staged/2026-09-13_hpsm-s44-answer-c11-hold.md`): **HOLD** (S44's default) until steps 7-10 are merged AND upgraded live; then C11 as its own batch + head mail + **STOP for Kam** (fresh engagements only on his word). At that merge: re-run merge-tree onto main as it stands then, C11/FX-PIN-Q1 overlap result in the head mail. Seat pins at merge accepted.
- **Card `hpsm-composer-demo-release-with-device-groups` marked DELIVERED 22:00** against `s44/lane-c11 bfce726` (store write gated on origin-ancestor rc 0; `decisions.json` parses locally; origin verify running).
- **Kam told on the panel ~22:01** (C11 built, held, stops for his word). Origin verify running.
- **Carry for Kam (only if C11 goes live before his review):** on REAL content every device-group engagement shows 55 extra critical SUPPORT_UNKNOWN_ON_DEVICES and its manifest hash changes on next Generate (by design). With HOLD it is not a Monday item.
- **Checkpoint rules:** start nothing heavy; the handover is this block. Waiting on: the live-delta QA verdict (`%8`, transcript b1a0f847); FX-PIN-Q1's web 409 check; S44's next head mail.
- **S44 STATUS 12:01:00Z (DKIM pass, read whole):** FX-PIN-Q1 GREEN `c1d47df` (Q1 createDraft refuses a stale pin; RED 2/21 → GREEN 21/21; 4 mutants). **Consequence 2 MET: web 409 check 13/13 PASS, 0 SILENT** (real Chromium, 5 stale-pinned engagements, scorer positive-controlled, snapshots unchanged). **Step 7 merging onto a4172b3 (chain m8).** S44's line "C11 answer still open" CROSSED Tuesday's 11:59:52Z ANSWER (same outcome: HOLD) — no chase.
- **F1 (predates FX-PIN; BACKLOG; MONDAY-VISIBLE):** no web screen can create the next draft of a released engagement (no web call to `POST /engagements/{id}/draft`); S8 says "Create the next draft from the engagement details" (`Validation.tsx:121-128`) but that screen offers only "Clone to new engagement" (`EngagementDetails.tsx:374-388`) — S44's citations, not re-read by Tuesday. **→ Kam's Monday list (5a).** BACKLOG smalls: S5/S7/S10 alert below a 1280x900 viewport with no focus move; generic "Conflict" title; S9 MANIFEST_CHANGED reload may hide its warning (UNVERIFIED, code-read); no manual-decision UI.
- **S44 STATUS 12:11:00Z (DKIM pass, read whole):** step 7 GREEN → LOCAL main `246fb92` (a4172b3 + FX-PIN d82ca16 + Q1 c1d47df; CI GREEN, switch-ON 80/80 zero-failure), NOT pushed, NOT live. Step 8 FX-ID merged in worktree as `9b8ea76`, chain m9-s44 (~12:23Z). Steps 9-10 prepared (edge route-table row `/api/feedback` 401 problem+json + a wrong-on-purpose nginx-404 control).
- **Tuesday ANSWER 12:12:15Z VERIFIED at the sent copy** (`briefs_staged/2026-09-13_hpsm-s44-answer-roll-step8.md`): **roll both stacks to the m9 head when GREEN** (Kam 18:51 "Upgrade as soon as it's ready"); conditions: any pin change at pre-check = STOP for Tuesday; post-check stays on A/B, never the QA Harness tenants; REPORT carries Azure down/up times + new head. **→ Expect a HEAD mail ~12:25Z: warn Kam on the panel (site restarts; the DO NOT USE stale engagements become read-only = W4B-m2 fixed).**
- **Live-delta QA (`%8`, b1a0f847) finished its LIVE pass on ONE head** (START 11:29Z → END 12:11Z, bundle index-GroKuQ3K.js, api 0.13.2, 0 wrong-credential attempts, ~25 edge paths) and is WRITING its report (22:12). The step-8 upgrade lands after its END reading, so its verdict does not split by head.
- **Watcher MARK now `2026-09-13T12:11:01`.** Ledger row filed 21:5x: ad-hoc freshness reader printed the other tab (w=2).

## ✅ 21:27 — LIVE UPGRADE DONE: both stacks on `87c0026` (S44 REPORT 11:25:29Z, DKIM pass, read whole); live-delta QA LAUNCHED
- **pc-lane-a** 11:22:33-48Z, **Azure** 11:23:13Z-11:24:05Z; rollback not needed. postcheck-ab FULL PASS 20/0/1 on both (Azure's **through the tunnel**). **`browser-gate-public.sh` PUBLIC PASS** (sign-in, /api/dashboard 200, stayed signed in, engagement 200); `public-gate-probes.sh` PUBLIC 26/26. Caddy fingerprint 61f519cd + start time UNCHANGED.
- **Use (unchanged):** Azure A `3bb6fcb2` / B `a9101d3f` (version b03aae4b); pc-lane-a A `e920ac1d` / B `8ce21d2a`. **Avoid:** Azure `c9bce98b`, `1ec31037`; pc-lane-a the 9 in S43's record. **New on A:** LOCAL_VALUE_NOT_DEFINED critical x7 (FX-LV naming what A never had; expected). A's preview no longer says "No local values are required" (FX-R live).
- **Kam told on the panel 21:26:31** (back up, public check named public, tunnel named tunnel, A's 7 criticals expected, avoid list, re-test starting); origin verify running. **Kam's 19:01 sign-in-descriptions instruction is now LIVE (FX-SI in 87c0026) → DELIVERED.**
- **Live-delta QA launched 21:27:01 in pane `%8` `QA/HPSM-live-delta`** from the committed launcher re-pointed to `LIVE_HEAD=87c0026…`, `EXPECTED_COMMITS=308` (`--check` rc 0). Report dir `Testing Agent MAIN/projects/hpsm/reports/2026-09-13-composer-87c0026-live-delta-after-gate-fix-tier1/`. Verdict mail subject `… LIVE delta after gate fix @ 87c0026 (tier 1)`. **RUNG 5 PROVEN:** transcript `b1a0f847-c50c-4ecf-a061-3d63a89401de` (first user record 21:27:02, after launch; carries the brief path; 22 pre-launch ids excluded) under `TUESDAY/4_Credentials/.claude/projects/-Volumes-KK-T9-External-HDD--CODING-Testing-Agent-MAIN/`. Resume if killed: `claude --resume b1a0f847-…` with that CLAUDE_CONFIG_DIR (trap 44). **Score at its verdict.**
- **S44 NEXT:** step 7 FX-PIN d82ca16 + Q1 seat commit → required web 409 browser check (S2/S4/S5 saves, S9 approve); step 8 FX-ID b57cf09 GREEN waiting; F-API + F-WEB; C11 running (STOPs for Tuesday on its content-hash change). Each GREEN batch gets its own head mail. **S44 ctx 65% at 21:19** (checkpoint only; band 80-90).
- **S44 STATUS 11:28:25Z (DKIM pass, read whole, no question):** Azure migrate verified read-only (15 applied, running archive composer-87c0026); tunnel 23990 CLOSED. **FX-ID FINISHED GREEN `b57cf09`** (55 id inputs / 47 ops → byte-identical 404; BACKLOG: trailing `%0A` id finds the real row on 3 routes). **Step 7 lane FX-PIN-Q1** on `s44/fx-pin-q1` (87c0026 + d82ca16, stack 24780): Q1 createDraft 409 RED-first; **REQUIRED web 409 browser check** scores every refused screen action PASS/SILENT — **a SILENT holds any upgrade carrying FX-PIN.** Dry-run merge-tree onto 87c0026 clean for FX-PIN, FX-ID, S-m3, f-web-b. **Same-file note:** FX-PIN-Q1's createDraft edit and C11's capability-pin change share a file (S44: different blocks); C11's edit is not yet written, so that pair is UNMEASURED — a conflict at merge is the partition's failure, reported. Order: 7 FX-PIN → 8 FX-ID → 9 F-API → 10 F-WEB → S-m3 → 11 C11 (STOP) → 12 credential round; D-M1/D-M2 per engine queue.
- **S44 STATUS 11:38:10Z (DKIM pass, read whole):** S-m3 MERGED GREEN → LOCAL main `a4172b3` (87c0026 + 1e62816, `apps/api/src/secrets.ts` only; CI GREEN, switch-ON 80/80 zero-failure), NOT pushed, NOT live (stacks stay 87c0026). **Order swap accepted by silence** (S-m3 ahead of feedback; no shared path with steps 7-10; merge-tree clean in every order). FX-ID `b57cf09` HELD until FX-PIN is on main (it is built on d82ca16). Lanes: FX-PIN-Q1 `c45702a` (24780), C11 (24380). S44 idle-acked 21:33 (hash 4c6aef38) while waiting on its agents.
- **Watcher MARK now `2026-09-13T11:38:11`.** Tuesday ctx 47% at 21:28 (checkpoint only).

## 🟠 21:18 — S44 HEAD MAIL 11:16:52Z (DKIM pass, read whole): LIVE UPGRADE to `87c0026` from ~11:22Z, pc-lane-a then Azure
- **Target** `87c0026d94e8e13c14329852239d35a463168503` = LOCAL main, 41 commits after caf63fd: FX-M1, FX-R, FX-S7, FX-SI+proof, picker, **FX-LV+FX-REL (merge 6 GREEN 11:15:59Z)**. Rollback caf63fd on both. NOT pushed. NOT in it: FX-PIN, FX-ID, S-m3, feedback, C11.
- **PIN ANSWER: pins UNCHANGED** (content hashes identical, capability sources unchanged) → A/B stay usable. Both prechecks NO STOP. No fresh engagements, no az write, gate b-tight unchanged. **No STOP condition → no HOLD sent.**
- **Kam WARNED on the panel 21:18:01** (restart window, A/B usable, what he will see: grey sign-in descriptions, narrower S7 with "Show full value", S10 release confirmation stays). Origin verify running.
- Post-check per S44: pc-lane-a postcheck-ab FULL + B's PDF; Azure smoke + postcheck-ab FULL **through the tunnel (label it tunnelled to Kam, trap 49)** + `browser-gate-public.sh` (the PUBLIC check that must PASS). REPORT carries use/avoid lists, A's validate codes, B's release record, "No local values are required" check.
- **ON THE REPORT:** panel note to Kam (public check result named as public; tunnel as tunnel); mark Kam's 19:01 sign-in relay delivered (live); re-point live-delta launcher `LIVE_HEAD=87c0026…` + `EXPECTED_COMMITS` (count below), `--check`, commit, `cockpit.sh add`, rung 5.
- S-m3 FINISHED GREEN `1e62816` (cap 64; S44 ruled its own brief's "depth 1,000" was its error, D-S44-19). **C11 LAUNCHING on 87c0026 (stack 24380): its content-hash change STOPS for Tuesday → card/panel question to Kam before any upgrade carries it; on C11 READY mark `hpsm-composer-demo-release-with-device-groups` --delivered.**
- **Watcher MARK now `2026-09-13T11:16:53`** (harness background task, deadline 23:55, pid 39799).

## 🟢 21:12 — s14 UP (Tuesday s14, session db070750; rotated in 21:00:10, LIVENESS OK 2/2)
- **Boot checks done:** `%0` renamed back to `wednesday` (rc 0, verified); transcript diff of s13 `886e95a5` from the pickup draft onward = 20:44:13 GO + 20:45:20 email line only, both in this pickup; nothing after the 20:57 commit. **No drop.**
- Brain: by-tier digest 5437 lines read to the last line; own ledger 110 lines whole; ctx 27% after load. Digests regenerated by the launcher committed + pushed (they had panel_sync on SKIP at 21:01).
- Linear `lesson` open = 0 (`board_count.sh`, real count). Kam's rulings: nothing after 18:02.
- **Panel note 21:04:36 VERIFIED AT ORIGIN** (rotation, no drop, gate holding, A/B, upgrade warning to come; default: NO harness email unless Kam asks).
- **S44 STATUS 11:06:17Z (DKIM pass, read whole):** steps 1-5 GREEN, LOCAL main `7dbf83f` (switch-ON 76/76 zero-failure), NOT pushed. 30-min FX-LV+FX-REL clock to ~11:35Z; head mail ~11:30Z on whichever head is GREEN; then ~5 min, pc-lane-a, Azure. Prechecks NO STOP at 7dbf83f, no pin changes. Lanes: FX-REL RED/GREEN committed; S-m3 cap 64 vs brief's "depth 1,000" (S44 judges at its final report; the gate line "50 accepted, 10,000 refused" is met); FX-ID RED committed. **Nothing answered — no question.**
- **Step-5 sign-in text CHECKED at `7dbf83f`** (`apps/web/src/screens/signInDescriptions.ts` vs `apps/api/src/authz.ts` TENANT_/PLATFORM_PERMISSIONS, read-only git show): all 7 role descriptions consistent; bridge_operator says the Bridge is a placeholder. NOT read: `lifecycle.ts`, `scopeToOwnEngagement` (the "once approved" / "own engagements" clauses rest on the file's comments). Kam's 19:01 relay: mark delivered at the upgrade REPORT, when it is live.
- **Watcher:** `watch_tuesday_exiting.sh 2026-09-13T11:06:18 23:55 39799` (harness background task; re-arm from the newest PROCESSED mail).
- **Live-delta QA: INSTALLED + COMMITTED, NOT LAUNCHED.** `2_Project_Files/fleet/qa-agent/launchers/launch_qa_hpsm_composer_live_delta_after_gate_fix.sh` + `briefs/2026-09-13_hpsm-composer-live-delta-after-gate-fix-tier1.{md,prompt.txt}`; `--check` rc 0 at caf63fd. Brief amended: the local half covers caf63fd ONLY (newer head's local half = the separate delta gate, NOT TESTED here). **At the upgrade REPORT:** edit `LIVE_HEAD` + `EXPECTED_COMMITS` at the top of the launcher (7dbf83f = 301 commits from base afc10e98, measured by the drafting subagent; re-count for the actual head), `--check`, commit, then `cockpit.sh add 'QA/HPSM-live-delta' "bash '<launcher>'"` + rung 5 (trap 47). The prompt carries @LIVE_HEAD@ placeholders the launcher renders.

## 🔄 20:57 — s13 ROTATING at ctx 80% (band), BEFORE S44's upgrade window
- **Rule-b check done:** s13's transcript since 10:25Z holds only Kam's 20:44:13 GO line and his 20:45:20 "Send me the email with the content…". Both are handled and recorded below. **The successor's first action (c) diffs s13's transcript `886e95a5-f138-4e94-b819-4a03523bfe14.jsonl` from this commit's time onward.**
- **S44 STATUS 10:52:50Z:** merge 4 FX-S7 GREEN, LOCAL main `693a5db` (switch-ON 71/71 zero-failure), NOT pushed. Step 5 merged as `7dbf83f`, chain m5-s44 running. **PIN ANSWER at 7dbf83f: NO STOP; nothing the stale check reads changes vs live caf63fd, so A/B stay usable.** Both gate backups are identical pre-fix files (sha 27eb0e26); live Caddyfile sha 61f519cd (b-tight). Records at analysis 09760b4 (D-S44-17 = its probe miss).
- **NEXT expected mails:** step 5 GREEN → the 30-min FX-LV+FX-REL clock → the upgrade HEAD mail (warn Kam; the head mail carries the pin line) → REPORT (panel note to Kam; engagements; the public browser check should now PASS).
- **Live-delta QA brief:** a subagent was drafting it into `/private/tmp/claude-501/-Volumes-KK-T9-External-HDD-TUESDAY/886e95a5-f138-4e94-b819-4a03523bfe14/scratchpad/qa-live-delta/` (three files: brief .md, .prompt.txt, `launch_qa_hpsm_composer_live_delta_after_gate_fix.sh`). **At rotation the folder did NOT exist yet, so the rotation probably killed the draft.** The successor checks all three exist, the launcher passes `bash -n`, and the brief is complete. **If not, re-draft from the original** `2_Project_Files/fleet/qa-agent/briefs/2026-09-13_hpsm-composer-09c1591-brief-acceptance-security-tier1.md` + `launchers/launch_qa_hpsm_composer_09c1591_brief_acceptance_security.sh`:
  - scope LIVE ONLY: verify b-tight row by row; the walk-through in its own "QA Harness (synthetic)" tenant; probes 1,2,3,5,7,9,11,12,13, 15-auth, 17-second-control; re-check D-M1/D-M2/S-m1/S-m2/S-p1;
  - credentials BY PATH: `/Volumes/KK_T9_External_HDD/!CODING/Datasec/HPSM/4_Credentials/hpsm-demo-site.txt` + `gate-check-public.env`, never values;
  - never Kam's tenant; ≥1.1 s pacing; ≤3 wrong credentials; head variables re-pointed.
  - **Launch ONLY after the upgrade REPORT:** copy into `2_Project_Files/fleet/qa-agent/`, commit, `--check`, `cockpit.sh add 'QA/HPSM-LIVE' "bash '<launcher>'"`, rung 5 (trap 47).
- **Panel notes VERIFIED AT ORIGIN since the draft:** credentials answer 20:46:25, gate warning 20:46:48, hiccup 20:50:44, "you can use the live site now" 20:52:41.
- **Watcher at rotation:** `watch_tuesday_exiting.sh 2026-09-13T10:52:51 23:55 39799` (dies with this seat; re-arm from the newest processed mail).

## ✅ 20:50 — LIVE GATE FIX b-tight APPLIED AND HOLDING since 10:49:58Z (S44 REPORT 10:51:00Z, DKIM pass, read whole)
- **Public URL checks:** `browser-gate-check.mjs` PASS (sign-in, /api/dashboard 200, stayed signed in, one engagement opened); curl set 26/26 as expected with no credentials (everything 401 Basic except /api/dashboard and /api/tenants 401 Bearer; /api/healthz/ 404); smoke OK. Live Composer unchanged at caf63fd.
- **Rollback source:** `/opt/hpsm/Caddyfile.pre-s43-20260913T104751Z` (the original; S44 confirming both backup hashes in its next STATUS).
- **S44 OWN MISS:** the first apply 10:47:52Z worked, but its probe script mis-scored every row (`grep -c … || echo 0` gives "0\n0"), so it ROLLED BACK at 10:48:06Z per procedure. The instrument was fixed and proven against the rolled-back live gate (3 FAIL exactly on the rows b-tight changes), then re-applied under the same GO. The public browser check ran without the docker lock (a stated exception). **Score this at the round's verdict** (the procedure worked; the instrument was not proven before it was armed).
- **Kam told on the panel ~20:52:** use A/B, avoid the old engagements, known issues (release confirmation flash; discovery not required).
- **NEXT:**
  - (1) The live-half re-run of the acceptance gate is being DRAFTED by a subagent into the s13 scratchpad (`qa-live-delta/`). **Launch it only AFTER S44's step-6 upgrade REPORT** (that upgrade restarts the site and changes the live head). Re-point its head to the upgraded head, copy it into `2_Project_Files/fleet/qa-agent/`, commit, `--check`, then `cockpit.sh add 'QA/HPSM-LIVE'` + rung 5 (trap 47).
  - (2) S44's upgrade head mail → warn Kam.
- Kam's open question (should the harness document be emailed to his Datasec address?) is still unanswered.

## 🟢 20:4x — KAM GAVE GO ON b-tight (terminal, verbatim): *"You have my go-ahead on the live side fix and make sure that you include the credentials in the testing document harness."*
- **KAM mail to S44 sent 10:45:04Z** (`briefs_staged/2026-09-13_hpsm-s44-kam-go-gate-b-tight.md`; tap `--mail` verified, prompt clear). Gate apply goes FIRST, ahead of step 6; head mail, then apply, public-URL browser check + curl set + smoke, report; rollback first on any failure. Panel receipt to Kam ~20:45. Prompt-logged.
- **NEXT:** S44 head mail → short panel warning to Kam → REPORT → panel note "you can sign in; use Azure A 3bb6fcb2 / B a9101d3f" (verify at origin) → commission the live-half re-run of the acceptance gate.
- **Credentials half (measured read-only):** the harness brief `qa-agent/briefs/2026-09-13_hpsm-composer-09c1591-brief-acceptance-security-tier1.md` §1 L35 already names `/Volumes/KK_T9_External_HDD/!CODING/Datasec/HPSM/4_Credentials/hpsm-demo-site.txt` (mode 600, read into memory only), and §4 "Credentials (pointer only)" names the idp-mock personas. HPSM `.gitignore:8` ignores `4_Credentials/`. The tester HAD the credentials; D-B1 was the header collision.
- **Kam then (terminal): *"Send me the email with the content, and I will send it to the agent that you identify in the email."*** s13 answered: no email is needed and the password is never mailed (the workspace rule "never put secrets in mail"). **Asked ONE question:** does he want the harness document (which names the credential file, not the password) emailed to his Datasec address? **If he says yes: send it to `kamil.kreiser@datasec.com.au` (pinned memory), attaching the brief with NO credential value, and name the agent as the QA agent running the live-half re-run.**
- **The re-run brief (after the gate fix) carries the same pointer:** the credential file by absolute path, plus the idp personas; values never in a tracked file.

## 🔴 WAITING ON KAM — ONE DECISION: go or hold on live gate fix "b-tight"
- **Asked** on the panel at 19:24:59 and 19:39:17 (both VERIFIED AT ORIGIN) and in the terminal. **No answer as of 20:32.**
- **The problem:** through the public URL, Caddy Basic and the app's bearer both need the `Authorization` header. Sign-in works, then every `/api` call gets 401 ("Your session ended"). The gate is VM-only state (`/opt/hpsm/Caddyfile`); there is no Caddy config in the repo.
- **What b-tight is:**
  - Basic is skipped ONLY for `/api/*` paths with no `..`, `%2e`, `%2f`, `%5c` or backslash (case-insensitive), and the API keeps its bearer check.
  - `/idp/*`, `/api/healthz`, `/api/openapi.json` and 11 traversal variants stay behind Basic.
- **Measured exposure (S43, replica Caddy on 23780 in front of pc-lane-a):**
  - reproduced FAIL in Chromium on the public URL; b-tight gives PASS;
  - no-bearer sweep of 56 operations plus 5 extras: 53 answer 401, one 405, a few 404s;
  - the only 200s are healthz and openapi, which stay gated. **No `/api` route returns data without a bearer.**
- **Scripts** are in `<S43 scratchpad>/gate/` (`/private/tmp/claude-501/-Volumes-KK-T9-External-HDD--CODING-Datasec-HPSM/28f5c90e-532c-47c4-965a-2ec71aa65ff4/scratchpad/`); committed copies at analysis `a8651e8` `qa-s43/gate-blocker/`. **/tmp may not survive a reboot.**
  - Apply: `apply-azure-gate.sh Caddyfile.b-tight` (backs up to `Caddyfile.pre-s43-<UTC>`, validates in `hpsm-caddy`, writes in place, graceful reload; takes seconds, no SHA change).
  - Rollback: `rollback-azure-gate.sh Caddyfile.pre-s43-<UTC>`.
  - Post-check: `browser-gate-check.mjs` through the PUBLIC URL; curl set (`/`, healthz, openapi, `/idp/users`, `POST /idp/token`, traversals all 401 Basic; `/api/dashboard` without a bearer 401 Bearer); `azure/smoke.sh`.
- **NEXT on "go":**
  1. Send S44 a mail whose subject starts `KAM`, quoting his word verbatim with its time and channel.
  2. S44 sends a head mail, runs the identity check and applies. On any failure it rolls back first.
  3. S44 runs the public-URL browser check and the curl set, then reports.
  4. Tuesday tells Kam on the panel (TUESDAY tab) and verifies at origin.
  5. Tuesday commissions the live-half re-run of the acceptance gate.
  - If the upgrade is also due, the gate goes FIRST.
- **NEXT on "hold":**
  1. Send S44 a `KAM` mail with "hold".
  2. The durable redesign (cookie gate, IP allowlist or dedicated header) goes to Monday's review.
  3. Upgrade post-checks keep reporting the public browser check as FAIL, and Tuesday says so plainly to Kam.

## 🔴 LIVE — S44 (seat hpsm-375c, pid 39799, pane `%7` `Datasec/HPSM-S44`, transcript `375c22cb`)
- **Launch:** 19:47:28 with a brief verified at `datasec-hpsm@` (`briefs_staged/2026-09-13_hpsm-s44-successor-merge-seat.md`). Rung 5 proven from `~/.claude/projects/-Volumes-KK-T9-External-HDD--CODING-Datasec-HPSM/375c22cb-878d-495f-b5a7-24379c82f071.jsonl`.
- **Plan:** CONFIRMED 09:56:56Z (`…-answer-plan-confirmed.md`). Acceptance routing sent (`…-answer-acceptance-verdict-routing.md`), then the FX-S7 FINAL answer (`…-answer-fxs7-final.md`).
- **S43 pane `%5` CLOSED 20:21** after FX-S7 FINAL at `ce62887` and S44's CONFIRMED. HANDOVER-S43 is `1a23e93`, addendum 1 `9e68dd9`.
- **Merge order as ruled.** Each step: chain plus switch-ON e2e at ZERO failures, fast-forward main only on GREEN. **LOCAL main = `2bfb42a` at 10:24Z, NOT pushed** (HPSM-light still `afc10e9`).
  1. **FX-M1: DONE GREEN.** `f80ebc4` + fixture fix `2bfb42a` (the `stack-api-isolation.mjs` approver had no tenant membership, now correctly 422). CI GREEN, switch-ON 63/63 at zero failures.
  2. FX-LV `19a5caa`, merged in the seat worktree as `b8fc2a9`: checks and e2e OFF GREEN; CI and switch-ON running at 10:28Z.
  3. FX-R `5eccefd`.
  4. FX-S7 `ce62887` (the bottom-pin is in its CSS: 0 px gap on 9 tiles, contrast 5.34:1).
  5. FX-SI `bc61c4f`: a PROOF of the bottom-pin on MERGED code. **Branch READY: `s44/seat-layout` `85cbe2d`** = ce62887 + bc61c4f + the proof in `s43-signin-descriptions.spec.ts` (≤1 px at 1440 and 390, RED/GREEN on a seat stack) + `#pc-tenant` max-width 260px CSS (1440 screenshot still to come) + e2e typecheck 4→0 + e2e README. A failure is fixed in the seat.
  6. Rolling upgrade: head mail, then Tuesday warns Kam; pc-lane-a then Azure; the post-check proves the A/B engagements plus the public-URL browser check.
  7. **FX-PIN (W4B-m2): FINISHED GREEN `d82ca16`** (`refuseStalePin` first on all 12 state-changing routes in lifecycle.ts and inputs.ts; 18 tests; 15/15 mutants; stale-pin stack proof). **Plus a seat commit: `createDraft` refuses a stale pin (Q1 YES).**
  8. FX-ID (W4B-m1): **lane RUNNING from `d82ca16`** on `problem.ts`, `problem.test.ts`, `context.ts` + new `s44-fx-id.db.test.ts`, stack 24180; lands after FX-PIN and before F-API.
  9. F-API `8d86395` + seat root commit `s44/feedback-root` `15f2542` (nginx `/api/feedback` 52m WITH proxy_pass; `PC_FEEDBACK_RETENTION_DAYS`).
  10. F-WEB, then feedback READY FOR QA with naming (b). **F-WEB-B FINISHED GREEN `5b8d843`** (e2e 70/70 OFF and ON; body-size proof through the edge).
  11. C11: **a content hash change, so it STOPS for Tuesday.**
  12. The credential round (A-m1, A-p2, N33/N09/N26, W4B-m3; partition in a STATUS first).
- **Lanes running (10:30Z):**
  - FX-ID from `d82ca16` on 24180;
  - S-m3 from main `2bfb42a` on 24480 (`secrets.ts` + unit test + new `s44-sm3-depth.db.test.ts`; STOP if the error code must be enumerated in the contract);
  - the upgrade-toolkit prep agent (`<S44 scratchpad>/upgrade-s44/`, GETs only on pc-lane-a; upgrade dry-run moved to 24680).
  - FX-PIN and F-WEB-B are FINISHED (above).
  - Ports 24080–24580; at most 3 agents plus the seat; docker one step at a time under the lock, gates first.
- **Engine serial queue** (S44 default, accepted by silence): C11 (24380, after FX-LV on main) → D-M1 → the credential round's engine part.
  - **D-M2 splits:** the API part after FX-PIN and F-API, the engine part after D-M1, and they land together.
  - **S-m3** runs as its own small lane when a slot frees.
- **Seat items:**
  - Tenant picker `max-width` on `#pc-tenant` is ruled into the seat's `app.css` if cheap (one commit, 1440 px proof), otherwise BACKLOG. It never delays the upgrade.
  - Out-of-lane commits: `apps/web/e2e/README.md` and `apps/web/e2e/tsconfig.json` (`DOM.Iterable`).
  - BACKLOG fold at analysis `6958d88`.
- **FX-PIN RULINGS 10:30:10Z** (`…-answer-fxpin-q1-q4.md`): Q1 createDraft refuses a stale pin (seat commit at step 7); Q2 leave updateEngagement (named in the drift guard); Q3 leave clone ruling (e), BACKLOG **FOR KAM'S MONDAY LIST**; Q4 start FX-ID and S-m3. **Consequences carried:** (1) a stale-pinned engagement is READ-ONLY until re-pin exists, so **any upgrade that changes pins turns Kam's A/B read-only**, and S44 measures whether steps 1–5 change any pin, answering in the head mail; (2) a web 409 browser check (S2/S4/S5 saves, S9 approve) is REQUIRED before any upgrade carries FX-PIN.
- **STOP for Tuesday:**
  - any content hash change (C11 certain), **and any pin change in steps 1–5 (see the head mail)**;
  - D-M1 or D-M2 before any upgrade that carries them (demo impact: measure release/validate on A and B first);
  - any `/api` 200 with data and no bearer;
  - an axe contrast failure (report the ratio; never change the colour);
  - anything on Azure without a head mail;
  - the gate apply without a `KAM` mail;
  - any push (none until the delta gate is GO and Tuesday gives the word).
- **NEXT per expected mail:**
  - **Head mail:** a short panel warning to Kam (the site restarts for a few minutes), verified at origin.
  - **Upgrade REPORT:**
    - a panel note: what changed, the engagements to use, the DO NOT USE list, and the public browser check result;
    - label any tunnelled check as tunnelled (trap 49);
    - tell Kam at once (his 17:48 ask).
  - **Step-5 proof STATUS:** check the sign-in text against `apps/api/src/authz.ts` (bridge_operator says the Bridge is a stub). **Mark Kam's 19:01 relay delivered only when a READY names the artefact.**
  - **STATUS naming lanes or partitions** (FX-ID, D-M1/D-M2, the credential round): check disjointness by path. Silence accepts a sound default.
  - **C11 / D-M1 / D-M2 STOP:** put it to Kam as a card or panel question (it strands his A/B engagements). On C11's READY, mark `hpsm-composer-demo-release-with-device-groups` `--delivered`.
  - **READY FOR QA:** commission ONE delta tier-1 gate on `09c1591..<fix head>` (Q + W + fixes; the combined gates never tested Q+W).
    - Model launchers: `2_Project_Files/fleet/qa-agent/launchers/resume_qa_hpsm_composer_09c1591_combined.sh` and `launch_qa_hpsm_composer_09c1591_combined.sh` (both exist).
    - Run it in a pane with `cockpit.sh add`, then rung 5 (trap 47).
    - Score the S43/S44 merge round at that verdict.
  - **S44 at 80–90%:** HANDOVER-S44 → `ps` census (trap 32) → S45 brief → routing row `Datasec/HPSM-S45|datasec-hpsm@agentmail.to|yes` → `cockpit.sh add` a new pane → rung 5 → `pane_close.sh %7` after S45 CONFIRMS. **Never `cockpit.sh rotate` (trap 37).**

- **20:44 — S44 STATUS 10:44:08Z (before the GO mail):** merge 3 FX-R GREEN, LOCAL main `47305ce` (CI GREEN, switch-ON 63/63 zero-failure), NOT pushed. Step 4 FX-S7 merged as `693a5db`, chain m4-s44 running. Step 5 `s44/seat-layout` `2d6b884` ready (proof run 2 GREEN). **Pins UNCHANGED caf63fd..step 5** (content/db/engine diffs empty; same release hashes). The 30-min FX-LV+FX-REL clock starts when step 5 is GREEN on main.
- **20:36 — S44 STATUS 10:36:39Z (DKIM pass, read whole) → ANSWER ~10:3xZ** (`briefs_staged/2026-09-13_hpsm-s44-answer-fxrel-order.md`):
  - **Merge 2 FX-LV HELD:** switch-ON e2e failed 1/67 at `s43-local-values.spec.ts:442`. A PRE-EXISTING S10 defect since S40 `d08531b`: the release confirmation banner is unmounted by the reload that release triggers (`Release.tsx` local state + `useLoad` sets loading). **Monday-visible.**
  - **New lane FX-REL** (`s44/fx-rel` at b8fc2a9, 24680, `Release.tsx` + component test; `useLoad.ts` forbidden with STOP).
  - **FX-R taken ahead** onto main as `47305ce` (chain m3r-s44); no objection.
  - **Step 5 bottom-pin proven** RED→GREEN at 1440 and 390; the tenant-picker proof re-running after S44's own locator bug (2d6b884).
  - **Pins:** precheck on 2bfb42a NO STOP (positive control against c2fbc36 gives 3 STOPs).
  - **Upgrade toolkit READY** (`<S44 scratchpad>/upgrade-s44/RUNBOOK-S44.md`; postcheck-ab read-only PASS on A e920ac1d / B 8ce21d2a).
  - **Ruled:** step 6 waits for FX-LV+FX-REL at most ~30 min after R/S7/SI are GREEN on main, otherwise it rolls without LV and batches LV+REL next.
  - **Tell Kam at the head mail:** the release confirmation flash is a known pre-existing defect being fixed (FX-REL).

## ✅ ACCEPTANCE+SECURITY GATE @ caf63fd — CLOSED, scored 1.00
- **Verdict** 09:58:13Z (DKIM pass), report read whole (538 lines): `Testing Agent MAIN/projects/hpsm/reports/2026-09-13-composer-caf63fd-brief-acceptance-security-tier1/report.md`. Pane `%6` closed.
- **DELIVERABLES NO GO 1/2/10/4:**
  - D-B1: the live gate;
  - D-M1: required discovery is never required (T3 cannot fail, `resolve.ts:694-706`);
  - D-M2: exception fields optional (201 → approved → released).
- **SECURITY GO WITH FINDINGS 0/0/3/1:**
  - S-m3 (deep JSON 500) → its own lane;
  - S-m1/S-m2 (edge headers; Mailpit/MinIO/worker on the edge) → BACKLOG with priority, as one post-round edge commit.
- **Routed to S44 as fix round 1 of 2** for this new class. Minors go to the BACKLOG fold. D-p2 is settled (D1 retired).
- **OWED after the gate fix is APPLIED:** re-run the LIVE half (the walk-through plus probes 2, 3, 5, 7, 9, 11–13) as a live-only delta. Model launcher: `…/launch_qa_hpsm_composer_09c1591_brief_acceptance_security.sh`. Own `QA Harness (synthetic)` tenant only.
- **D-m6** (S5 re-asks D-001…D-006) needs Kam's ruling on A-17 before anyone changes it.

## LIVE DEMO STATE (caf63fd on pc-lane-a AND Azure; upgraded 08:54–08:57Z)
- **Public URL:** `https://hpsm-composer-demo.australiaeast.cloudapp.azure.com`. **Unusable past sign-in until b-tight.**
- **USE, tenant "Synthetic Customer B (demo content)":**
  - Azure (tenant `e93302d2`): A drafts, one group `3bb6fcb2`; B released 1.0.0, zero groups `a9101d3f` (version `b03aae4b`).
  - pc-lane-a (tenant `fb2de441`): A `e920ac1d`; B `8ce21d2a` (version `3a951c52`).
- **DO NOT USE** (stale pin `0030d4c6`, they answer 409):
  - Azure `c9bce98b` "Office fleet hardening (demo)" and `1ec31037` "Demo content proofread (synthetic)";
  - 9 on pc-lane-a, listed in `sent_mail_s43_report-live-upgrade-caf63fd_seat-hpsm-28f5.txt`.
- **No agent touches** the `QA Harness (synthetic)` tenant, the `policy-composer-qa-*` stacks, or any engagement or tenant it did not create. **Kam is testing.**

## OTHER OPEN (not HPSM)
- **NexusAI RD-391** (High, `.dockerignore` any-depth) is the next Datasec lane once HPSM is stable.
  - Brief it only after a fresh read-only board read (`fleet/board_count.sh`; NexusAI's own `JIRA_*`, trap 31).
  - Residue RD-392/393/394/396/397/398 partitions by file; RD-395 is Kam's product call.
  - **The Mini's load is the constraint** (gate C saw ~115–347): NexusAI docker steps go under the shared lock.
- **For a future NexusAI seat** (s12's Explore read, not verified line by line): `backend/routes/feedback.js` PATCH/DELETE lack an admin-role check; the widget never sends `created_by` (stored as `'anonymous'`); `server.js:199` `autoCreateAIFeedback` hard-codes the dead VM URL; the Feedback_System link is dead (RD-50).
- **Wednesday coordination:** the resolver claim (above); she took the statusline-publisher skip-write as owed; traps 37, 38 and `launchers.conf` are on her owed list; the panel_sync race's durable fix is hers.

## 🔴 WITH KAM (asked; nothing blocks)
1. **b-tight go/hold** (above).
2. **A-17 ruling** for D-m6.
3. **Card `tuesday-seat-self-rotate-with-liveness-check`:** `status: open` in `decisions.json` when this was drafted. Mention it once.
4. `hpsm-composer-monday-review-scope` (amended by his note). **Kam reviews HPSM on Monday 2026-09-14.** W45-p2 stays his.
5. Which panel tab he reads: UNMEASURED; he was told the TUESDAY tab.
5b. **Monday list, from S44's F1 (12:01Z):** a released policy cannot be revised from the website at all (no web path to the next draft; S8 points users at a screen that only clones). Pairs with 5a (no re-pin). Not a card tonight.
5a. **Monday list, from S44's Q3:** after a content upgrade, a clone of a released engagement is born stale (ruling (e) vs W4B-m2), next to the missing re-pin action. S44 BACKLOGs it; Tuesday raises it at Monday's review, not as a card tonight.
6. Carried from s11, not re-measured: Registry B2 plus RD-391's bearing on it; `brew install gitleaks` (RD-342 option E); RD-281, the rebuilt Sustainability tab render; Full Disk Access for `/bin/bash` (ruled grant; his hands); HPSM Jira key (`HPSML`), R4-m2's owner option and the HPSM-40 analysis-repo remote; his vault on the T9 (484 behind, 102 uncommitted); RD-367's branching-model half; the ATTIO digest still going to `wednesday-agent@` (a production change; flag it first); `rd104-gh-identity-acceptance-false-premise` → `youcheck` undelivered. Not yet asked: whether `/api/admin/health` open before first-run should be a ticket (Tuesday's call).

## ⚠ TRAPS
1. Never `git pull --rebase --autostash`. A wedged rebase: `rebase --abort`, then `git -c core.editor=true merge origin/main`.
2. macOS has no `setsid`; use `nohup bash … &`.
3. Store writes are gated on `git merge-base --is-ancestor <origin sha> HEAD`.
4. zsh has no `PIPESTATUS` and does not word-split `$VAR`; loop in python.
5. `cockpit.sh say` takes the pane NAME; `pane_close.sh` and `wake_ack.sh` take the `%ID`.
6. The frozen-busy leg fires on `%0` while a background watcher runs: check the watcher output and the inbox, then `wake_ack.sh %0`.
7. The exiting watcher is tracked: `fleet/cockpit/watch_tuesday_exiting.sh <MARK> <HH:MM> <pid…>`.
8. Launch outputs go under `fleet/briefs_staged/*.out` (gitignored).
9. Outside `dashboard/data`, write and commit in ONE round; never two commits in parallel calls (a gap holds panel_sync a cycle).
10. `decision_queue.sh add --json` cannot take `--override-prior-rulings`.
11. `kam_rulings_today.sh`'s FRESHNESS line lags Kam's taps; `[Kam -> Tuesday]` mails do not.
12. `wake_watch` wakes this seat for `view=wednesday` messages; check the view.
13. `cockpit.sh launch` cannot start Datasec projects here; use `cockpit.sh add`.
14. Never a plain `git fetch` in a verify loop.
15. QA gates and build seats run in a tmux PANE, never nohup headless.
16. The card-ID send gate refuses a card id the store cannot show.
17. `send_brief.sh` subjects say `[Wednesday -> …]` while the sender is tuesday-agent@. Harmless.
18. panel_sync rebases local commits: verify by subject or content, never by local SHA.
19. A probe whose found and not-found branches both exit 0 proves nothing by rc.
20. Foreground `sleep` is blocked; use background loops.
21. Verify a brief at the destination inbox BEFORE `cockpit.sh add`.
22. Grep the target launcher for EVERY verb and path the HOLDS name, derived from the holds text.
23. `decision_queue.sh` and `reconcile_rulings.py` are in `2_Project_Files/tools/`; `board_count.sh` is in `2_Project_Files/fleet/`. Capture an rc on its own line before any `| grep`.
24. AgentMail `GET …/messages/<id>` needs the id URL-encoded.
25. The send gate refuses a ticket id in the QUEUE without a PROVENANCE state line.
26. Two QA gates booting at once collide on ports: stage the second, or name ports in both briefs.
27. A counts-file merge conflict: `1/1` placeholder, then `npm run verify -- --update-counts`.
28. A watcher or probe gives "the read failed" its own branch; a parse error is not mail.
29. Bound every network read (`subprocess.run(..., timeout=)`) and prefer the ref panel_sync already fetched (`ls-remote` hung 9 min).
30. CronCreate jobs are session-only; a rotation deletes them.
31. NexusAI Jira: `JIRA_SITE` is scheme-less (prefix `https://`). Parse only `JIRA_*` from NexusAI's own `4_Credentials/.env`; never source the file.
32. Before any project-seat launch and at rung 5, census `ps -axo pid,tty,lstart,command | grep "claude .*project '<Project>'"` across ALL terminals.
33. Before answering a plan confirmation, match it to the SEAT by its boot facts, and re-list the inbox for a second mail on the topic.
34. A harness background task on `%0` counts as BUSY, so frozen-busy wakes come about every 8 min. `wake_ack` cannot hold them under 24 h to a reset (the countdown is in the hash). Run extra waiters detached.
35. Wednesday's `rotate_liveness.sh` detects a fleet-session loss and relaunches the coordinator, but CANNOT restore other panes (1 loss in 63).
36. `wednesday_rotate.sh` respawns only its own pane and finds it by seat name (hence the rename procedure).
37. `cockpit.sh rotate` is UNSAFE for Datasec seats: it polls wednesday-agent@ for the wrap, force-kills at 10 min and brings no successor brief. Use checkpoint → wrap → brief → new pane → close after CONFIRM.
38. A project's second pane needs its own `inbox_routing.conf` row BEFORE `cockpit.sh say … --mail`; without it, exit 1 and silence. Check the rc and the pane.
39. A "frozen busy" builder while gates run usually waits on the docker lock or its own subagents. Check the inbox, then transcript and subagent mtimes, then `ps` lockf waiters, then the pane. Never tap a seat waiting on its own agents.
40. Cockpit "Fresh" kills EVERY agent pane (16:48 incident). When asking Kam to restart this seat, say "Resume, not Fresh" in the same sentence.
41. `usage_tuesday.json` churn aborts panel_sync rebases on a long backlog. Set `git update-index --assume-unchanged` on it for one cycle, then remove the flag.
42. Never put a command in a zsh variable (`$G log` fails, and `&& yes || no` prints "no"). Branch on the exact rc: 0 yes, 1 no, anything else ERROR.
43. `prompt_log.sh <channel> <text> [note]`. Read a tool's usage in a SEPARATE action before the first call.
44. Resume a killed QA gate with `claude --resume <session>` and `CLAUDE_CONFIG_DIR=TUESDAY/4_Credentials/.claude`. Map session to gate by counting report-dir mentions.
45. `reconcile_rulings.py` skips every Datasec card. Record Kam's Datasec taps with `WED_AGENT=tuesday decision_queue.sh rule <id> <choice>`; if the gate refuses, wait for panel_sync's pull.
46. A watcher MARK is one second past the newest PROCESSED mail's own timestamp, never the arming time; list the inbox unfiltered before arming. Kam's taps arrive as `[Kam -> Tuesday] panel message`. The runner's own unsent `[wake_watch]` line at `%0` HOLDS later taps.
47. **A rung-5 check on a successor:**
    - EXCLUDES every session id that existed before the launch;
    - requires the matched transcript's FIRST user record to be after the launch;
    - matches a string only the successor produces (its brief subject, "session 44").
    - A checker passed on S43's own transcript `28f5c90e`.
48. **Panel replies show only on the matching agent tab.** Verify-at-origin proves the row EXISTS, not that it is VISIBLE. Answer in the channel the question came in, yes/no first.
49. **"The site is up" for a gated site needs one authenticated journey (sign in, first screen) through the PUBLIC path, never a tunnel.** Label any tunnel, port-forward or localhost check as such in the sentence to Kam.
50. **Queued terminal input is dropped across a rotation.** The successor diffs the predecessor's transcript (first action c); the predecessor re-reads its own before `--self`. Never write "your instructions carried over" from panel and mail alone.
51. **A HOLD or permission that names a property of the code** ("the CSP", "behind auth") is grepped at source in the same action, or written conditionally. When a helper reports an absence, ask what else in flight assumed the thing exists. (S44 caught HANDOVER-S43's nginx one-liner missing `proxy_pass`.)

## OWED, not started
- The delta tier-1 gate after S44's READY FOR QA, and the live-half acceptance re-run after the gate fix (both above).
- Monday redesign note: the Caddy gate is VM-only state with no repo record (BACKLOG "durable gate redesign").
- Amend `Launch_Tuesday.command`: step 5 (no Tuesday daily note; name the pickup, this seat's ledger and `git log`) and the stale `FIRST-BOOT-TUESDAY.md` line. Red-proof it with a boot.
- NexusAI ticketing (a NexusAI seat's job): S53 m2/m3, S54's 8 BACKLOG items, round-3 NEW-3/NEW-4. Also 4 Dependabot alerts (RD-354 owns qs 6.15.2; three need a `gh` identity).
- Raise with Wednesday (shared tools, coordination only): `send_brief.sh` refusing a bare "No az/gh" when the launcher runs them; `wake_ack`'s hash including the countdown; `cockpit.sh add` refusing when that project's claude already runs; `--self` refusing while the transcript holds a human line newer than the pickup's last commit; Tuesday replies to Kam carrying `view: both` (or a badge on the other tab); `TASKS.md`'s NEXT PICKUP pointer naming her file.
- NAS WED-149: `com.tuesday.nassync` stays BOOTED OUT until the partition is built (design `1_Project_Definition/Architecture/2026-09-10_nas-two-seat-sync-check.md`).
- Capacity: if the allowance hits 100%, every seat on both machines stops mid-turn. Recovery reads each seat's transcript and handover, and a cut gate re-runs under a NEW report path.

## ✅ DONE IN s13 (verified)
- Rotation 19:04:15: `respawned OK` + `LIVENESS OK: 3/3 agent panes present` (19:04:39); `%0` renamed back 19:05 (rc 0).
- **Found the dropped 19:01:39 sign-in instruction** by transcript diff (ten lines, nine carried). Kam told 19:11:46 and answered "no" first in the terminal. Relayed to S43 09:14:09Z, which became lane FX-SI plus the FX-S7 CSS rule; the bottom-pin is in `ce62887`. Ledger w=4.
- Naming (b) ruled 09:14:10Z (`brand.ts` productName on screen, HPSM internally).
- Live gate blocker verified at source (`auth.ts:44`, `client.ts:23`, no Caddy in the repo); S43 briefed 09:25:25Z; b-tight READY-TO-APPLY read and measured; Kam asked twice.
- S44 briefed (verified at the destination 09:47:21Z), launched 19:47:28, rung 5 proven on `375c22cb` (the selector slip was caught before any report), plan CONFIRMED; FX-S7 FINAL answer and tenant-picker ruling sent.
- Acceptance+security verdict read whole, scored 1.00, `%6` closed, routed to S44. S43 wrapped; HANDOVER read whole; `%5` closed after FX-S7 FINAL.
- Panel notes VERIFIED AT ORIGIN: 19:08:00, 19:11:46, 19:18:24, 19:24:59, 19:39:17; and **confirmed by s13 reading each verifier's output line "FOUND AT ORIGIN <ts>" (not only its rc):** the handover note 19:49:05, the verdict note 20:01:12, the "sign-in built" note 20:22:02. The 19:21:41 "Straight answer: no" note: VERIFIED AT ORIGIN by s13 at 20:32 (2026-09-13T19:21:41).
- Ledger rows 2026-09-13: rung-5 selector (w=3), site-up checked the lock not the door (w=1), verified-exists-not-visible (w=1), dropped queued input (w=4).
