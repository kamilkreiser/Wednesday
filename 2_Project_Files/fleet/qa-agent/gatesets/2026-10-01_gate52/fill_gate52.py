#!/usr/bin/env python3
"""fill_gate52.py — fill the gate52 prompt, launcher and COMMISSION.md from their templates, pins_gate52.json and kit.json. TWO PRs (#1367 then
#1368). Refuses (rc 1) when: the pins are missing, a simulation, or not full shas; a pinned head != kit.json's head; a head's parent is not one kit
allows; a pinned file list != kit.json's; the mode pins fail or cannot discriminate (need both 100644 and 100755); an UNCHANGED pin is not
byte-equal; END_TREE_B != kit end_tree_after_b_predicted; gate51a's report no longer hashes to kit.json prev_report_sha256;
end_tree_crosscheck_1.out does not carry END_TREE_A and END_TREE_B three times each and end in ENDTREE AGREE; a drafter read (specdiff_1.out,
handlers_1.out, keyscan_1.out, gh_read_1.out) does not end in its PASS / OK line; specdiff_1.out or handlers_1.out was measured at another
develop / head; gh_read_1.json read another head; an output keeps an unfilled {{TOKEN}}; or the filled prompt lacks a keyword AS A TOKEN.
Writes ONLY: the prompt, the launcher (+x) and COMMISSION.md beside this script. Usage: fill_gate52.py"""
import json, os, re, datetime, hashlib
G = os.path.dirname(os.path.abspath(__file__)); K = json.load(open(os.path.join(G, 'kit.json'), encoding='utf-8'))
P = json.load(open(os.path.join(G, 'pins_gate52.json'), encoding='utf-8'))
ORDER = K['order']; NA, NB = ORDER; S = P['pr_pins']
if P.get('simulate'): raise SystemExit('REFUSING: pins_gate52.json is a SIMULATION (%s)' % P['simulate'])
for x in ('develop', 'develop_tree', 'end_tree_a', 'squash_sim_a', 'end_tree_b', 'squash_sim_b'):
    if not re.fullmatch(r'[0-9a-f]{40}', P.get(x) or ''): raise SystemExit('REFUSING: pin %s is not a full sha: %r' % (x, P.get(x)))
for n in ORDER:
    k = K['prs'][n]
    for x in ('head', 'merge_base', 'parent'):
        if not re.fullmatch(r'[0-9a-f]{40}', S[n].get(x) or ''): raise SystemExit('REFUSING: #%s pin %s is not a full sha' % (n, x))
    if S[n]['head'] != k['head']: raise SystemExit('REFUSING: #%s pinned head %s != kit.json head %s' % (n, S[n]['head'], k['head']))
    if S[n]['parent'] not in k['expected_parent_any']: raise SystemExit('REFUSING: #%s head parent %s is not an allowed parent' % (n, S[n]['parent']))
    if sorted(S[n]['files']) != sorted(k['files']): raise SystemExit('REFUSING: #%s pinned files != kit.json files' % n)
if P['end_tree_b'] != K['end_tree_after_b_predicted']: raise SystemExit('REFUSING: END_TREE_B %s != the seat\'s PREDICTED %s' % (P['end_tree_b'], K['end_tree_after_b_predicted']))
MS = P.get('modes') or []
if not MS or not all(m['ok'] for m in MS) or sorted(set(m['want'] for m in MS)) != ['100644', '100755']: raise SystemExit('REFUSING: the mode pins are missing, failed, or cannot discriminate')
UN = P.get('unchanged') or {}
if not UN or not all(v['same'] for v in UN.values()): raise SystemExit('REFUSING: an UNCHANGED pin is not byte-equal')
def txt(f): return open(os.path.join(G, f), encoding='utf-8').read()
def last(f, want):
    t = [l for l in txt(f).strip().splitlines() if l.startswith(want.split()[0])][-1:] or ['<none>']
    if not t[0].startswith(want): raise SystemExit('REFUSING: %s does not carry %s: %s' % (f, want, t[0]))
    return t[0]
KW = ['ENVELOPE-MATCHES-HANDLER', 'ERROR-CODES-MATCH', 'HANDLER-REJECTS-ABSENT', 'BODY-PARSER-DEFAULT', 'ALIASES-COVERED', 'GENERATE-NOT-REQUIRED',
      'GOLDENS-BYTE-EQUAL', 'GENERATOR-REPRODUCES', 'CHECK-OPENAPI-RC', 'YAML-SHAS', 'RED-FIRST', 'CONTROLS-GREEN', 'SUITES-BASE-HEAD', 'TSC-NO-REGRESSION',
      'SEQUENCE-A-THEN-B', 'CLEAN-MERGE', 'END-TREE', 'BOTH-MERGEABLE', 'MODES',
      'KEYSCAN-OWN-KEY', 'NO-CLOSING-KEYWORD', 'NO-TRAILER', 'SUBJECT-LANDS-AT', 'SUBJECT-TRUE-OF-DIFF', 'PR-BODY-CLAIMS', 'NO-RUNTIME-CHANGE',
      'COLLISION-CENSUS', 'NOT-TESTED-LIST', 'TIERING', 'DISK-ENOSPC', 'REPORT-HASH-LAST']
