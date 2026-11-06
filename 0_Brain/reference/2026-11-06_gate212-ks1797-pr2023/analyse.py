import json,collections,sys
E=sys.argv[1]
def load(p):
    return {json.dumps(r['key'],sort_keys=True):r for r in map(json.loads,open(p))}
B=load(E+'/table_base.jsonl');H=load(E+'/table_repo.jsonl')
assert B.keys()==H.keys()
ENV='{"success":false,"error":{"code":"BAD_REQUEST","message":"invalid_request","description":"state and code_challenge must each be a single string"}}'
STR={'absent','xyz','empty'}
ns_tot=ns_ok=st_tot=st_ok=0;bad=[];diff=[];tq=[]
for k,h in H.items():
    K=json.loads(k)
    if K['q']=='q4':continue
    b=B[k]
    if K['q']=='both': nonstr=True
    else: nonstr=K['shape'] not in STR
    if nonstr:
        ns_tot+=1
        ok=h['status']==400 and h['text']==ENV and h['location'] is None and h['setCookie'] is None and all(v==0 for v in h['calls'].values())
        ns_ok+=ok
        if not ok:bad.append((K,h))
    else:
        st_tot+=1
        same=all(h[f]==b[f] for f in('status','text','location','setCookie','ctype','calls','mintArg','getAppArg'))
        st_ok+=same
        if not same:diff.append((K,b,h))
print(f'HEAD non-string rows refused byte-identically, all counts 0: {ns_ok} of {ns_tot}')
print(f'HEAD string/absent rows identical to BASE (status,body,Location,cookie,ctype,6 counts,mint arg,lookup arg): {st_ok} of {st_tot}')
for x in bad[:10]:print('BAD',x)
for x in diff[:10]:print('DIFF',x)
print('distinct head bodies among non-string:',len({H[k]['text'] for k in H if json.loads(k)['q']!='q4' and (json.loads(k)['q']=='both' or json.loads(k)['shape'] not in STR)}))
# what mattered: distinct string/absent outcomes
print('head string/absent outcome mix',collections.Counter(H[k]['status'] for k in H if json.loads(k)['q'] not in('q4','both') and json.loads(k)['shape'] in STR))
# base behaviour per non-string shape
print('\nBASE per shape (mint-capable cell: valid creds, u0_nocode, JSON unless form; client conf; and pub):')
def row(K):return B[json.dumps(K,sort_keys=True)]
for q,comp,encs in(('state','chal',('json','form')),('cc','S256',('json','form'))):
  for enc in encs:
    shapes=[s for s in {json.loads(k)['shape'] for k in B if json.loads(k)['q']==q and json.loads(k)['enc']==enc}]
    order=['absent','xyz','empty','arr_ab','arr_a','arr_empty','obj_empty','obj_ab','rep_ab','br_a','null','0','123','true','false']
    for s in [o for o in order if o in shapes]:
      out=[]
      for act in('deny','approve','absent'):
        for cl in('client-conf','client-pub'):
          r=row(dict(q=q,enc=enc,shape=s,comp=comp,action=act,client=cl,creds='valid',mfa='u0_nocode'))
          h=H[json.dumps(dict(q=q,enc=enc,shape=s,comp=comp,action=act,client=cl,creds='valid',mfa='u0_nocode'),sort_keys=True)]
          loc=(r['location'] or '').replace('https://app.example.com/cb','')
          m=r['mintArg'].get('codeChallenge','<undef>') if r['mintArg'] else None
          out.append(f"{act[:3]}/{cl[7:11]}:{r['status']} {loc or json.loads(r['text'])['error']['description'][:28] if r['status']!=302 or loc else ''} mint={r['calls']['mint']}{' cc='+json.dumps(m) if q=='cc' and r['calls']['mint'] else ''} ->H{h['status']}")
      print(f"[{q} {enc} {s}] "+' | '.join(out))
# Enumeration on BASE vs HEAD
print('\nQ4 (other params) base vs head diffs:')
q4d=0;q4=0
for k,h in H.items():
    K=json.loads(k)
    if K['q']!='q4':continue
    q4+=1
    b=B[k]
    if any(h[f]!=b[f] for f in('status','text','location','setCookie','calls','mintArg','getAppArg')):
        q4d+=1;print('DIFF',K,b['status'],h['status'])
print(f'Q4 rows {q4}, differ {q4d}')
agg=collections.defaultdict(collections.Counter)
for k,h in H.items():
    K=json.loads(k)
    if K['q']!='q4':continue
    d=''
    if h['status']!=302:
        try:d=json.loads(h['text'])['error']['message']
        except:d='?'
    elif 'error=' in h['location']:d='access_denied'
    else:d='CODE'
    agg[(K['param'],K['shape'],'strict' if K['strict'] else 'perm',K['action'],K['client'][7:11])][f"{h['status']} {d}"]+=1
for a in sorted(agg,key=str):print(a,dict(agg[a]))
# mint args with non-string fields in q4
print('\nQ4 non-string values reaching createAuthorizationCode (head):')
seen=collections.Counter()
for k,h in H.items():
    K=json.loads(k)
    if K['q']!='q4' or not h['mintArg']:continue
    a=h['mintArg']
    for f,v in a.items():
        if v is not None and not isinstance(v,str):seen[(K['param'],K['shape'],K['strict'],f,json.dumps(v))]+=1
for s,c in sorted(seen.items(),key=str):print(s,c)
print('Q4 500s head:',collections.Counter((json.loads(k)['param'],json.loads(k)['shape'],json.loads(k)['action']) for k,h in H.items() if json.loads(k)['q']=='q4' and h['status']==500))
