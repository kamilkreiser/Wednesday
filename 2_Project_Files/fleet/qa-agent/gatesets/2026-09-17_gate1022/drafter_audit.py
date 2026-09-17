#!/usr/bin/env python3
"""drafter_audit.py — #1022: the SHIPPED audit-gate.mjs + audit-locks.mjs on the drafter's own head and base worktrees.
 H1 head, real baseline (35)          expect gate rc 0 / locks rc 0, 0 CLEANUP
 H2 head, BASE's baseline (38) CONTROL expect gate rc 0 + the 3 hono ids under CLEANUP; locks rc 0 (locks CLEANUP lists only standalone-locks scope)
 B0 base, real baseline (38) CONTROL  expect rc 0 / rc 0
 B1 base, HEAD's baseline (35) NEG    expect gate rc 1 + locks rc 1 naming exactly the 3 hono ids
Then the advisory data the gates themselves use: hono `via` entries (url, range) from `npm audit --json` at base, and the bulk endpoint
audit-locks.mjs POSTs to (its own URL, BULK_ADVISORY_URL) for hono 4.13.0 + 4.13.8, judged with scripts/audit's own semver.
scripts/audit deps: `npm ci --ignore-scripts` in each worktree's scripts/audit (lock sha asserted). Baseline copies live in scratch."""
import datetime, hashlib, json, os, re, subprocess, sys
CL = open('/private/tmp/claude-501/drafter1022/CLONE_PATH').read().strip()
GS = os.path.dirname(os.path.abspath(__file__)); OUT = GS + '/out'; os.makedirs(OUT, exist_ok=True)
def now(): return datetime.datetime.now().astimezone().strftime('%H:%M:%S %Z')
HONO = ['GHSA-crvj-82cr-hjcx', 'GHSA-g6gw-c38x-mqfc', 'GHSA-gqvv-2mrq-wpjv']
for t in ('head', 'base'):
    d = CL + '/wt-%s/Blockchain/Dev/scripts/audit' % t
    s0 = hashlib.sha256(open(d + '/package-lock.json', 'rb').read()).hexdigest()[:16]
    p = subprocess.run(['npm', 'ci', '--ignore-scripts', '--no-audit', '--no-fund'], cwd=d, capture_output=True, text=True)
    print(t, 'scripts/audit npm ci rc', p.returncode, '| lock sha', s0, '->', hashlib.sha256(open(d + '/package-lock.json', 'rb').read()).hexdigest()[:16],
          '| semver present', os.path.exists(d + '/node_modules/semver/package.json'), '| root node_modules present (must be False)', os.path.exists(CL + '/wt-%s/Blockchain/Dev/node_modules' % t), now())
bl = {t: CL + '/wt-%s/Blockchain/Dev/scripts/audit/audit-baseline.json' % t for t in ('head', 'base')}
copies = {}
for t in ('head', 'base'):
    copies[t] = CL + '/baseline_%s_copy.json' % t
    open(copies[t], 'wb').write(open(bl[t], 'rb').read())
print('baseline copies sha256: head', hashlib.sha256(open(copies['head'], 'rb').read()).hexdigest()[:16], 'base', hashlib.sha256(open(copies['base'], 'rb').read()).hexdigest()[:16])
RUNS = [('H1', 'head', None), ('H2', 'head', copies['base']), ('B0', 'base', None), ('B1', 'base', copies['head'])]
for tag, t, blpath in RUNS:
    dev = CL + '/wt-%s/Blockchain/Dev' % t
    env = dict(os.environ); env.pop('AUDIT_BASELINE_PATH', None)
    if blpath: env['AUDIT_BASELINE_PATH'] = blpath
    for gate in ('audit-gate', 'audit-locks'):
        f = OUT + '/%s_%s.out' % (tag, gate)
        t0 = now(); p = subprocess.run(['node', 'scripts/audit/%s.mjs' % gate], cwd=dev, env=env, capture_output=True, text=True, timeout=400)
        open(f, 'w').write(p.stdout + '\n--stderr--\n' + p.stderr)
        text = p.stdout + p.stderr
        head_line = next((l for l in text.splitlines() if l.startswith(gate.replace('-', '-') + ':') or 'standalone lockfiles' in l), '')
        cleanup = text.split('CLEANUP', 1)[1] if 'CLEANUP' in text else ''
        cl_ids = sorted(set(re.findall(r'GHSA-[0-9a-z]{4}-[0-9a-z]{4}-[0-9a-z]{4}', cleanup.split('FAIL')[0])))
        fail = text.split('FAIL', 1)[1] if 'FAIL' in text else ''
        fail_ids = sorted(set(re.findall(r'GHSA-[0-9a-z]{4}-[0-9a-z]{4}-[0-9a-z]{4}', fail)))
        print('%s %s %s baseline=%s rc %d %s->%s | %s | CLEANUP ids %s | FAIL ids %s | hono lines: %s' % (
            tag, t, gate, 'override:' + os.path.basename(blpath) if blpath else 'real', p.returncode, t0, now(), head_line.strip()[:120],
            cl_ids, fail_ids, [l.strip()[:140] for l in text.splitlines() if 'hono' in l.lower()][:8]))
# the gates' own advisory data
dev = CL + '/wt-base/Blockchain/Dev'
p = subprocess.run(['npm', 'audit', '--json'], cwd=dev, capture_output=True, text=True, timeout=400)
rep = json.loads(p.stdout)
for name, v in rep.get('vulnerabilities', {}).items():
    if name != 'hono': continue
    print('npm audit (base root) hono: range', v.get('range'), '| fixAvailable', v.get('fixAvailable'), '| nodes', v.get('nodes'))
    for via in v.get('via', []):
        if isinstance(via, dict): print('   via', via.get('url', '').split('/')[-1], via.get('severity'), 'range', via.get('range'), '|', via.get('title'))
node = r'''
const semver = (await import(process.env.SEMVER)).default;
const res = await fetch('https://registry.npmjs.org/-/npm/v1/security/advisories/bulk', { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify({ hono: ['4.13.0', '4.13.8'] }) });
const j = await res.json();
for (const a of j.hono ?? []) {
  const id = String(a.url).split('/').pop();
  console.log(`bulk ${res.status} ${id} ${a.severity} vulnerable_versions=${JSON.stringify(a.vulnerable_versions)} 4.13.0:${semver.satisfies('4.13.0', a.vulnerable_versions, { includePrerelease: true })} 4.13.8:${semver.satisfies('4.13.8', a.vulnerable_versions, { includePrerelease: true })}`);
}
for (const [who, rng] of [['@modelcontextprotocol/sdk', '^4.11.4'], ['@prisma/dev', '^4.12.8'], ['@hono/node-server peer', '^4']])
  console.log(`declarer ${who} ${rng}: 4.13.8 inside=${semver.satisfies('4.13.8', rng)} | control 5.0.0 inside=${semver.satisfies('5.0.0', rng)}`);
console.log(`control: semver.satisfies('4.13.0','<4.13.8') = ${semver.satisfies('4.13.0', '<4.13.8')}`);
'''
sv = 'file://' + CL + '/wt-base/Blockchain/Dev/scripts/audit/node_modules/semver/index.js'
open(CL + '/bulk_probe.mjs', 'w').write(node)
p = subprocess.run(['node', CL + '/bulk_probe.mjs'], cwd=CL, env=dict(os.environ, SEMVER=sv), capture_output=True, text=True, timeout=120)
print(p.stdout, p.stderr[-600:])
os.rename(CL + '/bulk_probe.mjs', CL + '/bulk_probe.mjs.ran')
print('done', now())
