# For every removed express.json(...) call and its added boundedJson(...) replacement, compare the option text minus `service`.
import re,subprocess,sys
R='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate126-ks1724-pr1944/repo'
d=subprocess.run(['git','-C',R,'diff','-U0','c70f339063ee','refs/gate/pr1944','--','Blockchain/Dev/services','Blockchain/Dev/packages/shared/src/middleware'],capture_output=True,text=True).stdout
f=None;pairs=[];rem=[];add=[]
def flush():
    global rem,add
    for a,b in zip(rem,add): pairs.append((f,a,b))
    if len(rem)!=len(add): pairs.append((f,'UNPAIRED rem=%d add=%d'%(len(rem),len(add)),str(add)))
    rem=[];add=[]
for line in d.splitlines():
    if line.startswith('diff --git'): flush(); f=line.split(' b/')[-1]
    elif line.startswith('@@'): flush()
    elif line.startswith('-') and not line.startswith('---'):
        m=re.search(r'express\.json\((.*?)\)(?=[)\s;(]|$)',line)
        if m and not line[1:].lstrip().startswith('//'): rem.append(m.group(1))
    elif line.startswith('+') and not line.startswith('+++'):
        m=re.search(r'boundedJson\((\{.*?\})\)',line)
        if m and not line[1:].lstrip().startswith('//'): add.append(m.group(1))
flush()
bad=0
for f,a,b in pairs:
    norm_b=re.sub(r"\s*service:\s*[^,}]+,?\s*","",b).strip()
    norm_b=norm_b.replace('{ ','{').replace(' }','}')
    na=(a.strip() or '{}').replace('{ ','{').replace(' }','}')
    ok = na==norm_b or (na=='{}' and norm_b in ('{}',))
    if not ok: bad+=1
    print('OK ' if ok else 'DIFF', f.replace('Blockchain/Dev/',''), '| before:', a or '()', '| after:', b)
print('pairs',len(pairs),'mismatch',bad)
