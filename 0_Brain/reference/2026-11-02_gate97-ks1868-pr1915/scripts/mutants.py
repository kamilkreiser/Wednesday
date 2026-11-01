import re, subprocess, hashlib
P='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate97-ks1868-pr1915'
PF=P+'/repo/Blockchain/Dev/services/nft-certificate/src/services/ipfs.service.ts'
HEAD=open(PF).read()
sha=lambda s: hashlib.sha256(s.encode()).hexdigest()
H=sha(HEAD)
GUARD=re.compile(r'(?P<i>[ ]*)let reason: string;\n[ ]*try \{\n[ ]*reason = error instanceof Error \? error\.message : String\(error\);\n[ ]*\} catch \{\n[ ]*reason = \'unreadable thrown value\';\n[ ]*\}\n')
guards=list(GUARD.finditer(HEAD)); assert len(guards)==2
THROW="throw new ServiceUnavailableError('IPFS gateway');"
def mutate(src,i,k):
    m=guards[i]; ind=m.group('i'); blk=m.group(0)
    end=m.end()
    t=src.index(THROW,end)           # the throw closing this catch
    lg=src.index('logger.warn(',end)
    lge=src.index('});\n',lg)+4
    if k=='M0': return src[:m.start()]+ind+"const reason = error instanceof Error ? error.message : String(error);\n"+src[m.end():]
    if k=='M2': return src[:m.start()]+blk.replace("reason = 'unreadable thrown value';","reason = String(error);")+src[m.end():]
    if k=='M3': return src[:m.start()]+blk.replace("reason = 'unreadable thrown value';","throw error;")+src[m.end():]
    if k=='M4': return src[:m.start()]+ind+"const reason = 'unreadable thrown value';\n"+src[m.end():]
    if k=='M5': return src[:t]+"throw error;"+src[t+len(THROW):]
    if k=='M6': return src[:m.start()]+blk.replace(": String(error);",": 'x';")+src[m.end():]
    if k=='M7': return src[:lg]+"void reason;\n"+src[lge:]
    if k=='M8': return src[:t]+"throw new Error('IPFS gateway');"+src[t+len(THROW):]
    if k=='M9': return src[:t]+"return Buffer.alloc(0);"+src[t+len(THROW):]
    raise SystemExit(k)
res=[]
for i,s in enumerate(['S1-request','S2-body']):
    for k in ['M0','M2','M3','M4','M5','M6','M7','M8','M9']:
        new=mutate(HEAD,i,k); assert new!=HEAD
        open(PF,'w').write(new)
        lab=f'mut_{s}_{k}'
        subprocess.run(['bash',P+'/scripts/vt.sh',lab,'ks1868-ipfs-fetch-unreadable-throw','ks1240b-ipfs-fetches-are-bounded-and-a-body-stall-maps-to-503','ipfs.service.test'])
        open(PF,'w').write(HEAD); ok=sha(open(PF).read())==H
        t=open(f'{P}/logs/{lab}.log').read()
        failed=re.findall(r'^ +× (.*?) \d+ms',t,re.M)
        res.append((s,k,'KILLED' if 'rc=1' in t else 'SURVIVED',failed,'AssertionError' in t,'restore '+str(ok)))
        print(res[-1],flush=True)
open(P+'/logs/mutants_table.log','w').write('\n'.join(map(str,res))+'\n')
