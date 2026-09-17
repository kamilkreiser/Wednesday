#!/usr/bin/env python3
"""guard_candidates_1032.py — READ-ONLY (GitHub GET): for every open PR head, compare 0a2b1603f...<head>; list heads that are strictly AHEAD of the pinned
develop and touch a GUARDED path without touching the #1032 files — usable as a real commit for the launcher's GUARDED (exit 18) arm control."""
import json, urllib.request
tok = ''
for line in open('/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env', encoding='utf-8'):
    if line.startswith('GH_TOKEN='): tok = line.split('=', 1)[1].strip().strip('"').strip("'")
api = 'https://api.github.com/repos/Secuura/Distributed_Secuura'
def get(p): return json.load(urllib.request.urlopen(urllib.request.Request(api + p, headers={'Authorization': 'Bearer ' + tok, 'Accept': 'application/vnd.github+json'}), timeout=60))
PIN = '0a2b1603fe52f0f3b8152588af78bbeab0237be7'
D = 'Blockchain/Dev/'; A = D + 'services/auth/'
GUARDED = [A + 'src/', A + 'package.json', A + 'vitest.config.ts', A + 'vitest.setup.ts', A + 'tsconfig.json', D + 'packages/shared/src/', D + 'docs/openapi/', D + 'eslint.config.mjs']
for p in sorted(get('/pulls?state=open&per_page=100'), key=lambda x: x['number']):
    c = get('/compare/%s...%s' % (PIN, p['head']['sha']))
    fs = [f['filename'] for f in c.get('files') or []]
    hits = sorted({f for f in fs for g in GUARDED if f == g or (g.endswith('/') and f.startswith(g))})
    print('#%d %s status %s ahead %d behind %d files %d guarded %d %s' % (p['number'], p['head']['sha'][:9], c['status'], c['ahead_by'], c['behind_by'], len(fs), len(hits), hits[:3]))
