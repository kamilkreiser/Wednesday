import subprocess,difflib,os,sys
S='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/src'
T='1cbf260548e7fd534603725f9fc6b05c5cdd9907'
B='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/'
def show(p): return subprocess.run(['git','-C',S,'show',f'{T}:{p}'],capture_output=True,text=True,check=True).stdout
def golden(path,subs):
    src=show(path); new=src
    for a,b in subs:
        assert new.count(a)==1,(a,new.count(a)); new=new.replace(a,b)
    d=list(difflib.unified_diff(src.splitlines(True),new.splitlines(True),f'a/{path}',f'b/{path}',n=3))
    d[0]=d[0].rstrip('\n')+'\n'
    return 'diff --git a/%s b/%s\n'%(path,path)+''.join(d)
CON='Blockchain/Dev/CONTRIBUTING.md'
MT='Blockchain/Dev/docs/MULTI-TENANCY.md'
RP='Blockchain/Dev/docs/RLS-FAIL-CLOSED-PLAN.md'
specs={
'ks_1320_o100_p1_contributing_squash_subject_limit':(CON,[(
"  fold-back/tombstone mechanics below depend on shared history. Feature PRs into `develop` stay squash.\n",
"  fold-back/tombstone mechanics below depend on shared history. Feature PRs into `develop` stay squash, and the squash\n  subject must be 92 characters or fewer and ASCII only, so keep the PR title within that limit (KS-1320: nothing\n  rejects a longer title when the PR is opened; the merge gate finds it, and a replacement subject then has to be written).\n")]),
'ks_1343_o100_p2_multitenancy_flag_wording':(MT,[(
"  they are in **different** states — a distinction the first version of this correction got wrong:\n",
"  they are in **different** states:\n"),(
"    **This is the flag that actually gates per-tenant databases**, and it is off everywhere.\n",
"    **This is the flag that actually gates per-tenant databases**, and in the repository it is off everywhere; live app\n    settings were not checked.\n")]),
'ks_1343_o100_p3_rls_plan_only_isolation_wording':(RP,[(
"  is the only tenant isolation that exists.** Readiness",
"  is the only database-level tenant isolation that exists.** Readiness")]),
}
for d,(p,subs) in specs.items():
    os.makedirs(B+d,exist_ok=True)
    g=golden(p,subs)
    open(B+d+'/golden.diff','w').write(g)
    print(d); print(g)
