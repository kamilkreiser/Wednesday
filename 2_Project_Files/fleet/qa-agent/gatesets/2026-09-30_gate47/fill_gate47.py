#!/usr/bin/env python3
"""fill_gate47.py — fill the gate47 prompt, launcher and COMMISSION.md from their templates, pins_gate47.json, testrefs_gate47.json and kit.json.
Refuses (rc 1) when pins are missing or not full shas, the pins are a simulation, a head's parent is not kit.json's expected_parent, the census
was measured at another tree than END_TREE, the mode pins fail or cannot discriminate, gate46's report no longer hashes to the sha256 in
Wednesday's gate46 GO (kit.json prev_report_sha256), an output keeps an unfilled {{TOKEN}}, the drafter's summary files (keyscan_1.out,
testrefs_1.out, linear_read_1.out, capture_1.out, drafts_1.out) do not end in PASS / OK, or the filled prompt lacks a keyword AS A TOKEN
(bounded by a non-[A-Za-z0-9-] character, so `MODES` is not satisfied by `MODES-X`, and `CLEAN-MERGE` not by `CLEAN-MERGE-1349`).
Writes ONLY: the prompt, the launcher (+x) and COMMISSION.md beside this script. Usage: fill_gate47.py"""
import json, os, re, sys, datetime, hashlib
G = os.path.dirname(os.path.abspath(__file__)); K = json.load(open(os.path.join(G, 'kit.json'), encoding='utf-8'))
P = json.load(open(os.path.join(G, 'pins_gate47.json'), encoding='utf-8'))
T = json.load(open(os.path.join(G, 'testrefs_gate47.json'), encoding='utf-8'))
ORDER = K['order']
if P.get('simulate'): raise SystemExit('REFUSING: pins_gate47.json is a SIMULATION (%s)' % P['simulate'])
for x in ('develop', 'develop_tree', 'end_tree', 'reverse_end_tree'):
    if not re.fullmatch(r'[0-9a-f]{40}', P.get(x) or ''): raise SystemExit('REFUSING: pin %s is not a full sha: %r' % (x, P.get(x)))
if P['end_tree'] != P['reverse_end_tree']: raise SystemExit('REFUSING: the reverse-order END differs from END_TREE')
for n in ORDER:
    p = P['prs'][n]; k = K['prs'][n]
    for x in ('head', 'merge_base', 'parent'):
        if not re.fullmatch(r'[0-9a-f]{40}', p.get(x) or ''): raise SystemExit('REFUSING: #%s pin %s is not a full sha' % (n, x))
    if p['parent'] != k['expected_parent']: raise SystemExit('REFUSING: #%s head parent %s is not the expected %s' % (n, p['parent'], k['expected_parent']))
    if sorted(p['files']) != sorted(k['files']): raise SystemExit('REFUSING: #%s pinned files != kit.json files' % n)
if P['overlap_pairs']: raise SystemExit('REFUSING: the two PRs overlap: %s' % P['overlap_pairs'])
if T['tree'] != P['end_tree']: raise SystemExit('REFUSING: testrefs_gate47.json was measured at %s, not the pinned END_TREE %s — re-run testrefs_gate47.py' % (T['tree'], P['end_tree']))
def last(f, want):
    t = open(os.path.join(G, f), encoding='utf-8').read().strip().splitlines()
    t = [l for l in t if l.startswith(want.split()[0])][-1:] or ['<none>']
    if not t[0].startswith(want): raise SystemExit('REFUSING: %s does not carry %s: %s' % (f, want, t[0]))
    return t[0]
