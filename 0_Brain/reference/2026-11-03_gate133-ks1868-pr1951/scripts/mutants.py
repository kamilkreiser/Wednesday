import subprocess, hashlib, re, sys
G='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate133-ks1868-pr1951'
S=G+'/repo/Blockchain/Dev/services/nft-certificate/src/services/'
IP=S+'ipfs.service.ts'; BV=S+'blockchain-verifier.service.ts'
def sha(p): return hashlib.sha256(open(p,'rb').read()).hexdigest()
ORIG={IP:sha(IP), BV:sha(BV)}
ip_new='reason = String((error as Error).message);'
M=[]
for i,prov in enumerate(['pinata','infura','web3']):
    M+= [(f'ipfs-{prov}','M0 revert (no String)',IP,ip_new,'reason = (error as Error).message;',i),
         (f'ipfs-{prov}','M1 constant for all',IP,ip_new,"reason = 'unreadable thrown value';",i),
         (f'ipfs-{prov}','M2 String(error) not message',IP,ip_new,'reason = String(error);',i),
         (f'ipfs-{prov}','M3 coerce then pass raw',IP,ip_new,'void String((error as Error).message); reason = (error as Error).message;',i)]
v_init='reason = String(err instanceof Error ? err.message : err);'
M+= [('verifier-init','M0 revert',BV,v_init,'reason = err instanceof Error ? err.message : String(err);',0),
     ('verifier-init','M1 constant for all',BV,v_init,"reason = 'unreadable thrown value';",0),
     ('verifier-init','M3 coerce then pass raw',BV,v_init,'void String(err instanceof Error ? err.message : err); reason = (err instanceof Error ? err.message : String(err)) as string;',0)]
l1='void String(err instanceof Error ? err.message : err);'; l2='void String((err as Error).message);'
M+= [('verifier-lookup','M0 revert both',BV,l1+'\n        '+l2,'void (err instanceof Error ? err.message : String(err));\n        void (err as Error).message;',0),
     ('verifier-lookup','M4 revert line 111 only',BV,l1,'void (err instanceof Error ? err.message : String(err));',0),
     ('verifier-lookup','M5 revert line 112 only',BV,l2,'void (err as Error).message;',0),
     ('verifier-lookup','M6 probe swallows all (always unreadable)',BV,l1,"throw new Error('x');",0)]
def apply(p,old,new,idx):
    s=open(p).read(); parts=s.split(old)
    assert len(parts)>idx+1, (p,old,idx,len(parts))
    s=old.join(parts[:idx+1])+new+old.join(parts[idx+1:]) if False else None
    # replace the idx-th occurrence
    pos=-1
    for _ in range(idx+1): pos=open(p).read().find(old,pos+1)
    t=open(p).read(); open(p,'w').write(t[:pos]+new+t[pos+len(old):])
rows=[]
for site,name,p,old,new,idx in M:
    apply(p,old,new,idx)
    log=f"{G}/logs/mut_{site}__{name.split()[0]}.log"
    rc=subprocess.run(['bash',G+'/scripts/vt.sh',log,'ks1868-blockchain-verifier-message-coercion','ks1868-ipfs-upload-message-coercion']).returncode
    subprocess.run(['cp',G+'/logs/head_ipfs.service.ts',IP]); subprocess.run(['cp',G+'/logs/head_blockchain-verifier.service.ts',BV])
    ok= sha(IP)==ORIG[IP] and sha(BV)==ORIG[BV]
    txt=open(log).read()
    failed=sorted(set(re.findall(r'(?:×|FAIL ).*?((?:RED|control) ks1868 [RC]\d+ [\w.]+)',txt)))
    asserts=len(re.findall('AssertionError',txt)); other=len(re.findall(r'^(TypeError|SyntaxError|Error:)',txt,re.M))
    rows.append(f"{site:16} {name:42} {'KILLED' if rc else 'SURVIVED'} rc={rc} restore={ok} failed={failed} assertionErrors={asserts}")
    print(rows[-1], flush=True)
open(G+'/logs/mutants_table.log','w').write('\n'.join(rows)+'\n')
