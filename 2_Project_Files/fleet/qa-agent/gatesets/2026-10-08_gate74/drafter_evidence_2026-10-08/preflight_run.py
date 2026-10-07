#!/usr/bin/env python3
"""Drafter prediction: S-1 installs, then the preflight exactly as .githooks/pre-push invokes it
(source systemTest/slot-target.sh at the repo root, then preflight.sh from Blockchain/Dev).
Usage: preflight_run.py <worktree> <tag> <evdir>"""
import os, subprocess, sys, time
wt, tag, ev = sys.argv[1:4]
def log(m):
    open(os.path.join(ev, 'pf_%s.steps' % tag), 'a').write('%s %s\n' % (time.strftime('%H:%M:%SZ', time.gmtime()), m))
def run(args, cwd, out, env=None):
    with open(out, 'w') as fh:
        rc = subprocess.run(args, cwd=cwd, stdout=fh, stderr=subprocess.STDOUT, env=env).returncode
    open(out, 'a').write('rc=%d\n' % rc); return rc
E = dict(os.environ); E.pop('GIT_SSH_COMMAND', None); E['TMPDIR'] = '/tmp'
log('start %s' % wt)
dev = os.path.join(wt, 'Blockchain/Dev')
log('ci dev rc=%d' % run(['npm', 'ci', '--ignore-scripts'], dev, os.path.join(ev, 'pf_%s_ci_dev.log' % tag), E))
log('build shared rc=%d' % run(['npm', 'run', 'build', '--workspace=packages/shared'], dev, os.path.join(ev, 'pf_%s_build_shared.log' % tag), E))
log('shared dist %s' % ('PRESENT' if os.path.isfile(os.path.join(dev, 'packages/shared/dist/index.js')) else 'ABSENT'))
for p in ('akto', 'api-explorer', 'performance', 'playwright'):
    d = os.path.join(wt, 'systemTest', p)
    if not os.path.isfile(os.path.join(d, 'package.json')): log('no package.json %s' % p); continue
    if os.path.isdir(os.path.join(d, 'node_modules')): log('%s already installed' % p); continue
    log('ci %s rc=%d' % (p, run(['npm', 'ci', '--ignore-scripts'], d, os.path.join(ev, 'pf_%s_ci_%s.log' % (tag, p)), E)))
log('installs done; preflight start')
script = ('. systemTest/slot-target.sh >/dev/null 2>&1 || true\n'
          'builtin pushd Blockchain/Dev >/dev/null || exit 1\n'
          'bash scripts/preflight/preflight.sh\n')
rc = run(['bash', '-c', script], wt, os.path.join(ev, 'pf_%s.out' % tag), E)
open(os.path.join(ev, 'pf_%s.rc' % tag), 'w').write('rc=%d\n' % rc)
log('preflight end rc=%d' % rc)
