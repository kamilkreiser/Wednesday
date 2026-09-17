#!/usr/bin/env python3
"""devmove_read_1034.py NEWDEV — READ-ONLY (GitHub GET): develop moved during drafting. compare 27e53ec3a...NEWDEV (status, commits with messages, files),
GUARDED hits (services/api-gateway/src/, gateway package.json / vitest.config.ts / vitest.setup.ts / tsconfig.json, packages/shared/src/, eslint.config.mjs),
the JUDGED blobs at NEWDEV (contents API), and compare NEWDEV...fd81a75f0 (merge_base, ahead, behind, files). GH_TOKEN by NAME, never printed."""
import json, sys, urllib.request, urllib.error, datetime
tok = ''
for line in open('/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env', encoding='utf-8'):
    if line.startswith('GH_TOKEN='): tok = line.split('=', 1)[1].strip().strip('"').strip("'")
assert tok
api = 'https://api.github.com/repos/Secuura/Distributed_Secuura'
def get(p): return json.load(urllib.request.urlopen(urllib.request.Request(api + p, headers={'Authorization': 'Bearer ' + tok, 'Accept': 'application/vnd.github+json'}), timeout=60))
PIN = '27e53ec3aa010b50cd9b2e4a1d15cbb34605ba7d'; H = 'fd81a75f0688f6cbe1e5f79b061bb1369c88f477'; NEW = sys.argv[1]
D = 'Blockchain/Dev/'; A = D + 'services/api-gateway/'
GUARDED = [A + 'src/', A + 'package.json', A + 'vitest.config.ts', A + 'vitest.setup.ts', A + 'tsconfig.json', D + 'packages/shared/src/', D + 'eslint.config.mjs']
print('devmove_read', datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z'), '| develop (branches API)', get('/branches/develop')['commit']['sha'])
c = get('/compare/%s...%s' % (PIN, NEW)); fs = [f['filename'] for f in c.get('files') or []]
hits = sorted({f for f in fs for g in GUARDED if f == g or (g.endswith('/') and f.startswith(g))})
print('compare %s...%s: status %s ahead %d behind %d files %d | GUARDED hits %d %s' % (PIN[:9], NEW[:9], c['status'], c['ahead_by'], c['behind_by'], len(fs), len(hits), hits))
for cm in c.get('commits') or []: print('  commit', cm['sha'][:9], 'parents', [p['sha'][:9] for p in cm['parents']], '|', cm['commit']['message'].split('\n')[0][:120])
for f in c.get('files') or []: print('  file', f['status'], f['sha'][:9], f['filename'])
c2 = get('/compare/%s...%s' % (NEW, H)); print('compare develop %s...head: merge_base %s status %s ahead %d behind %d files %d' % (NEW[:9], c2['merge_base_commit']['sha'][:9], c2['status'], c2['ahead_by'], c2['behind_by'], len(c2.get('files') or [])))