KW = ['HOOK-SKIPPED-LEGS-1349', 'FORMAT-GATE-1349', 'AUDIT-LEGS-1349', 'AUDIT-BASELINE-CLEANUP-NOTE',
      'SUITE-1349', 'RED-FIRST-1349', 'TAMPER-1349', 'NUMBERS-FROM-CODE-1349', 'NOT-COVERED-1349',
      'SUITE-1350-MACOS', 'SUITE-1350-GNU', 'RED-FIRST-1350', 'RED-AT-BASE', 'GREEN-AT-HEAD',
      'CALLER-CELLS-1350', 'ABSENT-STILL-PASSES-1350', 'N-1348-6-BOTH-WAYS', 'R8-EXECUTES', 'PYTHON3-ABSENT-FAILS-CLOSED', 'N-1348-7-COMMENT-FIXED', 'OTHER-CALLERS-1350',
      'TAMPER-ARMS-1350', 'TAMPER-UNIQUE-ANCHOR', 'TAMPER-RIGHT-REASON', 'RESTORE-SHA256',
      'DEPLOY-PATH-TABLE-1350', 'EMPTY-NONJSON-DIVERGENCE', 'N-1346-9-OUT-OF-SCOPE',
      'CLEAN-MERGE', 'END-TREE', 'OVERLAP-MEASURED', 'MODES', 'OUT-OF-KIT-1351',
      'DRAFTED-COMMENTS-CHECKED', 'DRAFT-POST-TIMING', 'CENSUS-TESTS-RUN', 'CENSUS-LISTED',
      'SUBJECT-KEY-SCAN', 'SUBJECT-LANDS-AT', 'SUBJECT-TRUE-OF-DIFF', 'REFS-OWN-KEY', 'NO-CLOSING-KEYWORD', 'PR-BODY-CLAIMS', 'HOOK-LINE-CITE',
      'WHOLE-SUITE-BEFORE-AFTER', 'NO-NEW-RED', 'SUITES-AT-END', 'CLASS-ROUND-1349', 'TIERING', 'DISK-ENOSPC', 'REPORT-HASH-LAST']
p49, p50 = P['prs']['1349'], P['prs']['1350']
rows = []; trs = []
for n in ORDER:
    p = P['prs'][n]; k = K['prs'][n]; files = sorted(p['files'])
    rows.append('  "%s|%s|%s|%s|%d|%d|%s|%d|%s|%s"' % (n, ' + '.join(k['keys']), k['branch'], p['head'], len(files), p['ahead'], p['merge_base'], p['behind'], ','.join(files), k['tier']))
    trs.append('| #%s | %s | %s | `%s` | `%s` | `%s` | %d / %d | %d | %d -> %d |' % (n, ' + '.join(k['keys']), k['tier'], p['head'], p['parent'][:12], p['merge_base'][:12], p['ahead'], p['behind'], len(files), len(k['subject']), len(k['subject']) + len(' (#%s)' % n)))
table = '\n'.join(['| PR | ticket | tier | head | parent | merge-base | ahead / behind develop | files | declared subject -> lands |', '|---|---|---|---|---|---|---|---|---|'] + trs)
subj = '\n'.join('- #%s: `%s` — declared %d, lands %d (%s)' % (n, K['prs'][n]['subject'], len(K['prs'][n]['subject']), len(K['prs'][n]['subject']) + len(' (#%s)' % n),
                 'the PR title verbatim' if K['prs'][n]['subject'] == K['prs'][n]['title'] else 'the DRAFTER PROPOSAL, not the PR title') for n in ORDER)
MS = P.get('modes') or []
if not MS or not all(m['ok'] for m in MS) or sorted(set(m['want'] for m in MS)) != ['100644', '100755']:
    raise SystemExit('REFUSING: the mode pins are missing, failed, or cannot discriminate (need both 100644 and 100755): %s' % MS)
MODE_LINE = 'Recorded modes (pin (H), `git ls-tree`, at head / alone / chain step / END): ' + '; '.join('#%s %s %s' % (m['pr'], m['path'].split('/')[-1], m['want']) for m in MS) + ' — all %d OK.' % len(MS)
HK = P.get('hooks') or {}; HC = P.get('hook_class') or {}
if not HK or not HC: raise SystemExit('REFUSING: pins carry no hook reading (pin (I) / (J))')
HOOK_LINE = 'THE HOOK (pin (I), (J)): ' + '; '.join('%s %s %s (%s)' % (p.split('/')[-1], v['develop'][0], v['develop'][1][:12], 'IDENTICAL at develop, both heads and END' if len(set(tuple(x) if x else None for x in v.values())) == 1 else 'DIFFERS between trees') for p, v in HK.items()) + \
            '. Path class: ' + '; '.join('#%s %d of %d path(s) under Blockchain/Dev/ (%s)' % (n, HC[n]['blockchain_dev'], HC[n]['total'], 'the preflight TRIGGERS' if HC[n]['blockchain_dev'] else 'the preflight FAST-SKIPS, formatting gate only') for n in ORDER) + '.'
