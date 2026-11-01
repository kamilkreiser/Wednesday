import subprocess,hashlib,re,json,sys,os
W='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate96-ks1868-pr1914'
A=W+'/repo/Blockchain/Dev/services/analytics'
PROD=A+'/src/routes/analytics.ts'
orig=open(PROD).read()
sha=hashlib.sha256(orig.encode()).hexdigest()
assert sha.startswith('d5afff9cd2073371')
Z_BLOCK="""    let error: unknown = thrown;
    try {
      if (!(thrown instanceof z.ZodError)) {
        String(thrown instanceof Error ? thrown.message : thrown);
      }
    } catch {
      error = new Error('unreadable thrown value');
    }
"""
Z_MUT={
 'M0_revert_no_probe': "    let error: unknown = thrown;\n",
 'M1_probe_read_removed': Z_BLOCK.replace("        String(thrown instanceof Error ? thrown.message : thrown);\n","        void thrown;\n"),
 'M2_swallow_wrong_value(error=thrown)': Z_BLOCK.replace("error = new Error('unreadable thrown value');","error = thrown;"),
 'M3_replace_always': Z_BLOCK.replace("let error: unknown = thrown;","let error: unknown = new Error('unreadable thrown value');"),
 'M4_rethrow': Z_BLOCK.replace("error = new Error('unreadable thrown value');","throw thrown;"),
 'M5_const_text_changed': Z_BLOCK.replace("new Error('unreadable thrown value')","new Error('x')"),
 'M6_guard_inverted': Z_BLOCK.replace("if (!(thrown instanceof z.ZodError))","if (thrown instanceof z.ZodError)"),
 'M7_probe_instanceof_only': Z_BLOCK.replace("String(thrown instanceof Error ? thrown.message : thrown);","void (thrown instanceof Error);"),
 'M8_zod_check_dropped_from_probe': Z_BLOCK.replace("if (!(thrown instanceof z.ZodError)) {","if (true) {"),
}
R_RE=re.compile(r"    let reason: string;\n    try \{\n      reason = error instanceof Error \? error\.message : String\(error\);\n    \} catch \{\n      reason = 'unreadable thrown value';\n    \}\n")
R_BLOCK="    let reason: string;\n    try {\n      reason = error instanceof Error ? error.message : String(error);\n    } catch {\n      reason = 'unreadable thrown value';\n    }\n"
R_MUT={
 'M0_revert_unguarded': "    const reason = error instanceof Error ? error.message : String(error);\n",
 'M1_const_for_all': "    let reason: string;\n    reason = 'unreadable thrown value';\n",
 'M2_rethrow': R_BLOCK.replace("reason = 'unreadable thrown value';","throw error;"),
 'M3_text_changed': R_BLOCK.replace("reason = 'unreadable thrown value'","reason = 'x'"),
 'M4_readable_string_branch_const': R_BLOCK.replace("String(error)","'x'"),
 'M5_readable_error_branch_const': R_BLOCK.replace("error.message : String","'x' : String"),
 'M6_no_guard_String_only': "    let reason: string;\n    try {\n      reason = String(error);\n    } catch {\n      reason = 'unreadable thrown value';\n    }\n",
}
ZNAMES=['GET /overview','GET /certifications','GET /verifications','GET /governance','GET /revenue','GET /users','GET /activity','POST /exports','POST /reports']
RNAMES=['GET /realtime','GET /exports/:id','GET /exports']
def nth(text,block,i):
    idx=-1
    for _ in range(i+1):
        idx=text.index(block,idx+1)
    return idx
def run():
    p=subprocess.run(['npx','vitest','run','src/__tests__/ks1868-analytics-routes','--reporter=json'],cwd=A,capture_output=True,text=True)
    try:
        j=json.loads(p.stdout[p.stdout.index('{'):])
    except Exception as e:
        return None,[str(e)]
    fails=[]
    for f in j['testResults']:
        for t in f['assertionResults']:
            if t['status']=='failed': fails.append(t['title'])
        if f['status']=='failed' and not f['assertionResults']: fails.append('SUITE_ERROR '+f['name'].split('/')[-1])
    return j['numFailedTests'],fails
assert orig.count(Z_BLOCK)==9, orig.count(Z_BLOCK)
assert orig.count(R_BLOCK)==3, orig.count(R_BLOCK)
rows=[]
def go(kind,block,muts,names):
    for i,name in enumerate(names):
        for mn,rep in muts.items():
            idx=nth(orig,block,i)
            assert rep!=block, (mn)
            new=orig[:idx]+rep+orig[idx+len(block):]
            open(PROD,'w').write(new)
            try: n,f=run()
            finally:
                open(PROD,'w').write(orig)
            ok=hashlib.sha256(open(PROD).read().encode()).hexdigest()==sha
            cells=sorted(set(re.sub(r'^(RED|control) ks1868 (\w\d) .*',r'\2',t) for t in f if re.match(r'(RED|control)',t)))
            own=[t for t in f if (name+':') in t]
            row=dict(site=name,mutant=mn,failed=n,restored=ok,cells=cells,own_route_cells=len(own),other_route_cells=len(f)-len(own),killed=bool(n))
            rows.append(row); print(json.dumps(row),flush=True)
go('z',Z_BLOCK,Z_MUT,ZNAMES)
go('r',R_BLOCK,R_MUT,RNAMES)
json.dump(rows,open(W+'/logs/mutants.json','w'),indent=1)
print('killed',sum(r['killed'] for r in rows),'of',len(rows),'all restored',all(r['restored'] for r in rows))
