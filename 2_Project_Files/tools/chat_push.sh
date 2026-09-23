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

# ── DELIVER TO TUESDAY WHEN THE MESSAGE WAS ADDRESSED TO HER ────────────────
# Kam, 2026-09-09 16:08: "I'm sending instructions to Tuesday using the Tuesday
# tab, and it looks like it's coming to you but not necessarily to Tuesday."
#
# MEASURED, and he was right: all five of his 15:37-16:07 messages carried
# view='tuesday' in chat_kam.json. The panel STORES the tab; this script IGNORED
# it and tapped Wednesday's pane unconditionally. Written 2026-08-17 when there
# was one agent; the 09-08 split made it wrong with nothing failing.
#
# THE DEEPER HALF: Tuesday runs on ANOTHER MACHINE, so her pane is not in this
# tmux at all — a tap could never have reached her however well it was routed.
# EMAIL is the only cross-machine channel this fleet has, and it is the one both
# seats have used all day. So a tuesday-addressed message is MAILED to her inbox.
#
# WHAT DELIBERATELY DOES NOT CHANGE:
#  · Wednesday is still tapped for EVERY message, including Tuesday's. That is
#    not noise — Kam's conversations with agents are the coordinator's
#    supervision surface (2026-08-10), and it keeps the relay-by-hand that has
#    been the only working path today as a BACKSTOP behind the new direct one.
#  · The watermark still advances only on a delivered Wednesday tap. Unchanged.
#  · A missing view, 'wednesday' or 'both' behaves exactly as before.
# Best-effort and non-blocking by construction: this runs detached from the HTTP
# response, every call is time-bounded, and a mail failure is LOGGED, never
# raised — a delivery problem must not cost Kam his tap.
VIEW="$(printf '%s' "${2:-}" | tr '[:upper:]' '[:lower:]')"
PUSHLOG="$PROJECT_DIR/2_Project_Files/logs/chat_push.log"
mkdir -p "$(dirname "$PUSHLOG")" 2>/dev/null || PUSHLOG=/dev/null
# FRIDAY (2026-09-23, Kam 10:49): a third seat on the LAPTOP — another machine, like Tuesday, so
# a view=friday message is MAILED to Friday's inbox (the "Friday" row of inbox_routing.conf) by
# the SAME code path. `both` is left exactly as it was (Tuesday only): its name is the two-seat
# broadcast, and whether a local-board broadcast should also mail the laptop is Kam's call, not
# a side effect of adding a seat. Friday reads broadcasts on the LIVE board (partition ALL).
# The Tuesday lines below are byte-identical in the log ("tuesday-push: ...").
push_to_seat() { # $1 = routing key (Tuesday|Friday)
  local NAME="$1" TAG ENVF KEY RCPT BODY CODE
  TAG="$(printf '%s' "$NAME" | tr '[:upper:]' '[:lower:]')-push"
    ENVF="$PROJECT_DIR/4_Credentials/.env"
    KEY="$(sed -n 's/^[[:space:]]*AGENTMAIL_API_KEY[[:space:]]*=[[:space:]]*//p' "$ENVF" 2>/dev/null | tr -d '"'"'"' \r' | head -1)"
    if [ -z "$KEY" ]; then
      printf '%s %s: AGENTMAIL_API_KEY not readable at %s — NOT delivered\n' \
        "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$TAG" "$ENVF" >> "$PUSHLOG" 2>/dev/null
    else
      RCPT="$(awk -F'|' -v k="$NAME" '$1==k{print $2; exit}' "$PROJECT_DIR/2_Project_Files/fleet/inbox_routing.conf" 2>/dev/null)"
      if [ -z "$RCPT" ]; then
        printf '%s %s: no %s row in inbox_routing.conf — NOT delivered\n' \
          "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$TAG" "$NAME" >> "$PUSHLOG" 2>/dev/null
      else
        BODY="$(TS="$TS" PD="$PROJECT_DIR" SEATNAME="$NAME" python3 - <<'PYEOF' 2>>"$PUSHLOG"
import json, os
ts = os.environ["TS"]
p = os.path.join(os.environ["PD"], "0_Brain/dashboard/data/chat_kam.json")
try:
    entries = json.load(open(p))
except Exception:
    entries = []
hit = next((e for e in reversed(entries) if e.get("ts") == ts), None)
text = (hit or {}).get("text", "")
print(json.dumps(
    "Kam addressed this to you on the " + os.environ.get("SEATNAME", "Tuesday") + " tab of the dashboard panel at "
    + ts + ". Delivered by the panel itself, not relayed by Wednesday.\n\n"
    "HIS WORDS, VERBATIM:\n\n" + text +
    "\n\n(If this is empty, the panel could not read the message back — open "
    "0_Brain/dashboard/data/chat_kam.json at that timestamp.)"))
PYEOF
)"
        [ -n "$BODY" ] || BODY='"(panel could not compose the body — read chat_kam.json)"'
        CODE="$(curl -s -o /dev/null -w '%{http_code}' --max-time 20 -X POST \
          "https://api.agentmail.to/v0/inboxes/${RCPT}/messages/send" \
          -H "Authorization: Bearer $KEY" -H "Content-Type: application/json" \
          -d "{\"to\":[\"${RCPT}\"],\"subject\":\"[Kam -> ${NAME}] panel message ${TS}\",\"text\":${BODY}}" \
          2>>"$PUSHLOG")"
        printf '%s %s: %s -> HTTP %s\n' \
          "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$TAG" "$RCPT" "${CODE:-none}" >> "$PUSHLOG" 2>/dev/null
      fi
    fi
}
case "$VIEW" in
  tuesday|both) push_to_seat Tuesday ;;
  friday)       push_to_seat Friday ;;
esac

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
