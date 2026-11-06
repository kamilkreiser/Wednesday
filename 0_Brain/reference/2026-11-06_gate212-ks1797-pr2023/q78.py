import subprocess,sys,hashlib,os
G=sys.argv[1]; R=G+'/repo'; D=R+'/Blockchain/Dev'
HEAD='5c828fa98931d605e69beec75565d0f548ee1377'; BASE='1b1b65c7415ff02b9e3b44e83b62d9a609adfe8b'
def run(cmd,cwd,**k):
    r=subprocess.run(cmd,cwd=cwd,capture_output=True,text=True,**k); return r.returncode,r.stdout+r.stderr
T=D+'/services/auth/src/__tests__/ks1797-authorize-post-refuses-an-array-state-or-code-challenge.test.ts'
print('--- test-types head'); rc,o=run(['node','scripts/typecheck-tests/check.cjs','services/auth'],D); print('rc',rc,o[-500:])
s=open(T).read(); sh=hashlib.sha256(s.encode()).hexdigest()
open(T,'w').write(s+"\nconst gate212planted: number = 'not a number'; export { gate212planted };\n")
rc,o=run(['node','scripts/typecheck-tests/check.cjs','services/auth'],D); print('planted rc',rc,[l for l in o.splitlines() if 'gate212' in l or 'TS2322' in l or 'new' in l.lower()][:5])
open(T,'w').write(s); print('restored',hashlib.sha256(open(T).read().encode()).hexdigest()==sh)
print('--- docs check')
for t in('repo','base'):
    r=G+'/'+t; rc,o=run(['node','Blockchain/Dev/scripts/docs-fragments.mjs','check'],r); print(t,'rc',rc,o[-900:])
F=R+'/Projects Documents/fragments/flow/KS-1797-post-authorize-refuses-an-array-state-or-code-challenge.html'
s=open(F).read(); sh=hashlib.sha256(s.encode()).hexdigest()
open(F,'w').write(s+"\n<div class=\"note\"><h2>unbalanced</h2>\n")
rc,o=run(['node','Blockchain/Dev/scripts/docs-fragments.mjs','check'],R); print('planted rc',rc,o[-500:])
open(F,'w').write(s); print('restored',hashlib.sha256(open(F).read().encode()).hexdigest()==sh)
rc,o=run(['node','Blockchain/Dev/scripts/docs-fragments.mjs','check'],R); print('after restore rc',rc)
print('--- merge'); rc,o=run(['git','merge-tree','--write-tree',BASE,HEAD],R); print('merge-tree rc',rc,o.strip()); tree=o.strip().splitlines()[0]
print('head tree',run(['git','rev-parse',HEAD+'^{tree}'],R)[1].strip())
print('merge-base',run(['git','merge-base',BASE,HEAD],R)[1].strip()); four=set(run(['git','diff','--name-only',BASE,HEAD],R)[1].split('\n'))-{''}
rng=set(run(['git','diff','--name-only',BASE,BASE],R)[1].split('\n'))-{''}; print('develop range from merge base paths',len(rng),'shared',len(four&rng))
other='Blockchain/Dev/services/auth/package.json'; print('planted control intersection (four + develop path vs range containing that path):',sorted((four|{other})&{other}))
print('--- other local PR-branch tips')
refs=[l.split('\t') for l in run(['git','ls-remote','origin','refs/heads/*'],R)[1].splitlines()]
print('local branch refs',len(refs))
hit=[];nobj=0;dis=0;seen=set();conf=[]
for sha,ref in refs:
    if sha in seen: continue
    seen.add(sha)
    if run(['git','cat-file','-t',sha],R)[0]!=0: nobj+=1; continue
    if run(['git','merge-base','--is-ancestor',sha,BASE],R)[0]==0: continue
    names=set(run(['git','diff','--name-only',BASE+'...'+sha],R)[1].split('\n'))-{''}
    dis+=1
    i=names&four
    if i: hit.append((ref,sha[:12],sorted(i)))
print('unmerged tips with objects',dis,'objects missing',nobj,'touching the four:',len(hit))
for h in hit: print(h, run(['git','log','-1','--format=%cI',h[1]],R)[1].strip())
for ref,sha in [('ks-1858 social','1a0fa7c23b245c1b6a9fa428908ddefe26ab27b0'),('ks-1858 auth','6b867a532ee7307ec5e32c1f18ac408f05b8b25a')]:
    n=set(run(['git','diff','--name-only',BASE+'...'+sha],R)[1].split('\n'))-{''}; print(ref,sha[:12],'files',len(n),'shared with four',sorted(n&four),'oauth.ts?',any(x.endswith('routes/oauth.ts') for x in n),sorted(n)[:6])
