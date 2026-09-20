#!/usr/bin/env python3
"""gh_pr_reads.py — READ-ONLY GitHub GETs for #1112-#1118: head sha vs pin, base sha, files (name, status, +/-), product bytes per PR from the
FILES API (0 outside __tests__/ = test-only), Refs lines (one per own key; two on C/E/F), closing-phrase / completeness detectors with
controls, archived / foreign keys in title + branch + commit subject, the seat's required scope sentences in the bodies (B / C / E / F), the
compare develop...head (merge_base, ahead, behind, files), ruleset 18499832, open PRs touching the 11 paths or the 10 tamper files, and the
NAMESPACE trap (do PRs numbered like the ten tickets exist?). Never prints a body, never prints the token (GH_TOKEN by NAME from the Secuura
.env). Writes nothing (stdout). Derived from gatesets/2026-09-21_gate1106to1111/gh_pr_reads.py."""
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
PRS = [(1112, 'A', ['KS-1203'], '3a28d2a3c4d030cb73b7775bb19c5844ce190e56'), (1113, 'B', ['KS-1283'], 'abf8321a9ca426a1d623a54a41453824dce34def'),
       (1114, 'C', ['KS-1244', 'KS-1198'], '762a70117c6cf40545f8a4ac5f24708e7fcd91fe'), (1115, 'D', ['KS-1275'], 'b008489e4fbc72bb8b68cb3bb925557978399780'),
       (1116, 'E', ['KS-1284', 'KS-1175'], '9a485cfe77406f47103ed6ab65c14ec01144cb68'), (1117, 'G', ['KS-1137'], 'b3f94f14a0cf3e0236284481b85781417fd233f3'),
       (1118, 'F', ['KS-1006', 'KS-1236'], 'f132c92147b5005c36e405d0116faa541d978a67')]
DEV = '362e51fe0db7e73d5557924902763fe3f10fd8c7'
ARCHIVED = ['KS-501', 'KS-480', 'KS-978', 'KS-721', 'KS-522', 'KS-726', 'KS-535', 'KS-867', 'KS-878', 'KS-914', 'KS-1238', 'KS-1282', 'KS-1062']
FOREIGN = ['KS-1194', 'KS-1136', 'KS-753', 'KS-1232', 'KS-1205', 'KS-1171', 'KS-1172', 'KS-1133', 'KS-794', 'KS-1215', 'KS-1273', 'KS-1274', 'KS-932', 'KS-741', 'KS-1260', 'KS-1209', 'KS-953']
SCOPE = {  # the brief's required scope sentences, as substrings the body must carry (case-insensitive)
  'B': ['guard', 'register-connector', 'requireSuperAdmin'], 'C': ['optional-mount', 'Bearer', 'NOT pinned'],
  'E': ['live sweep', 'MOCKED provider', 'nothing anchored', 'threadTokenMint'], 'F': ['mfaSecret', 'stale-approval', 'NOT decided'],
  'A': ['characterisation'], 'D': ['characterisation'], 'G': ['shellcheck']}
opens = get(REPO + 'pulls?state=open&per_page=100&sort=created&direction=desc')
print('open PRs listed', len(opens), '| numbers', sorted(p['number'] for p in opens))
MY11 = set(); TAMPER = {'Blockchain/Dev/services/api-gateway/src/services/enforcement.ts', 'Blockchain/Dev/services/api-gateway/src/routes/platform.ts', 'Blockchain/Dev/services/api-gateway/src/middleware/auth.ts',
  'Blockchain/Dev/services/originate/src/originate.openapi.ts', 'Blockchain/Dev/services/anchoring/src/anchorReadback.ts', 'Blockchain/Dev/services/anchoring/src/cardano/cardanoMetadatum.ts',
  'Blockchain/Dev/services/anchoring/src/index.ts', 'Blockchain/Dev/services/anchoring/src/cardano/transaction.ts', 'Blockchain/Dev/services/auth/src/routes/users.ts', 'Blockchain/Testing/jobs/04-container-trivy.sh'}
