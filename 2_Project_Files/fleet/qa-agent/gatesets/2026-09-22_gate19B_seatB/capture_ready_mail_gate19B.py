#!/usr/bin/env python3
"""capture_ready_mail_gate19B.py — read-only: capture every Seat B 19th/20th READY FOR QA mail verbatim (by message id) from wednesday-agent@ into
mail_seatB19_ready<k>_pr<N>_<ticket>.md (READY 1-3, tagged "(Seat B 19th)") / mail_seatB20_ready<k>_pr<N>_<ticket>.md (READY 4-9, tagged
"(Seat B 20th)") — k = the seat's push order 01..09 — never overwritten; plus EVERY Seat B 19th/20th STATUS / QUESTION / wrap / ACK mail
(mail_seatB19_*.md / mail_seatB20_*.md by the tag in the subject; the 07:55Z HOLD is Wednesday's own capture mail_seatB20_status_hold.md beside —
untouched — and the drafter's own capture mail_seatB20_status_0755.md), EVERY Wednesday mail to Secuura/Blockchain-B in the 19th/20th window
(the two briefs, the S1 ANSWER, the plan ANSWERs, the KS-1164 ANSWER, the band/handover ADDENDUM) as mail_wed_*.md, and — as CONTEXT for item 9 —
Wednesday's ADDENDUM mails to Secuura/Blockchain-C (the F-GUARD (2') addendum 06:22Z, the S1 addendum 04:10Z) as mail_wedC_*.md, and Seat C 19th's
STATUS / QUESTION mails as mail_seatC19_*.md (its twelve READYs are captured in the gate19C dir — NOT duplicated here). Then (re)build the combined
capture mail_gate19B_ready.md = the nine READY captures in push order, then the seat's STATUS mails, then its QUESTION / wrap mails. Key by NAME from
the WEDNESDAY .env; never printed. Datasec/Tuesday mails are never fetched (the filter is on the from-address AND the subject). Writes only into this
gateset dir. Derived from gatesets/2026-09-22_gate19C_seatC/capture_ready_mail_gate19C.py (itself from gate18C's / gate16B's / gate15's). Only mails
timestamped at/after the 19th briefs (2026-09-22T04:03Z) are considered."""
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
print('listed', len(msgs), 'oldest', min((m.get('timestamp') or '') for m in msgs))
WINDOW_START = '2026-09-22T04:03'   # the 19th briefs went 04:03:07Z (B) / 04:03:27Z (C)
SUBJ_B19 = '[Secuura/Blockchain-B -> Wednesday] READY FOR QA (Seat B 19th): PR '
SUBJ_B20 = '[Secuura/Blockchain-B -> Wednesday] READY FOR QA (Seat B 20th): PR '
WED_C = '[Wednesday -> Secuura/Blockchain-C] '
WED_B = '[Wednesday -> Secuura/Blockchain-B] '
PUSH = [str(i) for i in range(1, 10)]
ORDER = {p: '%02d' % int(p) for p in PUSH}
def is_seat(m): return 'secuura-blockchain@' in str(m.get('from'))
def is_wed(m): return 'wednesday-agent@' in str(m.get('from'))
def sub(m): return m.get('subject') or ''
def in_window(m): return str(m.get('timestamp') or '') >= WINDOW_START
def s_ok(s): return s.startswith('[Secuura/Blockchain-B ->') or s.startswith('[Secuura/Blockchain-C ->')
def w_ok(s): return s.startswith(WED_B) or (s.startswith(WED_C) and 'ADDENDUM' in s)
hits = [m for m in msgs if in_window(m) and ((is_seat(m) and s_ok(sub(m))) or (is_wed(m) and w_ok(sub(m))))]
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
    m19 = re.match(re.escape(SUBJ_B19) + r'(\d+) (KS-\d+)', s); m20 = re.match(re.escape(SUBJ_B20) + r'(\d+) (KS-\d+)', s)
    if (m19 or m20) and is_seat(m):
        n, tk = (m19 or m20).groups(); k = ORDER.get(n); seat = 'B19' if m19 else 'B20'
        if k is None: print('  UNKNOWN seat PR number', n, '- skipped'); continue
        if (m19 and int(n) > 3) or (m20 and int(n) < 4): print('  TAG/NUMBER MISMATCH', seat, n, '- captured under its subject tag'); 
        name = 'mail_seat%s_ready%s_pr%s_%s.md' % (seat, k, n, tk.lower().replace('-', ''))
        if 'CORRECTION' in s.upper():
            k = k + 'C_' + hhmm; name = 'mail_seat%s_ready%s_pr%s_%s_CORRECTION_%s.md' % (seat, ORDER[n], n, tk.lower().replace('-', ''), hhmm)
    elif is_seat(m) and s.startswith('[Secuura/Blockchain-B -> Wednesday] STATUS'):
        seat = 'B20' if '20th' in s else 'B19'; k = 'S_' + hhmm; name = 'mail_seat%s_status_%s.md' % (seat, hhmm)
    elif is_seat(m) and s.startswith('[Secuura/Blockchain-B -> Wednesday]') and 'QUESTION' in s:
        seat = 'B20' if '20th' in s else 'B19'; k = 'Q_' + hhmm; name = 'mail_seat%s_question_%s_%s.md' % (seat, slug(s)[:40], hhmm)
    elif is_seat(m) and s.startswith('[Secuura/Blockchain-B -> Wednesday]'):
        seat = 'B20' if '20th' in s else 'B19'; k = 'O_' + hhmm; name = 'mail_seat%s_other_%s_%s.md' % (seat, slug(s)[:40], hhmm)
    elif is_seat(m) and s.startswith('[Secuura/Blockchain-C -> Wednesday] READY FOR QA'):
        print('  Seat C READY - captured in the gate19C dir, skipped here'); continue
    elif is_seat(m) and s.startswith('[Secuura/Blockchain-C -> Wednesday]'):
        k = 'CO_' + hhmm; name = 'mail_seatC19_%s_%s.md' % (slug(s)[:40], hhmm)
    elif is_wed(m) and s.startswith(WED_C):
        k = 'WC_' + hhmm; name = 'mail_wedC_%s_%s.md' % (slug(s)[:40], hhmm)
    else:
        k = 'W_' + hhmm; name = 'mail_wed_%s_%s.md' % (slug(s)[:40], hhmm)
    out = os.path.join(G, name)
    if os.path.exists(out):
        print('  exists, not overwritten:', name)
    else:
        full = get(base + '/' + urllib.parse.quote(m['message_id'], safe=''))
        txt = full.get('text') or ''
        with open(out, 'w', encoding='utf-8') as f:
            f.write('SUBJECT: ' + s + '\nFROM: ' + str(m.get('from')) + '\nTO: ' + str(full.get('to')) + '\nTS: ' + ts
                    + '\nMESSAGE_ID: ' + m['message_id'] + '\nCAPTURED: ' + cap + ' by the gate19B (Seat B 19th/20th nine-PR) drafter, read-only by message id from wednesday-agent@ (key by name, never printed)'
                    + '\nTEXT_SHA256: ' + hashlib.sha256(txt.encode()).hexdigest() + '\n' + txt + '\n')
        print('  written', name, len(txt), 'chars')
    files[k] = out
