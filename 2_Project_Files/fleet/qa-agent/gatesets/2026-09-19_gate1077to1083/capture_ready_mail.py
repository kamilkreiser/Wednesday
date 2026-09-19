#!/usr/bin/env python3
"""capture_ready_mail.py — read-only: list wednesday-agent@ and capture the Secuura/Blockchain READY mail naming #1077..#1083 verbatim
(by message id) to mail_batch1077_ready.md. Key by NAME from the WEDNESDAY .env; never printed. Writes only into this gateset dir.
Refuses (exit 1) unless exactly ONE READY (Seat B 5th) from secuura-blockchain@ names all seven PRs, it is the 07:48:28Z send, and its
message id equals the one Wednesday handed the drafter (scratchpad/ready5_mid.txt).
Derived from gatesets/2026-09-19_gate1070to1076/capture_ready_mail.py (same shape; data changed; + the handed-id assertion)."""
import hashlib, json, os, sys, urllib.request, urllib.parse, datetime
G = os.path.dirname(os.path.abspath(__file__))
MID = open('/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/f8582263-fac0-44c3-8d2a-6ed1809e5766/scratchpad/ready5_mid.txt').read().strip()
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
    if not page or any((m.get('timestamp') or '') < '2026-09-19T03:00' for m in j.get('messages', [])): break
print('listed', len(msgs), 'oldest', min((m.get('timestamp') or '') for m in msgs))
PRS = ['#%d' % n for n in range(1077, 1084)]
SUBJ = '[Secuura/Blockchain -> Wednesday] READY (Seat B 5th): seven PRs, one batch - #1077-#1083'
hits = [m for m in msgs if 'secuura-blockchain@' in str(m.get('from')) and 'READY' in (m.get('subject') or '')
        and (m.get('timestamp') or '') >= '2026-09-19T04:00']
for m in sorted(hits, key=lambda m: m.get('timestamp') or ''): print(m.get('timestamp'), '|', m.get('from'), '|', m.get('subject'), '|', m.get('message_id'))
hits = [m for m in hits if (m.get('subject') or '').startswith(SUBJ)]
if len(hits) != 1: print('REFUSING: want exactly 1 READY (Seat B 5th) hit from secuura-blockchain@ since 04:00Z, got', len(hits)); sys.exit(1)
m = hits[0]
if m['message_id'] != MID: print('REFUSING: the listed READY is not the handed message id', m['message_id'], MID); sys.exit(1)
full = get(base + '/' + urllib.parse.quote(MID, safe=''))
txt = full.get('text') or ''
missing = [p for p in PRS if p not in txt + (m.get('subject') or '')]
if missing: print('REFUSING: the READY does not name', missing); sys.exit(1)
if not (m.get('timestamp') or '').startswith('2026-09-19T07:48:28'): print('REFUSING: not the 07:48:28Z READY', m.get('timestamp')); sys.exit(1)
out = os.path.join(G, 'mail_batch1077_ready.md')
if os.path.exists(out): print('REFUSING: capture exists; never overwrite', out); sys.exit(1)
cap = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
hdrs = full.get('headers') or {}
auth = ' '.join(str(v) for k, v in (hdrs.items() if isinstance(hdrs, dict) else []) if k.lower() == 'authentication-results')
with open(out, 'w', encoding='utf-8') as f:
    f.write('SUBJECT: ' + (m.get('subject') or '') + '\nFROM: ' + str(m.get('from')) + '\nTO: ' + str(full.get('to')) + '\nTS: ' + str(m.get('timestamp'))
            + '\nMESSAGE_ID: ' + MID + '\nCAPTURED: ' + cap + ' by the batch 1077-1083 drafter, read-only by message id from wednesday-agent@ (key by name, never printed)'
            + '\nTEXT_SHA256: ' + hashlib.sha256(txt.encode()).hexdigest() + '\n' + txt)
print('written', out, len(txt), 'chars')
print('auth-results:', auth[:400] if auth else '(headers not returned by the API)')
print('json keys (message):', sorted(full.keys()))
