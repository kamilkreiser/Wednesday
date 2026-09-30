#!/usr/bin/env python3
"""capture_mail_gate48b.py — the gate48b CAPTURE. Seat B 48th's READY FOR QA for #1355 (the CLAIMS) and the seat's thread that led to it, each
READ BY ID from wednesday-agent@ (AgentMail GET /v0/inboxes/<inbox>/messages/<id>; read-only, touches no seen-state), VERBATIM with TEXT_SHA256:
the READY ADDENDUM for #1354's PERMANENT head (01:22Z; checks: names 88802586cebe… in full and its parent 4370be410bbf), Wednesday's
'Kam ruled' ANSWER (01:05Z), the seat's c-ruling collision + correction QUESTIONs (01:09Z) and Wednesday's lift (01:10Z), the plan confirmation (00:02Z) and Wednesday's ANSWER (00:03Z), the override START (00:05Z), the override MEASURED STOP (00:12Z: the root override
INERT) and Wednesday's ANSWER (00:14Z: route 1), the ROUTE 1 status (00:21Z: contract / leg 6 / leg 7 all rc 0, no row) and Wednesday's ANSWER
(00:22Z: raise ONE PR, measure the image / served tree / suites BEFORE the READY, gate48b T1), the PUSH status (00:40Z), the READY (00:50Z),
Wednesday's ANSWER to the READY (00:52Z) and the seat's handover status (00:55Z). The LAUNCH BRIEF (23:33Z, ~65 KB) is recorded by id and
TEXT_SHA256 only (context; read on demand). Ids from ONE read-only listing (_mail_list_1.out).
Checks (rc 1 on any miss): the READY names the pinned head IN FULL and the base `37205947ddd2`; the push status names the head prefix; the READY
as captured == the seat's record mail/READY-1355.txt AND == Wednesday's scratch copy b48_ready48b.md (each compared stripped, after a leading
`Subject:`/`Id:` header block); the route-1 status carries `1970` and `1968`; the raise ANSWER carries `T1`. The key is read by name and never
printed. Also: KAM'S RULING on card secuura-undici-ghsa-r53p-exception-1354 from 0_Brain/dashboard/data/decisions.json (READ ONLY; rc 1 unless
ruled (c)), and every LATE mail from the seat naming 1354 after 00:56Z (one listing), verbatim. Writes mail_gate48b_ready.md. Usage: capture_mail_gate48b.py"""
import hashlib, json, os, urllib.request, urllib.parse, datetime
G = os.path.dirname(os.path.abspath(__file__)); K = json.load(open(os.path.join(G, 'kit.json'), encoding='utf-8'))
W = 'wednesday-agent@agentmail.to'
P = json.load(open(os.path.join(G, 'pins_gate48b.json'), encoding='utf-8'))
N = '1355'; HF = P['prs'][N]['head']; H1354 = P['prs']['1354']['head']; H12 = HF[:12]; D12 = P['develop'][:12]
SEAT_READY = os.path.join(K['seat_record'], 'mail', 'READY-1355.txt')
WED_READY = '/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/ffc4a192-4894-4f1e-abfb-22149b1bd26c/scratchpad/b48_ready48b.md'
MAILS = [
 ('<010001a0efe85f46-2f659f5a-67ca-4fec-a4b3-93dc4b4215b5-000000@email.amazonses.com>', 'CLAIM #1354 (Seat B 48th READY ADDENDUM: #1354 PERMANENT at its new head, contract / leg 6 / leg 7 rc 0, 12/15 ran, 01:22Z)', ['88802586cebe35855983f7639b5e18069fe11e13', '4370be410bbf']),
 ('<010001a0efdd1a82-0c9e9c6b-5f43-4b4b-9413-084dcf525eba-000000@email.amazonses.com>', 'CONTEXT (Wednesday ANSWER c-ruling collision: the lift for #1354, 01:10Z)', []),
 ('<010001a0efdc6d7b-e620aa6f-3db5-4b15-b5f7-754c288c3f05-000000@email.amazonses.com>', 'CONTEXT (Seat B 48th QUESTION correction, 01:09Z)', []),
 ('<010001a0efdbc5e3-f7d67749-34c8-4b72-b694-c2f82ac6d842-000000@email.amazonses.com>', 'CONTEXT (Seat B 48th QUESTION c-ruling collision, 01:09Z)', []),
 ('<010001a0efd83ea8-1beaa6c9-518e-423f-8cea-17c5df366af3-000000@email.amazonses.com>', 'CONTEXT (Wednesday ANSWER Kam ruled: accept GHSA-r53p permanently, 01:05Z)', ['r53p']),
 ('<010001a0efcaa318-60768252-8445-48aa-b750-56eb33d25d5e-000000@email.amazonses.com>', 'CLAIM #1355 (Seat B 48th READY FOR QA, 00:50Z)', [HF, D12]),
 ('<010001a0efc17365-00925bfe-6cc5-414e-b1e5-11006989dd93-000000@email.amazonses.com>', 'CONTEXT (Seat B 48th status push: legs 6 and 7 PASS in the hook, the first push REFUSED, 00:40Z)', ['6fab9c09']),
 ('<010001a0efb115c5-b0c9c5ba-4483-413a-8905-13a9aaca8826-000000@email.amazonses.com>', 'CONTEXT (Wednesday ANSWER route1: RAISE the one PR, measure image / served tree / suites before the READY, gate48b T1, 00:22Z)', ['T1']),
 ('<010001a0efaff6a7-d81c9fb2-6ec4-4670-bb3e-5f09a5f64885-000000@email.amazonses.com>', 'CONTEXT (Seat B 48th status route1: contract + leg 6 + leg 7 all rc 0 with NO row; root 1970 -> 1968, 00:21Z)', ['1970', '1968']),
 ('<010001a0efa9825d-db7596f2-e62c-4bc3-b7a6-a7a87fba3827-000000@email.amazonses.com>', 'CONTEXT (Wednesday ANSWER override measured: continue route 1, the pristine control, 00:14Z)', []),
 ('<010001a0efa81f92-ef6a2535-5cec-41bb-9cda-5cac25a03afa-000000@email.amazonses.com>', 'CONTEXT (Seat B 48th status override MEASURED: STOP, the root override INERT, leg 6 byte-identical, 00:12Z)', []),
 ('<010001a0efa18d8f-a750b26e-0c2c-42f4-bf8e-aff205dd0938-000000@email.amazonses.com>', 'CONTEXT (Seat B 48th status override start, 00:05Z)', []),
 ('<010001a0efa009cc-0e558987-18ff-45d6-802b-4f24d1c86df7-000000@email.amazonses.com>', 'CONTEXT (Wednesday ANSWER plan confirmation: branch B, Refs KS-1378, 00:03Z)', []),
 ('<010001a0ef9f1287-153c78ce-b39e-4530-ac5d-57c365133cb5-000000@email.amazonses.com>', 'CONTEXT (Seat B 48th plan confirmation, 00:02Z)', []),
 ('<010001a0efccb8a5-966ae7d4-f9f9-44c8-b444-1e49858fd646-000000@email.amazonses.com>', 'CONTEXT (Wednesday ANSWER to the READY: gate48b drafting, 00:52Z)', []),
 ('<010001a0efcf9379-01389f39-af12-4821-99e0-d471d0d28178-000000@email.amazonses.com>', 'CONTEXT (Seat B 48th handover status, 00:55Z)', []),
]
BRIEF = ('<010001a0ef83f917-3243a2c1-33ad-456d-860b-8af333d6a26f-000000@email.amazonses.com>', 'CONTEXT (Wednesday LAUNCH BRIEF for Seat B 48th, 23:33Z) — id and TEXT_SHA256 only')
key = ''
for l in open('/Volumes/DevMASTER/WEDNESDAY/4_Credentials/.env', encoding='utf-8'):
    if l.startswith('AGENTMAIL_API_KEY='): key = l.split('=', 1)[1].strip().strip('"').strip("'")
