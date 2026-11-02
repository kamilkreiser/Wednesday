# Mechanical judge over the gate-112 route probe recordings. usage: judge.py <logs dir> [fmt ...]; rc 1 on any fail.
import json, sys, re
L=sys.argv[1]; FMTS=sys.argv[2:] or ['test','production']
def load(p):
    recs={}; extra={}
    for line in open(p):
        r=json.loads(line)
        if 'cell' in r: recs[(r['cell'],r['kind'])]=r
        else: extra.update(r)
    return recs, extra
def norm(r):
    s=r['store']
    return {'status':r['status'],'body':r['body'],'keys':sorted((v['active'],v['usage']) for v in s['keys'].values()),
            'audit':s['audit'],'events':sorted(s['events'].values()),'mem':sorted(s['mem'].values()),
            'usageAttempts':r['usageAttempts'],'writes':[re.sub(r'key_\w{4}','key_*',w) for w in r['committedWrites']],
            'unhandled':r['unhandled'],'uncaught':r['uncaught'],'validateAfter':r.get('validateAfter')}
fails=[]; n=0
def check(cond,msg):
    global n; n+=1
    if not cond: fails.append(msg)
UNREAD=['revokedProxy','getterThrows']
for fmt in FMTS:
    B,bx=load(f'{L}/g112_probe_base_{fmt}.jsonl'); H,hx=load(f'{L}/g112_probe_head_{fmt}.jsonl')
    check(bx['positive_control']['initDb'] and hx['positive_control']['isDbAvailable'],f'{fmt} positive control')
    check(B[('control',None)]['validate'] is True and H[('control',None)]['validate'] is True,f'{fmt} control validate true (judge can see valid:true)')
    check(H[('control',None)]['afterRevoke']=={'valid':False,'reason':'Key revoked'},f'{fmt} control revoke works')
    check(hx['network']['outbound']==[] and bx['network']['outbound']==[],f'{fmt} no outbound network')
    cells=sorted({c for c,k in H if k})
    kinds=sorted({k for c,k in H if k})
    check(len(cells)==11 and len(kinds)==11,f'{fmt} grid {len(cells)}x{len(kinds)}')
    for tag,R in (('base',B),('head',H)):
        for (c,k),r in R.items():
            if k is None: continue
            b=r['body'] if isinstance(r['body'],dict) else {}
            # (a) fail closed
            if c!='validate-usage': check(b.get('valid') is not True,f'{fmt} {tag} {c}/{k} answered valid:true')
            if c=='validate-storedrevoked': check(r['usageAttempts']==0 and b.get('valid') is not True,f'{fmt} {tag} {c}/{k} usage reached on a revoked key')
            if c=='mint': check(not b.get('keyIssued') and r['store']['keys']=={} and r['store']['mem']=={} and r['status']!=201,f'{fmt} {tag} mint/{k} issued or stored a key')
            if c=='revoke':
                active=[v['active'] for v in r['store']['keys'].values()]
                check(not (any(active) and (b.get('success') is True or r['status']==200)),f'{fmt} {tag} revoke/{k} reported success without persisting')
                va=r.get('validateAfter')
                check(not (isinstance(va,dict) and va.get('valid') is True),f'{fmt} {tag} revoke/{k} key still valid after a refused revoke')
            if c=='validate-usage': check(not (b.get('valid') is True and r['store']['keys'] and not all(v['active'] for v in r['store']['keys'].values())),f'{fmt} {tag} usage valid:true on inactive row')
    for c in cells:
        # (b) no regression for ordinary values; unreadable at head equals ordinary at head
        for k in ['ordinary','ordinary08006','plainString']:
            check(norm(B[(c,k)])==norm(H[(c,k)]),f'{fmt} {c}/{k} base != head')
        for k in UNREAD:
            # Declared exception (measured, base == head, disclosed by the author as O74-P1): at the admin-scopes GET an Error
            # whose message getter throws passes the instanceof guard and crashes the SHARED errorHandler -> Express default 500.
            if c=='scopes' and k=='getterThrows':
                check(norm(H[(c,k)])==norm(B[(c,k)]),f'{fmt} scopes/getterThrows head != base'); continue
            check(norm(H[(c,k)])==norm(H[(c,'ordinary')]),f'{fmt} {c}/{k} head != head ordinary: {norm(H[(c,k)])} vs {norm(H[(c,"ordinary")])}')
            # validate-storedrevoked never reaches the failing statement; scopes' constant goes to the shared errorHandler's logger (not captured)
            if c not in ('validate-storedrevoked','scopes'): check(H[(c,k)]['unreadableConst'],f'{fmt} {c}/{k} head did not log the constant')
            check(H[(c,k)]['valueLeak']==0,f'{fmt} {c}/{k} head logged a thrown value')
        if c=='scopes': check(norm(H[(c,'getterThrows08006')])==norm(B[(c,'getterThrows08006')]),f'{fmt} scopes/getterThrows08006 head != base')
        else: check(norm(H[(c,'getterThrows08006')])==norm(H[(c,'ordinary08006')]),f'{fmt} {c}/getterThrows08006 head != head ordinary08006')
        # hostile non-string messages: head must equal base (no regression); reported, not required to be fixed
        for k in ['nullProto','msgSymbol','msgRevokedProxy','msgBigInt','msgToStringThrows']:
            check(norm(H[(c,k)])==norm(B[(c,k)]),f'{fmt} {c}/{k} hostile shape changed base -> head')
print('checks',n,'fails',len(fails))
for f in fails: print('FAIL',f)
sys.exit(1 if fails else 0)
