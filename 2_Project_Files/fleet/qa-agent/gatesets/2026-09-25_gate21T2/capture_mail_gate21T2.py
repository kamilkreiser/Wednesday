#!/usr/bin/env python3
"""capture_mail_gate21T2.py — READ-ONLY: capture, verbatim and by message id, from wednesday-agent@ the Secuura/Blockchain mails the round-21
TIER-2 batch gate needs (#1215 KS-1288 Seat L3; #1218 KS-897+KS-896 Seat L4; #1220 KS-1129 Seat L2; #1221 KS-1266 Seat L1; #1222 KS-1181 F2 Seat L3; #1223 KS-1118 Seat L1 — #1222/#1223 added by Wednesday mid-draft; FROZEN at six). Never marks seen
(direct GET by id). AGENTMAIL_API_KEY by NAME from Wednesday's .env, never printed. Filters on the from-address (secuura-blockchain@ /
wednesday-agent@) AND the Secuura/Blockchain subject prefixes AND the window: no other client's mail is fetched. Writes only beside itself
(mail_*.md); never overwrites. Then builds mail_gate21T2_ready.md = every READY-class mail naming one of the four PRs/keys (the launcher greps it).
Derived from gate21T1's capture_mail_gate21T1.py, re-keyed. Usage: capture_mail_gate21T2.py [--list]"""
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
KEYS = ('KS-1288', 'KS-897', 'KS-896', 'KS-1129', 'KS-1266', 'KS-1181', 'KS-1118', '#1223', '#1215', '#1218', '#1220', '#1221', '#1222', 'KS1288', 'KS897', 'KS1129', 'KS1266', 'KS1181', 'KS1118', 'ks1118', 'ks1129', 'ks1266', 'ks1288', 'ks897', 'ks1181')
SEATS = ('Seat L1', 'Seat L2', 'Seat L3', 'Seat L4')
files = []
for m in hits:
    s = sub(m); ts = str(m.get('timestamp') or ''); hhmm = re.sub(r'[^0-9]', '', ts[11:19])
    print(ts, '|', frm(m), '|', s, '|', m.get('message_id'))
    if '--list' in sys.argv: continue
    # narrowed: the four PRs/keys; each lane seat's brief, plan QUESTION + ANSWER; the fleet-wide COORDINATIONs (the un-suffixed copy only);
    # Seat L3's legs-3/4/8 QUESTION + ANSWER (the stack-at-the-gate ruling); Seat L2's anchoring findings + the KS-562 wording ANSWER.
    rel = any(k in s for k in KEYS) \
        or (any(x in s for x in SEATS) and ('plan confirmation' in s or 'plan CONFIRMED' in s or 'lane,' in s)) \
        or s.startswith('[Wednesday -> Secuura/Blockchain] COORDINATION') \
        or ('Seat L3' in s and 'legs 3/4/8' in s) \
        or ('Seat L2' in s and ('FINDINGS' in s or 'TWO FINDINGS' in s or 'both findings' in s or 'ks1129' in s))
    if not rel: continue
    _m = re.search(r'\(Seat (L\d)\)', s) or re.search(r'Seat (L\d)', s); seat = ('Seat ' + _m.group(1)) if _m else ''   # the subject's own (Seat Lx) tag first
    who = 'wed' if 'wednesday-agent@' in frm(m) else ('seat' + seat.split()[-1] if seat else 'secuura')
    name = 'mail_%s_%s_%s.md' % (who, slug(s), hhmm)
    out = os.path.join(G, name)
    if os.path.exists(out): print('  exists, not overwritten:', name)
    else:
        full = get(base + '/' + urllib.parse.quote(m['message_id'], safe=''))
        txt = full.get('text') or ''
        with open(out, 'w', encoding='utf-8') as f:
            f.write('SUBJECT: ' + s + '\nFROM: ' + frm(m) + '\nTO: ' + str(full.get('to')) + '\nTS: ' + ts + '\nMESSAGE_ID: ' + m['message_id']
                    + '\nCAPTURED: ' + cap + ' by the gate21T2 drafter, read-only by message id (key by name, never printed)'
                    + '\nTEXT_SHA256: ' + hashlib.sha256(txt.encode()).hexdigest() + '\n' + txt + '\n')
        print('  written', name, len(txt), 'chars')
    files.append((who, s, out))
if '--list' in sys.argv: sys.exit(0)
ready = [x for x in files if x[0] != 'wed' and 'READY FOR QA' in x[1] and any(k in x[1] for k in KEYS)]
comb = os.path.join(G, 'mail_gate21T2_ready.md')
with open(comb, 'w', encoding='utf-8') as f:
    f.write('COMBINED CAPTURE (rebuilt ' + cap + ') for the round-21 TIER-2 batch gate #1215 #1218 #1220 #1221 #1222 #1223: every READY FOR QA mail naming one of the four, verbatim from the per-mail file named in its header.\n')
    for who, s, out in ready:
        f.write('\n\n' + '#' * 8 + ' ' + os.path.basename(out) + ' ' + '#' * 8 + '\n' + open(out, encoding='utf-8').read())
covered = {k: any(k in open(o, encoding='utf-8').read() for _, s, o in ready) for k in ('KS-1288', 'KS-897', 'KS-1129', 'KS-1266', 'KS-1181', 'KS-1118')}
print('combined', comb, '| READY sections', len(ready), '| per key', covered)
sys.exit(0 if all(covered.values()) else 8)
