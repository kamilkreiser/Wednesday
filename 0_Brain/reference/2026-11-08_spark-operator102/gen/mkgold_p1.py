import difflib
R='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-08_spark-operator102/gen/p1/'
OUT='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_2022_o102_p1_stale_gate_citation_two_comments/golden.diff'
files=[('a.ts','Blockchain/Dev/services/auth/src/auth.openapi.ts'),('b.ts','Blockchain/Dev/services/auth/src/__tests__/ks796-f6-mfa-schema-identity.test.ts')]
old2="passwordLoginGate.ts:55` imports `z` from 'zod'\n// directly, so `MFA_CODE_ACCEPTED` is built on an UNEXTENDED zod. The spec\n"
new2="passwordLoginGate.ts` imported `z` from 'zod'\n// directly (KS-810; it now imports it from '@secuura/shared'), so\n// `MFA_CODE_ACCEPTED` was built on an UNEXTENDED zod. The spec\n"
out=''
for f,p in files:
    s=open(R+f,encoding='utf-8').read()
    assert s.count(old2)==1,f
    n=s.replace(old2,new2)
    d=list(difflib.unified_diff(s.splitlines(True),n.splitlines(True),'a/'+p,'b/'+p,n=3))
    out+='diff --git a/%s b/%s\n'%(p,p)+''.join(d)
open(OUT,'w',encoding='utf-8').write(out)
print(out)
