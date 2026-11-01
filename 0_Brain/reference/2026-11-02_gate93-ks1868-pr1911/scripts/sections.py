# Compare HEAD's auth.ts -U0 change lines (and the 3 new test files) to the operator's held sections (runs WITHOUT -control/-r2).
import subprocess,re,sys
R='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate93-ks1868-pr1911/repo'
RU='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o50_'
P={'p1':'p1_auth_register_publish_event_unreadable_throw','p2':'p2_auth_login_publish_event_unreadable_throw','p3':'p3_auth_reset_password_revoke_unreadable_throw'}
F='Blockchain/Dev/services/auth/src/routes/auth.ts'
def g(*a): return subprocess.run(['git','-C',R]+list(a),capture_output=True,text=True).stdout
d=g('diff','-U0','refs/gate/develop','refs/gate/pr1911','--',F)
hunks=re.split(r'^(?=@@)',d,flags=re.M)[1:]
head_changes=[]
for h in hunks:
    head_changes.append([l for l in h.splitlines()[1:] if l[:1] in '+-'])
allhead=[l for h in head_changes for l in h]
secs={}
for k,v in P.items():
    s=open(RU+v+'/out.md.checker/section_1.diff').read()
    secs[k]=[l for l in s.splitlines() if l[:1] in '+-' and not l.startswith(('+++','---'))]
union=secs['p1']+secs['p2']+secs['p3']
print('head -U0 hunks:',len(hunks),'change lines',len(allhead),'(-%d +%d)'%(sum(l[0]=='-' for l in allhead),sum(l[0]=='+' for l in allhead)))
for k in P: print(k,'section change lines',len(secs[k]))
print('multiset head == union(sections):',sorted(allhead)==sorted(union))
# order-sensitive: head file order is register(p1), login(p2), reset(p3)
print('ordered head == p1+p2+p3:',allhead==union)
# landing: for each -U0 hunk, find the enclosing authRoutes.post at head
head=g('show','refs/gate/pr1911:'+F).splitlines()
for h in hunks:
    m=re.match(r'@@ -\d+(?:,\d+)? \+(\d+)',h); n=int(m.group(1))
    route=None
    for i in range(n-1,-1,-1):
        mm=re.match(r"authRoutes\.(post|get|put|delete)\('([^']+)'",head[i])
        if mm: route=(i+1,mm.group(2)); break
    print('hunk at head line',n,'enclosing route',route)
# test files
for k,v in P.items():
    s2=open(RU+v+'/out.md.checker/section_2.diff').read()
    m=re.search(r'^\+\+\+ b/(\S+)',s2,flags=re.M); path=m.group(1)
    body=[l[1:] for l in s2.splitlines() if l.startswith('+') and not l.startswith('+++')]
    hb=g('show','refs/gate/pr1911:'+path).splitlines()
    print(k,'test',path.split('/')[-1],'section_2 == head file:',body==hb,len(body),len(hb))
