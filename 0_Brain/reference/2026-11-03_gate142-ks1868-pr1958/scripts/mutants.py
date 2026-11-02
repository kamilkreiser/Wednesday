import subprocess, hashlib, os, re, sys
W='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate142-ks1868-pr1958'
Dev=W+'/repo/Blockchain/Dev'; A=Dev+'/services/anchoring'; S=A+'/src/'
V=Dev+'/node_modules/.bin/vitest'
SITES={
 'S':(S+'anchorStatusUpdate.ts','src/__tests__/ks1868-anchor-status-update-catch-unreadable-throw.test.ts'),
 'C':(S+'cardano/confirmation.ts','src/__tests__/ks1868-confirmation-wait-catch-unreadable-throw.test.ts'),
}
def sha(p): return hashlib.sha256(open(p,'rb').read()).hexdigest()
RD="reason = m === undefined || m === null ? m : String(m);"
def mut(site, name, t):
    if name=='M0_unguarded':
        t2=re.sub(r"let reason: string \| null \| undefined;\n\s*try \{\n\s*const m = err\?\.message;\n\s*"+re.escape(RD)+r"\n\s*\} catch \{\n\s*reason = 'unreadable thrown value';\n\s*\}", "const reason = err?.message;", t, count=1)
        return t2
    if name=='M1_try_dropped':
        t=t.replace("try {\n      const m = err?.message;","if (true) {\n      const m = err?.message;",1) if site=='S' else t.replace("try {\n          const m = err?.message;","if (true) {\n          const m = err?.message;",1)
        i=t.index(RD); j=t.index("} catch {", i); return t[:j]+"} else {"+t[j+len("} catch {"):]
    if name=='M2_const_text': return t.replace("reason = 'unreadable thrown value';","reason = 'x';",1)
    if name=='M3_no_String': return t.replace(RD,"reason = m;",1)
    if name=='M4_optchain_dropped': return t.replace("const m = err?.message;","const m = err.message;",1)
    if name=='M5_String_all': return t.replace(RD,"reason = String(m);",1)
    if name=='M6_null_to_text': return t.replace(RD,"reason = m === undefined ? m : m === null ? 'null' : String(m);",1)
    if name=='M7_undef_to_text': return t.replace(RD,"reason = m === null ? m : m === undefined ? 'undefined-msg' : String(m);",1)
    if name=='M8_const_always': return t.replace(RD,"reason = 'unreadable thrown value';",1)
    if name=='M9_catch_rethrows': return t.replace("reason = 'unreadable thrown value';","throw new Error('x');",1)
    if name=='M10_drop_report':
        if site=='S': return t.replace("{ anchorId, error: reason }","{ anchorId }",1)
        return t.replace("onStatusUpdate(attempt, `error: ${reason}`);","onStatusUpdate(attempt, 'error');",1)
    if name=='M11_site_specific':
        if site=='S': return t.replace("deps.log('warn', 'Failed to update anchor status in DB', { anchorId, error: reason });\n    return null;","deps.log('warn', 'Failed to update anchor status in DB', { anchorId, error: reason });\n    return 0;",1)
        return t.replace("errored += 1;\n      if (onStatusUpdate) {","if (onStatusUpdate) {",1)
    if name=='M12_site_specific2':
        if site=='S': return t.replace("{ anchorId, error: reason });","{ anchorId: 'x', error: reason });",1)
        return t.replace("        onStatusUpdate(attempt, `error: ${reason}`);\n      }\n    }","        onStatusUpdate(attempt, `error: ${reason}`);\n      }\n      return { confirmed: false, polled, errored };\n    }",1)
NAMES=['M0_unguarded','M1_try_dropped','M2_const_text','M3_no_String','M4_optchain_dropped','M5_String_all','M6_null_to_text','M7_undef_to_text','M8_const_always','M9_catch_rethrows','M10_drop_report','M11_site_specific','M12_site_specific2']
rows=[]
for site,(prod,test) in SITES.items():
    orig=open(prod).read(); h=sha(prod)
    for n in NAMES:
        m=mut(site,n,orig)
        if m is None or m==orig: rows.append((site,n,'NOOP (mutation did not apply)')); print(site,n,'NOOP'); continue
        open(prod,'w').write(m)
        r=subprocess.run([V,'run','--root',A,test],capture_output=True,text=True)
        out=r.stdout+r.stderr
        open(W+f'/logs/mut_{site}_{n}.log','w').write(out)
        open(prod,'w').write(orig); ok=(sha(prod)==h)
        tm=re.search(r'Tests\s+(.*)',out); res='KILLED' if r.returncode!=0 else 'SURVIVED'
        to='timeout' if 'timed out' in out else ''
        rows.append((site,n,res,tm.group(1).strip() if tm else '', 'restore '+str(ok), to)); print(rows[-1],flush=True)
open(W+'/logs/mutants_table.log','w').write('\n'.join(map(str,rows)))
