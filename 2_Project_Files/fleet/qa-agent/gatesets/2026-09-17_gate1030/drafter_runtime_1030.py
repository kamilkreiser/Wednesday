#!/usr/bin/env python3
"""drafter_runtime_1030.py — #1030 RUNTIME REACH (b), SAMPLE: each Dockerfile's runtime node_modules step reproduced with HOST npm
(node 24 / npm 11, not node:24-alpine; no docker) OUTSIDE Blockchain/Dev (npm ci inside a member dir installs from the workspace ROOT lock),
at merge-base 20ab16f9a and head e43af4934, then a census of EVERY installed package (relpath, name, version) and a per-file sha256 of the
whole node_modules tree. Sample (the drafter's; the gate does all 22 service Dockerfiles):
 auth        Dockerfile:54  npm ci --ignore-scripts --omit=dev           (declares vite 7.3.6 as a PROD dependency)
 analytics   Dockerfile:51  npm ci --ignore-scripts --omit=dev --legacy-peer-deps (vite 7.3.6 PROD; manifest moved)
 api-gateway Dockerfile:47  npm ci --omit=dev --ignore-scripts
 vc-issuer   Dockerfile:86  npm ci --ignore-scripts --omit=dev           (manifest moved)
 referral    Dockerfile:38,39,61 sed @secuura/shared; npm ci --ignore-scripts; npm prune --omit=dev (manifest moved; prune route)
POSITIVE CONTROL on the same instrument: the FULL install (pre-prune for referral; a separate full npm ci for the others) base vs head must
show vitest 4.1.10/4.1.9 -> 4.1.11 moving. NEGATIVE CONTROL: vitest ABSENT after the runtime step. Lock sha256 asserted unchanged."""
import concurrent.futures, datetime, hashlib, json, os, shutil, subprocess
G = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1030'
P = json.load(open(G + '/drafter_paths.json')); SCR = P['SCR']
def now(): return datetime.datetime.now().astimezone().strftime('%H:%M:%S %Z')
def load(): return '%.1f/%.1f/%.1f' % os.getloadavg()
def sha(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]
def census(d):
    pk, files = {}, {}
    nm = d + '/node_modules'
    for root, dirs, fs in os.walk(nm):
        for f in fs:
            p = os.path.join(root, f); rel = os.path.relpath(p, d)
            if os.path.islink(p): continue
            files[rel] = hashlib.sha256(open(p, 'rb').read()).hexdigest()
            if f == 'package.json':
                par = os.path.basename(os.path.dirname(root)); par2 = os.path.basename(os.path.dirname(os.path.dirname(root)))
                if par == 'node_modules' or (par.startswith('@') and par2 == 'node_modules'):
                    try: j = json.load(open(p)); pk[os.path.relpath(root, d)] = j.get('version')
                    except Exception: pk[os.path.relpath(root, d)] = '?'
    return pk, files
PLANS = {'auth': ('omit', ['--ignore-scripts', '--omit=dev'], False), 'analytics': ('omit', ['--ignore-scripts', '--omit=dev', '--legacy-peer-deps'], False),
         'api-gateway': ('omit', ['--omit=dev', '--ignore-scripts'], False), 'vc-issuer': ('omit', ['--ignore-scripts', '--omit=dev'], False),
         'referral': ('prune', ['--ignore-scripts'], True)}
RT = SCR + '/runtime'; os.makedirs(RT)
print('drafter_runtime_1030 start', now(), 'load', load(), '| runtime dir outside the workspace:', '/Blockchain/Dev' not in RT)
def job(svc, tree):
    mode, flags, sed = PLANS[svc]
    src = SCR + '/wt_' + tree + '/Blockchain/Dev/services/' + svc
    out = {}
    def prep(d):
        os.makedirs(d)
        for f in ('package.json', 'package-lock.json'): shutil.copyfile(src + '/' + f, d + '/' + f)
        if sed:
            t = open(d + '/package.json').read(); open(d + '/package.json', 'w').write(''.join(l for l in t.splitlines(True) if '"@secuura/shared":' not in l))
        return sha(d + '/package-lock.json')
    rt = RT + '/%s-%s/app' % (svc, tree); s0 = prep(rt); log = RT + '/%s-%s.log' % (svc, tree)
    def npm(args, cwd):
        t0, l0 = now(), load(); p = subprocess.run(['npm'] + args + ['--no-audit', '--no-fund'], cwd=cwd, capture_output=True, text=True)
        open(log, 'a').write('$ npm ' + ' '.join(args) + '\n' + p.stdout + '\n--stderr--\n' + p.stderr + '\n')
        return 'rc %d [%s load %s -> %s]' % (p.returncode, t0, l0, now())
    if mode == 'prune':
        out['full_run'] = npm(['ci'] + flags, rt); out['full'] = census(rt)
        out['rt_run'] = npm(['prune', '--omit=dev'], rt); out['rt'] = census(rt)
    else:
        fd = RT + '/%s-%s/full' % (svc, tree); prep(fd)
        out['full_run'] = npm(['ci', '--ignore-scripts'] + (['--legacy-peer-deps'] if '--legacy-peer-deps' in flags else []), fd); out['full'] = census(fd)
        out['rt_run'] = npm(['ci'] + flags, rt); out['rt'] = census(rt)
    out['lock'] = '%s->%s' % (s0, sha(rt + '/package-lock.json'))
    return svc, tree, out
R = {}
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:
    for fut in concurrent.futures.as_completed([ex.submit(job, s, t) for s in PLANS for t in ('base', 'head')]):
        s, t, o = fut.result(); R[(s, t)] = o
        print('RUN %-12s %-4s full %s pkgs %d | runtime %s pkgs %d files %d vitest-in-runtime %s vite-in-runtime %s | lock %s' % (s, t, o['full_run'], len(o['full'][0]), o['rt_run'], len(o['rt'][0]), len(o['rt'][1]),
              sorted(k + '@' + str(v) for k, v in o['rt'][0].items() if k.endswith('/vitest')), sorted(k + '@' + str(v) for k, v in o['rt'][0].items() if k.endswith('/vite')), o['lock']), flush=True)
for s in PLANS:
    b, h = R[(s, 'base')], R[(s, 'head')]
    def pdiff(x, y): return sorted('%s %s->%s' % (k, x.get(k), y.get(k)) for k in set(x) | set(y) if x.get(k) != y.get(k))
    fpos = pdiff(b['full'][0], h['full'][0]); rpk = pdiff(b['rt'][0], h['rt'][0])
    rfiles = sorted(k for k in set(b['rt'][1]) | set(h['rt'][1]) if b['rt'][1].get(k) != h['rt'][1].get(k))
    print('CENSUS %-12s POSITIVE CONTROL full-install package moves %d (vitest among them: %s) | RUNTIME package moves %d %s | RUNTIME differing files %d %s' % (
        s, len(fpos), [x for x in fpos if x.startswith('node_modules/vitest ')], len(rpk), rpk[:5], len(rfiles), rfiles[:5]))
print('done', now(), 'load', load())
