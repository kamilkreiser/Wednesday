import subprocess,hashlib
C='/private/tmp/b1818-gate/clone'; X='2a58dc5d9c62cc021b01e3fe5ebdcd09e76d7f9a'
out=[]
for line in subprocess.run(['git','-C',C,'ls-tree','-r','-z',X],capture_output=True).stdout.split(b'\0'):
    if not line: continue
    meta,p=line.split(b'\t',1); mode,typ,sha=meta.split()
    data=subprocess.run(['git','-C',C,'cat-file','blob',sha.decode()],capture_output=True).stdout
    out.append(hashlib.sha256(data).hexdigest()+'  ./'+p.decode())
open('/private/tmp/b1818-gate/logs/host_sha.txt','w').write('\n'.join(sorted(out,key=lambda s:s[66:]))+'\n'); print(len(out))
