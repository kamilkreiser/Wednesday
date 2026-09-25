#!/usr/bin/env python3
"""capture_mail_gate21T2c.py — READ-ONLY: capture, verbatim and by message id, from wednesday-agent@ the Secuura/Blockchain mails the round-21 THIRD
tier-2 batch gate needs (#1218 round 2 KS-897+KS-896 from Seat L4; #1233 KS-1133, #1237 KS-1229, #1238 KS-1158 and #1219 KS-1277 from Seat L1; #1235
KS-1140 and #1236 KS-1110 from Seat B 25th; #1223 KS-1118 round 2 from Seat L1 ONLY if its READY exists at capture time). Never marks seen (list GET +
direct GET by id; the fleet's inbox_digest.sh is NOT used). AGENTMAIL_API_KEY by NAME from Wednesday's .env, never printed. Filters on the
from-address (secuura-blockchain@ / wednesday-agent@) AND the Secuura/Blockchain subject prefixes AND the window: no other client's mail is fetched.
Writes only beside itself (mail_*.md); never overwrites. Then builds mail_gate21T2c_ready.md = the READY set. The launcher greps it. Derived from
gate21T1b's capture_mail_gate21T1b.py, re-keyed.
Usage: capture_mail_gate21T2c.py [--list]"""
import hashlib, json, os, sys, urllib.request, urllib.parse, datetime, re
G = os.path.dirname(os.path.abspath(__file__))
key = ''
for line in open('/Volumes/DevMASTER/WEDNESDAY/4_Credentials/.env', encoding='utf-8'):
    if line.startswith('AGENTMAIL_API_KEY='): key = line.split('=', 1)[1].split('#')[0].strip().strip('"').strip("'")
assert key, 'AGENTMAIL_API_KEY unset'
H = {'Authorization': 'Bearer ' + key}
base = 'https://api.agentmail.to/v0/inboxes/wednesday-agent@agentmail.to/messages'
def get(u): return json.load(urllib.request.urlopen(urllib.request.Request(u, headers=H), timeout=60))
msgs = get(base + '?limit=200').get('messages', [])
WINDOW_START = '2026-09-25T00:00'
print('listed', len(msgs), 'oldest', min((m.get('timestamp') or '') for m in msgs), 'newest', max((m.get('timestamp') or '') for m in msgs))
if len(msgs) >= 200 and min((m.get('timestamp') or '') for m in msgs) >= WINDOW_START: print('WARNING: listing may be TRUNCATED'); sys.exit(2)
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
KEYS = ('KS-897', 'KS-896', '#1218', 'KS-1277', '#1219', 'KS-1133', '#1233', 'KS-1140', '#1235', 'KS-1110', '#1236', 'KS-1229', '#1237', 'KS-1158', '#1238',
        'KS-1118', '#1223')
files = []
for m in hits:
    s = sub(m); ts = str(m.get('timestamp') or ''); hhmm = re.sub(r'[^0-9]', '', ts[11:19])
    print(ts, '|', frm(m), '|', s, '|', m.get('message_id'))
    if '--list' in sys.argv: continue
    # narrowed: the batch's keys/PRs; the three seats' lane briefs, plan QUESTIONs + ANSWERs and wraps; EVERYTHING from 05:30Z on for the three seats
    # (the round-1 GO / NO GO, the pre-push-suite FLEET SAFETY rulings, the develop move) — COORDINATIONs only as the un-suffixed copy (no -B/-C/-D/-E dupes)
    seatish = ('Seat L1' in s or 'Seat L4' in s or 'Seat B 25th' in s or s.startswith('[Wednesday -> Secuura/Blockchain-B]') or s.startswith('[Wednesday -> Secuura/Blockchain-E]'))
    coord = 'COORDINATION' in s
    rel = (any(k in s for k in KEYS) and not (coord and not s.startswith('[Wednesday -> Secuura/Blockchain] '))) \
        or (seatish and not coord and ('plan confirmation' in s or 'plan CONFIRMED' in s or 'lane' in s or 'Session wrap' in s)) \
        or (ts >= '2026-09-25T05:30' and not coord and (seatish or 'GO' in s or 'MERGED' in s)) \
        or (ts >= '2026-09-25T05:30' and coord and s.startswith('[Wednesday -> Secuura/Blockchain] '))
    if not rel: continue
    _m = re.search(r'\(Seat (L\d|B 25th)\)', s) or re.search(r'Seat (L\d|B 25th)', s); seat = _m.group(1).replace(' ', '') if _m else ''
    who = 'wed' if 'wednesday-agent@' in frm(m) else ('seat' + seat if seat else 'secuura')
    name = 'mail_%s_%s_%s.md' % (who, slug(s), hhmm)
    out = os.path.join(G, name)
    if os.path.exists(out): print('  exists, not overwritten:', name)
    else:
        full = get(base + '/' + urllib.parse.quote(m['message_id'], safe=''))
        txt = full.get('text') or ''
        with open(out, 'w', encoding='utf-8') as f:
            f.write('SUBJECT: ' + s + '\nFROM: ' + frm(m) + '\nTO: ' + str(full.get('to')) + '\nTS: ' + ts + '\nMESSAGE_ID: ' + m['message_id']
                    + '\nCAPTURED: ' + cap + ' by the gate21T2c drafter, read-only by message id (key by name, never printed)'
                    + '\nTEXT_SHA256: ' + hashlib.sha256(txt.encode()).hexdigest() + '\n' + txt + '\n')
        print('  written', name, len(txt), 'chars')
    files.append((who, s, out, ts))
