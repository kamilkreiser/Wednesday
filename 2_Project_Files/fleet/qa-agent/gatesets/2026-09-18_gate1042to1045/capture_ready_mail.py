#!/usr/bin/env python3
"""capture_ready_mail.py — read-only: list wednesday-agent@ and capture the Secuura/Blockchain READY mail naming #1042..#1045 verbatim
(by message id) to mail_batch1042_ready.md. Key by NAME from the WEDNESDAY .env; never printed. Writes only into this gateset dir."""
import hashlib, json, os, sys, urllib.request, urllib.parse, datetime
G = os.path.dirname(os.path.abspath(__file__))
key = ''
for line in open('/Volumes/DevMASTER/WEDNESDAY/4_Credentials/.env', encoding='utf-8'):
    if line.startswith('AGENTMAIL_API_KEY='): key = line.split('=', 1)[1].strip().strip('"').strip("'")
assert key, 'AGENTMAIL_API_KEY unset'
H = {'Authorization': 'Bearer ' + key}
base = 'https://api.agentmail.to/v0/inboxes/wednesday-agent@agentmail.to/messages'
def get(u): return json.load(urllib.request.urlopen(urllib.request.Request(u, headers=H), timeout=60))
msgs = []; page = None
for _ in range(4):
    q = {'limit': 50}
    if page: q['page_token'] = page
    j = get(base + '?' + urllib.parse.urlencode(q)); msgs += j.get('messages', []); page = j.get('next_page_token')
    if not page: break
print('listed', len(msgs))
hits = [m for m in msgs if all(x in (m.get('subject') or '') for x in ('#1042', '#1043', '#1044', '#1045'))]
for m in sorted(hits, key=lambda m: m.get('timestamp') or ''): print(m.get('timestamp'), '|', m.get('from'), '|', m.get('subject'), '|', m.get('message_id'))
ready = [m for m in hits if 'READY' in (m.get('subject') or '') and 'secuura-blockchain@' in str(m.get('from'))]
if len(ready) != 1: print('REFUSING: want exactly 1 READY hit, got', len(ready)); sys.exit(1)
m = ready[0]; full = get(base + '/' + urllib.parse.quote(m['message_id'], safe=''))
txt = full.get('text') or ''
out = os.path.join(G, 'mail_batch1042_ready.md')
cap = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
with open(out, 'w', encoding='utf-8') as f:
    f.write('SUBJECT: ' + (m.get('subject') or '') + '\nFROM: ' + str(m.get('from')) + '\nTO: ' + str(full.get('to')) + '\nTS: ' + str(m.get('timestamp'))
            + '\nMESSAGE_ID: ' + m['message_id'] + '\nCAPTURED: ' + cap + ' by the batch 1042-1045 drafter, read-only by message id from wednesday-agent@ (key by name, never printed)'
            + '\nTEXT_SHA256: ' + hashlib.sha256(txt.encode()).hexdigest() + '\n' + txt)
print('written', out, len(txt), 'chars')
