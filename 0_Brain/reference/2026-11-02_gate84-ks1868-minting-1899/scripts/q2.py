import subprocess,re
W='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate84-ks1868-minting-1899'
F='Blockchain/Dev/services/nft-certificate/src/services/minting.service.ts'
d=subprocess.run(['git','-C',W+'/repo','diff','-U0','refs/gate/pr1899^','refs/gate/pr1899','--',F],capture_output=True,text=True).stdout
hunks=re.split(r'(?m)^@@ ',d)[1:]
print('hunks:',len(hunks))
norm=[]
for h in hunks:
    hdr,*body=h.split('\n')
    rem=[l[1:] for l in body if l.startswith('-')]
    add=[l[1:] for l in body if l.startswith('+')]
    print('@@',hdr.split(' @@')[0],'removed',len(rem),'added',len(add))
    # re-derive: removed line = logger.X('MSG', { error: EXPR });  added = guard + logger.X('MSG', { error: reason });
    m=re.match(r"\s*(logger\.\w+)\((.*), \{ error: (.*) \}\);$",rem[0]); 
    call,msg,expr=m.groups()
    expect=['let reason: string;','try {','  reason = '+expr+';','} catch {',"  reason = 'unreadable thrown value';",'}',call+'('+msg+', { error: reason });']
    got=[x.strip() if i in(0,1,3,5,6) else x.strip() for i,x in enumerate(add)]
    exp=[e.strip() for e in expect]
    print('  call',call,'| msg',msg,'| expr',expr)
    print('  guard shape == expected:',[x.strip() for x in add]==exp)
    print('  indent lines uniform:',len({len(x)-len(x.lstrip()) for x in add[:1]}))
    norm.append((call,expr,[x.strip() for x in add]))
print('all four exprs identical:',len({n[1] for n in norm})==1)
