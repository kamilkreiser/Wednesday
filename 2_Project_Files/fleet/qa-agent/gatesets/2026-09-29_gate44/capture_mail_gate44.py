#!/usr/bin/env python3
"""capture_mail_gate44.py — the gate44 CAPTURE: Seat B 45th's READY FOR QA for #1346 + #1347 (the CLAIMS; one mail, head-checked once per PR),
its STATUS "ITEM 2 DONE" raising #1346, its STATUS holding for gate44, Wednesday's ANSWER to the READY, Wednesday's LAUNCH BRIEF to Seat B 45th
(the commission of both items) and Tuesday's two ROUTED copies of Kam's KS-1374 instruction, each READ BY ID (AgentMail GET
/v0/inboxes/<inbox>/messages/<id>; read-only, touches no seen-state) and written VERBATIM with its TEXT_SHA256 into mail_gate44_ready.md beside
this script. Ids from ONE read-only listing (_mail_list_1.out). The key is read by name and never printed. Each CLAIM row must name its PR's
pinned head prefix (12 hex) — a mismatch is a problem (rc 1). A mail listed twice is fetched twice and written once. Usage: capture_mail_gate44.py"""
import hashlib, json, os, urllib.request, urllib.parse, datetime
G = os.path.dirname(os.path.abspath(__file__))
W = 'wednesday-agent@agentmail.to'
MAILS = [
 ('<010001a0ec707811-700f0d8e-f02f-4b7c-93d7-06c9a172cb71-000000@email.amazonses.com>', 'CLAIM #1346 (READY FOR QA, both PRs)', '2075c3ec7078'),
 ('<010001a0ec707811-700f0d8e-f02f-4b7c-93d7-06c9a172cb71-000000@email.amazonses.com>', 'CLAIM #1347 (READY FOR QA, the same mail, second head check)', '2c4b98253b1f'),
 ('<010001a0ec4a1c13-958a113d-3ed3-4058-a0e4-99d8df696972-000000@email.amazonses.com>', 'CLAIM #1346 (STATUS ITEM 2 DONE: KS-1054 raised)', '2075c3ec7078'),
 ('<010001a0ec74056b-cd09ce14-ed4d-4798-a96b-e0227592f65d-000000@email.amazonses.com>', 'STATUS (Seat B 45th holding for gate44)', ''),
 ('<010001a0ec716fb8-31d0452a-9819-4f9b-8651-0c9f4550a7d4-000000@email.amazonses.com>', 'CONTEXT (Wednesday ANSWER to the READY)', ''),
 ('<010001a0ec1bf318-3d3a1aab-3695-4cdf-94f4-d072913207b1-000000@email.amazonses.com>', 'CONTEXT (Wednesday LAUNCH BRIEF to Seat B 45th: gate43 merges + KS-1054 + KS-1374 A/B/C)', ''),
 ('<010001a0ebd169b8-857c8736-93a5-418f-b9a7-8cb045d066be-000000@email.amazonses.com>', 'CONTEXT (Tuesday ROUTED: Kam on KS-1374, 16:17:55, the later copy)', ''),
 ('<010001a0ebd0817c-2de14fce-d72f-4361-9f56-441c8a69ed80-000000@email.amazonses.com>', 'CONTEXT (Tuesday ROUTED: Kam on KS-1374, 16:17:55, the earlier copy)', ''),
]
key = ''
for l in open('/Volumes/DevMASTER/WEDNESDAY/4_Credentials/.env', encoding='utf-8'):
    if l.startswith('AGENTMAIL_API_KEY='): key = l.split('=', 1)[1].strip().strip('"').strip("'")
assert key, 'AGENTMAIL_API_KEY unset'
P = json.load(open(os.path.join(G, 'pins_gate44.json'), encoding='utf-8'))
out = ['# gate44 CAPTURE — seven distinct mails read by id, VERBATIM (eight head checks)', '',
       'Captured %s by capture_mail_gate44.py. Each block: role, inbox, id, from, timestamp, subject, TEXT_SHA256, then the text VERBATIM.' % datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'), '',
       '#1346 is KS-1054. #1347 is KS-1374.', '',
       'The pinned heads, in full (pins_gate44.json): ' + ' | '.join('#%s %s' % (n, P['prs'][n]['head']) for n in P['order']), '']
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
open(os.path.join(G, 'mail_gate44_ready.md'), 'w', encoding='utf-8').write('\n'.join(out) + '\n')
print('CAPTURE %s: %d head checks over %d distinct mails, %d problem(s) -> mail_gate44_ready.md' % ('OK' if bad == 0 else 'FAILED', len(MAILS), len(seen), bad))
raise SystemExit(1 if bad else 0)
