#!/usr/bin/env python3
"""capture_ready_mail.py — read-only: capture every Secuura/Blockchain "READY FOR QA (Seat B 13th): PR <L> ..." mail verbatim (by message id)
from wednesday-agent@ into mail_seatB13_ready<k>_<letter>_<ticket>.md (one per mail, k = the seat's push order B E G F H A D I J C -> 1..10,
never overwritten), plus the 00:13:13Z plan-confirmation QUESTION, the 00:58:10Z STATUS mail (all TEN RAISED), the 00:39:34Z PR C cross-stage-red
QUESTION and the 01:44:22Z PR D leg-14 QUESTION, plus — as context, not as the brief — Wednesday's three ANSWERs to this seat (plan confirmation
00:15:00Z; PR C 00:41:13Z; PR D 01:47:25Z), and (re)build the combined brief mail_batch1119_ready.md = the per-mail captures concatenated in PR push
order (B E G F H A D I J C), then the STATUS, then the plan confirmation, then the two mid-raise QUESTIONs. Missing sections are marked NOT YET
ARRIVED. Key by NAME from the WEDNESDAY .env; never printed. Writes only into this gateset dir. Derived from gatesets/2026-09-21_gate1112to1118/capture_ready_mail.py."""
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
SUBJ = '[Secuura/Blockchain -> Wednesday] READY FOR QA (Seat B 13th): PR '
STATUS_SUBJ = '[Secuura/Blockchain -> Wednesday] STATUS (Seat B 13th): all TEN RAISED'
PLAN_SUBJ = '[Secuura/Blockchain -> Wednesday] QUESTION: plan confirmation (Seat B 13th)'
QPRC_SUBJ = '[Secuura/Blockchain -> Wednesday] QUESTION: PR C cross-stage red (Seat B 13th)'
QPRD_SUBJ = '[Secuura/Blockchain -> Wednesday] QUESTION: PR D push refused by preflight leg 14 (Seat B 13th)'
ANS_PLAN = '[Wednesday -> Secuura/Blockchain-B] ANSWER: plan confirmation (Seat B 13th)'
ANS_PRC = '[Wednesday -> Secuura/Blockchain-B] ANSWER: PR C cross-stage red (Seat B 13th)'
ANS_PRD = '[Wednesday -> Secuura/Blockchain-B] ANSWER: PR D push refused by preflight leg 14 (Seat B 13th)'
ORDER = {'B': '01', 'E': '02', 'G': '03', 'F': '04', 'H': '05', 'A': '06', 'D': '07', 'I': '08', 'J': '09', 'C': '10'}
def is_seat(m): return 'secuura-blockchain@' in str(m.get('from'))
def is_wed(m): return 'wednesday-agent@' in str(m.get('from'))
def sub(m): return m.get('subject') or ''
hits = [m for m in msgs if (is_seat(m) and any(sub(m).startswith(s) for s in (SUBJ, STATUS_SUBJ, PLAN_SUBJ, QPRC_SUBJ, QPRD_SUBJ)))
        or (is_wed(m) and any(sub(m).startswith(s) for s in (ANS_PLAN, ANS_PRC, ANS_PRD)))]
cap = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
files = {}
for m in sorted(hits, key=lambda x: x.get('timestamp') or ''):
    s = sub(m)
    print(m.get('timestamp'), '|', m.get('from'), '|', s, '|', m.get('message_id'))
    mm = re.search(r'PR ([A-J]) (KS-\d+)', s)
    if mm and s.startswith(SUBJ):
        letter, tk = mm.groups(); k = ORDER[letter]
        name = 'mail_seatB13_ready%s_%s_%s.md' % (k, letter, tk.lower().replace('-', ''))
    elif s.startswith(STATUS_SUBJ): k = 'S'; name = 'mail_seatB13_status_0058.md'
    elif s.startswith(PLAN_SUBJ): k = 'P'; name = 'mail_seatB13_plan_confirmation_0013.md'
    elif s.startswith(QPRC_SUBJ): k = 'QC'; name = 'mail_seatB13_question_prc_0039.md'
    elif s.startswith(QPRD_SUBJ): k = 'QD'; name = 'mail_seatB13_question_prd_0144.md'
    elif s.startswith(ANS_PLAN): k = 'WP'; name = 'mail_wed_answer_plan_confirmation_0015.md'
    elif s.startswith(ANS_PRC): k = 'WC'; name = 'mail_wed_answer_prc_0041.md'
    else: k = 'WD'; name = 'mail_wed_answer_prd_0147.md'
    out = os.path.join(G, name)
    if os.path.exists(out):
        print('  exists, not overwritten:', name)
    else:
        full = get(base + '/' + urllib.parse.quote(m['message_id'], safe=''))
        txt = full.get('text') or ''
        with open(out, 'w', encoding='utf-8') as f:
            f.write('SUBJECT: ' + s + '\nFROM: ' + str(m.get('from')) + '\nTO: ' + str(full.get('to')) + '\nTS: ' + str(m.get('timestamp'))
                    + '\nMESSAGE_ID: ' + m['message_id'] + '\nCAPTURED: ' + cap + ' by the batch 1119-1128 drafter, read-only by message id from wednesday-agent@ (key by name, never printed)'
                    + '\nTEXT_SHA256: ' + hashlib.sha256(txt.encode()).hexdigest() + '\n' + txt + '\n')
        print('  written', name, len(txt), 'chars')
    files[k] = out
comb = os.path.join(G, 'mail_batch1119_ready.md')
with open(comb, 'w', encoding='utf-8') as f:
    f.write('COMBINED CAPTURE (rebuilt ' + cap + ') of the Seat B 13th READY FOR QA mails in PR push order (B E G F H A D I J C = 01..10), then the 00:58Z STATUS mail, then the 00:13Z plan-confirmation QUESTION, then the 00:39Z PR C and 01:44Z PR D QUESTIONs; each section is the verbatim per-mail capture file named in its header. Wednesday\'s three ANSWER mails are captured beside this file (mail_wed_answer_*.md) and are NOT part of this combined seat capture.\n')
    for k in ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', 'S', 'P', 'QC', 'QD']:
        if k in files:
            f.write('\n\n' + '#' * 8 + ' ' + os.path.basename(files[k]) + ' ' + '#' * 8 + '\n')
            f.write(open(files[k], encoding='utf-8').read())
        else:
            f.write('\n\n' + '#' * 8 + ' section ' + k + ': NOT YET ARRIVED at ' + cap + ' ' + '#' * 8 + '\n')
print('combined', comb, 'sections', sorted(files))
