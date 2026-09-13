---
date: 2026-09-14
type: pickup
scope: DATASEC ONLY — Tuesday, on Kamils-Mac-mini (T9 drive). Secuura and general are Wednesday's, on the Studio.
source: written WHOLESALE by Tuesday s15 at its wrap (06:52 AEST), on Kam's "please wrap up". The previous pickup (s14's, with s15's blocks) is at `NEXT-PICKUP-TUESDAY.md.pre-s16-wholesale` and in git at `ef4d002433`. Sections ON EVERY WAKE, ROTATION PROCEDURE, TRAPS (1–58), OWED and the carried Kam items were copied VERBATIM from it.
status: live
supersede: replace WHOLESALE at the next pickup; never append.
---

# NEXT PICKUP — Tuesday s16 (written by s15 at its wrap)

**BLUF.**
- **Live:** the HPSM feedback feature runs on both stacks at Composer `b9c6464f73e8d7199152a1f9b0d04b9cd8894b0a` (16 migrations, api 0.14.0) since 02:00–02:03 AEST 2026-09-14. **Rollback target = `b9c6464` (roll forward only; a `9b8ea76` redeploy is the M16 outage).** Gate b-tight is unchanged on the Azure Caddy.
- **No HPSM seat is live.** S45 wrapped at 02:41 and pane `%9` is closed. Stacks up: `pc-lane-a` (live local) and `pc-s45-edge` (kept for S46).
- **Next job = launch S46 when Kam rules C11** (or at the morning boundary). The brief is drafted, NOT sent. See the S46 LAUNCH PLAN below.
- **Nothing is waiting on Kam for tonight.** His Monday HPSM review list is under WITH KAM.

