# Mutants: one site x one form per run, product only, tests untouched, sha256 restored after every run.
import subprocess,json,hashlib,re,sys,os
G='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate137-ks1868-pr1955'
R=G+'/repo'; D=R+'/Blockchain/Dev'
PA=D+'/services/anchoring/src/index.ts'; PO=D+'/services/originate/src/routes/anchors.ts'
TO=D+'/services/originate/src/__tests__/ks1868-anchors-message-coercion-unreadable-throw.test.ts'
sha=lambda p: hashlib.sha256(open(p,'rb').read()).hexdigest()
A_LINE="reason = m === undefined || m === null ? m : String(m);"
O_LINES=["reason = String(err instanceof Error ? err.message : err);","reason = String(error instanceof Error ? error.message : error);"]
def sites(src, svc):
    # returns list of (start_index_of_guard_block, end_index) for the three guard blocks, in file order
    out=[]
    for m in re.finditer(r"let reason: string;\n\s*try \{\n(?:.*\n){1,2}?\s*\} catch \{\n\s*reason = 'unreadable thrown value';\n\s*\}\n", src):
        blk=m.group(0)
        if (svc=='anch' and A_LINE in blk) or (svc=='orig' and any(l in blk for l in O_LINES)): out.append((m.start(),m.end()))
    return out
def mutate(blk, form, svc):
    if svc=='anch':
        read="const m = err?.message;"
        forms={
          'M0_revert': lambda b: re.sub(r"const m = err\?\.message;\n(\s*)reason = .*;", r"reason = err?.message;", b),
          'M1_always_String': lambda b: b.replace(A_LINE,"reason = String(m);"),
          'M2_fallback_rethrows': lambda b: b.replace("reason = 'unreadable thrown value';","throw err;"),
          'M3_wrong_constant': lambda b: b.replace("reason = 'unreadable thrown value';","reason = 'x';"),
          'M4_always_constant': lambda b: b.replace(A_LINE,"void m; reason = 'unreadable thrown value';"),
          'M5_fallback_reads_value': lambda b: b.replace("reason = 'unreadable thrown value';","reason = String(err);"),
          'M6_template_literal': lambda b: b.replace("String(m)","`${m}`"),
        }
    else:
        forms={
          'M0_revert': lambda b: re.sub(r"reason = String\((err|error) instanceof Error \? \1\.message : \1\);", r"reason = \1 instanceof Error ? \1.message : String(\1);", b),
          'M2_fallback_rethrows': lambda b: b.replace("reason = 'unreadable thrown value';","throw new Error('g137 mutant');"),
          'M3_wrong_constant': lambda b: b.replace("reason = 'unreadable thrown value';","reason = 'x';"),
          'M4_always_constant': lambda b: re.sub(r"reason = String\(.*\);", "reason = 'unreadable thrown value';", b),
          'M5_fallback_reads_value': lambda b: re.sub(r"reason = 'unreadable thrown value';", "reason = String((err as any) ?? '');", b) if 'String(err ' in b else b.replace("reason = 'unreadable thrown value';","reason = String(error);"),
          'M6_template_literal': lambda b: re.sub(r"reason = String\((.*)\);", r"reason = `${\1}`;", b),
        }
    return forms[form](blk)
def run(svc, tag):
    out=f'{G}/logs/mut/{tag}'
    if svc=='anch':
        cmd=[D+'/node_modules/.bin/vitest','run','--root',D+'/services/anchoring','--maxWorkers=2','--reporter=json','--outputFile.json='+out+'.json','src/__tests__/ks1868-anchoring-message-coercion-unreadable-throw.test.ts']
    else:
        cmd=[D+'/node_modules/.bin/jest','--rootDir',D+'/services/originate','--config',D+'/services/originate/jest.config.js','--forceExit','--json','--outputFile='+out+'.json','--runTestsByPath',TO]
    env=dict(os.environ,TMPDIR='/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/c5199eda-e2e8-42ab-989c-f3882d521117/scratchpad')
    p=subprocess.run(['nice','-n','10']+cmd,capture_output=True,text=True,env=env,timeout=600)
    open(out+'.log','w').write(p.stdout+p.stderr+f'\nrc={p.returncode}\n')
    try: j=json.load(open(out+'.json'))
    except Exception: return p.returncode,['<no json>'],[]
    red=[];why=[]
    for t in j['testResults']:
        if not t['assertionResults'] and t.get('message'): red.append('<suite failed>'); why.append(t['message'][:80])
        for a in t['assertionResults']:
            if a['status']!='passed':
                nm=re.search(r'(C\d+|R\d+)',a['title']); red.append(nm.group(1) if nm else a['title'][:20])
                fm=' '.join(a.get('failureMessages') or [])
                why.append('timeout' if 'Exceeded timeout' in fm or 'timed out' in fm else ('assert' if re.search(r'expect|AssertionError|toBe|toEqual|toHaveLength',fm) else fm[:60]))
    return p.returncode,red,why
os.makedirs(G+'/logs/mut',exist_ok=True)
rows=[]
for svc,path,forms in [('anch',PA,['M0_revert','M1_always_String','M2_fallback_rethrows','M3_wrong_constant','M4_always_constant','M5_fallback_reads_value','M6_template_literal']),('orig',PO,['M0_revert','M2_fallback_rethrows','M3_wrong_constant','M4_always_constant','M5_fallback_reads_value','M6_template_literal'])]:
    orig=open(path).read(); h0=sha(path)
    ss=sites(orig,svc); assert len(ss)==3,(svc,len(ss))
    for i,(a,b) in enumerate(ss):
        for f in forms:
            blk=orig[a:b]; mb=mutate(blk,f,svc)
            if mb==blk: rows.append((svc,i+1,f,'NOT_APPLIED','','',True)); continue
            open(path,'w').write(orig[:a]+mb+orig[b:])
            rc,red,why=run(svc,f'{svc}_s{i+1}_{f}')
            open(path,'w').write(orig); ok=sha(path)==h0
            rows.append((svc,i+1,f,'KILLED' if red else 'SURVIVED',' '.join(red),','.join(sorted(set(why))),ok))
            print(rows[-1],flush=True)
with open(G+'/logs/mutants_table.log','w') as fh:
    for r in rows: fh.write('\t'.join(map(str,r))+'\n')
print('done', sum(1 for r in rows if r[3]=='KILLED'),'killed of',len(rows))
