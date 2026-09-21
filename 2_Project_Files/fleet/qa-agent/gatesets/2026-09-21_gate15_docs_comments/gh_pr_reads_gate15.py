#!/usr/bin/env python3
"""gh_pr_reads_gate15.py — READ-ONLY GitHub GETs for the Seat B 15th PRs whose READYs are captured (mail_seatB15_ready*_pr<N>_*.md): head sha vs
the READY, base sha == develop 581ed7fa1, files API (name, status, +/-; EVERY path either .md (docs PRs) or under __tests__/ (comment PRs) —
`outside __tests__ and *.md: []` per PR = the tier-2 proof), Refs lines (one per own key; TWO on PR 1 and PR 2), closing-phrase / completeness
detectors with controls, archived / foreign / content keys in title + branch + commit subject (the KS-979 `ks-597s-` excision; the KS-1152 `x5`
fold — no non-ASCII byte in any branch), the compare develop...head (merge_base, ahead, behind, files), ruleset 18499832, the open-PR sweep
against the 11 paths (F2: #920 / #887 also touch DEV-PROCESS.md), and the NAMESPACE trap (PRs numbered like the twelve tickets; the PR numbers
#1136.. as ticket numbers are Linear's side). Never prints a body, never prints the token (GH_TOKEN by NAME from the Secuura .env). Writes
nothing (stdout). Re-runnable. Derived from gatesets/2026-09-21_gate1130to1135/gh_pr_reads_1130.py."""
import glob, json, os, re, urllib.request, urllib.error, sys, subprocess
G = os.path.dirname(os.path.abspath(__file__))
print('date', subprocess.run(['date', '-u', '+%Y-%m-%dT%H:%M:%SZ'], capture_output=True, text=True).stdout.strip())
tok = ''
for l in open('/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env', encoding='utf-8'):
    if l.startswith('GH_TOKEN='): tok = l.split('=', 1)[1].strip().strip('"').strip("'")
assert tok, 'GH_TOKEN unset'
REPO = 'https://api.github.com/repos/Secuura/Distributed_Secuura/'; API = REPO + 'pulls/'
def get(u): return json.load(urllib.request.urlopen(urllib.request.Request(u, headers={'Authorization': 'Bearer ' + tok, 'Accept': 'application/vnd.github+json'}), timeout=60))
CLOSING = re.compile(r'\b(close[sd]?|fix(e[sd])?|resolve[sd]?|complete[sd]?)\s+#?KS-\d+', re.I)
COMPLETE = re.compile(r'\b(complete[sd]?|completeness|fully pins|now complete|closes the ticket|entire scope|all of KS-\d+)\b', re.I)
assert COMPLETE.search('Completes KS-1282') and not COMPLETE.search('pins todays 403 and claims nothing further'), 'completeness detector controls'
assert CLOSING.search('Completes KS-1282') and not CLOSING.search('Whether KS-1282 is now complete') and not CLOSING.search('PREFLIGHT INCOMPLETE — 12/15'), 'closing detector controls'
D = 'Blockchain/Dev/'
KEYS = {'1': ['KS-1035', 'KS-1036'], '2': ['KS-1037', 'KS-1049'], '3': ['KS-1045'], '4': ['KS-1097'], '5': ['KS-890'], '6': ['KS-1140'], '7': ['KS-1152'], '8': ['KS-979'], '9': ['KS-1120'], '10': ['KS-1156']}
FILES = {'1': [D + 'docs/DEV-PROCESS.md'], '2': [D + 'CONTRIBUTING.md'], '3': [D + 'deployment/KINTSUGI-DEV-SERVER-PLAN.md'], '4': ['CLAUDE.md'], '5': [D + 'deployment/DEPLOYMENT-ARCHITECTURE.md'],
         '6': [D + 'packages/shared/src/__tests__/ks879-no-raw-control-bytes-repo-wide.test.ts'],
         '7': [D + 'packages/shared/src/__tests__/ks764-key-revoke-call-site-guard.test.ts', D + 'services/originate/src/__tests__/ks764-admin-api-keys-revoke-route-contract.test.ts'],
         '8': [D + 'services/originate/src/__tests__/ks597-issuer-org-bind.test.ts'], '9': [D + 'services/vc-issuer/src/__tests__/ks1020-presentation-lookup-exact-or-404.test.ts'],
         '10': [D + 'services/api-gateway/src/__tests__/ks835-oauth-token-scope-gate.test.ts']}
PUSH = [str(i) for i in range(1, 11)]
READY = {}
for f in sorted(glob.glob(os.path.join(G, 'mail_seatB15_ready*_pr*_*.md'))):
    if 'CORRECTION' in f: continue
    m = re.search(r'READY FOR QA \(Seat B 15th\): PR (\d+) (KS-\d+)[^\n]*? — #(\d+) at head ([0-9a-f]{40})', open(f, encoding='utf-8').read())
    if m: READY[m.group(1)] = (int(m.group(3)), m.group(4))
