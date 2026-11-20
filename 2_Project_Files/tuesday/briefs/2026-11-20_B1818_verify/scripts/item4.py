import subprocess,re
C='/private/tmp/b1818-gate/clone'; X='2a58dc5d9c62cc021b01e3fe5ebdcd09e76d7f9a'; O='851057291ffb019baee6c3c51a50d7b8833f5b3a'; M='b4681297d974ac3d8e74a4a12baeb9ea41962c52'; B='308b7aa60cd8d2a8576b29e0422538cbaf140f24'
F='/Volumes/Datasec_DEV/!CODING/Datasec/Datasec Security Composer/1_Project_Definition/Briefs/2026-11-20_B1803_evidence/REVIEW-INDEX.md'
def rp(c,p): return subprocess.run(['git','-C',C,'rev-parse',f'{c}:{p}'],capture_output=True,text=True).stdout.strip()
rows=[l for l in open(F).read().splitlines()[23:60] if l.startswith('| ')]
print('rows',len(rows)); eq=mv=bad=0
for l in rows:
    c=[x.strip() for x in l.strip('|').split('|')]
    p=c[1].strip('`'); o=rp(O,p); n=rp(X,p); m=rp(M,p); b=rp(B,p)
    st='equal' if o==n else 'MOVED'
    claim=c[4]
    ok = (st==claim) and o.startswith(c[2]) and n.startswith(c[3])
    if st=='equal': eq+=1
    else: mv+=1
    if not ok: bad+=1
    extra='' if st=='equal' else f' new==main:{n==m} base==old:{b==o}'
    print(('OK ' if ok else 'BAD'),st,p,extra)
print('equal',eq,'moved',mv,'disagreeing rows',bad)