if '--list' in sys.argv: sys.exit(0)
# the READY set, by subject shape (never 'READY' alone would do: 'ALREADY' contains it — every match below needs 'READY ' + a seat marker)
# WIDENED 06:3xZ by Wednesday: #1223 KS-1118 ROUND 2 (READY FOR QA 9, 06:27:55Z) joins — eight, frozen there. The two ROUND-1 READYs (#1218 L4 READY 1,
# #1223 L1 READY 3) ride along as CONTEXT sections: the round-2 READYs never restate the ticket keys / the round-1 claims they answer.
READY_SUBJ = ('READY FOR QA ROUND 2 (Seat L4)', 'READY FOR QA 5/6/7 (Seat L1)', 'READY 6+7 (Seat B 25th)', 'READY FOR QA 1 (Seat L1)',
              'READY FOR QA 9 (Seat L1): #1223 KS-1118 ROUND 2', 'READY FOR QA 1 (Seat L4): #1218', 'READY FOR QA 3 (Seat L1): #1223')
ready = [x for x in files if x[0] != 'wed' and any(r in x[1] for r in READY_SUBJ)]
r1223 = [x for x in files if x[0] != 'wed' and 'READY' in x[1] and ('#1223' in x[1] or 'KS-1118' in x[1]) and 'ROUND 2' in x[1].upper()]
print('#1223 round-2 READY present:', bool(r1223), [x[1] for x in r1223])
ready += [x for x in r1223 if x not in ready]
comb = os.path.join(G, 'mail_gate21T2c_ready.md')
with open(comb, 'w', encoding='utf-8') as f:
    f.write('COMBINED CAPTURE (rebuilt ' + cap + ') for the round-21 THIRD tier-2 batch gate #1218 (round 2) #1219 #1233 #1235 #1236 #1237 #1238: the READY '
            'mails verbatim from the per-mail file named in each header (Seat L4 READY FOR QA ROUND 2 #1218; Seat L1 READY FOR QA 5/6/7 #1233 #1237 #1238; '
            'Seat B 25th READY 6+7 #1235 #1236; Seat L1 READY for #1219; Seat L1 READY FOR QA 9 #1223 ROUND 2 — widened by Wednesday 06:3xZ, eight, frozen). '
            'Two sections are ROUND-1 CONTEXT, not READYs for these heads: Seat L4 READY FOR QA 1 (#1218 at 999623d28) and Seat L1 READY FOR QA 3 (#1223 at 759726d8d).\n')
    for who, s, out, ts in ready:
        f.write('\n\n' + '#' * 8 + ' ' + os.path.basename(out) + ' ' + '#' * 8 + '\n' + open(out, encoding='utf-8').read())
body = open(comb, encoding='utf-8').read()
covered = {k: k in body for k in ('KS-897', 'KS-896', 'KS-1277', 'KS-1133', 'KS-1140', 'KS-1110', 'KS-1229', 'KS-1158', 'KS-1118',
                                  '#1218', '#1219', '#1223', '#1233', '#1235', '#1236', '#1237', '#1238')}
print('combined', comb, '| sections', len(ready), [os.path.basename(o) for _, _, o, _ in ready], '| per key', covered)
sys.exit(0 if all(covered.values()) else 8)
