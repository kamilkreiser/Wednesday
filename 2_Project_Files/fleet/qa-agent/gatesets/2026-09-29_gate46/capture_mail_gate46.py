#!/usr/bin/env python3
"""capture_mail_gate46.py — the gate46 CAPTURE: Seat B 45th's READY FOR QA for #1348 ROUND 2 (the CLAIMS, head-checked), its WRAP (the successor
handover context: the SUCCESSOR seat merges), Wednesday's ANSWER to MERGED #1347 ("do 1348 round 2"), the seat's MERGED #1347 mail, Wednesday's GO
that merged #1347 and sent #1348 to round 2 (it names what round 2 had to do), and gate45's verdict mail; each READ BY ID (AgentMail GET
/v0/inboxes/<inbox>/messages/<id>; read-only, touches no seen-state) and written VERBATIM with its TEXT_SHA256 into mail_gate46_ready.md beside this
script. Ids from ONE read-only listing (_mail_list_1.out). The key is read by name and never printed. Each CLAIM row must name the pinned head
prefix (12 hex) — a mismatch is a problem (rc 1). Usage: capture_mail_gate46.py"""
import hashlib, json, os, urllib.request, urllib.parse, datetime
G = os.path.dirname(os.path.abspath(__file__))
W = 'wednesday-agent@agentmail.to'
P = json.load(open(os.path.join(G, 'pins_gate46.json'), encoding='utf-8'))
H12 = P['prs']['1348']['head'][:12]
MAILS = [
 ('<010001a0ed24d8b1-4e2dbcba-7ca5-4f93-82e2-14fa0948aa65-000000@email.amazonses.com>', 'CLAIM #1348 (READY FOR QA, #1348 round 2)', H12),
 ('<010001a0ed265a74-9785649e-91d7-40dd-b042-91fbdcf5b715-000000@email.amazonses.com>', 'CONTEXT (Seat B 45th WRAP: #1348 r2 held for gate46; the successor merges)', ''),
 ('<010001a0ed1b8965-d67d1111-6cde-416c-9662-9a1420ba6636-000000@email.amazonses.com>', 'CONTEXT (Wednesday ANSWER to MERGED #1347: do 1348 round 2 then wrap)', ''),
 ('<010001a0ed1a596e-d47fe535-5e84-4e1e-a50f-4e9bc9902c74-000000@email.amazonses.com>', 'CONTEXT (Seat B 45th MERGED #1347, squash 8c810023f9c9 = the develop #1348 must merge over)', ''),
 ('<010001a0ed15620d-7a72bb75-5c32-46f2-91a0-272fbba3018e-000000@email.amazonses.com>', 'CONTEXT (Wednesday GO: merge 1347 on gate45, #1348 to round 2)', ''),
 ('<010001a0ed13a823-c93e7e98-ced8-4203-b829-68f5d2996e31-000000@email.amazonses.com>', 'CONTEXT (gate45 verdict mail, QA -> Wednesday)', ''),
]
key = ''
for l in open('/Volumes/DevMASTER/WEDNESDAY/4_Credentials/.env', encoding='utf-8'):
    if l.startswith('AGENTMAIL_API_KEY='): key = l.split('=', 1)[1].strip().strip('"').strip("'")
assert key, 'AGENTMAIL_API_KEY unset'
out = ['# gate46 CAPTURE — six distinct mails read by id, VERBATIM (one head check)', '',
       'Captured %s by capture_mail_gate46.py. Each block: role, inbox, id, from, timestamp, subject, TEXT_SHA256, then the text VERBATIM.' % datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'), '',
       '#1348 is KS-1054.', '',
       'The pinned head, in full (pins_gate46.json): #1348 %s | round 1 %s | develop %s' % (P['prs']['1348']['head'], P['prs']['1348']['parent'], P['develop']), '']
bad = 0; seen = set()
for mid, role, pre in MAILS:
    m = json.load(urllib.request.urlopen(urllib.request.Request('https://api.agentmail.to/v0/inboxes/%s/messages/%s' % (W, urllib.parse.quote(mid, safe='')), headers={'Authorization': 'Bearer ' + key}), timeout=60))
    t = m.get('text') or m.get('extracted_text') or ''
    ok = (not pre) or (pre in (m.get('subject') or '') or pre in t)
    if not ok: bad += 1
    if mid in seen: continue
    seen.add(mid)
    out += ['## %s' % role, '- inbox: %s' % W, '- id: %s' % m.get('message_id'), '- from: %s' % m.get('from'), '- timestamp: %s' % m.get('timestamp'),
            '- subject: %s' % m.get('subject'), '- names the pinned head prefix %s: %s' % (pre or '(n/a)', ok), '- TEXT_SHA256: %s' % hashlib.sha256(t.encode('utf-8')).hexdigest(), '', '```', t, '```', '']
    print('%-100s %s %s | %d chars' % (role, m.get('timestamp'), 'HEAD OK' if ok and pre else ('HEAD MISMATCH' if not ok else 'context'), len(t)))
open(os.path.join(G, 'mail_gate46_ready.md'), 'w', encoding='utf-8').write('\n'.join(out) + '\n')
print('CAPTURE %s: %d mails, %d head check(s), %d problem(s) -> mail_gate46_ready.md' % ('OK' if bad == 0 else 'FAILED', len(seen), sum(1 for x in MAILS if x[2]), bad))
raise SystemExit(1 if bad else 0)
