#!/usr/bin/env python3
"""Gate 184 mutant runner. Each mutant: anchor must occur exactly once; mutated file type-checked (tsc --noEmit on the
service); the PR's new test file + auth.test.ts run; file restored with `git checkout HEAD --`; sha256 compared."""
import hashlib, json, os, re, subprocess, sys

W = '/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-04_gate184-ks1244-pr1999'
REPO = f'{W}/repo'
DEV = f'{REPO}/Blockchain/Dev'
SVC = f'{DEV}/services/api-gateway'
IDX = 'Blockchain/Dev/services/api-gateway/src/index.ts'
AUTH = 'Blockchain/Dev/services/api-gateway/src/middleware/auth.ts'
ENV = {'PATH': os.environ['PATH'], 'HOME': f'{W}/home', 'TMPDIR': f'{W}/tmp'}
TESTS = ['src/__tests__/ks1244-a-repeated-x-api-key-is-refused-on-every-route.test.ts', 'src/__tests__/auth.test.ts']

FD = 'app.use(rejectRepeatedApiKey());\n'
MUTANTS = {
  'M1 front door unmounted': [(IDX, FD, 'void rejectRepeatedApiKey;\n')],
  'M2 inner check dropped': [(AUTH, '    if (carriesRepeatedApiKey(req)) {\n      refuseRepeatedApiKey(req, res);\n      return;\n    }\n', '')],
  'M3 line-count clause dropped': [(AUTH, 'if (lines > 1 || commaInLine) return true;', 'void lines; if (commaInLine) return true;')],
  'M4 raw comma clause dropped': [(AUTH, "      if (String(raw[i + 1]).includes(',')) commaInLine = true;\n", '')],
  'M5 req.headers clause dropped': [(AUTH, "  return typeof value !== 'string' || value.includes(',');", '  return false;')],
  'M6 status 401': [(AUTH, "res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'The x-api-key", "res.status(401).json({ success: false, error: { code: 'BAD_REQUEST', message: 'The x-api-key")],
  'M7 value logged': [(AUTH, '    requestId: req.requestId,\n  });\n  res.status(400)', "    requestId: req.requestId,\n    apiKeyValue: req.headers['x-api-key'],\n  });\n  res.status(400)")],
  'M8 front door above versioning': [(IDX, FD + 'app.use(rejectConnectorBearer());\n', 'app.use(rejectConnectorBearer());\n'), (IDX, 'app.use(versioningMiddleware());\n', FD + 'app.use(versioningMiddleware());\n')],
  'M9 front door after spec gate (just above the proxies)': [(IDX, FD + 'app.use(rejectConnectorBearer());\n', 'app.use(rejectConnectorBearer());\n'), (IDX, 'app.use(createProxyRoutes(', FD + 'app.use(createProxyRoutes(')],
  'M10 front door after the connector check': [(IDX, FD + 'app.use(rejectConnectorBearer());\n', 'app.use(rejectConnectorBearer());\n' + FD)],
  'M11 front door fails open on a throw': [(AUTH, '      next(err);\n      return;\n    }\n    if (!repeated)', '      void err; next();\n      return;\n    }\n    if (!repeated)')],
  'M12 refusal body echoes the header': [(AUTH, "message: 'The x-api-key header must be sent once' } });", "message: 'The x-api-key header must be sent once', got: String(req.headers['x-api-key']) } });")],
}

def sha(p):
    return hashlib.sha256(open(f'{REPO}/{p}', 'rb').read()).hexdigest()

def run(cmd, log, cwd=f'{W}/cwd'):
    with open(log, 'w') as f:
        return subprocess.run(cmd, cwd=cwd, env=ENV, stdout=f, stderr=subprocess.STDOUT).returncode

def main():
    only = sys.argv[1:]
    os.makedirs(f'{W}/runs/mut', exist_ok=True)
    clean = {p: sha(p) for p in (IDX, AUTH)}
    rows = []
    for name, edits in MUTANTS.items():
        if only and not any(name.startswith(o + ' ') for o in only):
            continue
        tag = name.split()[0]
        files = {}
        for p, a, b in edits:
            files.setdefault(p, open(f'{REPO}/{p}').read())
        ok = True
        for p, a, b in edits:
            n = files[p].count(a)
            if n != 1:
                ok = False; print(tag, 'ANCHOR COUNT', n, p); break
            files[p] = files[p].replace(a, b)
        if not ok:
            rows.append({'mutant': name, 'result': 'ANCHOR-FAIL'}); continue
        for p, s in files.items():
            open(f'{REPO}/{p}', 'w').write(s)
        tsc = run([f'{DEV}/node_modules/.bin/tsc', '--noEmit', '-p', f'{SVC}/tsconfig.json'], f'{W}/runs/mut/{tag}.tsc.log')
        vt = run([f'{DEV}/node_modules/.bin/vitest', 'run', '--root', SVC, *TESTS], f'{W}/runs/mut/{tag}.vitest.log')
        txt = re.sub(r'\x1b\[[0-9;]*m', '', open(f'{W}/runs/mut/{tag}.vitest.log').read())
        m = re.search(r'Tests\s+(?:(\d+) failed \| )?(\d+) passed \((\d+)\)', txt)
        failed = int(m.group(1) or 0) if m else None
        failing = sorted(set(re.findall(r'FAIL\s+\S+ > .*? > ((?:RED|GREEN|CONTROL)[^\n]{0,40})', txt)))
        subprocess.run(['git', '-C', REPO, 'checkout', 'HEAD', '--', IDX, AUTH], check=True)
        restored = all(sha(p) == clean[p] for p in clean)
        rows.append({'mutant': name, 'tsc_rc': tsc, 'vitest_rc': vt, 'failed': failed, 'total': int(m.group(3)) if m else None,
                     'killed': (vt != 0 and tsc == 0), 'failing_cells': failing, 'restored_sha_ok': restored})
        print(json.dumps(rows[-1]))
        if not restored:
            sys.exit('RESTORE FAILED')
    json.dump(rows, open(f'{W}/runs/mut/table{"_" + "_".join(only) if only else ""}.json', 'w'), indent=1)

main()
