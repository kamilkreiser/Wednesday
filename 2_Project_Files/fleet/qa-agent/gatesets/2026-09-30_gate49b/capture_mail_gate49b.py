#!/usr/bin/env python3
"""capture_mail_gate49b.py — the gate49b CAPTURE, found by ONE read-only listing of wednesday-agent@ (GET messages?limit=100; touches no
seen-state) and then read BY ID, VERBATIM, with TEXT_SHA256: every mail from 2026-09-30T03:20Z on whose subject names Seat B 49th / B49 / Seat D 1st
/ D1 / #1357 / #1358 / #1359 / item1a / item1c / gate49b (both seats' threads: plan confirmations, status mails, the three READYs, Wednesday's
ANSWERs). Wednesday's LAUNCH BRIEFs and ADDENDA are recorded by id + TEXT_SHA256 only (context, read on demand). Also: Wednesday's staged ANSWER
and ADDENDUM files for both seats (briefs_staged/2026-09-30_{answer,ADD*}_seat{B49,D1}_*.md — those two seats ONLY) verbatim with sha256, and KAM'S RULING CARD
(decision_queue.sh show <kit prs.1357.ruling_card>) verbatim with sha256.
Checks (rc 1 on any miss): for EACH kit PR exactly one mail FROM ITS SEAT whose subject carries READY and names the PR number (the CLAIM); that
READY names the pinned head IN FULL and its base (the PR's pinned merge-base, `377989cf3829` for all three); it carries a DRAFTED comment section (the text the gate checks line by line);
the READY as captured == the seat's record copy (kit authors.<seat>.record/mail/<file>) compared stripped — a difference or an absent record is
REPORTED, not refused; the ruling card reads `ruled` with choice 'a'. The key is read by name and never printed. Writes mail_gate49b_ready.md.
Usage: capture_mail_gate49b.py"""
import hashlib, json, os, re, urllib.request, urllib.parse, datetime, glob, subprocess
G = os.path.dirname(os.path.abspath(__file__)); K = json.load(open(os.path.join(G, 'kit.json'), encoding='utf-8'))
P = json.load(open(os.path.join(G, 'pins_gate49b.json'), encoding='utf-8')); D12 = P['develop'][:12]
AU = K.get('post_merge_audit'); CAPT = K['order'] + ([AU['pr']] if AU else [])   # the audit PR's READY carries the drafted comments the gate rules
PRX = lambda n: K['prs'][n] if n in K['prs'] else AU
HEADF = lambda n: P['prs'][n]['head'] if n in P['prs'] else AU['head']
MB12 = {n: (P['prs'][n]['merge_base'] if n in P['prs'] else AU['merge_base'])[:12] for n in CAPT}   # each READY names ITS base (the PR's merge-base), not a develop that moved on after it
W = 'wednesday-agent@agentmail.to'
key = ''
for l in open('/Volumes/DevMASTER/WEDNESDAY/4_Credentials/.env', encoding='utf-8'):
    if l.startswith('AGENTMAIL_API_KEY='): key = l.split('=', 1)[1].strip().strip('"').strip("'")
assert key, 'AGENTMAIL_API_KEY unset'
def req(u): return json.load(urllib.request.urlopen(urllib.request.Request(u, headers={'Authorization': 'Bearer ' + key}), timeout=60))
def get(mid): return req('https://api.agentmail.to/v0/inboxes/%s/messages/%s' % (W, urllib.parse.quote(mid, safe='')))
now = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
lst = req('https://api.agentmail.to/v0/inboxes/%s/messages?limit=100' % W).get('messages', [])
RX = re.compile(r'Seat B 49th|B ?49|Seat D 1st|\bD1\b|#?1357\b|#?1358\b|#?1359\b|item ?1a|item ?1c|gate49b', re.I)
sel = sorted([m for m in lst if RX.search(m.get('subject') or '') and (m.get('timestamp') or '') >= '2026-09-30T03:20'], key=lambda m: m.get('timestamp') or '')
RECF = {'1357': 'ready-1a.md', '1359': 'ready-1c.md', '1358': 'ready-1358.txt'}
out = ['# gate49b CAPTURE — the THREE READYs (#1357 and #1359 from Seat B 49th, #1358 from Seat D 1st) and both threads behind them, read by id, VERBATIM', '',
       'Captured %s by capture_mail_gate49b.py from ONE listing of %s (%d listed, %d selected). Each block: role, id, from, timestamp, subject, TEXT_SHA256, then the text VERBATIM.' % (now, W, len(lst), len(sel)), '',
       '#1357 is KS-1054 (ITEM 1a). #1359 is KS-1054 (ITEM 1c). #1358 is KS-1380 (Direction B).', '',
       'The pinned heads, in full (pins_gate49b.json): ' + ' | '.join('#%s %s' % (n, P['prs'][n]['head']) for n in K['order']) + ' | develop %s | END_TREE %s' % (P['develop'], P['end_tree']),
       'POST-MERGE AUDIT subject: #%s head %s, merge commit %s. %s' % (K['post_merge_audit']['pr'], K['post_merge_audit']['head'], K['post_merge_audit']['merge_commit'], K['post_merge_audit']['statement']), '']
