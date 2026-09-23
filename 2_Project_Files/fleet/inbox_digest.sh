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

# The seat's OWN inbox, plus the legacy shared bus. Keyed on WED_AGENT (exported by
# the launcher), NOT on the hostname — Tuesday will move machines, and a seat that
# polls the other agent's inbox is the 2026-08-13 cross-client capture in a new
# costume. An unknown value falls back to Wednesday's rather than guessing.
# FRIDAY (2026-09-23): the laptop seat reads ITS inbox, looked up from the "Friday" row of
# inbox_routing.conf (friday-laptop-agent@ — `friday-agent@` was taken outside our org, so the
# address is NOT composable from the seat name). A friday seat with no row REFUSES: falling back
# to Wednesday's inbox would be the cross-seat read this block exists to prevent.
case "${WED_AGENT:-wednesday}" in
  tuesday) SELF_INBOX="tuesday-agent@agentmail.to" ;;
  friday)  SELF_INBOX="$(awk -F'|' '$1=="Friday"{print $2; exit}' "$SCRIPT_DIR/inbox_routing.conf")"
           [ -n "$SELF_INBOX" ] || { echo "ERROR: seat friday has no 'Friday' row in fleet/inbox_routing.conf — REFUSING (not reading another seat's inbox)" >&2; exit 1; } ;;
  *)       SELF_INBOX="wednesday-agent@agentmail.to" ;;
esac
INBOXES=("$SELF_INBOX" "coagent@agentmail.to")

