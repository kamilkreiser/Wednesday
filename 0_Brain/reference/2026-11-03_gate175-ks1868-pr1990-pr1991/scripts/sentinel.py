import json,sys
W='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate175-ks1868-pr1990-pr1991/results/'
pr=sys.argv[1]
def load(t): return sorted([json.loads(l) for l in open(W+f'p{pr}_{t}.jsonl')], key=lambda r:(r['q'],r['site'],r['value']))
b,h=load('base'),load('head')
tb=th=0; more=[]; less=[]; bodyb=bodyh=0
for x,y in zip(b,h):
    sb,sh=x.get('sentinelLines',0),y.get('sentinelLines',0); tb+=sb; th+=sh
    bodyb+=bool(x.get('bodyHasSentinel')); bodyh+=bool(y.get('bodyHasSentinel'))
    if sh>sb or (y.get('bodyHasSentinel') and not x.get('bodyHasSentinel')): more.append((x['site'],x['value'],sb,sh,x.get('bodyHasSentinel'),y.get('bodyHasSentinel')))
    if sh<sb: less.append((x['site'],x['value'],sb,sh))
print('sentinel log lines base',tb,'head',th,'; response bodies with sentinel base',bodyb,'head',bodyh)
print('cells where head prints MORE:',len(more)); [print('  ',m) for m in more]
print('cells where head prints less:',len(less)); [print('  ',m) for m in less]
