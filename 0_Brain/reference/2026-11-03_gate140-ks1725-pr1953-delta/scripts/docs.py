# docs-fragments check at the head, then a planted unbalanced </table> in the FLOW fragment this round edited; byte-restore + sha256.
import subprocess, hashlib
G='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate140-ks1725-pr1953-delta'; R=G+'/repo'; L=G+'/logs'
F=R+'/Projects Documents/fragments/flow/KS-1725-zod-4-with-a-zod-3-issue-layer.html'
def check(tag):
    p=subprocess.run(['node',R+'/Blockchain/Dev/scripts/docs-fragments.mjs','check','--root',R],capture_output=True,text=True)
    open(L+'/docs_%s.log'%tag,'w').write(p.stdout+p.stderr); return p.returncode, (p.stdout+p.stderr).strip().splitlines()[-2:]
print('head', check('head'))
orig=open(F,'rb').read(); s=orig.decode(); k=s.rfind('</table>'); assert k>0
open(F,'wb').write((s[:k]+s[k+len('</table>'):]).encode())
print('planted', check('planted'))
open(F,'wb').write(orig); print('restore sha256 equal', hashlib.sha256(open(F,'rb').read()).hexdigest()==hashlib.sha256(orig).hexdigest())
print('status', repr(subprocess.run(['git','-C',R,'status','--porcelain'],capture_output=True,text=True).stdout))
print('restored', check('restored'))