for n, L, keys, h in PRS:
    p = get(API + str(n)); files = get(API + str(n) + '/files?per_page=100'); commits = get(API + str(n) + '/commits?per_page=100')
    b = p.get('body') or ''; ti = p.get('title') or ''; br = p['head']['ref']
    cm = '\n'.join(c['commit']['message'] for c in commits)
    refs = re.findall(r'^\s*Refs?:?\s+(KS-\d+)\s*$', b, re.M | re.I)
    body_keys = sorted(set(re.findall(r'KS-\d+', b)))
    print('#%d PR %s %s head %s (pin ok %s) base %s@%s (== DEV %s) state %s mergeable %s mergeable_state %s commits %d created %s | closing(title/body/commit) %d/%d/%d | completeness(title/body/commit) %d/%d/%d | Refs lines %s (want %s, own set == %s) | KS keys in title %s | branch %s | body chars %d | reviews-requested %d'
          % (n, L, '+'.join(keys), p['head']['sha'][:12], p['head']['sha'] == h, p['base']['ref'], p['base']['sha'][:9], p['base']['sha'] == DEV, p['state'], p.get('mergeable'), p.get('mergeable_state'), len(commits), p.get('created_at'),
             len(CLOSING.findall(ti)), len(CLOSING.findall(b)), len(CLOSING.findall(cm)), len(COMPLETE.findall(ti)), len(COMPLETE.findall(b)), len(COMPLETE.findall(cm)),
             refs, keys, sorted(refs) == sorted(keys), re.findall(r'KS-\d+', ti, re.I), br, len(b), len(p.get('requested_reviewers') or [])))
    print('    title:', ti)
    print('    commit subject:', cm.splitlines()[0] if cm else '', '| subject keys', re.findall(r'KS-\d+', cm.splitlines()[0] if cm else ''))
    for f in files: print('    %-8s +%-4d -%-4d %s' % (f['status'], f['additions'], f['deletions'], f['filename'])); MY11.add(f['filename'])
    prod = [f['filename'] for f in files if '__tests__/' not in f['filename']]
    print('    files outside __tests__/ (files API):', len(prod), prod, '| additions total', sum(f['additions'] for f in files), '| deletions total', sum(f['deletions'] for f in files))
    bad_arch = [k for k in ARCHIVED if re.search(re.escape(k) + r'\b', ti + ' ' + br.replace('-', '-') + ' ' + (cm.splitlines()[0] if cm else ''), re.I) or re.search(k.lower().replace('-', '-?'), br.lower())]
    bad_for = [k for k in FOREIGN if re.search(re.escape(k) + r'\b', ti + ' ' + (cm.splitlines()[0] if cm else ''), re.I) or re.search(k.lower().replace('-', '-?'), br.lower())]
    print('    archived keys in title/branch/subject:', bad_arch or 'NONE', '| foreign keys in title/branch/subject:', bad_for or 'NONE', '| ks-878867 in branch:', 'ks-878867' in br)
    print('    body KS keys:', body_keys, '| archived keys in body:', [k for k in ARCHIVED if k in body_keys] or 'NONE', '| KS-480/KS-721 in body:', [k for k in ('KS-480', 'KS-721') if re.search(k + r'\b', b)] or 'NONE')
    print('    body scope sentences (case-insensitive substring):', {s: (s.lower() in b.lower()) for s in SCOPE[L]})
    for w in ('INCOMPLETE', '12/15', 'SKIPPED', 'skips are not a pass', 'TEST-ONLY', 'Deviation from verbatim', 'mergeable_state'):
        c = len(re.findall(re.escape(w), b))
        if c: print('    body carries %r x%d' % (w, c))
    c = get(REPO + 'compare/develop...' + h)
    print('    compare develop...head: merge_base %s ahead %d behind %d files %d' % (c['merge_base_commit']['sha'], c['ahead_by'], c['behind_by'], len(c.get('files') or [])))
print('files API union', len(MY11), '(want 11)')
rs = get(REPO + 'rulesets/18499832')
print('ruleset 18499832', rs.get('name'), rs.get('enforcement'), 'updated_at', rs.get('updated_at'), '| rules', [r.get('type') for r in rs.get('rules', [])], '| pull_request params', [r.get('parameters') for r in rs.get('rules', []) if r.get('type') == 'pull_request'])
print('--- open PRs touching any of the 11 paths or the 10 tamper files (read-only; the seat: only #995 touches anchoring index.ts)')
mine = {n for n, *_ in PRS}
for p in opens:
    if p['number'] in mine: continue
    fl = [f['filename'] for f in get(API + str(p['number']) + '/files?per_page=100')]
    hit11 = sorted(set(fl) & MY11); hitT = sorted(set(fl) & TAMPER)
    if hit11 or hitT: print('  #%d %s head %s: ∩ 11 paths %s | ∩ tamper files %s' % (p['number'], p['head']['ref'][:70], p['head']['sha'][:9], hit11 or 'NONE', hitT or 'NONE'))
print('  control: #1105 (merged) files ∩ tamper files ->', sorted(set(f['filename'] for f in get(API + '1105/files?per_page=100')) & TAMPER))
# namespace trap: do PRs numbered like the ten tickets exist? read-only
for q in (1203, 1283, 1244, 1198, 1275, 1284, 1175, 1006, 1236, 1137):
    try:
        pq = get(API + str(q)); print('PR #%d exists: state %s title %r' % (q, pq['state'], (pq.get('title') or '')[:70]))
    except Exception as e: print('PR #%d: %s' % (q, type(e).__name__))