GHJ = json.load(open(os.path.join(G, 'gh_read_1.json'), encoding='utf-8'))
for n in ORDER:
    if GHJ['prs'][n]['head'] != S[n]['head']: raise SystemExit('REFUSING: gh_read_1.json read #%s at %s, the pin is %s — re-run gh_read' % (n, GHJ['prs'][n]['head'][:12], S[n]['head'][:12]))
subj = {n: K['prs'][n].get('subject') or GHJ['prs'][n]['title'] for n in ORDER}
rows = []; trows = ['| PR | ticket | role | tier | head | parent | merge-base | ahead / behind | files (+/-) | subject declared -> lands |', '|---|---|---|---|---|---|---|---|---|---|']; srows = []
for n in ORDER:
    k = K['prs'][n]; s = S[n]; files = sorted(s['files'])
    rows.append('  "%s|%s|%s|%s|%d|%d|%s|%d|%s|%s"' % (n, ' + '.join(k['keys']), k['branch'], s['head'], len(files), s['ahead'], s['merge_base'], s['behind'], ','.join(files), k['tier']))
    trows.append('| #%s | %s | %s | %s | `%s` | `%s` | `%s` | %d / %d | %d (+%d/-%d) | %d -> %d |' % (n, ' + '.join(k['keys']), k['role'], k['tier'], s['head'], s['parent'][:12], s['merge_base'][:12], s['ahead'], s['behind'], len(files), s['adds'], s['dels'], len(subj[n]), len(subj[n]) + len(' (#%s)' % n)))
    srows.append('- #%s: `%s` — declared %d, lands %d (%s)' % (n, subj[n], len(subj[n]), len(subj[n]) + len(' (#%s)' % n), ('kit.json subject' if k.get('subject') else 'the LIVE PR title as read at the pin (gh_read_1.json)') + (', == the commit subject' if s['subject_commit'] == subj[n] else ', != the commit subject %r' % s['subject_commit'])))
CHAIN_LINE = 'EACH ALONE over develop: #%s merge-tree clean, tree `%s`; #%s merge-tree clean, tree `%s`. THE CHAIN: #%s squashed (commit-tree -p develop, `%s`) -> END_TREE_A `%s`; #%s merged onto that squash with no conflict (`%s`) -> END_TREE_B `%s` == the seat\'s PREDICTED tree; `merge-tree --write-tree A B` reads the same tree.' % (
    NA, P['alone_trees'][NA], NB, P['alone_trees'][NB], NA, P['squash_sim_a'][:12], P['end_tree_a'], NB, P['squash_sim_b'][:12], P['end_tree_b'])
ctl = [m for m in MS if m['control']]
MODE_LINE = 'MODES (git ls-tree): all %d distinct PR paths 100644 (%d pins: the shared yaml is pinned once per PR) at their head / alone / END_TREE_B; control `%s` %s at develop / both heads / END_TREE_B.' % (len(set(m['path'] for m in MS if not m['control'])), sum(not m['control'] for m in MS), ctl[0]['path'], ctl[0]['want'])
HOOK_LINE = 'IDENTICAL at develop / both heads / END_A / END_B: ' + ', '.join('`%s` %s' % (p.split('/')[-1], (list(v.values())[0] or ['', ''])[1][:12]) for p, v in P['hooks'].items() if len(set(json.dumps(x) for x in v.values())) == 1) + '.'
pin_out = txt('pin_1.out')
SHORTSTAT_A = [l for l in pin_out.splitlines() if 'git diff --shortstat develop END_A' in l][-1].split('END_A: ', 1)[1]
SHORTSTAT_B = [l for l in pin_out.splitlines() if 'git diff --shortstat develop END_B' in l][-1].split('END_B: ', 1)[1]
NUMSTAT = 'The measured numstat: ' + '; '.join('#%s +%d/-%d over %d files (the seat claimed %s)' % (n, S[n]['adds'], S[n]['dels'], len(S[n]['files']), K['prs'][n]['claimed_numstat']) for n in ORDER) + '.'
XC = txt('end_tree_crosscheck_1.out')
if XC.count(P['end_tree_a']) < 4 or XC.count(P['end_tree_b']) < 4 or not last('end_tree_crosscheck_1.out', 'ENDTREE AGREE'):
    raise SystemExit('REFUSING: end_tree_crosscheck_1.out does not carry END_TREE_A / END_TREE_B three times each (+ the summary) — re-run endtree_gate52.py')
