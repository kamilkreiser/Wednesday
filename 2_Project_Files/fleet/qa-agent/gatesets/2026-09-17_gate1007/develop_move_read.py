#!/usr/bin/env python3
"""develop_move_read.py — READ-ONLY: develop moved during drafting. GitHub compare pinned...current develop (files, commits), compare
develop...#1007 head, #1005/#1006/#1007 PR state. GH_TOKEN by NAME, GET only, never printed."""
import json, urllib.request, datetime, sys
ENV='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'; tok=''
for line in open(ENV, encoding='utf-8'):
    if line.startswith('GH_TOKEN='): tok=line.split('=',1)[1].strip().strip('"').strip("'")
assert tok
api='https://api.github.com/repos/Secuura/Distributed_Secuura'
def get(p): return json.load(urllib.request.urlopen(urllib.request.Request(api+p, headers={'Authorization':'Bearer '+tok,'Accept':'application/vnd.github+json'}), timeout=60))
print('develop_move_read', datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z'))
cur=get('/branches/develop')['commit']['sha']; print('develop now', cur)
c=get('/compare/40fe4db6963cd11dba06bd46e0b00af39e68ef3a...'+cur)
print('pinned...develop status %s ahead %d behind %d files %d'%(c['status'],c['ahead_by'],c['behind_by'],len(c.get('files') or [])))
for x in c['commits']: print('  commit', x['sha'], [p['sha'][:9] for p in x['parents']], x['commit']['message'].split('\n')[0][:110])
for f in c.get('files') or []: print('  file', f['status'], f['sha'], f['filename'])
d=get('/compare/develop...b28ed490ada70df2056763f4512c98443285a694')
print('develop...#1007: merge_base %s status %s ahead %d behind %d files %d'%(d['merge_base_commit']['sha'],d['status'],d['ahead_by'],d['behind_by'],len(d.get('files') or [])))
for n in (1005,1006,1007):
    p=get('/pulls/%d'%n); print('PR #%d state %s merged %s head %s mergeable %s/%s'%(n,p['state'],p['merged'],p['head']['sha'],p.get('mergeable'),p.get('mergeable_state')))
