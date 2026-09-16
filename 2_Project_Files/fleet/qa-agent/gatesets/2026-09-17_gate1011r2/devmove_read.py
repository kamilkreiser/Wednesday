#!/usr/bin/env python3
"""devmove_read.py — READ-ONLY GitHub compare 79432c797...<current develop> for the #1011 ROUND 2 drafter (GET only; GH_TOKEN by NAME)."""
import json, sys, urllib.request, datetime
tok = ''
for line in open('/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env', encoding='utf-8'):
    if line.startswith('GH_TOKEN='): tok = line.split('=', 1)[1].strip().strip('"').strip("'")
assert tok
api = 'https://api.github.com/repos/Secuura/Distributed_Secuura'
get = lambda p: json.load(urllib.request.urlopen(urllib.request.Request(api + p, headers={'Authorization': 'Bearer ' + tok, 'Accept': 'application/vnd.github+json'}), timeout=60))
print('devmove_read', datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z'))
dev = get('/branches/develop')['commit']['sha']; print('develop', dev)
c = get('/compare/79432c797cfb6e647acdd8798dace000a0b35d75...' + dev)
print('status', c['status'], 'ahead', c['ahead_by'], 'behind', c['behind_by'])
for x in c['commits']: print(' commit', x['sha'][:9], [p['sha'][:9] for p in x['parents']], x['commit']['message'].split('\n')[0][:120])
for f in c.get('files') or []: print(' file', f['status'], '+%d -%d' % (f['additions'], f['deletions']), f['sha'][:9], f['filename'])
h = get('/compare/' + dev + '...6dc8256448b50de6a15519001a4f7032ace1ae19')
print('develop...head: merge_base', h['merge_base_commit']['sha'][:9], h['status'], 'ahead', h['ahead_by'], 'behind', h['behind_by'], 'files', len(h.get('files') or []))
