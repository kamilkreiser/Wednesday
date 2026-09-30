#!/usr/bin/env python3
"""fill_gate49b.py — fill the gate49b prompt, launcher and COMMISSION.md from their templates, pins_gate49b.json and kit.json. THREE PRs, TWO seats.
Refuses (rc 1) when: the pins are missing, a simulation, or not full shas; a pinned head != kit.json's head; a head's parent is not one kit.json
allows; a pinned file list != kit.json's; the pins show a shared path, or a permutation whose tree != END_TREE; the mode pins fail or cannot
discriminate (need both 100644 and 100755); an UNCHANGED pin is not byte-equal; a golden is not byte-equal; gate49a's report no longer hashes to
kit.json prev_report_sha256 (or gate48b's to gate48b_report_sha256); a drafter summary file (lockdelta_1.out, overlaps_1.out, keyscan_1.out,
claims_1.out, gh_read_1.out, capture_1.out) does not end in its PASS / READ / OK line; lockdelta / overlaps were measured at another head / squash
than the pins; gh_read_1.json read another head; an output keeps an unfilled {{TOKEN}}; or the filled prompt lacks a keyword AS A TOKEN.
Writes ONLY: the prompt, the launcher (+x) and COMMISSION.md beside this script. Usage: fill_gate49b.py"""
import json, os, re, datetime, hashlib
G = os.path.dirname(os.path.abspath(__file__)); K = json.load(open(os.path.join(G, 'kit.json'), encoding='utf-8'))
P = json.load(open(os.path.join(G, 'pins_gate49b.json'), encoding='utf-8')); ORDER = K['order']
if P.get('simulate'): raise SystemExit('REFUSING: pins_gate49b.json is a SIMULATION (%s)' % P['simulate'])
if P['order'] != ORDER: raise SystemExit('REFUSING: the pins order %s != kit.json order %s' % (P['order'], ORDER))
for x in ('develop', 'develop_tree', 'end_tree', 'squash_sim', 'reverse_end_tree'):
    if not re.fullmatch(r'[0-9a-f]{40}', P.get(x) or ''): raise SystemExit('REFUSING: pin %s is not a full sha: %r' % (x, P.get(x)))
for n in ORDER:
    S = P['prs'][n]; k = K['prs'][n]
    for x in ('head', 'merge_base', 'parent'):
        if not re.fullmatch(r'[0-9a-f]{40}', S.get(x) or ''): raise SystemExit('REFUSING: #%s pin %s is not a full sha' % (n, x))
    if S['head'] != k['head']: raise SystemExit('REFUSING: #%s pinned head %s != kit.json head %s' % (n, S['head'], k['head']))
    if S['parent'] not in k['expected_parent_any']: raise SystemExit('REFUSING: #%s head parent %s is not an allowed parent' % (n, S['parent']))
    if sorted(S['files']) != sorted(k['files']): raise SystemExit('REFUSING: #%s pinned files != kit.json files' % n)
if any(p['shared'] for p in P['disjoint_pairs']): raise SystemExit('REFUSING: the pins show a SHARED path — the batch is not disjoint')
import math
if P['reverse_end_tree'] != P['end_tree'] or any(t != P['end_tree'] for t in P['permutations'].values()) or len(P['permutations']) != math.factorial(len(ORDER)): raise SystemExit('REFUSING: a merge order gives another tree')
MS = P.get('modes') or []
if not MS or not all(m['ok'] for m in MS) or sorted(set(m['want'] for m in MS)) != ['100644', '100755']: raise SystemExit('REFUSING: the mode pins are missing, failed, or cannot discriminate')
UN = P.get('unchanged') or {}
if not UN or not all(v['same'] for v in UN.values()): raise SystemExit('REFUSING: an UNCHANGED pin is not byte-equal')
GD = P.get('goldens') or {}
if len(GD) != 8 or not all(v['ok'] for v in GD.values()): raise SystemExit('REFUSING: the goldens are not 8 of 8 byte-equal (%d read)' % len(GD))
def txt(f): return open(os.path.join(G, f), encoding='utf-8').read()
def last(f, want):
    t = [l for l in txt(f).strip().splitlines() if l.startswith(want.split()[0])][-1:] or ['<none>']
    if not t[0].startswith(want): raise SystemExit('REFUSING: %s does not carry %s: %s' % (f, want, t[0]))
    return t[0]
