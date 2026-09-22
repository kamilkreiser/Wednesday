#!/usr/bin/env python3
"""gh_pr_reads_gate18C.py — READ-ONLY GitHub GETs for the Seat C 18th six PRs (round18C): head sha vs the READY, base sha == develop 8c2f7b3fd, files
API (name, status, +/-; the changed set == the declared files EXACTLY — test-only rows `outside __tests__: []`, code_patch rows `outside __tests__` ==
the declared PRODUCT set; additions / deletions == the READY's counts), Refs lines (exactly one, the own key), closing-phrase / completeness detectors
with controls, archived / foreign / content keys in title + branch + commit subject (the `ks-733` EXCISION on #1167's branch; the ruled
`-r16-settingsdefaults-1` tail on #1175; the hyphenated-key SCANNER `re.findall(r'ks-\\d+')` on all six names + the withdrawn `threehunks` control), the
compare develop...head (merge_base, ahead, behind, files), ruleset 18499832, the open-PR sweep against the 10 paths + the 2 tamper files (Seat B 18th's
seven open PRs named), Seat B 18th's SEVEN PRs (head, base = 3916eacd1 — BEFORE the #1036 squash, so its compare against 8c2f7b3fd reads behind 1 —
author, created_at, head ref namespace `feature/ks-<key>-…-r1[68]-…-1`, files ∩ our 10 paths / 2 tamper files), the PR-number NAMESPACE trap (PRs
numbered like the own tickets: #947 #1123 #1192 #1231 #1246 #1257), the window 1167..1180, the merged #1036 (KS-763) files ∩ our paths (the base-move
non-event), positive controls from `git log -- <path>` (the last merged PR that touched index.ts / verification.ts / admin.ts / health.ts — read
verbs only). Never prints a body, never prints the token (GH_TOKEN by NAME from the Secuura .env). Writes nothing (stdout). Re-runnable. Derived
from gatesets/2026-09-22_gate16C_seatC/gh_pr_reads_gate16C.py."""
import glob, json, os, re, urllib.request, urllib.error, sys, subprocess
G = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, G); import round18C as R
print('date', subprocess.run(['date', '-u', '+%Y-%m-%dT%H:%M:%SZ'], capture_output=True, text=True).stdout.strip())
tok = ''
for l in open('/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env', encoding='utf-8'):
    if l.startswith('GH_TOKEN='): tok = l.split('=', 1)[1].strip().strip('"').strip("'")
assert tok, 'GH_TOKEN unset'
REPO = 'https://api.github.com/repos/Secuura/Distributed_Secuura/'; API = REPO + 'pulls/'
def get(u): return json.load(urllib.request.urlopen(urllib.request.Request(u, headers={'Authorization': 'Bearer ' + tok, 'Accept': 'application/vnd.github+json'}), timeout=60))
def lgit(*a): return subprocess.run(['git', '-C', R.REPO] + list(a), capture_output=True, text=True).stdout.strip()
CLOSING = re.compile(r'\b(close[sd]?|fix(e[sd])?|resolve[sd]?|complete[sd]?)\s+#?KS-\d+', re.I)
COMPLETE = re.compile(r'\b(complete[sd]?|completeness|fully pins|now complete|closes the ticket|entire scope|all of KS-\d+)\b', re.I)
assert COMPLETE.search('Completes KS-1282') and not COMPLETE.search('pins todays 403 and claims nothing further'), 'completeness detector controls'
assert CLOSING.search('Completes KS-1282') and not CLOSING.search('Whether KS-1282 is now complete') and not CLOSING.search('PREFLIGHT INCOMPLETE — 12/15'), 'closing detector controls'
SCAN = re.compile(r'ks-\d+')
assert SCAN.findall('feature/ks-1257-after-platform-settings-has-expired-a-partial-admin-write-r16-threehunks-1') == ['ks-1257', 'ks-1'], 'scanner control (the withdrawn tail reads ks-1)'
READY = {}
for f in sorted(glob.glob(os.path.join(G, 'mail_seatC18_ready*_pr*_*.md'))):
    if 'CORRECTION' in f: continue
    m = re.search(R.ready_regex(), open(f, encoding='utf-8').read())
    if m: READY[m.group(1)] = (int(m.group(3)), m.group(4))
