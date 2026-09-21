#!/usr/bin/env python3
"""gh_pr_reads_gate16B.py — READ-ONLY GitHub GETs for the Seat B 16th PRs (round16B): head sha vs the READY, base sha == develop 64ab10513, files API
(name, status, +/-; EVERY path under __tests__/ — `outside __tests__: []` per PR = the test-file-only proof; additions == the READY's `+` count), Refs
lines (exactly one, the own key), closing-phrase / completeness detectors with controls, archived / foreign / content keys in title + branch + commit
subject (the KS-1181 `ks-727` excision — the FILE NAME carries it as a PATH), the compare develop...head (merge_base, ahead, behind, files), ruleset
18499832, the open-PR sweep against the 8 paths + the 9 tamper files (Seat C 16th's open PRs named), Seat C 16th's PRs (head, author, created_at,
head ref namespace — the four-condition attribution rule's inputs), the PR-number NAMESPACE trap (PRs numbered like the own tickets: #928 #975
#1118 #1133 #1158 #1171 #1179 #1181 … and #1229 if it exists). Never prints a body, never prints the token (GH_TOKEN by NAME from the Secuura .env).
Writes nothing (stdout). Re-runnable. Derived from gatesets/2026-09-21_gate15_docs_comments/gh_pr_reads_gate15.py."""
import glob, json, os, re, urllib.request, urllib.error, sys, subprocess
G = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, G); import round16B as R
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
for f in sorted(glob.glob(os.path.join(G, 'mail_seatB16_ready*_pr*_*.md'))):
    if 'CORRECTION' in f: continue
    m = re.search(R.ready_regex(), open(f, encoding='utf-8').read())
    if m: READY[m.group(1)] = (int(m.group(3)), m.group(4))
