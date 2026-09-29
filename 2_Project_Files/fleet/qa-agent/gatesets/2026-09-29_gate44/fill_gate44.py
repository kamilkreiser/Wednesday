#!/usr/bin/env python3
"""fill_gate44.py — fill the gate44 prompt, launcher and COMMISSION.md from their templates, pins_gate44.json, testrefs_gate44.json and kit.json.
Refuses (rc 1) when pins are missing or not full shas, pins were measured on a develop other than the one testrefs ran at (END_TREE mismatch),
an output keeps an unfilled {{TOKEN}}, the drafter's summary files (keyscan_1.out, testrefs_1.out, linear_read_1.out) do not end in PASS / OK, or the filled prompt lacks
a keyword. Writes ONLY: the prompt, the launcher (+x) and COMMISSION.md beside this script. Usage: fill_gate44.py"""
import json, os, re, sys, datetime
G = os.path.dirname(os.path.abspath(__file__)); K = json.load(open(os.path.join(G, 'kit.json'), encoding='utf-8'))
P = json.load(open(os.path.join(G, 'pins_gate44.json'), encoding='utf-8'))
T = json.load(open(os.path.join(G, 'testrefs_gate44.json'), encoding='utf-8'))
if P.get('simulate'): raise SystemExit('REFUSING: pins_gate44.json is a SIMULATION (%s)' % P['simulate'])
for k in ('develop', 'develop_tree', 'end_tree'):
    if not re.fullmatch(r'[0-9a-f]{40}', P.get(k) or ''): raise SystemExit('REFUSING: pin %s is not a full sha: %r' % (k, P.get(k)))
for n in K['order']:
    for k in ('head', 'merge_base', 'parent'):
        if not re.fullmatch(r'[0-9a-f]{40}', P['prs'][n].get(k) or ''): raise SystemExit('REFUSING: #%s pin %s is not a full sha' % (n, k))
if T['tree'] != P['end_tree']: raise SystemExit('REFUSING: testrefs_gate44.json was measured at %s, not the pinned END_TREE %s — re-run testrefs_gate44.py' % (T['tree'], P['end_tree']))
def last(f, want):
    t = open(os.path.join(G, f), encoding='utf-8').read().strip().splitlines()
    t = [l for l in t if l.startswith(want.split()[0])][-1:] or ['<none>']
    if not t[0].startswith(want): raise SystemExit('REFUSING: %s does not carry %s: %s' % (f, want, t[0]))
    return t[0]
KW = ['RED-AT-BASE', 'GREEN-AT-HEAD', 'TAMPER-RIGHT-REASON', 'TAMPER-UNIQUE-ANCHOR', 'RESTORE-SHA256',
      'WHOLE-SUITE-BEFORE-AFTER', 'NO-NEW-RED', 'TSC-BEFORE-AFTER', 'SUITES-AT-END', 'CENSUS-TESTS-RUN', 'CENSUS-LISTED',
      'SUBJECT-KEY-SCAN', 'SUBJECT-LANDS-AT', 'REFS-OWN-KEY', 'NO-CLOSING-KEYWORD',
      'END-TREE', 'MERGE-ORDER-T1-FIRST', 'OVERLAP-MEASURED', 'NO-REBASE-NEEDED', 'BEHIND-5-NOT-2',
      'MODE-100755-RECORDED-1346', 'TAMPER-MODE-100644-1346', 'TAMPER-KEY-ON-ERROR-1346', 'ABSENT-FIELD-PASSES-WARNS-1346', 'TEST-HALF-0-11-1346',
      'DEPLOY-PATH-DRIVEN-1346', 'DEPLOY-SH-EXIT-CODE-1346', 'RAN-FALSE-1346', 'PASS-LINE-ON-SKIP-1346',
      'W1-GREEN-AT-BASE-1347', 'AKTO-OWN-NPM-CI-1347', 'DOTENV-ORDER-1347', 'LOWER-LIMIT-1-UNPACED-1347', 'PROD-COMPOSE-TEMPLATE-1347',
      'CI-TEMPLATE-1347', 'CORRECTION-LINES-1347', 'PETER-0914-1347',
      'DISK-ENOSPC', 'TIERING', 'REPORT-HASH-LAST']