END_XCHECK = 'Three instruments agree on each (end_tree_crosscheck_1.out): END_TREE_A by merge-tree + commit-tree, by A\'s own tree (parent == develop) and by GitHub\'s `refs/pull/%s/merge`; END_TREE_B by the chained merge-tree, by `merge-tree A B`, and by B\'s diff applied onto END_TREE_A under a temp index. Controls that differ: develop\'s own tree %s and GitHub\'s `refs/pull/%s/merge` (B alone).' % (NA, P['develop_tree'][:12], NB)
prev = K['prev_report']; prev_sha = hashlib.sha256(open(prev, 'rb').read()).hexdigest()
if prev_sha != K['prev_report_sha256']: raise SystemExit('REFUSING: gate51a report sha256 %s != kit %s' % (prev_sha, K['prev_report_sha256']))
SD = last('specdiff_1.out', 'SPECDIFF PASS'); HD = last('handlers_1.out', 'HANDLERS PASS'); KS = last('keyscan_1.out', 'KEYSCAN PASS')
b0 = txt('specdiff_1.out').splitlines()[0]
if ('base %s' % P['develop'][:12]) not in b0 or any(('#%s head %s' % (n, S[n]['head'][:12])) not in b0 for n in ORDER): raise SystemExit('REFUSING: specdiff_1.out was measured at another develop / head — re-run it')
h0 = txt('handlers_1.out').splitlines()[0]
if any(('#%s tree %s' % (n, S[n]['head'][:12])) not in h0 for n in ORDER): raise SystemExit('REFUSING: handlers_1.out was read at another tree — re-run it')
last('gh_read_1.out', 'GH READ OK')
cl = [l for l in txt('gh_read_1.out').splitlines() if l.startswith('CENSUS ')]
CENSUS_LINE = (cl[-1] if cl else 'no CENSUS line') + ' (the launch action re-reads it, rc 15 on any hit outside kit.json reported_overlaps)'
OV_LIST = '; '.join('#%s (%s)' % (n, v['why'].split(':')[0]) for n, v in K['reported_overlaps'].items()) or 'NONE touches any of the 7 paths or carries KS-1015 / KS-1364'
now = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
V = {'GS': G, 'PA': NA, 'PB': NB, 'HA': S[NA]['head'], 'HB': S[NB]['head'], 'HA_SHORT': S[NA]['head'][:12], 'HB_SHORT': S[NB]['head'][:12],
     'LAUNCHER': K['launcher'], 'PROMPT': K['prompt'], 'REPORT': K['report'], 'GO': K['go'], 'MERGE_SEAT': K['merge_seat'],
     'DEVELOP': P['develop'], 'DEVELOP_TREE': P['develop_tree'], 'DEVELOP_SHORT': P['develop'][:12], 'END_TREE_A': P['end_tree_a'], 'END_TREE_B': P['end_tree_b'],
     'MEASURED_AT': P['measured_at'], 'FILLED_AT': now, 'PIN_TABLE': '\n'.join(trows), 'ROWS': '\n'.join(rows), 'SUBJECT_TABLE': '\n'.join(srows),
     'MODE_LINE': MODE_LINE, 'HOOK_LINE': HOOK_LINE, 'CHAIN_LINE': CHAIN_LINE, 'SHORTSTAT_A': SHORTSTAT_A, 'SHORTSTAT_B': SHORTSTAT_B, 'NUMSTAT': NUMSTAT,
     'SPECDIFF': SD, 'HANDLERS': HD, 'GOLDENS_DIR': K['goldens_dir'], 'OVERLAP_LIST': OV_LIST, 'CENSUS_LINE': CENSUS_LINE, 'KEYSCAN': KS,
     'KEYWORDS': ' '.join(KW), 'N_KW': str(len(KW)), 'PREV_REPORT': prev, 'PREV_SHA': prev_sha, 'VERDICT_SUBJECT': K['verdict_subject'], 'END_XCHECK': END_XCHECK,
     'USAGE': K['usage_pct']}
def fill(src, dst, mode=None):
    t = open(os.path.join(G, src), encoding='utf-8').read()
    for a, v in V.items(): t = t.replace('{{%s}}' % a, v)
    left = sorted(set(re.findall(r'\{\{[A-Z0-9_]+\}\}', t)))
    if left: raise SystemExit('REFUSING: %s keeps unfilled token(s) %s' % (dst, left))
    if '<PR>' in t: raise SystemExit('REFUSING: %s keeps the <PR> placeholder' % dst)
    with open(os.path.join(G, dst), 'w', encoding='utf-8') as f: f.write(t)
    if mode: os.chmod(os.path.join(G, dst), mode)
    print('filled %s (%d bytes, sha256 %s)' % (dst, len(t.encode('utf-8')), hashlib.sha256(t.encode('utf-8')).hexdigest()[:12]))
fill('prompt_gate52.TEMPLATE.txt', K['prompt']); fill('launcher_gate52.TEMPLATE.sh.txt', K['launcher'], 0o755); fill('COMMISSION.TEMPLATE.md', 'COMMISSION.md')
pt = txt(K['prompt'])
missing = [w for w in KW if not re.search(r'(^|[^A-Za-z0-9-])%s([^A-Za-z0-9-]|$)' % re.escape(w), pt)]
if missing: raise SystemExit('REFUSING: the prompt lacks keyword(s) as a token %s' % missing)
print('FILL OK at %s: develop %s | END_TREE_A %s | END_TREE_B %s | 2 rows | %d keywords | #%s %s #%s %s | gate51a report sha256 %s' % (
    now, P['develop'], P['end_tree_a'], P['end_tree_b'], len(KW), NA, S[NA]['head'][:12], NB, S[NB]['head'][:12], prev_sha[:12]))