KW = ['POST-MERGE-AUDIT', 'MERGED-BEFORE-GATE', 'CLEAN-MERGE', 'DISJOINT', 'END-TREE', 'ORDER-INDEPENDENT', 'MODES', 'EXEC-BITS', 'COLLISION-CENSUS',
      'BEHAVIOUR-1357', 'RED-FIRST-1357', 'PREDICATE-CONTRACT', 'CALLERS-READ', 'RULING-VERBATIM',
      'BEHAVIOUR-1359', 'GOLDENS-BYTE-EQUAL', 'RED-FIRST-1359', 'NO-COUNTER-CHANGE', 'MESSAGE-TRUE',
      'IMAGE-BUILDS', 'LOCK-DELTA-15', 'LANDED-EQUALS-HEAD', 'DEPENDENT-RANGES', 'REGISTRY-TRUE', 'LOCK-AGREEMENT', 'AUDIT-LEGS-DEVELOP', 'TSC-NOT-A-RED-PROOF',
      'SUITES', 'SHELL-RUNNER', 'SHARED-BUILT-FIRST',
      'SUBJECT-KEY-SCAN', 'SUBJECT-LANDS-AT', 'SUBJECT-TRUE-OF-DIFF', 'REFS-OWN-KEY', 'NO-CLOSING-KEYWORD', 'PR-BODY-CLAIMS',
      'DRAFTED-COMMENTS', 'NO-REPEAT-49AFF833', 'FOLLOW-ONS', 'FUSE-COUNT', 'OUT-OF-SCOPE', 'TIERING', 'DISK-ENOSPC', 'REPORT-HASH-LAST']
GHJ = json.load(open(os.path.join(G, 'gh_read_1.json'), encoding='utf-8'))
for n in ORDER:
    if GHJ['prs'][n]['head'] != P['prs'][n]['head']: raise SystemExit('REFUSING: gh_read_1.json read #%s at %s, the pin is %s — re-run gh_read' % (n, GHJ['prs'][n]['head'][:12], P['prs'][n]['head'][:12]))
rows = []; trows = []; srows = []
for n in ORDER:
    S = P['prs'][n]; k = K['prs'][n]; files = sorted(S['files']); subj = k.get('subject') or GHJ['prs'][n]['title']
    rows.append('  "%s|%s|%s|%s|%d|%d|%s|%d|%s|%s"' % (n, ' + '.join(k['keys']), k['branch'], S['head'], len(files), S['ahead'], S['merge_base'], S['behind'], ','.join(files), k['tier']))
    trows.append('| #%s | %s | %s | %s | `%s` | `%s` | %d / %d | %d (+%d/-%d) | %d -> %d |' % (n, ' + '.join(k['keys']), k['tier'], k['seat'], S['head'], S['parent'][:12], S['ahead'], S['behind'], len(files), S['adds'], S['dels'], len(subj), len(subj) + len(' (#%s)' % n)))
    srows.append('- #%s (%s): `%s` — declared %d, lands %d (%s%s)' % (n, k['seat'], subj, len(subj), len(subj) + len(' (#%s)' % n), 'kit.json subject' if k.get('subject') else 'the LIVE PR title as read at the pin (gh_read_1.json)',
                                                                   ', == the commit subject' if S['subject_commit'] == subj else ', != the commit subject %r' % S['subject_commit']))
table = '\n'.join(['| PR | ticket | tier | seat | head | parent | ahead / behind | files (+/-) | subject declared -> lands |', '|---|---|---|---|---|---|---|---|---|'] + trows)
DISJOINT_LINE = 'DISJOINT (pin (D)): %s — 0 shared paths; %d paths, %d distinct. #1357 and #1359 share two DIRECTORIES (deployment/azure, scripts/__tests__), not a path.' % (
    '; '.join('#%s x #%s %d' % (p['a'], p['b'], len(p['shared'])) for p in P['disjoint_pairs']), P['paths_total'], P['paths_distinct'])
PERM_LINE = 'ORDER-INDEPENDENT (pin (G)/(G2)): the merge order #%s gives END_TREE `%s`; the reverse order gives `%s`; all %d permutations give the same tree.' % (
    ' -> #'.join(ORDER), P['end_tree'][:12], P['reverse_end_tree'][:12], len(P['permutations']))
