#!/usr/bin/env python3
"""mail_read.py — READ-ONLY: list wednesday-agent@agentmail.to messages, find Seat B's HEAD MOVED mail for #1022, save it verbatim
(subject, timestamp, from, auth, text) to mail_1022_head_moved.md. AGENTMAIL_API_KEY read by NAME, never printed. GET only."""
import json, urllib.request, urllib.parse, os
GS = os.path.dirname(os.path.abspath(__file__))
key = next(l.split('=', 1)[1].strip().strip('"').strip("'") for l in open('/Volumes/DevMASTER/WEDNESDAY/4_Credentials/.env') if l.startswith('AGENTMAIL_API_KEY='))
print('AGENTMAIL_API_KEY: set')
def get(p): return json.load(urllib.request.urlopen(urllib.request.Request('https://api.agentmail.to/v0/inboxes/wednesday-agent@agentmail.to/' + p, headers={'Authorization': 'Bearer ' + key}), timeout=60))
msgs = get('messages?limit=50').get('messages', [])
print('listed', len(msgs))
hits = [m for m in msgs if '1022' in (m.get('subject') or '') and 'MOVED' in (m.get('subject') or '').upper()]
for m in msgs[:15]: print(' ', m.get('timestamp'), (m.get('subject') or '')[:110])
assert hits, 'no HEAD MOVED #1022 mail found'
m = get('messages/' + urllib.parse.quote(hits[0]['message_id'], safe=''))
auth = {k: m.get(k) for k in ('spf', 'dkim', 'dmarc') if k in m}
hdr = m.get('headers') or {}
ar = hdr.get('Authentication-Results') or hdr.get('authentication-results')
txt = 'SUBJECT: %s\nTS: %s\nFROM: %s\nMESSAGE_ID: %s\nAUTH: %s\nAUTH-RESULTS-HEADER: %s\n\n%s' % (m.get('subject'), m.get('timestamp'), m.get('from'), m.get('message_id'), json.dumps(auth), ar, m.get('text') or m.get('extracted_text') or '')
open(GS + '/mail_1022_head_moved.md', 'w').write(txt)
print('saved', len(txt), 'chars; subject', m.get('subject'), '| ts', m.get('timestamp'), '| keys', sorted(m.keys())[:30])
