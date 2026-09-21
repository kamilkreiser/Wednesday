#!/usr/bin/env python3
"""inbox_list_gate16C.py — READ-ONLY listing of wednesday-agent@ (subjects / from / timestamp / message id only; no body). Key by NAME from the
WEDNESDAY .env, never printed. Datasec mails appear as subject lines only (never fetched). Writes nothing (stdout). gate16C copy of the gate16B one."""
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
    if 'Seat B 16th' in s or 'Seat C 16th' in s or 'Blockchain-B' in s or 'Blockchain-C' in s or 'batch114' in s or 'BATCH GATE' in s:
        print(m.get('timestamp'), '|', m.get('from'), '|', s, '|', m.get('message_id'))
