# Gate 135's corpus_cmp.py (same norm + alignment), re-pointed; argv: LBL [pairmap]
import json, re, sys, collections, difflib
G='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate140-ks1725-pr1953-delta'
LBL=sys.argv[1]; PM=len(sys.argv)>2
b=json.load(open(G+'/logs/corpus_base_%s.json'%LBL)); h=json.load(open(G+'/logs/corpus_head_%s.json'%LBL))
inp=json.load(open(G+'/logs/corpus_base_%s.inputs.json'%LBL))
def norm(t):
    t=re.sub(r'//[^\n]*','',t); t=re.sub(r'/\*.*?\*/','',t,flags=re.S)
    t=t.replace('.guid(','.uuid(').replace('z.record(z.string(), ','z.record(')
    t=t.replace('zod3NativeEnum(','z.nativeEnum(')  # G140: the F4 helper pairs with the raw call it replaced
    t=re.sub(r"pattern: '\^\[a-f0-9\]\{64\}\$',?",'',t)
    t=re.sub(r'\.openapi\(\{\s*\}\)','',t)
    return re.sub(r'\s+','',t)
def byfile(d):
    f=collections.defaultdict(list)
    for k,v in d.items(): f[k.split('#')[0]].append((int(k.split('#')[1]),k))
    return {x:[k for _,k in sorted(v)] for x,v in f.items()}
bf,hf=byfile(b),byfile(h)
pairs=[]; unpaired=[]
for f in sorted(set(bf)|set(hf)):
    bl=bf.get(f,[]); hl=hf.get(f,[])
    sm=difflib.SequenceMatcher(None,[norm(b[k]['text']) for k in bl],[norm(h[k]['text']) for k in hl],autojunk=False)
    for tag,i1,i2,j1,j2 in sm.get_opcodes():
        if tag=='equal': pairs+= [(bl[i],hl[j],True) for i,j in zip(range(i1,i2),range(j1,j2))]
        elif tag=='replace' and i2-i1==j2-j1: pairs+= [(bl[i],hl[j],False) for i,j in zip(range(i1,i2),range(j1,j2))]
        else: unpaired.append((tag,[b[k]['text'][:150] for k in bl[i1:i2]],[h[k]['text'][:150] for k in hl[j1:j2]]))
print('pairs',len(pairs),'text-equal',sum(1 for p in pairs if p[2]))
if PM:
    json.dump({kh:kb for kb,kh,_ in pairs},open(G+'/logs/pairmap_%s.json'%LBL,'w')); print('pairmap written'); sys.exit(0)
for p in pairs:
    if not p[2]: print('  TEXT-CHANGED',p[0],'|',re.sub(r'\s+',' ',b[p[0]]['text'])[:160],'||',re.sub(r'\s+',' ',h[p[1]]['text'])[:160])
for u in unpaired: print('  UNPAIRED',u)
skipped=collections.Counter(); ncells=0; classes=collections.Counter(); rows=[]; asym=[]
for kb,kh,_ in pairs:
    bc=b[kb]['cells']; hc=h[kh]['cells']
    if bc is None or hc is None:
        if (bc is None)!=(hc is None): asym.append((kb,b[kb]['err'],h[kh]['err']))
        skipped[(b[kb]['err'] or '')[:60]]+=1; continue
    for i,(x,y) in enumerate(zip(bc,hc)):
        ncells+=1
        if x==y: continue
        cls=('ACC->REJ' if x.startswith('OK') and y.startswith('ERR') else 'REJ->ACC' if x.startswith('ERR') and y.startswith('OK') else 'OK-DATA' if x.startswith('OK') else 'ERR-BODY' if x.startswith('ERR') and y.startswith('ERR') else 'THROW')
        classes[cls]+=1
        rows.append({'kind':('spec' if (kb.split('#')[0].endswith('.openapi.ts') or '/shared/src/openapi/' in kb) else 'frontend' if '/frontend/' in kb else 'product'),'id':kb,'line':b[kb]['line'],'hline':h[kh]['line'],'cls':cls,'input':inp[kb][i],'base':x,'head':y,'text':re.sub(r'\s+',' ',b[kb]['text'])[:240]})
print('cells',ncells,'diff classes',dict(classes)); print('by kind', collections.Counter((r['kind'],r['cls']) for r in rows))
print('evaluated on one side only',len(asym)); [print('  ',a) for a in asym]
print('not evaluated (both sides):',sum(skipped.values()), skipped.most_common(12))
json.dump(rows,open(G+'/logs/corpus_diffs_%s.json'%LBL,'w'),indent=0)
