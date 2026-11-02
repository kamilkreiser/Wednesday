# Mutants per site in the PRODUCT only (tests untouched); sha256 restored and checked after every run.
import hashlib, subprocess, re, json, os, sys
G='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate131-ks1868-pr1949'
P=G+'/repo/Blockchain/Dev/services/auth/src/routes/'
T={'auth.ts':'src/__tests__/ks1868-auth-rehash-denylist-message-coercion-unreadable-throw.test.ts',
   'internal.ts':'src/__tests__/ks1868-internal-connector-token-message-coercion-unreadable-throw.test.ts',
   'issuerCerts.ts':'src/__tests__/ks1868-issuer-certs-message-coercion-unreadable-throw.test.ts',
   'oauth.ts':'src/__tests__/ks1868-oauth-message-coercion-unreadable-throw.test.ts'}
MLINE='reason = m === undefined || m === null ? m : String(m);'
ILINE='reason = String(err instanceof Error ? err.message : err);'
SITES=[('auth.ts',0,'rehash'),('auth.ts',1,'logout'),('internal.ts',0,'connector-token'),('issuerCerts.ts',0,'list'),('issuerCerts.ts',1,'revoke'),('oauth.ts',0,'authorize'),('oauth.ts',1,'token')]
MM={'M0 revert (reason = m)':'reason = m;','M1 drop undefined/null pass-through':'reason = String(m);','M2 constant for every value':"reason = 'unreadable thrown value';",'M3 only strings pass, else constant':"reason = typeof m === 'string' ? m : 'unreadable thrown value';"}
MI={'M0 revert (base expression)':'reason = err instanceof Error ? err.message : String(err);','M1 constant for every value':"reason = 'unreadable thrown value';",'M2 non-Error branch broken':"reason = String(err instanceof Error ? err.message : 'x');",'M3 only string messages pass, else constant':"reason = err instanceof Error ? (typeof err.message === 'string' ? err.message : 'unreadable thrown value') : String(err);"}
sha=lambda p: hashlib.sha256(open(p,'rb').read()).hexdigest()
rows=[]
for f,occ,label in SITES:
    path=P+f; orig=open(path).read(); h0=sha(path)
    line = ILINE if f=='issuerCerts.ts' else MLINE
    muts = MI if f=='issuerCerts.ts' else MM
    idx=[m.start() for m in re.finditer(re.escape(line),orig)]
    assert len(idx)==2 if f!='internal.ts' else len(idx)==1, (f,len(idx))
    for name,rep in muts.items():
        s=orig[:idx[occ]]+rep+orig[idx[occ]+len(line):]
        open(path,'w').write(s)
        log=f"{G}/logs/mut_{f.replace('.ts','')}_{label}__{name.split()[0]}.log"
        r=subprocess.run([G+'/scripts/vt.sh',log,T[f],'--hookTimeout=60000','--testTimeout=30000'])
        open(path,'w').write(orig); ok = sha(path)==h0
        txt=re.sub(r'\x1b\[[0-9;]*m','',open(log).read())
        fails=sorted(set(re.findall(r'(?:RED|control) ks1868 ([RC]\d)[^\n>]*?(?:\s|:)\s*([a-z-]*)',txt)))
        tl=re.findall(r'Tests\s+([^\n]*)',txt)
        failnames=sorted(set(re.findall(r'FAIL .*?> ((?:RED|control) ks1868 [RC]\d [a-z-]*)',txt)))
        rows.append({'site':f+':'+label,'mutant':name,'rc':r.returncode,'killed':r.returncode!=0,'tests':tl[-1] if tl else '?','failing':failnames,'restore':ok})
        print(json.dumps(rows[-1]),flush=True)
        if not ok: sys.exit('RESTORE FAILED')
json.dump(rows,open(G+'/logs/mutants.json','w'),indent=1)