PRS = [(READY[p][0], p, R.PRS[p]['key'], READY[p][1]) for p in R.PUSH if p in READY]
print('PRs from READYs:', [(n, 'PR ' + p, k) for n, p, k, h in PRS])
FOREIGN = R.SEATC_KEYS + ['KS-1171', 'KS-1004', 'KS-1201', 'KS-256', 'KS-1287', 'KS-1286', 'KS-696', 'KS-485', 'KS-772']
opens = get(REPO + 'pulls?state=open&per_page=100&sort=created&direction=desc')
print('open PRs listed', len(opens), '| numbers', sorted(p['number'] for p in opens))
MYPATHS = set(); ALLPATHS = {R.PRS[p]['file'] for p in R.PUSH}; TAMPERS = {x[0] for x in R.TAMPER_BLOBS}
for n, L, key, h in PRS:
    pr = R.PRS[L]
    p = get(API + str(n)); files = get(API + str(n) + '/files?per_page=100'); commits = get(API + str(n) + '/commits?per_page=100')
    b = p.get('body') or ''; ti = p.get('title') or ''; br = p['head']['ref']
    cm = '\n'.join(c['commit']['message'] for c in commits)
    refs = re.findall(r'^\s*Refs?:?\s+(KS-\d+)\s*$', b, re.M | re.I); crefs = re.findall(r'^\s*Refs?:?\s+(KS-\d+)\s*$', cm, re.M | re.I)
    body_keys = sorted(set(re.findall(r'KS-\d+', b))); subj = cm.splitlines()[0] if cm else ''
    print('#%d PR %s %s head %s (READY ok %s; round16B ok %s) base %s@%s (== DEV %s) state %s mergeable %s mergeable_state %s commits %d created %s author %s | closing(title/body/commit) %d/%d/%d | completeness(title/body/commit) %d/%d/%d | body Refs lines %s (want [%s], == %s) | commit Refs lines %s (== %s) | KS keys in title %s | body chars %d | reviews-requested %d'
          % (n, L, key, p['head']['sha'][:12], p['head']['sha'] == h, p['head']['sha'] == pr['head'], p['base']['ref'], p['base']['sha'][:9], p['base']['sha'] == R.DEV, p['state'], p.get('mergeable'), p.get('mergeable_state'), len(commits), p.get('created_at'), (p.get('user') or {}).get('login'),
             len(CLOSING.findall(ti)), len(CLOSING.findall(b)), len(CLOSING.findall(cm)), len(COMPLETE.findall(ti)), len(COMPLETE.findall(b)), len(COMPLETE.findall(cm)),
             refs, key, refs == [key], crefs, crefs == [key], re.findall(r'KS-\d+', ti, re.I), len(b), len(p.get('requested_reviewers') or [])))
    for m_ in COMPLETE.finditer(b): print('      completeness hit in body: %r' % b[max(0, m_.start() - 60):m_.end() + 40].replace('\n', ' '))
    for m_ in CLOSING.finditer(b): print('      CLOSING hit in body: %r' % b[max(0, m_.start() - 60):m_.end() + 40].replace('\n', ' '))
    print('    title (%d chars, ascii %s) == round16B: %s | %s' % (len(ti), ti.isascii(), ti == pr['title'], ti)); print('    branch (ascii %s, non-ascii bytes %s, %d chars) == round16B: %s' % (br.isascii(), [c for c in br if ord(c) > 127] or 'NONE', len(br), 'refs/heads/' + br == pr['branch']))
    print('    commit subject (%d chars, ascii %s): %s | subject keys %s' % (len(subj), subj.isascii(), subj, re.findall(r'KS-\d+', subj)))
    for f in files: print('    %-8s +%-4d -%-4d %s' % (f['status'], f['additions'], f['deletions'], f['filename'])); MYPATHS.add(f['filename'])
    paths = [f['filename'] for f in files]; outside = [x for x in paths if '__tests__/' not in x]
    print('    files API == round16B [%s]: %s | outside __tests__: %s | additions total %d (want %d) | deletions total %d (want %d) | status %s' % (pr['file'].split('/')[-1], paths == [pr['file']], outside, sum(f['additions'] for f in files), pr['adds'], sum(f['deletions'] for f in files), pr['dels'], [f['status'] for f in files]))
    def inkey(k, s): return bool(re.search(re.escape(k) + r'(?!\d)', s, re.I)) or bool(re.search(k.lower().replace('-', '-?') + r'(?!\d)', s.lower()))
    hay = ti + ' ' + subj + ' ' + br
    bad_arch = [k for k in R.ARCHIVED if inkey(k, hay)]; bad_con = [k for k in R.CONTENT_LIVE if inkey(k, hay)]; bad_for = [k for k in FOREIGN if k != key and inkey(k, hay)]
    print('    archived keys in title/branch/subject:', bad_arch or 'NONE', '| live content keys in title/branch/subject:', bad_con or 'NONE', '(ks1213 in KS-1229 branch is a file-name form — the brief keeps it) | foreign keys:', bad_for or 'NONE', '| ks-727 in branch:', 'ks-727' in br, '| ks-727 in the FILE NAME (files API):', any('ks-727' in x for x in paths))
    print('    body KS keys:', body_keys, '| archived keys in body:', [k for k in R.ARCHIVED if k in body_keys] or 'NONE', '| foreign keys in body (not own):', [k for k in FOREIGN if k in body_keys and k != key] or 'NONE', '| own key in body:', key in body_keys)
    for w in ('INCOMPLETE', '12/15', 'SKIPPED', 'skips are not a pass', 'TEST-FILE-ONLY', '--recount', 'RECOUNT', 'truncat', 'corrupt patch', 'strict', 'cover', 'lock', 'started_utc', 'released', 'PROTOCOL-CLEAN', 'stubs=4', 'mergeable_state', 'typecheck17', 'TS2322', 'netlog', ':5432', 'anchoring:4005', 'threadTokenMint', 'UNVERIFIED', 'tier 1', 'tier 2', 'SECURITY'):
        c = len(re.findall(re.escape(w), b))
        if c: print('    body carries %r x%d' % (w, c))
    c = get(REPO + 'compare/develop...' + h)
    print('    compare develop...head: merge_base %s ahead %d behind %d files %d' % (c['merge_base_commit']['sha'], c['ahead_by'], c['behind_by'], len(c.get('files') or [])))
