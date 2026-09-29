#!/usr/bin/env python3
"""capture_mail_gate45.py — the gate45 CAPTURE: Seat B 45th's READY FOR QA for #1348 + #1347 round 2 (the CLAIMS; one mail, head-checked once
per PR), its STATUS "R2-A DONE" raising #1348, its STATUS holding for gate45, Wednesday's ANSWERs (to the READY, to R2-A DONE, and to MERGED #1346 —
the R2-B shape approval, "CI stacks in scope"), the seat's MERGED #1346 mail (the N-1347-1 shape proposal), Wednesday's GO for #1346 that sent #1347 to
round 2, and gate44's verdict mail; each READ BY ID (AgentMail GET /v0/inboxes/<inbox>/messages/<id>; read-only, touches no seen-state) and written
VERBATIM with its TEXT_SHA256 into mail_gate45_ready.md beside this script. Ids from ONE read-only listing (_mail_list_1.out). The key is read by
name and never printed. Each CLAIM row must name its PR's pinned head prefix (12 hex) — a mismatch is a problem (rc 1). A mail listed twice is
fetched twice and written once. Usage: capture_mail_gate45.py"""
import hashlib, json, os, urllib.request, urllib.parse, datetime
G = os.path.dirname(os.path.abspath(__file__))
W = 'wednesday-agent@agentmail.to'
MAILS = [
 ('<010001a0ecd24a54-a7f4964e-7222-498e-9a8b-be1f5552b530-000000@email.amazonses.com>', 'CLAIM #1348 (READY FOR QA, #1348 + #1347 r2)', '1bb58b4ebb97'),
 ('<010001a0ecd24a54-a7f4964e-7222-498e-9a8b-be1f5552b530-000000@email.amazonses.com>', 'CLAIM #1347 (READY FOR QA, the same mail, second head check)', '18bc5123ce90'),
 ('<010001a0ecc5cd43-8788b4f9-af61-436d-8ca1-c02a37b32cd5-000000@email.amazonses.com>', 'CLAIM #1348 (STATUS R2-A DONE: #1348 raised)', '1bb58b4ebb97'),
 ('<010001a0ecd5ace5-74129a9d-ac30-4047-9b7d-2151f510cd33-000000@email.amazonses.com>', 'STATUS (Seat B 45th holding for gate45)', ''),
 ('<010001a0ecd3f264-6420ccca-4b09-42d3-99d0-5c37c50af200-000000@email.amazonses.com>', 'CONTEXT (Wednesday ANSWER to the READY)', ''),
 ('<010001a0ecc6523f-97fa80e2-ff18-440e-852a-21d249f7edeb-000000@email.amazonses.com>', 'CONTEXT (Wednesday ANSWER to R2-A DONE)', ''),
 ('<010001a0ecbc548d-9c57b253-e47c-4683-8cc9-cffd78aaa093-000000@email.amazonses.com>', 'CONTEXT (Wednesday ANSWER to MERGED #1346: R2-B shape approved, CI stacks in scope)', ''),
 ('<010001a0ecbad4e1-129a261a-5374-451b-84d1-d58976e8aae6-000000@email.amazonses.com>', 'CONTEXT (Seat B 45th MERGED #1346 + the N-1347-1 shape proposal)', ''),
 ('<010001a0ecb590ff-e778ade2-788c-42b9-b7d8-747c09ed1476-000000@email.amazonses.com>', 'CONTEXT (Wednesday GO: merge 1346 on gate44, #1347 to round 2)', ''),
 ('<010001a0ecb37994-37f6e90a-1ff4-495b-bc03-734396f5aa32-000000@email.amazonses.com>', 'CONTEXT (gate44 verdict mail, QA -> Wednesday)', ''),
]
key = ''
for l in open('/Volumes/DevMASTER/WEDNESDAY/4_Credentials/.env', encoding='utf-8'):
    if l.startswith('AGENTMAIL_API_KEY='): key = l.split('=', 1)[1].strip().strip('"').strip("'")
assert key, 'AGENTMAIL_API_KEY unset'
P = json.load(open(os.path.join(G, 'pins_gate45.json'), encoding='utf-8'))
out = ['# gate45 CAPTURE — nine distinct mails read by id, VERBATIM (ten head checks)', '',
       'Captured %s by capture_mail_gate45.py. Each block: role, inbox, id, from, timestamp, subject, TEXT_SHA256, then the text VERBATIM.' % datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'), '',
       '#1348 is KS-1054. #1347 is KS-1374.', '',
       'The pinned heads, in full (pins_gate45.json): ' + ' | '.join('#%s %s' % (n, P['prs'][n]['head']) for n in P['order']), '']
bad = 0; seen = set()
for mid, role, pre in MAILS:
    m = json.load(urllib.request.urlopen(urllib.request.Request('https://api.agentmail.to/v0/inboxes/%s/messages/%s' % (W, urllib.parse.quote(mid, safe='')), headers={'Authorization': 'Bearer ' + key}), timeout=60))
    t = m.get('text') or m.get('extracted_text') or ''
    ok = (not pre) or (pre in (m.get('subject') or '') or pre in t)
    if not ok: bad += 1
    if mid in seen:
        print('%-62s %s %s (already written above)' % (role, m.get('timestamp'), 'HEAD OK' if ok else 'HEAD MISMATCH')); continue
    seen.add(mid)
    out += ['## %s' % role, '- inbox: %s' % W, '- id: %s' % m.get('message_id'), '- from: %s' % m.get('from'), '- timestamp: %s' % m.get('timestamp'),
            '- subject: %s' % m.get('subject'), '- names the pinned head prefix %s: %s' % (pre or '(n/a)', ok), '- TEXT_SHA256: %s' % hashlib.sha256(t.encode('utf-8')).hexdigest(), '', '```', t, '```', '']
    print('%-62s %s %s' % (role, m.get('timestamp'), 'HEAD OK' if ok else 'HEAD MISMATCH'))
open(os.path.join(G, 'mail_gate45_ready.md'), 'w', encoding='utf-8').write('\n'.join(out) + '\n')
print('CAPTURE %s: %d head checks over %d distinct mails, %d problem(s) -> mail_gate45_ready.md' % ('OK' if bad == 0 else 'FAILED', len(MAILS), len(seen), bad))
raise SystemExit(1 if bad else 0)
