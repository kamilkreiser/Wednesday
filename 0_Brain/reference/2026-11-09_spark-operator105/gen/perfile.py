import json,re,subprocess,os,tempfile,sys
O=sys.argv[1]; PIN='7eda23b34d3b7a413ca8f9c0945c7843708ce9f4'
N='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/'
Q=N+'_quarantine_2026-11-09/stale/'
S='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/src'
SCR='/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/8bd59522-1a3b-4b02-8fa6-5687685b3d9c/scratchpad'
rows=json.load(open(O+'/ready_all3.json'))
prs=json.load(open(O+'/prs_start.json')); prf={f for v in prs.values() for f in v['files']}
fwdfiles={}
for r in rows:
    if r['cls']=='FWD-OK':
        for f in r['files']: fwdfiles.setdefault(f,[]).append(r['name'][:40])
idx=tempfile.mkdtemp(dir=SCR)+'/idx'; env=dict(os.environ,GIT_INDEX_FILE=idx)
subprocess.run(['git','-C',S,'read-tree',PIN],env=env,check=True)
def chk(p,flag):
    return subprocess.run(['git','-C',S,'apply','--cached','--check']+flag+[p],env=env,capture_output=True,text=True).returncode==0
out=[]
for r in rows:
    if r['cls']!='NEITHER' or r['pr'] or r['live'] or r['state'] not in('Backlog','In Progress'): continue
    t=open(Q+r['name'],encoding='utf-8',errors='replace').read()
    m=re.search(r'```diff\n(.*?)\n```',t,re.S)
    if m: body=m.group(1)
    else:
        c=re.search(r'CANONICAL PATCH = `([^`]+)`',t); body=open(c.group(1),errors='replace').read().rstrip('\n')
    parts=re.split(r'(?m)^(?=--- (?:a/|/dev/null))',body)
    pf=[]
    for pt in parts:
        mm=re.search(r'^\+\+\+ b/(\S+)',pt,re.M)
        if not mm: continue
        f=mm.group(1)
        p=os.path.dirname(idx)+'/p.diff'; open(p,'w').write(pt.rstrip('\n')+'\n')
        s='FWD' if chk(p,[]) else ('REV' if chk(p,['-R']) else 'DRIFT')
        pf.append((f.replace('Blockchain/Dev/',''),s,f in prf,f in fwdfiles))
    r['pf']=pf; out.append(r)
json.dump(out,open(O+'/perfile.json','w'),indent=1)
import collections
print(collections.Counter(tuple(sorted({s for _,s,_,_ in r['pf']})) for r in out))
