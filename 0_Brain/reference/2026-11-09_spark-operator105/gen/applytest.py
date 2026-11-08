import re,subprocess,os,sys,tempfile
S='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/src'; P='7eda23b34d3b7a413ca8f9c0945c7843708ce9f4'
SCR='/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/8bd59522-1a3b-4b02-8fa6-5687685b3d9c/scratchpad'
N='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/_quarantine_2026-11-09/stale/'
f=[x for x in os.listdir(N) if sys.argv[1] in x][0]
t=open(N+f).read(); m=re.search(r'```diff\n(.*?)\n```',t,re.S).group(1)
p=SCR+'/o.diff'; open(p,'w').write(m.split('diff --git a/Blockchain/Dev/services/originate/src/__tests__')[0].rstrip('\n')+'\n')
idx=SCR+'/idx_t'; env=dict(os.environ,GIT_INDEX_FILE=idx)
subprocess.run(['git','-C',S,'read-tree',P],env=env,check=True)
for fl in ([],['--unidiff-zero'],['-C1']):
    r=subprocess.run(['git','-C',S,'apply','--cached','--check']+fl+[p],env=env,capture_output=True,text=True)
    print(fl,r.returncode,r.stderr[:200])
