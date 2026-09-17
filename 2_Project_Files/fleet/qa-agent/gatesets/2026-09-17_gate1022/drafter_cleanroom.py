#!/usr/bin/env python3
"""drafter_cleanroom.py — #1022: the shipped scripts/preflight/lockfile-cleanroom.sh on services/originate + services/mcp-server in the
drafter's head and base worktrees (host node 24 path: `npm ci --dry-run`, no write). CONTROL that can fail: at head, mcp-server package.json
zod "^3.24.0" -> "^9.0.0" (anchor count 1), run, restore sha256-identical."""
import datetime, hashlib, os, subprocess
CL = open('/private/tmp/claude-501/drafter1022/CLONE_PATH').read().strip()
GS = os.path.dirname(os.path.abspath(__file__)); OUT = GS + '/out'; os.makedirs(OUT, exist_ok=True)
def now(): return datetime.datetime.now().astimezone().strftime('%H:%M:%S %Z')
def sha(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]
def run(t, tag):
    dev = CL + '/wt-%s/Blockchain/Dev' % t
    t0 = now(); p = subprocess.run(['bash', 'scripts/preflight/lockfile-cleanroom.sh', 'services/originate', 'services/mcp-server'], cwd=dev, capture_output=True, text=True, timeout=500)
    open(OUT + '/cleanroom_%s.out' % tag, 'w').write(p.stdout + '\n--stderr--\n' + p.stderr)
    lines = [l for l in (p.stdout + p.stderr).splitlines() if l.strip()]
    print('%s %s rc %d %s->%s | %s' % (tag, t, p.returncode, t0, now(), ' || '.join(l.strip()[:110] for l in lines[-6:])))
    print('   git porcelain', len(subprocess.run(['git', '-C', dev, 'status', '--porcelain'], capture_output=True, text=True).stdout.splitlines()))
run('head', 'head')
run('base', 'base')
pj = CL + '/wt-head/Blockchain/Dev/services/mcp-server/package.json'
s0 = sha(pj); txt = open(pj).read(); anchor = '"zod": "^3.24.0"'
assert txt.count(anchor) == 1, 'anchor count %d' % txt.count(anchor)
open(pj, 'w').write(txt.replace(anchor, '"zod": "^9.0.0"'))
print('CONTROL tamper applied, sha', s0, '->', sha(pj))
try:
    run('head', 'control_zod9')
finally:
    open(pj, 'w').write(txt)
    print('CONTROL restored sha', sha(pj), 'identical', sha(pj) == s0)
print('done', now())
