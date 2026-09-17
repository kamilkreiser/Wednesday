#!/usr/bin/env python3
"""drafter_runtime.py — #1027 RUNTIME REACH. Reproduces each touched service's RUNTIME node_modules stage with HOST npm (node 24 / npm 11,
not the image's node:24-alpine; no docker) in the drafter's scratch, OUTSIDE Blockchain/Dev (npm ci inside a member dir installs from the
workspace ROOT lock — the #1022 drafter's trap). Head d7fc6cc55 only (the js-yaml/bbm flags are byte-identical develop vs head by parse).
 governance : Dockerfile:26-54  COPY package*.json; npm ci --ignore-scripts; [build]; npm prune --omit=dev; runner COPYs node_modules
 originate  : Dockerfile:64,79  runner COPY package.json+lock; npm ci --ignore-scripts --omit=dev
 referral   : Dockerfile:33-61  COPY package*.json; sed -i '/"@secuura\\/shared":/d' package.json; npm ci --ignore-scripts; npm prune --omit=dev
 vc-issuer  : Dockerfile:85-86  COPY package*.json; npm ci --ignore-scripts --omit=dev
 shared     : every service image COPYs /shared (full `npm ci --ignore-scripts`, never pruned) — census it too.
Census = every node_modules/**/js-yaml and baseline-browser-mapping dir with its version. POSITIVE CONTROL: the full install of each service
(pre-prune for governance/referral, a separate full npm ci for originate/vc-issuer) must contain js-yaml; NEGATIVE CONTROL: a dev-flagged
package (jest or vitest) must be ABSENT after the runtime step. Lock sha256 asserted unchanged."""
import datetime, hashlib, json, os, re, shutil, subprocess
SCR = open('/private/tmp/claude-501/drafter1027.CLONE_PATH').read().strip()
WT = SCR + '/wt-head/Blockchain/Dev'
def now(): return datetime.datetime.now().astimezone().strftime('%H:%M:%S %Z')
def sha(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]
def sh(args, cwd, log):
    p = subprocess.run(args, cwd=cwd, capture_output=True, text=True)
    open(log, 'a').write('$ ' + ' '.join(args) + '\n' + p.stdout + '\n--stderr--\n' + p.stderr + '\n')
    return p
def census(d):
    out = {}
    for root, dirs, files in os.walk(d + '/node_modules'):
        base = os.path.basename(root)
        if base in ('js-yaml', 'baseline-browser-mapping', 'jest', 'vitest', 'typescript') and 'package.json' in files:
            try: v = json.load(open(root + '/package.json')).get('version')
            except Exception: v = '?'
            out.setdefault(base, []).append(os.path.relpath(root, d) + '@' + str(v))
    return out
def tail(p): return (p.stdout.strip().splitlines() or p.stderr.strip().splitlines() or ['?'])[-1][:100]
RT = SCR + '/runtime'; os.makedirs(RT)
print('node', subprocess.run(['node', '-v'], capture_output=True, text=True).stdout.strip(), 'npm', subprocess.run(['npm', '-v'], capture_output=True, text=True).stdout.strip(), '| runtime dir outside the workspace:', not RT.startswith(WT), now())
PLANS = {
  'governance': ('ci-then-prune', False),
  'originate': ('ci-omit', False),
  'referral': ('ci-then-prune', True),
  'vc-issuer': ('ci-omit', False),
}
for svc, (mode, sed) in PLANS.items():
    src = WT + '/services/' + svc
    d = RT + '/' + svc + '/app'; os.makedirs(d); log = RT + '/' + svc + '.log'
    for f in ('package.json', 'package-lock.json'): shutil.copyfile(src + '/' + f, d + '/' + f)
    if sed:
        txt = open(d + '/package.json').read(); new = ''.join(l for l in txt.splitlines(True) if '"@secuura/shared":' not in l)
        print(svc, 'sed @secuura/shared lines removed:', txt.count('"@secuura/shared":')); open(d + '/package.json', 'w').write(new)
    s0 = sha(d + '/package-lock.json')
    if mode == 'ci-then-prune':
        p = sh(['npm', 'ci', '--ignore-scripts', '--no-audit', '--no-fund'], d, log)
        print(svc, 'FULL npm ci rc', p.returncode, '|', tail(p), '| census (POSITIVE CONTROL):', census(d), now())
        p = sh(['npm', 'prune', '--omit=dev', '--no-audit', '--no-fund'], d, log)
        print(svc, 'RUNTIME npm prune --omit=dev rc', p.returncode, '|', tail(p), '| census:', census(d), '| lock sha', s0, '->', sha(d + '/package-lock.json'), now())
    else:
        c = RT + '/' + svc + '/full'; os.makedirs(c)
        for f in ('package.json', 'package-lock.json'): shutil.copyfile(d + '/' + f, c + '/' + f)
        p = sh(['npm', 'ci', '--ignore-scripts', '--no-audit', '--no-fund'], c, log)
        print(svc, 'FULL npm ci (control dir) rc', p.returncode, '|', tail(p), '| census (POSITIVE CONTROL):', census(c), now())
        p = sh(['npm', 'ci', '--ignore-scripts', '--omit=dev', '--no-audit', '--no-fund'], d, log)
        print(svc, 'RUNTIME npm ci --omit=dev rc', p.returncode, '|', tail(p), '| census:', census(d), '| lock sha', s0, '->', sha(d + '/package-lock.json'), now())
# shared (/shared ships in every service image, full install)
d = RT + '/shared'; shutil.copytree(WT + '/packages/shared', d, ignore=shutil.ignore_patterns('node_modules', 'dist', 'src'))
p = sh(['npm', 'ci', '--ignore-scripts', '--no-audit', '--no-fund'], d, RT + '/shared.log')
print('shared FULL npm ci rc', p.returncode, '|', tail(p), '| census:', census(d), now())
# who would load js-yaml in the full tree: static requirers among installed packages (governance full = pre-prune is gone; use originate/full)
c = RT + '/originate/full/node_modules'
req = []
for root, dirs, files in os.walk(c):
    if '/js-yaml' in root: continue
    for f in files:
        if f.endswith(('.js', '.cjs', '.mjs')):
            try: t = open(os.path.join(root, f), errors='ignore').read()
            except Exception: continue
            if re.search(r'''require\(\s*['"]js-yaml['"]\s*\)|from\s+['"]js-yaml['"]|import\(\s*['"]js-yaml['"]\s*\)''', t): req.append(os.path.relpath(os.path.join(root, f), c))
ctl = sum(1 for root, dirs, files in os.walk(c) for f in files if f.endswith('.js') and 'require("semver")' in open(os.path.join(root, f), errors='ignore').read()) if False else None
print('static js-yaml importers in originate FULL tree:', len(req), req[:10], now())
print('done', now())
