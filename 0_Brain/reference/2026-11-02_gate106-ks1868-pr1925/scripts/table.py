import json,collections,re
TS=re.compile(r'\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d\.\d+Z')
L='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate106-ks1868-pr1925/logs/'
def load(p): return {(r['route'],r['mode'],r['kind'],r['who']):r for r in (json.loads(l) for l in open(L+p))}
B=load('probe_base.jsonl'); H=load('probe_head.jsonl')
UN=('revokedProxy','throwingGetter','getterThrowsProxy')
def sig(r): return dict(status=r['status'],ctype=r['ctype'],body=TS.sub('<ts>',r['body']),state=r['state'],ctx=[e[0] for e in r['errLines']],warn=[w[0] for w in r['warnLines']],esc=bool(r['escaped']))
ok=bad=pre=0; rows=collections.OrderedDict(); leaks=[]
assert set(B)==set(H), 'cell sets differ'
for k,h in H.items():
    route,mode,kind,who=k; b=B[k]
    rows.setdefault((route,mode),{})[(kind,who)]=(b,h)
    if kind in UN:
        o=H[(route,mode,'ordinaryError',who)]
        so,su=sig(o),sig(h)
        same = so==su and (not h['errLines'] or all(e[1]=={'error':'unreadable thrown value'} for e in h['errLines']) or 'proxy' in json.dumps(h['errLines']) or 'getter' in json.dumps(h['errLines']))
        # strict: when the PR's catch is the one logging, the logged value must be the constant
        if not same:
            b_eq = sig(b)==sig(h) and b['errLines']==h['errLines']
            if b_eq and not h['escaped']:
                print('PRE-EXISTING unreadable!=ordinary, base==head',k,'\n  ord',so,o['errLines'],'\n  unr',su,h['errLines']); pre+=1; continue
            print('DIFF unreadable!=ordinary',k,'\n  ord',so,'\n  unr',su)
    else:
        same = sig(b)==sig(h) and b['errLines']==h['errLines']
        tag='OK' if same else 'DIFF'
        if not same: print('DIFF base!=head',k,'\n  base',sig(b),b['errLines'],'\n  head',sig(h),h['errLines'])
    ok+=same; bad+=(not same)
    if any(h['leak'].values()) and not (mode=='none'): leaks.append((k,{w:v for w,v in h['leak'].items() if v}))
    if h['logHasHolder'] and kind in UN: leaks.append((k,'LOG holder/org/caller'))
print('CHECK ok',ok,'bad',bad,'pre-existing(base==head)',pre,'of',len(H))
print('LEAKS (non-success cells, response bodies; and error-log holder/org/caller):',leaks if leaks else 'none')
def s(r):
    st=r['status']; bd=r['body']
    try:
        j=json.loads(bd); bd=(j.get('error',{}).get('message') if isinstance(j.get('error'),dict) else j.get('error')) if 'error' in j else ('verified=%s'%j.get('verified') if 'verified' in j else 'ok')
    except Exception: bd=bd[:20]
    e=[x[1].get('error') if isinstance(x[1],dict) else x[1] for x in r['errLines']]
    return f"{st} {bd} w={r['state']['healWrites']} q={r['state']['queries']} log={e} esc={r['escaped']}"
print('\nTABLE route | mode | who || ordinaryError base / head || unreadable base / head (per kind)')
for (route,mode),d in rows.items():
    whos=sorted(set(w for (_,w) in d))
    for who in whos:
        if mode=='none':
            b,h=d[('none',who)]; print(f"{route} | success | {who}: base {s(b)} | head {s(h)}"); continue
        b,h=d[('ordinaryError',who)]; print(f"{route} | {mode} | {who}\n   ordinary base {s(b)}\n   ordinary head {s(h)}")
        for k in UN:
            b,h=d[(k,who)]; print(f"   {k:18} base {s(b)}\n   {'':18} head {s(h)}")
