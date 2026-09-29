#!/usr/bin/env python3
"""capture_mail_gate43.py — the gate43 CAPTURE: the author's five STATUS "branch N of 6 RAISED" mails (one per PR — the CLAIMS; Seat B 44th sent no
single READY for the batch) and Wednesday's LAUNCH BRIEF to Seat B 43rd (context: the tiering and the Spark raises), each READ BY ID
(AgentMail GET /v0/inboxes/<inbox>/messages/<id>; read-only, touches no seen-state) and written VERBATIM with its TEXT_SHA256 into
mail_gate43_ready.md beside this script. Ids from ONE read-only listing (_mail_list_1.out). The key is read by name and never printed.
Each claim mail must name its PR's pinned head prefix (12 hex) — a mismatch is a problem (rc 1). Usage: capture_mail_gate43.py"""
import hashlib, json, os, urllib.request, urllib.parse, datetime
G = os.path.dirname(os.path.abspath(__file__))
W = 'wednesday-agent@agentmail.to'
MAILS = [
 ('<010001a0ebe80f2d-96163ace-2c96-4f92-9eab-5298a24c15de-000000@email.amazonses.com>', 'CLAIM #1341 (branch 1 of 6)', 'bf0dfa64a424'),
 ('<010001a0ebef721a-66fc6bc1-7d6f-48e4-b2d2-47ee8d895042-000000@email.amazonses.com>', 'CLAIM #1342 (branch 2 of 6)', 'add62ea81146'),
 ('<010001a0ebf67cb3-349ef667-e8dd-4e88-bf85-fc3a53d01882-000000@email.amazonses.com>', 'CLAIM #1343 (branch 3 of 6)', '6600514d61ef'),
 ('<010001a0ec06390b-45fc3036-74dd-477b-a7f1-b721f590a593-000000@email.amazonses.com>', 'CLAIM #1344 (branch 4 of 6)', 'ca4aab7f3b33'),
 ('<010001a0ec0e230f-c4289232-749e-41ac-b6c7-baee6a9be961-000000@email.amazonses.com>', 'CLAIM #1345 (branch 5 of 6)', '052f4a3b9c56'),
 ('<010001a0ec10a7f5-a656776a-a039-49e2-ae0d-94d825e4833b-000000@email.amazonses.com>', 'CONTEXT (Wednesday ANSWER to branch 5: the wrap)', ''),
 ('<010001a0ea9586cb-e435dbaa-9523-4380-ae2b-f3345c40a5a1-000000@email.amazonses.com>', 'CONTEXT (Wednesday LAUNCH BRIEF to Seat B 43rd: the six items)', ''),
]
key = ''
for l in open('/Volumes/DevMASTER/WEDNESDAY/4_Credentials/.env', encoding='utf-8'):
    if l.startswith('AGENTMAIL_API_KEY='): key = l.split('=', 1)[1].strip().strip('"').strip("'")
assert key, 'AGENTMAIL_API_KEY unset'
P = json.load(open(os.path.join(G, 'pins_gate43.json'), encoding='utf-8'))
out = ['# gate43 CAPTURE — seven mails read by id, VERBATIM', '',
       'Captured %s by capture_mail_gate43.py. Each block: role, inbox, id, from, timestamp, subject, TEXT_SHA256, then the text VERBATIM.' % datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'), '',
       '#1341 is KS-1375 (Refs KS-1368 too). #1342 is KS-1369. #1343 is KS-1371. #1344 is KS-1359. #1345 is KS-1360.', '',
       'The pinned heads, in full (pins_gate43.json): ' + ' | '.join('#%s %s' % (n, P['prs'][n]['head']) for n in P['order']), '']
bad = 0
for mid, role, pre in MAILS:
    m = json.load(urllib.request.urlopen(urllib.request.Request('https://api.agentmail.to/v0/inboxes/%s/messages/%s' % (W, urllib.parse.quote(mid, safe='')), headers={'Authorization': 'Bearer ' + key}), timeout=60))
    t = m.get('text') or m.get('extracted_text') or ''
    ok = (not pre) or (pre in (m.get('subject') or '') or pre in t)
    if not ok: bad += 1
    out += ['## %s' % role, '- inbox: %s' % W, '- id: %s' % m.get('message_id'), '- from: %s' % m.get('from'), '- timestamp: %s' % m.get('timestamp'),
            '- subject: %s' % m.get('subject'), '- names the pinned head prefix %s: %s' % (pre or '(n/a)', ok), '- TEXT_SHA256: %s' % hashlib.sha256(t.encode('utf-8')).hexdigest(), '', '```', t, '```', '']
    print('%-62s %s %s' % (role, m.get('timestamp'), 'HEAD OK' if ok else 'HEAD MISMATCH'))
open(os.path.join(G, 'mail_gate43_ready.md'), 'w', encoding='utf-8').write('\n'.join(out) + '\n')
print('CAPTURE %s: %d mails, %d problem(s) -> mail_gate43_ready.md' % ('OK' if bad == 0 else 'FAILED', len(MAILS), bad))
raise SystemExit(1 if bad else 0)
