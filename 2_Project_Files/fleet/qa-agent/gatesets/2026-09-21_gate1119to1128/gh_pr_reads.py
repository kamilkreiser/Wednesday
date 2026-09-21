#!/usr/bin/env python3
"""gh_pr_reads.py — READ-ONLY GitHub GETs for #1119-#1128: head sha vs pin, base sha, files (name, status, +/-), product bytes per PR from the
FILES API (0 outside __tests__/ except PR F's one job path), Refs lines (one per own key; two on G), closing-phrase / completeness detectors
with controls, archived / foreign keys in title + branch + commit subject, the brief's required scope sentences in the bodies, the compare
develop...head (merge_base, ahead, behind, files), ruleset 18499832, open PRs touching the 13 paths or the 11 tamper files, and the
NAMESPACE trap (do PRs numbered like the eleven tickets exist?). Never prints a body, never prints the token (GH_TOKEN by NAME from the Secuura
.env). Writes nothing (stdout). Derived from gatesets/2026-09-21_gate1112to1118/gh_pr_reads.py."""
import json, re, urllib.request, sys, subprocess
print('date', subprocess.run(['date', '-u', '+%Y-%m-%dT%H:%M:%SZ'], capture_output=True, text=True).stdout.strip())
tok = ''
for l in open('/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env', encoding='utf-8'):
    if l.startswith('GH_TOKEN='): tok = l.split('=', 1)[1].strip().strip('"').strip("'")
assert tok, 'GH_TOKEN unset'
REPO = 'https://api.github.com/repos/Secuura/Distributed_Secuura/'
API = REPO + 'pulls/'
def get(u): return json.load(urllib.request.urlopen(urllib.request.Request(u, headers={'Authorization': 'Bearer ' + tok, 'Accept': 'application/vnd.github+json'}), timeout=60))
CLOSING = re.compile(r'\b(close[sd]?|fix(e[sd])?|resolve[sd]?|complete[sd]?)\s+#?KS-\d+', re.I)
COMPLETE = re.compile(r'\b(complete[sd]?|completeness|fully pins|now complete|closes the ticket|entire scope|all of KS-\d+)\b', re.I)
assert COMPLETE.search('Completes KS-1282') and not COMPLETE.search('pins todays 403 and claims nothing further'), 'completeness detector controls'
assert CLOSING.search('Completes KS-1282') and not CLOSING.search('Whether KS-1282 is now complete') and not CLOSING.search('PREFLIGHT INCOMPLETE — 12/15'), 'closing detector controls'
PRS = [(1119, 'B', ['KS-753'], 'e9e20196f2a91ca57ec6bc6d24087843e2611a08'), (1120, 'E', ['KS-1232'], '2a66cd17ec3bd5d91e2fc72c7e3f9102ce1eb839'),
       (1121, 'G', ['KS-957', 'KS-930'], '939de1ba519629cacd22031cbc42dbbb765b4040'), (1122, 'F', ['KS-1273'], '9aa5442aeef4d07a3d39e3c3e73e65ef9a42a350'),
       (1123, 'H', ['KS-1275'], 'c346999ad3956c02e56fca61f9ad30396ceee2ff'), (1124, 'A', ['KS-880'], 'bd907c5538286ee9333e2182d7b388c1007b7163'),
       (1125, 'D', ['KS-1223'], 'c50c0a8d402cb6fc585b889c528802fba74c0e40'), (1126, 'I', ['KS-1283'], 'b23ad259a880ecb207b2ab3cf7e9a1b0b8368dad'),
       (1127, 'J', ['KS-1244'], 'f0cc0aadc1a7856f76cbb69e925e23b94dd05a40'), (1128, 'C', ['KS-1234'], 'e35b5ddc27dffca5ad1a7cea17b4433484d460ac')]
