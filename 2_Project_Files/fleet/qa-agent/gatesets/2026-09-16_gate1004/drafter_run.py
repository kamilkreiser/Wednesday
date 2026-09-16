#!/usr/bin/env python3
"""drafter_run.py — the drafter's feasibility runs for #1004, in the scratch clone built by drafter_setup.py. Write verbs in the clone only.
Every tampered/base file is restored by `git checkout <head> -- <file>` and asserted by whole-file sha256."""
import hashlib, json, os, shutil, subprocess, sys, datetime, tempfile
SCR = '/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/9aed5a67-2729-4892-b685-13ab87142a58/scratchpad'
G = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-16_gate1004'
P = json.load(open(SCR + '/gate1004_draft_paths.json')); C = P['C']; W = P['W']
H = '6d077d3fe35cd5f3c09d394553d320e97b1abe32'; B = '5b4f38a48aeb40c2295895aaa5cd08e273aa7a08'
SH = C + '/Blockchain/Dev/packages/shared'; GUARD_REL = 'Blockchain/Dev/packages/shared/src/security/ssrf-guard.ts'; GUARD = C + '/' + GUARD_REL
SEAT = 'src/__tests__/ks932-timeout-bounds-dns.test.ts'
now = lambda: datetime.datetime.now().astimezone().strftime('%H:%M:%S')
sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()
def run(cmd, cwd=SH, env=None, timeout=900):
    e = dict(os.environ); e.update(env or {})
    t = datetime.datetime.now(); p = subprocess.run(cmd, cwd=cwd, env=e, capture_output=True, text=True, timeout=timeout)
    print(now(), 'rc', p.returncode, '%.1fs' % (datetime.datetime.now() - t).total_seconds(), ' '.join(cmd)[:150]); return p
def vitest(label, files, extra=None, env=None):
    out = W + '/vt_' + label + '.json'
    p = run(['npx', 'vitest', 'run', *files, '--reporter=json', '--outputFile=' + out] + (extra or []), env=env)
    if not os.path.exists(out): print('  NO JSON', p.stderr[-1500:]); return None
    j = json.load(open(out)); shutil.copyfile(out, G + '/vt_' + label + '.json')
    print('  %s: files %d tests %d passed %d failed %d | unhandled errors in stderr: %s' % (label, j['numTotalTestSuites'] and len(j['testResults']), j['numTotalTests'], j['numPassedTests'], j['numFailedTests'], 'Unhandled' in p.stdout + p.stderr))
    for tr in j['testResults']:
        for a in tr['assertionResults']:
            if a['status'] != 'passed' or label.startswith('seat'): print('   ', a['status'], round(a.get('duration') or 0), a['title'][:90], (a.get('failureMessages') or [''])[0][:160].replace('\n', ' '))
        if tr.get('message'): print('   file message:', tr['message'][:300])
    return j
HEAD_SHA256 = sha(GUARD); print(now(), 'head ssrf-guard.ts sha256', HEAD_SHA256[:16])
def restore():
    run(['git', '-C', C, 'checkout', H, '--', GUARD_REL], cwd=C)
    assert sha(GUARD) == HEAD_SHA256, 'restore sha mismatch'; print('  restored, sha256 ==', HEAD_SHA256[:16])
# 1. seat file at head x3
for i in (1, 2, 3): vitest('seat_head_%d' % i, [SEAT])
# 2. drafter probe at head and at base bytes
shutil.copyfile(G + '/qa1004-drafter-probe.test.ts', SH + '/src/__tests__/qa1004-drafter-probe.test.ts')
vitest('probe_head', ['src/__tests__/qa1004-drafter-probe.test.ts'], env={'QA1004_OUT': G + '/probe_head_rows.json'})
open(GUARD, 'wb').write(subprocess.run(['git', '-C', C, 'show', B + ':' + GUARD_REL], capture_output=True).stdout)
print('  base bytes written; Promise.race count', open(GUARD).read().count('Promise.race'))
vitest('probe_base', ['src/__tests__/qa1004-drafter-probe.test.ts'], env={'QA1004_OUT': G + '/probe_base_rows.json'})
vitest('seat_base', [SEAT])
# 3. FIFO real-lookup probe: dist at base (built now), then head
fifo_dir = tempfile.mkdtemp(prefix='fifo_', dir=W)
run(['npx', 'tsc', '-p', '.'], cwd=SH)
for label in ('base',):
    fifo = fifo_dir + '/park_' + label; os.mkfifo(fifo)
    p = run(['node', G + '/fifo_probe.js', SH + '/dist/security/ssrf-guard.js', fifo, 'dist@' + label, '300'], env={'UV_THREADPOOL_SIZE': '1'}, timeout=60)
    print('  ', p.stdout.strip()[:1500], p.stderr[-500:]); open(G + '/fifo_probe_' + label + '.out', 'w').write(p.stdout + p.stderr)
