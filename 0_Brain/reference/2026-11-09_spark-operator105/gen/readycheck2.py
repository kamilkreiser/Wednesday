# For each READY whose text mentions a path fragment: extract first ```diff fence, test git apply --cached --check forward/reverse vs pin tree (temp index).
import sys,os,re,subprocess,glob,tempfile
N='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/'
SRC='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/src'
PIN=sys.argv[1]; frags=sys.argv[2:]
idx=tempfile.mkdtemp(dir='/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/8bd59522-1a3b-4b02-8fa6-5687685b3d9c/scratchpad')+'/idx'
env=dict(os.environ,GIT_INDEX_FILE=idx)
subprocess.run(['git','-C',SRC,'read-tree',PIN],env=env,check=True)
for f in sorted(glob.glob(N+'READY_*.diff.md')):
    t=open(f,encoding='utf-8',errors='replace').read()
    if not any(x in t for x in frags): continue
    m=re.search(r'```diff\n(.*?)\n```',t,re.S)
    if not m: print('NODIFF','\t',os.path.basename(f),'\t',[]); continue
    p=tempfile.NamedTemporaryFile('w',suffix='.diff',delete=False,dir=os.path.dirname(idx)); p.write(m.group(1)+'\n'); p.close()
    files=sorted(set(re.findall(r'^\+\+\+ b/(\S+)',m.group(1),re.M)))
    res=[]
    for flag in ([],['-R']):
        r=subprocess.run(['git','-C',SRC,'apply','--cached','--check']+flag+[p.name],env=env,capture_output=True,text=True)
        res.append(r.returncode)
    st='FWD-OK(unmerged,still applicable)' if res[0]==0 else ('REV-OK(already in tip)' if res[1]==0 else 'NEITHER(drifted/partial)')
    hit=[x for x in files if any(fr in x for fr in frags)]
    print(st,'\t',os.path.basename(f),'\t',files)
