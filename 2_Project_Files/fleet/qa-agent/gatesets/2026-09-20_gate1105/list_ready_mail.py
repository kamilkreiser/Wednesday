#!/usr/bin/env python3
"""list_ready_mail.py — read-only listing of wednesday-agent@ mails from secuura-blockchain@ since 2026-09-20T12:00Z naming Seat A 15th
(subject, ts, message id, authentication results if returned). Prints no body, no key. For the #1105 gate: pins the READY (13:55:07Z) and
STATUS 2 (13:51:06Z) message ids and confirms the saved captures (gate1105_READY_seatA15.txt / _STATUS2_seatA15.txt) equal the API text."""
import hashlib, json, os, urllib.request, urllib.parse
key = ''
for line in open('/Volumes/DevMASTER/WEDNESDAY/4_Credentials/.env', encoding='utf-8'):
    if line.startswith('AGENTMAIL_API_KEY='): key = line.split('=', 1)[1].strip().strip('"').strip("'")
assert key, 'AGENTMAIL_API_KEY unset'
H = {'Authorization': 'Bearer ' + key}
base = 'https://api.agentmail.to/v0/inboxes/wednesday-agent@agentmail.to/messages'
def get(u): return json.load(urllib.request.urlopen(urllib.request.Request(u, headers=H), timeout=60))
G = os.path.dirname(os.path.abspath(__file__))
CAP = {'READY FOR QA (Seat A 15th)': os.path.join(os.path.dirname(G), '2026-09-20_gate1105_READY_seatA15.txt'), 'STATUS 2 (Seat A 15th)': os.path.join(os.path.dirname(G), '2026-09-20_gate1105_STATUS2_seatA15.txt')}
j = get(base + '?limit=50')
for m in j.get('messages', []):
    if 'secuura-blockchain@' in str(m.get('from')) and (m.get('timestamp') or '') >= '2026-09-20T12:00' and 'Seat A 15th' in (m.get('subject') or ''):
        print(m.get('timestamp'), '|', m.get('subject')[:110], '|', m.get('message_id'))
        for tag, path in CAP.items():
            if tag in (m.get('subject') or ''):
                full = get(base + '/' + urllib.parse.quote(m['message_id'], safe=''))
                txt = full.get('text') or ''
                cap = open(path, encoding='utf-8').read()
                body_in_cap = cap.split('\n---\n', 1)[1] if '\n---\n' in cap else ''
                print('   capture', os.path.basename(path), '| api text chars', len(txt), 'sha256', hashlib.sha256(txt.encode()).hexdigest()[:16], '| capture body chars', len(body_in_cap), 'sha256', hashlib.sha256(body_in_cap.encode()).hexdigest()[:16], '| equal (rstrip)', txt.rstrip() == body_in_cap.rstrip())
                auth = str(full.get('authentication_results') or full.get('headers', {}).get('authentication-results') if isinstance(full.get('headers'), dict) else full.get('authentication_results') or '')
                print('   auth-results:', auth[:300] if auth else '(not returned by the API listing; the gate verifies spf/dkim/dmarc at source)')
