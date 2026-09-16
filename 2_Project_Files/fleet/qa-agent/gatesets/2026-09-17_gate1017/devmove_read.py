#!/usr/bin/env python3
"""devmove_read.py — READ-ONLY: the develop move during drafting. GET /commits/<develop> (tree, parents, message head), GET /pulls/1014 (merged, merge_commit_sha),
compare 7e89318bc...develop (files + blobs). GH_TOKEN by NAME, never printed."""
import json, urllib.request, datetime
ENV = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'; tok = ''
for line in open(ENV, encoding='utf-8'):
    if line.startswith('GH_TOKEN='): tok = line.split('=', 1)[1].strip().strip('"').strip("'")
assert tok
api = 'https://api.github.com/repos/Secuura/Distributed_Secuura'
def get(p): return json.load(urllib.request.urlopen(urllib.request.Request(api + p, headers={'Authorization': 'Bearer ' + tok, 'Accept': 'application/vnd.github+json'}), timeout=60))
print('devmove_read', datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z'))
dev = get('/branches/develop')['commit']['sha']; c = get('/commits/' + dev)
print('develop', dev, 'tree', c['commit']['tree']['sha'], 'parents', [p['sha'] for p in c['parents']], 'committer date', c['commit']['committer']['date'], '|', c['commit']['message'].split('\n')[0][:140])
p = get('/pulls/1014'); print('PR #1014 state', p['state'], 'merged', p['merged'], 'merged_at', p['merged_at'], 'merge_commit_sha', p['merge_commit_sha'])
cmp = get('/compare/7e89318bcedbc9a35757d4298ace54a6a23020bd...' + dev)
print('compare 7e89318bc...develop status', cmp['status'], 'ahead', cmp['ahead_by'], 'behind', cmp['behind_by'], 'files', len(cmp.get('files') or []))
for f in cmp.get('files') or []: print('   ', f['status'], f['sha'], '+%d -%d' % (f['additions'], f['deletions']), f['filename'])
