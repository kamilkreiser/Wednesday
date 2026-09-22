#!/usr/bin/env python3
"""capture_ready_mail_gate18C.py — read-only: capture every "[Secuura/Blockchain-C -> Wednesday] READY FOR QA (Seat C 18th): PR <N> ..." mail verbatim
(by message id) from wednesday-agent@ into mail_seatC18_ready<k>_pr<N>_<ticket>.md (k = the seat's push order 1..6 -> 01..06; seat PR 4 carries
BOTH KS-1231 READY rows (Part A + Part B) in ONE mail — six mails, seven READY rows), never overwritten; plus EVERY Seat C 18th STATUS / QUESTION /
ACK mail from the seat (the 22:55Z "#1036 MERGED" STATUS and the 23:26Z "six RAISED + COMMITTED" STATUS) and EVERY Wednesday mail to
Secuura/Blockchain-C in the 18th window (the brief, the plan ANSWER, the `GO: merge #1036`, the KS-1257 tail ANSWER) (subject slug + HHMM); AND, as
CONTEXT for by-name item 3 (the zero overlap with Seat B 18th's paths) and item 9 (the two-seat artefacts), every Seat B 18th READY / STATUS /
QUESTION / ACK mail and Wednesday's mails to Secuura/Blockchain-B naming "Seat B 18th" or answering it (mail_seatB18_*.md / mail_wedB_*.md) —
captured beside, NOT part of the combined seat-C capture. Then (re)build the combined capture mail_gate18C_ready.md = the six READY captures in
push order, then the seat's STATUS mail(s), then its QUESTION / ACK mail(s). Key by NAME from the WEDNESDAY .env; never printed. Datasec/Tuesday
mails are never fetched (the filter is on the from-address AND the subject). Writes only into this gateset dir. Derived from
gatesets/2026-09-22_gate16C_seatC/capture_ready_mail_gate16C.py (itself from gate16B's / gate15's). Only mails timestamped at/after the 18th
brief (2026-09-21T22:27Z) are considered — the 16th's mails on the same subjects-shape are NOT re-captured here."""
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
SUBJ_C = '[Secuura/Blockchain-C -> Wednesday] READY FOR QA (Seat C 18th): PR '
SUBJ_B = '[Secuura/Blockchain-B -> Wednesday] READY FOR QA (Seat B 18th): PR '
WED_C = '[Wednesday -> Secuura/Blockchain-C] '
WED_B = '[Wednesday -> Secuura/Blockchain-B] '
PUSH = ['1', '2', '3', '4', '5', '6']
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
    mc = re.match(re.escape(SUBJ_C) + r'(\d+) (KS-\d+)', s); mb = re.match(re.escape(SUBJ_B) + r'(\d+) (KS-\d+)', s)
    if mc and is_seat(m):
        n, tk = mc.groups(); k = ORDER.get(n)
        if k is None: print('  UNKNOWN seat PR number', n, '- skipped'); continue
        name = 'mail_seatC18_ready%s_pr%s_%s.md' % (k, n, tk.lower().replace('-', ''))
        if 'CORRECTION' in s.upper():
            k = k + 'C_' + hhmm; name = 'mail_seatC18_ready%s_pr%s_%s_CORRECTION_%s.md' % (ORDER[n], n, tk.lower().replace('-', ''), hhmm)
    elif mb and is_seat(m):
        n, tk = mb.groups(); k = 'B_' + n.zfill(2) + '_' + hhmm; name = 'mail_seatB18_ready%s_pr%s_%s.md' % (n.zfill(2), n, tk.lower().replace('-', ''))
    elif is_seat(m) and s.startswith('[Secuura/Blockchain-C -> Wednesday] STATUS'):
        k = 'S_' + hhmm; name = 'mail_seatC18_status_%s.md' % hhmm   # the -C prefix tested BEFORE any Seat-B branch (gate16C drafter S1)
    elif is_seat(m) and s.startswith('[Secuura/Blockchain-C -> Wednesday]') and 'QUESTION' in s:
        k = 'Q_' + hhmm; name = 'mail_seatC18_question_%s_%s.md' % (slug(s)[:40], hhmm)
    elif is_seat(m) and s.startswith('[Secuura/Blockchain-C -> Wednesday]'):
        k = 'O_' + hhmm; name = 'mail_seatC18_other_%s_%s.md' % (slug(s)[:40], hhmm)
    elif is_seat(m) and s.startswith('[Secuura/Blockchain-B -> Wednesday]'):
        k = 'BO_' + hhmm; name = 'mail_seatB18_%s_%s.md' % (slug(s)[:40], hhmm)
    elif is_wed(m) and s.startswith(WED_B):
        k = 'WB_' + hhmm; name = 'mail_wedB_%s_%s.md' % (slug(s)[:40], hhmm)
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
                    + '\nMESSAGE_ID: ' + m['message_id'] + '\nCAPTURED: ' + cap + ' by the gate18C (Seat C 18th six-PR) drafter, read-only by message id from wednesday-agent@ (key by name, never printed)'
                    + '\nTEXT_SHA256: ' + hashlib.sha256(txt.encode()).hexdigest() + '\n' + txt + '\n')
        print('  written', name, len(txt), 'chars')
    files[k] = out
comb = os.path.join(G, 'mail_gate18C_ready.md')
with open(comb, 'w', encoding='utf-8') as f:
    f.write('COMBINED CAPTURE (rebuilt ' + cap + ') of the Seat C 18th READY FOR QA mails in PR push order (seat PRs 1 2 3 4 5 6 = #1167 #1168 #1169 #1171 #1173 #1175; seat PR 4 carries BOTH KS-1231 READY rows, Part A + Part B — six mails, seven READY rows), then the seat\'s STATUS mail(s) (22:55Z #1036 MERGED; 23:26Z six RAISED + COMMITTED), then the seat\'s QUESTION / ACK / other mail(s) (22:43Z plan confirmation; 22:46Z KS-1257 branch tail); each section is the verbatim per-mail capture file named in its header. Wednesday\'s brief / ANSWER / GO mails (mail_wed_*.md) and Seat B 18th\'s mails (mail_seatB18_*.md, mail_wedB_*.md) are captured beside this file and are NOT part of this combined seat-C capture.\n')
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
