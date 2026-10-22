import subprocess, re, sys, collections
G=sys.argv[1]
def git(*a): return subprocess.run(['git','-C',G,'--no-optional-locks',*a],capture_output=True,text=True,errors='replace').stdout
prs=[('#83','21c2aec7'),('#84','acfcf5de'),('#87','1b32bbe6'),('#85','f2584d36'),('#88','77e541c8'),('#86','67bf2004'),('#89','d2b956b7'),('#90','7bd7046a'),('#91','f78c6408'),('#92','1eccbc8b'),('#93','f5b6f5a7')]
lit=re.compile(r'''"((?:[^"\\]|\\.){6,})"|'((?:[^'\\]|\\.){6,})'|`((?:[^`\\]|\\.){6,})`''')
def prod(p):
    if not (p.startswith('web/src/') or p.startswith('src/') or p.startswith('docs/')): return False
    if re.search(r'\.test\.|/qa/|\.d\.ts|generated/|\.css$|\.json$',p): return False
    return p.endswith(('.ts','.tsx','.cs','.md'))
out=open(sys.argv[2],'w'); summ=collections.OrderedDict()
for pr,c in prs:
    files=[f for f in git('diff','--name-only',c+'^',c).split('\n') if f and prod(f)]
    n=0
    for f in files:
        d=git('diff','-U0',c+'^',c,'--',f)
        for ln in d.split('\n'):
            if not ln.startswith('+') or ln.startswith('+++'): continue
            t=ln[1:].strip()
            if f.endswith('.md'):
                if len(t)>20 and not t.startswith(('|---','```')): out.write(f'{pr}\t{f}\t{t[:200]}\n'); n+=1
                continue
            if t.startswith(('//','*','/*','///','import ','export type','export interface')): continue
            for m in lit.finditer(t):
                s=next(x for x in m.groups() if x is not None)
                if ' ' not in s or not re.search(r'[A-Za-z]{3}',s): continue
                if re.search(r'^(\.|/|#|\$\{)|[=>]{2}|^[a-z-]+( [a-z-]+)*:|\bclass(Name)?\b|^(GET|POST|PUT|DELETE) ',s) and not re.match(r'^[A-Z]',s): continue
                if re.match(r'^[a-z0-9_ -]+$',s) and s.count(' ')<2: continue
                out.write(f'{pr}\t{f}\t{s[:200]}\n'); n+=1
    summ[pr]=(len(files),n)
for k,v in summ.items(): print(k,'prod files',v[0],'candidate strings',v[1])
print('total',sum(v[1] for v in summ.values()))
