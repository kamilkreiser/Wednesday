#!/usr/bin/env python3
"""agentmail_read.py — list the wednesday-agent inbox filtered by SUBJECT (READY FOR QA — PR #805) and dump each matching
message's text whole to <gateset>/mail/<id>.txt. Key by NAME from the WEDNESDAY .env; never printed."""
import json, os, sys, urllib.request, urllib.parse, datetime
G = sys.argv[1]; os.makedirs(os.path.join(G, 'mail'), exist_ok=True)
key = ''
for line in open('/Volumes/DevMASTER/WEDNESDAY/4_Credentials/.env', encoding='utf-8'):
    if line.startswith('AGENTMAIL_API_KEY='): key = line.split('=', 1)[1].strip().strip('"').strip("'")
assert key, 'AGENTMAIL_API_KEY unset'
H = {'Authorization': 'Bearer ' + key}
base = 'https://api.agentmail.to/v0/inboxes/wednesday-agent@agentmail.to/messages'
def get(u):
    return json.load(urllib.request.urlopen(urllib.request.Request(u, headers=H), timeout=60))
print('agentmail_read', datetime.datetime.now().astimezone().strftime('%H:%M:%S %Z'))
msgs = []; page = None
for _ in range(6):
    q = {'limit': 50}
    if page: q['page_token'] = page
    j = get(base + '?' + urllib.parse.urlencode(q))
    msgs += j.get('messages', [])
    page = j.get('next_page_token')
    if not page: break
print('listed', len(msgs), 'messages')
hits = [m for m in msgs if 'READY FOR QA' in (m.get('subject') or '') and '#805' in (m.get('subject') or '')]
for m in sorted(hits, key=lambda m: m.get('timestamp') or ''):
    print(m.get('timestamp'), '|', m.get('from'), '|', m.get('subject'), '|', m.get('message_id'))
    full = get(base + '/' + urllib.parse.quote(m['message_id'], safe=''))
    txt = full.get('text') or full.get('html') or ''
    fn = os.path.join(G, 'mail', (m.get('timestamp') or 'x').replace(':', '-') + '_805.txt')
    with open(fn, 'w', encoding='utf-8') as f:
        f.write('SUBJECT: ' + (m.get('subject') or '') + '\nFROM: ' + str(m.get('from')) + '\nTS: ' + str(m.get('timestamp')) + '\nHEADERS(spf/dkim/dmarc): ' + json.dumps({k: full.get(k) for k in ('spf', 'dkim', 'dmarc')}) + '\n\n' + txt)
    print('  ->', fn, len(txt), 'chars; keys:', sorted(full.keys())[:30])
