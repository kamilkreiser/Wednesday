#!/usr/bin/env python3
"""capture_ready_mail.py — read-only: list wednesday-agent@ and capture the Secuura/Blockchain READY (Seat B 7th) mail naming #1092..#1096 verbatim
(by message id) to mail_batch1092_ready.md. Key by NAME from the WEDNESDAY .env; never printed. Writes only into this gateset dir.
Refuses (exit 1) unless exactly ONE READY (Seat B 7th) from secuura-blockchain@ names all five PRs, it is the 15:15:35Z send, and its
message id equals the id pinned below (read by the drafter's listing list_ready_mail.py at 2026-09-20 ~01:18 AEST).
Derived from gatesets/2026-09-19_gate1084to1091/capture_ready_mail.py (same shape; data changed)."""
import hashlib, json, os, sys, urllib.request, urllib.parse, datetime
G = os.path.dirname(os.path.abspath(__file__))
MID = '<010001a0ba3cb33a-906f3722-7595-4120-a36c-a7a80f85d604-000000@email.amazonses.com>'
key = ''
for line in open('/Volumes/DevMASTER/WEDNESDAY/4_Credentials/.env', encoding='utf-8'):
    if line.startswith('AGENTMAIL_API_KEY='): key = line.split('=', 1)[1].strip().strip('"').strip("'")
assert key, 'AGENTMAIL_API_KEY unset'
H = {'Authorization': 'Bearer ' + key}
base = 'https://api.agentmail.to/v0/inboxes/wednesday-agent@agentmail.to/messages'
def get(u): return json.load(urllib.request.urlopen(urllib.request.Request(u, headers=H), timeout=60))
msgs = []; page = None
for _ in range(10):
    q = {'limit': 50}
    if page: q['page_token'] = page
    j = get(base + '?' + urllib.parse.urlencode(q)); msgs += j.get('messages', []); page = j.get('next_page_token')
    if not page or any((m.get('timestamp') or '') < '2026-09-19T12:00' for m in j.get('messages', [])): break
print('listed', len(msgs), 'oldest', min((m.get('timestamp') or '') for m in msgs))
PRS = ['#%d' % n for n in range(1092, 1097)]
SUBJ = '[Secuura/Blockchain -> Wednesday] READY (Seat B 7th)'
hits = [m for m in msgs if 'secuura-blockchain@' in str(m.get('from')) and 'READY' in (m.get('subject') or '')
        and (m.get('timestamp') or '') >= '2026-09-19T12:00']
for m in sorted(hits, key=lambda m: m.get('timestamp') or ''): print(m.get('timestamp'), '|', m.get('from'), '|', m.get('subject'), '|', m.get('message_id'))
hits = [m for m in hits if (m.get('subject') or '').startswith(SUBJ)]
if len(hits) != 1: print('REFUSING: want exactly 1 READY (Seat B 7th) hit from secuura-blockchain@ since 12:00Z, got', len(hits)); sys.exit(1)
m = hits[0]
if m['message_id'] != MID: print('REFUSING: the listed READY is not the pinned message id', m['message_id'], MID); sys.exit(1)
full = get(base + '/' + urllib.parse.quote(MID, safe=''))
txt = full.get('text') or ''
missing = [p for p in PRS if p not in txt + (m.get('subject') or '')]
if missing: print('REFUSING: the READY does not name', missing); sys.exit(1)
if not (m.get('timestamp') or '').startswith('2026-09-19T15:15:35'): print('REFUSING: not the 15:15:35Z READY', m.get('timestamp')); sys.exit(1)
out = os.path.join(G, 'mail_batch1092_ready.md')
if os.path.exists(out): print('REFUSING: capture exists; never overwrite', out); sys.exit(1)
cap = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
hdrs = full.get('headers') or {}
auth = ' '.join(str(v) for k, v in (hdrs.items() if isinstance(hdrs, dict) else []) if k.lower() == 'authentication-results')
with open(out, 'w', encoding='utf-8') as f:
    f.write('SUBJECT: ' + (m.get('subject') or '') + '\nFROM: ' + str(m.get('from')) + '\nTO: ' + str(full.get('to')) + '\nTS: ' + str(m.get('timestamp'))
            + '\nMESSAGE_ID: ' + MID + '\nCAPTURED: ' + cap + ' by the batch 1092-1096 drafter, read-only by message id from wednesday-agent@ (key by name, never printed)'
            + '\nTEXT_SHA256: ' + hashlib.sha256(txt.encode()).hexdigest() + '\n' + txt)
print('written', out, len(txt), 'chars')
print('auth-results:', auth[:400] if auth else '(headers not returned by the API)')
print('json keys (message):', sorted(full.keys()))
