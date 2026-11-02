import subprocess,hashlib,shutil,re,json
W='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate143-ks1868-pr1959'
A=W+'/repo/Blockchain/Dev/services/auth'; P=A+'/src/events.ts'
V=W+'/repo/Blockchain/Dev/node_modules/.bin/vitest'
F=['src/__tests__/ks1868-auth-events-init-catch-unreadable-throw.test.ts','src/__tests__/ks1868-auth-events-redis-error-listener-unreadable-throw.test.ts']
orig=open(P).read(); sha=hashlib.sha256(orig.encode()).hexdigest()
# locate the two guards (listener first, catch second)
pat=re.compile(r"( *)let reason: string \| null \| undefined;\n.*?\n\1\}\n", re.S)
blocks=[m for m in pat.finditer(orig)]
assert len(blocks)==2, len(blocks)
names={0:'listener',1:'init-catch'}
def mut(kind,b):
    t=b
    if kind=='remove-guard':
        return re.sub(r"let reason.*?\n( *)\}\n(?=.*)", "", t, flags=re.S) if False else None
    if kind=='drop-optional-chain': return t.replace('err?.message','err.message')
    if kind=='wrong-constant': return t.replace("'unreadable thrown value'","'x'")
    if kind=='always-String': return t.replace("m === undefined || m === null ? m : String(m)","String(m)")
    if kind=='no-coercion': return t.replace("m === undefined || m === null ? m : String(m)","m")
    if kind=='swallow-undefined-in-catch': return t.replace("reason = 'unreadable thrown value';","reason = undefined;")
    if kind=='null-as-text': return t.replace("m === undefined || m === null ? m : String(m)","m === undefined ? m : String(m)")
    if kind=='undefined-as-text': return t.replace("m === undefined || m === null ? m : String(m)","m === null ? m : String(m)")
    if kind=='read-outside-try': return t.replace("try {\n","const m0 = err?.message;\n"+" "*0+"try {\n",1).replace("const m = err?.message;","const m = m0;")
    return None
kinds=['drop-optional-chain','wrong-constant','always-String','no-coercion','swallow-undefined-in-catch','null-as-text','undefined-as-text','read-outside-try']
res=[]
def run(label,src):
    open(P,'w').write(src)
    r=subprocess.run([V,'run','--root',A]+F,capture_output=True,text=True)
    out=r.stdout+r.stderr
    m=re.search(r"Tests\s+(.*)",out)
    res.append((label,r.returncode,(m.group(1) if m else '?')))
    print(label,r.returncode,m.group(1) if m else '?',flush=True)
try:
    # whole-guard removal (revert the hunk to base line)
    base=open(A+'/src/events_base.ts').read()
    for i in (0,1):
        b=blocks[i]; txt=b.group(0)
        repl = ("      logger.debug('EventBus Redis error (non-fatal)', { error: err.message });\n" if i==0 else None)
        # remove guard: replace block+following logger line using base text
        s=orig
        if i==0:
            full=re.search(r"    redis\.on\('error', \(err\) => \{\n.*?\n    \}\);\n",orig,re.S)
            s=orig.replace(full.group(0),"    redis.on('error', (err) => {\n      logger.debug('EventBus Redis error (non-fatal)', { error: err.message });\n    });\n")
        else:
            full=re.search(r"  \} catch \(err: any\) \{\n.*?\n    return false;\n",orig,re.S)
            s=orig.replace(full.group(0),"  } catch (err: any) {\n    logger.warn('Failed to initialise EventBus', { error: err?.message });\n    return false;\n")
        run('%s: remove-guard'%names[i],s)
    for i in (0,1):
        for k in kinds:
            b=blocks[i].group(0); nb=mut(k,b)
            if nb is None or nb==b: print('NOOP',names[i],k); res.append((names[i]+': '+k,'NOOP','')); continue
            run('%s: %s'%(names[i],k),orig[:blocks[i].start()]+nb+orig[blocks[i].end():])
finally:
    open(P,'w').write(orig)
    assert hashlib.sha256(open(P,'rb').read()).hexdigest()==sha; print('restored sha ok')
json.dump(res,open(W+'/logs/mutants.json','w'))
