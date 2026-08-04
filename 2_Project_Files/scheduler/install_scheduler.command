#!/bin/bash
# WED-16 — installs Wednesday's daily-rhythm launchd jobs on THIS Mac.
# Double-click from Finder (or run in a terminal). Idempotent: re-running
# replaces the existing jobs (e.g. after the drive path changes).
#
# What it installs (machine-local, ~/Library/LaunchAgents — PORTABILITY.md #12):
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
  <key>StandardOutPath</key><string>$SELF_DIR/logs/launchd_$label.out</string>
  <key>StandardErrorPath</key><string>$SELF_DIR/logs/launchd_$label.err</string>
</dict>
</plist>
PLIST
  launchctl bootout "gui/$(id -u)/$label" 2>/dev/null || true
  launchctl bootstrap "gui/$(id -u)" "$plist"
  echo "installed $label → $hour:$(printf '%02d' "$minute") → $script"
}

mkdir -p "$SELF_DIR/logs" "$SELF_DIR/state"
install_job "com.wednesday.wake"  "wake_wednesday.sh"  6  0
install_job "com.wednesday.close" "close_wednesday.sh" 23 0

echo ""
echo "── verification ──"
for label in com.wednesday.wake com.wednesday.close; do
  if launchctl print "gui/$(id -u)/$label" >/dev/null 2>&1; then
    echo "OK: $label loaded"
  else
    echo "FAILED: $label not loaded"
  fi
done
echo ""
echo "Done. Logs land in: $SELF_DIR/logs/"
