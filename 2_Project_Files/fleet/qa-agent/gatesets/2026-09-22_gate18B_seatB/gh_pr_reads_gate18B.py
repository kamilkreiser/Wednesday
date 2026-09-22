#!/usr/bin/env python3
"""gh_pr_reads_gate18B.py — READ-ONLY GitHub GETs for the Seat B 18th PRs (round18B): head sha vs the READY, base sha (develop at the PR's open;
the seat's commits' parent is 3916eacd1 — the compare develop...head reads merge_base 3916eacd1 / ahead 1 / BEHIND 1 (the #1036 squash) / files),
the files API (name, status, +/-; every path under __tests__/ EXCEPT the ONE product path documents.ts on #1174 — `outside __tests__` per PR = the
test-file-only / product-bytes proof; additions == the READY's `+` count), Refs lines (exactly one, the own key), closing-phrase / completeness
detectors with controls, archived / foreign / content keys in title + branch + commit subject, the ruleset 18499832, the open-PR sweep against the 9
paths + the 4 tamper files (Seat C 18th's open PRs named), Seat C 18th's six PRs (head, author, created_at, head ref namespace `-r16-…-1` — the
four-condition attribution rule's inputs; the ks-1257 tail as ruled), the PR-number NAMESPACE trap (PRs numbered like the own tickets: #811 #1118
#1158 #1171 #1181 #1188 #1265), the window #1167..#1180 as it stands. Never prints a body, never prints the token (GH_TOKEN by NAME from the
Secuura .env). Writes nothing (stdout). Re-runnable. Derived from gatesets/2026-09-22_gate16B_seatB/gh_pr_reads_gate16B.py."""
import glob, json, os, re, urllib.request, urllib.error, sys, subprocess
G = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, G); import round18B as R
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
READY = {}
for f in sorted(glob.glob(os.path.join(G, 'mail_seatB18_ready*_pr*_*.md'))):
    if 'CORRECTION' in f: continue
    m = re.search(R.ready_regex(), open(f, encoding='utf-8').read())
    if m: READY[m.group(1)] = (int(m.group(3)), m.group(4))