old = K['move_gate43']['from']
rows = []; table = ['| PR | tickets | tier | head | parent | behind develop | files | declared subject -> lands |', '|---|---|---|---|---|---|---|---|']; subj = []
for n in K['order']:
    k = K['prs'][n]; p = P['prs'][n]
    if p['head'] is None: raise SystemExit('REFUSING: #%s has no head' % n)
    files = sorted(p['files'])
    rows.append('  "%s|%s|%s|%s|%d|%d|%s|%d|%s|%s"' % (n, ' + '.join(k['keys']), k['branch'], p['head'], len(files), p['ahead'], p['merge_base'], p['behind'], ','.join(files), k['tier']))
    table.append('| #%s | %s | %s | `%s` | `%s` | %d | %d | %d -> %d |' % (n, ' + '.join(k['keys']), k['tier'], p['head'], p['parent'][:12], p['behind'], len(files), len(k['subject']), len(k['subject']) + len(' (#%s)' % n)))
    subj.append('- #%s: `%s` — declared %d, lands %d' % (n, k['subject'], len(k['subject']), len(k['subject']) + len(' (#%s)' % n)))
ov = 'OVERLAP: %d of 1 pair overlap; %d paths in total, %d distinct (measured at develop %s).' % (len(P['overlap_pairs']), P['paths_total'], P['paths_distinct'], P['develop'][:12])
now = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
MS = P.get('modes') or []
if not MS or not all(m['ok'] for m in MS) or sorted(set(m['want'] for m in MS)) != ['100644', '100755']:
    raise SystemExit('REFUSING: the mode pins are missing, failed, or cannot discriminate (need both 100644 and 100755): %s' % MS)
MODE_LINE = 'RECORDED MODES (pin (H), `git ls-tree`, at head / alone / chain step / END): ' + '; '.join('%s %s' % (m['path'].split('/')[-1], m['want']) for m in MS) + ' — all %d OK.' % len(MS)
V = {'GS': G, 'LAUNCHER': K['launcher'], 'PROMPT': K['prompt'], 'REPORT': K['report'], 'GO': K['go'], 'MERGE_SEAT': K['merge_seat'],
     'DEVELOP': P['develop'], 'DEVELOP_TREE': P['develop_tree'], 'DEVELOP_SHORT': P['develop'][:12], 'OLD_BASE': old, 'OLD_BASE_SHORT': old[:12],
     'END_TREE': P['end_tree'], 'REVERSE_END': P['reverse_end_tree'], 'MEASURED_AT': P['measured_at'], 'FILLED_AT': now,
     'PIN_TABLE': '\n'.join(table), 'ROWS': '\n'.join(rows), 'OVERLAP_LINE': ov, 'SUBJECT_TABLE': '\n'.join(subj),
     'HEAD_1346_SHORT': P['prs']['1346']['head'][:12], 'HEAD_1347_SHORT': P['prs']['1347']['head'][:12], 'BEHIND_1346': str(P['prs']['1346']['behind']),
     'MODE_LINE': MODE_LINE, 'LINEAR_LINE': last('linear_read_1.out', 'LINEAR READ OK'),
     'CENSUS_N': str(len(T['all_tests'])), 'CENSUS_LIST': '; '.join(t.replace('Blockchain/Dev/', '') for t in T['all_tests']),
     'KEYSCAN': last('keyscan_1.out', 'KEYSCAN PASS'), 'KEYWORDS': ' '.join(KW), 'N_KW': str(len(KW)),
     'VERDICT_SUBJECT': '[QA -> Wednesday] GATE44 batch #1346 #1347 (Seat B45, round 44; T1: KS-1054 deploy scripts read startupMigrations; T2: KS-1374 local limit + Akto reads it)'}
last('testrefs_1.out', 'TESTREFS PASS')
def fill(src, dst, mode=None):
    t = open(os.path.join(G, src), encoding='utf-8').read()
    for k, v in V.items(): t = t.replace('{{%s}}' % k, v)
    left = sorted(set(re.findall(r'\{\{[A-Z0-9_]+\}\}', t)))
    if left: raise SystemExit('REFUSING: %s keeps unfilled token(s) %s' % (dst, left))
    open(os.path.join(G, dst), 'w', encoding='utf-8').write(t)
    if mode: os.chmod(os.path.join(G, dst), mode)
    print('filled %s (%d bytes)' % (dst, len(t.encode('utf-8'))))
fill('prompt_gate44.TEMPLATE.txt', K['prompt']); fill('launcher_gate44.TEMPLATE.sh.txt', K['launcher'], 0o755); fill('COMMISSION.TEMPLATE.md', 'COMMISSION.md')
pt = open(os.path.join(G, K['prompt']), encoding='utf-8').read()
missing = [w for w in KW if w not in pt]
if missing: raise SystemExit('REFUSING: the prompt lacks keyword(s) %s' % missing)
print('FILL OK at %s: develop %s | END_TREE %s | %d rows | %d keywords | heads %s' % (now, P['develop'], P['end_tree'], len(rows), len(KW), ' '.join(P['prs'][n]['head'][:12] for n in K['order'])))
