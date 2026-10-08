import subprocess, sys, re, difflib, collections, hashlib
R='/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/ba10491f-d904-4eb7-a83b-e46c1bc8cc8e/scratchpad/gate75/clone'
B,H=sys.argv[1],sys.argv[2]
DOCS={'D1':'Projects Documents/API_Security_Functional_Testing_Architecture_Flow_Diagrams.html','D2':'Projects Documents/QA_Tool_Cheat_Sheet_Secuura_API_Testing.html'}
def show(rev,p): return subprocess.run(['git','-C',R,'show',f'{rev}:{p}'],capture_output=True,check=True).stdout.decode('utf-8')
TAG=re.compile(r'<(/?)([a-zA-Z][a-zA-Z0-9]*)(\s[^>]*)?>')
VOID={'br','hr','img','meta','link','input','wbr','col','source'}
def tags(t):
    c=collections.Counter()
    for m in TAG.finditer(t):
        n=m.group(2).lower()
        if n in VOID: continue
        c[(n,'close' if m.group(1) else 'open')]+=1
    return c
def bal(c): return {n:(c[(n,'open')],c[(n,'close')]) for n in sorted({k[0] for k in c}) if c[(n,'open')]!=c[(n,'close')]}
frags={}
for k,p in DOCS.items():
    b=show(B,p).split('\n'); h=show(H,p).split('\n')
    diff=[(i,j) for i,j in [(i,i) for i in range(min(len(b),len(h)))] if b[i]!=h[j]]
    print(k,p); print('  lines base',len(b),'head',len(h),'differing line idx (1-based)',[i+1 for i,_ in diff])
    for i,_ in diff:
        bl,hl=b[i],h[i]
        sm=difflib.SequenceMatcher(None,bl,hl,autojunk=False); ops=[o for o in sm.get_opcodes() if o[0]!='equal']
        print('  opcodes',[(o[0],o[1],o[2],o[3],o[4]) for o in ops])
        ins=[hl[o[3]:o[4]] for o in ops if o[0]=='insert']
        only_insert=all(o[0]=='insert' for o in ops) and len(ops)==1
        print('  INSERTION ONLY (one insert opcode):',only_insert)
        if only_insert:
            f=ins[0]; frags[k]=f
            print('  fragment bytes',len(f.encode()),'sha256/16',hashlib.sha256(f.encode()).hexdigest()[:16])
            print('  head line minus fragment == base line:', hl.replace(f,'',1)==bl, '| fragment occurs in head doc', '\n'.join(h).count(f))
            ft=tags(f); print('  fragment tag counts', dict(ft), 'unbalanced-in-fragment', bal(ft))
    tb,th=tags('\n'.join(b)),tags('\n'.join(h))
    print('  whole-doc unbalanced base',bal(tb),'head',bal(th))
    for n in ('code','tr','td'): print('   ',n,'base',(tb[(n,'open')],tb[(n,'close')]),'head',(th[(n,'open')],th[(n,'close')]))
    print('  CONTROL literal "<code>" opens base', '\n'.join(b).count('<code>'), 'vs attribute-aware', tb[('code','open')])
print('PARITY: the clause text') 
cl={k:re.sub(r'^(?:</td></tr><tr><td>)?\s*','',re.sub(r'(?:</td></tr><tr><td>[^<]*)?$','',v)) for k,v in frags.items()}
for k,v in frags.items(): print(' ',k,repr(v[:60]),'...',repr(v[-40:]))
core=lambda s: s[s.index('One bounded exemption'):s.index('silently.')+len('silently.')]
c1,c2=core(frags['D1']),core(frags['D2']); print('  core clause identical D1==D2:',c1==c2,'len',len(c1)); print('  CORE:',c1)
