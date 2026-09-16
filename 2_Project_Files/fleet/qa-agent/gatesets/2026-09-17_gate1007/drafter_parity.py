#!/usr/bin/env python3
"""drafter_parity.py — #1007: run the parity probe in base / head / merged (probe copied in, moved out by rename to _quarantine, never rm);
compare every cell's normalised /system/status, /api/system/status and /status/simple hashes across trees; print per-NODE_ENV
agreement counts with the tree named beside every count, the staging cells' URL deltas, and the dead-estate census in the bodies."""
import sys, os, json, shutil
sys.path.insert(0,'/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1007')
from drafterlib import *
SRC=GS+'/qa1007-drafter-parity.test.ts'; REL=GWR+'/src/__tests__/qa1007-drafter-parity.test.ts'
Q=W+'/_quarantine'; os.makedirs(Q, exist_ok=True)
def probe(label, tree):
    assert porcelain(tree)==FARM, porcelain(tree)
    dst=T[tree]+'/'+REL; shutil.copyfile(SRC, dst); out=W+'/parity_%s.jsonl'%label; open(out,'w').close()
    r=vitest('parity_'+label, tree, files=['src/__tests__/qa1007-drafter-parity.test.ts'], env_extra={'QA_OUT':out}, save=False)
    os.rename(dst, Q+'/qa1007-drafter-parity.%s.test.ts'%label)
    assert porcelain(tree)==FARM, porcelain(tree)
    rows={}
    for l in open(out):
        d=json.loads(l); rows[d['id']]=d
    return r, rows
P('drafter_parity start', ts())
R={}
for t in ('base','head','merged'):
    r,rows=probe(t,t); R[t]=rows
    P('  tree %s: probe cells %d (vitest %s/%s passed), rows %d'%(t, r['tests'] if r else -1, r and r['passed'], r and r['tests'], len(rows)))
json.dump({t:{k:{kk:vv for kk,vv in v.items() if kk!='body'} for k,v in R[t].items()} for t in R}, open(GS+'/parity_rows.json','w'), indent=1)
json.dump({t:{k:v['body'] for k,v in R[t].items() if k.startswith('staging|')} for t in ('base','head')}, open(GS+'/parity_staging_bodies.json','w'), indent=1)
ids=sorted(R['head'])
P('== agreement per NODE_ENV (cells = 6 configs x 2 fetch modes; each cell compares /system/status, /api/system/status, /status/simple normalised hashes + status codes + fetched URL list)')
for ne in ('development','test','production','UNSET','staging'):
    cells=[i for i in ids if i.split('|')[0]==ne]
    def same(a,b,i):
        x,y=R[a][i],R[b][i]
        return all(x[k]==y[k] for k in ('statusHash','apiStatusHash','simpleHash','statusCode','apiStatusCode','simpleCode','fetchedStatus','nodeEnvSeenInBody'))
    bh=sum(same('base','head',i) for i in cells); hm=sum(same('head','merged',i) for i in cells)
    P('  NODE_ENV=%-11s base-vs-head identical %d/%d | head-vs-merged identical %d/%d | mounts agree (head) %d/%d | env seen in body (head) %s | fetch hits per /status (head) %s'%(
        ne, bh, len(cells), hm, len(cells), sum(R['head'][i]['mountsAgree'] for i in cells), len(cells), sorted({R['head'][i]['nodeEnvSeenInBody'] for i in cells}), sorted({R['head'][i]['fetchHitsStatus'] for i in cells})))
    for i in cells:
        if not same('base','head',i):
            b,hh=R['base'][i],R['head'][i]
            d={n:(b['urls'].get(n),hh['urls'].get(n)) for n in hh['urls'] if b['urls'].get(n)!=hh['urls'].get(n)}
            P('    DIFF %-28s urls changed %d | overall %s->%s healthy %s->%s simple %s->%s | dead: base urls %d trouble %d total %d -> head urls %d trouble %d total %d'%(
                i, len(d), b['overall'], hh['overall'], b['healthy'], hh['healthy'], b['simpleCode'], hh['simpleCode'], b['deadInUrls'], b['deadInTroubleshooting'], b['deadCount'], hh['deadInUrls'], hh['deadInTroubleshooting'], hh['deadCount']))
P('== staging|none|offline URL map, base -> head')
b,hh=R['base']['staging|none|offline'],R['head']['staging|none|offline']
for n in hh['urls']: P('   %-17s %-95s -> %s'%(n, b['urls'][n], hh['urls'][n]))
P('== staging|all|offline URL map changes, base -> head')
b,hh=R['base']['staging|all|offline'],R['head']['staging|all|offline']
for n in hh['urls']:
    if b['urls'][n]!=hh['urls'][n]: P('   %-17s %s -> %s'%(n, b['urls'][n], hh['urls'][n]))
P('== dead-estate strings in the /system/status BODY, head, every cell (count, in urls, in troubleshooting)')
for i in ids:
    x=R['head'][i]
    if x['deadCount']: P('   %-28s total %d urls %d troubleshooting %d sample %s'%(i, x['deadCount'], x['deadInUrls'], x['deadInTroubleshooting'], x['deadSample'][:1]))
P('drafter_parity end', ts())
