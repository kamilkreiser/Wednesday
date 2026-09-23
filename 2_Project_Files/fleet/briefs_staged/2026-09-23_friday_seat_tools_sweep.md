# BRIEF — make every seat-aware TOOL recognise a third coordinator seat, FRIDAY (WED)

Commissioned by Wednesday (Studio coordinator), 2026-09-23 ~11:15 AEST, on Kam's words (live board, view=wednesday,
10:49:26, verbatim): *"…I'm thinking of changing the name of my laptop agent to Friday and creating a new folder. That
way the agents won't get confused… create a folder for Friday with all the instructions and a launch file… So create a
new agent called Friday… Friday will work on both Secura and Dataset projects from this laptop."*

WHOSE / WHERE: Wednesday's own repo (WED), `/Volumes/DevMASTER/WEDNESDAY`. **Your files: `2_Project_Files/tools/`,
`2_Project_Files/fleet/` (EXCEPT `fleet/briefs_staged/`, `fleet/state/`, `fleet/qa-agent/`), `2_Project_Files/scheduler/`,
`2_Project_Files/voice/`, `2_Project_Files/doctor.sh`, `2_Project_Files/tests/`.**
**NOT yours, other hands are in them RIGHT NOW:** `2_Project_Files/dashboard-cloud/**` (a builder is adding the friday
seat + `Friday` partition to the live board), `Launch_*.command` at the repo root, `2_Project_Files/friday/`,
`0_Brain/**` (Wednesday). If you need a change there, write it in your report instead.

## THE SEAT, as decided (do not redesign)
- Seat id **`friday`**, display **`Friday`**, tree folder name **`FRIDAY`** (the tree decides — the same rule
  `fleet/cockpit/seat_resolve.sh:seat_from_tree_name` and `Launch_Wednesday.command:44` use; `Friday`/`friday` also accepted).
- Runs on Kam's LAPTOP (sleeps, travels; no Studio services). Launched by `Launch_Friday.command` (exports
  `WED_AGENT=friday`, execs the shared launcher). Works BOTH Secuura and Datasec projects.
- Own inbox **`friday-laptop-agent@agentmail.to`** (created and read back 11:08 today; `friday-agent@` was taken
  outside our org). Add `Friday|friday-laptop-agent@agentmail.to|yes` to `fleet/inbox_routing.conf` beside the
  Wednesday/Tuesday rows (backup first).
- Own daily notes **`0_Brain/daily_friday/`** (Wednesday creates the folder + README), own ledger
  `_ledger_friday.md`, own pickup `NEXT-PICKUP-FRIDAY.md`, own chat stream **`chat_friday.json`**.
- **Live board**: client partition **`Friday`**, view **`friday`**, seat cert `4_Credentials/dashboard-cloud/friday-seat.pem`
  (+ `.crt`). `seat_common.py --seat friday` is being added by the other builder — call it, do not edit it.
- **Cards**: a card created by the friday seat carries `seat: "friday"`; the friday seat rules ONLY cards whose seat is
  friday, and wednesday/tuesday NEVER rule a seat=friday card (their existing Datasec/non-Datasec complement is
  unchanged for every other card). State this in the code comment.
- **Scheduler**: the laptop gets NO scheduled jobs by default. `install_all_jobs.sh` for a friday tree prints
  "friday seat: no scheduled jobs are installed on the laptop" and exits 0 (a clear no-op, not a refusal); the job
  scripts that refuse unknown seats may keep refusing friday, but say so by name.
- **Ornith / night / local-model**: the Studio seat's only — friday never runs them (Kam 2026-09-22 ruled the same for
  Tuesday). The week-instruction first act for friday is Claude agents only.

