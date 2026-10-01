#!/usr/bin/env python3
"""fill_gate50b.py — fill the gate50b prompt, launcher and COMMISSION.md from their templates, pins_gate50b.json and kit.json. ONE PR.
Refuses (rc 1) when: the pins are missing, a simulation, or not full shas; the pinned head != kit.json's head; the head's parent is not one kit.json
allows; the pinned file list != kit.json's 2; the mode pins fail or cannot discriminate (need both 100644 and 100755); an UNCHANGED pin is not
byte-equal; gate50a's report no longer hashes to kit.json prev_report_sha256; end_tree_crosscheck_1.out does not carry the pinned END_TREE three
times; a drafter read (baseline_1.out, sources_1.out, keyscan_1.out, gh_read_1.out, linear_read_1.out) does not end in its PASS / READ / OK line;
baseline_1.out was measured at another develop / head; gh_read_1.json read another head; an output keeps an unfilled {{TOKEN}}; or the filled
prompt lacks a keyword AS A TOKEN. Writes ONLY: the prompt, the launcher (+x) and COMMISSION.md beside this script. Usage: fill_gate50b.py"""
import json, os, re, datetime, hashlib
G = os.path.dirname(os.path.abspath(__file__)); K = json.load(open(os.path.join(G, 'kit.json'), encoding='utf-8'))
P = json.load(open(os.path.join(G, 'pins_gate50b.json'), encoding='utf-8'))
N = K['order'][0]; k = K['prs'][N]; S = P['pr_pins']
if P.get('simulate'): raise SystemExit('REFUSING: pins_gate50b.json is a SIMULATION (%s)' % P['simulate'])
for x in ('develop', 'develop_tree', 'end_tree', 'squash_sim'):
    if not re.fullmatch(r'[0-9a-f]{40}', P.get(x) or ''): raise SystemExit('REFUSING: pin %s is not a full sha: %r' % (x, P.get(x)))
for x in ('head', 'merge_base', 'parent'):
    if not re.fullmatch(r'[0-9a-f]{40}', S.get(x) or ''): raise SystemExit('REFUSING: pin %s is not a full sha' % x)
if S['head'] != k['head']: raise SystemExit('REFUSING: the pinned head %s != kit.json head %s' % (S['head'], k['head']))
if S['parent'] not in k['expected_parent_any']: raise SystemExit('REFUSING: head parent %s is not an allowed parent' % S['parent'])
if sorted(S['files']) != sorted(k['files']): raise SystemExit('REFUSING: pinned files != kit.json files')
MS = P.get('modes') or []
if not MS or not all(m['ok'] for m in MS) or sorted(set(m['want'] for m in MS)) != ['100644', '100755']: raise SystemExit('REFUSING: the mode pins are missing, failed, or cannot discriminate')
UN = P.get('unchanged') or {}
if not UN or not all(v['same'] for v in UN.values()): raise SystemExit('REFUSING: an UNCHANGED pin is not byte-equal')
def txt(f): return open(os.path.join(G, f), encoding='utf-8').read()
def last(f, want):
    t = [l for l in txt(f).strip().splitlines() if l.startswith(want.split()[0])][-1:] or ['<none>']
    if not t[0].startswith(want): raise SystemExit('REFUSING: %s does not carry %s: %s' % (f, want, t[0]))
    return t[0]
KW = ['DIFF-REDERIVED', 'TWO-FILES-ONLY', 'ROWS-26-25', 'REASON-CMP', 'NOTHING-REDATED', 'GRANDFATHERED-BYTE-EQUAL', 'CONTRACT-ONE-LINE', 'FLOOR-NOT-LOWERED',
      'MWP4-DEAD-BOTH-LEGS', 'LEG7-PROBE', 'LEGS-RC-HEAD', 'GATE-STILL-REFUSES', 'FUSE-COHORT', 'ITEM4-TICKET-TEXT', 'KS1397-COMMENT',
      'SUBJECT-KEY-SCAN', 'SUBJECT-LANDS-AT', 'SUBJECT-TRUE-OF-DIFF', 'REFS-OWN-KEY', 'NO-CLOSING-KEYWORD', 'DEHYPHENATED-KEYS', 'PR-BODY-CLAIMS',
      'CLEAN-MERGE', 'END-TREE', 'MODES', 'COLLISION-CENSUS', 'TIERING', 'DISK-ENOSPC', 'REPORT-HASH-LAST']
