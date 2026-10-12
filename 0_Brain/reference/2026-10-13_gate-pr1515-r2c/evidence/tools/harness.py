import json, os, subprocess, sys, shutil, re
S = '/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/f2077cbf-bb12-49ee-8d59-f5f537b335e0/scratchpad/g3'
TSC = S + '/head/Blockchain/Dev/node_modules/typescript/bin/tsc'
CHECKERS = {'prev': S + '/prev/Blockchain/Dev/scripts/typecheck-tests/check.cjs', 'dev': S + '/dev/Blockchain/Dev/scripts/typecheck-tests/check.cjs',
            'head': S + '/head/Blockchain/Dev/scripts/typecheck-tests/check.cjs'}
CLEAN = 'export const fine: number = 1;\n'
ZERO = 'examined-test-files 0\n'
P = 'node_modules/@secuura/shared/'
def tsconfig(extra=None, include=None, exclude=None):
    co = {'strict': True, 'noEmit': True, 'target': 'ES2022', 'module': 'commonjs', 'skipLibCheck': True, 'types': []}
    co.update(extra or {})
    d = {'compilerOptions': co, 'include': include or ['src/**/*']}
    if exclude: d['exclude'] = exclude
    return json.dumps(d)
def shared_pkg(**over):
    pj = {'name': '@secuura/shared', 'version': '0.0.0', 'main': 'dist/index.js', 'types': 'dist/index.d.ts',
          'exports': {'.': './dist/index.js', './thing': './dist/thing/theThing.js'},
          'typesVersions': {'*': {'thing': ['dist/thing/theThing.d.ts']}}}
    for k, v in over.items():
        if v is None: pj.pop(k, None)
        else: pj[k] = v
    return pj
def base(pj=None, dist=('index.js', 'index.d.ts', 'thing/theThing.js', 'thing/theThing.d.ts'), pkgdir=P, use="import { X } from '@secuura/shared/thing';\nexport const t: number = X;\n"):
    files = {'tsconfig.test.json': tsconfig(), 'src/ok.ts': 'export const ok: number = 1;\n',
             'src/__tests__/a.test.ts': CLEAN, 'baseline.txt': ZERO,
             pkgdir + 'package.json': json.dumps(pj if pj is not None else shared_pkg())}
    for rel in dist:
        files[pkgdir + 'dist/' + rel] = ('export declare const X: number;\n' if rel.endswith('.d.ts') else 'module.exports = { X: 1 };\n')
    if use is not None: files['src/u.ts'] = use
    return files
def use(spec, kind='import'):
    if kind == 'import': return f"import {{ X }} from '{spec}';\nexport const t: number = X;\n"
    if kind == 'type': return f"import type {{ X }} from '{spec}';\nexport type T = X;\n"
    if kind == 'typeof': return f"export type T = typeof import('{spec}');\n"
    if kind == 'root': return f"import * as R from '{spec}';\nexport const r = R;\n"
def build(name, files, symlinks=(), fifo=()):
    d = os.path.join(S, 'shapes', name)
    if os.path.exists(d): shutil.rmtree(d)
    os.makedirs(d)
    for rel, body in files.items():
        p = os.path.join(d, rel); os.makedirs(os.path.dirname(p), exist_ok=True)
        if isinstance(body, bytes): open(p, 'wb').write(body)
        else: open(p, 'w', newline='').write(body)
    for link, target in symlinks:
        p = os.path.join(d, link); os.makedirs(os.path.dirname(p), exist_ok=True); os.symlink(target, p)
    for f in fifo:
        p = os.path.join(d, f); os.makedirs(os.path.dirname(p), exist_ok=True); os.mkfifo(p)
    return d
def run(cmd, cwd=None, timeout=300, env=None):
    try:
        r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout, env=env)
        return r.returncode, r.stdout + r.stderr
    except subprocess.TimeoutExpired:
        return 'TIMEOUT', ''
def measure(name, files, init_with=None, symlinks=(), fifo=(), env=None, timeout=300):
    d = build(name, files, symlinks, fifo)
    trc, tout = run(['node', TSC, '--noEmit', '--pretty', 'false', '-p', 'tsconfig.test.json'], cwd=d, timeout=timeout, env=env)
    codes = sorted(set(re.findall(r'error (TS\d+)', tout)))
    if init_with:
        os.remove(os.path.join(d, 'baseline.txt'))
        irc, iout = run(['node', CHECKERS[init_with], d, '--baseline', os.path.join(d, 'baseline.txt'), '--init'], env=env)
        if irc != 0: print('INIT FAILED', name, irc, iout[:300])
    row = {'shape': name, 'tsc': trc, 'codes': codes}
    for k, c in CHECKERS.items():
        rc, out = run(['node', c, d, '--baseline', os.path.join(d, 'baseline.txt')], timeout=timeout, env=env)
        tags = []
        if 'CANNOT RUN' in out: tags.append('STALE')
        if 'note:' in out: tags.append('note')
        if 'NEW type errors' in out: tags.append('NEW')
        if 'Error:' in out and 'at ' in out and 'node:' in out: tags.append('CRASH?')
        m = re.findall(r'missing declaration target: (\S+)', out)
        row[k] = rc; row[k + '_tags'] = tags + (['->' + ','.join(m)] if m else [])
        open(os.path.join(S, 'out', f'shape_{name}_{k}.txt'), 'w').write(f'rc {rc}\n' + out)
    open(os.path.join(S, 'out', f'shape_{name}_tsc.txt'), 'w').write(f'rc {trc}\n' + tout)
    print(json.dumps(row)); sys.stdout.flush()
    with open(os.path.join(S, 'out', 'shapes.jsonl'), 'a') as f: f.write(json.dumps(row) + '\n')
    return row
