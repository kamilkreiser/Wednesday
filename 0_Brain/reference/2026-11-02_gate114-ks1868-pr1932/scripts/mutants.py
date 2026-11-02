# Per-site mutants on the PR's changed lines (product only; tests untouched; sha256-restored after each run).
import hashlib, json, subprocess, sys, os
G='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate114-ks1868-pr1932'
R=G+'/repo/Blockchain/Dev/services/'
FA=R+'anchoring/src/index.ts'; FO=R+'originate/src/routes/anchors.ts'
TA='src/__tests__/ks1868-anchoring-read-route-catches-unreadable-throw.test.ts'
TO=R+'originate/src/__tests__/ks1868-anchors-route-catches-unreadable-throw.test.ts'
sha=lambda p: hashlib.sha256(open(p,'rb').read()).hexdigest()
A_GUARD="""      let reason: string;
      try {
        reason = err?.message;
      } catch {
        reason = 'unreadable thrown value';
      }
      log('warn', '%s', { error: reason });"""
TX_GUARD="""    let reason: string;
    try {
      reason = err?.message;
    } catch {
      reason = 'unreadable thrown value';
    }
    log('warn', 'DB lookup anchor by tx failed', { txHash, error: reason });"""
def a_site(msg): return A_GUARD % msg
def a_muts(orig, logcall_new):
    base_line = logcall_new.replace('error: reason', 'error: err?.message')
    ind = orig.split('let reason')[0]
    return {
      'revert': base_line,
      'fallback_rethrows': orig.replace("reason = 'unreadable thrown value';", "throw err;"),
      'wrong_constant': orig.replace("'unreadable thrown value'", "'x'"),
      'always_constant': orig.replace("reason = err?.message;", "reason = 'unreadable thrown value';"),
      'fallback_reads_value': orig.replace("reason = 'unreadable thrown value';", "reason = String(err);"),
      'log_dropped': orig.replace(logcall_new, ind + 'void reason;'),
    }
SITES=[]
for name,msg in [('A1_verify_by_hash','verify-by-hash: local DB lookup failed'),('A2_verify_post','DB lookup anchor by content hash failed')]:
    o=a_site(msg); SITES.append((name,FA,o,a_muts(o, f"      log('warn', '{msg}', {{ error: reason }});")))
SITES.append(('A3_tx',FA,TX_GUARD,a_muts(TX_GUARD,"    log('warn', 'DB lookup anchor by tx failed', { txHash, error: reason });")))
O1="""    let reason: string;
    try {
      reason = err instanceof Error ? err.message : String(err);
    } catch {
      reason = 'unreadable thrown value';
    }
    logger.error('anchors: database connection FAILED — anchor operations will not be available', {
      error: reason,
    });"""
O2="""    let reason: string;
    try {
      reason = err instanceof Error ? err.message : String(err);
    } catch {
      reason = 'unreadable thrown value';
    }
    logger.warn('Failed to fetch anchor from DB', { documentId, error: reason });"""
O3="""      let reason: string;
      try {
        reason = error instanceof Error ? error.message : String(error);
      } catch {
        reason = 'unreadable thrown value';
      }
      logger.error('Failed to get anchor', { error: reason });"""
def o_muts(orig, var, logline_new, revert):
    expr=f"{var} instanceof Error ? {var}.message : String({var})"
    return {
      'revert': revert,
      'fallback_rethrows': orig.replace("reason = 'unreadable thrown value';", f"throw {var};"),
      'wrong_constant': orig.replace("'unreadable thrown value'", "'x'"),
      'always_constant': orig.replace(f"reason = {expr};", "reason = 'unreadable thrown value';"),
      'fallback_reads_value': orig.replace("reason = 'unreadable thrown value';", f"reason = String({var});"),
      'guard_only_message': orig.replace(f"reason = {expr};", f"reason = {var} instanceof Error ? {var}.message : 'nonerror';").replace("} catch {", "} catch {").replace(f"    }}\n", f"    }}\n") ,
    }
SITES.append(('O1_dbready',FO,O1,o_muts(O1,'err',None,"""    logger.error('anchors: database connection FAILED — anchor operations will not be available', {
      error: err instanceof Error ? err.message : String(err),
    });""")))
SITES.append(('O2_lookup_warn',FO,O2,o_muts(O2,'err',None,"""    logger.warn('Failed to fetch anchor from DB', { documentId, error: err instanceof Error ? err.message : String(err) });""")))
SITES.append(('O3_route_catch',FO,O3,o_muts(O3,'error',None,"""      logger.error('Failed to get anchor', { error: error instanceof Error ? error.message : String(error) });""")))
# guard_only_message for O sites: String(x) of a non-Error is left unguarded -> outside the try
for i,(n,f,o,m) in enumerate(SITES):
    if n.startswith('O'):
        var='error' if n=='O3_route_catch' else 'err'
        expr=f"{var} instanceof Error ? {var}.message : String({var})"
        m['string_unguarded']=o.replace(f"reason = {expr};", f"reason = {var} instanceof Error ? {var}.message : '';").replace("let reason: string;", f"let reason: string = String({var});").replace(f"{var}.message : '';", f"{var}.message : reason;")
        del m['guard_only_message']
ONLY=sys.argv[1:]
def run(svc, out):
    if svc=='anchoring':
        cmd=['bash',G+'/scripts/run.sh','anchoring',out,TA]
    else:
        cmd=['bash',G+'/scripts/run.sh','originate',out,'--runTestsByPath',TO]
    subprocess.run(cmd)
    try: d=json.load(open(out+'.json'))
    except Exception as e: return {'error':'no json '+str(e)}
    red=[]
    for f in d['testResults']:
        for a in f['assertionResults']:
            if a['status']=='failed':
                m=(a.get('failureMessages') or [''])[0]
                why='TIMEOUT' if 'Exceeded timeout' in m or 'timed out' in m.lower() else ('ASSERT' if ('AssertionError' in m or 'expect(' in m) else 'OTHER:'+m[:80])
                red.append(a['title'].split(' ')[1]+' '+a['title'].split(' ')[2]+':'+why)
    return {'total':d['numTotalTests'],'failed':d['numFailedTests'],'red':red,'failedSuites':d.get('numFailedTestSuites')}
res=[]
os.makedirs(G+'/logs/mut',exist_ok=True)
for name,f,orig,muts in SITES:
    for mn,new in muts.items():
        key=f'{name}.{mn}'
        if ONLY and key not in ONLY: continue
        h0=sha(f); src=open(f).read()
        assert src.count(orig)==1, f'site not unique {name}'
        assert new!=orig, f'mutant identical {key}'
        open(f,'w').write(src.replace(orig,new))
        try:
            r=run('anchoring' if f==FA else 'originate', G+'/logs/mut/'+key)
        finally:
            open(f,'w').write(src)
        ok=sha(f)==h0
        line={'mutant':key,**r,'restore_ok':ok}
        print(json.dumps(line),flush=True); res.append(line)
        if not ok: sys.exit('RESTORE FAILED '+key)