DEV = '7be81d5c9b109959b559e03652fb092c12de58e8'
ARCHIVED = ['KS-501', 'KS-480', 'KS-978', 'KS-721', 'KS-522', 'KS-726', 'KS-535', 'KS-867', 'KS-878', 'KS-914', 'KS-1238', 'KS-1282', 'KS-1062']
FOREIGN = ['KS-869', 'KS-740', 'KS-1136', 'KS-444', 'KS-921', 'KS-490', 'KS-1137', 'KS-1072', 'KS-815', 'KS-1215', 'KS-1203', 'KS-1198', 'KS-1284', 'KS-1175', 'KS-1006', 'KS-1236', 'KS-570', 'KS-719', 'KS-1194', 'KS-1279', 'KS-1272', 'KS-741', 'KS-1260', 'KS-1209', 'KS-953', 'KS-794', 'KS-1133', 'KS-887', 'KS-958']
SCOPE = {  # the brief's required scope sentences, as substrings the body must carry (case-insensitive)
  'B': ['NOT decided', 'persisted'], 'E': ['NOT decided', 'characterisation'], 'G': ['shellcheck', 'KS-930'], 'F': ['no runtime image', 'exit-code 0', '0.71.0'],
  'H': ['NOT decided', 'verb'], 'A': ['NOT decided', 'default tenant'], 'D': ['NOT decided', 'owners'], 'I': ['guard', 'NOT the handlers'],
  'J': ['wider', 'optional-mount', 'Bearer'], 'C': ['sanitize', 'NOT decided', 'allowance']}
opens = get(REPO + 'pulls?state=open&per_page=100&sort=created&direction=desc')
print('open PRs listed', len(opens), '| numbers', sorted(p['number'] for p in opens))
MY13 = set()
D = 'Blockchain/Dev/'
TAMPER = {D + 'services/security/src/index.ts', D + 'services/timestamping/src/index.ts', D + 'services/api-gateway/src/index.ts', D + 'services/api-gateway/src/routes/verification.ts',
  D + 'services/api-gateway/src/routes/platform.ts', D + 'services/api-gateway/src/middleware/auth.ts', D + 'services/originate/src/originate.openapi.ts', D + 'services/referral/src/routes/referrals.ts',
  D + 'services/mcp-server/src/tools/info.ts', D + 'services/mcp-server/src/http-server.ts', D + 'scripts/check-shared-relink.sh'}
for n, L, keys, h in PRS:
    p = get(API + str(n)); files = get(API + str(n) + '/files?per_page=100'); commits = get(API + str(n) + '/commits?per_page=100')
    b = p.get('body') or ''; ti = p.get('title') or ''; br = p['head']['ref']
    cm = '\n'.join(c['commit']['message'] for c in commits)
    refs = re.findall(r'^\s*Refs?:?\s+(KS-\d+)\s*$', b, re.M | re.I)
    crefs = re.findall(r'^\s*Refs?:?\s+(KS-\d+)\s*$', cm, re.M | re.I)
    body_keys = sorted(set(re.findall(r'KS-\d+', b)))
    subj = cm.splitlines()[0] if cm else ''
    print('#%d PR %s %s head %s (pin ok %s) base %s@%s (== DEV %s) state %s mergeable %s mergeable_state %s commits %d created %s | closing(title/body/commit) %d/%d/%d | completeness(title/body/commit) %d/%d/%d | body Refs lines %s (want %s, own set == %s) | commit Refs lines %s (== %s) | KS keys in title %s | body chars %d | reviews-requested %d'
          % (n, L, '+'.join(keys), p['head']['sha'][:12], p['head']['sha'] == h, p['base']['ref'], p['base']['sha'][:9], p['base']['sha'] == DEV, p['state'], p.get('mergeable'), p.get('mergeable_state'), len(commits), p.get('created_at'),
             len(CLOSING.findall(ti)), len(CLOSING.findall(b)), len(CLOSING.findall(cm)), len(COMPLETE.findall(ti)), len(COMPLETE.findall(b)), len(COMPLETE.findall(cm)),
             refs, keys, sorted(refs) == sorted(keys), crefs, sorted(crefs) == sorted(keys), re.findall(r'KS-\d+', ti, re.I), len(b), len(p.get('requested_reviewers') or [])))
    print('    title:', ti)
    print('    branch:', br)
    print('    commit subject (%d chars): %s | subject keys %s' % (len(subj), subj, re.findall(r'KS-\d+', subj)))
    for f in files: print('    %-8s +%-4d -%-4d %s' % (f['status'], f['additions'], f['deletions'], f['filename'])); MY13.add(f['filename'])
    prod = [f['filename'] for f in files if '__tests__/' not in f['filename']]
    print('    files outside __tests__/ (files API):', len(prod), prod, '| additions total', sum(f['additions'] for f in files), '| deletions total', sum(f['deletions'] for f in files))
    own_l = [k.lower() for k in keys]
    bad_arch = [k for k in ARCHIVED if re.search(re.escape(k) + r'\b', ti + ' ' + subj, re.I) or re.search(k.lower() + r'(?!\d)', br.lower())]
    bad_for = [k for k in FOREIGN if k not in keys and (re.search(re.escape(k) + r'\b', ti + ' ' + subj, re.I) or re.search(k.lower() + r'(?!\d)', br.lower()))]
    print('    archived keys in title/branch/subject:', bad_arch or 'NONE', '| foreign keys in title/branch/subject:', bad_for or 'NONE', '| ks-930 in branch:', 'ks-930' in br)
    print('    body KS keys:', body_keys, '| archived keys in body:', [k for k in ARCHIVED if k in body_keys] or 'NONE', '| foreign keys in body:', [k for k in FOREIGN if k in body_keys and k not in keys] or 'NONE')
    print('    body scope sentences (case-insensitive substring):', {s: (s.lower() in b.lower()) for s in SCOPE[L]})
    for w in ('INCOMPLETE', '12/15', 'SKIPPED', 'skips are not a pass', 'TEST-ONLY', 'Deviation from verbatim', 'mergeable_state', 'manifest_quarantine', 'no-useless-assignment', 'allowance', 'ONLY product'):
        c = len(re.findall(re.escape(w), b))
        if c: print('    body carries %r x%d' % (w, c))
    c = get(REPO + 'compare/develop...' + h)
    print('    compare develop...head: merge_base %s ahead %d behind %d files %d' % (c['merge_base_commit']['sha'], c['ahead_by'], c['behind_by'], len(c.get('files') or [])))
