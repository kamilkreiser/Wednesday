#!/usr/bin/env python3
"""drafter_static.py — #1006: tsc -p (each package's own program; count __tests__ files in it), an INCLUDING program per package
(tsconfig.qa-including.json: extends ./tsconfig.json, include src/**/*.ts; placed for the run, moved out by rename), new-error diff
base (develop 40fe4db69) -> head (86fe59e6b), errors located in the 5 touched files and matched against the head's ADDED line numbers
(from `git diff -U0`); eslint (flat config) on the 5 files. Positive control for both tools: a planted unused const in the ks844 test."""
import sys, os, json, re, subprocess
sys.path.insert(0, '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1006')
from drafterlib import *
D = 'Blockchain/Dev/'
TOUCHED = [D + 'services/demo-service/src/app.ts', D + 'services/demo-service/src/middleware/errorHandler.ts',
           D + 'services/demo-service/src/__tests__/ks844-demo-service-mounts-no-error-handler.test.ts',
           D + 'packages/shared/src/__tests__/ks727-errorhandler-class-guard.test.ts', D + 'packages/shared/src/__tests__/ks781-p3-3-body-parser-order.test.ts']
KS844 = TOUCHED[2]
INC = '{"extends": "./tsconfig.json", "include": ["src/**/*.ts"], "exclude": ["node_modules", "dist"]}\n'
Q = W + '/_quarantine'; os.makedirs(Q, exist_ok=True)
def tsc(tree, pkg, cfg, extra=()):
    p = subprocess.run([T[tree] + '/Blockchain/Dev/node_modules/.bin/tsc', '--noEmit', '-p', cfg, *extra], cwd=T[tree] + '/' + PKG[pkg], capture_output=True, text=True)
    return p.returncode, p.stdout + p.stderr
added = {}
dp = subprocess.run(['git', '-C', T['head'], 'diff', '-U0', PATHS['sha']['base'], PATHS['sha']['head'], '--', *TOUCHED], capture_output=True, text=True).stdout
cur = None
for l in dp.splitlines():
    if l.startswith('+++ b/'): cur = l[6:]; added[cur] = set()
    m = re.match(r'^@@ -\S+ \+(\d+)(?:,(\d+))? @@', l)
    if m and cur:
        s, n = int(m.group(1)), int(m.group(2) or 1)
        added[cur].update(range(s, s + n))
P('drafter_static start', ts(), '| head added lines per touched file', {k.split('/')[-1]: len(v) for k, v in added.items()})
raw = {}
for pkg in ('demo', 'shared'):
    errs = {}
    for t in ('base', 'head'):
        rc, o = tsc(t, pkg, '.'); P('tsc -p . pkg', pkg, 'tree', t, 'rc', rc, 'error lines', len(re.findall(r'error TS', o)))
        rc, o = tsc(t, pkg, '.', ['--listFilesOnly']); P('   own program __tests__ files', sum(1 for l in o.splitlines() if '/__tests__/' in l and '/node_modules/' not in l))
        cfg = T[t] + '/' + PKG[pkg] + '/tsconfig.qa-including.json'; open(cfg, 'w').write(INC)
        rc, o = tsc(t, pkg, 'tsconfig.qa-including.json', ['--listFilesOnly']); tl = [l for l in o.splitlines() if '/__tests__/' in l and '/node_modules/' not in l]
        P('   including program __tests__ files', len(tl), '| touched test files listed', sum(1 for f in TOUCHED if f.endswith('.test.ts') and any(l.endswith(f) for l in tl)))
        rc, o = tsc(t, pkg, 'tsconfig.qa-including.json'); lines = [l for l in o.splitlines() if 'error TS' in l]
        e = sorted(set(re.sub(r'\(\d+,\d+\)', '(L,C)', l) for l in lines)); errs[t] = (rc, e, lines)
        P('   including program rc', rc, 'error lines', len(lines), 'distinct (line-normalised)', len(e))
        os.rename(cfg, Q + '/tsconfig.qa-including.%s.%s.json' % (pkg, t))
        raw['%s_%s' % (pkg, t)] = o
    new = [x for x in errs['head'][1] if x not in errs['base'][1]]; gone = [x for x in errs['base'][1] if x not in errs['head'][1]]
    P('   NEW errors base -> head (%s):' % pkg, len(new)); [P('     +', x[:220]) for x in new]
    P('   disappeared (%s):' % pkg, len(gone)); [P('     -', x[:220]) for x in gone]
    for f in TOUCHED:
        name = f.split('/')[-1]
        hits = [l for l in errs['head'][2] if ('/' + name + '(') in l or l.startswith(name + '(') or (f.replace(PKG[pkg] + '/', '') + '(') in l]
        if not hits: continue
        on_added = []
        for l in hits:
            m = re.search(r'\((\d+),\d+\)', l)
            if m and int(m.group(1)) in added.get(f, set()): on_added.append(l)
        P('   head errors in touched %s: %d | on lines this PR ADDED: %d' % (name, len(hits), len(on_added)))
        for l in hits: P('      ', ('ADDED-LINE ' if l in on_added else 'unchanged  ') + l[:200])
open(GS + '/tsc_including.out', 'w').write('\n'.join('== %s\n%s' % (k, v) for k, v in raw.items()))
def eslint(tree, files):
    p = subprocess.run([T[tree] + '/Blockchain/Dev/node_modules/.bin/eslint', '-f', 'json', *[T[tree] + '/' + f for f in files]], cwd=T[tree] + '/Blockchain/Dev', capture_output=True, text=True)
    try: j = json.loads(p.stdout)
    except Exception: P('eslint NO JSON rc', p.returncode, p.stderr[-600:]); return
    for f in j: P('eslint', tree, f['filePath'].split('/Dev/')[-1], 'errors', f['errorCount'], 'warnings', f['warningCount'], sorted({str(m.get('ruleId')) for m in f['messages']}))
eslint('head', TOUCHED)
P('== positive control: plant an unused const in the ks844 test (head); the including tsc (--noUnusedLocals) and eslint must both see it')
pn = sha(T['head'] + '/' + KS844)
edit(T['head'] + '/' + KS844, "const ORIGINAL_ENV = { ...process.env };\n", "const ORIGINAL_ENV = { ...process.env };\nconst QA_UNUSED_PLANT = 'a'.repeat(64);\n", [('QA_UNUSED_PLANT', 1)])
cfg = T['head'] + '/' + PKG['demo'] + '/tsconfig.qa-including.json'; open(cfg, 'w').write(INC)
rc, o = tsc('head', 'demo', 'tsconfig.qa-including.json', ['--noUnusedLocals']); P('   including tsc --noUnusedLocals sees plant:', 'QA_UNUSED_PLANT' in o)
os.rename(cfg, Q + '/tsconfig.qa-including.demo.plant.json')
eslint('head', [KS844])
restore('head', KS844, pn)
P('porcelain head', [x for x in porcelain('head') if 'node_modules' not in x], '(node_modules symlinks excluded from this print)')
P('drafter_static end', ts())
