#!/bin/bash
# chat_push.sh — push-deliver a Kam chat message AND record the delivery watermark.
#
# WHY (Kam, 2026-08-17 20:01, verbatim: "I've noticed that you read the prompt
# twice... Reading the prompt once is enough."): the server's chat push and the
# watcher's chat backstop both fired on every message, so Wednesday read each
# message twice. The original design accepted duplicates (refire-over-swallow);
# Kam has ruled the duplicate read out.
#
# MECHANISM (keeps the 08-10 ack rule intact — a watermark advances ONLY to an
# event that PROVABLY reached the processor): this wrapper taps via
# tap_wednesday.sh; ONLY on exit 0 (tap delivered into the pane) does it write
# the message's UTC-minute timestamp to state/chat_pushed_through. wake_watch's
# chat leg then skips messages at-or-before that watermark. If the tap is
# log-only (exit 3), fails (exit 1), or this script never runs, the watermark
# does not advance and the backstop fires exactly as before — the de-dup can
# only suppress a wake for a message that was ALREADY delivered.
#
# Usage: chat_push.sh "<message-iso-ts>"   (the ts written into chat_log.json)

set -u
SELF_DIR="$(cd -P "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd -P "$SELF_DIR/../.." && pwd)"
STATE_DIR="$PROJECT_DIR/2_Project_Files/fleet/cockpit/state"
WM_FILE="$STATE_DIR/chat_pushed_through"

TS="${1:?usage: chat_push.sh <message-iso-ts>}"

# Convert the message ts to UTC minute precision (matches wake_watch's compare).
UTC_MIN=$(python3 -c "
import datetime,sys
try:
    t=datetime.datetime.fromisoformat('$TS').astimezone(datetime.timezone.utc)
    print(t.strftime('%Y-%m-%dT%H:%M'))
except Exception:
    print('')" 2>/dev/null)
if [ -z "$UTC_MIN" ]; then
  echo "chat_push: unparseable ts '$TS' — tapping without watermark" >&2
fi

if "$SELF_DIR/tap_wednesday.sh" "[chat-push] New chat message from Kam at $TS — read the dashboard chat now."; then
  if [ -n "$UTC_MIN" ]; then
    mkdir -p "$STATE_DIR"
    # advance-only: never move the watermark backwards
    CUR=$(cat "$WM_FILE" 2>/dev/null || echo "")
    if [ -z "$CUR" ] || [[ "$UTC_MIN" > "$CUR" ]]; then
      printf '%s\n' "$UTC_MIN" > "$WM_FILE"
    fi
  fi
  exit 0
fi
# tap not delivered (guard held / no pane / error): watermark untouched,
# backstop remains armed for this message.
exit $?
