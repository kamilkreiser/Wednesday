import subprocess,re
C='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-10-05_gate60/predict_1384_on_32e05897/clone'
H='852fc927632095fb603583cb543050d5edd66111'; D='32e058975d4e3a9bbabe828f45e7084de4cfa7f0'
MB=subprocess.check_output(['git','-C',C,'merge-base',H,D]).decode().strip()
F='Projects Documents/API_Security_Functional_Testing_Architecture_Flow_Diagrams.html'
Q='Projects Documents/QA_Tool_Cheat_Sheet_Secuura_API_Testing.html'
def show(r,p): return subprocess.check_output(['git','-C',C,'show',f'{r}:{p}'])
for name,r in (('MB',MB),('H',H),('D',D)):
  for p in (F,Q):
    b=show(r,p).decode()
    print('==',name,p.split('/')[-1][:20],len(b))
    for i,l in enumerate(b.split('\n'),1):
      if '<h2' in l or '</body>' in l or 'class="section"' in l: print(' ',i,l.strip()[:120])
