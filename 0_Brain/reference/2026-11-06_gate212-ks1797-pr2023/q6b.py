import subprocess,sys,json,hashlib,os
G=sys.argv[1]; R=G+'/repo'; D=R+'/Blockchain/Dev'; A=D+'/services/auth'; BIN=D+'/node_modules/.bin'
def run(cmd,cwd,**k):
    r=subprocess.run(cmd,cwd=cwd,capture_output=True,text=True,**k); return r.returncode,r.stdout+r.stderr
for T in('base','repo'):
    a=f'{G}/{T}/Blockchain/Dev/services/auth'
    rc,o=run([BIN+'/vitest','run','src/__tests__/ks949-platform-admin-seed-identity.test.ts'],a)
    print(T,'ks949 alone rc',rc,[l.strip() for l in o.splitlines() if 'Tests  ' in l])
    d=json.load(open(f'{G}/evidence/q6_whole_cwd_{T}.json'))
    print(T,'failed files',[f['name'].split('/')[-1] for f in d['testResults'] if f.get('status')=='failed'])
rc,o=run([BIN+'/tsc','--noEmit','-p','.'],A); print('tsc service rc',rc,o[-200:])
print(open(A+'/package.json').read().count('test-types'))
# eslint on both changed .ts
F=['services/auth/src/routes/oauth.ts','services/auth/src/__tests__/ks1797-authorize-post-refuses-an-array-state-or-code-challenge.test.ts']
rc,o=run([BIN+'/eslint',*F],D); print('eslint rc',rc,o[-400:])
t=D+'/'+F[1]; src=open(t).read(); sha=hashlib.sha256(src.encode()).hexdigest()
open(t,'w').write(src+"\ndebugger;\n")
rc,o=run([BIN+'/eslint',F[1]],D); print('eslint planted rc',rc,[l for l in o.splitlines() if 'debugger' in l.lower() or 'error' in l.lower()][:3])
open(t,'w').write(src); print('restored',hashlib.sha256(open(t).read().encode()).hexdigest()==sha)
