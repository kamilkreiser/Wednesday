#!/usr/bin/env python3
"""capture_ready_mail.py — read-only: capture the Secuura/Blockchain READY (Seat B 8th) mail naming #1097..#1099 verbatim (by message id) from
wednesday-agent@ to mail_batch1097_ready.md. Key by NAME from the WEDNESDAY .env; never printed. Writes only into this gateset dir.
Refuses (exit 1) unless exactly ONE READY (Seat B 8th) from secuura-blockchain@ names all three PRs, it is the 18:38:22Z send, and its message id
equals the id pinned below (read by list_ready_mail.py at 2026-09-19T18:41Z). Derived from gatesets/2026-09-20_gate1092to1096/capture_ready_mail.py."""
import hashlib, json, os, sys, urllib.request, urllib.parse, datetime
G = os.path.dirname(os.path.abspath(__file__))
MID = '<010001a0baf65c8a-af774173-f73c-4a9f-a7fe-bde133faa3ec-000000@email.amazonses.com>'
key = ''
for line in open('/Volumes/DevMASTER/WEDNESDAY/4_Credentials/.env', encoding='utf-8'):
    if line.startswith('AGENTMAIL_API_KEY='): key = line.split('=', 1)[1].strip().strip('"').strip("'")
assert key, 'AGENTMAIL_API_KEY unset'
H = {'Authorization': 'Bearer ' + key}
base = 'https://api.agentmail.to/v0/inboxes/wednesday-agent@agentmail.to/messages'
def get(u): return json.load(urllib.request.urlopen(urllib.request.Request(u, headers=H), timeout=60))
msgs = get(base + '?limit=50').get('messages', [])
print('listed', len(msgs), 'oldest', min((m.get('timestamp') or '') for m in msgs))
PRS = ['#%d' % n for n in range(1097, 1100)]
SUBJ = '[Secuura/Blockchain -> Wednesday] READY (Seat B 8th)'
hits = [m for m in msgs if 'secuura-blockchain@' in str(m.get('from')) and (m.get('subject') or '').startswith(SUBJ)]
for m in hits: print(m.get('timestamp'), '|', m.get('from'), '|', m.get('subject'), '|', m.get('message_id'))
if len(hits) != 1: print('REFUSING: want exactly 1 READY (Seat B 8th) from secuura-blockchain@, got', len(hits)); sys.exit(1)
m = hits[0]
if m['message_id'] != MID: print('REFUSING: the listed READY is not the pinned message id', m['message_id'], MID); sys.exit(1)
if not (m.get('timestamp') or '').startswith('2026-09-19T18:38:22'): print('REFUSING: not the 18:38:22Z READY', m.get('timestamp')); sys.exit(1)
full = get(base + '/' + urllib.parse.quote(MID, safe=''))
txt = full.get('text') or ''
missing = [p for p in PRS if p not in txt + (m.get('subject') or '')]
if missing: print('REFUSING: the READY does not name', missing); sys.exit(1)
out = os.path.join(G, 'mail_batch1097_ready.md')
if os.path.exists(out): print('REFUSING: capture exists; never overwrite', out); sys.exit(1)
cap = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
auth = str(full.get('authentication_results') or '')
with open(out, 'w', encoding='utf-8') as f:
    f.write('SUBJECT: ' + (m.get('subject') or '') + '\nFROM: ' + str(m.get('from')) + '\nTO: ' + str(full.get('to')) + '\nTS: ' + str(m.get('timestamp'))
            + '\nMESSAGE_ID: ' + MID + '\nCAPTURED: ' + cap + ' by the batch 1097-1099 drafter, read-only by message id from wednesday-agent@ (key by name, never printed)'
            + '\nTEXT_SHA256: ' + hashlib.sha256(txt.encode()).hexdigest() + '\n' + txt)
print('written', out, len(txt), 'chars')
print('auth-results:', auth[:400] if auth else '(not returned)')
