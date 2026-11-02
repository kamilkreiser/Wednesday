import os, re, subprocess, sys, hashlib
N='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night'
R='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate131-ks1868-pr1949/repo'
def parse(text):
    files={}; cur=None
    for ln in text.split('\n'):
        if ln.startswith('diff --git '):
            cur=ln.split(' b/',1)[1]; files[cur]=[]; continue
        if cur is None: continue
        if ln.startswith('+++') or ln.startswith('---') or ln.startswith('index ') or ln.startswith('new file') or ln.startswith('@@'): continue
        if ln.startswith('```'): cur=None; continue
        if ln.startswith('+') or ln.startswith('-'): files[cur].append(ln)
    return files
held={}
for p in ['P1','P2','P3','P4']:
    f=[x for x in os.listdir(N) if re.search('O82-'+p+'_',x,re.I)][0]
    t=open(os.path.join(N,f)).read()
    body=t[t.index('```diff')+7:]
    for k,v in parse(body).items():
        held.setdefault(k,[]).extend([(p,l) for l in v])
pr=parse(subprocess.run(['git','-C',R,'diff','3e688ee239f2...d2b49790d72c'],capture_output=True,text=True).stdout)
allok=True
for k in sorted(set(held)|set(pr)):
    h=[l for _,l in held.get(k,[])]; q=pr.get(k,[])
    srcs=sorted(set(p for p,_ in held.get(k,[])))
    same = h==q
    allok &= same
    print(('SAME ' if same else 'DIFF ')+f'{k.split("/")[-1]:90s} held({",".join(srcs) or "-"}) +{sum(1 for l in h if l[0]=="+")}/-{sum(1 for l in h if l[0]=="-")}  pr +{sum(1 for l in q if l[0]=="+")}/-{sum(1 for l in q if l[0]=="-")}  sha(held)={hashlib.sha256(chr(10).join(h).encode()).hexdigest()[:10]} sha(pr)={hashlib.sha256(chr(10).join(q).encode()).hexdigest()[:10]}')
print('ALL_IDENTICAL' if allok else 'MISMATCH')
