#!/usr/bin/env python3
"""capture_ready_mail_gate16C.py — read-only: capture every "[Secuura/Blockchain-C -> Wednesday] READY FOR QA (Seat C 16th): PR <N> ..." mail verbatim
(by message id) from wednesday-agent@ into mail_seatC16_ready<k>_pr<N>_<ticket>.md (k = the seat's push order: seat PRs 1, 3..13 -> 01, 03..13;
seat PR 2 KS-1123 F3b was HELD un-pushed by Wednesday's 16:53:40Z ruling (TS18046) and has no READY — its slot is recorded as HELD), never
overwritten; plus EVERY Seat C 16th STATUS / QUESTION / ACK mail from the seat (incl. the 19:12:28Z HOLDING STATUS) and EVERY Wednesday ANSWER /
ADDENDUM / SUCCESSOR mail to Secuura/Blockchain-C naming "Seat C 16th" (subject slug + HHMM); AND, as CONTEXT for by-name item 3 (the zero overlap
with Seat B 16th's eight paths) and item 9 (the two-seat artefacts), every Seat B 16th READY / STATUS / QUESTION / ACK mail and Wednesday's mails to
Secuura/Blockchain-B naming "Seat B 16th" (mail_seatB16_*.md / mail_wedB_*.md) — captured beside, NOT part of the combined seat-C capture.
Then (re)build the combined capture mail_gate16C_ready.md = the twelve READY captures in push order, then the seat's STATUS mail(s), then its
QUESTION / ACK mail(s). Key by NAME from the WEDNESDAY .env; never printed. Datasec/Tuesday mails are never fetched (the filter is on the
from-address AND the subject). Writes only into this gateset dir. Derived from gatesets/2026-09-22_gate16B_seatB/capture_ready_mail_gate16B.py
(itself from gate15's)."""
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
SUBJ_C = '[Secuura/Blockchain-C -> Wednesday] READY FOR QA (Seat C 16th): PR '
SUBJ_B = '[Secuura/Blockchain-B -> Wednesday] READY FOR QA (Seat B 16th): PR '
WED_C = '[Wednesday -> Secuura/Blockchain-C] '
WED_B = '[Wednesday -> Secuura/Blockchain-B] '
PUSH = ['1', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13']   # seat PR 2 (KS-1123 F3b) HELD — no READY
ORDER = {p: '%02d' % int(p) for p in PUSH}
def is_seat(m): return 'secuura-blockchain@' in str(m.get('from'))
def is_wed(m): return 'wednesday-agent@' in str(m.get('from'))
def sub(m): return m.get('subject') or ''
def b16(s): return 'Seat B 16th' in s
def c16(s): return 'Seat C 16th' in s
def s_ok(s): return s.startswith('[Secuura/Blockchain') and (b16(s) or c16(s))
def w_ok(s): return (s.startswith(WED_B) and b16(s)) or (s.startswith(WED_C) and c16(s))
hits = [m for m in msgs if (is_seat(m) and s_ok(sub(m))) or (is_wed(m) and w_ok(sub(m)))]
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
        if k is None: print('  UNKNOWN / HELD seat PR number', n, '- skipped'); continue
        name = 'mail_seatC16_ready%s_pr%s_%s.md' % (k, n, tk.lower().replace('-', ''))
        if 'CORRECTION' in s.upper():
            k = k + 'C_' + hhmm; name = 'mail_seatC16_ready%s_pr%s_%s_CORRECTION_%s.md' % (ORDER[n], n, tk.lower().replace('-', ''), hhmm)
    elif mb and is_seat(m):
        n, tk = mb.groups(); k = 'B_' + n.zfill(2) + '_' + hhmm; name = 'mail_seatB16_ready%s_pr%s_%s.md' % (n.zfill(2), n, tk.lower().replace('-', ''))
    elif is_seat(m) and s.startswith('[Secuura/Blockchain-C -> Wednesday] STATUS'):
        k = 'S_' + hhmm; name = 'mail_seatC16_status_%s.md' % hhmm   # tested BEFORE the Seat-B branch: the 16:56Z S3 STATUS names "Seat B 16th" in its subject (drafter S1)
    elif is_seat(m) and s.startswith('[Secuura/Blockchain-C -> Wednesday]') and 'QUESTION' in s:
        k = 'Q_' + hhmm; name = 'mail_seatC16_question_%s_%s.md' % (slug(s)[:40], hhmm)
    elif is_seat(m) and s.startswith('[Secuura/Blockchain-C -> Wednesday]'):
        k = 'O_' + hhmm; name = 'mail_seatC16_other_%s_%s.md' % (slug(s)[:40], hhmm)
    elif is_seat(m) and b16(s):
        k = 'BO_' + hhmm; name = 'mail_seatB16_%s_%s.md' % (slug(s)[:40], hhmm)
    elif is_seat(m):
        k = 'O_' + hhmm; name = 'mail_seatC16_other_%s_%s.md' % (slug(s)[:40], hhmm)
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
                    + '\nMESSAGE_ID: ' + m['message_id'] + '\nCAPTURED: ' + cap + ' by the gate16C (Seat C 16th twelve-PR) drafter, read-only by message id from wednesday-agent@ (key by name, never printed)'
                    + '\nTEXT_SHA256: ' + hashlib.sha256(txt.encode()).hexdigest() + '\n' + txt + '\n')
        print('  written', name, len(txt), 'chars')
    files[k] = out
comb = os.path.join(G, 'mail_gate16C_ready.md')
with open(comb, 'w', encoding='utf-8') as f:
    f.write('COMBINED CAPTURE (rebuilt ' + cap + ') of the Seat C 16th READY FOR QA mails in PR push order (seat PRs 1 3 4 5 6 7 8 9 10 11 12 13 = #1148 #1150 #1152 #1154 #1156 #1158 #1160 #1162 #1163 #1164 #1165 #1166; seat PR 2 KS-1123 F3b HELD un-pushed by Wednesday 16:53:40Z — no READY, not in this gate), then the seat\'s STATUS mail(s) (16:46Z raises 10/13; 16:51Z phase 2 green; 16:56Z S3 cross-seat; 19:12Z HOLDING), then the seat\'s QUESTION / ACK / other mail(s); each section is the verbatim per-mail capture file named in its header. Wednesday\'s ANSWER / ADDENDUM / SUCCESSOR mails (mail_wed_*.md) and Seat B 16th\'s mails (mail_seatB16_*.md, mail_wedB_*.md) are captured beside this file and are NOT part of this combined seat-C capture.\n')
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
    f.write('\n\n' + '#' * 8 + ' section 02 (seat PR 2, KS-1123 F3b): HELD un-pushed by Wednesday\'s 16:53:40Z ruling (TS18046 delta +1) — NO READY, NOT in this gate ' + '#' * 8 + '\n')
    for k in sorted(x for x in files if x.startswith('S_')) + sorted(x for x in files if x.startswith('Q_')) + sorted(x for x in files if x.startswith('O_')):
        f.write('\n\n' + '#' * 8 + ' ' + os.path.basename(files[k]) + ' ' + '#' * 8 + '\n')
        f.write(open(files[k], encoding='utf-8').read())
print('combined', comb, 'sections', sorted(files))
