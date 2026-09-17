#!/usr/bin/env python3
"""develop_move_read.py — READ-ONLY GitHub GET: compare 581c9db0d...81ee4b729 (the develop move seen by the launcher --check at 18:30) — files, commit message first line."""
import json, urllib.request, datetime
K = ''
for l in open('/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'):
    if l.startswith('GH_TOKEN='): K = l.split('=', 1)[1].strip().strip('"').strip("'")
print('GH_TOKEN set:', bool(K), '| read at', datetime.datetime.now().astimezone().strftime('%H:%M:%S %Z'))
c = json.load(urllib.request.urlopen(urllib.request.Request('https://api.github.com/repos/Secuura/Distributed_Secuura/compare/581c9db0db4201c42cbbf702f339b750989acdb1...81ee4b729e86a645fc9098aafa1aaf39035a9950', headers={'Authorization': 'Bearer ' + K, 'Accept': 'application/vnd.github+json'}), timeout=60))
print('status', c['status'], 'ahead', c['ahead_by'], 'behind', c['behind_by'])
for x in c['commits']: print('commit', x['sha'][:9], [p['sha'][:9] for p in x['parents']], repr(x['commit']['message'].split('\n')[0][:120]))
for f in c['files']: print('file', f['filename'], f['status'], '+%d -%d' % (f['additions'], f['deletions']), f['sha'][:9])