PRS = [(READY[p][0], p, KEYS[p], READY[p][1]) for p in PUSH if p in READY]
print('PRs from READYs:', [(n, 'PR ' + p, k) for n, p, k, h in PRS])
DEV = '581ed7fa124b85c7c2da89ac05d52f99c2502911'
ARCHIVED = ['KS-501', 'KS-480', 'KS-978', 'KS-721', 'KS-522', 'KS-726', 'KS-535', 'KS-867', 'KS-878', 'KS-914', 'KS-1238', 'KS-1282', 'KS-1062', 'KS-971', 'KS-1078', 'KS-921', 'KS-490', 'KS-597', 'KS-727']
CONTENT = ['KS-764', 'KS-879', 'KS-1020', 'KS-835', 'KS-869', 'KS-601', 'KS-1044']   # keys the touched files / text name (KS-764 / KS-879 / KS-1020 / KS-835 ARCHIVED per the seat's F3)
FOREIGN = ['KS-973', 'KS-1273', 'KS-958', 'KS-887', 'KS-880', 'KS-1236', 'KS-1006', 'KS-1135', 'KS-957', 'KS-930', 'KS-1260', 'KS-1209', 'KS-1194', 'KS-1118', 'KS-1158', 'KS-1181', 'KS-696', 'KS-961']
SCOPE = {'1': ['withdrawn', 'decayed', '2026-09-15', 'stale'], '2': ['force push', 'preflight', 'NOT RUN', '.githooks/pre-push'], '3': ['az vm show', 'SECUURA-DEMO-RG', 'secuura02-kintsugi-vm', 'Enabled', 'rc 0'],
         '4': ['TESTED', 'step 6', ':303', 'Merge flow'], '5': ['--no-deps', 'migrations'], '6': ['749', '791', '6fd033c36'], '7': ['generateAccessToken', 'jwt.ts'], '8': ['provenance.ts:109'], '9': ['DB path', 'isDbAvailable'], '10': ['seven', 'six', 'proxy.ts', 'stale']}
opens = get(REPO + 'pulls?state=open&per_page=100&sort=created&direction=desc')
print('open PRs listed', len(opens), '| numbers', sorted(p['number'] for p in opens))
MYPATHS = set(); ALLPATHS = {x for v in FILES.values() for x in v}
for n, L, keys, h in PRS:
    p = get(API + str(n)); files = get(API + str(n) + '/files?per_page=100'); commits = get(API + str(n) + '/commits?per_page=100')
    b = p.get('body') or ''; ti = p.get('title') or ''; br = p['head']['ref']
    cm = '\n'.join(c['commit']['message'] for c in commits)
    refs = re.findall(r'^\s*Refs?:?\s+(KS-\d+)\s*$', b, re.M | re.I); crefs = re.findall(r'^\s*Refs?:?\s+(KS-\d+)\s*$', cm, re.M | re.I)
    body_keys = sorted(set(re.findall(r'KS-\d+', b))); subj = cm.splitlines()[0] if cm else ''
    print('#%d PR %s %s head %s (READY ok %s) base %s@%s (== DEV %s) state %s mergeable %s mergeable_state %s commits %d created %s | closing(title/body/commit) %d/%d/%d | completeness(title/body/commit) %d/%d/%d | body Refs lines %s (want %s, own set == %s) | commit Refs lines %s (== %s) | KS keys in title %s | body chars %d | reviews-requested %d'
          % (n, L, '+'.join(keys), p['head']['sha'][:12], p['head']['sha'] == h, p['base']['ref'], p['base']['sha'][:9], p['base']['sha'] == DEV, p['state'], p.get('mergeable'), p.get('mergeable_state'), len(commits), p.get('created_at'),
             len(CLOSING.findall(ti)), len(CLOSING.findall(b)), len(CLOSING.findall(cm)), len(COMPLETE.findall(ti)), len(COMPLETE.findall(b)), len(COMPLETE.findall(cm)),
             refs, keys, sorted(refs) == sorted(keys), crefs, sorted(crefs) == sorted(keys), re.findall(r'KS-\d+', ti, re.I), len(b), len(p.get('requested_reviewers') or [])))
    for m_ in COMPLETE.finditer(b): print('      completeness hit in body: %r' % b[max(0, m_.start() - 60):m_.end() + 40].replace('\n', ' '))
    for m_ in CLOSING.finditer(b): print('      CLOSING hit in body: %r' % b[max(0, m_.start() - 60):m_.end() + 40].replace('\n', ' '))
    print('    title (%d chars, ascii %s): %s' % (len(ti), ti.isascii(), ti)); print('    branch (ascii %s, non-ascii bytes %s): %s' % (br.isascii(), [c for c in br if ord(c) > 127] or 'NONE', br))
    print('    commit subject (%d chars, ascii %s): %s | subject keys %s' % (len(subj), subj.isascii(), subj, re.findall(r'KS-\d+', subj)))
    for f in files: print('    %-8s +%-4d -%-4d %s' % (f['status'], f['additions'], f['deletions'], f['filename'])); MYPATHS.add(f['filename'])
    paths = [f['filename'] for f in files]
    outside = [x for x in paths if '__tests__/' not in x and not x.endswith('.md')]
    print('    files API == GROUPING %s: %s | outside __tests__ and *.md: %s | all .md: %s | all under __tests__/: %s | additions total %d | deletions total %d' % (sorted(FILES[L]), sorted(paths) == sorted(FILES[L]), outside, all(x.endswith('.md') for x in paths), all('__tests__/' in x for x in paths), sum(f['additions'] for f in files), sum(f['deletions'] for f in files)))
    def inkey(k, s): return bool(re.search(re.escape(k) + r'(?!\d)', s, re.I)) or bool(re.search(k.lower().replace('-', '-?') + r'(?!\d)', s.lower()))
    hay = ti + ' ' + subj + ' ' + br
    bad_arch = [k for k in ARCHIVED if inkey(k, hay)]; bad_con = [k for k in CONTENT if inkey(k, hay)]; bad_for = [k for k in FOREIGN if k not in keys and inkey(k, hay)]
    print('    archived keys in title/branch/subject:', bad_arch or 'NONE', '| content keys (file names) in title/branch/subject:', bad_con or 'NONE', '(ks879 in KS-1140 branch is Linear branchName text — the brief keeps it) | foreign keys:', bad_for or 'NONE', '| ks-597 in branch:', 'ks-597' in br, '| x5 in branch:', 'x5' in br)
    print('    body KS keys:', body_keys, '| archived keys in body:', [k for k in ARCHIVED if k in body_keys] or 'NONE', '| foreign keys in body:', [k for k in FOREIGN if k in body_keys and k not in keys] or 'NONE')
    print('    body scope substrings (case-insensitive):', {s: (s.lower() in b.lower()) for s in SCOPE[L]})
    for w in ('INCOMPLETE', '12/15', 'SKIPPED', 'skips are not a pass', 'DOCS-ONLY', 'TEST-FILE-COMMENT-ONLY', 'COMMENT-ONLY', 'Deviation from verbatim', 'mergeable_state', 'NOT RUN', 'NO legs', '--recount', 'run patch', 'fence', 'stale', 'F4', 'F5', 'F8', 'docs-only', 'preflight'):
        c = len(re.findall(re.escape(w), b))
        if c: print('    body carries %r x%d' % (w, c))
    c = get(REPO + 'compare/develop...' + h)
    print('    compare develop...head: merge_base %s ahead %d behind %d files %d' % (c['merge_base_commit']['sha'], c['ahead_by'], c['behind_by'], len(c.get('files') or [])))
