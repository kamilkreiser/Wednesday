import subprocess,sys
REPO='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate89-e25-1904-1906-1907/repo'
f=sys.argv[1]; lines=[int(x) for x in sys.argv[2].split(',')]
back=int(sys.argv[3]) if len(sys.argv)>3 else 5
src=subprocess.run(['git','-C',REPO,'show','origin/develop:Blockchain/Dev/services/'+f],capture_output=True,text=True).stdout.split('\n')
print('###',f)
for n in lines:
    print('--',n)
    for i in range(max(0,n-back),min(len(src),n+3)): print(f'{i+1}: {src[i][:140]}')