if [ "${1:-}" = "full" ]; then
  [ $# -eq 3 ] || { echo "usage: $0 full <inbox> <message_id>" >&2; exit 1; }
  MSG_ID_ENC=$(python3 -c "import urllib.parse,sys; print(urllib.parse.quote(sys.argv[1], safe=''))" "$3")
  curl -s -m 30 "https://api.agentmail.to/v0/inboxes/$2/messages/$MSG_ID_ENC" \
    -H "Authorization: Bearer $AGENTMAIL_API_KEY" | python3 -c "
import json,sys
m=json.load(sys.stdin)
print(f\"From: {m.get('from')}\nTo: {m.get('to')}\nDate: {m.get('timestamp')}\nSubject: {m.get('subject')}\n---\")
print(m.get('text') or m.get('html') or '(no body)')"
  exit 0
fi

MODE="${1:-digest}"

for inbox in "${INBOXES[@]}"; do
  curl -s -m 30 "https://api.agentmail.to/v0/inboxes/$inbox/messages?limit=50" \
    -H "Authorization: Bearer $AGENTMAIL_API_KEY" | \
  INBOX="$inbox" SEEN_FILE="$SEEN_FILE" MODE="$MODE" SEAT="${WED_AGENT:-wednesday}" SELF_INBOX="$SELF_INBOX" python3 -c "
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
# R0 AT THE TOOL LAYER (ledger _ledger_laptop_datasec 2026-09-18, w=4 cross-seat-read family;
# learnings/2026-08-13_shared-bus-tag-filter-or-leak rule 1): the Tuesday seat is Datasec-only, and the
# shared bus carries every client. Filter on the tag BEFORE any subject or preview is printed; the rest
# is a COUNT, so the seat knows mail exists and never sees its text. Wednesday's seat is unchanged.
seat = os.environ.get('SEAT', 'wednesday')
withheld = 0
if seat == 'tuesday' and inbox == 'coagent@agentmail.to':
    # 2026-09-21 01:4x: the old pattern datasec/ missed [QA/Datasec-NexusAI -> Tuesday] (no slash) - a QA gate verdict for HER seat would have been DROPPED. Any datasec keeps.
    keep = [m for m in show if re.search(r'datasec', m.get('subject') or '', re.I)]
    withheld = len(show) - len(keep)
    show = keep
# OWN-OUTBOUND is decided by the SENDER on the Tuesday seat (2026-09-18 round 2). The subject prefix
# '[Wednesday -> ' is what send_brief.sh writes on EVERY send, and it is also how Wednesday titles mail TO
# Tuesday, so on this seat the prefix absorbed her replies as if they were ours and marked them seen, never
# shown (learnings/2026-08-04_never-blanket-markseen-mid-monitoring: a handled-marker may only advance over
# what reached the processor). Wednesday's seat keeps the subject rule, byte-identical.
# FRIDAY (2026-09-23) follows the Tuesday rule: own-outbound = sent FROM its own inbox (SELF_INBOX).
# Friday works BOTH clients, so no client tag filter applies to it on the shared bus.
SEAT_NAME = 'Tuesday' if seat == 'tuesday' else ('Friday' if seat == 'friday' else 'Wednesday')
def is_out(m):
    if seat == 'tuesday':
        return 'tuesday-agent@agentmail.to' in str(m.get('from', ''))
    if seat == 'friday':
        return os.environ.get('SELF_INBOX', '\x00') in str(m.get('from', ''))
    return bool(re.match(r'\[Wednesday -> ', m.get('subject', '')))
LIMIT = 50
if len(msgs) >= LIMIT and len(new) == len(msgs):
    print(f'⚠ CAP: {inbox} — every one of the {len(msgs)} fetched messages is NEW; the listing may be TRUNCATED at the fetch limit — paginate before trusting it')

if mode == '--inbound':
    n_in = sum(1 for m in (show if withheld else new) if not is_out(m))
    print(f'===== {inbox} — {len(new)} new ({n_in} inbound shown; own outbound copies absorbed) =====')
else:
    print(f'===== {inbox} — {len(new)} new =====')

# FRESHNESS LINE (2026-09-23) — '0 new' IS NOT EVIDENCE THAT NO MAIL ARRIVED.
# Measured this morning: this digest reported '0 new' on tuesday-agent@ while a gate
# READY, a CI receipt and a demo receipt sat in the box, ALREADY MARKED SEEN. The
# seen-marker had advanced over mail that never reached a reader — the
# 2026-08-04_never-blanket-markseen-mid-monitoring failure (a handled-marker may only
# advance over what actually reached the processor). The root cause is NOT yet named,
# so this does not pretend to fix it; it makes the failure impossible to MISS by
# printing what is genuinely newest regardless of seen-state. A seat that reads '0 new'
# beside a three-minute-old READY will go and look.
if not new and msgs:
    print(f'        WARNING 0 new, but the box is NOT empty - newest {min(3,len(msgs))} regardless of seen-state:')
    for m in msgs[:3]:
        subj_f = (m.get('subject') or '(no subject)')
        if seat == 'tuesday' and inbox == 'coagent@agentmail.to' and not re.search(r'datasec', subj_f, re.I):
            subj_f = '(other-client, withheld)'
        ts_f = (m.get('timestamp') or '?')[:16]
        print('        . ' + ts_f + ' | ' + subj_f[:78])
if withheld:
    print(f'        ({withheld} other-client message(s) withheld on the shared bus: tag filter for the Tuesday seat; subject and preview not shown)')
for m in show:
    subj = m.get('subject', '(no subject)')
    # Routing classification from the subject convention
    tag = 'OTHER'
    client = '-'
    mm = re.match(r'\[([^\]]+) -> ' + SEAT_NAME + r'\]\s*(.*)', subj)
    if mm:
        client = mm.group(1)
        rest = mm.group(2)
        if rest.upper().startswith('QUESTION'): tag = 'QUESTION'
        elif rest.lower().startswith('session wrap'): tag = 'WRAP'
        else: tag = 'INBOUND'
    elif is_out(m):
        tag = 'OUTBOUND'
        mo = re.match(r'\[Wednesday -> ([^\]]+)\]', subj)
        if mo: client = mo.group(1)
    if mode == '--inbound' and tag == 'OUTBOUND':
        continue
    preview = (m.get('preview') or '').replace('\n', ' ')[:180]
    print(f\"[{tag}] {m['timestamp'][:16]} | {client} | {subj[:90]}\")
    # WEDNESDAY-SEAT MIRROR of the Tuesday tag filter (2026-09-18, the 10:0x seat): this seat reads Datasec mail by
    # SUBJECT ONLY (its boot scope). The shared bus carries every client, so on coagent@ a Datasec-tagged row keeps
    # its subject line (routing needs it) and its BODY PREVIEW is withheld. Tuesday's seat is untouched by this branch.
    # 2026-09-21 01:4x (ledger w=3 of the preview-leak costume, REGRESSION → this is the enforcement): the withhold now covers
    # EVERY inbox (the 09-20 ATTIO digest reached wednesday-agent@ addressed -> Wednesday) and matches datasec anywhere in the
    # subject OR a -> Tuesday] addressee ([QA/Datasec-NexusAI -> Tuesday] has no slash and leaked a gate-verdict preview at 01:3x).
    if seat == 'wednesday' and re.search(r'datasec|->\s*tuesday\]', subj, re.I):
        print('        (preview withheld: Datasec/Tuesday-scope mail, subject only for the Wednesday seat)')
    else:
        print(f'        {preview}')
    print(f\"        id: {m['message_id']}\")

# digest / --inbound mark what they just processed as seen (own outbound copies included)
if mode in ('digest', '--inbound'):
    with open(seen_file, 'a') as f:
        for m in new:
            f.write(m['message_id'] + '\n')
"
done