PRS = [(READY[p][0], p, R.PRS[p]['key'], READY[p][1]) for p in R.PUSH if p in READY]
print('PRs from READYs:', [(n, 'PR ' + p, k) for n, p, k, h in PRS])
FOREIGN = R.SEATC_KEYS + [R.DEFERRED, 'KS-1004', 'KS-1201', 'KS-256', 'KS-1287', 'KS-696', 'KS-485', 'KS-772', 'KS-795']
opens = get(REPO + 'pulls?state=open&per_page=100&sort=created&direction=desc')
print('open PRs listed', len(opens), '| numbers', sorted(p['number'] for p in opens))
MYPATHS = set(); ALLPATHS = set(R.all_paths()); TAMPERS = {x[0] for x in R.TAMPER_BLOBS}; PRODUCT = set(R.product_paths())
for n, L, key, h in PRS:
    pr = R.PRS[L]
    p = get(API + str(n)); files = get(API + str(n) + '/files?per_page=100'); commits = get(API + str(n) + '/commits?per_page=100')
    b = p.get('body') or ''; ti = p.get('title') or ''; br = p['head']['ref']
    cm = '\n'.join(c['commit']['message'] for c in commits)
    refs = re.findall(r'^\s*Refs?:?\s+(KS-\d+)\s*$', b, re.M | re.I); crefs = re.findall(r'^\s*Refs?:?\s+(KS-\d+)\s*$', cm, re.M | re.I)
    body_keys = sorted(set(re.findall(r'KS-\d+', b))); subj = cm.splitlines()[0] if cm else ''
    print('#%d PR %s %s %s head %s (READY ok %s; round18B ok %s) base %s@%s (== DEV 8c2f7b3fd %s; == PARENT 3916eacd1 %s) state %s mergeable %s mergeable_state %s commits %d created %s author %s | closing(title/body/commit) %d/%d/%d | completeness(title/body/commit) %d/%d/%d | body Refs lines %s (want [%s], == %s) | commit Refs lines %s (== %s) | KS keys in title %s | body chars %d | reviews-requested %d'
          % (n, L, key, pr['kind'], p['head']['sha'][:12], p['head']['sha'] == h, p['head']['sha'] == pr['head'], p['base']['ref'], p['base']['sha'][:9], p['base']['sha'] == R.DEV, p['base']['sha'] == R.PARENT, p['state'], p.get('mergeable'), p.get('mergeable_state'), len(commits), p.get('created_at'), (p.get('user') or {}).get('login'),
             len(CLOSING.findall(ti)), len(CLOSING.findall(b)), len(CLOSING.findall(cm)), len(COMPLETE.findall(ti)), len(COMPLETE.findall(b)), len(COMPLETE.findall(cm)),
             refs, key, refs == [key], crefs, crefs == [key], re.findall(r'KS-\d+', ti, re.I), len(b), len(p.get('requested_reviewers') or [])))
    for m_ in COMPLETE.finditer(b): print('      completeness hit in body: %r' % b[max(0, m_.start() - 60):m_.end() + 40].replace('\n', ' '))
    for m_ in CLOSING.finditer(b): print('      CLOSING hit in body: %r' % b[max(0, m_.start() - 60):m_.end() + 40].replace('\n', ' '))
    print('    title (%d chars, ascii %s) == round18B: %s | %s' % (len(ti), ti.isascii(), ti == pr['title'], ti)); print('    branch (ascii %s, non-ascii bytes %s, %d chars) == round18B: %s | scanner ks-\\d+ -> %s' % (br.isascii(), [c for c in br if ord(c) > 127] or 'NONE', len(br), 'refs/heads/' + br == pr['branch'], re.findall(r'ks-\d+', br)))
    print('    commit subject (%d chars, ascii %s): %s | subject keys %s | == round18B title: %s' % (len(subj), subj.isascii(), subj, re.findall(r'KS-\d+', subj), subj == pr['title']))
    for f in files: print('    %-8s +%-4d -%-4d %s' % (f['status'], f['additions'], f['deletions'], f['filename'])); MYPATHS.add(f['filename'])
    paths = [f['filename'] for f in files]; outside = [x for x in paths if '__tests__/' not in x]; want = sorted(fl['path'] for fl in pr['files']); wprod = sorted(fl['path'] for fl in pr['files'] if fl['kind'] == 'product')
    print('    files API == round18B %s: %s | outside __tests__: %s == the declared PRODUCT set %s: %s | additions total %d (want %d) | deletions total %d (want %d) | status %s | per-file +/- == pin: %s' % (
        [x.split('/')[-1] for x in want], sorted(paths) == want, [x.split('/')[-1] for x in outside], [x.split('/')[-1] for x in wprod], sorted(outside) == wprod, sum(f['additions'] for f in files), pr['adds'], sum(f['deletions'] for f in files), pr['dels'], [f['status'] for f in files],
        all((f['additions'], f['deletions']) == next((fl['adds'], fl['dels']) for fl in pr['files'] if fl['path'] == f['filename']) for f in files)))
    def inkey(k, s): return bool(re.search(re.escape(k) + r'(?!\d)', s, re.I)) or bool(re.search(k.lower().replace('-', '-?') + r'(?!\d)', s.lower()))
    hay = ti + ' ' + subj + ' ' + br
    bad_arch = [k for k in R.ARCHIVED if inkey(k, hay)]; bad_con = [k for k in R.CONTENT_LIVE if inkey(k, hay)]; bad_for = [k for k in FOREIGN if k != key and inkey(k, hay)]
    print('    archived keys in title/branch/subject:', bad_arch or 'NONE', '| live content keys in title/branch/subject:', bad_con or 'NONE', '| foreign keys:', bad_for or 'NONE', '| excised token %r in branch: %s | archived file-name tokens in the files API paths: %s' % (pr['excised'], (pr['excised'] + '-') in br if pr['excised'] else 'n/a', [t for t in ('ks727', 'ks549', 'ks1058', 'ks1103') if any(t in x for x in paths)] or 'NONE'))
    print('    body KS keys:', body_keys, '| archived keys in body:', [k for k in R.ARCHIVED if k in body_keys] or 'NONE', '| foreign keys in body (not own):', [k for k in FOREIGN if k in body_keys and k != key] or 'NONE', '| own key in body:', key in body_keys, '| sibling own keys in body (S4):', [k for k in R.OWN if k in body_keys and k != key] or 'NONE')
    for w in ('INCOMPLETE', '12/15', 'SKIPPED', 'skips are not a pass', 'TEST-FILE-ONLY', 'COMMENT-ONLY', 'CODE_PATCH', 'strict', 'cover', 'lock', 'started_utc', 'released', 'PROTOCOL-CLEAN', 'stubs=4', 'mergeable_state', 'typecheck', 'TS2322', 'TS1378', 'netlog', ':5432', 'anchoring:4005', 'threadTokenMint', 'A4', 'A5', 'tier 1', 'tier 2', 'AUTH', 'LANE COUNTS', 'bare', 'preload', 'ks795', 'QUARANTINE', 'F9'):
        c = len(re.findall(re.escape(w), b))
        if c: print('    body carries %r x%d' % (w, c))
    c = get(REPO + 'compare/develop...' + h)
    print('    compare develop...head: merge_base %s (== PARENT %s) ahead %d behind %d files %d' % (c['merge_base_commit']['sha'], c['merge_base_commit']['sha'] == R.PARENT, c['ahead_by'], c['behind_by'], len(c.get('files') or [])))
