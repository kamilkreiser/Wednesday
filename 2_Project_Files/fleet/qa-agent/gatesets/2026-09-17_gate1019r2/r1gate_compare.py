#!/usr/bin/env python3
"""compare.py — census per tree/mode from rows_<tree>.json (this gate's probe): oracle tallies, base->head and head->merged row diffs, grace, limiter, noemail, urlspy, verdict."""
import json,sys,collections,os,datetime
EV=os.path.dirname(os.path.abspath(__file__))
print('compare', datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z'))
T={t:json.load(open(f'{EV}/rows_{t}.json')) for t in ('base','head','merged17','merged17r2')}
def key(r): return (r['id'],r.get('rep',1),r['tok'],r['target'],r['method'])
def sig(r): return (r['status'],r['code'],tuple(r['hits']),r.get('location'))
for t in T: print('tree',t,'jwksFetches (NOT hits)',T[t]['jwksFetches'],'originateRoutes',len(T[t]['originateRoutes']),'regex control (gdprRouter.<verb>( count)',T[t].get('originateRouteControl'),'verdictExported',T[t].get('verdictExported'))
for st in ('test','prod'):
    B={key(r):r for r in T['base'][st]}; H={key(r):r for r in T['head'][st]}
    print('=====',st,'base->head diffs (id | tok | target | base status,code,hits -> head)')
    for k in H:
        if sig(H[k])!=sig(B[k]): print('  ',k[0],'r%d'%k[1],'|',k[2],'|',k[3],'|',sig(B[k])[:3],'->',sig(H[k])[:3])
    for m in ('merged17','merged17r2'):
        M={key(r):r for r in T[m][st]}; print(' head vs',m,'row diffs',sum(1 for k in H if sig(H[k])!=sig(M[k])))
    print(' unchanged classes base=head (not-door, originate-route, scope door):', sum(1 for k in H if H[k]['cls'] in ('not-door','originate-route') and sig(H[k])!=sig(B[k])), 'diffs in not-door/originate-route;', sum(1 for k in H if H[k]['cls']=='door' and k[2]=='scope' and sig(H[k])!=sig(B[k])),'diffs in WITH-scope door rows')
    print(' admitted WITH-scope forwards at head (target -> upstream line):')
    for k,r in H.items():
        if r['tok']=='scope' and r['cls']=='door': print('   ',r['id'],'|',r['target'],'->',r['status'],r['hits'])
for t in T:
    print('=== grace',t)
    for r in T[t]['grace']: print('  ',r['id'],r['status'],r['code'],'hits',len(r['hits']),'graceSpyCalls',r['graceSpyCalls'],r['graceRoute'])
    print('=== limiter',t)
    for r in T[t]['limiter']: print('  ',r['id'],r['status'],r['code'],'X-RateLimit-Remaining',r['rlRemaining'],'hits',len(r['hits']))
    print('=== noemail',t)
    for r in T[t]['noemail']: print('  ',r['mode'],r['id'],r['tok'],r['status'],r['code'],'hits',len(r['hits']),'x-user-email lines',r.get('headerErr'))
    print('=== urlspy',t)
    for r in T[t]['urlspy']: print('  ',{k:v for k,v in r.items()})
print('=== verdict table (head; ci / cs)')
for v in T['head']['verdict']: print('  ',v['sub'],'|',v['ci']['verdict'],v['ci']['canonicalPath'],'|',v['cs']['verdict'],v['cs']['canonicalPath'])
print('verdict tables head == merged17 == merged17r2:', T['head']['verdict']==T['merged17']['verdict']==T['merged17r2']['verdict'], '| base exported:', T['base'].get('verdictExported'))
