#!/usr/bin/env python3
"""capture_mail_gate48a.py — the gate48a CAPTURE. Seat B 47th's READY FOR QA for #1354 (the CLAIMS) and the seat's leg-7 thread, each READ BY
ID from wednesday-agent@ (AgentMail GET /v0/inboxes/<inbox>/messages/<id>; read-only, touches no seen-state), VERBATIM with its TEXT_SHA256:
the STOP (21:16Z), Wednesday's ANSWER (MEASURE, 21:18Z), the MEASURED status (21:29Z), Wednesday's leg-7 RULING (21:31Z: fix js-yaml, one undici
row, "no expires"), the baseline-row status ("no expires" needs a second file, 21:37Z), ROUTE A green (21:38Z), Wednesday's ROUTE B ruling
(21:39Z: expires 2026-10-09, SUPERSEDES "no expires", revert the contract edit), the ks470 committed status (21:43Z), the READY (21:50Z),
Wednesday's ANSWER to the READY (21:51Z) and the seat's handover status (21:56Z). Ids from ONE read-only listing (_mail_list_1.out).
Then, from files (read only): the CLAUSE-4 Kam flag — Wednesday's three chat entries to Kam (0_Brain/dashboard/data/chat_wednesday.json, ts
07:31:59 / 07:32:16 / 07:39:56 AEST) VERBATIM. Checks (rc 1 on any miss): the READY names the pinned head IN FULL and the base `37205947ddd2`;
the committed status names the head prefix; the READY as captured == the seat's record mail/READY-gate48a.txt (stripped, byte-equal); the
ROUTE B mail carries `2026-10-09` and `SUPERSEDES`. The key is read by name and never printed. Writes mail_gate48a_ready.md. Usage: capture_mail_gate48a.py"""
import hashlib, json, os, urllib.request, urllib.parse, datetime
G = os.path.dirname(os.path.abspath(__file__)); K = json.load(open(os.path.join(G, 'kit.json'), encoding='utf-8'))
W = 'wednesday-agent@agentmail.to'
P = json.load(open(os.path.join(G, 'pins_gate48a.json'), encoding='utf-8'))
N = K['order'][0]; HF = P['prs'][N]['head']; H12 = HF[:12]; D12 = P['develop'][:12]
SEAT_READY = os.path.join(K['seat_record'], 'mail', 'READY-gate48a.txt')
MAILS = [
 ('<010001a0ef2589c7-2c1eeffe-740a-473a-a862-6765a2133317-000000@email.amazonses.com>', 'CLAIM #1354 (Seat B 47th READY FOR QA, 21:50Z)', [HF, D12]),
 ('<010001a0ef1f5d7f-ef22625a-8664-41b8-bdf5-64e06c03d295-000000@email.amazonses.com>', 'CONTEXT (Seat B 47th status ks470: ROUTE B applied, contract revert cmp rc 0, committed, 21:43Z)', ['4370be410']),
 ('<010001a0ef06c2b3-ec3ff526-387f-4d96-ae76-e4aceadd7dd0-000000@email.amazonses.com>', 'CONTEXT (Seat B 47th STOP leg 7: two NEW advisories refuse every push, 21:16Z)', []),
 ('<010001a0ef088d76-d2cd04a1-d313-46b8-9f45-fae913cf95c2-000000@email.amazonses.com>', 'CONTEXT (Wednesday ANSWER: MEASURE clause 2 + the exception, Wednesday decides, 21:18Z)', []),
 ('<010001a0ef12fd77-8370e6cb-a566-4463-9370-856098ee8272-000000@email.amazonses.com>', 'CONTEXT (Seat B 47th status leg7 MEASURED: the exception does NOT fire per the seat, 21:29Z)', []),
 ('<010001a0ef14ac5c-5d75dd0d-ecea-440d-a7ae-883ca08710c9-000000@email.amazonses.com>', 'CONTEXT (Wednesday leg-7 RULING: fix js-yaml, one undici row, "no expires" — item 2 SUPERSEDED at 21:39Z, 21:31Z)', []),
 ('<010001a0ef1a41bb-f1afbe24-1497-44c1-82e7-5dc2616e7500-000000@email.amazonses.com>', 'CONTEXT (Seat B 47th status baseline row: "no expires" needs a second file, 21:37Z)', []),
 ('<010001a0ef1afe3f-df07f826-9281-41e0-b69a-3c0cdaeecc36-000000@email.amazonses.com>', 'CONTEXT (Seat B 47th status ROUTE A green, held for Wednesday\'s word, 21:38Z)', []),
 ('<010001a0ef1bf567-81dbf078-5dd2-4b95-984f-a1f2cc067a0a-000000@email.amazonses.com>', 'CONTEXT (Wednesday ROUTE B ruling: expires 2026-10-09, SUPERSEDES "no expires", revert the contract edit, 21:39Z)', ['2026-10-09', 'SUPERSEDES']),
 ('<010001a0ef272eb1-aaef02de-794f-4605-83b0-b6da729ec1a5-000000@email.amazonses.com>', 'CONTEXT (Wednesday ANSWER to the READY: gate48a drafting, 21:51Z)', []),
 ('<010001a0ef2b6536-14143d87-da6f-4022-88a2-67d2b5d1bd8b-000000@email.amazonses.com>', 'CONTEXT (Seat B 47th handover status: "one ANSWER of yours went un-read", 21:56Z)', []),
]
key = ''
for l in open('/Volumes/DevMASTER/WEDNESDAY/4_Credentials/.env', encoding='utf-8'):
    if l.startswith('AGENTMAIL_API_KEY='): key = l.split('=', 1)[1].strip().strip('"').strip("'")
