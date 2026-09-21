#!/usr/bin/env python3
"""gh_pr_reads_1130.py — READ-ONLY GitHub GETs for the Seat B 14th PRs whose READYs are captured (mail_seatB14_ready*_pr<N>_*.md): head sha vs the
READY, base sha, files (name, status, +/-), product bytes per PR from the FILES API (0 outside __tests__/ except PR 6's guard script), Refs lines
(one per own key; TWO on PR 4), closing-phrase / completeness detectors with controls, archived / foreign keys in title + branch + commit subject,
the brief's required scope sentences in the bodies, the compare develop...head (merge_base, ahead, behind, files), ruleset 18499832, open PRs
touching the six paths or the five tamper files (incl. #1129, the foreign chore head — a path conflict?), and the NAMESPACE trap (do PRs numbered
like the seven tickets exist?). Never prints a body, never prints the token (GH_TOKEN by NAME from the Secuura .env). Writes nothing (stdout).
Re-runnable. Derived from gatesets/2026-09-21_gate1119to1128/gh_pr_reads.py."""
import glob, json, os, re, urllib.request, sys, subprocess
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
KEYS = {'1': ['KS-1273'], '2': ['KS-1135'], '6': ['KS-958'], '3': ['KS-880'], '5': ['KS-887'], '4': ['KS-1236', 'KS-1006']}
PUSH = ['1', '2', '6', '3', '5', '4']
READY = {}
for f in sorted(glob.glob(os.path.join(G, 'mail_seatB14_ready*_pr*_*.md'))):
    m = re.search(r'READY FOR QA \(Seat B 14th\): PR (\d) (KS-\d+)[^\n]*? — #(\d+) at head ([0-9a-f]{40})', open(f, encoding='utf-8').read())
    if m: READY[m.group(1)] = (int(m.group(3)), m.group(4))
PRS = [(READY[p][0], p, KEYS[p], READY[p][1]) for p in PUSH if p in READY]
print('PRs from READYs:', [(n, 'PR ' + p, k) for n, p, k, h in PRS])
DEV = '9f0265eb06ecf24d4de18149ce862ad2330a61ee'
ARCHIVED = ['KS-501', 'KS-480', 'KS-978', 'KS-721', 'KS-522', 'KS-726', 'KS-535', 'KS-867', 'KS-878', 'KS-914', 'KS-1238', 'KS-1282', 'KS-1062', 'KS-971', 'KS-1078', 'KS-921', 'KS-490']
FOREIGN = ['KS-869', 'KS-1194', 'KS-1136', 'KS-1137', 'KS-957', 'KS-930', 'KS-969', 'KS-973', 'KS-1203', 'KS-1198', 'KS-1284', 'KS-1175', 'KS-1215', 'KS-753', 'KS-1232', 'KS-1223', 'KS-1234', 'KS-1283', 'KS-1244', 'KS-1275', 'KS-1279', 'KS-1272', 'KS-741', 'KS-1260', 'KS-1209', 'KS-953', 'KS-794', 'KS-1133', 'KS-1031']
SCOPE = {'1': ['declared cover', 'trivy.yaml', 'exit-code 0', 'flag > env > config'], '2': ['diagnostic', 'not a pin', 'NOT addressed', '14/14'], '6': ['latent', 'push-guard', 'no runtime image'],
         '3': ['NOT decided', 'default tenant', 'characterisation'], '5': ['--directory', 'overlap', 'deviation'], '4': ['NOT decided', 'stale', 'mfaSecret']}
