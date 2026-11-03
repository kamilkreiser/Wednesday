import subprocess, re, shutil, sys, json
W='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate155-ks1868-pr1972'
D=W+'/clone/Blockchain/Dev/services/originate'
SRC=D+'/src'
files={'events':SRC+'/events.ts','db':SRC+'/db.ts'}
orig={k:open(v).read() for k,v in files.items()}
for k,v in orig.items(): open(W+f'/mutants/{k}.ts.orig','w').write(v)
sites=[('events','listener',0),('events','ctor',1),('db','initdb',0)]
def block(text,n):
    starts=[m.start() for m in re.finditer(r'let reason:',text)]
    s=starts[n]; e=re.search(r"(logger\.(debug|warn)|console\.error)\([^\n]*\n",text[s:]).end()+s
    return s,e
muts=[
 ('M1 constant->undefined', lambda b:b.replace("reason = 'unreadable thrown value';","reason = undefined;")),
 ('M2 String(m)->m (uncoerced)', lambda b:b.replace("String(m)","m")),
 ('M3 drop null/undef passthrough', lambda b:b.replace("m === undefined || m === null ? m : String(m)","String(m)")),
 ('M4 err?.message->err.message', lambda b:b.replace("err?.message","err.message")),
 ('M5 catch rethrows', lambda b:b.replace("reason = 'unreadable thrown value';","throw new Error('mut');")),
 ('M6 constant text changed', lambda b:b.replace("'unreadable thrown value'","'unknown'")),
 ('M7 logged field blanked', lambda b:re.sub(r"error: reason","error: undefined",b)),
 ('M8 read hoisted out of try', lambda b:b.replace("      try {\n        const m = err?.message;","      const m = err?.message;\n      try {").replace("    try {\n      const m = err?.message;","    const m = err?.message;\n    try {").replace("        try {\n          const m = err?.message;","        const m = err?.message;\n        try {")),
 ('M9 try swallow w/o constant (reason stays undefined)', lambda b:b.replace("reason = 'unreadable thrown value';","/* none */")),
]
extra={('events','ctor'):[('X1 ctor catch returns true',lambda t:t.replace("logger.warn('Failed to initialise EventBus', { error: reason });\n    return false;","logger.warn('Failed to initialise EventBus', { error: reason });\n    return true;"))]}
def run_tests():
    r=subprocess.run([D+'/node_modules/.bin/jest','--rootDir',D,'--config',D+'/jest.config.js','__tests__/ks1868-originate','--silent'],capture_output=True,text=True)
    out=re.sub(r'\x1b\[[0-9;]*m','',r.stdout+r.stderr)
    m=re.search(r'Tests:\s+(.*)',out)
    return r.returncode,(m.group(1) if m else 'NO SUMMARY: '+out[-200:])
def run_rec(tree=D):
    bad=[]
    for arm in ['ctor','listener','initdb']:
        for k in ['revoked_proxy','getter_throws','symbol_message','message_frozen_throwing_toString','message_nullproto','message_toPrimitive_object','proxy_get_throws','null','undefined','ordinary']:
            r=subprocess.run(['node',W+'/recorder/case.cjs',tree,arm,k],capture_output=True,text=True)
            line=[l for l in r.stdout.splitlines() if l.startswith('@@REC@@')]
            if not line: bad.append((arm,k,'norec')); continue
            d=json.loads(line[0][7:])
            ok = not d['uncaught'] and not d['unhandled'] and d['result'] in ('returns false','resolves','init ok; listener ok') and d['loggedCount']==1 and (d['loggedType']=='string' or k in('null','undefined'))
            if not ok: bad.append((arm,k,d['result'],d['loggedType']))
    return bad
res=[]
try:
  for fk,site,n in sites:
    for name,fn in muts:
        t=orig[fk]; s,e=block(t,n); nb=fn(t[s:e])
        if nb==t[s:e]: res.append((site,name,'NOOP (pattern absent)','','')); continue
        open(files[fk],'w').write(t[:s]+nb+t[e:])
        rc,sm=run_tests(); bad=run_rec() if rc==0 else []
        res.append((site,name,'KILLED' if rc!=0 else 'SURVIVED-by-tests',sm,('recorder kills: %d'%len(bad)) if rc==0 else ''))
        print(res[-1],flush=True)
        open(files[fk],'w').write(t)
    for name,fn in extra.get((fk,site),[]):
        t=orig[fk]; nt=fn(t)
        if nt==t: res.append((site,name,'NOOP','','')); continue
        open(files[fk],'w').write(nt); rc,sm=run_tests(); bad=run_rec() if rc==0 else []
        res.append((site,name,'KILLED' if rc!=0 else 'SURVIVED-by-tests',sm,('recorder kills: %d'%len(bad)) if rc==0 else '')); print(res[-1],flush=True)
        open(files[fk],'w').write(t)
finally:
  for k,v in files.items(): open(v,'w').write(orig[k])
json.dump(res,open(W+'/logs/mutants.json','w'),indent=1)