PRS = [(READY[p][0], p, R.PRS[p]['key'], READY[p][1]) for p in R.PUSH if p in READY]
print('PRs from READYs:', [(n, 'PR ' + p, k) for n, p, k, h in PRS])
FOREIGN = R.SEATB_KEYS + ['KS-763', 'KS-775', 'KS-1201', 'KS-256', 'KS-485', 'KS-772', 'KS-1230', 'KS-871', 'KS-1227', 'KS-1185', 'KS-1072', 'KS-999']
opens = get(REPO + 'pulls?state=open&per_page=100&sort=created&direction=desc')
print('open PRs listed', len(opens), '| numbers', sorted(p['number'] for p in opens))
MYPATHS = set(); ALLPATHS = set(R.all_paths()); TAMPERS = {x[0] for x in R.TAMPER_BLOBS}
for n, L, key, h in PRS:
    pr = R.PRS[L]; want_paths = sorted(f['path'] for f in pr['files']); prod = sorted(f['path'] for f in pr['files'] if f['kind'] == 'product')
    p = get(API + str(n)); files = get(API + str(n) + '/files?per_page=100'); commits = get(API + str(n) + '/commits?per_page=100')
    b = p.get('body') or ''; ti = p.get('title') or ''; br = p['head']['ref']
    cm = '\n'.join(c['commit']['message'] for c in commits)
    refs = re.findall(r'^\s*Refs?:?\s+(KS-\d+)\s*$', b, re.M | re.I); crefs = re.findall(r'^\s*Refs?:?\s+(KS-\d+)\s*$', cm, re.M | re.I)
    body_keys = sorted(set(re.findall(r'KS-\d+', b))); subj = cm.splitlines()[0] if cm else ''
    print('#%d PR %s %s %s head %s (READY ok %s; round18C ok %s) base %s@%s (== DEV %s) state %s mergeable %s mergeable_state %s commits %d created %s author %s | closing(title/body/commit) %d/%d/%d | completeness(title/body/commit) %d/%d/%d | body Refs lines %s (want [%s], == %s) | commit Refs lines %s (== %s) | KS keys in title %s | body chars %d | reviews-requested %d'
          % (n, L, key, pr['kind'], p['head']['sha'][:12], p['head']['sha'] == h, p['head']['sha'] == pr['head'], p['base']['ref'], p['base']['sha'][:9], p['base']['sha'] == R.DEV, p['state'], p.get('mergeable'), p.get('mergeable_state'), len(commits), p.get('created_at'), (p.get('user') or {}).get('login'),
             len(CLOSING.findall(ti)), len(CLOSING.findall(b)), len(CLOSING.findall(cm)), len(COMPLETE.findall(ti)), len(COMPLETE.findall(b)), len(COMPLETE.findall(cm)),
             refs, key, refs == [key], crefs, crefs == [key], re.findall(r'KS-\d+', ti, re.I), len(b), len(p.get('requested_reviewers') or [])))
    for m_ in COMPLETE.finditer(b): print('      completeness hit in body: %r' % b[max(0, m_.start() - 60):m_.end() + 40].replace('\n', ' '))
    for m_ in CLOSING.finditer(b): print('      CLOSING hit in body: %r' % b[max(0, m_.start() - 60):m_.end() + 40].replace('\n', ' '))
    print('    title (%d chars, ascii %s) == round18C: %s | %s' % (len(ti), ti.isascii(), ti == pr['title'], ti)); print('    branch (ascii %s, non-ascii bytes %s, %d chars) == round18C: %s | scanner ks-N (not own): %s | tail: %s' % (br.isascii(), [c for c in br if ord(c) > 127] or 'NONE', len(br), 'refs/heads/' + br == pr['branch'], [x for x in SCAN.findall(br) if x != key.lower()] or 'NONE', br.rsplit('-r16-', 1)[-1] if '-r16-' in br else '?'))
    print('    commit subject (%d chars, ascii %s, <= 92: %s): %s | subject keys %s' % (len(subj), subj.isascii(), len(subj) <= 92, subj, re.findall(r'KS-\d+', subj)))
    for f in files: print('    %-8s +%-4d -%-4d %s' % (f['status'], f['additions'], f['deletions'], f['filename'])); MYPATHS.add(f['filename'])
    paths = sorted(f['filename'] for f in files); outside = sorted(x for x in paths if '__tests__/' not in x)
    print('    files API == round18C %s: %s | outside __tests__: %s == the declared PRODUCT set %s: %s | nothing under services/auth/: %s | additions total %d (want %d) | deletions total %d (want %d) | status %s' % ([x.split('/')[-1] for x in want_paths], paths == want_paths, [x.split('/')[-1] for x in outside], [x.split('/')[-1] for x in prod], outside == prod, not any(x.startswith(R.AU) for x in paths), sum(f['additions'] for f in files), pr['adds'], sum(f['deletions'] for f in files), pr['dels'], sorted(f['status'] for f in files)))
    def inkey(k, s): return bool(re.search(re.escape(k) + r'(?!\d)', s, re.I)) or bool(re.search(k.lower().replace('-', '-?') + r'(?!\d)', s.lower()))
    hay = ti + ' ' + subj + ' ' + br
    bad_arch = [k for k in R.ARCHIVED if inkey(k, hay)]; bad_con = [k for k in R.CONTENT_LIVE if inkey(k, hay)]; bad_for = [k for k in FOREIGN if k != key and inkey(k, hay)]
    print('    archived keys in title/branch/subject:', bad_arch or 'NONE', '| live content keys in title/branch/subject (the hyphenless file-name / branch forms ks871 / ks1230 / ks733 are CONTENT, the brief):', bad_con or 'NONE', '| foreign keys:', bad_for or 'NONE', '| excised %s in branch: %s' % (pr['excised'], ((pr['excised'] + '-') in br) if pr['excised'] else 'n/a'))
    print('    body KS keys:', body_keys, '| archived keys in body:', [k for k in R.ARCHIVED if k in body_keys] or 'NONE', '| foreign keys in body (not own):', [k for k in FOREIGN if k in body_keys and k != key] or 'NONE', '| own key in body:', key in body_keys)
    for w in ('INCOMPLETE', '12/15', 'SKIPPED', 'skips are not a pass', 'TEST-FILE-ONLY', 'PRODUCT BYTES', 'code_patch', 'RED-FIRST', 'GREEN-AFTER', 'A4', 'A5', '--pair-blob', 'PAIR blob', 'ae6017a84cf7', '--recount --ignore-whitespace', 'strict', 'DEVELOP COVER', 'cover-aware', 'lock', 'LOCK TAKEN', 'LOCK RELEASED', 'PROTOCOL-CLEAN', 'stubs=4', 'mergeable_state', 'typecheck18', 'TS2322', 'TS18046', 'netlog', ':5432', 'anchoring:4005', 'localhost:6000', 'UNVERIFIED', 'tier 1', 'tier 2', 'EXCISED', 'anchor-ambiguity', '45 passed', 'no-useless-assignment', '#1036', 'KS-763', 'settingsdefaults', 'threehunks', 'ks-1'):
        c = len(re.findall(re.escape(w), b))
        if c: print('    body carries %r x%d' % (w, c))
    c = get(REPO + 'compare/develop...' + h)
    print('    compare develop...head: merge_base %s ahead %d behind %d files %d' % (c['merge_base_commit']['sha'], c['ahead_by'], c['behind_by'], len(c.get('files') or [])))
