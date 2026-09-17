#!/usr/bin/env python3
"""drafter_regen_1033.py — #1033 Q6 + cause-side census.
R  Re-derive the READY's lock regeneration in the drafter's OWN clone (fresh detached worktrees at develop bb848b828, head manifests copied in):
   R1 root: `npm update mysql2 --package-lock-only --ignore-scripts` in Blockchain/Dev  -> must be byte-identical to head's root lock 646c19f6f
   R0 root TRAP control: `npm install --package-lock-only --ignore-scripts` in Blockchain/Dev (READY: rc 0 and INERT, lock stays 3.15.3)
   R2 originate: `npm install --package-lock-only --ignore-scripts --no-workspaces` in services/originate -> must equal head's 4c1800aee
   R3 control: the same originate command WITHOUT the manifest override -> lock must stay at 3.15.3 (the instrument can fail)
C  Cause-side census (#1027 F1 method): files in the base and head RUNTIME trees (runner :79) carrying mysql2-specific code markers
   ('mysql_clear_password' = GHSA-3f6p's auth plugin; 'compressed_protocol' / 'inflateSync' in a mysql2-shaped file = GHSA-rgwj's handler),
   inside vs OUTSIDE node_modules/mysql2. Positive control: the mysql2 dir itself carries the marker."""
import datetime, hashlib, json, os, re, shutil, subprocess, sys, glob
GS = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1033'
OUT = GS + '/out'
P = json.load(open(OUT + '/drafter_paths.json')); SCR, C = P['SCR'], P['C']
def now(): return datetime.datetime.now().astimezone().strftime('%H:%M:%S %Z')
def load(): return '%.1f/%.1f/%.1f' % os.getloadavg()
def blob(path): return subprocess.run(['git', 'hash-object', path], capture_output=True, text=True).stdout.strip()
def lockv(path, key='node_modules/mysql2'): return json.load(open(path))['packages'].get(key, {}).get('version')
print('drafter_regen_1033 start', now(), 'load', load())
def wt(name):
    d = SCR + '/wt_regen_' + name
    p = subprocess.run(['git', '-C', C, 'worktree', 'add', '--detach', '-q', d, P['BASE']], capture_output=True, text=True)
    if p.returncode: print('worktree add failed', p.stderr); sys.exit(1)
    return d + '/Blockchain/Dev'
def put_head_manifests(dev, root=True, orig=True):
    if root: shutil.copyfile(SCR + '/wt_head/Blockchain/Dev/package.json', dev + '/package.json')
    if orig: shutil.copyfile(SCR + '/wt_head/Blockchain/Dev/services/originate/package.json', dev + '/services/originate/package.json')
def npm(args, cwd):
    t0, l0 = now(), load()
    p = subprocess.run(['npm'] + args + ['--no-audit', '--no-fund'], cwd=cwd, capture_output=True, text=True, timeout=900)
    open(OUT + '/regen.cmdlog', 'a').write('\n### $ npm %s (cwd %s) rc %d\n%s\n--stderr--\n%s\n' % (' '.join(args), cwd, p.returncode, p.stdout[-5000:], p.stderr[-5000:]))
    return p.returncode, '[%s load %s -> %s]' % (t0, l0, now())
HEAD_ROOT, HEAD_ORIG = '646c19f6f', '4c1800aee'
d0 = wt('r0'); put_head_manifests(d0)
b0 = blob(d0 + '/package-lock.json'); rc, t = npm(['install', '--package-lock-only', '--ignore-scripts'], d0)
print('R0 TRAP root npm install --package-lock-only --ignore-scripts rc %s %s | lock %s -> %s | byte-identical to develop %s | mysql2 %s | nm created %s' % (
    rc, t, b0[:9], blob(d0 + '/package-lock.json')[:9], blob(d0 + '/package-lock.json') == b0, lockv(d0 + '/package-lock.json'), os.path.exists(d0 + '/node_modules')))
d1 = wt('r1'); put_head_manifests(d1)
rc, t = npm(['update', 'mysql2', '--package-lock-only', '--ignore-scripts'], d1)
print('R1 root npm update mysql2 --package-lock-only --ignore-scripts rc %s %s | lock -> %s | == head %s: %s | mysql2 %s' % (
    rc, t, blob(d1 + '/package-lock.json')[:9], HEAD_ROOT, blob(d1 + '/package-lock.json').startswith(HEAD_ROOT), lockv(d1 + '/package-lock.json')))
d2 = wt('r2'); put_head_manifests(d2, root=False)
o2 = d2 + '/services/originate'
rc, t = npm(['install', '--package-lock-only', '--ignore-scripts', '--no-workspaces'], o2)
print('R2 originate npm install --package-lock-only --ignore-scripts --no-workspaces rc %s %s | lock -> %s | == head %s: %s | mysql2 %s' % (
    rc, t, blob(o2 + '/package-lock.json')[:9], HEAD_ORIG, blob(o2 + '/package-lock.json').startswith(HEAD_ORIG), lockv(o2 + '/package-lock.json')))
d3 = wt('r3'); o3 = d3 + '/services/originate'
rc, t = npm(['install', '--package-lock-only', '--ignore-scripts', '--no-workspaces'], o3)
print('R3 CONTROL originate same command, NO override rc %s %s | lock -> %s | == develop 040908e22: %s | mysql2 %s' % (
    rc, t, blob(o3 + '/package-lock.json')[:9], blob(o3 + '/package-lock.json').startswith('040908e22'), lockv(o3 + '/package-lock.json')))
for d in (d0, d1, d2, d3):
    p = subprocess.run(['git', '-C', d, 'status', '--porcelain'], capture_output=True, text=True); print('   worktree', d.split('/')[-3], 'porcelain:', p.stdout.split('\n')[:4])
# C cause-side census
RT = sorted(glob.glob('/private/tmp/claude-501/drafter1033/runtime_*'))[-1]
MARK = [('mysql_clear_password', re.compile(rb'mysql_clear_password')), ('compressed_protocol', re.compile(rb'compressed_protocol|compressedProtocol')),
        ('COM_QUERY+handshake', re.compile(rb'HandshakeResponse41|ClientHandshake'))]
for tree in ('base', 'head'):
    nm = RT + '/%s/runner/node_modules' % tree
    res = {m: {'in': set(), 'out': set()} for m, _ in MARK}
    for root, dirs, files in os.walk(nm):
        for f in files:
            if not f.endswith(('.js', '.cjs', '.mjs')): continue
            p = os.path.join(root, f)
            if os.path.islink(p): continue
            try: b = open(p, 'rb').read()
            except Exception: continue
            rel = os.path.relpath(p, nm)
            for m, rx in MARK:
                if rx.search(b): res[m]['in' if rel.startswith('mysql2/') else 'out'].add(rel)
    print('C %s runtime tree %s: %s' % (tree, nm, {m: ('inside mysql2 %d (POSITIVE CONTROL)' % len(v['in']), 'OUTSIDE %d %s' % (len(v['out']), sorted(v['out'])[:5])) for m, v in res.items()}))
print('done', now(), 'load', load())
