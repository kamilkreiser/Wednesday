#!/usr/bin/env python3
"""capture_mail_gate21T1b.py — READ-ONLY: capture, verbatim and by message id, from wednesday-agent@ the Secuura/Blockchain mails the round-21 SECOND
tier-1 batch gate needs (#1224 KS-1179 + #1226 KS-872 from Seat L3; #1228 KS-1171 from Seat L2; #1230 KS-1131 from Seat B 25th — widened by
Wednesday 05:2xZ, frozen at four). Never marks seen (list GET + direct GET by id; the
fleet's inbox_digest.sh is NOT used). AGENTMAIL_API_KEY by NAME from Wednesday's .env, never printed. Filters on the from-address
(secuura-blockchain@ / wednesday-agent@) AND the Secuura/Blockchain subject prefixes AND the window: no other client's mail is fetched. Writes only
beside itself (mail_*.md); never overwrites. Then builds mail_gate21T1b_ready.md = Seat L2's READY FOR QA 4 (#1228) + Seat L3's SESSION WRAP (which
carries L3's READYs for #1224 and #1226 — L3 sent no separate READY mail for them; see capture_list.out) + L3's READY 2+3 (the KS-1179/KS-872
pre-announcement) + Seat B 25th's PUSHED + READY 3/4/5 (05:15:44Z; its #1230 section is the READY — #1231/#1232 in it are tier 2, NOT this gate). The launcher greps it. Derived from gate21T1's capture_mail_gate21T1.py, re-keyed.
Usage: capture_mail_gate21T1b.py [--list]"""
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
KEYS = ('KS-1179', 'KS-872', 'KS-1171', 'KS-1292', '#1224', '#1226', '#1228', 'KS-1131', '#1230')
files = []
for m in hits:
    s = sub(m); ts = str(m.get('timestamp') or ''); hhmm = re.sub(r'[^0-9]', '', ts[11:19])
    print(ts, '|', frm(m), '|', s, '|', m.get('message_id'))
    if '--list' in sys.argv: continue
    # narrowed: the three PRs/keys; Seat L2's and Seat L3's briefs, plan QUESTIONs + ANSWERs and session wraps; Seat L3's legs-3/4/8 QUESTION +
    # ANSWER; the fleet-wide COORDINATIONs (the un-suffixed copy only); the develop move (GO / MERGED / the base-invariant ANSWER and its QUESTION).
    rel = any(k in s for k in KEYS) \
        or (('Seat L2' in s or 'Seat L3' in s or 'Seat B 25th' in s) and ('plan confirmation' in s or 'plan CONFIRMED' in s or 'lane,' in s or 'Session wrap' in s)) \
        or ('Seat B 25th' in s and ('Ornith' in s or 'PUSHED + READY' in s)) \
        or ('Seat L3' in s and 'legs 3/4/8' in s) \
        or s.startswith('[Wednesday -> Secuura/Blockchain] COORDINATION') \
        or 'base-invariant' in s or 'HOLDING the #1214' in s or '] MERGED (' in s or '] GO (' in s
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
                    + '\nCAPTURED: ' + cap + ' by the gate21T1b drafter, read-only by message id (key by name, never printed)'
                    + '\nTEXT_SHA256: ' + hashlib.sha256(txt.encode()).hexdigest() + '\n' + txt + '\n')
        print('  written', name, len(txt), 'chars')
    files.append((who, s, out))
if '--list' in sys.argv: sys.exit(0)
# the READY set: 'READY FOR QA' exactly (never 'READY' alone: 'ALREADY' contains it) naming one of the three, PLUS Seat L3's session wrap (its READYs)
# capture_1 swept in L2's #1216/#1217 READY (its subject names 'KS-1171 census frame'): the READY set keys on THIS batch's PR numbers only
ready = [x for x in files if x[0] != 'wed' and (('READY FOR QA' in x[1] and any(k in x[1] for k in ('#1224', '#1226', '#1228', 'KS-1179 queued')))
                                                or ('PUSHED + READY' in x[1] and '#1230' in x[1])
                                                or (x[0] == 'seatL3' and 'Session wrap' in x[1]))]
comb = os.path.join(G, 'mail_gate21T1b_ready.md')
with open(comb, 'w', encoding='utf-8') as f:
    f.write('COMBINED CAPTURE (rebuilt ' + cap + ') for the round-21 SECOND tier-1 batch gate #1224 #1226 #1228 #1230: Seat L2\'s READY FOR QA 4 (#1228), Seat L3\'s '
            'READY 2+3 (KS-1179/KS-872 announced), Seat L3\'s SESSION WRAP (its READYs for #1224 and #1226) and Seat B 25th\'s PUSHED + READY 3/4/5 (its #1230 KS-1131 '
            'section is the READY; #1231/#1232 in the same mail are tier 2 and NOT in this gate), verbatim from the per-mail file named in each header.\n')
    for who, s, out in ready:
        f.write('\n\n' + '#' * 8 + ' ' + os.path.basename(out) + ' ' + '#' * 8 + '\n' + open(out, encoding='utf-8').read())
body = open(comb, encoding='utf-8').read()
covered = {k: k in body for k in ('KS-1179', 'KS-872', 'KS-1171', 'KS-1131', '#1224', '#1226', '#1228', '#1230')}
print('combined', comb, '| sections', len(ready), [os.path.basename(o) for _, _, o in ready], '| per key', covered)
sys.exit(0 if all(covered.values()) else 8)
