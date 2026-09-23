#!/usr/bin/env python3
"""capture_mail_r2.py — read-only: capture, verbatim and by message id, from wednesday-agent@ the mails the #1210 round-2 re-gate needs:
the tier-1 QA verdict (coagent@, `[QA -> Wednesday] TIER-1 BATCH GATE`), every Seat B 22nd (secuura-blockchain@, `[Secuura/Blockchain-B ->`)
mail and every Wednesday `[Wednesday -> Secuura/Blockchain-B]` mail at/after WINDOW_START. Never marks seen (direct GET). Key by NAME, never
printed. Filters on from-address AND subject prefix: no other client's mail is fetched. Writes only into this dir; never overwrites.
Then builds mail_r2_ready.md = READY round 2 for #1210 (the launcher greps it) + the QA round-1 verdict. `--list` prints subjects only."""
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
print('listed', len(msgs), 'oldest', min((m.get('timestamp') or '') for m in msgs), 'newest', max((m.get('timestamp') or '') for m in msgs))
WINDOW_START = '2026-09-23T08:59'
if len(msgs) >= 200 and min((m.get('timestamp') or '') for m in msgs) >= WINDOW_START: print('WARNING: listing may be TRUNCATED'); sys.exit(2)
def sub(m): return m.get('subject') or ''
def frm(m): return str(m.get('from'))
def want(m):
    if str(m.get('timestamp') or '') < WINDOW_START: return False
    s = sub(m); f = frm(m)
    return ('secuura-blockchain@' in f and s.startswith('[Secuura/Blockchain-B ->')) or ('wednesday-agent@' in f and s.startswith('[Wednesday -> Secuura/Blockchain-B]')) \
        or ('coagent@' in f and s.startswith('[QA -> Wednesday] TIER-1 BATCH GATE'))
hits = sorted([m for m in msgs if want(m)], key=lambda x: x.get('timestamp') or '')
cap = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
def slug(s):
    s = s.split('] ', 1)[1] if '] ' in s else s
    return re.sub(r'[^A-Za-z0-9]+', '_', s).strip('_').lower()[:50]
files = []
for m in hits:
    s = sub(m); ts = str(m.get('timestamp') or ''); hhmm = re.sub(r'[^0-9]', '', ts[11:19])
    print(ts, '|', frm(m), '|', s, '|', m.get('message_id'))
    if '--list' in sys.argv: continue
    who = 'qa' if 'coagent@' in frm(m) else ('seatB22' if 'secuura-blockchain@' in frm(m) else 'wed')
    name = 'mail_%s_%s_%s.md' % (who, slug(s), hhmm)
    out = os.path.join(G, name)
    if os.path.exists(out): print('  exists, not overwritten:', name)
    else:
        full = get(base + '/' + urllib.parse.quote(m['message_id'], safe=''))
        txt = full.get('text') or ''
        with open(out, 'w', encoding='utf-8') as f:
            f.write('SUBJECT: ' + s + '\nFROM: ' + frm(m) + '\nTO: ' + str(full.get('to')) + '\nTS: ' + ts + '\nMESSAGE_ID: ' + m['message_id']
                    + '\nCAPTURED: ' + cap + ' by the gate20T1r2 (#1210 round 2) drafter, read-only by message id (key by name, never printed)'
                    + '\nTEXT_SHA256: ' + hashlib.sha256(txt.encode()).hexdigest() + '\n' + txt + '\n')
        print('  written', name, len(txt), 'chars')
    files.append((who, s, out))
if '--list' in sys.argv: sys.exit(0)
ready = [x for x in files if x[0] == 'seatB22' and 'READY' in x[1].upper() and ('KS-1239' in x[1] or '1210' in x[1])]
verdict = [x for x in files if x[0] == 'qa']
comb = os.path.join(G, 'mail_r2_ready.md')
with open(comb, 'w', encoding='utf-8') as f:
    f.write('COMBINED CAPTURE (rebuilt ' + cap + ') for the #1210 KS-1239 round-2 re-gate: the seat\'s READY round 2 mail(s) for #1210, then the tier-1 QA round-1 verdict; each section verbatim from the per-mail file named in its header.\n')
    for who, s, out in ready + verdict:
        f.write('\n\n' + '#' * 8 + ' ' + os.path.basename(out) + ' ' + '#' * 8 + '\n' + open(out, encoding='utf-8').read())
print('combined', comb, '| READY r2 sections', len(ready), '| QA verdict sections', len(verdict))
sys.exit(0 if ready and verdict else 8)