print('files API union', len(MYPATHS), sorted(MYPATHS))
rs = get(REPO + 'rulesets/18499832')
print('ruleset 18499832', rs.get('name'), rs.get('enforcement'), 'updated_at', rs.get('updated_at'), '| rules', [r.get('type') for r in rs.get('rules', [])], '| pull_request params', [r.get('parameters') for r in rs.get('rules', []) if r.get('type') == 'pull_request'], '| conditions', rs.get('conditions'))
print('--- open PRs touching any of the ELEVEN paths (F2: the seat named #920 and #887 on DEV-PROCESS.md; read-only)')
mine = {n for n, *_ in PRS}; hits = 0
for p in opens:
    if p['number'] in mine: continue
    try: fl = [f['filename'] for f in get(API + str(p['number']) + '/files?per_page=100')]
    except urllib.error.HTTPError as e: print('  #%d files API HTTP %s' % (p['number'], e.code)); continue
    h1 = sorted(set(fl) & ALLPATHS)
    if h1:
        hits += 1
        print('  #%d %s head %s base %s@%s title %r files %d: ∩ our 11 paths %s' % (p['number'], p['head']['ref'][:60], p['head']['sha'][:9], p['base']['ref'], p['base']['sha'][:9], (p.get('title') or '')[:60], len(fl), h1))
print('  open-PR hits', hits, '| control POSITIVE: merged #721 files ∩ our 11 ->', sorted(set(f['filename'] for f in get(API + '721/files?per_page=100')) & ALLPATHS), '| control NEGATIVE: merged #1130 files ∩ ->', sorted(set(f['filename'] for f in get(API + '1130/files?per_page=100')) & ALLPATHS))
print('--- NAMESPACE trap: PRs numbered like the twelve tickets')
for q in (890, 979, 1035, 1036, 1037, 1045, 1049, 1097, 1120, 1140, 1152, 1156):
    try:
        pq = get(API + str(q)); print('PR #%d exists: state %s title %r head %s' % (q, pq['state'], (pq.get('title') or '')[:70], pq['head']['sha'][:9]))
    except urllib.error.HTTPError as e: print('PR #%d: HTTP %s' % (q, e.code))
    except Exception as e: print('PR #%d: %s' % (q, type(e).__name__))
print('--- the PR numbers of this round as they stand (1136..1147, whatever exists)')
for q in range(1136, 1148):
    try:
        pq = get(API + str(q)); print('PR #%d exists: state %s title %r head %s branch %s' % (q, pq['state'], (pq.get('title') or '')[:70], pq['head']['sha'][:9], pq['head']['ref'][:80]))
    except urllib.error.HTTPError as e: print('PR #%d: HTTP %s' % (q, e.code))
    except Exception as e: print('PR #%d: %s' % (q, type(e).__name__))
