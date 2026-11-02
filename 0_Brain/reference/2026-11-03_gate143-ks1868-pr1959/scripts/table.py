import json,re,sys
W='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate143-ks1868-pr1959'
rows=[json.loads(l) for l in open(W+'/logs/probe_matrix.jsonl')]
def desc(r):
    ls=[]
    for l in r['lines']:
        if 'raw' in l:
            m=re.search(r'\] (\w+): (.*)$',l['raw']); ls.append(m.group(1)+' '+m.group(2)[:70] if m else l['raw'])
        else: ls.append("%s %s err=%s%s"%(l['level'],l['message'][:28],json.dumps(l.get('error')),'' if l['hasErrorKey'] else '(nokey)'))
    ls=[x for x in ls if 'EventBus initialised' not in x]
    return "ret=%s threw=%s boot=%s unc=%s xadd=%s | %s"%(r['returned'],r['threw'],r['boot'][:14],r['uncaught'],r['publishXadds'],' ; '.join(ls) or 'NO LINE')
d={}
for r in rows: d.setdefault((r['nodeEnv'],r['site'],r['kase']),{})[r['variant']]=r
same=diff=0
for k,v in d.items():
    b,h=desc(v['base']),desc(v['head'])
    s=(b==h); same+=s; diff+=not s
    print(('SAME ' if s else 'DIFF ')+'/'.join(k)); print('   base: '+b)
    if not s: print('   head: '+h)
print('SAME',same,'DIFF',diff)
