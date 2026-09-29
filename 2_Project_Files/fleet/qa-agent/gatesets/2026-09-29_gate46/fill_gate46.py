#!/usr/bin/env python3
"""fill_gate46.py — fill the gate46 prompt, launcher and COMMISSION.md from their templates, pins_gate46.json, testrefs_gate46.json and kit.json.
Refuses (rc 1) when pins are missing or not full shas, the pins are a simulation, the head's parent is not round 1, the round-2 delta is not the
declared test-only set, the census was measured at another tree than END_TREE, an output keeps an unfilled {{TOKEN}}, the drafter's summary files
(keyscan_1.out, testrefs_1.out, linear_read_1.out) do not end in PASS / OK, or the filled prompt lacks a keyword.
Writes ONLY: the prompt, the launcher (+x) and COMMISSION.md beside this script. Usage: fill_gate46.py"""
import json, os, re, sys, datetime, hashlib
G = os.path.dirname(os.path.abspath(__file__)); K = json.load(open(os.path.join(G, 'kit.json'), encoding='utf-8'))
P = json.load(open(os.path.join(G, 'pins_gate46.json'), encoding='utf-8'))
T = json.load(open(os.path.join(G, 'testrefs_gate46.json'), encoding='utf-8'))
n = '1348'; k = K['prs'][n]
if P.get('simulate'): raise SystemExit('REFUSING: pins_gate46.json is a SIMULATION (%s)' % P['simulate'])
for x in ('develop', 'develop_tree', 'end_tree'):
    if not re.fullmatch(r'[0-9a-f]{40}', P.get(x) or ''): raise SystemExit('REFUSING: pin %s is not a full sha: %r' % (x, P.get(x)))
p = P['prs'][n]
for x in ('head', 'merge_base', 'parent'):
    if not re.fullmatch(r'[0-9a-f]{40}', p.get(x) or ''): raise SystemExit('REFUSING: #%s pin %s is not a full sha' % (n, x))
if p['parent'] != k['round1_head']: raise SystemExit('REFUSING: #1348 head parent %s is not round 1 %s' % (p['parent'], k['round1_head']))
if sorted(p['round2_delta']) != sorted(k['round2_files']) or not all(p['unchanged_since_round1'].values()): raise SystemExit('REFUSING: the round-2 delta %s / unchanged %s is not the declared test-only set' % (p['round2_delta'], p['unchanged_since_round1']))
if T['tree'] != P['end_tree']: raise SystemExit('REFUSING: testrefs_gate46.json was measured at %s, not the pinned END_TREE %s — re-run testrefs_gate46.py' % (T['tree'], P['end_tree']))
def last(f, want):
    t = open(os.path.join(G, f), encoding='utf-8').read().strip().splitlines()
    t = [l for l in t if l.startswith(want.split()[0])][-1:] or ['<none>']
    if not t[0].startswith(want): raise SystemExit('REFUSING: %s does not carry %s: %s' % (f, want, t[0]))
    return t[0]
KW = ['RED-AT-BASE', 'GREEN-AT-HEAD', 'TAMPER-RIGHT-REASON', 'TAMPER-UNIQUE-ANCHOR', 'RESTORE-SHA256',
      'N-1348-1-RECHECK', 'N-1348-2-RECHECK', 'SUITE-MACOS-BASH32', 'SUITE-GNU-DEBIAN', 'MKTEMP-GNU-1348', 'E1-RED-AT-BASE-1348',
      'TAMPER-RETURN-0-REDS-E1', 'TAMPER-UNCONDITIONAL-REDS-E2', 'E2-CLEAN-DEPLOY-RETURNS-0-1348', 'E1-ANY-NONZERO-1348', 'TAMPER-ARM-COMMENT-1348',
      'PRE-EXISTING-ARMS-1348', 'MODE-100755-RECORDED-1348', 'ROUND2-DELTA-TEST-ONLY', 'PRODUCT-UNCHANGED-SINCE-G45',
      'GATE45-HELD-STILL-HOLDS', 'GATE45-FINDINGS-ROWS-1348', 'PR-BODY-ROUND2-1348', 'RAISE-COMMENT-B82BEBB3',
      'DEPLOY-SH-VERIFY-DRIVEN-1348', 'DEPLOY-SERVICES-TAIL-1348', 'SET-E-CALL-SITES-1348', 'ERR-TRAP-LINE-1348', 'BEHAVIOUR-WIDER-THAN-MIGRATIONS-1348',
      'RULING-A-BOTH-SCRIPTS-1348', 'NAMED-NOT-FIXED-1348', 'WHOLE-SUITE-BEFORE-AFTER', 'NO-NEW-RED', 'SUITES-AT-END', 'CENSUS-TESTS-RUN', 'CENSUS-LISTED',
      'SUBJECT-KEY-SCAN', 'SUBJECT-LANDS-AT', 'SUBJECT-TRUE-OF-DIFF', 'REFS-OWN-KEY', 'NO-CLOSING-KEYWORD',
      'END-TREE', 'CLEAN-MERGE-1348-OVER-8C81', 'OVERLAP-MEASURED', 'ROUND-2-OF-2-CAP-1348', 'DISK-ENOSPC', 'TIERING', 'REPORT-HASH-LAST']
