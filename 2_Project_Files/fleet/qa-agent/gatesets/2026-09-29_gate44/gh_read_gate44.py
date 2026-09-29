#!/usr/bin/env python3
"""gh_read_gate44.py — REST GET only: each kit PR (title, body, head, base, mergeable, files) and the open-PR list; writes gh_read_1.json
beside this script and gh_body_<n>.md for each PR. The token is read by name from the Secuura .env and never printed. Usage: gh_read_gate44.py"""
import json, os, time, urllib.request, urllib.error, datetime
G = os.path.dirname(os.path.abspath(__file__))
tok = ''
for l in open('/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env', encoding='utf-8'):
    if l.startswith('GH_TOKEN='): tok = l.split('=', 1)[1].strip().strip('"').strip("'")
assert tok, 'GH_TOKEN unset'
def get(u):
    for i in range(4):
        try: return json.load(urllib.request.urlopen(urllib.request.Request('https://api.github.com/repos/Secuura/Distributed_Secuura/' + u, headers={'Authorization': 'Bearer ' + tok, 'Accept': 'application/vnd.github+json'}), timeout=60))
        except urllib.error.HTTPError as e:
            if e.code < 500 or i == 3: raise
            time.sleep(10)
out = {'read_at': datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'), 'prs': {}}
for n in ('1346', '1347'):
    p = get('pulls/' + n); t = 1
    while p.get('mergeable') is None and t < 3: time.sleep(8); p = get('pulls/' + n); t += 1
    fs = [f['filename'] for f in get('pulls/%s/files?per_page=100' % n)]
    out['prs'][n] = {'title': p['title'], 'state': p['state'], 'head': p['head']['sha'], 'branch': p['head']['ref'], 'base': p['base']['ref'],
                     'mergeable': p.get('mergeable'), 'mergeable_state': p.get('mergeable_state'), 'files': fs, 'body': p.get('body') or ''}
    open(os.path.join(G, 'gh_body_%s.md' % n), 'w', encoding='utf-8').write(p.get('body') or '')
    print('#%s %s | head %s | branch %s | base %s | mergeable %s (%s) | %d files | title %d chars: %s' % (n, p['state'], p['head']['sha'], p['head']['ref'], p['base']['ref'], p.get('mergeable'), p.get('mergeable_state'), len(fs), len(p['title']), p['title']))
op = get('pulls?state=open&per_page=100')
out['open'] = [{'number': x['number'], 'title': x['title'], 'branch': x['head']['ref']} for x in op]
print('OPEN PRs: %d -> %s' % (len(op), ' '.join(str(x['number']) for x in op)))
json.dump(out, open(os.path.join(G, 'gh_read_1.json'), 'w'), indent=1)
print('GH READ OK at %s' % out['read_at'])
