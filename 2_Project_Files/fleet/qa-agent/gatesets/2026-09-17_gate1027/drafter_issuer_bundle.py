#!/usr/bin/env python3
"""drafter_issuer_bundle.py — #1027: does bbm 2.10.43 -> 2.11.24 move frontend/issuer's BUILT bundle? Reproduces the Dockerfile builder stage
(frontend/issuer/Dockerfile:11-28) with HOST npm OUTSIDE Blockchain/Dev (the standalone lock, not the workspace root): app/ = issuer files minus
node_modules/dist, app/vendor/shared = frontend/shared, SHARED_DIR=./vendor/shared/src, `npm ci --no-audit --ignore-scripts` (the image runs
scripts; the drafter does not — named deviation), `npm run build`, at develop 19f1e5475 and head d7fc6cc55. Compares dist/ file-by-file sha256.
CONTROL: the same head build run twice must be byte-identical (build determinism), else a head/develop difference proves nothing."""
import datetime, hashlib, json, os, shutil, subprocess
SCR = open('/private/tmp/claude-501/drafter1027.CLONE_PATH').read().strip()
def now(): return datetime.datetime.now().astimezone().strftime('%H:%M:%S %Z')
def tree_hash(d):
    out = {}
    for root, dirs, files in os.walk(d):
        for f in files:
            p = os.path.join(root, f); out[os.path.relpath(p, d)] = hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]
    return out
res = {}
for tag, t in (('develop', 'develop'), ('head', 'head'), ('head2', 'head')):
    src = SCR + '/wt-%s/Blockchain/Dev' % t
    x = SCR + '/fe-issuer-' + tag; app = x + '/app'
    shutil.copytree(src + '/frontend/issuer', app, ignore=shutil.ignore_patterns('node_modules', 'dist'))
    shutil.copytree(src + '/frontend/shared', app + '/vendor/shared', ignore=shutil.ignore_patterns('node_modules', 'dist'))
    env = dict(os.environ, SHARED_DIR='./vendor/shared/src')
    p = subprocess.run(['npm', 'ci', '--no-audit', '--no-fund', '--ignore-scripts'], cwd=app, capture_output=True, text=True, env=env)
    open(x + '/ci.log', 'w').write(p.stdout + '\n--stderr--\n' + p.stderr)
    bbm = json.load(open(app + '/node_modules/baseline-browser-mapping/package.json'))['version'] if os.path.exists(app + '/node_modules/baseline-browser-mapping/package.json') else 'ABSENT'
    print(tag, 'npm ci rc', p.returncode, '| installed bbm', bbm, now())
    p = subprocess.run(['npm', 'run', 'build'], cwd=app, capture_output=True, text=True, env=env)
    open(x + '/build.log', 'w').write(p.stdout + '\n--stderr--\n' + p.stderr)
    print(tag, 'npm run build rc', p.returncode, '|', (p.stdout.strip().splitlines() or ['?'])[-1][:120], now())
    res[tag] = tree_hash(app + '/dist') if os.path.isdir(app + '/dist') else {}
    print(tag, 'dist files', len(res[tag]), 'bytes', sum(os.path.getsize(os.path.join(r, f)) for r, _, fs in os.walk(app + '/dist') for f in fs) if res[tag] else 0)
def cmp(a, b):
    return sorted(k for k in set(res[a]) | set(res[b]) if res[a].get(k) != res[b].get(k))
print('CONTROL head vs head2 differing files:', cmp('head', 'head2'))
print('develop vs head differing files:', cmp('develop', 'head'))
print('done', now())