opens = get(REPO + 'pulls?state=open&per_page=100&sort=created&direction=desc')
print('open PRs listed', len(opens), '| numbers', sorted(p['number'] for p in opens))
MYPATHS = set(); D = 'Blockchain/Dev/'
TAMPER = {'Blockchain/Testing/jobs/04-container-trivy.sh', 'systemTest/fixtures/manifest.ts', D + 'services/security/src/index.ts', D + 'services/auth/src/routes/users.ts', D + 'scripts/check-shared-relink.sh'}
SIBS = {D + 'scripts/__tests__/container_trivy_image_filter.test.sh', D + 'scripts/__tests__/container_trivy_failed_scan_is_loud.test.sh', D + 'scripts/__tests__/check_shared_relink.test.sh', D + 'scripts/__tests__/check_shared_relink_tooling_tokens.test.sh', D + 'scripts/__tests__/ks949_main_seed_idempotence.test.sh', D + 'scripts/__tests__/preflight_deps.test.sh', D + 'scripts/run-shell-suites.sh', D + 'scripts/preflight/preflight.sh', '.githooks/pre-push'}
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
    print('    title:', ti); print('    branch:', br)
    print('    commit subject (%d chars): %s | subject keys %s' % (len(subj), subj, re.findall(r'KS-\d+', subj)))
    for f in files: print('    %-8s +%-4d -%-4d %s' % (f['status'], f['additions'], f['deletions'], f['filename'])); MYPATHS.add(f['filename'])
    prod = [f['filename'] for f in files if '__tests__/' not in f['filename']]
    print('    files outside __tests__/ (files API):', len(prod), prod, '| additions total', sum(f['additions'] for f in files), '| deletions total', sum(f['deletions'] for f in files))
    bad_arch = [k for k in ARCHIVED if re.search(re.escape(k) + r'\b', ti + ' ' + subj, re.I) or re.search(k.lower() + r'(?!\d)', br.lower())]
    bad_for = [k for k in FOREIGN if k not in keys and (re.search(re.escape(k) + r'\b', ti + ' ' + subj, re.I) or re.search(k.lower() + r'(?!\d)', br.lower()))]
    print('    archived keys in title/branch/subject:', bad_arch or 'NONE', '| foreign keys in title/branch/subject:', bad_for or 'NONE', '| ks-869 in branch:', 'ks-869' in br)
    print('    body KS keys:', body_keys, '| archived keys in body:', [k for k in ARCHIVED if k in body_keys] or 'NONE', '| foreign keys in body:', [k for k in FOREIGN if k in body_keys and k not in keys] or 'NONE')
    print('    body scope sentences (case-insensitive substring):', {s: (s.lower() in b.lower()) for s in SCOPE[L]})
    for w in ('INCOMPLETE', '12/15', 'SKIPPED', 'skips are not a pass', 'TEST-ONLY', 'Deviation from verbatim', 'mergeable_state', 'NO PREFLIGHT VERDICT', 'ran NO legs', '--recount', 'golden', 'latent', 'S6', 'overlap', 'ONLY product', 'product byte'):
        c = len(re.findall(re.escape(w), b))
        if c: print('    body carries %r x%d' % (w, c))
    c = get(REPO + 'compare/develop...' + h)
    print('    compare develop...head: merge_base %s ahead %d behind %d files %d' % (c['merge_base_commit']['sha'], c['ahead_by'], c['behind_by'], len(c.get('files') or [])))
print('files API union', len(MYPATHS), sorted(MYPATHS))
rs = get(REPO + 'rulesets/18499832')
print('ruleset 18499832', rs.get('name'), rs.get('enforcement'), 'updated_at', rs.get('updated_at'), '| rules', [r.get('type') for r in rs.get('rules', [])], '| pull_request params', [r.get('parameters') for r in rs.get('rules', []) if r.get('type') == 'pull_request'], '| conditions', rs.get('conditions'))
print('--- open PRs touching any of our paths, the 5 tamper files or the siblings/harness (read-only)')
mine = {n for n, *_ in PRS}; hits = 0
for p in opens:
    if p['number'] in mine: continue
    fl = [f['filename'] for f in get(API + str(p['number']) + '/files?per_page=100')]
    h1 = sorted(set(fl) & MYPATHS); hT = sorted(set(fl) & TAMPER); hS = sorted(set(fl) & SIBS)
    if p['number'] == 1129 or h1 or hT or hS:
        hits += bool(h1 or hT or hS)
        print('  #%d %s head %s base %s@%s title %r files %d: ∩ our paths %s | ∩ tamper files %s | ∩ siblings/harness %s | files: %s' % (p['number'], p['head']['ref'][:60], p['head']['sha'][:9], p['base']['ref'], p['base']['sha'][:9], (p.get('title') or '')[:60], len(fl), h1 or 'NONE', hT or 'NONE', hS or 'NONE', fl[:10]))
print('  open-PR hits', hits, '| control POSITIVE: merged #1122 files ∩ (our paths ∪ tamper) ->', sorted(set(f['filename'] for f in get(API + '1122/files?per_page=100')) & (MYPATHS | TAMPER)), '| control NEGATIVE: merged #1119 files ∩ ->', sorted(set(f['filename'] for f in get(API + '1119/files?per_page=100')) & (MYPATHS | TAMPER)))
print('  control: #995 files ->', [f['filename'] for f in get(API + '995/files?per_page=100')])
for q in (1273, 1135, 958, 880, 887, 1236, 1006):
    try:
        pq = get(API + str(q)); print('PR #%d exists: state %s title %r' % (q, pq['state'], (pq.get('title') or '')[:70]))
    except Exception as e: print('PR #%d: %s' % (q, type(e).__name__))
for q in range(1129, 1138):
    try:
        pq = get(API + str(q)); print('PR #%d exists: state %s title %r head %s branch %s' % (q, pq['state'], (pq.get('title') or '')[:70], pq['head']['sha'][:9], pq['head']['ref'][:70]))
    except Exception as e: print('PR #%d: %s' % (q, type(e).__name__))
