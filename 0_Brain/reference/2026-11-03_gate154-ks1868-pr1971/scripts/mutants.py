import subprocess, hashlib, json, re
W='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate154-ks1868-pr1971'
M=W+'/repo/Blockchain/Dev/services/m365-integration'
P=M+'/src/oauthState.ts'
orig=open(P).read(); sha=hashlib.sha256(orig.encode()).hexdigest()
BLOCK="""    let reason: string | null | undefined;
    try {
      const m = err?.message;
      reason = m === undefined || m === null ? m : String(m);
    } catch {
      reason = 'unreadable thrown value';
    }
    logger.warn('DB %s OAuth state failed', { error: reason });"""
def blk(w): return BLOCK % w
def tr(w, new): return ('B', blk(w), new)
sites={'save':'save','consume':'consume'}
def muts(w):
    b=blk(w)
    return {
     'M0 revert to unguarded err?.message': b.replace(b[:b.index("    logger.warn")], '')[0:0] or None,
    }
mut=[]
for w in ('save','consume'):
    b=blk(w)
    lw="    logger.warn('DB %s OAuth state failed', { error: reason });"%w
    mut += [
     (w,'M0 revert to unguarded', b, "    logger.warn('DB %s OAuth state failed', { error: err?.message });"%w),
     (w,'M1 catch rethrows', b, b.replace("reason = 'unreadable thrown value';","throw err;")),
     (w,'M2 constant text changed', b, b.replace("'unreadable thrown value'","'unreadable'")),
     (w,'M3 null/undefined branch inverted', b, b.replace("m === undefined || m === null ? m : String(m)","m === undefined || m === null ? String(m) : m")),
     (w,'M4 always constant', b, b.replace("reason = m === undefined || m === null ? m : String(m);","void m; reason = 'unreadable thrown value';")),
     (w,'M5 log line dropped', b, b.replace(lw,"    void reason;")),
     (w,'M6 String(m) dropped (pass-through)', b, b.replace("m === undefined || m === null ? m : String(m)","m")),
     (w,'M7 null/undefined stringified (always String)', b, b.replace("m === undefined || m === null ? m : String(m)","String(m)")),
     (w,'M8 meta key renamed', b, b.replace("{ error: reason }","{ err: reason }")),
     (w,'M9 log level raised to error', b, b.replace("logger.warn(","logger.error(")),
    ]
mut.append(('consume','M10 return null removed', None, None))
mut.append(('consume','M11 return true-ish stub (returns mem record)', None, None))
res=[]
def apply(site, name, old, new):
    # apply to the n-th occurrence: save = first occurrence, consume = second
    idx=orig.index(old) if site=='save' else orig.index(old, orig.index(old)+1)
    if old==blk('save') or old==blk('consume'):
        pass
    return orig[:idx]+new+orig[idx+len(old):]
for site,name,old,new in mut:
    if old is None:
        # consume-only structural mutants
        tail="    logger.warn('DB consume OAuth state failed', { error: reason });\n    return null;"
        if 'M10' in name: o,n=tail, "    logger.warn('DB consume OAuth state failed', { error: reason });"
        else: o,n=tail, "    logger.warn('DB consume OAuth state failed', { error: reason });\n    return memOAuthStates.get(stateHash) ?? null;"
        assert o in orig
        text=orig.replace(o,n,1)
    else:
        # old text for consume must be located in the consume function
        bs=blk(site)
        i=orig.index(bs)
        if site=='save':
            text=orig[:i]+orig[i:].replace(old,new,1) if False else orig[:i]+new+orig[i+len(bs):]
        else:
            # consume block is in the consume function: find it after "export async function consumeOAuthState"
            j=orig.index('export async function consumeOAuthState')
            k=orig.index(bs, j)
            text=orig[:k]+new+orig[k+len(bs):]
        # for M0 'new' is only a logger line, replace whole block
        if name.startswith('M0'):
            pass
    assert text!=orig, name
    open(P,'w').write(text)
    r=subprocess.run([W+'/repo/Blockchain/Dev/node_modules/.bin/vitest','run','--root',M,'src/__tests__/ks1868-oauth-state-db-catches-unreadable-throw.test.ts'],capture_output=True,text=True)
    out=r.stdout+r.stderr
    failed=re.findall(r'(?:FAIL|×)\s.*?(R\d|C\d)',out)
    failed=sorted(set(re.findall(r'(?:RED|control) ks1868 (R\d|C\d)',' '.join(l for l in out.splitlines() if 'FAIL' in l))))
    open(P,'w').write(orig)
    ok=hashlib.sha256(open(P).read().encode()).hexdigest()==sha
    res.append({'site':site,'mutant':name,'rc':r.returncode,'killed':r.returncode!=0,'cells':failed,'restored':ok})
    print(json.dumps(res[-1]),flush=True)
open(W+'/logs/mutants.jsonl','w').write('\n'.join(json.dumps(x) for x in res)+'\n')
