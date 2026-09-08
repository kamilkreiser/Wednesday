#!/bin/bash
# Wednesday's voice — speak a short message aloud to Kam.
#
# Usage: speak.sh "message"            (1-3 sentences, written for the ear)
#        WEDNESDAY_VOICE=Daniel speak.sh "message"   (voice override)
#        WEDNESDAY_MUTE=1 speak.sh "..."             (print instead of speak)
#
# Protocol: 0_Brain/identity/voice-protocol.md. This script is the single seam
# for the TTS backend — upgrade to neural TTS here without changing callers.

set -u

# Voice preference (Kam, 2026-07-31: auditioned and chose Matilda Premium —
# neural en_AU). Fallback chain covers machines without the download
# (PORTABILITY.md item 2). WEDNESDAY_VOICE overrides everything.
if [ -z "${WEDNESDAY_VOICE:-}" ]; then
  INSTALLED="$(say -v '?' 2>/dev/null)"
  if echo "$INSTALLED" | grep -q '^Matilda (Premium)'; then
    VOICE="Matilda (Premium)"
  elif echo "$INSTALLED" | grep -q '^Matilda (Enhanced)'; then
    VOICE="Matilda (Enhanced)"
  elif echo "$INSTALLED" | grep -q '^Moira (Enhanced)'; then
    VOICE="Moira (Enhanced)"
  else
    VOICE="Moira"
  fi
else
  VOICE="$WEDNESDAY_VOICE"
fi
RATE="${WEDNESDAY_RATE:-175}"
MSG="${1:-}"

if [ -z "$MSG" ]; then
  echo "usage: speak.sh \"message\"" >&2
  exit 1
fi

# Log everything spoken (ear-channel audit trail, useful for tuning).
LOG_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)/0_Brain/daily"
printf '%s [spoken] %s\n' "$(date '+%Y-%m-%d %H:%M:%S')" "$MSG" >> "$LOG_DIR/.spoken.log" 2>/dev/null || true

if [ "${WEDNESDAY_MUTE:-0}" = "1" ]; then
  echo "[muted] $MSG"
  exit 0
fi

# Quiet hours (voice-protocol.md + daily-rhythm-6-to-23): NO speech 23:00–06:00
# unless something is genuinely on fire. This was rule-only until 2026-09-07,
# when a fresh 00:16 seat misread the clock as morning and spoke — the rule
# lived nowhere in the path (an-enforcement-you-must-arm; a-promise-is-not-a-
# mechanism). Now it is a guard. Override for a real emergency:
# WEDNESDAY_SPEAK_URGENT=1. WEDNESDAY_TEST_HOUR forces the hour for exercising
# both branches (close-ritual pattern, valid-is-not-delivered).
HOUR="${WEDNESDAY_TEST_HOUR:-$(date +%H)}"
HOUR=$((10#$HOUR))
if [ "${WEDNESDAY_SPEAK_URGENT:-0}" != "1" ] && { [ "$HOUR" -ge 23 ] || [ "$HOUR" -lt 6 ]; }; then
  echo "[quiet hours ${HOUR}:00 — NOT spoken; text stands. Set WEDNESDAY_SPEAK_URGENT=1 only if genuinely on fire] $MSG"
  exit 0
fi

# Background so the calling session never blocks on audio.
say -v "$VOICE" -r "$RATE" "$MSG" >/dev/null 2>&1 &
echo "[spoken:$VOICE] $MSG"