assert key, 'AGENTMAIL_API_KEY unset'
def get(mid): return json.load(urllib.request.urlopen(urllib.request.Request('https://api.agentmail.to/v0/inboxes/%s/messages/%s' % (W, urllib.parse.quote(mid, safe='')), headers={'Authorization': 'Bearer ' + key}), timeout=60))
def body(t):   # strip a leading header block (Subject: / Id: lines) and compare the rest
    if t is None: return None
    ls = t.split('\n'); i = 0
    while i < len(ls) and (ls[i].startswith(('Subject:', 'Id:', 'From:', 'To:', 'Date:')) or (i and not ls[i].strip() and i < 4)): i += 1
    return '\n'.join(ls[i:]).strip()
now = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
out = ['# gate48b CAPTURE — Seat B 48th\'s READY for #1355 and the thread behind it, read by id, VERBATIM', '',
       'Captured %s by capture_mail_gate48b.py. Each block: role, inbox, id, from, timestamp, subject, TEXT_SHA256, then the text VERBATIM.' % now, '',
       '#1354 is KS-470. #1355 is KS-1378.', '', 'The pinned heads, in full (pins_gate48b.json): #1354 %s | #1355 %s | develop %s | END_TREE %s' % (H1354, HF, P['develop'], P['end_tree']), '']
