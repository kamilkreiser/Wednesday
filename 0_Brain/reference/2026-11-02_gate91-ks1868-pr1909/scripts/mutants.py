import re, subprocess, hashlib, shutil, os, sys
P='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate91-ks1868-pr1909'
PF=P+'/repo/Blockchain/Dev/services/nft-certificate/src/services/minting.service.ts'
HEAD=open(P+'/scripts/minting.head.ts').read()
sha=lambda s: hashlib.sha256(s.encode()).hexdigest()
H=sha(HEAD)
GUARD=re.compile(r'(?P<i>[ ]*)let reason: string;\n[ ]*try \{\n[ ]*reason = err instanceof Error \? err\.message : String\(err\);\n[ ]*\} catch \{\n[ ]*reason = \'unreadable thrown value\';\n[ ]*\}\n')
ANCH={'P1':"logger.error('Error fetching certification data from originate service', {",
      'P2':"logger.error('DB get wallet certificates failed', { error: reason });"}
def site(src,s):
    a=src.index(ANCH[s]); ms=[m for m in GUARD.finditer(src) if m.end()<=a]; m=ms[-1]
    assert a-m.end()<10, (s,a-m.end())
    return m,a
def mutate(src,s,k):
    m,a=site(src,s); ind=m.group('i'); blk=m.group(0)
    if k=='M0': return src[:m.start()]+ind+"const reason = err instanceof Error ? err.message : String(err);\n"+src[m.end():]
    if k=='M2': return src[:m.start()]+blk.replace("reason = 'unreadable thrown value';","reason = String(err);")+src[m.end():]
    if k=='M3': return src[:m.start()]+blk.replace("reason = 'unreadable thrown value';","throw err;")+src[m.end():]
    if k=='M4': return src[:m.start()]+ind+"const reason = 'unreadable thrown value';\n"+src[m.end():]
    if k=='M6': return src[:m.start()]+blk.replace(": String(err);",": 'x';")+src[m.end():]
    if k=='M5':  # rethrow every value after the log
        if s=='P2': return src.replace(ANCH[s],ANCH[s]+"\n        throw err;",1)
        # P1: add throw err after the log call closing '});' that follows anchor
        j=src.index("      return null;\n",a); return src[:j]+"      throw err;\n"+src[j:]
    if k=='M7':
        if s=='P2': return src.replace(ANCH[s],"void reason;",1)
        j=src.index("});\n",a)+4; return src[:a]+"void reason;\n"+src[j:]
    if k=='M8':  # wrong value swallowed: the constant is logged but the thrown value is dropped differently -> return [] / undefined
        if s=='P1': j=src.index("      return null;\n",a); return src[:j]+"      return undefined as any;\n"+src[j:]
        j=src.index("return certificates.sort",a); return src[:j]+"return [];\n    // "+src[j:]
    raise SystemExit(k)
sites=['P1','P2']; ks=['M0','M2','M3','M4','M5','M6','M7','M8']
res=[]
for s in sites:
    for k in ks:
        try: new=mutate(HEAD,s,k)
        except Exception as e: print('SKIP',s,k,e); continue
        assert new!=HEAD
        open(PF,'w').write(new)
        log=f'{P}/logs/mut_{s}_{k}.log'
        subprocess.run(['bash',P+'/scripts/vt.sh',f'mut_{s}_{k}','ks1868-nft-get-certification-data-unreadable-throw','ks1868-nft-get-wallet-nft-certificates-unreadable-throw'])
        open(PF,'w').write(HEAD); ok=sha(open(PF).read())==H
        t=open(log).read()
        failed=re.findall(r'^ +× (.*?) \d+ms',t,re.M)
        killed='rc=1' in t
        assertion='AssertionError' in t
        res.append((s,k,'KILLED' if killed else 'SURVIVED',[f.split()[2] for f in failed],assertion,'restore '+str(ok)))
        print(res[-1],flush=True)
open(P+'/logs/mutants_table.log','w').write('\n'.join(map(str,res))+'\n')
