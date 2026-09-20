#!/usr/bin/env python3
"""capture_ready_mail.py — read-only: capture every Secuura/Blockchain "READY FOR QA (Seat B 12th): PR <L> ..." mail verbatim (by message id)
from wednesday-agent@ into mail_seatB12_ready<k>_<letter>_<ticket>.md (one per mail, k = the seat's push order A B C D E G F -> 1..7, never
overwritten), plus the 18:45:57Z plan-confirmation QUESTION and the 19:34:31Z STATUS mail (all SEVEN RAISED), plus — as context, not as the
brief — Wednesday's two ANSWERs to this seat (plan confirmation 18:47:45Z; all seven READYs read 20:31:57Z), and (re)build the combined brief
mail_batch1112_ready.md = the per-mail captures concatenated in PR push order (A B C D E G F), then the STATUS, then the plan confirmation.
Key by NAME from the WEDNESDAY .env; never printed. Writes only into this gateset dir. Derived from gatesets/2026-09-21_gate1106to1111/capture_ready_mail.py."""
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
SUBJ = '[Secuura/Blockchain -> Wednesday] READY FOR QA (Seat B 12th): PR '
STATUS_SUBJ = '[Secuura/Blockchain -> Wednesday] STATUS (Seat B 12th): all SEVEN RAISED'
PLAN_SUBJ = '[Secuura/Blockchain -> Wednesday] QUESTION: plan confirmation (Seat B 12th)'
ANS_PLAN = '[Wednesday -> Secuura/Blockchain-B] ANSWER: plan confirmation (Seat B 12th)'
ANS_READ = '[Wednesday -> Secuura/Blockchain-B] ANSWER: all seven READYs read (Seat B 12th)'
ORDER = {'A': '1', 'B': '2', 'C': '3', 'D': '4', 'E': '5', 'G': '6', 'F': '7'}
def is_seat(m): return 'secuura-blockchain@' in str(m.get('from'))
def is_wed(m): return 'wednesday-agent@' in str(m.get('from'))
hits = [m for m in msgs if (is_seat(m) and ((m.get('subject') or '').startswith(SUBJ) or (m.get('subject') or '').startswith(STATUS_SUBJ) or (m.get('subject') or '').startswith(PLAN_SUBJ)))
        or (is_wed(m) and ((m.get('subject') or '').startswith(ANS_PLAN) or (m.get('subject') or '').startswith(ANS_READ)))]
cap = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
files = {}
for m in sorted(hits, key=lambda x: x.get('timestamp') or ''):
    s = m.get('subject') or ''
    print(m.get('timestamp'), '|', m.get('from'), '|', s, '|', m.get('message_id'))
    mm = re.search(r'PR ([A-G]) (KS-\d+|anchoring)', s)
    if mm and s.startswith(SUBJ):
        letter, tk = mm.groups(); k = ORDER[letter]
        name = 'mail_seatB12_ready%s_%s_%s.md' % (k, letter, tk.lower().replace('-', ''))
    elif s.startswith(STATUS_SUBJ): k = 'S'; name = 'mail_seatB12_status_1934.md'
    elif s.startswith(PLAN_SUBJ): k = 'P'; name = 'mail_seatB12_plan_confirmation_1845.md'
    elif s.startswith(ANS_PLAN): k = 'WP'; name = 'mail_wed_answer_plan_confirmation_1847.md'
    else: k = 'WR'; name = 'mail_wed_answer_all_seven_read_2031.md'
    out = os.path.join(G, name)
    if os.path.exists(out):
        print('  exists, not overwritten:', name)
    else:
        full = get(base + '/' + urllib.parse.quote(m['message_id'], safe=''))
        txt = full.get('text') or ''
        with open(out, 'w', encoding='utf-8') as f:
            f.write('SUBJECT: ' + s + '\nFROM: ' + str(m.get('from')) + '\nTO: ' + str(full.get('to')) + '\nTS: ' + str(m.get('timestamp'))
                    + '\nMESSAGE_ID: ' + m['message_id'] + '\nCAPTURED: ' + cap + ' by the batch 1112-1118 drafter, read-only by message id from wednesday-agent@ (key by name, never printed)'
                    + '\nTEXT_SHA256: ' + hashlib.sha256(txt.encode()).hexdigest() + '\n' + txt + '\n')
        print('  written', name, len(txt), 'chars')
    files[k] = out
# combined brief, PR push order A B C D E G F (1..7), then the STATUS, then the plan confirmation; rebuilt every run (the launcher greps THIS file)
comb = os.path.join(G, 'mail_batch1112_ready.md')
with open(comb, 'w', encoding='utf-8') as f:
    f.write('COMBINED CAPTURE (rebuilt ' + cap + ') of the Seat B 12th READY FOR QA mails in PR push order (A B C D E G F = 1..7), then the 19:34Z STATUS mail, then the 18:45Z plan-confirmation QUESTION; each section is the verbatim per-mail capture file named in its header. Wednesday\'s two ANSWER mails are captured beside this file (mail_wed_answer_*.md) and are NOT part of this combined seat capture.\n')
    for k in ['1', '2', '3', '4', '5', '6', '7', 'S', 'P']:
        if k in files:
            f.write('\n\n' + '#' * 8 + ' ' + os.path.basename(files[k]) + ' ' + '#' * 8 + '\n')
            f.write(open(files[k], encoding='utf-8').read())
        else:
            f.write('\n\n' + '#' * 8 + ' section ' + k + ': NOT YET ARRIVED at ' + cap + ' ' + '#' * 8 + '\n')
print('combined', comb, 'sections', sorted(files))
