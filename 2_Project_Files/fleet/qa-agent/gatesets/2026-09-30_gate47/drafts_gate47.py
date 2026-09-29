#!/usr/bin/env python3
"""drafts_gate47.py — extract Seat B 46th's TWO DRAFTED, HELD, NOT-POSTED ticket texts VERBATIM from the captured READY (mail_gate47_ready.md,
the CLAIM block) into drafted_texts_gate47.md beside this script, each with its SHA256, so the gate checks every factual line of each against
the head / END / Linear as a ROW (DRAFTED-COMMENTS-CHECKED). Also asserts the captured READY is byte-identical (stripped) to the seat's own record
`5_Project_History/2026-09-29_seatB-46th/mail/READY-gate47.txt` (READ ONLY). The texts are the `> `-quoted blocks under `## DRAFTED, HELD, NOT
POSTED`, headed `**KS-1374 checklist tick (#1349):**` and `**KS-1054 facts comment (N-1348-9 + #1350):**`. rc 1 unless exactly those two are
found, each non-empty, and the READY matches the seat's file. Usage: drafts_gate47.py"""
import hashlib, os, re, datetime
G = os.path.dirname(os.path.abspath(__file__))
SEAT = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-29_seatB-46th/mail/READY-gate47.txt'
cap = open(os.path.join(G, 'mail_gate47_ready.md'), encoding='utf-8').read()
blocks = re.findall(r'```\n(.*?)\n```', cap, re.S)
ready = blocks[0]
same = ready.strip() == open(SEAT, encoding='utf-8').read().strip()
sec = ready.split('## DRAFTED, HELD, NOT POSTED', 1)[1].split('\n## ', 1)[0]
HEADS = [('KS-1374', '#1349', '**KS-1374 checklist tick (#1349):**'), ('KS-1054', '#1350', '**KS-1054 facts comment (N-1348-9 + #1350):**')]
out = ['# gate47 DRAFTED TICKET TEXTS — VERBATIM from Seat B 46th\'s READY (13:58:06Z), HELD, NOT POSTED', '',
       'Extracted %s by drafts_gate47.py from mail_gate47_ready.md (the CLAIM block). The READY as captured == the seat\'s record %s: %s.' % (
           datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'), SEAT, same), '',
       'Each text is the `> `-quoted block with the `> ` prefix removed; markdown emphasis is kept as the seat wrote it. The gate returns each as POST AS-IS / POST AMENDED (with the amended text) / DO NOT POST, after checking every factual claim as a ROW with evidence. Nothing is posted by anyone until the gate has read it (STANDING_LINES :352).', '']
bad = []
for key, pr, head in HEADS:
    if head not in sec: bad.append('heading %r not found' % head); continue
    part = sec.split(head, 1)[1]
    ql = []
    for l in part.split('\n')[1:]:
        if l.startswith('>'): ql.append(l[1:].lstrip(' ') if l != '>' else '')
        elif ql: break
    txt = '\n'.join(ql).strip()
    if not txt: bad.append('%s: empty quoted block' % key); continue
    out += ['## %s — %s' % (key, head.strip('*').rstrip(':')), '- TEXT_SHA256: %s' % hashlib.sha256(txt.encode('utf-8')).hexdigest(), '- %d chars, %d lines' % (len(txt), txt.count('\n') + 1), '', '```', txt, '```', '']
    print('%s %s: %d chars, sha256 %s' % (key, pr, len(txt), hashlib.sha256(txt.encode('utf-8')).hexdigest()[:16]))
if not same: bad.append('the captured READY != the seat file %s' % SEAT)
open(os.path.join(G, 'drafted_texts_gate47.md'), 'w', encoding='utf-8').write('\n'.join(out) + '\n')
for b in bad: print('PROBLEM: ' + b)
print('DRAFTS %s: %d text(s) -> drafted_texts_gate47.md | READY == seat file: %s' % ('OK' if not bad else 'FAILED', len(HEADS) - sum(1 for b in bad if 'heading' in b or 'empty' in b), same))
raise SystemExit(1 if bad else 0)
