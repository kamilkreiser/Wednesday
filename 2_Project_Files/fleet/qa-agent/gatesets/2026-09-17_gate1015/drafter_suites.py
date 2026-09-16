#!/usr/bin/env python3
"""drafter_suites.py — #1015 (KS-1018): auth whole suite base/head, project tsc per tree, red-before-green (head ks1018 test copied into the
base tree, then quarantined by rename), including tsc base/head + a planted control. Scratch clone only."""
import sys, os, shutil, subprocess, json
sys.path.insert(0, '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1015')
from drafterlib import *
P('drafter_suites start', ts())
TF = 'src/__tests__/ks1018-security-correctness-three-verification-store-reads.test.ts'
vitest('auth_base', 'base', 'auth')
vitest('auth_head', 'head', 'auth')
for t in ('base', 'head'):
    rc, out = tsc_project(t); P('project tsc auth tree', t, 'rc', rc, out.strip()[-300:])
src = T['head'] + '/Blockchain/Dev/services/auth/' + TF
dst = T['base'] + '/Blockchain/Dev/services/auth/' + TF
shutil.copyfile(src, dst)
vitest('rbg_base_ks1018', 'base', 'auth', files=[TF])
os.rename(dst, os.path.dirname(T['base']) + '/QUARANTINE_rbg_ks1018.test.ts.txt')
CFG = '{ "extends": "./tsconfig.json", "compilerOptions": { "noEmit": true }, "include": ["src/**/*.ts"], "exclude": [] }\n'
P('including tsconfig verbatim:', CFG.strip())
for t in ('base', 'head', 'head_planted'):
    tree = 'head' if t.startswith('head') else 'base'
    au = T[tree] + '/Blockchain/Dev/services/auth'
    open(au + '/tsconfig.qa-including.json', 'w').write(CFG)
    plant = au + '/src/qaPlant1015.ts'
    if t == 'head_planted': open(plant, 'w').write('export const qaPlant1015: number = "not a number";\n')
    tscb = T[tree] + '/Blockchain/Dev/node_modules/.bin/tsc'
    lf = subprocess.run([tscb, '-p', 'tsconfig.qa-including.json', '--listFilesOnly'], cwd=au, capture_output=True, text=True).stdout.splitlines()
    p = subprocess.run([tscb, '-p', 'tsconfig.qa-including.json'], cwd=au, capture_output=True, text=True)
    errs = [l for l in (p.stdout + p.stderr).splitlines() if 'error TS' in l]
    open(GS + '/tsc_including_%s.out' % t, 'w').write(p.stdout + p.stderr)
    P('including tsc', t, 'rc', p.returncode, 'error lines', len(errs), '| listed __tests__', sum(1 for l in lf if '/src/__tests__/' in l), 'ks1018 listed', sum(1 for l in lf if 'ks1018-security' in l), '| users.ts errs', sum(1 for l in errs if 'routes/users.ts' in l), 'ks1018 errs', sum(1 for l in errs if 'ks1018' in l), 'plant errs', sum(1 for l in errs if 'qaPlant1015' in l))
    os.rename(au + '/tsconfig.qa-including.json', os.path.dirname(T[tree]) + '/QUARANTINE_tsconfig.qa-including.%s.json.txt' % t)
    if t == 'head_planted': os.rename(plant, os.path.dirname(T[tree]) + '/QUARANTINE_qaPlant1015.ts.txt')
import re
def norm(path):
    return sorted(re.sub(r'\(\d+,\d+\)', '', l.split('/src/')[-1]) for l in open(path).read().splitlines() if 'error TS' in l)
b, h = norm(GS + '/tsc_including_base.out'), norm(GS + '/tsc_including_head.out')
from collections import Counter
new = Counter(h) - Counter(b); gone = Counter(b) - Counter(h)
P('including tsc NEW (line-number-free multiset) head-minus-base', sum(new.values()), list(new)[:10], '| base-minus-head', sum(gone.values()))
P('porcelain base', porcelain('base'), 'head', porcelain('head'))
P('drafter_suites end', ts())
