#!/bin/bash
# WED-16 — installs Wednesday's daily-rhythm launchd jobs on THIS Mac.
# Double-click from Finder (or run in a terminal). Idempotent: re-running
# replaces the existing jobs (e.g. after the drive path changes).
#
# What it installs (machine-local, ~/Library/LaunchAgents — PORTABILITY.md #12):
#   com.wednesday.shiftchange → 05:30 daily → shift_change.sh (wrap the night crew: taps live agent panes to run their end-of-session ritual so Kam starts fresh — Kam directive 2026-08-06)
#   com.wednesday.wake   → 06:00 daily → wake_wednesday.sh  (morning session)
#   com.wednesday.close  → 23:00 daily → close_wednesday.sh (day-end stamp + good night)
# The scripts themselves live on-drive; the plists just point at them.
#
# NOTE: launchd runs a missed job when the Mac next WAKES (the scripts guard
# against silly-hour fires). If the Mac may be asleep at 06:00 and you want a
# true wake, run once (optional, needs admin):
#   sudo pmset repeat wakeorpoweron MTWRFSU 05:58:00

set -u

SELF_DIR="$(cd -P "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
AGENTS_DIR="$HOME/Library/LaunchAgents"
mkdir -p "$AGENTS_DIR"

# ── AGENT-AWARE (2026-09-09, Kam ruled `parameterise` on the card
# `wed-scheduler-installer-arms-wednesday-jobs-on-any-machine` at 08:21) ──────────────
# WHAT WAS WRONG: this file used to arm com.wednesday.shiftchange/.wake/.close
# UNCONDITIONALLY and read WED_AGENT only for the NAS job. Tuesday's first boot measured
# the consequence: on her Mac mini, `com.wednesday.wake` would have run
# `Launch_Wednesday.command` OUT OF /Volumes/KK_T9_External_HDD/TUESDAY at 06:00 daily —
# a seat reading Wednesday's ledger and Wednesday's inbox from Tuesday's tree. The
# two-agent case had been thought about for the NAS job and not carried across.
#
# THE LABEL IS NOT ENOUGH. launchd hands a job a minimal environment, so WED_AGENT is
# NOT inherited at fire time — a correctly-labelled com.tuesday.wake would still have
# defaulted to Wednesday inside the script. So every plist now CARRIES WED_AGENT in
# EnvironmentVariables, and the scripts derive their launcher and inbox from it.
AGENT="${WED_AGENT:-wednesday}"
case "$AGENT" in
  wednesday|tuesday) ;;
  *) echo "install_scheduler: REFUSING — WED_AGENT='$AGENT' is not a known agent." >&2
     echo "  Set WED_AGENT=wednesday or WED_AGENT=tuesday. Guessing here arms a job that" >&2
     echo "  boots the wrong seat, which is the failure this parameterisation exists to stop." >&2
     exit 2 ;;
esac
AGENT_TITLE="$(printf '%s' "${AGENT:0:1}" | tr '[:lower:]' '[:upper:]')${AGENT:1}"
LAUNCHER="$(cd -P "$SELF_DIR/../.." && pwd)/Launch_${AGENT_TITLE}.command"
if [ ! -f "$LAUNCHER" ]; then
  echo "install_scheduler: REFUSING — no launcher at $LAUNCHER" >&2
  echo "  WED_AGENT=$AGENT but this tree has no Launch_${AGENT_TITLE}.command. Arming jobs" >&2
  echo "  that cannot find their launcher is how three rituals died silently on 2026-09-07." >&2
  exit 3
fi
echo "agent: $AGENT  ·  launcher: $LAUNCHER"

install_job() {
  local label="$1" script="$2" hour="$3" minute="$4"
  local plist="$AGENTS_DIR/$label.plist"
  cat > "$plist" <<PLIST
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key><string>$label</string>
  <key>ProgramArguments</key>
  <array>
    <string>/bin/bash</string>
    <string>$SELF_DIR/$script</string>
  </array>
  <key>StartCalendarInterval</key>
  <dict>
    <key>Hour</key><integer>$hour</integer>
    <key>Minute</key><integer>$minute</integer>
  </dict>
  <key>RunAtLoad</key><false/>
  <key>EnvironmentVariables</key>
  <dict>
    <key>WED_AGENT</key><string>$AGENT</string>
  </dict>
  <key>StandardOutPath</key><string>$HOME/Library/Logs/${AGENT}_${label##*.}.out</string>
  <key>StandardErrorPath</key><string>$HOME/Library/Logs/${AGENT}_${label##*.}.err</string>
</dict>
</plist>
PLIST
  launchctl bootout "gui/$(id -u)/$label" 2>/dev/null || true
  launchctl bootstrap "gui/$(id -u)" "$plist"
  echo "installed $label → $hour:$(printf '%02d' "$minute") → $script"
}

mkdir -p "$SELF_DIR/logs" "$SELF_DIR/state"
install_job "com.$AGENT.shiftchange" "shift_change.sh" 5 30
install_job "com.$AGENT.wake"  "wake_wednesday.sh"  6  0
install_job "com.$AGENT.close" "close_wednesday.sh" 23 0

# ── Nightly NAS sync (Kam, 2026-09-08 14:57) ──────────────────────────────────────────
# "create a schedule for both agents to sync to the NAS drive at night. Get Tuesday to
# sync at 11pm, and I think you should sync at 3 or 4am. The exact timing is up to you
# so that both drives are current."
# 03:30 for Wednesday: inside the window he gave, and clear of the 05:30 shift change so
# a long leg cannot still be running when the fleet's morning starts.
# The LABEL carries the agent so the two machines cannot collide in launchctl, and
# $SELF_DIR is self-locating so Tuesday's copy installs pointing at her own drive.
if [ "$AGENT" = "tuesday" ]; then NAS_HOUR=23; NAS_MIN=0; else NAS_HOUR=3; NAS_MIN=30; fi
install_job "com.$AGENT.nassync" "nas_sync.sh" "$NAS_HOUR" "$NAS_MIN"

# ── 15:00 daily sweep (Kam, panel 2026-09-10 11:41 + 11:41:58 "Do this at 3pm Sydney time") ──
# "archive items that have been deployed, merged, or completed at the end of the day,
#  and add to this schedule to archive, deploy, or merge any items that are ready to do so."
#
# WEDNESDAY'S SEAT ONLY, and that is not a preference. daily_sweep.sh sweeps the SECUURA
# board and Wednesday's own; arming it as com.tuesday.dailysweep would have the Datasec
# coordinator archiving another client's tickets on a timer — hard rule 2, on a schedule,
# with nobody watching. The script carries its own seat guard too; this is the outer half.
if [ "$AGENT" = "wednesday" ]; then
  install_job "com.$AGENT.dailysweep" "daily_sweep.sh" 15 0
else
  echo "skipped com.$AGENT.dailysweep — the daily sweep is Wednesday's seat only (it sweeps Secuura + WED)"
fi

echo ""
echo "── verification ──"
for label in "com.$AGENT.shiftchange" "com.$AGENT.wake" "com.$AGENT.close" "com.$AGENT.nassync"; do
  if launchctl print "gui/$(id -u)/$label" >/dev/null 2>&1; then
    echo "OK: $label loaded"
  else
    echo "FAILED: $label not loaded"
  fi
done
echo ""
echo "Done. Logs land in: $SELF_DIR/logs/"