old = K['move_since_base']['from']
files = sorted(p['files'])
row = '  "%s|%s|%s|%s|%d|%d|%s|%d|%s|%s"' % (n, ' + '.join(k['keys']), k['branch'], p['head'], len(files), p['ahead'], p['merge_base'], p['behind'], ','.join(files), k['tier'])
table = '\n'.join(['| PR | ticket | tier | head | parent (round 1) | merge-base | ahead / behind develop | files | declared subject -> lands |', '|---|---|---|---|---|---|---|---|---|',
                   '| #%s | %s | %s | `%s` | `%s` | `%s` | %d / %d | %d | %d -> %d |' % (n, ' + '.join(k['keys']), k['tier'], p['head'], p['parent'][:12], p['merge_base'][:12], p['ahead'], p['behind'], len(files), len(k['subject']), len(k['subject']) + len(' (#%s)' % n))])
subj = '- #%s: `%s` — declared %d, lands %d (%s)' % (n, k['subject'], len(k['subject']), len(k['subject']) + len(' (#%s)' % n), 'the PR title verbatim' if k['subject'] == k['title'] else 'the DRAFTER PROPOSAL, not the PR title')
MS = P.get('modes') or []
if not MS or not all(m['ok'] for m in MS) or sorted(set(m['want'] for m in MS)) != ['100644', '100755']:
    raise SystemExit('REFUSING: the mode pins are missing, failed, or cannot discriminate (need both 100644 and 100755): %s' % MS)
MODE_LINE = 'RECORDED MODES (pin (H), `git ls-tree`, at head / round 1 / END): ' + '; '.join('%s %s' % (m['path'].split('/')[-1], m['want']) for m in MS) + ' — all %d OK.' % len(MS)
R2_LINE = 'diff(round 1 %s, head %s) names ONLY %s; deploy.sh blob+mode BYTE-EQUAL between round 1 and the head: %s.' % (
    k['round1_head'][:12], p['head'][:12], ', '.join(x.split('/')[-1] for x in p['round2_delta']), all(p['unchanged_since_round1'].values()))
prev = K['prev_report']; prev_sha = hashlib.sha256(open(prev, 'rb').read()).hexdigest()
now = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
V = {'GS': G, 'LAUNCHER': K['launcher'], 'PROMPT': K['prompt'], 'REPORT': K['report'], 'GO': K['go'], 'MERGE_SEAT': K['merge_seat'],
     'DEVELOP': P['develop'], 'DEVELOP_TREE': P['develop_tree'], 'DEVELOP_SHORT': P['develop'][:12], 'OLD_BASE': old, 'OLD_BASE_SHORT': old[:12],
     'END_TREE': P['end_tree'], 'MEASURED_AT': P['measured_at'], 'FILLED_AT': now, 'PIN_TABLE': table, 'ROWS': row, 'SUBJECT_TABLE': subj,
     'HEAD': p['head'], 'HEAD_SHORT': p['head'][:12], 'BEHIND': str(p['behind']), 'R1': k['round1_head'], 'R1_SHORT': k['round1_head'][:12],
     'MODE_LINE': MODE_LINE, 'R2_LINE': R2_LINE, 'LINEAR_LINE': last('linear_read_1.out', 'LINEAR READ OK'),
     'CENSUS_N': str(len(T['all_tests'])), 'CENSUS_LIST': '; '.join(t.replace('Blockchain/Dev/', '') for t in T['all_tests']),
     'KEYSCAN': last('keyscan_1.out', 'KEYSCAN PASS'), 'KEYWORDS': ' '.join(KW), 'N_KW': str(len(KW)), 'PREV_REPORT': prev, 'PREV_SHA': prev_sha,
     'VERDICT_SUBJECT': '[QA -> Wednesday] GATE46 #1348 round 2 of 2 (Seat B45 author, Seat B46 merges, round 46; T1: KS-1054 red proof reads the return value, mktemp portable)'}
last('testrefs_1.out', 'TESTREFS PASS')
def fill(src, dst, mode=None):
    t = open(os.path.join(G, src), encoding='utf-8').read()
    for a, v in V.items(): t = t.replace('{{%s}}' % a, v)
    left = sorted(set(re.findall(r'\{\{[A-Z0-9_]+\}\}', t)))
    if left: raise SystemExit('REFUSING: %s keeps unfilled token(s) %s' % (dst, left))
    with open(os.path.join(G, dst), 'w', encoding='utf-8') as f: f.write(t)
    if mode: os.chmod(os.path.join(G, dst), mode)
    print('filled %s (%d bytes)' % (dst, len(t.encode('utf-8'))))
fill('prompt_gate46.TEMPLATE.txt', K['prompt']); fill('launcher_gate46.TEMPLATE.sh.txt', K['launcher'], 0o755); fill('COMMISSION.TEMPLATE.md', 'COMMISSION.md')
pt = open(os.path.join(G, K['prompt']), encoding='utf-8').read()
missing = [w for w in KW if w not in pt]
if missing: raise SystemExit('REFUSING: the prompt lacks keyword(s) %s' % missing)
print('FILL OK at %s: develop %s | END_TREE %s | 1 row | %d keywords | head %s | prev report sha256 %s' % (now, P['develop'], P['end_tree'], len(KW), p['head'][:12], prev_sha[:12]))
