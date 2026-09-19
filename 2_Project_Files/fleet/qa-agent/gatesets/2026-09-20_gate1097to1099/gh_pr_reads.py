#!/usr/bin/env python3
"""gh_pr_reads.py — READ-ONLY GitHub GETs for #1097-#1099: head sha, files (name, status, +/-), zero product bytes per PR from the FILES API,
body FACTS as booleans / counts (incl. the O-1 detector for #1099), ruleset 18499832. Never prints a body, never prints the token (GH_TOKEN by
NAME from the Secuura .env). Writes nothing (stdout). Derived from gatesets/2026-09-20_gate1092to1096/gh_pr_reads.py (data changed)."""
import json, re, urllib.request
tok = ''
for l in open('/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env', encoding='utf-8'):
    if l.startswith('GH_TOKEN='): tok = l.split('=', 1)[1].strip().strip('"').strip("'")
assert tok, 'GH_TOKEN unset'
REPO = 'https://api.github.com/repos/Secuura/Distributed_Secuura/'
API = REPO + 'pulls/'
def get(u): return json.load(urllib.request.urlopen(urllib.request.Request(u, headers={'Authorization': 'Bearer ' + tok, 'Accept': 'application/vnd.github+json'}), timeout=60))
CLOSING = re.compile(r'\b(close[sd]?|fix(e[sd])?|resolve[sd]?|complete[sd]?)\s+#?KS-\d+', re.I)
O1 = re.compile(r'\bO-1\b|revoked admin|admin session|session check|SESSION_INVALIDATED|KS-689', re.I)
TICKET = {1097: 'KS-1230', 1098: 'KS-1062(archived)', 1099: 'KS-1238+KS-1282'}
HEAD = {1097: 'f5364217952c1cb4d3755fbf8604b3edde124c42', 1098: 'efce14bed4a8adda15bca124fa60ae7d894fa6a6', 1099: 'b68aaf9b4581e67369be33d8ebcf4d61886c039b'}
WANTREFS = {1097: ['KS-1230'], 1098: [], 1099: ['KS-1238', 'KS-1282']}
assert O1.search('a revoked admin session') and O1.search('O-1 is') and not O1.search('KS-1238 N95-1 admin-shadow 401'), 'O-1 detector controls'
assert CLOSING.search('Completes KS-1282') and not CLOSING.search('Whether KS-1282 is now complete'), 'closing detector controls'
allok = True; t1ok = True; refsok = True
for n in (1097, 1098, 1099):
    p = get(API + str(n)); files = get(API + str(n) + '/files?per_page=100')
    commits = get(API + str(n) + '/commits?per_page=100')
    b = p.get('body') or ''; ti = p.get('title') or ''; br = p['head']['ref']
    cm = '\n'.join(c['commit']['message'] for c in commits)
    refs = sorted(set(re.findall(r'^\s*Refs?:?\s+(KS-\d+)', b, re.M | re.I)))
    own_num = ('KS-%d' % n) in (b + ti + cm)
    k1215 = [x for x in (('branch', br), ('title', ti), ('commit subject', cm.splitlines()[0] if cm else '')) if re.search(r'ks-?1215', x[1], re.I)]
    if refs != WANTREFS[n]: refsok = False
    print('#%d %s head %s (pin: %s) state %s mergeable %s mergeable_state %s base %s commits %d | closing(title/body/commit) %d/%d/%d | Refs lines %s (want %s) | names KS-%d (its own PR number) %s | KS keys in body %s | ks1215/ks-1215 in branch/title/commit-subject %s | KS keys in title %s | in branch %s | O-1 detector hits title/body/commit %d/%d/%d | body chars %d'
          % (n, TICKET[n], p['head']['sha'][:12], p['head']['sha'] == HEAD[n], p['state'], p.get('mergeable'), p.get('mergeable_state'), p['base']['ref'], len(commits),
             len(CLOSING.findall(ti)), len(CLOSING.findall(b)), len(CLOSING.findall(cm)), refs, WANTREFS[n], n, own_num, sorted(set(re.findall(r'KS-\d+', b))), [x[0] for x in k1215],
             re.findall(r'KS-\d+', ti, re.I), re.findall(r'ks-\d+', br, re.I), len(O1.findall(ti)), len(O1.findall(b)), len(O1.findall(cm)), len(b)))
    for f in files: print('    %-8s +%-4d -%-4d %s' % (f['status'], f['additions'], f['deletions'], f['filename']))
    prod = [f['filename'] for f in files if '/src/__tests__/' not in f['filename']]
    print('    files outside src/__tests__/ (files API):', len(prod), prod, '| deletions total', sum(f['deletions'] for f in files))
    if prod: allok = False
    if n == 1099 and (prod or len(files) != 1): t1ok = False
    print('    ks1215 occurrences in body %d | "KS-1215" in body %s' % (len(re.findall('ks1215', b)), 'KS-1215' in b))
print('ZERO PRODUCT BYTES in all three (files API):', allok)
print('TIER 1 #1099: one file, zero product bytes (files API):', t1ok)
print('Refs lines as wanted (#1097 KS-1230; #1098 none; #1099 KS-1238 + KS-1282):', refsok)
rs = get(REPO + 'rulesets/18499832')
print('ruleset 18499832 updated_at', rs.get('updated_at'), '| rules', [r.get('type') for r in rs.get('rules', [])],
      '| pull_request params', [r.get('parameters') for r in rs.get('rules', []) if r.get('type') == 'pull_request'])
