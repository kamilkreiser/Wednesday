#!/usr/bin/env python3
"""gh_read2.py — READ-ONLY: the api-gateway file names of the open PRs that touch api-gateway (for the launcher's GUARDED list), plus the
JUDGED blobs at develop d067725ff. GH_TOKEN by NAME; never printed. GET only."""
import json, urllib.request, datetime
ENV = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'
tok = [l.split('=', 1)[1].strip().strip('"').strip("'") for l in open(ENV, encoding='utf-8') if l.startswith('GH_TOKEN=')][0]
api = 'https://api.github.com/repos/Secuura/Distributed_Secuura'
def get(p): return json.load(urllib.request.urlopen(urllib.request.Request(api + p, headers={'Authorization': 'Bearer ' + tok, 'Accept': 'application/vnd.github+json'}), timeout=60))
print('gh_read2', datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z'))
for n in (1010, 995, 923, 649, 575):
    for f in get('/pulls/%d/files?per_page=100' % n):
        if '/api-gateway/' in f['filename']: print('  #%d %s %s' % (n, f['status'], f['filename'].replace('Blockchain/Dev/', '')))
D = 'Blockchain/Dev/'
for f in ('services/api-gateway/src/middleware/audit.ts', 'services/api-gateway/src/index.ts', 'services/api-gateway/src/routes/proxy.ts', 'services/api-gateway/src/middleware/normalisePath.ts',
          'services/api-gateway/src/routes/versioning.ts', 'services/api-gateway/src/db.ts', 'services/api-gateway/src/middleware/auth.ts', 'services/api-gateway/package.json',
          'services/api-gateway/vitest.config.ts', 'services/api-gateway/vitest.setup.ts', 'services/api-gateway/tsconfig.json', 'eslint.config.mjs'):
    print('  blob develop %s %s' % (get('/contents/' + D + f + '?ref=d067725ff1c7f036dbf0f726b9bf12f4daefebe7')['sha'], f))
