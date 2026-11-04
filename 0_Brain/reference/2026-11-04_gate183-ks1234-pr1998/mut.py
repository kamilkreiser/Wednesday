#!/usr/bin/env python3
"""Gate 183 mutant runner. Each mutant: anchor must occur exactly once, mutated file PARSED (typescript transpile diagnostics)
before the run, vitest run anchored with --root, file restored via git checkout and sha256 compared to the pre-mutation hash."""
import hashlib, json, os, re, subprocess, sys
W = '/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-04_gate183-ks1234-pr1998'
D = W + '/repo/Blockchain/Dev'
GW = D + '/services/api-gateway'
VER = 'Blockchain/Dev/services/api-gateway/src/routes/versioning.ts'
IDX = 'Blockchain/Dev/services/api-gateway/src/index.ts'
MUT = [
 ('M1 307->302', VER, "return res.redirect(307,", "return res.redirect(302,"),
 ('M2 query dropped', VER, "return res.redirect(307, `${versionedPath}${qs}`);", "return res.redirect(307, `${versionedPath}`);"),
 ('M3 production check removed', VER, "process.env.NODE_ENV === 'production' &&\n      folded", "folded"),
 ('M3b production check forced false (redirect never fires)', VER, "process.env.NODE_ENV === 'production' &&\n      folded", "false &&\n      folded"),
 ('M4 Location /api/v2/', VER, "`/api/${CURRENT_API_VERSION}/`);", "`/api/v2/`);"),
 ('M5 rewrite switched off', IDX, "if (foldAsciiCase(req.path).startsWith('/api/v1/')) req.url = req.url.replace(/\\/api\\/v1\\//i, '/api/');", "/* off */"),
 ('M6 original KS-1234 parser order', IDX, ".replace(/^\\/api\\/v1\\//, '/api/').startsWith(foldAsciiCase(p))", ".startsWith(foldAsciiCase(p))"),
]
env = {'PATH': os.environ['PATH'], 'HOME': W + '/home', 'TMPDIR': W + '/tmp'}
def sha(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]
def run(cmd): return subprocess.run(cmd, capture_output=True, text=True, env=env)
def vitest(extra_env=None):
    e = dict(env); e.update(extra_env or {})
    r = subprocess.run([D + '/node_modules/.bin/vitest', 'run', '--root', GW, 'src/__tests__/ks1234-production-mode-307.test.ts'], capture_output=True, text=True, env=e)
    out = re.sub(r'\x1b\[[0-9;]*m', '', r.stdout + r.stderr)
    m = re.search(r'Tests\s+(.*)', out)
    fails = re.findall(r'(?:FAIL|×)\s+.*?>\s+(hop \d|the redirect)', out)
    return r.returncode, (m.group(1).strip() if m else 'NO SUMMARY'), sorted(set(fails)), out
rows = []
only = sys.argv[1:]
for name, rel, a, b in MUT:
    if only and name.split()[0] not in only: continue
    p = W + '/repo/' + rel
    h0 = sha(p); src = open(p).read()
    n = src.count(a)
    if n != 1:
        rows.append((name, 'ANCHOR COUNT %d' % n)); continue
    open(p, 'w').write(src.replace(a, b))
    parse = subprocess.run(['node', '-e', "const ts=require(process.argv[1]);const s=require('fs').readFileSync(process.argv[2],'utf8');const r=ts.transpileModule(s,{reportDiagnostics:true,fileName:'x.ts'});console.log(r.diagnostics.length)", D + '/node_modules/typescript', p], capture_output=True, text=True, env=env).stdout.strip()
    rc, summ, fails, out = vitest() if parse == '0' else (-1, 'NOT RUN: parse diagnostics ' + parse, [], '')
    open(W + '/scratch/mut_%s.out' % name.split()[0], 'w').write(out)
    subprocess.run(['git', '-C', W + '/repo', 'checkout', '--', rel], env=env)
    h1 = sha(p)
    rows.append((name, 'parse_diag=%s rc=%s %s failed-cells=%s restored_sha_equal=%s (%s)' % (parse, rc, summ, fails, h0 == h1, h1)))
    print(rows[-1], flush=True)
# T1 contrast: NODE_ENV=test boot reading 0/3 -- the test stubs NODE_ENV itself, so T1 is a copy of the file with the NODE_ENV stub changed
t = W + '/repo/Blockchain/Dev/services/api-gateway/src/__tests__/ks1234-production-mode-307.test.ts'
if not only or 'T1' in only:
    src = open(t).read(); a = "vi.stubEnv('NODE_ENV', 'production');"
    cp = t.replace('ks1234-production-mode-307', 'zz-gate183-t1-copy')
    assert src.count(a) == 1
    open(cp, 'w').write(src.replace(a, "vi.stubEnv('NODE_ENV', 'test');"))
    r = subprocess.run([D + '/node_modules/.bin/vitest', 'run', '--root', GW, 'src/__tests__/zz-gate183-t1-copy.test.ts'], capture_output=True, text=True, env=env)
    out = re.sub(r'\x1b\[[0-9;]*m', '', r.stdout + r.stderr); open(W + '/scratch/mut_T1.out', 'w').write(out)
    m = re.search(r'Tests\s+(.*)', out)
    os.remove(cp)
    print(('T1 NODE_ENV=test copy', 'rc=%s %s' % (r.returncode, m.group(1).strip() if m else 'NO SUMMARY')), flush=True)
st = subprocess.run(['git', '-C', W + '/repo', 'status', '--porcelain'], capture_output=True, text=True).stdout
print('clone status after:', repr(st))
