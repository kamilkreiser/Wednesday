#!/usr/bin/env python3
"""devmove_read_1032.py — READ-ONLY (GitHub GET) judgement of a develop move under #1032: compare <pinned>...<current> files, commits, and whether any file
touches the launcher's GUARDED paths (services/auth/src/, auth package.json / vitest.config.ts / vitest.setup.ts / tsconfig.json, packages/shared/src/,
docs/openapi/, eslint.config.mjs) or the 19 JUDGED files; compare current develop...head 70ee7b6c0. GH_TOKEN by NAME; never printed."""
import json, sys, urllib.request, datetime
tok = ''
for line in open('/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env', encoding='utf-8'):
    if line.startswith('GH_TOKEN='): tok = line.split('=', 1)[1].strip().strip('"').strip("'")
assert tok
api = 'https://api.github.com/repos/Secuura/Distributed_Secuura'
def get(p): return json.load(urllib.request.urlopen(urllib.request.Request(api + p, headers={'Authorization': 'Bearer ' + tok, 'Accept': 'application/vnd.github+json'}), timeout=60))
pinned = '0a2b1603fe52f0f3b8152588af78bbeab0237be7'; H = '70ee7b6c03eeb7ef0609d6fc8fa5223e3647c039'
cur = sys.argv[1]
print('devmove_read', datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z'), '| pinned', pinned[:9], '| current', cur[:9])
c = get('/compare/%s...%s' % (pinned, cur))
print('compare pinned...current status', c['status'], 'ahead', c['ahead_by'], 'behind', c['behind_by'], 'files', len(c.get('files') or []))
for cm in c['commits']: print('  commit', cm['sha'][:9], 'parents', [p['sha'][:9] for p in cm['parents']], '|', cm['commit']['message'].split('\n')[0][:120])
D = 'Blockchain/Dev/'; A = D + 'services/auth/'
GUARDED = [A + 'src/', A + 'package.json', A + 'vitest.config.ts', A + 'vitest.setup.ts', A + 'tsconfig.json', D + 'packages/shared/src/', D + 'docs/openapi/', D + 'eslint.config.mjs']
hits = []
for f in c.get('files') or []:
    g = [x for x in GUARDED if f['filename'] == x or (x.endswith('/') and f['filename'].startswith(x))]
    print('  file', f['status'], '+%d -%d' % (f['additions'], f['deletions']), f['sha'][:9] if f.get('sha') else None, f['filename'], '| GUARDED' if g else '')
    if g: hits.append(f['filename'])
print('GUARDED hits', len(hits), hits)
c2 = get('/compare/develop...' + H)
print('compare develop...head: merge_base', c2['merge_base_commit']['sha'][:9], 'status', c2['status'], 'ahead', c2['ahead_by'], 'behind', c2['behind_by'], 'files', len(c2.get('files') or []), [f['filename'].split('/')[-1] for f in c2.get('files') or []])
