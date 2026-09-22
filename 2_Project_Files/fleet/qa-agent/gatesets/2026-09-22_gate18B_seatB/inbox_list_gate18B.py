#!/usr/bin/env python3
"""inbox_list_gate18B.py — READ-ONLY listing of wednesday-agent@ (subjects / from / timestamp / message id only; no body). Key by NAME from the
WEDNESDAY .env, never printed. Datasec mails appear as subject lines only (never fetched). Writes nothing (stdout). gate18B copy of the gate18C one
(filter re-keyed to the 18th round: Seat B 18th / Seat C 18th / Blockchain-B / Blockchain-C / #1036 / batch1167 / BATCH GATE)."""
import json, os, urllib.request, sys
key = ''
for line in open('/Volumes/DevMASTER/WEDNESDAY/4_Credentials/.env', encoding='utf-8'):
    if line.startswith('AGENTMAIL_API_KEY='): key = line.split('=', 1)[1].split('#')[0].strip().strip('"').strip("'")
assert key, 'AGENTMAIL_API_KEY unset'
H = {'Authorization': 'Bearer ' + key}
base = 'https://api.agentmail.to/v0/inboxes/wednesday-agent@agentmail.to/messages'
lim = int(sys.argv[1]) if len(sys.argv) > 1 else 150
r = json.load(urllib.request.urlopen(urllib.request.Request(base + '?limit=%d' % lim, headers=H), timeout=60))
msgs = r.get('messages', [])
print('listed', len(msgs), 'count', r.get('count'), 'oldest', min((m.get('timestamp') or '') for m in msgs) if msgs else '-')
for m in sorted(msgs, key=lambda x: x.get('timestamp') or ''):
    s = m.get('subject') or ''
    if 'Seat B 18th' in s or 'Seat C 18th' in s or 'Blockchain-B' in s or 'Blockchain-C' in s or 'batch116' in s or 'batch117' in s or 'BATCH GATE' in s or '#1036' in s:
        print(m.get('timestamp'), '|', m.get('from'), '|', s, '|', m.get('message_id'))
