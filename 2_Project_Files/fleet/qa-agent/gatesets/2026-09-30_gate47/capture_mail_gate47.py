#!/usr/bin/env python3
"""capture_mail_gate47.py — the gate47 CAPTURE: Seat B 46th's ONE READY FOR QA for #1349 (KS-1374) + #1350 (KS-1054) (the CLAIMS, BOTH heads
checked), its handover STATUS (holding cold for gate47; the seat merges on the GO), Wednesday's ANSWER to the READY, the seat's MERGED #1348 mail
(squash a72149a1a803 = the develop #1350 sits on), Wednesday's ANSWER to MERGED #1348 (start ITEM 3), Wednesday's GO for gate46 (it directed the
KS-1054 facts comment to be DRAFTED, folded N-1348-6/-7 into ITEM 3, and ruled the cap wording), gate46's verdict mail, the seat's plan
confirmation (the ITEM 3 design) and Wednesday's ANSWER to it (python3 absent FAILS CLOSED, rc 1; Q1-Q4), and the seat's #1349 RAISED mail (the
unlocked push, the preflight skip) with Wednesday's ANSWER to it. Each READ BY ID (AgentMail GET /v0/inboxes/<inbox>/messages/<id>; read-only,
touches no seen-state) and written VERBATIM with its TEXT_SHA256 into mail_gate47_ready.md beside this script. Ids from ONE read-only listing
(_mail_list_1.out). The key is read by name and never printed. Each CLAIM row must name EVERY pinned head prefix it lists (12 hex) — a
mismatch is a problem (rc 1). Usage: capture_mail_gate47.py"""
import hashlib, json, os, urllib.request, urllib.parse, datetime
G = os.path.dirname(os.path.abspath(__file__))
W = 'wednesday-agent@agentmail.to'
P = json.load(open(os.path.join(G, 'pins_gate47.json'), encoding='utf-8'))
H49 = P['prs']['1349']['head'][:12]; H50 = P['prs']['1350']['head'][:12]
MAILS = [
 ('<010001a0ed755aec-81f2c3e4-1937-477a-9e1a-b6b0c0d19d30-000000@email.amazonses.com>', 'CLAIM #1349 + #1350 (Seat B 46th READY FOR QA, ONE READY, both drafted ticket texts VERBATIM)', [H49, H50]),
 ('<010001a0ed780423-17f2b405-ea09-4a68-af4c-8fa35f624d85-000000@email.amazonses.com>', 'CONTEXT (Seat B 46th handover STATUS: holding cold for gate47, watcher armed)', [H49, H50]),
 ('<010001a0ed75e14a-21fa5008-a5a0-41f0-af76-0179135274df-000000@email.amazonses.com>', 'CONTEXT (Wednesday ANSWER to the READY: gate47 by the next Wednesday seat)', []),
 ('<010001a0ed5faef6-54f47d58-c8a2-49d7-86af-f19bce7053fb-000000@email.amazonses.com>', 'CONTEXT (Seat B 46th MERGED #1348, squash a72149a1a803 = the develop #1350 sits on)', []),
 ('<010001a0ed61056d-918bdfee-7d81-442e-ae21-cf32740d6d2b-000000@email.amazonses.com>', 'CONTEXT (Wednesday ANSWER to MERGED #1348: verified, start ITEM 3)', []),
 ('<010001a0ed5ab84f-10214e8f-92ff-4c4f-b6d7-408b83069943-000000@email.amazonses.com>', 'CONTEXT (Wednesday GO for gate46: merge 1348; DRAFT the KS-1054 facts comment; fold N-1348-6/-7; the cap wording)', []),
 ('<010001a0ed58c7bd-681a5ef5-5b29-4748-910a-8c1dfef07444-000000@email.amazonses.com>', 'CONTEXT (gate46 verdict mail, QA -> Wednesday)', []),
 ('<010001a0ed45fced-7981a777-0ac3-422f-a787-5118a6740903-000000@email.amazonses.com>', 'CONTEXT (Seat B 46th plan confirmation: the ITEM 3 design, rc 2 = PASS-WITH-SKIP, Q1-Q4)', []),
 ('<010001a0ed471a76-0daa4258-1ed5-4751-a691-6522493975b5-000000@email.amazonses.com>', 'CONTEXT (Wednesday ANSWER to the plan: design approved, python3 absent FAILS CLOSED rc 1; Q1-Q4 defaults accepted)', []),
 ('<010001a0ed57aae7-3088b49d-b5bf-4ce5-9d0d-f58dbffeec17-000000@email.amazonses.com>', 'CONTEXT (Seat B 46th: #1349 RAISED, pushed WITHOUT the lock, the preflight skipped by design)', []),
 ('<010001a0ed58a7fc-d337ce47-0999-4a14-a653-756600f43e86-000000@email.amazonses.com>', 'CONTEXT (Wednesday ANSWER: the unlocked push accepted as disclosed; gate47 runs the systemTest checks + audit legs for #1349)', []),
]
key = ''
for l in open('/Volumes/DevMASTER/WEDNESDAY/4_Credentials/.env', encoding='utf-8'):
    if l.startswith('AGENTMAIL_API_KEY='): key = l.split('=', 1)[1].strip().strip('"').strip("'")
assert key, 'AGENTMAIL_API_KEY unset'
out = ['# gate47 CAPTURE — eleven distinct mails read by id, VERBATIM (both heads checked in the READY and the handover)', '',
       'Captured %s by capture_mail_gate47.py. Each block: role, inbox, id, from, timestamp, subject, TEXT_SHA256, then the text VERBATIM.' % datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'), '',
       '#1349 is KS-1374. #1350 is KS-1054.', '',
       'The pinned heads, in full (pins_gate47.json): #1349 %s | #1350 %s | develop %s' % (P['prs']['1349']['head'], P['prs']['1350']['head'], P['develop']), '']
bad = 0; seen = set(); nchk = 0
for mid, role, pres in MAILS:
    m = json.load(urllib.request.urlopen(urllib.request.Request('https://api.agentmail.to/v0/inboxes/%s/messages/%s' % (W, urllib.parse.quote(mid, safe='')), headers={'Authorization': 'Bearer ' + key}), timeout=60))
    t = m.get('text') or m.get('extracted_text') or ''
    res = {p: (p in (m.get('subject') or '') or p in t) for p in pres}; nchk += len(pres)
    ok = all(res.values())
    if not ok: bad += 1
    if mid in seen: continue
    seen.add(mid)
    out += ['## %s' % role, '- inbox: %s' % W, '- id: %s' % m.get('message_id'), '- from: %s' % m.get('from'), '- timestamp: %s' % m.get('timestamp'),
            '- subject: %s' % m.get('subject'), '- names the pinned head prefix(es) %s: %s' % (pres or '(n/a)', res or 'n/a'), '- TEXT_SHA256: %s' % hashlib.sha256(t.encode('utf-8')).hexdigest(), '', '```', t, '```', '']
    print('%-110s %s %s | %d chars' % (role[:110], m.get('timestamp'), ('HEADS OK %s' % pres) if pres and ok else ('HEAD MISMATCH %s' % res if not ok else 'context'), len(t)))
open(os.path.join(G, 'mail_gate47_ready.md'), 'w', encoding='utf-8').write('\n'.join(out) + '\n')
print('CAPTURE %s: %d mails, %d head check(s), %d problem(s) -> mail_gate47_ready.md' % ('OK' if bad == 0 else 'FAILED', len(seen), nchk, bad))
raise SystemExit(1 if bad else 0)
