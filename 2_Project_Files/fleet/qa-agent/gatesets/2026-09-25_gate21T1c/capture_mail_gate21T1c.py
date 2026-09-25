#!/usr/bin/env python3
"""capture_mail_gate21T1c.py — READ-ONLY: capture, verbatim and by message id, from wednesday-agent@ the Secuura/Blockchain mails the round-21 THIRD
tier-1 batch gate (#1234 KS-1127+KS-1089+KS-1135, Seat L4; #1239 KS-1263, Seat L1) needs. List GET + direct GET by id only (never marks seen; the
fleet's inbox_digest.sh is NOT used). AGENTMAIL_API_KEY by NAME from Wednesday's .env, never printed. Filters on the from-address
(secuura-blockchain@ / wednesday-agent@) AND the Secuura/Blockchain subject prefixes AND the 2026-09-25 window: no other client's mail is fetched.
Writes only beside itself (mail_*.md); never overwrites. Then builds mail_gate21T1c_ready.md = Seat L4's READY FOR QA 4 (#1234, 06:17:31Z) + Seat
L1's READY FOR QA 8 (#1239 KS-1263, 06:18:33Z), verbatim. The launcher greps it. Derived from gate21T1b's capture_mail_gate21T1b.py, re-keyed.
Usage: capture_mail_gate21T1c.py [--list]"""
import hashlib, json, os, sys, urllib.request, urllib.parse, datetime, re
G = os.path.dirname(os.path.abspath(__file__))
key = ''
for line in open('/Volumes/DevMASTER/WEDNESDAY/4_Credentials/.env', encoding='utf-8'):
    if line.startswith('AGENTMAIL_API_KEY='): key = line.split('=', 1)[1].split('#')[0].strip().strip('"').strip("'")
assert key, 'AGENTMAIL_API_KEY unset'
H = {'Authorization': 'Bearer ' + key}
base = 'https://api.agentmail.to/v0/inboxes/wednesday-agent@agentmail.to/messages'
def get(u): return json.load(urllib.request.urlopen(urllib.request.Request(u, headers=H), timeout=60))
msgs = get(base + '?limit=300').get('messages', [])
WINDOW_START = '2026-09-25T00:00'
print('listed', len(msgs), 'oldest', min((m.get('timestamp') or '') for m in msgs), 'newest', max((m.get('timestamp') or '') for m in msgs))
if len(msgs) >= 300 and min((m.get('timestamp') or '') for m in msgs) >= WINDOW_START: print('WARNING: listing may be TRUNCATED'); sys.exit(2)
def sub(m): return m.get('subject') or ''
def frm(m): return str(m.get('from'))
def want(m):
    if str(m.get('timestamp') or '') < WINDOW_START: return False
    s = sub(m); f = frm(m)
    return ('secuura-blockchain@' in f and s.startswith('[Secuura/Blockchain')) or ('wednesday-agent@' in f and s.startswith('[Wednesday -> Secuura/Blockchain'))
hits = sorted([m for m in msgs if want(m)], key=lambda x: x.get('timestamp') or '')
cap = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
def slug(s):
    s = s.split('] ', 1)[1] if '] ' in s else s
    return re.sub(r'[^A-Za-z0-9]+', '_', s).strip('_').lower()[:50]
KEYS = ('#1234', '#1239', 'KS-1263', 'KS-1127', 'KS-1089', 'KS-1135', 'Q-G4', '#1218', 'FIXTURE', 'pre-push suite')
files = []
for m in hits:
    s = sub(m); ts = str(m.get('timestamp') or ''); hhmm = re.sub(r'[^0-9]', '', ts[11:19])
    print(ts, '|', frm(m), '|', s, '|', m.get('message_id'))
    if '--list' in sys.argv: continue
    # narrowed: the two PRs / five keys; Seat L1's and Seat L4's lane briefs, plan QUESTIONs + ANSWERs, wraps and the READY-then-wrap ANSWERs; the
    # #1218 NO GO + the fleet pre-push SAFETY COORDINATIONs (the un-suffixed copy only); the develop move (Seat B 26th's GOs / MERGED / plan).
    rel = any(k in s for k in KEYS) \
        or (('Seat L1' in s or 'Seat L4' in s) and ('plan confirmation' in s or 'plan CONFIRMED' in s or 'lane,' in s or 'Session wrap' in s or 'then wrap' in s or 'ctx 80%' in s)) \
        or ('Seat L4' in s and 'PR 2 tier 1' in s) \
        or s.startswith('[Wednesday -> Secuura/Blockchain] COORDINATION') \
        or ('Seat B 26th' in s)
    if not rel: continue
    _m = re.search(r'\(Seat (L\d|B 2\dth)\)', s) or re.search(r'Seat (L\d|B 2\dth)', s); seat = _m.group(1).replace(' ', '') if _m else ''
    who = 'wed' if 'wednesday-agent@' in frm(m) else ('seat' + seat if seat else 'secuura')
    name = 'mail_%s_%s_%s.md' % (who, slug(s), hhmm)
    out = os.path.join(G, name)
    if os.path.exists(out): print('  exists, not overwritten:', name)
    else:
        full = get(base + '/' + urllib.parse.quote(m['message_id'], safe=''))
        txt = full.get('text') or ''
        with open(out, 'w', encoding='utf-8') as f:
            f.write('SUBJECT: ' + s + '\nFROM: ' + frm(m) + '\nTO: ' + str(full.get('to')) + '\nTS: ' + ts + '\nMESSAGE_ID: ' + m['message_id']
                    + '\nCAPTURED: ' + cap + ' by the gate21T1c drafter, read-only by message id (key by name, never printed)'
                    + '\nTEXT_SHA256: ' + hashlib.sha256(txt.encode()).hexdigest() + '\n' + txt + '\n')
        print('  written', name, len(txt), 'chars')
    files.append((who, s, out))
if '--list' in sys.argv: sys.exit(0)
# the READY set: 'READY FOR QA' exactly naming #1234 (Seat L4) or #1239 (Seat L1) — never 'READY' alone ('ALREADY' contains it)
ready = [x for x in files if x[0] != 'wed' and 'READY FOR QA' in x[1] and (('#1234' in x[1] and x[0] == 'seatL4') or ('#1239' in x[1] and x[0] == 'seatL1'))]
comb = os.path.join(G, 'mail_gate21T1c_ready.md')
with open(comb, 'w', encoding='utf-8') as f:
    f.write('COMBINED CAPTURE (rebuilt ' + cap + ') for the round-21 THIRD tier-1 batch gate #1234 #1239: Seat L4\'s READY FOR QA 4 (#1234 KS-1127 + KS-1089 + '
            'KS-1135) and Seat L1\'s READY FOR QA 8 (#1239 KS-1263), verbatim from the per-mail file named in each header.\n')
    for who, s, out in ready:
        f.write('\n\n' + '#' * 8 + ' ' + os.path.basename(out) + ' ' + '#' * 8 + '\n' + open(out, encoding='utf-8').read())
body = open(comb, encoding='utf-8').read()
covered = {k: k in body for k in ('#1234', '#1239', 'KS-1127', 'KS-1089', 'KS-1135', 'KS-1263')}
print('combined', comb, '| sections', len(ready), [os.path.basename(o) for _, _, o in ready], '| per key', covered)
sys.exit(0 if all(covered.values()) and len(ready) == 2 else 8)