comb = os.path.join(G, 'mail_gate19B_ready.md')
with open(comb, 'w', encoding='utf-8') as f:
    f.write('COMBINED CAPTURE (rebuilt ' + cap + ') of the Seat B 19th/20th READY FOR QA mails in PR push order (seat PRs 1..9 = #1182 #1184 #1186 #1194 #1196 #1198 #1199 #1200 #1201; READY 1-3 by Seat B 19th, READY 4-9 by Seat B 20th after the mid-series hand-over), then the seat STATUS mails (05:24Z NINE RAISED; 07:09Z (2\') applied; 07:55Z HOLDING 9/9), then the seat QUESTION / wrap mails (04:09Z S1; 04:27Z plan 19th; 05:07Z KS-1164; 06:18Z the 19th\'s wrap/handover; 07:04Z plan 20th); each section is the verbatim per-mail capture file named in its header. Wednesday brief / ANSWER / ADDENDUM mails (mail_wed_*.md, mail_wedC_*.md) and Seat C 19th STATUS/QUESTION mails (mail_seatC19_*.md) are captured beside this file and are NOT part of this combined seat-B capture.\n')
    for p in PUSH:
        k = ORDER[p]
        if k in files:
            f.write('\n\n' + '#' * 8 + ' ' + os.path.basename(files[k]) + ' ' + '#' * 8 + '\n')
            f.write(open(files[k], encoding='utf-8').read())
            for kc in sorted(x for x in files if x.startswith(k + 'C_')):
                f.write('\n\n' + '#' * 8 + ' ' + os.path.basename(files[kc]) + ' (the seat\'s CORRECTION to the READY above) ' + '#' * 8 + '\n')
                f.write(open(files[kc], encoding='utf-8').read())
        else:
            f.write('\n\n' + '#' * 8 + ' section ' + k + ' (seat PR ' + p + '): NOT YET ARRIVED at ' + cap + ' ' + '#' * 8 + '\n')
    for k in sorted(x for x in files if x.startswith('S_')) + sorted(x for x in files if x.startswith('Q_')) + sorted(x for x in files if x.startswith('O_')):
        f.write('\n\n' + '#' * 8 + ' ' + os.path.basename(files[k]) + ' ' + '#' * 8 + '\n')
        f.write(open(files[k], encoding='utf-8').read())
print('combined', comb, 'sections', sorted(files))
