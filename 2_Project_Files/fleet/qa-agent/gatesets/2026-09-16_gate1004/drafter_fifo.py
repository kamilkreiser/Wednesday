#!/usr/bin/env python3
"""drafter_fifo.py — the FIFO real-lookup probe at dist@base and dist@head (second attempt; drafter_run2.out shows the first
attempt died on a SyntaxError the drafter introduced into fifo_probe.js — a load failure, not a measurement)."""
import hashlib, json, os, subprocess, tempfile, datetime
SCR = '/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/9aed5a67-2729-4892-b685-13ab87142a58/scratchpad'
G = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-16_gate1004'
P = json.load(open(SCR + '/gate1004_draft_paths.json')); C = P['C']; W = P['W']
H = '6d077d3fe35cd5f3c09d394553d320e97b1abe32'; B = '5b4f38a48aeb40c2295895aaa5cd08e273aa7a08'
SH = C + '/Blockchain/Dev/packages/shared'; REL = 'Blockchain/Dev/packages/shared/src/security/ssrf-guard.ts'; GUARD = C + '/' + REL
now = lambda: datetime.datetime.now().astimezone().strftime('%H:%M:%S')
sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()
def run(cmd, cwd=SH, env=None, timeout=120):
    e = dict(os.environ); e.update(env or {}); p = subprocess.run(cmd, cwd=cwd, env=e, capture_output=True, text=True, timeout=timeout)
    print(now(), 'rc', p.returncode, ' '.join(cmd)[:120]); return p
d = tempfile.mkdtemp(prefix='fifo2_', dir=W)
for label, ref in (('base', B), ('head', H)):
    open(GUARD, 'wb').write(subprocess.run(['git', '-C', C, 'show', ref + ':' + REL], capture_output=True).stdout)
    run(['npx', 'tsc', '-p', '.'])
    print('  dist@%s Promise.race count %d' % (label, open(SH + '/dist/security/ssrf-guard.js').read().count('Promise.race')))
    for tms in ('300',):
        fifo = d + '/park_%s_%s' % (label, tms); os.mkfifo(fifo); out = G + '/fifo_probe_%s.json' % label
        p = run(['node', G + '/fifo_probe.js', SH + '/dist/security/ssrf-guard.js', fifo, 'dist@' + label, tms], env={'UV_THREADPOOL_SIZE': '1', 'QA1004_FIFO_OUT': out})
        print('  rc', p.returncode, '(-9 = self-SIGKILL after writing)', open(out).read() if os.path.exists(out) else 'NO OUTPUT ' + p.stderr[-600:])
run(['git', '-C', C, 'checkout', H, '--', REL], cwd=C); print('  restored sha256', sha(GUARD)[:16], sha(GUARD).startswith('b546fc02578c8b1f'))
run(['npx', 'tsc', '-p', '.']); print('  dist back at head, Promise.race', open(SH + '/dist/security/ssrf-guard.js').read().count('Promise.race'))