ALONE_LINE = 'Each PR ALONE over develop (pin (E)): ' + '; '.join('#%s merge-tree clean, tree `%s`' % (n, P['prs'][n]['alone_tree']) for n in ORDER) + ' — either may merge without the other.'
prev = K['prev_report']; prev_sha = hashlib.sha256(open(prev, 'rb').read()).hexdigest()
if prev_sha != K['prev_report_sha256']: raise SystemExit('REFUSING: gate46 report sha256 %s != the GO\'s %s' % (prev_sha, K['prev_report_sha256']))
dl = last('drafts_1.out', 'DRAFTS OK')
dtx = open(os.path.join(G, 'drafts_1.out'), encoding='utf-8').read()
DRAFTS_LINE = 'both texts VERBATIM with TEXT_SHA256 (the KS-1374 checklist tick for #1349 and the KS-1054 facts comment for N-1348-9 + #1350), extracted from the captured READY by drafts_gate47.py (%s; %s).' % (
    ' | '.join(l.strip() for l in dtx.splitlines() if re.match(r'^KS-\d+ #\d+:', l)), dl)
now = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
V = {'GS': G, 'LAUNCHER': K['launcher'], 'PROMPT': K['prompt'], 'REPORT': K['report'], 'GO': K['go'], 'MERGE_SEAT': K['merge_seat'],
     'DEVELOP': P['develop'], 'DEVELOP_TREE': P['develop_tree'], 'DEVELOP_SHORT': P['develop'][:12], 'OLD_BASE': p49['merge_base'], 'OLD_BASE_SHORT': p49['merge_base'][:12],
     'END_TREE': P['end_tree'], 'MEASURED_AT': P['measured_at'], 'FILLED_AT': now, 'PIN_TABLE': table, 'ROWS': '\n'.join(rows), 'SUBJECT_TABLE': subj,
     'H49': p49['head'], 'H49_SHORT': p49['head'][:12], 'H50': p50['head'], 'H50_SHORT': p50['head'][:12],
     'MODE_LINE': MODE_LINE, 'HOOK_LINE': HOOK_LINE, 'ALONE_LINE': ALONE_LINE, 'LINEAR_LINE': last('linear_read_1.out', 'LINEAR READ OK'), 'DRAFTS_LINE': DRAFTS_LINE,
     'CENSUS_N': str(len(T['all_tests'])), 'CENSUS_LIST': '; '.join(t.replace('Blockchain/Dev/', '') for t in T['all_tests']),
     'KEYSCAN': last('keyscan_1.out', 'KEYSCAN PASS'), 'KEYWORDS': ' '.join(KW), 'N_KW': str(len(KW)), 'PREV_REPORT': prev, 'PREV_SHA': prev_sha, 'G45_REPORT': K['g45_report'],
     'VERDICT_SUBJECT': '[QA -> Wednesday] GATE47 #1349 #1350 (Seat B46 author and merger, round 47; T2: KS-1374 pace keyed on the scan target; T1: KS-1054 a skipped migration check stops reading as a pass)'}
last('testrefs_1.out', 'TESTREFS PASS'); last('capture_1.out', 'CAPTURE OK')
def fill(src, dst, mode=None):
    t = open(os.path.join(G, src), encoding='utf-8').read()
    for a, v in V.items(): t = t.replace('{{%s}}' % a, v)
    left = sorted(set(re.findall(r'\{\{[A-Z0-9_]+\}\}', t)))
    if left: raise SystemExit('REFUSING: %s keeps unfilled token(s) %s' % (dst, left))
    with open(os.path.join(G, dst), 'w', encoding='utf-8') as f: f.write(t)
    if mode: os.chmod(os.path.join(G, dst), mode)
    print('filled %s (%d bytes)' % (dst, len(t.encode('utf-8'))))
fill('prompt_gate47.TEMPLATE.txt', K['prompt']); fill('launcher_gate47.TEMPLATE.sh.txt', K['launcher'], 0o755); fill('COMMISSION.TEMPLATE.md', 'COMMISSION.md')
pt = open(os.path.join(G, K['prompt']), encoding='utf-8').read()
tok = lambda w: re.search(r'(^|[^A-Za-z0-9-])%s([^A-Za-z0-9-]|$)' % re.escape(w), pt) is not None
missing = [w for w in KW if not tok(w)]
if missing: raise SystemExit('REFUSING: the prompt lacks keyword(s) as a token %s' % missing)
print('FILL OK at %s: develop %s | END_TREE %s | %d rows | %d keywords | heads #1349 %s #1350 %s | gate46 report sha256 %s' % (now, P['develop'], P['end_tree'], len(rows), len(KW), p49['head'][:12], p50['head'][:12], prev_sha[:12]))
