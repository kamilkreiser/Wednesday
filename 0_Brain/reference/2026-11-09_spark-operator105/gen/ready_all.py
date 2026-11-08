# Operator 105: classify every night/READY_*.diff.md at the pin. Same instrument as 104 (first diff fence, git apply --cached --check fwd and -R vs temp index of pin tree);
# extension for 104's NODIFF class: if the READY names a CANONICAL PATCH file that still exists, check that file instead (flagged CANON).
import sys,os,re,subprocess,glob,tempfile,json
N='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/'
SRC='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/src'
SCR='/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/8bd59522-1a3b-4b02-8fa6-5687685b3d9c/scratchpad'
PIN=sys.argv[1]
idx=tempfile.mkdtemp(dir=SCR)+'/idx'
env=dict(os.environ,GIT_INDEX_FILE=idx)
subprocess.run(['git','-C',SRC,'read-tree',PIN],env=env,check=True)
rows=[]
for f in sorted(glob.glob(N+'READY_*.diff.md')):
    b=os.path.basename(f)
    t=open(f,encoding='utf-8',errors='replace').read()
    m=re.search(r'```diff\n(.*?)\n```',t,re.S)
    src='fence'
    if m: body=m.group(1)
    else:
        c=re.search(r'CANONICAL PATCH = `([^`]+)`',t)
        body=None
        if c and os.path.exists(c.group(1)):
            body=open(c.group(1),encoding='utf-8',errors='replace').read().rstrip('\n'); src='CANON'
        if body is None:
            rows.append(dict(name=b,cls='NODIFF',files=[],src='none',canon=bool(c))); continue
    p=os.path.join(os.path.dirname(idx),'x.diff'); open(p,'w').write(body+'\n')
    files=sorted(set(re.findall(r'^\+\+\+ b/(\S+)',body,re.M)))
    res=[]
    for flag in ([],['-R']):
        r=subprocess.run(['git','-C',SRC,'apply','--cached','--check']+flag+[p],env=env,capture_output=True,text=True)
        res.append(r.returncode)
    cls='FWD-OK' if res[0]==0 else ('REV-OK' if res[1]==0 else 'NEITHER')
    km=re.match(r'READY_(KS-\d+)',b)
    rows.append(dict(name=b,cls=cls,files=files,src=src,hold=os.path.exists(f.replace('.diff.md','.HOLD-NOTE.md'))))
json.dump(rows,open(sys.argv[2],'w'),indent=1)
from collections import Counter
print(Counter((r['cls'],r['src']) for r in rows))
