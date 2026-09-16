#!/usr/bin/env python3
"""probe_run.py — drafter feasibility probe for the #1001 gate set. Write verbs run ONLY in a fresh --shared clone under the
session scratchpad (mktemp -d); the Secuura checkout gets read verbs only. node_modules are symlinked FROM the main checkout.
Runs: (1) the seat's KS-1165 file at head; (2) the real-app probe at head; (3) the real-app probe with csrf.ts at the BASE blob
(the tamper 'v2 entry absent' by restoring base bytes), asserted landed by sha; restored and asserted by sha. Never rm."""
import hashlib, json, os, subprocess, sys, tempfile, datetime, shutil
SCR = '/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/9aed5a67-2729-4892-b685-13ab87142a58/scratchpad'
REPO = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
G = os.path.dirname(os.path.abspath(__file__))
H = '3925d4c072b940eb91de462b7b92eabfe8889c75'; B = '0b25f823f6660ac52b665f14055799ff0c3b616d'
GW = 'Blockchain/Dev/services/api-gateway'
CSRF = GW + '/src/middleware/csrf.ts'
def ts(): return datetime.datetime.now().astimezone().strftime('%H:%M:%S %Z')
def run(cmd, cwd=None, env=None):
    p = subprocess.run(cmd, cwd=cwd, env=env, capture_output=True, text=True)
    return p.returncode, p.stdout, p.stderr
def sha(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()
W = tempfile.mkdtemp(prefix='gate1001_probe_', dir=SCR)
C = os.path.join(W, 'clone')
print(ts(), 'workdir', W)
rc, o, e = run(['git', 'clone', '--shared', '--no-checkout', '--quiet', REPO, C]); print('clone rc', rc, e.strip()[:200])
rc, o, e = run(['git', '-C', C, 'checkout', '--quiet', '--detach', H]); print('checkout rc', rc, e.strip()[:200])
rc, o, e = run(['git', '-C', C, 'rev-parse', 'HEAD']); print('clone HEAD', o.strip(), '== H', o.strip() == H)
for rel in ('node_modules', 'Blockchain/Dev/node_modules', GW + '/node_modules'):
    src = os.path.join(REPO, rel); dst = os.path.join(C, rel)
    assert os.path.isdir(src) and not os.path.lexists(dst), rel
    os.symlink(src, dst); print('farm', rel, '->', src)
# the blobs
for ref in (H, B):
    rc, o, e = run(['git', '-C', C, 'rev-parse', ref + ':' + CSRF]); print('csrf.ts blob at', ref[:9], o.strip())
head_csrf_sha = sha(os.path.join(C, CSRF)); print('csrf.ts sha256 at head', head_csrf_sha)
gwdir = os.path.join(C, GW); vitest = os.path.join(C, 'Blockchain/Dev/node_modules/.bin/vitest')
rc, o, e = run(['node', '-e', "console.log(require.resolve('express'))"], cwd=gwdir); print('express resolves to', o.strip())
env0 = dict(os.environ); env0.pop('NODE_ENV', None)
def vit(label, files, extra_env=None):
    outj = os.path.join(W, label + '.json')
    env = dict(env0); env.update(extra_env or {})
    t0 = datetime.datetime.now()
    rc, o, e = run([vitest, 'run', *files, '--reporter=json', '--outputFile=' + outj], cwd=gwdir, env=env)
    dt = (datetime.datetime.now() - t0).total_seconds()
    try:
        j = json.load(open(outj))
        print(ts(), label, 'rc', rc, 'files', j['numTotalTestSuites'], 'tests total', j['numTotalTests'], 'passed', j['numPassedTests'], 'failed', j['numFailedTests'], 'secs %.1f' % dt)
        for tr in j['testResults']:
            for a in tr['assertionResults']:
                if a['status'] != 'passed': print('   ', a['status'], a['fullName'][:150], '|', (a.get('failureMessages') or [''])[0].split('\n')[0][:200])
            if tr.get('message'): print('   suite message:', tr['message'][:300])
    except Exception as ex:
        print(ts(), label, 'rc', rc, 'NO JSON', type(ex).__name__, 'stderr tail:', e[-1500:], 'stdout tail:', o[-800:])
    return rc
# (1) the seat's file at head
vit('seat_file_head', ['src/__tests__/ks1165-api-gateway-csrf-excludedpaths-carries-no.test.ts'])
# (2) the real-app probe at head
probe_dst = os.path.join(gwdir, 'src/__tests__/qa1001-drafter-probe.test.ts')
shutil.copyfile(os.path.join(G, 'qa1001-drafter-probe.test.ts'), probe_dst)
def probe(label):
    out = os.path.join(G, 'probe_' + label + '.json'); stack = os.path.join(G, 'probe_' + label + '_stack.json')
    vit('probe_' + label, ['src/__tests__/qa1001-drafter-probe.test.ts'], {'QA_PROBE_OUT': out, 'QA_PROBE_OUT_STACK': stack})
    if os.path.exists(out):
        for r in json.load(open(out)): print('   %-34s %-50s %3d %-22s upstream=%s %s' % (r['id'], r['path'], r['status'], r['code'], r['reachedUpstream'], r['upstreamUrl'] or ''))
    if os.path.exists(stack):
        names = json.load(open(stack)); idx = {n: i for i, n in reversed(list(enumerate(names)))}
        print('   stack layers', len(names), '| order:', [(n, i) for i, n in enumerate(names) if n in ('normaliseRepeatedSlashes', 'cookieParser', 'generateTokenMiddleware', 'protectMiddleware', 'enforceJsonContentType')])
probe('head')
# (3) csrf.ts at the BASE bytes (v2 entry absent), asserted, probe, restored by sha
rc, o, e = run(['git', '-C', C, 'show', B + ':' + CSRF])
open(os.path.join(C, CSRF), 'w', encoding='utf-8').write(o)
landed = open(os.path.join(C, CSRF), encoding='utf-8').read().count("'/api/v2/verification/verify'")
print(ts(), 'BASE csrf.ts landed: v2 entry count', landed, 'sha', sha(os.path.join(C, CSRF))[:16], '!= head', sha(os.path.join(C, CSRF)) != head_csrf_sha)
assert landed == 0
probe('base_csrf')
rc, o, e = run(['git', '-C', C, 'checkout', '--quiet', H, '--', CSRF])
print(ts(), 'restored csrf.ts sha == head', sha(os.path.join(C, CSRF)) == head_csrf_sha)
q = probe_dst + '.quarantined'; os.rename(probe_dst, q); print('probe quarantined by rename ->', q)
rc, o, e = run(['git', '-C', C, 'status', '--porcelain']); print('clone porcelain after:', o.strip().splitlines())
print(ts(), 'done')
