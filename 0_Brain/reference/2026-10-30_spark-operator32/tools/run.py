#!/usr/bin/env python3
"""run.py <grp> <tag>  : one hand-run Spark round for night/briefs/ks_1864_<grp>/KS-1864.md (own checker: tsc + per-file vitest)."""
import sys,os,json,subprocess,re,time,collections
O='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-10-30_spark-operator32'
L='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model'
grp,tag=sys.argv[1],sys.argv[2]
BR=f'{L}/night/briefs/ks_1864_{grp}'
RD=f'{O}/runs/{grp}_{tag}'; os.makedirs(RD,exist_ok=True)
CL=O+'/clone'; G=CL+'/Blockchain/Dev/services/api-gateway'; TSC=CL+'/Blockchain/Dev/node_modules/.bin/tsc'
brief=open(BR+'/KS-1864.md').read()
inp=json.load(open(BR+'/inputs.json'))
golden=open(BR+'/golden.diff').read()
task="""TASK: test_only_typefix

The INPUT is a JSON object with `brief` (the full written brief: read it first and execute it exactly) and `files` (the FULL current content of every file you may change, keyed by repo-relative path).
Produce the change the brief specifies as ONE unified diff against those files, and nothing else. The `+` lines are given byte-exact in the brief; copy them. Context lines are copied from `files`. Touch only the edits the brief names.
"""
open(RD+'/task.md','w').write(task)
json.dump({'brief':brief,'files':inp['files']},open(RD+'/input.json','w'))
t0=time.time()
CP=os.environ.get('CONTROL_PATCH')
if CP:
    open(RD+'/out.md','w').write('```diff\n'+open(CP).read()+'```\n'); open(RD+'/out.md.meta.json','w').write('{}')
    class R: returncode=0; stderr='CONTROL (no model call)'
    r=R()
else:
  r=subprocess.run(['python3','-I',L+'/lib/spark_call.py',RD+'/task.md',RD+'/input.json',RD+'/out.md',RD+'/out.md.meta.json','deepseek-v4-flash-0731','8000','http://127.0.0.1:47788','0'],capture_output=True,text=True)
open(RD+'/call.err','w').write(r.stderr)
print('call rc',r.returncode, r.stderr.strip().splitlines()[-1][:300] if r.stderr.strip() else '')
meta=json.load(open(RD+'/out.md.meta.json')) if os.path.exists(RD+'/out.md.meta.json') else {}
out=open(RD+'/out.md').read() if os.path.exists(RD+'/out.md') else ''
m=re.findall(r'```diff\n(.*?)```',out,re.S)
res={'grp':grp,'tag':tag,'model_s':meta.get('wall_clock_seconds'),'tokens':f"{meta.get('prompt_eval_count')}+{meta.get('eval_count')}",'checks':{}}
def fin(v):
    res['verdict']=v; res['round_s']=round(time.time()-t0,1); json.dump(res,open(RD+'/result.json','w'),indent=1); print(json.dumps(res)); sys.exit(0)
if len(m)!=1: res['checks']['A1_one_diff_block']=f'FAIL ({len(m)} blocks)'; fin('FAIL')
res['checks']['A1_one_diff_block']='PASS'
patch=m[0]; open(RD+'/patch.diff','w').write(patch)
# byte-compare added/removed lines to golden
def pm(d):
    c=collections.Counter()
    for l in d.split('\n'):
        if l.startswith('+++') or l.startswith('---'): continue
        if l.startswith('+'): c[l[1:]]+=1
        elif l.startswith('-'): c[l[1:]]-=1
    return sorted((k,v) for k,v in c.items() if v)
res['golden']='BYTE-IDENTICAL(+/- lines)' if pm(patch)==pm(golden) else 'DIFFERS'
res['golden_full_identical']= (patch.strip()==golden.strip())
files=re.findall(r'^\+\+\+ b/(\S+)',patch,re.M); exp=list(inp['files'].keys())
res['checks']['A3_files_exact']='PASS' if sorted(files)==sorted(exp) else f'FAIL {files}'
if res['checks']['A3_files_exact']!='PASS': fin('FAIL')
# apply strictly
orig={p:open(CL+'/'+p).read() for p in exp}
RC=['--recount'] if os.environ.get('RECOUNT') else []
ap=subprocess.run(['git','-C',CL,'apply','--check']+RC+['-'],input=patch,capture_output=True,text=True)
if ap.returncode!=0:
    res['checks']['A2_applies_strict']='FAIL: '+ap.stderr.strip()[:300]
    ap2=subprocess.run(['git','-C',CL,'apply','--check','--recount','-'],input=patch,capture_output=True,text=True)
    res['checks']['A2_recount_would_apply']= (ap2.returncode==0)
    fin('FAIL')
res['checks']['A2_applies_strict']='PASS'
subprocess.run(['git','-C',CL,'apply']+RC+['-'],input=patch,text=True,check=True)
def restore():
    for p,c in orig.items(): open(CL+'/'+p,'w').write(c)
def tsc(v):
    r=subprocess.run([TSC,'-p',f'{G}/tsconfig.o32-{v}.json'],capture_output=True,text=True)
    open(f'{RD}/tsc_{v}.txt','w').write(r.stdout+r.stderr)
    c=collections.Counter(re.sub(r'\(.*','',l.split('api-gateway/')[-1]) for l in (r.stdout+r.stderr).splitlines() if 'error TS' in l)
    return c
BASE={'csrf.test.ts':10,'ks1165-api-gateway-csrf-excludedpaths-carries-no.test.ts':5,'ks1374-global-limiter-at-demo-limit.test.ts':1,'ks1457-audit-finish-reads-use-the-entry-path.test.ts':2,'ks1464-limiter-key-hygiene.test.ts':2,'ks695-ask3-erase-connector-door.test.ts':1,'rateLimitEnforce.test.ts':6}
BASE={'src/__tests__/'+k:v for k,v in BASE.items()}
TOT={ 'ks1374':7,'ks695':6,'ks1464':12,'ks1457':9,'ks1165':7,'csrf':10,'rateLimitEnforce':13}
try:
    for v in ('node','unset'):
        c=tsc(v)
        want=dict(BASE)
        for p in exp: want[ 'src/__tests__/'+os.path.basename(p)]=0
        want={k:x for k,x in want.items() if x}
        ok = dict(c)==want
        res['checks'][f'B_tsc_{v}']=('PASS' if ok else f'FAIL got={dict(c)}')+f' (total {sum(c.values())}, want {sum(want.values())})'
    for p in exp:
        b=os.path.basename(p)
        sub=subprocess.run(['bash',O+'/tools/vt.sh',b,f'{RD}/vt_{b}.txt'])
        txt=open(f'{RD}/vt_{b}.txt').read()
        mm=re.search(r'Tests\s+(?:(\d+) failed \| )?(\d+) passed',txt)
        passed=int(mm.group(2)) if mm else -1; failed=int(mm.group(1) or 0) if mm else -1
        key=[k for k in TOT if b.startswith(k)][0]
        res['checks']['C_tests_'+key]= 'PASS' if (passed==TOT[key] and failed==0 and 'rc=0' in txt) else f'FAIL passed={passed} failed={failed}'
finally:
    restore()
bad=[k for k,v in res['checks'].items() if not v.startswith('PASS')]
fin('PASS' if not bad else 'FAIL')
