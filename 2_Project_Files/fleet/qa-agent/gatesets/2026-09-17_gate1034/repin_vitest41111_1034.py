#!/usr/bin/env python3
"""repin_vitest41111_1034.py — side install of develop 3961c2add's vitest 4.1.11 (RE-PIN; DEVSHA read from repin_paths.json) for the api-gateway runs, OUTSIDE Blockchain/Dev (WORKDIR/vitest41111).
The checkout install is vitest 4.1.10 (0a2b1603f's lock). Develop 27e53ec3a's Dev ROOT lock differs from 0a2b1603f's in exactly 8 hoisted entries used here
(vitest + @vitest/{expect,mocker,pretty-format,runner,snapshot,spy,utils}: 4.1.10 -> 4.1.11; the other 15 differences are other services' @vitest/coverage-v8).
Pins: the transitive dependency closure of node_modules/vitest in 27e53ec3a's lock, each at its LOCK version (exact), `npm install --ignore-scripts`.
Asserts after: every closure package installed at its lock version (instrument), vitest reports 4.1.11. Never rm; stderr kept."""
import json, os, subprocess, sys, datetime
PA = json.load(open(os.path.dirname(os.path.abspath(__file__)) + '/repin_paths.json')); W = PA['W']; C = PA['C']; DEVSHA = PA['sha']['dev']
def now(): return datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z')
lock = json.loads(subprocess.run(['git', '-C', C, 'show', DEVSHA + ':Blockchain/Dev/package-lock.json'], capture_output=True, text=True).stdout)['packages']
def resolve(name, frm):
    base = frm
    while True:
        k = (base + '/' if base else '') + 'node_modules/' + name
        if k in lock: return k
        if not base: return None
        i = base.rfind('/node_modules/'); base = base[:i] if i >= 0 else ''
seen = {}; stack = ['node_modules/vitest']
while stack:
    k = stack.pop()
    if k in seen: continue
    e = lock[k]; seen[k] = e['version']
    for dep in list((e.get('dependencies') or {}).keys()):  # optionalDependencies (platform binaries) left to npm: run 1 pinned aix/win32 and failed EBADPLATFORM
        r = resolve(dep, k)
        if r: stack.append(r)
nested = sorted(k for k in seen if k.count('node_modules/') > 1)
top = {k[len('node_modules/'):]: v for k, v in seen.items() if k.count('node_modules/') == 1}
print('repin_vitest41111_1034', now(), '| closure entries', len(seen), '| hoisted', len(top), '| nested (left to npm)', len(nested), nested[:10])
S = W + '/vitest41111'; os.makedirs(S)
json.dump({'name': 'qa1034r-vitest-41111-side', 'private': True, 'dependencies': dict(sorted(top.items()))}, open(S + '/package.json', 'w'), indent=1)
t0 = now(); p = subprocess.run(['npm', 'install', '--ignore-scripts', '--no-audit', '--no-fund', '--no-package-lock'], cwd=S, capture_output=True, text=True)
open(S + '/npm_install.log', 'w').write(p.stdout + '\n--stderr--\n' + p.stderr)
print('npm install rc', p.returncode, t0, '->', now(), '| stderr tail', p.stderr[-600:])
bad = []
for name, v in top.items():
    pj = S + '/node_modules/' + name + '/package.json'
    got = json.load(open(pj))['version'] if os.path.exists(pj) else 'ABSENT'
    if got != v: bad.append((name, v, got))
PLAT = {n for n in top if n.startswith('@esbuild/') or n.startswith('@rollup/rollup-') or n == 'fsevents'}
print('closure hoisted packages at their lock version:', len(top) - len(bad), '/', len(top), '| mismatches', bad[:20])
print('vitest --version:', subprocess.run([S + '/node_modules/.bin/vitest', '--version'], capture_output=True, text=True, cwd=S).stdout.strip())
json.dump({'S': S, 'top': top, 'mismatch': bad}, open(W + '/vitest41111.json', 'w'), indent=1)
