import subprocess,re,sys,os
O='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-10-05_gate60/predict_1384_on_32e05897'
C=O+'/clone'
H='852fc927632095fb603583cb543050d5edd66111'; D='32e058975d4e3a9bbabe828f45e7084de4cfa7f0'
F='Projects Documents/API_Security_Functional_Testing_Architecture_Flow_Diagrams.html'
Q='Projects Documents/QA_Tool_Cheat_Sheet_Secuura_API_Testing.html'
def g(*a,inp=None): return subprocess.run(['git','-C',C,*a],input=inp,capture_output=True,check=True).stdout
def show(r,p): return g('show',f'{r}:{p}').decode().splitlines(keepends=True)
MB=g('merge-base',H,D).decode().strip()
def h_insert(p):
  b=show(MB,p); h=show(H,p)
  # pure insertion before base tail: verify prefix/suffix identity
  n=len(h)-len(b)
  for k in range(len(b)+1):
    if h[:k]+h[k+n:]==b and k<=len(b):
      pass
  # find unique split: common prefix
  k=0
  while k<len(b) and b[k]==h[k]: k+=1
  assert h[k+n:]==b[k:], p
  return h[k:k+n]
fi=h_insert(F); qi=h_insert(Q)
assert fi[0].startswith('    <h2>18.'); assert 'KS-1210' in qi[1]
d=show(D,F); idx=[i for i,l in enumerate(d) if l.startswith('    <h2>19.')]; assert len(idx)==1
flow=d[:idx[0]]+fi+d[idx[0]:]
d=show(D,Q); idx=[i for i,l in enumerate(d) if re.search(r'<h2>.*KS-1005</h2>',l)]; assert len(idx)==1
cheat=d[:idx[0]]+qi+d[idx[0]:]
# wrong-order control: KS-1210 after KS-1005 (just before </body>)
bi=[i for i,l in enumerate(d) if l.startswith('  </body>')][-1]
cheat_wrong=d[:bi]+qi+d[bi:]
def tree(fl,ch):
  idxf=O+'/index_tmp'
  env=dict(os.environ,GIT_INDEX_FILE=idxf)
  subprocess.run(['git','-C',C,'read-tree',H],env=env,check=True)
  # merged result of other paths: take from the real merge index after staging docs
  return None
mode='right' if len(sys.argv)<2 else sys.argv[1]
ch=cheat if mode=='right' else cheat_wrong
open(C+'/'+F,'w',newline='').write(''.join(flow))
open(C+'/'+Q,'w',newline='').write(''.join(ch))
g('add','--',F,Q)
print(mode,g('write-tree').decode().strip())
