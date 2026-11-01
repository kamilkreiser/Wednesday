import glob,re,subprocess,difflib,sys
W='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate84-ks1868-minting-1899'
N='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/'
tot_add=tot_del=0
for p in ['P1','P2','P3','P4']:
    f=glob.glob(N+f'READY_KS-1868-KS-1868-O45-{p}_*')[0]
    txt=open(f).read().split('\n')
    # find diff sections
    files={};cur=None
    for l in txt:
        m=re.match(r'^diff --git a/(\S+) b/(\S+)',l)
        if m: cur=m.group(2); files[cur]=[]; continue
        if cur is None: continue
        if l.startswith('+++') or l.startswith('---') or l.startswith('@@') or l.startswith('index ') or l.startswith('new file'): continue
        if l.startswith('+'): files[cur].append(l[1:])
        elif l.startswith('```'): cur=None
    for fn,lines in files.items():
        if '__tests__' not in fn: continue
        head=subprocess.run(['git','-C',W+'/repo','show','refs/gate/pr1899:'+fn],capture_output=True,text=True).stdout.split('\n')
        d=[x for x in difflib.unified_diff(lines,head,'spark','head',lineterm='',n=0)]
        print('##',p,fn); print('\n'.join(d) if d else '(identical)')
        for x in d:
            if x.startswith('+') and not x.startswith('+++'): tot_add+=1
            if x.startswith('-') and not x.startswith('---'): tot_del+=1
print('TOTAL +%d -%d'%(tot_add,tot_del))
