"""measure.py <golden> <svc> <runner> <testrel> [tamper-prod-rel line from to]: apply golden in scratch tree, run test (green expected), plant tamper, run (red expected), restore tamper, revert golden."""
import sys,subprocess,os
S='/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/52e2783b-09e1-49d1-9200-c6e9ede3ba54/scratchpad/op16/src'
D=S+'/Blockchain/Dev/'
g,svc,runner,test=sys.argv[1:5]
def run(): 
    cmd=['npx','vitest','run',test] if runner=='vitest' else ['npx','jest',test]
    r=subprocess.run(cmd,cwd=D+svc,capture_output=True,text=True); o=r.stdout+r.stderr
    return r.returncode,'\n'.join(o.strip().split('\n')[-25:])
def git(*a): 
    r=subprocess.run(['git']+list(a),cwd=S,capture_output=True,text=True); return r.returncode,r.stderr
print('apply',git('apply',g))
try:
    print('=== GREEN at tip+golden'); rc,o=run(); print('rc',rc); print(o)
    if len(sys.argv)>5:
        prod,line,frm,to=sys.argv[5:9]
        p=D+svc+'/'+prod; orig=open(p,encoding='utf-8').read(); L=orig.split('\n'); i=int(line)-1
        assert L[i]==frm,(L[i],frm); L[i]=to
        try:
            open(p,'w',encoding='utf-8').write('\n'.join(L)); print('=== TAMPER'); rc,o=run(); print('rc',rc); print(o)
        finally: open(p,'w',encoding='utf-8').write(orig)
finally: print('revert',git('apply','-R',g)); print([l for l in subprocess.run(['git','status','--short'],cwd=S,capture_output=True,text=True).stdout.split(chr(10)) if l and 'node_modules' not in l] or 'tree clean')
