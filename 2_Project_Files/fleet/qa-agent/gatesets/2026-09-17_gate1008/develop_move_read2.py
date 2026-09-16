#!/usr/bin/env python3
"""develop_move_read2.py — READ ONLY (GitHub API GET): the second develop move seen by the final --check (93629700c -> 73d3fcb90)."""
import json, urllib.request, datetime
tok = ''
for line in open('/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env', encoding='utf-8'):
    if line.startswith('GH_TOKEN='): tok = line.split('=', 1)[1].strip().strip('"').strip("'")
api = 'https://api.github.com/repos/Secuura/Distributed_Secuura'
get = lambda p: json.load(urllib.request.urlopen(urllib.request.Request(api + p, headers={'Authorization': 'Bearer ' + tok, 'Accept': 'application/vnd.github+json'}), timeout=60))
print('develop_move_read2', datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z'))
c = get('/compare/0308b7a0447a2c01c12aad358c9b4d04a5178210...73d3fcb902d2a78fe68a4349903ff6c6bd24d4d5')
print('compare 0308b7a04...73d3fcb90 status', c['status'], 'ahead', c['ahead_by'], 'files', len(c['files']))
for x in c['commits']: print('  commit', x['sha'], 'parents', [p['sha'][:9] for p in x['parents']], x['commit']['committer']['date'], '|', x['commit']['message'].split('\n')[0][:120])
for f in c['files']: print('  ', f['status'], f['sha'][:9], f['filename'])
p6 = get('/pulls/1006'); print('PR #1006 merged', p6['merged'], p6.get('merged_at'), p6.get('merge_commit_sha'))
print('api-gateway files in the move:', sum(1 for f in c['files'] if '/services/api-gateway/' in f['filename']), '| control: all files', len(c['files']))