bad = []; nchk = 0; ready = None
for mid, role, pres in MAILS:
    m = get(mid); t = m.get('text') or m.get('extracted_text') or ''
    if role.startswith('CLAIM #1355'): ready = t
    res = {p: (p in (m.get('subject') or '') or p in t) for p in pres}; nchk += len(pres)
    if not all(res.values()): bad.append('%s: missing %s' % (role[:60], [p for p, v in res.items() if not v]))
    out += ['## %s' % role, '- inbox: %s' % W, '- id: %s' % m.get('message_id'), '- from: %s' % m.get('from'), '- timestamp: %s' % m.get('timestamp'),
            '- subject: %s' % m.get('subject'), '- carries %s: %s' % (pres or '(n/a)', res or 'n/a'), '- TEXT_SHA256: %s' % hashlib.sha256(t.encode('utf-8')).hexdigest(), '', '```', t, '```', '']
    print('%-110s %s %s | %d chars' % (role[:110], m.get('timestamp'), ('CHECKS OK %d' % len(pres)) if pres and all(res.values()) else ('CHECK MISS %s' % res if pres else 'context'), len(t)))
m = get(BRIEF[0]); t = m.get('text') or m.get('extracted_text') or ''
out += ['## %s' % BRIEF[1], '- id: %s' % m.get('message_id'), '- timestamp: %s' % m.get('timestamp'), '- subject: %s' % m.get('subject'), '- TEXT_SHA256: %s (%d chars; not reproduced here)' % (hashlib.sha256(t.encode('utf-8')).hexdigest(), len(t)), '']
print('%-110s %s id + sha256 only | %d chars' % (BRIEF[1][:110], m.get('timestamp'), len(t)))
for lab, f in (('the seat\'s record ' + SEAT_READY, SEAT_READY), ('Wednesday\'s scratch copy ' + WED_READY, WED_READY)):
    s = open(f, encoding='utf-8').read() if os.path.exists(f) else None
    same = s is not None and ready is not None and (ready.strip() == s.strip() or body(s) == ready.strip())
    print('READY as captured == %s (stripped, header block removed): %s' % (lab, same))
    if not same: bad.append('the captured READY != %s' % f)
