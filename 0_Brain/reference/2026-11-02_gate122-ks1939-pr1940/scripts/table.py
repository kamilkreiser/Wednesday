import json, re, collections
L='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate122-ks1939-pr1940/logs'
def load(v): return {(r['route'],r['mode'],r['kind'],r['who']): r for r in map(json.loads, open(f'{L}/probe_{v}.jsonl'))}
B,H=load('base'),load('head')
norm=lambda s: re.sub(r'"verifiedAt":"[^"]+"','"verifiedAt":"T"',s)
def out(r): return (r['status'], norm(r['body']), r['ctype'])
def st(r): s=r['state']; return (s['writeStmts'],s['execRaw'],s['updateDocument'],s['healWrites'])
UNR=['revokedProxy','throwingGetter','getterThrowsProxy']
cnt=collections.Counter(); lines=[]
basebodies=collections.defaultdict(set)
for k,r in B.items(): basebodies[k[0]].add(norm(r['body']))
newbodies=set()
for k in sorted(H):
    b,h=B[k],H[k]; route,mode,kind,who=k
    cls=None
    if out(b)==out(h) and st(b)==st(h): cls='SAME'
    else:
        o=H.get((route,mode,'ordinaryError',who))
        if kind in UNR and o and out(h)==out(o) and st(h)==st(o): cls='RAISED_TO_ORDINARY'
        elif kind in ('ordinaryError','string') and b['status']=='NO ANSWER': cls='NOANSWER_TO_ANSWER'
        else: cls='OTHER_DIFF'
    if kind in UNR and cls!='RAISED_TO_ORDINARY':
        o=H.get((route,mode,'ordinaryError',who))
        if o and (out(h)!=out(o)): cls+='+HEAD_UNREADABLE!=ORDINARY'
    if norm(h['body']) and norm(h['body']) not in basebodies[route]: newbodies.add((route,norm(h['body'])[:120]))
    cnt[cls]+=1
    lines.append(f"{route:12} {mode:13} {kind:17} {who:5} | base {str(b['status']):9} {norm(b['body'])[:48]:48} w={st(b)} esc={len(b['escaped'])} | head {str(h['status']):9} {norm(h['body'])[:48]:48} w={st(h)} esc={len(h['escaped'])} | {cls}")
allw=[ (k,v) for v in (B,H) for k,r in v.items() if any(st(r))]
leaks=[(k,H[k]['leak']) for k in H if H[k]['leak'] and not (k[1]=='none' or H[k]['body'].startswith('{"verified":false,"warning"') or '"verified":true' in H[k]['body'])]
unh=[(k,H[k]['unhandled']) for k in H if H[k]['unhandled']]
print('\n'.join(lines))
print('COUNTS',dict(cnt))
print('cells base',len(B),'head',len(H))
print('cells with ANY write (writeStmts,execRaw,updateDocument,healWrites) >0:',[(k,st(B[k] if k in B else H[k])) for k,_ in allw][:20])
print('head bodies not seen at base for that route:',sorted(newbodies))
print('leak words in head failure bodies:',leaks)
print('head unhandled:',unh)
print('head escaped cells:',sorted(set((k[0],k[1]) for k in H if H[k]['escaped'])))
print('base escaped cells:',sorted(set((k[0],k[1]) for k in B if B[k]['escaped'])))
