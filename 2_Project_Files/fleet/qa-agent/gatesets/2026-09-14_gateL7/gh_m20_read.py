#!/usr/bin/env python3
"""Re-read after M20 (#903 squashed): the three PRs' mergeable state, develop, the compares. Token by NAME, never printed."""
import json, os, urllib.request, datetime
ENV='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'
tok=''
for line in open(ENV,encoding='utf-8'):
    if line.startswith('GH_TOKEN='): tok=line.strip().split('=',1)[1].strip().strip('"').strip("'")
assert tok,'GH_TOKEN not found by name'
API='https://api.github.com/repos/Secuura/Distributed_Secuura'
def get(p):
    r=urllib.request.urlopen(urllib.request.Request(API+p,headers={'Authorization':'Bearer '+tok,'Accept':'application/vnd.github+json'}),timeout=60)
    return json.load(r)
OUT='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-14_gateL7/gh'
print('read at', datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z'))
b=get('/branches/develop'); print('develop', b['commit']['sha'], b['commit']['commit']['committer']['date'], '|', b['commit']['commit']['message'].split('\n')[0][:90])
json.dump(b,open(OUT+'/branch_develop_M20.json','w'),indent=1)
for n in (918,924,925,903):
    p=get('/pulls/%d'%n); json.dump(p,open(OUT+'/pr%d_after_M20.json'%n,'w'),indent=1)
    print('#%d'%n, p['state'], 'merged=%s'%p['merged'], 'head', p['head']['sha'], 'base', p['base']['sha'][:9], 'mergeable=%s'%p['mergeable'], 'mergeable_state=%s'%p['mergeable_state'], 'updated', p['updated_at'], 'commits', p['commits'], 'files', p['changed_files'], 'merge_commit_sha', (p.get('merge_commit_sha') or '')[:9])
for a,bb,label in [('8861e62161466c40f08d2b10a30edeb203123993','a5334350221c819f54d4a20a3308daeb9ca09617','M18...M20'),
                   ('6e78961e1d04277ecbdb0537e630afa0bf63b13c','a5334350221c819f54d4a20a3308daeb9ca09617','M19...M20'),
                   ('develop','b54487216ebb49f1de7ed9349f089d92a3e5bfc1','develop...918'),
                   ('develop','b85f1db24596a5e0ce98fe2b1343d9f515a1a995','develop...924'),
                   ('develop','5341b1daed8afe4254e05ef66ef4350fd8220d4f','develop...925')]:
    c=get('/compare/%s...%s'%(a,bb)); json.dump(c,open(OUT+'/compare_%s_after_M20.json'%label.replace('...','_'),'w'),indent=1)
    print(label, 'status',c['status'],'ahead',c['ahead_by'],'behind',c['behind_by'],'merge_base',c['merge_base_commit']['sha'][:9],'files',len(c.get('files') or []), sorted(f['filename'] for f in (c.get('files') or []))[:8])