print('files API union', len(MYPATHS), '(want 9)', sorted(x.split('/')[-1] for x in MYPATHS), '| product paths in the union:', sorted(x.split('/')[-1] for x in MYPATHS if '__tests__/' not in x))
rs = get(REPO + 'rulesets/18499832')
print('ruleset 18499832', rs.get('name'), rs.get('enforcement'), 'updated_at', rs.get('updated_at'), '| rules', [r.get('type') for r in rs.get('rules', [])], '| pull_request params', [r.get('parameters') for r in rs.get('rules', []) if r.get('type') == 'pull_request'], '| conditions', rs.get('conditions'))
print('--- the #1036 squash on develop (the move between the seat parent and develop)')
try:
    p36 = get(API + '1036'); print('  #1036 state %s merged %s merged_at %s merge_commit_sha %s (== DEV %s) head %s (== round18B %s) title %r' % (p36['state'], p36.get('merged'), p36.get('merged_at'), (p36.get('merge_commit_sha') or '?')[:12], p36.get('merge_commit_sha') == R.DEV, p36['head']['sha'][:12], p36['head']['sha'] == R.PR1036_HEAD, (p36.get('title') or '')[:80]))
    f36 = [f['filename'] for f in get(API + '1036/files?per_page=100')]; print('  #1036 files API: %d paths | ∩ our 9: %s | ∩ our 4 tamper files: %s | non-manifest paths: %s' % (len(f36), sorted(set(f36) & ALLPATHS) or 'NONE', sorted(set(f36) & TAMPERS) or 'NONE', [x for x in f36 if not x.endswith('package.json') and not x.endswith('package-lock.json')]))
except urllib.error.HTTPError as e: print('  #1036 HTTP %s' % e.code)
print('--- Seat C 18th PRs (the other seat on the same .git; its READYs captured beside): head / author / created / head-ref namespace / files')
mine = {n for n, *_ in PRS}; cpaths = set()
for cn, ck, ch, cf in R.SEATC:
    try:
        pc = get(API + cn); fl = [f['filename'] for f in get(API + cn + '/files?per_page=100')]; cpaths |= set(fl)
        ns_ok = bool(re.match(r'^feature/ks-%s-.*-r16-.*-1$' % ck.split('-')[1], pc['head']['ref']))
        print('  #%s %s head %s (== READY %s) base %s@%s (== DEV %s) state %s author %s created %s | head ref %s | namespace `feature/ks-%s-…-r16-…-1`: %s | scanner %s | files %s == READY paths: %s | ∩ our 9 paths %s | ∩ our 4 tamper files %s' % (
            cn, ck, pc['head']['sha'][:9], pc['head']['sha'] == ch, pc['base']['ref'], pc['base']['sha'][:9], pc['base']['sha'] == R.DEV, pc['state'], (pc.get('user') or {}).get('login'), pc.get('created_at'), pc['head']['ref'][:70], ck.split('-')[1], ns_ok, re.findall(r'ks-\d+', pc['head']['ref']), [x.split('/')[-1] for x in fl], sorted(fl) == sorted(set(cf)), sorted(set(fl) & ALLPATHS) or 'NONE', sorted(set(fl) & TAMPERS) or 'NONE'))
    except urllib.error.HTTPError as e: print('  #%s HTTP %s' % (cn, e.code))
