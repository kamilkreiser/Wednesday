#!/usr/bin/env python3
"""drafter_originate_omit.py — #1022: does originate's RUNTIME stage (`npm ci --ignore-scripts --omit=dev`, Dockerfile:79) install hono?
The lock marks prisma / @prisma/dev / hono devOptional. Installed OUTSIDE the workspace in the drafter's scratch, head only; control: the same
lock with a full install must have hono too, and a known dev-only package (typescript/jest) must be ABSENT under --omit=dev."""
import json, os, shutil, subprocess, datetime, hashlib
CL = open('/private/tmp/claude-501/drafter1022/CLONE_PATH').read().strip()
src = CL + '/wt-head/Blockchain/Dev/services/originate'
def now(): return datetime.datetime.now().astimezone().strftime('%H:%M:%S %Z')
def ver(d, p):
    f = d + '/node_modules/' + p + '/package.json'
    return json.load(open(f))['version'] if os.path.exists(f) else 'ABSENT'
lock = json.load(open(src + '/package-lock.json'))['packages']
devonly = sorted(k.split('node_modules/')[-1] for k, v in lock.items() if v.get('dev') and k.count('node_modules/') == 1)[:3]
for mode, extra in (('omitdev', ['--omit=dev']),):
    d = CL + '/orig-' + mode; os.makedirs(d)
    for f in ('package.json', 'package-lock.json'): shutil.copyfile(src + '/' + f, d + '/' + f)
    s0 = hashlib.sha256(open(d + '/package-lock.json', 'rb').read()).hexdigest()[:16]
    t0 = now(); p = subprocess.run(['npm', 'ci', '--ignore-scripts', '--no-audit', '--no-fund'] + extra, cwd=d, capture_output=True, text=True)
    open(d + '.log', 'w').write(p.stdout + '\n--stderr--\n' + p.stderr)
    print(mode, 'rc', p.returncode, t0, '->', now(), '| lock sha', s0, '->', hashlib.sha256(open(d + '/package-lock.json', 'rb').read()).hexdigest()[:16], '|', (p.stdout.strip().splitlines() or ['?'])[-1])
    for pkg in ['hono', '@hono/node-server', '@prisma/dev', 'prisma', '@prisma/client', 'express'] + devonly: print('   ', pkg, ver(d, pkg), '(lock flags %s)' % {f: lock.get('node_modules/' + pkg, {}).get(f) for f in ('dev', 'devOptional', 'optional', 'peer') if f in lock.get('node_modules/' + pkg, {})})
