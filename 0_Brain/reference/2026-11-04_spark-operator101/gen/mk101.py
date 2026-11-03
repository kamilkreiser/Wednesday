import subprocess,difflib,os,sys
S='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/src'
T=sys.argv[1]
B='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/'
def show(p): return subprocess.run(['git','-C',S,'show',f'{T}:{p}'],capture_output=True,text=True,check=True).stdout
def golden(path,subs):
    src=show(path); new=src
    for a,b in subs:
        assert new.count(a)==1,(a,new.count(a)); new=new.replace(a,b)
    d=list(difflib.unified_diff(src.splitlines(True),new.splitlines(True),f'a/{path}',f'b/{path}',n=3))
    d[0]=d[0].rstrip('\n')+'\n'
    return 'diff --git a/%s b/%s\n'%(path,path)+''.join(d)
P='Blockchain/Dev/scripts/preflight/no-tracked-credentials.sh'
specs={'ks_902_o101_p1_no_tracked_credentials_comment_idiom':(P,[(
"# `bare-path-scripts-executable.sh` and `action-pins-labelled.sh` already derive\n# their root this way and are structurally immune; this is the same idiom.\n",
"# The root is derived from this script's own location, not from the caller's\n# working directory, so it does not depend on where the preflight runs. Do not\n# copy `REPO_ROOT=\"$(cd ../.. && pwd)\"` from `bare-path-scripts-executable.sh`\n# or `action-pins-labelled.sh`: that form is cwd-relative (KS-902).\n")])}
for d,(p,subs) in specs.items():
    os.makedirs(B+d,exist_ok=True)
    g=golden(p,subs)
    open(B+d+'/golden.diff','w').write(g)
    print(d); print(g)
