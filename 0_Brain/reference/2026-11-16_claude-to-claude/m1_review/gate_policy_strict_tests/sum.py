import re,sys
p=f=i=0;src='';name='';pol=[]
for l in open(sys.argv[1]):
    m=re.search(r'Running (.+?) \((.*?)\)\s*$',l)
    if m: src=m.group(1); name=m.group(2).rsplit('/',1)[-1].rsplit('-',1)[0]
    m=re.search(r'test result: \w+\. (\d+) passed; (\d+) failed; (\d+) ignored',l)
    if m:
        a,b,c=map(int,m.groups()); p+=a;f+=b;i+=c
        if 'coagent_policy' in name or name in ('q01_gate_attacks','r2_gate_attacks','r3_gate_attacks','r4_gate_attacks','r5b_bound_probe','r5b_r4_regressions','r5b_shell_t3') or name.startswith(('t0','t1','qa_','r6')): pol.append((name,src,a,b))
print('workspace passed',p,'failed',f,'ignored',i)
print('policy-ish', sum(x[2] for x in pol), sum(x[3] for x in pol))
for x in pol: print(x[0],x[2],x[3])