print('files API union', len(MYPATHS), '(want 10)', sorted(x.split('/')[-1] for x in MYPATHS))
rs = get(REPO + 'rulesets/18499832')
print('ruleset 18499832', rs.get('name'), rs.get('enforcement'), 'updated_at', rs.get('updated_at'), '| rules', [r.get('type') for r in rs.get('rules', [])], '| pull_request params', [r.get('parameters') for r in rs.get('rules', []) if r.get('type') == 'pull_request'], '| conditions', rs.get('conditions'))
print('--- the merged #1036 (KS-763; the base move 3916eacd1 -> 8c2f7b3fd): state, merge_commit_sha == develop, files ∩ our 10 / our 2 tamper files')
p36 = get(API + '1036'); f36 = [f['filename'] for f in get(API + '1036/files?per_page=100')]
print('  #1036 state %s merged %s merge_commit_sha %s == DEV %s | head %s == round18C %s | files %d (seat: 50) | ∩ our 10: %s | ∩ our 2 tamper files: %s | locks %d manifests %d audit-baseline %d' % (p36['state'], p36.get('merged'), (p36.get('merge_commit_sha') or '?')[:9], p36.get('merge_commit_sha') == R.DEV, p36['head']['sha'][:9], p36['head']['sha'] == R.PR1036_HEAD, len(f36), sorted(set(f36) & ALLPATHS) or 'NONE', sorted(set(f36) & TAMPERS) or 'NONE', sum(1 for x in f36 if x.endswith('package-lock.json')), sum(1 for x in f36 if x.endswith('package.json')), sum(1 for x in f36 if x.endswith('audit-baseline.json'))))
print('--- Seat B 18th PRs (SEVEN; the other seat on the same .git; its READYs + HOLD captured beside): head / base / author / created / head-ref namespace / files')
mine = {n for n, *_ in PRS}; bpaths = set()
for bn, bk, bh, bf in R.SEATB:
    try:
        pb = get(API + bn); fl = [f['filename'] for f in get(API + bn + '/files?per_page=100')]; bpaths |= set(fl)
        ns_ok = bool(re.match(r'^feature/ks-%s-.*-r1[68]-.*-1$' % bk.split('-')[1], pb['head']['ref']))
        cb = get(REPO + 'compare/develop...' + pb['head']['sha'])
        print('  #%s %s head %s (== captured READY %s) base %s@%s (== 3916eacd1: %s) state %s author %s created %s | head ref %s | namespace `feature/ks-%s-…-r16|r18-…-1`: %s | scanner (not own) %s | files %s == captured %s | ∩ our 10 paths %s | ∩ our 2 tamper files %s | compare develop...head merge_base %s ahead %d behind %d files %d' % (
            bn, bk, pb['head']['sha'][:9], pb['head']['sha'] == bh, pb['base']['ref'], pb['base']['sha'][:9], pb['base']['sha'] == R.DEV_PRE1036, pb['state'], (pb.get('user') or {}).get('login'), pb.get('created_at'), pb['head']['ref'][:75], bk.split('-')[1], ns_ok, [x for x in SCAN.findall(pb['head']['ref']) if x != bk.lower()] or 'NONE', [x.split('/')[-1] for x in fl], sorted(fl) == sorted(bf), sorted(set(fl) & ALLPATHS) or 'NONE', sorted(set(fl) & TAMPERS) or 'NONE', cb['merge_base_commit']['sha'][:9], cb['ahead_by'], cb['behind_by'], len(cb.get('files') or [])))
    except urllib.error.HTTPError as e: print('  #%s HTTP %s' % (bn, e.code))
