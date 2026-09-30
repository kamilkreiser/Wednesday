#!/usr/bin/env python3
"""capture_mail_gate50a.py — the gate50a CAPTURE, found by ONE read-only listing of wednesday-agent@ (GET messages?limit=100; touches no
seen-state) and then read BY ID, VERBATIM, with TEXT_SHA256: every mail from 2026-09-30T20:00Z on whose subject names Seat B 51st / B51 / itemA /
ITEM A / #1363 / gate50a (the seat's plan confirmation, its STOP on the thirteen advisories, status itemA, the READY and anything after it;
Wednesday's ANSWERs, including route (a) at 20:54Z, the AUTHORITY). A LAUNCH BRIEF / ADDENDUM is recorded by id + TEXT_SHA256 only (context,
read on demand). Also the READY as Wednesday saved it beside this kit (READY_1363_mail.md), compared to the captured READY.
Checks (rc 1 on any miss): exactly one mail from the seat whose subject carries READY and names #<PR> (the CLAIM); the READY names the pinned head
IN FULL and the base `4f18c59a89db`; the READY as captured == the seat's record `mail/READY-<PR>.txt` when that file exists (compared stripped,
after a leading header block; its absence is REPORTED, not refused); the READY carries `13/13` and the new-ticket TITLE sha256 prefix; Wednesday's
route (a) ANSWER is present (the authority).
The key is read by name and never printed. Refuses while kit.json is UNPINNED. Writes mail_gate50a_ready.md. Usage: capture_mail_gate50a.py"""
import hashlib, json, os, re, urllib.request, urllib.parse, datetime, glob
G = os.path.dirname(os.path.abspath(__file__)); K = json.load(open(os.path.join(G, 'kit.json'), encoding='utf-8'))
N = K['order'][0]
if N == '<PR>': raise SystemExit('REFUSING: kit.json is UNPINNED (<PR>) — run pinpr_gate50a.py first')
P = json.load(open(os.path.join(G, 'pins_gate50a.json'), encoding='utf-8')); HF = P['pr_pins']['head']; D12 = P['develop'][:12]
W = 'wednesday-agent@agentmail.to'
key = ''
for l in open('/Volumes/DevMASTER/WEDNESDAY/4_Credentials/.env', encoding='utf-8'):
    if l.startswith('AGENTMAIL_API_KEY='): key = l.split('=', 1)[1].strip().strip('"').strip("'")
assert key, 'AGENTMAIL_API_KEY unset'
def req(u): return json.load(urllib.request.urlopen(urllib.request.Request(u, headers={'Authorization': 'Bearer ' + key}), timeout=60))
def get(mid): return req('https://api.agentmail.to/v0/inboxes/%s/messages/%s' % (W, urllib.parse.quote(mid, safe='')))
def body(t):
    ls = t.split('\n'); i = 0
    while i < len(ls) and (ls[i].startswith(('Subject:', 'Id:', 'From:', 'To:', 'Date:')) or (i and not ls[i].strip() and i < 4)): i += 1
    return '\n'.join(ls[i:]).strip()
now = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
lst = req('https://api.agentmail.to/v0/inboxes/%s/messages?limit=100' % W).get('messages', [])
RX = re.compile(r'B ?51|itemA|ITEM A|#?1363\b|gate50a', re.I)
sel = sorted([m for m in lst if RX.search(m.get('subject') or '') and (m.get('timestamp') or '') >= '2026-09-30T20:00'], key=lambda m: m.get('timestamp') or '')
out = ['# gate50a CAPTURE — Seat B 51st\'s READY for #%s (ITEM A) and the thread behind it, read by id, VERBATIM' % N, '',
       'Captured %s by capture_mail_gate50a.py from ONE listing of %s (%d listed, %d selected). Each block: role, id, from, timestamp, subject, TEXT_SHA256, then the text VERBATIM.' % (now, W, len(lst), len(sel)), '',
       '#%s is KS-1378.' % N, '', 'The pinned head, in full (pins_gate50a.json): #%s %s | develop %s | END_TREE %s' % (N, HF, P['develop'], P['end_tree']), '']
