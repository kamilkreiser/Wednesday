import subprocess,re,sys,collections
REPO='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate89-e25-1904-1906-1907/repo'
S='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_spark-operator57/'
files=collections.OrderedDict()
for fn in ('s_ternary.out','s_string.out','s_member.out'):
    for l in open(S+fn):
        p=l.split(':',2)
        files.setdefault(p[0],set()).add(int(p[1]))
excl=['billing/src/routes/billing.ts','nft-certificate/src/routes/nft.routes.ts','governance/','auth/src/services/issuerCert','auth/src/routes/issuerCerts','kyc/','tokenisation/','auth/src/routes/auth.ts','nft-certificate/src/services/minting','mcp-server/src/http-server','billing/src/routes/webhooks','security/src/index','tenant-provisioning/src/index','auth/src/routes/users','gdprService']
out=[]
for f,lines in files.items():
    if any(e in f for e in excl): continue
    src=subprocess.run(['git','-C',REPO,'show','origin/develop:Blockchain/Dev/services/'+f],capture_output=True,text=True).stdout.split('\n')
    # only ternary/String sites (s_ternary + s_string) count
    tern=set()
    for fn in ('s_ternary.out','s_string.out'):
        for l in open(S+fn):
            p=l.split(':',2)
            if p[0]==f: tern.add(int(p[1]))
    sites=[];g=0
    for n in sorted(tern):
        win=src[max(0,n-5):n+5]
        guarded=any('unreadable thrown value' in w or 'describeThrown' in w for w in win)
        (sites if not guarded else []).append(n) if not guarded else None
        g+=guarded
    out.append((f,len(tern),g,sites))
for f,t,g,s in sorted(out,key=lambda x:-len(x[3])):
    print(f,'total',t,'guarded_near',g,'unguarded',len(s),s)
