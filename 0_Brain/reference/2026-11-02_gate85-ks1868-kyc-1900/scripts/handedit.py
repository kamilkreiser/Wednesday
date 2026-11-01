import glob,re,subprocess,difflib
W='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate85-ks1868-kyc-1900'
N='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/'
ta=td=0
for p in ['P1','P2','P3','P4','P5']:
    f=glob.glob(N+f'READY_KS-1868-KS-1868-O47-{p}_*')[0]
    txt=open(f).read().split('\n')
    files={};cur=None;inblock=False
    for l in txt:
        m=re.match(r'^diff --git a/(\S+) b/(\S+)',l)
        if m: cur=m.group(2); files[cur]=[]; continue
        if cur is None: continue
        if l.startswith('```'): cur=None; continue
        if l.startswith(('+++','---','@@','index ','new file')): continue
        if l.startswith('+'): files[cur].append(l[1:])
        elif l.startswith('\\'): continue
    for fn,lines in files.items():
        if '__tests__' not in fn: continue
        head=subprocess.run(['git','-C',W+'/repo','show','refs/gate/pr1900:'+fn],capture_output=True,text=True).stdout.split('\n')
        if head and head[-1]=='': head=head[:-1]
        d=list(difflib.unified_diff(lines,head,'spark','head',lineterm='',n=0))
        print('##',p,fn,'spark lines',len(lines),'head lines',len(head)); print('\n'.join(d) if d else '(identical)')
        for x in d:
            if x.startswith('+') and not x.startswith('+++'): ta+=1
            if x.startswith('-') and not x.startswith('---'): td+=1
    # product hunk of this pass vs head product hunk
    prod=[l for l in files if 'index.ts' in l]
    print('   product files in pass:',prod)
print('TOTAL tests +%d -%d'%(ta,td))
