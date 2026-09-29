#!/usr/bin/env python3
"""fill_gate43.py — fill the gate43 prompt, launcher and COMMISSION.md from their templates, pins_gate43.json, testrefs_gate43.json and kit.json.
Refuses (rc 1) when pins are missing or not full shas, pins were measured on a develop other than the one testrefs ran at (END_TREE mismatch),
an output keeps an unfilled {{TOKEN}}, the drafter's summary files (keyscan_1.out, testrefs_1.out) do not end in PASS, or the filled prompt lacks
a keyword. Writes ONLY: the prompt, the launcher (+x) and COMMISSION.md beside this script. Usage: fill_gate43.py"""
import json, os, re, sys, datetime
G = os.path.dirname(os.path.abspath(__file__)); K = json.load(open(os.path.join(G, 'kit.json'), encoding='utf-8'))
P = json.load(open(os.path.join(G, 'pins_gate43.json'), encoding='utf-8'))
T = json.load(open(os.path.join(G, 'testrefs_gate43.json'), encoding='utf-8'))
if P.get('simulate'): raise SystemExit('REFUSING: pins_gate43.json is a SIMULATION (%s)' % P['simulate'])
for k in ('develop', 'develop_tree', 'end_tree'):
    if not re.fullmatch(r'[0-9a-f]{40}', P.get(k) or ''): raise SystemExit('REFUSING: pin %s is not a full sha: %r' % (k, P.get(k)))
for n in K['order']:
    for k in ('head', 'merge_base', 'parent'):
        if not re.fullmatch(r'[0-9a-f]{40}', P['prs'][n].get(k) or ''): raise SystemExit('REFUSING: #%s pin %s is not a full sha' % (n, k))
if T['tree'] != P['end_tree']: raise SystemExit('REFUSING: testrefs_gate43.json was measured at %s, not the pinned END_TREE %s — re-run testrefs_gate43.py' % (T['tree'], P['end_tree']))
def last(f, want):
    t = open(os.path.join(G, f), encoding='utf-8').read().strip().splitlines()
    t = [l for l in t if l.startswith(want.split()[0])][-1:] or ['<none>']
    if not t[0].startswith(want): raise SystemExit('REFUSING: %s does not carry %s: %s' % (f, want, t[0]))
    return t[0]
KW = ['RED-AT-BASE', 'GREEN-AT-HEAD', 'TAMPER-RIGHT-REASON', 'TAMPER-UNIQUE-ANCHOR', 'RESTORE-SHA256',
      'WHOLE-SUITE-BEFORE-AFTER', 'NO-NEW-RED', 'TSC-BEFORE-AFTER', 'SUITES-AT-END', 'CENSUS-TESTS-RUN', 'CENSUS-LISTED',
      'SUBJECT-KEY-SCAN', 'SUBJECT-LANDS-AT', 'REFS-OWN-KEY', 'NO-CLOSING-KEYWORD', 'HANG-GREP-1345', 'OPEN-HANDLE-1345',
      'END-TREE', 'MERGE-ORDER-T1-FIRST', 'OVERLAP-MEASURED', 'NO-REBASE-NEEDED', 'PATH-COUNT-15-VS-11',
      'ID-SWAP-TO-LIVE-1341', 'NO-RESOLVER-UNCHANGED-1341', 'STALE-DOC-RESOLVERS-1341', 'HEADERSSENT-REAL-SOCKET-1342', 'UPSTREAM-NOT-HUNG-1342',
      'DISK-ENOSPC', 'TIERING']
