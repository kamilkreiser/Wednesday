#!/usr/bin/env python3
"""capture_ready_mail_gate18B.py — read-only: capture every "[Secuura/Blockchain-B -> Wednesday] READY FOR QA (Seat B 18th): PR <N> ..." mail verbatim
(by message id) from wednesday-agent@ into mail_seatB18_ready<k>_pr<N>_<ticket>.md (k = the seat's push order 1..7 -> 01..07; seat PR 4 carries
BOTH KS-1171 READY rows (8J-TSFIX + GUARD3S-TSFIX) in ONE mail — seven mails, eight READY rows), never overwritten; plus EVERY Seat B 18th STATUS /
QUESTION / ACK mail from the seat (the 23:47Z "SEVEN RAISED + COMMITTED" STATUS and the 01:08:36Z HOLDING STATUS — the HOLD) and EVERY Wednesday
mail to Secuura/Blockchain-B in the 18th window (the brief, the plan ANSWER, the baselines (b) ANSWER) (subject slug + HHMM); AND, as CONTEXT for
by-name item 3 (the zero overlap with Seat C 18th's paths) and item 9 (the two-seat artefacts), every Seat C 18th READY / STATUS / QUESTION mail
and Wednesday's mails to Secuura/Blockchain-C (mail_seatC18_*.md / mail_wedC_*.md) — captured beside, NOT part of the combined seat-B capture.
Then (re)build the combined capture mail_gate18B_ready.md = the seven READY captures in push order, then the seat's STATUS mail(s), then its
QUESTION / ACK mail(s). Key by NAME from the WEDNESDAY .env; never printed. Datasec/Tuesday mails are never fetched (the filter is on the
from-address AND the subject). Writes only into this gateset dir. Derived from gatesets/2026-09-22_gate18C_seatC/capture_ready_mail_gate18C.py
(itself from gate16C's / gate16B's / gate15's) with the B/C roles swapped. Only mails timestamped at/after the 18th briefs (2026-09-21T22:27Z)
are considered — the 16th's / 17th's mails on the same subject shape are NOT re-captured here."""
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
WINDOW_START = '2026-09-21T22:27'   # the 18th briefs went 22:27:53Z (B) / 22:28:06Z (C)
SUBJ_B = '[Secuura/Blockchain-B -> Wednesday] READY FOR QA (Seat B 18th): PR '
SUBJ_C = '[Secuura/Blockchain-C -> Wednesday] READY FOR QA (Seat C 18th): PR '
WED_B = '[Wednesday -> Secuura/Blockchain-B] '
WED_C = '[Wednesday -> Secuura/Blockchain-C] '
PUSH = ['1', '2', '3', '4', '5', '6', '7']
ORDER = {p: '%02d' % int(p) for p in PUSH}
def is_seat(m): return 'secuura-blockchain@' in str(m.get('from'))
def is_wed(m): return 'wednesday-agent@' in str(m.get('from'))
def sub(m): return m.get('subject') or ''
def in_window(m): return str(m.get('timestamp') or '') >= WINDOW_START
def s_ok(s): return s.startswith('[Secuura/Blockchain-B ->') or s.startswith('[Secuura/Blockchain-C ->')
def w_ok(s): return s.startswith(WED_B) or s.startswith(WED_C)
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
    mb = re.match(re.escape(SUBJ_B) + r'(\d+) (KS-\d+)', s); mc = re.match(re.escape(SUBJ_C) + r'(\d+) (KS-\d+)', s)
    if mb and is_seat(m):
        n, tk = mb.groups(); k = ORDER.get(n)
        if k is None: print('  UNKNOWN seat PR number', n, '- skipped'); continue
        name = 'mail_seatB18_ready%s_pr%s_%s.md' % (k, n, tk.lower().replace('-', ''))
        if 'CORRECTION' in s.upper():
            k = k + 'C_' + hhmm; name = 'mail_seatB18_ready%s_pr%s_%s_CORRECTION_%s.md' % (ORDER[n], n, tk.lower().replace('-', ''), hhmm)
    elif mc and is_seat(m):
        n, tk = mc.groups(); k = 'C_' + n.zfill(2) + '_' + hhmm; name = 'mail_seatC18_ready%s_pr%s_%s.md' % (n.zfill(2), n, tk.lower().replace('-', ''))
    elif is_seat(m) and s.startswith('[Secuura/Blockchain-B -> Wednesday] STATUS'):
        k = 'S_' + hhmm; name = 'mail_seatB18_status_%s.md' % hhmm   # the -B prefix tested BEFORE any Seat-C branch (gate16C drafter S1)
    elif is_seat(m) and s.startswith('[Secuura/Blockchain-B -> Wednesday]') and 'QUESTION' in s:
        k = 'Q_' + hhmm; name = 'mail_seatB18_question_%s_%s.md' % (slug(s)[:40], hhmm)
    elif is_seat(m) and s.startswith('[Secuura/Blockchain-B -> Wednesday]'):
        k = 'O_' + hhmm; name = 'mail_seatB18_other_%s_%s.md' % (slug(s)[:40], hhmm)
    elif is_seat(m) and s.startswith('[Secuura/Blockchain-C -> Wednesday]'):
        k = 'CO_' + hhmm; name = 'mail_seatC18_%s_%s.md' % (slug(s)[:40], hhmm)
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
                    + '\nMESSAGE_ID: ' + m['message_id'] + '\nCAPTURED: ' + cap + ' by the gate18B (Seat B 18th seven-PR) drafter, read-only by message id from wednesday-agent@ (key by name, never printed)'
                    + '\nTEXT_SHA256: ' + hashlib.sha256(txt.encode()).hexdigest() + '\n' + txt + '\n')
        print('  written', name, len(txt), 'chars')
    files[k] = out
comb = os.path.join(G, 'mail_gate18B_ready.md')
with open(comb, 'w', encoding='utf-8') as f:
    f.write('COMBINED CAPTURE (rebuilt ' + cap + ') of the Seat B 18th READY FOR QA mails in PR push order (seat PRs 1 2 3 4 5 6 7 = #1170 #1172 #1174 #1176 #1177 #1178 #1179; seat PR 4 carries BOTH KS-1171 READY rows, 8J-TSFIX + GUARD3S-TSFIX — seven mails, eight READY rows), then the seat\'s STATUS mail(s) (23:47Z SEVEN RAISED + COMMITTED; 01:08Z HOLDING — the HOLD), then the seat\'s QUESTION / ACK / other mail(s) (22:50Z plan confirmation; 23:29Z auth + shared baselines). Each section is the verbatim per-mail capture file named in its header. Wednesday\'s brief / ANSWER mails (mail_wed_*.md) and Seat C 18th\'s mails (mail_seatC18_*.md, mail_wedC_*.md) are captured beside this file and are NOT part of this combined seat-B capture.\n')
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
