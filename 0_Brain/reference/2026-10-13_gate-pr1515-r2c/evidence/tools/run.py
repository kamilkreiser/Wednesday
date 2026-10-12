# usage: run.py <cwd> <outfile> cmd...
import subprocess,sys,time
cwd,out=sys.argv[1],sys.argv[2]
t=time.time()
r=subprocess.run(sys.argv[3:],cwd=cwd,capture_output=True,text=True)
open(out,'w').write(r.stdout+'\n----STDERR----\n'+r.stderr+f'\n----RC {r.returncode} secs {time.time()-t:.0f}\n')
print('rc',r.returncode)
