import subprocess,hashlib,re,sys,shutil
G='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate98-ks1868-pr1916/'
M=G+'repo/Blockchain/Dev/services/api-gateway/src/routes/admin.ts'
head=open(G+'logs/admin_head.ts').read()
sha=lambda s:hashlib.sha256(s.encode()).hexdigest()
GUARD="""      let reason: string;
      try {
        reason = err instanceof Error ? err.message : String(err);
      } catch {
        reason = 'unreadable thrown value';
      }
      log('error', '%s', { error: reason });
"""
sites=[('P1users','[Identity] Failed to fetch users'),('P1orgs','[Identity] Failed to fetch organizations'),('P1level','[Identity] Failed to update level')]
def mut(name,msg,src):
    g=GUARD%msg
    assert src.count(g)==1,(msg,src.count(g))
    L=lambda body: body
    if name=='M0': r="      log('error', '%s', { error: err instanceof Error ? err.message : String(err) });\n"%msg
    elif name=='M1': r=g.replace("      try {\n        reason = err instanceof Error ? err.message : String(err);\n      } catch {\n        reason = 'unreadable thrown value';\n      }\n","      reason = err instanceof Error ? err.message : String(err);\n")
    elif name=='M2': r=g.replace("reason = 'unreadable thrown value';","reason = String(err);")
    elif name=='M3': r=g.replace("reason = 'unreadable thrown value';","throw err;")
    elif name=='M4': r=g.replace("reason = err instanceof Error ? err.message : String(err);","reason = 'unreadable thrown value';")
    elif name=='M5': r=g+"      throw err;\n"
    elif name=='M6': r=g.replace("err.message : String(err);","err.message : 'x';")
    elif name=='M7': r=g.replace("      log('error', '%s', { error: reason });\n"%msg,"")
    return src.replace(g,r)
names=['M0','M1','M2','M3','M4','M5','M6','M7']
only=sys.argv[1:]  # optional site filter
open(G+'logs/mutants_table.log','a').write('')
for sn,msg in sites:
    for n in names:
        if only and sn not in only: continue
        m=mut(n,msg,head)
        open(M,'w').write(m)
        lg=G+f'logs/mut_{sn}__{n}.log'
        rc=subprocess.call(['bash',G+'scripts/vt.sh',lg,'ks1868-admin-identity'])
        open(M,'w').write(head)
        ok = sha(open(M).read())==sha(head)
        out=open(lg).read()
        failed=sorted(set(re.findall(r'(?:FAIL|×)\s+.*?(R\d|C\d)\b',out)))
        kinds=sorted(set(re.findall(r'(AssertionError|TypeError|Error: [a-z ]+)',out)))[:3]
        line=f'{sn} {n} rc={rc} {"KILLED" if rc!=0 else "SURVIVED"} restore={ok} cells={failed} {kinds}'
        print(line,flush=True); open(G+'logs/mutants_table.log','a').write(line+'\n')
