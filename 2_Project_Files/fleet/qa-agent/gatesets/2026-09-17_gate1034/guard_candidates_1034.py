#!/usr/bin/env python3
"""guard_candidates_1034.py — READ-ONLY (GitHub GET): for every open PR head, compare 27e53ec3a...<head>; print status / ahead / behind / GUARDED hits /
#1034-file overlap, to find REAL commits for the launcher's controls: AHEAD + disjoint (-> 0 through the MOVED arm) and AHEAD + a GUARDED hit outside the
JUDGED set (-> 18 through the compare arm alone). GH_TOKEN by NAME, never printed."""
import json, urllib.request
tok = ''
for line in open('/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env', encoding='utf-8'):
    if line.startswith('GH_TOKEN='): tok = line.split('=', 1)[1].strip().strip('"').strip("'")
assert tok
api = 'https://api.github.com/repos/Secuura/Distributed_Secuura'
def get(p): return json.load(urllib.request.urlopen(urllib.request.Request(api + p, headers={'Authorization': 'Bearer ' + tok, 'Accept': 'application/vnd.github+json'}), timeout=60))
PIN = '27e53ec3aa010b50cd9b2e4a1d15cbb34605ba7d'
D = 'Blockchain/Dev/'; A = D + 'services/api-gateway/'
GUARDED = [A + 'src/', A + 'package.json', A + 'vitest.config.ts', A + 'vitest.setup.ts', A + 'tsconfig.json', D + 'packages/shared/src/', D + 'eslint.config.mjs']
MINE = {A + 'src/middleware/auth.ts', A + 'src/__tests__/ks1215-the-connector-branch-never-carries-the-callers-bearer.test.ts'}
for p in sorted(get('/pulls?state=open&per_page=100'), key=lambda x: x['number']):
    c = get('/compare/%s...%s' % (PIN, p['head']['sha']))
    fs = [f['filename'] for f in c.get('files') or []]
    hits = sorted({f for f in fs for g in GUARDED if f == g or (g.endswith('/') and f.startswith(g))})
    print('#%d %s status %s ahead %d behind %d files %d guarded %d %s | mine %s' % (p['number'], p['head']['sha'], c['status'], c['ahead_by'], c['behind_by'], len(fs), len(hits), hits[:3], sorted(set(fs) & MINE)))
