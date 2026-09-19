#!/usr/bin/env python3
"""capture_ready_mail.py — read-only: list wednesday-agent@ and capture the Secuura/Blockchain READY mail naming #1070..#1076 verbatim
(by message id) to mail_batch1070_ready.md. Key by NAME from the WEDNESDAY .env; never printed. Writes only into this gateset dir.
Refuses (exit 1) unless exactly ONE READY (Seat B 4th) from secuura-blockchain@ names all seven PRs, and it is the 04:30:27Z send.
Derived from gatesets/2026-09-19_gate1061to1069/capture_ready_mail.py (same shape; data changed)."""
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
for _ in range(10):
    q = {'limit': 50}
    if page: q['page_token'] = page
    j = get(base + '?' + urllib.parse.urlencode(q)); msgs += j.get('messages', []); page = j.get('next_page_token')
    if not page or any((m.get('timestamp') or '') < '2026-09-18T23:00' for m in j.get('messages', [])): break
print('listed', len(msgs), 'oldest', min((m.get('timestamp') or '') for m in msgs))
PRS = ['#%d' % n for n in range(1070, 1077)]
SUBJ = '[Secuura/Blockchain -> Wednesday] READY (Seat B 4th): seven PRs, one batch - #1070-#1076'
hits = [m for m in msgs if 'secuura-blockchain@' in str(m.get('from')) and 'READY' in (m.get('subject') or '')
        and (m.get('timestamp') or '') >= '2026-09-19T00:00']
for m in sorted(hits, key=lambda m: m.get('timestamp') or ''): print(m.get('timestamp'), '|', m.get('from'), '|', m.get('subject'), '|', m.get('message_id'))
hits = [m for m in hits if (m.get('subject') or '').startswith(SUBJ)]
if len(hits) != 1: print('REFUSING: want exactly 1 READY (Seat B 4th) hit from secuura-blockchain@ since 00:00Z, got', len(hits)); sys.exit(1)
m = hits[0]; full = get(base + '/' + urllib.parse.quote(m['message_id'], safe=''))
txt = full.get('text') or ''
missing = [p for p in PRS if p not in txt + (m.get('subject') or '')]
if missing: print('REFUSING: the READY does not name', missing); sys.exit(1)
if not (m.get('timestamp') or '').startswith('2026-09-19T04:30:27'): print('REFUSING: not the 04:30:27Z READY', m.get('timestamp')); sys.exit(1)
out = os.path.join(G, 'mail_batch1070_ready.md')
if os.path.exists(out): print('REFUSING: capture exists; never overwrite', out); sys.exit(1)
cap = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
hdrs = full.get('headers') or {}
auth = ' '.join(str(v) for k, v in (hdrs.items() if isinstance(hdrs, dict) else []) if k.lower() == 'authentication-results')
with open(out, 'w', encoding='utf-8') as f:
    f.write('SUBJECT: ' + (m.get('subject') or '') + '\nFROM: ' + str(m.get('from')) + '\nTO: ' + str(full.get('to')) + '\nTS: ' + str(m.get('timestamp'))
            + '\nMESSAGE_ID: ' + m['message_id'] + '\nCAPTURED: ' + cap + ' by the batch 1070-1076 drafter, read-only by message id from wednesday-agent@ (key by name, never printed)'
            + '\nTEXT_SHA256: ' + hashlib.sha256(txt.encode()).hexdigest() + '\n' + txt)
print('written', out, len(txt), 'chars')
print('auth-results:', auth[:400] if auth else '(headers not returned by the API)')