## ON EVERY WAKE
- Run `2_Project_Files/tools/kam_rulings_today.sh`, **never `kam_msgs.sh` unfiltered** (it prints Wednesday's tab). Check `[Kam -> Tuesday]` mails. List `tuesday-agent@` UNFILTERED and route on SUBJECT.
- **A freshness comparison prints COUNTS and TIMESTAMPS only, never `text`** (ledger 2026-09-13, w=2). Any ad-hoc read of Kam's chat store filters `view in ("tuesday", "both", None)` in code BEFORE printing any field. When the rulings tool warns STALE-COPY, compare `git show origin/main:<file>` with the local copy by row count and newest `ts`, and never pull with `--autostash`.
- Run `git status --porcelain | grep -v 0_Brain/dashboard/data/`. Rotation band is 80–90; this seat's checkpoint band is 70.
- **Verify every panel message AT ORIGIN:** `git show origin/main:0_Brain/dashboard/data/chat_tuesday.json`.
- **Do NOT read `0_Brain/daily/`** (Wednesday's). **Kam types straight into this terminal; those lines are first-party.**
- **Kam sees Tuesday's panel replies ONLY on the orange TUESDAY tab** (`chat.html:190` `inView`, `cockpit.html:367` `msgInView`). Which tab he uses is UNMEASURED, so say where the reply is.
- **When Kam asks something in the terminal, answer in the terminal, with the literal yes or no as the first word.** The panel copy is secondary.


## 🔴 POST-WRAP 08:05 AEST: AN HPSM SEAT IS LIVE, LAUNCHED BY KAM — DO NOT LAUNCH S46 WHILE IT RUNS
- **Seat hpsm-e593:** `claude` pid **14191**, **Terminal.app `ttys000`, not a cockpit pane**. Started 2026-09-14 07:08:33 AEST, by Kam's own hand. Transcript `~/.claude/projects/-Volumes-KK-T9-External-HDD--CODING-Datasec-HPSM/e593664c-834e-4015-a999-71abc8e330e8.jsonl`. HPSM commits: `1a7ac18` boot 07:12 · `a2b269e` BACKLOG W6-p3 re-measured 08:00 · `ca74b00` user guide sent 08:04.
- **The BLUF's 'no HPSM seat is live' and the whole S46 LAUNCH PLAN are SUSPENDED while e593 runs.** A second seat would share `datasec-hpsm@` with it (the 2026-09-12 two-seat row). Census `ps` for an HPSM `claude` in ALL terminals before any launch (trap 32). Treat the S46 brief (`2c5f2f34`) as input for the successor only when e593 wraps or Kam says so.
- **Mail from e593 (DKIM pass), 22:03:44Z = 08:03 AEST:** `[Datasec/HPSM -> Kam] Policy Composer sign-in and user guide (PDF)`, TO `kamil.kreiser@datasec.com.au`, CC `tuesday-agent@`. Attachment `Datasec-Policy-Composer-User-Guide.pdf` (2,490,752 B). The file is at `!CODING/Datasec/HPSM/1_Project_Definition/Architecture/2026-09-10_policy-composer/user-guide-2026-09-14/Datasec-Policy-Composer-User-Guide.pdf`. The site password is NOT in the guide or the mail (it points at `4_Credentials/hpsm-demo-site.txt`). Screenshots come from a local copy of `b9c6464`; nothing live was changed.
- **Kam works with e593 directly.** Tuesday supervises by reading, and does not brief or contradict unasked. Its mails cc `tuesday-agent@`, so the wake runner surfaces them.

## POST-WRAP (Tuesday s15, 07:0x AEST): Wednesday's DEAD-leg fix, verified here
- Wednesday COORDINATION 20:59:21Z (DKIM pass): the shared DEAD-leg predicate was replaced by `2_Project_Files/fleet/cockpit/dead_banner_check.sh`, because the bare banner-literal grep killed healthy seats that had printed prose about the banner. **It arrived here as commit `885ecd8c4`, not the `376172e77` her mail named** (rebased by her panel_sync; trap 18). Measured 07:05:57: file present at origin and locally; `wake_watch.sh` and `wednesday_rotate.sh` each reference it; `--selftest` rc 0 PASS; `dead_banner_check.sh %0` rc 1 with no output. Reply sent from tuesday-agent@ and verified by its sent copy (ts 2026-09-13T21:06:43.157Z). **Never write the banner's literal words into a command or a note on this pane.** Under the old predicate that is exactly what triggers a false kill.

## FIRST ACTIONS (Tuesday s16, in order)
1. **Boot normally.** If you came in by a rotation, also do ROTATION PROCEDURE step 5 (rename `%0` back to `wednesday`) and read `fleet/cockpit/logs/rotate_wednesday.log` for LIVENESS.
2. **Diff the predecessor's human lines against this pickup** (ledger w=4). s15's transcript is `4_Credentials/.claude/projects/-Volumes-KK-T9-External-HDD-TUESDAY/82fb4ceb-af35-474b-b2dd-104e745c43c3.jsonl`. Look for `type: user` text and `queue-operation enqueue` records after this pickup's commit.
3. **`kam_rulings_today.sh`: look for a C11 ruling, or anything on HPSM.**
4. **Inbox, unfiltered.** The last processed mail is S45's wrap, 2026-09-13T16:41:03Z. No seat is live, so expect only Kam or QA.
5. **Wake cover:** the shared runner (pid `95836`, trap 60) covers mail. No exiting watcher is armed. Arm one on S46's pid once S46 is live.

## KAM'S WORDS (verbatim; T = terminal)
- **2026-09-14, T, 06:44:45:** *"did you email the new doc?  also whats the path"* → answered "No", with the paths.
- **2026-09-14, T, 06:47:42:** *"dont worry but we agreed you would email"* → owned. The lesson is filed; nothing was sent, per "dont worry".
- **2026-09-14, T, 06:47:48:** *"please wrap up"* → this wrap.
- **2026-09-14, T, 06:49:33:** *"pleas outline what you do to manage projects and sub agents?  use bullet points?  I need to decide whether this is a good credit spend or not"* → answered in the terminal at the wrap, BLUF-first with measured numbers. **His decision on the coordinator's cost is OPEN; do not assume the answer.**
- **Standing from 2026-09-13 (full list in git `ef4d002433`):** 09:17 *"spin up as many agents as possible … as long as multiple agents do not create a problem"* · 18:37 *"keep going until completion"* · 18:51 *"Upgrade as soon as it's ready"* · 17:48 *"tell me when the HPSM agent finishes and where the testing briefs are located"*.

## LIVE HPSM STATE (S45 REPORT 16:05:14Z + wrap 16:41:03Z, both DKIM pass, read whole by s15)
- **Both stacks on `b9c6464`.**
  - PUBLIC checks: TLS, gate 401/401, sign-in 200, a signed-in journey, 26/26 gate probes, Caddy `61f519cdf8ecfed9` unchanged.
  - TUNNELLED checks: post-check A/B 20/0/1, and a read-only feedback smoke (0 items).
  - s15's own public probe at 02:06: 401, ssl_verify 0, http→https 308.
- **USE:** Azure A `3bb6fcb2`, B `a9101d3f`; pc-lane-a A `e920ac1d`, B `8ce21d2a` (tenant "Synthetic Customer B"). **DO NOT USE:** stale-pin `c9bce98b`, `1ec31037` (read-only). Never touch the two QA Harness tenants.
- **Known quirk (FB-D-m1, Minor):** a platform_admin with no membership gets 422 on Feedback. Test with a consultant or approver.
- **Local main `b9c6464` is NOT pushed** (HPSM-light origin `afc10e9`).
- **Branches waiting, all GREEN, none merged:**
  - CR `da64f28`;
  - DM2 `22e4d61` (7 spec questions for Kam);
  - C11 `bfce726` / `c0c1b13` (HELD for Kam);
  - EDGE `48bb744` (`s45/edge-sm1-sm2`; evidence `<S45 scratchpad>/edge-evidence/`; stack `pc-s45-edge` 25780).
- **Handover:** `!CODING/Datasec/HPSM/5_Project_History/HANDOVER-S45_seat-hpsm-3562.md` §0 (current). Decisions D-S45-01..32.
- **Findings in HPSM BACKLOG** (S45 `13e7682` + EDGE residue): FB-D-m1/m2, FB-D-p1/p2/p3, FB-S-m1 (merged with F2), FB-S-m2, FB-S-m3, F1 (query strings reach the request logs), F3 (echo before scan), F4, F5.

## S46 LAUNCH PLAN (when Kam rules C11, or at the morning boundary)
1. Run `kam_rulings_today.sh`, then re-read HANDOVER-S45 §0.
2. **Fix the drafted brief** `2_Project_Files/fleet/briefs_staged/2026-09-14_hpsm-s46-successor-brief.md` (commit `2c5f2f34`, 375 lines; dry-run PASSED):
   - (a) ADD a queue item: **EDGE `48bb744` gets a tier-1 QA gate on `b9c6464..48bb744`, then the merge.** Any live edge change needs its own HEAD mail and Tuesday's ruling.
   - (b) If Kam has ruled C11, carry his words BY NAME and SUPERSEDE the "C11 HELD" line. Otherwise keep it HELD.
   - (c) Re-validate every fact against HANDOVER §0 at that time.
3. Census `ps` (trap 32), then re-snapshot the HPSM session ids.
4. `SEND_BRIEF_DRY_RUN=1 WED_AGENT=tuesday bash 2_Project_Files/fleet/send_brief.sh --to Datasec/HPSM --kind brief …`, then the real send. **Never use `--to …-S46` (trap 52).**
5. Verify at `datasec-hpsm@`. The routing row `Datasec/HPSM-S46` already exists.
6. `cockpit.sh add 'Datasec/HPSM-S46' "bash \"/Volumes/KK_T9_External_HDD/!CODING/Datasec/HPSM/Launch_Claude.command\""` → rung 5 → answer the plan → arm the exiting watcher on S46's pid.
7. **Tuesday commissions the EDGE tier-1 gate itself.** Clone the pattern of `qa-agent/launchers/launch_qa_hpsm_composer_b9c6464_feedback_fix_delta.sh`, set the range `b9c6464..48bb744`, **name the SENDING inbox `coagent@`** (trap 63), check its ports against S46's lanes, and rung-5 it.

## ROTATION PROCEDURE (this seat)
- **Why it is needed:** `wednesday_rotate.sh --self` finds the coordinator pane by `@cockpit_name == $SEAT` (`tuesday`), but `%0` is named `wednesday`. Without the rename `--self` refuses (rc 2), `--dead` refuses too, and a dead Tuesday seat cannot auto-respawn. **Never let this seat reach 90%.**
- **Rotate only when no live upgrade or gate apply is in progress.** A fleet-session loss would kill S45 mid-deploy.
  1. Re-read OWN transcript for human input received after this pickup was written, and relay it or add it here (ledger w=4, rule b).
  2. Check that the pickup is committed, that HEAD is in origin (the script gates on `merge-base --is-ancestor HEAD origin/main`), and that the tree is clean. **Assert that the newest block's heading is in `git show HEAD:0_Brain/tasks/NEXT-PICKUP-TUESDAY.md`** (trap 56).
  3. `tmux set -p -t %0 @cockpit_name tuesday`
  4. `WED_AGENT=tuesday nohup bash 2_Project_Files/fleet/cockpit/wednesday_rotate.sh --self > /dev/null 2>&1 &` (log `logs/rotate_wednesday.log`). `WED_AGENT=tuesday` resolves `Launch_Tuesday.command` (fixed `313325e7b`).
  5. The successor renames `%0` back to `wednesday` (first action b).
- **Wednesday's seat-name resolver fix is BUILT and STAGED, NOT installed** (COORDINATION 10:40:21Z, DKIM pass, read whole):
  - Location: `2_Project_Files/fleet/cockpit/staged/resolver-20260913/` at origin `59ec89ddf`.
  - Contents: a new `seat_resolve.sh` plus patched `wednesday_rotate.sh`, `wake_watch.sh` and `arm_wake_watch.sh`, with `DIFF.md` and `resolver_test.sh`/.out (22 PASS).
  - **Installing it on the mini is Tuesday's call. Neither s13 nor s14 installed it.** The install stops the running `wake_watch.sh` loop, copies the four files together (`seat_resolve.sh` sits beside the three) and re-arms. Do it at a boundary with no seat mid-turn.
  - **The second half is not built (Wednesday claims it):** `cockpit.conf`/`cockpit.sh up`, `apply_layout` (:90), `rotate` (:389) and `Launch_Cockpit.command:104` all hold the literal `wednesday`.
  - The live rotate renames the pane to `$SEAT` after a respawn (line 151), which is why the successor renames `%0` back. **Until both halves are installed, the rename workaround stands.**


## WITH KAM (Monday HPSM review; nothing blocks tonight)
1. **C11:** built and HELD. It changes demo content: the demo hash moves `fd7db6b8…` → `2971ffc4…`, and A and B become stale-pinned. D-M1, the D-M2 engine half, CR and the credential engine part all wait behind it.
2. **DM2's spec questions Q1–Q7:** HPSM analysis repo `qa-s45/dm2-exception-fields/REPORT.md`. DM2 means every demo exception needs an evidence reference, which changes Kam's walk-through.
3. **S44's F1:** there is no web path to a next draft. **The clone-born-stale tension:** a clone of a released engagement is out of date the moment it is made. **D-m6 / A-17.**
4. **Card `tuesday-seat-self-rotate-with-liveness-check`:** still open; mention it once.
5. **His credit-spend question** (above): his decision.
6. 7. Carried from s11, not re-measured:
   - Registry B2 plus RD-391's bearing on it;
   - `brew install gitleaks` (RD-342 option E);
   - RD-281 (the rebuilt Sustainability tab render);
   - Full Disk Access for `/bin/bash` (ruled grant; his hands);
   - the HPSM Jira key (`HPSML`), R4-m2's owner option and the HPSM-40 analysis-repo remote;
   - his vault on the T9 (484 behind, 102 uncommitted);
   - RD-367's branching-model half;
   - the ATTIO digest still going to `wednesday-agent@` (a production change; flag it first);
   - `rd104-gh-identity-acceptance-false-premise` → `youcheck` undelivered.
   - Not yet asked: whether `/api/admin/health` being open before first-run should be a ticket.


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
    - matches a string only the successor produces (its brief subject, "session 45").
    - A checker once passed on S43's own transcript `28f5c90e`.
48. **Panel replies show only on the matching agent tab.** Verify-at-origin proves the row EXISTS, not that it is VISIBLE. Answer in the channel the question came in, yes/no first.
49. **"The site is up" for a gated site needs one authenticated journey (sign in, first screen) through the PUBLIC path, never a tunnel.** Label any tunnel, port-forward or localhost check as such in the sentence to Kam.
50. **Queued terminal input is dropped across a rotation.** The successor diffs the predecessor's transcript (first action c); the predecessor re-reads its own before `--self`. Never write "your instructions carried over" from panel and mail alone.
51. **A HOLD or permission that names a property of the code** ("the CSP", "behind auth") is grepped at source in the same action, or written conditionally. When a helper reports an absence, ask what else in flight assumed the thing exists. (S44 caught HANDOVER-S43's nginx one-liner missing `proxy_pass`.)
52. **`send_brief.sh --to Datasec/HPSM-S45` (any `-S4x` name) skips the undelivered-ruling gate.** Always send a seat brief `--to Datasec/HPSM --kind brief`. (22:46 block: the S45 brief went out that way.)
53. **Two lanes can name the same port range in one mail.** S45's 13:12:24Z question offered the CRED lane 25280-25299, which G9 already held; Tuesday reassigned it to 25380-25399. Check every range a mail names against EVERY live lane before approving (extends trap 26).
54. **A watcher armed on a seat's pid exits when that seat's pane closes.** S44's pid 39799 ended with `pane_close.sh %7` at 22:53. Re-arm on the successor's pid (78373) in the same action as the close.
55. **String-compared timestamps need full precision.** S44's HOLD check refused once because `…12:23:36.000Z` sorts after `…12:23:36` (D-S44-34). Pass the mail's full timestamp including `.000Z`, the same family as the MARK-precision row.
56. **A quoted heredoc sees no shell variables; a readiness check must check the content, not the push.** The s13-rotation pickup edit raised `NameError` on a shell variable inside a python f-string. `git commit` then found nothing (rc 1), and a "READY to rotate" loop would have passed without the handover block. Write values literally, and assert the block heading is in `git show HEAD:<pickup>` (ledger 2026-09-13).
57. **An ad-hoc reader of `chat_kam.json` / `chat_log.json` drops the view filter** (s14 at 21:53 printed text from the other tab, w=2). Print counts and timestamps only; filter `view` in code before printing any field; `kam_rulings_today.sh` already does both.
58. **`watch_tuesday_exiting.sh` compares its HH:MM deadline as a STRING** (`[[ "$now" > "$DEADLINE" ]]`). A deadline after midnight armed before midnight exits on its first check ("23:48" > "05:55"), and the seat loses its mail wake silently. Before 00:00 use `23:59`, then re-arm after midnight (s14, 23:48 AEST).
59. **A kill list built from a `ps` substring match kills the killer.** The script's own `zsh -c` wrapper carries the script text, so it matches too. s15 killed its own shell at 02:5x (ledger 2026-09-14). Exclude your own pid and ancestors first, anchor `pgrep -f '^bash /…'`, or use a pid recorded at launch. Never kill and commit in one action.
60. **The shared wake runner is pid `95836`** (a `bash -c` loop, ppid 1). It spawns `wake_watch.sh` only at each arm, so `ps | grep wake_watch` between arms finds NOTHING: a false absence. Prove liveness from `fleet/cockpit/logs/wake_watch_runner.log` (an `armed:` line after the newest `tapped`) or `ps -p 95836`.
61. **With no agent seat live, a harness-tracked background watcher on `%0` makes the frozen-busy leg fire about every 8 minutes** (trap 34 in practice). Stop it; the wake runner covers mail. Re-arm the exiting watcher only when a seat is live.
62. **During a live run's HOLD window, ANY Tuesday mail to the seat's inbox stops the run** (S45's runner design). Between the GO and the REPORT, send nothing unless you mean to stop it.
63. **QA gate launchers must name the SENDING inbox (`coagent@`).** The `b9c6464` delta gate mailed its verdict FROM `tuesday-agent@`: label `sent`, authentication None, indistinguishable from Tuesday's own outbound. Authorship was proven only from its transcript.
64. **A Kam instruction stands until his own words withdraw it.** A refinement question with a do-nothing default inverts it (the 20:45 harness email; lesson 2026-09-14).

## OWED, not started
- **The ONE delta tier-1 gate** on `09c1591..<fix head>` after S45's READY FOR QA (NEXT above). Score the S43/S44/S45 merge round at its verdict.
- **A browser-driven pass on live** for what the live-delta gate could not render: FX-SI (sign-in descriptions), FX-REL (release confirmation) and W5-M3 (S7 width), plus the probe-12 negative half and W4B-m2 if still unmeasured. Kam was told he checks the visuals himself meanwhile.
- **Install the resolver fix** (`cockpit/staged/resolver-20260913/`) at a quiet boundary: no seat mid-turn, no live upgrade.
- Monday redesign note: the Caddy gate is VM-only state with no repo record (BACKLOG "durable gate redesign", now carrying S-p2 beside S-m1/S-m2).
- Amend `Launch_Tuesday.command`: step 5 (no Tuesday daily note; name the pickup, this seat's ledger and `git log`) and the stale `FIRST-BOOT-TUESDAY.md` line. Red-proof it with a boot.
- NexusAI ticketing (a NexusAI seat's job): S53 m2/m3, S54's 8 BACKLOG items, round-3 NEW-3/NEW-4. Also 4 Dependabot alerts (RD-354 owns qs 6.15.2; three need a `gh` identity).
- **Raise with Wednesday (shared tools, coordination only):**
  - `send_brief.sh` refuses a bare "No az/gh" when the launcher runs them;
  - `wake_ack`'s hash includes the countdown;
  - `cockpit.sh add` should refuse when that project's claude already runs;
  - `--self` should refuse while the transcript holds a human line newer than the pickup's last commit;
  - Tuesday replies to Kam could carry `view: both` (or a badge on the other tab);
  - `TASKS.md`'s NEXT PICKUP pointer names her file;
  - `send_brief.sh` `-S4x` names skip the undelivered-ruling gate (trap 52).
- NAS WED-149: `com.tuesday.nassync` stays BOOTED OUT until the partition is built (design `1_Project_Definition/Architecture/2026-09-10_nas-two-seat-sync-check.md`).
- Capacity: if the allowance hits 100%, every seat on both machines stops mid-turn. Recovery reads each seat's transcript and handover, and a cut gate re-runs under a NEW report path.
- **EDGE `48bb744` tier-1 QA gate** (S46 LAUNCH PLAN step 7).
- **Fix the QA launcher template so it names the SENDING inbox** (trap 63), shared tooling, so raise it with Wednesday.
- **The frozen-busy leg re-fires on an unchanged ack hash** (`cd537055e1dc` at 01:29, 01:3x and 01:45 on `%9`). Raise with Wednesday.
- **The S43/S44/S45 merge-round score** is owed at the ONE delta gate.

## s15 RETRO
- **Applied:**
  - verify at the destination for every mail, and at origin for every panel note;
  - rung 5 checked by session id, first-record time and brief path;
  - both gate reports read whole before ruling;
  - the gate before live, and a second gate on the fix;
  - verdict authorship proven from the gate's transcript;
  - no mail during S45's HOLD window;
  - an independent public probe;
  - the pickup kept current at every event;
  - S46 deferred rather than launched to idle.
- **Missed:**
  - repeated the inverted harness-email default in the boot summary without challenging it (Kam corrected it at 06:47:42, transcript);
  - a kill list matched its own shell;
  - the S46 drafting prompt contradicted Tuesday's own C11 ruling (the subagent caught it);
  - s14's first gate brief used a single-marker credential probe (scored against the gate at 0.85).
- **Candidates:** all FILED, none left as a candidate.
  - lesson `2026-09-14_kams-instruction-stands-until-he-withdraws-it` + pinned memory;
  - ledger rows for the kill list and the harness email;
  - traps 59–64;
  - OWED items for the launcher sending inbox and the ack re-fire.

## ✅ DONE IN s15
- 00:05 rotation-in: LIVENESS OK 3/3, `%0` renamed back, no dropped human lines, watcher re-armed.
- 0016 conditional GO (14:13Z) → G45 defect → retarget ruling (14:34Z) → delta gate drafted by a subagent, reviewed, amended, launched and proven at rung 5 → both verdicts read whole and scored → GO (15:53Z) → HEAD / no-mail window → REPORT accepted (16:06Z). Kam warned and told on the panel, both verified at origin.
- S45's checkpoint → S46 deferred; routing row added; S46 brief drafted (`2c5f2f34`); EDGE accepted branch-only; S45 wrap read whole and scored 0.90; `%9` closed (14→14 listeners).
- Ledger 3c archive (rows ≤2026-09-10, conserved); history entry; digests regenerated after the new lesson.
