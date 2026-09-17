#!/usr/bin/env python3
"""preflight_run.py — #1020 drafter: the REAL scripts/preflight/preflight.sh, run whole inside the drafter's OWN scratch clone worktrees
(never the Secuura checkout or its worktrees), head then base, GATEWAY_URL pointed at a closed loopback port so the stack legs SKIP.
Then audit:contract + lock-discovery on head under an injected 2026-09-24T00:00Z clock (does leg 5 red when the baseline rows lapse?).
Per-leg verdict lines are extracted from the saved output. Writes only inside the clone and to gatesets/…/out/."""
import json, os, re, subprocess, datetime, socket
GS = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1020'
T = json.load(open(GS + '/drafter_paths.json'))['trees']
FAKE = 'file://' + GS + '/fakeclock.mjs'
def ts(): return datetime.datetime.now().astimezone().strftime('%H:%M:%S %Z')
def P(*a): print(' '.join(str(x) for x in a), flush=True)
def env(fake=None, port=None):
    e = dict(os.environ)
    for k in ('GIT_DIR', 'GIT_WORK_TREE', 'GIT_INDEX_FILE', 'GIT_COMMON_DIR', 'NODE_OPTIONS', 'QA_FAKE_NOW', 'NODE_ENV'): e.pop(k, None)
    if port: e['GATEWAY_URL'] = 'http://127.0.0.1:%d' % port
    if fake: e['NODE_OPTIONS'] = '--import=' + FAKE; e['QA_FAKE_NOW'] = fake
    return e
s = socket.socket(); s.bind(('127.0.0.1', 0)); port = s.getsockname()[1]; s.close()
rc = subprocess.run(['curl', '-sf', '-o', '/dev/null', '--max-time', '3', 'http://127.0.0.1:%d/health' % port]).returncode
P('preflight_run', datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z'), '| closed port', port, 'curl rc', rc, '(non-zero = closed, as intended)')
for tree in ('head', 'base'):
    dev = T[tree] + '/Blockchain/Dev'; t0 = datetime.datetime.now()
    p = subprocess.run(['bash', 'scripts/preflight/preflight.sh'], cwd=dev, env=env(port=port), capture_output=True, text=True, timeout=1800)
    dt = (datetime.datetime.now() - t0).total_seconds(); out = p.stdout + '\n--- stderr\n' + p.stderr
    open(GS + '/out/P_preflight_%s.out' % tree, 'w').write('# cwd %s rc %d secs %.1f\n%s' % (dev, p.returncode, dt, out))
    P('\n%s preflight.sh tree %s rc %d secs %.1f' % (ts(), tree, p.returncode, dt))
    cur = None; verdicts = {}
    for l in out.splitlines():
        m = re.search(r'\b(\d+)/15\s', l)
        if m and ('==' in l or l.lstrip().startswith(m.group(1))): cur = int(m.group(1)); verdicts.setdefault(cur, []); continue
        if cur and re.match(r'\s*(OK|FAIL|SKIP|PASS|  \^ leg)', l): verdicts[cur].append(l.strip()[:150])
    for k in sorted(verdicts): P('  leg %2d: %s' % (k, ' || '.join(verdicts[k][:2]) or '(no OK/FAIL/SKIP line captured — read the raw output)'))
    for l in out.splitlines()[-12:]: P('  tail |', l[:160])
    r = subprocess.run(['git', '-C', T[tree], 'status', '--porcelain', '--untracked-files=no'], capture_output=True, text=True).stdout
    P('  tracked porcelain after', len(r.splitlines()))
P('\n%s head under injected 2026-09-24T00:00:00.000Z' % ts())
dev = T['head'] + '/Blockchain/Dev'
for label, cmd in (('contract', ['npm', 'run', 'audit:contract', '--silent']), ('lockdiscovery', ['node', '--test', 'scripts/audit/lock-discovery.test.mjs'])):
    p = subprocess.run(cmd, cwd=dev, env=env(fake='2026-09-24T00:00:00.000Z'), capture_output=True, text=True, timeout=900)
    o = p.stdout + p.stderr
    open(GS + '/out/P_head_0924_%s.out' % label, 'w').write('# cwd %s fake 2026-09-24T00:00:00.000Z rc %d\n%s' % (dev, p.returncode, o))
    g = lambda k: (re.findall(r'^ℹ %s (\d+)' % k, o, re.M) or ['NO-SUMMARY'])[-1]
    P('  %-14s rc %d tests %s pass %s fail %s' % (label, p.returncode, g('tests'), g('pass'), g('fail')))
    for l in o.split('✖ failing tests:')[0].splitlines():
        if l.startswith('✖ '): P('     fail:', l[2:130])
P('done', ts())