print('  Seat B pushed paths', len(bpaths), '(seat: 9) ∩ our 10:', sorted(bpaths & ALLPATHS) or 'NONE', '| ∩ our 2 tamper files:', sorted(bpaths & TAMPERS) or 'NONE', '| every Seat B path under its dirs (originate / anchoring / auth / packages/shared):', all(any(x.startswith(d) for d in R.SEATB_DIRS) for x in bpaths), '| any under api-gateway:', sorted(x for x in bpaths if x.startswith(R.AG)) or 'NONE')
print('--- open PRs touching any of the TEN paths or the TWO tamper files (read-only; Seat B\'s PRs named)')
hits = 0
for p in opens:
    if p['number'] in mine: continue
    try: fl = [f['filename'] for f in get(API + str(p['number']) + '/files?per_page=100')]
    except urllib.error.HTTPError as e: print('  #%d files API HTTP %s' % (p['number'], e.code)); continue
    h1 = sorted(set(fl) & ALLPATHS); h2 = sorted(set(fl) & TAMPERS)
    if h1 or h2:
        hits += 1
        print('  #%d %s head %s base %s@%s title %r files %d: ∩ our 10 paths %s | ∩ our 2 tamper files %s' % (p['number'], p['head']['ref'][:60], p['head']['sha'][:9], p['base']['ref'], p['base']['sha'][:9], (p.get('title') or '')[:60], len(fl), [x.split('/')[-1] for x in h1], [x.split('/')[-1] for x in h2]))