MBS = sorted(set(P['prs'][n]['merge_base'] for n in ORDER)); BEH = sorted(set(P['prs'][n]['behind'] for n in ORDER))
DEVELOP_LINE = ('develop %s (tree %s). Every PR sits on its merge-base %s (#1356\'s squash; its tree == gate49a\'s END_TREE) and is %s behind develop: the move since is %s, and pin (C) reads it reaching NONE of the 21 kit paths — re-derive that.' % (
    P['develop'], P['develop_tree'], ', '.join(MBS), '/'.join(map(str, BEH)), 'NONE (develop == the merge-base)' if MBS == [P['develop']] else '%d path(s)' % len(P['prs'][ORDER[0]]['move'])))
STEP_LINE = 'PER-STEP trees in the merge order (pin (F)): ' + ' -> '.join('#%s `%s`' % (st['pr'], st['tree']) for st in P['chain']) + ' (the last == END_TREE)'
SUBSET_LINE = 'PER-AUTHOR SUBSETS (pin (G2)): ' + '; '.join('%s alone (%s) -> tree `%s`' % (s, ' '.join('#' + x for x in v['prs']), v['tree']) for s, v in P['subsets'].items()) + '.'
MODE_LINE = 'MODES (git ls-tree, at head / alone / chain step / END): check-startup-migrations.sh, deploy.sh, deploy-all.sh 100755; the three suites 100644; all 15 locks 100644; controls `.githooks/pre-push` 100755 and `preflight.sh` 100644 at develop / heads / END — %d of %d OK.' % (sum(m['ok'] for m in MS), len(MS))
HOOK_LINE = 'IDENTICAL at develop / every head / END: ' + ', '.join('`%s` %s' % (p.split('/')[-1], (list(v.values())[0] or ['', ''])[1][:12]) for p, v in P['hooks'].items() if len(set(json.dumps(x) for x in v.values())) == 1) + '.'
GOLDEN_LINE = 'GOLDENS (pin (M)): each golden.diff applied with `git apply --cached` under a temp index to its base 3e3a68260d0e AND to develop gives #1359\'s 4 blobs byte-for-byte (%d of 8 comparisons BYTE-EQUAL; develop\'s blob differs from the head for each, the control).' % sum(v['ok'] for v in GD.values())
SHORTSTAT = [l for l in txt('pin_1.out').splitlines() if 'git diff --shortstat develop END' in l][-1].split('END: ', 1)[1]
prev = K['prev_report']; prev_sha = hashlib.sha256(open(prev, 'rb').read()).hexdigest()
if prev_sha != K['prev_report_sha256']: raise SystemExit('REFUSING: gate49a report sha256 %s != kit %s' % (prev_sha, K['prev_report_sha256']))
g48 = hashlib.sha256(open(K['gate48b_report'], 'rb').read()).hexdigest()
if g48 != K['gate48b_report_sha256']: raise SystemExit('REFUSING: gate48b report sha256 %s != kit %s' % (g48, K['gate48b_report_sha256']))
LD = last('lockdelta_1.out', 'LOCKDELTA PASS'); OV = last('overlaps_1.out', 'OVERLAPS READ'); KS = last('keyscan_1.out', 'KEYSCAN PASS'); CLM = last('claims_1.out', 'CLAIMS READ')
l0 = txt('lockdelta_1.out').splitlines()[0]
AU = K['post_merge_audit']
if ('head %s' % AU['merge_commit'][:12]) not in l0 or ('base %s' % AU['merge_first_parent'][:12]) not in l0 or ('develop %s' % P['develop'][:12]) not in l0: raise SystemExit('REFUSING: lockdelta_1.out was measured at another develop / head — re-run it')
if ('squash_sim %s' % P['squash_sim'][:12]) not in txt('overlaps_1.out').splitlines()[0]: raise SystemExit('REFUSING: overlaps_1.out was measured over another squash — re-run it')
if ('END %s' % P['end_tree'][:12]) not in txt('claims_1.out').splitlines()[0]: raise SystemExit('REFUSING: claims_1.out was measured at another END — re-run it')
last('gh_read_1.out', 'GH READ OK')
cl = [l for l in txt('gh_read_1.out').splitlines() if l.startswith('CENSUS ')]
CENSUS_LINE = (cl[-1] if cl else 'no CENSUS line') + ' (the launch action re-reads it, rc 15 on any hit outside kit.json reported_overlaps)'
OV_LIST = '; '.join('#%s (%s)' % (n, v['why'].split(';')[0]) for n, v in sorted(K['reported_overlaps'].items(), key=lambda x: int(x[0]))) or 'NONE'
AC = [l for l in txt('gh_read_1.out').splitlines() if l.startswith('AUDIT-OVERLAP')]
AUDIT_CENSUS = '; '.join('#' + l.split(') #', 1)[1].split(' ')[0] for l in AC) or 'NONE'
CAP = last('capture_1.out', 'CAPTURE OK')
CAPTURE_LINE = 'both seats\' threads from the plan confirmations to the three READYs, read by id from one listing, verbatim, with TEXT_SHA256; Kam\'s ruling card verbatim; Wednesday\'s staged ANSWER / ADDENDUM files for both seats (%s).' % CAP
now = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
H = {n: P['prs'][n]['head'] for n in ORDER}
V = {'GS': G, 'LAUNCHER': K['launcher'], 'PROMPT': K['prompt'], 'REPORT': K['report'], 'PANE': K['pane'],
     'GO': K['go'], 'STEP_LINE': STEP_LINE, 'DEVELOP_LINE': DEVELOP_LINE,
     'DEVELOP': P['develop'], 'DEVELOP_TREE': P['develop_tree'], 'DEVELOP_SHORT': P['develop'][:12], 'END_TREE': P['end_tree'], 'MEASURED_AT': P['measured_at'],
     'FILLED_AT': now, 'PIN_TABLE': table, 'ROWS': '\n'.join(rows), 'SUBJECT_TABLE': '\n'.join(srows),
     'H1357': H['1357'], 'H1359': H['1359'], 'H1358': AU['head'], 'H1357_SHORT': H['1357'][:12], 'H1359_SHORT': H['1359'][:12], 'H1358_SHORT': AU['head'][:12],
     'M1358': AU['merge_commit'], 'M1358_SHORT': AU['merge_commit'][:12], 'MP1358_SHORT': AU['merge_first_parent'][:12], 'AUDIT_STATEMENT': AU['statement'], 'AUDIT_CENSUS': AUDIT_CENSUS,
     'DISJOINT_LINE': DISJOINT_LINE, 'PERM_LINE': PERM_LINE, 'SUBSET_LINE': SUBSET_LINE, 'MODE_LINE': MODE_LINE, 'HOOK_LINE': HOOK_LINE, 'GOLDEN_LINE': GOLDEN_LINE,
     'SHORTSTAT': SHORTSTAT, 'CAPTURE_LINE': CAPTURE_LINE, 'LOCKDELTA': LD, 'OVERLAPS': OV, 'OVERLAP_LIST': OV_LIST, 'CENSUS_LINE': CENSUS_LINE, 'KEYSCAN': KS, 'CLAIMS': CLM,
     'KEYWORDS': ' '.join(KW), 'N_KW': str(len(KW)), 'PREV_REPORT': prev, 'PREV_SHA': prev_sha, 'G48B_REPORT': K['gate48b_report'], 'G48B_SHA': g48,
     'VERDICT_SUBJECT': K['verdict_subject']}
