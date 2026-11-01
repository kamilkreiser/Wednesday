import hashlib, subprocess
W='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-01_gate77-ks1868-demostate-1892'
R=W+'/repo'
F={'cheat':R+'/Projects Documents/fragments/cheat/KS-1868-demo-service-state-get-unreadable-thrown-value.html',
   'flow':R+'/Projects Documents/fragments/flow/KS-1868-demo-service-state-get-unreadable-thrown-value.html'}
sha=lambda p: hashlib.sha256(open(p,'rb').read()).hexdigest()
def chk(log):
    r=subprocess.run(['nice','-n','10','node','Blockchain/Dev/scripts/docs-fragments.mjs','check'],cwd=R,capture_output=True,text=True)
    open(log,'w').write(r.stdout+'\n--stderr--\n'+r.stderr+f'\nrc={r.returncode}\n'); return r.returncode
print('head check rc',chk(W+'/logs/frag_head.log'),flush=True)
H={k:sha(v) for k,v in F.items()}
PL={
 'cheat P1 unbalanced tag (drop first </table>)':('cheat','</table>\n</div>','\n</div>',1),
 'cheat P2 two entries in one file (extra h2)':('cheat','<h3>Figures</h3>','<h2>second entry</h2>\n<h3>Figures</h3>',1),
 'flow P1 literal number replaces <!--n--> in h2':('flow','<h2><!--n-->.','<h2>7.',1),
 'flow P2 unbalanced tag (drop </pre>)':('flow','</code></pre>','</code>',1),
}
for name,(k,a,b,n) in PL.items():
    p=F[k]; o=open(p).read()
    if o.count(a)<1: print(name,'PATTERN MISSING',flush=True); continue
    open(p,'w').write(o.replace(a,b,1))
    rc=chk(W+'/logs/frag_'+name.split()[0]+'_'+name.split()[1]+'.log')
    open(p,'w').write(o); assert sha(p)==H[k]
    print(name,'rc',rc,'restored OK',flush=True)
print('final head check rc',chk(W+'/logs/frag_end.log'))
