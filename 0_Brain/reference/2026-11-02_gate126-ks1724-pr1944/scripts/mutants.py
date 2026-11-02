# Mutants on boundedJson (product only, tests untouched), in the mut/ worktree; sha256 restored + checked after each run.
import subprocess,hashlib,re,sys
G='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate126-ks1724-pr1944'
D=G+'/mut/Blockchain/Dev'
RL=D+'/packages/shared/src/middleware/request-limits.ts'
VC=D+'/services/vc-issuer/src/index.ts'
sha=lambda p: hashlib.sha256(open(p,'rb').read()).hexdigest()
def rep(old,new,count=1):
    def f(s):
        assert s.count(old)==count,(old,s.count(old)); return s.replace(old,new)
    return f
M={
 'M01_no_array_check': (RL,[rep("      if (v.length > caps.maxArrayLength) return 'array length';\n","")]),
 'M02_no_node_check_per_pop': (RL,[rep("    if (nodes > caps.maxNodes) return 'node count';\n","")]),
 'M03_no_node_precheck_array': (RL,[rep("      if (nodes + stack.length + v.length > caps.maxNodes) return 'node count';\n","")]),
 'M04_no_node_precheck_object': (RL,[rep("      if (nodes + stack.length + keys.length > caps.maxNodes) return 'node count';\n","")]),
 'M05_no_node_checks_at_all': (RL,[rep("    if (nodes > caps.maxNodes) return 'node count';\n",""),rep("      if (nodes + stack.length + v.length > caps.maxNodes) return 'node count';\n",""),rep("      if (nodes + stack.length + keys.length > caps.maxNodes) return 'node count';\n","")]),
 'M06_no_depth_check': (RL,[rep("    if (depth >= caps.maxDepth) return 'depth';\n","")]),
 'M07_array_off_by_one_ge': (RL,[rep("v.length > caps.maxArrayLength","v.length >= caps.maxArrayLength")]),
 'M08_array_off_by_one_plus1': (RL,[rep("v.length > caps.maxArrayLength","v.length > caps.maxArrayLength + 1")]),
 'M09_nodes_ge_everywhere': (RL,[rep("> caps.maxNodes",">= caps.maxNodes",3)]),
 'M10_nodes_plus1_everywhere': (RL,[rep("> caps.maxNodes","> caps.maxNodes + 1",3)]),
 'M11_depth_gt': (RL,[rep("depth >= caps.maxDepth","depth > caps.maxDepth")]),
 'M12_depth_minus1': (RL,[rep("depth >= caps.maxDepth","depth >= caps.maxDepth - 1")]),
 'M13_drop_warn': (RL,[rep("      log.warn('request body refused by the structural JSON cap', { service, kind: breach, path });\n","")]),
 'M14_handler_runs_instead_of_refusal': (RL,[rep("      res.status(400).json({\n        success: false,\n        error: { code: 'BAD_REQUEST', message: `Request body exceeds the structural limit (${breach}).` },\n      });\n","      next();\n")]),
 'M15_handler_runs_after_refusal': (RL,[rep("        error: { code: 'BAD_REQUEST', message: `Request body exceeds the structural limit (${breach}).` },\n      });\n","        error: { code: 'BAD_REQUEST', message: `Request body exceeds the structural limit (${breach}).` },\n      });\n      next();\n")]),
 'M16_warn_keeps_query': (RL,[rep("const path = String(req.originalUrl || req.url || '').split('?')[0];","const path = String(req.originalUrl || req.url || '');")]),
 'M17_warn_carries_body': (RL,[rep("{ service, kind: breach, path });","{ service, kind: breach, path, body: req.body });")]),
 'M18_caps_read_per_request': (RL,[rep("  const caps = readStructuralCaps(log);\n  const parse","  const parse"),rep("      const breach = req.body === undefined ? null : findStructuralBreach(req.body, caps);","      const caps = readStructuralCaps(log);\n      const breach = req.body === undefined ? null : findStructuralBreach(req.body, caps);")]),
 'M19_env_zero_accepted': (RL,[rep("Number.isSafeInteger(n) && n > 0","Number.isSafeInteger(n) && n >= 0")]),
 'M20_env_warn_names_value': (RL,[rep("{ variable: name });","{ variable: name, value: raw });")]),
 'M21_status_413': (RL,[rep("res.status(400).json({\n        success: false,","res.status(413).json({\n        success: false,")]),
 'M22_parse_error_swallowed_to_next': (RL,[rep("      if (err) {\n        next(err);\n        return;\n      }\n","      if (err) {\n        next();\n        return;\n      }\n")]),
 'M23_verify_dropped': (RL,[rep("  const parse = express.json(jsonOptions);","  const { verify: _v, ...noVerify } = jsonOptions as any;\n  const parse = express.json(noVerify);")]),
 'M24_limit_dropped': (RL,[rep("  const parse = express.json(jsonOptions);","  const { limit: _l, ...noLimit } = jsonOptions as any;\n  const parse = express.json(noLimit);")]),
 'M25_vc_issuer_swap_reverted': (VC,[rep("app.use(boundedJson({ service: 'vc-issuer', limit: '10mb' }));","app.use(express.json({ limit: '10mb' }));")]),
 'M26_vc_issuer_named_import_json': (VC,[rep("import express, { Request, Response } from 'express';","import express, { Request, Response, json } from 'express';"),rep("app.use(boundedJson({ service: 'vc-issuer', limit: '10mb' }));","app.use(json({ limit: '10mb' }));")]),
 'M27_vc_issuer_require_express_json': (VC,[rep("app.use(boundedJson({ service: 'vc-issuer', limit: '10mb' }));","app.use(require('express').json({ limit: '10mb' }));")]),
 'M28_vc_issuer_bodyparser_named': (VC,[rep("import express, { Request, Response } from 'express';","import express, { Request, Response } from 'express';\nimport { json as bpJson } from 'body-parser';"),rep("app.use(boundedJson({ service: 'vc-issuer', limit: '10mb' }));","app.use(bpJson({ limit: '10mb' }));")]),
}
only=sys.argv[1:] or list(M)
for name in only:
    path,fs=M[name]; orig=open(path).read(); h0=sha(path); s=orig
    for f in fs: s=f(s)
    assert s!=orig
    open(path,'w').write(s)
    log=f'{G}/logs/mut_{name}.log'
    r=subprocess.run(['bash',G+'/scripts/vt.sh','mut','packages/shared',log,'ks1724-bounded-json'],capture_output=True,text=True)
    open(path,'w').write(orig); ok=sha(path)==h0
    t=open(log).read()
    summ=(re.findall(r'Tests\s+(.*)',t) or ['?'])[-1].strip()
    failed=[l.strip()[2:].split(' ')[0:12] for l in t.splitlines() if l.strip().startswith('×')]
    kinds=sorted(set(re.findall(r'^(AssertionError|TypeError|Error|SyntaxError)\b',t,flags=re.M)))
    st='KILLED' if r.returncode!=0 else 'SURVIVED'
    print(name,st,'|',summ,'| kinds',kinds,'| restore',ok,'|',[' '.join(x) for x in failed][:4],flush=True)
