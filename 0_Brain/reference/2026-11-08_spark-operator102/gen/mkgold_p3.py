import difflib
R='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-08_spark-operator102/gen/'
B='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_2077_o102_p3_arch_ref_rewards_route/'
p='Projects Documents/Secuura-Architecture-Reference.md'
s=open(R+'arch.md.tip',encoding='utf-8').read()
a="| `/api/staking/*`, `/api/rewards/*`, `/api/pool/*` | Staking (:4015) | Yes |\n| `/api/referral/*` | Referral (:4016) | Yes |\n"
b="| `/api/staking/*`, `/api/pool/*` | Staking (:4015) | Yes |\n| `/api/referral/*`, `/api/rewards/*` | Referral (:4016) | Yes |\n"
assert s.count(a)==1
n=s.replace(a,b)
out='diff --git a/%s b/%s\n'%(p,p)+''.join(difflib.unified_diff(s.splitlines(True),n.splitlines(True),'a/'+p,'b/'+p,n=3))
open(B+'golden.diff','w',encoding='utf-8').write(out); print(out)
