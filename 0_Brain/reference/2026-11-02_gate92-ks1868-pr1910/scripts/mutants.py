import re,subprocess,hashlib,sys
W='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate92-ks1868-pr1910'
M=W+'/repo/Blockchain/Dev/services/mcp-server'; P=M+'/src/http-server.ts'
orig=open(P).read(); h0=hashlib.sha256(orig.encode()).hexdigest()
lines=[l for l in orig.split('\n') if 'describeThrown(err));' in l and "failed:'" in l and 'item failed' not in l]
print('sites',len(lines))
def mut(kind,l):
    ind=l[:len(l)-len(l.lstrip())]
    pre=l.strip().split(', describeThrown(err));')[0]
    if kind=='M0 revert inline read': return l.replace('describeThrown(err)',"(err instanceof Error ? err.message : String(err))")
    if kind=='M1 String(err)': return l.replace('describeThrown(err)','String(err)')
    if kind=='M2 constant x': return l.replace('describeThrown(err)',"'x'")
    if kind=='M3 log removed': return ind+'void 0;'
    if kind=='M4 wrong prefix': return l.replace('[mcp-http] ','[mcp] ')
    if kind=='M5 log raw err value': return l.replace('describeThrown(err)','err')
    if kind=='M6 helper-less message read': return l.replace('describeThrown(err)',"(err as Error)?.message")
kinds=['M0 revert inline read','M1 String(err)','M2 constant x','M3 log removed','M4 wrong prefix','M5 log raw err value','M6 helper-less message read']
files=['ks1868-mcp-http-route-catches-p1','ks1868-mcp-http-route-catches-p2','ks1868-mcp-http-route-catches-p3','ks1410-mcp-http-500-part-a','ks1410-mcp-http-500-part-b','ks1901-mcp-http']
out=[];surv=[]
try:
  for l in lines:
    site=re.search(r"\] (\S+ \S+) failed",l).group(1)
    for k in kinds:
        assert orig.count(l)==1,l
        open(P,'w').write(orig.replace(l,mut(k,l)))
        r=subprocess.run(['npx','vitest','run']+['src/__tests__/'+f for f in files],cwd=M,capture_output=True,text=True)
        t=r.stdout+r.stderr
        failed=sorted(set(re.findall(r'FAIL\s+src/__tests__/(\S+?)\.test\.ts',t)))
        nred=len(re.findall(r'^\s*(?:FAIL|×)',t,re.M))
        ok=hashlib.sha256(open(P,'w').write(orig) and orig.encode()).hexdigest()
        status='KILLED' if r.returncode!=0 else 'SURVIVED'
        if status=='SURVIVED': surv.append((site,k))
        out.append(f"{site:22} {k:28} {status} files={[f[:28] for f in failed]}")
        print(out[-1],flush=True)
finally:
  open(P,'w').write(orig)
  print('restore',hashlib.sha256(open(P).read().encode()).hexdigest()==h0)
print('survivors',surv)