def fill(src, dst, mode=None):
    t = open(os.path.join(G, src), encoding='utf-8').read()
    for a, v in V.items(): t = t.replace('{{%s}}' % a, v)
    left = sorted(set(re.findall(r'\{\{[A-Z0-9_]+\}\}', t)))
    if left: raise SystemExit('REFUSING: %s keeps unfilled token(s) %s' % (dst, left))
    if '<PR>' in t: raise SystemExit('REFUSING: %s keeps the <PR> placeholder' % dst)
    with open(os.path.join(G, dst), 'w', encoding='utf-8') as f: f.write(t)
    if mode: os.chmod(os.path.join(G, dst), mode)
    print('filled %s (%d bytes, sha256 %s)' % (dst, len(t.encode('utf-8')), hashlib.sha256(t.encode('utf-8')).hexdigest()[:12]))
fill('prompt_gate49b.TEMPLATE.txt', K['prompt']); fill('launcher_gate49b.TEMPLATE.sh.txt', K['launcher'], 0o755); fill('COMMISSION.TEMPLATE.md', 'COMMISSION.md')
pt = txt(K['prompt'])
missing = [w for w in KW if not re.search(r'(^|[^A-Za-z0-9-])%s([^A-Za-z0-9-]|$)' % re.escape(w), pt)]
if missing: raise SystemExit('REFUSING: the prompt lacks keyword(s) as a token %s' % missing)
print('FILL OK at %s: develop %s | END_TREE %s | 2 rows | %d keywords | %s | gate49a report sha256 %s' % (now, P['develop'], P['end_tree'], len(KW), ' '.join('#%s %s' % (n, H[n][:12]) for n in ORDER), prev_sha[:12]))