print('  Seat C pushed paths (%d distinct) ∩ our 9:' % len(cpaths), sorted(cpaths & ALLPATHS) or 'NONE', '| ∩ our 4 tamper files:', sorted(cpaths & TAMPERS) or 'NONE', '| every Seat C path under api-gateway:', all(x.startswith(R.AG) for x in cpaths), '| our 9 paths ∪ 4 tamper files under api-gateway:', [x for x in ALLPATHS | TAMPERS if x.startswith(R.AG)] or 'NONE')
print('--- open PRs touching any of the NINE paths or the FOUR tamper files (read-only; Seat C\'s PRs named)')
hits = 0
for p in opens:
    if p['number'] in mine: continue
    try: fl = [f['filename'] for f in get(API + str(p['number']) + '/files?per_page=100')]
    except urllib.error.HTTPError as e: print('  #%d files API HTTP %s' % (p['number'], e.code)); continue
    h1 = sorted(set(fl) & ALLPATHS); h2 = sorted(set(fl) & TAMPERS)
    if h1 or h2:
        hits += 1
        print('  #%d %s head %s base %s@%s title %r files %d: ∩ our 9 paths %s | ∩ our 4 tamper files %s' % (p['number'], p['head']['ref'][:60], p['head']['sha'][:9], p['base']['ref'], p['base']['sha'][:9], (p.get('title') or '')[:60], len(fl), h1, h2))
print('  open-PR hits', hits, '| control POSITIVE: merged #1163 files ∩ our 9 paths + tamper files ->', sorted(set(f['filename'] for f in get(API + '1163/files?per_page=100')) & (ALLPATHS | TAMPERS)), '(want []: the earlier KS-1188 PR touched three OTHER auth test files) | control POSITIVE 2: merged #1159 (the KS-1181 F3 pin) ∩ our 9 ->', sorted(set(f['filename'] for f in get(API + '1159/files?per_page=100')) & ALLPATHS), '| control NEGATIVE: merged #1146 ∩ our 9 ->', sorted(set(f['filename'] for f in get(API + '1146/files?per_page=100')) & ALLPATHS))
print('  the prior PRs the tickets carry (merged): #1149 KS-1118 files', [f['filename'].split('/')[-1] for f in get(API + '1149/files?per_page=100')], '| #1153 KS-1158', [f['filename'].split('/')[-1] for f in get(API + '1153/files?per_page=100')], '| #1159 KS-1181', [f['filename'].split('/')[-1] for f in get(API + '1159/files?per_page=100')], '| #1163 KS-1188', [f['filename'].split('/')[-1] for f in get(API + '1163/files?per_page=100')])
print('--- NAMESPACE trap: PRs numbered like the own tickets')
for q in (811, 1118, 1158, 1171, 1181, 1188, 1265, 815):
    try:
        pq = get(API + str(q)); print('PR #%d exists: state %s title %r head %s' % (q, pq['state'], (pq.get('title') or '')[:70], pq['head']['sha'][:9]))
    except urllib.error.HTTPError as e: print('PR #%d: HTTP %s' % (q, e.code))
    except Exception as e: print('PR #%d: %s' % (q, type(e).__name__))
print('--- the PR numbers of this round\'s window as they stand (1167..1181, whatever exists)')
for q in range(1167, 1182):
    try:
        pq = get(API + str(q)); print('PR #%d exists: state %s title %r head %s branch %s author %s created %s' % (q, pq['state'], (pq.get('title') or '')[:60], pq['head']['sha'][:9], pq['head']['ref'][:70], (pq.get('user') or {}).get('login'), pq.get('created_at')))
    except urllib.error.HTTPError as e: print('PR #%d: HTTP %s' % (q, e.code))
    except Exception as e: print('PR #%d: %s' % (q, type(e).__name__))
