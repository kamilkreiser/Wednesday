import json,sys,re
from collections import OrderedDict
L=sys.argv[1]
def load(v):
    d=OrderedDict()
    for line in open(f"{L}/probe_{v}.jsonl"):
        o=json.loads(line); d[(o['site'],o['route'],o['mode'],o['kind'],o['who'])]=o
    return d
B=load('base'); H=load('head')
ts=re.compile(r'\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d\.\d+Z')
def norm(o): return (o['status'], ts.sub('T', o['body']), o['ctype'])
def logsig(o): return [(l['level'],l['message'],l['error']) for l in o['logs']]
UNREAD={'revokedProxy','throwingGetter','getterThrowsProxy','msgRevokedProxy','msgThrowToJson','msgNullProto'}
READ_ODD={'msgObject','msgToString','msgNumber','string'}
def short(o):
    b=ts.sub('T',o['body']); b=b if len(b)<70 else b[:67]+'...'
    w=o['state']; lg=';'.join(f"{l['level']}:{l['message'][:28]}|{l['error'][:40]}" for l in o['logs']) or 'NO LOG'
    return f"{o['status']} {b} | q={w['queries']} x={w['executes']} hw={w['healWrites']} cf={w['chainFetches']} eh={w['errorHandler']} | {lg} | esc={len(o['escaped'])} unh={len(o['unhandled'])}"
out=[]; counts={'OK_EQ_ORDINARY':0,'PRE_EXISTING_base_eq_head':0,'DIFF':0,'readable_changed':0,'readable_same':0}
newleak=[]; diffs=[]
for k,h in H.items():
    b=B[k]; site,route,mode,kind,who=k
    ordk=(site,route,mode,'ordinaryError',who)
    tag=''
    if kind in UNREAD:
        o=H.get(ordk)
        if norm(h)==norm(o) and len(h['escaped'])==0 and [x for x in h['state'].items()]==[x for x in o['state'].items()]:
            tag='OK_EQ_ORDINARY'
        elif norm(h)==norm(b) and logsig(h)==logsig(b): tag='PRE_EXISTING_base_eq_head'
        else: tag='DIFF'
        counts[tag]+=1
    elif kind!='none':
        tag='readable_same' if (norm(h)==norm(b) and logsig(h)==logsig(b)) else 'readable_changed'; counts[tag]+=1
    else:
        tag='control_same' if norm(h)==norm(b) and logsig(h)==logsig(b) else 'CONTROL_CHANGED'
    if set(h['leak'])-set(b['leak']): newleak.append((k,sorted(set(h['leak'])-set(b['leak']))))
    out.append((k,tag,short(b),short(h)))
cur=None
for k,tag,sb,sh in out:
    hd=f"{k[0]} | {k[1]}"
    if hd!=cur: print(f"\n## {hd}"); cur=hd
    print(f"- {k[2]:8} {k[3]:17} {k[4]:5} [{tag}]\n    base: {sb}\n    head: {sh}")
print('\nJUDGE', counts, 'controls_changed', sum(1 for x in out if x[1]=='CONTROL_CHANGED'))
print('NEW LEAK base->head in response bodies:', newleak or 'none')
allleak=sorted(set((k[0],k[3],w) for k,h in H.items() for w in h['leak'] if k[3]!='none'))
print('ANY leak word in head non-success bodies:', allleak or 'none')
