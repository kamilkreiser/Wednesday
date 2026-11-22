#!/bin/bash
# windows_wo_send.sh — mail a work order (text + optional ONE attachment) from Friday's own inbox
# to the Windows checking seat on Kam's PC, then read it back in the PC's inbox.
#
# WHY A FILE (2026-11-22): WO-1..WO-6 were sent with scratch one-offs that died with each seat.
# send_brief.sh has no attachment and routes to project seats; the PC seat is General/CoAgent only
# (grant: tasks/EXPIRING-GRANTS.md, the "work with the Windows PC" row).
#
# Usage: windows_wo_send.sh '<subject>' <body file> [attachment file]
#   The subject is sent as given: begin it "[Friday -> Windows agent] ".
# Prints: body bytes, attachment bytes + sha256, the send's HTTP code and message id, then the
# read-back from friday-windows-agent@ (subject, attachment name and size). Never prints a key.
# Exit: 0 sent and seen at the destination · 1 send failed · 2 usage/env · 3 sent but NOT seen.
set -u
SELF="$(cd "$(dirname "$0")" && pwd)"; ROOT="$(cd "$SELF/../.." && pwd)"
SUBJ="${1:-}"; BODY="${2:-}"; ATT="${3:-}"
[ -n "$SUBJ" ] && [ -f "$BODY" ] || { echo "usage: windows_wo_send.sh '<subject>' <body file> [attachment file]" >&2; exit 2; }
[ -z "$ATT" ] || [ -f "$ATT" ] || { echo "windows_wo_send: no attachment file at $ATT" >&2; exit 2; }
BB=$(wc -c < "$BODY" | tr -d ' '); [ "$BB" -gt 200 ] || { echo "windows_wo_send: body is only $BB bytes; refusing" >&2; exit 2; }
if grep -q '<<' "$BODY"; then echo "windows_wo_send: the body still holds a << placeholder; refusing" >&2; exit 2; fi
set -a; . "$ROOT/4_Credentials/.env"; set +a
[ -n "${AGENTMAIL_API_KEY:-}" ] && [ -n "${WINDOWS_AGENT_AGENTMAIL_KEY:-}" ] || { echo "windows_wo_send: a mail key is missing in 4_Credentials/.env" >&2; exit 2; }
T="$(mktemp -d "${TMPDIR:-/tmp}/wosend.XXXXXX")" || exit 2
python3 - "$SUBJ" "$BODY" "$ATT" > "$T/payload.json" <<'PY'
import base64, json, os, sys
subj, body, att = sys.argv[1], sys.argv[2], sys.argv[3]
d = {"to": ["friday-windows-agent@agentmail.to"], "subject": subj, "text": open(body, encoding="utf-8").read()}
if att:
    d["attachments"] = [{"filename": os.path.basename(att), "content_type": "application/octet-stream",
                         "content": base64.b64encode(open(att, "rb").read()).decode()}]
json.dump(d, sys.stdout)
PY
[ -s "$T/payload.json" ] || { echo "windows_wo_send: could not build the payload" >&2; exit 2; }
echo "body: $BB bytes, last line: $(tail -n 1 "$BODY" | cut -c1-80)"
[ -z "$ATT" ] || echo "attachment: $(basename "$ATT") $(wc -c < "$ATT" | tr -d ' ') bytes sha256 $(shasum -a 256 "$ATT" | cut -d' ' -f1)"
CODE=$(curl -sS -m 120 -o "$T/send.json" -w '%{http_code}' -X POST "https://api.agentmail.to/v0/inboxes/friday-laptop-agent@agentmail.to/messages/send" \
  -H "Authorization: Bearer $AGENTMAIL_API_KEY" -H 'Content-Type: application/json' --data-binary @"$T/payload.json" 2> "$T/curl.err")
echo "send $CODE"
[ "$CODE" = "200" ] || { echo "windows_wo_send: send failed:" >&2; head -c 400 "$T/send.json" >&2; cat "$T/curl.err" >&2; exit 1; }
python3 -c 'import json,sys; d=json.load(open(sys.argv[1])); print("message_id", d.get("message_id"))' "$T/send.json"
SEEN=1; i=0
while [ $i -lt 6 ]; do
  sleep 5
  curl -sS -m 30 "https://api.agentmail.to/v0/inboxes/friday-windows-agent@agentmail.to/messages?limit=5" -H "Authorization: Bearer $WINDOWS_AGENT_AGENTMAIL_KEY" > "$T/list.json" 2>> "$T/curl.err"
  if python3 - "$T/list.json" "$SUBJ" <<'PY'
import json, sys
try: d = json.load(open(sys.argv[1]))
except Exception as e: print("read-back: not JSON:", e); sys.exit(1)
for m in d.get("messages", []):
    if (m.get("subject") or "") == sys.argv[2]:
        a = m.get("attachments") or []
        print("seen at friday-windows-agent@:", m.get("timestamp", "")[:19], "|", m.get("subject"))
        print("  attachments:", [(x.get("filename"), x.get("size")) for x in a])
        sys.exit(0)
sys.exit(1)
PY
  then SEEN=0; break; fi
  i=$((i+1))
done
[ $SEEN -eq 0 ] || { echo "windows_wo_send: SENT but not seen in the PC's inbox after 30 s" >&2; exit 3; }
exit 0
