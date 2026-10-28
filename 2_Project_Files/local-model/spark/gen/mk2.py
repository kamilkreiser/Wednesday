import sys, os, difflib, re, importlib.util
HERE=os.path.dirname(os.path.abspath(__file__))
SPARK=os.path.dirname(HERE)
SRC=os.environ.get('GEN_SRC',SPARK+'/cache/src/').rstrip('/')+'/'
BR=os.environ.get('GEN_BRIEFS',os.path.dirname(SPARK)+'/night/briefs/').rstrip('/')+'/'
TIP=os.environ.get('GEN_TIP','65bc28234507ffcf242381f8020d80b3efe83e85')
import subprocess
def rd(p):
    # default: the file as it is AT `TIP` (git show in the cache clone) so a brief regenerates the same on any day;
    # GEN_SRC=<dir> reads a checked-out tree instead
    if os.environ.get('GEN_SRC'): return open(SRC+p,encoding='utf-8').read()
    return subprocess.run(['git','-C',SRC.rstrip('/'),'show',TIP+':'+p],check=True,capture_output=True).stdout.decode('utf-8')
def trim(body):
    hunks=[];cur=None
    for l in body:
        if l.startswith('@@'):
            cur=[l,[]];hunks.append(cur)
        else: cur[1].append(l)
    res=[]
    for h,lines in hunks:
        m=re.match(r'@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@',h)
        os_,oc,ns,nc=int(m.group(1)),int(m.group(2) or 1),int(m.group(3)),int(m.group(4) or 1)
        i=0
        while i<len(lines) and lines[i][0]==' ': i+=1
        cut=0
        for k in range(i):
            if lines[k][1:].strip()=='': cut=k+1
        lines=lines[cut:]; os_+=cut; ns+=cut; oc-=cut; nc-=cut
        j=len(lines)
        while j>0 and lines[j-1][0]==' ': j-=1
        trail=lines[j:]
        keep=len(trail)
        for k,l in enumerate(trail):
            if l[1:].strip()=='': keep=k;break
        drop=len(trail)-keep
        if drop: lines=lines[:len(lines)-drop]; oc-=drop; nc-=drop
        res.append('@@ -%d,%d +%d,%d @@\n'%(os_,oc,ns,nc)); res+=lines
    return res
def udiff(path,old,new,newfile=False):
    a=old.splitlines(keepends=True); b=new.splitlines(keepends=True)
    out=[f'diff --git a/{path} b/{path}\n']
    if newfile: out.append('new file mode 100644\n'); out.append('--- /dev/null\n')
    else: out.append(f'--- a/{path}\n')
    out.append(f'+++ b/{path}\n')
    body=list(difflib.unified_diff(a,b,n=3))[2:]
    out+=trim(body)
    return ''.join(out)