# KAM'S RULING on the card (decisions.json, READ ONLY) + Wednesday's verbatim quote of the live board (kit.json kam_ruling)
dj = json.load(open('/Volumes/DevMASTER/WEDNESDAY/0_Brain/dashboard/data/decisions.json', encoding='utf-8'))
items = dj if isinstance(dj, list) else (dj.get('decisions') or dj.get('cards') or dj.get('items') or [])
card = [c for c in items if c.get('id') == K['kam_ruling']['card']]
kr = K['kam_ruling']
out += ['## KAM\'S RULING — card %s' % kr['card'], '', '- Wednesday\'s quote of the live board (scope-change message to the drafter): "%s" at %s' % (kr['verbatim'], kr['ts'])]
if card:
    c = card[0]; oc = [o for o in c.get('options', []) if o.get('key') == c.get('ruled_choice')]
    out += ['- decisions.json (read %s): status %s | ruled_choice %s | ruled_ts %s | recommended %s | title: %s' % (now, c.get('status'), c.get('ruled_choice'), c.get('ruled_ts'), c.get('recommended'), c.get('title')),
            '- the ruled option, verbatim: %s' % json.dumps(oc[0] if oc else None, ensure_ascii=False),
            '- NOTE: decisions.json carries no free-text note field; "And fix now" is from Wednesday\'s quote. Its ruled_ts differs from the quoted 11:03:17 by ~84 s (board write vs message time) — both are recorded, neither is edited.', '']
    print('KAM RULING card %s: status %s, ruled_choice %s, ruled_ts %s (Wednesday quoted %s)' % (kr['card'], c.get('status'), c.get('ruled_choice'), c.get('ruled_ts'), kr['ts']))
    if c.get('ruled_choice') != 'c' or c.get('status') != 'ruled': bad.append('the card is not ruled (c) in decisions.json')
else: bad.append('the card %s is not in decisions.json' % kr['card'])
# LATE mails from the seat about #1354's NEW head (after the handover): ONE read-only listing, every secuura-blockchain mail naming 1354 after 00:56Z
lst = json.load(urllib.request.urlopen(urllib.request.Request('https://api.agentmail.to/v0/inboxes/%s/messages?limit=60' % W, headers={'Authorization': 'Bearer ' + key}), timeout=60)).get('messages', [])
known = set(x[0] for x in MAILS)
late = [m for m in lst if 'secuura-blockchain' in (m.get('from') or '') and '1354' in (m.get('subject') or '') and (m.get('timestamp') or '') > '2026-09-30T00:56' and m.get('message_id') not in known]
for m in sorted(late, key=lambda x: x.get('timestamp') or ''):
    mm = get(m['message_id']); t = mm.get('text') or mm.get('extracted_text') or ''
    out += ['## LATE (the seat on #1354\'s new head, found by listing): %s' % mm.get('subject'), '- id: %s' % mm.get('message_id'), '- timestamp: %s' % mm.get('timestamp'),
            '- names the pinned #1354 head %s: %s' % (H1354[:12], H1354[:12] in t or H1354[:12] in (mm.get('subject') or '')), '- TEXT_SHA256: %s' % hashlib.sha256(t.encode('utf-8')).hexdigest(), '', '```', t, '```', '']
    print('LATE %s %s | names the pinned #1354 head: %s | %d chars' % (mm.get('timestamp'), (mm.get('subject') or '')[:100], H1354[:12] in t, len(t)))
print('LATE mails from the seat naming 1354 after 00:56Z, beyond the ids captured above: %d' % len(late))
out += ['## Wednesday\'s ANSWER files (briefs_staged, as written before sending; VERBATIM with sha256)', '']
bs = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged'
for fn in ('2026-09-30_answer_seatB48_plan.md', '2026-09-30_answer_seatB48_route1.md', '2026-09-30_answer_seatB48_raise.md', '2026-09-30_answer_seatB48_ready48b.md'):
    t = open(os.path.join(bs, fn), encoding='utf-8').read()
    out += ['### %s — sha256 %s' % (fn, hashlib.sha256(t.encode()).hexdigest()), '', '```', t, '```', '']
    print('ANSWER FILE %s sha256 %s | %d chars' % (fn, hashlib.sha256(t.encode()).hexdigest()[:16], len(t)))
open(os.path.join(G, 'mail_gate48b_ready.md'), 'w', encoding='utf-8').write('\n'.join(out) + '\n')
for b in bad: print('PROBLEM: ' + b)
print('CAPTURE %s: %d mails + the brief by id, %d check(s), %d problem(s) -> mail_gate48b_ready.md' % ('OK' if not bad else 'FAILED', len(MAILS), nchk + 2, len(bad)))
raise SystemExit(1 if bad else 0)
