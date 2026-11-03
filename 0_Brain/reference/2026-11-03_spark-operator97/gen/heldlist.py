import os,re,sys
N='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/'
names=[n for n in sorted(os.listdir(N)) if n.startswith('READY_') and n.endswith('.diff.md')]
prods=set(); per={}
for n in names:
    try: t=open(N+n,encoding='utf-8',errors='replace').read()
    except Exception as e: print('ERR',n,e,file=sys.stderr); continue
    fs=re.findall(r'^diff --git a/(\S+) b/',t,re.M)
    per[n]=fs
    for f in fs: prods.add(f)
open(sys.argv[1],'w').write('\n'.join(sorted(prods))+'\n')
open(sys.argv[2],'w').write('\n'.join(n for n in names)+'\n')
print(len(names),'READY files',len(prods),'paths')
