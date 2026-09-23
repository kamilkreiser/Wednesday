#!/usr/bin/env python3
"""capture_ready_mail_gate20T1.py — read-only: capture the round-20 TIER-1 READY FOR QA mails verbatim (by message id) from wednesday-agent@ —
Seat B 21st's PR 3 (KS-851, #1204), PR 6 (KS-1287, #1208), PR 7 (KS-1245, #1207) and Seat B 22nd's PR 8 (KS-1033, #1209), PR 9 (KS-1239, #1210),
PR 10 (KS-1084, #1211) — into mail_seatB2x_ready<k>_pr<k>_<ticket>.md (never overwritten); plus EVERY Seat B 21st / 22nd STATUS / QUESTION / wrap
mail, EVERY Wednesday mail to Secuura/Blockchain-B in the round-20 window (the 04:52Z brief, the ANSWERs incl. 06:52Z ruling (a) on PR 6's YAML and
07:52Z ruling (a) on PR 10's raise-engine stop, the 07:15Z Seat B 22nd successor brief, the 07:36Z tier-2 GO) as mail_wed_*.md, and the tier-2 QA
verdict (coagent@ 07:35Z, the `[QA -> Wednesday] TIER-2 BATCH GATE #1202-#1206` subject) as mail_qa_*.md. The TIER-2 READYs (seat PRs 1, 2, 4, 5)
are the tier-2 gate's (already gated) and are SKIPPED here (subject printed only). Then (re)build the combined capture mail_gate20T1_ready.md = the six
tier-1 READYs in seat order (3, 6, 7, 8, 9, 10; a `NOT YET ARRIVED` section for any READY not in the inbox), then the seats' STATUS mails, then their
QUESTION / wrap mails. Key by NAME from the WEDNESDAY .env; never printed. Never marks anything seen (a direct API GET). Filter: the from-address
(secuura-blockchain@ / wednesday-agent@ / coagent@) AND the Blockchain-B / QA-batch subject prefixes — no other client's mail is fetched or printed.
Writes only into this gateset dir. The gate20T2 capture script re-keyed. Only mails at/after the round-20 brief (2026-09-23T04:52Z) are considered.
Idempotent."""
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
WINDOW_START = '2026-09-23T04:52'
SUBJ_R = re.compile(r'^\[Secuura/Blockchain-B -> Wednesday\] READY FOR QA \(Seat B (21st|22nd)\): PR (\d+) (KS-\d+)')
WED_B = '[Wednesday -> Secuura/Blockchain-B] '
QA_T2 = '[QA -> Wednesday] TIER-2 BATCH GATE #1202-#1206'
TIER1 = ['3', '6', '7', '8', '9', '10', '11']   # PR 11 (KS-1143) by Wednesday's AMENDMENT 18:1x
ORDER = {p: '%02d' % int(p) for p in TIER1}
SEATTAG = {'21st': 'B21', '22nd': 'B22'}
def is_seat(m): return 'secuura-blockchain@' in str(m.get('from'))
def is_wed(m): return 'wednesday-agent@' in str(m.get('from'))
def is_qa(m): return 'coagent@' in str(m.get('from'))
def sub(m): return m.get('subject') or ''
def in_window(m): return str(m.get('timestamp') or '') >= WINDOW_START
hits = [m for m in msgs if in_window(m) and ((is_seat(m) and sub(m).startswith('[Secuura/Blockchain-B ->')) or (is_wed(m) and sub(m).startswith(WED_B)) or (is_qa(m) and sub(m).startswith(QA_T2)))]
if len(msgs) >= 200 and min((m.get('timestamp') or '') for m in msgs) >= WINDOW_START: print('WARNING: the listing may be TRUNCATED before the window start — paginate'); sys.exit(2)
cap = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
files = {}
def slug(s):
    s = s.split('] ', 1)[1] if '] ' in s else s
    s = re.sub(r'[^A-Za-z0-9]+', '_', s).strip('_').lower()
    return s[:60]
