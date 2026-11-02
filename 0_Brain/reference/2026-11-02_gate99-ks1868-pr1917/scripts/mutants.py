import hashlib, subprocess, re, json, sys
W='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate99-ks1868-pr1917'
M=W+'/repo/Blockchain/Dev/services/tenant-provisioning/src/index.ts'
HEAD=open(W+'/logs/head_index.ts').read(); HL=HEAD.split('\n')
sha=lambda s: hashlib.sha256(s.encode()).hexdigest()
H0=sha(HEAD)
SITES={'S1 POST zod':(337,345),'S2 GET list zod':(386,394),'S5 PATCH :id zod':(562,570),
 'S3 GET :id':(440,445),'S4 PATCH status':(503,508),'S7 DELETE outer':(662,667),'S9 audit-log':(702,707),
 'S6 DELETE rollback':(637,643),'S8 DELETE audit':(674,680)}
ZOD={
 'Z0 probe removed (empty try)': lambda t: re.sub(r"      if \(!\(thrown instanceof z\.ZodError\)\) \{\n        String\(thrown instanceof Error \? thrown\.message : thrown\);\n      \}\n","",t),
 'Z1 invert zod test': lambda t: t.replace('if (!(thrown instanceof z.ZodError))','if (thrown instanceof z.ZodError)'),
 'Z2 fallback keeps thrown': lambda t: t.replace("err = new Error('unreadable thrown value');","err = thrown;"),
 'Z3 replace every value': lambda t: t.replace("    } catch {\n      err = new Error('unreadable thrown value');\n    }","    } catch {\n      /* */\n    }\n    err = new Error('unreadable thrown value');"),
 'Z4 unreadable -> ZodError(400)': lambda t: t.replace("err = new Error('unreadable thrown value');","err = new z.ZodError([]);"),
}
def msgm(var, src):
  return {
 'M0 guard removed': lambda t: re.sub(r"(\s*)let %s: string;\n\s*try \{\n\s*(%s = .*;)\n\s*\} catch \{\n\s*%s = 'unreadable thrown value';\n\s*\}" % (var,var,var), lambda m: m.group(1)+'const '+m.group(2), t),
 'M1 fallback re-reads': lambda t: t.replace("%s = 'unreadable thrown value';" % var, "%s = String(%s);" % (var,src)),
 'M2 constant for every value': lambda t: t.replace("%s = %s instanceof Error ? %s.message : String(%s);" % (var,src,src,src), "%s = 'unreadable thrown value';" % var),
 'M3 fallback rethrows': lambda t: t.replace("%s = 'unreadable thrown value';" % var, "throw new Error('unreadable thrown value');"),
}
def mutate(site, fn):
  a,b=SITES[site]; seg='\n'.join(HL[a-1:b]); new=fn(seg)
  if new==seg: return None
  return '\n'.join(HL[:a-1]+new.split('\n')+HL[b:])
rows=[]
for site in SITES:
  if 'zod' in site: muts=ZOD
  elif 'rollback' in site: muts=msgm('reason','rollbackErr')
  elif 'DELETE audit' in site: muts=msgm('reason','auditErr')
  else: muts=msgm('message','err')
  for name,fn in muts.items():
    txt=mutate(site,fn)
    if txt is None: rows.append((site,name,'NOT APPLIED','')); continue
    open(M,'w').write(txt)
    tag=re.sub(r'\W+','_',site+'__'+name)
    log=f'{W}/logs/mut_{tag}.log'
    rc=subprocess.run(['bash',W+'/scripts/vt.sh',log]).returncode
    out=open(log).read()
    fails=sorted(set(re.findall(r'FAIL  src/__tests__/(\S+?)\.test\.ts > (.*)',out)))
    kinds=sorted(set(re.findall(r'^\s*(\w*Error):',out,re.M)))
    summ=re.findall(r'Tests\s+(.*)',out)
    open(M,'w').write(HEAD); ok=sha(open(M).read())==H0
    rows.append((site,name,'KILLED' if rc!=0 else 'SURVIVED', f"{summ[-1] if summ else '?'} | errs {kinds} | restore {ok} | "+'; '.join(f'{f}:{t[:70]}' for f,t in fails[:4])))
    print(rows[-1],flush=True)
with open(W+'/logs/mutants_table.log','w') as f:
  for r in rows: f.write(' | '.join(r)+'\n')