print('  open-PR hits', hits)
print('--- controls for the sweep: the LAST merged PR that touched each product path (git log --format=%s -1 <develop> -- <path>, read verb) and its files API ∩ our sets')
for path in (R.AG + 'src/index.ts', R.AG + 'src/routes/verification.ts', R.AG + 'src/routes/admin.ts', R.AG + 'src/services/health.ts', R.AG + 'src/__tests__/ks733-users-mfa-rate-limit-mount.test.ts', R.AG + 'src/__tests__/ks1230-settings-write-validates-allowed-document-types.test.ts'):
    subj = lgit('log', '--format=%s', '-1', R.DEV, '--', path); m = re.search(r'\(#(\d+)\)\s*$', subj)
    if not m: print('  %-70s last subject %r (no PR number in it)' % (path.split('/')[-1], subj[:80])); continue
    try:
        fl = [f['filename'] for f in get(API + m.group(1) + '/files?per_page=100')]
        print('  %-70s last touched by merged #%s (%r): its files ∩ our 10 -> %s | ∩ our 2 tamper files -> %s (POSITIVE control: the path itself must appear in one of the two)' % (path.split('/')[-1], m.group(1), subj[:60], [x.split('/')[-1] for x in sorted(set(fl) & ALLPATHS)], [x.split('/')[-1] for x in sorted(set(fl) & TAMPERS)]))
    except urllib.error.HTTPError as e: print('  %-70s merged #%s files API HTTP %s' % (path.split('/')[-1], m.group(1), e.code))
print('  NEGATIVE control: merged #1166 (KS-910, scripts) files ∩ our 10 ->', sorted(set(f['filename'] for f in get(API + '1166/files?per_page=100')) & ALLPATHS), '| merged #1002 (KS-1123 earlier) files ∩ our 10 ->', sorted(set(f['filename'] for f in get(API + '1002/files?per_page=100')) & ALLPATHS), '| ∩ our 2 tamper files ->', [x.split('/')[-1] for x in sorted(set(f['filename'] for f in get(API + '1002/files?per_page=100')) & TAMPERS)])
print('--- NAMESPACE trap: PRs numbered like the own tickets')
for q in (947, 1123, 1192, 1231, 1246, 1257):
    try:
        pq = get(API + str(q)); print('PR #%d exists: state %s title %r head %s' % (q, pq['state'], (pq.get('title') or '')[:70], pq['head']['sha'][:9]))
    except urllib.error.HTTPError as e: print('PR #%d: HTTP %s' % (q, e.code))
    except Exception as e: print('PR #%d: %s' % (q, type(e).__name__))
print('--- the PR numbers of this round\'s window as they stand (1167..1181, whatever exists)')
for q in range(1167, 1182):
    try:
        pq = get(API + str(q)); print('PR #%d exists: state %s title %r head %s branch %s author %s created %s base %s' % (q, pq['state'], (pq.get('title') or '')[:60], pq['head']['sha'][:9], pq['head']['ref'][:75], (pq.get('user') or {}).get('login'), pq.get('created_at'), pq['base']['sha'][:9]))
    except urllib.error.HTTPError as e: print('PR #%d: HTTP %s' % (q, e.code))
    except Exception as e: print('PR #%d: %s' % (q, type(e).__name__))
print('done', subprocess.run(['date', '-u', '+%Y-%m-%dT%H:%M:%SZ'], capture_output=True, text=True).stdout.strip())