print('files API union', len(MY13), '(want 13)')
rs = get(REPO + 'rulesets/18499832')
print('ruleset 18499832', rs.get('name'), rs.get('enforcement'), 'updated_at', rs.get('updated_at'), '| rules', [r.get('type') for r in rs.get('rules', [])], '| pull_request params', [r.get('parameters') for r in rs.get('rules', []) if r.get('type') == 'pull_request'])
print('--- open PRs touching any of the 13 paths or the 11 tamper files (read-only)')
mine = {n for n, *_ in PRS}
hits = 0
for p in opens:
    if p['number'] in mine: continue
    fl = [f['filename'] for f in get(API + str(p['number']) + '/files?per_page=100')]
    hit13 = sorted(set(fl) & MY13); hitT = sorted(set(fl) & TAMPER)
    if hit13 or hitT: hits += 1; print('  #%d %s head %s: ∩ 13 paths %s | ∩ tamper files %s' % (p['number'], p['head']['ref'][:70], p['head']['sha'][:9], hit13 or 'NONE', hitT or 'NONE'))
print('  open-PR hits', hits, '| control POSITIVE: merged #1108 files ∩ (13 paths ∪ tamper) ->', sorted(set(f['filename'] for f in get(API + '1108/files?per_page=100')) & (MY13 | TAMPER)), '| control NEGATIVE: merged #1115 files ∩ ->', sorted(set(f['filename'] for f in get(API + '1115/files?per_page=100')) & (MY13 | TAMPER)))
print('  control: #995 files ->', [f['filename'] for f in get(API + '995/files?per_page=100')])
for q in (753, 1232, 957, 930, 1273, 1275, 880, 1223, 1283, 1244, 1234):
    try:
        pq = get(API + str(q)); print('PR #%d exists: state %s title %r' % (q, pq['state'], (pq.get('title') or '')[:70]))
    except Exception as e: print('PR #%d: %s' % (q, type(e).__name__))
for q in (1129, 1130):
    try:
        pq = get(API + str(q)); print('PR #%d exists: state %s title %r head %s' % (q, pq['state'], (pq.get('title') or '')[:70], pq['head']['sha'][:9]))
    except Exception as e: print('PR #%d: %s' % (q, type(e).__name__))
