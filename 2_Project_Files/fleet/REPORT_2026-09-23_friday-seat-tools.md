# REPORT 2026-09-23 — Friday seat: seat-aware tools sweep (builder B)

Saved by Wednesday from the builder's final message (its own write was refused by the harness). Brief:
`fleet/briefs_staged/2026-09-23_friday_seat_tools_sweep.md`.

## BLUF
33 tool files changed + 2 arms files extended + 2 new (`tools/tap_friday.sh`, `tests/friday_seat_tools_arms.sh`).
A FRIDAY tree / `WED_AGENT=friday` gets inbox friday-laptop-agent@ (routing row `Friday|…|yes`), stream
`chat_friday.json`, notes `0_Brain/daily_friday/`, launcher `Launch_Friday.command`, live-board partition `Friday`
(view friday, friday-seat.pem), cards stamped `seat:"friday"` ruled only by friday. The laptop installs NO scheduled
jobs (installers print a no-op, exit 0); wake/shift/NAS refuse friday by name. THURSDAY still refuses everywhere.
Arms: 110 run, 0 fail (1 live-fleet arm skipped by design); wednesday byte-identical to the pre-friday backups.

## Behaviour changes
1. `pathguard.py` refuses Wednesday-shell writes into `/Volumes/*/FRIDAY/**` (override `WED_ALLOW_CROSS_TREE=1`).
2. `kam_rulings_today.sh` withholds view=friday rows from wednesday/tuesday.
3. `panel_sync.sh` / `chat_streams.py` carry `chat_friday.json` once it exists.
4. BUG FIXED in `scheduler/shift_change.sh`: it resolved the seat from `…/2_Project_Files/..` (basename `..`), so on
   the mini (no WED_AGENT under launchd) the 05:30 tap told agents to wrap to wednesday-agent@; now tuesday-agent@.

## Left unchanged (reason)
arm_wake_watch (uses seat_resolve) · pretooluse_seat_scoped_chat (seat-agnostic) · note_entry/speak/session_start_compact
(via seat_note.sh) · tap_tuesday · daily_sweep (refuses all but wednesday) · plist templates · usage_gate (generic) ·
chat_sync/wed_claim/brief_and_launch (no seat logic) · literal "wednesday" pane names in cockpit.sh:90,460,
pane_close.sh:72, pane_prompt_check.sh:29, monitor.sh:213, tap_wednesday.sh:78 (Tuesday has the same gap — follow-up) ·
staged/resolver-20260913 (staged copy) · dashboard/chat.html, cockpit.html (not in brief).

## Backups
35 × `<file>.pre-0923-HHMM-friday` (shift_change.sh has two; original `.pre-0923-1121-friday`). Every edit via `.tmp`
→ `bash -n`/compile → atomic `mv`; running processes left on the old inode (panel_sync, live_chat_poll, nas_sync,
server.py not restarted).

## Arms
friday_seat_tools_arms.sh 61/61 (negative controls H4, L1, U3, Y1) · seat_daily_note_arms.sh 27/27 ·
wake_coordinator_pane_arms.sh 22 PASS 1 SKIP · regressions: reconcile 23/0, inbox_digest 9/0, doctor_exithint 13/0,
doctor_pause_queue 6/0, doctor_root_check 10/0, ornith_status 11/0, nas_sync_retry 0 fail, wake_watch_falsewake 39/0,
rotate_liveness 23/0. Unrelated: exited_seat_arms 10/1 (ARM6 reads the live pane's process tree; no file of this change).
**Wednesday's independent re-run: friday_seat_tools_arms 61/61, seat_daily_note_arms 27/27.**

## Open decisions / gaps
- No `fleet/USAGE_STOP.friday` → Friday inherits Wednesday's cut.
- chat_push view=both still mails Tuesday only.
- Pre-existing: kam_msgs flags Tuesday's own rows as not-addressed; shift_change bus mail always sends from
  wednesday-agent@; chat_streams MBP→tuesday guess (the laptop is Friday's now).
- dashboard-cloud (builder A) must accept `--seat friday` / `--client Friday` in seat_common, post_card, share_file.

## NOT TESTED (laptop-only or awaiting the deploy)
Full chain on a real FRIDAY tree; live API with the real friday-seat.pem (kam readers, poll ticks, chat_reply posts
and --file, cards, reconcile live source); real AgentMail as friday; tap_friday on the laptop cockpit and a real friday
respawn; statusline/usage publishing on the laptop; panel_sync against a real origin; nas_sync as wednesday; server.py
beyond compile; safe_push beyond bash -n + review.
