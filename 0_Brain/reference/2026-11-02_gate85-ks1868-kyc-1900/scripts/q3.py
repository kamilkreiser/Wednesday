import subprocess,re
W='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate85-ks1868-kyc-1900'
F='Blockchain/Dev/services/kyc/src/index.ts'
d=subprocess.run(['git','-C',W+'/repo','diff','-U0','refs/gate/pr1900^','refs/gate/pr1900','--',F],capture_output=True,text=True).stdout
hunks=re.split(r'(?m)^@@ ',d)[1:]
print('hunks:',len(hunks))
exprs=set(); ok=0
for h in hunks:
    hdr,*body=h.split('\n')
    rem=[l[1:] for l in body if l.startswith('-')]
    add=[l[1:] for l in body if l.startswith('+')]
    print('@@',hdr.split(' @@')[0],'removed',len(rem),'added',len(add))
    m=re.match(r"\s*(logger\.\w+)\(('[^']*'), \{ (?:(\w+), )?error: (.*) \}\);$",rem[0])
    call,msg,extra,expr=m.groups()
    pre=(extra+', ') if extra else ''
    exp=['let reason: string;','try {','reason = '+expr+';','} catch {',"reason = 'unreadable thrown value';",'}',call+'('+msg+', { '+pre+'error: reason });']
    got=[x.strip() for x in add]
    same=got==exp; ok+=same
    ind=[len(x)-len(x.lstrip()) for x in add]
    print('  call',call,'| msg',msg,'| extra key',extra,'| expr',expr,'| shape==expected',same,'| indents',ind)
    exprs.add(expr)
print('all exprs identical:',len(exprs)==1, exprs)
print('shape matches:',ok,'of',len(hunks))
