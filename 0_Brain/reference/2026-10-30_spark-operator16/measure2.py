"""measure2.py <golden> <svc> <runner> <testrel> <prodrel> : code_patch2 check: golden applied -> GREEN; product file restored to tip content (tests kept) -> expect RED; revert."""
import sys,subprocess
S='/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/52e2783b-09e1-49d1-9200-c6e9ede3ba54/scratchpad/op16/src'
D=S+'/Blockchain/Dev/'
TIP='7152ac669d2d6af08be5b9dcd35132818377155d'
g,svc,runner,test,prod=sys.argv[1:6]
def run():
    cmd=['npx','vitest','run',test] if runner=='vitest' else ['npx','jest',test]
    r=subprocess.run(cmd,cwd=D+svc,capture_output=True,text=True); o=r.stdout+r.stderr
    return r.returncode,[l for l in o.split('\n') if ('FAIL' in l or 'Tests ' in l or 'Test Files' in l or '✓' in l or '✗' in l or '×' in l or '●' in l)][:12]
def git(*a):
    r=subprocess.run(['git']+list(a),cwd=S,capture_output=True,text=True); return r.returncode,r.stdout,r.stderr
print('apply',git('apply',g)[::2])
try:
    print('GREEN golden:',run())
    tipc=git('show',TIP+':Blockchain/Dev/'+prod)[1]
    p=D+prod; cur=open(p,encoding='utf-8').read(); open(p,'w',encoding='utf-8').write(tipc)
    try: print('RED (product at tip, new test kept):',run())
    finally: open(p,'w',encoding='utf-8').write(cur)
finally:
    print('revert',git('apply','-R',g)[::2])
    print([l for l in git('status','--short')[1].split('\n') if l and 'node_modules' not in l] or 'tree clean')