def build(S):
    prods=[]; 
    for path,edits in S['products']:
        old=rd(path); new=old
        for e in edits:
            if callable(e): new=e(new); continue
            o,n=e
            assert new.count(o)==1,(path,o[:60],new.count(o))
            new=new.replace(o,n)
        prods.append((path,old,new))
    tests=[]
    for t in S['tests']:
        path=t['path']
        if t.get('new',True): tests.append((path,'',t['content'],True))
        else:
            old=rd(path); new=old
            for o,n in t['edits']:
                assert new.count(o)==1,(path,o[:60]); new=new.replace(o,n)
            tests.append((path,old,new,False))
    pd=[udiff(p,o,n) for p,o,n in prods]
    td=[udiff(p,o,n,nf) for p,o,n,nf in tests]
    golden=''.join(pd+td)
    d=BR+S['dir']
    if os.path.exists(d+'/golden.diff') and not os.environ.get('GEN_OVERWRITE'): sys.exit('REFUSED: %s already exists (set GEN_OVERWRITE=1 to replace it; briefs are tracked and may be queued or held)'%d)
    os.makedirs(d,exist_ok=True)
    open(d+'/golden.diff','w',encoding='utf-8').write(golden)
    open(d+'/spark.pins','w').write(S['pins'])
    T=S['ticket']; tier=S['tier']
    hdr=f"# {T} {S['title']}\n\n{S['intro']}\n\n"
    for i,(p,_,_) in enumerate(prods,1):
        hdr+=f"File: `{p}`  ({S['prodnote'][i-1]})\n"
    for (p,o,n,nf),note in zip(tests,S['testnote']):
        hdr+=f"Test file: `{p}`  ({note})\n"
    hdr+=f"Tip: `{TIP}` (origin/develop read through `git ls-remote` on 2026-10-28; every line number and quote below was read from the cache clone at exactly this sha)\nRunner: `{S['runner']}`\nTier: `{tier}`\nRung: {S['rung_raw'] if S.get('rung_raw') else '**'+S['rung']+'**'}\n\n"
    nfiles=len(prods)+len(tests)
    order=''
    k=1
    for p,_,_ in prods: order+=f"{k}. `{p}` - modified in place: EXACTLY the hunks under \"The exact change\", byte for byte.\n"; k+=1
    for p,o,n,nf in tests:
        if nf: order+=f"{k}. `{p}` - a NEW file: `--- /dev/null` (NEVER `--- a/`), `+++ b/<path>`, ONE hunk `@@ -0,0 +1,{len(n.splitlines())} @@`, every line `+`.\n"
        else: order+=f"{k}. `{p}` - modified in place: EXACTLY the hunks under \"The test\", byte for byte.\n"
        k+=1
    mode=f"## The mode - read this twice\n\nCODE+TEST. Your diff touches EXACTLY {nfiles} file(s), in this order:\n{order}\nYou never touch any other file and no other line of the files above.\n\n"
    wrong=f"## What is wrong (one paragraph)\n\n{S['wrong']}\n\n## Where\n\n{S['where']}\n\n"
    exact="## The exact change\n\n"+S.get('exactnote','')+"\n```diff\n"+''.join(pd)+"```\n\nThe `+` lines are byte-exact: copy them. Indentation is spaces only. Context lines begin with one space (the diff marker) followed by the file text.\n\n"+S.get('donot','')+"\n\n"
    if S.get('loose'): exact="## The exact change\n\nNo diff is given for the product file: you write it. "+S['loose']+"\n\n"+S.get('donot','')+"\n\n"
    test="## The test\n\n"
    for (p,o,n,nf),d_ in zip(tests,td):
        test+=f"File: `{p}`\n\n{S.get('testnote2','')}\n\n```diff\n{d_}```\n\n"
    red="## Red cells\n"+''.join(f"- {c}\n" for c in S['red'])+"\n## Cells and controls\n\n"+S['cells']+"\n\n"
    prem="## Premises (each one measured, with where)\n\n"+S['premises']+"\n\n## UNMEASURED - stated rather than glossed\n\n"+S['unmeasured']+"\n\n## Scope\n\n"+S['scope']+"\n\n"
    nfdiff=len(prods)+len(tests)
    outp=f"## Output\n\nExactly ONE fenced ```diff block, nothing outside it: {nfdiff} file section(s) in the order of `## The mode`"
    if any(nf for _,_,_,nf in tests): outp+="; a NEW file's section is `diff --git`, `new file mode 100644`, `--- /dev/null` (NEVER `--- a/`), `+++ b/<path>`, then the hunk header `@@ -0,0 +1,N @@` and every body line starting `+`"
    outp+=".\nEvery `+` line on its own physical line. Every context line keeps its leading space. Count each hunk header: old and new line counts must match the hunk body.\n"
    open(d+f'/{T}.md','w',encoding='utf-8').write(hdr+mode+wrong+exact+test+red+prem+outp)
    print('wrote',d,len(golden),'bytes golden')
if __name__=='__main__':
    spec=importlib.util.spec_from_file_location('s',sys.argv[1]); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m); build(m.S)
