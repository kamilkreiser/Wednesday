#!/usr/bin/env python3
"""capture_ready_mail_gate20T2.py — read-only: capture Seat B 21st's TIER-2 READY FOR QA mails (seat PRs 1, 2, 4, 5 — KS-965, KS-1019, KS-1081,
KS-1139) verbatim (by message id) from wednesday-agent@ into mail_seatB21_ready0<k>_pr<k>_<ticket>.md — never overwritten; plus EVERY Seat B 21st
STATUS / QUESTION / wrap mail (mail_seatB21_*.md) and EVERY Wednesday mail to Secuura/Blockchain-B in the round-20 window (the brief 04:52Z, the plan
ANSWER 05:12Z, the rhythm ANSWERs 05:41Z / 05:58Z) as mail_wed_*.md. The TIER-1 READYs (seat PRs 3, 6-10: KS-851 re-graded to tier 1 by Wednesday's
05:12:13Z ANSWER, KS-1287, KS-1245, KS-1033, KS-1239, KS-1084) are the tier-1 gate's and are SKIPPED here (subject printed only). Then (re)build the
combined capture mail_gate20T2_ready.md = the four tier-2 READYs in push order (a section `NOT YET ARRIVED` for any READY not in the inbox — READY 5 at
the drafter's first run), then the seat's STATUS mails, then its QUESTION / wrap mails. Key by NAME from the WEDNESDAY .env; never printed. Never marks
anything seen (a direct API GET; the digest's seen-state file is not touched). Filter: the from-address (secuura-blockchain@ / wednesday-agent@) AND the
Blockchain-B subject prefixes — no other client's mail is fetched or printed. Writes only into this gateset dir. Derived from
gatesets/2026-09-22_gate19B_seatB/capture_ready_mail_gate19B.py. Only mails timestamped at/after the round-20 brief (2026-09-23T04:52Z) are considered.
Idempotent: re-run it when READY 5 lands (take_pr5_gate20T2.sh does)."""
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
WINDOW_START = '2026-09-23T04:52'   # the round-20 brief to Seat B 21st went 04:52Z
SUBJ_R = '[Secuura/Blockchain-B -> Wednesday] READY FOR QA (Seat B 21st): PR '
WED_B = '[Wednesday -> Secuura/Blockchain-B] '
TIER2 = ['1', '2', '4', '5']
ORDER = {p: '%02d' % int(p) for p in TIER2}
def is_seat(m): return 'secuura-blockchain@' in str(m.get('from'))
def is_wed(m): return 'wednesday-agent@' in str(m.get('from'))
def sub(m): return m.get('subject') or ''
def in_window(m): return str(m.get('timestamp') or '') >= WINDOW_START
hits = [m for m in msgs if in_window(m) and ((is_seat(m) and sub(m).startswith('[Secuura/Blockchain-B ->')) or (is_wed(m) and sub(m).startswith(WED_B)))]
if len(msgs) >= 200 and min((m.get('timestamp') or '') for m in msgs) >= WINDOW_START: print('WARNING: the listing may be TRUNCATED before the window start — paginate'); sys.exit(2)
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
    mr = re.match(re.escape(SUBJ_R) + r'(\d+) (KS-\d+)', s)
    if mr and is_seat(m):
        n, tk = mr.groups()
        if n not in TIER2: print('  tier-1 READY (seat PR %s) - the tier-1 gate\'s, skipped here' % n); continue
        k = ORDER[n]; name = 'mail_seatB21_ready%s_pr%s_%s.md' % (k, n, tk.lower().replace('-', ''))
        if 'CORRECTION' in s.upper():
            k = k + 'C_' + hhmm; name = 'mail_seatB21_ready%s_pr%s_%s_CORRECTION_%s.md' % (ORDER[n], n, tk.lower().replace('-', ''), hhmm)
    elif is_seat(m) and s.startswith('[Secuura/Blockchain-B -> Wednesday] STATUS'):
        k = 'S_' + hhmm; name = 'mail_seatB21_status_%s.md' % hhmm
    elif is_seat(m) and 'QUESTION' in s:
        k = 'Q_' + hhmm; name = 'mail_seatB21_question_%s_%s.md' % (slug(s)[:40], hhmm)
    elif is_seat(m):
        k = 'O_' + hhmm; name = 'mail_seatB21_other_%s_%s.md' % (slug(s)[:40], hhmm)
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
                    + '\nMESSAGE_ID: ' + m['message_id'] + '\nCAPTURED: ' + cap + ' by the gate20T2 (Seat B 21st tier-2) drafter, read-only by message id from wednesday-agent@ (key by name, never printed)'
                    + '\nTEXT_SHA256: ' + hashlib.sha256(txt.encode()).hexdigest() + '\n' + txt + '\n')
        print('  written', name, len(txt), 'chars')
    files[k] = out
comb = os.path.join(G, 'mail_gate20T2_ready.md')
with open(comb, 'w', encoding='utf-8') as f:
    f.write('COMBINED CAPTURE (rebuilt ' + cap + ') of Seat B 21st\'s TIER-2 READY FOR QA mails in push order (seat PRs 1, 2, 4, 5 = #1202 KS-965, #1203 KS-1019, #1205 KS-1081, and PR 5 KS-1139 — its PR number is read from its READY when it lands), then the seat STATUS mails, then its QUESTION / wrap mails; each section is the verbatim per-mail capture file named in its header. Seat PR 3 (KS-851, tier 1 by Wednesday\'s 05:12:13Z ANSWER) and PRs 6-10 are the TIER-1 gate\'s and are not captured here. Wednesday\'s brief / ANSWER mails (mail_wed_*.md) are captured beside this file and are NOT part of this combined seat capture.\n')
    for p in TIER2:
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
missing = [p for p in TIER2 if ORDER[p] not in files]
print('combined', comb, 'sections', sorted(files), '| tier-2 READYs present', [p for p in TIER2 if ORDER[p] in files], '| NOT YET ARRIVED', missing or 'NONE')
