#!/usr/bin/env python3
"""capture_mail_gate21T1.py — READ-ONLY: capture, verbatim and by message id, from wednesday-agent@ the Secuura/Blockchain mails the round-21
tier-1 batch gate needs (#1213 KS-530 + #1214 KS-528 from Seat B 25th; #1216 KS-975 + #1217 KS-976 from Seat L2). Never marks seen (direct GET by id).
AGENTMAIL_API_KEY by NAME from Wednesday's .env, never printed. Filters on the from-address (secuura-blockchain@ / wednesday-agent@) AND the
Secuura/Blockchain subject prefixes AND the window: no other client's mail is fetched. Writes only beside itself (mail_*.md); never overwrites.
Then builds mail_gate21T1_ready.md = every READY-class mail naming one of the four PRs/keys (the launcher greps it).
Usage: capture_mail_gate21T1.py [--list]"""
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
KEYS = ('KS-530', 'KS-528', 'KS-975', 'KS-976', '#1213', '#1214', '#1216', '#1217')
files = []
for m in hits:
    s = sub(m); ts = str(m.get('timestamp') or ''); hhmm = re.sub(r'[^0-9]', '', ts[11:19])
    print(ts, '|', frm(m), '|', s, '|', m.get('message_id'))
    if '--list' in sys.argv: continue
    rel = any(k in s for k in KEYS) or 'Seat B 25th' in s or 'Seat L2' in s or 'audit row' in s \
        or (s.startswith('[Wednesday -> Secuura/Blockchain] COORDINATION') and 'legs 3/4/8' in s) \
        or (s.startswith('[Wednesday -> Secuura/Blockchain] COORDINATION') and 'load false-red' in s)
    if not rel: continue
    who = 'wed' if 'wednesday-agent@' in frm(m) else ('seatL2' if 'Seat L2' in s or 'Blockchain-C' in s else ('seatB25' if 'Blockchain-B' in s or 'Seat B 25' in s else 'secuura'))
    name = 'mail_%s_%s_%s.md' % (who, slug(s), hhmm)
    out = os.path.join(G, name)
    if os.path.exists(out): print('  exists, not overwritten:', name)
    else:
        full = get(base + '/' + urllib.parse.quote(m['message_id'], safe=''))
        txt = full.get('text') or ''
        with open(out, 'w', encoding='utf-8') as f:
            f.write('SUBJECT: ' + s + '\nFROM: ' + frm(m) + '\nTO: ' + str(full.get('to')) + '\nTS: ' + ts + '\nMESSAGE_ID: ' + m['message_id']
                    + '\nCAPTURED: ' + cap + ' by the gate21T1 drafter, read-only by message id (key by name, never printed)'
                    + '\nTEXT_SHA256: ' + hashlib.sha256(txt.encode()).hexdigest() + '\n' + txt + '\n')
        print('  written', name, len(txt), 'chars')
    files.append((who, s, out))
if '--list' in sys.argv: sys.exit(0)
ready = [x for x in files if x[0] != 'wed' and 'READY FOR QA' in x[1] and any(k in x[1] for k in KEYS)]   # 'READY FOR QA' exactly: 'ALREADY' contains READY (capture_1 swept one in)
comb = os.path.join(G, 'mail_gate21T1_ready.md')
with open(comb, 'w', encoding='utf-8') as f:
    f.write('COMBINED CAPTURE (rebuilt ' + cap + ') for the round-21 tier-1 batch gate #1213 #1214 #1216 #1217: every READY FOR QA mail naming one of the four, verbatim from the per-mail file named in its header.\n')
    for who, s, out in ready:
        f.write('\n\n' + '#' * 8 + ' ' + os.path.basename(out) + ' ' + '#' * 8 + '\n' + open(out, encoding='utf-8').read())
covered = {k: any(k in s for _, s, _ in ready) for k in ('KS-530', 'KS-528', 'KS-975', 'KS-976')}
print('combined', comb, '| READY sections', len(ready), '| per key', covered)
sys.exit(0 if all(covered.values()) else 8)
