#!/usr/bin/env python3
"""fill_gate42b.py — fill the gate42b prompt, launcher and COMMISSION.md from their templates, pins_gate42b.json and kit.json (beside this script).
Refuses (rc 1) when pins are missing, a pin is not a full sha, an output keeps an unfilled {{TOKEN}}, or the drafter's summary files
(fieldcheck_1.out, keyscan_1.out) do not end in PASS. Writes ONLY: the prompt, the launcher (+x) and COMMISSION.md beside this script.
Usage: fill_gate42b.py"""
import json, os, re, sys, datetime
G = os.path.dirname(os.path.abspath(__file__)); K = json.load(open(os.path.join(G, 'kit.json'), encoding='utf-8'))
P = json.load(open(os.path.join(G, 'pins_gate42b.json'), encoding='utf-8'))
for k in ('head', 'develop', 'merge_base', 'end_tree', 'blob_head', 'blob_develop', 'develop_tree'):
    if not re.fullmatch(r'[0-9a-f]{40}', P.get(k) or ''): raise SystemExit('REFUSING: pin %s is not a full sha: %r' % (k, P.get(k)))
def last(f, want):
    t = open(os.path.join(G, f), encoding='utf-8').read().strip().splitlines()[-1]
    if not t.startswith(want): raise SystemExit('REFUSING: %s does not end in %s: %s' % (f, want, t))
    return t
KW = ['FIELD-FOUR-ROWS-ONLY', 'FIELD-EXPIRES-AND-REASON-ONLY', 'ROWS-25-BOTH', 'TOP-KEYS-UNCHANGED', 'ONE-FILE-ONLY', 'KAM-EMAIL-VERBATIM', 'NO-UNNAMED-ROW',
      'LEGS-6-7-REAL-CLOCK-HEAD', 'LEGS-6-7-REAL-CLOCK-BASE', 'FROZEN-CLOCK-BY-THE-GATE', 'PRELOAD-POSITIVE-ARM', 'PRELOAD-REFUSES-UNSET', 'FUSE-BASE-RED',
      'FUSE-HEAD-GREEN', 'FUSE-CONTROL-1010-RED', 'SUBJECT-KEY-SCAN', 'SUBJECT-LANDS-AT', 'REFS-THREE-KEYS', 'NO-CLOSING-KEYWORD', 'END-TREE',
      'MERGE-ORDER-1340-ALONE', 'DISK-ENOSPC', 'TIERING']
fp = os.path.join(G, 'fuseproof_1.out')
fuse = ' | '.join(l.strip() for l in open(fp, encoding='utf-8') if l.startswith('ARM')) if os.path.exists(fp) else 'NOT RUN'
now = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
V = {'GS': G, 'LAUNCHER': K['launcher'], 'PROMPT': K['prompt'], 'REPORT': K['report'], 'GO': K['go'], 'MERGE_SEAT': K['merge_seat'],
     'FUSE': K['fuse_utc'], 'HEAD': P['head'], 'DEVELOP': P['develop'], 'DEVELOP_TREE': P['develop_tree'], 'MERGE_BASE': P['merge_base'],
     'AHEAD': str(P['ahead']), 'BEHIND': str(P['behind']), 'END_TREE': P['end_tree'], 'BLOB_HEAD': P['blob_head'], 'BLOB_DEVELOP': P['blob_develop'],
     'BRANCH': P['branch'], 'PATH': K['path'], 'MEASURED_AT': P['measured_at'], 'FILLED_AT': now,
     'AUTH_TEXT': K['authority']['text'], 'AUTH_ID': K['authority']['message_id'], 'AUTH_AT': K['authority']['at'],
     'SUBJECT': K['subject'], 'SUBJ_LEN': str(len(K['subject'])), 'SUBJ_LAND': str(len(K['subject']) + len(' (#%s)' % K['pr'])),
     'MANDATED': K['mandated_body'], 'FIELDCHECK': last('fieldcheck_1.out', 'FIELDCHECK PASS'), 'KEYSCAN': last('keyscan_1.out', 'KEYSCAN PASS'),
     'FUSEPRED': fuse, 'KEYWORDS': ' '.join(KW), 'N_KW': str(len(KW)),
     'VERDICT_SUBJECT': '[QA -> Wednesday] GATE42b batch #1340 (Seat B44, round 42b; T2: KS-530 the audit-baseline re-date, round 1 of 2)'}
def fill(src, dst, mode=None):
    t = open(os.path.join(G, src), encoding='utf-8').read()
    for k, v in V.items(): t = t.replace('{{%s}}' % k, v)
    left = sorted(set(re.findall(r'\{\{[A-Z0-9_]+\}\}', t)))
    if left: raise SystemExit('REFUSING: %s keeps unfilled token(s) %s' % (dst, left))
    open(os.path.join(G, dst), 'w', encoding='utf-8').write(t)
    if mode: os.chmod(os.path.join(G, dst), mode)
    print('filled %s (%d bytes)' % (dst, len(t.encode('utf-8'))))
fill('prompt_gate42b.TEMPLATE.txt', K['prompt']); fill('launcher_gate42b.TEMPLATE.sh.txt', K['launcher'], 0o755); fill('COMMISSION.TEMPLATE.md', 'COMMISSION.md')
missing = [w for w in KW if w not in open(os.path.join(G, K['prompt']), encoding='utf-8').read()]
if missing: raise SystemExit('REFUSING: the prompt lacks keyword(s) %s' % missing)
print('FILL OK at %s: head %s | develop %s | END_TREE %s | %d keywords' % (now, P['head'], P['develop'], P['end_tree'], len(KW)))
