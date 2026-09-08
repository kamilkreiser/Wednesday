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
  <key>StandardOutPath</key><string>$HOME/Library/Logs/wednesday_${label##*.}.out</string>
  <key>StandardErrorPath</key><string>$HOME/Library/Logs/wednesday_${label##*.}.err</string>
</dict>
</plist>
PLIST
  launchctl bootout "gui/$(id -u)/$label" 2>/dev/null || true
  launchctl bootstrap "gui/$(id -u)" "$plist"
  echo "installed $label → $hour:$(printf '%02d' "$minute") → $script"
}

mkdir -p "$SELF_DIR/logs" "$SELF_DIR/state"
install_job "com.wednesday.shiftchange" "shift_change.sh" 5 30
install_job "com.wednesday.wake"  "wake_wednesday.sh"  6  0
install_job "com.wednesday.close" "close_wednesday.sh" 23 0

# ── Nightly NAS sync (Kam, 2026-09-08 14:57) ──────────────────────────────────────────
# "create a schedule for both agents to sync to the NAS drive at night. Get Tuesday to
# sync at 11pm, and I think you should sync at 3 or 4am. The exact timing is up to you
# so that both drives are current."
# 03:30 for Wednesday: inside the window he gave, and clear of the 05:30 shift change so
# a long leg cannot still be running when the fleet's morning starts.
# The LABEL carries the agent so the two machines cannot collide in launchctl, and
# $SELF_DIR is self-locating so Tuesday's copy installs pointing at her own drive.
NAS_AGENT="${WED_AGENT:-wednesday}"
if [ "$NAS_AGENT" = "tuesday" ]; then NAS_HOUR=23; NAS_MIN=0; else NAS_HOUR=3; NAS_MIN=30; fi
install_job "com.${NAS_AGENT}.nassync" "nas_sync.sh" "$NAS_HOUR" "$NAS_MIN"

echo ""
echo "── verification ──"
for label in com.wednesday.shiftchange com.wednesday.wake com.wednesday.close "com.${NAS_AGENT}.nassync"; do
  if launchctl print "gui/$(id -u)/$label" >/dev/null 2>&1; then
    echo "OK: $label loaded"
  else
    echo "FAILED: $label not loaded"
  fi
done
echo ""
echo "Done. Logs land in: $SELF_DIR/logs/"
