#!/usr/bin/env python3
"""devmove_read.py — READ-ONLY: develop moved 81ee4b729 -> ee40d3099 during the guard controls. Compare API files, commit message, and whether the Dev
package-lock.json delta touches any package auth resolves (lock keys under node_modules/ that auth's own tree or root hoisting would use). GH_TOKEN by NAME."""
import json, urllib.request, datetime, re
tok = ''
for line in open('/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env', encoding='utf-8'):
    if line.startswith('GH_TOKEN='): tok = line.split('=', 1)[1].strip().strip('"').strip("'")
assert tok
api = 'https://api.github.com/repos/Secuura/Distributed_Secuura'
def get(p, raw=False):
    h = {'Authorization': 'Bearer ' + tok, 'Accept': 'application/vnd.github.raw' if raw else 'application/vnd.github+json'}
    r = urllib.request.urlopen(urllib.request.Request(api + p, headers=h), timeout=60).read()
    return r if raw else json.loads(r)
P, N = '81ee4b729e86a645fc9098aafa1aaf39035a9950', 'ee40d3099599fa2db23a37049da8e00ac953eacd'
print('devmove_read', datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z'), '| develop now', get('/branches/develop')['commit']['sha'])
c = get('/compare/%s...%s' % (P, N)); print('compare status', c['status'], 'ahead', c['ahead_by'], 'files', len(c['files']))
for cm in c['commits']: print('  commit', cm['sha'][:9], cm['commit']['committer']['date'], cm['commit']['message'].split('\n')[0][:140])
for f in c['files']: print('  file', f['status'], '+%d -%d' % (f['additions'], f['deletions']), f['filename'])
L = 'Blockchain/Dev/package-lock.json'
a = json.loads(get('/contents/%s?ref=%s' % (L, P), raw=True)); b = json.loads(get('/contents/%s?ref=%s' % (L, N), raw=True))
pa, pb = a['packages'], b['packages']
ch = sorted(k for k in set(pa) | set(pb) if pa.get(k) != pb.get(k))
print('lock packages changed', len(ch), '| entries', len(pa), '->', len(pb))
for k in ch: print('   ', k, (pa.get(k) or {}).get('version'), '->', (pb.get(k) or {}).get('version'))
auth = [k for k in ch if k.startswith('services/auth') or k == '' ]
print('changed keys under services/auth or root package:', auth)
ctl = [k for k in pa if k.startswith('services/auth/node_modules/')]; print('control: auth-nested lock keys at pinned', len(ctl))
ad = pb.get('services/auth', {}); names = set((ad.get('dependencies') or {}) | (ad.get('devDependencies') or {}))
print('changed top-level names that auth declares:', sorted(k for k in ch if k.startswith('node_modules/') and k.split('node_modules/')[-1] in names), '| auth declares', len(names))
