#!/usr/bin/env python3
"""drafts_gate48a.py — Seat B 47th's TWO DRAFTED, NOT-FILED ticket texts, VERBATIM with SHA256, into drafted_texts_gate48a.md beside this script,
for DRAFTED-TICKETS-CHECKED (every factual line a ROW; POST AS-IS / AMENDED / DO NOT POST). The READY does NOT carry the texts: it names them
"Verbatim at 5_Project_History/2026-09-30_seatB-47th/ks470/" (Wednesday's leg-7 ruling said "Put the ticket text in your READY"), so they are
read from the seat's record folder (READ ONLY): ks470/TICKET-DRAFT-override.md (the undici override follow-up) and ks470/TICKET-DRAFT-cleanroom.md
(the cleanroom script's remediation command). Also asserts: each file exists, is non-empty and carries the DRAFTED-NOT-FILED header; the READY
names both file names; whether the READY carries either text's title line (recorded, not refused). rc 1 unless both texts are found.
Usage: drafts_gate48a.py"""
import hashlib, os, re, datetime, json
G = os.path.dirname(os.path.abspath(__file__)); K = json.load(open(os.path.join(G, 'kit.json'), encoding='utf-8'))
D = os.path.join(K['seat_record'], 'ks470')
cap = open(os.path.join(G, 'mail_gate48a_ready.md'), encoding='utf-8').read()
ready = re.findall(r'```\n(.*?)\n```', cap, re.S)[0]
T = [('override', 'TICKET-DRAFT-override.md', 'the undici override follow-up (13 accepted advisories; the unscoped override; build + suites UNMEASURED)'),
     ('cleanroom', 'TICKET-DRAFT-cleanroom.md', 'the cleanroom script\'s remediation command (per-dir mount EMISSINGTARGET; npm install inert)')]
now = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
out = ['# gate48a DRAFTED TICKET TEXTS — VERBATIM from Seat B 47th\'s record folder (READ ONLY), DRAFTED, NOT FILED', '',
       'Read %s by drafts_gate48a.py from %s. The READY names these files but does not carry the texts (a finding for the gate: Wednesday\'s leg-7 ruling said "Put the ticket text in your READY"). The seat files them under the board identity only AFTER the merge, on the GO (its handover, 21:56Z). The gate returns each as POST AS-IS / POST AMENDED (with the amended text in full) / DO NOT POST, after checking every factual line as a ROW with evidence.' % (now, D), '']
bad = []
for tag, fn, what in T:
    p = os.path.join(D, fn)
    if not os.path.isfile(p): bad.append('%s missing' % p); continue
    txt = open(p, encoding='utf-8').read()
    if not txt.strip(): bad.append('%s empty' % fn); continue
    hdr = 'DRAFTED, NOT FILED' in txt.split('\n', 1)[0]
    title = (re.search(r'^\*\*Title:\*\*\s*(.+)$', txt, re.M) or [None, ''])[1]
    named = fn in ready; carried = bool(title) and title in ready
    sha = hashlib.sha256(txt.encode('utf-8')).hexdigest()
    out += ['## %s — %s' % (tag, what), '- file: %s' % p, '- SHA256 (file bytes): %s' % sha, '- %d chars, %d lines | DRAFTED-NOT-FILED header: %s | the READY names the file: %s | the READY carries the title: %s' % (len(txt), txt.count('\n') + 1, hdr, named, carried), '', '```', txt.rstrip('\n'), '```', '']
    print('%s %s: %d chars, sha256 %s | header %s | READY names file %s | READY carries text %s' % (tag, fn, len(txt), sha[:16], hdr, named, carried))
    if not hdr: bad.append('%s lacks the DRAFTED, NOT FILED header' % fn)
    if not named: bad.append('the READY does not name %s' % fn)
open(os.path.join(G, 'drafted_texts_gate48a.md'), 'w', encoding='utf-8').write('\n'.join(out) + '\n')
for b in bad: print('PROBLEM: ' + b)
print('DRAFTS %s: %d text(s) -> drafted_texts_gate48a.md | the READY carries the texts verbatim: NO (it names the files)' % ('OK' if not bad else 'FAILED', len(T) - len([b for b in bad if 'missing' in b or 'empty' in b])))
raise SystemExit(1 if bad else 0)
