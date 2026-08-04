#!/bin/bash
# WED-16 — 06:00 scheduled wake. Fired by launchd (com.wednesday.wake).
# Opens a full interactive Wednesday session via the normal launcher; the boot
# ritual does the rest (greeting, briefing, day plan). A marker file tells the
# launcher this is the SCHEDULED morning wake so the session knows to lead
# with the morning briefing + contemplation/consolidation slot.
#
# Guards: once per day · never before 06:00 · not after noon (launchd coalesces
# missed jobs to next Mac wake — a "morning" briefing at 22:00 would be silly).
# Portability: everything here is on-drive; only the plist is machine-local
# (PORTABILITY.md item 12, installed by install_scheduler.command).

set -u

SELF_DIR="$(cd -P "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd -P "$SELF_DIR/../.." && pwd)"
LOG_DIR="$SELF_DIR/logs"
STATE_DIR="$SELF_DIR/state"
mkdir -p "$LOG_DIR" "$STATE_DIR"
LOG="$LOG_DIR/wake_$(date +%F).log"
log() { echo "$(date '+%F %T') $*" >> "$LOG"; }

TODAY="$(date +%F)"
HOUR="$((10#$(date +%H)))"

if [ -f "$STATE_DIR/last_wake" ] && [ "$(cat "$STATE_DIR/last_wake")" = "$TODAY" ]; then
  log "skip: already woke today"
  exit 0
fi
if [ "$HOUR" -lt 6 ]; then
  log "skip: before 06:00 (quiet hours)"
  exit 0
fi
if [ "$HOUR" -ge 12 ]; then
  log "skip: past noon — coalesced fire too late for a morning briefing"
  exit 0
fi
if [ ! -f "$PROJECT_DIR/Launch_Wednesday.command" ]; then
  log "ERROR: launcher not found at $PROJECT_DIR — drive renamed?"
  exit 1
fi

echo "morning" > "$STATE_DIR/wake_mode"     # consumed (deleted) by the launcher
echo "$TODAY" > "$STATE_DIR/last_wake"

if [ "${WEDNESDAY_DRYRUN:-0}" = "1" ]; then
  log "DRYRUN: would open $PROJECT_DIR/Launch_Wednesday.command (wake_mode=morning)"
  rm -f "$STATE_DIR/wake_mode"
  exit 0
fi

log "opening Wednesday session (morning wake)"
open -a Terminal "$PROJECT_DIR/Launch_Wednesday.command"
