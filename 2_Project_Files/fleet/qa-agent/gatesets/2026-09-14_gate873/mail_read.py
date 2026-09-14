#!/usr/bin/env python3
"""mail_read.py — reads the READY FOR QA mail for PR #873 from the AgentMail API (key by NAME from Wednesday's .env; never printed).
Writes ready_873.txt (the whole body) and prints headers + auth results. Filter by SUBJECT."""
import json, urllib.request, urllib.parse, sys, datetime, os
ENV = '/Volumes/DevMASTER/WEDNESDAY/4_Credentials/.env'
key = ''
for line in open(ENV, encoding='utf-8'):
    if line.startswith('AGENTMAIL_API_KEY='): key = line.split('=', 1)[1].strip().strip('"').strip("'")
assert key
H = {'Authorization': 'Bearer ' + key}
base = 'https://api.agentmail.to/v0/inboxes/wednesday-agent@agentmail.to/messages'
def get(u):
    return json.load(urllib.request.urlopen(urllib.request.Request(u, headers=H), timeout=60))
print('mail_read', datetime.datetime.now().astimezone().strftime('%H:%M:%S %Z'))
msgs = []
u = base + '?limit=100'
j = get(u)
msgs = j.get('messages', [])
print('listed', len(msgs), 'messages; count field', j.get('count'))
hits = [m for m in msgs if 'READY FOR QA' in (m.get('subject') or '') and '#873' in (m.get('subject') or '')]
print('subject hits for READY FOR QA + #873:', len(hits))
ctl = [m for m in msgs if 'READY FOR QA' in (m.get('subject') or '')]
print('positive control (any READY FOR QA):', len(ctl))
for m in hits:
    print('  ', m.get('timestamp'), '|', m.get('from'), '|', m.get('subject'), '| id', m.get('message_id'))
if not hits: sys.exit(1)
m = sorted(hits, key=lambda x: x.get('timestamp') or '')[-1]
full = get(base + '/' + urllib.parse.quote(m['message_id'], safe=''))
out = os.path.join(sys.argv[1], 'ready_873.txt')
body = full.get('text') or ''
with open(out, 'w', encoding='utf-8') as f:
    f.write('SUBJECT: ' + str(full.get('subject')) + '\n')
    f.write('FROM: ' + str(full.get('from')) + '\n')
    f.write('TIMESTAMP: ' + str(full.get('timestamp')) + '\n')
    f.write('MESSAGE_ID: ' + str(full.get('message_id')) + '\n')
    hdrs = full.get('headers') or {}
    for k in ('authentication-results', 'Authentication-Results', 'received-spf', 'dkim-signature'):
        if k in hdrs: f.write(k + ': ' + str(hdrs[k])[:400] + '\n')
    f.write('\n' + body)
print('wrote', out, 'body chars', len(body), 'lines', body.count('\n'))
ar = ''
hdrs = full.get('headers') or {}
for k, v in hdrs.items():
    if k.lower() == 'authentication-results': ar = str(v)
print('authentication-results:', ar[:300] if ar else '(header not exposed by API; keys: ' + ','.join(sorted(hdrs.keys()))[:300] + ')')
