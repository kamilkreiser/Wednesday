#!/usr/bin/env python3
"""drafter_static.py — #1009: service tsc -p . and an INCLUDING program (extends ./tsconfig.json, include src/**/*, exclude node_modules+dist;
placed for the run, moved out by rename) on base / head / merged, inclusion proven by --listFilesOnly, raw error lines total + in the ks864 files,
NEW/GONE diff by full diagnostic line; planted positive control in ks864c (head); parser proof of P-1007-1; eslint on the three head files."""
import sys, os, json, re, subprocess
sys.path.insert(0, '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1009')
from drafterlib import *
GWR = 'Blockchain/Dev/services/api-gateway'; KC = GWR + '/src/__tests__/ks864c-portal-env-vars.test.ts'
INC = '{"extends": "./tsconfig.json", "include": ["src/**/*"], "exclude": ["node_modules", "dist"]}\n'
def q(): n = len(os.listdir(W + '/_quarantine')); return n
def tsc(tree, cfg, extra=()):
    p = subprocess.run([T[tree] + '/Blockchain/Dev/node_modules/.bin/tsc', '--noEmit', '-p', cfg, *extra], cwd=T[tree] + '/' + GWR, capture_output=True, text=True); return p.returncode, p.stdout + p.stderr
def including(tree, extra=()):
    cfg = T[tree] + '/' + GWR + '/tsconfig.qa-including.json'; open(cfg, 'w').write(INC)
    r = tsc(tree, 'tsconfig.qa-including.json', extra); os.rename(cfg, W + '/_quarantine/tsconfig.qa-including.static.%s.%d.json' % (tree, q())); return r
P('drafter_static start', ts())
E = {}
for t in ('base', 'head', 'merged'):
    rc, o = tsc(t, '.'); P('tsc -p . tree', t, 'rc', rc, 'error lines', o.count('error TS'))
    rc, o = including(t, ['--listFilesOnly']); tl = [l for l in o.splitlines() if '/__tests__/' in l and '/node_modules/' not in l]
    P('   including program __tests__ files', len(tl), '| ks864a/b/c listed', [any(x in l for l in tl) for x in ('ks864a', 'ks864b', 'ks864c')])
    rc, o = including(t); lines = [l for l in o.splitlines() if 'error TS' in l]; E[t] = lines
    P('   including rc', rc, 'raw error lines', len(lines), '| in ks864 files', len([l for l in lines if 'ks864' in l]), '| distinct by code+file', len({re.sub(r'\(\d+,\d+\)', '', l) for l in lines}))
    for l in lines:
        if 'ks864' in l: P('      ', l[:170])
    open(GS + '/tsc_including_%s.out' % t, 'w').write(o)
for a, b in (('base', 'head'), ('head', 'merged')):
    new = [l for l in E[b] if l not in E[a]]; gone = [l for l in E[a] if l not in E[b]]
    P('%s -> %s: NEW %d, GONE %d' % (a, b, len(new), len(gone))); [P('   +', l[:170]) for l in new]; [P('   -', l[:170]) for l in gone]
P('error codes per tree:', {t: dict(sorted({c: sum(1 for l in E[t] if c in l) for c in set(re.findall(r'error (TS\d+)', '\n'.join(E[t])))}.items())) for t in E})
P('== positive control: plant `const qaPlanted: number = \'qa\';` in ks864c at head; the including program must report TS2322 + TS6133 on ks864c')
pk = sha(T['head'] + '/' + KC)
edit(T['head'] + '/' + KC, "const savedEnv = { ...process.env };\n", "const savedEnv = { ...process.env };\nconst qaPlanted: number = 'qa';\n", [('qaPlanted', 1)])
rc, o = including('head'); P('   rc', rc, '| ks864c lines', [l.split('): ')[1][:40] for l in o.splitlines() if 'ks864c' in l])
restore('head', KC, pk)
tsbin = T['head'] + '/Blockchain/Dev/node_modules/typescript'
p = subprocess.run(['node', GS + '/parser_proof.cjs', tsbin, GS], capture_output=True, text=True); P('== parser_proof.cjs rc', p.returncode); P(p.stdout.strip(), p.stderr.strip()[:500])
p = subprocess.run([T['head'] + '/Blockchain/Dev/node_modules/.bin/eslint', '-f', 'json', *[T['head'] + '/' + GWR + '/src/__tests__/' + f for f in ('ks864a-dead-estate-helper.test.ts', 'ks864b-dead-estate-portals.test.ts', 'ks864c-portal-env-vars.test.ts')]], cwd=T['head'] + '/Blockchain/Dev', capture_output=True, text=True)
try:
    for f in json.loads(p.stdout): P('eslint head', f['filePath'].split('/src/')[-1], 'errors', f['errorCount'], 'warnings', f['warningCount'])
except Exception: P('eslint NO JSON rc', p.returncode, p.stderr[-400:])
P('porcelain head', [l for l in porcelain('head') if not l.rstrip('/').endswith('node_modules')])
P('drafter_static end', ts())
