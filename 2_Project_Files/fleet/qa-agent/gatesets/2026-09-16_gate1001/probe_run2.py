#!/usr/bin/env python3
"""probe_run2.py — drafter pre-check of the brief's proposed tamper rows, in the SAME scratch clone probe_run.py built
(argv[1] = its workdir). Every tamper asserts its anchor count BEFORE and its marker AFTER; restore = git checkout of the
file at head, asserted by sha256. Runs the seat's file AND the real-app probe2 under each; the full api-gateway suite at head
once. Write verbs in the clone only. Never rm; the probe file is quarantined by rename at the end."""
import hashlib, json, os, subprocess, sys, datetime, shutil
W = sys.argv[1]; C = os.path.join(W, 'clone')
G = os.path.dirname(os.path.abspath(__file__))
H = '3925d4c072b940eb91de462b7b92eabfe8889c75'
GW = 'Blockchain/Dev/services/api-gateway'; gwdir = os.path.join(C, GW)
IDX = os.path.join(C, GW, 'src/index.ts')
vitest = os.path.join(C, 'Blockchain/Dev/node_modules/.bin/vitest')
def ts(): return datetime.datetime.now().astimezone().strftime('%H:%M:%S %Z')
def sha(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()
def run(cmd, cwd=None, env=None):
    p = subprocess.run(cmd, cwd=cwd, env=env, capture_output=True, text=True); return p.returncode, p.stdout, p.stderr
rc, o, e = run(['git', '-C', C, 'rev-parse', 'HEAD']); assert o.strip() == H, o
idx_sha = sha(IDX); print(ts(), 'index.ts sha256 at head', idx_sha[:16])
env0 = dict(os.environ); env0.pop('NODE_ENV', None)
probe_dst = os.path.join(gwdir, 'src/__tests__/qa1001-drafter-probe2.test.ts')
shutil.copyfile(os.path.join(G, 'qa1001-drafter-probe2.test.ts'), probe_dst)
SHOW = {'v2-verify', 'v2-verify-file-octet', 'neighbour-documents', 'neighbour-documents-octet', 'neighbour-documents-no-cookie', 'v1-dot-segment-to-documents', 'dot-segment-to-documents'}
def vit(label, files, extra=None, show_rows=False):
    outj = os.path.join(W, 'r2_' + label + '.json'); env = dict(env0); env.update(extra or {})
    t0 = datetime.datetime.now(); rc, o, e = run([vitest, 'run', *files, '--reporter=json', '--outputFile=' + outj], cwd=gwdir, env=env)
    dt = (datetime.datetime.now() - t0).total_seconds()
    try:
        j = json.load(open(outj))
        print(ts(), label, 'rc', rc, 'suites', len(j['testResults']), 'tests', j['numTotalTests'], 'passed', j['numPassedTests'], 'failed', j['numFailedTests'], 'secs %.1f' % dt)
        for tr in j['testResults']:
            if tr.get('status') == 'failed' and not tr['assertionResults']: print('   LOAD FAILURE', os.path.basename(tr['name']), (tr.get('message') or '')[:300])
            for a in tr['assertionResults']:
                if a['status'] != 'passed': print('   ', a['status'], os.path.basename(tr['name']), '|', a['title'][:110], '|', (a.get('failureMessages') or [''])[0].split('\n')[0][:160])
    except Exception as ex:
        print(ts(), label, 'rc', rc, 'NO JSON', type(ex).__name__, e[-800:])
def both(label):
    vit(label + '_seatfile', ['src/__tests__/ks1165-api-gateway-csrf-excludedpaths-carries-no.test.ts'])
    out = os.path.join(G, 'probe2_' + label + '.json'); stack = os.path.join(G, 'probe2_' + label + '_stack.json')
    for p in (out, stack):
        if os.path.exists(p): os.rename(p, p + '.stale-' + datetime.datetime.now().strftime('%H%M%S'))
    vit(label + '_realapp', ['src/__tests__/qa1001-drafter-probe2.test.ts'], {'QA_PROBE_OUT': out, 'QA_PROBE_OUT_STACK': stack})
    if os.path.exists(out):
        for r in json.load(open(out)):
            if r['id'] in SHOW: print('     %-30s %3d %-20s upstream=%s %s' % (r['id'], r['status'], r['code'], r['reachedUpstream'], r['upstreamUrl'] or ''))
    if os.path.exists(stack):
        names = json.load(open(stack))
        print('     order:', [(n, i) for i, n in enumerate(names) if n in ('cookieParser', 'generateTokenMiddleware', 'protectMiddleware', 'enforceJsonContentType')])
def tamper(label, old, new, count_old=1, marker=None):
    s = open(IDX, encoding='utf-8').read(); c = s.count(old)
    print(ts(), label, 'anchor count', c, 'expected', count_old); assert c == count_old, label
    s2 = s.replace(old, new); open(IDX, 'w', encoding='utf-8').write(s2)
    m = marker or new; mc = open(IDX, encoding='utf-8').read().count(m); print(ts(), label, 'marker count after', mc); assert mc >= 1
    both(label)
    run(['git', '-C', C, 'checkout', '--quiet', H, '--', GW + '/src/index.ts']); ok = sha(IDX) == idx_sha
    print(ts(), label, 'restored index.ts sha == head', ok); assert ok
# 0. the full api-gateway suite at head (probe2 excluded by rename first)
os.rename(probe_dst, probe_dst + '.hold'); vit('full_suite_head', []); os.rename(probe_dst + '.hold', probe_dst)
# 1. head, no tamper (probe2's extra rows)
both('head')
# T-ENV: the F-14 regression — CSRF mounted only in production. The seat's order cell reads text, not the condition.
tamper('T_ENV', "if (NODE_ENV !== 'test') {\n  app.use(csrfMiddleware.generateToken);", "if (NODE_ENV === 'production') {\n  app.use(csrfMiddleware.generateToken);", 1, "if (NODE_ENV === 'production') {\n  app.use(csrfMiddleware.generateToken);")
# T-DECOY: the real protect mount moved BELOW enforceJsonContentType, a comment copy of the old line left in its place.
old = "  app.use(csrfMiddleware.protect);\n}\n"
s = open(IDX, encoding='utf-8').read(); assert s.count(old) == 1 and s.count('app.use(enforceJsonContentType);\n') == 1
new_block = "  // app.use(csrfMiddleware.protect);\n}\n"
tamper_old = old + s[s.index(old) + len(old): s.index('app.use(enforceJsonContentType);\n') + len('app.use(enforceJsonContentType);\n')]
tamper_new = new_block + s[s.index(old) + len(old): s.index('app.use(enforceJsonContentType);\n') + len('app.use(enforceJsonContentType);\n')] + "if (NODE_ENV !== 'test') app.use(csrfMiddleware.protect);\n"
tamper('T_DECOY', tamper_old, tamper_new, 1, "if (NODE_ENV !== 'test') app.use(csrfMiddleware.protect);\n")
q = probe_dst + '.quarantined'; os.rename(probe_dst, q); print('probe2 quarantined ->', os.path.basename(q))
rc, o, e = run(['git', '-C', C, 'status', '--porcelain']); print('clone porcelain after:', o.strip().splitlines())
print(ts(), 'done')
