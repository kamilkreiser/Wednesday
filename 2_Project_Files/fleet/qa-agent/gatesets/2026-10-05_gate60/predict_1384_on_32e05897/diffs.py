import subprocess,difflib
C='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-10-05_gate60/predict_1384_on_32e05897/clone'
H='852fc927632095fb603583cb543050d5edd66111'; D='32e058975d4e3a9bbabe828f45e7084de4cfa7f0'
MB=subprocess.check_output(['git','-C',C,'merge-base',H,D]).decode().strip()
F='Projects Documents/API_Security_Functional_Testing_Architecture_Flow_Diagrams.html'
Q='Projects Documents/QA_Tool_Cheat_Sheet_Secuura_API_Testing.html'
def show(r,p): return subprocess.check_output(['git','-C',C,'show',f'{r}:{p}']).decode().splitlines(keepends=True)
for p in (F,Q):
  b=show(MB,p)
  for nm,r in (('H',H),('D',D)):
    o=show(r,p)
    sm=difflib.SequenceMatcher(None,b,o,autojunk=False)
    ops=[x for x in sm.get_opcodes() if x[0]!='equal']
    print(p[-30:],nm,ops)
    for t,i1,i2,j1,j2 in ops:
      print('  base ctx before:',repr(''.join(b[max(0,i1-3):i1])[-300:]))
      print('  ins first lines:',repr(''.join(o[j1:j1+3])[:300]))
      print('  ins last lines:',repr(''.join(o[j2-3:j2])[-300:]))
      print('  base after:',repr(''.join(b[i1:i1+3])[:200]))