restore()
run(['npx', 'tsc', '-p', '.'], cwd=SH)
print('  dist rebuilt at head; Promise.race in dist', open(SH + '/dist/security/ssrf-guard.js').read().count('Promise.race'))
for label in ('head',):
    fifo = fifo_dir + '/park_' + label; os.mkfifo(fifo)
    p = run(['node', G + '/fifo_probe.js', SH + '/dist/security/ssrf-guard.js', fifo, 'dist@' + label, '300'], env={'UV_THREADPOOL_SIZE': '1'}, timeout=60)
    print('  ', p.stdout.strip()[:1500], p.stderr[-500:]); open(G + '/fifo_probe_' + label + '.out', 'w').write(p.stdout + p.stderr)
# 4. tsc: the package program vs an including program
p = run(['npx', 'tsc', '--noEmit', '-p', '.', '--listFiles'], cwd=SH)
lst = p.stdout.splitlines(); print('  tsc -p packages/shared rc', p.returncode, 'files', len(lst), '__tests__ files in program', sum('__tests__' in x for x in lst))
open(SH + '/tsconfig.qa-incl.json', 'w').write(json.dumps({'extends': './tsconfig.json', 'compilerOptions': {'noEmit': True, 'types': ['node']},
    'include': [], 'files': ['src/__tests__/ks932-timeout-bounds-dns.test.ts', 'src/__tests__/ks914-shipped-path.test.ts']}))
p = run(['npx', 'tsc', '-p', 'tsconfig.qa-incl.json', '--listFiles'], cwd=SH)
errs = [x for x in p.stdout.splitlines() if 'error TS' in x]
print('  including program rc', p.returncode, 'errors', len(errs), 'ks932 in program', any('ks932-timeout' in x for x in p.stdout.splitlines()))
for x in errs: print('   ', x[:260])
open(G + '/tsc_including.out', 'w').write(p.stdout + p.stderr)
# 5. the seat file under a deterministic FAST RST and a deterministic SILENT hang; plus the seat's budget-unshared tamper under both
shutil.copyfile(G + '/qa-netredirect.setup.ts', SH + '/qa-netredirect.setup.ts'); shutil.copyfile(G + '/qa-netredirect.config.ts', SH + '/qa-netredirect.config.ts')
for mode in ('rst', 'silent'):
    vitest('seat_net_' + mode, [SEAT], ['--config', 'qa-netredirect.config.ts'], env={'QA1004_NET': mode})
s = open(GUARD).read(); anchor = '    }, remainingMs);\n'; assert s.count(anchor) == 1, s.count(anchor)
open(GUARD, 'w').write(s.replace(anchor, '    }, timeoutMs);\n')); assert open(GUARD).read().count('}, remainingMs);') == 0
print('  TAMPER budget-unshared written (anchor count 1 -> 0)')
for mode in ('rst', 'silent'):
    vitest('seat_unshared_net_' + mode, [SEAT], ['--config', 'qa-netredirect.config.ts'], env={'QA1004_NET': mode})
restore()
# 6. quarantine the probe + scratch config by rename; then the whole shared suite at head
for f in ('src/__tests__/qa1004-drafter-probe.test.ts', 'qa-netredirect.setup.ts', 'qa-netredirect.config.ts', 'tsconfig.qa-incl.json'):
    os.rename(SH + '/' + f, SH + '/' + f + '.quarantined')
vitest('shared_full_head', [])