bad = []; ready = []; meas = []; route = []
for m in sel:
    s = m.get('subject') or ''
    mm = get(m['message_id']); t = mm.get('text') or mm.get('extracted_text') or ''
    fromseat = 'secuura-blockchain' in (mm.get('from') or '')
    ctx_only = (not fromseat) and re.search(r'\] (LAUNCH BRIEF|ADDENDUM)', s)   # Wednesday's long briefs only; every seat mail is verbatim
    role = ('CLAIM (the READY)' if fromseat and 'READY' in s and re.search(r'#?%s\b' % N, s + t[:400]) else
            'CONTEXT (id + sha256 only)' if ctx_only else ('CONTEXT (seat)' if fromseat else 'CONTEXT (Wednesday)'))
    if role.startswith('CLAIM'): ready.append(t)
    if (not fromseat) and re.search(r'route \(a\)', s, re.I): route.append(t)
    sha = hashlib.sha256(t.encode('utf-8')).hexdigest()
    out += ['## %s — %s' % (role, s), '- id: %s' % mm.get('message_id'), '- from: %s' % mm.get('from'), '- timestamp: %s' % mm.get('timestamp'), '- TEXT_SHA256: %s (%d chars)' % (sha, len(t)), '']
    if not ctx_only: out += ['```', t, '```', '']
    print('%-28s %s %s | %d chars | %s' % (role, mm.get('timestamp'), sha[:16], len(t), s[:110]))
if len(ready) != 1: bad.append('%d READY mail(s) from the seat naming #%s (want exactly 1)' % (len(ready), N))
else:
    r = ready[0]
    for p in (HF, D12):
        if p not in r: bad.append('the READY does not name %s' % p)
    print('READY names the pinned head IN FULL: %s | the base %s: %s' % (HF in r, D12, D12 in r))
    rec = os.path.join(K['seat_record'], 'mail', 'READY-%s.txt' % N)
    if os.path.exists(rec):
        s = open(rec, encoding='utf-8').read(); same = r.strip() == s.strip() or body(s) == r.strip()
        print('READY as captured == the seat\'s record %s (stripped, header block removed): %s' % (rec, same))
        if not same: bad.append('the captured READY != %s' % rec)
    else: print('NOTE: the seat\'s record %s does not exist (reported, not refused)' % rec)
if not route: bad.append("Wednesday's route (a) ANSWER (the authority) is not in the capture")
if ready and not all(x in ready[0] for x in ('13/13', '2dc03e152a5dbc13')): bad.append('the READY lacks 13/13 or the new-ticket title sha256 prefix')
loc = os.path.join(G, 'READY_1363_mail.md')
if ready and os.path.exists(loc):
    lt = open(loc, encoding='utf-8').read(); rb = ready[0].strip(); same = rb in lt or ''.join(rb.split()) in ''.join(lt.split())
    print('READY as captured is contained in the kit copy READY_1363_mail.md (whitespace-normalised): %s | kit copy sha256 %s' % (same, hashlib.sha256(lt.encode()).hexdigest()[:16]))
    if not same: bad.append('the captured READY != the kit copy READY_1363_mail.md')
out += ['## Wednesday\'s ANSWER files for Seat B 51st (briefs_staged, as written before sending; VERBATIM with sha256; the mails above are the record)', '']
for fn in sorted(glob.glob('/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-*_answer_seatB51_*.md')):
    t = open(fn, encoding='utf-8').read()
    out += ['### %s — sha256 %s' % (os.path.basename(fn), hashlib.sha256(t.encode()).hexdigest()), '', '```', t, '```', '']
    print('ANSWER FILE %s sha256 %s | %d chars' % (os.path.basename(fn), hashlib.sha256(t.encode()).hexdigest()[:16], len(t)))
open(os.path.join(G, 'mail_gate50a_ready.md'), 'w', encoding='utf-8').write('\n'.join(out) + '\n')
for b in bad: print('PROBLEM: ' + b)
print('CAPTURE %s: %d mails by id (%d READY), %d problem(s) -> mail_gate50a_ready.md' % ('OK' if not bad else 'FAILED', len(sel), len(ready), len(bad)))
raise SystemExit(1 if bad else 0)
