#!/bin/bash
# inbox_digest.sh — summaries-firewall poller for Wednesday's fleet mail.
# WED-42 seamless integration v1. Blueprint: orchestrator-adws adoption #1
# (two-tier summarization: digest by default, raw body only on request).
#
# Usage:
#   inbox_digest.sh                digest of NEW mail (both inboxes) since last run
#   inbox_digest.sh --all          digest ignoring seen-state (last 50 per inbox)
#   inbox_digest.sh --inbound      digest of NEW mail, INBOUND ONLY, unbounded up to the
#                                  fetch limit (50) — prints a LOUD CAP line if every fetched
#                                  message is new (a-cap-is-never-neutral w=16, 2026-09-06: three
#                                  listing caps in one day hid a QUESTION, a READY and a VERDICT).
#                                  Wednesday's own OUTBOUND copies are absorbed (marked seen), not shown.
#   inbox_digest.sh full <inbox> <message_id>   raw body of one message
#   inbox_digest.sh mark-seen      record current mail as seen without printing
#                                  ⚠ SESSION-BASELINE ONLY. Never mid-monitoring:
#                                  it blanket-marks and RACES concurrent arrivals
#                                  (swallowed a live QUESTION 2026-08-04 — see
#                                  learnings/2026-08-04_never-blanket-markseen…)
#
# State: state/seen_ids.txt (gitignored — pre-commit hook also blocks state/).
# Never prints or stores the API key.

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
STATE_DIR="$SCRIPT_DIR/state"
SEEN_FILE="${INBOX_DIGEST_SEEN_FILE:-$STATE_DIR/seen_ids.txt}"   # override = test hook only
mkdir -p "$STATE_DIR"
touch "$SEEN_FILE"

set -a; source "$PROJECT_DIR/4_Credentials/.env" 2>/dev/null; set +a
if [ -z "${AGENTMAIL_API_KEY:-}" ]; then
  echo "ERROR: AGENTMAIL_API_KEY not set (4_Credentials/.env)" >&2; exit 1
fi

INBOXES=("wednesday-agent@agentmail.to" "coagent@agentmail.to")

if [ "${1:-}" = "full" ]; then
  [ $# -eq 3 ] || { echo "usage: $0 full <inbox> <message_id>" >&2; exit 1; }
  MSG_ID_ENC=$(python3 -c "import urllib.parse,sys; print(urllib.parse.quote(sys.argv[1], safe=''))" "$3")
  curl -s "https://api.agentmail.to/v0/inboxes/$2/messages/$MSG_ID_ENC" \
    -H "Authorization: Bearer $AGENTMAIL_API_KEY" | python3 -c "
import json,sys
m=json.load(sys.stdin)
print(f\"From: {m.get('from')}\nTo: {m.get('to')}\nDate: {m.get('timestamp')}\nSubject: {m.get('subject')}\n---\")
print(m.get('text') or m.get('html') or '(no body)')"
  exit 0
fi

MODE="${1:-digest}"

for inbox in "${INBOXES[@]}"; do
  curl -s "https://api.agentmail.to/v0/inboxes/$inbox/messages?limit=50" \
    -H "Authorization: Bearer $AGENTMAIL_API_KEY" | \
  INBOX="$inbox" SEEN_FILE="$SEEN_FILE" MODE="$MODE" python3 -c "
import json, sys, os, re

inbox = os.environ['INBOX']
seen_file = os.environ['SEEN_FILE']
mode = os.environ['MODE']

with open(seen_file) as f:
    seen = set(line.strip() for line in f if line.strip())

d = json.load(sys.stdin)
msgs = d.get('messages', [])
new = [m for m in msgs if m['message_id'] not in seen]

if mode == 'mark-seen':
    with open(seen_file, 'a') as f:
        for m in new:
            f.write(m['message_id'] + '\n')
    sys.exit(0)

show = msgs if mode == '--all' else new
LIMIT = 50
if len(msgs) >= LIMIT and len(new) == len(msgs):
    print(f'⚠ CAP: {inbox} — every one of the {len(msgs)} fetched messages is NEW; the listing may be TRUNCATED at the fetch limit — paginate before trusting it')

if mode == '--inbound':
    n_in = sum(1 for m in new if not re.match(r'\[Wednesday -> ', m.get('subject','')))
    print(f'===== {inbox} — {len(new)} new ({n_in} inbound shown; own outbound copies absorbed) =====')
else:
    print(f'===== {inbox} — {len(new)} new =====')
for m in show:
    subj = m.get('subject', '(no subject)')
    # Routing classification from the subject convention
    tag = 'OTHER'
    client = '-'
    mm = re.match(r'\[([^\]]+) -> Wednesday\]\s*(.*)', subj)
    if mm:
        client = mm.group(1)
        rest = mm.group(2)
        if rest.upper().startswith('QUESTION'): tag = 'QUESTION'
        elif rest.lower().startswith('session wrap'): tag = 'WRAP'
        else: tag = 'INBOUND'
    elif re.match(r'\[Wednesday -> ', subj):
        tag = 'OUTBOUND'
        mo = re.match(r'\[Wednesday -> ([^\]]+)\]', subj)
        if mo: client = mo.group(1)
    if mode == '--inbound' and tag == 'OUTBOUND':
        continue
    preview = (m.get('preview') or '').replace('\n', ' ')[:180]
    print(f\"[{tag}] {m['timestamp'][:16]} | {client} | {subj[:90]}\")
    print(f'        {preview}')
    print(f\"        id: {m['message_id']}\")

# digest / --inbound mark what they just processed as seen (own outbound copies included)
if mode in ('digest', '--inbound'):
    with open(seen_file, 'a') as f:
        for m in new:
            f.write(m['message_id'] + '\n')
"
done
