import json,subprocess,os
R='/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/02f26010-3405-430b-9101-389a22dcbb3d/scratchpad/j2/repo'
O='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-09_spark-operator106/j2/pr2097'
g=lambda *a: subprocess.run(['git','-C',R,*a],capture_output=True,text=True,check=True).stdout.strip()
H=g('rev-parse','FETCH_HEAD'); assert H=='ebf1ed1d0869e54ae91e4f36c53c4d501ba8187b',H
MB=g('merge-base',H,'origin/develop')
open(O+'/diff.patch','w').write(subprocess.run(['git','-C',R,'diff',MB,H],capture_output=True,text=True).stdout)
ns=[l.split('\t') for l in g('diff','--numstat',MB,H).splitlines()]
t=[{'status':'M','path':p,'added':a,'deleted':d} for a,d,p in ns]
f={'pr':2097,'head_sha':H,'head_mode':'tip','merge_base':MB,'base_ref':'develop','touched_files':t,'test_files':[],'product_files':[x['path'] for x in t],'diff_stat':{'files':len(t),'added':sum(int(x['added']) for x in t),'deleted':sum(int(x['deleted']) for x in t)},'targeted_on_head':None,'targeted_on_base_product_code':None,'not_run':['no test file exists for a docs-only PR; spark_gate.sh refuses a run with no test file, so this facts.json was written by hand from git diff (operator 106); nothing was executed','live/integration runs']}
json.dump(f,open(O+'/facts.json','w'),indent=1)
print(MB,f['diff_stat'])
