---
date: 2026-08-06
type: preference
source: Kam (morning, after WED-16's first successful live run)
status: live — PARTLY SUPERSEDED 2026-08-28: the tap is no longer a wrap ORDER for agents with a live queue (see 2026-08-28_overnight-is-working-time); the checkpoint + the 06:00 verification stay
---

# Morning shift change — night crew wraps before Kam starts

**What Kam said:** "please get all agents working to wrap up and finish so that
when I start with them and you I can launch and refresh to start fresh sessions."

**The principle:** the daily rhythm is a *shift change*, not just a wake-up.
Kam's 06:00 start deserves a clean floor: every overnight/lingering session
wrapped (committed, history written, wrap email sent), panes free to be
relaunched fresh. Stale sessions carry stale context — fresh launches re-read
the world (mental-model rule applied to sessions themselves).

**Mechanism (built same session):**
- `2_Project_Files/scheduler/shift_change.sh`, fired 05:30 by
  `com.wednesday.shiftchange` (installed via install_scheduler.command).
- Taps every live fleet pane's prompt (tmux send-keys, same as `cockpit.sh
  say`): agents get the end-of-session instruction; Wednesday's own pane gets
  the overnight-handover instruction. `fleet-monitor` skipped.
- One `[Wednesday -> all agents]` bus mail as the record.
- Guards: once/day, 05:00–05:59 window only (a coalesced late fire must never
  wrap sessions Kam is actively using).
- The 06:00 wake session **verifies** wraps arrived (launcher step 1b) and
  reports any session that didn't.

**Why it matters:** WED-16's value isn't the alarm clock — it's that the whole
fleet breathes on Kam's rhythm. Links: [[2026-08-03_daily-rhythm-6-to-23]],
[[2026-08-03_mental-model-not-source-of-truth]].
