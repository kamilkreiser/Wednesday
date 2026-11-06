import json,sys,collections
G=sys.argv[1]
def load(n): return [json.loads(l) for l in open(f"{G}/evidence/q3_{n}.jsonl")]
b=[r for r in load('base') if 'adapter' in r]; h=[r for r in load('head') if 'adapter' in r]
print("rows base",len(b),"head",len(h))
ads=['google','facebook','linkedin','microsoft-personal','github']
def key(r): return (r['adapter'],r['label'])
bd={key(r):r for r in b}; hd={key(r):r for r in h}
assert set(bd)==set(hd) and len(bd)==len(b)
def show(r):
    if r['cell']=='PROFILE': return 'PROFILE(%s)'%json.dumps(r['carried'],ensure_ascii=True)
    if r['cell']=='REFUSED': return 'REFUSED'
    return 'OTHER[%s:%s]'%(r['errName'],r['outcome'][:50])
labels=[]
for r in h:
    if r['adapter']=='google' and r['cls']!='trimset' and r['label'] not in labels: labels.append(r['label'])
print("\n## 18+extra values, per adapter (base -> head)")
for a in ads:
    print("\n###",a)
    for l in labels:
        print(f"{l:12} {show(bd[(a,l)]):34} -> {show(hd[(a,l)])}")
print("\n## github error field (base -> head)")
for r in h:
    if r['cls']=='errfield': print(f"{r['label'][:44]:46} {show(bd[key(r)]):30} -> {show(r)} | warn={r['warn'][:170]}")
fails=[]
for r in h:
    c=r['cls']
    if c in('ws','trimset') and r['label']!='x' and r['cell']!='REFUSED': fails.append(('ws-not-refused',key(r),show(r)))
    if c=='vis' and (r['cell']!='PROFILE' or not r['exact']): fails.append(('vis-altered',key(r),show(r)))
    if c=='nonstr' and (r['cell']!='REFUSED'): fails.append(('nonstr',key(r),show(r)))
    if r['errName']=='TypeError': fails.append(('TypeError',key(r),show(r)))
print("\nHEAD FAIL-condition hits:",len(fails)); [print(' ',f) for f in fails[:30]]
print("\n## counts")
for cls in ['ws','trimset','vis','nonstr','zwsp','odd','errfield']:
    H=[r for r in h if r['cls']==cls]; B=[bd[key(r)] for r in H]
    print(cls,'M=%d'%len(H),'head',dict(collections.Counter(r['cell'] for r in H)),'base',dict(collections.Counter(r['cell'] for r in B)))
print("\n## base datum: trim-removable non-empty string reached profile on base, per adapter")
for a in ads:
    B=[r for r in b if r['adapter']==a and r['cls'] in('ws','trimset') and r['sent']!='']
    print(a,sum(r['cell']=='PROFILE' for r in B),'of',len(B),' exact-carried',sum(bool(r['exact']) for r in B))
print("\n## differing cells base vs head, outside whitespace classes")
print([ (key(r),show(bd[key(r)]),show(r)) for r in h if r['cls'] not in('ws','trimset') and show(bd[key(r)])!=show(r)])
print("\n## refusal-path log hygiene: distinct warn payloads on head")
s=collections.Counter()
for r in h:
    if r['cell']=='REFUSED': s[(r['adapter'],r['warn'][:230])]+=1
for k,v in s.items(): print(v,k)
print("sentinel in any warn:",sum('SENTINEL' in r['warn'] for r in h),"; sentinel in any error text:",sum('SENTINEL' in r['outcome'] for r in h))
print("non-empty whitespace value in warn:",sum(1 for r in h if r['cls'] in('ws','trimset') and r['sent'] and json.dumps(r['sent'])[1:-1] in r['warn'] and r['sent'].strip(' ')!=''))
