#!/usr/bin/env python3
"""capture_ready_mail.py — read-only: capture every Secuura/Blockchain "READY FOR QA (Seat B 10th): PR k ..." mail verbatim (by message id)
from wednesday-agent@ into mail_seatB10_readyK_<ticket>.md (one per mail, never overwritten), plus the 12:46Z STATUS mail (the two findings),
and (re)build the combined brief mail_batch1102_ready.md = the per-mail captures concatenated in PR order. Key by NAME from the WEDNESDAY .env;
never printed. Writes only into this gateset dir. Derived from gatesets/2026-09-20_gate1100to1101/capture_ready_mail.py."""
import hashlib, json, os, sys, urllib.request, urllib.parse, datetime, re
G = os.path.dirname(os.path.abspath(__file__))
key = ''
for line in open('/Volumes/DevMASTER/WEDNESDAY/4_Credentials/.env', encoding='utf-8'):
    if line.startswith('AGENTMAIL_API_KEY='): key = line.split('=', 1)[1].split('#')[0].strip().strip('"').strip("'")
assert key, 'AGENTMAIL_API_KEY unset'
H = {'Authorization': 'Bearer ' + key}
base = 'https://api.agentmail.to/v0/inboxes/wednesday-agent@agentmail.to/messages'
def get(u): return json.load(urllib.request.urlopen(urllib.request.Request(u, headers=H), timeout=60))
msgs = get(base + '?limit=50').get('messages', [])
print('listed', len(msgs), 'oldest', min((m.get('timestamp') or '') for m in msgs))
SUBJ = '[Secuura/Blockchain -> Wednesday] READY FOR QA (Seat B 10th): PR '
STATUS_SUBJ = '[Secuura/Blockchain -> Wednesday] STATUS (Seat B 10th): three RAISED'
hits = [m for m in msgs if 'secuura-blockchain@' in str(m.get('from')) and ((m.get('subject') or '').startswith(SUBJ) or (m.get('subject') or '').startswith(STATUS_SUBJ))]
cap = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
files = {}
for m in sorted(hits, key=lambda x: x.get('timestamp') or ''):
    s = m.get('subject') or ''
    print(m.get('timestamp'), '|', m.get('from'), '|', s, '|', m.get('message_id'))
    mm = re.search(r'PR (\d) (KS-\d+) (\S+)', s)
    if mm:
        k, tk, item = mm.groups(); name = 'mail_seatB10_ready%s_%s.md' % (k, tk.lower())
    else:
        k, tk, item = '0', 'STATUS', 'status'; name = 'mail_seatB10_status_1246.md'
    out = os.path.join(G, name)
    if os.path.exists(out):
        print('  exists, not overwritten:', name)
    else:
        full = get(base + '/' + urllib.parse.quote(m['message_id'], safe=''))
        txt = full.get('text') or ''
        with open(out, 'w', encoding='utf-8') as f:
            f.write('SUBJECT: ' + s + '\nFROM: ' + str(m.get('from')) + '\nTO: ' + str(full.get('to')) + '\nTS: ' + str(m.get('timestamp'))
                    + '\nMESSAGE_ID: ' + m['message_id'] + '\nCAPTURED: ' + cap + ' by the batch 1102-1104 drafter, read-only by message id from wednesday-agent@ (key by name, never printed)'
                    + '\nTEXT_SHA256: ' + hashlib.sha256(txt.encode()).hexdigest() + '\n' + txt + '\n')
        print('  written', name, len(txt), 'chars')
    files[k] = out
# combined brief, PR order 1,2,3 then the STATUS mail; rebuilt every run from the per-mail captures (the launcher greps THIS file)
comb = os.path.join(G, 'mail_batch1102_ready.md')
with open(comb, 'w', encoding='utf-8') as f:
    f.write('COMBINED CAPTURE (rebuilt ' + cap + ') of the Seat B 10th READY FOR QA mails in PR order, then the 12:46Z STATUS mail; each section is the verbatim per-mail capture file named in its header.\n')
    for k in ['1', '2', '3', '0']:
        if k in files:
            f.write('\n\n' + '#' * 8 + ' ' + os.path.basename(files[k]) + ' ' + '#' * 8 + '\n')
            f.write(open(files[k], encoding='utf-8').read())
        else:
            f.write('\n\n' + '#' * 8 + ' PR ' + k + ': NOT YET ARRIVED at ' + cap + ' ' + '#' * 8 + '\n')
print('combined', comb, 'sections', sorted(files))
