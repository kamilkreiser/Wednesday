#!/usr/bin/env python3
"""drafter_frontends_1030.py — #1030 RUNTIME REACH (a): does the PR move any SHIPPED frontend dist/? Enumerated from the repo: every
Blockchain/Dev/frontend/*/Dockerfile that COPYs /app/dist from a node builder (admin, demo-overlay, issuer, outlook-addin, verifier, website;
status ships a static index.html, gmail-addon has no Dockerfile). Builder stage reproduced with HOST npm (node 24 / npm 11, NOT the image's
node:24-alpine; no docker) OUTSIDE Blockchain/Dev in the drafter scratch: app/ = frontend/<x> minus node_modules/dist; app/vendor/shared =
frontend/shared where the Dockerfile copies it (SHARED_DIR=./vendor/shared/src); `npm ci --no-audit` WITH install scripts (as the image);
outlook-addin also the manifest.xml sed; `npm run build`. Trees: merge-base 20ab16f9a (= develop's audit inputs; current develop 75ad0e55c
differs only in services/auth) vs head e43af4934. CONTROL (determinism): issuer head built twice. Every dist/ compared by per-file sha256.
Input identity per frontend (git diff base..head over frontend/<x>, frontend/shared, packages/shared) printed first."""
import concurrent.futures, datetime, hashlib, json, os, re, shutil, subprocess, sys
G = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1030'
P = json.load(open(G + '/drafter_paths.json')); SCR = P['SCR']; C = P['C']
def now(): return datetime.datetime.now().astimezone().strftime('%H:%M:%S %Z')
def load(): return '%.1f/%.1f/%.1f' % os.getloadavg()
def tree_hash(d):
    out = {}
    for root, dirs, files in os.walk(d):
        for f in files:
            p = os.path.join(root, f); out[os.path.relpath(p, d)] = hashlib.sha256(open(p, 'rb').read()).hexdigest()
    return out
FE = ['admin', 'demo-overlay', 'issuer', 'outlook-addin', 'verifier', 'website']
VENDOR = {'admin', 'issuer', 'verifier'}
print('drafter_frontends_1030 start', now(), 'load', load(), 'node', subprocess.run(['node', '-v'], capture_output=True, text=True).stdout.strip(), 'npm', subprocess.run(['npm', '-v'], capture_output=True, text=True).stdout.strip())
for fe in FE:
    d = subprocess.run(['git', '-C', C, 'diff', '--name-only', P['BASE'], P['HEAD'], '--', 'Blockchain/Dev/frontend/' + fe, 'Blockchain/Dev/frontend/shared', 'Blockchain/Dev/packages/shared'], capture_output=True, text=True).stdout.split()
    tmp = subprocess.run(['git', '-C', C, 'grep', '-c', '/tmp/shared', P['HEAD'], '--', 'Blockchain/Dev/frontend/' + fe], capture_output=True, text=True).stdout.split()
    print('INPUTS %-14s base..head changed files %s | "/tmp/shared" references at head %s' % (fe, d, tmp))
FEFB = os.path.join(SCR, 'fe'); os.makedirs(FEFB)
def build(fe, tag, tree):
    src = SCR + '/wt_' + tree + '/Blockchain/Dev'
    x = os.path.join(FEFB, fe + '-' + tag); app = x + '/app'
    shutil.copytree(src + '/frontend/' + fe, app, ignore=shutil.ignore_patterns('node_modules', 'dist'))
    env = dict(os.environ)
    if fe in VENDOR:
        shutil.copytree(src + '/frontend/shared', app + '/vendor/shared', ignore=shutil.ignore_patterns('node_modules', 'dist'))
        env['SHARED_DIR'] = './vendor/shared/src'
    lk = hashlib.sha256(open(app + '/package-lock.json', 'rb').read()).hexdigest()[:16]
    t0, l0 = now(), load()
    p = subprocess.run(['npm', 'ci', '--no-audit', '--no-fund'], cwd=app, capture_output=True, text=True, env=env)
    if p.returncode != 0 and fe == 'outlook-addin':
        p = subprocess.run(['npm', 'ci', '--no-audit', '--no-fund'], cwd=app, capture_output=True, text=True, env=env)
    open(x + '/ci.log', 'w').write(p.stdout + '\n--stderr--\n' + p.stderr)
    ci_rc = p.returncode
    vv = {}
    for n in ('vite', 'vitest', 'rolldown', 'lightningcss', 'tinyrainbow'):
        pj = app + '/node_modules/' + n + '/package.json'
        vv[n] = json.load(open(pj))['version'] if os.path.exists(pj) else '-'
    if fe == 'outlook-addin':
        m = open(app + '/manifest.xml').read(); open(app + '/manifest.xml', 'w').write(m.replace('{{ADDIN_BASE_URL}}', 'https://localhost:6104'))
    t1, l1 = now(), load()
    p = subprocess.run(['npm', 'run', 'build'], cwd=app, capture_output=True, text=True, env=env)
    open(x + '/build.log', 'w').write(p.stdout + '\n--stderr--\n' + p.stderr)
    h = tree_hash(app + '/dist') if os.path.isdir(app + '/dist') else {}
    size = sum(os.path.getsize(os.path.join(r, f)) for r, _, fs in os.walk(app + '/dist') for f in fs) if h else 0
    lk2 = hashlib.sha256(open(app + '/package-lock.json', 'rb').read()).hexdigest()[:16]
    return (fe, tag, h, 'ci rc %d [%s load %s] build rc %d [%s load %s -> %s load %s] | installed %s | dist files %d bytes %d | lock sha %s->%s' % (
        ci_rc, t0, l0, p.returncode, t1, l1, now(), load(), vv, len(h), size, lk, lk2))
jobs = [('issuer', 'base', 'base'), ('issuer', 'head', 'head'), ('issuer', 'head2', 'head')] + [(fe, t, t) for fe in FE if fe != 'issuer' for t in ('base', 'head')]
res = {}
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:
    for fut in concurrent.futures.as_completed([ex.submit(build, *j) for j in jobs]):
        fe, tag, h, line = fut.result(); res[(fe, tag)] = h
        print('BUILD %-14s %-5s %s' % (fe, tag, line), flush=True)
def cmp(a, b): return sorted(k for k in set(res[a]) | set(res[b]) if res[a].get(k) != res[b].get(k))
print('CONTROL issuer head vs head2 differing files:', cmp(('issuer', 'head'), ('issuer', 'head2')))
for fe in FE:
    print('DIST %-14s base vs head differing files: %s (files %d/%d; empty dist would be a VOID comparison)' % (fe, cmp((fe, 'base'), (fe, 'head')), len(res[(fe, 'base')]), len(res[(fe, 'head')])))
print('done', now(), 'load', load())
