import subprocess, hashlib, json
W='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate122-ks1939-pr1940'
D=W+'/repo/Blockchain/Dev'; A=D+'/services/originate'; L=W+'/logs'
P=A+'/src/routes/verification.ts'
def sha(p): return hashlib.sha256(open(p,'rb').read()).hexdigest()
orig=open(P).read(); h0=sha(P)
AW="            return await respondExistenceOnly(\n"
G=("        let reason: string | undefined;\n        try {\n          reason = dbErr?.message;\n        } catch {\n          reason = 'unreadable thrown value';\n        }\n"
   "        logger.warn('Verification lookup failed', { documentId, error: reason });\n")
assert orig.count(AW)==1 and orig.count(G)==1
def rg(new): return orig.replace(G,new)
M={
 'P1 A0 drop await (revert)': orig.replace(AW,"            return respondExistenceOnly(\n"),
 'P1 A1 swallow: .catch answers lookup-failed with no log': orig.replace(AW,"            return await respondExistenceOnly(\n").replace(
     "'Document found by ID but no hash was provided. To verify integrity, provide the document file or its SHA-256 hash.',\n            );",
     "'Document found by ID but no hash was provided. To verify integrity, provide the document file or its SHA-256 hash.',\n            ).catch(() => res.json({ verified: false, error: 'Verification lookup failed' }));",1),
 'P1 A2 void (fire and forget)': orig.replace(AW,"            return void respondExistenceOnly(\n"),
 'P2 M0 unguard (revert)': rg("        logger.warn('Verification lookup failed', { documentId, error: dbErr?.message });\n"),
 'P2 M1 drop inner try': rg("        let reason: string | undefined;\n        reason = dbErr?.message;\n        logger.warn('Verification lookup failed', { documentId, error: reason });\n"),
 'P2 M2 catch -> String(dbErr)': rg(G.replace("reason = 'unreadable thrown value';","reason = String(dbErr);")),
 'P2 M3 catch rethrows': rg(G.replace("reason = 'unreadable thrown value';","throw dbErr;")),
 'P2 M4 constant for every value (swallow the readable)': rg(G.replace("reason = dbErr?.message;","reason = 'unreadable thrown value';")),
 'P2 M5 readable branch String()-wrapped': rg(G.replace("reason = dbErr?.message;","reason = String(dbErr?.message);")),
 'P2 M6 constant text changed': rg(G.replace("'unreadable thrown value'","'x'")),
 'P2 M7 log removed': rg(G.replace("        logger.warn('Verification lookup failed', { documentId, error: reason });\n","        void reason;\n")),
 'P2 M8 log ignores reason': rg(G.replace("error: reason }","error: reason && undefined }")),
 'P2 M9 unreadable -> 500 answer': rg(G.replace("reason = 'unreadable thrown value';","return res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Verification failed' } });")),
}
rows=[]
for name,txt in M.items():
    assert txt!=orig, name
    open(P,'w').write(txt)
    r=subprocess.run([D+'/node_modules/.bin/jest','--config',A+'/jest.config.js','--rootDir',A,'--forceExit','--json','--outputFile='+L+'/mut_tmp.json','ks1939-verification'],capture_output=True,text=True)
    open(P,'w').write(orig); ok=sha(P)==h0
    try:
        j=json.load(open(L+'/mut_tmp.json'))
        failed=[(t['name'].split('ks1939-verification-')[-1][:14],a['title'][:22],any('expect(' in m for m in a['failureMessages'])) for t in j['testResults'] for a in t['assertionResults'] if a['status']=='failed']
        nt=j['numTotalTests']; fs=[t['message'][:200] for t in j['testResults'] if t['status']=='failed' and not t['assertionResults']]
    except Exception as e:
        failed=[('PARSEFAIL',str(e),False)]; nt=-1; fs=[]
    res='KILLED' if failed or fs else 'SURVIVED'
    rows.append({'mutant':name,'result':res,'cells':len(failed),'byExpect':sum(1 for f in failed if f[2]),'failed':failed,'suiteErr':fs,'nt':nt,'restore':ok})
    print(f"{name:58} | {res:8} | {len(failed)} cells, {sum(1 for f in failed if f[2])} by expect | tests {nt} | restore {ok} | {[f[0][:6]+':'+f[1] for f in failed]}",flush=True)
json.dump(rows,open(L+'/mutants_table.json','w'),indent=1)