GHJ = json.load(open(os.path.join(G, 'gh_read_1.json'), encoding='utf-8'))
if GHJ['prs'][N]['head'] != S['head']: raise SystemExit('REFUSING: gh_read_1.json read #%s at %s, the pin is %s — re-run gh_read' % (N, GHJ['prs'][N]['head'][:12], S['head'][:12]))
subj = k.get('subject') or GHJ['prs'][N]['title']; files = sorted(S['files'])
row = '  "%s|%s|%s|%s|%d|%d|%s|%d|%s|%s"' % (N, ' + '.join(k['keys']), k['branch'], S['head'], len(files), S['ahead'], S['merge_base'], S['behind'], ','.join(files), k['tier'])
table = '\n'.join(['| PR | ticket | tier | head | parent | merge-base | ahead / behind | files (+/-) | subject declared -> lands |', '|---|---|---|---|---|---|---|---|---|',
                   '| #%s | %s | %s | `%s` | `%s` | `%s` | %d / %d | %d (+%d/-%d) | %d -> %d |' % (N, ' + '.join(k['keys']), k['tier'], S['head'], S['parent'][:12], S['merge_base'][:12], S['ahead'], S['behind'], len(files), S['adds'], S['dels'], len(subj), len(subj) + len(' (#%s)' % N))])
srow = '- #%s: `%s` — declared %d, lands %d (%s)' % (N, subj, len(subj), len(subj) + len(' (#%s)' % N), ('kit.json subject' if k.get('subject') else 'the LIVE PR title as read at the pin (gh_read_1.json)') + (', == the commit subject' if S['subject_commit'] == subj else ', != the commit subject %r' % S['subject_commit']))
ALONE_LINE = 'ALONE over develop: merge-tree clean, tree `%s` == END_TREE (the squash is simulated with commit-tree, parent develop: `%s`).' % (P['alone_tree'], P['squash_sim'][:12])
ctl = [m for m in MS if m['control']]
MODE_LINE = 'MODES (git ls-tree): both PR paths 100644 at head / alone / END; control `%s` %s at develop / head / END.' % (ctl[0]['path'], ctl[0]['want'])
HOOK_LINE = 'IDENTICAL at develop / head / END: ' + ', '.join('`%s` %s' % (p.split('/')[-1], (list(v.values())[0] or ['', ''])[1][:12]) for p, v in P['hooks'].items() if len(set(json.dumps(x) for x in v.values())) == 1) + '.'
SHORTSTAT = [l for l in txt('pin_1.out').splitlines() if 'git diff --shortstat develop END' in l][-1].split('END: ', 1)[1]
NUMSTAT = 'The measured numstat is +%d/-%d over %d files; the seat claimed %s.' % (S['adds'], S['dels'], len(files), k['claimed_numstat'])
XC = txt('end_tree_crosscheck_1.out')
if XC.count(P['end_tree']) != 3: raise SystemExit('REFUSING: end_tree_crosscheck_1.out does not carry the pinned END_TREE %s three times (the three instruments) — re-run it' % P['end_tree'])
END_XCHECK = 'Three instruments agree on it (end_tree_crosscheck_1.out): merge-tree + commit-tree over develop, the head\'s own tree (parent == develop), and GitHub\'s `refs/pull/%s/merge` tree; develop\'s own tree %s is the control that differs.' % (N, P['develop_tree'][:12])
prev = K['prev_report']; prev_sha = hashlib.sha256(open(prev, 'rb').read()).hexdigest()
if prev_sha != K['prev_report_sha256']: raise SystemExit('REFUSING: gate50a report sha256 %s != kit %s' % (prev_sha, K['prev_report_sha256']))
BL = last('baseline_1.out', 'BASELINE PASS'); SO = last('sources_1.out', 'SOURCES READ'); KS = last('keyscan_1.out', 'KEYSCAN PASS'); LI = last('linear_read_1.out', 'LINEAR READ OK')
b0 = txt('baseline_1.out').splitlines()[0]
if ('base %s' % P['develop'][:12]) not in b0 or ('head %s' % S['head'][:12]) not in b0: raise SystemExit('REFUSING: baseline_1.out was measured at another develop / head — re-run it')
if ('develop %s' % P['develop'][:12]) not in txt('sources_1.out').splitlines()[0]: raise SystemExit('REFUSING: sources_1.out was measured at another develop — re-run it')
last('gh_read_1.out', 'GH READ OK')
cl = [l for l in txt('gh_read_1.out').splitlines() if l.startswith('CENSUS ')]
CENSUS_LINE = (cl[-1] if cl else 'no CENSUS line') + ' (the launch action re-reads it, rc 15 on any hit outside kit.json reported_overlaps)'
OV_LIST = '; '.join('#%s (%s)' % (n, v['why'].split(':')[0]) for n, v in K['reported_overlaps'].items()) or 'NONE touches either path or carries KS-729'
now = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'); H = S['head']
V = {'GS': G, 'PR': N, 'LAUNCHER': K['launcher'], 'PROMPT': K['prompt'], 'REPORT': K['report'], 'GO': K['go'], 'MERGE_SEAT': K['merge_seat'],
     'DEVELOP': P['develop'], 'DEVELOP_TREE': P['develop_tree'], 'DEVELOP_SHORT': P['develop'][:12], 'END_TREE': P['end_tree'], 'MEASURED_AT': P['measured_at'],
     'FILLED_AT': now, 'PIN_TABLE': table, 'ROWS': row, 'SUBJECT_TABLE': srow, 'H': H, 'H_SHORT': H[:12], 'MODE_LINE': MODE_LINE, 'HOOK_LINE': HOOK_LINE,
     'ALONE_LINE': ALONE_LINE, 'SHORTSTAT': SHORTSTAT, 'NUMSTAT': NUMSTAT, 'BASELINE': BL, 'SOURCES': SO, 'LINEAR': LI,
     'OVERLAP_LIST': OV_LIST, 'CENSUS_LINE': CENSUS_LINE, 'KEYSCAN': KS, 'KEYWORDS': ' '.join(KW), 'N_KW': str(len(KW)), 'PREV_REPORT': prev, 'PREV_SHA': prev_sha,
     'VERDICT_SUBJECT': K['verdict_subject'], 'END_XCHECK': END_XCHECK}