def seat_of(s):
    m = re.search(r'\(Seat B (21st|22nd)\)', s) or re.search(r'Seat B (21st|22nd)', s)
    return SEATTAG[m.group(1)] if m else 'Bxx'
for m in sorted(hits, key=lambda x: x.get('timestamp') or ''):
    s = sub(m); ts = str(m.get('timestamp') or '')
    hhmm = re.sub(r'[^0-9]', '', ts[11:16]) or '0000'
    print(ts, '|', m.get('from'), '|', s, '|', m.get('message_id'))
    mr = SUBJ_R.match(s)
    if mr and is_seat(m):
        seat, n, tk = mr.groups()
        if n not in TIER1: print('  tier-2 READY (seat PR %s) - the tier-2 gate\'s, skipped here' % n); continue
        k = ORDER[n]; name = 'mail_seat%s_ready%s_pr%s_%s.md' % (SEATTAG[seat], k, n, tk.lower().replace('-', ''))
        if 'CORRECTION' in s.upper():
            k = k + 'C_' + hhmm; name = 'mail_seat%s_ready%s_pr%s_%s_CORRECTION_%s.md' % (SEATTAG[seat], ORDER[n], n, tk.lower().replace('-', ''), hhmm)
    elif is_seat(m) and s.startswith('[Secuura/Blockchain-B -> Wednesday] STATUS'):
        k = 'S_' + hhmm; name = 'mail_seat%s_status_%s.md' % (seat_of(s), hhmm)
    elif is_seat(m) and 'QUESTION' in s:
        k = 'Q_' + hhmm; name = 'mail_seat%s_question_%s_%s.md' % (seat_of(s), slug(s)[:40], hhmm)
    elif is_seat(m):
        k = 'O_' + hhmm; name = 'mail_seat%s_other_%s_%s.md' % (seat_of(s), slug(s)[:40], hhmm)
    elif is_qa(m):
        k = 'A_' + hhmm; name = 'mail_qa_t2_verdict_%s.md' % hhmm
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
                    + '\nMESSAGE_ID: ' + m['message_id'] + '\nCAPTURED: ' + cap + ' by the gate20T1 (round-20 tier-1) drafter, read-only by message id from wednesday-agent@ (key by name, never printed)'
                    + '\nTEXT_SHA256: ' + hashlib.sha256(txt.encode()).hexdigest() + '\n' + txt + '\n')
        print('  written', name, len(txt), 'chars')
    files[k] = out
comb = os.path.join(G, 'mail_gate20T1_ready.md')
with open(comb, 'w', encoding='utf-8') as f:
    f.write('COMBINED CAPTURE (rebuilt ' + cap + ') of the round-20 TIER-1 READY FOR QA mails in seat order (seat PRs 3, 6, 7 = Seat B 21st #1204 KS-851, #1208 KS-1287, #1207 KS-1245; seat PRs 8, 9, 10 = Seat B 22nd #1209 KS-1033, #1210 KS-1239, #1211 KS-1084), then the seats\' STATUS mails, then their QUESTION / wrap mails; each section is the verbatim per-mail capture file named in its header. Seat PRs 1, 2, 4, 5 are the TIER-2 gate\'s (gated 07:35Z, GO 07:36Z) and are not captured here. Wednesday\'s brief / ANSWER / GO mails (mail_wed_*.md) and the tier-2 QA verdict (mail_qa_t2_verdict_*.md) are captured beside this file and are NOT part of this combined seat capture.\n')
    for p in TIER1:
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
missing = [p for p in TIER1 if ORDER[p] not in files]
print('combined', comb, 'sections', sorted(files), '| tier-1 READYs present', [p for p in TIER1 if ORDER[p] in files], '| NOT YET ARRIVED', missing or 'NONE')
sys.exit(0)   # a missing READY 11 is PENDING, not an error — round20T1.py's self-check decides (PR11_PENDING)
