// Gate 169 mutants: each replaces EXACTLY ONE occurrence in head's threadTokenIndex.ts, runs the PR's 2 test files and the
// gate's stand-in matrix, compares the matrix to the unmutated head matrix, restores the file and checks its sha256.
const fs=require('fs'),cp=require('child_process'),crypto=require('crypto');
const W='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate169-ks1962-pr1986';
const A=W+'/scratch/head/Blockchain/Dev/services/anchoring';const F=A+'/src/cardano/threadTokenIndex.ts';
const orig=fs.readFileSync(F,'utf8');const sha=s=>crypto.createHash('sha256').update(s).digest('hex');const S0=sha(orig);
const M=[
 ['M1 readRegistryOrNull answers [] (empty) on a failed read','    return null;\n  }\n}','    return [];\n  }\n}'],
 ['M2 utxoIsTrusted answers true on a failed read','if (registry === null) return false;','if (registry === null) return true;'],
 ['M3 filterUtxosByRegistry passes every UTxO through on a failed read','if (registry === null) return [];','if (registry === null) return utxos.map((utxo) => ({ utxo, documentId: null, policyId: null }));'],
 ['M4 loadActiveRegistry non-strict resolves [] again','      }\n      throw err;\n    }\n    let reason','      }\n      return [];\n    }\n    let reason'],
 ['M5 non-strict failure line carries the message value',"{ thrownType: thrownTypeOf(err) }","{ thrownType: thrownTypeOf(err), error: (() => { try { return String(err?.message); } catch { return 'x'; } })() }"],
 ['M6 strict failure swallowed in readRegistryOrNull','    if (STRICT_MODE) throw err;\n    return null;','    return null;'],
 ['M7 thrownTypeOf catch leaks a value-derived text',"    return 'unreadable';","    return 'unreadable:' + (() => { try { return String((value as any)?.message); } catch { return '?'; } })();"],
 ['M8 the "unreachable" trailing throw returns a fabricated registry row (expect EQUIVALENT)','    // KS-1962: unreachable (non-strict returned above); kept so the strict branch reads exactly as before.\n    throw err;',"    return [{ documentId: 'MUT', policyId: 'f'.repeat(56) }];"],
 ['M9 the non-strict branch removed (falls to the strict block)','    if (!STRICT_MODE) {\n      try {','    if (false as boolean) {\n      try {'],
 ['M10 the logger try/catch removed (a throwing logger replaces the original value)',"      try {\n        logger.error('state_thread_registry could not be read — no UTxO is trusted', { thrownType: thrownTypeOf(err) });\n      } catch {\n        // A logger that throws cannot turn the failed read into an empty registry; the original value is rethrown below.\n      }","      logger.error('state_thread_registry could not be read — no UTxO is trusted', { thrownType: thrownTypeOf(err) });"],
 ['M11 thrownTypeOf reports object for every object (constructor name dropped)',"return typeof name === 'string' && name !== '' ? name : 'object';","return 'object';"],
 ['M12 empty readable registry trusts nothing in non-strict (success path changed)','if (registry.length === 0) return !STRICT_MODE;','if (registry.length === 0) return false;'],
];
const norm=f=>fs.readFileSync(f,'utf8').trim().split('\n').map(l=>{const o=JSON.parse(l);for(const k of ['trustedForeign','trustedGenuine','filter','load'])delete o[k].ms;o.logs=o.logs.map(x=>x.replace(/"timestamp":"[^"]*"/,''));return JSON.stringify(o)});
const vt=(o,args,extra)=>{cp.spawnSync('bash',[W+'/harness/vt.sh','head',o,...args],{env:{...process.env,EXTRA_ENV:extra||''},stdio:'ignore'});const r=JSON.parse(fs.readFileSync(W+'/runs/'+o+'.json','utf8'));let p=0,f=0,a=0;for(const t of r.testResults)for(const x of t.assertionResults){if(x.status==='passed')p++;else{f++;if(/AssertionError/.test(x.failureMessages.join('')))a++}}return {p,f,a,files:r.testResults.length};};
const PR=['src/__tests__/ks1962-thread-token-registry-fails-closed.test.ts','src/__tests__/ks1868-thread-token-index-load-registry-catch-unreadable-throw.test.ts'];
const T=A+'/src/__tests__/';for(const f of ['g169-common.ts','g169-standin.test.ts'])fs.copyFileSync(W+'/harness/'+f,T+f);
const base=norm(W+'/runs/standin_head.jsonl');
const out=[];const ctl=vt('mut_control',PR);const ctlM=vt('mut_control_m',['src/__tests__/g169-standin.test.ts'],'G169_OUT='+W+'/runs/mut_control.jsonl LOG_LEVEL=debug');
const ctlDiff=norm(W+'/runs/mut_control.jsonl').filter((l,i)=>l!==base[i]).length;
out.push(`CONTROL unmutated: PR tests ${ctl.p}/${ctl.p+ctl.f} pass; matrix rows differing from head matrix: ${ctlDiff}`);
for(const [name,from,to] of M){const n=orig.split(from).length-1;if(n!==1){out.push(`${name}: NOT APPLIED (occurrences ${n})`);continue}
 fs.writeFileSync(F,orig.replace(from,to));
 const pr=vt('mut_pr',PR);vt('mut_m',['src/__tests__/g169-standin.test.ts'],'G169_OUT='+W+'/runs/mut_m.jsonl LOG_LEVEL=debug');
 const mm=norm(W+'/runs/mut_m.jsonl');const d=mm.filter((l,i)=>l!==base[i]).length;
 fs.writeFileSync(F,orig);const ok=sha(fs.readFileSync(F,'utf8'))===S0;
 out.push(`${name}: PR-tests ${pr.f?'KILLED':'survived'} (fail ${pr.f}, by assertion ${pr.a}, files ${pr.files}) | gate matrix ${d?'KILLED':'survived'} (${d} rows differ) | restored ${ok}`);
 console.log(out[out.length-1]);}
for(const f of ['g169-common.ts','g169-standin.test.ts'])fs.renameSync(T+f,W+'/mut/_quarantine_2026-11-03/head/'+f+'.post-mutants');
fs.writeFileSync(W+'/runs/mutants.txt',out.join('\n')+'\n');console.log(out[0]);