def fill(src, dst, mode=None):
    t = open(os.path.join(G, src), encoding='utf-8').read()
    for a, v in V.items(): t = t.replace('{{%s}}' % a, v)
    left = sorted(set(re.findall(r'\{\{[A-Z0-9_]+\}\}', t)))
    if left: raise SystemExit('REFUSING: %s keeps unfilled token(s) %s' % (dst, left))
    if '<PR>' in t: raise SystemExit('REFUSING: %s keeps the <PR> placeholder' % dst)
    with open(os.path.join(G, dst), 'w', encoding='utf-8') as f: f.write(t)
    if mode: os.chmod(os.path.join(G, dst), mode)
    print('filled %s (%d bytes, sha256 %s)' % (dst, len(t.encode('utf-8')), hashlib.sha256(t.encode('utf-8')).hexdigest()[:12]))
fill('prompt_gate50b.TEMPLATE.txt', K['prompt']); fill('launcher_gate50b.TEMPLATE.sh.txt', K['launcher'], 0o755); fill('COMMISSION.TEMPLATE.md', 'COMMISSION.md')
pt = txt(K['prompt'])
missing = [w for w in KW if not re.search(r'(^|[^A-Za-z0-9-])%s([^A-Za-z0-9-]|$)' % re.escape(w), pt)]
if missing: raise SystemExit('REFUSING: the prompt lacks keyword(s) as a token %s' % missing)
print('FILL OK at %s: develop %s | END_TREE %s | 1 row | %d keywords | #%s %s | gate50a report sha256 %s' % (now, P['develop'], P['end_tree'], len(KW), N, H[:12], prev_sha[:12]))