old = K['move_1340']['from']
rows = []; table = ['| PR | tickets | tier | head | parent | behind develop | files | declared subject -> lands |', '|---|---|---|---|---|---|---|---|']; subj = []
for n in K['order']:
    k = K['prs'][n]; p = P['prs'][n]
    if p['head'] is None: raise SystemExit('REFUSING: #%s has no head' % n)
    files = sorted(p['files'])
    rows.append('  "%s|%s|%s|%s|%d|%d|%s|%d|%s|%s"' % (n, ' + '.join(k['keys']), k['branch'], p['head'], len(files), p['ahead'], p['merge_base'], p['behind'], ','.join(files), k['tier']))
    table.append('| #%s | %s | %s | `%s` | `%s` | %d | %d | %d -> %d |' % (n, ' + '.join(k['keys']), k['tier'], p['head'], p['parent'][:12], p['behind'], len(files), len(k['subject']), len(k['subject']) + len(' (#%s)' % n)))
    subj.append('- #%s: `%s` — declared %d, lands %d' % (n, k['subject'], len(k['subject']), len(k['subject']) + len(' (#%s)' % n)))
ov = 'OVERLAP: %d of 10 pairs overlap; %d paths in total, %d distinct (measured at develop %s).' % (len(P['overlap_pairs']), P['paths_total'], P['paths_distinct'], P['develop'][:12])
now = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
V = {'GS': G, 'LAUNCHER': K['launcher'], 'PROMPT': K['prompt'], 'REPORT': K['report'], 'GO': K['go'], 'MERGE_SEAT': K['merge_seat'],
     'DEVELOP': P['develop'], 'DEVELOP_TREE': P['develop_tree'], 'DEVELOP_SHORT': P['develop'][:12], 'OLD_BASE': old, 'OLD_BASE_SHORT': old[:12],
     'END_TREE': P['end_tree'], 'REVERSE_END': P['reverse_end_tree'], 'MEASURED_AT': P['measured_at'], 'FILLED_AT': now,
     'PIN_TABLE': '\n'.join(table), 'ROWS': '\n'.join(rows), 'OVERLAP_LINE': ov, 'SUBJECT_TABLE': '\n'.join(subj),
     'HEAD_1341_SHORT': P['prs']['1341']['head'][:12],
     'CENSUS_N': str(len(T['all_tests'])), 'CENSUS_LIST': '; '.join(t.replace('Blockchain/Dev/', '') for t in T['all_tests']),
     'KEYSCAN': last('keyscan_1.out', 'KEYSCAN PASS'), 'KEYWORDS': ' '.join(KW), 'N_KW': str(len(KW)),
     'VERDICT_SUBJECT': '[QA -> Wednesday] GATE43 batch #1341-#1345 (Seat B44 -> B45, round 43; T1: KS-1375 fail closed + KS-1369 proxy crash guard; T2: KS-1371, KS-1359, KS-1360)'}
last('testrefs_1.out', 'TESTREFS PASS')
def fill(src, dst, mode=None):
    t = open(os.path.join(G, src), encoding='utf-8').read()
    for k, v in V.items(): t = t.replace('{{%s}}' % k, v)
    left = sorted(set(re.findall(r'\{\{[A-Z0-9_]+\}\}', t)))
    if left: raise SystemExit('REFUSING: %s keeps unfilled token(s) %s' % (dst, left))
    open(os.path.join(G, dst), 'w', encoding='utf-8').write(t)
    if mode: os.chmod(os.path.join(G, dst), mode)
    print('filled %s (%d bytes)' % (dst, len(t.encode('utf-8'))))
fill('prompt_gate43.TEMPLATE.txt', K['prompt']); fill('launcher_gate43.TEMPLATE.sh.txt', K['launcher'], 0o755); fill('COMMISSION.TEMPLATE.md', 'COMMISSION.md')
pt = open(os.path.join(G, K['prompt']), encoding='utf-8').read()
missing = [w for w in KW if w not in pt]
if missing: raise SystemExit('REFUSING: the prompt lacks keyword(s) %s' % missing)
print('FILL OK at %s: develop %s | END_TREE %s | %d rows | %d keywords | heads %s' % (now, P['develop'], P['end_tree'], len(rows), len(KW), ' '.join(P['prs'][n]['head'][:12] for n in K['order'])))
