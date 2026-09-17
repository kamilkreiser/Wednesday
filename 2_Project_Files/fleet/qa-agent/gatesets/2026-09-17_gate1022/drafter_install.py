#!/usr/bin/env python3
"""drafter_install.py (r2) — #1022: install mcp-server the way its Dockerfile does, OUTSIDE the workspace (a first run of `npm ci` inside the
member dir silently installed from the Blockchain/Dev workspace ROOT lock, not the standalone lock — quarantined, see the .first-run out).
Per tree: img-<t>/prod = package.json + package-lock.json, `npm ci --ignore-scripts --omit=dev` (the runtime stage);
img-<t>/build = the same + `npm ci --ignore-scripts` (full) + src/tsconfig/openapi copied + packages/shared built and symlinked, `npm run build`.
Lock sha256 before/after asserted; installed versions read from node_modules."""
import hashlib, json, os, shutil, subprocess, datetime
CL = open('/private/tmp/claude-501/drafter1022/CLONE_PATH').read().strip()
def now(): return datetime.datetime.now().astimezone().strftime('%H:%M:%S %Z')
def sh(args, cwd, log):
    p = subprocess.run(args, cwd=cwd, capture_output=True, text=True)
    open(log, 'w').write(p.stdout + '\n--stderr--\n' + p.stderr)
    return p
def ver(d, pkg):
    f = d + '/node_modules/' + pkg + '/package.json'
    return json.load(open(f))['version'] if os.path.exists(f) else 'ABSENT'
print('node', subprocess.run(['node', '-v'], capture_output=True, text=True).stdout.strip())
for t in ('head', 'base'):
    src = CL + '/wt-%s/Blockchain/Dev' % t
    img = CL + '/img-' + t; os.makedirs(img, exist_ok=False)
    # shared, as Dockerfile stage 0
    shared = img + '/shared'; shutil.copytree(src + '/packages/shared', shared, ignore=shutil.ignore_patterns('node_modules', 'dist'))
    p = sh(['npm', 'ci', '--ignore-scripts', '--no-audit', '--no-fund'], shared, img + '/shared_ci.log'); print(t, 'shared npm ci rc', p.returncode, now())
    p = sh(['npm', 'run', 'build'], shared, img + '/shared_build.log'); print(t, 'shared build rc', p.returncode, 'dist index.js', os.path.exists(shared + '/dist/index.js'), now())
    for stage, extra in (('build', []), ('prod', ['--omit=dev'])):
        d = img + '/' + stage; os.makedirs(d)
        for f in ('package.json', 'package-lock.json'): shutil.copyfile(src + '/services/mcp-server/' + f, d + '/' + f)
        s0 = hashlib.sha256(open(d + '/package-lock.json', 'rb').read()).hexdigest()[:16]
        p = sh(['npm', 'ci', '--ignore-scripts', '--no-audit', '--no-fund'] + extra, d, img + '/%s_ci.log' % stage)
        s1 = hashlib.sha256(open(d + '/package-lock.json', 'rb').read()).hexdigest()[:16]
        print(t, stage, 'npm ci', ' '.join(extra), 'rc', p.returncode, '| lock sha', s0, '->', s1, '|', (p.stdout.strip().splitlines() or ['?'])[-1], now())
        for pkg in ('hono', '@hono/node-server', '@modelcontextprotocol/sdk', 'express', 'zod', 'typescript'): print('   ', pkg, ver(d, pkg))
        os.makedirs(d + '/node_modules/@secuura', exist_ok=True); os.symlink(shared, d + '/node_modules/@secuura/shared')
        if stage == 'build':
            for f in ('tsconfig.json', 'openapi.yaml'): shutil.copyfile(src + '/services/mcp-server/' + f, d + '/' + f)
            shutil.copytree(src + '/services/mcp-server/src', d + '/src')
            p = sh(['npm', 'run', 'build'], d, img + '/build_tsc.log'); print(t, 'mcp-server npm run build rc', p.returncode, '| dist', sorted(os.listdir(d + '/dist')) if os.path.isdir(d + '/dist') else 'none', now())
    shutil.copytree(img + '/build/dist', img + '/prod/dist'); shutil.copyfile(src + '/services/mcp-server/openapi.yaml', img + '/prod/openapi.yaml')
    print(t, 'prod stage assembled (dist from build, as Dockerfile stage 2)')
