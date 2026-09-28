#!/usr/bin/env python3
"""_api_peek_gate37.py — drafting peek (READ, REST GET only): the open PR list (number, head, base ref, branch, created, title) + #1327-#1328 detail. Token by name, never printed."""
import json, urllib.request
tok = ''
for l in open('/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env', encoding='utf-8'):
    if l.startswith('GH_TOKEN='): tok = l.split('=', 1)[1].strip().strip('"').strip("'")
def get(u): return json.load(urllib.request.urlopen(urllib.request.Request('https://api.github.com/repos/Secuura/Distributed_Secuura/' + u, headers={'Authorization': 'Bearer ' + tok, 'Accept': 'application/vnd.github+json'}), timeout=60))
op = get('pulls?state=open&per_page=100&sort=created&direction=desc')
print('open PRs', len(op))
for x in op: print(x['number'], x['head']['sha'][:12], x['base']['ref'], x['head']['ref'], x['created_at'], x['title'][:90])
for n in ('1327', '1328'):
    try: p = get('pulls/' + n)
    except Exception as e: print('#%s: %s' % (n, e)); continue
    print('#%s state %s draft %s base %s base.sha %s head %s mergeable %s | %s' % (n, p['state'], p['draft'], p['base']['ref'], p['base']['sha'][:12], p['head']['sha'], p.get('mergeable'), p['title']))
