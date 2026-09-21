#!/usr/bin/env python3
"""capture_ready_mail_gate15.py — read-only: capture every Secuura/Blockchain "READY FOR QA (Seat B 15th): PR <N> ..." mail verbatim (by message id)
from wednesday-agent@ into mail_seatB15_ready<k>_pr<N>_<ticket>.md (one per mail, k = the seat's push order 1..10 -> 01..10, never overwritten),
plus EVERY Seat B 15th STATUS / QUESTION mail from the seat and EVERY Wednesday ANSWER / SUCCESSOR mail to Secuura/Blockchain-B that names
"Seat B 15th" in its subject (named by a subject slug + HHMM), and (re)build the combined capture mail_gate15_ready.md = the per-mail READY
captures concatenated in PR push order (1..10), then the STATUS mail(s), then the seat's QUESTION mail(s). Missing READY sections are marked
NOT YET ARRIVED. Wednesday's ANSWERs are captured beside it as context, NOT part of the combined seat capture. Key by NAME from the WEDNESDAY
.env; never printed. Datasec/Tuesday mails are never fetched (the seat filter is on the from-address AND the subject prefix). Writes only into
this gateset dir. Derived from gatesets/2026-09-21_gate1130to1135/capture_ready_mail_1130.py (CORRECTION handling inherited from its S5)."""
import hashlib, json, os, sys, urllib.request, urllib.parse, datetime, re
G = os.path.dirname(os.path.abspath(__file__))
key = ''
for line in open('/Volumes/DevMASTER/WEDNESDAY/4_Credentials/.env', encoding='utf-8'):
    if line.startswith('AGENTMAIL_API_KEY='): key = line.split('=', 1)[1].split('#')[0].strip().strip('"').strip("'")
assert key, 'AGENTMAIL_API_KEY unset'
H = {'Authorization': 'Bearer ' + key}
base = 'https://api.agentmail.to/v0/inboxes/wednesday-agent@agentmail.to/messages'
def get(u): return json.load(urllib.request.urlopen(urllib.request.Request(u, headers=H), timeout=60))
msgs = get(base + '?limit=60').get('messages', [])
print('listed', len(msgs), 'oldest', min((m.get('timestamp') or '') for m in msgs))
SUBJ = '[Secuura/Blockchain -> Wednesday] READY FOR QA (Seat B 15th): PR '
SEAT_PFX = '[Secuura/Blockchain -> Wednesday] '
WED_PFX = '[Wednesday -> Secuura/Blockchain-B] '
ORDER = {str(i): '%02d' % i for i in range(1, 11)}
def is_seat(m): return 'secuura-blockchain@' in str(m.get('from'))
def is_wed(m): return 'wednesday-agent@' in str(m.get('from'))
def sub(m): return m.get('subject') or ''
def seat15(s): return 'Seat B 15th' in s
hits = [m for m in msgs if (is_seat(m) and sub(m).startswith(SEAT_PFX) and seat15(sub(m)))
        or (is_wed(m) and sub(m).startswith(WED_PFX) and seat15(sub(m)))]
cap = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
files = {}
def slug(s):
    s = s.split('] ', 1)[1] if '] ' in s else s
    s = re.sub(r'[^A-Za-z0-9]+', '_', s).strip('_').lower()
    return s[:60]
for m in sorted(hits, key=lambda x: x.get('timestamp') or ''):
    s = sub(m); ts = str(m.get('timestamp') or '')
    hhmm = re.sub(r'[^0-9]', '', ts[11:16]) or '0000'
    print(ts, '|', m.get('from'), '|', s, '|', m.get('message_id'))
    mm = re.match(re.escape(SUBJ) + r'(\d+) (KS-\d+)', s)
    if mm and is_seat(m):
        n, tk = mm.groups(); k = ORDER.get(n)
        if k is None: print('  UNKNOWN PR number', n, '- skipped'); continue
        name = 'mail_seatB15_ready%s_pr%s_%s.md' % (k, n, tk.lower().replace('-', ''))
        if 'CORRECTION' in s.upper():
            k = k + 'C_' + hhmm; name = 'mail_seatB15_ready%s_pr%s_%s_CORRECTION_%s.md' % (ORDER[n], n, tk.lower().replace('-', ''), hhmm)
    elif is_seat(m) and s.startswith(SEAT_PFX + 'STATUS'):
        k = 'S_' + hhmm; name = 'mail_seatB15_status_%s.md' % hhmm
    elif is_seat(m) and s.startswith(SEAT_PFX + 'QUESTION'):
        k = 'Q_' + hhmm; name = 'mail_seatB15_question_%s_%s.md' % (slug(s)[:40], hhmm)
    elif is_wed(m):
        k = 'W_' + hhmm; name = 'mail_wed_%s_%s.md' % (slug(s)[:40], hhmm)
    else:
        k = 'O_' + hhmm; name = 'mail_seatB15_other_%s_%s.md' % (slug(s)[:40], hhmm)
    out = os.path.join(G, name)
    if os.path.exists(out):
        print('  exists, not overwritten:', name)
    else:
        full = get(base + '/' + urllib.parse.quote(m['message_id'], safe=''))
        txt = full.get('text') or ''
        with open(out, 'w', encoding='utf-8') as f:
            f.write('SUBJECT: ' + s + '\nFROM: ' + str(m.get('from')) + '\nTO: ' + str(full.get('to')) + '\nTS: ' + ts
                    + '\nMESSAGE_ID: ' + m['message_id'] + '\nCAPTURED: ' + cap + ' by the gate15 (Seat B 15th ten-PR) drafter, read-only by message id from wednesday-agent@ (key by name, never printed)'
                    + '\nTEXT_SHA256: ' + hashlib.sha256(txt.encode()).hexdigest() + '\n' + txt + '\n')
        print('  written', name, len(txt), 'chars')
    files[k] = out
comb = os.path.join(G, 'mail_gate15_ready.md')
with open(comb, 'w', encoding='utf-8') as f:
    f.write('COMBINED CAPTURE (rebuilt ' + cap + ') of the Seat B 15th READY FOR QA mails in PR push order (1..10 = 01..10), then the seat\'s STATUS mail(s), then the seat\'s QUESTION mail(s) (plan confirmation 12:02Z; any later); each section is the verbatim per-mail capture file named in its header. Wednesday\'s ANSWER / SUCCESSOR mails are captured beside this file (mail_wed_*.md) and are NOT part of this combined seat capture.\n')
    for k in ['%02d' % i for i in range(1, 11)]:
        if k in files:
            f.write('\n\n' + '#' * 8 + ' ' + os.path.basename(files[k]) + ' ' + '#' * 8 + '\n')
            f.write(open(files[k], encoding='utf-8').read())
            for kc in sorted(x for x in files if x.startswith(k + 'C_')):
                f.write('\n\n' + '#' * 8 + ' ' + os.path.basename(files[kc]) + ' (the seat\'s CORRECTION to the READY above) ' + '#' * 8 + '\n')
                f.write(open(files[kc], encoding='utf-8').read())
        else:
            f.write('\n\n' + '#' * 8 + ' section ' + k + ' (push-order slot ' + k + '): NOT YET ARRIVED at ' + cap + ' ' + '#' * 8 + '\n')
    for k in sorted(x for x in files if x.startswith('S_')) + sorted(x for x in files if x.startswith('Q_')):
        f.write('\n\n' + '#' * 8 + ' ' + os.path.basename(files[k]) + ' ' + '#' * 8 + '\n')
        f.write(open(files[k], encoding='utf-8').read())
print('combined', comb, 'sections', sorted(files))