bad = []; ready = {n: [] for n in CAPT}
for m in sel:
    s = m.get('subject') or ''
    mm = get(m['message_id']); t = mm.get('text') or mm.get('extracted_text') or ''
    fromseat = 'secuura-blockchain' in (mm.get('from') or '') or s.startswith('[Secuura/Blockchain')
    ctx_only = (not fromseat) and re.search(r'\] (LAUNCH BRIEF|ADDENDUM)', s)
    role = 'CONTEXT (id + sha256 only)' if ctx_only else ('CONTEXT (seat)' if fromseat else 'CONTEXT (Wednesday)')
    if fromseat and 'READY' in s:
        for n in CAPT:
            if re.search(r'#%s\b' % n, s):
                seat = PRX(n)['seat']
                if seat in s: role = 'CLAIM (the READY for #%s, %s)' % (n, seat); ready[n].append(t)
    sha = hashlib.sha256(t.encode('utf-8')).hexdigest()
    out += ['## %s — %s' % (role, s), '- id: %s' % mm.get('message_id'), '- from: %s' % mm.get('from'), '- timestamp: %s' % mm.get('timestamp'), '- TEXT_SHA256: %s (%d chars)' % (sha, len(t)), '']
    if not ctx_only: out += ['```', t, '```', '']
    print('%-40s %s %s | %d chars | %s' % (role[:40], mm.get('timestamp'), sha[:16], len(t), s[:100]))
for n in CAPT:
    seat = PRX(n)['seat']; hf = HEADF(n)
    if len(ready[n]) != 1: bad.append('%d READY mail(s) from %s naming #%s (want exactly 1)' % (len(ready[n]), seat, n)); continue
    r = ready[n][0]
    for p in (hf, MB12[n]):
        if p not in r: bad.append('the #%s READY does not name %s' % (n, p))
    dr = bool(re.search(r'DRAFTED|DRAFT for KS-', r))
    if not dr: bad.append('the #%s READY carries no DRAFTED comment section' % n)
    print('READY #%s (%s): names the pinned head IN FULL %s | its base (merge-base) %s %s | develop now %s | carries a DRAFTED comment section %s' % (n, seat, hf in r, MB12[n], MB12[n] in r, D12, dr))
    rec = os.path.join((K['authors'].get(seat) or K['seats'].get(seat))['record'], 'mail', RECF[n])
    if os.path.exists(rec):
        s2 = open(rec, encoding='utf-8').read().strip(); same = s2 == r.strip() or r.strip() in s2 or s2 in r.strip()
        print('READY #%s as captured vs the seat\'s record %s (stripped; containment either way): %s' % (n, rec, 'SAME' if same else 'DIFFERS (reported, not refused)'))
    else: print('NOTE: the seat\'s record %s does not exist (reported, not refused)' % rec)
card = K['prs']['1357']['ruling_card']
cr = subprocess.run(['bash', '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/tools/decision_queue.sh', 'show', card], capture_output=True, text=True)
ct = cr.stdout
if cr.returncode or not re.search(r"status:\s+ruled", ct) or "choice='a'" not in ct: bad.append('the ruling card %s does not read ruled / choice a (rc %d)' % (card, cr.returncode))
out += ['## KAM\'S RULING CARD `%s` (decision_queue.sh show, rc %d) — sha256 %s' % (card, cr.returncode, hashlib.sha256(ct.encode()).hexdigest()), '', '```', ct.rstrip('\n'), '```', '']
print('RULING CARD %s rc %d | ruled %s | choice a %s | sha256 %s' % (card, cr.returncode, bool(re.search(r"status:\s+ruled", ct)), "choice='a'" in ct, hashlib.sha256(ct.encode()).hexdigest()[:16]))
out += ['## Wednesday\'s staged ANSWER / ADDENDUM files for Seat B 49th and Seat D 1st (briefs_staged, as written before sending; VERBATIM with sha256)', '']
BS = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/'
fs = sorted(set(f for pat in ('2026-09-30_answer_seatB49_*.md', '2026-09-30_answer_seatD1_*.md', '2026-09-30_ADD*_seatB49_*.md', '2026-09-30_ADD*_seatD1_*.md') for f in glob.glob(BS + pat)))
for fn in fs:
    t = open(fn, encoding='utf-8').read()
    out += ['### %s — sha256 %s' % (os.path.basename(fn), hashlib.sha256(t.encode()).hexdigest()), '', '```', t, '```', '']
    print('STAGED FILE %s sha256 %s | %d chars' % (os.path.basename(fn), hashlib.sha256(t.encode()).hexdigest()[:16], len(t)))
open(os.path.join(G, 'mail_gate49b_ready.md'), 'w', encoding='utf-8').write('\n'.join(out) + '\n')
for b in bad: print('PROBLEM: ' + b)
print('CAPTURE %s: %d mails by id (%s READY), %d staged file(s), %d problem(s) -> mail_gate49b_ready.md' % ('OK' if not bad else 'FAILED', len(sel), '/'.join('#%s:%d' % (n, len(ready[n])) for n in CAPT), len(fs), len(bad)))
raise SystemExit(1 if bad else 0)
