import subprocess,hashlib,sys
G=sys.argv[1]; E=f"{G}/evidence"
def run(cwd,cmd,log):
    r=subprocess.run(cmd,cwd=cwd,capture_output=True,text=True); out=r.stdout+r.stderr
    open(f"{E}/{log}",'w').write(out); return r.returncode,out
sha=lambda p:hashlib.sha256(open(p,'rb').read()).hexdigest()
for name in('repo','base'):
    D=f"{G}/{name}/Blockchain/Dev"; A=f"{D}/services/auth"; N='head' if name=='repo' else 'base'
    tsc=f"{D}/node_modules/typescript/bin/tsc"
    rc,o=run(A,['node',tsc,'--noEmit','-p','.'],f'q5_tsc_{N}.txt'); print(N,'tsc rc',rc,'errors',o.count('error TS'))
    rc,o=run(D,['node','scripts/typecheck-tests/check.cjs','services/auth'],f'q5_ratchet_{N}.txt'); print(N,'ratchet rc',rc); print('\n'.join(o.strip().splitlines()[-6:])[:700])
D=f"{G}/repo/Blockchain/Dev"; A=f"{D}/services/auth"
tf=f"{A}/src/__tests__/ks1858-google-refuses-a-token-answer-without-an-access-token.test.ts"; b=sha(tf); s=open(tf).read()
open(tf,'w').write(s+"\nexport const gate211Planted: number = 'not a number';\n"); assert sha(tf)!=b
try:
    rc,o=run(D,['node','scripts/typecheck-tests/check.cjs','services/auth'],'q5_ratchet_planted.txt'); print('planted ratchet rc',rc,'TS2322 lines',[l[:170] for l in o.splitlines() if 'TS2322' in l and 'ks1858-google' in l][:2])
finally: open(tf,'w').write(s)
assert sha(tf)==b; print('ratchet plant restored sha256-equal')
files=[f"src/providers/social/{x}.ts" for x in('google','facebook','linkedin','microsoft-personal','github')]+[f"src/__tests__/{x}-refuses-a-token-answer-without-an-access-token.test.ts" for x in('ks1792-github','ks1858-facebook','ks1858-google','ks1858-linkedin','ks1858-microsoft-personal')]
es=f"{D}/node_modules/eslint/bin/eslint.js"
rc,o=run(A,['node',es]+files,'q5_eslint_head.txt'); print('eslint rc',rc,'bytes',len(o)); print(o[-400:])
g=f"{A}/src/providers/social/google.ts"; b=sha(g); s=open(g).read()
open(g,'w').write(s+"\nvar gate211Planted = 1;\nexport { gate211Planted };\n"); assert sha(g)!=b
try:
    rc,o=run(A,['node',es]+files,'q5_eslint_planted.txt'); print('eslint planted rc',rc,[l.strip()[:120] for l in o.splitlines() if 'no-var' in l])
finally: open(g,'w').write(s)
assert sha(g)==b; print('eslint plant restored sha256-equal')