print('files API union', len(MYPATHS), '(want 8)', sorted(x.split('/')[-1] for x in MYPATHS))
rs = get(REPO + 'rulesets/18499832')
print('ruleset 18499832', rs.get('name'), rs.get('enforcement'), 'updated_at', rs.get('updated_at'), '| rules', [r.get('type') for r in rs.get('rules', [])], '| pull_request params', [r.get('parameters') for r in rs.get('rules', []) if r.get('type') == 'pull_request'], '| conditions', rs.get('conditions'))
print('--- Seat C 16th PRs (the other seat on the same .git; its READYs captured beside): head / author / created / head-ref namespace / files')
mine = {n for n, *_ in PRS}; cpaths = set()
for cn, ck, ch, cf in R.SEATC:
    try:
        pc = get(API + cn); fl = [f['filename'] for f in get(API + cn + '/files?per_page=100')]; cpaths |= set(fl)
        ns_ok = bool(re.match(r'^feature/ks-%s-.*-r15-.*-1$' % ck.split('-')[1], pc['head']['ref']))
        print('  #%s %s head %s (== READY %s) base %s@%s state %s author %s created %s | head ref %s | namespace `feature/ks-%s-…-r15-…-1`: %s | files %s | ∩ our 8 paths %s | ∩ our 9 tamper files %s' % (
            cn, ck, pc['head']['sha'][:9], pc['head']['sha'] == ch, pc['base']['ref'], pc['base']['sha'][:9], pc['state'], (pc.get('user') or {}).get('login'), pc.get('created_at'), pc['head']['ref'][:70], ck.split('-')[1], ns_ok, [x.split('/')[-1] for x in fl], sorted(set(fl) & ALLPATHS) or 'NONE', sorted(set(fl) & TAMPERS) or 'NONE'))
    except urllib.error.HTTPError as e: print('  #%s HTTP %s' % (cn, e.code))
print('  Seat C pushed paths ∩ our 8:', sorted(cpaths & ALLPATHS) or 'NONE', '| ∩ our 9 tamper files:', sorted(cpaths & TAMPERS) or 'NONE', '| every Seat C path under its three dirs:', all(any(x.startswith(d) for d in R.SEATC_DIRS) for x in cpaths))
print('--- open PRs touching any of the EIGHT paths or the NINE tamper files (read-only; Seat C\'s PRs named)')
hits = 0
for p in opens:
    if p['number'] in mine: continue
    try: fl = [f['filename'] for f in get(API + str(p['number']) + '/files?per_page=100')]
    except urllib.error.HTTPError as e: print('  #%d files API HTTP %s' % (p['number'], e.code)); continue
    h1 = sorted(set(fl) & ALLPATHS); h2 = sorted(set(fl) & TAMPERS)
    if h1 or h2:
        hits += 1
        print('  #%d %s head %s base %s@%s title %r files %d: ∩ our 8 paths %s | ∩ our 9 tamper files %s' % (p['number'], p['head']['ref'][:60], p['head']['sha'][:9], p['base']['ref'], p['base']['sha'][:9], (p.get('title') or '')[:60], len(fl), h1, h2))
print('  open-PR hits', hits, '| control POSITIVE: merged #894 files ∩ our 9 tamper files ->', sorted(set(f['filename'] for f in get(API + '894/files?per_page=100')) & TAMPERS), '(the seat S1 control) | control NEGATIVE: merged #1146 files ∩ our 8 ->', sorted(set(f['filename'] for f in get(API + '1146/files?per_page=100')) & ALLPATHS))
print('--- NAMESPACE trap: PRs numbered like the own tickets (and the held KS-1171)')
for q in (928, 975, 1118, 1133, 1158, 1171, 1179, 1181, 1229):
    try:
        pq = get(API + str(q)); print('PR #%d exists: state %s title %r head %s' % (q, pq['state'], (pq.get('title') or '')[:70], pq['head']['sha'][:9]))
    except urllib.error.HTTPError as e: print('PR #%d: HTTP %s' % (q, e.code))
    except Exception as e: print('PR #%d: %s' % (q, type(e).__name__))
print('--- the PR numbers of this round\'s window as they stand (1147..1165, whatever exists)')
for q in range(1147, 1166):
    try:
        pq = get(API + str(q)); print('PR #%d exists: state %s title %r head %s branch %s author %s created %s' % (q, pq['state'], (pq.get('title') or '')[:60], pq['head']['sha'][:9], pq['head']['ref'][:70], (pq.get('user') or {}).get('login'), pq.get('created_at')))
    except urllib.error.HTTPError as e: print('PR #%d: HTTP %s' % (q, e.code))
    except Exception as e: print('PR #%d: %s' % (q, type(e).__name__))