assert key, 'AGENTMAIL_API_KEY unset'
now = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
out = ['# gate48a CAPTURE — Seat B 47th\'s READY for #1354 and the leg-7 thread, read by id, VERBATIM; then the clause-4 Kam flag', '',
       'Captured %s by capture_mail_gate48a.py. Each block: role, inbox, id, from, timestamp, subject, TEXT_SHA256, then the text VERBATIM.' % now, '',
       '#1354 is KS-470.', '', 'The pinned head, in full (pins_gate48a.json): #1354 %s | develop %s | END_TREE %s' % (HF, P['develop'], P['end_tree']), '']
bad = []; nchk = 0; ready = None
for mid, role, pres in MAILS:
    m = json.load(urllib.request.urlopen(urllib.request.Request('https://api.agentmail.to/v0/inboxes/%s/messages/%s' % (W, urllib.parse.quote(mid, safe='')), headers={'Authorization': 'Bearer ' + key}), timeout=60))
    t = m.get('text') or m.get('extracted_text') or ''
    if role.startswith('CLAIM'): ready = t
    res = {p: (p in (m.get('subject') or '') or p in t) for p in pres}; nchk += len(pres)
    if not all(res.values()): bad.append('%s: missing %s' % (role[:60], [p for p, v in res.items() if not v]))
    out += ['## %s' % role, '- inbox: %s' % W, '- id: %s' % m.get('message_id'), '- from: %s' % m.get('from'), '- timestamp: %s' % m.get('timestamp'),
            '- subject: %s' % m.get('subject'), '- carries %s: %s' % (pres or '(n/a)', res or 'n/a'), '- TEXT_SHA256: %s' % hashlib.sha256(t.encode('utf-8')).hexdigest(), '', '```', t, '```', '']
    print('%-100s %s %s | %d chars' % (role[:100], m.get('timestamp'), ('CHECKS OK %d' % len(pres)) if pres and all(res.values()) else ('CHECK MISS %s' % res if pres else 'context'), len(t)))
seat = open(SEAT_READY, encoding='utf-8').read() if os.path.exists(SEAT_READY) else None
same = seat is not None and ready is not None and ready.strip() == seat.strip()
if not same:
    # the seat's file may carry the Subject line on top; compare the body after a leading `Subject:` header block too
    body = seat.split('\n\n', 1)[1] if seat and seat.startswith('Subject:') else seat
    same = body is not None and ready is not None and ready.strip() == body.strip()
print('READY as captured == the seat\'s record %s (stripped): %s' % (SEAT_READY, same))
if not same: bad.append('the captured READY != the seat file %s' % SEAT_READY)
cj = json.load(open('/Volumes/DevMASTER/WEDNESDAY/0_Brain/dashboard/data/chat_wednesday.json', encoding='utf-8'))
cj = cj if isinstance(cj, list) else (cj.get('messages') or cj.get('entries') or [])
want = ('2026-09-30T07:31:59', '2026-09-30T07:32:16', '2026-09-30T07:39:56')
flags = [e for e in cj if isinstance(e, dict) and str(e.get('ts', '')).startswith(want)]
out += ['## CLAUSE 4 — Wednesday\'s flag to Kam (0_Brain/dashboard/data/chat_wednesday.json, role wednesday, VERBATIM; %d of 3 entries found)' % len(flags), '']
for e in flags:
    out += ['- ts: %s | TEXT_SHA256: %s' % (e.get('ts'), hashlib.sha256((e.get('text') or '').encode()).hexdigest()), '', '```', e.get('text') or '', '```', '']
print('CLAUSE-4 Kam flag entries found: %d of 3 (%s)' % (len(flags), ', '.join(e.get('ts', '')[:19] for e in flags)))
if len(flags) != 3: bad.append('the three clause-4 chat entries were not all found')
open(os.path.join(G, 'mail_gate48a_ready.md'), 'w', encoding='utf-8').write('\n'.join(out) + '\n')
for b in bad: print('PROBLEM: ' + b)
print('CAPTURE %s: %d mails, %d check(s), %d problem(s) -> mail_gate48a_ready.md' % ('OK' if not bad else 'FAILED', len(MAILS), nchk + 1, len(bad)))
raise SystemExit(1 if bad else 0)
