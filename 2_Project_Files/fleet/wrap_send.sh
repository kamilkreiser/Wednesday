#!/bin/bash
# wrap_send.sh — send Wednesday's OWN wrap/handover mail with the recipient
# fixed BY CONSTRUCTION.
#
# WHY THIS EXISTS (enforcement, not advice): ledger 2026-08-22, mis-send
# family w=2. The 20:15 rotation wrap was hand-built with curl and its full
# body (Datasec/ATTIO state, an incident record, Kam's rulings) ALSO went to
# secuura-blockchain@ under subject "x" — hard-rule-2 content in another
# client's channel, contained at zero reads only because the successor caught
# it within 4 minutes. A wrap mail's recipient must never pass through hands.
#
# WHAT IT ENFORCES:
#   1. Recipient is HARDCODED: wednesday-agent@agentmail.to. There is no --to
#      flag on purpose; a wrap that needs another recipient is not a wrap.
#   2. The subject timestamp is GENERATED at send time (clock-composition
#      family w=24: typed timestamps are composed timestamps).
#   3. Refuses an empty/missing body. stderr is never discarded (2026-08-06).
#
# Usage:
#   wrap_send.sh --label "<from-label>" --topic "<short topic>" --body-file <path>
#     → subject: [Wednesday-<label> -> Wednesday-successor] Session wrap <YYYY-MM-DD HH:MM> — <topic>
#
# Exit codes: 0 sent+verified · 1 refused (usage/body) · 2 env/API error
set -uo pipefail

SELF_DIR="$(cd -P "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd -P "$SELF_DIR/../.." && pwd)"
ENV_FILE="$PROJECT_DIR/4_Credentials/.env"

# The one recipient a Wednesday wrap can have. Not a parameter. Not ever.
WRAP_INBOX="wednesday-agent@agentmail.to"

LABEL=""; TOPIC=""; BODY_FILE=""
while [ $# -gt 0 ]; do
  case "$1" in
    --label) LABEL="${2:-}"; shift 2 ;;
    --topic) TOPIC="${2:-}"; shift 2 ;;
    --body-file) BODY_FILE="${2:-}"; shift 2 ;;
    --to|--recipient|--inbox)
      echo "wrap_send: REFUSED — this tool takes no recipient. Wraps go to $WRAP_INBOX by construction (mis-send w=2, 2026-08-22)." >&2
      exit 1 ;;
    *) echo "wrap_send: unknown arg '$1'" >&2; exit 1 ;;
  esac
done

[ -n "$LABEL" ] || { echo "wrap_send: REFUSED — --label required (e.g. 'morning', 'evening', 'overnight')." >&2; exit 1; }
[ -n "$TOPIC" ] || { echo "wrap_send: REFUSED — --topic required (short subject tail)." >&2; exit 1; }
[ -n "$BODY_FILE" ] && [ -s "$BODY_FILE" ] || { echo "wrap_send: REFUSED — --body-file missing or empty." >&2; exit 1; }

[ -f "$ENV_FILE" ] || { echo "wrap_send: no .env at $ENV_FILE" >&2; exit 2; }
set -a; source "$ENV_FILE"; set +a
[ -n "${AGENTMAIL_API_KEY:-}" ] || { echo "wrap_send: AGENTMAIL_API_KEY empty after sourcing .env" >&2; exit 2; }

# Timestamp GENERATED here, in the send action — never typed by the caller.
STAMP="$(date '+%Y-%m-%d %H:%M')"
SUBJECT="[Wednesday-$LABEL -> Wednesday-successor] Session wrap $STAMP — $TOPIC"

PAYLOAD="$(python3 - "$WRAP_INBOX" "$SUBJECT" "$BODY_FILE" <<'PY'
import json, sys
to, subject, body_file = sys.argv[1], sys.argv[2], sys.argv[3]
body = open(body_file, encoding="utf-8").read()
print(json.dumps({"to": [to], "subject": subject, "text": body}))
PY
)" || { echo "wrap_send: payload build failed" >&2; exit 2; }

HTTP="$(curl -sS -o /tmp/wrap_send_resp.$$ -w '%{http_code}' \
  -X POST "https://api.agentmail.to/v0/inboxes/$WRAP_INBOX/messages/send" \
  -H "Authorization: Bearer $AGENTMAIL_API_KEY" -H "Content-Type: application/json" \
  -d "$PAYLOAD")" || { echo "wrap_send: curl failed" >&2; cat /tmp/wrap_send_resp.$$ >&2 2>/dev/null; rm -f /tmp/wrap_send_resp.$$; exit 2; }

if [ "$HTTP" != "200" ] && [ "$HTTP" != "201" ] && [ "$HTTP" != "202" ]; then
  echo "wrap_send: API returned HTTP $HTTP — NOT sent. Response:" >&2
  cat /tmp/wrap_send_resp.$$ >&2; rm -f /tmp/wrap_send_resp.$$; exit 2
fi
rm -f /tmp/wrap_send_resp.$$

# Verify at the destination (send rc is not delivery — 2026-08-06/valid-is-not-delivered).
sleep 2
FOUND="$(curl -sS "https://api.agentmail.to/v0/inboxes/$WRAP_INBOX/messages?limit=5" \
  -H "Authorization: Bearer $AGENTMAIL_API_KEY" \
  | python3 -c 'import json,sys; subj=sys.argv[1]; d=json.load(sys.stdin); print(sum(1 for m in d.get("messages",[]) if m.get("subject")==subj))' "$SUBJECT")"
if [ "$FOUND" -ge 1 ] 2>/dev/null; then
  echo "sent+verified at $WRAP_INBOX: $SUBJECT"
else
  echo "wrap_send: WARNING — send accepted (HTTP $HTTP) but not yet visible at $WRAP_INBOX. Re-check before relying." >&2
  exit 2
fi
