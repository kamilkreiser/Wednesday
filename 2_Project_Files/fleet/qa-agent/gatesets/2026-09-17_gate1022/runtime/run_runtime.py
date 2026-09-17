#!/usr/bin/env python3
"""run_runtime.py — #1022 drafter runtime reach, head and base. Probes A (stdio shipped entry), B (express image CMD entry), C (SDK
StreamableHTTP, not shipped) with a module census per process; lsof TCP LISTEN census of node pids before/after; every listener started is
ended by pid inside its probe (B SIGTERM, C in-process close, A transport close) and re-counted here. cwd per probe = img-<tree>/prod."""
import datetime, hashlib, json, os, socket, subprocess, sys
RT = os.path.dirname(os.path.abspath(__file__))
CL = open('/private/tmp/claude-501/drafter1022/CLONE_PATH').read().strip()
OUTD = RT + '/out'; os.makedirs(OUTD, exist_ok=True)
def now(): return datetime.datetime.now().astimezone().strftime('%H:%M:%S %Z')
def listen_census(tag):
    p = subprocess.run(['lsof', '-nP', '-iTCP', '-sTCP:LISTEN'], capture_output=True, text=True)
    rows = [l for l in p.stdout.splitlines()[1:] if l.split()[0] == 'node']
    pids = sorted({int(l.split()[1]) for l in rows})
    stubs = subprocess.run(['pgrep', '-f', 'login_stub.mjs'], capture_output=True, text=True).stdout.split()
    print('LISTEN %s %s: lsof rows %d (rc %d) | node LISTEN rows %d | node pids %d | login_stub.mjs procs %d' % (tag, now(), len(p.stdout.splitlines()), p.returncode, len(rows), len(pids), len(stubs)))
    return set(pids)
sample = CL + '/sample-1022.txt'
if not os.path.exists(sample): open(sample, 'w').write('qa-1022 sample document\n')
print('sample sha256', hashlib.sha256(open(sample, 'rb').read()).hexdigest())
s = socket.socket(); s.bind(('127.0.0.1', 0)); closed = s.getsockname()[1]; s.close()
print('closed loopback port', closed)
before = listen_census('before')
HONO = '/node_modules/hono/'; NODESRV = '/node_modules/@hono/node-server/'
for tree in ('base', 'head'):
    cwd = CL + '/img-%s/prod' % tree
    print('TREE', tree, 'hono', json.load(open(cwd + '/node_modules/hono/package.json'))['version'], '| cwd', cwd)
    for name, script in (('A', 'probe_stdio.mjs'), ('B', 'probe_http_express.mjs'), ('C', 'probe_sdk_http.mjs')):
        census = OUTD + '/census_%s_%s.txt' % (name, tree); out = OUTD + '/probe_%s_%s.json' % (name, tree); addr = OUTD + '/addr_%s_%s.json' % (name, tree)
        for f in (census, out, addr):
            if os.path.exists(f): os.rename(f, f + '.prior-' + datetime.datetime.now().strftime('%H%M%S'))
        open(census, 'w').close()
        env = dict(os.environ, CENSUS=RT + '/census.mjs', PIN=RT + '/loopback_pin.mjs', CENSUS_OUT=census, CLOSED_PORT=str(closed), SAMPLE=sample, OUT=out, ADDR_OUT=addr)
        env.pop('NODE_OPTIONS', None)
        args = ['node'] + (['--import', RT + '/census.mjs'] if name == 'C' else []) + [RT + '/' + script]
        # the probe scripts live outside the tree: bare specifiers must resolve from cwd's node_modules, so run a copy inside cwd
        local = cwd + '/.qa1022_' + script
        open(local, 'w').write(open(RT + '/' + script).read())
        args[-1] = local
        t0 = now(); p = subprocess.run(args, cwd=cwd, env=env, capture_output=True, text=True, timeout=120)
        lines = open(census).read().splitlines()
        urls = [l for l in lines if not l.startswith('#')]
        ctrl_idx = next((i for i, l in enumerate(lines) if 'positive control' in l), None)
        pre = lines[:ctrl_idx] if ctrl_idx is not None else lines
        post = lines[ctrl_idx:] if ctrl_idx is not None else []
        print('  probe %s %s rc %d %s->%s | census urls %d (distinct %d) | hono resolved %d | @hono/node-server resolved %d | @modelcontextprotocol/sdk %d | express %d | processes %d%s' % (
            name, tree, p.returncode, t0, now(), len(urls), len(set(urls)), sum(HONO in l for l in pre), sum(NODESRV in l for l in pre),
            sum('/@modelcontextprotocol/sdk/' in l for l in pre), sum('/node_modules/express/' in l for l in pre), sum(l.startswith('# census') for l in lines),
            (' | CONTROL after import(hono): hono resolved %d' % sum(HONO in l for l in post)) if ctrl_idx is not None else ''))
        if p.returncode: print('    stderr:', p.stderr[-1500:])
        os.rename(local, local + '.ran')
after = listen_census('after')
print('node listener pids new after the runs:', sorted(after - before), '| gone:', sorted(before - after))
# base vs head response comparison
for name in ('A', 'B', 'C'):
    try:
        a = json.load(open(OUTD + '/probe_%s_base.json' % name)); b = json.load(open(OUTD + '/probe_%s_head.json' % name))
    except Exception as e:
        print('COMPARE', name, 'unreadable', type(e).__name__, e); continue
    VOL = {'serverPid', 'childPid', 'addr', 'pid', 'serverStderr', 'stderr'}
    keys = sorted(set(a) | set(b))
    diffs = [k for k in keys if k not in VOL and a.get(k) != b.get(k)]
    print('COMPARE %s base vs head: keys %d | differing (volatile %s excluded): %s' % (name, len(keys), sorted(VOL & set(keys)), diffs))
    for k in keys:
        if k in VOL: continue
        v = json.dumps(b.get(k))
        print('   %s: %s' % (k, v[:260]))
print('done', now())
