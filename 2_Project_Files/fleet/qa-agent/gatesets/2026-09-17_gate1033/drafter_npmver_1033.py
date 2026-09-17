#!/usr/bin/env python3
"""drafter_npmver_1033.py — #1033 Q6 follow-up: the READY's root recipe (`npm update mysql2 --package-lock-only --ignore-scripts` on develop's
root lock + the head manifests) was INERT on host npm 11.5.1 (drafter_regen.out R1). Is it npm-version dependent?
Minimal workspace copy = every package.json / package-lock.json under Blockchain/Dev of a fresh develop bb848b828 worktree (no node_modules),
head's root + originate manifests copied in. Runs, each on its OWN fresh copy:
 N0 host npm 11.5.1 update (CONTROL: must reproduce R1's 86c3685d8 — proves the minimal copy is equivalent)
 N1 node:24-alpine npm (11.19.0) update                    -> == head 646c19f6f ?
 N2 node:24-alpine npm install --package-lock-only (TRAP)   -> READY: byte-identical to develop at 3.15.3
 N3 node:24-alpine npm update, NO manifest override (CONTROL: must stay 3.15.3)
Containers named drafter1033-npmver-<run>-<epoch>, removed by exact name."""
import datetime, json, os, shutil, subprocess, sys, tempfile, time
GS = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1033'
OUT = GS + '/out'
P = json.load(open(OUT + '/drafter_paths.json')); SCR = P['SCR']
NV = tempfile.mkdtemp(prefix='npmver_', dir='/private/tmp/claude-501/drafter1033')
def now(): return datetime.datetime.now().astimezone().strftime('%H:%M:%S %Z')
def load(): return '%.1f/%.1f/%.1f' % os.getloadavg()
def blob(p): return subprocess.run(['git', 'hash-object', p], capture_output=True, text=True).stdout.strip()
SRC = SCR + '/wt_regen_r3/Blockchain/Dev'   # develop bb848b828, untouched by R3 (porcelain empty)
p = subprocess.run(['git', '-C', SRC, 'status', '--porcelain'], capture_output=True, text=True)
print('drafter_npmver_1033 start', now(), 'load', load(), '| source worktree porcelain', repr(p.stdout), '| HEAD', subprocess.run(['git', '-C', SRC, 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip()[:9])
def mk(name, override=True):
    d = NV + '/' + name
    n = 0
    for root, dirs, files in os.walk(SRC):
        dirs[:] = [x for x in dirs if x not in ('node_modules', '.git')]
        for f in files:
            if f in ('package.json', 'package-lock.json'):
                rel = os.path.relpath(os.path.join(root, f), SRC); os.makedirs(os.path.dirname(d + '/' + rel), exist_ok=True)
                shutil.copyfile(os.path.join(root, f), d + '/' + rel); n += 1
    if override:
        shutil.copyfile(SCR + '/wt_head/Blockchain/Dev/package.json', d + '/package.json')
        shutil.copyfile(SCR + '/wt_head/Blockchain/Dev/services/originate/package.json', d + '/services/originate/package.json')
    return d, n
def verdict(tag, d, t, rc, extra=''):
    lk = json.load(open(d + '/package-lock.json'))['packages']
    b = blob(d + '/package-lock.json')
    print('%s rc %s %s | root lock %s | == head 646c19f6f %s | == develop 5bd5680f8 %s | == host-11.5.1 R1 86c3685d8 %s | mysql2 %s sql-escaper %s sqlstring %s %s' % (
        tag, rc, t, b[:9], b.startswith('646c19f6f'), b.startswith('5bd5680f8'), b.startswith('86c3685d8'), lk.get('node_modules/mysql2', {}).get('version'),
        lk.get('node_modules/sql-escaper', {}).get('version'), lk.get('node_modules/sqlstring', {}).get('version'), extra))
d, n = mk('n0'); print('minimal copy files', n)
t0, l0 = now(), load(); r = subprocess.run(['npm', 'update', 'mysql2', '--package-lock-only', '--ignore-scripts', '--no-audit', '--no-fund'], cwd=d, capture_output=True, text=True, timeout=600)
verdict('N0 host npm %s update' % subprocess.run(['npm', '-v'], capture_output=True, text=True).stdout.strip(), d, '[%s load %s -> %s]' % (t0, l0, now()), r.returncode, r.stderr[-200:].strip())
for tag, cmd, override in (('N1', 'npm update mysql2 --package-lock-only --ignore-scripts --no-audit --no-fund', True),
                           ('N2', 'npm install --package-lock-only --ignore-scripts --no-audit --no-fund', True),
                           ('N3', 'npm update mysql2 --package-lock-only --ignore-scripts --no-audit --no-fund', False)):
    d, n = mk(tag.lower(), override)
    name = 'drafter1033-npmver-%s-%d' % (tag.lower(), int(time.time()))
    t0, l0 = now(), load()
    r = subprocess.run(['docker', 'run', '--name', name, '-v', d + ':/w', '-w', '/w', 'node:24-alpine', 'sh', '-c', 'echo npm $(npm -v); ' + cmd + '; echo RC=$?'], capture_output=True, text=True, timeout=900)
    rm = subprocess.run(['docker', 'rm', name], capture_output=True, text=True)
    open(OUT + '/npmver_%s.log' % tag, 'w').write(r.stdout + '\n--stderr--\n' + r.stderr)
    verdict('%s container %s (%s; override %s)' % (tag, name, cmd.split(' --')[0], override), d, '[%s load %s -> %s]' % (t0, l0, now()), [l for l in r.stdout.splitlines() if l.startswith(('RC=', 'npm '))], 'docker rm rc %d' % rm.returncode)
print('containers of mine remaining:', subprocess.run(['docker', 'ps', '-a', '--filter', 'name=drafter1033-', '--format', '{{.Names}}'], capture_output=True, text=True).stdout.split())
print('done', now(), 'load', load())
