#!/usr/bin/env python3
"""drafter_suites.py — #1013: auth whole suite base/head, shared at head, red-before-green (head ks999 test copied into the base tree, then quarantined by rename), including tsc base/head + plant."""
import sys, os, shutil, subprocess, json
sys.path.insert(0, '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1013')
from drafterlib import *
P('drafter_suites start', ts())
vitest('auth_base', 'base', 'auth')
for t in ('base', 'head'):
    rc, out = tsc_project(t); P('project tsc auth tree', t, 'rc', rc, out.strip()[-300:])
src = T['head'] + '/Blockchain/Dev/services/auth/src/__tests__/ks999-getuserbyid-awaits-fromrow.test.ts'
dst = T['base'] + '/Blockchain/Dev/services/auth/src/__tests__/ks999-getuserbyid-awaits-fromrow.test.ts'
shutil.copyfile(src, dst)
vitest('rbg_base_ks999', 'base', 'auth', files=['src/__tests__/ks999-getuserbyid-awaits-fromrow.test.ts'])
os.rename(dst, os.path.dirname(T['base']) + '/QUARANTINE_rbg_ks999.test.ts.txt')
vitest('ks949_base', 'base', 'auth', files=['src/__tests__/ks949-platform-admin-seed-identity.test.ts'])
CFG = '{ "extends": "./tsconfig.json", "compilerOptions": { "noEmit": true }, "include": ["src/**/*.ts"], "exclude": [] }\n'
for t in ('base', 'head', 'head_planted'):
    tree = 'head' if t.startswith('head') else 'base'
    au = T[tree] + '/Blockchain/Dev/services/auth'
    open(au + '/tsconfig.qa-including.json', 'w').write(CFG)
    plant = au + '/src/qaPlant1013.ts'
    if t == 'head_planted': open(plant, 'w').write('const QA_UNUSED_PLANT = 1;\nfunction qaPlant(x: number) { return 1; }\nexport {};\n')
    tscb = T[tree] + '/Blockchain/Dev/node_modules/.bin/tsc'
    lf = subprocess.run([tscb, '-p', 'tsconfig.qa-including.json', '--listFilesOnly'], cwd=au, capture_output=True, text=True).stdout.splitlines()
    p = subprocess.run([tscb, '-p', 'tsconfig.qa-including.json'], cwd=au, capture_output=True, text=True)
    errs = [l for l in (p.stdout + p.stderr).splitlines() if 'error TS' in l]
    open(GS + '/tsc_including_%s.out' % t, 'w').write(p.stdout + p.stderr)
    P('including tsc', t, 'rc', p.returncode, 'error lines', len(errs), '| listed __tests__', sum(1 for l in lf if '/src/__tests__/' in l), 'ks999 listed', sum(1 for l in lf if 'ks999-getuserbyid' in l), 'ks949 listed', sum(1 for l in lf if 'ks949-platform' in l), '| userRepo.ts errs', sum(1 for l in errs if 'userRepo.ts' in l), 'ks999 errs', sum(1 for l in errs if 'ks999' in l), 'ks949 errs', sum(1 for l in errs if 'ks949' in l), 'TS2741', sum(1 for l in errs if 'TS2741' in l), 'plant errs', sum(1 for l in errs if 'qaPlant1013' in l))
    os.rename(au + '/tsconfig.qa-including.json', os.path.dirname(T[tree]) + '/QUARANTINE_tsconfig.qa-including.%s.json.txt' % t)
    if t == 'head_planted': os.rename(plant, os.path.dirname(T[tree]) + '/QUARANTINE_qaPlant1013.ts.txt')
P('porcelain base', porcelain('base'), 'head', porcelain('head'))
P('drafter_suites end', ts())
