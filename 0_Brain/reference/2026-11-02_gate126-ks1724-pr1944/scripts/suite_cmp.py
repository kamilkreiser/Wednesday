# Compare base vs head per unit: summary line, and the set of failing test names (vitest × / FAIL lines, jest ✕).
import re,os,glob
G='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate126-ks1724-pr1944/logs/suites/'
def parse(p):
    if not os.path.exists(p): return None
    t=open(p,errors='replace').read()
    summ=re.findall(r'^\s*Tests\s+(.*)$',t,flags=re.M)
    files=re.findall(r'^\s*Test (?:Files|Suites):?\s+(.*)$',t,flags=re.M)
    fails=set()
    for l in t.splitlines():
        m=re.match(r'\s*FAIL\s+(\S+\.test\.ts)\s+>\s+(.*?)\s*$',l)
        if m: fails.add(m.group(1)+' > '+re.sub(r'\s+\d+ms$','',m.group(2)))
        m=re.match(r'\s*[×✕]\s+(.*?)(\s+\(?\d+\s?ms\)?)?$',l)
        if m: fails.add('x '+m.group(1))
    rc=re.findall(r'^rc=(\d+)',t,flags=re.M)
    load=re.findall(r'load=\{([^}]*)\}',t)
    return dict(summ=summ[-1].strip() if summ else '?',files=files[-1].strip() if files else '?',fails=fails,rc=rc[-1] if rc else '?',load=load[0].strip() if load else '?')
units=sorted(set(re.sub(r'_(base|repo)\.log$','',os.path.basename(p)) for p in glob.glob(G+'*_*.log')))
for u in units:
    b=parse(G+u+'_base.log'); h=parse(G+u+'_repo.log')
    if not b or not h: print(u,'INCOMPLETE'); continue
    newf=h['fails']-b['fails']; gone=b['fails']-h['fails']; both=b['fails']&h['fails']
    print(f"== {u}: base rc={b['rc']} [{b['files']}] [{b['summ']}] load {b['load']} | head rc={h['rc']} [{h['files']}] [{h['summ']}] load {h['load']}")
    for x in sorted(both): print('   RED BOTH:',x[:200])
    for x in sorted(newf): print('   RED HEAD ONLY:',x[:200])
    for x in sorted(gone): print('   RED BASE ONLY:',x[:200])