## THE SITES (measured by Wednesday 11:1x with `git grep -n -i -E 'tuesday\)|"tuesday"|=tuesday|TUESDAY\|'`; RE-MEASURE
yourself, with a positive control, before you start — this list is a frame, not the universe)
seat_resolve.sh · seat_note.sh · chat_reply.sh · _live_board.sh · _kam_live.sh · kam_rulings_today.sh · kam_msgs.sh ·
live_chat_poll.sh · statusline_publish.sh · inbox_digest.sh · send_brief.sh · wake_watch.sh · arm_wake_watch.sh ·
wednesday_rotate.sh (SEAT_LAUNCHER → `Launch_Friday.command`) · rotate_liveness.sh · decision_queue.sh ·
reconcile_rulings.py · panel_sync.sh · chat_streams.py · chat_push.sh · close_wednesday.sh · wake_wednesday.sh ·
shift_change.sh · install_all_jobs.sh · nas_sync.sh · speak.sh · doctor.sh · fleet/hooks/pathguard.py (allow a
`FRIDAY` tree root beside `WEDNESDAY|TUESDAY`) · fleet/hooks/pretooluse_seat_scoped_chat.sh (view=friday is the
friday seat's) · dashboard/server.py (local board: include friday's stream where it enumerates seats, harmlessly).
For EACH: change it so friday behaves correctly per the design above, or leave it with a one-line reason. **Every
"unknown seat → REFUSE" guard stays a refusal for anything that is not wednesday|tuesday|friday** — never widen a guard
to a default.
doctor.sh for a friday tree: skip Studio-only checks exactly as it already does for tuesday (dashboard server, Ornith,
scheduler jobs, NAS), and ADD friday checks: `4_Credentials/.env` has AGENTMAIL_API_KEY; `4_Credentials/dashboard-cloud/
friday-seat.pem` exists 0600; `CLAUDE_CONFIG_DIR` under the tree; the first-run marker `4_Credentials/.friday_configured`
exists (WARN, not fail, with "run Launch_Friday.command — it runs first-time setup").

## RULES (house)
Backups beside every edited file: `<file>.pre-0923-<HHMM>-friday`, HHMM from `$(date +%H%M)` captured in the SAME command
as the `cp`. Never delete. zsh tool, no `cd` (hook refuses), no `timeout`, never `2>/dev/null` on a refusable step.
**Never edit a script that is RUNNING** — `pgrep -f <name>` first; `panel_sync.sh loop`, `wake_watch.sh`,
`live_chat_poll.sh` run on this Studio right now: for those, write the new version to `<file>.tmp`, `bash -n` it, then
`mv` it over (atomic replace — the running process keeps its old inode). **Do NOT stop, restart or re-arm any running
mechanism.** Do NOT commit, push, stash, reset, checkout or pull — Wednesday verifies and commits; another seat commits
concurrently.

## PROOF (each arm must be able to fail)
- Extend the existing arms files that already cover seat resolution (`fleet/tests/seat_daily_note_arms.sh`,
  `tests/wake_coordinator_pane_arms.sh`, `fleet/cockpit/staged/resolver-20260913/resolver_test.sh` if still used) with a
  FRIDAY case, and run them all: old cases still pass, friday cases pass, an unknown tree (`THURSDAY`) still REFUSES.
- For each changed tool, one run with `WED_AGENT=friday` against a SCRATCH copy of the tree or the tool's own
  dry-run/`--where`/`--check` mode proving it picks the friday names (inbox, stream, note dir, launcher), and one with
  `WED_AGENT=wednesday` proving Wednesday is byte-identical to before (the Studio seat is live on these tools now).
- `bash -n` every edited shell script; `python3 -m py_compile` every edited .py.
- **NO live network write**: do not post to the live board, do not send mail, do not tap panes.

## REPORT
`/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/REPORT_2026-09-23_friday-seat-tools.md`: BLUF; a table of every site
(file:line, changed/left, why); backups; the arms run with their outputs (file paths); a NOT-TESTED list (everything
that can only be proven on the laptop itself — say which). Last line of your final message: the report path.
